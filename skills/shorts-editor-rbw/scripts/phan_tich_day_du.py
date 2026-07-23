# -*- coding: utf-8 -*-
"""GOP 3 BUOC PHAN TICH MIEN PHI thanh 1 lenh — them 23/07/2026 (Sep Huy yeu cau,
dung y "1 lan goi thay vi 3 lan qua lai" trong bao giao nang cap toi 22-23/07).

Chay noi tiep DUNG THU TU da chot trong SKILL.md ("Thu tu dung cua ca 4 buoc"):
    1. analyze_footage.py   — bat diem doi canh, ghep anh luoi, nghe thoai (Whisper + VAD)
    2. do_ky_thuat.py       — cham do net/chuyen dong TUNG clip (mien phi, 100% clip)
    3. loc_thoai_that.py    — tim moc cat CHINH XAC cho clip co thoai (mien phi)

KHONG gom quet_mat_ai.py (mat AI Gemini) — buoc do TON TIEN THAT + gui clip len
cloud, theo dung luat SKILL.md phai HOI NGUOI DUNG truoc, khong duoc tu chay.
Chay rieng sau khi nguoi dung dong y (xem SKILL.md Buoc 2c).

Sau khi ca 3 buoc xong, doc lai index.json va in 1 BAO CAO TONG (thay vi phai
tu doc 3 log rieng): so clip theo tung co canh bao, so clip da co moc cat thoai,
danh sach clip dang chu y nhat.

Usage:
    python phan_tich_day_du.py "<folder-source>" "<workspace>\\analysis"
    python phan_tich_day_du.py "<folder-source>" "<workspace>\\analysis" --force --khung 8

Cac co chuyen tiep dung cho tung buoc con (tuy chon):
    --max-frames N   (analyze_footage: so khung/anh luoi, mac dinh 10)
    --no-whisper     (analyze_footage: bo qua nghe thoai)
    --force          (analyze_footage: phan tich lai ca clip da co)
    --khung N        (do_ky_thuat: so khung do net/clip, mac dinh 6)
    --lam-lai        (do_ky_thuat: do lai ca clip da co ket qua)
    --limit N        (loc_thoai_that: gioi han so clip xu ly, 0 = het)
"""
import argparse
import json
import os
import subprocess
import sys
import time

SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def chay_buoc(nhan, cmd):
    print("\n" + "=" * 72)
    print("BUOC: %s" % nhan)
    print("=" * 72)
    t0 = time.time()
    r = subprocess.run([sys.executable] + cmd)
    dt = time.time() - t0
    if r.returncode != 0:
        sys.exit("\n!!! BUOC '%s' LOI (exit %d) — dung lai, sua roi chay lai lenh nay"
                 " (cac buoc truoc da lam se tu bo qua nho co --force/--lam-lai chi khi can).\n"
                 % (nhan, r.returncode))
    print("-> Xong '%s' sau %.0fs" % (nhan, dt))


def bao_cao_tong(index_path, src):
    if not os.path.exists(index_path):
        print("\n[!] Khong thay index.json de tong hop bao cao: %s" % index_path)
        return
    idx = json.load(open(index_path, encoding="utf-8"))
    clips = list(idx.get("clips", {}).values())
    tong = len(clips)

    def dem_canh_bao(co):
        return sum(1 for c in clips if co in ((c.get("do_ky_thuat") or {}).get("canh_bao") or []))

    co_thoai = [c for c in clips if c.get("has_speech")]
    chua_nghe = [c for c in clips if c.get("has_speech") is None and c.get("has_audio")]
    da_loc_thoai = [c for c in clips if c.get("loc_thoai") and c["loc_thoai"].get("doan")]
    co_doan_dung = sum(1 for c in da_loc_thoai
                       if any(d.get("gan_mic") and not d.get("nghi_e_kip")
                              for d in c["loc_thoai"]["doan"]))
    canh_bao_cheo = []
    for c in da_loc_thoai:
        for w in (c["loc_thoai"].get("canh_bao") or []):
            canh_bao_cheo.append("%s: %s" % (c.get("file", "?"), w))

    print("\n" + "#" * 72)
    print("BAO CAO TONG — %s" % src)
    print("#" * 72)
    print("Tong so clip trong index:        %d" % tong)
    print("  Co thoai (has_speech=True):    %d" % len(co_thoai))
    if chua_nghe:
        print("  CHUA NGHE DUOC thoai:          %d (thieu model/loi luc chay — chay lai analyze_footage.py sau)" % len(chua_nghe))
    print("  Da lay duoc moc cat (loc_thoai_that): %d/%d clip co thoai (%d clip co doan DUNG DUOC)"
          % (len(da_loc_thoai), len(co_thoai), co_doan_dung))
    print()
    print("Do ky thuat (%d clip da do):" % sum(1 for c in clips if c.get("do_ky_thuat")))
    print("  mo (bo)            : %d" % dem_canh_bao("mo"))
    print("  hoi-mo (xem lai)   : %d" % dem_canh_bao("hoi-mo"))
    print("  net-tung-doan      : %d" % dem_canh_bao("net-tung-doan"))
    print("  canh-tinh          : %d" % dem_canh_bao("canh-tinh"))
    if canh_bao_cheo:
        print("\nCANH BAO DOI CHIEU (loc_thoai_that x Gemini, %d):" % len(canh_bao_cheo))
        for w in canh_bao_cheo[:15]:
            print("  ⚠ %s" % w)
        if len(canh_bao_cheo) > 15:
            print("  ... con %d canh bao nua, xem truc tiep trong index.json" % (len(canh_bao_cheo) - 15))

    dung_tot = [c for c in clips if c.get("do_ky_thuat")
                and "mo" not in (c["do_ky_thuat"].get("canh_bao") or [])
                and c.get("do_ky_thuat", {}).get("do_net_hang", 0) >= 0.7]
    print("\nGOI Y: %d clip xep hang do net cao (>=0.7) VA khong bi 'mo' — uu tien mo anh luoi nhom nay truoc."
          % len(dung_tot))
    print("\nBuoc tiep theo (KHONG tu chay — can hoi nguoi dung truoc, ton tien):")
    print("  python quet_mat_ai.py --src \"%s\" --index \"%s\" --limit 10" % (src, index_path))
    print("#" * 72)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src", help="folder chua footage buoi quay")
    ap.add_argument("dst", help="thu muc analysis (se chua index.json, sheets/...)")
    ap.add_argument("--max-frames", type=int, default=10)
    ap.add_argument("--no-whisper", action="store_true")
    ap.add_argument("--force", action="store_true", help="phan tich lai ca clip da co (analyze_footage)")
    ap.add_argument("--khung", type=int, default=6)
    ap.add_argument("--lam-lai", action="store_true", help="do lai ca clip da co ket qua (do_ky_thuat)")
    ap.add_argument("--limit", type=int, default=0)
    a = ap.parse_args()

    index_path = os.path.join(a.dst, "index.json")
    t_bat_dau = time.time()

    cmd1 = [os.path.join(SCRIPTS_DIR, "analyze_footage.py"), a.src, a.dst,
            "--max-frames", str(a.max_frames)]
    if a.no_whisper:
        cmd1.append("--no-whisper")
    if a.force:
        cmd1.append("--force")
    chay_buoc("1/3 analyze_footage.py (doi canh + nghe thoai)", cmd1)

    cmd2 = [os.path.join(SCRIPTS_DIR, "do_ky_thuat.py"), "--src", a.src,
            "--index", index_path, "--khung", str(a.khung)]
    if a.lam_lai:
        cmd2.append("--lam-lai")
    chay_buoc("2/3 do_ky_thuat.py (do net + chuyen dong)", cmd2)

    cmd3 = [os.path.join(SCRIPTS_DIR, "loc_thoai_that.py"), "--index", index_path, "--folder", a.src]
    if a.limit:
        cmd3 += ["--limit", str(a.limit)]
    chay_buoc("3/3 loc_thoai_that.py (moc cat thoai that)", cmd3)

    print("\nCA 3 BUOC XONG sau %.0f phut." % ((time.time() - t_bat_dau) / 60))
    bao_cao_tong(index_path, a.src)


if __name__ == "__main__":
    main()

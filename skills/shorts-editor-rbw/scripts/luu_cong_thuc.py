# -*- coding: utf-8 -*-
"""Luu "cong thuc dung" cua 1 video thanh pham — GIAI QUYET dung noi buc nhat cua
Sep Huy (chot dem 22-23/07/2026): "chi can dung vao 1 cho KHONG lien quan la ket
qua tut ve nhu video dau tien" — vi truoc gio moi lenh ffmpeg go roi trong phien
chat, khong luu lai duoc. Sua 1 loi cu the sau khi giao phai do nguoc bang cach
trich anh hang loat + doi chieu timestamp thu cong (da xay ra that 19/07/2026).

Luat da co tu 19/07/2026 (SKILL.md Buoc 4, muc 8) nhung chi la VAN XUOI — de
Claude "nho" tu viet, nen ap dung khong deu. Script nay bien no thanh 1 LENH CU
THE de kiem tra duoc: co goi hay khong goi la biet ngay (kiem_cai_dat.py doi
chieu duoc), khong con phu thuoc tri nho phien chat.

CACH DUNG — ngay SAU KHI dung xong 1 video (Buoc 4 SKILL.md), Claude tu ghep 1
file JSON tho theo dung khung duoi day roi goi:

    python luu_cong_thuc.py --ghi "<workspace>\\cong-thuc\\video-1.json" \\
        --tu-du-lieu "<file JSON tho vua ghep>"

Script se: kiem cac truong bat buoc, LUU BAN CHUAN vao dung --ghi, VA tu sinh
kem 1 file .ps1 cung ten — moi lenh ffmpeg thanh 1 khoi co nhan chu thich, de
Sep/Claude mo ra, sua dung 1 tham so (doi nhac, sua 1 cau chu...) roi chay lai
DUNG khoi do, khong phai dung lai tu dau.

KHUNG JSON THO (Claude tu dien sau khi dung xong, luu thanh file tam roi tro
--tu-du-lieu vao do):
{
  "video": "video-1-hook-abc.mp4",          // ten file thanh pham
  "kieu_dung": "Kieu 2",                     // Kieu 1 | Kieu 2 | Kieu 3
  "canh": [                                  // DANH SACH CANH DA DUNG — cot loi
    {"nhan": "Canh 1 - hook", "clip": "0043.MP4", "t0": 4.2, "t1": 9.8,
     "am_thanh": "goc"}                      // "goc" = tieng dung clip nay tai
  ],                                         // dung moc; khac "goc" (vd "voice",
                                              // "nhac", "clip-khac") = B-roll cau
                                              // am thanh tu nguon khac — DE cho
                                              // kiem_cai_dat.py doi chieu luat MC gia
  "lenh_ffmpeg": [                           // TOAN BO lenh ffmpeg da chay, DUNG THU TU
    {"nhan": "1. Cat + chuan hoa canh 1", "lenh": ["ffmpeg", "-y", "-ss", "4.2", "..."]}
  ],
  "nhac": {"file": "...", "muc": 0.2},       // tuy chon
  "sfx": [{"file": "...", "offset": 12.3}],  // tuy chon
  "mix_cuoi": {"lufs_do_duoc": -13.9},       // tuy chon, ghi lai ket qua nghiem thu
  "logo_outro": true,
  "output": "<folder>\\Final\\video-1-...mp4"
}

KIEM LAI (truoc khi giao hang, hoac khi nghi ngo cong thuc da cu):
    python luu_cong_thuc.py --kiem "<workspace>\\cong-thuc\\video-1.json"
"""
import argparse
import datetime
import json
import os
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

BAT_BUOC = ["video", "canh", "lenh_ffmpeg", "output"]


def _ps1_quote(s):
    """Bao 1 tham so ffmpeg thanh dang an toan de dan vao PowerShell."""
    s = str(s)
    if s == "" or any(c in s for c in ' \t"$`'):
        return '"%s"' % s.replace('`', '``').replace('"', '`"').replace('$', '`$')
    return s


def sinh_ps1(cong_thuc):
    dong = [
        "# Cong thuc dung: %s" % cong_thuc.get("video", "?"),
        "# Sinh tu dong boi luu_cong_thuc.py — %s" % datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
        "# Sua 1 tham so trong DUNG 1 khoi ben duoi roi chay lai KHOI DO (bam chon + F8 trong VSCode/PowerShell ISE),",
        "# khong nhat thiet phai chay lai ca file.",
        "",
    ]
    for i, buoc in enumerate(cong_thuc.get("lenh_ffmpeg", []), 1):
        nhan = buoc.get("nhan", "Buoc %d" % i)
        lenh = buoc.get("lenh", [])
        dong.append("# ---- %s ----" % nhan)
        dong.append(" ".join(_ps1_quote(x) for x in lenh))
        dong.append("")
    dong.append("# ---- Output ----")
    dong.append("# %s" % cong_thuc.get("output", "?"))
    return "\n".join(dong)


def ghi(a):
    if not os.path.exists(a.tu_du_lieu):
        sys.exit("\n!!! Khong thay file du lieu tho: %s\n"
                 "    Doc docstring dau file nay de biet khung JSON can ghep.\n" % a.tu_du_lieu)
    cong_thuc = json.load(open(a.tu_du_lieu, encoding="utf-8"))

    thieu = [k for k in BAT_BUOC if not cong_thuc.get(k)]
    if thieu:
        sys.exit("\n!!! CONG THUC THIEU TRUONG BAT BUOC: %s\n"
                 "    Xem khung JSON trong docstring dau file luu_cong_thuc.py.\n" % ", ".join(thieu))
    if not isinstance(cong_thuc.get("canh"), list) or not cong_thuc["canh"]:
        sys.exit("\n!!! Truong 'canh' phai la danh sach KHONG RONG (danh sach canh da dung).\n")
    for i, c in enumerate(cong_thuc["canh"]):
        for k in ("clip", "t0", "t1"):
            if k not in c:
                sys.exit("\n!!! canh[%d] thieu truong '%s': %s\n" % (i, k, c))

    cong_thuc.setdefault("luc_dung", datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))

    os.makedirs(os.path.dirname(os.path.abspath(a.ghi)), exist_ok=True)
    json.dump(cong_thuc, open(a.ghi, "w", encoding="utf-8"), ensure_ascii=False, indent=2)

    ps1_path = os.path.splitext(a.ghi)[0] + ".ps1"
    open(ps1_path, "w", encoding="utf-8-sig").write(sinh_ps1(cong_thuc))

    print("Da luu cong thuc dung -> %s" % a.ghi)
    print("Da sinh script chay lai duoc -> %s" % ps1_path)
    print("   %d canh, %d lenh ffmpeg" % (len(cong_thuc["canh"]), len(cong_thuc["lenh_ffmpeg"])))
    mc_gia = [c for c in cong_thuc["canh"] if (c.get("am_thanh") or "goc") != "goc"]
    if mc_gia:
        print("   %d canh dung am thanh KHAC nguon goc (B-roll) — kiem_cai_dat.py se doi chieu"
              " voi co 'co_nguoi_dang_noi' cua mat AI de bat MC gia neu co." % len(mc_gia))


def kiem(a):
    if not os.path.exists(a.kiem):
        sys.exit("\n!!! KHONG THAY FILE CONG THUC: %s\n"
                 "    Dang le phai ghi ngay sau khi dung xong video (SKILL.md Buoc 4, muc 8).\n" % a.kiem)
    cong_thuc = json.load(open(a.kiem, encoding="utf-8"))
    loi, canh_bao = [], []

    out = cong_thuc.get("output", "")
    if out and not os.path.exists(out):
        canh_bao.append("Output ghi trong cong thuc khong con ton tai: %s (video da bi xoa/di chuyen?)" % out)

    for i, c in enumerate(cong_thuc.get("canh", [])):
        clip = c.get("clip", "")
        if clip and not any(clip in (buoc.get("nhan", "") + " ".join(str(x) for x in buoc.get("lenh", [])))
                            for buoc in cong_thuc.get("lenh_ffmpeg", [])):
            canh_bao.append("canh[%d] (%s) khong thay xuat hien trong danh sach lenh_ffmpeg — "
                            "co the ghi thieu khi luu." % (i, clip))

    print("=" * 72)
    print("KIEM CONG THUC DUNG — %s" % cong_thuc.get("video", a.kiem))
    print("=" * 72)
    print("  So canh:          %d" % len(cong_thuc.get("canh", [])))
    print("  So lenh ffmpeg:   %d" % len(cong_thuc.get("lenh_ffmpeg", [])))
    print("  Luc dung:         %s" % cong_thuc.get("luc_dung", "khong ro"))
    if canh_bao:
        print("\nCanh bao (%d):" % len(canh_bao))
        for x in canh_bao:
            print("   - %s" % x)
    if not loi and not canh_bao:
        print("\nOK — cong thuc con nguyen ven, dung tham chieu duoc.")
    print("=" * 72)
    sys.exit(1 if loi else 0)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ghi", help="duong dan file cong thuc (.json) can GHI")
    ap.add_argument("--tu-du-lieu", help="file JSON tho (theo khung trong docstring) de doc va chuan hoa")
    ap.add_argument("--kiem", help="duong dan file cong thuc (.json) can DOI CHIEU lai")
    a = ap.parse_args()

    if a.ghi:
        if not a.tu_du_lieu:
            sys.exit("Thieu --tu-du-lieu (file JSON tho de doc).")
        return ghi(a)
    if a.kiem:
        return kiem(a)
    ap.print_help()


if __name__ == "__main__":
    main()

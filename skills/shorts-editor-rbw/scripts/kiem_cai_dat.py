# -*- coding: utf-8 -*-
"""Kiem video thanh pham co DUNG nhung gi nguoi dung da chon khong.

VI SAO CAN (Sep Huy yeu cau 22/07/2026: "dac biet la phan chac chan cac cai dat
nen cua nguoi dung sau duoc thuc hien"):
    Luong hoi dai (huong dung -> so luong -> nhac -> giong -> muc phu -> kenh dang),
    den luc dung thi rat de quen mot lua chon. Vd nguoi dung chon "kenh ca nhan"
    (bo logo + outro) nhung luc dung van chen logo — KHONG CO GI BAT DUOC, tan
    khi ho xem video moi phat hien.
    Script nay doi chieu video that voi file cai dat, bao DAT/SAI tung muc.

CACH DUNG:
    # 1. Ngay sau khi hoi xong, ghi lua chon ra file:
    python kiem_cai_dat.py --ghi "<Workspace>/cai-dat-nguoi-dung.json" \
        --kenh ca-nhan --so-video 2 --nhac trend --giong "Thanh Ngoc" \
        --huong voice-over --muc-phu "dan dau"

    # 2. Truoc khi giao hang, kiem lai:
    python kiem_cai_dat.py --kiem "<Workspace>/cai-dat-nguoi-dung.json" \
        --final "<folder Final>"

TU DONG DO DUOC: so luong video · do phan giai · fps · thoi luong · LUFS ·
                 co outro khong · co logo overlay khong
PHAI KIEM BANG TAI/MAT: giong doc dung nguoi chua · nhac dung bai chua ·
                        muc phu giong · noi dung bam mo ta nguoi dung
(script se LIET KE ro phan nay chu khong im lang bo qua)
"""
import argparse
import json
import os
import subprocess
import sys

try:
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from chung_ffmpeg import nap_ffmpeg
    nap_ffmpeg()
except ImportError:
    pass

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

CHUAN = {"rong": 1080, "cao": 1920, "fps": 30, "lufs_min": -15.0, "lufs_max": -13.0}


def chay(cmd, timeout=600):
    return subprocess.run(cmd, capture_output=True, text=True,
                          encoding="utf-8", errors="replace", timeout=timeout)


def do_video(path):
    """Tra ve dict thong so video, hoac None neu doc khong duoc."""
    r = chay(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
              "stream=width,height,r_frame_rate:format=duration", "-of", "json", path])
    if r.returncode != 0:
        return None
    try:
        d = json.loads(r.stdout)
        st = d["streams"][0]
        num, den = st["r_frame_rate"].split("/")
        return {"rong": int(st["width"]), "cao": int(st["height"]),
                "fps": round(float(num) / float(den), 2),
                "dai": round(float(d["format"]["duration"]), 2)}
    except Exception:
        return None


def do_lufs(path):
    r = chay(["ffmpeg", "-i", path, "-af", "loudnorm=print_format=summary",
              "-f", "null", "-"], timeout=900)
    for line in (r.stderr or "").splitlines():
        if "Input Integrated" in line:
            try:
                return float(line.split(":")[1].strip().split()[0])
            except Exception:
                return None
    return None


def co_logo_overlay(path, dai):
    """Do xem co logo overlay tinh o vung GIUA-TREN khong.

    Cach do: lay 5 khung rai deu trong phan than video, cat rieng vung logo
    (giua ngang, ~8-16% chieu cao), so cac khung voi nhau. Logo overlay la anh
    TINH de len moi khung -> vung do gan nhu khong doi giua cac khung, trong khi
    canh quay thi doi lien tuc.

    Tra ve: True (co) / False (khong) / None (khong do duoc)."""
    try:
        import cv2
        import numpy as np
    except ImportError:
        return None
    cap = cv2.VideoCapture(path)
    if not cap.isOpened():
        return None
    khung = []
    # bo 15% dau va 25% cuoi (tranh hook va outro) roi lay 5 moc
    for i in range(5):
        t = dai * (0.15 + 0.60 * i / 4.0)
        cap.set(cv2.CAP_PROP_POS_MSEC, t * 1000)
        ok, f = cap.read()
        if not ok:
            continue
        h, w = f.shape[:2]
        vung = f[int(h * 0.08):int(h * 0.16), int(w * 0.30):int(w * 0.70)]
        khung.append(cv2.cvtColor(vung, cv2.COLOR_BGR2GRAY).astype("float32"))
    cap.release()
    if len(khung) < 3:
        return None
    # do lech trung binh giua cac khung o vung logo
    lech = [float(np.mean(np.abs(khung[i] - khung[i + 1]))) for i in range(len(khung) - 1)]
    tb = sum(lech) / len(lech)
    # vung logo tinh -> lech rat nho. Canh quay doi -> lech lon.
    return tb < 6.0


def co_outro(path, dai, file_outro):
    """So khung gan cuoi video voi khung giua file outro (so bang histogram mau)."""
    if not file_outro or not os.path.exists(file_outro):
        return None
    try:
        import cv2
    except ImportError:
        return None

    def lay_khung(p, giay):
        cap = cv2.VideoCapture(p)
        if not cap.isOpened():
            return None
        cap.set(cv2.CAP_PROP_POS_MSEC, giay * 1000)
        ok, f = cap.read()
        cap.release()
        return f if ok else None

    do = do_video(file_outro)
    if not do:
        return None
    a = lay_khung(path, max(0.0, dai - do["dai"] / 2.0))   # giua doan outro trong video
    b = lay_khung(file_outro, do["dai"] / 2.0)             # giua file outro goc
    if a is None or b is None:
        return None
    ha = cv2.calcHist([a], [0, 1, 2], None, [8, 8, 8], [0, 256] * 3)
    hb = cv2.calcHist([b], [0, 1, 2], None, [8, 8, 8], [0, 256] * 3)
    cv2.normalize(ha, ha); cv2.normalize(hb, hb)
    return float(cv2.compareHist(ha, hb, cv2.HISTCMP_CORREL)) > 0.75


def ghi_cai_dat(a):
    cai = {k: v for k, v in {
        "huong_dung": a.huong, "so_video": a.so_video, "kenh_dang": a.kenh,
        "nhac": a.nhac, "giong": a.giong, "muc_phu": a.muc_phu,
        "mo_ta_nguoi_dung": a.mo_ta, "cach_lam": a.cach_lam,
    }.items() if v not in (None, "")}
    os.makedirs(os.path.dirname(os.path.abspath(a.ghi)), exist_ok=True)
    json.dump(cai, open(a.ghi, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print("Da ghi cai dat nguoi dung -> %s" % a.ghi)
    for k, v in cai.items():
        print("   %-18s %s" % (k, v))
    print("\n=> TRUOC KHI GIAO HANG nho chay lai voi --kiem de doi chieu.")


def kiem(a):
    if not os.path.exists(a.kiem):
        sys.exit("\n!!! KHONG THAY FILE CAI DAT: %s\n"
                 "    Dang le phai ghi file nay NGAY SAU khi hoi xong nguoi dung.\n"
                 "    Xem SKILL.md muc 'cai dat nguoi dung'.\n" % a.kiem)
    cai = json.load(open(a.kiem, encoding="utf-8"))
    vids = []
    if os.path.isdir(a.final):
        for f in sorted(os.listdir(a.final)):
            if f.lower().endswith((".mp4", ".mov")):
                vids.append(os.path.join(a.final, f))
    elif os.path.exists(a.final):
        vids = [a.final]
    if not vids:
        sys.exit("\n!!! KHONG THAY VIDEO NAO trong: %s\n" % a.final)

    print("=" * 72)
    print("KIEM CAI DAT NGUOI DUNG — %d video" % len(vids))
    print("=" * 72)
    loi, canh_bao = [], []

    # --- so luong ---
    muon = cai.get("so_video")
    if muon:
        try:
            muon = int(muon)
            if len(vids) != muon:
                loi.append("So luong video: nguoi dung chon %d, thuc te xuat %d" % (muon, len(vids)))
            else:
                print("  So luong video       DAT (%d)" % len(vids))
        except ValueError:
            pass

    kenh = (cai.get("kenh_dang") or "").lower()
    for v in vids:
        ten = os.path.basename(v)
        d = do_video(v)
        if not d:
            loi.append("%s: khong doc duoc file" % ten)
            continue
        print("\n--- %s" % ten)
        # --- khung hinh ---
        if (d["rong"], d["cao"]) == (CHUAN["rong"], CHUAN["cao"]):
            print("  Khung hinh 1080x1920 DAT")
        else:
            loi.append("%s: khung hinh %dx%d, chuan la 1080x1920" % (ten, d["rong"], d["cao"]))
        if abs(d["fps"] - CHUAN["fps"]) > 1:
            canh_bao.append("%s: fps %.1f (chuan 30)" % (ten, d["fps"]))
        print("  Thoi luong           %.1fs" % d["dai"])
        # --- am luong ---
        lufs = do_lufs(v)
        if lufs is None:
            canh_bao.append("%s: khong do duoc LUFS" % ten)
        elif CHUAN["lufs_min"] <= lufs <= CHUAN["lufs_max"]:
            print("  Am luong %.1f LUFS   DAT" % lufs)
        else:
            loi.append("%s: am luong %.1f LUFS, chuan -14 (+-1)" % (ten, lufs))
        # --- logo + outro theo kenh dang ---
        if kenh:
            logo = co_logo_overlay(v, d["dai"])
            outro = co_outro(v, d["dai"], a.file_outro)
            if "ca-nhan" in kenh or "ca nhan" in kenh:
                if logo is True:
                    loi.append("%s: chon KENH CA NHAN nhung VAN CO logo overlay" % ten)
                elif logo is False:
                    print("  Khong logo           DAT (dung kenh ca nhan)")
                if outro is True:
                    loi.append("%s: chon KENH CA NHAN nhung VAN CO outro" % ten)
                elif outro is False:
                    print("  Khong outro          DAT (dung kenh ca nhan)")
            elif "page" in kenh or "cong ty" in kenh:
                if logo is False:
                    loi.append("%s: chon PAGE CONG TY nhung THIEU logo" % ten)
                elif logo is True:
                    print("  Co logo              DAT (dung page cong ty)")
                if outro is False:
                    loi.append("%s: chon PAGE CONG TY nhung THIEU outro" % ten)
                elif outro is True:
                    print("  Co outro             DAT (dung page cong ty)")
            if logo is None:
                canh_bao.append("%s: khong do duoc logo (thieu cv2?)" % ten)

    # --- phan may KHONG do duoc ---
    print("\n" + "=" * 72)
    print("MAY KHONG DO DUOC — PHAI TU KIEM BANG TAI/MAT:")
    if cai.get("giong"):
        print("  [ ] Giong doc dung '%s' chua" % cai["giong"])
    if cai.get("nhac"):
        print("  [ ] Nhac dung loai '%s' chua" % cai["nhac"])
    if cai.get("muc_phu"):
        print("  [ ] Muc phu giong dung '%s' chua" % cai["muc_phu"])
    if cai.get("mo_ta_nguoi_dung"):
        print("  [ ] Noi dung co bam mo ta nguoi dung khong:")
        print("      \"%s\"" % str(cai["mo_ta_nguoi_dung"])[:200])
    print("  [ ] Khong lap canh trong 1 video, va giua cac video cung lenh")

    print("\n" + "=" * 72)
    if loi:
        print("SAI %d MUC — PHAI SUA TRUOC KHI GIAO:" % len(loi))
        for x in loi:
            print("   - %s" % x)
    else:
        print("MOI MUC DO DUOC BANG MAY: DAT")
    if canh_bao:
        print("\nCanh bao (%d):" % len(canh_bao))
        for x in canh_bao:
            print("   - %s" % x)
    print("=" * 72)
    sys.exit(1 if loi else 0)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ghi", help="duong dan file cai dat de GHI")
    ap.add_argument("--kiem", help="duong dan file cai dat de DOI CHIEU")
    ap.add_argument("--final", help="file video hoac folder Final can kiem")
    ap.add_argument("--file-outro", help="duong dan file outro goc (de so khop)")
    ap.add_argument("--huong", help="text+nhac | voice-over | mc-dan")
    ap.add_argument("--so-video", help="so luong video")
    ap.add_argument("--kenh", help="ca-nhan | page-cong-ty | ca-hai")
    ap.add_argument("--nhac", help="trend | khong-ban-quyen | elevenlabs | tieng-goc | khong")
    ap.add_argument("--giong", help="ten giong doc")
    ap.add_argument("--muc-phu", help="dan dau | full | nhac ca bai")
    ap.add_argument("--cach-lam", help="lam-luon | trao-doi-tiep")
    ap.add_argument("--mo-ta", help="nguyen van cau mo cua nguoi dung")
    a = ap.parse_args()

    if a.ghi:
        return ghi_cai_dat(a)
    if a.kiem:
        if not a.final:
            sys.exit("Thieu --final (file video hoac folder Final can kiem).")
        return kiem(a)
    ap.print_help()


if __name__ == "__main__":
    main()

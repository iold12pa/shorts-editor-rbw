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
        --final "<folder Final>" \
        --cong-thuc "<Workspace>/cong-thuc/video-1.json" --index "<Workspace>/analysis/index.json"

TU DONG DO DUOC: so luong video · do phan giai · fps · thoi luong · LUFS ·
                 co outro khong · co logo overlay khong · vung an toan chu
                 (khong vuong UI TikTok/Reels) · luat cam canh MC gia (them
                 23/07/2026 — CAN --cong-thuc + --index, xem luu_cong_thuc.py) ·
                 luat "Kieu 2 khong duoc giu nguyen cu may dai ~3s/canh" (them
                 23/07/2026 sau khi Sep Huy bat canh hanh lang 12.1s trong
                 video-3 Ba Na Hills — CAN --cong-thuc, --index de loai tru
                 dung canh MC dang noi dong bo, xem kiem_canh_qua_dai())
PHAI KIEM BANG TAI/MAT: giong doc dung nguoi chua · nhac dung bai chua ·
                        muc phu giong · noi dung bam mo ta nguoi dung
(script se LIET KE ro phan nay chu khong im lang bo qua)
"""
import argparse
import json
import os
import re
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


def kiem_vung_an_toan_chu(path, dai):
    """Kiem chu dot (burn-in) co roi vao vung UI TikTok/Reels hay che khong
    (them 23/07/2026, Gemini de xuat trong dot ra soat 22-23/07).

    UI TikTok/Reels thuong che ~15% tren cung (thanh trang thai/caption ngan)
    va ~20% duoi cung (nut tuong tac, ten kenh, caption dai). Do bang canh: chu
    burn-in luon co VIEN DEN dam + chu TRANG/VANG sang -> mat do canh (Canny
    edge) trong vung do cao gap nhieu lan vung khong chu. Khong phai OCR — chi
    la phep do THO de canh bao, khong thay the mat nguoi soi truoc khi giao."""
    try:
        import cv2
        import numpy as np
    except ImportError:
        return None
    cap = cv2.VideoCapture(path)
    if not cap.isOpened():
        return None
    h_top_qua_cao, h_bot_qua_thap = 0, 0
    tong = 0
    # bo 10% dau/cuoi (hook/outro co the co chu chu dong o vi tri khac quy chuan)
    for i in range(6):
        t = dai * (0.15 + 0.70 * i / 5.0)
        cap.set(cv2.CAP_PROP_POS_MSEC, t * 1000)
        ok, f = cap.read()
        if not ok:
            continue
        tong += 1
        hgt, w = f.shape[:2]
        gray = cv2.cvtColor(f, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 80, 160)
        vung_top = edges[0:int(hgt * 0.15), int(w * 0.15):int(w * 0.85)]
        vung_bot = edges[int(hgt * 0.80):hgt, int(w * 0.15):int(w * 0.85)]
        # nguong kinh nghiem: chu dam dac cho mat do canh > ~6%; nen video thuong < ~3%
        if float(np.mean(vung_top > 0)) > 0.06:
            h_top_qua_cao += 1
        if float(np.mean(vung_bot > 0)) > 0.06:
            h_bot_qua_thap += 1
    cap.release()
    if tong < 3:
        return None
    return {"nghi_chu_o_vung_tren": h_top_qua_cao >= max(2, tong // 2),
            "nghi_chu_o_vung_duoi": h_bot_qua_thap >= max(2, tong // 2)}


def kiem_mc_gia(cong_thuc_path, index_path):
    """CHAN CUNG luat "cam canh MC gia" (them 23/07/2026, thay cho viec chi dan
    Claude bang chu — luat chu tung bi VI PHAM 2 LAN o 2 kieu dung khac nhau
    trong cung 1 buoi giao hang, cho thay day la loi HE THONG chu khong phai
    nho quen 1 lan).

    Doi chieu tung "canh" trong file cong-thuc (luu_cong_thuc.py) voi co
    'co_nguoi_dang_noi' cua mat AI Gemini trong index.json: canh nao dung am
    thanh KHAC nguon goc cua chinh clip do (am_thanh != "goc" — tuc dang dung
    lam B-roll duoi tieng khac) MA clip do co nguoi dang noi truoc camera ->
    VI PHAM, tra ve danh sach loi.

    Gioi han: cho CHUA chay mat AI Gemini cho clip do thi khong doi chieu duoc
    (bo qua, khong bao loi oan) — day la lop chan BO SUNG, khong thay viec tu
    soi bang mat khi chua co co Gemini."""
    if not os.path.exists(cong_thuc_path) or not os.path.exists(index_path):
        return None  # thieu du lieu de doi chieu -> khong chan, de kiem() tu bao rieng
    cong_thuc = json.load(open(cong_thuc_path, encoding="utf-8"))
    idx = json.load(open(index_path, encoding="utf-8"))
    clips = idx.get("clips", {})

    def tim_clip(ten):
        for k, v in clips.items():
            rel = k.split("|")[0]
            if os.path.basename(rel) == ten or rel == ten or rel.replace("\\", "/").endswith("/" + ten):
                return v
        return None

    loi = []
    for c in cong_thuc.get("canh", []):
        ten_clip = c.get("clip", "")
        am_thanh = c.get("am_thanh") or "goc"
        if am_thanh == "goc" or not ten_clip:
            continue
        found = tim_clip(ten_clip)
        if not found:
            continue  # clip chua co trong index (chua analyze_footage) -> khong doi chieu duoc
        g = found.get("gemini") or {}
        if g.get("co_nguoi_dang_noi") is True:
            loi.append(
                "CAM MC GIA: canh '%s' (clip %s, %.1fs-%.1fs) co NGUOI DANG NOI theo mat AI, "
                "nhung am thanh cua canh nay lay tu nguon khac ('%s') thay vi tieng goc dong bo — "
                "dung lam B-roll kieu nay la vi pham luat cam canh MC gia."
                % (c.get("nhan", "?"), ten_clip, c.get("t0", 0), c.get("t1", 0), am_thanh))
    return loi


def kiem_canh_qua_dai(cong_thuc_path, index_path):
    """CHAN CUNG luat "Kieu 2 khong duoc giu nguyen cu may dai" (them 23/07/2026,
    sau khi Sep Huy bat 1 canh 12.1s lien tuc trong video-3 Ba Na Hills — luat
    van da co san bang chu trong quy-trinh-chon-canh.md tu 21/07 ("cong thuc 2C
    la ~3s/canh... de nguyen 10 giay mot khung la loi, khong phai phong cach")
    nhung chi la LUAT CHU nen bi lo, giong het duong luat "cam canh MC gia" tung
    bi lo 2 lan truoc khi co kiem_mc_gia() chan cung ben tren.

    QUAN TRONG — luat nay CHI ap cho B-ROLL (canh khong co nguoi dang noi dong
    bo), KHONG ap cho chinh canh MC dang noi truoc camera: cau thoai dai bao
    nhieu giay thi canh MC do duoc phep dai bay nhieu giay, vi "loi co san la
    xuong song bat bien" (tu-lua-chon-den-san-pham.md) — cat ngang mat MC dang
    noi moi la loi, khong phai giu canh dai. Phan biet bang chinh co
    'co_nguoi_dang_noi' cua mat AI Gemini trong index.json (dung lai logic cua
    kiem_mc_gia): co=True VA am_thanh bat dau bang "goc" (tieng dong bo that,
    khong phai muon tu clip khac) -> day la canh MC dan, BO QUA. Con lai (khong
    co ai dang noi, hoac co nguoi noi nhung dang dung lam B-roll duoi tieng
    khac) -> ap luat ~3s/canh.

    Chi ap dung cho Kieu 2 — Kieu 1 duoc PHEP giu 1 cu may dai neu canh dep
    (xem gu-kieu-2-3.md: "DUNG mac dinh Kieu 1 la phai cat nhieu", T300 tiec
    cuoi 29.6s khong cat lan nao). Kieu 3 co luat rieng ve doi text (~2.5s).

    Doc do dai THUC TE tren man hinh (chia cho he so tempo neu canh do da duoc
    tang toc — vd am_thanh ghi "goc-tempo-1.5x"), khong phai do dai cat tho.
    Cho phep canh DAU va canh CUOI (hook/CTA) dai hon 1 chut theo dung quy uoc
    "canh hook va CTA nen de dai hon" (so-hieu-ung.md)."""
    if not os.path.exists(cong_thuc_path):
        return None
    d = json.load(open(cong_thuc_path, encoding="utf-8"))
    if d.get("kieu_dung") != "Kieu 2":
        return []  # luat nay chi ap cho Kieu 2, xem docstring

    clips = {}
    if index_path and os.path.exists(index_path):
        idx = json.load(open(index_path, encoding="utf-8"))
        clips = idx.get("clips", {})

    def co_nguoi_dang_noi(ten_clip):
        for k, v in clips.items():
            rel = k.split("|")[0]
            if os.path.basename(rel) == ten_clip or rel == ten_clip or rel.replace("\\", "/").endswith("/" + ten_clip):
                return (v.get("gemini") or {}).get("co_nguoi_dang_noi")
        return None  # chua quet mat AI cho clip nay -> khong biet, coi nhu B-roll de an toan

    canh = d.get("canh", [])
    n = len(canh)
    loi = []
    for i, c in enumerate(canh):
        am_thanh = c.get("am_thanh") or "goc"
        ten_clip = c.get("clip", "")
        if am_thanh.startswith("goc") and co_nguoi_dang_noi(ten_clip) is True:
            continue  # canh MC dan dong bo that -> dai bao nhieu cung duoc, bo qua

        t0, t1 = c.get("t0", 0), c.get("t1", 0)
        dai_cat = t1 - t0
        m = re.search(r"tempo-([\d.]+)x", am_thanh)
        speed = float(m.group(1)) if m else 1.0
        dai_thuc = dai_cat / speed
        gioi_han = 9.0 if i == 0 or i == n - 1 else 6.0
        if dai_thuc > gioi_han:
            loi.append(
                "CANH QUA DAI (Kieu 2, B-roll): '%s' (clip %s) keo dai %.1fs LIEN TUC 1 goc may "
                "(gioi han %.1fs cho vi tri nay) — vi pham luat quy-trinh-chon-canh.md "
                "'~3s/canh, de nguyen 1 khung dai la loi khong phai phong cach'. "
                "Sua: cat highlight 3-4s + chen canh khac (uu tien), hoac tua nhanh theo "
                "duong cong 1x-cao diem-1x xem ffmpeg-recipes.md muc 2."
                % (c.get("nhan", "?"), ten_clip, dai_thuc, gioi_han))
    return loi


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

        # --- vung an toan chu (khong bi UI TikTok/Reels che) ---
        an_toan = kiem_vung_an_toan_chu(v, d["dai"])
        if an_toan is None:
            canh_bao.append("%s: khong do duoc vung an toan chu (thieu cv2?)" % ten)
        else:
            if an_toan["nghi_chu_o_vung_tren"]:
                canh_bao.append("%s: NGHI co chu/logo o vung 15%% tren cung — de bi thanh trang thai app che" % ten)
            if an_toan["nghi_chu_o_vung_duoi"]:
                canh_bao.append("%s: NGHI co chu o vung 20%% duoi cung — de bi nut tuong tac/caption app che" % ten)
            if not an_toan["nghi_chu_o_vung_tren"] and not an_toan["nghi_chu_o_vung_duoi"]:
                print("  Vung an toan chu     DAT (khong vuong UI tren/duoi)")

    # --- luat cam canh MC gia (chan cung, doi chieu voi cong-thuc-dung neu co) ---
    if a.cong_thuc and a.index:
        mc_gia = kiem_mc_gia(a.cong_thuc, a.index)
        if mc_gia is None:
            canh_bao.append("Khong doi chieu duoc luat MC gia (thieu file cong-thuc hoac index.json)")
        elif mc_gia:
            loi.extend(mc_gia)
        else:
            print("\n  Luat cam canh MC gia   DAT (khong canh nao vi pham theo du lieu co)")
    elif a.cong_thuc or a.index:
        canh_bao.append("Can CA --cong-thuc VA --index de doi chieu luat MC gia — hien chi co 1 trong 2.")

    # --- luat "Kieu 2 khong duoc giu nguyen cu may dai" (chan cung) ---
    if a.cong_thuc:
        qua_dai = kiem_canh_qua_dai(a.cong_thuc, a.index)
        if qua_dai:
            loi.extend(qua_dai)
        elif qua_dai == []:
            print("  Luat canh qua dai (K2) DAT (khong canh nao vuot gioi han, hoac khong phai Kieu 2)")

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
    ap.add_argument("--cong-thuc", help="file cong-thuc-dung (.json tu luu_cong_thuc.py) de doi chieu luat MC gia")
    ap.add_argument("--index", help="file analysis/index.json (co truong 'gemini') de doi chieu luat MC gia")
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

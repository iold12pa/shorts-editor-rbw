# -*- coding: utf-8 -*-
"""Tim cac doan CO GIONG NGUOI THAT NOI VAO MAY — va cho MOC CAT chinh xac.

Y tuong goc: Sep Huy 21/07/2026 — "dung muc am de phan biet thoai nguoi noi hay khong".

VI SAO CAN SCRIPT NAY (bai hoc dat gia 21/07/2026, da nghiem thu bang tai Sep):
  - Moc Whisper KHONG PHAI so do. Whisper NOI DUOI cac doan: doan sau bat dau
    dung cho doan truoc ket thuc. Ca that clip 0010: Whisper bao cau MC bat dau
    19.99s, THUC TE 24.0s — lech 4 giay, cat theo la mat dau cau.
    Dau hieu nhan biet: doan dai bat thuong so voi so chu (10 giay cho cau 5 giay).
  - silencedetect CHET trong moi truong on lien tuc (nha sach, nha may). No chi
    nhin to/nho, khong nhin CHAT giong -> bat nham tieng on nhap nho la "het cau".
  - Gemini doan moc tot hon Whisper nhung van sai (dung 2/4 ca da cham).
  => Script nay do TRUC TIEP tren am thanh goc, dung 2 chi so:
       1. MUC so voi SAN NHIEU cua chinh clip do (khong dung nguong tuyet doi —
          san nhieu ca kho trai tu -20 den -49 dB, moi nguong co dinh deu sai)
       2. DO AM = nang luong 100-400Hz / 2-6kHz. Giong nguoi gan mic thi AM;
          loa robot / tieng vong tu xa thi MONG va CHOI.

CAM TUYET DOI: khong loc on / speechnorm / highpass TRUOC khi chay script nay.
  Do that 21/07: afftdn lam do am sai gap 4-27 lan va bat nham gap 5 lan;
  speechnorm lam cach san tut 17.2 -> 10.3 dB (mat kha nang chon ban take tot).
  Bo loc chi duoc chay o buoc MIX CUOI — xem ffmpeg-recipes.md muc 5c.

KHONG DUNG DUOC CHO FILE TTS (giong may doc) — gioi han that, do chieu 21/07:
  Script tinh san nhieu tu CHINH clip (phan vi 20). File TTS thi khoang lang la
  IM TUYET DOI nen phep tinh san vo nghia -> no cham CA 3 doan giong la "XA MIC",
  co doan ra cach san = -21.8 dB (am, tuc thap hon ca san).
  => File TTS thi dung `silencedetect` (nen im tuyet doi nen no chay hoan hao).
     File tieng THU THAT (co on nen) moi dung script nay.

LUU Y KHI DOC KET QUA — truong "loi" BAO DU CHU:
  "loi" ghep tu cac doan Whisper GIAO NHAU voi lat cat, nen no thuong hien
  NHIEU CHU HON thuc te lat cat chua. Ca that 21/07: doan 11.90-17.20 hien loi
  "nhung nha sach rong the nay biet quay nao ma tim..." nhung cat ra nghe lai
  chi con tu "sach rong the nay" — mat "Nhung nha". Bien dung la 11.50.
  => LUON cho Whisper nghe lai chinh lat cat truoc khi chot (phep ra bat buoc
     trong SKILL.md buoc 4 muc 7).

Usage:
    # 1 clip
    python loc_thoai_that.py <clip.mp4> [--index <index.json>] [--json <out.json>]

    # ca folder: doc index.json, ghi ket qua vao truong "loc_thoai" cua tung clip
    python loc_thoai_that.py --index <index.json> --folder <thu muc goc> [--limit N]
"""
import argparse
import glob
import json
import os
import subprocess
import sys

# Bao dam goi ffmpeg/ffprobe chay duoc tren MOI may (them 22/07/2026).
# Thieu ffmpeg thi bao bang tieng nguoi, khong de vo voi 'WinError 2'.
try:
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from chung_ffmpeg import nap_ffmpeg
    nap_ffmpeg()
except ImportError:
    pass


if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

try:
    import numpy as np
except ImportError:
    sys.exit("Chua cai numpy. Chay: python -m pip install numpy")

SR = 16000
WIN_S = 0.40          # cua so phan tich
HOP_S = 0.10          # buoc nhay -> do phan giai moc cat 0.1s
MARGIN_DB = 8.0       # cao hon san nhieu bao nhieu dB moi tinh la co tieng noi
WARM_MIN = 0.45       # duoi nguong nay = mong/choi = loa xa, khong phai nguoi noi gan
GAP_FILL_S = 0.35     # 2 doan cach nhau duoi nguong nay thi noi lam 1 (ngat hoi giua cau)
MIN_SEG_S = 0.50      # doan ngan hon nguong nay thi bo
GAP_GAN_MIC = 15.0    # cach san >= nguong nay = noi vao may, dung duoc
SAN_ON_QUA = -25.0    # san nhieu cao hon muc nay -> silencedetect chac chan chet
GIONG_NHAU = 0.70     # ty le tu chung de coi 2 doan la CUNG MOT CAU noi lai

# Tu dem, khong mang noi dung. Cau chi gom may tu nay = e-kip noi, khong phai thoai.
FILLER = {"ừ", "à", "ờ", "ok", "oke", "okay", "dạ", "vâng", "rồi", "đấy", "ừm", "ạ",
          "đó", "thế", "này", "kia", "hả", "nhé", "nha", "đi", "em", "anh", "chị"}

# Cum CHI DAO khong the nham — moi ra tu 1.383 doan thoai that trong kho (21/07).
# CO Y KHONG dung cac tu mo ho nhu "thoi", "cat", "dung", "cho", "bat dau":
# do that cho thay chung nam trong NOI DUNG THAT ("dung lai danh gia roi tiep tuc"
# la tinh nang robot; "khong can cho doi" la cau quang cao) -> gan co nham hang loat.
# "quen roi" (khong dau) la ban Whisper phien sai cua "quen roi" — ca that clip 0014,
# tai Sep nghe ra MC quen thoai o cuoi cau. Chi bat CUM day du, KHONG bat tu "quen"
# don le (do that: "quen mat cai chan sac tren xe" la noi dung that).
NG_CUM = ["lại câu", "cho thoại", "à quên", "ok chưa", "được chưa",
          "làm lại", "nói lại", "quay lại từ", "diễn lại", "một lần nữa",
          "quên rồi", "quen rồi", "quên mất rồi", "lại lúc nãy", "lúc nãy đi"]

# Xung ho suong sa — kich ban marketing KHONG BAO GIO dung. Do that tren 1.383 doan:
# "may" 5/5 lan deu la e-kip ("chac may dang zoom a?", "may cho no quay sang"),
# "tao" 5/6 lan la e-kip (1 ca sai la ten nha hang bi phien nham). Ty le du cao
# de dung lam co NGHI (khong phai loai thang) — nguoi dung nghe lai la biet.
XUNG_HO_SUONG = ["tao", "mày", "bọn mày", "chúng mày"]

# Cum RA LENH QUAY LAI — khi thay cum nay, doan NGAY TRUOC no la take vua bi bo.
# Cach lam phim: MC dien hong -> e-kip noi "lai cau luc nay di" -> MC dien lai.
LENH_QUAY_LAI = ["lại câu", "lại lúc nãy", "lúc nãy đi", "làm lại", "nói lại",
                 "diễn lại", "một lần nữa", "cho thoại"]

# ---- LOP SOI CHEO: Silero VAD (tuy chon, bo qua im lang neu thieu) ----
# Silero rat gioi cau hoi "co phai GIONG NGUOI khong", nhung KHONG phan biet duoc
# dau la lan noi that (do that 21/07: no gop ca 3 lan MC noi lai thanh 1 doan
# 21.31->29.98, trong khi ban that o 24.4). Nen KHONG dung no thay he do chinh —
# chi dung soi cheo: cho nao he do bao "co nguoi noi" ma Silero bao "khong phai
# giong nguoi" -> nhieu kha nang la TIENG DONG TO, khong phai nguoi.
SILERO_PATHS = [
    os.path.expanduser("~/.claude/roboworld-assets/models/silero_vad.onnx"),
    os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                 "assets", "models", "silero_vad.onnx"),
]
SILERO_CHUNK, SILERO_CTX = 512, 64      # v5 doi dung 512 mau + 64 mau ngu canh chunk truoc
SILERO_NGUONG = 0.5


def silero_xac_suat(x):
    """Tra ve (xac_suat, moc_giay) hoac None neu khong chay duoc (thieu model/onnxruntime)."""
    mp = next((p for p in SILERO_PATHS if os.path.exists(p)), None)
    if not mp:
        return None
    try:
        import onnxruntime as ort
    except ImportError:
        return None
    try:
        s = ort.InferenceSession(mp, providers=["CPUExecutionProvider"])
        st = np.zeros((2, 1, 128), dtype=np.float32)
        ctx = np.zeros(SILERO_CTX, dtype=np.float32)
        sr = np.array(SR, dtype=np.int64)
        ps = []
        for i in range(0, len(x) - SILERO_CHUNK, SILERO_CHUNK):
            ch = x[i:i + SILERO_CHUNK]
            out, st = s.run(None, {"input": np.concatenate([ctx, ch]).reshape(1, -1),
                                   "state": st, "sr": sr})
            ctx = ch[-SILERO_CTX:]
            ps.append(float(out[0][0]))
        # BAY: thieu 64 mau ngu canh thi prob ra gan 0 het ma KHONG bao loi —
        # da dinh that 21/07, tuong Silero hong trong khi loi o cach goi.
        return np.array(ps), np.arange(len(ps)) * SILERO_CHUNK / SR
    except Exception:
        return None


def doc_am(path):
    p = subprocess.run(["ffmpeg", "-v", "quiet", "-i", path, "-ac", "1",
                        "-ar", str(SR), "-f", "s16le", "-"], capture_output=True)
    if p.returncode != 0 or not p.stdout:
        return None
    return np.frombuffer(p.stdout, dtype=np.int16).astype(np.float32) / 32768.0


def do_cua_so(x):
    win, hop = int(WIN_S * SR), int(HOP_S * SR)
    if len(x) < win * 2:
        return None
    w = np.hanning(win)
    fr = np.fft.rfftfreq(win, 1.0 / SR)
    ml, mh = (fr >= 100) & (fr < 400), (fr >= 2000) & (fr < 6000)
    n = (len(x) - win) // hop + 1
    t = np.arange(n) * HOP_S
    db = np.empty(n)
    warm = np.empty(n)
    for k in range(n):
        seg = x[k * hop:k * hop + win]
        S = np.abs(np.fft.rfft(seg * w))
        db[k] = 20.0 * np.log10(max(float(np.sqrt((seg ** 2).mean())), 1e-9))
        warm[k] = float(S[ml].sum() / max(S[mh].sum(), 1e-9))
    return t, db, warm


def gom_doan(t, mask):
    segs, mo = [], None
    for i, ok in enumerate(mask):
        if ok and mo is None:
            mo = float(t[i])
        elif not ok and mo is not None:
            segs.append([mo, float(t[i]) + WIN_S])
            mo = None
    if mo is not None:
        segs.append([mo, float(t[-1]) + WIN_S])
    gop = []
    for s in segs:
        if gop and s[0] - gop[-1][1] <= GAP_FILL_S:
            gop[-1][1] = s[1]
        else:
            gop.append(s)
    return [s for s in gop if s[1] - s[0] >= MIN_SEG_S]


def tu(s):
    import re
    return [w for w in re.sub(r"[^\w\s]", " ", (s or "").lower()).split() if w]


def giong_nhau(a, b):
    A, B = set(tu(a)), set(tu(b))
    if not A or not B:
        return 0.0
    return len(A & B) / max(len(A), len(B))


def nghi_e_kip(chu):
    """Nhan dien loi E-KIP thay vi noi dung. Tin hieu chinh la CAU TRUC, khong phai tu vung."""
    import re
    if not chu or not chu.strip():
        return False, ""
    low = chu.lower()
    for c in NG_CUM:
        if re.search(r"(?<!\w)%s(?!\w)" % re.escape(c), low):
            return True, 'co cum chi dao: "%s"' % c
    for x in XUNG_HO_SUONG:
        if re.search(r"(?<!\w)%s(?!\w)" % re.escape(x), low):
            return True, 'xung ho suong sa "%s" — kich ban khong dung' % x
    w = tu(chu)
    if len(w) <= 3 and all(x in FILLER for x in w):
        return True, "cau %d tu toan tu dem" % len(w)
    if re.search(r"(?:,|\bvà|\bthì|\blà|\bmà|\bnhưng)\s*$", low):
        return True, "cau cut giua chung"
    return False, ""


def co_lenh_quay_lai(chu):
    import re
    low = (chu or "").lower()
    return any(re.search(r"(?<!\w)%s(?!\w)" % re.escape(c), low) for c in LENH_QUAY_LAI)


def diem_gemini(gem, t0, t1):
    """Diem noi dung cua Gemini cho doan [t0,t1].

    PHAN CONG RO RANG (chot 21/07/2026):
      - script nay  -> MOC CAT (o dau) + co dung duoc khong (gan mic, khong phai e-kip)
      - Gemini      -> DOAN NAO DANG LEN HINH (diem noi dung, hook)
      - Whisper     -> NOI GI (noi dung chu)
    Gemini cham MOC sai 2/4 ca da kiem nen KHONG lay moc cua no; nhung no la thu
    duy nhat VUA XEM VUA NGHE ca clip nen diem noi dung cua no dang tin.
    """
    if not isinstance(gem, dict):
        return None, False
    diem = None
    for m in (gem.get("khoanh_khac") or []):
        if not isinstance(m, dict):
            continue
        try:
            a, b = float(m.get("t0", 0)), float(m.get("t1", 0))
        except (TypeError, ValueError):
            continue
        if b > t0 and a < t1:                      # co giao nhau
            d = m.get("diem_10")
            if isinstance(d, (int, float)):
                diem = max(diem, float(d)) if diem is not None else float(d)
    hook = False
    ht = gem.get("hook_tiem_nang")
    if isinstance(ht, str) and ht.strip():
        import re
        for g in re.finditer(r"(\d+):(\d+)|giây\s*(\d+(?:\.\d+)?)", ht.lower()):
            s = (int(g.group(1)) * 60 + int(g.group(2))) if g.group(1) else float(g.group(3))
            if t0 - 1.0 <= s <= t1 + 1.0:
                hook = True
    return diem, hook


def phan_tich(path, transcript=None, gem=None):
    x = doc_am(path)
    if x is None:
        return {"loi": "khong doc duoc am thanh"}
    r = do_cua_so(x)
    if r is None:
        return {"loi": "clip qua ngan"}
    t, db, warm = r
    san = float(np.percentile(db, 20))
    mask = (db > san + MARGIN_DB) & (warm > WARM_MIN)
    segs = gom_doan(t, mask)

    sil = silero_xac_suat(x)          # None neu khong co model / onnxruntime

    tr = transcript or []
    ds = []
    for s0, s1 in segs:
        sel = (t >= s0) & (t <= s1)
        if not sel.any():
            continue
        # chi so cua CHINH doan nay
        m_db = float(db[sel].mean())
        idx = [i for i, s in enumerate(tr)
               if s.get("t1", 0) > s0 and s.get("t0", 0) < s1]
        chu = " ".join((tr[i].get("text") or "") for i in idx).strip()
        ds.append({"t0": round(s0, 2), "t1": round(s1, 2), "dai": round(s1 - s0, 2),
                   "db": round(m_db, 1), "cach_san": round(m_db - san, 1),
                   "do_am": round(float(warm[sel].mean()), 2),
                   "gan_mic": (m_db - san) >= GAP_GAN_MIC,
                   "_wid": tuple(idx), "loi": chu})

    # Gom cac doan NOI LAI CUNG MOT CAU -> giu ban TO NHAT.
    # LUU Y (da thu va bo): TUNG doi hoi 2 doan phai roi vao 2 doan Whisper KHAC NHAU
    # moi coi la "noi lai". Sai — vi Whisper thuong GOP ca 3 lan noi lai vao MOT doan
    # (ca that clip 0010: 3 lan noi cung nam gon trong doan Whisper 19.99-30.01), nen
    # dieu kien do lam tat han tinh nang o dung ca no can nhat. Gio chi so khop LOI.
    nhom = []
    for d in ds:
        for n in nhom:
            if (giong_nhau(d["loi"], n[0]["loi"]) >= GIONG_NHAU
                    and len(tu(d["loi"])) >= 3):
                n.append(d)
                break
        else:
            nhom.append([d])
    for n in nhom:
        tot = max(n, key=lambda d: d["db"])
        for d in n:
            d["so_lan_noi"] = len(n)
            d["ban_tot_nhat"] = (d is tot) if len(n) > 1 else None

    for d in ds:
        ng, ly_do = nghi_e_kip(d["loi"])
        d["nghi_e_kip"] = ng
        d["ly_do_nghi"] = ly_do
        d["diem_gemini"], d["la_hook"] = diem_gemini(gem, d["t0"], d["t1"])
        d.pop("_wid", None)
        # soi cheo Silero: doan nay co that su la GIONG NGUOI khong
        if sil is not None:
            sp, stt = sil
            sel2 = (stt >= d["t0"]) & (stt <= d["t1"])
            if sel2.any():
                d["silero"] = round(float(sp[sel2].mean()), 2)
                if d["silero"] < SILERO_NGUONG and not d["nghi_e_kip"]:
                    d["nghi_e_kip"] = True
                    d["ly_do_nghi"] = ("Silero cham %.2f — nghi la TIENG DONG TO, khong phai giong nguoi"
                                       % d["silero"])

    # E-KIP RA LENH QUAY LAI -> doan NGAY TRUOC do la take vua bi bo.
    # Cach lam phim: MC dien hong -> e-kip noi "lai cau luc nay di" -> MC dien lai.
    # Khong co luat nay thi take hong van lot qua neu chinh no khong chua tu tu-sua.
    for i, d in enumerate(ds):
        if co_lenh_quay_lai(d["loi"]) and i > 0:
            truoc = ds[i - 1]
            if not truoc["nghi_e_kip"]:
                truoc["nghi_e_kip"] = True
                truoc["ly_do_nghi"] = "ngay sau doan nay e-kip ra lenh quay lai"

    # Doi chieu cheo voi Gemini — bat 2 tinh huong dang ngo
    canh_bao = []
    if isinstance(gem, dict):
        co_dung = [d for d in ds if d["gan_mic"] and not d["nghi_e_kip"]]
        if gem.get("co_nguoi_dang_noi") and not co_dung:
            canh_bao.append("Gemini thay CO nguoi dang noi nhung khong doan nao du gan mic"
                            " -> nguoi noi o xa/ngoai khung, dung lam thoai chinh se te.")
        if co_dung and gem.get("co_nguoi_dang_noi") is False:
            canh_bao.append("Script tim ra thoai nhung Gemini bao KHONG co ai dang noi tren hinh"
                            " -> co the la loi dan ngoai hinh; cam dat lam B-roll de voice khac"
                            " (luat cam MC-cutaway).")

    return {"san_nhieu_db": round(san, 1),
            "silencedetect_dung_duoc": san <= SAN_ON_QUA,
            "canh_bao": canh_bao,
            "doan": ds}


def in_ket_qua(ten, kq):
    print("CLIP: %s" % ten)
    if kq.get("loi"):
        print("   LOI: %s" % kq["loi"])
        return
    print("   San nhieu: %.1f dB" % kq["san_nhieu_db"])
    if not kq["silencedetect_dung_duoc"]:
        print("   ⚠ San nhieu cao hon %.0f dB -> silencedetect SE CHET o clip nay."
              " Dung moc cua script nay, DUNG THU silencedetect." % SAN_ON_QUA)
    if not kq["doan"]:
        print("   Khong tim thay doan nao co giong nguoi noi gan mic.")
        return
    for i, d in enumerate(kq["doan"], 1):
        co = []
        if d.get("la_hook"):
            co.append("HOOK (Gemini)")
        if d.get("so_lan_noi", 1) > 1:
            co.append("BAN TOT NHAT trong %d lan noi lai" % d["so_lan_noi"]
                      if d["ban_tot_nhat"] else
                      "ban thua (%d lan noi lai)" % d["so_lan_noi"])
        if not d["gan_mic"]:
            co.append("XA MIC (cach san %.1f dB)" % d["cach_san"])
        if d["nghi_e_kip"]:
            co.append("NGHI E-KIP: %s" % d["ly_do_nghi"])
        dg = "" if d.get("diem_gemini") is None else " G%.0f/10" % d["diem_gemini"]
        if d.get("silero") is not None:
            dg += " S%.2f" % d["silero"]
        print("   %2d) %6.2f -> %6.2f  (%.2fs)  %6.1f dB  cach san %5.1f  am %.2f%-6s%s"
              % (i, d["t0"], d["t1"], d["dai"], d["db"], d["cach_san"], d["do_am"], dg,
                 ("   << " + " | ".join(co)) if co else ""))
        if d["loi"]:
            print("        noi: %s" % d["loi"][:110])
    for c in kq.get("canh_bao", []):
        print("   ⚠ %s" % c)
    dung = [d for d in kq["doan"] if d["gan_mic"] and not d["nghi_e_kip"]
            and d.get("ban_tot_nhat") is not False]
    # xep uu tien theo diem noi dung cua Gemini (hook len dau), chua co diem thi giu thu tu thoi gian
    dung_xep = sorted(dung, key=lambda d: (not d.get("la_hook"),
                                           -(d.get("diem_gemini") or 0), d["t0"]))
    print("   => DUNG DUOC: %d/%d doan%s" % (len(dung), len(kq["doan"]),
          ("  " + ", ".join("%.2f-%.2f%s" % (d["t0"], d["t1"],
           "" if d.get("diem_gemini") is None else "(G%.0f)" % d["diem_gemini"])
           for d in dung_xep)) if dung else ""))


def nap_index(p):
    d = json.load(open(p, encoding="utf-8"))
    clips = d if isinstance(d, list) else d.get("clips", d)
    if isinstance(clips, dict):
        clips = list(clips.values())
    return d, [c for c in clips if isinstance(c, dict)]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("clip", nargs="?")
    ap.add_argument("--index", help="index.json de lay transcript (va de ghi ket qua o che do folder)")
    ap.add_argument("--folder", help="thu muc goc chua clip — bat che do quet CA FOLDER")
    ap.add_argument("--json", help="ghi ket qua 1 clip ra file json")
    ap.add_argument("--limit", type=int, default=0)
    a = ap.parse_args()

    tr_map, gem_map = {}, {}
    goc = None
    if a.index and os.path.exists(a.index):
        goc, clips = nap_index(a.index)
        for c in clips:
            if c.get("file"):
                tr_map[c["file"]] = c.get("transcript") or []
                gem_map[c["file"]] = c.get("gemini")

    # ---- che do CA FOLDER ----
    if a.folder:
        if not a.index:
            sys.exit("Che do folder can --index tro toi index.json.")
        goc, clips = nap_index(a.index)
        can = [c for c in clips if c.get("file") and c.get("has_speech")]
        if a.limit:
            can = can[:a.limit]
        print("Quet %d clip co thoai trong: %s\n" % (len(can), a.folder))
        xong = 0
        for c in can:
            src = None
            for p in glob.glob(os.path.join(a.folder, "**", c["file"]), recursive=True):
                src = p
                break
            if not src:
                print("CLIP: %s  -> KHONG TIM THAY FILE, bo qua" % c["file"])
                continue
            kq = phan_tich(src, c.get("transcript"), c.get("gemini"))
            in_ket_qua(c["file"], kq)
            print()
            c["loc_thoai"] = kq
            xong += 1
        json.dump(goc, open(a.index, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print("XONG %d clip. Da ghi truong 'loc_thoai' vao %s" % (xong, a.index))
        return

    # ---- che do 1 CLIP ----
    if not a.clip:
        sys.exit(__doc__)
    kq = phan_tich(a.clip, tr_map.get(os.path.basename(a.clip)),
                   gem_map.get(os.path.basename(a.clip)))
    in_ket_qua(os.path.basename(a.clip), kq)
    if a.json:
        json.dump(kq, open(a.json, "w", encoding="utf-8"), ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()

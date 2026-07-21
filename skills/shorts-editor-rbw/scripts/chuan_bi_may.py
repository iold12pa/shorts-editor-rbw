# -*- coding: utf-8 -*-
"""CHUAN BI MAY — tu kiem + tu cai MOI THU, de may nguoi dung giong het may quan tri.

Muc tieu (chi dao Sep Huy 21/07/2026): nguoi dung KHONG phai cai thu cong gi ca.
Truoc day cai dat la quy trinh 5 buoc ma Claude ben may ho phai lam dung thu tu —
de sot. Gio gom vao 1 lenh.

Usage:
    python chuan_bi_may.py                 # kiem + tu cai tat ca (chay NEN, ~10-20 phut)
    python chuan_bi_may.py --nhanh         # bo qua 2 khoan tai nang (model 1.6GB + kho 180MB)
    python chuan_bi_may.py --kiem          # CHI kiem, khong cai gi
    python chuan_bi_may.py --luu-key TEN   # doc gia tri key tu STDIN roi ghi vao file bi mat
                                           # (dung stdin de key KHONG lot vao lich su lenh)
"""
import argparse
import importlib.util
import json
import os
import shutil
import subprocess
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

BEN = os.path.expanduser("~/.claude/roboworld-assets")
MODELS = os.path.join(BEN, "models")
KHO = os.path.join(BEN, "tai-nguyen-chung")
ENV_KEY = os.path.expanduser("~/.claude/abs6-secrets.env")
SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ten import -> ten cai pip + mat gi neu thieu
THU_VIEN = [
    ("numpy",        "numpy<2",          "moi phep do deu chet — numpy PHAI ghim <2, ban 2.x lam hong cv2/rembg"),
    ("cv2",          "opencv-python",    "khong cham duoc diem ky thuat clip (do net/chuyen dong)"),
    ("gdown",        "gdown",            "khong tai duoc kho tai nguyen tu Drive"),
    ("edge_tts",     "edge-tts",         "mat giong doc du phong — Kieu 3 chet khi chua co key ElevenLabs"),
    ("librosa",      "librosa",          "mat cat-bam-phach va mat tach nhac tu mix dai"),
    ("moderngl",     "moderngl",         "mat ~80 kieu chuyen canh GL"),
    ("PIL",          "pillow",           "mat luma wipe, the chu dong, mask logo"),
    ("google.genai", "google-genai",     "mat mat AI Gemini"),
    ("onnxruntime",  "onnxruntime",      "mat lop soi cheo Silero VAD khi do moc thoai"),
    ("soundfile",    "soundfile",        "mot so buoc doc/ghi wav se loi"),
]

MODEL_FILES = [
    ("ggml-large-v3-turbo.bin", 1_500_000_000,
     "https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-large-v3-turbo.bin",
     "Bo nghe giong noi (Whisper ~1.6GB)", True),
    ("silero_vad.onnx", 2_000_000,
     "https://github.com/snakers4/silero-vad/raw/master/src/silero_vad/data/silero_vad.onnx",
     "Silero VAD (soi cheo giong nguoi, 2.3MB)", False),
]

KEYS = [
    ("ELEVENLABS_API_KEY", "giong doc AI tieng Viet + sinh nhac", False),
    ("GEMINI_API_KEY",     "mat AI xem clip",                     False),
    ("GROQ_API_KEY",       "du phong, it dung",                   False),
]


def co(mod):
    try:
        return importlib.util.find_spec(mod) is not None
    except (ImportError, ValueError):
        return False


def chay(cmd, timeout=900):
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return p.returncode, (p.stdout or "") + (p.stderr or "")
    except Exception as e:
        return 1, str(e)


def tim_ffmpeg():
    if shutil.which("ffmpeg"):
        return shutil.which("ffmpeg")
    cfg = os.path.join(SKILL_DIR, "config.json")
    if os.path.exists(cfg):
        try:
            v = (json.load(open(cfg, encoding="utf-8")) or {}).get("ffmpeg_path", "")
            if v and os.path.exists(v):
                return v
        except Exception:
            pass
    import glob
    for p in glob.glob(os.path.expandvars(
            r"%LOCALAPPDATA%\Microsoft\WinGet\Packages\Gyan.FFmpeg*\**\bin\ffmpeg.exe"),
            recursive=True):
        return p
    return None


def ghi_config_ffmpeg(path):
    cfg = os.path.join(SKILL_DIR, "config.json")
    d = {}
    if os.path.exists(cfg):
        try:
            d = json.load(open(cfg, encoding="utf-8")) or {}
        except Exception:
            d = {}
    d["ffmpeg_path"] = path
    d["ffprobe_path"] = os.path.join(os.path.dirname(path), "ffprobe.exe")
    json.dump(d, open(cfg, "w", encoding="utf-8"), ensure_ascii=False, indent=2)


def doc_keys():
    co_key = {}
    if os.path.exists(ENV_KEY):
        for line in open(ENV_KEY, encoding="utf-8"):
            if "=" in line and not line.strip().startswith("#"):
                k, v = line.split("=", 1)
                if v.strip().strip('"').strip("'"):
                    co_key[k.strip()] = True
    return co_key


def luu_key(ten):
    """Doc gia tri tu STDIN (khong qua tham so dong lenh -> khong lot vao lich su)."""
    val = sys.stdin.read().strip()
    if not val:
        sys.exit("Khong nhan duoc gia tri key tu stdin.")
    os.makedirs(os.path.dirname(ENV_KEY), exist_ok=True)
    dong = []
    thay = False
    if os.path.exists(ENV_KEY):
        for line in open(ENV_KEY, encoding="utf-8"):
            if line.strip().startswith(ten + "="):
                dong.append("%s=%s\n" % (ten, val))
                thay = True
            else:
                dong.append(line if line.endswith("\n") else line + "\n")
    if not thay:
        dong.append("%s=%s\n" % (ten, val))
    open(ENV_KEY, "w", encoding="utf-8").writelines(dong)
    print("Da luu %s vao %s (%d ky tu). KHONG in gia tri ra man hinh." % (ten, ENV_KEY, len(val)))


def nhap_key_bang_hop_thoai():
    """Mo hop thoai nho de nguoi dung DAN key vao — gia tri di thang tu clipboard
    vao file tren o cung, KHONG di qua chat, KHONG len may chu nao.

    Day la cach DUY NHAT vua tu dong vua thuc su local:
      - dan vao chat  -> key di qua may chu Anthropic + nam lai trong lich su hoi thoai
      - de file .docx -> Claude van phai DOC file do moi lay duoc key => y het tren,
                         lai them viec key phoi tren Desktop (thuong dong bo OneDrive)
      - hop thoai nay -> Claude chi CHAY lenh, khong bao gio thay gia tri
    """
    try:
        import tkinter as tk
        from tkinter import messagebox
    except ImportError:
        print("May khong co tkinter — dung cach stdin: "
              '"<gia-tri>" | python chuan_bi_may.py --luu-key TEN_KEY')
        return

    da_co = doc_keys()
    root = tk.Tk()
    root.title("Nhap API key — Roboworld")
    root.attributes("-topmost", True)
    root.resizable(False, False)

    tk.Label(root, text="Dan key vao o tuong ung roi bam LUU.",
             font=("Segoe UI", 10, "bold")).grid(row=0, column=0, columnspan=2,
                                                 padx=14, pady=(14, 2), sticky="w")
    tk.Label(root, text="Key di thang vao file tren may ban — khong qua chat, khong len mang.",
             fg="#555", font=("Segoe UI", 8)).grid(row=1, column=0, columnspan=2,
                                                   padx=14, pady=(0, 10), sticky="w")
    o = {}
    for i, (ten, dung_de, _) in enumerate(KEYS):
        nhan = "%s\n(%s)%s" % (ten, dung_de, "  — DA CO, de trong neu khong doi" if da_co.get(ten) else "")
        tk.Label(root, text=nhan, justify="left", font=("Segoe UI", 9)).grid(
            row=2 + i, column=0, padx=(14, 8), pady=6, sticky="w")
        e = tk.Entry(root, width=42, show="*")
        e.grid(row=2 + i, column=1, padx=(0, 14), pady=6)
        o[ten] = e

    ket_qua = {"da_luu": []}

    def luu():
        for ten, e in o.items():
            v = e.get().strip()
            if v:
                dong, thay = [], False
                if os.path.exists(ENV_KEY):
                    for line in open(ENV_KEY, encoding="utf-8"):
                        if line.strip().startswith(ten + "="):
                            dong.append("%s=%s\n" % (ten, v))
                            thay = True
                        else:
                            dong.append(line if line.endswith("\n") else line + "\n")
                if not thay:
                    dong.append("%s=%s\n" % (ten, v))
                os.makedirs(os.path.dirname(ENV_KEY), exist_ok=True)
                open(ENV_KEY, "w", encoding="utf-8").writelines(dong)
                ket_qua["da_luu"].append(ten)
        if ket_qua["da_luu"]:
            messagebox.showinfo("Xong", "Da luu: %s" % ", ".join(ket_qua["da_luu"]))
        else:
            messagebox.showwarning("Chua co gi", "Ban chua dan key nao.")
        root.destroy()

    tk.Button(root, text="LUU", width=14, command=luu).grid(
        row=2 + len(KEYS), column=1, pady=(6, 14), sticky="e", padx=(0, 14))
    tk.Button(root, text="Bo qua", width=10, command=root.destroy).grid(
        row=2 + len(KEYS), column=0, pady=(6, 14), sticky="w", padx=(14, 0))

    root.update_idletasks()
    x = (root.winfo_screenwidth() - root.winfo_width()) // 2
    y = (root.winfo_screenheight() - root.winfo_height()) // 3
    root.geometry("+%d+%d" % (x, y))
    root.mainloop()

    if ket_qua["da_luu"]:
        print("Da luu key: %s  (KHONG in gia tri)" % ", ".join(ket_qua["da_luu"]))
    else:
        print("Nguoi dung khong nhap key nao.")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--kiem", action="store_true", help="chi kiem, khong cai gi")
    ap.add_argument("--nhanh", action="store_true", help="bo qua 2 khoan tai nang")
    ap.add_argument("--luu-key", metavar="TEN")
    ap.add_argument("--nhap-key", action="store_true",
                    help="mo hop thoai de nguoi dung tu dan key (khong qua chat)")
    a = ap.parse_args()

    if a.nhap_key:
        return nhap_key_bang_hop_thoai()
    if a.luu_key:
        return luu_key(a.luu_key)

    bang = []
    print("=" * 70)
    print("CHUAN BI MAY — %s" % ("CHI KIEM" if a.kiem else "kiem + tu cai"))
    print("=" * 70)

    # --- 1. Python ---
    v = sys.version.split()[0]
    bang.append(("Python", "OK %s" % v if sys.version_info >= (3, 9)
                 else "CU (%s) — nen nang len 3.10+" % v))

    # --- 2. Thu vien ---
    thieu = [(m, pip, mat) for m, pip, mat in THU_VIEN if not co(m)]
    if not thieu:
        bang.append(("Thu vien Python", "OK du %d/%d" % (len(THU_VIEN), len(THU_VIEN))))
    elif a.kiem:
        bang.append(("Thu vien Python", "THIEU: " + ", ".join(m for m, _, _ in thieu)))
    else:
        print("\n[thu vien] thieu %d goi, dang cai..." % len(thieu), flush=True)
        for m, pip, mat in thieu:
            print("   cai %-16s (thieu thi: %s)" % (pip, mat), flush=True)
        rc, out = chay([sys.executable, "-m", "pip", "install", "-U"]
                       + [pip for _, pip, _ in thieu], timeout=1800)
        con = [m for m, _, _ in thieu if not co(m)]
        bang.append(("Thu vien Python",
                     "OK da cai du" if not con else "VAN THIEU: " + ", ".join(con)))
        if con:
            print("   loi pip (200 ky tu cuoi): %s" % out[-200:], flush=True)

    # --- 3. FFmpeg ---
    ff = tim_ffmpeg()
    if ff:
        bang.append(("FFmpeg", "OK"))
    elif a.kiem:
        bang.append(("FFmpeg", "THIEU"))
    else:
        print("\n[ffmpeg] chua co, dang cai qua winget (~3-5 phut)...", flush=True)
        chay(["winget", "install", "ffmpeg", "-e", "--source", "winget",
              "--accept-package-agreements", "--accept-source-agreements"], timeout=1800)
        ff = tim_ffmpeg()
        if ff and not shutil.which("ffmpeg"):
            ghi_config_ffmpeg(ff)
            print("   da ghi duong dan vao config.json (khong can khoi dong lai)", flush=True)
        bang.append(("FFmpeg", "OK vua cai" if ff else "LOI — can cai tay"))

    # --- 4. Model ---
    os.makedirs(MODELS, exist_ok=True)
    for ten, cothe, url, nhan, nang in MODEL_FILES:
        p = os.path.join(MODELS, ten)
        if os.path.exists(p) and os.path.getsize(p) > cothe * 0.9:
            bang.append((nhan, "OK (%.0f MB)" % (os.path.getsize(p) / 1048576)))
            continue
        if a.kiem or (nang and a.nhanh):
            bang.append((nhan, "THIEU" + (" (bo qua vi --nhanh)" if nang and a.nhanh else "")))
            continue
        print("\n[tai] %s ..." % nhan, flush=True)
        tam = p + ".part"
        rc, out = chay(["powershell", "-NoProfile", "-Command",
                        "$ProgressPreference='SilentlyContinue';"
                        "Invoke-WebRequest -Uri '%s' -OutFile '%s'" % (url, tam)],
                       timeout=3600)
        if os.path.exists(tam) and os.path.getsize(tam) > cothe * 0.9:
            os.replace(tam, p)
            bang.append((nhan, "OK vua tai"))
        else:
            if os.path.exists(tam):
                os.remove(tam)
            bang.append((nhan, "LOI tai — thu lai sau"))

    # --- 5. Kho tai nguyen ---
    so_file = sum(len(f) for _, _, f in os.walk(KHO)) if os.path.isdir(KHO) else 0
    if so_file >= 80:
        bang.append(("Kho tai nguyen cong ty", "OK (%d file)" % so_file))
    elif a.kiem or a.nhanh:
        bang.append(("Kho tai nguyen cong ty",
                     "THIEU (%d file)%s" % (so_file, " — bo qua vi --nhanh" if a.nhanh else "")))
    else:
        print("\n[kho] tai kho logo/nhac/SFX tu Drive (~180MB)...", flush=True)
        chay([sys.executable, os.path.join(SKILL_DIR, "scripts", "tai_kho_tai_nguyen.py")],
             timeout=3600)
        so_file = sum(len(f) for _, _, f in os.walk(KHO)) if os.path.isdir(KHO) else 0
        bang.append(("Kho tai nguyen cong ty",
                     "OK (%d file)" % so_file if so_file >= 80 else "THIEU (%d file) — chay lai sau" % so_file))

    # --- 6. GPU ---
    rc, out = chay([sys.executable, os.path.join(SKILL_DIR, "scripts", "cai_driver_nvidia.py"),
                    "--check"], timeout=120)
    tt = "KHONG_CO_CARD"
    for k in ("GPU_SAN_SANG", "CAN_NANG_DRIVER", "KHONG_CO_CARD"):
        if k in out:
            tt = k
            break
    bang.append(("Card do hoa (render nhanh)",
                 {"GPU_SAN_SANG": "OK — render nhanh 2-5 lan",
                  "CAN_NANG_DRIVER": "CAN NANG DRIVER — hoi nguoi dung roi chay lai script driver",
                  "KHONG_CO_CARD": "khong co card (van dung duoc, cham hon)"}[tt]))

    # --- 7. Key ---
    ck = doc_keys()
    for ten, dung_de, _ in KEYS:
        bang.append(("Key %s" % ten.replace("_API_KEY", ""),
                     "OK" if ck.get(ten) else "CHUA CO — %s" % dung_de))

    # --- in bang ---
    print("\n" + "=" * 70)
    print("BANG TRANG THAI MAY")
    print("=" * 70)
    for k, v in bang:
        print("  %-28s %s" % (k, v))

    thieu_bat_buoc = [k for k, v in bang if v.startswith(("THIEU", "LOI", "VAN THIEU"))
                      and "Key " not in k]
    print()
    if not thieu_bat_buoc:
        print("=> MAY DA SAN SANG DUNG VIDEO.")
    else:
        print("=> CON THIEU: %s" % ", ".join(thieu_bat_buoc))
    thieu_key = [t for t, _, _ in KEYS if not ck.get(t)]
    if thieu_key:
        print()
        print("KEY con thieu: %s" % ", ".join(thieu_key))
        print("Cach lay: xin quan tri (Sep Huy) gui qua Zalo, roi DAN THANG VAO CHAT")
        print("va noi 'luu key nay' — Claude tu ghi, ban KHONG phai mo file nao.")
        print("(Key KHONG duoc de trong repo/Drive cong khai vi ai cung dung duoc,")
        print(" ma ElevenLabs/Gemini tinh tien theo luong dung.)")


if __name__ == "__main__":
    main()

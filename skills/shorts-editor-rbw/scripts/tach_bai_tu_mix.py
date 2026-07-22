# -*- coding: utf-8 -*-
"""Tach 1 file mix dai (kieu "Top 20 nhac hot" tren YouTube) thanh tung BAI rieng,
va tu chon DOAN HAY NHAT cua moi bai de dung lam nhac nen cho shorts.

Vi sao can: cac ban mix nay la DJ mix lien mach co crossfade -> KHONG co khoang im
giua 2 bai, `silencedetect` tra ve 0 su kien, khong tach duoc bang cach thong thuong.
Cach chac chan nhat la lay TRACKLIST tu phan mo ta video goc (chu kenh luon ghi san),
luu thanh file .txt cung ten dat canh file mp3.

Cach dung:
    python tach_bai_tu_mix.py "<duong dan file mix.mp3>" [--dai 30] [--khong-cat-bai]

  - Tu tim file tracklist: cung thu muc, ten "tracklist.txt" hoac "<ten mp3>.txt".
  - Xuat ra thu muc con "<ten mix>_tach/":
      bai/       : tung bai day du (mp3)
      doan-hay/  : doan hay nhat cua tung bai (mac dinh 30s) - dung lam nhac nen shorts
      danh-muc.json : bang tra cuu (ten bai, moc trong mix, moc doan hay, BPM, do manh)

Cach chon "doan hay nhat" (khong doan mo ho, do bang so):
  1. Do duong bao nang luong RMS + do manh onset (mat do go nhip) theo tung khung.
  2. Truot cua so <dai> giay, cham diem = 0.7*nang luong + 0.3*mat do onset
     (chuan hoa 0-1). Diep khuc / doan "drop" gan nhu luon la cua so diem cao nhat.
  3. BO 12s dau va 8s cuoi moi bai (vung intro + vung crossfade sang bai sau).
  4. Nan diem bat dau ve PHACH gan nhat (librosa beat track) -> cat khong bi lech nhip.
"""
import argparse
import glob
import json
import os
import re
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


def ffmpeg_bin(ten):
    """Lay duong dan ffmpeg/ffprobe: uu tien PATH, sau do config.json cua skill."""
    from shutil import which
    if which(ten):
        return ten
    cfg = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "config.json")
    if os.path.exists(cfg):
        try:
            d = json.load(open(cfg, encoding="utf-8"))
            p = d.get(ten + "_path") or ""
            if p and os.path.exists(p):
                return p
        except Exception:
            pass
    return ten


FF = ffmpeg_bin("ffmpeg")
FP = ffmpeg_bin("ffprobe")


def giay(mmss):
    p = [float(x) for x in mmss.strip().split(":")]
    while len(p) < 3:
        p.insert(0, 0.0)
    return p[0] * 3600 + p[1] * 60 + p[2]


def an_toan(ten):
    """Ten file an toan cho Windows (bo dau nhay, dau hoi, gach cheo...)."""
    ten = re.sub(r'[\\/:*?"<>|]', "", ten)
    return re.sub(r"\s+", " ", ten).strip()[:90]


def doc_tracklist(mix_path):
    thu_muc = os.path.dirname(mix_path)
    ung_vien = [os.path.join(thu_muc, "tracklist.txt"),
                os.path.splitext(mix_path)[0] + ".txt"]
    tl = next((p for p in ung_vien if os.path.exists(p)), None)
    if not tl:
        sys.exit("CHUA CO TRACKLIST. Tao file 'tracklist.txt' canh file mp3, moi dong:\n"
                 "  00:04:16  Ten bai - Ca si\n"
                 "(lay tu phan mo ta video goc tren YouTube).")
    bai = []
    for dong in open(tl, encoding="utf-8"):
        dong = dong.strip()
        if not dong or dong.startswith("#"):
            continue
        m = re.match(r"^((?:\d{1,2}:)?\d{1,2}:\d{2})\s+(.*)$", dong)
        if m:
            bai.append((giay(m.group(1)), m.group(2).strip()))
    if not bai:
        sys.exit("Tracklist khong doc duoc dong nao hop le: " + tl)
    return sorted(bai), tl


def thoi_luong(path):
    return float(subprocess.check_output(
        [FP, "-v", "error", "-show_entries", "format=duration",
         "-of", "default=nw=1:nk=1", path]).decode().strip())


def tim_doan_hay(path, dai=30.0, bo_dau=12.0, bo_cuoi=8.0):
    """Tra ve (bat_dau, diem, bpm). Dung librosa; thieu thu vien thi lui ve giua bai."""
    try:
        import librosa
        import numpy as np
    except ImportError:
        d = thoi_luong(path)
        return max(0.0, (d - dai) / 2.0), None, None

    y, sr = librosa.load(path, sr=22050, mono=True)
    d = len(y) / sr
    if d <= dai + bo_dau + bo_cuoi:
        return max(0.0, (d - dai) / 2.0), None, None

    hop = 512
    rms = librosa.feature.rms(y=y, hop_length=hop)[0]
    onset = librosa.onset.onset_strength(y=y, sr=sr, hop_length=hop)
    n = min(len(rms), len(onset))
    rms, onset = rms[:n], onset[:n]

    def chuan(a):
        lo, hi = float(a.min()), float(a.max())
        return (a - lo) / (hi - lo) if hi > lo else a * 0.0

    diem_khung = 0.7 * chuan(rms) + 0.3 * chuan(onset)
    fps = sr / hop
    w = int(dai * fps)
    tich = np.concatenate([[0.0], np.cumsum(diem_khung)])
    i_dau, i_cuoi = int(bo_dau * fps), int(n - bo_cuoi * fps) - w
    if i_cuoi <= i_dau:
        return max(0.0, (d - dai) / 2.0), None, None
    tb = (tich[i_dau + w:i_cuoi + w] - tich[i_dau:i_cuoi]) / w
    i_tot = int(np.argmax(tb)) + i_dau
    t_tot = i_tot / fps

    bpm, phach = librosa.beat.beat_track(y=y, sr=sr, hop_length=hop, units="time")
    if len(phach):
        gan = phach[np.argmin(np.abs(phach - t_tot))]
        if abs(gan - t_tot) < 1.0:
            t_tot = float(gan)
    try:
        bpm = float(np.atleast_1d(bpm)[0])
    except Exception:
        bpm = None
    return round(t_tot, 2), round(float(tb.max()), 4), (round(bpm, 1) if bpm else None)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("mix")
    ap.add_argument("--dai", type=float, default=30.0, help="do dai doan hay (giay), mac dinh 30")
    ap.add_argument("--khong-cat-bai", action="store_true", help="chi xuat doan hay, khong xuat bai day du")
    a = ap.parse_args()

    mix = os.path.abspath(a.mix)
    if not os.path.exists(mix):
        sys.exit("Khong thay file: " + mix)
    bai, tl_path = doc_tracklist(mix)
    tong = thoi_luong(mix)
    goc = os.path.join(os.path.dirname(mix), os.path.splitext(os.path.basename(mix))[0][:60] + "_tach")
    d_bai, d_hay = os.path.join(goc, "bai"), os.path.join(goc, "doan-hay")
    os.makedirs(d_bai, exist_ok=True)
    os.makedirs(d_hay, exist_ok=True)
    print("Mix: %.1f phut | tracklist: %s | %d bai" % (tong / 60, os.path.basename(tl_path), len(bai)))

    danh_muc = []
    for i, (t0, ten) in enumerate(bai):
        t1 = bai[i + 1][0] if i + 1 < len(bai) else tong
        dai_bai = t1 - t0
        ten_file = "%02d - %s" % (i + 1, an_toan(ten))
        f_bai = os.path.join(d_bai, ten_file + ".mp3")
        # luon can file bai rieng de phan tich, ke ca khi khong giu lai
        subprocess.run([FF, "-y", "-v", "error", "-ss", str(t0), "-t", str(dai_bai),
                        "-i", mix, "-c:a", "libmp3lame", "-b:a", "192k", f_bai], check=True)

        bd, diem, bpm = tim_doan_hay(f_bai, dai=a.dai)
        f_hay = os.path.join(d_hay, ten_file + " [doan hay].mp3")
        subprocess.run([FF, "-y", "-v", "error", "-ss", str(bd), "-t", str(a.dai), "-i", f_bai,
                        "-af", "afade=t=in:st=0:d=0.4,afade=t=out:st=%.2f:d=0.8" % (a.dai - 0.8),
                        "-c:a", "libmp3lame", "-b:a", "192k", f_hay], check=True)

        danh_muc.append({"stt": i + 1, "ten": ten, "trong_mix": [round(t0, 2), round(t1, 2)],
                         "dai_bai_s": round(dai_bai, 2), "doan_hay_trong_bai": bd,
                         "doan_hay_trong_mix": round(t0 + bd, 2), "dai_doan_hay_s": a.dai,
                         "diem": diem, "bpm": bpm,
                         "file_bai": os.path.relpath(f_bai, goc),
                         "file_doan_hay": os.path.relpath(f_hay, goc)})
        print("  %02d. %-58s bai %5.1fs | doan hay tu %6.1fs | BPM %s"
              % (i + 1, ten[:58], dai_bai, bd, bpm))
        if a.khong_cat_bai:
            os.remove(f_bai)

    with open(os.path.join(goc, "danh-muc.json"), "w", encoding="utf-8") as f:
        json.dump({"mix": os.path.basename(mix), "tong_s": round(tong, 2), "bai": danh_muc},
                  f, ensure_ascii=False, indent=2)
    print("\nXONG ->", goc)


if __name__ == "__main__":
    main()

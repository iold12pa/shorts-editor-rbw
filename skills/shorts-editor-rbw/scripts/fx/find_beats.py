# -*- coding: utf-8 -*-
"""Do PHACH cua bai nhac -> in BPM + moc tung phach + goi y do dai canh.

Dung de cat canh BAM PHACH: moi diem cat canh roi dung vao 1 phach thi video an nhip
nhac, khong bi le. Rat hop Kieu 1 (nhac + chu), nhat la khi dung nhac trend.

Cach dung:
    python find_beats.py "<file nhac.mp3>" [--tu 0] [--dai 90] [--moi 8]

    --tu    giay bat dau doc (mac dinh 0) - dung khi chi lay "doan hay" giua bai
    --dai   do dai doan can do (mac dinh 90s) - do ca bai rat cham, khong can
    --moi   in them goi y do dai canh khi cat moi <n> phach (mac dinh 8)

Vi du that (video MT1 ngay 20/07): bai 143.6 BPM -> cat moi 8 phach = 3.44s/canh,
moi 12 phach = 5.13s/canh. Lay dung 2 so do lam do dai canh la moi cu cat deu vao nhip.
"""
import argparse
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ap = argparse.ArgumentParser()
ap.add_argument("nhac", help="duong dan file nhac")
ap.add_argument("--tu", type=float, default=0.0, help="giay bat dau doc")
ap.add_argument("--dai", type=float, default=90.0, help="do dai doan can do (giay)")
ap.add_argument("--moi", type=int, default=8, help="goi y do dai canh khi cat moi N phach")
a = ap.parse_args()

try:
    import librosa
    import numpy as np
except ImportError:
    sys.exit('THIEU THU VIEN: chay  python -m pip install librosa "numpy<2"  roi thu lai.')

y, sr = librosa.load(a.nhac, sr=22050, mono=True, offset=a.tu, duration=a.dai)
if len(y) == 0:
    sys.exit("Khong doc duoc am thanh - kiem lai duong dan hoac moc --tu.")

bpm, phach = librosa.beat.beat_track(y=y, sr=sr, units="time")
bpm = float(np.atleast_1d(bpm)[0])
if len(phach) < 2:
    sys.exit("Khong do duoc phach (doan nay qua ngan hoac khong co nhip ro).")

print("BPM: %.1f   |   %d phach trong %.0fs (doc tu giay %.1f cua bai)"
      % (bpm, len(phach), a.dai, a.tu))
print("")
print("MOC PHACH (giay, tinh tu diem bat dau doc):")
print(" ".join("%.3f" % b for b in phach))
print("")
for n in sorted({4, a.moi, a.moi + 4, a.moi * 2}):
    if n < len(phach):
        khoang = [phach[i + n] - phach[i] for i in range(0, len(phach) - n, n)]
        tb = sum(khoang) / len(khoang)
        print("  cat moi %2d phach  ->  %.2fs/canh" % (n, tb))
print("")
print("CACH DUNG: lay do dai canh o tren lam do dai tung canh khi cat. Muon chac tuyet doi")
print("thi dat diem cat vao dung moc phach (nho cong them --tu neu co dung).")

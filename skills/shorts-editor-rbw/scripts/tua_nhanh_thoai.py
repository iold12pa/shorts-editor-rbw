# -*- coding: utf-8 -*-
"""TUA NHANH video/audio co tieng NGUOI THU cho do nham — GIU NGUYEN cao do giong.

Sep Huy 21/07/2026: "muc dich ban dau la de tua cac video MC thu, hoac voice over
nguoi thu len toc do do cho do nham chan".

CACH DO (Sep chi 21/07): "lay doan nao noi lien tuc, tinh trung binh bao nhieu chu
tren 1 phut, CAT HET NHUNG DOAN TRONG DI CHO KHACH QUAN" — roi lay 2 con so chia
ti le, tua theo ti le do.
  file mau do duoc 427 chu/phut (cat khoang trong) -> Sep lay 85%% = MOC 363.
  File mau: ~/.claude/roboworld-assets/mau/toc-do-chuan.mp3

CACH LAM — phai lam DONG THOI ca hinh lan tieng, neu khong se lech tieng:
  hinh:  setpts=PTS/<he so>
  tieng: atempo=<he so>     <- atempo GIU NGUYEN CAO DO, khong bi the the giong vit
                               (dung asetrate se lam giong cao vut len, cam)
  atempo chi nhan 0.5-2.0 moi lan -> he so >2 thi noi chuoi atempo=2.0,atempo=x

Usage:
    python tua_nhanh_thoai.py <video-hoac-audio> [--ra <file ra>] [--he-so 1.25]
                              [--muc-tieu 363]   # tu do roi tu tinh he so
"""
import argparse
import os
import re
import subprocess
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# MOC CHUAN = 363 chu/phut khi CAT HET KHOANG TRONG (toc do nha chu thuan).
# File mau Sep dua do duoc 427 theo cach nay; Sep chinh xuong 85% vi mau hoi nhanh.
# (Con so 291 truoc do la do theo cach khac — khoang tu chu dau den chu cuoi,
#  co tinh ca nhip ngat. Hai cach ra hai con so, DUNG TRON.)
CHUAN = 363
TOI_DA = 1.6         # tren muc nay giong bat dau nghe gap gap, khong tu nhien


def khoang_noi(path):
    """Tong thoi gian DANG NHA CHU — CAT HET khoang trong (cach Sep chi 21/07).

    Vi sao cat khoang trong: nhip ngat giua cau khac nhau tuy nguoi tuy kich ban.
    Bo het thi con lai TOC DO NHA CHU thuan -> so sanh 2 file moi cong bang.

    Do bang MUC so voi SAN NHIEU cua chinh clip, KHONG dung silencedetect —
    silencedetect chet trong moi truong on: do that tren video MC nha sach no bao
    "0 giay trong" trong khi thuc te co 17.8 giay khong ai noi.
    """
    import numpy as np
    raw = subprocess.run(["ffmpeg", "-v", "quiet", "-i", path, "-ac", "1",
                          "-ar", "16000", "-f", "s16le", "-"], capture_output=True).stdout
    if not raw:
        sys.exit("Khong doc duoc am thanh: " + path)
    x = np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768.0
    win = 1600                      # cua so 0.1s
    db = np.array([20 * np.log10(max(float(np.sqrt((x[i:i + win] ** 2).mean())), 1e-9))
                   for i in range(0, len(x) - win, win)])
    san = float(np.percentile(db, 20))
    noi = float((db > san + 8).sum()) * 0.1
    return noi, len(x) / 16000.0, san


def chuoi_atempo(he_so):
    """atempo chi nhan 0.5-2.0 moi lan -> chia nho ra noi chuoi."""
    con, khuc = he_so, []
    while con > 2.0:
        khuc.append("atempo=2.0")
        con /= 2.0
    khuc.append("atempo=%.4f" % con)
    return ",".join(khuc)


def co_hinh(path):
    r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0",
                        "-show_entries", "stream=codec_type", "-of", "csv=p=0", path],
                       capture_output=True, text=True).stdout.strip()
    return r.startswith("video")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("nguon")
    ap.add_argument("--ra")
    ap.add_argument("--he-so", type=float)
    ap.add_argument("--muc-tieu", type=float, default=CHUAN)
    ap.add_argument("--am-tiet", type=int,
                    help="so am tiet cua loi (dem tay) — de tu tinh he so")
    a = ap.parse_args()

    sp, dur, san = khoang_noi(a.nguon)
    print("Nguon : %s" % os.path.basename(a.nguon))
    print("        dai %.2fs | dang noi %.2fs | trong %.2fs | san nhieu %.0f dB"
          % (dur, sp, dur - sp, san))

    he_so = a.he_so
    if he_so is None:
        if not a.am_tiet:
            sys.exit("Can --he-so, HOAC --am-tiet (dem tay so am tiet trong loi) de tu tinh.")
        hien = a.am_tiet / sp * 60
        he_so = a.muc_tieu / hien
        print("        toc do hien tai %.0f am tiet/phut -> muc tieu %.0f"
              % (hien, a.muc_tieu))

    if he_so <= 1.001:
        print("=> Da du nhanh (he so %.3f), KHONG can tua." % he_so)
        return
    # Chi CHAN khi he so do MAY TU TINH ra. Nguoi dung go tay --he-so thi cho chay,
    # chi canh bao — (loi cu: chan ca khi da truyen --he-so, cua thoat khong dung duoc).
    if he_so > TOI_DA:
        if a.he_so is None:
            print("!! He so %.2f VUOT nguong %.1f — tua manh the nay giong nghe gap gap."
                  % (he_so, TOI_DA))
            print("   Nen: cat bot doan thua thay vi tua, hoac chap nhan cham hon mau.")
            print("   Van muon tua thi go tay: --he-so %.2f" % he_so)
            return
        print("!! CANH BAO: he so %.2f vuot nguong %.1f — nghe ky xem co gap gap khong."
              % (he_so, TOI_DA))

    ra = a.ra or os.path.splitext(a.nguon)[0] + "-nhanh%.2f.mp4" % he_so
    at = chuoi_atempo(he_so)
    print("        he so %.3f  |  audio: %s" % (he_so, at))

    if co_hinh(a.nguon):
        cmd = ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", a.nguon,
               "-filter_complex",
               "[0:v]setpts=PTS/%.6f[v];[0:a]%s,aresample=48000[a]" % (he_so, at),
               "-map", "[v]", "-map", "[a]",
               "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p",
               "-c:a", "aac", "-b:a", "192k", ra]
    else:
        ra = os.path.splitext(ra)[0] + ".mp3"
        cmd = ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", a.nguon,
               "-af", at + ",aresample=48000", "-c:a", "libmp3lame", "-q:a", "3", ra]

    p = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if p.returncode:
        print(p.stderr[-600:])
        sys.exit(1)
    d2 = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                               "-of", "csv=p=0", ra], capture_output=True, text=True).stdout.strip())
    print("XONG  : %s" % ra)
    print("        %.2fs -> %.2fs (ngan hon %.0f%%)" % (dur, d2, (1 - d2 / dur) * 100))
    print()
    print("NHO: tua xong thi MOI moc thoai deu doi -> phai lam LAI sub/the chu/SFX")
    print("     theo moc moi. Tua TRUOC khi cat canh va dat chu, dung tua sau.")


if __name__ == "__main__":
    main()

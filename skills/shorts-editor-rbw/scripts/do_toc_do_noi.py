# -*- coding: utf-8 -*-
"""Do TOC DO NOI cua mot file tieng noi — de so voi file mau chuan cua Sep.

Sep Huy 21/07/2026: dua file mau "Toc do chuan.MP3" lam moc. Video dan nao do ra
CHAM hon dang ke thi phai day toc do len bang hoac gan bang mau.

CACH DO (Sep chi 21/07 — chot 1 cach duy nhat, dung chung voi tua_nhanh_thoai.py):
    toc do = so CHU / (TONG THOI GIAN DANG NOI) x 60
  - Tieng Viet moi CHU la mot AM TIET -> dem tu cach nhau bang dau cach (tu dong
    bang Whisper).
  - Mau so CAT HET KHOANG TRONG cho khach quan: nhip ngat giua cau khac nhau tuy
    nguoi tuy kich ban, bo het thi con lai TOC DO NHA CHU thuan -> so sanh cong bang.

Usage:
    python do_toc_do_noi.py <file-am-thanh-hoac-video> [file2 ...]
"""
import glob
import os
import re
import subprocess
import sys
import tempfile

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

# Whisper hay BIA cau o cuoi file khi gap doan im — loai truoc khi dem
BIA = ["subscribe", "ghiền mì gõ", "hẹn gặp lại", "cảm ơn các bạn đã theo dõi",
       "video tiếp theo", "đừng quên", "chúc các bạn"]

# MOC CHUAN = 363 chu/phut, do bang cach CAT HET KHOANG TRONG (Sep chi 21/07).
# File mau do duoc 427 theo cach nay -> Sep lay 85% = 363.
# File mau: ~/.claude/roboworld-assets/mau/toc-do-chuan.mp3
#
# DUNG CUNG MOT CACH DO voi tua_nhanh_thoai.py — truoc day 2 script dung 2 cach
# khac nhau (291 vs 363), chac chan gay nham. Nay thong nhat.
#
# MUC DICH CHINH: TUA NHANH video MC thu / voice-over nguoi thu cho do nham chan
# — xem scripts/tua_nhanh_thoai.py. Script nay chi lo phan DEM AM TIET tu dong.
CHUAN = 363


def whisper_srt(path):
    m = sorted(glob.glob(os.path.expanduser("~/.claude/roboworld-assets/models/ggml-*.bin")))
    if not m:
        m = sorted(glob.glob(os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "assets", "models", "ggml-*.bin")))
    if not m:
        sys.exit("Khong thay model Whisper")
    out = os.path.join(tempfile.gettempdir(), "rbw_toc_do_%d.srt" % os.getpid())
    # LUAT: duong dan trong filter phai escape dau hai cham + boc nhay don, va PHAI
    # goi qua Python subprocess (goi thang trong Git Bash se hong escape).
    # BAY: KHONG chi model — duong dan DESTINATION cung chua "C:" nen cung phai
    # escape, neu khong ffmpeg bao "khong nghe duoc" ma khong noi ro vi sao.
    esc = m[0].replace("\\", "/").replace(":", "\\:")
    esc_out = out.replace("\\", "/").replace(":", "\\:")
    af = ("whisper=model='%s':language=vi:queue=3:destination='%s':format=srt"
          % (esc, esc_out))
    p = subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
                        "-i", path, "-af", af, "-f", "null", "-"],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    if p.returncode or not os.path.exists(out):
        return None
    return out


def thoi_gian_noi(path):
    """Tong thoi gian DANG NHA CHU — cat het khoang trong (cach Sep chi 21/07).
    Do bang MUC so voi SAN NHIEU, KHONG dung silencedetect (no chet trong moi
    truong on: bao 0 giay trong trong khi thuc te co 17.8 giay khong ai noi)."""
    import numpy as np
    raw = subprocess.run(["ffmpeg", "-v", "quiet", "-i", path, "-ac", "1",
                          "-ar", "16000", "-f", "s16le", "-"], capture_output=True).stdout
    if not raw:
        return None
    x = np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768.0
    win = 1600
    db = np.array([20 * np.log10(max(float(np.sqrt((x[i:i + win] ** 2).mean())), 1e-9))
                   for i in range(0, len(x) - win, win)])
    san = float(np.percentile(db, 20))
    return float((db > san + 8).sum()) * 0.1


def giay(t):
    h, m, s = t.replace(",", ".").split(":")
    return int(h) * 3600 + int(m) * 60 + float(s)


def do(path):
    srt = whisper_srt(path)
    if not srt:
        print("%-38s KHONG NGHE DUOC" % os.path.basename(path)[:36])
        return None
    khoi = re.findall(r"(\d\d:\d\d:\d\d[,.]\d+)\s*-->\s*(\d\d:\d\d:\d\d[,.]\d+)\s*\n(.+?)(?=\n\s*\n|\Z)",
                      open(srt, encoding="utf-8").read(), re.S)
    dau, cuoi, am = None, None, 0
    for a, b, loi in khoi:
        loi = " ".join(loi.split())
        if any(k in loi.lower() for k in BIA):
            continue
        n = len([w for w in re.sub(r"[^\w\s]", " ", loi).split() if w])
        if n == 0:
            continue
        am += n
        if dau is None:
            dau = giay(a)
        cuoi = giay(b)
    try:
        os.remove(srt)
    except OSError:
        pass
    if not am:
        print("%-38s khong du du lieu" % os.path.basename(path)[:36])
        return None
    noi = thoi_gian_noi(path)
    if not noi:
        print("%-38s khong do duoc thoi gian noi" % os.path.basename(path)[:36])
        return None
    td = am / noi * 60
    lech = (td - CHUAN) / CHUAN * 100
    if td >= CHUAN * 0.9:
        nx = "DAT (bang/nhanh hon mau)"
    elif td >= CHUAN * 0.75:
        nx = "hoi cham — nen day len ~%.0f%%" % ((CHUAN / td - 1) * 100)
    else:
        nx = "CHAM RO — phai day len ~%.0f%%" % ((CHUAN / td - 1) * 100)
    print("%-38s %3d chu / %5.1fs noi  ->  %3.0f chu/phut  (%+.0f%% so moc)  %s"
          % (os.path.basename(path)[:36], am, noi, td, lech, nx))
    if td < CHUAN * 0.98:
        print("        -> tua nhanh: python tua_nhanh_thoai.py <file> --he-so %.2f"
              % (CHUAN / td))
    return td


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    print("Moc chuan: %d am tiet/phut (file mau Sep dua 21/07/2026)\n" % CHUAN)
    for p in sys.argv[1:]:
        do(p)

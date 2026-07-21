# -*- coding: utf-8 -*-
"""Do TOC DO NOI cua mot file tieng noi — de so voi file mau chuan cua Sep.

Sep Huy 21/07/2026: dua file mau "Toc do chuan.MP3" lam moc. Video dan nao do ra
CHAM hon dang ke thi phai day toc do len bang hoac gan bang mau.

CACH DO (chot 1 cach duy nhat de ai chay cung ra cung so):
    toc do = so AM TIET / (moc chu CUOI - moc chu DAU) x 60
  - Tieng Viet moi CHU la mot AM TIET -> dem tu cach nhau bang dau cach.
  - Mau so tinh CA nhip ngat tu nhien giua cau, vi tai nguoi cam nhan nhip nghi
    la mot phan cua toc do. (Neu tru het khoang lang thi con so bi thoi phong —
    do that: cung 1 file ra 357 hay 452 tuy cach tinh.)

Usage:
    python do_toc_do_noi.py <file-am-thanh-hoac-video> [file2 ...]
"""
import glob
import os
import re
import subprocess
import sys
import tempfile

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# Whisper hay BIA cau o cuoi file khi gap doan im — loai truoc khi dem
BIA = ["subscribe", "ghiền mì gõ", "hẹn gặp lại", "cảm ơn các bạn đã theo dõi",
       "video tiếp theo", "đừng quên", "chúc các bạn"]

# MOC CHUAN = 291 am tiet/phut.
# File mau Sep dua do duoc 342, nhung Sep CHINH XUONG con 85% vi mau goc hoi nhanh.
# File mau: ~/.claude/roboworld-assets/mau/toc-do-chuan.mp3
#
# MUC DICH CHINH cua moc nay (Sep noi ro 21/07): de TUA NHANH video MC thu /
# voice-over nguoi thu cho do nham chan — xem scripts/tua_nhanh_thoai.py.
# Dung cho giong may chi la muc dung phu.
CHUAN = 291


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
    if not am or cuoi is None or cuoi <= dau:
        print("%-38s khong du du lieu" % os.path.basename(path)[:36])
        return None
    td = am / (cuoi - dau) * 60
    lech = (td - CHUAN) / CHUAN * 100
    if td >= CHUAN * 0.9:
        nx = "DAT (bang/nhanh hon mau)"
    elif td >= CHUAN * 0.75:
        nx = "hoi cham — nen day len ~%.0f%%" % ((CHUAN / td - 1) * 100)
    else:
        nx = "CHAM RO — phai day len ~%.0f%%" % ((CHUAN / td - 1) * 100)
    print("%-38s %3d am tiet / %5.1fs  ->  %3.0f am tiet/phut  (%+.0f%% so mau)  %s"
          % (os.path.basename(path)[:36], am, cuoi - dau, td, lech, nx))
    # Goi y chinh cho edge-tts: no nhan --rate=+N%% so voi toc do goc cua giong.
    if td < CHUAN * 0.9:
        can = (CHUAN / td - 1) * 100
        print("        -> neu la giong may: tang them ~%+.0f%% vao --rate hien tai" % can)
    return td


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    print("Moc chuan: %d am tiet/phut (file mau Sep dua 21/07/2026)\n" % CHUAN)
    for p in sys.argv[1:]:
        do(p)

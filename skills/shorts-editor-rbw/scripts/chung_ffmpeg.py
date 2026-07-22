"""Nap duong dan FFmpeg cho moi script trong skill — goi 1 dong la xong.

VI SAO CAN (do ra 22/07/2026 trong dot ra soat cua Sep Huy):
    Dem that: 11/15 script co goi "ffmpeg"/"ffprobe". Trong do 9 script goi thang
    ma KHONG kiem tra co hay khong (2 script con lai — chuan_bi_may.py va
    cai_driver_nvidia.py — da co cach tim ffmpeg rieng nen khong can chot nay).
    May da chay "chuan bi may" thi khong sao. Nhung may MOI, hoac may co ffmpeg
    nam ngoai PATH (winget cai vao thu muc rieng), se vo voi:
        FileNotFoundError: [WinError 2] The system cannot find the file specified
    Nguoi dung khong phai dev doc dong do khong the biet la THIEU FFMPEG.

CACH DUNG — them 2 dong ngay sau phan import cua script:

    from chung_ffmpeg import nap_ffmpeg
    nap_ffmpeg()

Sau do moi lenh subprocess goi "ffmpeg"/"ffprobe" nhu cu deu chay duoc, KHONG
phai sua gi them: ham nay tim thay ffmpeg o dau thi them dung thu muc do vao
PATH cua tien trinh dang chay.

Khong tim thay thi dung han, in huong dan bang tieng nguoi thay vi de script
vo giua chung sau khi da ton cong nen/tai file.
"""
import json
import os
import sys
from shutil import which

# Cac cho winget/choco hay dat ffmpeg tren Windows (dung khi no khong nam trong PATH)
CHO_HAY_NAM = [
    r"%LOCALAPPDATA%\Microsoft\WinGet\Links",
    r"%LOCALAPPDATA%\Microsoft\WinGet\Packages",
    r"C:\ProgramData\chocolatey\bin",
    r"C:\ffmpeg\bin",
]


def _tu_config():
    """Doc duong dan ffmpeg da ghi san trong config.json cua skill (neu co)."""
    cfg = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                       "config.json")
    if not os.path.exists(cfg):
        return None
    try:
        d = json.load(open(cfg, encoding="utf-8"))
        p = d.get("ffmpeg_path") or ""
        return p if p and os.path.exists(p) else None
    except Exception:
        return None


def _do_tim_trong_thu_muc():
    """Lan tim ffmpeg.exe trong cac thu muc winget/choco quen thuoc."""
    for goc in CHO_HAY_NAM:
        goc = os.path.expandvars(goc)
        if not os.path.isdir(goc):
            continue
        for root, _dirs, files in os.walk(goc):
            for ten in ("ffmpeg.exe", "ffmpeg"):
                if ten in files:
                    return os.path.join(root, ten)
    return None


def nap_ffmpeg(bat_buoc=True):
    """Bao dam goi "ffmpeg"/"ffprobe" chay duoc. Tra ve duong dan ffmpeg dang dung.

    bat_buoc=True  -> khong tim thay thi dung han kem huong dan (mac dinh).
    bat_buoc=False -> tra ve None de script tu xu ly.
    """
    if which("ffmpeg") and which("ffprobe"):
        return "ffmpeg"

    duong = _tu_config() or _do_tim_trong_thu_muc()
    if duong:
        thu_muc = os.path.dirname(os.path.abspath(duong))
        os.environ["PATH"] = thu_muc + os.pathsep + os.environ.get("PATH", "")
        if which("ffmpeg"):
            return duong

    if not bat_buoc:
        return None

    sys.exit(
        "\n!!! KHONG TIM THAY FFMPEG tren may nay.\n"
        "    FFmpeg la bo cong cu cat/ghep/do am thanh — thieu no thi khong\n"
        "    lam duoc bat ky viec gi voi video.\n\n"
        "    Cach sua nhanh nhat — chay lenh nay roi thu lai:\n"
        "        python \"%s\"\n\n"
        "    (lenh do tu cai FFmpeg + kiem luon cac thu khac may can)\n"
        % os.path.join(os.path.dirname(os.path.abspath(__file__)), "chuan_bi_may.py"))

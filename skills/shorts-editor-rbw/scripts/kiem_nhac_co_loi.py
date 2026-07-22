# -*- coding: utf-8 -*-
"""
KIEM NHAC CO GIONG HAT HAY KHONG — bang may, khong phai doan theo ten file.

VI SAO CAN: luat 21/07/2026 (chon-kieu-dung.md, muc "Luat nhac theo muc phu giong")
quy dinh video Kieu 2/3 co giong dan xuyen suot thi nhac nen BAT BUOC KHONG LOI.
Luat cung ghi ro "khong chac thi NGHE KIEM truoc khi dung" — nhung Claude khong nghe
duoc, va doan theo ten file thi sai (folder "nhac khong ban quyen" van lan bai co loi).

CACH LAM: cho Whisper nghe vai doan cua bai, roi LOC BO cac cum Whisper hay BIA ra
khi khong co loi ("Thank you", "Bye", "*music*", "Hay subscribe cho kenh Ghien Mi Go"...).
Con lai chu co nghia = bai co giong hat that.

    BAY DA DINH THAT 21/07/2026: neu KHONG loc bo cum bia thi bai khong loi van tra ve
    day chu va bi cham nham la "co giong hat" — sai 6/6 bai trong lan chay dau tien.

DUNG:
    python kiem_nhac_co_loi.py "<file.mp3>" [file2.mp3 ...]
    python kiem_nhac_co_loi.py --folder "<thu muc chua mp3>"

IN RA moi bai 1 dong: KHONG LOI (dung duoc cho Nhom A) / CO GIONG HAT (chi dung Nhom B)
Thoat ma 1 neu co it nhat 1 bai co giong hat -> tien cho script khac goi.
"""
import argparse, os, re, subprocess, sys, io

# Bao dam goi ffmpeg/ffprobe chay duoc tren MOI may (them 22/07/2026).
# Thieu ffmpeg thi bao bang tieng nguoi, khong de vo voi 'WinError 2'.
try:
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from chung_ffmpeg import nap_ffmpeg
    nap_ffmpeg()
except ImportError:
    pass


if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

# Cum Whisper BIA ra khi KHONG co loi that (xem bang day du trong style-voice-karaoke.md)
CUM_BIA = [
    r"thank you", r"thanks for watching", r"\bbye\b", r"\byou\b", r"music",
    r"applause", r"please subscribe", r"subscribe", r"foreign",
    r"we'?ll be right back", r"stay tuned", r"see you next time",
    r"\bmmm?\b", r"\byeah\b", r"\bwee\b", r"\boh\b", r"\bah\b", r"\bla\b",
    r"hãy subscribe", r"ghiền mì gõ", r"không bỏ lỡ những video",
    r"cảm ơn các bạn đã theo dõi", r"đăng ký kênh", r"ủng hộ kênh",
]
# Ghi chu: nhom "mmm/yeah/wee/oh/ah/la" la VOCAL CHOP - nhieu ban nhac khong loi van co
# tieng nguoi ngan lam nhac cu. Loc ra vi chung KHONG phai loi hat ke chuyen.
# Neu muon nghiem ngat tuyet doi (khong chap nhan ca vocal chop) thi xoa dong do di.
RE_BIA = re.compile("|".join(CUM_BIA), re.I)


def tim_model():
    for p in (os.path.expanduser("~/.claude/roboworld-assets/models/ggml-large-v3-turbo.bin"),
              os.path.join(os.path.dirname(__file__), "..", "assets", "models",
                           "ggml-large-v3-turbo.bin")):
        if os.path.exists(p):
            return os.path.abspath(p)
    return None


def do_dai(p):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                        "-of", "csv=p=0", p], capture_output=True, text=True)
    try:
        return float(r.stdout.strip())
    except ValueError:
        return 0.0


def nghe(path, model, moc, dai=30):
    """Cho Whisper nghe 1 doan, tra ve chu CON LAI sau khi loc cum bia."""
    tmp = os.path.join(os.environ.get("TEMP", "."), "_kiemnhac.wav")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", str(moc), "-t", str(dai),
                    "-i", path, "-ac", "1", "-ar", "16000", tmp], check=True)
    mf = model.replace("\\", "/").replace(":", "\\:")
    r = subprocess.run(
        ["ffmpeg", "-v", "error", "-i", tmp,
         "-af", "whisper=model='%s':language=en:queue=3:destination=-:format=text" % mf,
         "-f", "null", "-"],
        capture_output=True, text=True, encoding="utf-8", errors="replace")
    raw = " ".join((r.stdout or "").split())
    sach = RE_BIA.sub(" ", raw)                      # bo cum bia
    sach = re.sub(r"[^\w\sÀ-ỹ]", " ", sach)          # bo dau cau
    return " ".join(w for w in sach.split() if len(w) > 1), raw


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="*")
    ap.add_argument("--folder")
    ap.add_argument("--nguong", type=int, default=40,
                    help="so ky tu co nghia toi thieu de coi la CO GIONG HAT (mac dinh 40)")
    ap.add_argument("--chi-tiet", action="store_true", help="in ca chu Whisper tra ve tho")
    a = ap.parse_args()

    ds = list(a.files)
    if a.folder:
        for f in sorted(os.listdir(a.folder)):
            if f.lower().endswith((".mp3", ".wav", ".m4a")):
                ds.append(os.path.join(a.folder, f))
    if not ds:
        print("Chua dua file nao. Dung --folder hoac liet ke file."); return 2

    model = tim_model()
    if not model:
        print("LOI: khong tim thay model Whisper (ggml-large-v3-turbo.bin).")
        print("     Xem huong dan tai trong assets/models/README.md"); return 2

    co_loi = False
    for p in ds:
        if not os.path.exists(p):
            print("%-52s -> KHONG TIM THAY FILE" % os.path.basename(p)[:50]); continue
        d = do_dai(p)
        # nghe 3 doan rai deu, tranh intro/outro
        mocs = [max(5, d * r) for r in (0.20, 0.45, 0.70)] if d > 60 else [max(0, d * 0.3)]
        giu, tho = [], []
        for m in mocs:
            s, raw = nghe(p, model, round(m, 1))
            if s:
                giu.append(s)
            tho.append(raw)
        con = " | ".join(giu)
        hat = len(con) >= a.nguong
        co_loi = co_loi or hat
        print("%-52s -> %s" % (os.path.basename(p)[:50],
                               "*** CO GIONG HAT ***" if hat else "khong loi (dung duoc)"))
        if con:
            print("      chu con lai sau khi loc: %s" % con[:160])
        if a.chi_tiet:
            for i, t in enumerate(tho):
                print("      [tho %d] %s" % (i + 1, t[:160]))

    print("\nNhom A (giong dan xuyen suot) chi duoc dung bai 'khong loi'.")
    print("Nhom B (giong chi 1-2 cau mo dau) dung bai nao cung duoc.")
    return 1 if co_loi else 0


if __name__ == "__main__":
    sys.exit(main())

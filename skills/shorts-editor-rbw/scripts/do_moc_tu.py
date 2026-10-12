# Do moc BAT DAU cua tung tu khoa trong file wav bang Whisper (khong can thu vien moi).
# Y tuong: cua so [s, s+WIN] "chua tron tu khoa" la DUNG khi s <= moc that, SAI khi s cat vao tu.
# => tim nhi phan s lon nhat con DUNG = moc bat dau tu. Sai so ~0.05s.
# Dung: python do_moc_tu.py <wav> <model.bin> "<tu khoa>" <uoc_tu> <uoc_den>
#   <wav>: am thanh ban DA CAT (chua tang toc), 16kHz mono. <model.bin>: ggml Whisper (vd ~/.claude/roboworld-assets/models/ggml-large-v3-turbo.bin)
#   uoc_tu/uoc_den: khoang chac chan bao quanh dau tu (lay tu srt queue=3).
# 🔴 Bat buoc NGHE LAI: cat [moc, moc+1.5s] cho Whisper nghe, cau phai BAT DAU bang tu khoa.
#   Moc nam sat mep khoang do -> nghi trung lan noi thu 2, do lai voi khoang hep hon.
#   Khong ra ket qua -> truot diem bat dau tung 0.1s, chon diem dau tien ma cau nghe duoc bat dau bang tu khoa.
#   ~30s/tu (7 lan goi Whisper). Ghi file tam _dm.wav/_dm.srt canh model.
import os, re, subprocess, sys, unicodedata
sys.stdout.reconfigure(encoding="utf-8")

WAV, MODEL = sys.argv[1], sys.argv[2]
WIN = 2.2


def norm(s):
    s = unicodedata.normalize("NFC", s.lower())
    return re.sub(r"[^\w\s]", " ", s).split()


def nghe(a, b):
    mdir, mname = os.path.split(MODEL)
    w = os.path.join(mdir, "_dm.wav"); srt = os.path.join(mdir, "_dm.srt")
    if os.path.exists(srt): os.remove(srt)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", "%.3f" % max(0, a), "-to", "%.3f" % b, "-i", WAV, w], check=True)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", "_dm.wav", "-af",
                    "whisper=model=%s:language=vi:queue=30:destination=_dm.srt:format=srt" % mname,
                    "-f", "null", "-"], check=True, cwd=mdir)
    t = open(srt, encoding="utf-8").read() if os.path.exists(srt) else ""
    return " ".join(l for l in t.splitlines() if l.strip() and "-->" not in l and not l.strip().isdigit())


def co_tu(text, kw):
    w, k = norm(text), norm(kw)
    return any(w[i:i + len(k)] == k for i in range(len(w) - len(k) + 1))


def tim(kw, lo, hi):
    # lo: diem chac chan TRUOC tu (cua so chua tu); hi: diem chac chan da QUA dau tu
    if not co_tu(nghe(lo, lo + WIN + (hi - lo)), kw):
        return None, "khong nghe thay tu trong khoang"
    for _ in range(6):
        mid = (lo + hi) / 2
        if co_tu(nghe(mid, mid + WIN), kw):
            lo = mid
        else:
            hi = mid
    return round(lo, 2), "ok"


if __name__ == "__main__":
    kw, a, b = sys.argv[3], float(sys.argv[4]), float(sys.argv[5])
    print(kw, *tim(kw, a, b))

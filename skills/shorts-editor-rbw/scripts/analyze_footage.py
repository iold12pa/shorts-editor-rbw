# -*- coding: utf-8 -*-
"""Phan tich footage v2: metadata + khung hinh THONG MINH (bat diem doi canh) + VOICE (Whisper) + index.json.

Usage:
    python analyze_footage.py <source_dir> <analysis_dir> [--max-frames 10] [--no-whisper] [--force]

Output:
    <analysis_dir>/footage_report.json      - metadata + moc doi canh + transcript tho
    <analysis_dir>/sheets/<clip>.jpg        - 1 anh luoi/clip (khung tai diem doi canh) de Claude Read
    <analysis_dir>/index.json               - chi muc chuan hoa; truong "content/tags/key_moments"
                                              de null cho Claude dien sau khi xem sheet.
                                              Clip da co trong index -> TU BO QUA (khong phan tich lai,
                                              tru khi --force).

Whisper (nhan dang giong noi trong footage):
    - Dung filter whisper cua ffmpeg 8.x. Model tim theo thu tu:
      ~/.claude/roboworld-assets/models/ggml-*.bin (cho ben) -> assets/models/ trong skill (cho cu).
    - Chua co model / ffmpeg thieu filter whisper -> bao RO va ghi has_speech=null ("chua nghe duoc",
      khac voi false = "nghe roi, khong co thoai"); chay lai khi du dieu kien se nghe bo sung.
"""
import glob
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

VIDEO_EXTS = {".mp4", ".mov", ".mts", ".m2ts", ".avi", ".mkv", ".webm", ".3gp", ".wmv"}
SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Model tim theo thu tu: cho luu ben (song sot khi go-cai-lai plugin) -> cho cu trong skill
MODEL_DIRS = [
    os.path.expanduser("~/.claude/roboworld-assets/models"),
    os.path.join(SKILL_DIR, "assets", "models"),
]
CONFIG_PATH = os.path.join(SKILL_DIR, "config.json")


def load_config():
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, encoding="utf-8") as f:
            return json.load(f)
    return {}


CONFIG = load_config()


def find_tool(name):
    p = shutil.which(name)
    if p:
        return p
    cfg_key = "%s_path" % name  # ffmpeg_path / ffprobe_path trong config.json
    cfg_path = (CONFIG.get(cfg_key) or "").strip()
    if cfg_path and os.path.exists(cfg_path):
        return cfg_path
    sys.exit(
        "Khong tim thay %s. Cai ffmpeg roi them vao PATH he thong, HOAC dien duong dan "
        "day du vao '%s' trong config.json (cung thu muc voi SKILL.md)." % (name, cfg_key))


FFMPEG, FFPROBE = find_tool("ffmpeg"), find_tool("ffprobe")


def run(cmd, timeout=600, cwd=None):
    return subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8",
                          errors="replace", timeout=timeout, cwd=cwd)


def probe(path):
    r = run([FFPROBE, "-v", "error", "-print_format", "json", "-show_format", "-show_streams", path])
    return json.loads(r.stdout) if r.returncode == 0 else None


def scene_times(path, duration, thr=0.2):
    """Moc thoi gian hinh anh doi dot ngot (doi canh/chuyen dong manh)."""
    # timeout theo do dai clip — clip dai >30 phut tung lam crash script vi tran 600s
    r = run([FFMPEG, "-i", path, "-vf", "select='gt(scene,%s)',showinfo" % thr, "-f", "null", "-"],
            timeout=max(600, int(duration * 6)))
    ts = [float(x) for x in re.findall(r"pts_time:([0-9.]+)", r.stderr)]
    return [t for t in ts if 0.3 < t < duration - 0.2]


def pick_times(duration, changes, max_frames):
    """Chon moc trich khung: uu tien diem doi canh (RAI DEU tren toan bo danh sach
    neu nhieu hon so slot — khong lay don dau video), lap day bang moc chia deu."""
    # clip ngan khong can nhieu khung — do bot chi phi doc sheet
    if duration < 8:
        max_frames = min(max_frames, 4)
    elif duration < 25:
        max_frames = min(max_frames, 6)
    uniq = sorted(set(round(t, 1) for t in changes))
    cap = max(1, max_frames - 2)
    if len(uniq) > cap:
        if cap == 1:
            times = [uniq[len(uniq) // 2]]
        else:
            idx = [round(i * (len(uniq) - 1) / (cap - 1)) for i in range(cap)]
            times = [uniq[i] for i in sorted(set(idx))]
    else:
        times = uniq[:]
    n_fill = max(3, max_frames - len(times))
    fill = [duration * (i + 0.5) / n_fill for i in range(n_fill)]
    for t in fill:
        if len(times) < max_frames and all(abs(t - x) > 1.5 for x in times):
            times.append(round(t, 1))
    return sorted(times)[:max_frames]


def extract_sheet(path, name, times, out_dir):
    """Trich khung tai cac moc -> ghep 1 anh luoi (toi da 12 o, 4 cot)."""
    # file tam de trong TEMP he thong — KHONG de trong out_dir (folder co the dang
    # duoc Google Drive/OneDrive sync: file tam vua sinh da xoa gay thong bao "items
    # removed" + Drive khoa file lam buoc ghep tile that bai)
    tmp = tempfile.mkdtemp(prefix="rbw_frames_")
    font = os.path.join(SKILL_DIR, "assets", "fonts", "Anton-Regular.ttf").replace("\\", "/")
    font = font[0] + "\\:" + font[2:] if re.match(r"^[A-Za-z]:", font) else font
    files = []
    for i, t in enumerate(times):
        fp = os.path.join(tmp, "f_%02d.jpg" % i)
        vf = "scale=280:-2,drawtext=fontfile='%s':text='%.1fs':x=8:y=8:fontsize=28:fontcolor=yellow:box=1:boxcolor=black@0.6" % (font, t)
        r = run([FFMPEG, "-v", "error", "-ss", "%.2f" % t, "-i", path, "-frames:v", "1",
                 "-vf", vf, "-q:v", "5", "-y", fp])
        if r.returncode != 0:  # drawtext loi (font/filter) -> thu lai khong co nhan thoi gian
            r = run([FFMPEG, "-v", "error", "-ss", "%.2f" % t, "-i", path, "-frames:v", "1",
                     "-vf", "scale=280:-2", "-q:v", "5", "-y", fp])
        if r.returncode == 0 and os.path.exists(fp):
            files.append(fp)
    if not files:
        shutil.rmtree(tmp, ignore_errors=True)
        return None
    sheets = os.path.join(out_dir, "sheets")
    os.makedirs(sheets, exist_ok=True)
    lst = os.path.join(tmp, "list.txt")
    with open(lst, "w", encoding="utf-8") as f:
        for fp in files:
            f.write("file '%s'\n" % fp.replace("\\", "/"))
    cols = 4 if len(files) > 6 else 3
    rows = (len(files) + cols - 1) // cols
    out = os.path.join(sheets, name + ".jpg")
    run([FFMPEG, "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", lst,
         "-vf", "tile=%dx%d:padding=4:color=black" % (cols, rows), "-frames:v", "1", "-update", "1", out])
    shutil.rmtree(tmp, ignore_errors=True)
    return out if os.path.exists(out) else None


def find_whisper_model():
    for d in MODEL_DIRS:
        if os.path.isdir(d):
            m = sorted(glob.glob(os.path.join(d, "ggml-*.bin")))
            if m:
                return m[0]
    return None


def whisper_filter_ok():
    """Kiem tra ffmpeg dang dung CO filter whisper khong (may dong nghiep hay dinh
    ban ffmpeg cu tren PATH de len ban moi -> nghe loi bi bo qua IM LANG)."""
    try:
        r = run([FFMPEG, "-hide_banner", "-filters"], timeout=60)
        return bool(re.search(r"\bwhisper\b", r.stdout or ""))
    except Exception:
        return False


def transcribe(path, model, out_dir, name, duration=0):
    """Whisper qua ffmpeg -> list {t0,t1,text}.
    Tra ve None neu LOI THAT (ffmpeg fail/khong ra file) — de index ghi "chua nghe duoc"
    thay vi ghi nham "khong co thoai"; tra [] chi khi nghe xong ma khong co loi nao."""
    tmpdir = tempfile.mkdtemp(prefix="rbw_whisper_")
    srt = os.path.join(tmpdir, "out.srt")
    mpath = model.replace("\\", "/")
    if re.match(r"^[A-Za-z]:", mpath):  # duong dan Windows trong filter: escape ':' VA boc nhay don
        mpath = "'" + mpath[0] + "\\:" + mpath[2:] + "'"
    r = run([FFMPEG, "-y", "-v", "error", "-i", os.path.abspath(path), "-vn",
             "-af", "whisper=model=%s:language=vi:queue=20:destination=out.srt:format=srt" % mpath,
             "-f", "null", "-"], timeout=max(1800, int(duration * 20)), cwd=tmpdir)
    if r.returncode != 0 or not os.path.exists(srt):
        err = (r.stderr or "").strip().splitlines()
        print("  [!] Whisper LOI o clip %s: %s" % (name, err[-1] if err else "khong ro"))
        shutil.rmtree(tmpdir, ignore_errors=True)
        return None
    segs = []
    txt = open(srt, encoding="utf-8", errors="replace").read()
    for m in re.finditer(r"(\d{2}):(\d{2}):(\d{2})[,.](\d{3}) --> (\d{2}):(\d{2}):(\d{2})[,.](\d{3})\s*\n(.*?)(?:\n\n|\Z)", txt, re.S):
        g = [int(x) for x in m.groups()[:8]]
        t0 = g[0] * 3600 + g[1] * 60 + g[2] + g[3] / 1000.0
        t1 = g[4] * 3600 + g[5] * 60 + g[6] + g[7] / 1000.0
        text = " ".join(m.group(9).split())
        # Loc ao giac Whisper (hay bia cau YouTube khi gap im lang/nhac): cau qua ngan
        # (<0.6s) hoac chua cum quang cao kenh dien hinh -> bo
        halluc = re.search(r"subscribe|đăng ký kênh|Ghiền Mì Gõ|cảm ơn.{0,10}đã (xem|theo dõi)", text, re.I)
        if text and (t1 - t0) >= 0.6 and not halluc:
            segs.append({"t0": round(t0, 2), "t1": round(t1, 2), "text": text})
    shutil.rmtree(tmpdir, ignore_errors=True)
    return segs


def mean_volume(path, duration=0):
    r = run([FFMPEG, "-i", path, "-af", "volumedetect", "-vn", "-f", "null", "-"],
            timeout=max(600, int(duration * 6)))
    m = re.search(r"mean_volume:\s*(-?[0-9.]+)", r.stderr)
    return float(m.group(1)) if m else None


def main():
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    src, dst = sys.argv[1], sys.argv[2]
    max_frames = int(sys.argv[sys.argv.index("--max-frames") + 1]) if "--max-frames" in sys.argv else 10
    use_whisper = "--no-whisper" not in sys.argv
    force = "--force" in sys.argv
    os.makedirs(dst, exist_ok=True)

    index_path = os.path.join(dst, "index.json")
    index = json.load(open(index_path, encoding="utf-8")) if os.path.exists(index_path) else {"clips": {}}

    model = find_whisper_model() if use_whisper else None
    if use_whisper and not model:
        print("[!] Chua co model Whisper (da tim: %s) -> phan voice se ghi 'chua nghe duoc',"
              " chay lai khi co model de nghe bo sung." % " ; ".join(MODEL_DIRS))
    if model and not whisper_filter_ok():
        print("[LOI] ffmpeg dang dung KHONG co filter whisper: %s\n"
              "      -> May nay co the dinh ban ffmpeg cu tren PATH de len ban moi (can ffmpeg 8.x"
              " ban full cua Gyan).\n"
              "      Phan nghe thoai se ghi 'chua nghe duoc' (KHONG ghi nham 'khong co thoai')."
              % FFMPEG)
        model = None

    clips = []
    for root, _d, files in os.walk(src):
        for f in sorted(files):
            if os.path.splitext(f)[1].lower() in VIDEO_EXTS:
                clips.append(os.path.join(root, f))
    if not clips:
        sys.exit("Khong thay video trong %s" % src)

    report, skipped, errors = [], 0, 0
    for path in clips:
        # Dinh danh bang duong dan TUONG DOI (2 the nho co the trung ten file DJI_0001.MP4 —
        # dinh danh theo ten file se ghi de sheet/index cua nhau -> nguy co cat nham file)
        rel = os.path.relpath(path, src).replace("\\", "/")
        size = os.path.getsize(path)
        key = "%s|%d" % (rel, size)
        legacy_key = "%s|%d" % (os.path.basename(path), size)
        if key not in index["clips"] and legacy_key != key and legacy_key in index["clips"]:
            # migration index cu (dinh danh theo ten file): doi key, GIU nguyen content/tags da dien
            index["clips"][key] = index["clips"].pop(legacy_key)
        # ten sheet theo duong dan tuong doi de 2 clip trung ten khong ghi de nhau
        name = re.sub(r"[^\w.\-]+", "_", os.path.splitext(rel)[0], flags=re.U)
        if not force and key in index["clips"]:
            old = index["clips"][key]
            sheet_ok = old.get("sheet") and os.path.exists(old["sheet"])
            speech_known = old.get("has_speech") is not None
            # bo qua khi: da co sheet VA (da nghe xong HOAC hien khong co model de nghe bo sung)
            if sheet_ok and (speech_known or not model):
                skipped += 1
                continue
        else:
            old = None
        try:
            info = probe(path)
            if not info:
                print("LOI  %s (ffprobe that bai)" % name)
                errors += 1
                continue
            v = next((s for s in info["streams"] if s["codec_type"] == "video"), {})
            a = next((s for s in info["streams"] if s["codec_type"] == "audio"), None)
            dur = float(info.get("format", {}).get("duration", 0) or 0)
            if old and old.get("sheet") and os.path.exists(old["sheet"]):
                changes = old.get("scene_changes", [])
                times = old.get("frame_times", [])
                sheet = old["sheet"]
            else:
                changes = scene_times(path, dur) if dur > 3 else []
                times = pick_times(dur, changes, max_frames)
                sheet = extract_sheet(path, name, times, dst)
            vol = old.get("mean_volume_db") if old else None
            if vol is None and a:
                vol = mean_volume(path, dur)
            # speech: list = da nghe xong (co the rong); None = CHUA nghe duoc (thieu model/loi)
            if old and old.get("transcript"):
                speech = old["transcript"]  # tai su dung transcript lan truoc, khoi nghe lai
            elif a is None or (vol is not None and vol <= -45):
                speech = []  # thuc su khong co tieng de nghe
            elif model:
                speech = transcribe(path, model, dst, name, dur)
            else:
                speech = None  # chua co model/filter -> danh dau "chua nghe duoc" de nghe bo sung sau
        except subprocess.TimeoutExpired:
            print("LOI  %s: qua gio xu ly (clip qua dai?) — bo qua, chay lai se thu tiep." % name)
            errors += 1
            continue
        except Exception as e:
            print("LOI  %s: %s — bo qua clip nay, chay lai se thu tiep." % (name, e))
            errors += 1
            continue
        entry = {
            "file": os.path.basename(path), "relpath": rel, "duration_s": round(dur, 1),
            "width": v.get("width"), "height": v.get("height"),
            "orientation": "doc" if (v.get("height") or 0) > (v.get("width") or 1) else "ngang",
            "has_audio": a is not None, "mean_volume_db": vol,
            "scene_changes": [round(t, 1) for t in changes],
            "frame_times": times, "sheet": sheet,
            "transcript": speech,
            "has_speech": (bool(speech) if speech is not None else None),
            # Claude dien sau khi Read sheet (giu lai neu lan truoc da dien):
            "content": old.get("content") if old else None,
            "tags": old.get("tags") if old else None,
            "key_moments": old.get("key_moments") if old else None,
            "quality": old.get("quality") if old else None,
        }
        index["clips"][key] = entry
        report.append(entry)
        # luu ngay sau moi clip -> bi ngat giua chung thi chay lai tu noi tiep
        json.dump(index, open(index_path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print("OK  %-38s %5.1fs  %d khung (%d diem doi canh)%s" % (
            name[:38], dur, len(times), len(changes),
            ("  speech: %d cau" % len(speech)) if speech else
            ("  speech: CHUA NGHE DUOC" if speech is None and a is not None else "")), flush=True)

    json.dump(index, open(index_path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    json.dump(report, open(os.path.join(dst, "footage_report.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    print("\nXong: %d clip moi, %d bo qua (da co index), %d LOI%s. Index: %s" % (
        len(report), skipped, errors,
        " (chay lai de thu tiep)" if errors else "", index_path))
    unheard = sum(1 for c in index["clips"].values() if c.get("has_speech") is None and c.get("has_audio"))
    if unheard:
        print("[!] %d clip CHUA NGHE DUOC thoai (thieu model/filter luc chay) — chay lai script"
              " sau khi model san sang de nghe bo sung, DUNG coi la 'khong co thoai'." % unheard)


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""MAT AI Gemini: cho cong cu "nhin" duoc noi dung 1 clip video (khong chi nghe tieng).

Gui clip len Gemini 2.5 Flash -> tra JSON: co robot khong, robot dong gi/dang lam gi,
boi canh, chat luong hinh, co nguoi dang noi khong, khoanh khac dang dung, mo ta + tags.
Bo sung dung phan Whisper con thieu (Whisper chi NGHE, Gemini NHIN).

Chi phi: ~150-200d/phut video (Gemini 2.5 Flash). Key doc tu ~/.claude/abs6-secrets.env.

Usage:
    python gemini_vision.py --video CLIP.mp4 [--model gemini-3.6-flash] [--json OUT.json]
                            [--update-index INDEX.json --key "relpath|size"]
"""
import argparse
import hashlib
import json
import os
import re
import sys
import time

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ENV_PATH = os.path.expanduser("~/.claude/abs6-secrets.env")
# CACHE THEO HASH (23/07/2026) — quet_mat_ai.py (quet ca folder) da tu cache qua
# index.json (bo qua clip da co truong "gemini"). Cong cu nay quet 1 clip LE nen
# khong di qua index — them cache rieng de goi lai cung 1 clip khong ton tien lan 2.
# Hash theo ten+kich thuoc+mtime (nhanh) chu khong hash noi dung file (cham voi clip lon).
CACHE_DIR = os.path.expanduser("~/.claude/roboworld-assets/cache/gemini_vision")

PROMPT = """Bạn là biên tập viên video marketing cho công ty robot Roboworld (phân phối robot
PUDU: robot phục vụ BellaBot, robot giao hàng, robot lễ tân, robot vệ sinh, T300...).
Xem kỹ clip này và trả về DUY NHẤT một object JSON (không giải thích thêm) với các trường:

{
  "co_robot": true/false,                // trong hình có robot không
  "robot_nhan_ra": "ten dong robot neu doan duoc, vd BellaBot / khong ro",
  "hanh_dong": "robot / nguoi dang lam gi (1 cau ngan)",
  "boi_canh": "noi chon: nha hang / nha may / kho / su kien / showroom...",
  "co_nguoi_dang_noi": true/false,       // co nguoi noi truoc camera (canh bao khi lam B-roll de voice)
  "chat_luong_hinh": "tot / kha / kem",
  "ly_do_chat_luong": "vd: net va on dinh / hoi rung / thieu sang / mo",
  "khoanh_khac_dang_dung": ["mo ta ngan khoanh khac noi bat, vd: robot bung do ra ban"],
  "nen_dung_lam_shorts": true/false,     // co dang highlight cho video ngan khong
  "ly_do": "vi sao nen/khong nen dung",
  "tu_khoa": ["3-6 tag ngan"],
  "mo_ta": "1 cau tom tat canh nay"
}

Chỉ trả JSON hợp lệ, tiếng Việt không dấu hay có dấu đều được."""


def load_key(name):
    if not os.path.exists(ENV_PATH):
        sys.exit("Khong thay file key: %s" % ENV_PATH)
    for line in open(ENV_PATH, encoding="utf-8", errors="replace"):
        line = line.strip()
        if line.startswith(name + "="):
            return line[len(name) + 1:].strip().strip('"').strip("'")
    sys.exit("Khong thay %s trong %s" % (name, ENV_PATH))


def video_cache_key(path, model):
    st = os.stat(path)
    raw = "%s|%d|%d|%s" % (os.path.abspath(path), st.st_size, int(st.st_mtime), model)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:24]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--video", required=True)
    ap.add_argument("--model", default="gemini-3.6-flash")
    ap.add_argument("--json")
    ap.add_argument("--update-index")
    ap.add_argument("--key")
    ap.add_argument("--no-cache", action="store_true")
    a = ap.parse_args()

    if not os.path.exists(a.video):
        sys.exit("Khong thay video: %s" % a.video)

    ckey = video_cache_key(a.video, a.model)
    cpath = os.path.join(CACHE_DIR, ckey + ".json")
    data = None
    if not a.no_cache and os.path.exists(cpath):
        data = json.load(open(cpath, encoding="utf-8"))
        print("CACHE (khong goi API — clip nay da quet truoc do, cung model): %s" % os.path.basename(a.video))

    if data is None:
        try:
            from google import genai
            from google.genai import types
        except ImportError:
            sys.exit("Chua cai SDK. Chay: python -m pip install google-genai")

        client = genai.Client(api_key=load_key("GEMINI_API_KEY"))

        size_mb = os.path.getsize(a.video) / 1e6
        print("Gui clip len Gemini (%.1f MB): %s" % (size_mb, os.path.basename(a.video)))
        f = client.files.upload(file=a.video)
        # cho Gemini xu ly xong video (PROCESSING -> ACTIVE)
        waited = 0
        while getattr(f.state, "name", str(f.state)) == "PROCESSING":
            time.sleep(2)
            waited += 2
            f = client.files.get(name=f.name)
            if waited > 300:
                sys.exit("Gemini xu ly video qua lau (>5 phut).")
        if getattr(f.state, "name", str(f.state)) == "FAILED":
            sys.exit("Gemini khong xu ly duoc video nay.")

        t0 = time.time()
        resp = client.models.generate_content(
            model=a.model,
            contents=[f, PROMPT],
            config=types.GenerateContentConfig(response_mime_type="application/json",
                                               temperature=0.2))
        dt = time.time() - t0
        try:
            client.files.delete(name=f.name)  # don file tam tren cloud
        except Exception:
            pass

        raw = (resp.text or "").strip()
        m = re.search(r"\{.*\}", raw, re.S)
        try:
            data = json.loads(m.group(0) if m else raw)
        except Exception:
            print("[!] Gemini tra ve khong phai JSON hop le:\n" + raw)
            return
        print("\n=== MAT AI GEMINI NHIN THAY (%.1fs) ===" % dt)
        try:
            os.makedirs(CACHE_DIR, exist_ok=True)
            json.dump(data, open(cpath, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        except Exception:
            pass  # cache la toi uu, loi ghi cache khong lam hong ket qua da co
    else:
        print("\n=== MAT AI GEMINI NHIN THAY (tu cache) ===")
    print(json.dumps(data, ensure_ascii=False, indent=2))

    if a.json:
        json.dump(data, open(a.json, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
        print("\nDa luu: %s" % a.json)

    # tuy chon: dien thang vao index.json cua analyze_footage (content/tags/quality/key_moments)
    if a.update_index and a.key and os.path.exists(a.update_index):
        idx = json.load(open(a.update_index, encoding="utf-8"))
        c = idx.get("clips", {}).get(a.key)
        if c is not None:
            c["content"] = data.get("mo_ta")
            c["tags"] = data.get("tu_khoa")
            c["quality"] = data.get("chat_luong_hinh")
            c["key_moments"] = data.get("khoanh_khac_dang_dung")
            c["gemini"] = data  # giu ban day du de tra cuu
            json.dump(idx, open(a.update_index, "w", encoding="utf-8"),
                      ensure_ascii=False, indent=1)
            print("Da cap nhat index cho clip: %s" % a.key)
        else:
            print("[!] Khong thay key '%s' trong index." % a.key)


if __name__ == "__main__":
    main()

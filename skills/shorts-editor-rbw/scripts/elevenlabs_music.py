# -*- coding: utf-8 -*-
"""Sinh nhac nen KHONG LOI bang ElevenLabs Music, do dung do dai video (option MO RONG).

Usage:
    python elevenlabs_music.py "<mo ta nhac, tieng Anh cang cu the cang tot>" <output.mp3> --length-ms <do_dai_ms>

Vi du:
    python elevenlabs_music.py "upbeat corporate tech, light percussion, optimistic" nhac.mp3 --length-ms 43000

LUAT SU DUNG (ghi trong SKILL.md):
    - Nhac mac dinh van la KHO RIENG cua Sep tren Drive. Script nay CHI dung khi:
      (a) nguoi dung chu dong yeu cau "nhac do ni theo video", HOAC
      (b) kho khong co bai hop VA nguoi dung dong y.
    - Goi Free se loi (Music can goi tra phi) -> DUNG BAO "can goi ElevenLabs tra phi",
      KHONG tu thay bang nguon nhac khac.
    - Quyen thuong mai cho video social doanh nghiep co tu goi Starter tro len
      (music-terms cua ElevenLabs).
- Key doc nhu elevenlabs_tts.py: bien moi truong ELEVENLABS_API_KEY hoac ~/.claude/abs6-secrets.env.
- Tinh phi ~900 credits/phut nhac — dung can nhac, sinh 1 lan cho ban duyet cuoi, dung sinh thu nhieu ban.
"""
import json
import os
import sys
import urllib.error
import urllib.request

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ENV_FILE = os.path.expanduser("~/.claude/abs6-secrets.env")


def get_api_key():
    key = os.environ.get("ELEVENLABS_API_KEY", "").strip()
    if not key and os.path.exists(ENV_FILE):
        for line in open(ENV_FILE, encoding="utf-8"):
            if line.strip().startswith("ELEVENLABS_API_KEY="):
                key = line.split("=", 1)[1].strip().strip('"').strip("'")
                break
    if not key:
        sys.exit("CHUA CO KEY: them dong ELEVENLABS_API_KEY=sk_... vao %s roi chay lai." % ENV_FILE)
    return key


def main():
    if len(sys.argv) < 3 or "--length-ms" not in sys.argv:
        sys.exit(__doc__)
    prompt, out_path = sys.argv[1], sys.argv[2]
    length_ms = int(sys.argv[sys.argv.index("--length-ms") + 1])
    if not (10000 <= length_ms <= 300000):
        sys.exit("length-ms phai trong khoang 10000-300000 (10s-5phut), dang la %d." % length_ms)

    req = urllib.request.Request(
        "https://api.elevenlabs.io/v1/music?output_format=mp3_44100_128",
        data=json.dumps({
            "prompt": prompt,
            "music_length_ms": length_ms,
            "force_instrumental": True,
        }).encode("utf-8"),
        headers={"xi-api-key": get_api_key(), "Content-Type": "application/json"},
        method="POST")
    try:
        with urllib.request.urlopen(req, timeout=300) as r:
            audio = r.read()
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", "replace")[:300]
        if e.code in (401, 402, 403):
            sys.exit("ElevenLabs Music loi HTTP %s — tinh nang nay CAN GOI TRA PHI"
                     " (Starter tro len; goi Free bi chan).\n-> DUNG BAO nguoi dung"
                     " 'can nang goi ElevenLabs', KHONG tu thay nguon nhac khac.\nChi tiet: %s"
                     % (e.code, body))
        sys.exit("ElevenLabs Music loi HTTP %s: %s" % (e.code, body))
    except urllib.error.URLError as e:
        sys.exit("ElevenLabs Music KHONG GOI DUOC (loi mang/DNS): %s -> kiem tra mang, chay lai." % e.reason)
    except (TimeoutError, OSError) as e:
        sys.exit("ElevenLabs Music QUA GIO/dut ket noi: %s -> thu lai 1 lan." % e)

    if not audio or (audio[:1] == b"{"):  # tra JSON thay vi mp3 = co loi bao trong body
        sys.exit("ElevenLabs Music tra ve bat thuong (khong phai file mp3): %s"
                 % audio[:300].decode("utf-8", "replace"))
    with open(out_path, "wb") as f:
        f.write(audio)
    print("OK  %s  (%.1f MB, dat hang %.1fs nhac khong loi)"
          % (out_path, len(audio) / 1048576, length_ms / 1000.0))


if __name__ == "__main__":
    main()

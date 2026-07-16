# -*- coding: utf-8 -*-
"""Sinh voiceover ElevenLabs cho shorts Roboworld + timestamp de lam sub karaoke.

Usage:
    python elevenlabs_tts.py <input_txt_utf8> <output_mp3> [--voice VOICE_ID] [--srt out.srt] [--words out.json]

- Doc API key tu bien moi truong ELEVENLABS_API_KEY, hoac tu file
  ~/.claude/abs6-secrets.env (dong ELEVENLABS_API_KEY=...) - duong dan tu
  gian ve thu muc nguoi dung tren MAY DANG CHAY, khong co dinh rieng cho 1 may.
- Goi endpoint /with-timestamps -> tra ve mp3 + timing TUNG KY TU.
- Xuat kem: .srt (cum 4-7 tu, cho sub thuong) va .json word-level (cho sub karaoke ASS).
- Het quota / loi mang -> bao ro va exit 1, de skill fallback sang edge-tts.
"""
import base64
import json
import os
import sys
import urllib.request

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ENV_FILE = os.path.expanduser("~/.claude/abs6-secrets.env")
# Giong mac dinh: "George" (nam, tram am) - model multilingual doc duoc tieng Viet.
# Doi giong: truyen --voice <id> (xem danh sach: https://elevenlabs.io/app/voice-library)
DEFAULT_VOICE = "JBFqnCBsd6RMkjVDRZzb"
MODEL = "eleven_multilingual_v2"


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


def chars_to_words(chars, starts, ends):
    """Gom timing ky tu -> tung tu."""
    words, cur, t0, t1 = [], "", None, None
    for ch, s, e in zip(chars, starts, ends):
        if ch.isspace():
            if cur:
                words.append({"word": cur, "start": round(t0, 3), "end": round(t1, 3)})
                cur, t0 = "", None
        else:
            if t0 is None:
                t0 = s
            cur += ch
            t1 = e
    if cur:
        words.append({"word": cur, "start": round(t0, 3), "end": round(t1, 3)})
    return words


def fmt_ts(t):
    h, m = divmod(int(t), 3600)
    m, s = divmod(m, 60)
    return "%02d:%02d:%02d,%03d" % (h, m, s, int((t - int(t)) * 1000))


def words_to_srt(words, per_group=6):
    lines = []
    for i in range(0, len(words), per_group):
        g = words[i:i + per_group]
        lines.append("%d\n%s --> %s\n%s\n" % (
            len(lines) + 1, fmt_ts(g[0]["start"]), fmt_ts(g[-1]["end"]),
            " ".join(w["word"] for w in g)))
    return "\n".join(lines)


def main():
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    txt_path, mp3_path = sys.argv[1], sys.argv[2]
    voice = sys.argv[sys.argv.index("--voice") + 1] if "--voice" in sys.argv else DEFAULT_VOICE
    srt_path = sys.argv[sys.argv.index("--srt") + 1] if "--srt" in sys.argv else None
    words_path = sys.argv[sys.argv.index("--words") + 1] if "--words" in sys.argv else None

    text = open(txt_path, encoding="utf-8").read().strip()
    if not text:
        sys.exit("File loi doc rong: %s" % txt_path)

    req = urllib.request.Request(
        "https://api.elevenlabs.io/v1/text-to-speech/%s/with-timestamps?output_format=mp3_44100_128" % voice,
        data=json.dumps({"text": text, "model_id": MODEL}).encode("utf-8"),
        headers={"xi-api-key": get_api_key(), "Content-Type": "application/json"},
        method="POST")
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            resp = json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", "replace")[:300]
        sys.exit("ElevenLabs loi HTTP %s: %s\n-> Kiem tra key/quota. Skill co the fallback edge-tts." % (e.code, body))

    with open(mp3_path, "wb") as f:
        f.write(base64.b64decode(resp["audio_base64"]))
    align = resp.get("alignment") or {}
    words = chars_to_words(
        align.get("characters", []),
        align.get("character_start_times_seconds", []),
        align.get("character_end_times_seconds", []))

    if words_path:
        json.dump(words, open(words_path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    if srt_path:
        open(srt_path, "w", encoding="utf-8").write(words_to_srt(words))
    dur = words[-1]["end"] if words else 0
    print("OK  %s  (%.1fs, %d tu)%s%s" % (
        mp3_path, dur, len(words),
        "  srt: %s" % srt_path if srt_path else "",
        "  words: %s" % words_path if words_path else ""))


if __name__ == "__main__":
    main()

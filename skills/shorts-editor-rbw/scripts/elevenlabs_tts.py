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

# ===== GIONG DOC — CAP NHAT 22/07/2026, DOC KY TRUOC KHI DOI =====
#
# 🔴 DINH CHINH LON 22/07/2026 — LUAT CU QUY SAI THU PHAM.
# Luat 20/07 ghi: "George doc tieng Viet meo VI DO LA GIONG ANH". Do thang lai bang
# cach doi TUNG MODEL doc tren CUNG mot giong, cho Whisper nghe lai:
#     cau goc: "Roboworld mang robot phục vụ tới nhà hàng của bạn."
#     eleven_multilingual_v2 -> "robot phúc vật hoàn hà hàn kòa bàn"   (MEO NANG)
#     eleven_turbo_v2_5      -> "robot phục vụ tới nhà hàng của bạn"   (CHUAN TUNG CHU)
#     eleven_flash_v2_5      -> chuan tung chu
# Cung giong do, chi doi model. => THU PHAM LA MODEL, khong phai giong.
# Voi turbo_v2_5 thi CA GIONG ANH cung doc ro tieng Viet (Adam: chuan 100%).
#
# ⚠️ GIOI HAN CUA PHEP DO NAY: Whisper chi do RO CHU, KHONG do CHAT GIONG TU NHIEN.
# Giong Anh doc tieng Viet van co the nghe ra chat Tay du tung chu deu ro. Chon giong
# cho video that van phai qua TAI SEP. Xem mau da xuat trong Desktop\NGHE-CHON-GIONG.
MODEL = "eleven_turbo_v2_5"   # KHONG lui ve multilingual_v2 — da do that, no lam meo tieng Viet

# --- Bang giong (do that 22/07/2026: CA 4 giong deu tao duoc, khong con bi chan) ---
GIONG_VIET_NAM = "7XOKiK112QRZRSLbCfMc"   # MC Xuan Tu - VIP (nam, giong Bac)
GIONG_VIET_NU = "Na15FlRRkMEDtEW4nVVP"    # Thanh Ngoc - Warm & Trusted (nu, giong Nam)
GIONG_PHUONG_UYEN = "Y9oZ1fkOxoaT3zFqTPzg"  # Phuong Uyen RBW (nu, VIET, giong NHAN BAN cua RBW)
GIONG_ADAM = "pNInz6obpgDQGcFmaJgB"       # Adam - Dominant, Firm (nam, goc Anh, chac & manh)
GIONG_ANH = "JBFqnCBsd6RMkjVDRZzb"        # George (nam, Anh)
DEFAULT_VOICE = GIONG_VIET_NAM

# HET BI CHAN (do lai 22/07/2026): truoc day goi Free chan giong library bang loi 402
# "Free users cannot use library voices via the API" — nay ca 4 giong deu tao duoc
# binh thuong. Ghi chu cu "cho nang goi Starter $6" khong con dung nua.
#
# 2 GIONG SEP HUY CHI DINH THEM 22/07/2026 (dung khi nguoi dung chon voice-over EL):
#   1) Phuong Uyen RBW - nu, tieng Viet, giong nhan ban cua chinh Roboworld
#   2) Adam            - nam, chac & manh
#   3) "Tuy noi dung"  - tu chon giong hop voi van ban (xem references/chon-kieu-dung.md)


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
        if e.code == 402:
            sys.exit(
                "ElevenLabs 402 — giong nay can GOI TRA PHI (giong Voice Library bi chan o goi Free).\n"
                "  Chi tiet: %s\n"
                "\n"
                "  DAY LA TINH HUONG DA BIET TRUOC, khong phai hong:\n"
                "  - Tai khoan cong ty DA CO 2 giong Viet: MC Xuan Tu (nam) va Thanh Ngoc (nu),\n"
                "    nang goi ElevenLabs la dung duoc ngay, khong phai di tim giong khac.\n"
                "  - Trong luc con goi Free: LUI VE edge-tts giong vi-VN-NamMinhNeural /\n"
                "    vi-VN-HoaiMyNeural (mien phi, doc cau tieng Viet thuan rat sach).\n"
                "  - TUYET DOI khong lui ve giong George: do la giong ANH, doc tieng Viet meo\n"
                "    ca cau thuong (da do that 20/07).\n"
                "  - Nho luat viet loi cho TTS: ten san pham/thuong hieu/thong so KHONG cho may\n"
                "    doc, day len the chu (xem style-voice-karaoke.md).\n"
                "  - Nguoi dung chi dinh DICH DANH 1 giong ma gap 402 -> DUNG BAO, cho ho quyet,\n"
                "    khong tu doi giong (luat SKILL.md)." % body)
        sys.exit("ElevenLabs loi HTTP %s: %s\n-> Kiem tra key/quota. Skill co the fallback edge-tts." % (e.code, body))
    except urllib.error.URLError as e:
        sys.exit("ElevenLabs KHONG GOI DUOC (loi mang/DNS/proxy): %s\n"
                 "-> Kiem tra mang roi chay lai; van loi thi fallback edge-tts theo luat SKILL.md." % e.reason)
    except (TimeoutError, OSError) as e:
        sys.exit("ElevenLabs QUA GIO/dut ket noi giua chung: %s\n"
                 "-> Thu chay lai 1 lan; van loi thi fallback edge-tts theo luat SKILL.md." % e)

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

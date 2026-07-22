# -*- coding: utf-8 -*-
"""Sinh voiceover ElevenLabs cho shorts Roboworld + timestamp de lam sub karaoke.

Usage:
    python elevenlabs_tts.py <input_txt_utf8> <output_mp3> [--voice VOICE_ID] [--srt out.srt] [--words out.json]

- Doc API key tu bien moi truong ELEVENLABS_API_KEY, hoac tu file
  ~/.claude/abs6-secrets.env (dong ELEVENLABS_API_KEY=...) - duong dan tu
  gian ve thu muc nguoi dung tren MAY DANG CHAY, khong co dinh rieng cho 1 may.
- Goi endpoint /with-timestamps -> tra ve mp3 + timing TUNG KY TU.
- Xuat kem: .srt (cum 4-7 tu, cho sub thuong) va .json word-level (cho sub karaoke ASS).
- Het quota / loi mang -> bao ro va exit 1. KHONG co giong thay the: edge-tts
  da bi bo 22/07/2026 (Sep Huy nghe mau, ket luan doc meo) -> DUNG BAO nguoi dung.
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
#
# VAI TRO — Sep Huy chot 22/07/2026: "giong Phuong Uyen chi la giong phu thoi,
# con lai 2 giong kia la giong chinh, cu hien ca 4 len cho ho chon".
#
# GIONG CHINH (mac dinh lay trong 2 giong nay):
GIONG_VIET_NAM = "7XOKiK112QRZRSLbCfMc"   # MC Xuan Tu - VIP (nam, giong Bac)   [CHINH]
GIONG_VIET_NU = "Na15FlRRkMEDtEW4nVVP"    # Thanh Ngoc (nu, giong Nam)          [CHINH]
# GIONG PHU (van hien du trong the chon, nhung KHONG tu lay lam mac dinh —
# chi dung khi nguoi dung chi dinh dich danh, hoac noi dung hop ro ret + noi ro ly do):
GIONG_PHUONG_UYEN = "Y9oZ1fkOxoaT3zFqTPzg"  # Phuong Uyen RBW (nu, VIET, nhan ban RBW) [PHU]
GIONG_ADAM = "pNInz6obpgDQGcFmaJgB"       # Adam - Dominant, Firm (nam, goc Anh)  [PHU]
GIONG_ANH = "JBFqnCBsd6RMkjVDRZzb"        # George (nam, Anh) - khong nam trong bang chon
DEFAULT_VOICE = GIONG_VIET_NAM            # mac dinh = giong CHINH

# HET BI CHAN (do lai 22/07/2026): truoc day goi Free chan giong library bang loi 402
# "Free users cannot use library voices via the API" — nay ca 4 giong deu tao duoc
# binh thuong. Ghi chu cu "cho nang goi Starter $6" khong con dung nua.
#
# BANG CHON GIONG hien du 4 lua chon + o "tuy noi dung", thu tu giong CHINH truoc:
#   1) MC Xuan Tu   [CHINH]   2) Thanh Ngoc [CHINH]
#   3) Phuong Uyen  [phu]     4) Adam       [phu]
#   -) "Tuy noi dung" - doc kich ban roi tu chon, UU TIEN 2 giong CHINH.
# Chi tiet cach chon + ly do: references/chon-kieu-dung.md, khoi "Chon giong doc".


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
                "  BAT THUONG — do lai 22/07/2026 thi CA 4 GIONG deu tao duoc, het bi chan:\n"
                "    Phuong Uyen / Adam / MC Xuan Tu / Thanh Ngoc.\n"
                "  - Gap 402 bay gio la dau hieu co chuyen khac (key doi, goi bi ha, giong bi go)\n"
                "    -> DUNG, BAO NGUOI DUNG, CHO QUYET. KHONG tu doi sang giong khac.\n"
                "  - KHONG CON PHUONG AN THAY THE: edge-tts da bi BO 22/07/2026 vi Sep Huy nghe\n"
                "    mau va ket luan DOC MEO. Dung lui ve edge-tts, cung dung lui ve George.\n"
                "  - Nho luat viet loi cho TTS: ten san pham/thuong hieu/thong so KHONG cho may\n"
                "    doc, day len the chu (xem style-voice-karaoke.md)." % body)
        sys.exit("ElevenLabs loi HTTP %s: %s\n"
                 "-> Kiem tra key/quota roi BAO NGUOI DUNG, cho quyet.\n"
                 "   Khong co giong thay the: edge-tts da bo 22/07/2026 vi doc meo." % (e.code, body))
    except urllib.error.URLError as e:
        sys.exit("ElevenLabs KHONG GOI DUOC (loi mang/DNS/proxy): %s\n"
                 "-> Kiem tra mang roi chay lai; van loi thi BAO NGUOI DUNG, cho quyet\n"
                 "   (khong con fallback edge-tts tu 22/07/2026)." % e.reason)
    except (TimeoutError, OSError) as e:
        sys.exit("ElevenLabs QUA GIO/dut ket noi giua chung: %s\n"
                 "-> Thu chay lai 1 lan; van loi thi BAO NGUOI DUNG, cho quyet\n"
                 "   (khong con fallback edge-tts tu 22/07/2026)." % e)

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

# -*- coding: utf-8 -*-
"""Cau noi Telegram <-> Claude Code cho skill shorts-editor-rbw (Kenh A).

Dong nghiep nhan tin/gui video cho bot Telegram -> bot goi CLI "claude" that
(qua subprocess, che do -p khong tuong tac) chay skill shorts-editor-rbw ->
tra loi/hoi lai + tu gui video/caption thanh pham qua dung Telegram. Moi
nguoi dung 1 session_id rieng (tu sinh UUID, luu vao sessions.json) -> noi
tiep dung cau chuyen ho da noi truoc do.

QUAN TRONG - da sua 2026-07-15 dem sau khi tu kiem tra:
  - KHONG dung goi "claude_agent_sdk" (ban dau tuong co, kiem tra bang pip
    trong 1 virtualenv sach thi KHONG TON TAI tren PyPI - agent nghien cuu
    truoc do bao sai). Chuyen sang goi thang CLI that qua subprocess.
  - Da tu chay thu "claude.exe -p ... --session-id ..." that -> loi
    "Not logged in". Phien chat Claude Desktop cua Sep dung co che dang nhap
    RIENG, KHONG tu dong ap dung cho 1 tien trinh claude.exe moi goi qua
    subprocess. BAT BUOC Sep phai tu chay 1 lan: claude setup-token (sinh
    token dang nhap dai han) TRUOC khi bot nay chay duoc - xem README.md.

CHUA TEST THAT DAU CUOI (chua co bot token + chua co token dang nhap luc
viet code nay) - xem README.md truoc khi chay lan dau.

Usage:
    python bot.py
"""
import asyncio
import glob
import json
import logging
import os
import re
import shutil
import subprocess
import sys
import uuid

from telegram import Update
from telegram.ext import Application, MessageHandler, ContextTypes, filters

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("rbw-bot")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(BASE_DIR, "config.json")
SESSIONS_PATH = os.path.join(BASE_DIR, "sessions.json")
WORKSPACES_DIR = os.path.join(BASE_DIR, "workspaces")  # 1 folder rieng/nguoi dung, tranh dam vao nhau
CLAUDE_TIMEOUT_S = 900  # video dai/Whisper co the mat vai phut, cho rong rai

# Bao Claude luon ket thuc bang 1 dong may-doc-duoc liet ke file thanh pham
# vua tao (video final + caption) de bot tu dinh kem gui lai qua Telegram -
# khong dung cach do thu muc truoc/sau vi workspace thuc te (Edit video root)
# nam ngoai folder rieng cua bot, dung chung cho moi nguoi dung.
DELIVERABLE_INSTRUCTION = (
    "Khi ban da DUNG XONG va BAN GIAO video (xuat file .mp4 + caption .md o "
    "buoc 5 cua SKILL.md), LUON ket thuc cau tra loi bang 1 dong RIENG dung "
    "dinh dang chinh xac: RBW_FILES: <duong dan tuyet doi 1>|<duong dan "
    "tuyet doi 2>|... (liet ke DUNG cac file .mp4 va .md vua tao trong buoc "
    "nay, cach nhau boi ky tu |). Neu tin nhan nay khong lien quan toi ban "
    "giao file (vd dang hoi lai thong tin) thi KHONG duoc them dong nay."
)
FILES_LINE_RE = re.compile(r"^RBW_FILES:\s*(.+)$", re.MULTILINE)


def load_config():
    if not os.path.exists(CONFIG_PATH):
        sys.exit(
            "CHUA CO config.json. Copy config.json.example thanh config.json roi dien "
            "bot_token (xem README.md muc 'Lay bot token')."
        )
    with open(CONFIG_PATH, encoding="utf-8") as f:
        return json.load(f)


def load_sessions():
    if os.path.exists(SESSIONS_PATH):
        with open(SESSIONS_PATH, encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_sessions(sessions):
    with open(SESSIONS_PATH, "w", encoding="utf-8") as f:
        json.dump(sessions, f, ensure_ascii=False, indent=1)


CONFIG = load_config()
SESSIONS = load_sessions()  # { "<telegram_chat_id>": "<claude_session_id_da_dung_lan_dau>" }
ALLOWED_USERS = set(str(u) for u in (CONFIG.get("allowed_user_ids") or []))
OAUTH_TOKEN = (CONFIG.get("claude_oauth_token") or "").strip()


def subprocess_env():
    """claude.exe goi qua subprocess KHONG tu ke thua dang nhap cua phien
    Claude Desktop - phai tu truyen token dai han (sinh boi `claude
    setup-token`) qua bien moi truong CLAUDE_CODE_OAUTH_TOKEN moi lan goi."""
    env = os.environ.copy()
    if OAUTH_TOKEN and not OAUTH_TOKEN.startswith("DIEN_"):
        env["CLAUDE_CODE_OAUTH_TOKEN"] = OAUTH_TOKEN
    return env


def find_claude_binary():
    """Uu tien PATH he thong (portable nhat). Neu khong co, tu do ban Claude
    Code di kem Claude Desktop (Windows) - KHONG hardcode so phien ban vi
    app tu cap nhat, luon lay ban moi nhat tim thay. Cuoi cung cho phep ghi
    de qua config.json neu may nao cai kieu khac."""
    p = shutil.which("claude")
    if p:
        return p
    pattern = os.path.expandvars(r"%APPDATA%\Claude\claude-code\*\claude.exe")
    candidates = sorted(glob.glob(pattern), key=os.path.getmtime, reverse=True)
    if candidates:
        return candidates[0]
    cfg_path = (CONFIG.get("claude_binary_path") or "").strip()
    if cfg_path and os.path.exists(cfg_path):
        return cfg_path
    return None


CLAUDE_BIN = find_claude_binary()


def check_claude_ready():
    """Kiem tra truoc khi bot nhan tin nhan dau tien: co tim thay claude.exe
    khong, va token dang nhap dai han (CLAUDE_CODE_OAUTH_TOKEN, sinh boi
    `claude setup-token`) co dung khong. KHONG dung `claude auth status` -
    lenh do kiem tra kieu dang nhap tuong tac (Desktop), khong phan anh dung
    token nay; phai tu goi thu 1 cau that moi biet token co chay duoc khong.
    Bao loi ro ngay tu dau thay vi de moi tin nhan cua nguoi dung deu loi am
    tham."""
    if not CLAUDE_BIN:
        sys.exit(
            "Khong tim thay claude.exe (khong co tren PATH, khong thay trong "
            "%APPDATA%\\Claude\\claude-code\\, config.json cung chua co "
            "'claude_binary_path'). Xem README.md muc cai dat."
        )
    log.info("Dung claude.exe tai: %s", CLAUDE_BIN)
    if not OAUTH_TOKEN or OAUTH_TOKEN.startswith("DIEN_"):
        sys.exit(
            "config.json chua co 'claude_oauth_token' hop le. Sep can tu chay 1 lan "
            'trong PowerShell: & "%s" setup-token — copy chuoi token dai in ra man '
            "hinh, dan vao config.json muc 'claude_oauth_token'. Xem README.md." % CLAUDE_BIN
        )
    log.info("Dang tu goi thu claude.exe bang token de xac nhan hoat dong that...")
    try:
        r = subprocess.run(
            [CLAUDE_BIN, "-p", "ping", "--output-format", "json"],
            capture_output=True, text=True, encoding="utf-8", errors="replace",
            timeout=60, env=subprocess_env(),
        )
    except subprocess.TimeoutExpired:
        sys.exit("Goi thu claude.exe qua 60s khong xong - kiem tra mang/token roi thu lai.")
    try:
        data = json.loads(r.stdout)
    except json.JSONDecodeError:
        sys.exit(
            "Goi thu claude.exe that bai (token co the sai/het han).\nstdout=%r\nstderr=%r\n"
            "Chay lai 'claude setup-token' de lay token moi." % (r.stdout[:500], r.stderr[:500])
        )
    if data.get("is_error"):
        sys.exit("Goi thu claude.exe bao loi: %s" % data.get("result"))
    log.info("Token hop le, claude.exe san sang.")
    if not ALLOWED_USERS:
        log.warning(
            "!!! config.json chua co 'allowed_user_ids' -> bot dang tra loi "
            "BAT KY AI nhan tin, khong gioi han. Xem log de lay user id roi "
            "dien vao config.json de khoa lai."
        )
    else:
        log.info("Danh sach duoc phep dung bot: %s", ", ".join(sorted(ALLOWED_USERS)))


def workspace_for(chat_id):
    """Moi nguoi dung Telegram rieng 1 thu muc lam viec (dung lam cwd cho
    claude.exe) - tranh dam vao nhau va tranh anh huong toi cac session
    Claude Code khac dang mo tren may Sep. Luu y: day chi la noi claude.exe
    KHOI DONG - skill van doc/ghi vao edit_video_root dung chung theo cau
    hinh cua skill, khong bi gioi han trong folder nay."""
    d = os.path.join(WORKSPACES_DIR, str(chat_id))
    os.makedirs(d, exist_ok=True)
    return d


def is_allowed(update: Update):
    uid = str(update.effective_user.id)
    if not ALLOWED_USERS:
        log.info(
            "Tin nhan tu user_id=%s username=@%s ten=%s (chua khoa allowed_user_ids, dang cho qua).",
            uid, update.effective_user.username, update.effective_user.full_name,
        )
        return True  # chua cau hinh -> tam cho qua, da canh bao lon luc khoi dong
    if uid in ALLOWED_USERS:
        return True
    log.warning(
        "Chan nguoi la: user_id=%s username=@%s ten=%s — them user_id nay vao "
        "'allowed_user_ids' trong config.json neu muon cho phep.",
        uid, update.effective_user.username, update.effective_user.full_name,
    )
    return False


def ask_claude(chat_id, user_text):
    """Goi claude.exe che do -p (khong tuong tac) cho dung phien cua nguoi
    nay - lan dau tu sinh 1 session_id moi (--session-id), cac lan sau noi
    tiep bang --resume dung session_id do. Tra ve (text_hien_thi, list_file_dinh_kem, loi_hay_khong).
    Chay dong bo (subprocess.run) - python-telegram-bot tu chay ham nay trong
    thread rieng qua run_in_executor nen khong chan cac nguoi dung khac."""
    key = str(chat_id)
    existing_sid = SESSIONS.get(key)
    cmd = [
        CLAUDE_BIN, "-p", user_text,
        "--output-format", "json",
        "--permission-mode", "acceptEdits",  # bot chay khong nguoi giam sat, tu dong chap nhan sua file
        "--append-system-prompt", DELIVERABLE_INSTRUCTION,
    ]
    if existing_sid:
        cmd += ["--resume", existing_sid]
        new_sid = existing_sid
    else:
        new_sid = str(uuid.uuid4())
        cmd += ["--session-id", new_sid]

    try:
        r = subprocess.run(
            cmd, cwd=workspace_for(chat_id), capture_output=True, text=True,
            encoding="utf-8", errors="replace", timeout=CLAUDE_TIMEOUT_S,
            env=subprocess_env(),
        )
    except subprocess.TimeoutExpired:
        return ("Việc này mất quá lâu (>%d phút), có thể do xử lý video dài. "
                "Thử lại hoặc báo quản trị viên." % (CLAUDE_TIMEOUT_S // 60)), [], True

    try:
        data = json.loads(r.stdout)
    except json.JSONDecodeError:
        log.error("claude.exe tra ve khong phai JSON hop le. stdout=%r stderr=%r", r.stdout[:500], r.stderr[:500])
        return "Có lỗi kỹ thuật khi xử lý (phản hồi không đúng định dạng). Báo quản trị viên kèm giờ nhắn tin này nhé.", [], True

    SESSIONS[key] = data.get("session_id") or new_sid
    save_sessions(SESSIONS)

    if data.get("is_error"):
        log.error("claude.exe bao loi cho chat_id=%s: %s", chat_id, data.get("result"))
        return "Có lỗi khi xử lý: %s" % data.get("result", "(không rõ)"), [], True

    text = data.get("result") or "(Claude không trả về nội dung)"
    files = []
    m = FILES_LINE_RE.search(text)
    if m:
        text = text[:m.start()].rstrip()  # bo dong RBW_FILES: khoi tin nhan hien thi cho nguoi dung
        for p in m.group(1).split("|"):
            p = p.strip()
            if p and os.path.exists(p):
                files.append(p)
            elif p:
                log.warning("Claude bao file '%s' nhung khong thay tren dia — bo qua.", p)
    return text, files, False


async def send_reply(update, text, files):
    if text:
        await update.message.reply_text(text)
    for path in files:
        try:
            ext = os.path.splitext(path)[1].lower()
            with open(path, "rb") as f:
                if ext == ".mp4":
                    await update.message.reply_video(f, filename=os.path.basename(path))
                else:
                    await update.message.reply_document(f, filename=os.path.basename(path))
        except Exception:  # noqa: BLE001 - 1 file loi khong duoc lam mat cac file con lai
            log.exception("Gui file that bai: %s", path)
            await update.message.reply_text("(Không gửi được file: %s — file có thể quá lớn cho Telegram)" % os.path.basename(path))


async def on_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_allowed(update):
        await update.message.reply_text("Xin lỗi, bạn chưa được cấp quyền dùng bot này. Liên hệ quản trị viên nhé.")
        return
    chat_id = update.effective_chat.id
    text = update.message.text or ""
    await context.bot.send_chat_action(chat_id=chat_id, action="typing")
    reply, files, _is_error = await asyncio.get_running_loop().run_in_executor(None, ask_claude, chat_id, text)
    await send_reply(update, reply, files)


async def on_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Video/anh gui truc tiep qua Telegram (footage nho). Footage buoi quay
    lon (nhieu GB) KHONG gui qua day duoc - Telegram gioi han dung luong bot
    tai ve (~20MB), nguoi dung phai upload Drive roi gui LINK qua tin nhan
    chu (xu ly o on_text)."""
    if not is_allowed(update):
        await update.message.reply_text("Xin lỗi, bạn chưa được cấp quyền dùng bot này. Liên hệ quản trị viên nhé.")
        return
    chat_id = update.effective_chat.id
    doc = update.message.document or update.message.video or (
        update.message.photo[-1] if update.message.photo else None)
    if doc is None:
        return
    file = await context.bot.get_file(doc.file_id)
    fname = getattr(doc, "file_name", None) or ("%s.mp4" % doc.file_id)
    dest = os.path.join(workspace_for(chat_id), fname)
    await file.download_to_drive(dest)
    caption = update.message.caption or ""
    note = "Đã nhận file, lưu tại: %s. %s" % (dest, caption)
    await context.bot.send_chat_action(chat_id=chat_id, action="typing")
    reply, files, _is_error = await asyncio.get_running_loop().run_in_executor(None, ask_claude, chat_id, note)
    await send_reply(update, reply, files)


def main():
    token = CONFIG.get("bot_token", "").strip()
    if not token or token.startswith("DIEN_"):
        sys.exit("config.json chua dien bot_token that. Xem README.md.")
    check_claude_ready()
    os.makedirs(WORKSPACES_DIR, exist_ok=True)
    app = (
        Application.builder().token(token)
        .connect_timeout(30)  # mang co the chap chon - mac dinh qua ngan, gay ConnectTimeout gia
        .read_timeout(30)
        .write_timeout(30)
        .build()
    )
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, on_text))
    app.add_handler(MessageHandler(filters.Document.ALL | filters.VIDEO | filters.PHOTO, on_file))
    log.info("Bot dang chay — bam Ctrl+C de dung.")
    app.run_polling()


if __name__ == "__main__":
    main()

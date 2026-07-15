# Giao diện Telegram cho Shorts Editor ROBOWORLD (tùy chọn, cài trên MÁY BẠN)

Nếu bạn thấy nhắn tin qua Telegram tiện hơn mở Claude Code gõ tay (đặc biệt lúc đang ở ngoài, dùng điện thoại), có thể tự cài "cầu nối" này — **chạy hoàn toàn trên máy của chính bạn**, xử lý video bằng đúng Claude Code + skill đã cài trên máy bạn, footage của ai người đó tự lo, không phụ thuộc máy ai khác phải bật.

**Bắt buộc phải làm xong trước**: cài Claude Code + skill `shorts-editor-rbw` trên máy bạn theo hướng dẫn ở `../README.md` (thư mục cha) trước — cầu nối này chỉ là lớp giao diện Telegram phủ lên trên, không thay thế được.

## ⚠️ Trạng thái thật: đã tự kiểm tra từng phần, CHƯA chạy thử đầu-cuối

Xem chi tiết trong code `bot.py` (phần comment đầu file) — đã sửa 1 lỗi kiến trúc lớn (gói phần mềm ban đầu dùng không tồn tại, đã đổi sang gọi thẳng chương trình `claude` thật), đã tự test riêng từng mảnh (dò đường dẫn, gọi lệnh, tách file đính kèm). Ai là người đầu tiên cài thật sẽ cần báo lại lỗi nếu có.

## Bước 0 — Đăng nhập cho bot (làm 1 lần trên máy bạn)

Khi bạn mở app Claude Desktop để chat, nó tự đăng nhập theo cách riêng. Nhưng khi bot này gọi chương trình `claude` như 1 chương trình độc lập (để tự động hóa), nó KHÔNG tự có sẵn đăng nhập đó — cần 1 "token dài hạn" riêng (cần tài khoản Claude có subscription). Mở PowerShell:

```powershell
# Vao thu muc chua claude.exe (thay <phien ban> bang ten folder so ban thay trong do)
& "$env:APPDATA\Claude\claude-code\<phien ban>\claude.exe" setup-token
```

Làm theo hướng dẫn trên màn hình. Xong bước này bot mới gọi được Claude trên máy bạn.

## Bước 1 — Tạo bot Telegram CỦA RIÊNG BẠN (mỗi người 1 bot, không dùng chung)

1. Mở Telegram, tìm chat với **@BotFather**
2. Gõ `/newbot`, đặt tên riêng cho bot của bạn (ví dụ "Huy Shorts Bot")
3. BotFather trả về 1 chuỗi dài dạng `123456:ABC-DEF...` — đó là **bot token** của riêng bạn, giữ bí mật như mật khẩu

## Bước 2 — Cài đặt (máy bạn cần BẬT khi muốn xử lý video qua Telegram)

```powershell
cd "<đường dẫn tới folder telegram-bot này trên máy bạn>"
pip install -r requirements.txt
Copy-Item config.json.example config.json
# Mở config.json, dán bot token vào, lưu lại
python bot.py
```

Nếu báo "claude.exe TIM THAY nhung CHUA DANG NHAP" → quay lại Bước 0. Nếu báo "Khong tim thay claude.exe" → mở `config.json`, điền đường dẫn đầy đủ tới `claude.exe` vào `claude_binary_path`.

Thấy dòng `Bot dang chay — bam Ctrl+C de dung.` là bot đã hoạt động. Mở Telegram, nhắn thử cho chính bot bạn vừa tạo.

## Cách hoạt động

- Đây là bot **CÁ NHÂN** — chỉ chạy khi máy bạn bật, chỉ xử lý bằng dữ liệu/footage trên máy bạn. Không liên quan gì tới máy đồng nghiệp khác hay máy admin.
- Nhắn tin nhiều lần liên tiếp → bot nhớ đúng ngữ cảnh cuộc trò chuyện trước đó
- Khi Claude dựng xong video, bot tự động gửi kèm file .mp4 + caption .md ngược lại qua Telegram
- Mặc định `allowed_user_ids` trong config.json nên chỉ điền đúng `user_id` Telegram của chính bạn (bot cá nhân, không cần cho người khác dùng) — cách lấy: nhắn thử bot 1 câu, xem log dòng `Chan nguoi la: user_id=...`, copy số đó điền vào
- Muốn chạy nền không cần mở PowerShell tay: chạy `.\install_task.ps1` sau khi đã thử ổn định bằng tay

## Cập nhật khi admin sửa skill

Vì code này nằm CHUNG kho GitHub với skill, mỗi lần cập nhật plugin (`/plugin marketplace update` hoặc tự động khi mở lại Claude) cũng đồng thời tải bản `bot.py` mới nhất — nếu đang chạy bot nền thì khởi động lại (`Ctrl+C` rồi `python bot.py` lại, hoặc restart task đã đăng ký) để áp dụng bản mới.

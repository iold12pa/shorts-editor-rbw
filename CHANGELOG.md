# Nhật ký cập nhật — shorts-editor-rbw

File này ghi lại các thay đổi đáng chú ý theo ngày, mới nhất ở trên cùng. Xem chi tiết đầy đủ từng thay đổi bằng lịch sử commit trên GitHub.

## 2026-07-16
- **Tự động hoá cài đặt hoàn toàn**: skill tự cài FFmpeg (winget), tự tải model Whisper (~1.6GB), tự bật auto-update cho marketplace ngay lần đầu được gọi — người dùng không phải cài tay bất kỳ thứ gì ngoài 2 lệnh cài plugin ban đầu.
- **Hỏi phiên bản = kiểm tra GitHub thật**: khi người dùng hỏi "đang bản nào / có bản mới không", skill tự chạy lệnh cập nhật rồi báo số bản thực tế, không trả lời suông theo bản đang nằm trên máy.
- **Chính sách không tạo file backup** khi sửa `settings.json` (quyết định của chủ repo, có ghi rõ lý do trong SKILL.md) — kèm tự dọn file `.bak` cũ nếu gặp.
- **Bỏ cấu hình thư mục cố định**: người dùng đưa đường dẫn đầy đủ (hoặc kéo-thả folder) mỗi lần dựng video — cài xong dùng ngay, không có bước chọn thư mục.
- **Đóng gói tài nguyên dùng chung** (logo, outro, nhạc, SFX, ảnh sản phẩm — ~104MB) vào plugin — mọi máy có sẵn giống hệt nhau, tự cập nhật cùng skill.
- **Repo chuyển sang public** — bỏ toàn bộ bước mời collaborator + đăng nhập git.
- Sửa lệch cỡ chữ ASS trong ffmpeg-recipes (mẫu cũ 100/66pt → chuẩn đã duyệt 135/90pt).
- Xác nhận đầu-cuối thành công trên máy người dùng thật đầu tiên (Cao Đắc Chiến).

## 2026-07-15
- Đóng gói skill thành Claude Code Plugin, đưa lên GitHub.
- Chốt khung 3 KIỂU DỰNG (highlight+nhạc / theo thoại sẵn / ghép cảnh+voice-over) thay hệ ①②③④ cũ.
- Rút quy tắc chọn cảnh từ đối chiếu source thô ↔ video final thật (`chon-canh-highlight.md`).
- Bộ Telegram bot cá nhân (tùy chọn) — mỗi người tự cài trên máy mình.

# Shorts Editor ROBOWORLD — gói cài cho đồng nghiệp

Skill Claude Code giúp dựng shorts video Roboworld tự động từ footage buổi quay, theo đúng phong cách công ty (học từ hàng chục video mẫu thật). Hỏi bạn chọn 1 trong 3 kiểu dựng, kiểm tra đủ nguyên liệu, đề xuất kịch bản cho duyệt, rồi tự dựng bằng ffmpeg.

## Cài đặt (máy đã có Claude Code)

1. Thêm marketplace này (thay `<đường-dẫn-hoặc-link>` bằng đường dẫn folder này hoặc link Git repo khi đã đưa lên):
   ```
   /plugin marketplace add <đường-dẫn-hoặc-link>
   ```
2. Cài plugin:
   ```
   /plugin install shorts-editor-rbw@roboworld-tools
   ```
3. **Tải model Whisper riêng** (bắt buộc nếu muốn dùng Kiểu 2/3 — video có thoại): xem hướng dẫn trong `skills/shorts-editor-rbw/assets/models/README.md`.
4. Mở file `skills/shorts-editor-rbw/config.json` (trong thư mục plugin đã cài, thường ở `~/.claude/plugins/cache/...`), điền đúng đường dẫn folder chứa footage của bạn vào `edit_video_root`.
5. Muốn nhận cập nhật mới nhất mỗi lần mở Claude: vào `/plugin` → tab **Marketplaces** → bật auto-update cho `roboworld-tools` (mặc định TẮT với marketplace không phải của Anthropic).

## Dùng thử

Mở Claude Code, gõ tự nhiên kiểu: *"dựng video từ folder [tên buổi quay]"* — skill sẽ tự hỏi bạn chọn kiểu dựng + xin thông tin còn thiếu.

## Lưu ý quan trọng

- **Đây là bản đóng gói đầu tiên, CHƯA được cài thử end-to-end** — trước khi gửi cho đồng nghiệp, nên tự cài thử trên 1 máy khác (hoặc máy ảo) để chắc luồng `/plugin marketplace add` → `/plugin install` chạy đúng như tài liệu Claude Code mô tả.
- Mỗi người dùng cần: (a) `config.json` riêng trỏ đúng folder footage của họ, (b) model Whisper riêng nếu cần Kiểu 2/3, (c) file key ElevenLabs riêng ở `~/.claude/abs6-secrets.env` nếu muốn dùng giọng AI (không bắt buộc).

# Assets của skill

## Có sẵn trong gói cài
- `fonts/Anton-Regular.ttf` — font Anton (Google Fonts, hỗ trợ tiếng Việt) dùng cho mọi text đè. Đừng xóa.
- `models/` — chỗ chứa model Whisper THEO KIỂU CŨ (xem `models/README.md`). Máy cài mới: model tải về chỗ bền `~/.claude/roboworld-assets/models/` thay vì vào đây.

## KHÔNG còn nằm trong gói cài (từ 2026-07-17)
Kho tài nguyên dùng chung (logo, outro, nhạc, SFX, ảnh sản phẩm) **đã chuyển ra Google Drive của Sếp** — không đóng gói trong repo nữa để: (a) cài plugin nhẹ và nhanh, (b) Sếp thêm nhạc/logo mới chỉ cần kéo file vào Drive, mọi máy gõ "cập nhật kho tài nguyên" là có, không cần qua GitHub.

- Chỗ lưu trên máy (tải 1 lần, bền qua gỡ-cài-lại): `~/.claude/roboworld-assets/tai-nguyen-chung/`
- Script tải + tự kiểm đếm từng file: `scripts/tai_kho_tai_nguyen.py` (skill tự chạy lần đầu dùng)
- Chi tiết cơ chế + đường dẫn từng loại tài nguyên: xem mục "Tài nguyên dùng chung" trong `SKILL.md`
- Máy cài bản cũ còn folder `tai-nguyen-chung/` ngay tại đây: vẫn dùng được (skill tìm chỗ bền trước, chỗ này sau), nhưng bản trong Drive mới là bản được cập nhật.

# Shorts Editor ROBOWORLD — gói cài cho đồng nghiệp

Skill Claude Code giúp dựng shorts video Roboworld tự động từ footage buổi quay, theo đúng phong cách công ty (học từ hàng chục video mẫu thật). Hỏi bạn chọn 1 trong 3 kiểu dựng, kiểm tra đủ nguyên liệu, đề xuất kịch bản cho duyệt, rồi tự dựng bằng ffmpeg.

## Cài đặt (máy đã có Claude Code)

0. **Điều kiện trước khi bắt đầu**:
   - Đã cài Claude Code và có gói subscription (Sếp là người cấp/hướng dẫn nếu chưa có).
   - Đã được Sếp mời làm **collaborator** trên GitHub cho repo này (repo để ở chế độ riêng tư — private — chỉ người được mời mới xem/tải được, không phải ai có link cũng vào được). Sếp sẽ gửi lời mời qua email gắn với tài khoản GitHub của bạn, bạn chỉ cần bấm **Accept**.
   - Kiểm tra đã có quyền chưa: mở https://github.com/iold12pa/shorts-editor-rbw trên trình duyệt (đã đăng nhập GitHub) — vào xem được nội dung là đã có quyền, còn báo "404 Not Found" nghĩa là chưa được mời hoặc chưa bấm Accept.
   - Máy cần có sẵn chương trình **Git** (công cụ tải code, đa số máy lập trình đã có sẵn) và đã đăng nhập GitHub trên Git — cách kiểm tra nhanh: mở PowerShell, gõ `git clone https://github.com/iold12pa/shorts-editor-rbw.git` ở một thư mục bất kỳ, nếu tải về được (không báo lỗi quyền truy cập) là ổn, sau đó xoá thư mục vừa tải thử đi cũng được (không cần dùng tới, bước cài thật ở dưới làm khác).
1. Mở Claude Code, gõ lệnh sau để "chỉ đường" cho Claude biết kho công cụ nội bộ Roboworld nằm ở đâu (gọi là "marketplace" — chỉ là 1 kho chứa nhiều plugin, ở đây kho này hiện có đúng 1 plugin):
   ```
   /plugin marketplace add https://github.com/iold12pa/shorts-editor-rbw
   ```
2. Gõ tiếp lệnh này để cài đúng plugin (gói công cụ) `shorts-editor-rbw` từ kho vừa thêm:
   ```
   /plugin install shorts-editor-rbw@roboworld-tools
   ```
   Cài xong, Claude Code sẽ **tự hiện 1 hộp thoại hỏi bạn chọn thư mục** chứa footage buổi quay của bạn — chọn đúng thư mục đó là xong, không cần mở file gì để sửa tay.
3. **Tải model Whisper riêng** (bắt buộc nếu muốn dùng Kiểu 2/3 — video có thoại, cần Claude "nghe" được lời nói trong video): xem hướng dẫn trong `skills/shorts-editor-rbw/assets/models/README.md`.
4. Muốn nhận bản cập nhật mới nhất mỗi lần Sếp sửa skill: vào `/plugin` → tab **Marketplaces** → bật auto-update cho `roboworld-tools` (mặc định TẮT vì đây không phải marketplace chính thức của Anthropic).

Vậy chỉ còn **2 việc chính** (cài Claude Code + được mời vào repo đã tính là điều kiện có sẵn từ trước): gõ 2 lệnh ở bước 1-2, rồi chọn thư mục footage khi được hỏi. Bước 3 (Whisper) chỉ cần nếu dùng Kiểu 2/3.

## Dùng thử

Mở Claude Code, gõ tự nhiên kiểu: *"dựng video từ folder [tên buổi quay]"* — skill sẽ tự hỏi bạn chọn kiểu dựng + xin thông tin còn thiếu.

## Muốn dùng qua Telegram thay vì gõ trực tiếp vào Claude Code?

Xem `telegram-bot/README.md` — cài thêm (tùy chọn) 1 "cầu nối" chạy trên chính máy bạn, cho phép nhắn tin/gửi video qua Telegram thay vì mở Claude Code gõ tay. Vẫn xử lý hoàn toàn trên máy bạn, không phụ thuộc máy ai khác.

## Lưu ý quan trọng

- Đã tự chạy thật `/plugin marketplace add` + `/plugin install` (2026-07-15) từ repo GitHub thật, trên máy sạch chưa cài gì — cả 2 lệnh chạy đúng, plugin cài xong có đủ file, `config.json` sạch không lộ dữ liệu riêng. Vẫn khuyến khích người đầu tiên cài thật báo lại nếu gặp lỗi khác máy khác môi trường.
- Mỗi người dùng cần: (a) chọn đúng thư mục footage của họ khi được hỏi lúc cài (hộp thoại `userConfig`, không phải sửa file tay nữa), (b) model Whisper riêng nếu cần Kiểu 2/3, (c) file key ElevenLabs riêng ở `~/.claude/abs6-secrets.env` nếu muốn dùng giọng AI (không bắt buộc).

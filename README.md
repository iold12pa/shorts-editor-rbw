# Shorts Editor ROBOWORLD — gói cài cho đồng nghiệp

Skill Claude Code giúp dựng shorts video Roboworld tự động từ footage buổi quay, theo đúng phong cách công ty (học từ hàng chục video mẫu thật). Hỏi bạn chọn 1 trong 3 kiểu dựng, kiểm tra đủ nguyên liệu, đề xuất kịch bản cho duyệt, rồi tự dựng bằng ffmpeg.

## Cài đặt (máy đã có Claude Code)

**Điều kiện trước khi bắt đầu**: đã cài Claude Code và có gói subscription (Sếp là người cấp/hướng dẫn nếu chưa có). Repo này ở chế độ **công khai (public)** — không cần tài khoản GitHub, không cần đăng nhập git.

**Cách cài — dán đúng 1 câu này vào app Claude (mục Code) rồi Enter:**

```
Chạy giúp tôi 2 lệnh sau qua Bash rồi báo kết quả: 1) claude plugin marketplace add https://github.com/iold12pa/shorts-editor-rbw 2) claude plugin install shorts-editor-rbw@roboworld-tools
```

**LƯU Ý**: đừng gõ trực tiếp `/plugin marketplace add ...` vào app Claude — cú pháp `/plugin` chỉ chạy trong cửa sổ terminal, gõ vào app sẽ báo "isn't available in this environment" (đã có người gặp thật). Cứ dán nguyên câu trên là Claude tự chạy đúng.

**Cài xong là dùng được luôn** — không cần chọn thư mục hay cấu hình gì thêm. Ngay lần đầu nhờ Claude dựng video, skill tự lo nốt mọi thứ còn lại (xem "Lần đầu dựng video" bên dưới).

## Lần đầu dựng video — skill TỰ làm, bạn chỉ chờ vài phút

Lần đầu tiên bạn nói "dựng video từ [folder]...", skill tự động:
1. **Tự cài FFmpeg** (bộ xử lý video, qua kho ứng dụng chính thức của Windows) nếu máy chưa có — không cần đóng/mở lại gì cả, skill tự tìm đường dẫn vừa cài và dùng ngay.
2. **Tự tải "bộ nghe giọng nói"** (model Whisper ~1.6GB — để Claude nghe được lời thoại tiếng Việt trong video) — tải nền, bạn cứ trả lời các câu hỏi dựng video song song. Lưu ở chỗ bền `~/.claude/roboworld-assets/` — sau này gỡ/cài lại plugin KHÔNG phải tải lại.
3. **Tự tải kho tài nguyên chung** (logo, outro, nhạc, hiệu ứng âm thanh, ảnh sản phẩm — từ Google Drive của Sếp) về cùng chỗ bền đó. Script tải tự kiểm đếm từng file, thiếu file nào báo đích danh file đó.
4. **Tự bật auto-update** — từ đó về sau chỉ cần thỉnh thoảng đóng/mở lại Claude Code là nhận bản mới nhất, không cần gõ lệnh gì.

## Kiểm tra sau khi cài (test nhanh)

1. **Xác nhận plugin đã cài**: nhắn "kiểm tra plugin shorts-editor-rbw đã cài chưa" — Claude chạy `claude plugin list` và báo kết quả.
2. **Test bằng 1 buổi quay nhỏ có thật**: nhắn *"dựng video từ [đường dẫn đầy đủ tới 1 folder buổi quay]"* (hoặc kéo-thả folder vào khung chat) — skill phải hỏi bạn chọn 1 trong 3 kiểu dựng (không tự đoán bừa) và liệt kê đúng tên các clip trong folder. Báo "không tìm thấy folder" → kiểm tra lại đường dẫn.
3. **Dựng thử 1 video hoàn chỉnh**: đi hết quy trình tới lúc có file `.mp4` — mở lên xem đúng khung dọc 9:16, có logo, không giật/lỗi hình là đạt.

## Giọng đọc AI (không bắt buộc — chỉ cần cho video có thuyết minh)

- Key ElevenLabs **dùng chung của công ty, Sếp gửi riêng cho từng người qua Zalo** (không nằm trong gói cài này vì repo public). Nhận được key thì nhờ Claude: "lưu key ElevenLabs này vào file abs6-secrets.env cho tôi" — Claude tự tạo file `~/.claude/abs6-secrets.env` đúng định dạng.
- Chưa có key vẫn dựng video bình thường — giọng AI tự chuyển sang giọng miễn phí (edge-tts), chất lượng thấp hơn chút nhưng không lỗi.
- Vì key dùng chung cả team: đừng sinh giọng thử nghiệm tràn lan — mỗi video chỉ sinh giọng khi kịch bản đã được duyệt.

## Cập nhật phiên bản

Hỏi Claude bất kỳ dạng nào: "đang bản nào", "có bản mới không" — skill tự kiểm tra GitHub thật, tự cập nhật nếu có bản mới rồi báo số bản cụ thể (quy tắc nằm trong SKILL.md, không trả lời suông).

## Cài lỗi giữa chừng? Gỡ sạch rồi cài lại

Dán câu này vào app Claude:

```
Chạy giúp tôi 2 lệnh sau qua Bash rồi báo kết quả: 1) claude plugin uninstall shorts-editor-rbw@roboworld-tools 2) claude plugin marketplace remove roboworld-tools
```

Rồi cài lại như mục "Cách cài" ở trên. Model Whisper + kho tài nguyên nằm ở chỗ bền `~/.claude/roboworld-assets/` nên KHÔNG bị mất khi gỡ-cài-lại — không phải tải lại 1.6GB.

## Lưu ý quan trọng

- Đã xác nhận đầu-cuối với người dùng thật khác máy (2026-07-16, Cao Đắc Chiến) — cài qua chính app Claude, không cần mở terminal riêng.
- Mỗi lần dựng video, tự đưa đường dẫn đầy đủ tới folder buổi quay (không có bước cấu hình cố định lúc cài) — footage để ở ổ đĩa/thư mục nào cũng được.
- Lần đầu Claude thao tác vào 1 thư mục footage mới, Windows/Claude Code sẽ hiện hộp thoại xin quyền — chọn "luôn cho phép", chỉ hỏi 1 lần cho mỗi thư mục.
- Muốn dùng qua Telegram thay vì gõ trực tiếp: xem `telegram-bot/README.md` (tùy chọn, đang gác lại — chưa khuyến khích dùng).

# Shorts Editor ROBOWORLD — gói cài cho đồng nghiệp

Skill Claude Code giúp dựng shorts video Roboworld tự động từ footage buổi quay, theo đúng phong cách công ty (học từ hàng chục video mẫu thật). Hỏi bạn chọn 1 trong 3 kiểu dựng, kiểm tra đủ nguyên liệu, đề xuất kịch bản cho duyệt, rồi tự dựng bằng ffmpeg.

## Cài đặt (máy đã có Claude Code)

0. **Điều kiện trước khi bắt đầu**: đã cài Claude Code và có gói subscription (Sếp là người cấp/hướng dẫn nếu chưa có). Repo `shorts-editor-rbw` giờ để ở chế độ **công khai (public)** — không cần được mời, không cần tài khoản GitHub, không cần đăng nhập git gì cả, ai có link cũng cài được ngay.
1. Mở Claude Code, gõ lệnh sau để "chỉ đường" cho Claude biết kho công cụ nội bộ Roboworld nằm ở đâu (gọi là "marketplace" — chỉ là 1 kho chứa nhiều plugin, ở đây kho này hiện có đúng 1 plugin):
   ```
   /plugin marketplace add https://github.com/iold12pa/shorts-editor-rbw
   ```
2. Gõ tiếp lệnh này để cài đúng plugin (gói công cụ) `shorts-editor-rbw` từ kho vừa thêm:
   ```
   /plugin install shorts-editor-rbw@roboworld-tools
   ```
   **Cài xong là dùng được luôn** — không cần chọn thư mục hay cấu hình gì thêm. Lúc muốn dựng video, chỉ cần nói với Claude đường dẫn đầy đủ tới folder buổi quay (gõ tay, hoặc kéo-thả folder đó thẳng vào khung chat để Windows tự dán đường dẫn).
3. **Bật tự động cập nhật (làm 1 lần, đỡ phải gõ lệnh cập nhật tay về sau)**: vào `/plugin` → tab **Marketplaces** → bật auto-update cho `roboworld-tools` (mặc định TẮT). Bật xong, mỗi lần Sếp sửa skill và đẩy lên GitHub, chỉ cần **đóng Claude Code rồi mở lại** là tự nhận bản mới — không cần gõ lệnh gì cả. Repo đã public nên cơ chế này chạy ổn định.
4. **Tải model Whisper riêng** (bắt buộc nếu muốn dùng Kiểu 2/3 — video có thoại, cần Claude "nghe" được lời nói trong video): xem hướng dẫn trong `skills/shorts-editor-rbw/assets/models/README.md`. (Thực ra bước này skill tự làm khi cần — xem mục "Lưu ý quan trọng" bên dưới.)
5. **Muốn tự kiểm tra/cập nhật bằng tay bất cứ lúc nào** (không bắt buộc nếu đã bật auto-update ở bước 3) — gõ đúng 2 lệnh này, an toàn, không sợ hỏng gì:
   ```
   /plugin marketplace update roboworld-tools
   /plugin update shorts-editor-rbw@roboworld-tools
   ```
   Lệnh 1 tải thông tin mới nhất về từ GitHub, lệnh 2 tự so sánh rồi báo thẳng 1 trong 2 kết quả — không cần đoán:
   - `shorts-editor-rbw is already at the latest version (...)` → máy bạn **đã là bản mới nhất**, không cần làm gì thêm.
   - `updated from <bản cũ> to <bản mới>. Restart to apply changes.` → máy bạn **vừa được cập nhật**, đóng Claude Code mở lại là dùng được bản mới.

   (Kỹ thuật phía sau: mỗi lần Sếp sửa gì trong skill và đẩy lên GitHub tính là 1 "bản" mới tự động theo đúng lần lưu đó, không cần Sếp phải nhớ tăng số phiên bản tay — tránh trường hợp quên tăng số khiến máy đồng nghiệp tưởng nhầm là "chưa có gì mới".)

Vậy chỉ còn **2 việc chính** (cài Claude Code là điều kiện có sẵn từ trước): gõ đúng 2 lệnh ở bước 1-2, bật auto-update ở bước 3 — xong là dùng được ngay và tự cập nhật mãi về sau, không cần làm gì thêm.

## Kiểm tra sau khi cài (test nhanh, 4 bước)

Làm đúng 4 bước này để chắc chắn đã cài thành công, không phải đoán:

1. **Xác nhận plugin đã cài đúng**: gõ `/plugin` → tab **Installed** → thấy `shorts-editor-rbw` trạng thái **enabled** là đạt bước 1.
2. **Test bằng 1 buổi quay nhỏ có thật**: gõ *"dựng video từ [đường dẫn đầy đủ tới 1 folder buổi quay bất kỳ]"* (hoặc kéo-thả folder đó vào khung chat) — skill phải tự hỏi bạn chọn 1 trong 3 kiểu dựng (không tự đoán bừa) và liệt kê đúng tên các clip trong folder đó. Nếu báo "không tìm thấy folder" → kiểm tra lại đường dẫn đã đưa đúng chưa.
3. **Dựng thử 1 video hoàn chỉnh**: đi hết quy trình tới lúc có file `.mp4` xuất ra — mở file lên xem đúng khung dọc 9:16, có logo, không bị giật/lỗi hình là đạt. Đây là bước xác nhận chắc chắn nhất, các bước 1-2 chỉ là kiểm tra nhanh trước khi tốn thời gian dựng thật.

Nếu dùng Kiểu 2/3 (cần nghe thoại) hoặc giọng AI, kiểm tra thêm:
- Model Whisper đã tải đúng vị trí `skills/shorts-editor-rbw/assets/models/` (xem README trong đó) — thiếu thì bước phân tích thoại sẽ báo lỗi rõ, không chạy ngầm sai.
- Key ElevenLabs riêng (nếu dùng) đã có ở `~/.claude/abs6-secrets.env` trên máy bạn — mỗi người 1 key riêng, không dùng chung key của Sếp.

## Cài lỗi giữa chừng? Gỡ sạch rồi cài lại

Không cần gỡ Claude Code hay cài lại máy — chỉ cần 2 lệnh, dữ liệu footage của bạn không hề bị đụng tới:
```
/plugin uninstall shorts-editor-rbw@roboworld-tools
/plugin marketplace remove roboworld-tools
```
Rồi quay lại làm đúng bước 1-2 ở trên từ đầu.

## Muốn dùng qua Telegram thay vì gõ trực tiếp vào Claude Code?

Xem `telegram-bot/README.md` — cài thêm (tùy chọn) 1 "cầu nối" chạy trên chính máy bạn, cho phép nhắn tin/gửi video qua Telegram thay vì mở Claude Code gõ tay. Vẫn xử lý hoàn toàn trên máy bạn, không phụ thuộc máy ai khác.

## Lưu ý quan trọng

- Đã tự chạy thật `/plugin marketplace add` + `/plugin install` (2026-07-16) từ repo GitHub thật, trên máy sạch chưa cài gì — cả 2 lệnh chạy đúng, cài xong dùng được ngay không cần cấu hình gì thêm.
- **Đã xác nhận đầu-cuối với người dùng thật khác máy** (2026-07-16, Cao Đắc Chiến) — cài qua chính app Claude (không cần mở terminal riêng), phát hiện và tự sửa 3 vấn đề thật ngay trong lần đầu: cú pháp `/plugin` không chạy trong app Claude thường (phải dùng câu nói tự nhiên nhờ Claude tự gọi lệnh), thiếu bước tự cài FFmpeg, model Whisper tải trễ tới lúc cần Kiểu 2/3 thay vì tải ngay từ đầu — cả 3 đã vá trong skill, không phải chỉ ghi chú suông.
- Mỗi lần dựng video, tự đưa đường dẫn đầy đủ tới folder buổi quay (không có bước cấu hình cố định lúc cài) — footage để ở ổ đĩa/thư mục nào cũng được, miễn đưa đúng đường dẫn.
- Mỗi người dùng cần thêm: (a) model Whisper riêng nếu cần Kiểu 2/3, (b) file key ElevenLabs riêng ở `~/.claude/abs6-secrets.env` nếu muốn dùng giọng AI (không bắt buộc).
- Lần đầu Claude thao tác vào 1 thư mục footage mới (ngoài thư mục đang mở Claude Code), Windows/Claude Code sẽ hiện 1 hộp thoại hỏi xin quyền — chọn "luôn cho phép", chỉ hỏi đúng 1 lần cho mỗi thư mục.

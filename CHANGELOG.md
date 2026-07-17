# Nhật ký cập nhật — shorts-editor-rbw

File này ghi lại các thay đổi đáng chú ý theo ngày, mới nhất ở trên cùng. Xem chi tiết đầy đủ từng thay đổi bằng lịch sử commit trên GitHub.

## 2026-07-17
- **Cài đặt = 1 câu dán, tự cài TRỌN BỘ từ đầu** (chỉ đạo Huy sau lần cài máy đồng nghiệp): câu cài mới trỏ Claude đọc `references/cai-dat-lan-dau.md` — báo trước mất khoảng bao lâu, tự cài plugin + FFmpeg + bộ nghe 1.6GB + kho ~180MB (chạy nền) + dò GPU, xong mục nào báo mục đó, chốt bằng bảng trạng thái + tổng thời gian thật.
- **Lệnh "chuẩn bị máy" / "kiểm tra máy đủ đồ chưa"**: rà lại từng mục bất cứ lúc nào, in bảng trạng thái — hết cảnh cài xong không biết máy mình đủ đồ chưa.
- **Tự dò + cài giúp driver NVIDIA** (script `cai_driver_nvidia.py`): máy có card NVIDIA nhưng driver cũ → skill hỏi đúng 1 câu đời thường, người dùng OK là tự tải bản chuẩn từ nvidia.com + cài im lặng, chỉ cần bấm Yes 1 lần trên hộp thoại Windows (trôi hộp thoại thì tự bật lại, tối đa 3 lần) — xong render nhanh 2-5 lần. Không bao giờ tự cài khi chưa được OK.
- **Kho tài nguyên chung chuyển sang Google Drive** (không còn nằm trong gói cài): cài plugin nhẹ hơn hẳn; Sếp thêm nhạc = kéo file vào Drive; script mới `tai_kho_tai_nguyen.py` tải về chỗ bền `~/.claude/roboworld-assets/` và TỰ KIỂM ĐẾM — thiếu file nào báo đích danh file đó. Model Whisper cũng chuyển về chỗ bền này (gỡ-cài-lại plugin không phải tải lại 1.6GB).
- **Vá 3 lỗi "hỏng im lặng"** trong script phân tích: (a) ffmpeg thiếu filter whisper giờ báo RÕ + index ghi "chưa nghe được" thay vì ghi nhầm "không có thoại"; (b) clip trùng tên giữa 2 thẻ nhớ hết ghi đè sheet của nhau (định danh theo đường dẫn tương đối, index cũ tự migration giữ nguyên phần đã điền); (c) lỗi mạng ElevenLabs báo tiếng Việt dễ hiểu thay vì văng lỗi thô.
- **Chuẩn -14 LUFS vào thẳng lệnh xuất final + bước nghiệm thu đo thật** (trước đây chỉ nằm trong file style karaoke — video Kiểu 1 dễ giao thiếu chuẩn).
- **Chọn encoder GPU (NVENC) đầu phiên dựng** bằng test-encode thật — máy có card NVIDIA + driver mới tự render nhanh 2-5 lần, máy khác tự về libx264 như cũ.
- **Cài lần đầu mượt hơn**: FFmpeg cài xong dùng ngay không bắt đóng/mở lại Claude Code (tự ghi đường dẫn vào config.json); model tải NỀN kiểu `.part` an toàn; câu hỏi khởi động gộp 1 lượt + phân tích footage chạy nền song song.
- **Đọc footage tiết kiệm**: sàng lọc shortlist từ index trước, chỉ đọc sheet của clip liên quan (folder 58 clip không còn đốt 70-90k token khi chỉ cần 1 video); vá bug chia-0 + bug timeout clip dài >30 phút; số khung trích tự co theo độ dài clip.
- **Giọng đọc**: George là giọng mặc định chính thức (chạy được gói Free); Kiểu 3 hỏi rõ muốn giọng nam/nữ; cảnh báo lỗi 402 (giọng Voice Library cần gói trả phí) ghi đúng chỗ.
- **Nhạc**: luật mới — bài thuộc diện nhạc trend/thương mại thì nhắc đúng 1 câu rủi ro bản quyền tại điểm dừng duyệt kịch bản rồi làm theo quyết định người dùng; thêm `elevenlabs_music.py` (sinh nhạc không lời đo ni theo video — option mở rộng, cần gói ElevenLabs trả phí).
- **Sửa tài liệu lệch thực tế**: bảng hashtag thêm BellaBot + SH1, sửa tag Phantas sai; template kịch bản viết lại theo 3 kiểu dựng (Kiểu 2 có mục "take nghi vấn cần nghe kiểm"); "3 điểm dừng" → đúng 2 điểm dừng; README viết lại đường cài 1-câu-dán + key ElevenLabs dùng chung gửi Zalo.

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

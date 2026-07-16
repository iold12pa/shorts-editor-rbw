# Style chuẩn Roboworld — học từ video mẫu (Video mẫu\Short+text+nhạc\)

Phân tích 2 video mẫu ngày 2026-07-02: `MT1 (1).mp4` (30.5s, 1080x1920) và `Robot tại Vinschool.mp4` (44.4s, 2160x3840). Video mẫu mới xuất hiện trong `Video mẫu\` thì phân tích lại và cập nhật file này.

## Dạng video chủ đạo: SHORT + TEXT + NHẠC
Video mẫu KHÔNG có voiceover — câu chuyện kể bằng **text đè Anton in hoa + nhạc nền + cảnh quay đẹp**. Đây là dạng mặc định. Chỉ thêm voiceover khi ý tưởng cần lời dẫn (review chi tiết, giải thích tính năng) và ghi rõ trong kịch bản để Sếp duyệt.

## Logo
- Wordmark ROBOWORLD **màu trắng** (icon robot + chữ), có bóng đổ nhẹ
- Vị trí: **giữa-trên**, mép trên ~40-60px (theo khung 1080x1920), rộng ~480-500px (~45% khung)
- Hiện suốt video. Tìm file logo trắng trong `Claude Edit video\` (logo*.png) hoặc `assets/logo.png` của skill; chưa có thì hỏi Sếp.

## Text đè (font Anton — `assets/fonts/Anton-Regular.ttf`, hỗ trợ tiếng Việt)
- **Hook mở đầu**: IN HOA, màu **vàng ~#FFD200**, viền/bóng đen đậm, cỡ **130-135pt** theo khung 1080x1920. Lịch sử: bắt đầu 100pt → 118pt → 135pt, cả 2 lần tăng đều do Sếp phản hồi "chữ vẫn nhỏ" — 130-135pt là mốc hiện tại đã được duyệt, coi đây là baseline mặc định, KHÔNG lùi về mức thấp hơn trừ khi Sếp nói. 2-3 dòng, đặt ngay **dưới logo** (bắt đầu ~11-13% chiều cao khung). Ví dụ mẫu: "BELLABOT PRO TẠI VINSCHOOL".
- **Text nội dung**: IN HOA, màu **trắng**, viền đen, cỡ **85-90pt** (cùng lịch sử tăng dần như trên, từ 66→78→90pt), 1-2 dòng, cùng vị trí dưới logo. Mỗi text 1 ý ngắn (5-9 từ), giữ 3-8 giây tùy độ dài cảnh nền. Ví dụ mẫu: "TƯƠNG TÁC BIỂU CẢM THÂN THIỆN", "THU HÚT SỰ CHÚ Ý CỦA MỌI NGƯỜI".
- Biến thể MT1: text trắng 2 dòng đặt thấp (~65-75% chiều cao) — dùng khi cảnh phía trên rối, che mất chủ thể.
- **Trước khi dựng cả video, LUÔN render thử 1 frame** với cỡ chữ + xuống dòng dự kiến rồi Read để mắt kiểm tra không tràn viền — đừng tính toán lý thuyết (đo bằng mm/pixel suông dễ sai vì Anton là font hẹp/condensed, khó ước lượng chính xác). Cách làm: burn ASS test lên 1 frame tĩnh của cảnh sẽ dùng, xem qua, chỉnh cỡ/số dòng nếu cần, rồi mới áp dụng cho toàn bộ kịch bản.
- **Hiệu ứng ra/vào cho text**: mặc định luôn dùng fade nhẹ (`\fad(200~300,250~300)` trong ASS) thay vì text bật/tắt cứng — cảm giác chuyên nghiệp hơn mà không phô. Đây là hiệu ứng tối thiểu bắt buộc; hiệu ứng mạnh hơn (bounce, scale-in) chỉ thêm khi kịch bản thật sự cần nhấn, tránh dùng tràn lan.
- **Dấu câu gọn gàng**: không để thừa dấu (vd hook không viết "ROBOT?!" — chỉ 1 dấu, chọn "?" hoặc "!" theo đúng tông câu, không cả hai). Đọc lại toàn bộ text trong kịch bản trước khi burn để bắt lỗi này.

## Chọn cảnh mở đầu (hook) — nguyên tắc quan trọng

> Xem thêm `references/chon-canh-highlight.md` — quy tắc chọn cảnh đầy đủ (không chỉ hook) đúc kết từ đối chiếu TRỰC TIẾP 1 buổi quay thô với 2 video final thật đã dựng ra từ đó, áp dụng chung cho cả 3 kiểu dựng.

Hook quyết định người xem có ở lại hay lướt qua trong 1-2 giây đầu. Khi rà footage, ưu tiên tìm cảnh **gây chú ý thị giác mạnh** thay vì cảnh "hành chính" (mở hộp đồ nghề, chuẩn bị dụng cụ...). Các dạng cảnh hook tốt, xếp theo độ ưu tiên:
1. Khoảnh khắc "reveal" bất ngờ/hơi sốc (vd: tay chỉ vào đống tóc quấn đầy bánh xe robot vừa gỡ ra — vừa gây tò mò vừa "ghê mà cuốn")
2. Robot tương tác với người thật (trẻ em, khách hàng chạm/đi cạnh/phản ứng với robot)
3. Chuyển động ấn tượng của robot (tháo lắp cận cảnh có ánh đèn LED, robot di chuyển giữa đám đông)
Chỉ dùng cảnh "chuẩn bị/hành chính" (mở hộp đồ, xếp dụng cụ) làm cảnh THỨ 2 trở đi, không mở đầu bằng nó trừ khi footage không có gì mạnh hơn.

## Nhịp dựng
- Cảnh 3-5 giây, ưu tiên cảnh robot chuyển động + phản ứng người thật (trẻ em, công nhân, khách)
- Mở đầu bằng cảnh mạnh nhất + hook vàng
- Kết hợp footage DJI (mượt, rộng) làm cảnh chính + iPhone (cận, đời thường) làm cảnh chen
- **Chuyển cảnh: 100% hard-cut** — đã kiểm tra bằng lưới dày (fps=8, quanh từng điểm scene_change) trên 4 video style này (Vinschool, Phúc Yên 2, Unbox Omnie, GGG Hà Nội), không thấy crossfade/wipe nào. Đừng tự thêm hiệu ứng chuyển cảnh.
- **Text KHÔNG bắt buộc đổi theo từng cut** — 1 dòng text có thể giữ nguyên xuyên qua 2-3 lần cắt cảnh bên dưới nếu vẫn cùng 1 ý (đo được ở Vinschool: "THU HÚT SỰ CHÚ Ý CỦA MỌI NGƯỜI" giữ nguyên qua nhiều giây dù hình đổi). Đổi text theo NHỊP THÔNG ĐIỆP, không phải nhịp cắt hình.
- **Đo màu vàng thực tế** (pixel, không phải lý thuyết): 2 video đo được ra `#EFFC00` (vàng-chanh hơi khác `#FFD200` gốc) — chấp nhận cả 2 sắc trong khoảng "vàng thương hiệu", không cần tuyệt đối khớp mã hex nếu do nén video.

## Outro
2 video mẫu đều có outro nền đen→đỏ (logo đỏ animation lắp ráp dần + card hotline/địa chỉ/FB/web, 6s cuối). **Sếp đã yêu cầu KHÔNG dùng intro/outro** → mặc định bỏ, dùng outro dọc hiện có của skill thay thế. Nếu Sếp đổi ý muốn dùng lại đúng outro này: đây KHÔNG phải dựng tay — có sẵn file `assets/tai-nguyen-chung/Logo+outro Uyên/Logo Animation_1.mp4` (xác nhận 2026-07-15, cùng file xuất hiện lặp lại ở ít nhất 6 video khác trong HUY MKT — CC1 ads, Vinschool ×2, Phúc Yên ×2, Unbox Omnie — nên là asset dùng chung thật, không phải trùng hợp). File này có bản card cá nhân hóa "Phương Uyên" — nếu dùng cho video khác cần hỏi Sếp có bản card công ty chung hay phải làm lại card riêng.

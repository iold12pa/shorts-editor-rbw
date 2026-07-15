# Style "QUẢNG CÁO SẢN PHẨM (ADS)" — học từ 5 quảng cáo trong kho `HUY MKT`

Phân tích 2026-07-15, nguồn: `18.SH1 ads`, `20.CC1 ads`, `21.MT1 ads`, `35.Uyên ads thuê`, `38.Bella + Dung RBW` (đều đã có `_phan_tich/index.json` + sheets điền đủ content/tags/key_moments). Đo màu/vị trí bằng cách trích frame full-res + numpy đọc pixel chính xác (không đoán bằng mắt), soi transition bằng lưới dày `fps=10,tile` quanh từng mốc `scene_changes`.

**Khi nào dùng style này**: Sếp muốn video mang tính "quảng cáo sản phẩm" rõ ràng (nêu vấn đề → giới thiệu robot → thông số → CTA), khác với style ①②③ vốn thiên về nội dung/khoảnh khắc buổi quay. Style này KHÔNG phải 1 công thức duy nhất — là 1 rổ 5 biến thể, chọn biến thể theo ngân sách/thời gian có (xem mục "Khuyến nghị" cuối file).

## Tổng quan 5 biến thể đã soi

| # | Nguồn | Robot | Đặc điểm hình ảnh chính | Độ khó tái tạo bằng ffmpeg tay |
|---|---|---|---|---|
| A | SH1 ads 2.mp4 | PUDU SH1 | VO chuyên nghiệp + B-roll thật, thẻ chữ nền vàng, watermark góc, **toàn hard-cut** | **Dễ** — đúng năng lực hiện tại của skill |
| B | CC1 ads 1.mp4 | PUDU CC1 | Reveal điện ảnh studio tối + badge giải thưởng + masked-wipe + thẻ từ-khóa chớp nhanh + outro logo animation | **Vừa** — outro logo animation đã có sẵn file dùng lại được (xem đính chính cuối file); phần reveal điện ảnh + masked-wipe vẫn cần quay riêng |
| C | MT1 ads 2.mp4 | PUDU MT1 | Trộn **CGI 3D từ hãng PUDU** (robot xoay lơ lửng, wireframe map) với footage thật + transition light-flare | **Không tái tạo được phần CGI** bằng ffmpeg — chỉ dùng được nếu có sẵn asset CGI từ hãng |
| D | Uyên order ads (V1/V2/V3) | BellaBot Pro (transcript ghi "Bella Pop Pro" — có thể nghe nhầm, hỏi lại Sếp nếu dùng tên này) | MC/UGC nói trực tiếp + sub karaoke cụm-từ + B-roll TÁI SỬ DỤNG từ thư viện có sẵn | **Dễ** — gần giống style ② đã có, chỉ khác cách viết kịch bản |
| E | Bella + Dung RBW (Final.mp4) | BellaBot | Nhân viên Roboworld mặc đồng phục giới thiệu tại showroom thật + demo màn hình UI cận cảnh + karaoke | **Dễ-Trung bình** — cần nhân viên lên hình + quay tại văn phòng/showroom |

Biến thể A/B/C dùng giọng đọc voice-over chuyên nghiệp (không lộ mặt người nói); D/E dùng người thật nói trực tiếp trên hình (MC hoặc nhân viên). **Cả 5 đều mở bằng câu hỏi/pain-point trong 3 giây đầu** — không có ngoại lệ.

## Công thức kịch bản lời thoại (rút từ transcript 3 quảng cáo VO: SH1, CC1, MT1)

Cả 3 video A/B/C dùng **gần như CÙNG MỘT khung sườn thoại**, chỉ đổi số liệu/tên sản phẩm — đây là công thức Roboworld đã dùng lặp lại, nên coi là chuẩn mặc định khi viết kịch bản VO chuyên nghiệp:

1. **Hook nghi vấn (0-3s)**: nêu bối cảnh quy mô lớn ("nhà xưởng/kho bãi/bệnh viện/TTTM rộng hàng nghìn mét vuông") + đặt câu hỏi chê cách làm cũ ("mà cứ [làm thủ công] ư?")
2. **Bắc cầu (3-8s)**: "Hôm nay cùng mình xem/trải nghiệm em robot này xử lý thế nào nhé"
3. **Định danh sản phẩm (8-12s)**: "Đây là [Tên robot], robot [loại] tích hợp [tính năng nổi bật nhất]"
4. **Liệt kê thông số (12-40s)**: cân nặng/kích thước → cách vận hành (tự động/cảm biến) → pin/thời lượng → năng suất so sánh (vd "gấp hàng chục lần thủ công") — MỖI thông số đi kèm 1 cảnh B-roll minh họa đúng thông số đó
5. **CTA (cuối)**: "Trải nghiệm ngay [Tên robot] để thấy sự khác biệt nhé!" — công thức CTA cố định, gần như nguyên văn ở cả 3 video

Kịch bản MC/UGC (D/E) khác hẳn: không có thông số kỹ thuật dồn dập, thay bằng **pain-point cá nhân hóa + proof-point thương hiệu lớn** (xem case-studies.md — Golden Gate, Samsung, Viettel, May 10 đã có số liệu thật) + CTA mời inbox/nhắn tin thay vì "trải nghiệm ngay".

## Hồ sơ chữ/màu đã đo (4 kiểu — số liệu đo pixel thật, không ước lượng)

### 1. Thẻ chữ nền vàng 2 dòng (SH1, cũng là gốc của style ①②)
- Màu nền: **#FEDB00** (≈ #FFD200 brand yellow đã dùng ở style ①② — xác nhận ĐÚNG 1 brand yellow xuyên suốt)
- Chữ: đen, in hoa/thường lẫn, font condensed bold (kiểu Anton)
- Kích thước: hộp bo góc rộng **~64.5% chiều rộng khung nội dung**, cao **~12.6% chiều cao khung**, căn giữa ngang
- Vị trí: **66-79% chiều cao** (phần dưới khung, dưới logo/dưới robot)
- **Đặc điểm riêng so với style ②**: thẻ TỒN TẠI XUYÊN QUA NHIỀU LẦN HARD-CUT của hình bên dưới — không đổi thẻ mỗi khi đổi cảnh, mà đổi theo nhịp lời thoại. 1 thẻ có thể phủ 2-3 cảnh B-roll khác nhau.

### 2. Thẻ từ-khóa chớp nhanh không nền (CC1)
- Chữ trắng đậm, hơi nghiêng, có motion-blur/glitch nhẹ lúc xuất hiện — KHÔNG có hộp nền
- Cỡ chữ RẤT LỚN: cap-height **~12.5% chiều cao khung** (to hơn cả hook style ①②)
- Vị trí: lệch trái (~33% margin trái, không căn giữa), dọc ở khoảng 56-68% chiều cao
- Nhịp: MỖI TỪ <1 GIÂY, đổi từ đồng bộ chính xác với hard-cut hình bên dưới (ngược với kiểu 1 — ở đây chữ THEO cut, không persist)
- Dùng cho chuỗi liệt kê nhanh (quét → hút → lau → tráng — tên 4 tác vụ của CC1)

### 3. Karaoke cụm-từ (Uyên, Bella+Dung — TRÙNG với spec style ② đã có)
- Giống hệt cơ chế đã ghi trong `style-voice-karaoke.md`: nền hộp đen, chữ trắng, từ đang đọc tô màu
- Khác biệt nhỏ đã đo: màu tô ở đây là **vàng thuần #FEFF02** (≈#FFFF00) chứ không phải #FFD200 brand — vì 2 video này dùng preset caption tự động (kiểu CapCut) chứ không chỉnh tay theo brand. Bella+Dung dùng màu tô **đỏ #EC1C1C** thay vì vàng.
- **Không cần tạo spec mới** — áp lại đúng công thức karaoke của style ②, chỉ đổi màu tô nếu Sếp muốn khớp video mẫu này.

### 4. Tiêu đề đỏ nghiêng không nền (Bella+Dung)
- Màu: **#EC1C1C** (đỏ thuần), font in nghiêng kiểu script/bold-italic (KHÁC Anton — Anton là condensed đứng, đây là chữ nghiêng bo tròn hơn)
- Vị trí: ngay dưới logo, **16-24% chiều cao**, căn trái (~17% margin), không hộp nền, có viền/bóng trắng mỏng để nổi trên nền phức tạp
- Dùng cho câu khẳng định ngắn 2 dòng kiểu USP ("Giao diện thân thiện / Tương tác niềm nở")

## Kiểu chuyển cảnh (transition) đã bắt được

Soi lưới dày `fps=10,tile` quanh 10 mốc `scene_changes` khác nhau, phát hiện 3 kiểu:

1. **Hard cut** (SH1 toàn bộ, Uyên, Bella+Dung, phần lớn CC1/MT1) — cắt cứng, không hiệu ứng. **Đây vẫn là mặc định** của skill, không cần đổi gì.
2. **Masked-wipe** (CC1 @13.1s): 1 vật thể tối (như cánh tay/panel) quét ngang qua ống kính che khuất khung hình trong ~0.3-0.4s rồi lộ ra cảnh mới phía sau — hiệu ứng composite quay thật, KHÔNG PHẢI filter `xfade=wipeleft` của ffmpeg (xfade wipe là 1 đường thẳng cứng ăn dần, còn cái này có motion-blur và vật thể thật che ống kính).
3. **Light-flare/burst transition** (MT1 @19.2s): hiệu ứng tunnel ánh sáng trắng bùng nổ/zoom làm cầu nối giữa 2 cảnh — có thể ffmpeg giả lập gần đúng bằng `xfade=fadewhite` hoặc chèn 2-3 frame trắng/overexposed ở điểm cắt, nhưng sẽ không mượt bằng bản gốc (bản gốc là 1 shot dựng riêng, không phải filter).

**Kết luận thực dụng**: nếu Sếp muốn dựng style ADS nhanh bằng ffmpeg như hiện tại, dùng **hard-cut là chính** (biến thể A/D/E) — đã đủ chuyên nghiệp và đúng năng lực skill. Muốn có masked-wipe/CGI như CC1/MT1 thì cần quay riêng cảnh reveal hoặc thuê dựng motion graphics — ghi rõ giới hạn này khi Sếp yêu cầu, đừng nhận làm rồi ra bản kém hơn video mẫu.

**Đính chính 2026-07-15 — outro logo animation KHÔNG cần dựng mới**: khảo sát thêm 10 folder khác trong HUY MKT phát hiện outro logo động y hệt CC1 (đen → 2 chấm đỏ → chữ R lắp ráp → card liên hệ) xuất hiện lặp lại ở NHIỀU video khác (Vinschool, Phúc Yên, Unbox Omnie...) — đây là 1 **file asset có sẵn** (`D:\VIDEO RBW\Edit video\02.Tài nguyên chung\Logo+outro Uyên\Logo Animation_1.mp4`, 6s, 1080x1920, có bản card cá nhân hóa "Phương Uyên" — có thể còn bản card công ty chung ở nơi khác chưa tìm thấy), KHÔNG phải dựng riêng cho từng video. Tuy nhiên `references/style-mau.md` đã ghi rõ: **Sếp từng được hỏi và đã từ chối dùng outro card đỏ này**, chọn outro dọc hiện tại thay thế. Vì vậy: đây là THÔNG TIN để Sếp biết có sẵn, KHÔNG tự động đổi outro mặc định của skill — chỉ dùng nếu Sếp chủ động chọn lại cho video ADS.

## B-roll tái sử dụng (kỹ thuật rút từ Uyên ads)

Uyên ads chèn cảnh KHÔNG quay riêng cho video này (hội thảo du lịch, hội chợ LEFASO, sự kiện có trẻ em — footage có sẵn trong thư viện) để minh họa luận điểm "dùng được ở mọi sự kiện", xen giữa các đoạn MC nói chính. Đây là cách tiết kiệm effort hợp lý khi kho footage cũ đã đủ đa dạng bối cảnh — **áp dụng được cho các buổi quay sau**: khi viết kịch bản ADS mới, kiểm tra trước index.json của các folder cũ xem có B-roll bối cảnh tương tự claim đang muốn đưa ra không, tránh phải quay lại từ đầu.

## Khuyến nghị khi Sếp muốn dựng video theo style ADS

- Muốn nhanh, đúng năng lực ffmpeg hiện tại → chọn khung sườn A (VO + thẻ vàng + hard-cut) hoặc D/E (MC/nhân viên lên hình + karaoke) tùy có người sẵn sàng lên hình hay không
- Muốn hoành tráng như CC1/MT1 (reveal điện ảnh, CGI, logo animation) → phải báo trước với Sếp đây là mức đầu tư khác (quay riêng/thuê motion graphics), skill hiện tại chỉ làm được phần B-roll + text + hard-cut, KHÔNG tự tạo được phần điện ảnh/CGI
- Viết lời thoại VO → dùng đúng khung sườn 5 bước ở mục "Công thức kịch bản" phía trên, giữ câu CTA gần với mẫu đã có
- Có claim kiểu "dùng được nhiều bối cảnh" → cân nhắc B-roll tái sử dụng như Uyên ads thay vì quay mới toàn bộ

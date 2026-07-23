# SỔ GU KIỂU 2 + KIỂU 3 — rút từ đối chiếu THẬT source↔final các video chuẩn vàng Sếp chỉ định (17/07/2026)
<!-- tags: chung -->

> Cách rút: máy nghe transcript 10 folder thô + 15 folder final chuẩn vàng, so khớp từng câu final về câu gốc trong source (clip nào, mốc nào, % khớp) → lộ ra luật CHỌN CÂU, ĐẢO THỨ TỰ, NHỊP CẮT thật — không suy đoán. Bản đối chiếu gốc: `scratchpad doichieu_*.txt` (phiên 17/07). Đọc kèm: luật chống lỗi voice gốc trong `style-voice-karaoke.md` (vẫn áp nguyên), `chon-canh-highlight.md`.

## KIỂU 2 — DỰNG THEO THOẠI MC CÓ SẴN: 3 CÔNG THỨC CON
<!-- tags: kieu-2 -->

**Nhận diện công thức nào: nhìn SOURCE trước.** MC nói 1 take dài liền mạch → 2A. Mỗi câu quay 1 clip riêng (tên file đặt theo câu) → 2B. Câu đắt rải rác nhiều take/nhiều clip → 2C.

> So sánh nhịp cắt của 3 công thức này với các kiểu/nhánh khác: bảng gộp tại `quy-trinh-chon-canh.md` mục 4b.

### 2A — "MỘT MẠCH KỂ CHUYỆN" (mẫu vàng: 45.Xử lí robot lỗi 51.8s, 47.Cáp treo 85.9s)
<!-- tags: kieu-2 -->
- Giữ MẠCH của take chính (mọi câu cùng 1 clip nguồn), chọn lọc nhẹ: nội dung giải đáp/giới thiệu giữ ~80% câu (45: giữ 12/15); nội dung HÀNH TRÌNH/trải nghiệm chỉ giữ ~20% làm phần dẫn (47: 10/55) — phần còn lại của video để HÌNH + NHẠC tự kể, không lời.
- Thoại phủ: 100% thời lượng (dạng giải đáp) HOẶC ~45% (dạng hành trình — thoại dồn nửa đầu).
- Nhịp cắt ~1.8-2.1s/cảnh: B-roll đè dày trong khi tiếng MC chạy liên tục (mở đoạn bằng chính MC trên hình 2-3s rồi mới cắt B-roll — luật khẩu hình cũ).

### 2B — "LISTICLE TỪNG CÂU" (mẫu vàng: 38.Bella+Dung bản FInal2 47.7s)
<!-- tags: kieu-2 -->
- Source đặc trưng: mỗi câu 1 file quay riêng → ghép tuần tự câu 1→N, mỗi câu = 1 cảnh.
- Nhịp CHẬM CHỦ ĐÍCH: ~5.3s/cảnh, có khoảng thở 1-3s giữa câu (nhạc lấp) — khác hẳn 2A/2C, đừng "sửa" thành nhịp nhanh.
- Cấu trúc: hook listicle ("Tốp những lý do bạn nên chọn...") → proof đối tác lớn (Samsung, Viettel, May 10, Golden Gate) → mỗi tính năng 1 câu 1 cảnh → **chốt FOMO dạng câu hỏi** ("Golden Gate đã sở hữu, còn nhà hàng của bạn đã có chưa?") — KHÔNG kết bằng "liên hệ ngay" khô.
- Được giữ câu đùa/tương tác đời thường làm gia vị ("Cảm ơn Chú đã quan tâm...").

### 2C — "ADS GHÉP ĐA TAKE" (mẫu vàng: 37.Thuê 2/Thuê 3 45s)
<!-- tags: kieu-2 -->
- Nhặt câu đắt từ NHIỀU clip rải khắp buổi quay (mẫu: 8 clip khác nhau) và **ĐƯỢC PHÉP ĐẢO THỨ TỰ** so với lúc quay để phục vụ cấu trúc.
- Cấu trúc ads: hook vấn đề "Top 1..." → nỗi đau CÓ SỐ CỤ THỂ ("bỏ cả chục củ thuê PG, khách vẫn ngó lơ") → "thử ngay cách này" → tên SP đứng riêng 1 câu → tính năng BẮN LIÊN THANH (câu cực ngắn 1-2s: "Màn hình 18.5 inch" / "Banner quảng cáo di động") → lợi ích theo tình huống khách → giá/thuê ("không cần đầu tư mấy trăm triệu...") → CTA inbox.
- Nhịp ~3.0s/cảnh; thoại phủ ~80%; câu ngắn 1-2s chính là "phát súng" tạo nhịp.

### BÀI HỌC XƯƠNG MÁU video thi 17/07 (Sếp chấm trượt bản đầu — 4 lỗi, khắc thành luật)
<!-- tags: kieu-2 -->
1. **Biên cắt thoại KHÔNG ĐƯỢC đi tắt** (sửa 21/07/2026 — luật cũ ghi "phải đo silencedetect thật", nay thay bằng công cụ đúng): mọi biên cắt phải đo bằng `scripts/loc_thoai_that.py`, **cấm tin mốc Whisper + đệm cố định** — đệm cố định = cắt vấp, mốc Whisper = số nối đuôi chứ không phải số đo. `silencedetect` chết trong môi trường ồn nền (nhà sách, nhà máy) nên không còn là công cụ chính.
2. **Mối nối 2 take khác clip PHẢI được che**: bằng B-roll đè hoặc chuyển cảnh — cấm để 2 cảnh MC đứng nhảy cắt cạnh nhau (lộ vấp cả hình lẫn nhịp giọng).
3. **Track thoại ghép đa take**: thêm `dynaudnorm` nhẹ san mức mic giữa các take + `acrossfade` ~50ms tại mối nối tiếng.
4. **Phải DÙNG kho chuyển cảnh + SFX đã học** (sổ hiệu ứng + sổ SFX + giáo lý riser/im lặng/hit): video "sạch nhưng nhạt" cũng là trượt — đúng liều nhưng phải CÓ.

### Luật chung Kiểu 2 (cả 3 công thức)
<!-- tags: kieu-2 -->
- **HOOK: KHÔNG BAO GIỜ mở bằng "Xin chào"** — mở bằng vấn đề/câu hỏi/tuyên bố; câu chào (nếu giữ) đứng SAU hook (mẫu 47: "Đi Bà Nà thì chơi cái gì ạ?" rồi mới "Xin chào anh chị").
- CTA 2 kiểu được duyệt: inbox/liên hệ + "đăng ký dùng thử miễn phí" (45), hoặc câu hỏi FOMO (38).
- Sub karaoke + luật voice gốc MC (silencedetect, cấm ghép tiếng A hình B đang nói, take nghi vấn trình Sếp nghe) áp nguyên từ style-voice-karaoke.md.

## KIỂU 3 — VOICE-OVER MỚI: 2 CÔNG THỨC CON
<!-- tags: kieu-3 -->

### 3A — "SHOWCASE SẢN PHẨM" (mẫu vàng: VNPT "Robot AI của tương lai" 47.1s)
<!-- tags: kieu-3 -->
- Voice phủ kín ~97% video; câu 10-15 từ (~2.5-3.5s); nhịp cắt ~3.6s/cảnh.
- Cấu trúc: hook tuyên bố đắt ("AI không chỉ nằm trên bảng hiệu, nó đang ở trong bộ não những chú robot này") → đặt người xem vào trải nghiệm ("Lần đầu tiên bước vào sự kiện và người đón bạn là robot") → TỪNG SP lần lượt, mỗi SP 2-3 câu (khả năng → lợi ích) → chốt gom ("3 robot, 1 mục tiêu duy nhất") → CTA theo dõi kênh.

### 3B — "CASE STUDY / PHÓNG SỰ BÀN GIAO" (mẫu vàng: An Phát Xanh 103.5s; bản lai dài: Dragon Thái Bình 177s)
<!-- tags: kieu-3 -->
Cấu trúc 9 nhịp đã kiểm chứng:
1. Danh tiếng khách + tuyên bố bước ngoặt ("một trong những tập đoàn nhựa sinh học lớn nhất VN... ngày nói lời tạm biệt xe vệ sinh có người lái")
2. Đội mình xuất hiện, nhân cách hóa (xưng "em/bọn em", robot là "em MT1", cảm xúc thật "mỗi lần bàn giao vẫn có gì đó đặc biệt")
3. TRƯỚC ĐÂY: cách cũ + nỗi đau (tốn người, tốn phí, "hình ảnh tự động hóa chưa như kỳ vọng")
4. Dẫn lời khách muốn gì
5. Giải pháp: tên robot + 3-4 tính năng NGẮN
6. Các bước setup kể DỄ HIỂU, tên công nghệ luôn kèm giải thích ("quét map — dùng V-SLAM + LiDAR để tự vẽ bản đồ")
7. Demo thử thách trực quan ("em thử ném vật cản bất ngờ ra trước mặt nó")
8. Chia tay + lời chúc (cảm xúc, không bán hàng)
9. CTA đúng chân dung khách ("anh chị nào đang có nhà máy, kho bãi vẫn dùng xe có người lái... comment để bọn em tư vấn")
- Video DÀI (>2 phút): thêm **retention hook** ngay đầu — đặt câu hỏi + "câu trả lời ở cuối video" (Dragon TB), trả lời thật ở ~2/3 video.
- Chi tiết đời thường được GIỮ (gặp bạn cũ trong nhà máy, cô chú công nhân hỏi đùa "thay lao công à") — chất human là gu của kênh, đừng gọt sạch.

### Luật chung Kiểu 3
<!-- tags: kieu-3 -->
- Câu voice 8-15 từ (khớp kichban-template); giọng Việt (MC Xuân Tú / Thanh Ngọc) hoặc giọng Sếp chọn — không dùng George cho lời tiếng Việt.
- Dạng lai (MC trên hình + voice-off chèn — như Dragon TB) = hợp lệ: phần MC theo luật Kiểu 2, phần voice-off theo Kiểu 3, chọn cảnh theo chon-canh-highlight.

## Bảng chọn công thức nhanh
<!-- tags: kieu-2, kieu-3 -->

| Đầu vào | Công thức |
|---|---|
| MC nói 1 take dài giải đáp/giới thiệu | 2A (giữ ~80% lời, B-roll dày) |
| Sự kiện/trải nghiệm MC dẫn mở | 2A hành trình (dẫn ~20 câu đầu, còn lại hình+nhạc) |
| Source từng-câu-từng-clip | 2B listicle (nhịp chậm 5s, chốt FOMO) |
| Cần video bán hàng/cho thuê từ kho take rời | 2C ads (ghép + đảo, bắn liên thanh) |
| Giới thiệu dải SP không có câu chuyện khách | 3A showcase |
| Có buổi bàn giao/khảo sát khách thật | 3B case study (9 nhịp) |

## BỔ SUNG VÒNG 2 (đã khai thác đủ 15/15 bản đối chiếu — 17/07 chiều)
<!-- tags: chung -->

### Kiểu 3 có thêm công thức thứ 3
<!-- tags: kieu-3 -->
**3C — "PHÓNG SỰ SỰ KIỆN + PIVOT THƯƠNG HIỆU"** (mẫu vàng: 19.Du lịch 87.7s, biến thể branding mềm: 10.Vinschool 125.2s)
- Cấu trúc: đặt mình giữa sự kiện lớn ("em được ngồi giữa những người đang dẫn dắt sự thay đổi") → tóm nội dung sự kiện như NGƯỜI THAM DỰ kể lại (không phải MC đọc thông cáo) → nhận định cá nhân ("ngồi nghe cả buổi em nhận ra...") → **PIVOT 1 câu về Roboworld** ("và Roboworld chúng em cũng có mặt ở đó") → SP liên quan → CTA đúng chân dung ngành.
- Biến thể BRANDING MỀM (Vinschool): hook tò mò xã hội ("học phí cả trăm triệu/năm... học sinh học gì nhỉ?"), robot chỉ là bạn đồng hành ("mang em BellaBot đến tham dự"), humor tự trào ("hồi cấp 2 mình đang làm gì nhỉ?"), **KHÔNG CTA bán hàng cứng** — video xây thương hiệu, không phải video bán.
- Nhịp cắt sự kiện hội thảo chậm hơn (8.8s); sự kiện động thì 3.4s.

### Kho hook Kiểu 3 mở rộng (từ các mẫu vàng)
<!-- tags: kieu-3 -->
| Dạng hook | Mẫu nguyên văn |
|---|---|
| Tuyên bố phản trực giác | "AI không chỉ nằm trên bảng hiệu..." (VNPT) |
| Câu hỏi khả thi + hẹn trả lời | "Liệu có khả thi?... câu trả lời ở cuối video" (Nam Sơn, Dragon TB) |
| Insight nghề (phân công người-máy) | "Giao tiếp, tư vấn món... chỉ con người làm tốt; còn bưng bê lặp lại — đó là lý do đưa robot vào" (Cuốn Corner) |
| Tò mò xã hội | "Học phí cả trăm triệu một năm... học sinh học gì nhỉ?" (Vinschool) |
| Danh tiếng khách + bước ngoặt | "Tập đoàn nhựa sinh học lớn nhất VN... ngày nói lời tạm biệt xe có người lái" (APX) |
- Luật nỗi đau: phải là **NỖI ĐAU NGÀNH CỤ THỂ** người trong nghề gật gù ("chỉ thừa bám vào thành phẩm, mất thời gian gỡ chỉ khỏi áo" — Nam Sơn), không nói nỗi đau chung chung.

> **Chuyển đi 24/07/2026**: luật "Kiểu 1 chuẩn vàng — 2 nhánh nhịp" từng nằm ở đây đã dọn sang `style-mau.md` mục "Nhịp dựng" — file `gu-kieu-2-3.md` (tên đã nói rõ) chỉ nên chứa luật Kiểu 2/3, quy trình dựng Kiểu 1 không đọc file này nên nội dung Kiểu 1 để ở đây coi như vô hình.

### Còn nợ
<!-- tags: chung -->
- Dựng thử 1 video Kiểu 2 (2C) + 1 video Kiểu 3 (3A) từ folder 30 → Sếp chấm → tinh chỉnh sổ.
- Cặp VNPT/APX/Nam Sơn source chứa sẵn bản final (match tự thân) — cấu trúc chuẩn nhưng muốn học luật CHỌN CẢNH Kiểu 3 sâu hơn thì cần cặp có source thô thật (Cuốn Corner/Du lịch/Vinschool source thô ĐÃ index đủ, dùng được).

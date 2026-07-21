# Quy tắc chọn cảnh (highlight) từ nguồn thô — áp dụng chung cho cả 3 kiểu dựng

Viết 2026-07-15, dựa trên bằng chứng THẬT (không suy đoán): đối chiếu trực tiếp 1 buổi quay thô — `D:\VIDEO RBW\Edit video\30.Nhà sách Tràng An` (58 clip DJI, quay 2026-07-02) — với **2 video final khác nhau** dựng ra từ đúng nguồn đó: `HUY MKT\34.Nhà sách Tràng An (rv nhà sách)` và `HUY MKT\35.Uyên ads thuê` (quảng cáo cho thuê sự kiện). Cùng 1 buổi quay, 2 mục đích khác nhau → 2 cách chọn cảnh khác nhau, nhưng theo chung 1 bộ nguyên tắc bên dưới.

**Con số thực tế cần nhớ**: 58 clip thô (tổng ~15-20 phút) → 2 video final ~52-63 giây MỖI VIDEO. Tỷ lệ "chọn lọc" cực gắt — phần lớn footage quay được sẽ KHÔNG được dùng, kể cả footage "đẹp". Đừng kỳ vọng dùng hết footage hay, việc của mình là CHỌN ĐÚNG, không phải DÙNG NHIỀU.

## 1. Khi nhiều take cùng nói 1 câu thoại — chọn theo tiêu chí gì

Buổi quay này có RẤT nhiều lần MC nói lặp lại cùng 1 câu kịch bản (để có nhiều lựa chọn khi dựng — đây là cách quay chủ động, nên khuyến khích khi tư vấn Sếp về cách quay). Ví dụ thực tế: câu "khối nghỉ hè đã đổ bộ, bố mẹ lại đau đầu" xuất hiện ở ít nhất 4 clip khác nhau (0014, 0015, 0018, 0019).

Thứ tự ưu tiên khi chọn giữa nhiều take CÙNG nội dung:
1. **Tiếng sạch nhất** thắng trước — kể cả khi take đó hình kém đẹp hơn. Bằng chứng: clip 0025 (MC xoa đầu robot, mặt mèo nheo mắt) tự đánh giá là "cảnh cưng nhất buổi quay" nhưng KHÔNG phải take được chọn — clip 0024 (cùng câu thoại, tiếng rõ hơn) mới là take lên video final. **Đẹp không thắng được sạch tiếng.**
2. Nếu tiếng ngang nhau, ưu tiên take robot có hành động khớp với ý câu nói (vd câu nói về "dẫn đường" thì ưu tiên take có robot đang di chuyển thật, không phải robot đứng yên)
3. Take có PHẢN ỨNG NGƯỜI THẬT tự nhiên (trẻ em cười, khách ngạc nhiên) được ưu tiên hơn take chỉ có MC diễn một mình

## 2. Khi nhiều B-roll gần giống nhau — chỉ 1 cái được dùng

Buổi quay có 5 clip lia cận kệ sách gần như giống hệt nhau (0031, 0033, 0034, 0039, 0044 — đều là "lia kệ sách, không robot", dùng làm nền cho đoạn thoại "4 khay đựng đồ"). Đây là kiểu **quay dự phòng** (backup coverage) — quay nhiều góc/nhiều lần cùng 1 loại cảnh để có lựa chọn, nhưng **thành phẩm chỉ dùng đúng 1**, phần còn lại là hàng dự phòng không lên hình.

Áp dụng: khi rà index.json thấy nhiều clip cùng tag/mô tả gần giống nhau, đừng cố nhét tất cả vào — CHỌN 1 đại diện tốt nhất (rõ nét nhất, bố cục đẹp nhất, hoặc khớp nhịp cắt còn thiếu), bỏ qua phần còn lại.

## 3. Cảnh bị loại thẳng — nhận diện sớm để khỏi phí thời gian

Từ buổi quay này, các loại cảnh sau **hoàn toàn không lên video final** dù chất lượng kỹ thuật tốt ("quality": "tot"):
- **Sai nhân vật/không khớp câu chuyện**: 2 clip MC NAM tự selfie (0057, 0059) — bản final xoay quanh MC Uyên (nữ), nên dù quay đẹp vẫn bị loại vì không đúng người dẫn dắt câu chuyện
- **B-roll không có robot VÀ không có người**: cảnh phố/vỉa hè/mặt tiền đơn thuần (0066, 0067, 0069) — không mang thông tin gì mới, không dùng
- **Trùng lặp dư thừa**: đã nêu ở mục 2

Nguyên tắc: khi rà source, GẠCH BỎ SỚM 2 loại này khỏi danh sách ứng viên để đỡ mất công cân nhắc.

## 3b. LUẬT CẤM CẢNH "MC-CUTAWAY" — áp dụng CẢ 3 KIỂU DỰNG (Sếp bắt lỗi 19/07/2026, 2 lần)

**Luật**: TUYỆT ĐỐI không dùng cảnh **"người đang đứng nói / nhìn trực diện máy quay"** làm B-roll/cutaway, nếu âm thanh phát tại chính giây đó **không phải giọng gốc đồng bộ của chính khoảnh khắc đó**. Khán giả thấy miệng người ta mấp máy mà tiếng lại là của người khác/của voice-over → lộ ngay là ghép ẩu.

**Vẫn được phép**:
- (a) Đúng đoạn đang dùng voice gốc của MC → chèn cảnh **MINH HỌA nội dung đang nói** (MC nói "thu hút khách" → cắt sang cảnh khách vây quanh robot).
- (b) Cảnh **"mọi người nói chuyện với nhau"**, không nhìn máy quay, không rõ đang phát ngôn nội dung nào → dùng trám bình thường.

**Vì sao thành luật cứng**: Sếp bắt đúng lỗi này **2 lần trong 1 ngày, ở 2 kiểu dựng khác nhau** — video-1 (Kiểu 2C có thoại, giây 29.0-30.5: nhân viên áo xanh + bé trai đứng trực diện máy quay trong khi voice đang đọc nốt câu của MC khác) và video-2 (Kiểu 1 không thoại, giây 23.5-26.17, cùng 1 diễn viên áo xanh). Lặp ở 2 kiểu = **lỗi hệ thống trong logic chọn cutaway**, không phải sơ suất lẻ.

**Bước rà soát BẮT BUỘC trước khi chốt mọi video (cả 3 kiểu)**: duyệt lại từng cảnh cutaway, tự hỏi *"trong khung này có ai đang nói/nhìn thẳng máy quay không, và tiếng đang phát có đúng là của chính họ tại chính lúc đó không?"* — sai một trong hai thì thay cảnh. Cảnh thay thế an toàn nhất đã dùng thực tế: người tương tác với robot (trẻ em chạm robot, khách nhảy nhót cạnh quầy).

### 3b-1. LỌC BẰNG CỜ NÀO — chỗ sai đi sai lại (Sếp bắt lỗi lần 3, 21/07/2026)

🔴 **`has_speech` KHÔNG dùng để lọc cảnh này được.** Đó là cờ **ÂM THANH** (Whisper có nghe ra tiếng không). Người trong hình mấp máy môi mà mic không bắt được — vì đứng xa, vì quay ngoài đường ồn — thì `has_speech` vẫn `false`. Lọt lưới hoàn toàn.

✅ **Phải lọc bằng `gemini.co_nguoi_dang_noi`** — đó là cờ **HÌNH**, Gemini nhìn thấy miệng người ta đang nói.

**Đo thật trên folder 30 (21 clip đã quét Gemini):**

| | Số clip |
|---|---|
| Lọc bằng `has_speech=false` | tưởng là 6 clip sạch |
| **Lọt lưới** — `has_speech=false` NHƯNG `co_nguoi_dang_noi=true` | **4 clip** (`0994`, `0007`, `0009`, `0016`) |
| Thật sự sạch (`co_robot=true` + `co_nguoi_dang_noi=false`) | **chỉ 2 clip** |

Ngày 21/07 đã dựng 2 video (Kiểu 1 + Kiểu 3) dùng nhầm **3 trong 4 clip lọt lưới** đó. Sếp xem ra ngay: *"trong hình người nói nhưng không có tiếng, nó kỳ lắm"*.

**Hệ quả dây chuyền phải biết**: lọc đúng thì số clip dùng được **tụt rất mạnh** (6 → 2). Không đủ clip mà vẫn cố dựng cho đủ thời lượng thì sẽ đẻ ra lỗi lặp cảnh ở mục 3d. **Thiếu clip sạch thì phải quét Gemini thêm clip mới, không được quay vòng lấy lại clip cũ.**

## 3d. CẤM LẶP CẢNH — tối kỵ ở CẢ 3 KIỂU (Sếp Huy chốt 21/07/2026)

**Luật**: không lấy lại cùng một cảnh, và cũng không lấy 2 đoạn khác nhau của **cùng một cú máy** nếu người xem nhìn ra là "vẫn cảnh đó". Kể cả 2 clip **khác file** nhưng là 2 lần quay lại cùng một bối cảnh/động tác — nhìn vào vẫn thấy trùng — cũng tính là lặp.

**Vì sao Sếp gọi là tối kỵ**: người xem nhận ra ngay video bị "kéo dài cho đủ giây", cảm giác nghèo tư liệu. Nó phá hỏng cảm giác chuyên nghiệp nhanh hơn mọi lỗi kỹ thuật khác.

**Cách tự bắt trước khi dựng**: lập bảng cảnh rồi đếm — **mỗi file nguồn chỉ nên xuất hiện 1 lần**, tối đa 2 lần nếu 2 đoạn khác hẳn nhau về góc máy/hành động. Thấy 1 file xuất hiện 3 lần trở lên là đang thiếu tư liệu, phải đi tìm clip khác chứ không chia nhỏ clip cũ ra dùng tiếp.

**Ca thật 21/07**: video Kiểu 1 và Kiểu 3 đều dùng `0009` 3 lần, `0021` 3 lần, `0007` 2 lần, `0016` 2 lần. Sếp xem ra ngay từ 5-6 giây đầu.

## 3c. SOI ĐÚNG ĐOẠN SẼ CẮT, không tin khung đại diện của clip (bài học 20/07/2026)

Khi rà nhiều clip cùng lúc, cách nhanh là ghép mỗi clip 1 khung đại diện thành ảnh lưới. **Nhưng khung đó thường lấy ở giữa clip (~45%), còn đoạn định cắt lại nằm ở chỗ khác** — nội dung có thể khác hoàn toàn.

Ca thật (video MT1, buổi bàn giao An Phát Xanh): lưới cho thấy clip `0023` là **người ngồi lái máy chà sàn cũ** — đúng cảnh "cách làm cũ" cần cho hook. Nhưng đoạn cắt đặt ở giây 6-11 lại ra **cảnh xe nâng bốc hàng**, chẳng liên quan. Cảnh đúng nằm ở giây 22. Dựng xong nghiệm thu mới phát hiện, phải dựng lại.

**Luật**: sau khi chốt danh sách cảnh + mốc bắt đầu, **trích 1 khung ở GIỮA từng đoạn sẽ cắt** rồi xem lại một lượt, trước khi chạy dựng. Rẻ hơn nhiều so với dựng lại.

Cách làm (không có script sẵn — viết tại chỗ, ~10 dòng; *sửa 21/07: chỗ này từng trỏ `scratchpad/soi_doan.py`, nhưng scratchpad là thư mục tạm của MỘT phiên, phiên sau không có file đó*):
1. Với mỗi cảnh, tính `mid = bắt_đầu + độ_dài/2`.
2. `ffmpeg -y -ss <mid> -i "<clip>" -frames:v 1 -vf scale=340:-2 soi_sNN.jpg`
3. Ghép các khung thành 1 ảnh lưới bằng filter **`tile`** rồi xem một lượt:
   `ffmpeg -y -i "soi_s%02d.jpg" -vf "scale=340:-2,tile=4x3:padding=6:color=white" -frames:v 1 LUOI.jpg`
   (đừng dùng `drawtext` để dán nhãn — máy dựng thiếu fontconfig nên nó crash, xem `ffmpeg-recipes.md` mục 0.7)

**Hiệu quả đo thật 21/07/2026** (buổi dựng folder 33): bước này bắt được **3/11 cảnh sai** trước khi dựng — 1 cảnh hook yếu, 1 cảnh hoá ra là lưng áo che kín khung chứ không phải nội dung tưởng, 1 cảnh có vật lạ trong khung. Không soi thì cả 3 lọt vào bản final.

**Kèm theo**: tên file clip có phần timestamp rất dễ gõ nhầm (`..._122541_0062_D` vs `..._122749_0062_D`). Tìm clip theo **mã 4 số** (`_0062_D`) chắc hơn gõ cả tên.

## 4. Cảnh dài (60s+) chỉ bị "khai thác" vài giây, không dùng nguyên clip

Buổi quay có nhiều clip rất dài do MC nói liên tục nhiều đoạn kịch bản trong 1 lần bấm quay (0023: 118.5s, 0035: 86.5s, 0051: 60.8s, 0045: 44.5s). Video final chỉ trích ra ĐÚNG câu cần dùng từ mỗi clip dài này, cắt bỏ phần còn lại (kể cả khi phần còn lại cũng có thoại).

Áp dụng: đừng ngại clip dài — cứ xem hết transcript của nó, tìm ĐÚNG câu/đoạn cần cho kịch bản đang viết, cắt phần đó ra, KHÔNG cần dùng nguyên clip hay lo "phí" phần còn lại.

## 5. Nguyên tắc chọn cảnh mở đầu (hook) — theo từng kiểu dựng

Đã có nguyên tắc chung trong `style-mau.md` (reveal moment > tương tác người thật > chuyển động ấn tượng > cảnh hành chính), nhưng đối chiếu thêm với nhóm ADS (SH1/CC1/MT1 ads) cho thấy **hook phụ thuộc vào kiểu dựng đang dùng**:

- **Kiểu 1 (chỉ nhạc/B-roll, không thoại)**: hook = khoảnh khắc reveal/bất ngờ hoặc tương tác người-robot mạnh nhất, đúng như style-mau.md đã ghi
- **Kiểu 2 (voice gốc/thoại sẵn có)**: hook = câu thoại đầu tiên chạm đúng nỗi đau/tò mò của khán giả, hình đi kèm là chính người nói (không cần cảnh "đẹp" nhất, cần người nói tự nhiên nhất)
- **Kiểu 3 (voice over thêm vào, ghép nhiều cảnh)**: hook theo công thức "hiện trạng vấn đề" — LUÔN mở bằng cảnh MINH HOẠ CÁCH LÀM CŨ/THỦ CÔNG kém hiệu quả trước (người lau sàn tay, ke gạch bẩn cận cảnh...), rồi mới cắt sang giới thiệu robot ở giây thứ 8-12. Đây là mẫu số chung ở CẢ 3 video ADS-VO (SH1/CC1/MT1) — không dùng cảnh robot đẹp làm hook cho kiểu này, phải dựng đối lập vấn đề trước.

## 6. Cảnh "phải có" xuyên suốt thân video (không phân biệt kiểu dựng)

Đối chiếu toàn bộ 15 video đã phân tích sâu, các loại cảnh sau lặp lại ở hầu hết video và nên chủ động tìm khi rà source:
- **Cận cảnh chi tiết khớp ĐÚNG với thông số đang nói/viết** (nói "27kg gọn nhẹ" → phải có cận tay cầm; nói "4 khay" → phải có cảnh khay mở ra) — không dùng cảnh robot chung chung để minh hoạ thông số cụ thể
- **Phản ứng người thật** (trẻ em, khách hàng, nhân viên) — xuất hiện ở gần như mọi video, kể cả video kỹ thuật/hướng dẫn
- **Màn hình/UI thật của robot** (không phải đồ hoạ chèn) khi có sẵn trong cảnh — dùng làm bằng chứng "thật", đáng tin hơn chữ đè
- **Robot di chuyển ở nhiều bối cảnh/góc khác nhau** nếu mục đích là chứng minh độ phủ (đặc biệt Kiểu 3)

## 7. Khi rà 1 buổi quay mới, việc đầu tiên nên làm

Trước khi viết kịch bản, sau khi có index.json đầy đủ: quét nhanh xem source có đủ 4 nhóm cảnh không — (a) ít nhất 1 cảnh hook mạnh đúng kiểu dựng sẽ chọn, (b) đủ cận cảnh khớp từng thông số dự kiến sẽ nhắc tới, (c) có phản ứng người thật hay không, (d) có cảnh kết/CTA tự nhiên hay không. Thiếu nhóm nào thì báo Sếp TRƯỚC khi viết kịch bản, đừng bịa cảnh không có.

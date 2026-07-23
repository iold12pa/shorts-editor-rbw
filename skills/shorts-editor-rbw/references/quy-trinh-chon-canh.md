# QUY TRÌNH CHỌN CẢNH — công cụ nào dẫn, công cụ nào đối chiếu
<!-- tags: chung -->

## 🔴 KHÔNG ĐỦ CHỖ ĐỂ LÀM TỬ TẾ THÌ DỪNG VÀ BÁO — CẤM CẮT XÉN (luật 22/07/2026, sau khi Sếp Huy trả về 3 video)
<!-- tags: chung -->

**Ca thật, phải nhớ**: cuối một phiên chat rất dài, skill được giao dựng 3 video từ folder 58 clip. Ngữ cảnh sắp cạn → thay vì báo, nó **tự cắt xén quy trình**: mở **4/58 ảnh lưới** rồi dựng cả 3 video từ đúng 5 clip.

| Video | Số cảnh | Lấy từ mấy clip | Hậu quả |
|---|---|---|---|
| Kiểu 1 | 10 | **5** | 0042 ×3 · 0010 ×3 · 0036 ×2 — lặp thấy rõ |
| Kiểu 3 | 10 | **cùng 5 clip đó** | lặp cả trong video lẫn với video kia |
| Kiểu 2 | 5 | 3 đoạn thoại | mỗi đoạn **9-10 giây một cú máy tĩnh**, không cắt B-roll |

Kho có **34 clip robot, 38 clip hình tốt**. Dùng đúng 5. Sếp: *"cực kì dở và đa phần dính vào các lỗi tôi đã góp ý rồi"*.

**Ba thứ bị bỏ, đều là bước BẮT BUỘC sinh ra sau lần Sếp bắt lỗi 21/07:** mở đủ ảnh lưới clip ứng viên *(mở 4, cần 20-30)* · bước 2d đếm tư liệu + 4 cổng lọc · nghiệm thu tầng B rà lặp cảnh *(chỉ chạy tầng kỹ thuật rồi báo "đạt")*.

**LUẬT:**
- **Ước lượng TRƯỚC khi nhận việc**: N video × ~10 cảnh cần mở ảnh lưới của **ít nhất 20-25 clip ứng viên**. Không đủ chỗ cho ngần đó → **DỪNG, BÁO NGƯỜI DÙNG NGAY**, đề nghị mở phiên chat mới. Đây là một dạng **thiếu nguyên liệu**, cùng loại với thiếu clip sạch.
- **CẤM tự hạ chuẩn để vừa sức**: giảm số clip mở · bỏ bước đếm · bỏ rà lặp · giữ nguyên cú máy dài thay vì cắt nhịp. Mọi cách "làm cho xong" đều **tệ hơn việc nói thẳng là chưa làm được**.
- **Người dùng cho phép dùng lại cảnh cũ ≠ cho phép xào 5 clip trong một video.** Hiểu nới rộng theo hướng có lợi cho mình là sai. Cho phép trùng **giữa video mới và video cũ**; **trong cùng một video vẫn cấm lặp**.
- **Kiểu 2 không được giữ nguyên cú máy dài**: công thức 2C là **~3s/cảnh**, thoại dài phải **cắt B-roll đè lên** trong khi tiếng chạy liền mạch. Để nguyên 10 giây một khung là lỗi, không phải phong cách.

> Sếp Huy chốt 21/07/2026, sau khi xem 3 video và bắt 3 lỗi nội dung mà toàn bộ hệ nghiệm thu kỹ thuật đều báo "đạt".
>
> **Yêu cầu gốc của Sếp**: *"đoạn nào cần cắt theo thoại thì ưu tiên cắt bằng âm thanh, đoạn nào không có thoại thì dùng hình ảnh để lấy chuẩn cái đẹp nhất, linh hoạt cho từng trường hợp nhưng phải cho ra đầu ra tốt nhất. Khi chọn hình ảnh hay âm thanh thì dùng dữ liệu từ TẤT CẢ các công cụ để đưa ra quyết định cuối cùng."*

---

## 0. ĐÃ NGHIỆM THU BẰNG TAI SẾP — giữ nguyên cách này (Sếp chốt 21/07/2026)
<!-- tags: chung -->

> Nguyên văn Sếp sau khi xem 3 video dựng theo quy trình này: *"đầu ra giờ khá oke rồi nên cái cách đối chiếu các công cụ khác nhau để cho ra kết quả tốt nhất về cả hình ảnh và âm thanh này khá ổn, lưu lại nhé."*

**Cốt lõi đã được xác nhận là đúng**: mỗi quyết định (cắt ở đâu, chọn cảnh nào, mức nhạc bao nhiêu) không dựa vào MỘT công cụ, mà **đối chiếu nhiều công cụ**, mỗi công cụ trả lời phần nó giỏi nhất, và khi chúng mâu thuẫn thì **mở ra xem/nghe thật** chứ không tin công cụ nào mù quáng.

**Ba lần đối chiếu này đã cứu lỗi thật trong buổi dựng 21/07:**
1. **Hình**: Gemini gắn cờ clip 0043 "có người đang nói" → nhưng mở **ảnh lưới** thấy 10/10 khung robot đẹp không người → dùng được (nếu tin cờ thì mất clip đẹp nhất). Ngược lại clip 0045 cờ báo có người → ảnh lưới xác nhận đúng (MC cầm mic) → loại. Cùng một cờ, hai kết quả ngược nhau, chỉ ảnh lưới phân biệt được.
2. **Âm thanh cắt**: `loc_thoai_that` cho mốc thô → nhưng **Whisper nghe lại lát cắt** phát hiện mất chữ "Nhưng nhà" → lùi biên 0.4s.
3. **Âm thanh mix**: đo thấy chữ "nhà sách" nghe không rõ → đối chiếu voice gốc vs mix từng 0.1s → hoá ra MC ngắt hơi + nhạc nền lấp khoảng ngắt (không phải mất chữ, không phải SFX) → hạ nhạc nền riêng câu đó.

**Đừng rút gọn thành "tin công cụ X".** Sức mạnh nằm ở chỗ đối chiếu + mở ra kiểm khi mâu thuẫn.

### 0b. VAI TRÒ THẬT của mắt AI (Gemini) — Sếp làm rõ 21/07
<!-- tags: chung -->

> Nguyên văn: *"vai trò thực sự của mắt AI đang là chọn ra được các khoảnh khắc đẹp chứ không phải xác định người có đang nói không. Tôi thấy cái đấy đang làm khá ổn rồi. Dù vậy càng nhiều con để đối chiếu thì càng tốt."*

**Giá trị chính của Gemini = chấm KHOẢNH KHẮC ĐẸP** (`khoanh_khac` + điểm 1-10). Đây là thứ nó giỏi và đang làm tốt — **giữ nguyên, đừng đụng**.

**`co_nguoi_dang_noi` KHÔNG phải vai trò chính của Gemini** — nó chỉ là **một trong nhiều tín hiệu đối chiếu** cho câu "có người đang nói không". Cờ này sai cả 2 chiều (0043, 0045), nên **không được coi nó là câu trả lời**; nó chỉ là một phiếu, và **ảnh lưới (mắt người) mới là trọng tài**.

**Nguyên tắc bao trùm — MỌI con chỉ là công cụ ĐỐI CHIẾU, không con nào là trọng tài.** Càng nhiều con đối chiếu càng chắc, nhưng quyết định cuối luôn là **mắt/tai người** khi các con mâu thuẫn.

**Thêm con mới thì được, NHƯNG không được phá con đang chạy** (đo thật 21/07): thử cài **MediaPipe** (đo môi động để biết ai đang nói) — đúng việc về lý thuyết, nhưng nó đòi `numpy 2.x` + protobuf cũ, xung đột với `numpy<2` (cv2 cần) và protobuf mới (google-genai cần). Cài vào là phá cả cv2 lẫn Gemini. **Đã gỡ.** Bài học: con đối chiếu mới phải **không đụng dependency** của con đang chạy — ưu tiên thứ dùng lib đã có (vd `cv2` có sẵn face detection, không cần cài gì) hơn là kéo cả bộ mới về.

## 1. Nguyên tắc gốc
<!-- tags: chung -->

Mỗi đoạn video có **đúng một câu hỏi chính**. Công cụ nào trả lời được câu đó thì công cụ đó **DẪN**. Các công cụ còn lại **không biến mất** — chúng chuyển sang vai **ĐỐI CHIẾU**, và vẫn có quyền phủ quyết ở những chỗ chúng giỏi hơn.

Sai lầm phải tránh: **dùng một công cụ cho mọi việc**, hoặc **dùng công cụ mình vừa xây thay vì công cụ đúng việc**.

> Ca thật 21/07: cả buổi đang làm hệ đo âm thanh nên khi cần lọc "cảnh có người đang nói", đã với tay lấy `has_speech` (cờ ÂM THANH) thay vì `co_nguoi_dang_noi` (cờ HÌNH) — dù cả hai nằm cạnh nhau trong cùng file index.

---

## 2. Phân vai theo loại đoạn
<!-- tags: chung -->

| Loại đoạn | Câu hỏi chính | Công cụ **DẪN** | Công cụ **ĐỐI CHIẾU** |
|---|---|---|---|
| **Giữ nguyên lời người nói** (Kiểu 2, và Kiểu 3 khi dùng voice gốc) | Cắt ở đâu để không mất chữ? | `loc_thoai_that` — đo mức + độ ấm trên âm thanh gốc | Whisper nghe lại lát cắt (bắt buộc) · **Gemini chấm đoạn nào ĐẸP** (vai trò chính của Gemini) |
| **Không thoại** (Kiểu 1, B-roll) | Khung nào đẹp nhất, robot đang làm gì? | **Gemini `khoanh_khac` (chấm khoảnh khắc đẹp — vai trò chính)** + ảnh lưới | `do_ky_thuat` (nét/rung) · `co_nguoi_dang_noi` (chỉ 1 phiếu, ảnh lưới kiểm cuối) |
| **B-roll đè lên voice khác** (Kiểu 3 có voice-over mới) | Cảnh nào minh hoạ đúng lời đang đọc? | Gemini `khoanh_khac` + ảnh lưới | `co_nguoi_dang_noi` (1 phiếu) → **ảnh lưới quyết** loại cảnh có người nói |

**Đọc bảng này cho đúng**: "DẪN" nghĩa là *lấy con số/lựa chọn từ đó*. "ĐỐI CHIẾU" nghĩa là *nếu nó mâu thuẫn thì phải dừng lại xem xét, không được lờ đi*.

### 2b. Hai cái bẫy khi đọc kết quả `loc_thoai_that` (đo thật 21/07)
<!-- tags: chung -->

**Bẫy 1 — trường `loi` báo DƯ CHỮ.** Nó ghép từ các đoạn Whisper *giao nhau* với lát cắt, nên hiện nhiều chữ hơn thực tế lát cắt chứa.

> Ca thật: đoạn `11.90-17.20` hiện lời *"nhưng nhà sách rộng thế này biết quầy nào mà tìm…"*, nhưng cắt ra nghe lại chỉ còn từ *"sách rộng thế này"* — **mất "Nhưng nhà"**. Biên đúng là **11.50**.
>
> → **Luôn cho Whisper nghe lại chính lát cắt trước khi chốt.** Đây chính là phép rà bắt buộc ở `SKILL.md` bước 4 mục 7 — bỏ nó là giao hàng với câu cụt đầu.

**Bẫy 2 — script KHÔNG dùng được cho file TTS (giọng máy đọc).** Nó tính sàn nhiễu từ chính clip; file TTS thì khoảng lặng là **im tuyệt đối** nên phép tính vô nghĩa — chấm cả 3 đoạn giọng là "XA MIC", có đoạn ra `cách sàn = -21.8 dB`.

| Loại file | Đo mốc bằng |
|---|---|
| Tiếng **thu thật** (có ồn nền) | `loc_thoai_that.py` |
| File **TTS máy đọc** | **`silencedetect`** |

---

## 3. Bốn cổng mọi cảnh phải qua
<!-- tags: chung -->

Xét theo thứ tự. Rớt cổng nào thì loại luôn, không xét tiếp.

### Cổng 1 — LOẠI (phủ quyết, không thương lượng)
<!-- tags: chung -->

| Điều kiện | Nguồn dữ liệu | Ngoại lệ duy nhất |
|---|---|---|
| `co_nguoi_dang_noi = true` | Gemini (cờ HÌNH) | Đang dùng **chính giọng đồng bộ của người đó tại chính giây đó** |
| Không có robot trong khung | Gemini `co_robot` | Kịch bản **đang nói về đúng bối cảnh đó** (thẻ chữ đang là tên nhà sách → được lấy cảnh nhà sách) |
| `do_ky_thuat` gắn cờ `mo` | Đo kỹ thuật | Mờ có chủ ý (bokeh, motion blur) — phải **xem ảnh lưới xác nhận**, không tin cờ suông |

⚠️ **`has_speech` KHÔNG dùng ở cổng này.** Đó là cờ âm thanh. Người mấp máy môi mà mic không bắt được vẫn lọt. Đo thật folder 30: lọc bằng `has_speech` sót **4/21 clip**.

### Cổng 2 — CHẤT LƯỢNG HÌNH
<!-- tags: chung -->

- Robot **ở giữa khung, chính diện, đang hoạt động** (ưu tiên cao nhất cho Kiểu 1 — xem `style-mau.md`)
- `do_net` cao, không rung
- Cờ `net-tung-doan` → phải chọn **đúng đoạn nét**, không lấy cả clip

### Cổng 3 — KHỚP NỘI DUNG
<!-- tags: chung -->

- Cảnh có minh hoạ đúng **thẻ chữ / lời đang nói tại chính giây đó** không?
- Không khớp thì đổi cảnh **hoặc** đổi chữ — không để lệch.

> Ca thật 21/07: thẻ "4 KHAY CHỞ ĐỦ THỨ" rơi vào cảnh khách bấm màn hình, còn "KHÁCH TỰ BẤM CHỌN" rơi vào cảnh robot đi. Phải canh lại theo mốc từng cảnh.

### Cổng 4 — ĐA DẠNG (chống lặp — tối kỵ)
<!-- tags: chung -->

- **Mỗi file nguồn xuất hiện tối đa 1 lần**; 2 lần chỉ khi hai đoạn khác hẳn nhau về góc máy và hành động.
- Hai clip **khác file** nhưng là 2 lần quay lại cùng bối cảnh → vẫn tính là lặp.
- Thấy một file phải dùng 3 lần trở lên = **đang thiếu tư liệu**, sang mục 4.

---

## 4. ĐẾM TƯ LIỆU TRƯỚC KHI VIẾT KỊCH BẢN — bước mới, bắt buộc
<!-- tags: chung -->

**Sai lầm cũ**: viết kịch bản 10 cảnh trước, rồi đi tìm footage lấp vào. Không đủ thì kéo dãn cái đang có → đẻ ra lặp cảnh.

**Thứ tự đúng**:

1. Lọc toàn bộ clip qua **Cổng 1**, đếm số clip còn lại.
2. Ước lượng: `số clip sạch × 3 giây ≈ thời lượng tối đa dựng được không lặp`.
3. So với thời lượng định làm:
   - **Đủ** → viết kịch bản, dựng bình thường.
   - **Thiếu** → **DỪNG, BÁO NGƯỜI DÙNG**, đưa 3 lựa chọn: (a) quét thêm clip bằng mắt AI — nói rõ tốn bao nhiêu tiền và footage sẽ rời máy lên cloud; (b) rút ngắn video cho vừa tư liệu; (c) bổ sung footage mới.

🔴 **Thiếu tư liệu là một dạng BỊ CHẶN — áp luật DỪNG-BÁO.** Luật cũ chỉ nói về *lỗi/bị chặn kỹ thuật*; nay mở rộng sang **thiếu nguyên liệu**. Tự xoay xở bằng cách lấy lại clip cũ là **sai quy trình**, kể cả khi video vẫn xuất ra được.

> Ca thật 21/07: folder 30 lọc đúng chỉ còn **2 clip sạch** trong 21 clip đã quét. Đáng lẽ phải dừng báo ngay; thay vào đó đã quay vòng lấy lại clip → Sếp thấy lặp ngay 5-6 giây đầu.

---

## 5. Ảnh lưới — bước rẻ nhất, hay bị bỏ nhất
<!-- tags: chung -->

`analyze_footage.py` **tạo sẵn 1 ảnh lưới cho MỖI clip** trong `Workspace/analysis/sheets/`, khung lấy đúng điểm đổi cảnh, **có nhãn giây trên từng khung**.

🔴 **LUẬT: chưa mở ảnh lưới của một clip thì KHÔNG được đưa clip đó vào kịch bản.**

**Mô tả bằng chữ của Gemini KHÔNG thay được việc nhìn.** Nó dùng để **thu hẹp danh sách phải xem**, không dùng để thay việc xem.

> Bằng chứng 21/07: clip `0016` được Gemini mô tả là *"Người phụ nữ cúi xuống tương tác với màn hình của robot"*. Mở ảnh lưới ra thì khung 0.3s và 1.9s cho thấy cô ấy **đứng thẳng, quay vào máy quay, miệng đang nói**. Mô tả sai hoàn toàn. Clip này đã lọt vào 2 video.

**Cỡ ảnh**: xem ở **ít nhất 340px/khung**. Ảnh nhỏ hơn không nhìn ra miệng ai đang mấp máy — đã dính thật khi rà bằng ảnh 250px.

---

## 6. Nghiệm thu 2 TẦNG — tầng nội dung là tầng máy không đo được
<!-- tags: chung -->

Nghiệm thu cũ toàn tiêu chí đo bằng máy, nên **mọi con số xanh mà video vẫn sai**.

### Tầng A — kỹ thuật (máy đo, đã có sẵn)
<!-- tags: chung -->
Âm lượng -14 LUFS · 1080x1920 · chữ không tràn viền · không frame đen · thời lượng đúng.

### Tầng B — nội dung (BẮT BUỘC, chỉ mắt người làm được)
<!-- tags: chung -->

| Câu hỏi tự kiểm | Rớt thì làm gì |
|---|---|
| Xem lại từ đầu — có cảnh nào **thấy quen** không? | Có = đang lặp, thay cảnh |
| Có ai trong hình **đang nói mà không nghe tiếng họ** không? | Có = vi phạm cổng 1, thay cảnh |
| Robot có phải **nhân vật chính** của mọi cảnh không? (Kiểu 1) | Không = cảnh thừa, thay |
| Từng thẻ chữ có rơi đúng cảnh minh hoạ nó không? | Không = canh lại mốc chữ |
| Nghe thử: nhạc có át lời không, hay nhạc quá bé? | Xem `ffmpeg-recipes.md` mục 5 — mức nhạc khác nhau giữa giọng thu thật và giọng máy |

**Cách làm tầng B**: trích 6-8 khung **ở 340px trở lên**, xem một lượt, tự trả lời 5 câu trên. Đừng báo "đạt chuẩn" khi mới chỉ chạy xong tầng A.

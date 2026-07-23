# Từ lựa chọn của người dùng → tới sản phẩm
<!-- tags: chung -->

> **Luật Sếp Huy chốt 22/07/2026.** Nguyên văn: *"những cái tôi bạn xây dựng lại giờ nó không phải là chỉ để chọn và để đấy... nó là thứ trực tiếp ảnh hưởng đến video bạn làm ra. Hãy làm một bộ quy tắc để biến những đầu vào này của người dùng gần nhất với sản phẩm đó ra. Tuy nhiên về những quy tắc edit, quy tắc chọn cảnh thì vẫn phải tuyệt đối tuân theo những gì đã xây dựng từ đầu — cái này chỉ là dẫn dắt thôi. Và sẽ luôn phải có những phản biện từ bạn, từ nguồn thật, với những gì người dùng mong muốn."*

## 0. Ba tầng quyền — nhớ thứ tự này trước khi đọc tiếp
<!-- tags: chung -->

| Tầng | Là gì | Quyền |
|---|---|---|
| **1. LUẬT DỰNG** | `chon-canh-highlight.md` · `quy-trinh-chon-canh.md` · `style-*.md` · `gu-kieu-2-3.md` · `ffmpeg-recipes.md` | **TUYỆT ĐỐI**. Đúc kết từ video thật Sếp đã duyệt. Lựa chọn của người dùng **không ghi đè được** |
| **2. LỰA CHỌN người dùng** | Những gì họ bấm + câu mở họ gõ | **DẪN DẮT**. Quyết hướng đi, không quyết cách làm |
| **3. TƯ LIỆU THẬT** | Những gì máy đọc được từ footage | **CHẶN**. Không có cảnh thì mọi mong muốn đều vô nghĩa |

**Xung đột thì báo, đừng tự xử im lặng.** Tầng 1 thắng tầng 2, nhưng **phải nói cho người dùng biết vì sao** — họ có quyền hiểu tại sao ý mình không được làm y nguyên.

---

## 1. Bảng ánh xạ — mỗi lựa chọn đổi cái gì trong sản phẩm
<!-- tags: chung -->

Đây là phần cốt lõi: người dùng bấm xong thì **video phải khác đi thật**, không phải chỉ ghi vào biên bản.

### Hướng dựng
<!-- tags: chung -->

| Chọn | Sản phẩm phải khác thế nào |
|---|---|
| **Text + nhạc** | Không một giây voice. Câu chuyện kể **hoàn toàn bằng chữ đè + nhịp cắt**. Chữ IN HOA 5-9 từ, mỗi thẻ chữ 1 SFX pop. Nhịp bám beat nhạc. Cảnh phải **tự nói được** — cảnh cần lời giải thích mới hiểu thì loại |
| **Voice-over** | Lời viết trước, **cảnh chọn theo lời** chứ không ngược lại. Mỗi câu 8-15 từ. Cảnh phải minh hoạ đúng câu đang đọc — nói "robot né người" thì hình phải có người |
| **MC dẫn** | Lời có sẵn là **xương sống bất biến**, cấm sửa lời. Cảnh cắt theo nhịp thở của người nói. Mốc cắt lấy từ `loc_thoai_that.py`, **không lấy từ Whisper** |

### Số lượng video
<!-- tags: chung -->

| Chọn | Sản phẩm phải khác thế nào |
|---|---|
| **1 video** | Dồn hết cảnh mạnh nhất vào một cái. Được phép "xa xỉ" — cảnh đẹp nhất đặt ở hook |
| **2-3 video** | **Chia cảnh trước khi viết kịch bản**, mỗi video một bộ cảnh riêng. Tầng 2 của luật tránh trùng. Đủ thì mỗi video có hook riêng đủ mạnh; **thiếu thì DỪNG-BÁO**, cấm tự xào lại |
| **Để tôi đề xuất** | Đếm cảnh sạch trước, chia cho ~7 cảnh/video, **báo con số kèm lý do** — không im lặng chọn |

### Kênh đăng
<!-- tags: chung -->

| Chọn | Sản phẩm phải khác thế nào |
|---|---|
| **Page công ty** | Có logo trắng giữa-trên + outro dọc 9s. Giọng văn **chỉn chu**, xưng danh Roboworld. Số liệu phải chính xác tuyệt đối — sai số trên page chính thức là mất uy tín |
| **Kênh cá nhân** | **Bỏ hẳn logo và outro.** Giọng văn **đời thường**, như người thật quay được rồi kể lại. Hook nghiêng về khoảnh khắc thật hơn là thông điệp bán hàng |
| **Cả hai** | Dựng một lần, xuất 2 bản. **Không chỉ khác logo** — bản cá nhân nên đổi cả câu chốt cho bớt mùi quảng cáo |

### Nhạc
<!-- tags: chung -->

| Chọn | Sản phẩm phải khác thế nào |
|---|---|
| **Nhạc trend** | **Nhịp cắt bám beat** — đây là lý do chính dùng nhạc trend. Cắt lệch beat thì mất hết cái hay. Ghi rõ trong caption: chỉ đăng Facebook |
| **Không bản quyền** | Nhịp cắt theo **nội dung cảnh**, không bị bó theo beat. An toàn mọi nền tảng |
| **ElevenLabs đo ni** | Mô tả nhạc bằng tiếng Anh **bám đúng cảm xúc kịch bản**, dài đúng bằng video → không phải fade ép ở cuối |
| **Giữ tiếng gốc** | **Không đè nhạc.** Phải chọn cảnh có tiếng hiện trường đáng nghe — tiếng khách trầm trồ, tiếng robot chạy. Cảnh im lặng vô hồn thì loại |

### Giọng đọc (chỉ Voice-over)
<!-- tags: kieu-3 -->

| Chọn | Sản phẩm phải khác thế nào |
|---|---|
| **MC Xuân Tú** | Văn phong **dẫn chương trình** — câu rõ ràng, có nhịp, hợp phóng sự/sự kiện |
| **Thanh Ngọc** | Giọng Nam → văn phong **gần gũi, tư vấn**. Tránh từ ngữ đặc Bắc nghe lệch giọng |
| **Phương Uyên** | Giọng của chính Roboworld → hợp **kể chuyện khách hàng**, xưng "bên mình" tự nhiên |
| **Adam** | Câu **ngắn, dứt khoát**, nhiều số liệu. Gốc tiếng Anh nên tránh câu nhiều từ Hán-Việt khó |
| **Để tôi chọn** | Viết kịch bản trước → chọn giọng theo chất văn → **báo lại đã chọn ai và vì sao** |

### Mức phủ giọng
<!-- tags: kieu-2, kieu-3 -->

| Chọn | Sản phẩm phải khác thế nào |
|---|---|
| **Giọng dẫn ở đầu** | Lời chỉ 1-2 câu mở. **Phần sau phải đủ mạnh để tự kể** bằng hình + chữ. Nhạc dâng `0.18 → 0.55` |
| **Voice-over full** | Lời phủ gần hết → **kịch bản phải kín**, không có khoảng chết. Nhạc nhỏ suốt bài `0.12-0.20` |
| **Nhạc cả bài, giọng phủ lên** | Nhịp sôi động. ⚠️ Nhạc có giọng hát là **hỏng** — bắt buộc bài không lời |

---

## 2. Xử lý câu mở — biến chữ người dùng gõ thành quyết định dựng
<!-- tags: chung -->

Câu mở là thứ **giàu thông tin nhất** trong cả bước hỏi. Bóc theo 4 nhóm, mỗi nhóm ra một quyết định cụ thể:

| Họ nói gì | Biến thành quyết định gì |
|---|---|
| **Bối cảnh** — nơi chốn, khách hàng, robot dòng nào | Tên riêng đưa vào chữ đè/lời đọc *(chỉ khi footage quay đúng ở đó)* · chọn đúng thông số robot từ `robot-products.md` · tránh bịa |
| **Thông điệp** — muốn nói điều gì | Quyết **hook** và **câu chốt**. Bán hàng → hook chạm nỗi đau + CTA rõ. Khoe năng lực → hook quy mô + proof point. Kể chuyện khách → hook khoảnh khắc thật |
| **Thứ tự cảnh** — mở bằng gì, kết bằng gì | Ràng buộc cứng lên bảng phân cảnh. ⚠️ Nếu cảnh họ muốn mở đầu **yếu về mặt hook** (theo `chon-canh-highlight.md`) → vẫn làm theo ý họ nhưng **phản biện 1 câu** kèm lý do |
| **Ràng buộc** — cảnh cấm, tên đọc đúng, độ dài | Áp thẳng, không bàn. Cảnh cấm → loại khỏi mọi video. Độ dài lệch vùng vàng 25-40s → làm theo + nói rõ đánh đổi |

**Không có câu mở** → nói rõ *"không có mô tả nên tôi bám theo những gì đọc được trong clip"*, rồi tự quyết theo luật dựng. **Không đọc được nghĩa** → hỏi lại, cấm diễn giải bừa.

---

## 3. 🔴 PHẢN BIỆN BẮT BUỘC — ba tầng đối chiếu trước khi dựng
<!-- tags: chung -->

> Sếp: *"sẽ luôn phải có những phản biện từ bạn, từ nguồn thật, với những gì người dùng mong muốn."*

Nhận đủ đầu vào rồi **không được lao vào dựng ngay**. Chạy 3 phép đối chiếu này trước:

### Tầng A — mong muốn ↔ TƯ LIỆU THẬT
<!-- tags: chung -->

Đối chiếu từng ý họ nêu với những gì máy đọc được. Câu hỏi phải trả lời: *"cảnh họ muốn có thật trong folder không?"*

- Có → dùng, ghi rõ clip nào
- **Không có** → **BÁO NGAY**, đừng thay bằng cảnh gần giống rồi im lặng. Người duyệt tưởng đã có mới là hỏng
- Có nhưng chất lượng kém (rung, mờ, lọt người đang nói) → báo kèm phương án: dùng cảnh khác, hay chấp nhận?

### Tầng B — mong muốn ↔ LUẬT DỰNG
<!-- tags: chung -->

Ý họ có phạm luật đã đúc kết không? Các ca hay gặp:

| Mong muốn | Luật va phải | Xử lý |
|---|---|---|
| Mở đầu bằng cảnh toàn cảnh rộng cho "hoành tráng" | Hook phải **bắt mắt trong 3 giây đầu**; toàn cảnh rộng thường yếu | Làm theo ý họ + phản biện 1 câu, đề xuất cảnh thay |
| Muốn nhét nhiều thông tin, video 60s+ | Vùng vàng **25-40s** | Báo đánh đổi: dài hơn thì tỉ lệ xem hết giảm |
| Muốn dùng lại cảnh đẹp ở cả 3 video | Cấm trùng cảnh **2 tầng** | Báo thiếu tư liệu, **hỏi có được xào lại không** |
| Muốn nhạc trend cho video voice-over full | Nhạc có giọng hát đè lời | Báo + đề xuất 2 bài không lời còn lại |

**Nguyên tắc**: luật thắng, nhưng **người dùng có quyền biết vì sao** và có quyền yêu cầu làm theo ý mình. Họ khăng khăng → làm theo, ghi lại là theo yêu cầu của họ.

### Tầng C — mong muốn ↔ HIỆU QUẢ THẬT
<!-- tags: chung -->

Đối chiếu với gu đã đúc kết từ video final Sếp duyệt (`gu-kieu-2-3.md`, `chon-canh-highlight.md`):

- Hook mở bằng "Xin chào" → **luật đinh: không bao giờ**
- Nhịp cắt quá thưa so với công thức của kiểu đó (2A 1.8-2.1s · 2B ~5.3s · 2C ~3s/cảnh — bảng đầy đủ mọi kiểu: `quy-trinh-chon-canh.md` mục 4b)
- CTA nhét giữa video thay vì cuối
- Chữ đè quá nhiều chữ, đọc không kịp trong thời lượng cảnh

### Trình bày phản biện thế nào
<!-- tags: chung -->

**Không phải bàn lùi.** Mỗi phản biện đủ 3 phần, gói trong 2-3 câu:

1. **Ý họ là gì** — nhắc lại để họ biết mình được hiểu đúng
2. **Va vào cái gì** — luật nào, hay tư liệu thiếu gì, kèm **số đo thật**
3. **Đề xuất thay thế** — luôn có phương án, không chỉ nêu vấn đề

> *Ví dụ*: "Sếp muốn mở đầu bằng cảnh toàn khu du lịch cho thấy quy mô. Nhưng theo quy tắc chọn cảnh đúc kết từ video Sếp đã duyệt, hook 3 giây đầu cần cảnh bắt mắt ngay — toàn cảnh rộng người xem chưa kịp thấy gì đã lướt. Tôi đề xuất mở bằng cảnh robot tiến thẳng tới ống kính (clip 0043), rồi cắt sang toàn cảnh ở giây thứ 4 để giữ ý quy mô của Sếp. Sếp vẫn muốn giữ nguyên thì tôi làm theo."

---

## 4. 🔴 PHẢN BIỆN CHỈ ÁP CHO NHÁNH "TRAO ĐỔI TIẾP" (Sếp Huy chốt 22/07/2026)
<!-- tags: chung -->

> Nguyên văn: *"nếu họ chọn làm luôn thì cứ làm, không cần phản biện, coi những gì họ nói là tham khảo thôi."*

| Người dùng chọn | Mong muốn của họ được coi là | Phản biện |
|---|---|---|
| **Trao đổi tiếp** | **Yêu cầu** — bám sát, va luật thì báo và bàn | ✅ Chạy đủ 3 tầng A/B/C ở mục 3 |
| **Làm luôn** | **THAM KHẢO** — dùng để định hướng, không phải mệnh lệnh | ❌ **KHÔNG phản biện. Cứ làm.** |

**Nhánh "làm luôn" xử lý xung đột thế nào:** ý họ đá với luật dựng → **im lặng theo LUẬT DỰNG**, không hỏi, không báo, không đề xuất thay thế. Họ đã chọn giao việc cho máy thì đừng bắt họ quay lại quyết từng chi tiết.

*Ví dụ*: họ viết "mở đầu bằng toàn cảnh khu du lịch". Luật hook nói toàn cảnh rộng yếu ở 3 giây đầu. → Nhánh **trao đổi tiếp**: phản biện, đề xuất cảnh khác. Nhánh **làm luôn**: mở bằng cảnh mạnh theo luật, đưa toàn cảnh vào giây thứ 4 — làm luôn, không hỏi.

### Nhưng vẫn DỪNG-BÁO ở 4 tình huống — đây KHÔNG phải phản biện
<!-- tags: chung -->

Phân biệt rõ: **phản biện** = góp ý về hướng làm *(đã bỏ ở nhánh này)*. **Dừng-báo** = không làm được, buộc phải hỏi:

1. **Thiếu tư liệu** — không đủ cảnh sạch cho số video yêu cầu. Hỏi có được xào lại cảnh không. **Cấm tự xoay.**
2. **Yêu cầu đích danh bị chặn** — giọng/nhạc/clip họ chỉ tên mà lỗi. Luật gốc của Sếp từ đầu.
3. **Nguyên liệu mâu thuẫn lựa chọn** — chọn MC dẫn nhưng không clip nào có người nói mạch lạc.
4. **Tốn tiền ngoài mức đã biết.**

### Giao hàng thì tóm tắt đã quyết gì
<!-- tags: chung -->

Không phải xin phép, chỉ là báo cáo: hook chọn góc nào, cảnh nào bị loại và vì sao, chỗ nào làm khác mô tả của họ. Để họ soi nhanh chứ không phải xem lại từ đầu.

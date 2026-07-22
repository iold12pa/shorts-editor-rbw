# Chọn kiểu dựng + kiểm tra đủ nguyên liệu — hỏi ngay khi skill được gọi

File này tách riêng để **dễ cập nhật realtime**: thêm/sửa 1 câu hỏi hay 1 điều kiện thì sửa đúng dòng trong bảng bên dưới, không cần đụng SKILL.md hay file style.

> 🔴 **ĐỌC TRƯỚC KHI HỎI BẤT CỨ CÂU NÀO — luật Sếp Huy chốt 22/07/2026.**
>
> Mọi câu hỏi trong file này là **NỘI DUNG** cần hỏi, không phải **cách trình bày**. Cách trình bày bắt buộc:
>
> 1. **Dùng thẻ chọn bấm được** (`AskUserQuestion` hoặc tương đương) — mỗi câu một thẻ, mỗi lựa chọn có nhãn ngắn + một dòng nói rõ chọn nó thì được gì. **CẤM dán khối chữ "1... 2... 3..." rồi chờ người dùng gõ số.** Nguyên văn Sếp: *"các dạng câu hỏi không được lần lượt hiện lên trực quan sinh động để chọn mà gộp lại như thế này"*.
> 2. **Gộp vào một lượt** — tối đa 4 câu, mỗi câu tối đa 4 lựa chọn. Đừng hỏi nhỏ giọt từng câu.
> 3. **PHÂN TÍCH FOOTAGE TRƯỚC RỒI MỚI HỎI.** Thứ gì máy tự biết được thì **tuyệt đối không hỏi**: bối cảnh buổi quay, robot dòng nào, địa điểm, trong clip có ai đang nói — Whisper nghe được lời, mắt AI nhận ra robot và nơi chốn, ảnh lưới cho thấy khung hình. Chạy phân tích (miễn phí, chạy nền) rồi hãy hỏi. Chỉ hỏi thứ **không nằm trong file**: kênh đăng · loại nhạc · số lượng video · ý tưởng riêng nếu có.
>
> Vì vậy thứ tự đúng là: **nhận folder → chạy phân tích nền → hỏi 1 lượt bằng thẻ chọn (những gì còn thiếu) → dựng.** KHÔNG phải hỏi hết rồi mới phân tích.

---

## 🔀 LUỒNG HỎI PHÂN NHÁNH — Sếp Huy thiết kế lại 22/07/2026 (ĐÂY LÀ LUỒNG CHÍNH THỨC)

Hỏi **theo nhánh**, không dồn hết mọi câu cho mọi người. Chọn kiểu dựng xong mới biết cần hỏi tiếp gì.

### BƯỚC 1 — ngay khi nhận source, hỏi 1 thẻ duy nhất

> **"Bạn muốn dựng theo hướng nào?"**

| Lựa chọn | Là kiểu | Đi tiếp nhánh |
|---|---|---|
| **Text + nhạc** | Kiểu 1 | Nhánh A |
| **Voice-over (giọng đọc)** | Kiểu 3 | Nhánh B |
| **Edit theo MC dẫn** | Kiểu 2 | Nhánh C |

### NHÁNH A — Text + nhạc

1. **Số lượng video**
2. **Chọn nhạc** (trend / không bản quyền / ElevenLabs đo ni / giữ tiếng gốc)
3. **Câu mở** (xem khối "Câu mở" bên dưới)

### NHÁNH B — Voice-over

1. **Giọng ở đâu ra** — 2 lựa chọn:
   - *Tôi đã có file giọng đọc sẵn* → người dùng gửi file, skill tự tìm file voice trong folder họ đưa
   - *Dùng giọng AI* → **hiện tiếp thẻ chọn giọng** (4 giọng, chính trước phụ sau — xem khối "Chọn giọng đọc")
2. **Số lượng video**
3. **Chọn nhạc**
4. **Mức phủ của giọng so với nhạc** — 3 lựa chọn:
   - *Giọng dẫn ở đầu, phần còn lại để nhạc chạy*
   - *Nhạc chạy cả bài, giọng phủ lên trên*
   - *Voice-over phủ full, nhạc chỉ làm nền nhỏ*
   ⚠️ Chọn "nhạc cả bài" hoặc "voice full" mà nhạc lại là **nhạc trend có giọng hát** → **báo ngay**: hai giọng sẽ chồng nhau. 14/16 bài trong `Nhạc hot` có giọng hát.
5. **Câu mở**

### NHÁNH C — Edit theo MC dẫn

1. **Chọn nhạc — bản quyền hay không bản quyền**
2. **Số lượng video**
3. **Câu mở** — nhánh này nhấn mạnh hỏi **buổi quay diễn ra ở đâu, có gì**, vì lời MC đã có sẵn trong clip nên thứ cần nhất là bối cảnh để chọn đúng đoạn.

### 🔴 CÂU MỞ PHẢI LÀ MỘT LƯỢT RIÊNG — DỪNG LẠI CHỜ HỌ GÕ

**Sếp Huy bắt lỗi 22/07/2026**: *"sao mô tả không có thời gian để họ nhập vậy"* — vì skill hiện câu mở xong là **gọi thẻ bấm tiếp theo ngay trong cùng một lượt**, người dùng chưa kịp gõ chữ nào đã sang câu khác. Câu mở thành ra chỉ để trang trí.

**Nguyên nhân kỹ thuật**: thẻ bấm và ô gõ tự do **không hiện cùng lúc được**. Đang hiện thẻ thì người dùng chỉ bấm được, không gõ được.

**Luật cứng:**
1. Hiện câu mở xong → **KẾT THÚC LƯỢT NGAY**. Không gọi thêm thẻ nào nữa.
2. **Chờ người dùng gõ xong** rồi mới hỏi thẻ cuối.
3. Họ trả lời trống / bảo "bỏ qua" → vẫn đi tiếp, nhưng nói rõ: *"không có mô tả thêm nên tôi bám theo những gì đọc được trong clip"*.
4. 🔴 **Mô tả gõ ra KHÔNG ĐỌC ĐƯỢC NGHĨA** (chuỗi ký tự bừa như `fefwefkw`, dán nhầm, trượt phím) → **HỎI LẠI, TUYỆT ĐỐI KHÔNG TỰ DIỄN GIẢI.** Đưa 2 lựa chọn: *bỏ qua, bám theo clip* / *để tôi gõ lại*.

   *Vì sao nghiêm trọng*: câu mở là thứ định hướng cả video. Bịa ra thông điệp từ một chuỗi vô nghĩa thì **sai từ gốc** — mọi cảnh, mọi chữ, mọi lời đọc đều đi lệch, và người duyệt phải xem xong mới phát hiện. Thà hỏi lại 5 giây. *(Ca thật 22/07/2026: Sếp gõ `fefwefkw` khi chạy thử luồng.)*

**Thứ tự đúng của cả luồng:**
```
[lượt 1]  thẻ chọn hướng dựng
[lượt 2]  các thẻ của nhánh (số lượng · nhạc · giọng...)
[lượt 3]  CÂU MỞ  →  DỪNG, chờ gõ          ← chỗ hay làm sai
[lượt 4]  thẻ cuối: làm luôn hay trao đổi tiếp
```

### BƯỚC CUỐI — áp cho CẢ BA nhánh

Sau khi người dùng **đã gõ xong câu mở**, hỏi thêm 1 thẻ:

> **"Bạn muốn tôi làm luôn, hay sau khi tôi đọc xong source thì hai bên tiếp tục trao đổi?"**

| Lựa chọn | Luồng chạy |
|---|---|
| **Làm luôn** | Chạy thẳng tới thành phẩm. Vẫn dừng-báo ở 4 tình huống bắt buộc (xem khối "Mức tự chủ") |
| **Đọc source xong rồi trao đổi tiếp** | Đọc hiểu source → **dựa vào chính source + những gì họ vừa trả lời** để hỏi tiếp cho rõ → rồi mới dựng |

**Nhánh "trao đổi tiếp" phải hỏi có căn cứ**, không hỏi chung chung: nêu số liệu thật đọc được rồi hỏi đúng chỗ còn mơ hồ. Vd: *"Có 14 clip nghe thấy tiếng, nhưng chỉ 5 câu đủ sạch — Sếp muốn tôi dùng cả 5 hay bỏ 2 câu bị lẫn tiếng ồn?"*

---

## ⏰ HỎI CÁI GÌ LÚC NÀO — chia 2 nhóm (Sếp Huy chốt 22/07/2026)

Sếp bắt lỗi thật: thẻ mức tự chủ từng ghi *"sau khi tôi đọc và hiểu rõ video..."* trong khi lúc hỏi **mới nhận folder, chưa đọc gì cả** — hứa hão. Truy ra nguyên nhân gốc: **chưa phân loại câu hỏi theo việc nó CÓ CẦN HIỂU NỘI DUNG hay không.**

### NHÓM 1 — hỏi NGAY khi tiếp nhận folder (không cần hiểu nội dung)

Hỏi ngay trong lúc phân tích chạy nền, để người dùng vừa trả lời vừa chờ, không phí thời gian.

| Câu | Vì sao hỏi được ngay |
|---|---|
| **Mức tự chủ** — tự sản xuất luôn / xác nhận cùng tôi | Đây là cách họ muốn làm việc, chẳng liên quan clip có gì |
| **Kênh đăng** — page công ty / cá nhân / cả hai | Quyết định logo + outro, không phụ thuộc nội dung |
| **Câu mở** — mô tả buổi quay + đầu ra mong muốn | Chính họ là người biết, máy không đọc ra được |

⚠️ Câu chữ phải khớp thời điểm: viết **"sau khi tiếp nhận video"**, KHÔNG viết "sau khi tôi đọc hiểu video" — lúc đó chưa đọc.

### NHÓM 2 — chỉ hỏi SAU khi phân tích xong (cần hiểu nội dung mới khuyên đúng)

| Câu | Cần biết gì từ footage trước khi hỏi |
|---|---|
| **Kiểu dựng** | Có bao nhiêu clip thật sự có người nói → mới biết Kiểu 2 khả thi không |
| **Số video** | Bao nhiêu cảnh sạch, khác nhau → mới biết làm được mấy video mà không lặp cảnh |
| **Nhạc** | Nhịp cảnh, có tiếng hiện trường đáng giữ không |
| **Mức phủ giọng** *(Kiểu 2/3)* | Lượng thoại thật có trong clip |
| **Giọng đọc** *(Kiểu 3)* | Nội dung nghiêng chất nào → mới gợi ý được giọng hợp |

**Kèm số liệu thật vào từng lựa chọn** để người dùng chọn có căn cứ — vd *"Kiểu 2: máy đếm được 14 clip có tiếng nói nên làm được"*, *"3 video: 31 clip sạch, đủ cảnh riêng cho từng video, không phải lặp"*. Đó chính là giá trị của việc phân tích trước khi hỏi.

## Bước A — Hỏi kiểu dựng (bỏ qua nếu người dùng đã nói rõ ngay từ tin đầu)

Hỏi bằng lời dễ hiểu, không dùng thuật ngữ kỹ thuật:

> "Bạn muốn tôi dựng video theo hướng nào?
> **1) Video/clip đã có sẵn** — tôi tự chọn đoạn hay, chèn chữ, ghép nhạc (không cần lời thoại)
> **2) Video đã có người nói sẵn trong đó rồi** — tôi dựng theo đúng lời đó
> **3) Ghép nhiều đoạn video lại, rồi thêm lời thuyết minh mới**"

## Bước B — Checklist theo từng kiểu (chỉ hỏi phần CÒN THIẾU, không hỏi lại cái đã có)

### Kiểu 1 — Highlight + chữ + nhạc (không thoại)
| Cần | Mức độ | Nếu thiếu → hỏi |
|---|---|---|
| Source video/folder | **Bắt buộc** | "Cho tôi xin folder hoặc link video nguồn nhé" |
| Mô tả buổi quay (địa điểm, robot, sự kiện hôm đó) | Nên có | "Buổi quay này ở đâu, quay robot gì, hôm đó có nội dung/sự kiện gì đặc biệt không?" |
| Chữ đè: tự viết hay để Claude viết | Cần biết | "Bạn muốn tự viết sẵn câu chữ đè lên video, hay để tôi xem nội dung rồi tự viết?" |
| **LOẠI NHẠC: trend hay không bản quyền** | **Bắt buộc hỏi — luật Sếp Huy 20/07/2026** | Xem khối ngay bên dưới |
| Nhạc nền: bài cụ thể hay để chọn | Cần biết | "Có bài nhạc cụ thể muốn dùng không, hay để tôi chọn phù hợp?" |
| Style cụ thể | Xem `references/style-mau.md` |

**Câu hỏi BẮT BUỘC của Kiểu 1 — loại nhạc** (Kiểu 1 thì LUÔN hỏi câu này; Kiểu 2/3 chỉ hỏi khi rơi vào **Nhóm B** — xem "Luật nhạc theo mức phủ giọng" bên dưới. Sửa 21/07: chỗ này từng ghi "chỉ Kiểu 1 mới hỏi", nay không còn đúng):

> "Video này bạn muốn dùng **nhạc trend** (nhạc hot TikTok — bắt tai, dễ lên tương tác, **nhưng chỉ nên đăng Facebook page**, đăng YouTube khả năng cao dính bản quyền/bị tắt tiếng), hay **nhạc không bản quyền** (đăng được mọi nền tảng kể cả YouTube, an toàn tuyệt đối)?"

**Bốn lựa chọn nhạc** (Sếp Huy thêm mục 4 ngày 22/07/2026):

| Lựa chọn | Lấy từ đâu | Lưu ý |
|---|---|---|
| **Nhạc không bản quyền** | `Kho nhạc free YT/` các folder ngoài `Nhạc hot` (`Chill nhẹ + vui vẻ`, `POP tươi sáng`...) | Đăng được mọi nền tảng kể cả YouTube |
| **Nhạc trend** | `Kho nhạc free YT/Nhạc hot/` — cách dùng ở `style-mau.md` mục "Kho nhạc trend" | **Chỉ nên đăng Facebook**; YouTube khả năng cao dính bản quyền |
| **Giữ tiếng gốc trong clip** | không dùng nhạc | Hợp khi cảnh có tiếng khách nói, tiếng robot chạy |
| **Nhạc ElevenLabs (đo ni theo video)** | `scripts/elevenlabs_music.py` — sinh bài **không lời**, dài đúng bằng video | Xem khối bên dưới trước khi chọn |

**Nhạc ElevenLabs — đọc trước khi mời người dùng chọn:**

- Sinh nhạc **theo mô tả bằng tiếng Anh, càng cụ thể càng hợp** (vd `upbeat corporate tech, light percussion, optimistic`), **dài đúng bằng video** nên không phải cắt/fade ép.
- **Tốn tiền**: ~900 credits mỗi phút nhạc. **Sinh 1 lần cho bản duyệt cuối**, đừng sinh thử nhiều bản.
- 🔴 **Trạng thái 22/07/2026: CHƯA DÙNG ĐƯỢC — key thiếu quyền.** Đo thật, ElevenLabs trả `missing the permission music_generation`. **Đây KHÔNG phải thiếu gói** (ghi chú cũ đoán sai là "cần nâng gói", suýt khiến đi mua oan). Cách mở, ~1 phút: **elevenlabs.io → API Keys → sửa key → bật quyền `Music`** → key mới thì nhập lại bằng `chuan_bi_may.py --nhap-key`.
- Chừng nào chưa bật quyền: người dùng chọn mục này thì **BÁO đúng 3 bước trên rồi chờ họ quyết** — không tự đổi sang kho nhạc khác.
- Kho nhạc riêng của Sếp trên Drive **vẫn là mặc định**. Nhạc ElevenLabs dùng khi người dùng chủ động chọn, hoặc kho không có bài hợp và họ đồng ý.

- Người dùng chỉ định đích danh 1 bài → dùng đúng bài đó, không hỏi lại loại nhạc.
- Đã hỏi rồi thì **không nhắc lại rủi ro bản quyền lần 2** trong cùng video (luật cũ: nhắc đúng 1 câu tại điểm duyệt kịch bản).

### Thẻ BẮT BUỘC cuối cùng — người dùng chọn MỨC TỰ CHỦ (Sếp Huy chốt 22/07/2026)

Hỏi sau khi đã hỏi xong các thẻ kỹ thuật. **Thẻ này quyết định có điểm dừng duyệt kịch bản hay không** — nên hỏi rõ, đừng tự quyết thay.

| Lựa chọn | Nghĩa | Luồng chạy |
|---|---|---|
| **Tôi tự sản xuất luôn** | Tự viết kịch bản dựa trên nội dung clip + kiến thức về Roboworld, dựng ra video hoàn chỉnh, giao thành phẩm | **BỎ điểm dừng duyệt kịch bản.** Chạy thẳng: phân tích → viết kịch bản → dựng → giao video + caption |
| **Xác nhận nội dung cùng tôi** | Sau khi đọc hiểu video, trình kịch bản để người dùng duyệt/sửa rồi mới dựng | **GIỮ điểm dừng duyệt kịch bản** theo mẫu bảng biểu trong `kichban-template.md`. Tiếp tục tương tác cho tới khi họ ưng |

**Chọn "tự sản xuất luôn" KHÔNG có nghĩa im lặng làm bằng mọi giá.** Bốn tình huống vẫn PHẢI dừng và báo, kể cả khi họ đã cho tự chạy:

1. **Thiếu tư liệu** — không đủ cảnh sạch cho số video yêu cầu (luật đếm tư liệu, `quy-trinh-chon-canh.md`). Báo rõ thiếu gì, hỏi có được xào lại cảnh không. **Cấm tự xoay.**
2. **Yêu cầu đích danh bị chặn** — giọng/nhạc/clip họ chỉ tên mà lỗi. Dừng báo, không tự thay.
3. **Nguyên liệu mâu thuẫn lựa chọn** — vd chọn Kiểu 2 nhưng không clip nào có người nói; chọn nhạc trend nhưng giọng dẫn xuyên suốt (nhạc có lời sẽ đè lên).
4. **Tốn tiền ngoài mức đã biết** — vd phải sinh nhạc ElevenLabs, quét thêm nhiều clip.

Giao hàng xong vẫn **tóm tắt lại đã quyết những gì thay họ** (hook chọn góc nào, cảnh nào bị loại và vì sao) — để họ soi nhanh chứ không phải xem lại từ đầu.

### Câu BẮT BUỘC cuối cùng — mô tả buổi quay + đầu ra mong muốn (Sếp Huy chốt 22/07/2026)

Sau khi hỏi xong các thẻ chọn, **luôn hỏi thêm một câu mở** (câu này không bấm được, phải để người dùng tự gõ):

> **"Bạn muốn triển khai video này theo hướng nào? Mô tả giúp tôi càng cụ thể càng tốt."**
>
> Gợi ý cho người dùng biết nên đưa gì vào (in kèm câu hỏi):
> - **Buổi quay hôm đó diễn ra thế nào** — ở đâu, khách nào, robot nào, có gì đáng chú ý
> - **Thứ tự xuất hiện của các cảnh** — muốn mở đầu bằng cảnh gì, kết bằng cảnh gì
> - **Thông điệp muốn truyền** — bán hàng · khoe năng lực triển khai · kể chuyện khách hàng · thông báo sự kiện
> - **Ràng buộc** — cảnh bắt buộc phải có, cảnh phải tránh, tên riêng đọc đúng, độ dài mong muốn

**Đây là thông tin quan trọng nhất trong cả bước hỏi.** Mọi thẻ chọn phía trên chỉ quyết định khung kỹ thuật; câu này mới cho biết **video phải nói lên điều gì**. Nguyên văn Sếp: *"cái này là thông tin mà bạn phải xử lý để đầu ra giống họ mong muốn nhất"*.

**Xử lý câu trả lời thế nào — không đọc lướt rồi bỏ đó:**

1. **Bóc ra 3 nhóm tin** và ghi lại rõ ràng:
   - **Bối cảnh**: sự kiện gì, khách hàng nào, robot nào, diễn ra ở đâu — dùng để viết hook và chữ đè cho đúng, không bịa.
   - **Thông điệp muốn truyền**: bán hàng · khoe năng lực triển khai · kể chuyện khách hàng · tuyển dụng · thông báo sự kiện. Cái này quyết định giọng văn kịch bản.
   - **Ràng buộc cụ thể**: cảnh nào bắt buộc phải có, cảnh nào cấm dùng, tên riêng phải đọc đúng, độ dài mong muốn, hạn nộp.
2. **Đối chiếu với những gì máy đọc được từ footage.** Người dùng nói có cảnh A mà phân tích không thấy → **hỏi lại ngay**, đừng tự dựng thiếu rồi báo sau.
3. **Phản chiếu lại trong kịch bản trình duyệt**: ghi rõ câu nào/cảnh nào đáp ứng ý nào họ nêu. Người duyệt thấy ý mình được hiểu đúng thì duyệt nhanh, và sai ở đâu cũng chỉ ra được ngay.
4. **Người dùng bỏ trống câu này** → vẫn làm được, nhưng phải nói rõ: *"Sếp không mô tả thêm nên tôi bám theo những gì đọc được trong clip"* — để họ biết mà bổ sung nếu lệch.

### Kiểu 2 — Dựng theo lời thoại có sẵn (voice gốc, đồng bộ lúc quay)
| Cần | Mức độ | Nếu thiếu → hỏi |
|---|---|---|
| Source video có thoại | **Bắt buộc** | "Cho tôi xin video/folder nguồn — trong đó đã có người nói sẵn đúng không?" |
| Xác nhận THẬT SỰ có thoại (không đoán) | **Bắt buộc trước khi viết kịch bản** | Sau khi chạy `analyze_footage.py`, nếu phần lớn clip `has_speech=false` → báo lại: "Tôi nghe thử thì video này không có lời rõ, bạn xác nhận lại giúp, hay muốn chuyển sang Kiểu 1?" — KHÔNG tự chuyển kiểu, phải hỏi. |
| Bối cảnh (để hiểu đúng ý câu nói, tránh cắt sai/lệch khẩu hình) | Nên có | "Buổi quay này về chuyện gì, để tôi hiểu đúng ngữ cảnh lời thoại?" |
| **MỨC PHỦ GIỌNG → quyết định loại nhạc** | **Bắt buộc hỏi** | "Giọng nói phủ cả bài, hay chỉ 1-2 câu mở đầu?" — xem khối "Luật nhạc theo mức phủ giọng" dưới bảng Kiểu 3 |
| **XỬ LÝ TIẾNG NÓI (4 lựa chọn)** | **Bắt buộc hỏi** — MC dẫn trực tiếp luôn áp | Xem khối "Xử lý tiếng nói" dưới bảng Kiểu 3 |
| Style cụ thể | Xem `references/gu-kieu-2-3.md` (chọn công thức con 2A/2B/2C theo dạng source) + mục "Quy tắc VOICE GỐC MC" trong `references/style-voice-karaoke.md` |

### Kiểu 3 — Ghép cảnh + thêm voice-over mới (không đồng bộ lúc quay)
| Cần | Mức độ | Nếu thiếu → hỏi |
|---|---|---|
| Source video/clip để ghép | **Bắt buộc** | "Cho tôi xin các video/clip muốn ghép lại" |
| Voice-over: đã có file sẵn hay chưa | **Bắt buộc phải hỏi rõ, đây là lỗi hay gặp nhất** | "Bạn đã có sẵn file giọng đọc chưa? Nếu chưa, tôi viết kịch bản cho bạn duyệt trước, rồi tạo giọng đọc (AI hoặc bạn tự thu đều được)" |
| Nếu ĐÃ có voice-over: khớp với video nào | **Bắt buộc** | "File giọng đọc này đi cùng (những) video nào? Có sẵn lời thoại/kịch bản để tôi khớp cảnh theo không?" |
| Nếu CHƯA có voice-over: **CHỌN GIỌNG** | **Bắt buộc hỏi** — xem khối "Chọn giọng đọc" ngay dưới bảng này | Người dùng chọn giọng AI thì hiện tiếp thẻ chọn giọng cụ thể |
| Bối cảnh | Nên có | như Kiểu 1/2 |
| **MỨC PHỦ GIỌNG → quyết định loại nhạc** | **Bắt buộc hỏi** | "Giọng đọc phủ cả bài, hay chỉ 1-2 câu mở đầu?" — xem khối ngay dưới bảng này |
| **XỬ LÝ TIẾNG NÓI (4 lựa chọn)** | Hỏi **CHỈ KHI** giọng đọc do **người thu**. Giọng AI thì **BỎ QUA, không hỏi** | Xem khối "Xử lý tiếng nói" dưới khối luật nhạc |
| Style cụ thể | Xem `references/gu-kieu-2-3.md` (chọn công thức 3A showcase / 3B case study 9 nhịp) + `references/style-voice-karaoke.md` (karaoke sub) hoặc `references/style-ads-huy.md` (nếu dạng quảng cáo bán hàng) |

### Chọn giọng đọc — hỏi khi Kiểu 3 chưa có sẵn file voice-over (Sếp Huy chốt 22/07/2026)

**Hỏi 2 tầng, tầng sau chỉ hiện khi tầng trước chọn giọng AI.**

**Tầng 1 — giọng ở đâu ra:**

| Lựa chọn | Nghĩa |
|---|---|
| **Giọng AI (ElevenLabs)** | Tôi tạo giọng đọc — hiện tiếp tầng 2 |
| **Tôi tự thu** | Người dùng gửi file giọng, bỏ qua tầng 2 (nhớ hỏi tiếp khối "Xử lý tiếng nói") |

**Tầng 2 — chọn giọng cụ thể (CHỈ hiện khi tầng 1 chọn giọng AI). SÁU lựa chọn, Sếp Huy chốt 22/07/2026:**

**Luôn hiện đủ cả 4 cho người dùng chọn** (Sếp Huy 22/07/2026: *"cứ hiện cả 4 lên cho họ chọn"*). Thứ tự dưới đây là thứ tự hiện — **giọng chính lên trước**.

| # | Lựa chọn | Vai trò | Mã giọng | Hợp với nội dung nào |
|---|---|---|---|---|
| 1 | **MC Xuân Tú** — nam, giọng Bắc, chất MC | **CHÍNH** | `7XOKiK112QRZRSLbCfMc` | Dẫn chuyên nghiệp, phóng sự, sự kiện, video cho page công ty |
| 2 | **Thanh Ngọc** — nữ, giọng Nam, ấm & đáng tin | **CHÍNH** | `Na15FlRRkMEDtEW4nVVP` | Tư vấn, chăm sóc khách hàng, nội dung gần gũi miền Nam |
| 3 | **Phương Uyên** — nữ, giọng **nhân bản của chính Roboworld** | phụ | `Y9oZ1fkOxoaT3zFqTPzg` | Giới thiệu sản phẩm, kể chuyện khách hàng, nội dung mềm mại thân thiện |
| 4 | **Adam** — nam, chắc và mạnh | phụ | `pNInz6obpgDQGcFmaJgB` | Dứt khoát: hiệu quả, số liệu, kêu gọi hành động. **Gốc là giọng tiếng Anh** |
| — | **Tuỳ theo nội dung** | — | tự chọn | **Đọc kịch bản rồi tự chọn giọng hợp nhất**, nói rõ đã chọn giọng nào và vì sao |

**CHÍNH / phụ nghĩa là gì** (Sếp Huy chốt 22/07/2026):
- **Giọng chính = MC Xuân Tú và Thanh Ngọc.** Đây là 2 giọng mặc định của Roboworld. Chọn "tuỳ theo nội dung" thì **ưu tiên 2 giọng này**; giọng mặc định khi người dùng không nói gì cũng lấy trong 2 giọng này.
- **Giọng phụ = Phương Uyên và Adam.** Vẫn hiện đủ trong thẻ chọn để người dùng tự chọn, nhưng **không tự lấy làm mặc định** — chỉ dùng khi người dùng chỉ định đích danh, hoặc khi nội dung hợp rõ rệt (và khi đó phải nói rõ lý do chọn).
- ⚠️ **Adam** xếp nhóm phụ vì Sếp mới nói rõ vai trò cho Phương Uyên; Adam là **giọng gốc tiếng Anh** nên tôi để cùng nhóm phụ cho an toàn. Sếp muốn nâng Adam lên giọng chính thì báo một câu là đổi.

> 🔴 **ĐÃ BỎ 22/07/2026 — hai giọng miễn phí edge-tts** (`vi-VN-NamMinhNeural` nam, `vi-VN-HoaiMyNeural` nữ). **Sếp Huy nghe mẫu và kết luận: đọc méo, không dùng được.** Đừng đưa lại vào bảng chọn, đừng dùng làm phương án thay thế khi ElevenLabs lỗi.
>
> **Đây là ca đáng nhớ nhất về giới hạn của phép đo bằng máy**: cho Whisper nghe lại, 2 giọng này trả về **đúng nguyên câu, chuẩn 100% từng chữ** — ngang điểm với 4 giọng ElevenLabs. Máy chấm "đạt". Tai Sếp nghe ra méo ngay. **Whisper đo được RÕ CHỮ, không đo được NGHE CÓ THẬT KHÔNG.** Lần sau đừng lấy "Whisper nghe ra đúng" làm bằng chứng một giọng dùng được.

> **Lựa chọn "tuỳ nội dung" làm thế nào** — **ưu tiên 2 giọng CHÍNH trước**: dẫn chuyên nghiệp, phóng sự, sự kiện, video page công ty → **MC Xuân Tú**; tư vấn, chăm sóc khách, nội dung gần gũi (nhất là khách miền Nam) → **Thanh Ngọc**. Chỉ chọn giọng **phụ** khi nội dung hợp rõ rệt: kể chuyện khách hàng mềm mại, muốn chất giọng riêng của Roboworld → **Phương Uyên**; lời tiếng Anh, hoặc cần chất nam dứt khoát mạnh → **Adam**. Nội dung dài có nhiều chất thì chọn theo **đoạn mở đầu**, vì đó là chỗ giữ người xem. Chọn xong **báo 1 câu kèm lý do**, đừng chọn thầm.

**Bốn giọng vừa khít một thẻ hỏi** (công cụ hỏi cho tối đa 4 lựa chọn) — hiện thẳng cả 4, không cần chia bước. Người dùng muốn "tuỳ nội dung" thì gõ vào ô tự nhập.

⚠️ **Không còn phương án miễn phí thay thế.** Trước đây ElevenLabs lỗi thì tự lui về edge-tts; nay edge-tts đã bị loại vì đọc méo, nên **gặp lỗi ElevenLabs là DỪNG và BÁO người dùng**, chờ quyết — đúng luật gốc của Sếp: *yêu cầu đích danh mà bị chặn thì dừng báo, không tự thay bằng thứ khác*.

⚠️ **Mốc tốc độ `+41%` KHÔNG áp cho 4 giọng này.** Con số đó đo trên edge-tts (đã bỏ). ElevenLabs chỉnh tốc độ bằng đường khác (`voice_settings.speed`), **chưa đo mốc chuẩn** — cần đo lại khi nào cần tăng/giảm tốc độ giọng đọc. Đừng chép `+41%` sang đây.

**Ba điều đã đo thật 22/07/2026, đừng làm sai:**

1. **Model đọc bắt buộc là `eleven_turbo_v2_5`** (đã đặt sẵn trong `elevenlabs_tts.py`). **Tuyệt đối không lui về `eleven_multilingual_v2`** — đo thật: cùng một giọng, model cũ đọc *"phục vụ tới nhà hàng của bạn"* thành *"phúc vật hoàn hà hàn kòa bàn"*, model mới đọc chuẩn từng chữ.
2. **Luật cũ "George méo vì là giọng Anh" đã được đính chính** — thủ phạm là model chứ không phải giọng. Với `turbo_v2_5`, Adam (giọng gốc Anh) đọc tiếng Việt **chuẩn 100%** qua phép nghe lại bằng Whisper.
3. **Cả 4 giọng ElevenLabs đều HẾT bị chặn** — ghi chú cũ "gói Free chặn 402, chờ nâng Starter $6" không còn đúng, đã đo lại. Giờ 2 giọng miễn phí là **lựa chọn có chủ đích** (tiết kiệm / bản nháp), không còn là phương án chữa cháy. Nếu vẫn gặp lỗi 402 thì **DỪNG BÁO người dùng**, không tự đổi giọng khác.

**Đo thật 22/07/2026 — cả 6 giọng đọc CHUẨN 100% từng chữ** (cho Whisper nghe lại câu *"Một robot BellaBot phục vụ bằng ba nhân viên chạy bàn, làm việc mười hai tiếng không nghỉ. Nhà hàng của bạn đã sẵn sàng chưa?"*, cả 6 đều trả về đúng nguyên câu). Nghĩa là **không giọng nào bị loại vì đọc sai** — khác biệt còn lại hoàn toàn nằm ở **chất giọng**.

⚠️ **Whisper chỉ đo RÕ CHỮ, không đo giọng nghe có tự nhiên không.** Giọng gốc Anh đọc tiếng Việt vẫn có thể nghe ra chất Tây dù từng chữ đều rõ; giọng miễn phí có thể nghe "máy" hơn dù đọc đúng. Chọn giọng cho video thật vẫn phải qua **tai người** — mẫu 6 giọng đã xuất sẵn tại `Desktop\NGHE-CHON-GIONG`.

### Luật nhạc theo mức phủ giọng — áp cho Kiểu 2 và Kiểu 3 (Sếp Huy chốt 21/07/2026)

**Câu hỏi BẮT BUỘC, hỏi ngay sau khi người dùng chọn Kiểu 2 hoặc Kiểu 3:**

> "Video này giọng nói phủ tới đâu — **dẫn xuyên suốt cả bài**, hay **chỉ 1-2 câu mở đầu** rồi phần sau để cảnh robot chạy với nhạc?"

Trả lời xong mới chọn nhạc. Hai nhóm, luật khác hẳn nhau:

**NHÓM A — giọng dẫn xuyên suốt** (MC nói cả bài, hoặc voice-over phủ phần lớn thời lượng)
- Nhạc nền **TUYỆT ĐỐI KHÔNG LỜI**.
- Áp cho **CẢ video**, kể cả đoạn cuối không còn ai nói. Ví dụ công thức 2A dạng hành trình thoại chỉ phủ ~45%, nửa sau chỉ còn hình + nhạc — nửa sau đó **vẫn phải không lời**, vì đổi nhạc giữa chừng nghe gãy (Sếp chốt phương án A ngày 21/07).
- **KHÔNG hỏi câu "trend hay không bản quyền"**, và **cấm dùng folder `Nhạc hot`** (nhạc trend gần như luôn có lời).

**NHÓM B — giọng chỉ mở màn 1-2 câu rồi im hẳn**, phần sau để cảnh robot + nhạc tự kể
- **ĐƯỢC dùng nhạc có lời, kể cả nhạc hot.**
- **PHẢI hỏi "trend hay không bản quyền"** giống hệt Kiểu 1 (dùng đúng câu hỏi ở mục Kiểu 1 bên trên) — vì nhạc hot chỉ đăng được Facebook page.
- Nhạc **nhỏ trong lúc đang nói (0.15-0.2)**, nói xong **dâng dần lên to đến hết bài (~0.55)**. Đây là một bài duy nhất chạy suốt, chỉ đổi âm lượng — **không phải đổi bài**. Công thức ffmpeg: `references/ffmpeg-recipes.md` mục 5b.

**Lý do luật gốc**: hai giọng chồng lên nhau bắt tai người nghe chia sự chú ý, lời dẫn bị nuốt — hạ volume nhạc **không cứu được**, vì vấn đề là có 2 giọng chứ không phải nhạc to. Nhóm B thoát luật vì sau 1-2 câu đầu không còn giọng nào để chồng lên nữa.

**Chung cho cả 2 nhóm:**
- Không chắc bài có giọng hát hay không → **NGHE KIỂM trước khi dùng**. Kể cả nhóm "nhạc không bản quyền" vẫn lẫn bài có lời (folder `POP tươi sáng`).
- Nhạc sinh bằng ElevenLabs Music đang khoá `force_instrumental=True` → luôn hợp Nhóm A; muốn nhạc có lời cho Nhóm B thì phải lấy từ kho.
- **Kiểu 1 không áp luật này** — vẫn dùng nhạc có lời bình thường.

### Xử lý tiếng nói — 4 lựa chọn (Sếp Huy chốt 21/07/2026)

**Áp cho**: MC dẫn trực tiếp (Kiểu 2) và voice-over do **người thu** (Kiểu 3).
**BỎ QUA hoàn toàn với voice-over giọng AI** — file TTS vốn đã sạch, xử lý thêm chỉ làm méo. Đừng hỏi câu này khi giọng do máy đọc.

**Câu hỏi, hỏi bằng lời đời thường:**

> "Tiếng người nói trong video, bạn muốn tôi xử lý thế nào?
> **1) Giữ nguyên** — an toàn nhất, tiếng thật như lúc quay
> **2) Lọc ồn** — bóc bớt tiếng nền (máy móc, xe cộ, người xung quanh)
> **3) Làm rõ giọng** — không đụng tiếng nền, chỉ làm giọng nghe rõ và đều hơn
> **4) Cả hai** — vừa lọc ồn vừa làm rõ giọng"

- **Không trả lời / nói "tùy" → chọn 1 (giữ nguyên).** Không xử lý thì không hỏng; xử lý sai thì hỏng.
- **Phân vân → cắt 4 bản thử 10 giây cho nghe chọn.** Bắt buộc cân bằng cả 4 về cùng độ to (`loudnorm=I=-16`) trước khi đưa nghe, không thì tai luôn chọn bản to nhất chứ không phải bản hay nhất.
- Công thức từng lựa chọn: `references/ffmpeg-recipes.md` **mục 5c**.

⛔ **Bộ lọc CHỈ chạy ở bước mix cuối, sau khi đã cắt xong.** Chạy trước bước đo mốc thoại sẽ phá hệ đo mà không báo lỗi (đo thật 21/07: độ ấm sai gấp 4-27 lần, bắt nhầm gấp 5 lần) — lý do chi tiết ở mục 5c.

⚠️ **Tiếng quá xa thì không cứu được**: đo thấy cách sàn nhiễu < 8 dB thì mọi bộ lọc đều vô ích (ca thật: nhà máy dập folder 33 chỉ **2.2 dB**). Lúc đó báo người dùng đổi cảnh khác, đừng hứa xử lý được.

## Bước C — Câu hỏi chung, mọi kiểu đều cần
- Robot xuất hiện là model nào → tra `references/robot-products.md` trước, chỉ hỏi lại nếu không chắc hoặc model chưa có trong danh mục
- Đã có ý tưởng nội dung cụ thể chưa, hay muốn Claude tự đề xuất từ footage
- **ĐĂNG Ở ĐÂU → quyết định có logo + outro hay không** (bắt buộc hỏi, xem khối ngay dưới)

### Video này đăng ở đâu — hỏi CUỐI CÙNG, trước khi dựng (Sếp Huy chốt 21/07/2026)

**Câu hỏi:**

> "Video này đăng ở **page chính của công ty**, hay ở **kênh cá nhân**?"

| | **Page công ty** | **Kênh cá nhân** |
|---|---|---|
| Logo trắng giữa-trên | ✅ có | ❌ **không** |
| Outro dọc cuối video | ✅ có | ❌ **không** |
| Phần hình còn lại | giống nhau | giống nhau |

**Kênh cá nhân thì để mộc — chỉ có video thôi, trông cho tự nhiên.** Gắn logo với outro vào là thành quảng cáo ngay, mất cái tự nhiên vốn là điểm mạnh của kênh cá nhân.

- Áp cho **cả 3 kiểu dựng**.
- Người dùng không trả lời → **mặc định page công ty** (có logo + outro), vì đó là phần lớn video.
- Hỏi rồi thì không hỏi lại trong cùng buổi dựng — trừ khi họ đổi ý.
- Chi tiết kỹ thuật khi bỏ 2 thứ này: `references/ffmpeg-recipes.md` mục 4d và 5.

## Nguyên tắc validate
- Thiếu mục **Bắt buộc** → hỏi ngay, KHÔNG viết kịch bản hay tự đoán/tự bịa để lấp chỗ trống
- Thiếu mục **Nên có** → vẫn làm được, nhưng khi trình kịch bản phải nói rõ chỗ nào đang tự suy đoán để người dùng sửa nếu sai
- Người dùng đã trả lời sẵn trong tin nhắn đầu tiên → chỉ hỏi tiếp PHẦN CÒN THIẾU, không hỏi lại từ đầu

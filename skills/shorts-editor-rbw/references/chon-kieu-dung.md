# Chọn kiểu dựng + kiểm tra đủ nguyên liệu — hỏi ngay khi skill được gọi

File này tách riêng để **dễ cập nhật realtime**: thêm/sửa 1 câu hỏi hay 1 điều kiện thì sửa đúng dòng trong bảng bên dưới, không cần đụng SKILL.md hay file style. Đây là bước ĐẦU TIÊN của mọi lần chạy skill, trước cả khi phân tích footage.

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

- Chọn **nhạc trend** → lấy từ `Kho nhạc free YT/Nhạc hot/` (xem cách dùng kho này ở `references/style-mau.md`, mục "Kho nhạc trend").
- Chọn **nhạc không bản quyền** → lấy từ các folder còn lại trong `Kho nhạc free YT/` (`Chill nhẹ + vui vẻ`, `POP tươi sáng`...).
- Người dùng chỉ định đích danh 1 bài → dùng đúng bài đó, không hỏi lại loại nhạc.
- Đã hỏi rồi thì **không nhắc lại rủi ro bản quyền lần 2** trong cùng video (luật cũ: nhắc đúng 1 câu tại điểm duyệt kịch bản).

### Kiểu 2 — Dựng theo lời thoại có sẵn (voice gốc, đồng bộ lúc quay)
| Cần | Mức độ | Nếu thiếu → hỏi |
|---|---|---|
| Source video có thoại | **Bắt buộc** | "Cho tôi xin video/folder nguồn — trong đó đã có người nói sẵn đúng không?" |
| Xác nhận THẬT SỰ có thoại (không đoán) | **Bắt buộc trước khi viết kịch bản** | Sau khi chạy `analyze_footage.py`, nếu phần lớn clip `has_speech=false` → báo lại: "Tôi nghe thử thì video này không có lời rõ, bạn xác nhận lại giúp, hay muốn chuyển sang Kiểu 1?" — KHÔNG tự chuyển kiểu, phải hỏi. |
| Bối cảnh (để hiểu đúng ý câu nói, tránh cắt sai/lệch khẩu hình) | Nên có | "Buổi quay này về chuyện gì, để tôi hiểu đúng ngữ cảnh lời thoại?" |
| **MỨC PHỦ GIỌNG → quyết định loại nhạc** | **Bắt buộc hỏi** | "Giọng nói phủ cả bài, hay chỉ 1-2 câu mở đầu?" — xem khối "Luật nhạc theo mức phủ giọng" dưới bảng Kiểu 3 |
| Style cụ thể | Xem `references/gu-kieu-2-3.md` (chọn công thức con 2A/2B/2C theo dạng source) + mục "Quy tắc VOICE GỐC MC" trong `references/style-voice-karaoke.md` |

### Kiểu 3 — Ghép cảnh + thêm voice-over mới (không đồng bộ lúc quay)
| Cần | Mức độ | Nếu thiếu → hỏi |
|---|---|---|
| Source video/clip để ghép | **Bắt buộc** | "Cho tôi xin các video/clip muốn ghép lại" |
| Voice-over: đã có file sẵn hay chưa | **Bắt buộc phải hỏi rõ, đây là lỗi hay gặp nhất** | "Bạn đã có sẵn file giọng đọc chưa? Nếu chưa, tôi viết kịch bản cho bạn duyệt trước, rồi tạo giọng đọc (AI hoặc bạn tự thu đều được)" |
| Nếu ĐÃ có voice-over: khớp với video nào | **Bắt buộc** | "File giọng đọc này đi cùng (những) video nào? Có sẵn lời thoại/kịch bản để tôi khớp cảnh theo không?" |
| Nếu CHƯA có voice-over: giọng nam hay nữ | Cần biết | "Bạn muốn giọng đọc nam hay nữ?" — mặc định giờ là **giọng VIỆT** (MC Xuân Tú nam / Thanh Ngọc nữ). Gói ElevenLabs còn Free thì 2 giọng này bị chặn 402 → tự lui về edge-tts giọng Việt. **Tuyệt đối không lui về George** — đó là giọng Anh, đọc tiếng Việt méo cả câu thường |
| Bối cảnh | Nên có | như Kiểu 1/2 |
| **MỨC PHỦ GIỌNG → quyết định loại nhạc** | **Bắt buộc hỏi** | "Giọng đọc phủ cả bài, hay chỉ 1-2 câu mở đầu?" — xem khối ngay dưới bảng này |
| Style cụ thể | Xem `references/gu-kieu-2-3.md` (chọn công thức 3A showcase / 3B case study 9 nhịp) + `references/style-voice-karaoke.md` (karaoke sub) hoặc `references/style-ads-huy.md` (nếu dạng quảng cáo bán hàng) |

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

## Bước C — Câu hỏi chung, mọi kiểu đều cần
- Robot xuất hiện là model nào → tra `references/robot-products.md` trước, chỉ hỏi lại nếu không chắc hoặc model chưa có trong danh mục
- Đã có ý tưởng nội dung cụ thể chưa, hay muốn Claude tự đề xuất từ footage

## Nguyên tắc validate
- Thiếu mục **Bắt buộc** → hỏi ngay, KHÔNG viết kịch bản hay tự đoán/tự bịa để lấp chỗ trống
- Thiếu mục **Nên có** → vẫn làm được, nhưng khi trình kịch bản phải nói rõ chỗ nào đang tự suy đoán để người dùng sửa nếu sai
- Người dùng đã trả lời sẵn trong tin nhắn đầu tiên → chỉ hỏi tiếp PHẦN CÒN THIẾU, không hỏi lại từ đầu

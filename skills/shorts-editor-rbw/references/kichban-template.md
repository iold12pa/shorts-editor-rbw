# Mẫu kịch bản shorts Roboworld — theo 3 KIỂU DỰNG

Mỗi ý tưởng video → 1 file `kichban/video-N-<slug>.md`. Kịch bản là hợp đồng giữa phần "viết" và phần "dựng": mỗi dòng bảng phân cảnh phải đủ thông tin để dựng mà không cần mở lại footage. Dùng đúng khối theo KIỂU đã chọn ở bước 0 — đừng bắt Kiểu 1 (không thoại) phải có mục "kịch bản voiceover".

## Khung chung (mọi kiểu đều có)

```markdown
# Video N — <Tên video>  (Kiểu <1/2/3>)

## Ý tưởng gốc (lời người dùng)
<chép nguyên văn ý tưởng được đưa, hoặc ghi "skill tự đề xuất" + lý do>

## Thông số
- Thời lượng mục tiêu: ~<X>s
- Nhạc nền: <file trong kho / "giữ âm gốc" / "không">
- Đối tượng xem: <chủ nhà hàng / chủ nhà máy / ...>

## Hook (0-3s)
- Chữ trên màn hình: "<HOOK NGẮN, GÂY SỐC HOẶC GÂY TÒ MÒ>"
- Cảnh nền: <clip + timecode — chọn cảnh MẠNH nhất của cả buổi quay>

## Bảng phân cảnh
| # | Nội dung (text đè / câu thoại) | Clip nguồn | Timecode in-out | Xử lý |
|---|---|---|---|---|
| 1 | <...> | clip03.mp4 | 01:23.5 - 01:27.0 | crop giữa |
| 2 | <...> | clip07.mp4 | 00:05.0 - 00:09.0 | blur-pad, giữ âm gốc 25% |

## CTA (câu chốt)
<câu kết + thông tin Roboworld — website roboworld.com.vn>
```

## Khối bổ sung theo kiểu

### Kiểu 1 — Highlight + chữ + nhạc (KHÔNG thoại)
- Không có mục voiceover. Cột "Nội dung" trong bảng phân cảnh = dòng text đè (IN HOA, 5-9 từ).
- Ghi rõ: nhạc nào (bài trong kho / âm gốc), SFX dự kiến ở khoảnh khắc nào (nếu có).

### Kiểu 2 — Dựng theo lời thoại có sẵn (voice gốc MC)
Thêm 2 mục BẮT BUỘC:

```markdown
## Các đoạn thoại dùng (từ transcript index.json)
| # | Clip | Câu thoại | Mốc Whisper (chỉ để TÌM) | Ghi chú |
|---|---|---|---|---|

## Take nghi vấn cần NGƯỜI DÙNG NGHE KIỂM trước khi dựng
<liệt kê các câu: chỉ có 1 take (nhất là voice-off), có từ chèn lặp ("à à", "tiếp tục lại..."),
hoặc transcript sạch nhưng chưa chắc take sạch — kèm clip + mốc thời gian để nghe đúng đoạn.
KHÔNG có đoạn nghi vấn nào thì ghi rõ "không có". Đây là 1 phần của điểm dừng duyệt kịch bản.>
```

- Luật cắt (**sửa 21/07/2026**): mốc Whisper chỉ để TÌM câu, **không bao giờ dùng để cắt** — Whisper nối đuôi các đoạn nên mốc bắt đầu là số bịa, không phải số đo (ca thật: báo 19.99s, thực tế 24.0s). Mốc cắt lấy từ `scripts/loc_thoai_that.py`. `silencedetect` chỉ còn là công cụ đối chiếu và **chỉ tin khi nó thật sự tìm ra khoảng im** — chi tiết: style-voice-karaoke.md, mục Quy tắc VOICE GỐC MC.

### Kiểu 3 — Ghép cảnh + voice-over mới
Thêm mục:

```markdown
## Kịch bản voiceover (đọc liền mạch)
<toàn bộ lời đọc, viết như nói chuyện, câu ngắn — đưa vào ElevenLabs>

## Giọng đọc
- ElevenLabs — **4 giọng** (đo 22/07/2026: đều dùng được, hết bị chặn): **Phương Uyên** (`Y9oZ1fkOxoaT3zFqTPzg` — nữ, giọng nhân bản RBW) · **Adam** (`pNInz6obpgDQGcFmaJgB` — nam, chắc mạnh) · **MC Xuân Tú** (`7XOKiK112QRZRSLbCfMc` — nam, giọng Bắc) · **Thanh Ngọc** (`Na15FlRRkMEDtEW4nVVP` — nữ, giọng Nam). Cách chọn: `references/chon-kieu-dung.md` khối "Chọn giọng đọc";
  người dùng muốn giọng khác → ghi voice ID được chọn ở đây
- ⛔ **Không có fallback** — edge-tts đã bỏ 22/07/2026 (Sếp nghe thấy đọc méo). ElevenLabs lỗi → DỪNG, báo người dùng, chờ quyết
```

- Cột "Nội dung" trong bảng phân cảnh = câu voiceover tương ứng cảnh đó.

## Nguyên tắc viết cho khách của Roboworld

- Người xem là **chủ chuỗi nhà hàng, chủ nhà máy/kho** — họ quan tâm: tiết kiệm nhân sự, chi phí, vận hành ổn định, khách của họ thích thú. Viết theo lợi ích, không theo thông số kỹ thuật.
- Hook tốt thường thuộc 1 trong 4 kiểu: con số gây sốc ("1 robot = lương 3 nhân viên?"), câu hỏi chạm nỗi đau ("Thiếu nhân viên chạy bàn mùa cao điểm?"), khoảnh khắc thật ("Khách Golden Gate lần đầu thấy robot..."), phản trực giác ("Nhà máy này KHÔNG tuyển thêm người").
- Mỗi câu voiceover 8-15 từ. Câu dài đọc lê thê, sub tràn màn hình.
- 25-40s là vùng vàng: đủ kể 1 ý, chưa kịp chán.
- Tên riêng khách hàng (Golden Gate, May 10...) chỉ đưa vào khi footage quay tại đó thật — tăng uy tín, nhưng tuyệt đối không bịa.

# Mẫu kịch bản shorts Roboworld

Mỗi ý tưởng video → 1 file `kichban/video-N-<slug>.md` theo đúng cấu trúc này. Kịch bản là hợp đồng giữa phần "viết" và phần "dựng": mỗi dòng bảng phân cảnh phải đủ thông tin để dựng mà không cần mở lại footage.

```markdown
# Video N — <Tên video>

## Ý tưởng gốc (lời Sếp)
<chép nguyên văn ý tưởng Sếp đưa, hoặc ghi "skill tự đề xuất" + lý do>

## Thông số
- Thời lượng mục tiêu: ~<X>s
- Giọng đọc: ElevenLabs <voice ID, ưu tiên số 1 — xem SKILL.md> — hoặc fallback edge-tts: vi-VN-NamMinhNeural / vi-VN-HoaiMyNeural (chỉ dùng khi ElevenLabs lỗi/hết quota)
- Nhạc nền: <file hoặc "không">
- Đối tượng xem: <chủ nhà hàng / chủ nhà máy / ...>

## Hook (0-3s)
- Chữ trên màn hình: "<HOOK NGẮN, GÂY SỐC HOẶC GÂY TÒ MÒ>"
- Cảnh nền: <clip + timecode — chọn cảnh MẠNH nhất của cả buổi quay>

## Kịch bản voiceover (đọc liền mạch)
<toàn bộ lời đọc, viết như nói chuyện, câu ngắn. Đây là phần đưa vào edge-tts.>

## Bảng phân cảnh
| # | Lời đọc (câu) | Clip nguồn | Timecode in-out | Xử lý |
|---|---|---|---|---|
| 1 | <câu 1> | clip03.mp4 | 01:23.5 - 01:27.0 | crop giữa |
| 2 | <câu 2> | clip07.mp4 | 00:05.0 - 00:09.0 | blur-pad, giữ âm gốc 25% |
| 3 | ... | ... | ... | tăng tốc 2x |

## CTA (câu chốt)
<câu kết + thông tin Roboworld — website roboworld.com.vn>
```

## Nguyên tắc viết cho khách của Roboworld

- Người xem là **chủ chuỗi nhà hàng, chủ nhà máy/kho** — họ quan tâm: tiết kiệm nhân sự, chi phí, vận hành ổn định, khách của họ thích thú. Viết theo lợi ích, không theo thông số kỹ thuật.
- Hook tốt thường thuộc 1 trong 4 kiểu: con số gây sốc ("1 robot = lương 3 nhân viên?"), câu hỏi chạm nỗi đau ("Thiếu nhân viên chạy bàn mùa cao điểm?"), khoảnh khắc thật ("Khách Golden Gate lần đầu thấy robot..."), phản trực giác ("Nhà máy này KHÔNG tuyển thêm người").
- Mỗi câu voiceover 8-15 từ. Câu dài đọc lê thê, sub tràn màn hình.
- 25-40s là vùng vàng: đủ kể 1 ý, chưa kịp chán.
- Tên riêng khách hàng (Golden Gate, May 10...) chỉ đưa vào khi footage quay tại đó thật — tăng uy tín, nhưng tuyệt đối không bịa.

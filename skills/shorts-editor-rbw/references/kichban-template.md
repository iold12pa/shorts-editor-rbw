# Mẫu kịch bản shorts Roboworld — theo 3 KIỂU DỰNG
<!-- tags: chung -->

Mỗi ý tưởng video → 1 file `kichban/video-N-<slug>.md`. Kịch bản là hợp đồng giữa phần "viết" và phần "dựng": mỗi dòng bảng phân cảnh phải đủ thông tin để dựng mà không cần mở lại footage. Dùng đúng khối theo KIỂU đã chọn ở bước 0 — đừng bắt Kiểu 1 (không thoại) phải có mục "kịch bản voiceover".

## 🔴 CÁCH TRÌNH BÀY — Sếp Huy chốt 22/07/2026
<!-- tags: chung -->

> Nguyên văn: *"Kịch bản hiện ra cho người dùng cũng phải khoa học dễ nhìn, bảng biểu có mốc thời gian ước chừng đàng hoàng."*

Kịch bản trình cho người duyệt **bắt buộc** có đủ 4 phần dưới, theo đúng thứ tự này. Người duyệt phải **nhìn một cái là hình dung được cả video chạy ra sao**, không phải tự cộng nhẩm.

**Ba lỗi trình bày bị cấm:**
1. **Chỉ ghi timecode của clip nguồn** mà không ghi cảnh đó rơi vào **giây thứ mấy của video thành phẩm** — người duyệt không hình dung được nhịp.
2. **Không ghi độ dài từng cảnh** và **không có dòng TỔNG** — không biết video dài bao nhiêu, cảnh nào bị lê thê.
3. Viết thành đoạn văn dài kể lể thay vì bảng.

Mốc thời gian là **ước chừng** (cảnh cắt theo nhịp lời/nhạc nên xê dịch ±0.5s) — cứ ghi rõ là ước chừng, đừng giả vờ chính xác tuyệt đối.

## Khung chung (mọi kiểu đều có)
<!-- tags: chung -->

```markdown
# Video N — <Tên video>   ·   Kiểu <1/2/3>   ·   ~<X>s

## 📋 Tóm tắt nhanh
| Mục | Nội dung |
|---|---|
| **Thông điệp chính** | <1 câu — video này nói lên điều gì> |
| **Người xem mục tiêu** | <chủ chuỗi nhà hàng / chủ nhà máy / khách tham quan...> |
| **Thời lượng** | ~<X>s (ước chừng, ±2s) |
| **Kênh đăng** | <page công ty: có logo + outro / cá nhân: bỏ hết> |
| **Nhạc** | <tên bài + loại: trend hay không bản quyền> |
| **Giọng đọc** | <tên giọng — chỉ Kiểu 3> |
| **Số cảnh** | <N> cảnh, nhịp trung bình <Y>s/cảnh |

## 🎬 Ý tưởng gốc
<chép nguyên văn mô tả của người dùng, hoặc ghi "skill tự đề xuất" + lý do.
Người dùng có mô tả buổi quay/đầu ra mong muốn → ghi rõ ý nào của họ nằm ở cảnh nào.>

## ⏱️ Bảng phân cảnh
| # | Mốc trong video | Dài | Nội dung hiện ra | Cảnh dùng | Lấy từ | Xử lý |
|---|---|---|---|---|---|---|
| 1 | **0:00 – 0:03** | 3.0s | 🔤 "CHỮ HOOK IN HOA" | robot tiến tới gần ống kính | `0043` @ 12.5–15.5 | zoom nhẹ |
| 2 | **0:03 – 0:08** | 5.0s | 🎙️ "câu lời đọc..." | khách vỗ tay nhìn robot | `0051` @ 03.0–08.0 | crop giữa |
| 3 | **0:08 – 0:12** | 4.0s | 🔤 "CHỮ ĐÈ" | robot bê đồ qua bàn | `0045` @ 20.0–24.0 | giữ tiếng gốc 25% |
|  | **TỔNG** | **12.0s** |  |  |  |  |

Ký hiệu cột "Nội dung": 🔤 chữ đè màn hình · 🎙️ lời đọc/lời thoại · 🔇 không chữ không lời, để hình chạy

## 🔊 Dải âm thanh theo mốc
| Mốc | Nhạc | Lời | Ghi chú |
|---|---|---|---|
| 0:00 – 0:08 | nhỏ (0.18) | có lời đọc | hạ nhạc để nghe rõ lời |
| 0:08 – hết | dâng (0.55) | không lời | nhạc lên, để hình kể chuyện |

## ✅ Điểm cần Sếp duyệt trước khi tôi dựng
1. <điều đáng phân vân nhất — vd: hook đã đủ mạnh chưa>
2. <cảnh nào còn nghi ngờ, hoặc chỗ thiếu tư liệu phải xoay>
3. <take thoại cần nghe kiểm — chỉ Kiểu 2>
```

## Khối bổ sung theo kiểu
<!-- tags: chung -->

### Kiểu 1 — Highlight + chữ + nhạc (KHÔNG thoại)
<!-- tags: kieu-1 -->
- Không có mục voiceover. Cột "Nội dung" trong bảng phân cảnh = dòng text đè (IN HOA, 5-9 từ).
- Ghi rõ: nhạc nào (bài trong kho / âm gốc), SFX dự kiến ở khoảnh khắc nào (nếu có).

### Kiểu 2 — Dựng theo lời thoại có sẵn (voice gốc MC)
<!-- tags: kieu-2 -->
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
<!-- tags: kieu-3 -->
Thêm mục:

```markdown
## Kịch bản voiceover (đọc liền mạch)
<toàn bộ lời đọc, viết như nói chuyện, câu ngắn — đưa vào ElevenLabs>

## Giọng đọc
- ElevenLabs — **4 giọng, hiện đủ cả 4 cho người dùng chọn** (đo 22/07/2026: đều dùng được, hết bị chặn). **Giọng CHÍNH**: **MC Xuân Tú** (`7XOKiK112QRZRSLbCfMc` — nam, giọng Bắc) · **Thanh Ngọc** (`Na15FlRRkMEDtEW4nVVP` — nữ, giọng Nam). **Giọng phụ** (không tự lấy làm mặc định): **Phương Uyên** (`Y9oZ1fkOxoaT3zFqTPzg` — nữ, giọng nhân bản RBW) · **Adam** (`pNInz6obpgDQGcFmaJgB` — nam, gốc tiếng Anh). Cách chọn: `references/chon-kieu-dung.md` khối "Chọn giọng đọc";
  người dùng muốn giọng khác → ghi voice ID được chọn ở đây
- ⛔ **Không có fallback** — edge-tts đã bỏ 22/07/2026 (Sếp nghe thấy đọc méo). ElevenLabs lỗi → DỪNG, báo người dùng, chờ quyết
```

- Cột "Nội dung" trong bảng phân cảnh = câu voiceover tương ứng cảnh đó.

## Nguyên tắc viết cho khách của Roboworld
<!-- tags: chung -->

- Người xem là **chủ chuỗi nhà hàng, chủ nhà máy/kho** — họ quan tâm: tiết kiệm nhân sự, chi phí, vận hành ổn định, khách của họ thích thú. Viết theo lợi ích, không theo thông số kỹ thuật.
- Hook tốt thường thuộc 1 trong 4 kiểu: con số gây sốc ("1 robot = lương 3 nhân viên?"), câu hỏi chạm nỗi đau ("Thiếu nhân viên chạy bàn mùa cao điểm?"), khoảnh khắc thật ("Khách Golden Gate lần đầu thấy robot..."), phản trực giác ("Nhà máy này KHÔNG tuyển thêm người").
- Mỗi câu voiceover 8-15 từ. Câu dài đọc lê thê, sub tràn màn hình.
- 25-40s là vùng vàng: đủ kể 1 ý, chưa kịp chán.
- Tên riêng khách hàng (Golden Gate, May 10...) chỉ đưa vào khi footage quay tại đó thật — tăng uy tín, nhưng tuyệt đối không bịa.

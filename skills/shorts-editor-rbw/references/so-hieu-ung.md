# Sổ hiệu ứng & năng lực dựng — bản đồ đầy đủ so với CapCut (lập 2026-07-17)

> Tổng hợp theo yêu cầu Sếp Huy: "tất cả chuyển cảnh, hiệu ứng... khiến edit video hơn, giống chức năng CapCut".
> **Trạng thái**: ✅ đã dựng demo (chờ Sếp chấm) · 🔧 làm được ngay bằng đồ có sẵn (chưa demo) · 📦 cần cài thêm (miễn phí) · 💰 cần trả phí/duyệt chủ trương · ❌ không đáng làm.
> **LUẬT**: hiệu ứng chỉ thành "chuẩn Roboworld" sau khi Sếp chấm đậu — khi đó ghi recipe chi tiết + LUẬT LIỀU LƯỢNG vào file này. Chưa chấm thì không tự ý dùng trong video giao hàng.
> 3 video demo cho Sếp chấm (Desktop máy legion): `DEMO HIEU UNG` (10 hiệu ứng chữ + 8 chuyển cảnh), `DEMO WOW` (10 món nâng cao), `DEMO BONUS` (4 món đặc biệt).

## A. HIỆU ỨNG CHỮ ĐỘNG

| # | Hiệu ứng | Trạng thái | Ghi chú kỹ thuật |
|---|---|---|---|
| A1 | Nảy bật vào (pop-in bounce) | ✅ DEMO#1-1 | ASS \t scale overshoot |
| A2 | Đập từng từ theo nhịp | ✅ DEMO#1-2 | event/từ + punch scale |
| A3 | Gõ máy chữ | ✅ DEMO#1-3 | event/ký tự |
| A4 | Quét hiện chữ (wipe reveal) | ✅ DEMO#1-4 | \t \clip |
| A5 | Trượt lên + mờ dần | ✅ DEMO#1-5 | \move + \fad |
| A6 | Karaoke tô vàng | ✅ DEMO#1-6 (đang là chuẩn Kiểu 2/3) | \k tags |
| A7 | Viền sáng nhấp nháy (glow) | ✅ DEMO#1-7 | \t \blur chu kỳ |
| A8 | Rung nhấn mạnh (impact) | ✅ DEMO#1-8 | \t \frz + scale giáng |
| A9 | Số liệu nhảy số (counter) | ✅ DEMO#1-9 | chuỗi event số tăng |
| A10 | Thẻ vàng quét hiện | ✅ DEMO#1-10 | BorderStyle=3 + \clip |
| A11 | Tiêu đề gradient + bóng đổ dài | ✅ WOW-6 | PIL render PNG overlay |
| A12 | Chữ NẰM SAU chủ thể | ✅ WOW-9 | rembg tách nền/khung + overlay 3 lớp |
| A13 | Chữ neon đổi màu / blur-in / nổ chữ cái / đếm ngược 3-2-1 / highlight nền chạy từng từ | 🔧 | đều là biến thể ASS, dựng thêm khi cần |
| A14 | Chữ bám theo vật chuyển động (tracking) | ❌ | đất của editor chuyên, không đáng cho shorts |

## B. CHUYỂN CẢNH

| # | Kiểu | Trạng thái | Ghi chú |
|---|---|---|---|
| B1-B8 | Chớp trắng, zoom xuyên, quét tròn, vỡ pixel/glitch, quét ngang mượt, trượt dọc, mờ ngang (whip), quét kim đồng hồ | ✅ DEMO#1 phần 2 | ffmpeg xfade |
| B9 | **Chuyển cảnh theo hình LOGO ROBOWORLD** (độc quyền thương hiệu) | ✅ BONUS-3 | mask PIL + maskedmerge — CapCut KHÔNG có món này |
| B10 | ~40 kiểu xfade còn lại (quét chéo, tan chữ thập, thu nhỏ, dissolve, fadegrays...) | 🔧 | có sẵn, demo thêm khi Sếp muốn xem hết |
| B11 | Chuyển cảnh 3D (lật khối, gương vỡ, bay qua) | ❌ tạm | cần bản ffmpeg build đặc biệt, lợi không bõ công |

## C. HIỆU ỨNG HÌNH / TỐC ĐỘ

| # | Hiệu ứng | Trạng thái | Ghi chú |
|---|---|---|---|
| C1 | Speed ramp (chậm-nhanh) | ✅ WOW-1 | setpts từng khúc |
| C2 | Zoom theo nhịp nhạc | ✅ WOW-2 | zoompan pulse |
| C3 | Rung màn hình (impact shake) | ✅ WOW-3 | crop jitter theo t |
| C4 | Glitch tách màu RGB | ✅ WOW-4 | rgbashift + noise burst |
| C5 | Đóng băng + thẻ tên | ✅ WOW-5 | freeze frame + zoom + card |
| C6 | Ken Burns ảnh sản phẩm | ✅ WOW-7 | PIL bóng đổ + overlay trôi |
| C7 | Màu phim điện ảnh | ✅ WOW-8 | eq + vignette |
| C8 | 2 góc máy giả từ 1 clip (punch-in) | ✅ BONUS-1 | crop 1.4x cắt qua lại — cứu cảnh phỏng vấn 1 máy |
| C9 | Boomerang | ✅ BONUS-2 | reverse + concat |
| C10 | Cắt cảnh theo beat TỰ ĐỘNG | ✅ WOW-10 | librosa dò phách → điểm cắt; LƯU Ý: tính duration lũy tiến theo frame để khỏi trôi |
| C11 | Tua ngược / mirror / đen trắng hồi tưởng / phim cũ nhiễu hạt / PIP hình-trong-hình / chia 3 màn dọc | 🔧 | 1-2 dòng filter mỗi món |
| C12 | Slow-mo mượt nội suy khung (minterpolate) | 🔧 | có sẵn, render chậm — chỉ dùng cho 1-2s khoảnh khắc vàng |
| C13 | Chống rung footage cầm tay (vidstab) | 🔧 | ffmpeg bản Gyan có sẵn libvidstab — đáng thử với clip quay tay |
| C14 | LUT màu điện ảnh (.cube) | 📦 miễn phí | tải LUT pack free + lut3d; cho "tông màu Roboworld" thống nhất |

## D. ÂM THANH

| # | Món | Trạng thái | Ghi chú |
|---|---|---|---|
| D1 | Nhạc ducking tự né giọng / chuẩn -14 LUFS / kho 35 SFX | ✅ đang là chuẩn | sidechaincompress, loudnorm |
| D2 | Khử ồn giọng hiện trường | ✅ BONUS-4 | highpass + afftdn — cứu phỏng vấn ồn |
| D3 | Dò beat bài nhạc | ✅ (nền của WOW-10) | librosa, đã cài |
| D4 | EQ làm dày giọng / de-esser / visualizer sóng nhạc chạy theo beat | 🔧 | ffmpeg có sẵn |
| D5 | Tách giọng khỏi nhạc (vocal remover) | ❌ tạm | demucs nặng máy, nhu cầu chưa rõ |

## E. AI / TỰ ĐỘNG

| # | Món | Trạng thái | Ghi chú |
|---|---|---|---|
| E1 | Nghe thoại tiếng Việt (Whisper) + sub karaoke | ✅ chuẩn hiện tại | |
| E2 | Tách nền AI (đã dùng cho chữ-sau-chủ-thể) | ✅ WOW-9 | rembg local, không upload gì |
| E3 | Xóa nền CẢ CLIP ngắn (green screen ảo) / cắt robot từ footage làm sticker dán video khác | 🔧 | rembg từng khung, ~1-2 phút/giây clip — dùng chấm phá |
| E4 | Gemini "xem" video chọn khoảnh khắc | 💰 chờ Sếp duyệt (Đợt 5) | upload footage lên cloud |
| E5 | Sinh nhạc đo ni (ElevenLabs Music) | 💰 chờ nâng gói | script đã nằm sẵn |
| E6 | Auto-caption theo template có sẵn kiểu CapCut | ✅ hơn CapCut | mình tự chủ style ASS theo brand, không lệ thuộc template |

## Đồ đã cài thêm cho mảng này (2026-07-17, đều miễn phí, chạy local)

- `librosa` (dò beat/tempo), `rembg` + model u2net ~170MB tại `~/.u2net/` (tách nền AI), `onnxruntime`.
- **LƯU Ý tương thích**: rembg/cv2 cần `numpy<2` — máy legion đã hạ numpy 1.26.4; máy mới cài rembg nhớ kèm `pip install "numpy<2"`.

## Việc còn nợ trong sổ này

1. Sếp chấm 3 demo → đánh dấu món ĐẬU, ghi recipe chi tiết + luật liều lượng (hook→pop-in, số liệu→nhảy số, chuyển cảnh mạnh chỉ ở bước ngoặt, WOW tối đa 1-2 lần/video...).
2. Món 🔧 nào Sếp muốn xem thì dựng demo bổ sung (nói tên là dựng).
3. Cập nhật `chon-kieu-dung.md`/kịch bản template để bước duyệt kịch bản ghi rõ video này dùng hiệu ứng nào.

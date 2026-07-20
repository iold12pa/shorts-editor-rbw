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
| B10 | TOÀN BỘ 48 kiểu xfade còn lại | ✅ DEMO#6 (catalog 127s, nhãn XF 1-48) | ffmpeg có sẵn |
| B11 | **Luma wipe dựng sẵn** (mực loang, quét chéo mềm, iris, rèm, sóng lượn) | ✅ DEMO#4 (LUMA 1-5) | mask PIL 18 khung + maskedmerge; kho mở rộng vô hạn (tự sinh mẫu hoặc nạp pack luma free) |
| B12 | **GL-TRANSITIONS — kho ~80 chuyển cảnh pro của giới editor** (khối 3D xoay, cửa lùa, gợn sóng, giọt nước, morph, glitch ký ức, zoom xuyên, mơ màng, gió cuốn, tổ ong...) | ✅ ĐÃ CÀI + DEMO#5 10 kiểu tuyển (GL 1-10) | chạy shader chính thức gl-transitions trên GPU máy qua `moderngl`; runner: `temp gl_runner.py` (sẽ đóng chính thức vào scripts/ sau khi Sếp chấm); muốn kiểu nào trong ~70 kiểu còn lại chỉ cần tải 1 file .glsl từ repo gl-transitions |

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
- `moderngl` (chạy shader GL-Transitions trên GPU — đã xác minh chạy tốt trên GTX 1650 Ti); shader nguồn tải từ `github.com/gl-transitions/gl-transitions` (giấy phép mở, dùng thương mại OK).
- **LƯU Ý tương thích**: rembg/cv2 cần `numpy<2` — máy legion đã hạ numpy 1.26.4; máy mới cài rembg nhớ kèm `pip install "numpy<2"`.
- **Kỹ thuật lõi 2 dòng chuyển cảnh mới**: (a) luma wipe = bộ mask PNG 18 khung (PIL sinh) + `maskedmerge`; (b) GL = trích 18 khung giao thoa mỗi bên → shader render qua moderngl → ráp lại. Cả 2 đều đóng gói được thành lệnh `noi-2-canh --kieu <tên>` khi Sếp chấm xong.
- **BẪY đường dẫn chứa `[ ]` (bài học 19/07/2026 — lỗi IM LẶNG, tốn nhiều thời gian truy)**: `glob.glob` của Python hiểu `[ ]` là dải-ký-tự nên trả **rỗng**, `gl_runner.py` chạy xong vẫn in "OK ... 0 khung" và `exit 0` như thành công. Cùng ngày xác nhận **`ffmpeg -i` cũng hỏng y hệt** trên path có `[ ]`. Đã vá script (`glob.escape` + thoát lỗi rõ ràng thay vì im lặng), nhưng **lệnh gõ tay vẫn dính** → gặp footage nằm trong folder kiểu `D:\...\[EDIT]\...` thì **copy ra đường dẫn sạch trước khi xử lý**.
- **`xfade` trên ffmpeg 8.x**: bắt buộc `fps=30,settb=AVTB` (fps TRƯỚC settb) ở CẢ 2 nhánh, offset lấy từ duration đo SAU concat — chi tiết ở `ffmpeg-recipes.md` mục 4c.

## NGUYÊN TẮC DÙNG từ giáo lý dựng phim + motion design (tra cứu nguồn ngành 17/07/2026)

**Chọn điểm cắt — Rule of Six của Walter Murch (editor huyền thoại, giản lược cho shorts):** khi phân vân cắt ở đâu, ưu tiên theo thứ tự: **CẢM XÚC (quan trọng nhất, đáng hơn cả 5 tiêu chí còn lại cộng lại) > tiến câu chuyện > đúng nhịp > hướng mắt người xem đang nhìn**. Phải hy sinh thì hy sinh từ dưới lên — không bao giờ hy sinh cảm xúc.

**Ngữ pháp chuyển cảnh (điện ảnh kinh điển — chống lưng cho luật sẵn có của mình):** cắt cứng = mặc định kể chuyện; crossfade/dissolve = báo hiệu ĐỔI thời gian/không gian; chuyển cảnh mạnh (GL cube, glitch, luma...) = bước ngoặt lớn — **1-2 lần/video là tối đa**, dùng nhiều thành TVC chợ.

**Timing chữ động (chuẩn motion design):**
- Chữ VÀO hoàn tất trong **0.3-0.8s** (pop-in demo của mình 0.36s — đạt chuẩn); lâu hơn = ì.
- **Ease-out khi VÀO** (nhanh trước chậm sau — tự nhiên), **ease-in khi RA** (tăng tốc thoát); tuyến tính đều đều = máy móc.
- Nhiều dòng/nhiều từ: so le mỗi phần tử **0.05-0.15s** tạo nhịp sóng.
- Hiệu ứng che diện tích màn hình LỚN cần thời lượng dài hơn hiệu ứng nhỏ.

Nguồn: StudioBinder/NoFilmSchool — Walter Murch Rule of Six; Material Design — Easing and duration; NN/g — Executing UX Animations; Demotion — Text Animation Secrets.

## Việc còn nợ trong sổ này

1. Sếp chấm 3 demo → đánh dấu món ĐẬU, ghi recipe chi tiết + luật liều lượng (hook→pop-in, số liệu→nhảy số, chuyển cảnh mạnh chỉ ở bước ngoặt, WOW tối đa 1-2 lần/video...).
2. Món 🔧 nào Sếp muốn xem thì dựng demo bổ sung (nói tên là dựng).
3. Cập nhật `chon-kieu-dung.md`/kịch bản template để bước duyệt kịch bản ghi rõ video này dùng hiệu ứng nào.

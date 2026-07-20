# Cài đặt lần đầu — kịch bản TỰ ĐỘNG TRỌN BỘ (dành cho phiên Claude đang cài máy mới)

> File này được câu lệnh cài dán-1-lần trỏ tới. Đọc xong làm theo NGAY, đừng hỏi lại người dùng
> trừ chỗ ghi rõ phải hỏi. Mục tiêu: người dùng (không rành kỹ thuật) dán 1 câu là máy được cài
> TRỌN BỘ, biết trước mất bao lâu, biết từng mục xong lúc nào — không phải làm gì thêm.

## Bước 0 — BÁO TRƯỚC cho người dùng (nói ngay, trước khi làm bất cứ gì)

Nói tự nhiên theo ý này (đừng chép máy móc):

> "Plugin đã vào máy. Giờ tôi cài nốt toàn bộ đồ nghề — tự động hết, bạn không phải bấm gì:
> (1) bộ xử lý video FFmpeg (nếu máy chưa có, ~3-5 phút),
> (2) bộ nghe giọng nói tiếng Việt ~1.6GB (~5-15 phút tùy mạng — tải ngầm),
> (3) kho logo/nhạc/hiệu ứng của công ty ~180MB (~2-5 phút — tải ngầm),
> (4) dò card đồ họa xem có tăng tốc render được không (vài giây).
> **Tổng khoảng 10-20 phút với mạng bình thường** — phần nặng chạy ngầm, xong mục nào tôi báo mục đó.
> Bạn cứ để máy đấy, làm việc khác thoải mái."

Rồi làm tuần tự bên dưới. Đường dẫn gốc của gói (dùng cho mọi script bên dưới, gọi tắt `<PKG>`):
`~/.claude/plugins/marketplaces/roboworld-tools/skills/shorts-editor-rbw`

## Bước 1 — Nền tảng: Python + FFmpeg (làm trước, nhanh)

1. Kiểm `python --version` — chưa có thì `winget install Python.Python.3.12 -e --source winget` (báo 1 câu).
2. **Cài BỘ THƯ VIỆN PYTHON (bắt buộc — thiếu là mất nửa số tính năng)**, im lặng, ~1-3 phút:
   ```powershell
   python -m pip install -U gdown edge-tts pillow moderngl librosa opencv-python google-genai "numpy<2"
   ```
   | Thư viện | Thiếu thì mất gì |
   |---|---|
   | `gdown` | không tải được kho tài nguyên từ Drive |
   | `edge-tts` | không có giọng đọc dự phòng (Kiểu 3 chết khi chưa có key ElevenLabs) |
   | `librosa` | **không dò được phách/BPM** → mất cắt-bám-phách và mất tính năng tách nhạc từ mix dài |
   | `moderngl` | không chạy được chuyển cảnh GL (~80 kiểu) |
   | `pillow` | không làm được luma wipe, thẻ chữ động, mask logo |
   | `opencv-python` | không chấm được điểm kỹ thuật clip (độ nét / chuyển động) → mất bước lọc clip hỏng |
   | `google-genai` | không chạy được **mắt AI Gemini** (`quet_mat_ai.py`, `gemini_vision.py`) |
   | `numpy<2` | **phải ghim <2** — numpy 2.x làm hỏng rembg/cv2 (đã dính thật) |

   Không cài trong lệnh trên: **`rembg`** (tách nền AI) — nó kéo theo `onnxruntime` + model u2net ~170MB, chỉ cần khi dựng cảnh cutout. Để dành, khi nào thật sự cần thì `python -m pip install rembg` rồi báo người dùng mất thêm ~2 phút.
3. Kiểm `ffmpeg -version` — chưa có thì báo 1 câu rồi `winget install ffmpeg -e --source winget`.
   Cài xong nếu lệnh `ffmpeg` chưa nhận trong phiên này: tự tìm `ffmpeg.exe`/`ffprobe.exe` trong
   `%LOCALAPPDATA%\Microsoft\WinGet\Packages\Gyan.FFmpeg*\` (đệ quy, lấy trong thư mục `bin`) và dùng
   đường dẫn đầy đủ cho các bước sau — KHÔNG bắt người dùng khởi động lại giữa chừng.

## Bước 2 — Bộ nghe giọng nói (1.6GB, chạy NỀN ngay)

Chạy nền (run_in_background) lệnh trong `<PKG>/assets/models/README.md`: tải `.part` rồi rename,
đích `~/.claude/roboworld-assets/models/ggml-large-v3-turbo.bin`. Đã có sẵn file này (máy cài lại) → báo "có sẵn, bỏ qua".

## Bước 3 — Kho tài nguyên công ty (~180MB, chạy NỀN ngay, song song bước 2)

Chạy nền: `python "<PKG>/scripts/tai_kho_tai_nguyen.py"` — script tự tải từ Google Drive về
`~/.claude/roboworld-assets/tai-nguyen-chung/`, TỰ KIỂM ĐẾM từng file, thiếu file nào báo đích danh.
Nếu nó báo thiếu + "Google chặn tạm": báo người dùng "kho về thiếu N file do Google giới hạn tải,
15-30 phút nữa nhắn 'cập nhật kho tài nguyên' là đủ" — KHÔNG coi là lỗi cài đặt.

## Bước 4 — Dò card đồ họa (vài giây, trong lúc chờ bước 2-3)

`python "<PKG>/scripts/cai_driver_nvidia.py" --check`:
- `GPU_SAN_SANG` / `KHONG_CO_CARD` → không nói gì nhiều, ghi vào bảng trạng thái.
- `CAN_NANG_DRIVER` → HỎI người dùng đúng 1 câu: *"Máy bạn có card đồ họa NVIDIA nhưng bộ điều khiển
  cũ nên render chậm. Cho tôi tải bản mới từ NVIDIA (~1GB, miễn phí) cài giúp nhé? Nếu Windows hiện
  hộp thoại xanh thì bấm YES — nhiều máy tự chạy không hỏi. Xong render nhanh 2-5 lần."* — OK thì chạy
  nền script đó KHÔNG có `--check` (nó tự lo hết, kể cả ca máy cần khởi động lại — sẽ tự báo).

## Bước 4b — BẬT AUTO-UPDATE (bắt buộc, vài giây — đừng bỏ qua)

Sửa `~/.claude/settings.json`: đặt `extraKnownMarketplaces."roboworld-tools".autoUpdate = true` (giữ nguyên mọi trường khác, nhất là `source`). Không tạo file backup (chính sách chủ repo — xem SKILL.md).

**Vì sao phải làm ngay ở bước cài, không đợi lần dựng video đầu tiên**: đây là công cụ nội bộ được cập nhật liên tục; máy nào không bật cờ này sẽ đứng yên ở bản cài ban đầu, dựng theo luật cũ mà không ai biết. Đã có tiền lệ 2 máy kẹt bản cũ nhiều ngày.

## Bước 5 — Chốt: bảng trạng thái + dặn dò (khi bước 2-3 xong hết)

In bảng trạng thái đúng mẫu trong SKILL.md mục "Lệnh CHUẨN BỊ MÁY" (FFmpeg / Bộ nghe / Kho x-trên-x
file theo manifest / GPU / Key giọng đọc AI), kèm **tổng thời gian thật đã mất**, rồi dặn 2 câu:
1. "Đóng app Claude mở lại 1 lần cho plugin nhận đủ — xong là dựng video được ngay: kéo-thả folder
   buổi quay vào chat và nói 'dựng video từ folder này'."
2. "Giọng đọc AI xịn (không bắt buộc): khi nào nhận được key từ quản trị qua Zalo, dán vào đây và nói
   'lưu key ElevenLabs này' là xong — chưa có key vẫn dựng bình thường bằng giọng dự phòng."

## Nếu có bước lỗi

Báo rõ bước nào lỗi + nguyên văn dòng lỗi + các bước còn lại vẫn hoàn tất bình thường. Đừng dừng cả
quy trình vì 1 mục phụ (thiếu kho/model vẫn dựng được Kiểu 1 sau khi tải bù; chỉ FFmpeg là bắt buộc).

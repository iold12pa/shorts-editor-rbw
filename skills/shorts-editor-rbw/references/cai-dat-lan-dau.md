# Cài đặt lần đầu — MỘT LỆNH TỰ CÀI TRỌN BỘ

> File này được câu lệnh cài dán-1-lần trỏ tới. Đọc xong làm theo NGAY.
> Mục tiêu (chỉ đạo Sếp Huy 21/07/2026): **máy người dùng có đúng mọi thứ máy quản trị có,
> mà họ KHÔNG phải cài thủ công gì cả.**
>
> **Sửa 21/07/2026**: trước đây mục này là quy trình 5 bước mà Claude bên máy người dùng phải
> làm đúng thứ tự — dễ sót, và đã sót thật (thiếu `onnxruntime`, thiếu model Silero, chỉ dặn
> key ElevenLabs mà quên Gemini). Nay gom hết vào **1 script duy nhất**.

## Bước 0 — Báo trước cho người dùng (nói ngay, trước khi chạy)

Nói tự nhiên theo ý này:

> "Plugin đã vào máy. Giờ tôi cài nốt toàn bộ đồ nghề — tự động hết, bạn không phải bấm gì:
> bộ xử lý video, bộ nghe giọng nói tiếng Việt ~1.6GB, kho logo/nhạc/hiệu ứng của công ty ~180MB,
> các thư viện cần thiết, và dò card đồ hoạ xem có tăng tốc render được không.
> **Tổng khoảng 10-20 phút** với mạng bình thường — chạy ngầm, bạn cứ làm việc khác."

## Bước 1 — Chạy đúng MỘT lệnh (chạy NỀN)

```powershell
python "<PKG>\scripts\chuan_bi_may.py"
```

`<PKG>` = `~/.claude/plugins/marketplaces/roboworld-tools/skills/shorts-editor-rbw`

Chạy bằng `run_in_background` vì mất 10-20 phút. Script tự làm hết, in tiến độ từng mục:

| Script tự lo | Ghi chú |
|---|---|
| 10 thư viện Python | tự `pip install` món nào thiếu. `numpy` **ghim <2** — bản 2.x làm hỏng cv2 |
| FFmpeg | tự `winget install`; nếu PATH chưa nhận thì **tự ghi đường dẫn vào `config.json`** — không bắt khởi động lại |
| Whisper 1.6GB | tải vào `.part` rồi mới đổi tên → không có chuyện script khác vớ nhầm file tải dở |
| Silero VAD 2.3MB | model soi chéo giọng người khi đo mốc thoại |
| Kho tài nguyên ~180MB | gọi `tai_kho_tai_nguyen.py`, tự đếm file |
| Card đồ hoạ | dò `nvidia`, báo 1 trong 3 trạng thái |

Kết thúc script in **bảng trạng thái máy** + câu chốt `MAY DA SAN SANG DUNG VIDEO` hoặc liệt kê thứ còn thiếu.

**Cờ phụ**: `--kiem` chỉ kiểm không cài (dùng cho lệnh "kiểm tra máy đủ đồ chưa"); `--nhanh` bỏ qua 2 khoản tải nặng.

**Script báo `CAN_NANG_DRIVER`** → hỏi người dùng đúng 1 câu:
> *"Máy bạn có card đồ hoạ NVIDIA nhưng bộ điều khiển cũ nên render chậm. Cho tôi tải bản mới từ NVIDIA (~1GB, miễn phí) cài giúp nhé? Nếu Windows hiện hộp thoại xanh thì bấm YES — nhiều máy tự chạy không hỏi. Xong render nhanh 2-5 lần."*

OK thì chạy nền `python "<PKG>\scripts\cai_driver_nvidia.py"` (không có `--check`). Không OK thì thôi, không hỏi lại trong phiên.

## Bước 2 — Bật auto-update (vài giây, đừng bỏ qua)

Sửa `~/.claude/settings.json`: đặt `extraKnownMarketplaces."roboworld-tools".autoUpdate = true` (giữ nguyên mọi trường khác, nhất là `source`). Không tạo file backup (chính sách chủ repo).

**Vì sao phải làm ngay lúc cài**: đây là công cụ nội bộ cập nhật liên tục; máy không bật cờ này sẽ đứng yên ở bản cài ban đầu, dựng theo luật cũ mà không ai biết. **Đã có tiền lệ 2 máy kẹt bản cũ nhiều ngày.**

## Bước 3 — API key (phần DUY NHẤT không tự động được)

Script sẽ liệt kê key nào còn thiếu. Cách đưa key cho người dùng:

> **Người dùng chỉ cần DÁN KEY VÀO CHAT và nói "lưu key này". Không phải mở file, không phải biết đường dẫn.**

Claude nhận key rồi ghi bằng:

```powershell
"<gia-tri-key>" | python "<PKG>\scripts\chuan_bi_may.py" --luu-key ELEVENLABS_API_KEY
```

Truyền qua **stdin** chứ không qua tham số dòng lệnh — để key không lọt vào lịch sử lệnh. Script không in giá trị key ra màn hình. Ghi đè key cũ thì không nhân đôi dòng.

Ba key: `ELEVENLABS_API_KEY` (giọng đọc + sinh nhạc) · `GEMINI_API_KEY` (mắt AI xem clip) · `GROQ_API_KEY` (dự phòng).

### ⛔ Vì sao KHÔNG tự tải key về được — giới hạn thật, không phải chưa làm

Muốn script tự lấy key mà không cần đăng nhập thì key phải nằm ở chỗ ai cũng vào được — tức là **key thành công khai**. Mà kho tài nguyên trên Drive **đang share công khai và link nằm trong repo GitHub public**, nên để key vào đó là phát tán key. ElevenLabs/Gemini tính tiền theo lượng dùng, ai cầm được key là tiêu tiền của công ty.

→ Key phải đi đường riêng (Zalo), nhưng **thao tác của người dùng chỉ còn 1 bước dán vào chat**.

**Chưa có key vẫn dựng video bình thường**: giọng đọc tự lui về edge-tts tiếng Việt (miễn phí, sạch); mắt AI Gemini bỏ qua, dùng tầng đo kỹ thuật miễn phí thay thế.

## Bước 4 — Chốt

In lại bảng trạng thái từ script, kèm tổng thời gian thật đã mất, rồi dặn:

1. *"Đóng app Claude mở lại 1 lần cho plugin nhận đủ — xong là dựng video được ngay: kéo-thả folder buổi quay vào chat và nói 'dựng video từ folder này'."*
2. *"Khi nào nhận được key từ quản trị qua Zalo, dán vào đây nói 'lưu key này' là xong."*

## Nếu có bước lỗi

Báo rõ mục nào lỗi + nguyên văn dòng lỗi, và nói rõ **các mục còn lại vẫn hoàn tất bình thường**. Đừng dừng cả quy trình vì 1 mục phụ — thiếu kho/model vẫn dựng được Kiểu 1 sau khi tải bù; **chỉ FFmpeg là bắt buộc tuyệt đối**.

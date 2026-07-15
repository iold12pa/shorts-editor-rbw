# Model Whisper — tải riêng, không nằm trong gói cài

File model (`ggml-large-v3-turbo.bin`, ~1.6GB) dùng để nghe tiếng Việt trong footage (Whisper). File này quá lớn để đưa vào gói cài qua Git, nên cần tải riêng **1 lần duy nhất** sau khi cài plugin.

## Cách tải (chọn 1 trong 2)

**Cách 1 — PowerShell (khuyên dùng):**
```powershell
Invoke-WebRequest -Uri "https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-large-v3-turbo.bin" -OutFile "ggml-large-v3-turbo.bin"
```
Chạy lệnh này ngay trong thư mục `assets/models/` này (dùng `cd` tới đây trước, hoặc sửa `-OutFile` thành đường dẫn đầy đủ).

**Cách 2 — Tải tay:** mở link `https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-large-v3-turbo.bin` trên trình duyệt, tải về, đặt đúng tên file `ggml-large-v3-turbo.bin` vào chính thư mục này.

## Không có model thì sao?

Skill vẫn chạy được bình thường — chỉ là phần "nghe lời thoại trong footage" (Whisper) sẽ tự động bỏ qua, script sẽ báo rõ khi thiếu model. Cần Kiểu 2/3 (video có thoại) thì bắt buộc phải có model này; Kiểu 1 (chỉ nhạc, không thoại) thì không cần.

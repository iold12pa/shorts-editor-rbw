# Model Whisper — tải riêng, không nằm trong gói cài

File model (`ggml-large-v3-turbo.bin`, ~1.6GB) dùng để nghe tiếng Việt trong footage (Whisper). File này quá lớn để đưa vào gói cài qua Git, nên cần tải riêng.

**Chỗ lưu chuẩn (máy cài mới): `~/.claude/roboworld-assets/models/`** — chỗ bền, gỡ/cài lại plugin KHÔNG mất, không phải tải lại 1.6GB. Máy cũ đã có model ngay trong thư mục `assets/models/` này vẫn dùng bình thường — script tự tìm cả 2 nơi, ưu tiên chỗ bền.

**Không cần tự tải tay**: Claude TỰ ĐỘNG tải file này ngay lần đầu bạn dùng skill — tải NỀN (bạn cứ làm việc tiếp, không phải ngồi chờ; 1.6GB mất vài phút tới vài chục phút tùy mạng). Chỉ cần tự tải theo hướng dẫn dưới nếu muốn chuẩn bị trước, hoặc nếu Claude báo lỗi khi tự tải (mạng chặn, v.v).

## Quy tắc tải (áp dụng cả khi Claude tự tải lẫn tải tay)

Tải vào tên file tạm đuôi `.part`, xong mới đổi tên thành `.bin` — để script phân tích không vớ nhầm file đang tải dở:

```powershell
New-Item -ItemType Directory -Force "$env:USERPROFILE\.claude\roboworld-assets\models" | Out-Null
Invoke-WebRequest -Uri "https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-large-v3-turbo.bin" `
  -OutFile "$env:USERPROFILE\.claude\roboworld-assets\models\ggml-large-v3-turbo.bin.part"
Rename-Item "$env:USERPROFILE\.claude\roboworld-assets\models\ggml-large-v3-turbo.bin.part" "ggml-large-v3-turbo.bin"
```

(Tải tay bằng trình duyệt cũng được: mở link trên, tải về, đặt đúng tên `ggml-large-v3-turbo.bin` vào thư mục `~/.claude/roboworld-assets/models/`.)

## Không có model thì sao?

Skill vẫn chạy được bình thường — phần "nghe lời thoại" sẽ ghi trạng thái **"chưa nghe được"** (khác với "không có thoại") và tự nghe bổ sung khi chạy lại lúc model đã sẵn sàng. **Kiểu 2/3 (video có thoại) phải chờ model tải xong mới phân tích** — Kiểu 1 (chỉ nhạc) thì không cần.

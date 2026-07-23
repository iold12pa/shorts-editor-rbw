# Cài đặt & cập nhật — Công cụ dựng video Roboworld

File này chỉ nói về **cài lần đầu** và **cập nhật bản mới** — 2 phút đọc. Học cách dùng để dựng video thì đọc [HUONG-DAN-NGUOI-MOI.md](HUONG-DAN-NGUOI-MOI.md).

---

## 1. Cài lần đầu (~10-20 phút, làm 1 lần)

**Điều kiện**: máy đã có app Claude Code + tài khoản còn hạn dùng.

Mở app Claude → vào mục **Code** → dán nguyên đoạn dưới đây → Enter:

```
Cài bộ công cụ dựng video Roboworld cho tôi: chạy qua Bash 2 lệnh 1) claude plugin marketplace add https://github.com/iold12pa/shorts-editor-rbw 2) claude plugin install shorts-editor-rbw@roboworld-tools — xong ĐỌC file ~/.claude/plugins/marketplaces/roboworld-tools/skills/shorts-editor-rbw/references/cai-dat-lan-dau.md và làm đúng theo file đó: cài tự động trọn bộ, báo tôi tiến độ và tổng thời gian ước tính.
```

Máy sẽ tự cài hết, không cần bạn làm gì thêm: FFmpeg (bộ xử lý video) → bộ nghe giọng nói tiếng Việt (~1.6GB) → kho logo/nhạc/hiệu ứng công ty (~180MB) → dò card đồ hoạ để tăng tốc render. Xong sẽ in ra 1 **bảng trạng thái** đủ/thiếu từng mục.

> ⚠️ **Đừng gõ thẳng `/plugin marketplace add ...` vào app** — cú pháp đó chỉ chạy trong cửa sổ terminal, gõ vào app Claude thường sẽ báo lỗi "isn't available in this environment". Cứ dán nguyên đoạn trên, để Claude tự chạy giúp.

**Sau khi cài xong: đóng app và mở lại 1 lần** — bản vừa cài chỉ có hiệu lực đầy đủ sau khi khởi động lại.

Muốn kiểm tra bất cứ lúc nào máy đã đủ đồ chưa: nhắn **"kiểm tra máy đủ đồ chưa"**.

---

## 2. Nhập key giọng đọc AI (tuỳ chọn — chỉ cần nếu dựng video có thuyết minh)

Quản trị gửi bạn key riêng qua Zalo. Nhận được key thì nhắn Claude:

> **"nhập key"**

Một **cửa sổ nhỏ hiện lên** với ô nhập che dấu sao — dán key vào, bấm **LƯU**. *(Đã test thật ngày 24/07/2026 — hoạt động đúng: không nhập gì thì báo "không nhập key nào", không ghi đè gì cả.)*

> 🔒 **Đừng bao giờ dán key vào khung chat.** Mọi thứ gõ vào chat đều đi qua máy chủ và nằm lại trong lịch sử hội thoại. Cửa sổ nhập key thì giá trị đi thẳng vào máy bạn, Claude không bao giờ thấy được.

Nhập xong, nhắn lại **"kiểm tra máy đủ đồ chưa"** — hiện "đúng key chuẩn công ty" là ổn; hiện "SAI KEY" thì dán nhầm, xin lại quản trị.

**Chưa có key vẫn dựng video bình thường** — chỉ là dùng giọng đọc dự phòng thay vì giọng cao cấp.

---

## 3. Cập nhật bản mới

**Bình thường bạn không phải làm gì.** Mỗi lần nhờ dựng video, công cụ tự kiểm tra GitHub và tự kéo bản mới ngay đầu phiên chat. Vừa có bản mới thì nó tự báo 1 câu.

**Muốn chủ động kiểm tra** (ví dụ quản trị báo "vừa có luật mới"): nhắn

> **"đang bản nào"** hoặc **"có bản mới không"**

Công cụ sẽ trả lời bằng **số Ver** dễ nhớ (vd *"Đang ở Ver 29"*) — không phải dãy số ngày tháng khó nhớ. Hỏi "bản 29 sửa gì" thì nó tra và tóm tắt lại cho bạn.

> ⚠️ **Điều quan trọng nhất cần nhớ**: Claude Code chỉ nạp bản mới lúc **khởi động app**. Nên khi công cụ báo "vừa cập nhật", phiên đang mở vẫn đang chạy bản CŨ — phải **đóng/mở lại app 1 lần** thì bản mới mới có hiệu lực thật sự. Đây không phải lỗi, là cách Claude Code hoạt động.

---

## 4. Cài lỗi giữa chừng / cần gỡ-cài-lại? Dán câu này

```
Cài lại bộ công cụ dựng video Roboworld cho tôi: chạy qua Bash 4 lệnh 1) claude plugin uninstall shorts-editor-rbw@roboworld-tools 2) claude plugin marketplace remove roboworld-tools 3) claude plugin marketplace add https://github.com/iold12pa/shorts-editor-rbw 4) claude plugin install shorts-editor-rbw@roboworld-tools — xong ĐỌC file ~/.claude/plugins/marketplaces/roboworld-tools/skills/shorts-editor-rbw/references/cai-dat-lan-dau.md và làm đúng theo file đó: cài tự động trọn bộ, báo tôi tiến độ và tổng thời gian ước tính.
```

Bộ nghe giọng nói + kho tài nguyên nằm ở chỗ bền `~/.claude/roboworld-assets/`, **không mất khi gỡ-cài-lại** — bước cài sẽ thấy "có sẵn" và bỏ qua, chỉ mất ~1 phút thay vì 10-20 phút.

---

## Tóm tắt 1 dòng

Cài: dán 1 câu ở mục 1 → đóng/mở app. Cập nhật: tự động, không cần làm gì — muốn chắc thì hỏi "đang bản nào".

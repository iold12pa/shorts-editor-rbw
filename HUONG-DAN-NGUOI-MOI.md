# Hướng dẫn dùng công cụ dựng video Roboworld

Dành cho người mới, không cần biết kỹ thuật. Đọc hết mất khoảng 5 phút.

---

## Phần 1 — Công cụ này làm gì

Bạn đưa cho nó **folder footage một buổi quay** (đống video thô từ máy quay/điện thoại). Nó xem hết, đề xuất kịch bản cho bạn duyệt, rồi tự dựng ra **video ngắn dọc 9:16 hoàn chỉnh** — có chữ, nhạc, logo, hiệu ứng, outro — kèm sẵn **bài caption để đăng**.

Nó **không** thay bạn quyết định. Có 2 lúc nó dừng lại hỏi ý bạn: chọn kiểu dựng lúc đầu, và duyệt kịch bản trước khi dựng.

---

## Phần 2 — Cài đặt (làm 1 lần, ~10-20 phút)

**Điều kiện**: máy đã có app Claude Code và tài khoản còn hạn dùng.

Mở app Claude → vào mục **Code** → dán nguyên đoạn dưới đây rồi Enter:

```
Cài bộ công cụ dựng video Roboworld cho tôi: chạy qua Bash 2 lệnh 1) claude plugin marketplace add https://github.com/iold12pa/shorts-editor-rbw 2) claude plugin install shorts-editor-rbw@roboworld-tools — xong ĐỌC file ~/.claude/plugins/marketplaces/roboworld-tools/skills/shorts-editor-rbw/references/cai-dat-lan-dau.md và làm đúng theo file đó: cài tự động trọn bộ, báo tôi tiến độ và tổng thời gian ước tính.
```

Sau đó **cứ để máy đấy làm việc khác**. Nó tự cài: bộ xử lý video, bộ nghe giọng nói tiếng Việt (~1.6 GB), kho logo/nhạc/hiệu ứng của công ty (~180 MB), và dò card đồ họa để tăng tốc.

Xong nó in ra một **bảng trạng thái** đủ/thiếu từng mục. **Đóng app mở lại 1 lần** là dùng được.

> ⚠️ Đừng gõ thẳng `/plugin marketplace add ...` vào app — cú pháp đó chỉ chạy trong cửa sổ terminal, gõ vào app sẽ báo lỗi. Cứ dán nguyên đoạn trên.

**Muốn kiểm tra máy đủ đồ chưa** (bất cứ lúc nào): nhắn *"kiểm tra máy đủ đồ chưa"*.

---

## Phần 3 — Dựng video đầu tiên

### Bước 1: đưa folder footage

Kéo-thả folder buổi quay vào khung chat (Windows tự dán đường dẫn), rồi gõ thêm mô tả ngắn. Ví dụ:

> *"Dựng video từ folder này. Hôm nay quay buổi bàn giao robot lau sàn MT1 tại nhà máy An Phát Xanh."*

Mô tả càng rõ (quay ở đâu, robot gì, có gì đặc biệt) thì kịch bản càng đúng ý.

### Bước 2: chọn kiểu dựng — nó sẽ hỏi bạn

| Kiểu | Khi nào chọn | Ra video thế nào |
|---|---|---|
| **Kiểu 1** | Footage **không có ai nói**, hoặc có nhưng không dùng lời | Cảnh đẹp + chữ đè + nhạc |
| **Kiểu 2** | Trong footage **đã có người nói sẵn** lúc quay | Dựng bám đúng lời người đó nói |
| **Kiểu 3** | Ghép nhiều cảnh rồi **thêm lời thuyết minh mới** | Có giọng đọc (người thật hoặc AI) |

Không chắc chọn gì thì cứ nói *"tôi không rõ, bạn xem footage rồi đề xuất giúp"*.

**Riêng Kiểu 1 nó sẽ hỏi thêm về nhạc** — đọc kỹ chỗ này:

- **Nhạc trend** (nhạc hot TikTok): bắt tai, dễ lên tương tác — nhưng **chỉ nên đăng Facebook page**. Đăng YouTube khả năng cao dính bản quyền, bị tắt tiếng hoặc chặn.
- **Nhạc không bản quyền**: đăng được mọi nền tảng, kể cả YouTube. An toàn tuyệt đối.

Định đăng đâu thì chọn loại đó. Cần cả hai thì bảo nó dựng 2 bản.

### Bước 3: duyệt kịch bản

Nó trình ra: mở đầu bằng cảnh gì, mạch cảnh ra sao, chữ đè viết gì, nhạc nào, dài bao nhiêu giây.

**Đọc kỹ rồi mới gật.** Sửa gì cứ nói thẳng — *"đổi câu mở đầu"*, *"bỏ cảnh số 3"*, *"làm ngắn lại còn 30 giây"*. Sửa xong nó dựng luôn theo ý mới.

### Bước 4: nhận hàng

Dựng xong nó tự mở folder **`Final`** nằm ngay trong folder buổi quay của bạn. Trong đó chỉ có 2 loại file:

- **`.mp4`** — video thành phẩm, đăng được ngay
- **`.md`** — bài caption của đúng video đó (10 gợi ý tiêu đề, bài đăng Facebook, hashtag, từ khoá YouTube)

Folder `Workspace` bên cạnh là đồ nghề của máy — **bạn không cần mở**.

---

## Phần 4 — Những câu hay dùng

| Bạn nhắn | Nó làm gì |
|---|---|
| *"kiểm tra máy đủ đồ chưa"* | In bảng trạng thái từng mục |
| *"có bản mới không"* | Kiểm tra GitHub, tự cập nhật |
| *"cập nhật kho tài nguyên"* | Tải nhạc/logo mới Sếp vừa thêm |
| *"từ giờ chữ hook đổi màu khác"* | Ghi nhớ thành quy tắc riêng của máy bạn |
| *"lưu key ElevenLabs này"* | Lưu key giọng đọc AI vào máy |

---

## Phần 5 — Vài điều nên biết trước

**Máy hỏi xin quyền vào thư mục** — lần đầu nó đụng vào một thư mục footage mới, Windows sẽ hiện hộp thoại. Chọn "luôn cho phép", chỉ hỏi 1 lần cho mỗi thư mục.

**Giọng đọc AI** (chỉ cần cho Kiểu 3) — chưa có key vẫn dựng bình thường bằng giọng miễn phí. Nhận được key từ quản trị qua Zalo thì nhắn *"lưu key ElevenLabs này: ..."*.

**Giọng AI đọc sai tên thương hiệu** — đây là hạn chế thật của mọi giọng máy hiện nay (BellaBot Pro dễ thành "Bella Popper"). Nên công cụ **cố tình không cho máy đọc tên sản phẩm**, mà đưa lên chữ trên màn hình. Đó là chủ ý, không phải lỗi.

**Video dựng ra không ưng?** Cứ nói thẳng chỗ nào chưa được — *"nhạc to quá"*, *"cảnh mở đầu chán"*, *"chữ nhỏ"*. Nó sửa và dựng lại. Nếu là quy tắc muốn áp dụng mãi về sau thì nói *"từ giờ nhớ là..."* — nó ghi vào bộ nhớ.

**Công cụ không tự nghĩ ra cảnh đẹp.** Nó chọn được cảnh đắt nhất trong những gì bạn quay được, nhưng không tạo ra thứ không có. Quay tốt vẫn là phần quan trọng nhất.

---

## Phần 6 — Gặp trục trặc

| Hiện tượng | Cách xử lý |
|---|---|
| Báo "không tìm thấy folder" | Kiểm lại đường dẫn, hoặc kéo-thả folder vào chat thay vì gõ tay |
| Cài xong vẫn không dùng được | Đóng app mở lại 1 lần |
| Sửa rồi mà video vẫn như cũ | Đóng/mở lại app — bản mới chỉ có hiệu lực sau khi khởi động lại |
| Máy chạy rất chậm | Nhắn *"kiểm tra máy đủ đồ chưa"* — xem có thiếu mục nào không |
| Cài lỗi giữa chừng | Dùng câu gỡ-cài-lại trong `README.md` |

Không tự xử được thì chụp màn hình gửi quản trị — **kèm nguyên văn dòng lỗi**, đừng chỉ nói "nó lỗi".

---

## Tóm tắt một dòng

Kéo folder quay vào → chọn kiểu dựng → duyệt kịch bản → lấy video + caption trong folder `Final`.

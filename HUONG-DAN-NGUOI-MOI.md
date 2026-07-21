# Hướng dẫn dùng công cụ dựng video Roboworld

Dành cho người mới, không cần biết kỹ thuật. Đọc hết mất khoảng 6 phút.

---

## Phần 1 — Công cụ này làm gì

Bạn đưa cho nó **folder footage một buổi quay** (đống video thô từ máy quay/điện thoại). Nó xem hết, nghe hết, đề xuất kịch bản cho bạn duyệt, rồi tự dựng ra **video ngắn dọc 9:16 hoàn chỉnh** — có chữ, nhạc, logo, hiệu ứng, tiếng động, outro — kèm sẵn **bài caption để đăng**.

Nó **không** thay bạn quyết định. Có đúng 2 lúc nó dừng lại hỏi: chọn kiểu dựng lúc đầu, và duyệt kịch bản trước khi dựng.

---

## Phần 2 — Cài đặt (làm 1 lần, ~10-20 phút)

**Điều kiện**: máy đã có app Claude Code và tài khoản còn hạn dùng.

Mở app Claude → vào mục **Code** → dán nguyên đoạn dưới đây rồi Enter:

```
Cài bộ công cụ dựng video Roboworld cho tôi: chạy qua Bash 2 lệnh 1) claude plugin marketplace add https://github.com/iold12pa/shorts-editor-rbw 2) claude plugin install shorts-editor-rbw@roboworld-tools — xong ĐỌC file ~/.claude/plugins/marketplaces/roboworld-tools/skills/shorts-editor-rbw/references/cai-dat-lan-dau.md và làm đúng theo file đó: cài tự động trọn bộ, báo tôi tiến độ và tổng thời gian ước tính.
```

Rồi **cứ để máy đấy làm việc khác**. Nó tự cài hết: bộ xử lý video, bộ nghe giọng nói tiếng Việt (~1.6 GB), kho logo/nhạc/hiệu ứng của công ty (~180 MB), các thư viện cần thiết, và dò card đồ hoạ để tăng tốc render.

Xong nó in ra **bảng trạng thái** đủ/thiếu từng mục. **Đóng app mở lại 1 lần** là dùng được.

> ⚠️ Đừng gõ thẳng `/plugin marketplace add ...` vào app — cú pháp đó chỉ chạy trong cửa sổ terminal, gõ vào app sẽ báo lỗi. Cứ dán nguyên đoạn trên.

**Muốn kiểm tra máy đủ đồ chưa** (bất cứ lúc nào): nhắn *"kiểm tra máy đủ đồ chưa"*.

### Nhập API key (làm sau khi cài xong)

Quản trị sẽ gửi bạn key qua Zalo. Nhắn với công cụ:

> *"nhập key"*

Một **cửa sổ nhỏ hiện lên** với các ô nhập. Dán key vào ô tương ứng, bấm **LƯU**. Xong.

> 🔒 **Đừng dán key thẳng vào khung chat.** Mọi thứ gõ vào chat đều đi qua máy chủ và nằm lại trong lịch sử hội thoại. Cửa sổ kia thì key đi thẳng vào máy bạn, không qua đâu cả. Ô nhập che dấu sao nên người ngồi cạnh cũng không đọc được.

Nhập xong nhắn *"kiểm tra máy đủ đồ chưa"* — nếu hiện **"đúng key chuẩn công ty"** là ổn. Nếu hiện **"SAI KEY"** thì bạn dán nhầm key, xin lại quản trị.

**Chưa có key vẫn dựng video bình thường** — chỉ là dùng giọng đọc miễn phí thay vì giọng cao cấp.

---

## Phần 3 — Dựng video đầu tiên

### Bước 1: đưa folder footage

Kéo-thả folder buổi quay vào khung chat (Windows tự dán đường dẫn), rồi gõ thêm mô tả ngắn:

> *"Dựng video từ folder này. Hôm nay quay buổi bàn giao robot lau sàn MT1 tại nhà máy An Phát Xanh."*

Mô tả càng rõ (quay ở đâu, robot gì, có gì đặc biệt) thì kịch bản càng đúng ý.

### Bước 2: chọn kiểu dựng — nó sẽ hỏi bạn

| Kiểu | Khi nào chọn | Ra video thế nào |
|---|---|---|
| **Kiểu 1** | Footage **không có ai nói**, hoặc có nhưng không dùng lời | Cảnh đẹp + chữ đè + nhạc |
| **Kiểu 2** | Trong footage **đã có người nói sẵn** lúc quay | Dựng bám đúng lời người đó nói |
| **Kiểu 3** | Ghép nhiều cảnh rồi **thêm lời thuyết minh mới** | Có giọng đọc (người thật hoặc AI) |

Không chắc chọn gì thì cứ nói *"tôi không rõ, bạn xem footage rồi đề xuất giúp"*.

### Bước 2b: mấy câu hỏi nó sẽ hỏi thêm

**Về nhạc** — quan trọng, đọc kỹ:

- **Nhạc trend** (nhạc hot TikTok): bắt tai, dễ lên tương tác — nhưng **chỉ nên đăng Facebook page**. Đăng YouTube khả năng cao dính bản quyền, bị tắt tiếng hoặc chặn.
- **Nhạc không bản quyền**: đăng được mọi nền tảng kể cả YouTube. An toàn tuyệt đối.

Định đăng đâu thì chọn loại đó. Cần cả hai thì bảo nó dựng 2 bản.

**Riêng video có người nói (Kiểu 2, Kiểu 3)** nó sẽ hỏi thêm: *giọng phủ cả bài hay chỉ 1-2 câu mở đầu?*

- **Dẫn xuyên suốt** → nhạc bắt buộc **không lời**. Lý do: hai giọng chồng nhau làm tai người nghe chia sự chú ý, lời dẫn bị nuốt — vặn nhỏ nhạc cũng không cứu được.
- **Chỉ 1-2 câu mở đầu** rồi để cảnh robot chạy → được dùng nhạc có lời, nhạc hot. Nhạc sẽ nhỏ lúc đang nói rồi dâng to dần lên đến hết.

**Về tiếng người nói** (Kiểu 2 và Kiểu 3 có giọng người thu) nó hỏi bạn muốn xử lý thế nào:

| Lựa chọn | Khi nào chọn |
|---|---|
| **Giữ nguyên** | Mặc định. Tiếng thu tốt rồi thì đừng đụng vào |
| **Lọc ồn** | Quay chỗ ồn — nhà máy, đường phố, quán đông |
| **Làm rõ giọng** | Tiếng nghe đục, nhỏ, thiếu rõ |
| **Cả hai** | Vừa ồn vừa đục |

Phân vân thì bảo *"cắt 4 bản cho tôi nghe thử"* — nó cắt 4 đoạn ngắn cùng độ to để bạn chọn bằng tai.

### Bước 3: duyệt kịch bản

Nó trình ra: mở đầu bằng cảnh gì, mạch cảnh ra sao, chữ đè viết gì, nhạc nào, dài bao nhiêu giây.

**Đọc kỹ rồi mới gật.** Sửa gì cứ nói thẳng — *"đổi câu mở đầu"*, *"bỏ cảnh số 3"*, *"làm ngắn còn 30 giây"*. Sửa xong nó dựng luôn theo ý mới.

### Bước 4: nhận hàng

Dựng xong nó tự mở folder **`Final`** nằm ngay trong folder buổi quay. Trong đó chỉ có 2 loại file:

- **`.mp4`** — video thành phẩm, đăng được ngay
- **`.md`** — bài caption của đúng video đó (10 gợi ý tiêu đề, bài đăng Facebook, hashtag, từ khoá YouTube)

Folder `Workspace` bên cạnh là đồ nghề của máy — **bạn không cần mở**.

---

## Phần 4 — Những câu hay dùng

| Bạn nhắn | Nó làm gì |
|---|---|
| *"kiểm tra máy đủ đồ chưa"* | In bảng trạng thái từng mục + kiểm key có đúng chuẩn không |
| *"nhập key"* | Mở cửa sổ để bạn dán API key |
| *"có bản mới không"* | Kiểm tra GitHub, tự cập nhật |
| *"cập nhật kho tài nguyên"* | Tải nhạc/logo mới quản trị vừa thêm |
| *"cắt 4 bản cho tôi nghe thử"* | Cắt mẫu tiếng để bạn chọn cách xử lý |
| *"từ giờ chữ hook đổi màu khác"* | Ghi nhớ thành quy tắc riêng của máy bạn |

---

## Phần 5 — Vài điều nên biết trước

**Máy hỏi xin quyền vào thư mục** — lần đầu đụng vào một thư mục footage mới, Windows sẽ hiện hộp thoại. Chọn "luôn cho phép", chỉ hỏi 1 lần cho mỗi thư mục.

**Giọng AI đọc sai tên thương hiệu** — hạn chế thật của mọi giọng máy hiện nay (BellaBot Pro dễ thành "Bella Popper"). Nên công cụ **cố tình không cho máy đọc tên sản phẩm**, mà đưa lên chữ trên màn hình. Đó là chủ ý, không phải lỗi.

**Tiếng quay quá xa thì không cứu được.** Nếu người nói đứng xa micro, mọi cách lọc đều vô ích — công cụ sẽ báo thẳng và khuyên bạn dùng cảnh khác. Đừng mất công bắt nó xử lý.

**Video dựng ra không ưng?** Cứ nói thẳng chỗ nào chưa được — *"nhạc to quá"*, *"cảnh mở đầu chán"*, *"chữ nhỏ"*. Nó sửa và dựng lại. Nếu là quy tắc muốn áp dụng mãi thì nói *"từ giờ nhớ là..."*.

**Công cụ không tự nghĩ ra cảnh đẹp.** Nó chọn được cảnh đắt nhất trong những gì bạn quay được, nhưng không tạo ra thứ không có. **Quay tốt vẫn là phần quan trọng nhất.**

---

## Phần 6 — Gặp trục trặc

| Hiện tượng | Cách xử lý |
|---|---|
| Báo "không tìm thấy folder" | Kéo-thả folder vào chat thay vì gõ tay đường dẫn |
| Cài xong vẫn không dùng được | Đóng app mở lại 1 lần |
| Sửa rồi mà video vẫn như cũ | Đóng/mở lại app — bản mới chỉ có hiệu lực sau khi khởi động lại |
| Bảng trạng thái báo **"SAI KEY"** | Bạn dán nhầm key. Xin lại quản trị rồi nhắn *"nhập key"* |
| Máy chạy rất chậm | Nhắn *"kiểm tra máy đủ đồ chưa"* — xem thiếu mục nào |
| Cài lỗi giữa chừng | Dùng câu gỡ-cài-lại trong `README.md` |

Không tự xử được thì chụp màn hình gửi quản trị — **kèm nguyên văn dòng lỗi**, đừng chỉ nói "nó lỗi".

---

## Tóm tắt một dòng

Kéo folder quay vào → chọn kiểu dựng → duyệt kịch bản → lấy video + caption trong folder `Final`.

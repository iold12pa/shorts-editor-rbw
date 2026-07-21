# Shorts Editor ROBOWORLD — gói cài cho đồng nghiệp

Skill Claude Code giúp dựng shorts video Roboworld tự động từ footage buổi quay, theo đúng phong cách công ty (học từ hàng chục video mẫu thật). Hỏi bạn chọn 1 trong 3 kiểu dựng, kiểm tra đủ nguyên liệu, đề xuất kịch bản cho duyệt, rồi tự dựng bằng ffmpeg.

> ### 👉 Người mới đọc file này trước: **[HUONG-DAN-NGUOI-MOI.md](HUONG-DAN-NGUOI-MOI.md)**
> Hướng dẫn cài + dùng cơ bản, viết cho người không rành kỹ thuật, đọc 5 phút.
> File README bạn đang đọc thiên về kỹ thuật và quy tắc bảo trì repo.

## Cài đặt (máy đã có Claude Code)

**Điều kiện trước khi bắt đầu**: đã cài Claude Code và có gói subscription (Sếp là người cấp/hướng dẫn nếu chưa có). Repo này ở chế độ **công khai (public)** — không cần tài khoản GitHub, không cần đăng nhập git.

**Cách cài — dán đúng 1 câu này vào app Claude (mục Code) rồi Enter. Cài TRỌN BỘ tự động (~10-20 phút tùy mạng, Claude tự báo tiến độ + thời gian từng mục):**

```
Cài bộ công cụ dựng video Roboworld cho tôi: chạy qua Bash 2 lệnh 1) claude plugin marketplace add https://github.com/iold12pa/shorts-editor-rbw 2) claude plugin install shorts-editor-rbw@roboworld-tools — xong ĐỌC file ~/.claude/plugins/marketplaces/roboworld-tools/skills/shorts-editor-rbw/references/cai-dat-lan-dau.md và làm đúng theo file đó: cài tự động trọn bộ, báo tôi tiến độ và tổng thời gian ước tính.
```

Claude sẽ tự cài đủ: plugin → FFmpeg (nếu thiếu) → bộ nghe giọng nói 1.6GB (tải ngầm) → kho logo/nhạc công ty ~180MB (tải ngầm) → dò card đồ họa (có card NVIDIA thì hỏi bạn 1 câu để tăng tốc render) → chốt bằng **bảng trạng thái từng mục** + báo tổng thời gian thật. Xong đóng/mở lại app 1 lần là dựng video được ngay.

**LƯU Ý**: đừng gõ trực tiếp `/plugin marketplace add ...` vào app Claude — cú pháp `/plugin` chỉ chạy trong cửa sổ terminal, gõ vào app sẽ báo "isn't available in this environment" (đã có người gặp thật). Cứ dán nguyên câu trên là Claude tự chạy đúng.

**Muốn kiểm tra máy đủ đồ chưa (bất cứ lúc nào về sau)**: nhắn *"kiểm tra máy đủ đồ chưa"* hoặc *"chuẩn bị công cụ dựng video"* — Claude rà lại từng mục và in bảng trạng thái.

## Lần đầu dựng video — lưới an toàn (nếu lúc cài có mục nào chưa xong)

Từ bản 17/07, mọi thứ dưới đây được cài NGAY lúc chạy câu cài đặt ở trên. Mục này là lưới an toàn: nếu máy nào cài kiểu cũ hoặc lúc cài lỡ thiếu mục nào, thì lần đầu tiên bạn nói "dựng video từ [folder]...", skill vẫn tự động:
1. **Tự cài FFmpeg** (bộ xử lý video, qua kho ứng dụng chính thức của Windows) nếu máy chưa có — không cần đóng/mở lại gì cả, skill tự tìm đường dẫn vừa cài và dùng ngay.
2. **Tự tải "bộ nghe giọng nói"** (model Whisper ~1.6GB — để Claude nghe được lời thoại tiếng Việt trong video) — tải nền, bạn cứ trả lời các câu hỏi dựng video song song. Lưu ở chỗ bền `~/.claude/roboworld-assets/` — sau này gỡ/cài lại plugin KHÔNG phải tải lại.
3. **Tự tải kho tài nguyên chung** (logo, outro, nhạc, hiệu ứng âm thanh, ảnh sản phẩm — từ Google Drive của Sếp) về cùng chỗ bền đó. Script tải tự kiểm đếm từng file, thiếu file nào báo đích danh file đó.
4. **Tự bật auto-update** — từ đó về sau chỉ cần thỉnh thoảng đóng/mở lại Claude Code là nhận bản mới nhất, không cần gõ lệnh gì.

## Kiểm tra sau khi cài (test nhanh)

1. **Xác nhận plugin đã cài**: nhắn "kiểm tra plugin shorts-editor-rbw đã cài chưa" — Claude chạy `claude plugin list` và báo kết quả.
2. **Test bằng 1 buổi quay nhỏ có thật**: nhắn *"dựng video từ [đường dẫn đầy đủ tới 1 folder buổi quay]"* (hoặc kéo-thả folder vào khung chat) — skill phải hỏi bạn chọn 1 trong 3 kiểu dựng (không tự đoán bừa) và liệt kê đúng tên các clip trong folder. Báo "không tìm thấy folder" → kiểm tra lại đường dẫn.
3. **Dựng thử 1 video hoàn chỉnh**: đi hết quy trình tới lúc có file `.mp4` — mở lên xem đúng khung dọc 9:16, có logo, không giật/lỗi hình là đạt.

## Giọng đọc AI (không bắt buộc — chỉ cần cho video có thuyết minh)

- **API key**: quản trị gửi riêng qua Zalo (không nằm trong gói cài vì repo public). Nhận được key thì nhắn Claude **"nhập key"** — một cửa sổ nhỏ hiện lên để bạn dán vào, key đi thẳng vào máy bạn. **Đừng dán key vào khung chat** (mọi thứ vào chat đều đi qua máy chủ và nằm lại trong lịch sử). Nhập xong nhắn *"kiểm tra máy đủ đồ chưa"* — hiện "đúng key chuẩn công ty" là ổn, hiện "SAI KEY" là dán nhầm.
- Chưa có key vẫn dựng video bình thường — giọng AI tự chuyển sang giọng miễn phí (edge-tts), chất lượng thấp hơn chút nhưng không lỗi.
- Vì key dùng chung cả team: đừng sinh giọng thử nghiệm tràn lan — mỗi video chỉ sinh giọng khi kịch bản đã được duyệt.

## Cập nhật phiên bản

**Bình thường bạn không phải làm gì** — từ bản 20/07, mỗi lần bạn nhờ dựng video, tool tự kiểm tra GitHub và tự kéo bản mới ngay đầu phiên. Nếu vừa có bản mới, nó báo bạn 1 câu và nhắc đóng/mở lại app.

**Cần chủ động kiểm** (vd Sếp báo "vừa có luật mới"): nhắn *"kiểm tra phiên bản tool"* hoặc *"có bản mới không"* — tool kiểm tra thật với GitHub, tự cập nhật, rồi báo mã bản cụ thể.

**Điều quan trọng cần biết**: Claude Code chỉ nạp plugin lúc **khởi động app**. Nên khi tool báo "vừa cập nhật", phiên đang mở vẫn chạy bản cũ — **đóng/mở lại app 1 lần** thì bản mới mới có hiệu lực. Đây không phải lỗi, là cách Claude Code hoạt động.

## Cài lỗi giữa chừng / cần gỡ-cài-lại? Dán 1 câu này

```
Cài lại bộ công cụ dựng video Roboworld cho tôi: chạy qua Bash 4 lệnh 1) claude plugin uninstall shorts-editor-rbw@roboworld-tools 2) claude plugin marketplace remove roboworld-tools 3) claude plugin marketplace add https://github.com/iold12pa/shorts-editor-rbw 4) claude plugin install shorts-editor-rbw@roboworld-tools — xong ĐỌC file ~/.claude/plugins/marketplaces/roboworld-tools/skills/shorts-editor-rbw/references/cai-dat-lan-dau.md và làm đúng theo file đó: cài tự động trọn bộ, báo tôi tiến độ và tổng thời gian ước tính.
```

Model Whisper + kho tài nguyên nằm ở chỗ bền `~/.claude/roboworld-assets/` nên KHÔNG bị mất khi gỡ-cài-lại — kịch bản cài sẽ thấy "có sẵn" và bỏ qua, chỉ mất ~1 phút.

## Quy tắc bảo trì repo (cho người/phiên Claude quản lý — người dùng thường bỏ qua mục này)

Mục tiêu tối thượng: **mọi bản cập nhật, kể cả nâng cấp lớn, máy đồng nghiệp chỉ cần update — KHÔNG BAO GIỜ phải gỡ-cài-lại nữa** (chỉ đạo của Huy 17/07/2026). Update chỉ gãy khi lịch sử git bị viết lại, và lý do duy nhất từng phải viết lại là file nặng lỡ nằm trong lịch sử. Vậy nên 3 luật cứng:

1. **Cấm commit file nặng/media vào repo** — mọi thứ nặng (nhạc, video, ảnh, model, zip) đi đường kho Google Drive. `.gitignore` đã chặn sẵn các đuôi media; máy quản lý có thêm hook `pre-push` tự chặn mọi file ≥5MB.
2. **Cấm force push / viết lại lịch sử / amend commit đã đẩy** — hook `pre-push` trên máy quản lý tự chặn. Trường hợp cực hiếm bắt buộc: hẹn trước mọi máy qua Zalo, tạm gỡ hook, đẩy, cài lại hook.
3. **Chỉ commit đích danh file, cấm `git add -A`** — tránh vô tình cuốn file rác/file nặng vào commit.

## Lưu ý quan trọng

- Đã xác nhận đầu-cuối với người dùng thật khác máy (2026-07-16, Cao Đắc Chiến) — cài qua chính app Claude, không cần mở terminal riêng.
- Mỗi lần dựng video, tự đưa đường dẫn đầy đủ tới folder buổi quay (không có bước cấu hình cố định lúc cài) — footage để ở ổ đĩa/thư mục nào cũng được.
- Lần đầu Claude thao tác vào 1 thư mục footage mới, Windows/Claude Code sẽ hiện hộp thoại xin quyền — chọn "luôn cho phép", chỉ hỏi 1 lần cho mỗi thư mục.

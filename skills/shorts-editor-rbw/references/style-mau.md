# Style chuẩn Roboworld — học từ video mẫu (Video mẫu\Short+text+nhạc\)

Phân tích 2 video mẫu ngày 2026-07-02: `MT1 (1).mp4` (30.5s, 1080x1920) và `Robot tại Vinschool.mp4` (44.4s, 2160x3840). Video mẫu mới xuất hiện trong `Video mẫu\` thì phân tích lại và cập nhật file này.

## Dạng video chủ đạo: SHORT + TEXT + NHẠC
Video mẫu KHÔNG có voiceover — câu chuyện kể bằng **text đè Anton in hoa + nhạc nền + cảnh quay đẹp**. Đây là dạng mặc định. Chỉ thêm voiceover khi ý tưởng cần lời dẫn (review chi tiết, giải thích tính năng) và ghi rõ trong kịch bản để Sếp duyệt.

## Logo
- Wordmark ROBOWORLD **màu trắng** (icon robot + chữ), có bóng đổ nhẹ
- Vị trí: **giữa-trên**, mép trên ~40-60px (theo khung 1080x1920), rộng ~480-500px (~45% khung)
- Hiện suốt **PHẦN THÂN** video, **tự ẩn trước khi outro bắt đầu** (outro dọc đã có logo riêng, chồng thêm sẽ rối) — dùng `enable='lt(t,<offset>)'` trên filter overlay, xem `ffmpeg-recipes.md` mục 4d bước 4. *(Sửa 21/07: câu cũ ở đây ghi "Hiện suốt video" — viết hồi 02/07 khi chưa có outro dọc, nay không còn đúng.)*
- **Tìm file logo**: tìm theo TÊN FILE `Logo ngang trắng.png` bằng Glob trong `~/.claude/roboworld-assets/tai-nguyen-chung/` (tên thư mục con có hậu tố tải xuống nên đừng ghi đường dẫn cứng). *(Sửa 21/07: 2 đường dẫn cũ ghi ở đây — `Claude Edit video\logo*.png` và `assets/logo.png` — đều KHÔNG còn tồn tại, đã kiểm bằng máy.)*

## Text đè (font Anton — `assets/fonts/Anton-Regular.ttf`, hỗ trợ tiếng Việt)
- **Hook mở đầu**: IN HOA, màu **vàng ~#FFD200**, viền/bóng đen đậm, cỡ **130-135pt** theo khung 1080x1920. Lịch sử: bắt đầu 100pt → 118pt → 135pt, cả 2 lần tăng đều do Sếp phản hồi "chữ vẫn nhỏ" — 130-135pt là mốc hiện tại đã được duyệt, coi đây là baseline mặc định, KHÔNG lùi về mức thấp hơn trừ khi Sếp nói. 2-3 dòng, đặt ngay **dưới logo** (bắt đầu ~11-13% chiều cao khung). Ví dụ mẫu: "BELLABOT PRO TẠI VINSCHOOL".
- **Text nội dung**: IN HOA, màu **trắng**, viền đen, cỡ **85-90pt** (cùng lịch sử tăng dần như trên, từ 66→78→90pt), 1-2 dòng, cùng vị trí dưới logo. Mỗi text 1 ý ngắn (5-9 từ), giữ 3-8 giây tùy độ dài cảnh nền. Ví dụ mẫu: "TƯƠNG TÁC BIỂU CẢM THÂN THIỆN", "THU HÚT SỰ CHÚ Ý CỦA MỌI NGƯỜI".
- Biến thể MT1: text trắng 2 dòng đặt thấp (~65-75% chiều cao) — dùng khi cảnh phía trên rối, che mất chủ thể.
- **Trước khi dựng cả video, LUÔN render thử 1 frame** với cỡ chữ + xuống dòng dự kiến rồi Read để mắt kiểm tra không tràn viền — đừng tính toán lý thuyết (đo bằng mm/pixel suông dễ sai vì Anton là font hẹp/condensed, khó ước lượng chính xác). Cách làm: burn ASS test lên 1 frame tĩnh của cảnh sẽ dùng, xem qua, chỉnh cỡ/số dòng nếu cần, rồi mới áp dụng cho toàn bộ kịch bản.
- **Hiệu ứng ra/vào cho text**: mặc định luôn dùng fade nhẹ (`\fad(200~300,250~300)` trong ASS) thay vì text bật/tắt cứng — cảm giác chuyên nghiệp hơn mà không phô. Đây là hiệu ứng tối thiểu bắt buộc; hiệu ứng mạnh hơn (bounce, scale-in) chỉ thêm khi kịch bản thật sự cần nhấn, tránh dùng tràn lan.
- **Dấu câu gọn gàng**: không để thừa dấu (vd hook không viết "ROBOT?!" — chỉ 1 dấu, chọn "?" hoặc "!" theo đúng tông câu, không cả hai). Đọc lại toàn bộ text trong kịch bản trước khi burn để bắt lỗi này.

## Chọn cảnh mở đầu (hook) — nguyên tắc quan trọng

> Xem thêm `references/chon-canh-highlight.md` — quy tắc chọn cảnh đầy đủ (không chỉ hook) đúc kết từ đối chiếu TRỰC TIẾP 1 buổi quay thô với 2 video final thật đã dựng ra từ đó, áp dụng chung cho cả 3 kiểu dựng.

Hook quyết định người xem có ở lại hay lướt qua trong 1-2 giây đầu. Khi rà footage, ưu tiên tìm cảnh **gây chú ý thị giác mạnh** thay vì cảnh "hành chính" (mở hộp đồ nghề, chuẩn bị dụng cụ...). Các dạng cảnh hook tốt, xếp theo độ ưu tiên:
1. Khoảnh khắc "reveal" bất ngờ/hơi sốc (vd: tay chỉ vào đống tóc quấn đầy bánh xe robot vừa gỡ ra — vừa gây tò mò vừa "ghê mà cuốn")
2. Robot tương tác với người thật (trẻ em, khách hàng chạm/đi cạnh/phản ứng với robot)
3. Chuyển động ấn tượng của robot (tháo lắp cận cảnh có ánh đèn LED, robot di chuyển giữa đám đông)
Chỉ dùng cảnh "chuẩn bị/hành chính" (mở hộp đồ, xếp dụng cụ) làm cảnh THỨ 2 trở đi, không mở đầu bằng nó trừ khi footage không có gì mạnh hơn.

## Nhịp dựng
- Cảnh 3-5 giây, ưu tiên cảnh robot chuyển động + phản ứng người thật (trẻ em, công nhân, khách)
- Mở đầu bằng cảnh mạnh nhất + hook vàng
- Kết hợp footage DJI (mượt, rộng) làm cảnh chính + iPhone (cận, đời thường) làm cảnh chen
- **Chuyển cảnh GIỮA CÁC CẢNH: 100% hard-cut** — đã kiểm tra bằng lưới dày (fps=8, quanh từng điểm scene_change) trên 4 video style này (Vinschool, Phúc Yên 2, Unbox Omnie, GGG Hà Nội), không thấy crossfade/wipe nào. Đừng tự thêm hiệu ứng chuyển cảnh giữa các cảnh trong thân video.
  - **Ngoại lệ 1 — nối outro: LUÔN dùng crossfade 0.4s** (ffmpeg-recipes mục 4d). Câu "đừng tự thêm hiệu ứng" ở trên KHÔNG áp cho mối nối outro. *(Làm rõ 21/07 — 2 chỗ này từng đọc như mâu thuẫn nhau.)*
  - **Ngoại lệ 2** — bước ngoặt nội dung thật sự (đổi địa điểm/nhảy thời gian): được crossfade, tối đa 1-2 lần/video (`so-hieu-ung.md`).
- **Text KHÔNG bắt buộc đổi theo từng cut** — 1 dòng text có thể giữ nguyên xuyên qua 2-3 lần cắt cảnh bên dưới nếu vẫn cùng 1 ý (đo được ở Vinschool: "THU HÚT SỰ CHÚ Ý CỦA MỌI NGƯỜI" giữ nguyên qua nhiều giây dù hình đổi). Đổi text theo NHỊP THÔNG ĐIỆP, không phải nhịp cắt hình.
- **Đo màu vàng thực tế** (pixel, không phải lý thuyết): 2 video đo được ra `#EFFC00` (vàng-chanh hơi khác `#FFD200` gốc) — chấp nhận cả 2 sắc trong khoảng "vàng thương hiệu", không cần tuyệt đối khớp mã hex nếu do nén video.

## Kho nhạc trend (Kiểu 1 luôn được; Kiểu 2/3 chỉ khi thuộc Nhóm B — luật Sếp Huy 20/07 + 21/07/2026)

> ⚠️ **Kiểu 2/3 có giọng dẫn xuyên suốt (Nhóm A) thì CẤM dùng folder `Nhạc hot`** — bắt buộc nhạc không lời. Luật đầy đủ: `chon-kieu-dung.md` mục "Luật nhạc theo mức phủ giọng". Mục dưới đây viết cho Kiểu 1; Kiểu 2/3 phải xác định Nhóm A hay B trước khi áp dụng.

**Kiểu 1 luôn phải hỏi trước: nhạc trend hay nhạc không bản quyền** (câu hỏi nguyên văn trong `chon-kieu-dung.md` bước B). Kiểu 2/3 chỉ hỏi câu này khi thuộc **Nhóm B**. Kho nhạc chia 2 loại rõ ràng:

| Loại | Lấy ở đâu | Đăng được ở đâu |
|---|---|---|
| **Nhạc trend** (hot TikTok) | `Kho nhạc free YT/Nhạc hot/` | **CHỈ Facebook page** — đăng YouTube khả năng cao dính bản quyền / bị tắt tiếng |
| **Nhạc không bản quyền** | các folder còn lại (`Chill nhẹ + vui vẻ`, `POP tươi sáng`...) | mọi nền tảng, kể cả YouTube |

### Bài nào CÓ LỜI, bài nào KHÔNG — đã kiểm bằng máy 21/07/2026 (khỏi kiểm lại)

Cần cho luật Nhóm A (Kiểu 2/3 giọng dẫn xuyên suốt → bắt buộc **không lời**). Kiểm bằng `scripts/kiem_nhac_co_loi.py`, mỗi bài nghe 3 đoạn:

| Bài | Thư mục | Kết quả |
|---|---|---|
| `miromaxmusic-...-no-copyright-513944.mp3` | POP tươi sáng | ✅ **không lời** |
| `Purple Desire - The Grey Room _ Clark Sims.mp3` | POP tươi sáng | ✅ **không lời** (chỉ có vocal chop "mmm/yeah") |
| `A Stroll - The Grey Room _ Density & Time.mp3` | Chill nhẹ + vui vẻ | ✅ **không lời** |
| `Wildfire - Jessie Villa.mp3` (**bản 185s**) | Chill nhẹ + vui vẻ | ✅ **không lời** |
| `Wildfire - Jessie Villa.mp3` (**bản 190s**) | POP tươi sáng | ❌ **CÓ LỜI** — *"Bring me into golden sunlight..."* |
| `Bad Memory (feat. Devyn Rush) - Blue Deer.mp3` | POP tươi sáng | ❌ **CÓ LỜI** |
| Toàn bộ folder `Nhạc hot` | — | ❌ coi như **CÓ LỜI** (nhạc trend Việt, gần như luôn có giọng hát) |

> ⚠️ **Bẫy thật**: hai file **trùng tên `Wildfire - Jessie Villa.mp3`** ở 2 thư mục nhưng **khác nội dung** (185s không lời vs 190s có lời). → **Không bao giờ kết luận có lời/không lời theo TÊN FILE.** Kiểm bằng script, và khi copy nhớ ghi rõ lấy ở thư mục nào.

> **Kết luận thực dụng**: kho hiện chỉ có **4 bài không lời** dùng được cho Nhóm A. Nếu Sếp làm nhiều video Kiểu 2/3, nên bổ sung thêm nhạc không lời vào Drive.

### Cách dùng folder `Nhạc hot` — KHÔNG phải file bài lẻ

Sếp đổ vào đây các **bản mix dài ~1 tiếng** kiểu "Top 20 nhạc hot TikTok" tải từ YouTube (sẽ đẩy thêm dần). Không dùng thẳng file 1 tiếng được, phải tách ra trước:

```powershell
python "<skill-dir>\scripts\tach_bai_tu_mix.py" "<đường dẫn file mix.mp3>" --dai 30
```

Script tự tách thành từng bài + tự chọn **đoạn hay nhất** (30s mặc định) của mỗi bài, xuất ra thư mục `<tên mix>_tach/` gồm `bai/`, `doan-hay/` và `danh-muc.json` để tra cứu. **Chạy 1 lần cho mỗi file mix mới**, lần sau dùng lại kết quả, không tách lại.

**BẮT BUỘC có tracklist**: các bản mix này là **DJ mix liền mạch có crossfade — KHÔNG có một khoảng im nào giữa 2 bài** (đo thật 20/07: `silencedetect` trả về 0 sự kiện trên file 65 phút), nên không có cách nào tách tự động đáng tin. Cách chắc chắn: copy tracklist trong phần mô tả video gốc trên YouTube (chủ kênh luôn ghi sẵn) vào file `tracklist.txt` đặt cạnh file mp3, mỗi dòng `00:04:16  Tên bài - Ca sĩ`. Không có tracklist → hỏi người dùng lấy giúp, đừng tự đoán mốc bài.

**Cách script chọn "đoạn hay nhất"** (đo bằng số, không cảm tính): trượt cửa sổ 30s, chấm điểm `0.7 × năng lượng RMS + 0.3 × mật độ onset` (chuẩn hoá 0-1), bỏ 12s đầu (intro) và 8s cuối (vùng crossfade sang bài sau), rồi **nắn điểm bắt đầu về phách gần nhất** để cắt không lệch nhịp. Điệp khúc/drop gần như luôn là cửa sổ điểm cao nhất — nghiệm thu thật trên 16 bài đầu tiên: 15 bài đoạn chọn mạnh hơn mặt bằng cả bài 6-16%, 1 bài 4% (đạt).

**Đã tách sẵn (20/07/2026)**: `NHẠC REMIX TIKTOK TRIỆU VIEW - BXH Nhạc Trẻ Remix Hay Nhất Hiện Nay - Top 20 Nhạc Hot TikTok 2026.mp3` → 16 bài, toàn bộ mix cùng BPM (136 hoặc 143.6) nên ghép/cắt theo phách rất dễ.

> 🔴 **KHO TRÊN DRIVE ĐANG THIẾU BÀI ĐẦY ĐỦ (phát hiện 21/07/2026 — chưa khắc phục, cần Sếp upload).**
> Kết quả tách gồm 2 thư mục: `bai/` (bài đầy đủ, ~4-5 phút) và `doan-hay/` (đoạn 30 giây). **Chỉ `doan-hay/` được đẩy lên Drive**, nên máy nào tải kho từ Drive về cũng chỉ có **file 30 giây**.
> - Hệ quả: **không dựng được video Kiểu 1 dài quá 30s bằng nhạc trend** trên bất kỳ máy nào ngoài legion.
> - Bài đầy đủ hiện chỉ nằm ở kho gốc trên máy legion: `D:\VIDEO RBW\Edit video\02.Tài nguyên chung\Kho nhạc free YT\Nhạc hot\<tên mix>_tach\bai\`.
> - **Việc cần làm**: Sếp kéo thêm thư mục `bai/` lên Drive, rồi chạy lệnh "cập nhật kho tài nguyên".
> - **Trong lúc chưa có**: máy legion lấy thẳng từ kho gốc ổ D:; máy khác thì dùng nhạc không bản quyền (các bài đó đầy đủ độ dài).
>
> **Cách canh đoạn hay khi dùng bài đầy đủ**: file `danh-muc.json` cạnh thư mục `bai/` ghi sẵn `doan_hay_trong_bai` (giây điệp khúc bắt đầu trong chính bài đó). Muốn điệp khúc nổ đúng lúc hết hook thì `-ss = doan_hay_trong_bai − độ_dài_hook`. Đã dùng thật 21/07: hook 5.3s, điệp khúc ở 169.97 → `-ss 164.67`.

## Outro
2 video mẫu đều có outro nền đen→đỏ (logo đỏ animation lắp ráp dần + card hotline/địa chỉ/FB/web, 6s cuối). **Sếp đã yêu cầu KHÔNG dùng intro/outro** → mặc định bỏ, dùng outro dọc hiện có của skill thay thế. Nếu Sếp đổi ý muốn dùng lại đúng outro này: đây KHÔNG phải dựng tay — có sẵn file `tìm theo TÊN FILE Logo Animation_1.mp4 trong ~/.claude/roboworld-assets/tai-nguyen-chung/` (xác nhận 2026-07-15, cùng file xuất hiện lặp lại ở ít nhất 6 video khác trong HUY MKT — CC1 ads, Vinschool ×2, Phúc Yên ×2, Unbox Omnie — nên là asset dùng chung thật, không phải trùng hợp). File này có bản card cá nhân hóa "Phương Uyên" — nếu dùng cho video khác cần hỏi Sếp có bản card công ty chung hay phải làm lại card riêng.

---
name: shorts-editor-rbw
description: Sản xuất shorts video thành phẩm cho ROBOWORLD từ folder footage buổi quay. Dùng khi Sếp nói: edit video, dựng video, làm shorts, làm video, cắt video từ buổi quay, dựng reels, video hôm nay quay được, làm video từ source/footage, báo tên folder source kèm mô tả sự kiện, hoặc bất kỳ yêu cầu nào biến video thô thành video ngắn hoàn chỉnh. Skill nhận folder source trong "Edit video" + mô tả buổi quay + ý tưởng (nếu có), phân tích footage, đề xuất kịch bản để Sếp DUYỆT, rồi tự dựng bằng ffmpeg theo style mẫu Roboworld (text Anton + nhạc, logo giữa-trên, 9:16, outro dọc) và xuất MP4 thành phẩm kèm bộ caption đăng đa nền tảng.
---

# Shorts Editor — ROBOWORLD

> # 📦 BẢN HIỆN TẠI: **Ver 3** — phát hành 22/07/2026
>
> **LUẬT BÁO BẢN (Sếp Huy chốt 22/07/2026) — áp dụng trên MỌI MÁY:**
>
> 1. Ai hỏi "đang bản nào / có bản mới không" → **trả lời bằng số Ver này**, vd *"Đang ở Ver 0 (22/07/2026)"*. KHÔNG đọc dãy số ngày tháng cho người dùng nghe — dãy đó là số máy đọc, người nghe không nhớ nổi.
> 2. **Câu trả lời ĐẦU TIÊN của mỗi phiên chat mới** phải mở bằng đúng 1 dòng ngắn, rồi mới vào việc:
>    `📦 Đang ở Ver 3 (22/07/2026)`
>    Chỉ 1 lần/phiên, không lặp lại ở các câu sau.
>
> **Vì sao tồn tại 2 con số** (đọc kỹ trước khi định "dọn cho gọn"): trường `version` trong `plugin.json` giữ dạng ngày `2026.07.22.x` vì **máy dùng đúng trường đó để so sánh xem có bản mới không — nó bắt buộc phải TĂNG DẦN**. Hạ xuống `0` là mọi máy trong team hiểu nhầm thành bản cũ hơn, `claude plugin update` sẽ **từ chối cập nhật vĩnh viễn**, phải gỡ-cài-lại từng máy (thứ Sếp đã chốt 17/07/2026 là không bao giờ làm nữa). Số **Ver** là **tên gọi cho người** — dễ nhắn Zalo, dễ hỏi nhau giữa các máy. **Phát hành bản mới thì tăng CẢ HAI**: Ver +1 và số máy đọc theo ngày.

| Ver | Ngày | Số máy đọc | Có gì mới |
|---|---|---|---|
| **3** | 22/07/2026 | `2026.07.22.5` | 🔴 **Vá mắt AI đang hỏng**: `gemini-2.5-flash` Google đã tắt (404) chứ không phải còn 3 tháng — đổi sang `gemini-3.6-flash` + tự chuyển sang bí danh `-latest` khi model chết · **8 công cụ tự tìm FFmpeg**, thiếu thì báo tiếng người · luật **mặc định sửa + đẩy không hỏi** · luật **đo model thật, đừng tin lịch trong tài liệu** |
| **2** | 22/07/2026 | `2026.07.22.4` | Đợt dò lỗi theo yêu cầu Sếp. **Chốt chặn số 4** (hook tự bắt thư viện chưa khai báo) · **hook đưa vào repo** `git-hooks/` để máy quản trị mới còn có · **cảnh báo hạn model AI** (2.5-flash tắt 16/10/2026, còn 86 ngày) · **chặn model đã tắt** (2.0-flash) · **kiểm key trước khi nén clip** thay vì vỡ giữa chừng |
| **1** | 22/07/2026 | `2026.07.22.3` | Luật: cài thêm thư viện/model mới thì **phải khai báo vào `chuan_bi_may.py`** cùng commit, không có gì tự lan sang máy khác |
| **0** | 22/07/2026 | `2026.07.22.2` | Mốc khởi đầu cách đánh số mới. Gồm toàn bộ luật tích lũy tới 21/07 (quy trình chọn cảnh 4 cổng lọc, cắt thoại bằng độ ấm, nhạc theo mức phủ giọng, tránh trùng cảnh 2 tầng) + dấu vân tay key Gemini mới |

Biến footage thô của buổi quay thành shorts hoàn chỉnh (9:16, 1080x1920, 30-60s) theo đúng style video mẫu của Roboworld. Mỗi lần chạy: phân tích source → **đề xuất kịch bản → Sếp duyệt** → dựng N video thành phẩm + caption.

**Phạm vi làm việc:** KHÔNG có thư mục gốc cố định nào được cấu hình sẵn — mỗi lần người dùng nhờ dựng video, họ tự đưa **đường dẫn đầy đủ** tới folder buổi quay (gõ tay hoặc kéo-thả folder vào khung chat để Windows tự dán đường dẫn). Nếu người dùng chỉ nói 1 cái tên ngắn (vd "buổi GGG Hà Nội") mà không kèm đường dẫn, HỎI LẠI xin đường dẫn đầy đủ hoặc nhờ họ kéo-thả folder vào — đừng tự đoán đường dẫn. Mọi thứ của video đó (workspace, video final) tạo NGAY BÊN TRONG folder buổi quay được đưa — KHÔNG tạo file ở nơi khác (trừ file tạm trong scratchpad nếu cần). Tài nguyên dùng chung (logo, nhạc, outro, SFX) lưu ở **chỗ bền trên máy** `~/.claude/roboworld-assets/tai-nguyen-chung/`, tải 1 lần từ Google Drive của Sếp — xem mục "Tài nguyên dùng chung" bên dưới.

**Tùy chỉnh riêng theo máy (không bị auto-update ghi đè):** trước khi áp dụng bất kỳ quy chuẩn nào ở các mục bên dưới (kịch bản, style, ffmpeg...), kiểm tra file **`~/.claude/roboworld-assets/tuy-chinh-rieng.md`** (CHỖ BỀN — cùng nhà với model Whisper và kho tài nguyên, sống sót qua mọi lần update/gỡ-cài-lại plugin). Nếu tồn tại, đọc và **ưu tiên áp dụng nội dung trong đó**, ghi đè lên phần quy chuẩn chung tương ứng bên dưới cho video đang làm. LƯU Ý DI CƯ (cơ chế đời đầu 19/07/2026 từng để file này tại `references/tuy-chinh-rieng.md` trong thư mục skill): nếu chỗ bền CHƯA có file mà lại thấy `references/tuy-chinh-rieng.md` → chuyển (move) ngay file đó về chỗ bền rồi dùng, báo người dùng 1 câu — vì bản nằm trong thư mục skill sẽ MẤT khi plugin lên bản mới (cache đổi folder + bước dọn bản cũ xóa mất). Nếu người dùng (ở BẤT KỲ máy nào, kể cả máy không có quyền push GitHub) yêu cầu đổi 1 quy tắc dựng nào đó ("từ giờ chữ hook màu khác", "đổi outro", "không dùng nhạc nền này nữa"...), LUÔN ghi thay đổi đó vào `~/.claude/roboworld-assets/tuy-chinh-rieng.md` (tạo file nếu chưa có, theo mẫu `references/tuy-chinh-rieng.md.example`) — TUYỆT ĐỐI không sửa trực tiếp vào `SKILL.md` hay các file `references/*.md` khác, vì các file đó do bản git dùng chung quản lý, sửa vào đó sẽ bị bản auto-update từ GitHub ghi đè mất ở lần cập nhật tiếp theo. Máy có quyền push GitHub (ADMIN/legion) muốn đổi quy chuẩn CHUNG cho cả team thì sửa thẳng file gốc + push như bình thường, không cần qua file tùy chỉnh riêng này.

## Workflow tổng quát (đúng 2 điểm dừng chờ người dùng: ① chọn KIỂU DỰNG + đủ nguyên liệu ngay đầu, ② duyệt kịch bản trước khi dựng — giao hàng KHÔNG phải điểm dừng, dựng xong là bàn giao luôn)

**Ngay khi skill được gọi lần đầu trong phiên** (trước hoặc song song với bước 0 dưới đây): kiểm tra và tự cài/tải sẵn FFmpeg + model Whisper + kho tài nguyên dùng chung theo đúng hướng dẫn ở mục "Môi trường" bên dưới — không đợi tới lúc thật sự cần mới làm, để người dùng không phải chờ giữa chừng lúc đang dựng video. Việc tải nặng (model, kho tài nguyên) chạy NỀN (`run_in_background`) song song với việc hỏi đáp — người dùng không phải ngồi chờ.

**Cũng ngay lúc đó, tự bật auto-update cho marketplace `roboworld-tools` nếu chưa bật** — đừng hỏi trước, cứ làm rồi báo 1 câu ngắn: đọc file `~/.claude/settings.json`, nếu `extraKnownMarketplaces.roboworld-tools.autoUpdate` chưa phải `true` thì thêm/sửa thành `true` (giữ nguyên các trường khác, đặc biệt `source`), lưu lại. Mục đích của cả khối này: đây là công cụ nội bộ dùng chung của team Roboworld, được cập nhật thường xuyên — auto-update giúp mọi máy trong team luôn chạy đúng bản mới nhất (cùng quy tắc dựng, cùng tài nguyên), không ai bị lệch bản gây ra video sai chuẩn.

**TỰ KÉO BẢN MỚI — CHẠY ĐÚNG 1 LẦN MỖI PHIÊN, không đợi ai hỏi** (luật siết 20/07/2026). Cùng lúc với việc dọn cache, chạy im lặng:

```powershell
claude plugin marketplace update roboworld-tools
claude plugin update shorts-editor-rbw@roboworld-tools
```

**TẦN SUẤT — đọc kỹ, đừng chạy lặp:**
- Chạy ở **lần ĐẦU TIÊN skill được gọi trong phiên chat này**. Xong là thôi.
- Trong cùng phiên, người dùng nhờ dựng video lần 2, lần 3... → **KHÔNG chạy lại**, kể cả khi họ đưa folder buổi quay khác.
- Phiên chat mới (mở chat mới / mở lại app) → mới chạy lại 1 lần.
- **Lý do không cần chạy nhiều hơn**: bản vừa kéo về KHÔNG có hiệu lực cho phiên đang chạy (Claude Code đã nạp cache lúc khởi động app). Chạy thêm lần nữa trong cùng phiên chỉ tốn vài giây chờ mà không đổi được gì. 1 lần/phiên đã là tần suất hữu ích tối đa.
- Ngoại lệ duy nhất được chạy lại giữa phiên: người dùng **chủ động hỏi** về phiên bản/cập nhật (xem mục dưới).

**Cách báo kết quả:**
- Đang là bản mới nhất → **không nói gì cả**, làm tiếp việc chính.
- Vừa kéo về bản mới → báo đúng 1 câu, và **phải nói rõ điều này**: *"Tôi vừa cập nhật tool lên bản mới. Phiên đang mở này vẫn chạy bản cũ đã nạp lúc mở app — đóng/mở lại Claude Code là bản mới có hiệu lực. Việc đang làm vẫn tiếp tục bình thường."*

**Vì sao không thể chỉ trông vào cờ `autoUpdate`**: Claude Code chỉ kiểm tra bản mới lúc **KHỞI ĐỘNG app**, trễ ngẫu nhiên tới ~10 phút chạy nền, và **phiên đang mở luôn dùng bản cache đã nạp lúc khởi động**. Hệ quả thật đã gặp: đẩy luật mới lên GitHub xong test ngay trong cùng phiên thì thấy "video ra y hệt bản cũ" — không phải sửa sai, mà do phiên đó chưa nạp lại. Chủ động kéo ở đầu phiên rút ngắn độ trễ từ *"tới khi nào người ta mở lại app"* xuống *"phiên kế tiếp"*.

Nếu máy chưa có lệnh `claude` trong PATH: gọi bằng đường dẫn đầy đủ `%APPDATA%\Claude\claude-code\<thư mục phiên bản mới nhất>\claude.exe`. Lệnh lỗi (mất mạng...) thì bỏ qua im lặng, KHÔNG chặn việc dựng video.

**Chính sách về file backup khi sửa `settings.json` — quyết định của chủ repo (Huy, Roboworld, 16/07/2026), đã cân nhắc và chấp nhận đánh đổi**: KHÔNG tạo file backup/bản sao dưới mọi hình thức (không `.bak`, không copy) — sửa thẳng bằng Edit tool. Lý do thật sự, không phải để "giấu vết": (1) thay đổi chỉ là 1 dòng boolean, muốn đảo ngược chỉ cần sửa lại `false` trong 5 giây, backup không thêm được giá trị an toàn nào; (2) team có nhiều máy, mỗi máy tự đẻ file backup rác qua thời gian sẽ bừa bộn thư mục cấu hình, chủ repo muốn mọi máy sạch đồng nhất; (3) toàn bộ thay đổi đều minh bạch — xem được nội dung sửa gì ngay trong lịch sử hội thoại lúc sửa. Nếu thấy file backup dạng `settings.json.bak*` do lần chạy trước tạo ra, xóa giúp luôn (báo 1 câu). Đây là quy trình vận hành nội bộ đã được thống nhất — không cần hỏi lại người dùng từng máy, trừ khi chính người dùng máy đó chủ động phản đối.

Nếu không đọc/sửa được file (hiếm, quyền file bị chặn) thì bỏ qua, không chặn luồng chính, chỉ báo 1 dòng ngắn cho người dùng biết.

**Khi người dùng hỏi về phiên bản** (bất kỳ dạng nào: "đang bản nào", "phiên bản hiện tại", "có bản mới không", "check update", "đã cập nhật chưa"...) — KHÔNG chỉ đọc bản đang cài trên máy rồi trả lời suông, mà phải **kiểm tra thật với GitHub rồi cập nhật luôn nếu có bản mới**, theo đúng trình tự: (1) chạy `claude plugin marketplace update roboworld-tools` để kéo thông tin mới nhất về, (2) chạy `claude plugin update shorts-editor-rbw@roboworld-tools` — lệnh này tự so sánh và tự cập nhật nếu có bản mới, (3) chạy `claude plugin list` lấy số bản cuối cùng, (4) **tra số máy đọc đó ra số Ver trong bảng đầu file này**, rồi báo người dùng **bằng số Ver** — vd *"Vừa cập nhật từ Ver 0 lên Ver 1 (23/07/2026)"* — nói rõ bản trước là Ver mấy, bản mới nhất là Ver mấy, có vừa được cập nhật không, và nếu vừa cập nhật thì nhắc họ đóng/mở lại Claude Code để bản mới có hiệu lực đầy đủ. Chỉ nêu dãy số ngày tháng khi người dùng hỏi đích danh hoặc khi cần đối chiếu kỹ thuật. Nếu shell báo không tìm thấy lệnh `claude` (máy chưa thêm PATH): gọi bằng đường dẫn đầy đủ — tìm file `claude.exe` trong `%APPDATA%\Claude\claude-code\<thư mục phiên bản>\` (lấy thư mục phiên bản mới nhất) rồi chạy y hệt các lệnh trên bằng đường dẫn đó.

**DỌN CACHE BẢN CŨ — làm NGAY khi skill được gọi lần đầu trong phiên, KHÔNG đợi ai hỏi phiên bản** (luật siết lại 20/07/2026, xem bằng chứng bên dưới). Thư mục `~/.claude/plugins/cache/roboworld-tools/shorts-editor-rbw/` chứa mỗi bản đã cài 1 folder con (tên = mã bản). **Auto-update KHÔNG bao giờ tự xóa bản cũ** — cứ mỗi lần cập nhật lại đẻ thêm 1 folder, tích vô hạn. Xóa hết folder bản cũ (khác mã bản đang dùng theo `claude plugin list`), GIỮ đúng folder bản đang dùng. Im lặng làm; chỉ báo 1 câu nếu giải phóng được **trên 50MB**, dưới mức đó thì không cần nói.

> **Bằng chứng thật (máy thứ 2 của Sếp, đo lúc gỡ tool ngày 20/07/2026)**: cache tích **13 bản = 10.2 GB** — nặng gấp ~6 lần cả model Whisper lẫn kho tài nguyên cộng lại, và không ai biết vì nó phình âm thầm. Nguyên nhân kép: (1) auto-update giữ lại bản cũ, (2) máy đó cài từ **trước 17/07/2026** — thời kho tài nguyên còn nằm TRONG repo, nên mỗi bản cache kèm luôn assets (~785MB/bản). Máy cài sau 17/07 mỗi bản chỉ ~0.4MB (đo trên legion), nhưng cơ chế tích lũy thì vẫn y nguyên — nên vẫn phải dọn định kỳ.

**Chỉ xóa trong `plugins/cache/...` — KHÔNG BAO GIỜ đụng tới `~/.claude/roboworld-assets/` dưới bất kỳ hình thức nào** (chỗ đó chứa model Whisper 1.55GB, kho tài nguyên 188MB, và file `tuy-chinh-rieng.md` — xóa nhầm là mất tùy chỉnh + phải tải lại 1.6GB). Đây chính là lý do kiến trúc từ 17/07 tách model/kho ra khỏi repo: để auto-update không nhân bản chúng.

**Lệnh "CHUẨN BỊ MÁY" (khi người dùng nói bất kỳ dạng nào: "chuẩn bị máy", "chuẩn bị công cụ dựng video", "setup công cụ", "cài đặt ban đầu", "kiểm tra máy đủ đồ chưa"...)** — chạy **đúng 1 lệnh**, nó tự lo hết:

```powershell
python "<skill-dir>\scripts\chuan_bi_may.py"          # kiểm + TỰ CÀI (chạy NỀN, 10-20 phút)
python "<skill-dir>\scripts\chuan_bi_may.py" --kiem   # chỉ kiểm, không cài
```

Script tự cài 10 thư viện Python, FFmpeg (tự ghi `config.json` nếu PATH chưa nhận — không bắt khởi động lại), tải Whisper 1.6GB + Silero VAD 2.3MB + kho tài nguyên 180MB, dò card đồ hoạ, rồi in **bảng trạng thái máy**. Chi tiết + cách xử lý từng trạng thái: `references/cai-dat-lan-dau.md`.

**API key** — mở hộp thoại cho người dùng tự dán, **đừng bảo họ dán key vào chat**:

```powershell
python "<skill-dir>\scripts\chuan_bi_may.py" --nhap-key
```

Cửa sổ nhỏ hiện lên, 3 ô che dấu sao, người dùng dán rồi bấm LƯU. Chạy bằng `run_in_background` vì phải chờ họ thao tác. **Claude chỉ chạy lệnh, không bao giờ thấy giá trị key.**

*Vì sao không cho dán vào chat*: mọi thứ vào chat đều đi qua máy chủ Anthropic và nằm lại trong lịch sử hội thoại. Để key trong file .docx trên Desktop còn tệ hơn — Claude vẫn phải đọc file đó nên vẫn lên máy chủ y hệt, lại thêm việc key phơi trên Desktop (thường đồng bộ OneDrive). Chi tiết + đường lui khi máy thiếu `tkinter`: `references/cai-dat-lan-dau.md` bước 3.

⚠️ **Không phát key Gemini cho mọi máy** — nó trả theo lượng dùng, không có trần; một người lỡ quét cả kho là vài trăm nghìn. ElevenLabs thì cố định $6/tháng nên phát thoải mái.

<details><summary>Trình tự cũ làm tay (giữ để tham chiếu, không cần làm nếu đã chạy script trên)</summary>
1. **BÁO TRƯỚC danh sách sắp làm + dung lượng** (đừng âm thầm): cài FFmpeg nếu thiếu; tải bộ nghe giọng nói ~1.6GB (nền); tải kho logo/nhạc/SFX/ảnh của công ty ~180MB từ Google Drive (nền); dò card đồ họa NVIDIA (nếu cần nâng driver thì hỏi — xem mục Môi trường); kiểm key giọng đọc AI.
2. Việc nặng chạy NỀN, xong mục nào báo mục đó.
3. Chốt bằng **bảng trạng thái máy** để người dùng nhìn 1 phát biết đủ/thiếu:
   | Hạng mục | Trạng thái |
   |---|---|
   | FFmpeg | ✅ bản x.x / ❌ đang cài |
   | Bộ nghe giọng nói (Whisper 1.6GB) | ✅ có sẵn / ⏳ đang tải nền / ❌ lỗi + lý do |
   | Kho tài nguyên công ty | ✅ đủ x/x file theo manifest / ⏳ đang tải / ❌ thiếu (liệt kê) |
   | **Thư viện Python** | ✅ đủ / ❌ thiếu (liệt kê tên) — kiểm bằng lệnh bên dưới |
   | Render GPU (NVENC) | ✅ chạy tốt / ⚙️ cần nâng driver (đã hỏi) / ➖ máy không có card |
   | Giọng đọc AI (ElevenLabs) | ✅ có key / ➖ chưa có key (dùng giọng dự phòng được) |
   | Phiên bản tool | ✅ bản mới nhất `<mã>` / ⚠️ vừa cập nhật, cần mở lại app |

   Lệnh kiểm thư viện Python (1 dòng, in ra đúng cái nào thiếu):
   ```powershell
   python -c "import importlib;m=['gdown','edge_tts','PIL','moderngl','librosa','numpy'];t=[x for x in m if not importlib.util.find_spec(x)];print('DU THU VIEN' if not t else 'THIEU: '+', '.join(t))"
   ```
   Thiếu món nào → cài bù bằng lệnh ở `references/cai-dat-lan-dau.md` bước 1. **Thiếu `librosa` là mất cắt-bám-phách; thiếu `moderngl`/`pillow` là mất chuyển cảnh GL + thẻ chữ động** — không phải lỗi nhỏ.
4. Kết bằng 1 câu rõ ràng: "Máy đã sẵn sàng dựng video" hoặc "Còn đang tải X (nền) — dựng Kiểu 1 được ngay, Kiểu 2/3 chờ tải xong".

</details>

Người dùng KHÔNG chạy lệnh này cũng không sao — lần đầu nhờ dựng video, mọi bước trên vẫn tự chạy như cũ; lệnh này chỉ để chuẩn bị chủ động ngay sau khi cài + biết trạng thái máy bất cứ lúc nào.

**Lệnh "HỌC KIẾN THỨC MỚI" (khi Sếp/người dùng nói bất kỳ dạng nào: "học cái này", "ghi nhớ luật này", "từ nay làm thế này", "train cho tool", hoặc góp ý sửa sau khi duyệt/xem video)** — đây là cách tool được huấn luyện, làm NGHIÊM TÚC từng bước:
1. **Tìm đúng file đích** theo bảng (đừng nhét bừa vào SKILL.md):
   | Loại kiến thức | Ghi vào |
   |---|---|
   | Luật chọn cảnh nào lên hình / cảnh nào bỏ | `references/chon-canh-highlight.md` |
   | Style hình/chữ/nhạc Kiểu 1 (highlight) | `references/style-mau.md` |
   | Luật voice gốc / sub karaoke / Kiểu 2-3 | `references/style-voice-karaoke.md` |
   | Style video quảng cáo bán hàng | `references/style-ads-huy.md` |
   | Câu hỏi đầu vào / checklist thiếu-đủ | `references/chon-kieu-dung.md` |
   | Caption / hashtag / từ khóa | `references/caption-format.md` |
   | Thông số robot | `references/robot-products.md` |
   | Số liệu khách hàng thật (proof point) | `references/case-studies.md` |
   | Lệnh ffmpeg / kỹ thuật dựng | `references/ffmpeg-recipes.md` |
   | Hiệu ứng / chuyển cảnh / script `scripts/fx/` | `references/so-hieu-ung.md` |
   | Chọn tiếng SFX theo khoảnh khắc | `references/so-sfx.md` |
   | Quy trình tổng / luật vận hành | `SKILL.md` |
2. Viết luật **ngắn, kèm lý do + ngày + ai dạy** (vd "— Sếp Huy chỉnh 2026-07-17 sau video X"), đặt đúng mục có sẵn trong file, không phá cấu trúc.
3. Luật mới **mâu thuẫn luật cũ** → chỉ ra chỗ mâu thuẫn, hỏi người dạy chốt rồi mới ghi đè (ghi cả dòng "thay luật cũ ngày ...").
4. **Sửa CẢ 2 BẢN trên máy quản trị** (bản sống `~/.claude/skills/shorts-editor-rbw/` + bản repo trong `AI Boss\shorts-editor-rbw-plugin\`) — máy đồng nghiệp không có bản repo thì chỉ sửa được bản trên máy họ + NHẮC họ báo Sếp để đưa vào bản chung.
5. Trên máy quản trị: commit đích danh file vừa sửa + **push NGAY, TỰ ĐỘNG — không hỏi "có đẩy không"** (chỉ đạo Sếp Huy 17/07/2026: "học được cái gì là auto đẩy lên"; điểm dừng duy nhất là bước 3 khi luật mới mâu thuẫn luật cũ). Kể cả đang giữa buổi dựng video cũng khắc + đẩy luôn rồi dựng tiếp, đừng để dồn cuối buổi rồi quên. Thêm 1 dòng CHANGELOG nếu luật đáng chú ý → báo lại 1 câu: *"đã khắc luật vào <file>, đã đẩy lên — cả team nhận khi mở lại app"*.

   🔴 **BẮT BUỘC KÈM THEO — TĂNG SỐ BẢN, nếu không thì luật vừa khắc KHÔNG tới được máy nào cả.**
   Sửa bất cứ file nào trong `skills/` thì **phải sửa luôn `version` trong `.claude-plugin/plugin.json`** thành ngày hôm nay, định dạng `YYYY.MM.DD` (vd `2026.07.21`). Commit chung một lần với file luật.

   🔴 **VÀ TĂNG SỐ Ver** (luật Sếp Huy chốt 22/07/2026) — sửa **2 chỗ trong SKILL.md đầu file**: dòng `📦 BẢN HIỆN TẠI: Ver N` và **thêm 1 hàng vào bảng lịch sử Ver** (Ver mới / ngày / số máy đọc / có gì mới). Ver tăng **+1 mỗi lần phát hành**, không theo ngày. Cùng một ngày phát hành 2 lần thì là 2 Ver khác nhau. Bỏ bước này thì người dùng vẫn nhận được luật mới nhưng **mọi máy báo sai số bản cho nhau**, không ai biết ai đang chạy gì.

   *Vì sao*: lệnh `claude plugin update` **so sánh đúng trường `version` đó**, không nhìn mã commit. Version không đổi → mọi máy chạy update đều nhận câu *"already at the latest version"* và **không kéo gì về**, dù GitHub đã có luật mới.

   *Đã dính thật 21/07/2026*: 2 commit luật mới (nhạc Kiểu 2/3) push lên GitHub lúc 10:09 và 10:17 nhưng quên tăng version → nằm kẹt trên GitHub, không máy nào nhận. Phát hiện ra khi Sếp hỏi "tool cập nhật tới đâu rồi".

   *Chốt chặn đã cài*: hook `.git/hooks/pre-push` trên máy legion **chặn push** nếu có sửa trong `skills/` mà không đổi version (đã test đúng ca này). ⚠️ Hook **không tự lan sang máy khác** — máy quản trị nào clone mới phải copy hook theo, hoặc tự nhớ luật này.
6. 🔴 **MẶC ĐỊNH SỬA HẾT THỨ CẢN ĐƯỜNG DỰNG VIDEO, RỒI ĐẨY LUÔN — KHÔNG HỎI** (chỉ đạo Sếp Huy 22/07/2026: *"mặc định sửa hết những thứ cản đường edit video, tối ưu nhất là đẩy lên cho các máy khác chức năng tương tự"*).

   Thấy thứ gì chặn/làm hỏng việc dựng video — công cụ vỡ, model chết, báo lỗi khó hiểu, thiếu thứ máy khác không có — thì **sửa ngay + đẩy lên GitHub**, không dừng lại xin phép. Mọi thứ sửa phải **lan được sang máy khác**, không để thành bản vá chỉ sống trên một máy.

   **Ba điểm dừng duy nhất còn lại**: (a) luật mới mâu thuẫn luật cũ · (b) việc xoá/ghi đè dữ liệu của Sếp · (c) thứ tốn tiền ngoài mức đã biết. Ngoài ba cái đó thì tự quyết.

   **Sửa xong phải chạy thử thật** rồi mới đẩy — mọi công cụ động vào ít nhất phải chạy `--help` không lỗi, công cụ sửa sâu thì chạy trên file thật. Đẩy code chưa chạy thử là đẩy lỗi cho cả team.

7. 🔴 **CÀI THÊM THƯ VIỆN / MODEL MỚI → PHẢI KHAI BÁO VÀO `chuan_bi_may.py`, cùng commit** (luật Sếp Huy hỏi ra 22/07/2026: *"tôi quyết định cài thì bản đẩy lên cho máy khác có mặc định kèm theo không"* — câu trả lời là **KHÔNG, không có gì tự động cả**).

   Cài bằng `pip install` chỉ có tác dụng **trên đúng máy đang ngồi**. Muốn cả team có thì thêm dòng vào:
   - **`THU_VIEN`** — thư viện Python. Mỗi dòng 3 phần: tên module để `import` thử · tên gói pip · **"thiếu cái này thì MẤT GÌ"** (viết bằng lời đời thường, vd *"mất mắt AI Gemini"*).
   - **`MODEL_FILES`** — file model tải về. Gồm: tên file · dung lượng tối thiểu để biết tải đủ chưa · **link tải trực tiếp** · mô tả · cờ bắt buộc.

   *Vì sao nghiêm trọng*: quên khai báo thì trên máy quản trị mọi thứ chạy ngon lành, **push trót lọt, không có gì báo lỗi** — nhưng máy đồng nghiệp chạy đúng lệnh đó sẽ vỡ với thông báo kiểu `No module named ...`, mà họ không biết vì sao vì bản trên GitHub trông đã đầy đủ. Cùng họ với ca "luật nằm chết trên GitHub vì quên tăng version" (21/07).

   *Kiểm nhanh trước khi push*: chạy `python chuan_bi_may.py --kiem` — bảng phải báo **OK đủ N/N**, và N phải bằng đúng số dòng trong `THU_VIEN`.

   *Kèm điều kiện bắt buộc (bài học MediaPipe 21/07)*: thư viện mới **không được phá dependency của con đang chạy**. Cài xong phải kiểm lại `cv2` và `google.genai` còn import được không — MediaPipe đòi `numpy 2.x` + protobuf cũ trong khi máy ghim `numpy<2`, cài vào là hỏng cả 2 con đang chạy tốt. Hỏng thì **gỡ ra**, đừng cố ép.

8. 🔴 **LỊCH KHAI TỬ MODEL AI: ĐỪNG TIN TÀI LIỆU, ĐO THẬT** (bài học đắt 22/07/2026).

   Mọi tài liệu trong dự án ghi *"`gemini-2.5-flash` bị khai tử 16/10/2026"* → ai đọc cũng tưởng còn 3 tháng. **Gọi thử thì nó đã TẮT SẴN rồi**: `404 no longer available`. Tức là **mắt AI đang hỏng mà không ai biết**, chỉ lộ ra lúc đang dựng video giữa chừng. Cùng lúc đó `gemini-2.0-flash` — thứ tài liệu ghi *"đã tắt 01/06/2026"* — lại **vẫn còn sống** (chỉ báo hết lượt). **Cả hai dòng ghi chép đều sai, theo hai hướng ngược nhau.**

   *Luật*: nghi model có vấn đề thì **gọi một lệnh siêu ngắn để đo**, đừng tra tài liệu. Vài chục token, gần như 0 đồng.

   *Đã cài sẵn chốt*: `quet_mat_ai.py` tự kiểm model **trước khi nén clip nào**, gặp 404 thì **tự chuyển sang bí danh `gemini-flash-latest`** (bí danh luôn trỏ bản còn sống nên không bao giờ chết vì khai tử) và báo 1 dòng. Người dùng không bị kẹt giữa buổi dựng.

9. **Không đưa vào repo**: bí mật (API key), đường dẫn riêng của 1 máy, sở thích cá nhân 1 người — những thứ đó chỉ ghi máy cục bộ.

0. **LUÔN làm theo đúng `references/chon-kieu-dung.md` NGAY khi skill được gọi** (file này tách riêng để dễ cập nhật — thêm/sửa câu hỏi thì sửa trong đó, không sửa SKILL.md): hỏi người dùng chọn 1 trong **3 KIỂU DỰNG**, rồi kiểm tra đã đủ nguyên liệu bắt buộc cho đúng kiểu đó chưa, thiếu gì hỏi ngay — đừng viết kịch bản khi còn thiếu mục bắt buộc. Tóm tắt 3 kiểu (chi tiết + checklist đầy đủ nằm trong file trên):
   - **Kiểu 1 — Highlight + chữ + nhạc** (có source, không cần thoại; spec: `references/style-mau.md`)
   - **Kiểu 2 — Dựng theo lời thoại có sẵn** (source đã có người nói đồng bộ lúc quay; spec: mục "Quy tắc VOICE GỐC MC" trong `references/style-voice-karaoke.md`)
   - **Kiểu 3 — Ghép cảnh + thêm voice-over mới** (giọng AI hoặc thu riêng, không đồng bộ lúc quay; spec: `references/style-voice-karaoke.md` phần karaoke sub, hoặc `references/style-ads-huy.md` nếu kịch bản dạng quảng cáo bán hàng)
   Người dùng nói rõ kiểu + đủ nguyên liệu ngay trong tin đầu thì không hỏi lại — chỉ hỏi đúng phần còn thiếu.

   **Hỏi gọn trong 1 lượt, chạy máy song song**: mọi câu hỏi còn thiếu (kiểu dựng, mô tả buổi quay, chữ đè, nhạc, giọng đọc...) GỘP vào đúng 1 tin nhắn — đừng bắt người dùng trả lời 2-3 lượt mới khởi động được. Và ngay khi đã có đường dẫn folder source hợp lệ (kể cả khi còn đang chờ trả lời các câu hỏi khác), **khởi chạy `analyze_footage.py` chạy NỀN luôn** (0 token, thuần máy) — với điều kiện ffmpeg + model Whisper đã sẵn sàng (chưa sẵn thì chờ phần cài/tải nền xong mới chạy, đừng chạy phân tích khi thiếu model kẻo index ghi nhầm "không có thoại"). Lúc người dùng trả lời xong thì phân tích thường cũng vừa xong — tiết kiệm nhiều phút chờ.
1. Sau khi đủ nguyên liệu: xác nhận đã có đường dẫn đầy đủ tới folder source (nếu chưa, hỏi xin ngay — xem mục "Phạm vi làm việc" ở trên). Robot xuất hiện trong footage là model nào → tra `references/robot-products.md` trước; chỉ hỏi lại nếu không chắc chắn model hoặc model chưa có trong danh mục.
2. Skill phân tích footage → viết kịch bản cho từng ý tưởng (chưa có ý tưởng cụ thể thì tự đề xuất 2-3 ý hay nhất từ footage, xem thêm `references/chon-canh-highlight.md` để chọn đúng cảnh highlight)
3. **Trình duyệt kịch bản** (tóm tắt ngắn gọn từng video: hook, mạch cảnh, text đè, nhạc, thời lượng; nêu rõ chỗ nào đang tự suy đoán nếu thông tin "nên có" còn thiếu). OK cái nào dựng cái đó; sửa thì cập nhật rồi dựng luôn theo ý sửa
4. Dựng tự động toàn bộ, tự nghiệm thu, xuất video final + caption, mở folder giao hàng

## Môi trường (đã cài & kiểm chứng trên máy này)

- **ffmpeg/ffprobe**: gọi `ffmpeg` trực tiếp; nếu shell báo không tìm thấy VÀ `ffmpeg_path`/`ffprobe_path` trong `config.json` (cùng thư mục file này) cũng để trống — **TỰ CÀI LUÔN, đừng hỏi trước "bạn có muốn cài không"**: báo 1 câu ngắn ("máy chưa có FFmpeg, tôi cài luôn nhé — vài phút"), chạy `winget install ffmpeg -e --source winget` (nguồn cài đặt chính thức của Windows, an toàn). **Cài xong KHÔNG bắt người dùng đóng/mở lại Claude Code** (làm vậy mất sạch những gì họ vừa khai): PATH của phiên đang chạy chưa nhận lệnh mới là chuyện bình thường — tự tìm file `ffmpeg.exe` vừa cài trong `%LOCALAPPDATA%\Microsoft\WinGet\Packages\Gyan.FFmpeg*\` (tìm đệ quy, lấy file trong thư mục `bin`), ghi đường dẫn đầy đủ vào `ffmpeg_path`/`ffprobe_path` trong `config.json`, rồi dùng ngay qua đường dẫn đó — mọi script của skill đều tự đọc `config.json`. Chỉ hỏi lại người dùng nếu `winget` báo lỗi thật (máy không có winget, mạng chặn...) — đây là bước bắt buộc để dùng được skill, không phải tùy chọn.
- **Model Whisper** (`ggml-large-v3-turbo.bin`, ~1.6GB, dùng để nghe lời thoại — cần cho Kiểu 2/3): chỗ lưu chuẩn là **`~/.claude/roboworld-assets/models/`** (chỗ bền — gỡ/cài lại plugin KHÔNG mất, không phải tải lại 1.6GB); máy cũ có sẵn model ở `assets/models/` trong skill vẫn dùng được bình thường (script tự tìm cả 2 nơi, ưu tiên chỗ bền). Kiểm tra ngay khi skill được gọi lần đầu trong phiên — nếu cả 2 nơi đều chưa có, **TỰ TẢI LUÔN, đừng hỏi trước**: báo 1 câu ngắn ("cần tải thêm bộ nghe giọng nói ~1.6GB, tôi tải nền — bạn cứ trả lời tiếp, không phải chờ"), rồi chạy NỀN lệnh trong `assets/models/README.md` (`Invoke-WebRequest` tới file `.bin` trên Hugging Face, lưu vào `~/.claude/roboworld-assets/models/`). **Quy tắc bắt buộc khi tải**: tải vào tên file tạm đuôi `.part` rồi mới `Rename-Item` thành `.bin` khi xong — kẻo script phân tích vớ nhầm file tải dở. **Kiểu 2/3 phải CHỜ model tải xong mới chạy phân tích thoại** (chạy phân tích khi thiếu model sẽ ghi nhầm "không có thoại" vào index); Kiểu 1 không cần chờ. Chỉ hỏi lại người dùng nếu lệnh tải lỗi thật (mạng chặn, hết dung lượng).
- **Python 3.9** + `gdown` + `edge-tts`
- **Card đồ họa NVIDIA (nếu máy có)**: đầu phiên dựng đầu tiên, chạy `python "<skill-dir>\scripts\cai_driver_nvidia.py" --check` (im lặng, 2 giây). Báo `CAN_NANG_DRIVER` → hỏi người dùng 1 câu (mẫu câu + luồng đầy đủ trong ffmpeg-recipes mục 0.6, GỘP vào đợt câu hỏi bước 0) — họ OK thì script tự tải + cài, họ chỉ bấm Yes 1 lần. Báo `GPU_SAN_SANG` hay `KHONG_CO_CARD` → không nói gì thêm, dựng bình thường. **Không bao giờ tự cài driver khi chưa được OK.**
- **Voice AI (khi kịch bản có voiceover)** — `scripts/elevenlabs_tts.py`, key đọc từ `~/.claude/abs6-secrets.env` dòng `ELEVENLABS_API_KEY=`. **KHÔNG BAO GIỜ in key ra chat/log.**

  **Thứ tự chọn giọng (cập nhật 20/07/2026 — đã đo thật, đừng làm ngược):**

  | Ưu tiên | Giọng | Khi nào |
  |---|---|---|
  | 1 | **MC Xuân Tú** `7XOKiK112QRZRSLbCfMc` (nam, Bắc) · **Thanh Ngọc** `Na15FlRRkMEDtEW4nVVP` (nữ, Nam) | Mặc định cho **mọi lời tiếng Việt**. Đã có sẵn trong tài khoản công ty. Cần gói trả phí |
  | 2 | **edge-tts** `vi-VN-NamMinhNeural` / `vi-VN-HoaiMyNeural` | Khi gói còn Free (2 giọng trên trả 402). Miễn phí, đọc câu tiếng Việt thuần rất sạch |
  | 3 | **George** `JBFqnCBsd6RMkjVDRZzb` | **CHỈ khi lời đọc là tiếng Anh** |

  **George KHÔNG còn là mặc định** — đó là giọng Anh. Cho Whisper nghe lại bản George đọc tiếng Việt: *"Thử cách này"* → *"Thú káč nai"*, *"Khai trương thì bùng nổ doanh số"* → *"Cái truong thị bùng no đoàn so"*. Gặp 402 mà lui về George là làm hỏng video.

  **Gặp 402**: script tự in hướng dẫn đầy đủ. Nếu giọng do người dùng **chỉ định đích danh** → DỪNG BÁO, chờ họ quyết, không tự đổi giọng. Nếu là giọng mặc định → lui edge-tts giọng Việt, báo 1 câu.

  **Luôn nhớ luật viết lời cho TTS**: tên sản phẩm/thương hiệu/thông số **không cho máy đọc**, đẩy lên thẻ chữ — mọi giọng máy đều đọc sai mấy từ đó (xem `style-voice-karaoke.md`).
- **Font Anton** (style CapCut, Sếp chỉ định): `assets/fonts/Anton-Regular.ttf` trong thư mục skill — copy vào workspace mỗi lần dựng (xem recipes)
- **Tài nguyên dùng chung** (logo, outro, nhạc, SFX, ảnh sản phẩm) — kho chính thức nằm trên **Google Drive của Sếp** (Sếp thêm nhạc/logo mới bằng cách kéo file vào Drive, không cần đụng GitHub), link cố định:
  `https://drive.google.com/drive/folders/1eofLwPIE6XtoMPI6Wo19gf48KwM1OYIr`
  - **Chỗ lưu trên máy (bền, tải 1 lần)**: `~/.claude/roboworld-assets/tai-nguyen-chung/`. Lần đầu dùng skill (hoặc khi thiếu folder này): tự tải cả kho về bằng `python "<skill-dir>\scripts\tai_kho_tai_nguyen.py"` — script tự dùng gdown, tự đối chiếu danh sách file Drive khai báo với file thật tải về, **thiếu file nào báo ĐÍCH DANH file đó** (đừng tin "chạy xong không lỗi" = đủ). Tải nền được — không bắt người dùng ngồi chờ. Máy cài bản cũ còn kho tại `assets/tai-nguyen-chung/` trong skill: vẫn dùng được (tìm chỗ bền trước, chỗ cũ sau).
  - **Lệnh "cập nhật kho tài nguyên"**: khi người dùng nói vậy (hoặc Sếp báo vừa thêm nhạc mới) → chạy lại đúng script trên, nó chỉ tải phần thiếu/mới (`--continue`), xong báo có gì mới.
  - **Lỗi hay gặp khi tải**: (a) đường dẫn quá dài — script đã tự tải vào thư mục tạm ngắn rồi mới chuyển về chỗ bền, đừng tự tải thẳng vào đường dẫn sâu; (b) Google chặn tạm vì tải dồn dập ("Cannot retrieve... many accesses") — đợi 15-30 phút chạy lại với `--continue`, KHÔNG tải lại từ đầu.
  - **LƯU Ý đường dẫn trong kho**: tên folder trên Drive có thể kèm hậu tố tải xuống (vd `Logo + Outro-20260529T.../Logo + Outro/`) — **tìm tài nguyên theo TÊN FILE bằng Glob trong toàn kho** (vd tìm `Logo ngang trắng.png`), đừng dựa vào đường dẫn folder cứng.
  - **Logo**: file `Logo ngang trắng.png` (dùng overlay giữa-trên) — logo TRẮNG, không dùng bản đỏ (bản đỏ chỉ dùng trong outro có sẵn).
  - **Outro dọc**: file `outro dọc.mp4` (2160x3840, ~9s, có sẵn nhạc/audio riêng) — nối vào cuối bằng crossfade, xem `references/ffmpeg-recipes.md` mục 4d. Đừng tự bịa outro khác khi đã có file này. **Chỉ dùng cho video đăng page công ty** — kênh cá nhân bỏ hẳn (luật 21/07, xem `references/chon-kieu-dung.md` bước C).
  - **Nhạc nền**: kho nhạc riêng của Sếp trong folder `Kho nhạc free YT` — ưu tiên dùng bài trong kho trước; Sếp chỉ định bài nào thì dùng ĐÚNG bài đó.
    - **LUẬT 20/07/2026 (Sếp Huy) — Kiểu 1 BẮT BUỘC hỏi loại nhạc trước khi chọn bài**: nhạc **trend** (folder `Nhạc hot`, bắt tai nhưng **chỉ đăng được Facebook page** — YouTube khả năng cao dính bản quyền) hay nhạc **không bản quyền** (các folder còn lại, đăng được mọi nền tảng). Câu hỏi nguyên văn + cách xử lý: `references/chon-kieu-dung.md` bước B; chi tiết kho + cách tách: `references/style-mau.md` mục "Kho nhạc trend". Hỏi rồi thì không nhắc lại rủi ro bản quyền lần 2 trong cùng video.
    - Folder `Nhạc hot` chứa **bản mix dài ~1 tiếng** (Sếp đẩy thêm dần), không dùng thẳng được — tách bằng `scripts/tach_bai_tu_mix.py` (cần file `tracklist.txt` lấy từ mô tả video gốc; các mix này crossfade liền mạch nên KHÔNG tách tự động bằng silencedetect được).
    - **LUẬT 21/07/2026 (Sếp Huy) — Kiểu 2 & Kiểu 3 chia 2 NHÓM theo mức phủ của giọng nói. BẮT BUỘC hỏi ngay sau khi chọn kiểu** (câu hỏi nguyên văn: `references/chon-kieu-dung.md`, khối "Luật nhạc theo mức phủ giọng"):
      - **Nhóm A — giọng dẫn xuyên suốt** (MC nói cả bài, hoặc voice-over phủ phần lớn thời lượng): nhạc nền **TUYỆT ĐỐI KHÔNG LỜI**, áp cho **CẢ video** kể cả đoạn cuối không ai nói (đổi nhạc giữa chừng nghe gãy — Sếp chốt 21/07). **KHÔNG hỏi trend/không-bản-quyền; cấm folder `Nhạc hot`.**
      - **Nhóm B — giọng chỉ mở màn 1-2 câu rồi im hẳn**, phần sau để cảnh robot + nhạc tự kể: **ĐƯỢC dùng nhạc có lời, kể cả nhạc hot**. Nhạc để **nhỏ trong lúc đang nói (0.15-0.2), nói xong dâng dần lên to đến hết bài (~0.55)** — công thức ở `references/ffmpeg-recipes.md` mục 5b. Nhóm này **PHẢI hỏi trend hay không bản quyền** giống Kiểu 1, vì nhạc hot chỉ đăng được Facebook page.
      - **Lý do luật gốc**: 2 giọng chồng lên nhau bắt tai người nghe chia sự chú ý, lời dẫn bị nuốt — hạ volume nhạc KHÔNG cứu được. Nhóm B thoát luật vì sau 1-2 câu đầu không còn giọng nào để chồng lên nữa.
      - Không chắc bài có giọng hát hay không → **nghe kiểm trước khi dùng** (folder `POP tươi sáng` có lẫn bài có lời). **Kiểu 1 không áp luật này.**
  - **Nhạc sinh bằng AI (ElevenLabs Music — option mở rộng, cần gói trả phí)**: chỉ dùng khi (a) người dùng chủ động yêu cầu "nhạc đo ni theo video", hoặc (b) kho không có bài hợp VÀ người dùng đồng ý. Chạy `python "<skill-dir>\scripts\elevenlabs_music.py" "<mô tả nhạc>" <output.mp3> --length-ms <độ dài video>` — gói Free sẽ lỗi, khi đó DỪNG BÁO "cần gói ElevenLabs trả phí", không tự thay bằng nguồn nhạc khác.
  - **Sound effect**: kho SFX trong `SFX/Bo 35 SFX` (vd `08 - Woosh fire transition.mp3`) — ưu tiên dùng kho này trước khi tải thêm. **Đếm thật 21/07/2026: 36 file trong folder đó + 3 file rời ngay ngoài `SFX/` = 39 file.** Tên folder "Bo 35 SFX" và các con số "35"/"38" trong tài liệu cũ đều KHÔNG khớp thực tế — đừng tin số, cứ liệt kê thư mục khi cần. **Luật hiện hành (19/07/2026): MỖI thẻ chữ đều kèm 1 SFX "pop" hợp nghĩa, CỘNG các SFX khớp hành động trong hình** — mật độ kiểu TikTok/Reels, ~14 lớp/55s. Chi tiết + bảng lead-in đã đo sẵn: ffmpeg-recipes mục 4b; cây chọn tiếng: `so-sfx.md`.
    > ⚠️ Luật cũ 03/07/2026 ("chỉ dùng SFX khi khớp hành động cụ thể, đừng gắn SFX chỉ vì text vừa xuất hiện") **đã bị Sếp Huy bãi bỏ ngày 19/07** sau khi xem video-1 Tràng An thấy SFX còn thưa. Câu đó từng còn sót ở đây tới 21/07 — nếu gặp lại ở file nào khác thì đó là tàn dư, gỡ đi.
  - **Ảnh sản phẩm không nền**: folder `Ảnh sản phẩm ko nền/<tên robot>/` — dùng khi kịch bản cần ghép ảnh sản phẩm rời (không phải cảnh quay), vd làm thumbnail hoặc card thông số.

## Quy trình chi tiết

### Bước 1 — Xác định source & lập workspace

- Dùng đúng đường dẫn đầy đủ người dùng đã đưa (gõ tay hoặc kéo-thả). Nếu bên trong có subfolder rõ ràng chứa clip nguồn (vd `Nguồn video\`), dùng đúng subfolder đó làm source; nếu clip nằm ngay cấp ngoài, dùng luôn folder đó.
- **Chỗ để hàng giao (luật Sếp Huy 20/07/2026) — TÁCH RÕ 2 NƠI:**
  | Thư mục | Chứa gì | Ai xem |
  |---|---|---|
  | **`<folder buổi quay>\Final\`** | **CHỈ 2 thứ: video thành phẩm (.mp4) + file caption (.md) của chính video đó** | Sếp — mở là thấy hàng, không phải lục |
  | `<folder buổi quay>\Workspace\` | Toàn bộ đồ nghề trung gian: `analysis`, `kichban`, `fonts`, `temp`, `voice`, `build-*.ps1` | Chỉ Claude dùng lại ở phiên sau |

  Bộ khung folder buổi quay của Sếp **vốn đã có sẵn thư mục `Final` (để trống)** — dùng đúng thư mục đó, không tạo thêm tên khác. Chưa có thì tạo. **TUYỆT ĐỐI không để file trung gian, file tạm, ảnh sheet, log hay script vào `Final`** — vào đó là làm rối đúng chỗ Sếp cần gọn nhất.
- Tạo workspace ngay trong folder buổi quay đó: `<folder buổi quay>\Workspace\` với các thư mục con: `analysis`, `kichban`, `fonts`, `temp` (thêm `voice\` nếu kịch bản có voiceover). **Không tạo `output\` nữa** — thành phẩm đi thẳng ra `Final\`.
- Ghi input của Sếp (mô tả sự kiện, ý tưởng) vào `kichban\00-input.md`.
- Nguồn là link Google Drive (hiếm) → tải bằng `python -m gdown --folder --continue "<link>" -O <workspace>\source` (nhớ đặt `PYTHONUTF8=1` nếu tên folder có dấu tiếng Việt; gdown bản mới ≥5.2 đã bỏ trần 50 file — nếu máy đang gdown cũ thì `pip install -U gdown` trước).

### Bước 2 — Phân tích footage (v2: khung thông minh + voice + index tái sử dụng)

Model Whisper đã được kiểm tra/tự tải sẵn từ đầu phiên (xem mục "Môi trường" ở trên) — không cần kiểm tra lại ở bước này.

```powershell
python "<skill-dir>\scripts\analyze_footage.py" "<folder-source>" "<workspace>\analysis"
```

Script tự: bắt điểm đổi cảnh để trích khung đúng khoảnh khắc (không rải mù), ghép 1 ảnh lưới/clip có **nhãn timecode trên từng khung** (`analysis\sheets\`), nhận dạng lời nói trong clip bằng Whisper (transcript + timestamp, cần model trong `assets/models/` — chưa có thì tự bỏ qua), và ghi tất cả vào `analysis\index.json`. **Clip đã có trong index sẽ tự bỏ qua** — folder cũ thêm clip mới chỉ tốn phân tích phần mới.

**Bước 2b — ĐO KỸ THUẬT (chạy ngay sau khi index xong, trước khi đọc sheet)** — luật 20/07/2026:

```powershell
python "<skill-dir>\scripts\do_ky_thuat.py" --src "<folder-source>" --index "<workspace>\analysis\index.json"
```

Miễn phí, chạy offline, không gọi API, ~1-2 giây/clip. Đo **độ nét** (clip có khoảnh khắc nào dùng được không) và **độ chuyển động**, ghi cờ cảnh báo vào index. Mục đích: **loại bớt clip hỏng TRƯỚC khi tốn công đọc sheet hoặc tốn tiền gọi mắt AI**.

Đọc cờ: `mo` = bỏ · `hoi-mo` = xem lại · **`net-tung-doan` = clip có đoạn nét có đoạn mờ, phải chọn ĐÚNG đoạn** · `canh-tinh` = hợp làm nền hơn làm cảnh chính.

**Đây là cờ cảnh báo, không phải án quyết định** — bokeh hay motion blur cố ý cũng bị chấm "mờ". Dùng để thu hẹp việc phải xem, không thay việc xem.

**Bước 2c — MẮT AI GEMINI (TUỲ CHỌN — TỐN TIỀN THẬT + GỬI CLIP LÊN CLOUD)**

> ⚠️ **HAI ĐIỀU PHẢI HỎI NGƯỜI DÙNG TRƯỚC KHI CHẠY, KHÔNG ĐƯỢC TỰ Ý:**
> 1. **Tốn tiền thật** trên tài khoản Google của chủ key (~150-200đ/phút video). Quét cả một buổi quay 15 phút ≈ 3.000đ; quét cả kho 35 folder ≈ vài trăm nghìn. **Không bao giờ tự quét cả folder** khi chưa được đồng ý — mặc định chỉ chạy khi người dùng nói rõ, và nên kèm `--limit` cho lần đầu.
> 2. **Clip được UPLOAD lên máy chủ Google** (script tự xoá ngay sau mỗi clip, nhưng dữ liệu vẫn đã rời khỏi máy). Footage quay tại nhà máy/bệnh viện/trường học của khách hàng có thể thuộc diện ràng buộc bảo mật — **hỏi trước khi gửi footage của khách lên cloud.**
>
> Bước này KHÔNG bắt buộc. Không có nó thì vẫn dựng video bình thường (đọc sheet bằng mắt như cũ).

```powershell
python "<skill-dir>\scripts\quet_mat_ai.py" --src "<folder buổi quay>" --index "<workspace>\analysis\index.json" --limit 10
```

Gemini **xem** clip (không chỉ nghe) rồi trả về: có robot không, robot dòng nào, đang làm gì, bối cảnh, chất lượng hình, **`co_nguoi_dang_noi`**, khoảnh khắc đáng dùng. Ghi vào index, tự resume, ngắt giữa chừng không mất gì.

- **Tự bỏ qua clip đã bị bước 2b chấm "mờ"** — không tốn tiền hỏi về clip không dùng được. Muốn quét cả thì thêm `--quet-ca-clip-mo`.
- Chi phí ~150-200đ/phút video (Gemini 2.5 Flash); gói free có trần ~20 lượt/ngày, chạm trần thì script nghỉ lùi dần rồi dừng — **chạy lại là quét tiếp**, không làm lại từ đầu.
- Trường **`co_nguoi_dang_noi` chính là thứ hỗ trợ luật cấm cảnh MC-cutaway** — dùng để lọc ứng viên B-roll trước khi soi khung bằng mắt.
- Quét 1 clip lẻ: `python "<skill-dir>\scripts\gemini_vision.py" --video CLIP.mp4`

### Bước 4 — LỌC THOẠI THẬT + lấy mốc cắt (BẮT BUỘC với Kiểu 2 và Kiểu 3, miễn phí, offline)

```powershell
python "<skill-dir>\scripts\loc_thoai_that.py" --index "<workspace>\analysis\index.json" --folder "<folder buổi quay>"
```

- **BẮT BUỘC chạy trước khi viết kịch bản** với mọi video có tiếng người nói. Bỏ qua bước này là quay lại đúng cái sai ngày 21/07 (cắt lệch 4 giây, mất đầu câu MC).
- Trả về từng đoạn **có giọng người thật nói vào máy**, kèm mốc vào/ra chính xác, và tự đánh dấu:
  - **BẢN TỐT NHẤT** khi MC nói lại cùng một câu nhiều lần (chọn bản to nhất = gần mic nhất)
  - **XA MIC** khi cách sàn nhiễu < 15 dB
  - **NGHI Ê-KÍP** khi là lời chỉ đạo/quên thoại chứ không phải nội dung
- **PHÂN CÔNG 3 CÔNG CỤ — đừng dùng nhầm việc** (chốt 21/07 sau khi Sếp chấm tai 4 ca):

  | Công cụ | Trả lời câu hỏi | Đừng dùng nó để |
  |---|---|---|
  | `loc_thoai_that` | **Cắt Ở ĐÂU** + đoạn có dùng được không | — |
  | **Gemini** | **Đoạn nào ĐÁNG LÊN HÌNH** (điểm nội dung, hook) | ~~lấy mốc cắt~~ (sai 2/4 ca) |
  | Whisper | **Nói GÌ** (nội dung chữ) | ~~lấy mốc cắt~~ (số nối đuôi, không phải số đo) |

  Script **tự ghép sẵn** điểm Gemini vào từng đoạn: cột `G9/10` là điểm khoảnh khắc, cờ `HOOK (Gemini)` là ứng viên mở đầu. Dòng `DUNG DUOC` đã xếp sẵn theo ưu tiên hook → điểm cao → thứ tự thời gian. **Cứ lấy theo thứ tự đó mà dựng.**

  Script cũng **đối chiếu chéo** và cảnh báo 2 tình huống: (a) Gemini thấy có người đang nói mà không đoạn nào đủ gần mic → người nói ở xa/ngoài khung, dùng làm thoại chính sẽ tệ; (b) script tìm ra thoại mà Gemini bảo không có ai đang nói trên hình → nhiều khả năng là lời dẫn ngoài hình, **cấm đặt làm B-roll đè voice khác** (luật cấm MC-cutaway).

  Bằng chứng đầy đủ: `references/style-voice-karaoke.md` mục 3.
- **Lớp soi chéo Silero VAD** (tuỳ chọn, tự bỏ qua nếu thiếu): model `silero_vad.onnx` (2.3MB) đặt ở chỗ bền `~/.claude/roboworld-assets/models/`. Máy chưa có thì tải:
  ```powershell
  Invoke-WebRequest "https://github.com/snakers4/silero-vad/raw/master/src/silero_vad/data/silero_vad.onnx" -OutFile "$HOME\.claude\roboworld-assets\models\silero_vad.onnx"
  ```
  Cần thư viện `onnxruntime` (**không cần `torch`**). Cột `S0.99` trong kết quả là điểm Silero — dưới 0.5 nghĩa là **nghi tiếng động to chứ không phải giọng người**, script tự gắn cờ.

  ⚠️ **Silero KHÔNG thay được hệ đo chính** — đã so thật 21/07 trên 3 ca tai Sếp chấm: **hệ đo hiện tại thắng 2, hoà 1**. Lý do: Silero trả lời *"có phải giọng người không"* nên nó **gộp cả 3 lần MC nói lại thành 1 đoạn** (21.31→29.98) trong khi bản thật ở 24.4. Nó không phân biệt được lần nói thật với lần tập — mà đó chính là bài toán. Chỉ dùng làm lớp soi chéo. *(Lưu ý khi đọc kết quả so sánh đó: ngưỡng 15 dB của hệ đo chính được hiệu chỉnh trên chính mấy clip đem ra thi, còn Silero thi trần trụi — nên phần thắng chưa hoàn toàn công bằng.)*
- ⛔ **Chạy TRƯỚC mọi bộ lọc âm thanh.** Lọc ồn/`speechnorm` chạy trước sẽ phá hệ đo mà không báo lỗi — xem `references/ffmpeg-recipes.md` mục 5c.
- Script in `San nhieu` ngay đầu: **cao hơn -25 dB thì đừng phí công thử `silencedetect`**, nó sẽ chết.

**Thứ tự đúng của cả 4 bước**: `analyze_footage` (nghe + đổi cảnh) → `do_ky_thuat` (đo, miễn phí, 100% clip) → `quet_mat_ai` (hiểu, tốn tiền, chỉ clip đã lọc) → `loc_thoai_that` (mốc cắt, miễn phí, chỉ clip có thoại). Làm ngược là vừa chậm vừa tốn.

Rồi xem footage theo nguyên tắc **SÀNG LỌC TRƯỚC — đọc sheet là phần tốn nhất, đừng đọc cả kho khi chỉ cần 1 video**:
1. **Lập shortlist 0 token trước**: đọc `index.json` (transcript, độ dài, tên file, số điểm đổi cảnh, `content`/`tags` đã điền từ lần trước) để khoanh ~10-20 clip liên quan nhất tới video đang định dựng. Kiểu 2/3 lọc theo transcript; Kiểu 1 lọc theo độ dài/điểm đổi cảnh/`content` cũ.
2. **Chỉ Read ảnh sheet của shortlist** rồi điền index cho đúng các clip đó: `content` (1-2 câu mô tả), `tags` (robot/hành động/bối cảnh), `key_moments` (list `{t, mota}` — lấy đúng timecode in trên khung), `quality` ("tot"/"rung"/"toi"/"bo"). Index đầy dần qua các lần dựng — folder dùng nhiều thì tự nhiên xem đủ hết.
3. **Lối thoát**: không có tín hiệu lọc nào (folder mới tinh chưa có content, không transcript, tên file không gợi ý — thường gặp ở Kiểu 1 folder lạ) → đọc hết như cũ, chấp nhận tốn 1 lần.
4. **Luật cứng giữ nguyên**: clip CHƯA XEM SHEET thì không được đưa vào kịch bản. Đừng viết kịch bản khi chưa xem footage — kịch bản bịa cảnh không có thật là lỗi nặng nhất của skill này.

### Bước 2d — ĐẾM TƯ LIỆU + CHỌN CẢNH theo quy trình chuẩn (BẮT BUỘC, trước khi viết kịch bản)

🔴 **Đọc `references/quy-trinh-chon-canh.md` và làm đúng theo đó.** File này là quy trình chuẩn Sếp chốt 21/07 sau khi bắt 3 lỗi nội dung mà hệ nghiệm thu kỹ thuật báo "đạt" hết.

Tóm tắt 4 điều không được bỏ:

1. **Công cụ nào dẫn tuỳ loại đoạn** — đoạn giữ nguyên lời người nói thì `loc_thoai_that` (âm thanh) dẫn; đoạn không thoại thì **ảnh lưới + Gemini** (hình) dẫn. Công cụ còn lại chuyển sang vai đối chiếu, **không được lờ đi khi nó mâu thuẫn**.
2. **Lọc cảnh có người đang nói bằng `gemini.co_nguoi_dang_noi`, KHÔNG bằng `has_speech`** — `has_speech` là cờ âm thanh, người mấp máy môi mà mic không bắt được thì lọt (đo thật: sót 4/21 clip).
3. **ĐẾM tư liệu TRƯỚC khi viết kịch bản.** Số clip qua được cổng lọc × ~3 giây = thời lượng tối đa dựng được không lặp. **Thiếu thì DỪNG BÁO người dùng** — thiếu tư liệu là một dạng bị chặn, tự xoay xở bằng cách lấy lại clip cũ là sai quy trình.
4. **Chưa mở ảnh lưới của clip thì không được đưa clip đó vào kịch bản.** Mô tả bằng chữ của Gemini dùng để thu hẹp danh sách, **không thay được việc nhìn** (ca thật: Gemini tả "cúi xuống bấm màn hình", ảnh lưới cho thấy người đó đang đứng nói vào máy quay).

### Bước 3 — Viết kịch bản & TRÌNH SẾP DUYỆT

Đọc file style theo KIỂU đã chọn ở bước 0 (xem link style tương ứng trong `references/chon-kieu-dung.md`), cùng `references/kichban-template.md`, `references/robot-products.md` (thông số robot chính xác — không bịa số), `references/case-studies.md` (số liệu khách hàng thật, dùng làm proof point cho hook/CTA khi đúng ngữ cảnh) và `references/chon-canh-highlight.md` (quy tắc chọn cảnh nào lên hình, cảnh nào bỏ — đúc kết từ đối chiếu source thô thật với video final thật) trước khi viết.

- Mỗi ý tưởng → 1 file `kichban/video-N-<slug>.md`.
- Trình duyệt tóm tắt mỗi video: **hook (mở đầu) → chuỗi cảnh chính (3-5 cảnh, clip nào) → các dòng text đè/lời thoại → nhạc → thời lượng**. Kèm câu hỏi còn thiếu (logo? nhạc?). Chờ OK rồi mới dựng — đây là điểm dừng thứ 2 của workflow.

### Bước 4 — Dựng video (sau khi Sếp duyệt)

Đọc `references/ffmpeg-recipes.md` trước khi dựng video đầu tiên trong phiên. Trình tự mỗi video:

1. Cắt & chuẩn hóa từng cảnh về 1080x1920/30fps theo bảng phân cảnh
2. Ghép cảnh (concat)
3. Burn text ASS font Anton (hook vàng + text trắng, vị trí dưới logo — spec trong style-mau.md); copy `Anton-Regular.ttf` vào `<workspace>\fonts\` và dùng `fontsdir`
4. Nối **outro dọc** vào cuối bằng crossfade (xem mục 4d trong recipes) — **CHỈ khi video đăng page công ty**. Kênh cá nhân thì BỎ HẲN bước này (luật 21/07, xem recipes mục 5d).
5. Overlay logo giữa-trên — **CHỈ khi video đăng page công ty** (chỉ trong phần thân video, tự ẩn trước khi outro bắt đầu — outro đã có logo riêng) + trộn nhạc nền (và voiceover nếu kịch bản có — edge-tts, nhớ dùng `--file` UTF-8) + **sound effect theo luật 19/07/2026: MỖI thẻ chữ đều kèm 1 SFX pop hợp nghĩa (kiểu TikTok/Reels, dày ~14 lớp/55s), CỘNG các SFX khớp hành động trong hình**; mọi SFX đặt theo công thức `offset = mốc hành động − lead-in` (bảng lead-in 11 file đã đo sẵn ở mục 4b recipes — không đo lại). Nguồn: kho `Bo 35 SFX`, cây chọn tiếng trong `so-sfx.md`
6. Xuất thẳng ra **`<folder buổi quay>\Final\video-N-<slug>.mp4`** (H.264 CRF 20, AAC). Chuyển cảnh: cắt cứng là mặc định cho nhịp nhanh; chỉ crossfade khi có bước ngoặt nội dung (đổi địa điểm/thời gian, hoặc nối outro) — xem mục 4c
7. **Tự nghiệm thu bắt buộc**: trích 4-5 frame (rải cả trong thân video lẫn đoạn outro) + Read kiểm tra (chữ đủ to, không tràn viền, không thừa dấu câu, logo không đè text và tự ẩn đúng lúc trước outro, hình không méo, không frame đen); ffprobe xác nhận thời lượng; **đo âm lượng bằng loudnorm** (lệnh đo trong ffmpeg-recipes mục 6) — chuẩn giao hàng là **-14 LUFS (±1)**, lệch thì mix lại. Sai thì sửa và dựng lại trước khi bàn giao.

   🔴 **NGHIỆM THU TẦNG B — NỘI DUNG (bắt buộc, luật 21/07)**: mọi thứ ở trên là **tầng kỹ thuật máy đo được**. Ba lỗi Sếp bắt ngày 21/07 **không lỗi nào máy đo được**, mà mọi con số đều xanh. Trích 6-8 khung **ở 340px trở lên** rồi tự trả lời 5 câu trong `references/quy-trinh-chon-canh.md` mục 6: có cảnh nào thấy quen (lặp) không · có ai đang nói mà không nghe tiếng họ không · robot có phải nhân vật chính không · thẻ chữ có rơi đúng cảnh không · nhạc có át lời hoặc quá bé không. **Đừng báo "đạt chuẩn" khi mới chạy xong tầng kỹ thuật.**

   **3 phép rà bắt buộc thêm (bài học 19/07/2026 — Sếp bắt lỗi thật, xem `chon-canh-highlight.md` mục 3b + `style-voice-karaoke.md`):**
   - **Rà cutaway**: duyệt từng cảnh chèn, loại mọi cảnh có người đang nói/nhìn trực diện máy quay mà tiếng phát tại đó không phải giọng gốc đồng bộ của chính họ. Áp dụng cho CẢ 3 kiểu dựng (Sếp đã bắt lỗi này ở cả Kiểu 1 lẫn Kiểu 2C).
   - **Rà sub karaoke**: đọc soát toàn bộ sub Whisper trước khi burn, soi kỹ tên riêng + từ tiếng Anh (Roboworld, Tràng An, BellaBot, PUDU, Customize...) — 1 buổi từng có 11 lỗi nghe. Sửa theo VỊ TRÍ TỪ trong từng event, không thay cả dòng (mất tô màu).
   - **Rà biên cắt thoại**: mọi lát cắt "câu đứng riêng" phải cho Whisper nghe lại chính lát cắt đó xác nhận đủ chữ — khoảng im ≥0.3s có thể chỉ là MC ngắt hơi giữa câu (ca thật: cắt mất "BellaBot Pro").

8. **Lưu công thức dựng** (luật từ 19/07/2026): ghi lại toàn bộ chuỗi lệnh ffmpeg đã dùng thành `<workspace>\build.ps1` (kèm tên clip + mốc thời gian mỗi bước) — **không cần chạy lại tự động, chỉ để tham chiếu**. Lý do: khi Sếp yêu cầu sửa 1 lỗi cụ thể sau đó, có script gốc thì chỉ cần đọc + sửa 1 tham số; không có thì phải dò ngược bằng cách trích hàng loạt frame + đối chiếu timestamp thủ công (đã xảy ra thật ngày 19/07, rất tốn thời gian).

### Bước 5 — Bàn giao (LUÔN làm đủ cả 2 phần, không chỉ giao video)

1. **Caption**: tạo bộ caption cho TỪNG video theo đúng `references/caption-format.md` (5 phần: 10 hook, caption FB, footnote cố định, hashtag, từ khóa + hook YouTube) → lưu **`<folder buổi quay>\Final\video-N-<slug>-caption.md`**, đặt tên khớp đúng tên video để nhìn là biết caption của bài nào. Đây là phần bàn giao bắt buộc đi kèm video, không phải tùy chọn — thiếu caption coi như chưa xong việc.
2. `explorer "<folder buổi quay>\Final"` để mở folder hàng giao cho Sếp. **Trước khi mở, rà lại: trong `Final` chỉ được có .mp4 và .md — thấy thứ gì khác thì dọn về `Workspace\` ngay.**
3. Báo cáo: mỗi video ý tưởng gì, hook nào, thời lượng, cảnh đắt nhất; kèm nhận xét footage còn thiếu gì cho buổi quay sau.

## Quy chuẩn thành phẩm (theo video mẫu — chi tiết trong style-mau.md)

| Hạng mục | Chuẩn |
|---|---|
| Khung hình | 1080x1920 dọc (9:16), 30fps — đăng phủ mọi nền tảng (Reels/TikTok/Shorts) |
| Thời lượng | 30-60s |
| Font | **Anton** in hoa, viền/bóng đen (file trong assets/fonts của skill), có fade in/out nhẹ |
| Hook mở đầu | Vàng #FFD200, **130-135pt** (đã tăng 2 lần sau góp ý "chữ nhỏ" — luôn test render 1 frame trước khi dựng cả video, xem style-mau.md), 2-3 dòng, ngay dưới logo |
| Text nội dung | Trắng, **85-90pt**, 1-2 dòng, dưới logo, mỗi ý 3-8s |
| Logo | Trắng, giữa-trên, rộng ~480px, cách mép trên ~50px, hiện suốt PHẦN THÂN video, tự ẩn trước khi outro bắt đầu |
| Intro/Outro | Không dùng intro. **Outro dọc luôn có** (file có sẵn, nối bằng crossfade — mục 4d recipes) |
| Dấu câu | Viết gọn, không thừa dấu (vd "ROBOT?" chứ không "ROBOT?!") — rà lại trước khi burn text |
| Âm thanh | Nhạc nền là chính; âm gốc footage 0-30% khi có tiếng hay (robot, tiếng cười); **SFX: mỗi thẻ chữ 1 pop + SFX khớp hành động** (luật 19/07, xem mục Sound effect ở trên) |

## Xử lý sự cố nhanh

- **NGUYÊN TẮC ĐẦU TIÊN — Sếp chỉ định đích danh (voice ID, bài nhạc, clip cụ thể...) mà thao tác lỗi/bị chặn**: DỪNG, báo lỗi rõ ràng + nêu phương án, CHỜ Sếp quyết. Không tự chạy phương án thay thế khi chưa có lệnh (bài học 2026-07-13: tự thay giọng ElevenLabs bị Sếp nhắc).

- **ffmpeg lỗi filter trên Windows**: `Set-Location` vào workspace, dùng đường dẫn tương đối trong `ass=`/`fontsdir` — chi tiết trong recipes.
- **edge-tts (nếu dùng voiceover)**: tiếng Việt PHẢI truyền qua `--file` UTF-8, không dùng `--text`.
- **Tên file/folder tiếng Việt có dấu**: input đọc được bình thường, nhưng file TRUNG GIAN và workspace luôn đặt tên không dấu.
- **Nguồn HEVC/10-bit**: re-encode chuẩn hóa ngay ở bước cắt (recipes có lệnh).
- **Không chắc cỡ chữ có tràn viền không**: đừng đoán — render thử 1 frame với style dự kiến, Read xem, rồi mới dựng cả video (xem cách làm trong style-mau.md).

# Style "VOICE + NHẠC NỀN" (sub karaoke) — học từ video mẫu `HUY MKT\37.Tràng An thuê page RBW\Thuê 3.mp4`

Phân tích 2026-07-13 (45s, 2160x3840, 30fps, đo cỡ chữ bằng frame quy về 1080x1920 + lưới 50px). Dạng video: **MC nói trực tiếp / voiceover AI + sub karaoke từng từ + thẻ từ khóa + nhạc nền**. Khác hoàn toàn style "text + nhạc" (style-mau.md) — hỏi Sếp chọn style TRƯỚC khi viết kịch bản.

## Bố cục 3 tầng text (tọa độ theo khung 1080x1920)
<!-- tags: kieu-2, kieu-3 -->

| Tầng | Vị trí | Cỡ chữ (ASS, PlayResY 1920) | Style |
|---|---|---|---|
| Logo ROBOWORLD | giữa-trên, mép trên ~40-60px, rộng ~480px | — | trắng, nhỏ gọn |
| **Thẻ từ khóa** (keyword card) | y ≈ 320-460 (~17-24% chiều cao), giữa ngang | **95-100pt**, chữ ĐEN IN HOA | hộp NỀN VÀNG bo góc (cao ~140px, rộng theo chữ + padding ~60px); biến thể: nền đỏ chữ trắng cho ý nhấn mạnh (BELLABOT PRO, KHAI TRƯƠNG BÙNG NỔ) |
| **Sub karaoke** | tâm chữ ~80% chiều cao (baseline ~1555, Alignment 2 + MarginV ≈ 340-370) | **66pt** — GIỮ ĐÚNG cỡ này, đã đo từ video mẫu, KHÔNG tự phóng to | trắng bold, viền đen dày + bóng; **TỪ ĐANG NÓI tô VÀNG #FFD200**; mỗi cụm 1 dòng 2-4 từ, đổi theo giọng |

- Sub karaoke dùng font đậm bo tròn (video mẫu không phải Anton — Anton chỉ dùng cho thẻ từ khóa; sub dùng font sans đậm như Montserrat ExtraBold nếu có, không có thì Anton vẫn chấp nhận được).
- Cách làm karaoke bằng ASS: mỗi cụm 2-4 từ = 1 Dialogue; trong cụm, tô vàng từ hiện tại bằng nhiều event nối tiếp (mỗi event 1 trạng thái màu) theo word-timestamp — timing lấy từ `voice\*-words.json` (ElevenLabs) hoặc Whisper (giọng MC thật).

## Cấu trúc & nhịp (đo từ video mẫu 45s)
<!-- tags: kieu-2, kieu-3 -->

1. **Hook 0-2s**: hình "lạ mắt" gây tò mò (không phải cảnh sản phẩm), 2 cắt nhanh 0.8-1s
2. **Nêu vấn đề 2-9s**: MC + robot, chạm nỗi đau, thẻ từ khóa cảm xúc (ĐAU ĐẦU) + emoji đúng lúc lời nhắc tới
3. **Giới thiệu 9-16s**: ra mắt sản phẩm, thẻ tên sản phẩm + MŨI TÊN đỏ chỉ vào robot
4. **Chứng minh 16-30s**: B-roll thật mỗi cảnh **1.8-2.5s**, MỖI CẢNH 1 thẻ từ khóa lợi ích mới
5. **Chốt 30-37s**: MC nói 1 cảnh tĩnh dài được — NHƯNG thẻ từ khóa phải thay 2-3 lần (quy tắc vàng: **màn hình không được đứng yên quá ~2.5s** — hình không đổi thì chữ phải đổi)
6. **Outro 37.5-45s**: outro đỏ có sẵn

Nhịp cắt trung bình 2.6s/cảnh. Điểm nhấn thị giác rải đều: emoji bay vào (~90px, gần thẻ từ khóa), mũi tên chỉ, 1 hiệu ứng chớp trắng chuyển đoạn (4 cắt trong 0.25s) ở bước ngoặt giữa video.

## Âm thanh (chuẩn bắt buộc của style này)
<!-- tags: kieu-2, kieu-3 -->

- **Giọng là chủ, nhạc là nền**: nhạc nền volume ~0.12-0.18 khi có giọng, có thể nâng 0.35-0.5 ở khoảng nghỉ/hook không lời. Cách tự động: sidechain ducking —
  ```
  [nhac]volume=0.5[bg];[bg][voice]sidechaincompress=threshold=0.03:ratio=8:attack=20:release=350[bgduck]
  ```
  (nhạc tự chìm khi giọng nói, tự nổi khi giọng nghỉ). Đơn giản hơn: đặt volume nhạc cố định 0.15 nếu giọng nói liên tục cả video.
- **Chuẩn hóa loudness -14 LUFS (chuẩn YouTube), bước CUỐI CÙNG của chuỗi audio** sau khi mix xong mọi lớp:
  ```
  [mix]loudnorm=I=-14:TP=-1.5:LRA=11[aout]
  ```
  Nghiệm thu: đo lại bằng `ffmpeg -i final.mp4 -af loudnorm=I=-14:TP=-1.5:LRA=11:print_format=summary -f null -` — Input Integrated phải ra ≈ -14 (±1). Ghi kết quả đo vào báo cáo bàn giao.
- Giọng: ElevenLabs (scripts/elevenlabs_tts.py, xuất words.json làm karaoke) — giọng do Sếp chỉ định (4 giọng, xem `chon-kieu-dung.md`); lỗi/chặn thì **DỪNG BÁO và chờ quyết**. **KHÔNG có phương án thay thế** — edge-tts đã bị loại 22/07/2026 vì Sếp nghe thấy đọc méo.
- SFX theo **luật hiện hành 19/07/2026**: mỗi thẻ chữ 1 SFX "pop" hợp nghĩa + các SFX khớp hành động trong hình (mục 4b ffmpeg-recipes). *(Câu cũ ở đây ghi "vẫn theo nguyên tắc cũ, khớp hành động cụ thể" — đó là luật 03/07 đã bị bãi bỏ, sửa 21/07.)*

> ## 🔴 TRƯỚC KHI CHỌN NHẠC CHO KIỂU 2/3 — ĐỌC LUẬT NÀY
>
> **Nhạc cho Kiểu 2/3 KHÔNG chọn tự do.** Luật Sếp Huy 21/07/2026 chia 2 nhóm theo **mức phủ giọng**:
>
> | Nhóm | Khi nào | Nhạc |
> |---|---|---|
> | **A** — giọng dẫn **xuyên suốt** (MC nói cả bài, hoặc voice-over phủ phần lớn) | phần lớn video Kiểu 2/3 | **TUYỆT ĐỐI KHÔNG LỜI**, áp cho CẢ video kể cả đoạn cuối không ai nói. **CẤM folder `Nhạc hot`.** Không hỏi "trend hay không bản quyền" |
> | **B** — giọng chỉ **1-2 câu mở đầu** rồi im hẳn | ít gặp | Được nhạc có lời/nhạc hot. PHẢI hỏi "trend hay không bản quyền". Nhạc nhỏ 0.15-0.2 lúc nói → dâng ~0.55 đến hết (công thức ffmpeg-recipes mục 5b) |
>
> **Câu hỏi bắt buộc hỏi người dùng ngay khi chốt Kiểu 2 hoặc 3:**
> *"Video này giọng nói phủ tới đâu — dẫn xuyên suốt cả bài, hay chỉ 1-2 câu mở đầu rồi phần sau để cảnh robot chạy với nhạc?"*
>
> **Lý do**: hai giọng chồng nhau bắt tai người nghe chia sự chú ý, lời dẫn bị nuốt. **Hạ volume nhạc KHÔNG cứu được** — vấn đề là có 2 giọng, không phải nhạc to.
>
> **Không chắc bài có giọng hát không → kiểm bằng máy, đừng đoán theo tên file:**
> ```powershell
> python "<skill-dir>\scripts\kiem_nhac_co_loi.py" --folder "<thư mục nhạc>"
> ```
> Folder "nhạc không bản quyền" vẫn lẫn bài có lời (`POP tươi sáng` có ít nhất 2 bài hát thật).
>
> **Luật đầy đủ + bảng chi tiết**: `chon-kieu-dung.md` mục "Luật nhạc theo mức phủ giọng".
>
> *(Khối này thêm 21/07/2026 sau một ca thật: phiên dựng đọc đúng file này để làm Kiểu 2 + Kiểu 3, nhưng file khi đó không nhắc gì luật nhạc → chọn nhầm nhạc trend có lời đè lên giọng MC cho cả 2 video, phải mix lại. Luật có ở `chon-kieu-dung.md` là chưa đủ — người dựng Kiểu 2/3 mở thẳng file này.)*

## Quy tắc VOICE GỐC MC (format ③ — học từ lỗi video-3, 2026-07-13)
<!-- tags: kieu-2 -->

1. **Cấm ghép tiếng take A vào hình take B nếu trong hình có người đang nói** — dù là cùng câu kịch bản, nhịp 2 take khác nhau → lệch khẩu hình lộ liễu. Trước khi dùng 1 clip làm B-roll đè voice, PHẢI xem sheet xác nhận không ai trong hình đang nói (index tag `on-camera`/`noi-mic` = cảnh báo đỏ).
2. **Pattern chuẩn cho mỗi đoạn thoại**: mở bằng chính người nói trên hình 2-3s đầu (tiếng + hình CÙNG take → khớp môi tuyệt đối), sau đó mới cắt sang B-roll trong khi voice chạy tiếp. Voice-off 100% chỉ khi clip nguồn vốn là narration sau camera (0031/0039 kiểu lia kệ sách).
3. **Mốc transcript Whisper trong index chỉ để TÌM câu thoại, KHÔNG BAO GIỜ để cắt.**

   **CÔNG CỤ CHÍNH LẤY MỐC CẮT (chốt 21/07/2026, thay silencedetect):**

   ```powershell
   python "<skill-dir>\scripts\loc_thoai_that.py" <clip.mp4> --index <index.json>
   ```

   Nó đo trực tiếp trên âm thanh gốc 2 chỉ số: **mức so với sàn nhiễu của chính clip đó** (không dùng ngưỡng tuyệt đối — sàn nhiễu cả kho trải từ -20 đến -49 dB, mọi ngưỡng cố định đều sai) và **độ ấm** = 100-400Hz / 2-6kHz (giọng người gần mic thì ấm; loa robot, tiếng vọng từ xa thì mỏng và chói). Trả về từng đoạn kèm mốc vào/ra, cờ **XA MIC**, cờ **NGHI Ê-KÍP**, và tự chọn **bản take to nhất** khi MC nói lại nhiều lần.

   - **Cách sàn ≥ 15 dB** = nói vào máy, dùng được · **8-15 dB** = xa, cân nhắc · **< 8 dB** = không tính là thoại.
   - Nghiệm thu 21/07 trên 3 ca tai Sếp đã chấm: **đúng cả 3**.

   **Vì sao bỏ silencedetect làm công cụ chính** — ca thật cùng ngày: nhà sách Tràng An, `silencedetect` trả mốc **20.2s** trong khi câu MC thật sự bắt đầu **24.0s**. Nó chỉ nhìn TO/NHỎ, không nhìn CHẤT giọng, nên trong quán ồn nó bắt nhầm tiếng ồn nhấp nhô. Còn Whisper trả 19.99s — cũng sai, vì **Whisper nối đuôi các đoạn**: đoạn sau bắt đầu đúng chỗ đoạn trước kết thúc, nên mốc bắt đầu là số nối chứ không phải số đo. Dấu hiệu nhận ra: đoạn dài bất thường so với số chữ (10 giây cho câu 5 giây).

   ⛔ **Chạy script này TRƯỚC mọi bộ lọc.** Lọc ồn / `speechnorm` / `highpass` chạy trước sẽ phá hệ đo mà không báo lỗi — xem `ffmpeg-recipes.md` mục 5c.

   `silencedetect` giờ chỉ còn là **công cụ đối chiếu**, và chỉ tin khi nó thật sự tìm ra khoảng im:
   - **NHƯNG: khoảng im ≥0.3s KHÔNG chắc là hết câu** (bài học 19/07/2026, ca thật clip 0049): `silencedetect` báo im tại 21.38s nên biên cắt chốt ở đó — thực tế MC chỉ **ngắt hơi giữa câu**, cụm **"BellaBot Pro"** nằm ngay SAU đó và bị cắt mất, video thi giao đi thiếu nguyên tên sản phẩm. Biên đúng của 0049 là **19.10 → 23.06**.
   - **Luật bắt buộc**: với khối thoại định dùng làm "câu đứng riêng", sau khi chốt biên bằng silencedetect phải **cho Whisper nghe LẠI CHÍNH LÁT CẮT đó** xác nhận đủ chữ, đủ nghĩa rồi mới dùng. Cấm tin mỗi silencedetect. (Và cấm đi tắt bỏ qua silencedetect — 2 việc này bổ sung cho nhau, không thay thế nhau.)

   - **NGOẠI LỆ ĐÃ ĐO THẬT 21/07/2026 — môi trường ồn liên tục thì `silencedetect` VÔ DỤNG, không phải mình làm sai.**
     Ca thật: buổi quay trong nhà máy dập (folder 33, BG1 King Duan). Tiếng máy dập + gió vào mic làm **nền tiếng không bao giờ tụt xuống dưới ngưỡng**. Đo thật trên clip 0148: `mean_volume -16.6 dB`, và `silencedetect` trả **0 sự kiện ở MỌI ngưỡng đã thử: -27dB, -18dB, -15dB, -12dB** (d=0.25).
     **Dấu hiệu nhận biết sớm** — có 2 cách, dùng cách 1 trước vì nhanh hơn hẳn:
     1. **Đo sàn nhiễu (2 giây, biết trước khi thử lần nào)**: `loc_thoai_that.py` in ra `San nhieu`. **Sàn cao hơn -25 dB → silencedetect chắc chắn chết, bỏ qua luôn.** Đo thật: folder 33 sàn **-22.6 dB** (cao nhất cả kho) — đúng folder gây ra ca này. Nhà sách Tràng An sàn -38.6 dB, silencedetect vẫn chạy nhưng cho số SAI vì lý do khác (bắt nhầm tiếng ồn nhấp nhô).
     2. Cách cũ: chạy silencedetect trên 5-6 vùng khác nhau mà vùng nào cũng ra "không có khoảng im" → dừng ngay, đừng nới ngưỡng thêm.

     **Quy trình thay thế (đã dùng thật, chốt được đủ 6 lát trong 2 vòng):**
     1. Lấy mốc thô từ `transcript` trong `index.json`, cộng/trừ đệm ~0.3s.
     2. Cắt thử ra file `.wav` rồi **cho Whisper nghe lại chính lát cắt đó**.
     3. Đọc kết quả theo 3 dấu hiệu:
        - Câu **cụt giữa chừng / hết đột ngột** → biên PHẢI quá sớm, nới thêm.
        - **Bắt đầu bằng nửa từ** (vd nghe ra *"bước bg1"* trong khi lời thật là *"quan tâm đến PUDU BG1"*) → biên TRÁI quá muộn, lùi lại.
        - Xuất hiện **câu bịa** (xem mục "2 lỗi Whisper phải bắt bằng mắt") → đuôi lát cắt đang là ĐOẠN IM → cắt ngắn lại. **Đây là tín hiệu tốt, dùng nó để dò biên phải.**
     4. Lặp lại bước 2-3 cho tới khi nghe ra đủ câu, đủ nghĩa, không có câu bịa ở đuôi.

     **Kèm theo — Whisper nghe lát NGẮN kém hơn hẳn lát RỘNG** (cùng một đoạn tiếng): cắt 33.8→45.3 ra *"Về giá thì em nghĩ nó phải tương đương với lại trước xe ô tô đấy"*, nhưng nới thành 30.2→45.3 thì ra đúng *"Bên Roboworld mà em từng cung cấp, và giá thành của một chú robot này thì em nghĩ là nó phải tương đương với lại một chiếc xe ô tô đấy"*. **Whisper cần ngữ cảnh hai bên mới nghe đúng.**
     → Khi kiểm 1 lát nghi vấn, **nghe thử ở cửa sổ RỘNG hơn dự định trước** để biết lời thật là gì, rồi mới thu về biên cần dùng. Đừng vội kết luận "take này hỏng" chỉ vì lát hẹp nghe ra chữ vô nghĩa — rất dễ loại oan một take tốt.
3d. **TỐC ĐỘ NÓI — TUA NHANH tiếng đã thu cho đỡ nhàm (Sếp Huy 21/07/2026)**

> **Mục đích chính**: MC nói chậm làm video nhàm. Luật này để **tua nhanh tiếng MC/người thu ĐÃ QUAY**, không phải để chỉnh giọng máy. *(Bản đầu của mục này hiểu nhầm thành chỉnh TTS — Sếp đã đính chính.)*

### Cách đo — CẮT HẾT KHOẢNG TRỐNG cho khách quan (Sếp chỉ 21/07)
<!-- tags: kieu-2, kieu-3 -->

> *"Lấy đoạn nào nói liên tục, tính ra trung bình bao nhiêu chữ trên 1 phút, cắt hết những đoạn trống đi cho khách quan. Video sau này cũng đo tương tự, xong lấy 2 cái chia tỉ lệ rồi tua theo."*

**Vì sao phải cắt khoảng trống**: nhịp ngắt giữa câu khác nhau tuỳ người tuỳ kịch bản. Bỏ hết thì còn lại **tốc độ nhả chữ thuần** — so sánh hai file mới công bằng. Và chỉ cần **tỉ lệ**, không phụ thuộc con số tuyệt đối.

⚠️ **Đo khoảng trống bằng MỨC SO VỚI SÀN NHIỄU, không dùng `silencedetect`.** Đo thật: trên video MC nhà sách, `silencedetect` báo **0 giây trống** trong khi thực tế có **17.8 giây** không ai nói — vì ồn nền không bao giờ tụt đủ thấp.

**Mốc chuẩn: 363 chữ/phút.** File mẫu đo được **427** theo cách này; Sếp lấy **85%** vì mẫu gốc hơi nhanh.

```powershell
python "<skill-dir>\scripts\tua_nhanh_thoai.py" <clip> --am-tiet <đếm tay số chữ>
```

Script tự đo tốc độ hiện tại, tự chia tỉ lệ với mốc, rồi tua **cả hình lẫn tiếng cùng lúc**. Biết hệ số rồi thì `--he-so 1.24`.

**Kỹ thuật — 2 điều bắt buộc:**
- Tiếng dùng **`atempo`** (giữ nguyên cao độ). **Đừng dùng `asetrate`** — nó kéo cao độ lên, giọng thành the thé như vịt.
- Hình phải `setpts=PTS/<hệ số>` **cùng lúc**, không thì lệch tiếng.
- `atempo` chỉ nhận 0.5-2.0 mỗi lần → hệ số > 2 phải nối chuỗi `atempo=2.0,atempo=x`.

**Đo thật trên video-2 (MC nhà sách Tràng An, 133 chữ):**

| | Tổng | Đang nói | Trống | Chữ/phút |
|---|---|---|---|---|
| File mẫu | 15.70s | 11.80s | 3.90s | **427** |
| MC video-2 | 45.12s | 27.30s | **17.82s** | **292** |

→ Mục tiêu 363 ÷ 292 = **hệ số 1.24×** → video 45.1s rút còn **36.4s** (ngắn hơn 19%).

⚠️ **Ngưỡng an toàn đang đặt 1.6× — con số này do tôi phán đoán, CHƯA qua tai Sếp chấm.** Trên mức đó script vẫn chạy nhưng in cảnh báo. Mẫu để nghe: Desktop, thư mục `NGHE-CHON-TOC-DO`. Sếp chốt mức nào thì sửa `TOI_DA` trong script.

> **Đừng trộn 2 cách đo.** Cách cũ (khoảng từ chữ đầu đến chữ cuối, có tính nhịp ngắt) cho mẫu **342** và MC **178**; cách mới (cắt hết khoảng trống) cho **427** và **292**. Hai cách ra hai bộ số khác hẳn — hệ số tính ra chênh nhau 1.24× vs 1.64×. **Luôn đo cả hai bên bằng cùng một cách.**

🔴 **TUA TRƯỚC KHI CẮT CẢNH VÀ ĐẶT CHỮ.** Tua xong thì mọi mốc thoại đều đổi — sub, thẻ chữ, SFX phải làm lại theo mốc mới. Tua sau là hỏng hết timing.

```powershell
python "<skill-dir>\scripts\do_toc_do_noi.py" <file voice hoac video>
```

Script tự nghe bằng Whisper, đếm âm tiết, chia cho khoảng từ chữ đầu tới chữ cuối, rồi so với mốc 338 và **gợi ý luôn cần tăng `--rate` bao nhiêu** nếu là giọng máy.

**Cách đo (chốt 1 cách duy nhất)**: `âm tiết ÷ (mốc chữ cuối − mốc chữ đầu) × 60`. Mẫu số **tính cả nhịp ngắt tự nhiên** — vì tai người cảm nhận nhịp nghỉ là một phần của tốc độ. *(Trừ hết khoảng lặng thì con số bị thổi phồng: cùng 1 file ra 338 hay 452 tuỳ cách tính.)*

⚠️ **Phép đo KHÔNG ổn định trên file dưới ~10 giây** — cùng một file TTS 6.6s, Whisper lúc nhận 14 âm tiết lúc 23. Với giọng máy thì **đếm tay số âm tiết trong kịch bản rồi chia cho độ dài file** chắc hơn (mình biết chính xác lời).

### ⛔ Mức giọng máy edge-tts `--rate=+41%` — ĐÃ BỎ 22/07/2026, GIỮ ĐỂ TRA CỨU
<!-- tags: lich-su -->

> 🔴 **edge-tts ĐÃ BỎ 22/07/2026 — Sếp Huy nghe mẫu và kết luận ĐỌC MÉO, không dùng được.**
> Mọi hướng dẫn edge-tts bên dưới **chỉ còn giá trị tra cứu lịch sử**, KHÔNG được dùng để tạo giọng đọc video nữa.
> ElevenLabs lỗi/bị chặn → **DỪNG và BÁO người dùng**, chờ quyết. Không tự lui về giọng miễn phí.
> Giọng đang dùng: 4 giọng ElevenLabs, xem `references/chon-kieu-dung.md` khối "Chọn giọng đọc".
> Ca này đáng nhớ: Whisper nghe lại 2 giọng miễn phí ra **đúng nguyên câu, chuẩn 100%** — máy chấm đạt, tai Sếp nghe méo ngay.

> ⚠️ **Mốc `+41%` không chuyển sang giọng ElevenLabs được** — nó đo trên edge-tts. ElevenLabs chỉnh tốc độ bằng `voice_settings.speed`, **chưa đo mốc chuẩn**. Cần thì đo lại bằng `do_toc_do_noi.py`.


> **Đây là GIỌNG MÁY TẠO MỚI (edge-tts), khác hẳn việc TUA tiếng đã thu ở mục 3d bên trên.** Đừng lẫn: tua tiếng thu dùng `tua_nhanh_thoai.py`; tạo giọng máy dùng `edge-tts --rate`.

**Diễn biến**: ban đầu chốt `+76%` để khớp đúng tốc độ file mẫu (342 chữ/phút). Nhưng Sếp nghe Video 3 ở `+76%` thấy **hơi nhanh**, chỉnh xuống **còn 80%** tốc độ đó.

```powershell
edge-tts --voice vi-VN-NamMinhNeural --rate=+41% --file <loi.txt> --write-media <out.mp3>
```

Đo thật (giọng `vi-VN-NamMinhNeural`): `+76%` = 471 chữ/phút → **80% = 378** → `+41%` cho ra **378** ✅ (đúng 80%).

⚠️ **Con số `+41%` chỉ đúng cho giọng `vi-VN-NamMinhNeural`.** Đổi giọng (HoaiMy, hay giọng ElevenLabs khi lên gói trả phí) thì **phải đo lại**: sinh thử → `do_toc_do_noi.py` → chỉnh `--rate` cho tới khi ra ~80% của tốc độ mẫu.

*(Lịch sử để tham chiếu: `+76%` là mức khớp mẫu 342 nếu muốn nhanh bằng MC hiện trường; `+41%` là mức Sếp thấy dễ nghe hơn cho giọng máy. Mặc định dùng +41%.)*

**Bẫy khi so tốc độ — dễ ra kết luận sai**: phải đo hai bên **cùng một thước**. Ban đầu đã so nhầm — mẫu đo theo *khoảng từ chữ đầu đến chữ cuối*, còn giọng máy lại tính theo *cả độ dài file* (gồm khoảng lặng đầu/cuối). Cùng một file `+45%` ra **272** hay **311** tuỳ cách tính — lệch đủ để chỉnh sai hẳn một mức.

4. **Sau khi ghép voice track, chạy Whisper lại trên chính track thành phẩm** để lấy mốc sub thật — không đặt sub theo tỉ lệ ước lượng.
5. **Transcript sạch KHÔNG có nghĩa là take sạch** (bài học lần 2, video-3: đoạn 0039 văn bản đọc ổn nhưng tai nghe là take lỗi). Quy tắc chọn take: (a) câu có NHIỀU take → lấy take CUỐI (thường là bản đạt); (b) câu chỉ có 1 take duy nhất, nhất là dạng voice-off narration → xếp loại NGHI VẤN; (c) văn bản có từ lặp/chèn bất thường ("tiếp tục *lại* làm việc", "à à", từ đệm) = dấu hiệu vấp, tránh dùng; (d) khi trình kịch bản duyệt, LIỆT KÊ RÕ các take thuộc diện nghi vấn để Sếp nghe kiểm chứng đúng đoạn đó trước khi dựng — tai người là bộ lọc cuối, transcript không thay được.

6. **Sub karaoke do Whisper sinh ra PHẢI rà tay từng cụm trước khi burn** (bài học 19/07/2026 — 1 buổi dựng bắt **11 lỗi nghe** trong sub tự động). Whisper nghe tiếng Việt sai nhiều nhất ở **tên riêng, tên thương hiệu và thuật ngữ tiếng Anh** — đúng những chữ không được phép sai:

   | Whisper nghe ra | Đúng phải là |
   |---|---|
   | hội trợ | hội chợ |
   | danh số | doanh số |
   | Automate | Customize |
   | Piri | PG |
   | Trà Ngan | Tràng An |
   | Full Ngoan | Fanpage Roboworld |

   **Cách vá mà KHÔNG mất tô màu karaoke**: file .ass karaoke chia chữ theo từng event có tag `\k`, nên **không được thay cả dòng** — phải sửa **đúng từ theo VỊ TRÍ TỪ trong từng event**, giữ nguyên số cụm và các mốc `\k`. Thay cả dòng là mất đồng bộ tô màu toàn câu.

   Rà bắt buộc trước khi burn: đọc soát toàn bộ sub, soi kỹ mọi tên riêng (Roboworld, Tràng An, BellaBot, PUDU, tên khách hàng) và mọi từ tiếng Anh.

   **CÁCH VÁ (bài học 20/07/2026 — lần đầu vá hụt mất nửa số dòng)**: trong file .ass karaoke, **tag màu `{\c...}` nằm CHEN GIỮA các từ** (vd `nhà sách {\c&H00D2FF&}Trang{\c&HFFFFFF&} An`) → tìm chuỗi liên tục `"Trang An"` sẽ **sót** đúng những dòng đang tô từ đó. Phải thay theo **TOKEN TỪ** (regex biên từ) trên cả dòng, mới quét đủ mọi event.

   **2 lỗi Whisper phải bắt bằng mắt, không có cách tự động (20/07/2026)**:
   - **Whisper BỊA chữ trên đoạn im**: đoạn không có tiếng hay bị gán câu quảng cáo YouTube ("Hãy subscribe cho kênh Ghiền Mì Gõ...", "Cảm ơn các bạn đã theo dõi") — đây KHÔNG phải thoại thật, thấy là xoá.

     **Bộ câu bịa đã gặp thật — dùng làm danh sách nhận diện (bổ sung 21/07/2026):**
     | Nghe tiếng Việt | Nghe tiếng Anh (`language=en`, hay gặp khi cho nghe NHẠC) |
     |---|---|
     | "Hãy subscribe cho kênh Ghiền Mì Gõ" · "Để không bỏ lỡ những video hấp dẫn" · "Cảm ơn các bạn đã theo dõi" · "Các bạn hãy đăng ký kênh để ủng hộ kênh của chúng tôi nhé" | "Thank you." · "Bye." · "you" · "*music*" · "Applause" · "Please subscribe" |

     **Hai cách dùng danh sách này:**
     1. **Lọc bỏ** trước khi làm sub — đây không phải lời thật.
     2. **Dùng làm tín hiệu**: câu bịa xuất hiện ở ĐUÔI một lát cắt = đuôi đó đang là đoạn im → biên phải đang quá dài, cắt ngắn lại (xem quy trình dò biên ở mục 3).

     ⚠️ **Cảnh báo ngược — đừng chấm "có lời" chỉ vì Whisper trả về nhiều chữ.** Ca thật 21/07: cho Whisper nghe 6 bản nhạc để lọc bài có giọng hát, bài KHÔNG LỜI vẫn trả về đầy chữ ("Thank you. Bye. Bye. *music*...") nên bị chấm nhầm là "có giọng hát" cả 6/6. **Phải lọc bộ câu bịa ở trên ra trước, phần còn lại mới là lời hát thật.** Có script làm sẵn việc này: `scripts/kiem_nhac_co_loi.py` (xem `style-mau.md`).
   - **Whisper GÁN NHẦM câu vào đoạn B-roll không tiếng**: ca thật video K2 — cụm "Chính xác luôn" bị kéo dài **19.93 → 31.53 (12 giây)** phủ hết đoạn B-roll, trong khi câu đó thực tế nằm ở giây 29.6. Cách sửa: dồn lại đúng mốc cảnh có thoại, giữ nguyên số event + tag màu.

## LUẬT VIẾT LỜI CHO GIỌNG AI (Kiểu 3) — đo thật 20/07/2026
<!-- tags: kieu-3 -->

**Mọi giọng TTS hiện có đều đọc SAI tên thương hiệu và thuật ngữ nước ngoài.** Đã kiểm chứng khách quan bằng cách cho Whisper nghe lại bản đọc:

| Giọng | Kết quả |
|---|---|
| **ElevenLabs "George"** (giọng mặc định trong skill, `JBFqnCBsd6RMkjVDRZzb`) | **KHÔNG dùng được cho tiếng Việt** — là giọng Anh, đọc tiếng Việt méo cả câu thường: "Thử cách này" → nghe ra *"Thú káč nai"*, "Khai trương thì bùng nổ doanh số" → *"Cái truong thị bùng no đoàn so"*. Chỉ dùng George khi lời đọc là tiếng Anh. |
| **edge-tts `vi-VN-NamMinhNeural`** (giọng Việt, miễn phí) | Câu tiếng Việt thuần đọc **sạch**. Nhưng từ nước ngoài vẫn sai: "thuê PG" → *"thuê pin"*, "BellaBot Pro" → *"Bella Popper"*, "banner" → *"BN"*, "đề can" → *"DK"*, "Roboworld" → *"Robo uống"*. |
| Viết phiên âm ("Bê la Bốt Pro") | **TỆ HƠN** — ra *"B là bố"*. Đừng chữa bằng phiên âm. |

**→ LUẬT: lời cho giọng AI chỉ viết TIẾNG VIỆT THUẦN. Tên sản phẩm, thông số, tên thương hiệu, từ tiếng Anh → ĐẨY LÊN THẺ CHỮ trên hình, không cho TTS đọc.** Vừa chắc đúng, vừa dễ nhớ hơn cho người xem. Ví dụ đã dùng thật (video K3 20/07): voice đọc *"một em robot phục vụ sự kiện"* + thẻ chữ **BELLABOT PRO**; voice đọc *"màn hình quảng cáo lớn, di động"* + thẻ chữ **MÀN HÌNH 18.5 INCH**; voice đọc *"nhắn tin ngay cho chúng tôi"* + thẻ chữ **INBOX ROBOWORLD**.

**Mẹo kèm theo**:
- Sub karaoke cho Kiểu 3 nên **sinh từ CHÍNH LỜI GỐC đã viết + mốc câu của TTS** (edge-tts xuất kèm file `.srt`), **không cho Whisper nghe lại rồi làm sub** — lời gốc thì chắc chắn đúng chữ, Whisper thì thêm lỗi nghe.
- **edge-tts báo `NoAudioReceived` là lỗi TẠM của dịch vụ Microsoft**, không phải sai tham số — cứ thử lại 2-3 lần là chạy (đã dính 20/07, lần 1 hỏng, lần 2 OK). Nhớ kiểm dung lượng file > 10KB rồi mới dùng, kẻo dựng nhầm file rỗng.
- Trước khi dựng, **luôn cho Whisper nghe lại bản TTS** để bắt từ đọc sai — rẻ và nhanh hơn nhiều so với phát hiện sau khi đã dựng xong.

## Khi nào KHÔNG dùng karaoke tô màu (rút từ khảo sát 2026-07-15, 10 folder HUY MKT)
<!-- tags: kieu-2, kieu-3 -->

So sánh video hướng dẫn kỹ thuật (`28.Hướng dẫn sử dụng SH1`, `30.Hướng dẫn vs SH1` — nhân viên thao tác trực tiếp + tự thuyết minh) với video marketing/review (`34.Nhà sách Tràng An`, nhóm ADS) cho thấy 2 mục đích dùng 2 kiểu phụ đề khác nhau:

- **Video hướng dẫn/kỹ thuật** (dạy thao tác, các bước vận hành): phụ đề **trắng thường, KHÔNG tô màu karaoke** — ưu tiên dễ đọc/theo dõi từng bước hơn là bắt mắt.
- **Video marketing/review/quảng cáo** (mục đích thu hút, chốt hành động): dùng karaoke tô màu như mô tả ở trên.

Quy tắc chọn: hỏi mục đích video trước khi chọn — nếu Sếp mô tả là "hướng dẫn dùng/sửa/vệ sinh máy" → mặc định phụ đề trắng thường; các mục đích khác (review, quảng cáo, giới thiệu) → mặc định karaoke tô màu như spec chính ở trên.

**Nhịp dựng video hướng dẫn kỹ thuật khác hẳn mọi style khác** (đo bằng scene_changes trên 2 video mẫu 28+30, xác nhận lại bằng lưới dày fps=8 tại vài mốc): trung bình **32-248 giây/cảnh** — gần như 1 cú máy liên tục, camera pan/zoom theo tay người thao tác thay vì cắt dựng. Ngược hẳn với mọi style marketing khác (1.8-4s/cảnh). Áp dụng: khi Sếp yêu cầu video hướng dẫn kỹ thuật, ĐỪNG cắt vụn theo thói quen "3-5s/cảnh" của style ① — giữ cảnh dài, để hành động thật của người thao tác dẫn dắt, chỉ cắt khi đổi hẳn góc quay/công đoạn.

## Biến thể "montage nhiều địa điểm" (voice over kể chuyện diện rộng)
<!-- tags: kieu-3 -->

Khác với video mẫu gốc (1 sản phẩm, đào sâu tính năng), một số video voice-over trong HUY MKT (`10.Vinschool-01`, `12.BV Phúc Yên`, `16.GGG SG1`) kể chuyện theo hướng **"xuất hiện ở nhiều nơi/nhiều bối cảnh"** — cắt qua nhiều địa điểm/sự kiện khác nhau dưới 1 lời dẫn xuyên suốt, KHÔNG có 1 người cố định lên hình. Nhịp cắt vừa phải (3.5-4.1s/cảnh, nhanh hơn hướng dẫn kỹ thuật nhưng chậm hơn ADS chuyên nghiệp). Dùng khi mục đích là chứng minh độ phủ/uy tín ("đã triển khai ở đây, ở đây, ở đây") thay vì bán 1 sản phẩm cụ thể. Karaoke sub như spec chính. Kết thúc bằng outro logo animation có sẵn (xem `style-mau.md` mục Outro).

## Nghiệm thu riêng cho style này (thêm vào checklist chung)
<!-- tags: kieu-2, kieu-3 -->

- Trích frame tại 2-3 mốc có sub: từ vàng phải đúng từ đang đọc (đối chiếu words.json), sub không đè lên thẻ từ khóa/logo
- Đo loudness ra ≈ -14 LUFS
- Rà timeline: không khoảng nào màn hình đứng yên quá 2.5s (không cắt cảnh thì phải có thẻ/emoji đổi)

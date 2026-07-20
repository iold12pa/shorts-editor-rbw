# Style "VOICE + NHẠC NỀN" (sub karaoke) — học từ video mẫu `HUY MKT\37.Tràng An thuê page RBW\Thuê 3.mp4`

Phân tích 2026-07-13 (45s, 2160x3840, 30fps, đo cỡ chữ bằng frame quy về 1080x1920 + lưới 50px). Dạng video: **MC nói trực tiếp / voiceover AI + sub karaoke từng từ + thẻ từ khóa + nhạc nền**. Khác hoàn toàn style "text + nhạc" (style-mau.md) — hỏi Sếp chọn style TRƯỚC khi viết kịch bản.

## Bố cục 3 tầng text (tọa độ theo khung 1080x1920)

| Tầng | Vị trí | Cỡ chữ (ASS, PlayResY 1920) | Style |
|---|---|---|---|
| Logo ROBOWORLD | giữa-trên, mép trên ~40-60px, rộng ~480px | — | trắng, nhỏ gọn |
| **Thẻ từ khóa** (keyword card) | y ≈ 320-460 (~17-24% chiều cao), giữa ngang | **95-100pt**, chữ ĐEN IN HOA | hộp NỀN VÀNG bo góc (cao ~140px, rộng theo chữ + padding ~60px); biến thể: nền đỏ chữ trắng cho ý nhấn mạnh (BELLABOT PRO, KHAI TRƯƠNG BÙNG NỔ) |
| **Sub karaoke** | tâm chữ ~80% chiều cao (baseline ~1555, Alignment 2 + MarginV ≈ 340-370) | **66pt** — GIỮ ĐÚNG cỡ này, đã đo từ video mẫu, KHÔNG tự phóng to | trắng bold, viền đen dày + bóng; **TỪ ĐANG NÓI tô VÀNG #FFD200**; mỗi cụm 1 dòng 2-4 từ, đổi theo giọng |

- Sub karaoke dùng font đậm bo tròn (video mẫu không phải Anton — Anton chỉ dùng cho thẻ từ khóa; sub dùng font sans đậm như Montserrat ExtraBold nếu có, không có thì Anton vẫn chấp nhận được).
- Cách làm karaoke bằng ASS: mỗi cụm 2-4 từ = 1 Dialogue; trong cụm, tô vàng từ hiện tại bằng nhiều event nối tiếp (mỗi event 1 trạng thái màu) theo word-timestamp — timing lấy từ `voice\*-words.json` (ElevenLabs) hoặc Whisper (giọng MC thật).

## Cấu trúc & nhịp (đo từ video mẫu 45s)

1. **Hook 0-2s**: hình "lạ mắt" gây tò mò (không phải cảnh sản phẩm), 2 cắt nhanh 0.8-1s
2. **Nêu vấn đề 2-9s**: MC + robot, chạm nỗi đau, thẻ từ khóa cảm xúc (ĐAU ĐẦU) + emoji đúng lúc lời nhắc tới
3. **Giới thiệu 9-16s**: ra mắt sản phẩm, thẻ tên sản phẩm + MŨI TÊN đỏ chỉ vào robot
4. **Chứng minh 16-30s**: B-roll thật mỗi cảnh **1.8-2.5s**, MỖI CẢNH 1 thẻ từ khóa lợi ích mới
5. **Chốt 30-37s**: MC nói 1 cảnh tĩnh dài được — NHƯNG thẻ từ khóa phải thay 2-3 lần (quy tắc vàng: **màn hình không được đứng yên quá ~2.5s** — hình không đổi thì chữ phải đổi)
6. **Outro 37.5-45s**: outro đỏ có sẵn

Nhịp cắt trung bình 2.6s/cảnh. Điểm nhấn thị giác rải đều: emoji bay vào (~90px, gần thẻ từ khóa), mũi tên chỉ, 1 hiệu ứng chớp trắng chuyển đoạn (4 cắt trong 0.25s) ở bước ngoặt giữa video.

## Âm thanh (chuẩn bắt buộc của style này)

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
- Giọng: ElevenLabs (scripts/elevenlabs_tts.py, xuất words.json làm karaoke) — giọng do Sếp chỉ định; lỗi/chặn thì DỪNG BÁO, fallback edge-tts chỉ khi Sếp đồng ý (edge-tts không có word-timestamp chuẩn từng từ, sub karaoke sẽ kém chính xác hơn — nói rõ điều này khi xin ý kiến).
- SFX vẫn theo nguyên tắc cũ (khớp hành động cụ thể, mục 4b ffmpeg-recipes).

## Quy tắc VOICE GỐC MC (format ③ — học từ lỗi video-3, 2026-07-13)

1. **Cấm ghép tiếng take A vào hình take B nếu trong hình có người đang nói** — dù là cùng câu kịch bản, nhịp 2 take khác nhau → lệch khẩu hình lộ liễu. Trước khi dùng 1 clip làm B-roll đè voice, PHẢI xem sheet xác nhận không ai trong hình đang nói (index tag `on-camera`/`noi-mic` = cảnh báo đỏ).
2. **Pattern chuẩn cho mỗi đoạn thoại**: mở bằng chính người nói trên hình 2-3s đầu (tiếng + hình CÙNG take → khớp môi tuyệt đối), sau đó mới cắt sang B-roll trong khi voice chạy tiếp. Voice-off 100% chỉ khi clip nguồn vốn là narration sau camera (0031/0039 kiểu lia kệ sách).
3. **Mốc transcript Whisper trong index chỉ để TÌM câu thoại, không phải để cắt** — trước khi cắt phải đo lại biên bằng `silencedetect=noise=-27dB:d=0.3` trên đúng vùng đó (Whisper hay tính cả khoảng lặng/hơi thở, có khi lệch nguyên một take).
   - **NHƯNG: khoảng im ≥0.3s KHÔNG chắc là hết câu** (bài học 19/07/2026, ca thật clip 0049): `silencedetect` báo im tại 21.38s nên biên cắt chốt ở đó — thực tế MC chỉ **ngắt hơi giữa câu**, cụm **"BellaBot Pro"** nằm ngay SAU đó và bị cắt mất, video thi giao đi thiếu nguyên tên sản phẩm. Biên đúng của 0049 là **19.10 → 23.06**.
   - **Luật bắt buộc**: với khối thoại định dùng làm "câu đứng riêng", sau khi chốt biên bằng silencedetect phải **cho Whisper nghe LẠI CHÍNH LÁT CẮT đó** xác nhận đủ chữ, đủ nghĩa rồi mới dùng. Cấm tin mỗi silencedetect. (Và cấm đi tắt bỏ qua silencedetect — 2 việc này bổ sung cho nhau, không thay thế nhau.)
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
   - **Whisper GÁN NHẦM câu vào đoạn B-roll không tiếng**: ca thật video K2 — cụm "Chính xác luôn" bị kéo dài **19.93 → 31.53 (12 giây)** phủ hết đoạn B-roll, trong khi câu đó thực tế nằm ở giây 29.6. Cách sửa: dồn lại đúng mốc cảnh có thoại, giữ nguyên số event + tag màu.

## LUẬT VIẾT LỜI CHO GIỌNG AI (Kiểu 3) — đo thật 20/07/2026

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

So sánh video hướng dẫn kỹ thuật (`28.Hướng dẫn sử dụng SH1`, `30.Hướng dẫn vs SH1` — nhân viên thao tác trực tiếp + tự thuyết minh) với video marketing/review (`34.Nhà sách Tràng An`, nhóm ADS) cho thấy 2 mục đích dùng 2 kiểu phụ đề khác nhau:

- **Video hướng dẫn/kỹ thuật** (dạy thao tác, các bước vận hành): phụ đề **trắng thường, KHÔNG tô màu karaoke** — ưu tiên dễ đọc/theo dõi từng bước hơn là bắt mắt.
- **Video marketing/review/quảng cáo** (mục đích thu hút, chốt hành động): dùng karaoke tô màu như mô tả ở trên.

Quy tắc chọn: hỏi mục đích video trước khi chọn — nếu Sếp mô tả là "hướng dẫn dùng/sửa/vệ sinh máy" → mặc định phụ đề trắng thường; các mục đích khác (review, quảng cáo, giới thiệu) → mặc định karaoke tô màu như spec chính ở trên.

**Nhịp dựng video hướng dẫn kỹ thuật khác hẳn mọi style khác** (đo bằng scene_changes trên 2 video mẫu 28+30, xác nhận lại bằng lưới dày fps=8 tại vài mốc): trung bình **32-248 giây/cảnh** — gần như 1 cú máy liên tục, camera pan/zoom theo tay người thao tác thay vì cắt dựng. Ngược hẳn với mọi style marketing khác (1.8-4s/cảnh). Áp dụng: khi Sếp yêu cầu video hướng dẫn kỹ thuật, ĐỪNG cắt vụn theo thói quen "3-5s/cảnh" của style ① — giữ cảnh dài, để hành động thật của người thao tác dẫn dắt, chỉ cắt khi đổi hẳn góc quay/công đoạn.

## Biến thể "montage nhiều địa điểm" (voice over kể chuyện diện rộng)

Khác với video mẫu gốc (1 sản phẩm, đào sâu tính năng), một số video voice-over trong HUY MKT (`10.Vinschool-01`, `12.BV Phúc Yên`, `16.GGG SG1`) kể chuyện theo hướng **"xuất hiện ở nhiều nơi/nhiều bối cảnh"** — cắt qua nhiều địa điểm/sự kiện khác nhau dưới 1 lời dẫn xuyên suốt, KHÔNG có 1 người cố định lên hình. Nhịp cắt vừa phải (3.5-4.1s/cảnh, nhanh hơn hướng dẫn kỹ thuật nhưng chậm hơn ADS chuyên nghiệp). Dùng khi mục đích là chứng minh độ phủ/uy tín ("đã triển khai ở đây, ở đây, ở đây") thay vì bán 1 sản phẩm cụ thể. Karaoke sub như spec chính. Kết thúc bằng outro logo animation có sẵn (xem `style-mau.md` mục Outro).

## Nghiệm thu riêng cho style này (thêm vào checklist chung)

- Trích frame tại 2-3 mốc có sub: từ vàng phải đúng từ đang đọc (đối chiếu words.json), sub không đè lên thẻ từ khóa/logo
- Đo loudness ra ≈ -14 LUFS
- Rà timeline: không khoảng nào màn hình đứng yên quá 2.5s (không cắt cảnh thì phải có thẻ/emoji đổi)

# Sổ tay ffmpeg cho shorts Roboworld

Đọc file này trước khi dựng video đầu tiên trong phiên. Mọi lệnh viết cho PowerShell trên Windows.

## 0. Quy tắc chung (đọc kỹ — tránh 90% lỗi)

1. **Luôn `Set-Location` vào workspace rồi dùng đường dẫn tương đối** trong các filter (`subtitles=`, `movie=`). Filter ffmpeg trên Windows hỏng với đường dẫn tuyệt đối vì dấu `:` — `C:\...` bị hiểu là tham số filter.
2. Nếu `ffmpeg` không có trên PATH của shell, đọc `ffmpeg_path` trong `config.json` (cùng thư mục SKILL.md) rồi đặt biến ở đầu mỗi lệnh, vd:
   ```powershell
   $FF = "<gia tri ffmpeg_path trong config.json>"
   ```
   (`config.json` mặc định để trống — chỉ cần điền khi ffmpeg không có sẵn trên PATH hệ thống, xem ghi chú trong chính file đó)
3. File trung gian đặt trong `temp\`, đặt tên có số thứ tự (`s01.mp4`, `s02.mp4`...) đúng thứ tự kịch bản.
   - **Đường dẫn chứa ngoặc vuông `[ ]` — ĐO LẠI CHÍNH XÁC 20/07/2026** (bản ghi 19/07 nói "ffmpeg cũng hỏng" là **SAI**, đã kiểm chứng lại trên folder thật `05.An Phát Xanh\[24.04.26] Bàn giao MT1...`):

     | Cách gọi | Path có `[ ]` | Cách xử lý |
     |---|---|---|
     | `ffmpeg -i "<path>"`, `ffprobe` | ✅ **CHẠY BÌNH THƯỜNG** | không phải làm gì |
     | concat demuxer (file list) | ✅ chạy bình thường | không phải làm gì |
     | Python `glob.glob` | ❌ trả **rỗng**, lỗi IM LẶNG | `glob.escape(dir)` — hoặc dùng `os.walk`/`os.listdir` |
     | PowerShell `Get-ChildItem` | ❌ trả **0 file** dù thư mục có file | thêm **`-LiteralPath`** |
     | **PowerShell `Copy-Item` / `Move-Item` / `Test-Path` / `Remove-Item`** | ❌ **báo "No such file or directory"** dù file có thật | thêm **`-LiteralPath`** (bổ sung 21/07/2026) |

     > **Bổ sung 21/07/2026 — luật đúng là: MỌI cmdlet PowerShell nhận tham số `-Path` đều diễn giải `[ ]` là ký tự đại diện (wildcard), không riêng `Get-ChildItem`.** Ca thật: copy 1 file nhạc tên `...Orinn Mix [doan hay].mp3` bằng `Copy-Item -Path` → báo *"No such file or directory"*, tưởng thiếu file trong kho, suýt đi tải lại cả kho. Đổi sang `-LiteralPath` là chạy ngay.
     > **Cách nhớ gọn**: file/thư mục của Sếp rất hay có `[ ]` (tên buổi quay, tên bài nhạc tách từ mix) → **mặc định dùng `-LiteralPath` cho mọi cmdlet thao tác file**, chỉ bỏ ra khi thật sự cần wildcard.

     → **KHÔNG cần copy footage ra đường dẫn sạch** (bản ghi cũ khuyên vậy, làm mất công copy hàng GB vô ích). Chỉ cần dùng đúng hàm liệt kê file. Riêng path nằm **trong filter** (`ass=`, `subtitles=`, `movie=`) vẫn phải escape dấu `:` như quy tắc 0.1 — lỗi đó do dấu hai chấm, không liên quan ngoặc vuông.
4. Mọi file trung gian encode cùng một chuẩn (1080x1920, 30fps, h264, yuv420p, aac 48kHz) — concat mới không lỗi.
5. File text cho ffmpeg (concat list, .ass, .srt) ghi bằng **UTF-8** — PowerShell `Out-File` mặc định UTF-16 sẽ hỏng; luôn dùng `-Encoding utf8` hoặc viết bằng tool Write.
6. **Chọn encoder cho CẢ PHIÊN (GPU nếu có)** — chạy đúng 1 lần ở đầu phiên dựng, rồi dùng thống nhất cho mọi lệnh (quy tắc 0.4 cần các segment trung gian cùng chuẩn để `concat -c copy`):
   ```powershell
   ffmpeg -hide_banner -loglevel error -f lavfi -i color=c=black:s=256x256:d=1 -c:v h264_nvenc -f null -; $LASTEXITCODE
   ```
   - Exit `0` → máy có card NVIDIA dùng được: file trung gian (`temp\sNN.mp4`, ghép, xfade) dùng `-c:v h264_nvenc -preset p5 -rc vbr -cq 19 -b:v 0 -pix_fmt yuv420p` thay cho `libx264 -crf 18`; file final giữ `libx264 -crf 20` nếu muốn chắc chất lượng, hoặc `h264_nvenc -cq 18` (đủ cho social 1080x1920). **NVENC dùng `-cq`, KHÔNG có `-crf` — đừng trộn 2 cờ.**
   - Exit khác 0 (máy không có card NVIDIA, hoặc driver cũ — lỗi thường gặp: "Driver does not support the required nvenc API version") → giữ nguyên `libx264` như mọi lệnh mẫu bên dưới, không hỏng gì. **KHÔNG tin danh sách `ffmpeg -encoders`** — bản ffmpeg nào cũng liệt kê nvenc kể cả máy không chạy được; chỉ tin test-encode thật ở trên.
   - **Probe fail nhưng máy CÓ card NVIDIA** (gõ `nvidia-smi` thấy tên card): chạy `python "<skill-dir>\scripts\cai_driver_nvidia.py" --check` — nếu báo `CAN_NANG_DRIVER` thì **hỏi người dùng đúng 1 câu đời thường** (gộp cùng đợt câu hỏi bước 0 nếu đang ở đầu phiên): *"Máy bạn có card đồ họa NVIDIA nhưng bộ điều khiển đang cũ nên render chậm. Cho phép tôi tải bản mới từ NVIDIA (~1GB, miễn phí) và cài giúp bạn nhé? Bạn chỉ cần bấm YES 1 lần khi Windows hiện hộp thoại xanh — xong render nhanh gấp 2-5 lần."* Người dùng OK → chạy lại script **không có** `--check` (chạy NỀN, việc dựng vẫn tiếp tục bằng libx264 trong lúc chờ), nhắc họ để ý bấm Yes; script tự lo hết phần còn lại (tra đúng bản theo tên card, tải, cài im lặng, tự bật lại hộp thoại nếu bị trôi, tối đa 3 lần). KHÔNG OK → thôi, dùng libx264, không hỏi lại trong phiên.
   - Input là footage 4K/HEVC: thêm `-hwaccel auto` TRƯỚC `-i` (GPU lo giải mã — thắng lớn nhất ở bước cắt/chuẩn hóa, dùng được cả khi encoder vẫn là libx264).
   - **Số đo THẬT trên laptop dựng chính (legion, GTX 1650 Ti, driver 610.74, đo 2026-07-17)** — cùng 1 video test 24s (3 cảnh + xfade outro + ASS + mix loudnorm), chất lượng nghiệm thu tương đương (-13.9 LUFS, hình sắc nét):
     | Bước | libx264 (CPU) | NVENC (GPU) | Nhanh hơn |
     |---|---|---|---|
     | Cắt + chuẩn hóa 3 cảnh (kèm `-hwaccel auto`) | 16.0s | 10.5s | 1.5× |
     | xfade nối outro | 10.7s | 3.7s | 2.9× |
     | Burn ASS | 9.9s | 2.6s | 3.8× |
     | Mix final (logo+nhạc+loudnorm) | 10.8s | 3.2s | 3.4× |
     | **Tổng** | **~48s** | **~20s** | **2.4×** |

## 0.7. Hai thứ KHÔNG chạy trên máy dựng (đo thật 21/07/2026 — đừng phí thời gian thử lại)

| Thứ | Triệu chứng | Dùng gì thay |
|---|---|---|
| **`drawtext`** (ghi chữ lên ảnh/video) | `Fontconfig error: Cannot load default config file` rồi ffmpeg **crash mã 3221225477** | Ghép lưới có nhãn thì dùng filter **`tile`** hoặc `hstack`/`vstack`. Cần chữ THẬT lên video thì dùng **ASS** (`ass=`) như mục 4 — vốn là cách chuẩn của skill này, `drawtext` chỉ tiện cho ảnh nháp |
| **`-pattern_type glob`** | `Pattern type 'glob' was selected but globbing is not supported by this libavformat build` | Liệt kê file bằng Python (`glob.glob`) rồi truyền **từng `-i` một**; hoặc đặt tên file theo dãy số và dùng `-i "check_%02d.jpg"` |

Cả 2 đều là giới hạn của bản ffmpeg đang cài (gyan.dev full build), không phải lỗi câu lệnh — thử lại kiểu khác vẫn hỏng.

## 1a. Voiceover ElevenLabs (ƯU TIÊN khi có key — giọng tự nhiên + timestamp từng từ)

```powershell
python "<skill-dir>\scripts\elevenlabs_tts.py" voice\video-1-script.txt voice\video-1.mp3 `
  --srt voice\video-1.srt --words voice\video-1-words.json
```

- Key: file `~/.claude/abs6-secrets.env` dòng `ELEVENLABS_API_KEY=sk_...`. Script tự đọc, không truyền key qua tham số.
- Lời đọc ghi vào file .txt UTF-8 bằng tool Write (giống quy tắc edge-tts).
- Đổi giọng: `--voice <voice_id>`. **Giọng mặc định cho MỌI lời tiếng Việt là giọng Việt** — `MC Xuân Tú` `7XOKiK112QRZRSLbCfMc` (nam) / `Thanh Ngọc` `Na15FlRRkMEDtEW4nVVP` (nữ). Bảng ưu tiên đầy đủ ở SKILL.md mục Voice AI.
  > ⚠️ **George `JBFqnCBsd6RMkjVDRZzb` KHÔNG phải mặc định** — đó là giọng ANH, đọc tiếng Việt méo cả câu thường ("Thử cách này" → *"Thú káč nai"*). Chỉ dùng George khi lời đọc là tiếng Anh. *(Sửa 21/07: dòng này từng ghi "mặc định George nam trầm" — tàn dư trước luật 20/07.)*
- **Cảnh báo lỗi 402**: 2 giọng Việt trên nằm ở Voice Library, bị chặn khi tài khoản còn gói Free. Gặp 402:
  - giọng do Sếp **chỉ định đích danh** → DỪNG BÁO, chờ Sếp quyết, không tự thay giọng;
  - giọng mặc định → lui về **edge-tts `vi-VN-NamMinhNeural` / `vi-VN-HoaiMyNeural`** (miễn phí, đọc tiếng Việt thuần rất sạch), báo 1 câu. **TUYỆT ĐỐI không lui về George.**
- Output: mp3 + `.srt` (cụm 6 từ, sub thường) + `-words.json` (timing từng từ → làm sub karaoke ASS: mỗi từ 1 Dialogue event, hoặc dùng `\k` tags).
- Script lỗi (chưa có key/hết quota/mất mạng) → nó exit 1 kèm lý do → chuyển sang edge-tts mục 1 bên dưới, KHÔNG dừng cả quy trình.
- Free tier ~10k credits/tháng (~10 phút audio) — voiceover shorts ~35s tốn ít, nhưng đừng gọi thử nhiều lần vô ích; test bằng câu ngắn.

## 1. Voiceover edge-tts (fallback miễn phí — CHỈ khi kịch bản được duyệt có lời dẫn — mặc định video là text + nhạc)

Nếu dùng, làm TRƯỚC khi cắt hình để lấy timing.

**BẮT BUỘC truyền lời đọc qua file UTF-8 (không BOM), KHÔNG dùng `--text`** — PowerShell làm hỏng encoding tiếng Việt trên tham số dòng lệnh, edge-tts sẽ báo `NoAudioReceived`. Ghi file bằng tool Write (mặc định UTF-8) rồi:

```powershell
edge-tts --voice vi-VN-NamMinhNeural --rate=+76% `
  --file voice\video-1-script.txt `
  --write-media voice\video-1.mp3 --write-subtitles voice\video-1.srt
```

- Giọng: `vi-VN-NamMinhNeural` (nam, chắc chắn) / `vi-VN-HoaiMyNeural` (nữ, thân thiện).
- File `.srt` sinh ra cho biết timing từng cụm từ → căn thời lượng cảnh và làm phụ đề. Đo tổng thời lượng voice: `ffprobe -v error -show_entries format=duration -of csv=p=0 voice\video-1.mp3`

## 2. Cắt + chuẩn hóa từng cảnh về 1080x1920/30fps

**Clip quay ngang → crop giữa** (mặc định, đẹp nhất khi chủ thể ở giữa khung):

```powershell
ffmpeg -y -ss 00:01:23.5 -to 00:01:27.0 -i source\clip01.mp4 `
  -vf "scale=-2:1920,crop=1080:1920,fps=30" `
  -c:v libx264 -preset fast -crf 18 -pix_fmt yuv420p -c:a aac -ar 48000 temp\s01.mp4
```

**Clip ngang nhưng chủ thể lệch/khung rộng cần giữ → nền mờ (blur-pad):**

```powershell
ffmpeg -y -ss 5 -to 9 -i source\clip02.mp4 `
  -vf "split[a][b];[a]scale=1080:1920,boxblur=20:5,setsar=1[bg];[b]scale=1080:-2[fg];[bg][fg]overlay=(W-w)/2:(H-h)/2,fps=30" `
  -c:v libx264 -preset fast -crf 18 -pix_fmt yuv420p -c:a aac -ar 48000 temp\s02.mp4
```

**Clip đã quay dọc:** chỉ cần `scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30`.

- Cảnh không cần âm gốc: thêm `-an`. Cảnh cần giữ tiếng hiện trường (robot chạy, khách nói): giữ audio, chỉnh volume lúc mix cuối.
- Nguồn HEVC/10-bit lỗi: thêm `-map 0:v:0 -map 0:a:0?` và cứ re-encode như trên là chuẩn hóa xong.
- Tăng tốc cảnh (timelapse robot chạy): thêm `setpts=PTS/2` vào cuối -vf (2x) và `-an`.

## 3. Ghép cảnh (concat)

Tạo `temp\list.txt` (UTF-8). **Đường dẫn trong list tính TƯƠNG ĐỐI VỚI VỊ TRÍ FILE LIST**, không phải cwd — list nằm cùng chỗ với segment thì chỉ ghi tên file:

```
file 's01.mp4'
file 's02.mp4'
file 's03.mp4'
```

```powershell
ffmpeg -y -f concat -safe 0 -i temp\list.txt -c copy temp\ghep.mp4
```

`-c copy` chỉ an toàn vì mọi segment đã encode cùng chuẩn ở bước 2.

## 4. Text đè Anton (file .ass) — style video mẫu Roboworld

Text kể chuyện bằng font **Anton in hoa** (spec vị trí/màu học từ video mẫu — xem `style-mau.md`). Trước khi burn, copy font vào workspace:

```powershell
Copy-Item "<skill-dir>\assets\fonts\Anton-Regular.ttf" fonts\
```

Mẫu ASS chuẩn (hook vàng + text trắng, đều nằm dưới logo giữa-trên):

```
[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 0

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Hook,Anton,135,&H0000D2FF,&H00FFFFFF,&H00000000,&H80000000,0,0,0,0,100,100,1,0,1,6,3,8,60,60,215,163
Style: Text,Anton,90,&H00FFFFFF,&H00FFFFFF,&H00000000,&H80000000,0,0,0,0,100,100,1,0,1,5,2,8,60,60,225,163
Style: TextDuoi,Anton,90,&H00FFFFFF,&H00FFFFFF,&H00000000,&H80000000,0,0,0,0,100,100,1,0,1,5,2,2,60,60,480,163

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
Dialogue: 0,0:00:00.00,0:00:03.50,Hook,,0,0,0,,BELLABOT PRO\NTẠI VINSCHOOL
Dialogue: 0,0:00:03.50,0:00:07.00,Text,,0,0,0,,TƯƠNG TÁC BIỂU CẢM THÂN THIỆN
Dialogue: 0,0:00:07.00,0:00:10.50,Text,,0,0,0,,THU HÚT SỰ CHÚ Ý CỦA MỌI NGƯỜI
```

- **Cỡ chữ 135pt (Hook) / 90pt (Text) là mốc ĐÃ DUYỆT** sau 2 lần Sếp phản hồi "chữ nhỏ" (xem lịch sử đầy đủ ở `style-mau.md`) — đây là baseline mặc định, KHÔNG tự ý lùi về cỡ nhỏ hơn.
- **Nội dung text luôn IN HOA** (đúng style mẫu; Anton vốn thiết kế cho chữ hoa).
- Màu ASS là **&HAABBGGRR** (đảo ngược RGB): vàng #FFD200 → `&H0000D2FF`; trắng → `&H00FFFFFF`. Nghi ngờ màu thì burn thử 1 frame và Read để xem — đừng tin công thức suông.
- `Alignment: 8` = giữa-trên; `MarginV: 215-225` đặt text ngay dưới logo (logo chiếm vùng ~40-190px đầu khung). Style `TextDuoi` (Alignment 2, cách đáy 480px) dùng khi phần trên khung hình rối/che chủ thể — như video mẫu MT1.
- Mỗi dòng text 1 ý ngắn 5-9 từ, giữ 3-4s. `\N` xuống dòng; hook tối đa 3 dòng, text tối đa 2 dòng.
- Nếu video có voiceover: timing text lấy từ file `.srt` của edge-tts, gộp cụm 4-7 từ.

Burn vào video (đường dẫn TƯƠNG ĐỐI + fontsdir, xem quy tắc 0.1):

```powershell
ffmpeg -y -i temp\ghep.mp4 -vf "ass=temp/video-1.ass:fontsdir=fonts" -c:v libx264 -preset fast -crf 18 -c:a copy temp\ghep_sub.mp4
```

## 4b. Sound effect (SFX) — dùng DÀY theo kiểu TikTok/Reels

Nguồn an toàn: **YouTube Studio → Thư viện âm thanh → tab "Hiệu ứng âm thanh"** (`https://studio.youtube.com/channel/<id>/music`, cùng tài khoản/cùng cách tải với nhạc nền — nút "Tải xuống" xuất hiện khi hover từng dòng, xem mục 1b). Tìm bằng từ khoá tiếng Anh mô tả âm thanh (vd "whoosh", "wrench", "chime", "click") vì thư viện không có bản tiếng Việt. Kho sẵn có: `kho tài nguyên: tìm theo tên thư mục SFX/Bo 35 SFX trong ~/.claude/roboworld-assets/tai-nguyen-chung/` — cây quyết định chọn tiếng nào xem `so-sfx.md`.

### Luật 1 — MỖI thẻ chữ đều kèm 1 SFX "pop" (Sếp Huy chốt 19/07/2026, THAY luật cũ 03/07/2026)

> **Luật cũ ngày 03/07/2026 nay KHÔNG còn hiệu lực**: luật đó ghi "KHÔNG gắn SFX chỉ vì text vừa xuất hiện — SFX phải khớp hành động cụ thể trong hình", chốt liều 3-5 SFX/video. Sếp xem video-1 Tràng An bản v3 (19/07) thấy còn thưa, được hỏi rõ "luật mới mâu thuẫn luật cũ, chọn cái nào" → **Sếp chọn luật mới thành chuẩn**.

**Luật hiện hành**: **mỗi thẻ chữ xuất hiện đều được gắn 1 SFX "pop"** phù hợp NGHĨA của chữ (không random) — đây là cảm giác dày SFX kiểu TikTok/Reels. Mật độ thực tế đã dựng: **14 lớp SFX / 55 giây** (video-1 v4).

- **Chọn loại tiếng theo nghĩa**: chữ hook → `04 - Pop`; tên sản phẩm/thông báo → `14 - Apple notification`; chữ mang cảm giác công nghệ ("CUSTOMIZE...") → `24 - Glitch`; chữ mang nghĩa bùng nổ ("KHAI TRƯƠNG BÙNG NỔ") → `29 - Boom`; còn lại → Pop/chime.
- **Chỉ dùng "sound quốc dân" AN TOÀN cho brand B2B** (pop/notification/boom/glitch/chime). **CẤM** loại troll/meme (Bruh, Wasted, SpongeBob...) — không hợp thương hiệu Roboworld + có rủi ro bản quyền (nghiên cứu 19/07).
- **Ngoại lệ (giữ nguyên, KHÔNG bị luật mới thay)**: thẻ chữ nào trùng mốc (~trong 1s) với 1 SFX hành động/transition đã có sẵn (riser, ding, fire, hit...) thì **KHÔNG thêm pop chồng lên** — vẫn giữ luật "không chồng quá 2 lớp SFX cùng lúc". Thực tế video-1 v4: 8/11 thẻ được gắn pop, 3 thẻ bỏ qua vì trùng mốc.
- SFX gắn với **hành động trong hình** (whoosh lúc chuyển cảnh, ding lúc chốt) vẫn giữ nguyên như cũ — luật mới chỉ THÊM lớp text-pop, không bỏ lớp hành động.

### Luật 2 — Đặt SFX theo ĐỈNH âm, không theo đầu file (Peak Impact Rule)

Mọi file SFX đều có một đoạn **"lead-in"** câm/nhỏ ở đầu trước khi tới đỉnh thật. Đặt `adelay` bằng đúng mốc hành động là **SAI** — tiếng sẽ nổ muộn hơn hình. Nguyên tắc ngành (WeVideo/whitenoisestudio): **đỉnh TO NHẤT của SFX phải trùng khoảnh khắc hành động**, không phải điểm bắt đầu phát.

```
adelay_offset = mốc_hành_động − lead_in_đo_được
```

**Bảng lead-in đã ĐO THẬT (19/07/2026) — dùng lại cho mọi video, KHÔNG cần đo lại:**

| File SFX | Lead-in (giây) | Volume khuyên dùng | Ghi chú |
|---|---|---|---|
| `01 - riser-metallic-sound-effect.mp3` | **1.80** | 1.05 | File có ~1s đệm câm ở CUỐI — cấm dùng full `ffprobe duration` để tính offset (từng lệch 964ms) |
| `01 - Whoosh.mp3` | 0.10 | 0.95 | |
| `19 - Whoosh 2.mp3` | 0.10 | 0.90 | |
| `34 - Ding.mp3` | 0.25 | 1.40 | Volume cũ 0.75 quá nhỏ (đỉnh -6.4dB, thấp hơn thoại 6dB → không nghe thấy "keng") |
| `08 - Woosh fire transition.mp3` | 0.20 | 0.90 | |
| `26 - Cinematic hit.mp3` | **0.50** | 0.85 | Gần nửa giây "room tone" trước cú hit chính |
| `04 - Pop.mp3` | 0.05 | 1.9 | |
| `14 - Apple notification.mp3` | 0.30 | 2.2 | |
| `24 - Glitch.mp3` | 0.10 | 2.0 | |
| `29 - Boom.mp3` | **0.60** | 1.2 | |
| `09 - Game point.mp3` | 0.05 | 1.4 | |
| `21 - Kids yeyy.mp3` | **0.70** | 1.2 | đo 20/07/2026 — tiếng trẻ reo, hợp cảnh bé tương tác robot |
| `22 - Display digits.mp3` | **0.50** | 1.3 | đo 20/07/2026 — hợp thẻ chữ có SỐ LIỆU (thông số, giá) |

**Đo lead-in cho 1 file SFX mới** (chưa có trong bảng) — dùng đường bao biên độ, **KHÔNG dùng `silencedetect` ngưỡng đơn** (từng cho số SAI với "Ding" vì bắt nhầm đoạn nhiễu cuối file):

```powershell
ffmpeg -i "file.mp3" -t 1.0 -af "asetnsamples=n=2205,astats=metadata=1:reset=1,ametadata=print:key=lavfi.astats.Overall.RMS_level:file=-" -f null -
```
→ tìm khung 50ms có dB cao nhất, đó là lead-in.

**Mốc âm lượng chuẩn**: lấy đỉnh thoại sau `dynaudnorm` (mean ≈ -14.5dB) làm chuẩn so sánh; SFX phải ngang hoặc nhỉnh hơn mốc đó mới nghe rõ. Kiểm bằng `volumedetect`.

### Luật 3 — 3 cái bẫy khi mix (đều đã dính thật ngày 20/07/2026)

1. **`amix=duration=first` CẮT MẤT OUTRO**: nếu nhánh audio đầu tiên là track âm gốc (dài đúng bằng thân video), `duration=first` khiến audio kết thúc ở cuối thân → `-shortest` cắt luôn phần outro khỏi video final (đo ra 38.3s thay vì 46.7s). **Luôn dùng `amix=duration=longest`** khi mix có track outro trễ (`adelay`).
2. **Trích khung để soi chữ ASS: `-ss` đặt TRƯỚC `-i` là chữ KHÔNG hiện** — seek đầu vào làm timestamp output về 0 nên filter `ass` không thấy sự kiện nào ở mốc đó. Cách đúng: **burn ASS vào video trước, rồi mới trích khung từ video đã burn** (bước burn dù sao cũng cần).
3. **`loudnorm` 1 lượt có thể trượt chuẩn**: bản K3 20/07 chạy 1 lượt ra **-15.35 LUFS** (ngoài -14 ±1). Nghiệm thu bắt được → phải chạy **lượt 2** với số đã đo, video giữ nguyên (`-c:v copy`, chỉ mã hoá lại audio):
   ```powershell
   ffmpeg -y -i final.mp4 -af "loudnorm=I=-14:TP=-1.5:LRA=11:measured_I=-15.35:measured_TP=-1.41:measured_LRA=4.80:measured_thresh=-25.89:offset=0.67:linear=true" -c:v copy -c:a aac -b:a 192k fix.mp4
   ```
   → đo lại ra -14.38 LUFS, đạt. **Luôn đo sau khi mix; lệch quá ±1 thì chạy lượt 2, đừng bỏ qua.**

Mỗi SFX là 1 input riêng, canh thời điểm bằng `adelay` (đơn vị milliseconds, ghi 2 lần cách nhau `|` cho stereo) rồi gộp cùng nhạc nền bằng `amix`:

```powershell
ffmpeg -y -i video.mp4 -i logo.png -i nhac.mp3 -i "whoosh.mp3" -i "wrench.mp3" -i "chime.mp3" `
  -filter_complex "[1:v]scale=480:-1[lg];[0:v][lg]overlay=(W-w)/2:50[v];[2:a]volume=0.55,afade=t=out:st=42:d=1[bgm];[3:a]volume=0.9,adelay=0|0[wh];[4:a]volume=0.9,adelay=9300|9300[wr];[5:a]atrim=0:1.8,volume=0.8,adelay=31300|31300[ch];[bgm][wh][wr][ch]amix=inputs=4:duration=first:normalize=0[a]" `
  -map "[v]" -map "[a]" -c:v libx264 -preset medium -crf 20 -pix_fmt yuv420p -c:a aac -b:a 192k -shortest ..\Final\video.mp4
```

`adelay=9300|9300` = SFX phát ở giây 9.3 của timeline cuối cùng (không phải timeline riêng của SFX). `atrim=0:1.8` cắt bớt SFX dài (vd chime 9.8s) xuống còn phần đầu cần dùng. Nhạc nền hạ nhẹ volume (0.55 thay vì 0.85) khi có nhiều SFX chồng lên để không rối.

## 4c. Chuyển cảnh mượt (crossfade) — dùng cho bước ngoặt nội dung, KHÔNG dùng tràn lan

Trong 1 chuỗi montage nhịp nhanh, cắt cứng (hard cut) vẫn là mặc định — tạo cảm giác dồn dập, đúng style video mẫu. Chỉ chuyển sang crossfade khi có **bước ngoặt nội dung thật sự** (đổi địa điểm, nhảy thời gian, ví dụ: "sửa xong tại quán" → "robot chạy ra ngoài phố tiếp tục làm việc"). Dùng `xfade` giữa 2 clip đã dựng xong (không phải giữa các segment thô):

```powershell
ffmpeg -y -i main_sequence.mp4 -i ending_scene.mp4 `
  -filter_complex "[0:v][1:v]xfade=transition=fade:duration=0.6:offset=<main_duration-0.6>,format=yuv420p" `
  -c:v libx264 -preset fast -crf 18 temp\full_nosub.mp4
```

`offset` = thời điểm (giây) trong `main_sequence.mp4` mà transition bắt đầu — lấy bằng `ffprobe` đo duration của main_sequence rồi trừ đi duration của transition (0.5-0.8s là đủ mượt mà không lê thê). Burn text ASS **sau** bước xfade này, dùng timeline của video ĐÃ GHÉP để mọi mốc thời gian trong .ass khớp đúng.

**BẮT BUỘC với ffmpeg 8.x (bài học 19/07/2026)**: `xfade` đòi **timebase 2 nhánh phải khớp nhau**, không khớp thì transition ra sai chỗ hoặc lỗi thẳng. Luôn chuẩn hoá CẢ 2 nhánh trước khi xfade, **`fps` đặt TRƯỚC `settb`**:

```powershell
-filter_complex "[0:v]fps=30,settb=AVTB[a];[1:v]fps=30,settb=AVTB[b];[a][b]xfade=transition=fade:duration=0.6:offset=<offset>,format=yuv420p"
```

Và `offset` phải lấy từ duration **ĐO SAU KHI concat** (`ffprobe` trên chính file đã ghép), không cộng dồn thời lượng từng clip trên giấy — sai số concat tích lại làm lệch mốc.

## 4d. Nối outro dọc vào cuối video

Outro dọc là file có sẵn (`tìm theo TÊN FILE outro dọc.mp4 trong ~/.claude/roboworld-assets/tai-nguyen-chung/`, 2160x3840, ~9s, có sẵn nhạc/audio riêng). Luôn nối vào cuối mọi video (trừ khi Sếp nói không cần). Trình tự:

1. Scale outro về đúng khung 1080x1920 (chia đúng 1/2, không méo):
```powershell
ffmpeg -y -v error -i "outro dọc.mp4" -vf "scale=1080:1920,fps=30" -an -c:v libx264 -preset fast -crf 18 -pix_fmt yuv420p temp\outro_v.mp4
```

2. Crossfade video chính (đã dựng xong phần thân, video-only) với outro, 0.4s, offset = (thời lượng thân video - 0.4):
```powershell
ffmpeg -y -v error -i temp\full_video_nosub.mp4 -i temp\outro_v.mp4 -filter_complex "[0:v][1:v]xfade=transition=fade:duration=0.4:offset=<than_video_duration-0.4>,format=yuv420p" -c:v libx264 -preset fast -crf 18 temp\full_video_with_outro.mp4
```

3. Burn ASS lên video ĐÃ có outro (timeline giờ dài hơn, nhưng text chỉ có event trong khoảng thân video — không cần thêm text cho đoạn outro, outro đã tự có branding riêng).

4. Ở bước mix âm thanh cuối, KHÔNG overlay logo lên đoạn outro (outro đã có logo riêng, chồng thêm sẽ rối) — dùng `enable` trên filter overlay để tự ngắt đúng lúc:
```
[1:v]scale=480:-1[lg];[0:v][lg]overlay=(W-w)/2:50:enable='lt(t,<offset_bat_dau_crossfade>)'[v]
```

5. Audio: outro có track riêng — input trực tiếp file outro gốc (có audio) làm 1 input audio, delay đúng bằng thời điểm crossfade bắt đầu (`adelay=<offset_ms>|<offset_ms>`), rồi `amix` cùng nhạc nền (nhạc nền nên `afade=t=out` kết thúc ngay trước mốc đó để 2 lớp nhạc không đè nhau thô). Xem ví dụ đầy đủ ở mục 5 bên dưới.

## 5. Logo + trộn âm thanh + xuất thành phẩm

Logo Roboworld bản TRẮNG, **giữa-trên** (học từ video mẫu): rộng ~480px, cách mép trên ~50px. Dạng video mặc định là **text + nhạc** (không voiceover):

```powershell
ffmpeg -y -i temp\ghep_sub.mp4 -i logo.png -stream_loop -1 -i nhac.mp3 `
  -filter_complex "[1:v]scale=480:-1[lg];[0:v][lg]overlay=(W-w)/2:50[v];[0:a]volume=0.25[orig];[2:a]volume=0.85[bgm];[orig][bgm]amix=inputs=2:duration=first:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000[a]" `
  -map "[v]" -map "[a]" -c:v libx264 -preset medium -crf 20 -pix_fmt yuv420p `
  -c:a aac -b:a 192k -shortest ..\Final\video-1-ten-video.mp4
```

(`logo.png`, `nhac.mp3` copy sẵn vào workspace để dùng đường dẫn tương đối.)

Tùy biến:
- Không logo → bỏ input 1 và nhánh `[lg]`/overlay.
- Âm gốc footage: 0.2-0.3 khi có tiếng môi trường hay (tiếng robot, tiếng cười); segment nào ồn thì đã `-an` từ bước cắt. Nếu bỏ hết âm gốc → chỉ map `[2:a]` làm audio, bỏ amix.

**Ví dụ đầy đủ có outro + SFX khớp hành động** (tình huống chuẩn — video có outro dọc, vài SFX đúng chỗ, `<offset>` = thời lượng thân video trước outro, tính bằng giây và mili-giây):

```powershell
ffmpeg -y -i temp\full_video_with_outro_sub.mp4 -i logo.png -i nhac.mp3 `
  -i "sfx1.mp3" -i "sfx2.mp3" -i "outro dọc.mp4" `
  -filter_complex "[1:v]scale=480:-1[lg];[0:v][lg]overlay=(W-w)/2:50:enable='lt(t,<offset>)'[v];[2:a]volume=0.5,afade=t=out:st=<offset-0.6>:d=0.6[bgm];[3:a]volume=0.9,adelay=<t1_ms>|<t1_ms>[a1];[4:a]volume=0.85,adelay=<t2_ms>|<t2_ms>[a2];[5:a]adelay=<offset_ms>|<offset_ms>[a3];[bgm][a1][a2][a3]amix=inputs=4:duration=longest:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000[a]" `
  -map "[v]" -map "[a]" -c:v libx264 -preset medium -crf 20 -pix_fmt yuv420p -c:a aac -b:a 192k -shortest ..\Final\video-final.mp4
```

Input cuối (`outro dọc.mp4`) đưa thẳng file GỐC (chưa scale) vào làm nguồn audio — chỉ cần `[5:a]`, không cần `[5:v]` vì phần hình outro đã ghép sẵn vào input 0 từ bước 4d. `amix duration=longest` để không cắt cụt track outro; `-shortest` ở lệnh xuất cuối mới là thứ thật sự khớp độ dài với video.

**Chuỗi `loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000` ở cuối filter audio là BẮT BUỘC trong lệnh xuất final** (chuẩn giao hàng -14 LUFS của Sếp — áp cho MỌI kiểu dựng, không riêng video có voice). `aresample=48000` đi kèm vì loudnorm tự đổi sample rate lên 192kHz. Video có voiceover: vẫn loudnorm cả mix như trên, RIÊNG track giọng MC thu nhiều khoảng cách mic khác nhau thì loudnorm I=-16 trên track voice ghép TRƯỚC khi mix (luật trong style-voice-karaoke.md).
- **Có voiceover** (khi kịch bản được duyệt có lời dẫn): thêm input `voice\video-N.mp3`, voiceover volume 1.0, nhạc nền hạ còn 0.15-0.2, `amix=inputs=3`.

  **MỨC NHẠC ĐÃ CHỈNH THEO TAI SẾP (21/07/2026)** — con số 0.15-0.2 ở trên là khoảng chung, nhưng **giọng thu thật và giọng máy cần mức khác nhau**:

  | Loại giọng | Nhạc lúc đang nói | Vì sao |
  |---|---|---|
  | **Tiếng MC thu thật** (Kiểu 2) | **0.20-0.22** | Giọng thu thật to và dày, nhạc 0.15 nghe **hơi bé** — Sếp nhận xét đúng ca video-2 ngày 21/07 |
  | **Giọng máy TTS** (Kiểu 3) | **0.12-0.14** | Giọng TTS mỏng hơn giọng người, nhạc 0.18 là **lấn át lời dẫn** — Sếp bắt lỗi ca video-3 cùng ngày |

  Đây là chênh lệch dễ bỏ sót vì `loudnorm` cuối lệnh chuẩn hoá tổng thể, nên đo LUFS vẫn đạt mà **tương quan giọng/nhạc thì sai**. Máy không tự bắt được — chỉ tai người nghe ra.
- Nhạc ngắn hơn video: `-stream_loop -1` đã lo; nhạc dài hơn: `-shortest` đã lo.

## 5b. Nhạc DÂNG LÊN sau khi giọng dẫn kết thúc (Nhóm B — luật 21/07/2026)

Dùng khi giọng nói **chỉ mở màn 1-2 câu** rồi im hẳn, phần sau để cảnh robot + nhạc tự kể (xem `references/chon-kieu-dung.md`, khối "Luật nhạc theo mức phủ giọng"). Nhóm này **được dùng nhạc có lời/nhạc hot**, vì sau đoạn mở đầu không còn giọng nào chồng lên nữa.

**Nguyên tắc: MỘT bài nhạc duy nhất chạy suốt, chỉ thay đổi âm lượng — tuyệt đối không đổi bài giữa chừng.**

Bước 1 — **đo mốc giọng kết thúc bằng `scripts/loc_thoai_that.py`**:

```powershell
python "<skill-dir>\scripts\loc_thoai_that.py" voice\video-N.mp3
```

`t1` của đoạn cuối cùng chính là `T_END` (giây) — thời điểm câu dẫn cuối vừa dứt.

> ⚠️ **SỬA LUẬT SAI ngày 21/07/2026** — bản đầu của mục này (viết sáng cùng ngày) bảo *"đo mốc giọng kết thúc bằng `silencedetect`"*. **SAI, đã gây hậu quả thật ngay trong ngày**: trên clip nhà sách Tràng An, `silencedetect` trả mốc 20.2s trong khi câu MC thật sự bắt đầu ở 24.0s — lệch 4 giây, cắt theo là mất đầu câu.
>
> Nguyên nhân: `silencedetect` chỉ nhìn TO/NHỎ, không nhìn CHẤT giọng. Trong môi trường ồn nền liên tục (nhà sách, siêu thị, nhà máy) nó bắt nhầm tiếng ồn nhấp nhô thành "hết câu". Phải nới ngưỡng từ -32 lên -25dB mới ra kết quả — **chính việc phải nới ngưỡng đã là dấu hiệu công cụ không dùng được ở đó**.
>
> 🔴 **SỬA TIẾP CÙNG NGÀY (chiều 21/07) — câu cuối của khối này TỪNG SAI.** Nó viết *"dùng script trên cho mọi trường hợp thì khỏi phải phân biệt"*. **Không đúng: với file TTS thì phải làm NGƯỢC LẠI.**
>
> | Loại file | Dùng gì để đo mốc giọng dứt |
> |---|---|
> | Tiếng **thu thật** (có ồn nền) | `loc_thoai_that.py` |
> | File **TTS máy đọc** | **`silencedetect`** — script kia KHÔNG dùng được |
>
> **Vì sao script không dùng được cho TTS**: nó tính sàn nhiễu từ chính clip (phân vị 20). File TTS thì khoảng lặng là **im tuyệt đối**, nên phép tính sàn vô nghĩa — nó chấm cả 3 đoạn giọng là "XA MIC", thậm chí ra `cách sàn = -21.8 dB` (âm, tức thấp hơn cả sàn). Đo thật trên `voice/v3.mp3` chiều 21/07.
>
> Ngược lại `silencedetect` chạy hoàn hảo trên TTS vì nền im tuyệt đối — trả đúng mốc giọng dứt 5.79s.

Bước 2 — nhạc nhỏ trong lúc nói, dâng dần lên trong 1.5s, rồi giữ to đến hết:

```powershell
# T_END = 6.2  (giọng dứt ở giây 6.2) ; 0.18 = mức nhỏ khi đang nói ; 0.55 = mức to sau đó
[2:a]volume='if(lt(t,6.2),0.18,if(lt(t,7.7),0.18+(t-6.2)/1.5*0.37,0.55))':eval=frame[bgm]
```

- `eval=frame` **bắt buộc** — thiếu nó ffmpeg tính volume đúng 1 lần ở frame đầu rồi giữ nguyên cả bài, nhạc sẽ nhỏ suốt và Sếp sẽ tưởng công thức hỏng.
- `0.37` trong công thức = `0.55 - 0.18` (biên độ dâng). Đổi 2 mức thì phải đổi cả số này.
- Dâng trong **1.5s** là vừa tai. Dưới 0.5s nghe như bị giật volume; trên 3s nghe ì ạch, mất cú hích.
- Mức nhỏ `0.15-0.2` giống luật voiceover ở mục 5; mức to `0.5-0.6` giống nhạc nền Kiểu 1.

Phần còn lại của lệnh xuất giữ nguyên như mục 5 — vẫn `amix` cùng track giọng + SFX + outro, vẫn `loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000` ở cuối.

**Nghiệm thu riêng cho mục này**: nghe lại quanh mốc `T_END` xem nhạc có dâng mượt không, và kiểm chữ cuối của câu dẫn có bị nhạc trùm lên không — dâng sớm quá là nuốt mất chữ cuối.

## 5c. Xử lý tiếng nói — 4 lựa chọn cho người dùng chọn (luật Sếp Huy 21/07/2026)

**Áp cho**: voice-over do **người thu** + **MC dẫn trực tiếp** (Kiểu 2).
**KHÔNG áp cho voice-over giọng AI** — file TTS vốn đã sạch hoàn toàn, lọc thêm chỉ làm méo.

⛔ **LUẬT CỨNG VỀ THỨ TỰ — đọc trước khi dùng bất kỳ bộ lọc nào bên dưới:**

> Mọi bộ lọc ở mục này **CHỈ được chạy ở bước MIX CUỐI, sau khi đã cắt xong**.
> **TUYỆT ĐỐI KHÔNG chạy trước bước ĐO mốc thoại.**
>
> Đã đo thật 21/07/2026, lọc ồn phá hệ đo theo 3 cách, đều **âm thầm không báo lỗi**:
> | | Gốc | afftdn mạnh |
> |---|---|---|
> | Cách sàn (dùng để chọn bản take tốt) | 17.2 dB | 18.5 dB — *không cải thiện* |
> | Độ ấm (dùng để phân biệt giọng người / loa robot) | 0.85 | **3.81** (nhà máy: **23.27**) — *hỏng hẳn* |
> | Số cửa sổ bắt được | 28 | **151** — *bắt nhầm gấp 5* |
>
> Riêng `speechnorm` nén dải động làm **cách sàn tụt 17.2 → 10.3** — xoá đúng thứ dùng để phân biệt bản take tốt với bản tập. Và `highpass=120` trong môi trường ồn to làm **mất hẳn khả năng phát hiện thoại**.
>
> Thứ tự bắt buộc: **đo → cắt → (lọc/cải thiện nếu người dùng chọn) → loudnorm → xuất.**

### Bốn lựa chọn

```powershell
# 1) GOC — khong xu ly gi (MAC DINH khi nguoi dung khong chon / noi "tuy")
$AF = ""

# 2) CHI LOC ON — boc tieng nen
$AF = "afftdn=nr=12:nf=-25"

# 3) CHI CAI THIEN — khong loc on, chi lam giong ro va deu hon
$AF = "highpass=f=80,equalizer=f=250:t=q:w=1.2:g=-2.5,equalizer=f=3200:t=q:w=1.5:g=3.5,deesser=i=0.4,compand=attacks=0.02:decays=0.30:points=-60/-48|-30/-22|-15/-12|0/-9"

# 4) CA HAI
$AF = "afftdn=nr=12:nf=-25,highpass=f=80,equalizer=f=250:t=q:w=1.2:g=-2.5,equalizer=f=3200:t=q:w=1.5:g=3.5,deesser=i=0.4,compand=attacks=0.02:decays=0.30:points=-60/-48|-30/-22|-15/-12|0/-9"
```

Chuỗi này chèn vào **track giọng** trước khi `amix`, không áp lên nhạc nền. `loudnorm` cuối lệnh xuất vẫn giữ nguyên như mục 5.

**Mặc định = lựa chọn 1 (gốc)** khi người dùng không trả lời — không xử lý thì không hỏng, xử lý sai thì hỏng.

### Lưu ý khi dùng

- **Chuỗi `compand` có dấu `|`** — luôn bọc trong nháy kép khi viết vào PowerShell, để trần là vỡ lệnh.
- **Tiếng Việt có thanh điệu**: `afftdn` mức mạnh (`nr` > 15) làm méo dấu nặng/dấu ngã, nghe như dưới nước. Đừng tự nâng `nr` để "sạch hơn".
- **Tiếng quá xa thì không cứu được**: đo thấy cách sàn < 8 dB (vd nhà máy dập folder 33, đo thật chỉ **2.2 dB**) thì mọi bộ lọc đều vô ích — báo người dùng dùng cảnh khác, đừng cố xử lý.
- Người dùng phân vân → cắt thử 4 bản 10 giây cho họ nghe chọn, **nhớ cân bằng cả 4 về cùng độ to** (`loudnorm=I=-16`) rồi mới đưa nghe; không cân bằng thì tai luôn chọn bản to nhất chứ không phải bản hay nhất.

## 5d. Video cho KÊNH CÁ NHÂN — bỏ logo + outro (luật Sếp Huy 21/07/2026)

Hỏi ở bước C (`references/chon-kieu-dung.md`): *"Video này đăng ở page chính của công ty, hay ở kênh cá nhân?"*

**Kênh cá nhân → để mộc, chỉ có video thôi, trông cho tự nhiên.** Gắn logo với outro vào là thành quảng cáo ngay, mất đúng cái tự nhiên vốn là điểm mạnh của kênh cá nhân.

| | Page công ty | Kênh cá nhân |
|---|---|---|
| Logo trắng giữa-trên | ✅ | ❌ bỏ |
| Outro dọc | ✅ | ❌ bỏ |
| Chữ, nhạc, SFX, chuyển cảnh, loudnorm | giống nhau | giống nhau |

**Cách bỏ — sửa đúng 2 chỗ, đừng đụng gì khác:**

1. **Bỏ bước nối outro (mục 4d)**: không chạy `xfade` nối outro. Video kết thúc ngay ở cảnh cuối cùng của thân bài. Nhớ bỏ luôn input file outro và nhánh `[N:a]` của nó trong `amix` ở lệnh mix cuối — **để sót nhánh audio là ffmpeg báo lỗi khó hiểu về số input**.
2. **Bỏ overlay logo (mục 5)**: bỏ input `logo.png` và cả cụm `[1:v]scale=480:-1[lg];[0:v][lg]overlay=...` trong `filter_complex`, map thẳng `[0:v]`.

Mọi thứ còn lại **giữ nguyên**: vẫn 1080x1920, vẫn burn chữ, vẫn nhạc + SFX, và **vẫn phải `loudnorm` về -14 LUFS** — chuẩn âm lượng không liên quan tới chuyện đăng ở đâu.

**Nghiệm thu**: trích frame kiểm **không còn logo ở giữa-trên**, và frame cuối là cảnh thật chứ không phải outro.

## 6. Tự nghiệm thu (bắt buộc trước khi bàn giao)

```powershell
ffprobe -v error -show_entries format=duration -show_entries stream=width,height -of default=noprint_wrappers=1 ..\Final\video-1-ten-video.mp4
ffmpeg -y -i ..\Final\video-1-ten-video.mp4 -vf "fps=1/8,scale=480:-2" -q:v 5 temp\check_%02d.jpg
```

Read các file `temp\check_*.jpg` và kiểm: hook hiện đúng 3s đầu, sub không tràn mép/không bị logo đè, hình không méo, không có frame đen. Nghe thử không được thì tin timing: tổng thời lượng video phải ≥ thời lượng voiceover.

**Đo âm lượng giao hàng (bắt buộc, chuẩn -14 LUFS ±1):**

```powershell
ffmpeg -hide_banner -i ..\Final\video-1-ten-video.mp4 -af loudnorm=I=-14:TP=-1.5:LRA=11:print_format=summary -f null -
```

Đọc dòng **`Input Integrated:`** trong kết quả — đó là âm lượng THẬT của file (các dòng "Output..." chỉ là mô phỏng nếu chạy loudnorm thêm lần nữa, bỏ qua). Đạt: -15 đến -13 LUFS. Lệch hơn → quay lại lệnh xuất final kiểm tra đã có chuỗi loudnorm chưa, mix lại. Ghi con số đo được vào báo cáo bàn giao.

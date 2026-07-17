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

## 1a. Voiceover ElevenLabs (ƯU TIÊN khi có key — giọng tự nhiên + timestamp từng từ)

```powershell
python "<skill-dir>\scripts\elevenlabs_tts.py" voice\video-1-script.txt voice\video-1.mp3 `
  --srt voice\video-1.srt --words voice\video-1-words.json
```

- Key: file `~/.claude/abs6-secrets.env` dòng `ELEVENLABS_API_KEY=sk_...`. Script tự đọc, không truyền key qua tham số.
- Lời đọc ghi vào file .txt UTF-8 bằng tool Write (giống quy tắc edge-tts).
- Đổi giọng: `--voice <voice_id>` (mặc định George nam trầm, model multilingual v2 đọc được tiếng Việt; chọn giọng khác ở elevenlabs.io/app/voice-library). **Cảnh báo lỗi 402**: giọng lấy từ Voice Library (như 2 giọng Việt Sếp từng chọn) bị chặn ở gói Free — chỉ giọng premade (George, Bella...) chạy được miễn phí. Gặp 402 với giọng được chỉ định đích danh → DỪNG BÁO, không tự thay giọng (luật trong SKILL.md).
- Output: mp3 + `.srt` (cụm 6 từ, sub thường) + `-words.json` (timing từng từ → làm sub karaoke ASS: mỗi từ 1 Dialogue event, hoặc dùng `\k` tags).
- Script lỗi (chưa có key/hết quota/mất mạng) → nó exit 1 kèm lý do → chuyển sang edge-tts mục 1 bên dưới, KHÔNG dừng cả quy trình.
- Free tier ~10k credits/tháng (~10 phút audio) — voiceover shorts ~35s tốn ít, nhưng đừng gọi thử nhiều lần vô ích; test bằng câu ngắn.

## 1. Voiceover edge-tts (fallback miễn phí — CHỈ khi kịch bản được duyệt có lời dẫn — mặc định video là text + nhạc)

Nếu dùng, làm TRƯỚC khi cắt hình để lấy timing.

**BẮT BUỘC truyền lời đọc qua file UTF-8 (không BOM), KHÔNG dùng `--text`** — PowerShell làm hỏng encoding tiếng Việt trên tham số dòng lệnh, edge-tts sẽ báo `NoAudioReceived`. Ghi file bằng tool Write (mặc định UTF-8) rồi:

```powershell
edge-tts --voice vi-VN-NamMinhNeural --rate=+8% `
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

## 4b. Sound effect (SFX) — tuỳ chọn, dùng thưa

Nguồn an toàn: **YouTube Studio → Thư viện âm thanh → tab "Hiệu ứng âm thanh"** (`https://studio.youtube.com/channel/<id>/music`, cùng tài khoản/cùng cách tải với nhạc nền — nút "Tải xuống" xuất hiện khi hover từng dòng, xem mục 1b). Tìm bằng từ khoá tiếng Anh mô tả âm thanh (vd "whoosh", "wrench", "chime", "click") vì thư viện không có bản tiếng Việt.

Nguyên tắc dùng (quan trọng, đã bị nhắc nhở khi làm sai — ngày 03/07/2026): **mỗi SFX phải khớp với một hành động/khoảnh khắc CỤ THỂ đang diễn ra trong hình** (tiếng cờ lê khi tay đang vặn ốc, tiếng whoosh khi hình đang chuyển cảnh, tiếng chime khi câu chữ báo "hoàn tất"). KHÔNG gắn SFX chỉ vì text vừa xuất hiện trên màn hình — nếu hành động trong hình không tạo ra âm thanh đó một cách tự nhiên thì đừng thêm, dù nghe "cho vui tai" đến đâu. Trước khi thêm 1 SFX, tự hỏi: "âm thanh này có match với thứ đang xảy ra trên hình không, hay chỉ đang lấp chỗ trống?" — nếu là lấp chỗ trống thì bỏ. Số lượng SFX không quan trọng bằng độ khớp; 1 video có thể chỉ cần 3-5 SFX thật sự đắt, không cần rải đều mỗi lần đổi chữ.

Mỗi SFX là 1 input riêng, canh thời điểm bằng `adelay` (đơn vị milliseconds, ghi 2 lần cách nhau `|` cho stereo) rồi gộp cùng nhạc nền bằng `amix`:

```powershell
ffmpeg -y -i video.mp4 -i logo.png -i nhac.mp3 -i "whoosh.mp3" -i "wrench.mp3" -i "chime.mp3" `
  -filter_complex "[1:v]scale=480:-1[lg];[0:v][lg]overlay=(W-w)/2:50[v];[2:a]volume=0.55,afade=t=out:st=42:d=1[bgm];[3:a]volume=0.9,adelay=0|0[wh];[4:a]volume=0.9,adelay=9300|9300[wr];[5:a]atrim=0:1.8,volume=0.8,adelay=31300|31300[ch];[bgm][wh][wr][ch]amix=inputs=4:duration=first:normalize=0[a]" `
  -map "[v]" -map "[a]" -c:v libx264 -preset medium -crf 20 -pix_fmt yuv420p -c:a aac -b:a 192k -shortest output\video.mp4
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

## 4d. Nối outro dọc vào cuối video

Outro dọc là file có sẵn (`assets/tai-nguyen-chung/Logo + Outro/outro dọc.mp4`, 2160x3840, ~9s, có sẵn nhạc/audio riêng). Luôn nối vào cuối mọi video (trừ khi Sếp nói không cần). Trình tự:

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
  -c:a aac -b:a 192k -shortest output\video-1-ten-video.mp4
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
  -map "[v]" -map "[a]" -c:v libx264 -preset medium -crf 20 -pix_fmt yuv420p -c:a aac -b:a 192k -shortest output\video-final.mp4
```

Input cuối (`outro dọc.mp4`) đưa thẳng file GỐC (chưa scale) vào làm nguồn audio — chỉ cần `[5:a]`, không cần `[5:v]` vì phần hình outro đã ghép sẵn vào input 0 từ bước 4d. `amix duration=longest` để không cắt cụt track outro; `-shortest` ở lệnh xuất cuối mới là thứ thật sự khớp độ dài với video.

**Chuỗi `loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000` ở cuối filter audio là BẮT BUỘC trong lệnh xuất final** (chuẩn giao hàng -14 LUFS của Sếp — áp cho MỌI kiểu dựng, không riêng video có voice). `aresample=48000` đi kèm vì loudnorm tự đổi sample rate lên 192kHz. Video có voiceover: vẫn loudnorm cả mix như trên, RIÊNG track giọng MC thu nhiều khoảng cách mic khác nhau thì loudnorm I=-16 trên track voice ghép TRƯỚC khi mix (luật trong style-voice-karaoke.md).
- **Có voiceover** (khi kịch bản được duyệt có lời dẫn): thêm input `voice\video-N.mp3`, voiceover volume 1.0, nhạc nền hạ còn 0.15-0.2, `amix=inputs=3`.
- Nhạc ngắn hơn video: `-stream_loop -1` đã lo; nhạc dài hơn: `-shortest` đã lo.

## 6. Tự nghiệm thu (bắt buộc trước khi bàn giao)

```powershell
ffprobe -v error -show_entries format=duration -show_entries stream=width,height -of default=noprint_wrappers=1 output\video-1-ten-video.mp4
ffmpeg -y -i output\video-1-ten-video.mp4 -vf "fps=1/8,scale=480:-2" -q:v 5 temp\check_%02d.jpg
```

Read các file `temp\check_*.jpg` và kiểm: hook hiện đúng 3s đầu, sub không tràn mép/không bị logo đè, hình không méo, không có frame đen. Nghe thử không được thì tin timing: tổng thời lượng video phải ≥ thời lượng voiceover.

**Đo âm lượng giao hàng (bắt buộc, chuẩn -14 LUFS ±1):**

```powershell
ffmpeg -hide_banner -i output\video-1-ten-video.mp4 -af loudnorm=I=-14:TP=-1.5:LRA=11:print_format=summary -f null -
```

Đọc dòng **`Input Integrated:`** trong kết quả — đó là âm lượng THẬT của file (các dòng "Output..." chỉ là mô phỏng nếu chạy loudnorm thêm lần nữa, bỏ qua). Đạt: -15 đến -13 LUFS. Lệch hơn → quay lại lệnh xuất final kiểm tra đã có chuỗi loudnorm chưa, mix lại. Ghi con số đo được vào báo cáo bàn giao.

# Kiểu 2A "Huy nói chuyện + khung nổi" và Kiểu 2B "Voice POV + chèn full màn"

> Rút từ 2 video kênh Quang Huy Robot, Sếp Huy chấm và sửa qua 7 vòng ngày 12/10/2026:
> - **Video 64** — *Cần bao tiền để sở hữu robot hình người* (Kiểu 2A)
> - **Video 65** — *Làm sao để gian hàng nổi bật giữa hội chợ* (Kiểu 2B)
>
> Video mẫu gốc của Sếp là **63** — *RObot bên trung có thực sự phổ biến* (`HUY MKT\03.PAGE QUANG HUY ROBOT\63...`).
> Đây là **nhánh con của Kiểu 2** (dựng theo lời thoại có sẵn). Mọi luật chung của Kiểu 2 (`style-voice-karaoke.md`) vẫn áp dụng, trừ chỗ file này ghi khác.
>
> 🔴 **Mọi con số trong file này là SỐ ĐO THẬT**, không phải ước lượng. Khi gặp video mẫu mới, **đo lại bằng lệnh** rồi mới dựng. Đừng tin cảm giác.

| | **2A — nói chuyện trước camera** | **2B — voice POV** |
|---|---|---|
| Nhận diện | Mặt người nói chiếm khung, quay selfie / chân máy | Không thấy mặt; người cầm máy vừa quay vừa thuyết minh |
| Cảnh chèn | **Khung nổi** đè lên nền mặt người | **Full màn hình**, cắt hẳn sang cảnh khác |
| Ví dụ | Video 63, 64 | Video 65 (VEC) |

---

## 1. Việc làm chung cho cả 2A và 2B

### 1.1. Cắt thoại
- Bỏ mọi câu vấp, câu nói lại, "ừ ừ", "à à". Lấy **lần nói trọn vẹn cuối cùng** của mỗi ý.
- Quãng lặng dài hơn 0,2 giây → rút còn khoảng 0,12 giây. Bản đầu video 65 rút còn 0,24 giây vẫn bị Sếp chê "nhiều khoảng trống thoại" (13/10).
- 🔴 **Dò quãng lặng lần cuối bằng Silero VAD** (`analyze_footage.vad_speech_segments`) trên bản đã cắt, rồi Whisper nghe lại từng quãng lớn hơn 0,3 giây. Bắt buộc với môi trường ồn: cách đo năng lượng bị nền ồn lấp, sót mất 8 giây lặng ở video 65 (1,7 giây đầu video toàn tiếng ồn, 3,6 giây lặng giữa bài, chữ "Mà" lửng). Xuất xong chạy lại VAD trên file thành phẩm: **không còn quãng lặng nào lớn hơn 0,3 giây**.
- Cắt xong **bắt buộc cho Whisper nghe lại từng chỗ nối**. Whisper nghe lát RỘNG (8 giây) chuẩn hơn lát ngắn.
- **Môi trường ồn** (hội trường, triển lãm): `loc_thoai_that.py` sẽ ra 0 đoạn, vì giọng chỉ cao hơn sàn ồn khoảng 6 dB (đo thật ở VEC: sàn -25,7 dB). Làm thay thế bằng 2 bước:
  - (a) Whisper nghe từng khúc 8 giây, mỗi khúc gối lên khúc trước 2 giây, để đọc lời và bắt chỗ vấp.
  - (b) Đo năng lượng **dải giọng 150–3500 Hz** từng khung 20 ms (FFT), ngưỡng = sàn + 35% khoảng (sàn → mức nói) → ra các quãng lặng thật để đặt điểm cắt.
- **Câu Whisper hay bịa ra ở đoạn im hoặc ồn** (bổ sung bảng cũ):
  - *"Hãy subscribe cho kênh Ghiền Mì Gõ…"*
  - *"Các bạn hãy đăng ký kênh để ủng hộ kênh của mình nhé"*
  - *"Cảm ơn các bạn đã theo dõi và hẹn gặp lại"*

  Thấy các câu này giữa bài → khúc đó là tiếng ồn hoặc giọng nhỏ. Phải cắt lát nhỏ hơn để nghe lại, đừng vội xoá.

### 1.2. Tốc độ nói
- Đo số chữ/giây của bản đã cắt. Mẫu 63 nói **4,8 chữ/giây**.
- Chậm hơn mẫu thì tăng tốc cả bài (`setpts=PTS/k` + `atempo=k`):
  - Video 64 gốc 4,0 chữ/giây → tăng **1,2x**
  - Video 65 gốc 4,1 chữ/giây → tăng **1,15x**
- Áp tăng tốc ở **bước cuối, cho cả khung hình đã ghép**. Nhờ vậy mọi mốc chèn ghi theo thời gian bản chưa tăng tốc, không phải tính lại.

### 1.3. Màu
- Mẫu 63 đậm màu **gấp đôi** file iPhone gốc. Đo vùng tường: độ bão hoà 0,38 so với 0,19; độ lệch chuẩn sáng 43 so với 34.
- Cảnh mặt người (2A): `eq=saturation=1.7:contrast=1.18:gamma=0.97,colorbalance=rm=0.05:gm=-0.04:bm=0.015:bh=0.04`
- Cảnh hội trường (2B): `eq=saturation=1.25:contrast=1.06` (nhẹ hơn, áp cho cả cảnh chèn để đồng bộ).
- 2A: chỉnh màu **chỉ nền mặt người**. Cảnh chèn giữ màu gốc.

### 1.4. Chèn cảnh phải "khôn" (Sếp chê 2 lần trước khi chốt)
- **Mỗi cảnh chèn phải khớp NGHĨA câu đang nói**, không chỉ đúng chủ đề chung. Cảnh "robot dắt chó ngoài phố" cho câu "bao nhiêu tiền" là bị chê "không liên quan".
- **Ưu tiên video trend của chính kênh** (`HUY MKT\03.PAGE QUANG HUY ROBOT\`), rồi mới tới clip lấy trên mạng. Bảng đã dùng:

  | Câu nói về | Lấy video |
  |---|---|
  | khả năng vận động / nhảy | 45 *Anh Robot quẩy cùng vinfast lạc hồng* (K1 nhảy bài **A Trương nội thất**; đoạn đẹp nhất giây 15–20) |
  | giữ thăng bằng / đấm đá | 43 *Robot hạ đo ván em Quang Huy Robot* (2 cú đá trúng người ở giây 5,5 và 7,5) |
  | sự kiện / thuê robot sự kiện | 44 *Robot CR7 ghi bàn* (có khoảnh khắc "GOAL" ở giây ~2), 57 *múa Trung Thu* |
  | giao tiếp | 55 *Nhanh như chớp cùng robot* |
  | người điều khiển từ xa | `64.Booster nói chuyện P1\...153932_A.mov` (người cầm tay cầm) |
  | uy tín / kinh nghiệm của Huy | VTV2 *Điểm chạm công nghệ*, file trong `Downloads` của máy legion, đoạn có dòng tên "Anh Trương Quang Huy – Kỹ sư Robotics" ở giây **334–340** |

- **Trích video trend: để chạy dài (4–7 giây), hoặc nếu ngắn thì lấy ĐÚNG khoảnh khắc hay nhất.** Robot đá người thì lấy lúc đá, không lấy lúc lấy đà. Bắt buộc soi lưới **0,5 giây/khung** (`fps=2`) để chọn, đừng chọn theo lưới thưa.
- **Clip mạng hay tự cắt xen cảnh không có robot.** Ví dụ clip "49 robot G1 múa võ" chèn cảnh Thiên Đàn trống 0,5–1 giây. Phải soi lưới 0,5 giây đúng đoạn định dùng.
- **Clip có nền mờ / viền xám** (tin VnExpress, TikTok đăng lại): đo dải ảnh thật rồi cắt sát. Cách đo: độ chênh lệch pixel liền kề theo từng hàng; ảnh thật trên 5, nền mờ dưới 2. Lọt viền xám là bị bắt lỗi ngay.
- Clip mạng có chữ sai sự thật (ví dụ nhãn BBC "Amazon launches…" trong khi lời đã sửa thành GXO) → chọn đoạn sau khi nhãn biến mất.

### 1.5. Kiểm kiến thức (bắt buộc trước khi dựng)
- Tra web từng con số/sự kiện trong lời thoại. Video 64 bắt được 2 lỗi:
  - Figure làm ở nhà máy BMW **tại Mỹ** (Spartanburg), không phải "BMW Đức"; góp phần sản xuất 30.000+ xe X3.
  - Digit chuyển **100.000 thùng hàng ở kho GXO**, không phải "Amazon, 100.000 đơn".
- Sếp chọn cách xử lý: **giữ giọng, hiện hộp chữ sửa đè** (ghi rõ con số đúng), không thu lại.
- Caption máy sinh (Gemini) cũng hay phóng đại, ví dụ "đông khách gấp mấy lần". Đọc lại và sửa trước khi bàn giao.

### 1.6. Chữ nhấn mạnh — TỪ KHOÁ BẬT ĐÚNG LÚC NÓI (Sếp chốt 13/10/2026, THAY luật "hộp chữ cả dòng" 12/10)
- 🔴 **CẤM hiện cả câu/cả dòng trước rồi tô vàng từ khoá.** Người xem đọc trước mất, tới lúc nghe thì hết bất ngờ. Nguyên văn Sếp: *"từ nào cần highlight thì từ đấy mới xuất hiện thôi và xuất hiện ngay lập tức"*.
- Chỉ hiện **đúng cụm từ khoá** (1–4 chữ), bật lên **đúng khoảnh khắc người nói bắt đầu từ đó** (sai số ≤ 0,1 giây).
- Kiểu chữ:
  - DT Phudu Black khoảng 156px, **vàng `#FFDE3C` viền đen dày + bóng**, tâm y≈1400.
  - Cụm dài thì tách 2 dòng (`"KHÔNG CẦN|CON NGƯỜI"`). Chữ rộng hơn 1050px thì tự thu nhỏ.
  - Hiệu ứng nảy: cỡ 118% → 107% → 100% trong 0,1 giây (3 ảnh PNG), kèm tiếng Pop.
  - Mỗi từ hiện tối đa 1,7 giây hoặc tới từ kế tiếp.
- **Lấy mốc từ:** Whisper ffmpeg chỉ cho mốc theo câu, nên dùng `scripts/do_moc_tu.py`. Cách làm: tìm nhị phân điểm cắt lớn nhất mà khúc nghe được vẫn còn trọn từ khoá. Sau đó **bắt buộc nghe lại**: cắt khúc bắt đầu từ mốc vừa tìm cho Whisper nghe, câu phải bắt đầu bằng đúng từ khoá. Xuất xong kiểm lần nữa trên file thành phẩm (mốc ÷ hệ số tăng tốc).
- Chọn từ khoá: **từ mang thông tin** (con số, vị trí, kết quả, lợi ích), khoảng 1 từ mỗi 5 giây. Bỏ từ Whisper nghe không chắc. Ví dụ video 65 đã bỏ "va chạm".
- CTA cuối (`"LIÊN HỆ|QUANG HUY ROBOT"`, dòng 2 màu trắng): giữ khung cuối thêm khoảng 1,6 giây (`tpad=stop_mode=clone` + `apad`) cho kịp đọc.
- Hộp chữ trắng cả dòng chỉ còn dùng để **sửa sai sự thật** (mục 1.5), ví dụ "Figure tại nhà máy BMW (Mỹ)…".
- Biểu tượng minh hoạ (pin yếu đỏ / pin đầy xanh) vẫn dùng được, đặt cạnh từ khoá.
- Nhãn mục lớn (ví dụ "PHÂN KHÚC 1 / DƯỚI 300 TRIỆU"): font DT Phudu Black trắng viền đen, nền xanh `#40B6F0` kiểu nét cọ. **Cũng phải hiện đúng lúc nói.**

### 1.7. SFX (cho cuốn)

| Tiếng | Dùng khi | Âm lượng |
|---|---|---|
| Whoosh 2 | cảnh chèn bật lên | 0,30 |
| Pop | hiện hộp chữ | 0,40 |
| Ding | hiện chữ sửa sai / CTA | 0,35 |
| Cinematic hit | hiện nhãn mục lớn | 0,30 |
| **Tiếng tiền xu rơi** | đúng lúc nói giá ("bao nhiêu tiền", "dưới 300 triệu"…) | 0,4 |
| Cash register | ngay sau tiếng tiền xu | 0,8 |
| Slap | cú đá trúng người | 0,22 |
| Party horn | khoảnh khắc ghi bàn | 0,5 |

- Tiếng tiền xu rơi: Mixkit **"Coins sound" id 2000**, miễn phí bản quyền: `https://assets.mixkit.co/active_storage/sfx/2000/2000-preview.mp3`.
- **Đo bằng ebur128 momentary**: SFX không được to hơn giọng quá +2…+3 dB. Lần đầu để tiền xu 0,9 → to hơn giọng 7 dB, lấn lời.
- Giọng ở bước mix cuối: `highpass=f=80`; môi trường ồn thêm `afftdn=nf=-30`. **Chỉ lọc ở bước mix cuối**, không lọc trước khi đo thoại.
- Không nhạc nền (mẫu 63 không có; đo sàn ồn bản mẫu bằng bản gốc).

### 1.8. Ảnh bìa (bắt buộc)
- **Bìa = khung đầu tiên của video** (hiện khoảng 0,4 giây) + xuất kèm file `<tên>-Cover.jpg` cạnh video.
- Bố cục mẫu 63:
  - Nửa trên (0–1150) là mặt người hoặc cảnh chính.
  - Tiêu đề 3 dòng in hoa DT Phudu Black khoảng 112–118px, nền xanh nét cọ, đặt đè đường nối (tâm y≈960).
  - Nửa dưới (1150–1920) là ảnh robot rõ nét, đúng chủ đề.
- Chọn khung **sắc nét, không nhoè chuyển động, mắt mở**. Soi ảnh bìa xong mới xuất (đã 3 lần chọn sai khung: nhoè, mắt nhắm, mặt robot bị cắt).

### 1.9. Âm lượng, logo, outro
- Chuẩn **-14 LUFS**, đỉnh ≤ -1,5 dBTP: loudnorm đo 2 lượt, lượt 2 `linear=true`.
- **Kênh cá nhân Quang Huy Robot: không logo, không outro** (giống mẫu 63).

---

## 2. Riêng Kiểu 2A — Huy nói chuyện + khung nổi

Mặt Huy trong khung quay iPhone (1080x1920) chiếm **y≈590–1350** (cằm ở y≈1350, đo trên ảnh Sếp gửi 12/10). Đây là con số quyết định mọi vị trí.

| Thứ | Vị trí (1080x1920) | Ghi chú |
|---|---|---|
| Khung dọc | x135, y240, rộng 735, cao tối đa 1305 | che mặt — được, như mẫu 63 |
| Khung ngang trên | y210, full rộng, cao ≤760 | |
| Khung ngang giữa | y560 | |
| **Khung trong HOOK** | **y0–590, sát mép trên, cao 590** (`crop=1080:590:0:ih-590`) | 🔴 **hook (~10 giây đầu) KHÔNG được che mặt**. Đặt dưới cằm là sai, Sếp bắt đưa lên trên |
| Hộp chữ + nhãn mục | tâm y≈1480–1500 (từ y≈1400 trở xuống) | 🔴 **không được đè lên mặt** |
| Ảnh sản phẩm cắt nền | 2 góc dưới, cao 330–400 | không đè nhãn |

- **Tần suất:** khoảng 1 cảnh/10 giây, mỗi cảnh 2–6 giây. Mẫu 63 có 12 cảnh trong 122 giây, phủ khoảng 35% thời lượng. Bản 1 của video 64 lồng 15 cảnh trong 161 giây (55%) và bị chê "lồng quá nhiều".
- Câu **"hiểu biết cá nhân / kinh nghiệm"** → chèn cảnh Huy lên VTV2 (mục 1.4).

## 3. Riêng Kiểu 2B — Voice POV + chèn full màn

- Nền là clip có giọng (ví dụ `IMG_6857.MOV`). Cảnh chèn **thay hẳn khung hình**, giọng vẫn chạy liền.
- Clip DJI 4K ngang → cắt dọc 9:16 quanh tâm chủ thể: `crop=ih*9/16:ih:(iw-ih*9/16)*tam_x:0,scale=1080:1920`. Từ 4K cắt ra vẫn nét.
- 🔴 **Tốc độ cảnh chèn tự khớp câu nói**: chọn đoạn nguồn [s0,s1] rồi kéo hoặc nén về đúng độ dài câu, `setpts=(PTS-STARTPTS)*(độ dài câu)/(s1-s0)`. Giữ hệ số trong khoảng 0,7–1,6 để không giật hoặc lê thê.
- **Nhặt cảnh gian hàng ĐÔNG NGƯỜI** cho các câu "khách dừng lại", "nổi bật nhất". Cuối bài dồn liền 2–3 cảnh đông nhất.
- Câu mở kiểu "giữa rất nhiều gian hàng…" → **cảnh dọc hành lang hội chợ** (nhìn dọc dãy gian, mái vòm), **tua nhanh cho cảm giác LƯỚT QUA** (Sếp chê bản chạy 1x là "hơi chậm"). 🔴 **Chỉ lấy đoạn camera ĐI THẲNG giữa hành lang, cắt TRƯỚC lúc camera lia vào gian hàng.** Soi lưới 0,5 giây để tìm giây bắt đầu lia. Video 65: `DJI_20260911153758_0352_D.MP4` giây 0–6,6 (lia vào gian từ giây 6,8).
- 🔴 **Đầu video đừng cắt dồn dập** (Sếp chê "chóng mặt"): 15 giây đầu tối đa 2 cảnh chèn, cảnh thứ 2 nên là cảnh tĩnh (khách ngồi xem). Bỏ các cảnh lia trùng ý.
- **Chống rung vidstab: ĐỪNG dùng cho cảnh quay tay trong hội trường đông người.** Đo thật video 65: độ lệch khung liền kề tăng từ 14,7 lên 21,0 (tệ hơn), vì người đi lại và sàn bóng làm bộ dò bám nhầm. Muốn bớt chóng mặt thì bớt nhát cắt, đừng trông vào chống rung.
- Đoạn người nói đang **demo trực tiếp** (vuốt mặt robot, đứng chắn cho robot né) → **giữ cảnh gốc**, chỉ thêm chữ. Không chèn đè lên phần demo.

## 4. Script mẫu
`scripts/do_moc_tu.py`: dò mốc bắt đầu từng từ khoá (mục 1.6).

`scripts/mau_voice_pov.py`: bản dựng video 65, đủ 4 bước.
- `assets`: ảnh bìa + hộp chữ
- `compose`: ghép cảnh chèn có tốc độ tự khớp + chữ + tăng tốc
- `sfx`: trộn SFX

Chép sang Workspace của buổi quay, sửa 3 bảng `BROLL / TEXTS / SFX` cùng đường dẫn rồi chạy:
```
python mau_voice_pov.py <thư mục làm việc> [assets|compose|sfx|all]
```
Kiểu 2A dùng cùng khung này: thêm loại khung `v` / `ht` / `top` theo bảng mục 2. Nền mặt người thì không tăng màu cho cảnh chèn.

# Sổ SFX — cây quyết định "khoảnh khắc nào dùng tiếng nào" (lập 2026-07-17)
<!-- tags: chung -->

> 🔴 **VIẾT LẠI TOÀN BỘ 03/08/2026 (Sếp Huy chỉ đạo sau khi bắt lỗi thật: nghe "Ding" thấy không đúng "ting" mong muốn, và nhận xét thẳng "bộ quy tắc SFX này đang có vấn đề vãi").** Đây là bản thay thế hoàn toàn 2 luật cũ (03/07 "chỉ gắn khi khớp hành động" và 19/07 "mỗi thẻ chữ bắt buộc 1 pop") — cả 2 bản cũ đọc theo lịch sử ở cuối file, không dùng để dựng nữa.
>
> **3 lỗi gốc đã tìm ra, sửa cả 3:**
> 1. **Chọn tiếng theo TÊN FILE, chưa ai đo ÂM THANH THẬT.** Vụ "Ding" là bằng chứng: tên nghe hợp nhưng đo sóng thật thì tắt sau **0.058 giây**, gần như không có đuôi ngân — không phải tiếng "ting" nghe thấy trong đầu. Đã đo lại **cả 39 file trong kho** bằng `librosa` (độ sáng phổ tần, độ ngân, lead-in) — bảng đầy đủ ở mục "PHÂN LOẠI THEO ÂM THANH ĐO ĐƯỢC" bên dưới, dùng thay cho việc đoán qua tên.
> 2. **Luật "mỗi thẻ chữ = 1 SFX" tối ưu sai đại lượng** — đếm SỐ LƯỢNG thẻ chữ thay vì đếm ĐỘ QUAN TRỌNG của khoảnh khắc. Tra nguồn ngành 2026 (TikTok editing trends, SFX Engine, B2B video sound design case study — link cuối file): thuật toán và người xem đều phân biệt được SFX **có chủ đích** với SFX **rải đều cho đủ số** — dùng sai kiểu bị đánh giá là "spam tiếng", không phải "chuyên nghiệp". Với khách hàng Roboworld là **chủ nhà máy/chuỗi nhà hàng** (không phải Gen Z lướt giải trí), nguồn B2B càng nhấn: SFX nên **tinh tế, có chức năng dẫn mắt**, không phải nhồi liên tục.
> 3. **Không phân biệt "đổi CẢNH" với "đổi Ý"** — luật cũ gắn SFX theo từng lần cắt hình, trong khi 1 dòng chữ hoàn toàn có thể giữ nguyên qua 3-4 lần đổi cảnh (đã là luật ở `style-mau.md` mục "Nhịp dựng" từ lâu: *"Text KHÔNG bắt buộc đổi theo từng cut"*) — SFX phải đi theo NHỊP CHỮ/THÔNG ĐIỆP, không đi theo nhịp cắt hình, nếu không sẽ vượt xa mọi khuyến nghị mật độ.

## NGUYÊN TẮC GỐC MỚI — "chủ đích theo Ý, không phải theo chữ/theo cắt"
<!-- tags: chung -->

**3 mốc BẮT BUỘC có SFX** (đây là khoảnh khắc quyết định giữ chân người xem, theo đúng nguồn ngành — bỏ 1 trong 3 mốc này là thiếu, không phải tùy chọn):

1. **Hook — trong 1.5 giây đầu video.** Đây là mốc "neo" người xem trước khi họ vuốt qua — luôn có ít nhất 1 SFX rõ (Pop/Whoosh/Hit tùy tông hook).
2. **Mỗi lần ĐỔI THÔNG ĐIỆP** (không phải đổi cảnh/hình) — đúng lúc dòng chữ đổi sang ý mới. Nếu 1 dòng chữ giữ nguyên qua nhiều cảnh thì CHỈ 1 SFX ở đầu đoạn đó, không lặp lại mỗi lần cắt hình bên dưới.
3. **CTA/kết** — khoảnh khắc chốt (nút bấm, lời mời để lại bình luận, khoảnh khắc cuối trước outro).

**KHÔNG bắt buộc SFX**: hard-cut bình thường trong lúc vẫn cùng 1 thông điệp. Để IM hoặc dùng whoosh RẤT nhẹ nếu cần giữ nhịp — đây chính là nguyên tắc "im lặng là vũ khí" (mục "NGUYÊN TẮC VÀNG" bên dưới) áp dụng nhất quán, thay vì lấp đầy mọi giây bằng tiếng.

**Kết quả thực tế**: mật độ SFX sẽ GIẢM so với luật cũ (không còn "1 pop/thẻ chữ" cứng) nhưng ĐÚNG LÚC hơn — 1 video Kiểu 1 có 3-4 lần đổi Ý + 1 hook + 1 CTA thường ra 4-6 lớp SFX, không phải 14 lớp/55s như luật cũ. Video nào có nhiều khoảnh khắc hành động thật (robot tương tác, phản ứng người) thì cộng thêm SFX-theo-hành-động ở mục "MA TRẬN" bên dưới — lúc đó tổng số có thể cao hơn tự nhiên, không phải ép cho đủ.

**Ca minh họa đã áp dụng ĐÚNG hướng này trước cả khi viết thành luật** (video-1 CC1 Go Vĩnh Phúc, dựng 03/08/2026): 8 cảnh, 4 lần đổi thông điệp (hook → "tự di chuyển..." → "khách hàng thích thú..." → CTA), chỉ 4 lớp SFX đặt đúng 4 mốc đổi ý — không lặp theo 8 lần cắt cảnh bên dưới.

## VỤ "DING" — kết luận + việc còn dở
<!-- tags: chung -->

Đo thật: `34 - Ding.mp3` là tiếng **sáng nhưng KHÔ, tắt sau 0.058s** — hợp vai "click xác nhận nhanh, gọn" hơn là "ting" ngân nhẹ mà Sếp hình dung. Đã dò cả kho tìm file thay thế bằng đo sóng (độ sáng + độ ngân), nhưng **kiểm kỹ hơn thì phát hiện ứng viên sáng nhất kho (`22 - Display digits`) thực chất là 1 tiếng CLICK rất ngắn** (đỉnh chỉ dài ~60ms rồi tụt), không phải tiếng chuông ngân — đo brightness cao KHÔNG đồng nghĩa nghe "ting".

**Quyết định tạm thời (chờ Sếp nghe xác nhận)**:
- **`14 - Apple notification.mp3`** lên làm tiếng CHÍNH cho vai "xác nhận/chốt ý nhẹ nhàng" (brand-safe, mềm hơn, gần với cảm giác "ting thông báo" nhất trong kho hiện có) — thay cho vị trí độc quyền cũ của Ding.
- **`34 - Ding.mp3`** giữ lại làm phương án PHỤ, dùng khi cần tiếng khô/gọn/nhanh hơn (vd chốt số liệu chạy xong).
- **CÒN THIẾU thật**: kho **chưa có** 1 tiếng "chuông ting ngân nhẹ" đúng nghĩa (bell/glass chime với đuôi rung 0.2-0.5s, brightness vừa phải chứ không quá gắt). Việc cần làm: tải bổ sung 2-3 file từ Mixkit/Pixabay (free, license rõ — xem mục "Nguồn bổ sung" cuối file) với từ khóa `"bell ting"`/`"chime confirm"`/`"UI ting"`, để vào kho Drive, rồi nghe chọn.
- 4 file nghe-thử đã chuẩn bị sẵn (đo bằng máy, CHƯA ai nghe xác nhận): `Desktop\NGHE-CHON-SFX-TING\` — Sếp nghe xong báo lại để chốt luật này thành chính thức thay vì "quyết định tạm thời" như hiện tại.

## CÂY QUYẾT ĐỊNH (đi từ trên xuống, fail bước nào dừng bước đó)
<!-- tags: chung -->

1. **Đây có phải 1 trong 3 mốc BẮT BUỘC không?** (hook 1.5s đầu / đổi thông điệp / CTA-kết) → Không phải cả 3 → mặc định KHÔNG gắn SFX, để hard-cut im lặng (trừ khi rơi vào bước 2).
2. **Trong hình có hành động/khoảnh khắc gì đang XẢY RA THẬT** (dù không phải 1 trong 3 mốc trên)? Có → đi tiếp lấy SFX hành động ở ma trận bên dưới (lớp SFX-theo-hành-động luôn được phép cộng thêm, độc lập với 3 mốc bắt buộc).
3. **Khoảnh khắc đó có ÂM GỐC hay không?** (trẻ em cười, robot beep thật, tiếng khách reo) → DÙNG ÂM GỐC (volume 0.2-0.3 theo chuẩn), KHÔNG đè SFX giả lên tiếng thật hay.
4. **Tra ma trận** → chọn NHÓM theo Ý NGHĨA khoảnh khắc, rồi **đối chiếu với bảng ÂM THANH ĐO ĐƯỢC** bên dưới để chắc chắn file chọn đúng CẢM GIÁC (sáng-giòn/trung tính/trầm-uy lực), không chỉ đúng tên.
5. **Kiểm liều lượng cả video**:
   - Không chồng quá 2 lớp tiếng cùng lúc → thẻ chữ trùng mốc (~1s) với SFX hành động sẵn có (riser/ding/hit) thì **BỎ SFX chữ**, không chồng.
   - 2 SFX cùng loại không đứng sát nhau <5s.
   - Chỉ dùng "sound quốc dân" an toàn cho B2B; **cấm** troll/meme (Bruh, Wasted, SpongeBob) — lệch thương hiệu + rủi ro bản quyền.
6. **Canh timing bằng số liệu, không áng chừng** (Peak Impact Rule — GIỮ NGUYÊN, nguồn ngành 2026 xác nhận lại đúng): lấy mốc hành động/mốc đổi Ý từ sheet/scene_changes của index (hoặc soi frame), rồi đặt `adelay` theo công thức **`offset = mốc hành động − lead-in`** (mọi file SFX đều có đoạn câm ở đầu; bảng lead-in đã đo sẵn ở `ffmpeg-recipes.md` mục 4b). Tiếng dài cắt bằng `atrim` lấy phần cần.

## PHÂN LOẠI THEO ÂM THANH ĐO ĐƯỢC — đo thật bằng `librosa` 03/08/2026, dùng thay cho đoán qua tên
<!-- tags: chung -->

Đo 3 chỉ số cho cả 39 file: **độ sáng phổ tần** (Hz — càng cao càng "giòn/chói", càng thấp càng "trầm/ấm"), **lead-in** (đoạn câm đầu file, để tính `adelay`), **độ ngân** (decay — thời gian tắt dần sau đỉnh, số càng lớn càng "ngân/vang", càng nhỏ càng "khô/gọn"). File thô đầy đủ: `scripts/` chưa có bản chính thức, xin số liệu lại nếu cần đo lại (lệnh mẫu ở cuối mục này).

### Nhóm SÁNG-GIÒN (>4000Hz) — hợp hook, xác nhận tích cực, khoảnh khắc vui
| File | Sáng (Hz) | Ngân (s) | Lead-in (s) | Cảm giác thật |
|---|---|---|---|---|
| `22 - Display digits` | 8087 | 0.66* | 0.21 | *đo cả file ra "ngân" nhưng thực chất là chuỗi tick rồi 1 click chốt rất ngắn (~60ms) — KHÔNG phải tiếng ngân thật, xem "VỤ DING" ở trên |
| `27 - In and out` | 6014 | 0.16 | 0.09 | giòn, gọn |
| `03 - Click` | 5404 | 0.04 | 0.04 | click khô, rất ngắn |
| `31 - Clock ticking` | 5041 | 0.05 | 0.04 | tick đồng hồ, lặp |
| `18 - Camera shutter` | 4764 | 0.16 | 0.04 | tiếng chụp ảnh |
| `05 - Cash register` | 4700 | 0.52 | 0.05 | "cha-ching" — có ngân vừa phải, hợp cảnh số liệu/tiết kiệm |
| `25 - Anvil` | 4350 | 0.29 | 0.04 | va chạm kim loại, dễ quá đà |
| `35 - Glitch 2` | 4332 | 0.63 | 0.07 | hiệu ứng số, có ngân |

### Nhóm TRUNG TÍNH (1000-4000Hz) — chuyển động, công nghệ, xác nhận nhẹ
| File | Sáng (Hz) | Ngân (s) | Lead-in (s) | Cảm giác thật |
|---|---|---|---|---|
| `33 - Crumpled paper` | 4037 | 0.86 | 0.12 | |
| `23 - Party horn` | 3881 | 0.49 | 0.06 | |
| `30 - Glass shatter` | 3714 | 0.27 | 0.04 | |
| `01 - riser-metallic` | 3608 | 0.12 | **0.92** | riser build-up dài, lead-in lớn nhất kho — canh cẩn thận |
| `34 - Ding` | 3605 | **0.06** | 0.04 | sáng nhưng KHÔ — không phải "ting ngân", xem mục trên |
| `16 - Bone crack` | 3515 | 0.10 | 0.05 | |
| `20 - Paper` | 3298 | 0.07 | 0.13 | |
| `24 - Glitch` | 3294 | 0.26 | 0.05 | |
| `32 - Mario coin` | 3220 | 0.78 | 0.04 | sáng, có ngân — nhưng thiên game/vui rõ, cân nhắc kỹ với tông B2B |
| `Magic Chime` | 3196 | 0.80 | 1.27 | file dài 9.8s, phải `atrim` lấy đúng khúc cần |
| `28 - Sudden suspense` | 3078 | 0.42 | 0.06 | |
| `02 - Gear` | 3004 | 0.53 | 0.04 | |
| `07 - Wrong answer` | 2998 | 0.48 | 0.04 | thiên game show, liều thấp |
| `17 - Slap` | 2943 | 0.28 | 0.07 | |
| `21 - Kids yeyy` | 2616 | 2.38 | 0.08 | tiếng trẻ reo, ngân dài nhất nhóm |
| `15 - Anime wow` | 2345 | 1.55 | 0.04 | thiên hài, chỉ video tông vui |
| `19 - Whoosh 2` | 2180 | 0.12 | 0.06 | |
| `08 - Woosh fire transition` | 2069 | 0.44 | 0.13 | |

### Nhóm TRUNG-TRẦM (1000-1700Hz) — thông báo mềm, chuyển cảnh êm
| File | Sáng (Hz) | Ngân (s) | Lead-in (s) | Cảm giác thật |
|---|---|---|---|---|
| `14 - Apple notification` | 1668 | 0.20 | 0.04 | **mềm, sạch — đang đề xuất làm "ting/xác nhận" chính, xem "VỤ DING"** |
| `Rake Swing Whoosh Close` | 1573 | 0.15 | 0.16 | |
| `04 - Pop` | 1402 | 0.10 | 0.05 | pop chuẩn, dùng cho hook/vật thể xuất hiện |
| `06 - Aww` | 1248 | 0.95 | 0.09 | |
| `01 - Whoosh` | 1167 | 0.16 | 0.07 | |
| `13 - Iphone receive` | 1062 | 0.24 | 0.08 | |
| `12 - Iphone send` | 1055 | 0.12 | 0.09 | |

### Nhóm TRẦM-UY LỰC (<1000Hz) — nhấn mạnh, CTA mạnh, chốt lớn
| File | Sáng (Hz) | Ngân (s) | Lead-in (s) | Cảm giác thật |
|---|---|---|---|---|
| `09 - Game point` | 855 | 0.19 | 0.04 | |
| `10 - Discord join` | 557 | 0.28 | 0.04 | |
| `29 - Boom` | 540 | 0.57 | 0.04 | trầm, uy lực — hợp CTA/con số gây sốc |
| `11 - Discord leave` | 343 | 0.34 | 0.04 | |
| `26 - Cinematic hit` | 270 | 1.50 | **0.49** | trầm nhất kho, ngân dài — hợp cú "đấm" nghiêm túc, lead-in lớn |

**Lệnh đo lại 1 file mới** (khi Sếp/Drive thêm SFX mới vào kho, đo cho vào đúng nhóm):
```powershell
python -c "
import librosa, numpy as np
y, sr = librosa.load(r'<duong dan file>', sr=22050, mono=True)
rms = librosa.feature.rms(y=y, frame_length=1024, hop_length=256)[0]
times = librosa.frames_to_time(np.arange(len(rms)), sr=sr, hop_length=256)
peak_idx = int(np.argmax(rms))
thresh = 0.2*rms[peak_idx]; above = np.where(rms>=thresh)[0]
lead_in = float(times[above[0]]) if len(above) else 0.0
tail = np.where(rms[peak_idx:] < 0.1*rms[peak_idx])[0]
decay = float(times[peak_idx+tail[0]]-times[peak_idx]) if len(tail) else float(len(y)/sr-times[peak_idx])
cent = librosa.feature.spectral_centroid(y=y, sr=sr, hop_length=256)[0]
mask = rms > 0.3*rms[peak_idx]
bright = float(np.median(cent[:len(mask)][mask[:len(cent)]]))
print('lead_in=%.3f decay=%.3f brightness=%.0fHz' % (lead_in, decay, bright))
"
```

## MA TRẬN: khoảnh khắc Roboworld → SFX trong kho (đã đo thời lượng)
<!-- tags: chung -->

> **Đếm lại thật 21/07/2026**: `SFX/Bo 35 SFX/` có **36 file**, cộng **3 file rời** ngay ngoài `SFX/` = **39 file**. Con số "38" ghi trước đây và tên folder "Bo 35 SFX" đều không khớp — khi cần chắc chắn thì liệt kê thư mục, đừng trích số từ tài liệu.

### Nhóm CHUYỂN ĐỘNG (robot/camera lướt)
<!-- tags: chung -->
| Khoảnh khắc trong hình | File | Ghi chú |
|---|---|---|
| Robot LƯỚT NGANG qua camera nhanh | `01 - Whoosh` (0.6s) hoặc `19 - Whoosh 2` (0.4s — gắt hơn) | đặt đúng frame robot gần camera nhất |
| Robot tiến TỪ XA VỀ GẦN camera | `Rake Swing Whoosh Close` (2.0s) | tiếng dài theo cả cú tiến |
| Chuyển cảnh whoosh/quét mạnh (xfade smoothleft, wipe...) | `08 - Woosh fire transition` (1.7s) | SFX đi KÈM chuyển cảnh — đặt trùng mốc offset |
| Build-up trước cú reveal/drop nhạc | `01 - riser-metallic` (2.8s) | kết thúc riser ĐÚNG mốc reveal |

### Nhóm VA CHẠM / NHẤN MẠNH
<!-- tags: chung -->
| Khoảnh khắc | File | Ghi chú |
|---|---|---|
| Freeze frame + thẻ tên robot đập vào | `26 - Cinematic hit` (3.4s — atrim lấy 1.2s đầu) | cú "trầm uy lực", hợp video nghiêm túc |
| Con số gây sốc hiện + hình RUNG (hiệu ứng WOW-3/8) | `29 - Boom` (1.3s) | chỉ khi hình có rung/impact thật sự |
| Robot đặt món/hạ khay CHẠM bàn | `25 - Anvil` (1.2s — volume hạ 0.5, nghe quá đà thì bỏ) | cân nhắc — dễ quá lố |
| Đồ vật rơi/va trong hình | `16 - Bone crack`/`17 - Slap`/`30 - Glass shatter` | CHỈ khi đúng nghĩa đen; mặc định né (thiên meme) |

### Nhóm SỐ LIỆU / THÀNH QUẢ (dùng khi màn hình đang show số/kết quả)
<!-- tags: chung -->
| Khoảnh khắc | File | Ghi chú |
|---|---|---|
| Số liệu doanh thu/tiết kiệm CHỐT trên hình | `05 - Cash register` (0.9s) | đúng lúc số chốt, không lúc số đang chạy |
| Số ĐANG NHẢY (hiệu ứng counter SỐ 9) | `22 - Display digits` (2.2s) | chạy theo đoạn số nhảy |
| Chốt điểm/hoàn thành checklist vui | `32 - Mario coin` (1.1s)/`09 - Game point` (0.5s) | tông vui, kênh nghiêm túc thì dùng `14 - Apple notification` |
| Xác nhận hoàn tất/robot báo xong | `14 - Apple notification` (0.7s)/`34 - Ding` (0.7s, phương án phụ) | gọn, sạch — xem "VỤ DING" đầu file để biết vì sao đổi thứ tự ưu tiên |
| Thông báo "cấp đơn/nhận lệnh" trên UI mô phỏng | `12/13 - Iphone send/receive` | CHỈ khi hình có mô phỏng màn hình chat |

### Nhóm CẢM XÚC NGƯỜI XEM (cẩn thận nhất — dễ phá tông)
<!-- tags: chung -->
| Khoảnh khắc | File | Ghi chú |
|---|---|---|
| Cảnh dễ thương (robot mèo, trẻ em) KHÔNG có âm gốc tốt | `06 - Aww` (1.5s) | nếu âm gốc có tiếng cười thật → ưu tiên âm gốc |
| Trẻ em ùa vào vui | `21 - Kids yeyy` (3.6s) | CHỈ thay thế khi âm gốc hỏng |
| Khách trầm trồ/cú "không thể tin nổi" | `15 - Anime wow` (1.9s) | THIÊN HÀI — chỉ video tông vui, cấm video corporate |
| Tình huống "sai cách cũ" trong kịch bản vấn đề-giải pháp | `07 - Wrong answer` (0.9s) | meme game show — liều thấp |
| Tiệc/khai trương/kết quả lớn | `23 - Party horn` (0.9s) | đúng bối cảnh lễ |

### Nhóm KỸ THUẬT / MÁY MÓC
<!-- tags: chung -->
| Khoảnh khắc | File | Ghi chú |
|---|---|---|
| Tay vặn ốc/sửa chữa robot TRONG HÌNH | `Ratchet Wrench Slow` (1.2s) | đúng nhịp tay vặn |
| Bánh răng/cơ cấu chuyển động cận cảnh | `02 - Gear` (1.2s) | |
| Bấm nút/chạm màn hình robot | `03 - Click` (0.3s) | đúng frame ngón tay chạm |
| Freeze frame chụp lại khoảnh khắc | `18 - Camera shutter` (0.5s) | đi cặp với hiệu ứng đóng băng WOW-5 |
| Hiệu ứng glitch RGB (WOW-4) đang chạy | `24 - Glitch` (1.3s)/`35 - Glitch 2` (1.0s) | SFX + hình glitch phải TRÙNG mốc |
| Đếm thời gian/chờ đợi trong kịch bản | `31 - Clock ticking` (2.0s) | |
| Suspense trước reveal | `28 - Sudden suspense` (1.1s) | |
| Lật trang/giấy tờ trong hình | `20 - Paper` (1.1s)/`33 - Crumpled paper` (1.9s) | |
| Nhân vật vào/rời khung (UI style) | `10/11 - Discord join/leave` | thiên meme — mặc định né |
| Khoảnh khắc "phép màu"/twinkle | `Magic Chime` (9.8s — atrim từng khúc) | lấy 1-1.5s, đừng dùng cả file |
| Pop nhẹ vật thể xuất hiện | `04 - Pop` (0.4s) | vật thể THẬT xuất hiện (ảnh SP bay vào), không phải text |

## NGUYÊN TẮC VÀNG từ giáo lý sound design (tra cứu nguồn ngành 17/07/2026 + bồi thêm 03/08/2026)
<!-- tags: chung -->

1. **"Ngũ hành" SFX chuẩn ngành** khớp với kho mình: Whoosh (chuyển động/reveal) — Hit (chốt cú cắt mạnh/title slam) — Riser (dẫn lên đỉnh) — Ambience (nền không gian) — Braaam (trailer đại cảnh, ít hợp shorts Roboworld).
2. **Đỉnh riser phải TRÙNG CHÍNH XÁC mốc reveal** — đặt riser sao cho điểm cao trào rơi đúng frame cắt/hiện thẻ, không phải "bắt đầu riser tại mốc".
3. **IM LẶNG LÀ VŨ KHÍ**: hạ nhạc/im ~0.3-0.5s NGAY TRƯỚC cú hit → hit đấm mạnh gấp bội. Đừng lấp đầy mọi giây bằng âm thanh — **đây giờ là nguyên tắc TRUNG TÂM của cả bộ luật** (mục "NGUYÊN TẮC GỐC MỚI" đầu file), không còn là ghi chú phụ.
4. **Layering tạo chất riêng**: whoosh trơn + 1 lớp mỏng đặc trưng bên dưới. Gợi ý chữ ký Roboworld: whoosh + beep robot rất nhẹ = "whoosh robot" nhận diện thương hiệu (chờ Sếp duyệt thử).
5. **Giọng người là VUA**: SFX không bao giờ được đè lên từ quan trọng MC đang nói — đặt SFX vào khoảng nghỉ giữa câu, hoặc hạ volume SFX khi trùng thoại (ducking áp cho cả SFX, không riêng nhạc).
6. **Sai số cho phép tính bằng chục mili-giây**: transient (đầu tiếng) phải khớp frame hành động — khớp luật đo-frame sẵn có của mình.
7. **MỚI 03/08/2026 — "chủ đích thắng số lượng"**: nguồn TikTok 2026 xác nhận thuật toán/người xem phân biệt được SFX rải đều cho đủ số với SFX đặt đúng khoảnh khắc quan trọng — dùng sai kiểu (nhồi liên tục) bị đọc là kém tinh tế, không phải "chuyên nghiệp, dày dặn" như hiểu nhầm trước đây.
8. **MỚI 03/08/2026 — tông B2B khác tông giải trí**: nguồn sound design cho video demo B2B khuyên SFX tinh tế/có chức năng dẫn mắt, KHÔNG nhồi kiểu nội dung giải trí đại chúng — nhắc lại vì khách hàng Roboworld là chủ doanh nghiệp, không phải khán giả TikTok phổ thông.

Nguồn: SFX Engine — Ultimate Guide to Sound Effects for Video Editing; Krotos — What is sound design; Editors Keys — Ultimate Guide to Sound Design; Vortex Xcel — TikTok Editing Trends 2026; SFX Engine — TikTok sound effects tips; Advids — Case Study: Measurable Impact of Professional Sound Design on B2B Video Performance.

## Nguồn bổ sung khi kho thiếu (xếp theo độ ưu tiên)
<!-- tags: chung -->

1. **Kho 39 file hiện tại** — nguồn chính. LƯU Ý license: phần lớn gốc YouTube Audio Library — về lý giấy phép chỉ chắc chắn cho YouTube; với FB/TikTok là vùng xám (rủi ro thấp với SFX ngắn, nhưng biết để không cãi được thì thay dần).
2. 🔴 **CẦN LÀM NGAY (03/08/2026)**: kho thiếu 1 tiếng "chuông ting ngân nhẹ" đúng nghĩa — tìm trên **Mixkit/Pixabay** (free, license rõ) với từ khóa `"bell ting"`/`"chime confirm"`/`"UI ting"`, tải 2-3 ứng viên, đo bằng lệnh ở mục "PHÂN LOẠI THEO ÂM THANH" rồi để Sếp nghe chọn, sau đó đẩy vào Drive kho SFX.
3. 📦 **Freesound.org API** (key miễn phí, lọc license CC0 = thương mại thoải mái) — đấu tự động được như đã làm với Pexels; chờ Sếp gật tạo key.
4. 📦 **Mixkit / Pixabay SFX** — free thương mại rõ ràng, tải tay bổ sung vào kho Drive.
5. 💰 **ElevenLabs SFX** (sinh tiếng theo mô tả, ~11-40 credits/giây, dùng key sẵn có) — cho tiếng "đo ni" kho không có (vd "tiếng bánh xe robot lăn trên sàn gỗ") — chờ Sếp gật vì credits chung.
6. ❌ Né: BBC archive (phi thương mại), trending sounds TikTok (bản quyền), kho SFX "crack".

## Trạng thái duyệt
<!-- tags: chung -->

- **Khung mới (3 mốc bắt buộc + phân loại theo âm thanh đo được) đã áp dụng chính thức từ 03/08/2026** theo chỉ đạo Sếp Huy ("làm lại đi").
- **Còn CHỜ Sếp xác nhận**: (a) file "ting" thay Ding — 4 ứng viên ở `Desktop\NGHE-CHON-SFX-TING\`, hiện đang tạm dùng `14 - Apple notification`; (b) mật độ mới (giảm SFX/video so với luật cũ) có đúng cảm giác Sếp muốn không, nghe thử video tiếp theo dựng theo luật này rồi góp ý chỉnh tiếp.
- Lịch sử 2 luật cũ (03/07 gốc, 19/07 sửa lần 1) đã bị thay thế hoàn toàn — không tham chiếu nữa, giữ trong lịch sử git nếu cần tra cứu.

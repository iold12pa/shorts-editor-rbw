# Sổ SFX — cây quyết định "khoảnh khắc nào dùng tiếng nào" (lập 2026-07-17)

> ⚠️ **CẬP NHẬT 19/07/2026 — luật nền của sổ này ĐÃ ĐỔI.** Luật gốc 03/07/2026 ("KHÔNG gắn SFX chỉ vì text vừa hiện", liều 3-5 SFX/video) **đã bị Sếp Huy thay** bằng luật mới: **mỗi thẻ chữ đều kèm 1 SFX pop hợp nghĩa** (kiểu TikTok/Reels, thực tế 14 lớp/55s) — xem `ffmpeg-recipes.md` mục 4b. Cây quyết định + ma trận bên dưới **vẫn dùng tốt cho lớp SFX-theo-hành-động**, nhưng phần liều lượng ở bước 4 đã lỗi thời, đọc theo bản vá ngay bên dưới.

> Phần vẫn còn nguyên giá trị: **SFX khớp hành động cụ thể trong hình** (tiếng cờ lê khi vặn ốc, whoosh khi chuyển cảnh) — luật mới THÊM lớp text-pop chứ không bỏ lớp này.

## CÂY QUYẾT ĐỊNH (đi từ trên xuống, fail bước nào dừng bước đó)

1. **Trong hình có hành động/khoảnh khắc gì đang XẢY RA THẬT?** Có → đi tiếp lấy SFX hành động. Không có nhưng **có thẻ chữ xuất hiện** → gắn 1 SFX **pop hợp nghĩa chữ** (luật mới 19/07, xem bước 4 bản vá).
2. **Khoảnh khắc đó có ÂM GỐC hay không?** (trẻ em cười, robot beep thật, tiếng khách reo) → DÙNG ÂM GỐC (volume 0.2-0.3 theo chuẩn), KHÔNG đè SFX giả lên tiếng thật hay.
3. **Tra ma trận bên dưới** → chọn NHÓM → chọn FILE theo tiêu chí: thời lượng khớp khoảnh khắc (tiếng ngắn cho hành động chớp nhoáng, riser dài cho build-up), tông video (nghiêm túc vs vui).
4. **Kiểm liều lượng cả video — BẢN VÁ 19/07/2026** (thay dòng "tối đa 3-5 SFX/video" cũ):
   - Mỗi thẻ chữ = 1 pop hợp nghĩa (hook→Pop, tên sản phẩm→notification, chữ công nghệ→Glitch, chữ bùng nổ→Boom).
   - **Vẫn giữ**: không chồng quá 2 lớp tiếng cùng lúc → thẻ chữ trùng mốc (~1s) với SFX hành động sẵn có (riser/ding/hit) thì **BỎ pop**, không chồng.
   - **Vẫn giữ**: 2 SFX cùng loại không đứng sát nhau <5s.
   - Chỉ dùng "sound quốc dân" an toàn cho B2B; **cấm** troll/meme (Bruh, Wasted, SpongeBob) — lệch thương hiệu + rủi ro bản quyền.
5. **Canh timing bằng số liệu, không áng chừng**: lấy mốc hành động từ sheet/scene_changes của index (hoặc soi frame), rồi đặt `adelay` theo công thức **`offset = mốc hành động − lead-in`** (mọi file SFX đều có đoạn câm ở đầu; bảng lead-in 11 file đã đo sẵn ở `ffmpeg-recipes.md` mục 4b — riser lệch tới 964ms nếu đặt sai). Tiếng dài cắt bằng `atrim` lấy phần cần.

## MA TRẬN: khoảnh khắc Roboworld → SFX trong kho (38 file, đã đo thời lượng)

### Nhóm CHUYỂN ĐỘNG (robot/camera lướt)
| Khoảnh khắc trong hình | File | Ghi chú |
|---|---|---|
| Robot LƯỚT NGANG qua camera nhanh | `01 - Whoosh` (0.6s) hoặc `19 - Whoosh 2` (0.4s — gắt hơn) | đặt đúng frame robot gần camera nhất |
| Robot tiến TỪ XA VỀ GẦN camera | `Rake Swing Whoosh Close` (2.0s) | tiếng dài theo cả cú tiến |
| Chuyển cảnh whoosh/quét mạnh (xfade smoothleft, wipe...) | `08 - Woosh fire transition` (1.7s) | SFX đi KÈM chuyển cảnh — đặt trùng mốc offset |
| Build-up trước cú reveal/drop nhạc | `01 - riser-metallic` (2.8s) | kết thúc riser ĐÚNG mốc reveal |

### Nhóm VA CHẠM / NHẤN MẠNH
| Khoảnh khắc | File | Ghi chú |
|---|---|---|
| Freeze frame + thẻ tên robot đập vào | `26 - Cinematic hit` (3.4s — atrim lấy 1.2s đầu) | cú "trầm uy lực", hợp video nghiêm túc |
| Con số gây sốc hiện + hình RUNG (hiệu ứng WOW-3/8) | `29 - Boom` (1.3s) | chỉ khi hình có rung/impact thật sự |
| Robot đặt món/hạ khay CHẠM bàn | `25 - Anvil` (1.2s — volume hạ 0.5, nghe quá đà thì bỏ) | cân nhắc — dễ quá lố |
| Đồ vật rơi/va trong hình | `16 - Bone crack`/`17 - Slap`/`30 - Glass shatter` | CHỈ khi đúng nghĩa đen; mặc định né (thiên meme) |

### Nhóm SỐ LIỆU / THÀNH QUẢ (dùng khi màn hình đang show số/kết quả)
| Khoảnh khắc | File | Ghi chú |
|---|---|---|
| Số liệu doanh thu/tiết kiệm CHỐT trên hình | `05 - Cash register` (0.9s) | đúng lúc số chốt, không lúc số đang chạy |
| Số ĐANG NHẢY (hiệu ứng counter SỐ 9) | `22 - Display digits` (2.2s) | chạy theo đoạn số nhảy |
| Chốt điểm/hoàn thành checklist vui | `32 - Mario coin` (1.1s)/`09 - Game point` (0.5s) | tông vui, kênh nghiêm túc thì dùng `34 - Ding` |
| Xác nhận hoàn tất/robot báo xong | `34 - Ding` (0.7s)/`14 - Apple notification` (0.7s) | gọn, sạch, an toàn nhất nhóm |
| Thông báo "cấp đơn/nhận lệnh" trên UI mô phỏng | `12/13 - Iphone send/receive` | CHỈ khi hình có mô phỏng màn hình chat |

### Nhóm CẢM XÚC NGƯỜI XEM (cẩn thận nhất — dễ phá tông)
| Khoảnh khắc | File | Ghi chú |
|---|---|---|
| Cảnh dễ thương (robot mèo, trẻ em) KHÔNG có âm gốc tốt | `06 - Aww` (1.5s) | nếu âm gốc có tiếng cười thật → ưu tiên âm gốc |
| Trẻ em ùa vào vui | `21 - Kids yeyy` (3.6s) | CHỈ thay thế khi âm gốc hỏng |
| Khách trầm trồ/cú "không thể tin nổi" | `15 - Anime wow` (1.9s) | THIÊN HÀI — chỉ video tông vui, cấm video corporate |
| Tình huống "sai cách cũ" trong kịch bản vấn đề-giải pháp | `07 - Wrong answer` (0.9s) | meme game show — liều thấp |
| Tiệc/khai trương/kết quả lớn | `23 - Party horn` (0.9s) | đúng bối cảnh lễ |

### Nhóm KỸ THUẬT / MÁY MÓC
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

## NGUYÊN TẮC VÀNG từ giáo lý sound design (tra cứu nguồn ngành 17/07/2026 — bồi thêm cho cây quyết định)

1. **"Ngũ hành" SFX chuẩn ngành** khớp với kho mình: Whoosh (chuyển động/reveal) — Hit (chốt cú cắt mạnh/title slam) — Riser (dẫn lên đỉnh) — Ambience (nền không gian) — Braaam (trailer đại cảnh, ít hợp shorts Roboworld).
2. **Đỉnh riser phải TRÙNG CHÍNH XÁC mốc reveal** — đặt riser sao cho điểm cao trào rơi đúng frame cắt/hiện thẻ, không phải "bắt đầu riser tại mốc".
3. **IM LẶNG LÀ VŨ KHÍ**: hạ nhạc/im ~0.3-0.5s NGAY TRƯỚC cú hit → hit đấm mạnh gấp bội. Đừng lấp đầy mọi giây bằng âm thanh.
4. **Layering tạo chất riêng**: whoosh trơn + 1 lớp mỏng đặc trưng bên dưới. Gợi ý chữ ký Roboworld: whoosh + beep robot rất nhẹ = "whoosh robot" nhận diện thương hiệu (chờ Sếp duyệt thử).
5. **Giọng người là VUA**: SFX không bao giờ được đè lên từ quan trọng MC đang nói — đặt SFX vào khoảng nghỉ giữa câu, hoặc hạ volume SFX khi trùng thoại (ducking áp cho cả SFX, không riêng nhạc).
6. **Sai số cho phép tính bằng chục mili-giây**: transient (đầu tiếng) phải khớp frame hành động — khớp luật đo-frame sẵn có của mình.

Nguồn: SFX Engine — Ultimate Guide to Sound Effects for Video Editing; Krotos — What is sound design; Editors Keys — Ultimate Guide to Sound Design.

## Nguồn bổ sung khi kho thiếu (xếp theo độ ưu tiên)

1. **Kho 38 file hiện tại** — nguồn chính. LƯU Ý license: phần lớn gốc YouTube Audio Library — về lý giấy phép chỉ chắc chắn cho YouTube; với FB/TikTok là vùng xám (rủi ro thấp với SFX ngắn, nhưng biết để không cãi được thì thay dần).
2. 📦 **Freesound.org API** (key miễn phí, lọc license CC0 = thương mại thoải mái) — đấu tự động được như đã làm với Pexels; chờ Sếp gật tạo key.
3. 📦 **Mixkit / Pixabay SFX** — free thương mại rõ ràng, tải tay bổ sung vào kho Drive.
4. 💰 **ElevenLabs SFX** (sinh tiếng theo mô tả, ~11-40 credits/giây, dùng key sẵn có) — cho tiếng "đo ni" kho không có (vd "tiếng bánh xe robot lăn trên sàn gỗ") — chờ Sếp gật vì credits chung.
5. ❌ Né: BBC archive (phi thương mại), trending sounds TikTok (bản quyền), kho SFX "crack".

## Trạng thái duyệt

- Cây quyết định + ma trận trên là ĐỀ XUẤT dựa trên luật gốc 03/07 của Sếp — demo A/B `DEMO SFX A-B` trên Desktop để Sếp nghe thẩm; Sếp duyệt/chỉnh dòng nào sửa dòng đó rồi mới thành luật cứng.
- Sau khi duyệt: mục 4b của ffmpeg-recipes sẽ trỏ về sổ này thay vì tự liệt kê.

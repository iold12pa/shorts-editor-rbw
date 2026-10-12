# MAU Kieu 2B "voice POV + chen full man" (ban dung that video 65 VEC, Sep duyet 13/10/2026).
# Spec: references/style-noi-chuyen-va-voice-pov.md. Chep sang Workspace, sua D/BROLL/KEYS/TOTAL/SPEED roi chay:
#   python mau_voice_pov.py <thu muc lam viec co base.mov> [assets|compose|sfx|all]
# base.mov = clip giong da cat sach (chua tang toc). Moc trong BROLL/KEYS ghi theo base.mov.
# Moc KEYS do bang scripts/do_moc_tu.py roi NGHE LAI xac nhan.
import os, random, subprocess, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W = sys.argv[1]
STEP = sys.argv[2] if len(sys.argv) > 2 else "all"
A = os.path.join(W, "assets"); os.makedirs(A, exist_ok=True)
D = r"D:\VIDEO RBW\Edit video\67.Ảnh VEC + Trung Thu\video VEC"
J = lambda n: os.path.join(D, n)
SFXD = r"D:\VIDEO RBW\Edit video\02.Tài nguyên chung\SFX\Bo 35 SFX"
PHUDU = os.path.expanduser(r"~\AppData\Local\Microsoft\Windows\Fonts\DTPhudu-Black.otf")
BOLD = r"C:\Windows\Fonts\segoeuib.ttf"
BLUE = (64, 182, 240); HL = (255, 222, 60)
SPEED = 1.15
GRADE = "eq=saturation=1.25:contrast=1.06"
TOTAL = 103.45

# (bat dau, ket thuc, file, src_tu, src_den, tam_x)  -> toc do tu khop: (src_den-src_tu)/(ket thuc-bat dau)
BROLL = [
    (0.40, 7.30, J("DJI_20260911153758_0352_D.MP4"), 0.0, 17.0, 0.5),   # "giua rat nhieu gian hang" -> LUOT doc hanh lang toi gian RBW (x2.5, Sep: "nhanh han de cam giac luot qua")
    (7.30, 11.70, J("DJI_20260910144057_0217_D.MP4"), 0.5, 5.5, 0.5),   # "vi du cuc ky de ap dung" -> gian kin ghe nguoi xem (canh tinh, do chong mat)
    (41.20, 47.10, J("DJI_20260911094923_0007_D.MP4"), 0.0, 7.5, 0.5),  # "chay ra ngoai hanh lang moi khach"
    (47.10, 52.00, J("DJI_20260909102948_0005_D.MP4"), 0.0, 6.5, 0.45), # "khach dung lai tuong tac" -> khach vay BellaBot
    (52.00, 55.90, J("IMG_6803.MOV"), 1.0, 5.5, None),                  # dong nguoi quanh robot (clip doc)
    (55.90, 61.80, J("IMG_6804.MOV"), 0.0, 6.5, None),                  # "marketing cuc tot" -> gian dong khach
    (61.80, 66.50, J("DJI_20260909103341_0008_D.MP4"), 2.0, 8.0, 0.5),  # "khach thay tu nhien"
    (66.50, 71.00, J("DJI_20260909103529_0009_D.MP4"), 0.0, 5.5, 0.5),  # "tuong tac dang yeu"
    (89.50, 92.30, J("DJI_20260910144057_0217_D.MP4"), 2.0, 5.5, 0.5),  # "noi bat nhat hoi cho" -> don canh dong nguoi
    (92.30, 95.00, J("IMG_6804.MOV"), 13.0, 16.5, None),
    (95.00, 100.00, J("DJI_20260909102917_0003_D.MP4"), 0.0, 6.0, 0.42), # "lien he em" -> Huy tu van khach
]
# TU KHOA: hien DUNG cum tu, bat len NGAY moc nguoi noi bat dau tu do (moc do bang do_moc_tu.py + nghe lai xac nhan)
KEYS = [
    (6.60, "NỔI BẬT?"), (10.06, "DỄ ÁP DỤNG"), (20.00, "SẢNH 2 · GIAN 17"),
    (25.27, "KHÔNG TO NHẤT"), (26.91, "KHÔNG Ở|CỬA VÀO"), (30.87, "LỐI ĐI CHUNG"),
    (36.36, "CHẠY LIÊN TỤC"), (45.50, "MỜI KẸO"), (46.53, "PHÁT TỜ RƠI"),
    (50.98, "TỰ DỪNG LẠI"), (56.50, "MARKETING|CỰC TỐT"), (59.60, "KHÔNG CẦN|CON NGƯỜI"),
    (65.45, "TỰ NHIÊN"), (69.45, "ĐÁNG YÊU"), (77.04, "ROBOT CƯỜI"), (78.36, "TỰ NÉ NGƯỜI"),
    (85.60, "DANH THIẾP"), (94.20, "NỔI BẬT NHẤT"), (102.60, "LIÊN HỆ|QUANG HUY ROBOT"),
]
HOLD = 1.6        # giu khung cuoi them (giay, theo base) cho CTA kip doc
KEY_MAX = 1.7     # moi tu khoa hien toi da (giay base), hoac toi tu ke tiep
SFX = {"whoosh": ("19 - Whoosh 2.mp3", 0.30), "pop": ("04 - Pop.mp3", 0.45), "ding": ("34 - Ding.mp3", 0.35)}


def brush(d, x0, y0, x1, y1, rnd):
    pts = []; x = x0
    while x <= x1: pts.append((x, y0 + rnd.randint(-6, 6))); x += 18
    pts.append((x1 + rnd.randint(4, 14), (y0 + y1) // 2)); x = x1
    while x >= x0: pts.append((x, y1 + rnd.randint(-6, 6))); x -= 18
    pts.append((x0 - rnd.randint(4, 14), (y0 + y1) // 2))
    d.polygon(pts, fill=BLUE)


def pill(name, lines, size=56, cy=1500):
    f = ImageFont.truetype(BOLD, size)
    c = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0)); d = ImageDraw.Draw(c)
    lh = int(size * 1.5)
    rows = []
    for ln in lines:
        segs = [(p, i % 2 == 1) for i, p in enumerate(ln.split("*")) if p]
        rows.append((segs, sum(d.textlength(p, font=f) for p, _ in segs)))
    top = cy - lh * len(lines) // 2
    for i, (segs, w) in enumerate(rows):
        x = (1080 - w) / 2; y = top + i * lh
        d.rounded_rectangle((x - 24, y - 4, x + w + 24, y + lh - 8), 18, fill="white")
        for p, hl in segs:
            tw = d.textlength(p, font=f)
            if hl: d.rounded_rectangle((x - 6, y + 4, x + tw + 6, y + lh - 16), 10, fill=HL)
            d.text((x, y + 2), p, font=f, fill=(12, 12, 12)); x += tw
    c.save(os.path.join(A, name + ".png"))


def grab(src, t, out, vf="null"):
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(t), "-i", src, "-map", "0:v:0", "-frames:v", "1",
                    "-vf", vf, out], check=True)
    return Image.open(out).convert("RGB")


def fit(im, w, h, fx=0.5, fy=0.5):
    s = max(w / im.width, h / im.height)
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    x = int((im.width - w) * fx); y = int((im.height - h) * fy)
    return im.crop((x, y, x + w, y + h))


def key_png(name, text, scale):
    lines = text.split("|"); size = int((156 if len(lines) == 1 else 128) * scale)
    f = ImageFont.truetype(PHUDU, size)
    c = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0)); d = ImageDraw.Draw(c)
    lh = int(size * 1.1); top = 1400 - lh * len(lines) // 2
    while max(d.textlength(l, font=f) for l in lines) > 1050:   # qua dai thi thu nho
        size -= 4; f = ImageFont.truetype(PHUDU, size); lh = int(size * 1.1)
    sh = Image.new("RGBA", c.size, (0, 0, 0, 0)); sd = ImageDraw.Draw(sh)
    for i, l in enumerate(lines):
        x = (1080 - d.textlength(l, font=f)) / 2; y = top + i * lh
        sd.text((x + 6, y + 9), l, font=f, fill=(0, 0, 0, 190))
    c.alpha_composite(sh.filter(ImageFilter.GaussianBlur(5)))
    for i, l in enumerate(lines):
        x = (1080 - d.textlength(l, font=f)) / 2; y = top + i * lh
        col = (255, 255, 255) if (text.startswith("LIÊN HỆ") and i == 1) else HL
        d.text((x, y), l, font=f, fill=col, stroke_width=max(6, size // 14), stroke_fill=(10, 10, 10))
    c.save(os.path.join(A, name + ".png"))


def assets():
    for k, (_, t) in enumerate(KEYS):
        for tag, sc in (("a", 1.18), ("b", 1.07), ("c", 1.0)):   # 3 co -> hieu ung nay 0.1s
            key_png(f"k{k}{tag}", t, sc)
    # ANH BIA: tren = gian RBW kin nguoi, duoi = can mat meo BellaBot
    top = grab(J("DJI_20260910144057_0217_D.MP4"), 3.0, os.path.join(A, "_t.png"), GRADE)
    bot = grab(J("IMG_6857.MOV"), 79.0, os.path.join(A, "_b.png"), GRADE)
    cv = Image.new("RGBA", (1080, 1920), "black")
    cv.paste(fit(top, 1080, 1150, 0.5, 0.5), (0, 0)); cv.paste(fit(bot, 1080, 770, 0.5, 0.40), (0, 1150))
    rnd = random.Random(7); f = ImageFont.truetype(PHUDU, 112); d = ImageDraw.Draw(cv)
    lines = ["LÀM SAO ĐỂ", "GIAN HÀNG NỔI BẬT", "GIỮA HỘI CHỢ?"]
    lh = int(112 * 1.08); top_y = 960 - lh * 3 // 2; boxes = []
    for i, ln in enumerate(lines):
        l, t, r, b = d.textbbox((0, 0), ln, font=f); x = (1080 - (r - l)) // 2; y = top_y + i * lh
        boxes.append((ln, x - l, y - t + 7)); brush(d, x - 22, y + 2, x + (r - l) + 22, y + lh + 2, rnd)
    sh = Image.new("RGBA", cv.size, (0, 0, 0, 0)); sd = ImageDraw.Draw(sh)
    for ln, x, y in boxes: sd.text((x + 5, y + 7), ln, font=f, fill=(0, 0, 0, 170))
    cv.alpha_composite(sh.filter(ImageFilter.GaussianBlur(3)))
    d = ImageDraw.Draw(cv)
    for ln, x, y in boxes: d.text((x, y), ln, font=f, fill="white", stroke_width=3, stroke_fill=(20, 20, 20))
    cv.convert("RGB").save(os.path.join(A, "cover.jpg"), quality=95); cv.save(os.path.join(A, "cover.png"))


def compose():
    args = ["ffmpeg", "-v", "error", "-y", "-i", os.path.join(W, "base.mov")]
    fc = [f"[0:v]{GRADE}[b0]"]; last = "[b0]"; idx = 1
    for k, (a, b, f, s0, s1, cx) in enumerate(BROLL):
        args += ["-ss", str(s0), "-t", f"{s1 - s0 + 0.3:.2f}", "-i", f]
        k_fit = (b - a) / (s1 - s0)          # he so keo/nen thoi gian de khop cau noi
        if cx is None:   # clip doc san
            geo = "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920"
        else:            # 4K ngang -> cat doc 9:16 quanh tam_x
            geo = f"crop=ih*9/16:ih:(iw-ih*9/16)*{cx}:0,scale=1080:1920"
        fc.append(f"[{idx}:v:0]{geo},{GRADE},fps=30,setsar=1,setpts=(PTS-STARTPTS)*{k_fit:.4f}+{a}/TB,format=yuv420p[c{k}]")
        fc.append(f"{last}[c{k}]overlay=0:0:eof_action=pass:enable='between(t,{a},{b})'[o{k}]"); last = f"[o{k}]"; idx += 1
    ov = []
    for k, (t, _) in enumerate(KEYS):
        end = min(t + KEY_MAX, KEYS[k + 1][0] - 0.05) if k + 1 < len(KEYS) else TOTAL + HOLD
        ov += [(t, t + 0.05, f"k{k}a"), (t + 0.05, t + 0.10, f"k{k}b"), (t + 0.10, end, f"k{k}c")]
    ov.append((0.0, 0.4, "cover"))
    for k, (a, b, n) in enumerate(ov):
        args += ["-loop", "1", "-t", "120", "-i", os.path.join(A, n + ".png")]
        fc.append(f"[{idx}:v]format=rgba[p{k}]")
        fc.append(f"{last}[p{k}]overlay=0:0:enable='between(t,{a:.3f},{b:.3f})'[q{k}]"); last = f"[q{k}]"; idx += 1
    # giu khung cuoi HOLD giay de CTA kip doc
    fc.insert(0, f"[0:v]tpad=stop_mode=clone:stop_duration={HOLD}[bg0]")
    fc[1] = fc[1].replace("[0:v]", "[bg0]", 1)
    fc.append(f"{last}trim=0:{TOTAL + HOLD},setpts=(PTS-STARTPTS)/{SPEED},format=yuv420p[vout]")
    fc.append(f"[0:a]atrim=0:{TOTAL},asetpts=PTS-STARTPTS,apad=pad_dur={HOLD},atempo={SPEED}[aout]")
    args += ["-filter_complex", ";".join(fc), "-map", "[vout]", "-map", "[aout]", "-r", "30",
             "-c:v", "libx264", "-preset", "medium", "-crf", "17", "-c:a", "pcm_s16le", os.path.join(W, "comp.mov")]
    subprocess.run(args, check=True)


def sfx():
    ev = [("whoosh", a - 0.05) for a, *_ in BROLL] + [("pop", t) for t, _ in KEYS[:-1]]
    ev += [("ding", KEYS[-1][0])]
    args = ["ffmpeg", "-v", "error", "-y", "-i", os.path.join(W, "comp.mov")]; fc = []
    for k, (n, t) in enumerate(ev):
        f, vol = SFX[n]; args += ["-i", os.path.join(SFXD, f)]; ms = max(0, int(t / SPEED * 1000))
        fc.append(f"[{k + 1}:a]aformat=sample_rates=48000:channel_layouts=stereo,volume={vol},adelay={ms}|{ms}[s{k}]")
    # hoi truong on: highpass + giam on nhe o buoc MIX CUOI (luat skill: khong loc truoc khi do thoai)
    fc.append("[0:a]aformat=sample_rates=48000:channel_layouts=stereo,highpass=f=90,afftdn=nf=-30[v]")
    fc.append("[v]" + "".join(f"[s{k}]" for k in range(len(ev))) + f"amix=inputs={len(ev) + 1}:duration=first:normalize=0[a]")
    args += ["-filter_complex", ";".join(fc), "-map", "[a]", "-c:a", "pcm_s16le", os.path.join(W, "mix.wav")]
    subprocess.run(args, check=True)


if STEP in ("all", "assets"): assets(); print("assets ok")
if STEP in ("all", "compose"): compose(); print("compose ok")
if STEP in ("all", "sfx"): sfx(); print("sfx ok")

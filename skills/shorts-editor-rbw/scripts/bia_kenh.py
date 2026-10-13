# Anh bia kieu kenh Quang Huy Robot (rut tu ~50 bia that trong HUY MKT\03, 13/10/2026):
# chu dat THANG len anh (khong hop nen), moi dong mot mau, vien DOI (trang manh trong + toi day ngoai) + bong.
import os, sys
# Dung:
#   from bia_kenh import ve_tieu_de, nen
#   cv = nen("anh.png")  (hoac tu ghep 2 nua anh 1080x1150 + 1080x770)
#   cv = ve_tieu_de(cv, [[("LAM SAO DE","trang")],[("GIAN HANG","hong")],[('"NOI BAT"',"vang")],[("GIUA HOI CHO ???","trang")]], cy=960, size=170)
#   Tu trong o vang: ("NOI BAT","hong","hop"). Mau: trang vang hong xanhla ngoc cam.
#   Nen dong nguoi -> them dai toi mo sau chu (xem references/style-noi-chuyen-va-voice-pov.md muc 1.8).
from PIL import Image, ImageDraw, ImageFont, ImageFilter

PHUDU = os.path.expanduser(r"~\AppData\Local\Microsoft\Windows\Fonts\DTPhudu-Black.otf")
MAU = {"trang": (255, 255, 255), "vang": (255, 222, 40), "hong": (255, 64, 160), "xanhla": (110, 255, 80),
       "ngoc": (60, 225, 255), "cam": (255, 150, 30)}
TOI = (18, 24, 60)   # vien ngoai xanh than nhu bia that


def ve_tieu_de(cv, dong, cy=960, size=128, kieu="vien_doi"):
    """dong: list cac dong; moi dong = list (chu, mau) hoac (chu, mau, 'hop') de dat trong hop vang."""
    d = ImageDraw.Draw(cv)
    f = ImageFont.truetype(PHUDU, size)
    lh = int(size * 1.12)
    rows = []
    for ln in dong:
        w = sum(d.textlength(t[0], font=f) for t in ln)
        rows.append((ln, w))
    scale = min(1.0, 1020 / max(w for _, w in rows))
    if scale < 1:
        size = int(size * scale); f = ImageFont.truetype(PHUDU, size); lh = int(size * 1.12)
        rows = [(ln, sum(d.textlength(t[0], font=f) for t in ln)) for ln, _ in rows]
    top = cy - lh * len(rows) // 2
    so = max(10, size // 9); si = max(4, size // 28)
    # bong mo
    sh = Image.new("RGBA", cv.size, (0, 0, 0, 0)); sd = ImageDraw.Draw(sh)
    for i, (ln, w) in enumerate(rows):
        x = (1080 - w) / 2; y = top + i * lh
        for t in ln:
            sd.text((x + 8, y + 12), t[0], font=f, fill=(0, 0, 0, 200), stroke_width=so, stroke_fill=(0, 0, 0, 200))
            x += d.textlength(t[0], font=f)
    cv.alpha_composite(sh.filter(ImageFilter.GaussianBlur(10)))
    d = ImageDraw.Draw(cv)
    for i, (ln, w) in enumerate(rows):
        x = (1080 - w) / 2; y = top + i * lh
        for t in ln:
            txt, mau = t[0], MAU[t[1]]
            tw = d.textlength(txt, font=f)
            if len(t) > 2 and t[2] == "hop":       # tu khoa trong hop vang chu den
                d.rounded_rectangle((x - 14, y + size * 0.08, x + tw + 14, y + lh - size * 0.02), 16, fill=MAU["vang"],
                                    outline=TOI, width=6)
                d.text((x, y), txt, font=f, fill=(15, 15, 15))
            else:
                d.text((x, y), txt, font=f, fill=TOI, stroke_width=so, stroke_fill=TOI)        # vien ngoai toi
                d.text((x, y), txt, font=f, fill=mau, stroke_width=si, stroke_fill=(255, 255, 255) if mau != MAU["trang"] else TOI)
            x += tw
    return cv


def nen(path, fx=0.5, fy=0.5):
    im = Image.open(path).convert("RGB")
    s = max(1080 / im.width, 1920 / im.height)
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    x = int((im.width - 1080) * fx); y = int((im.height - 1920) * fy)
    return im.crop((x, y, x + 1080, y + 1920)).convert("RGBA")

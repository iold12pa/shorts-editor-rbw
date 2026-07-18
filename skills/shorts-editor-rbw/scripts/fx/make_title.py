# -*- coding: utf-8 -*-
# Ve tieu de gradient (vang -> trang) + bong do dai kieu poster -> title.png (RGBA)
from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 520
TEXT = "ROBOWORLD"
font = ImageFont.truetype("fonts/Anton-Regular.ttf", 150)

img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
d = ImageDraw.Draw(img)
bbox = d.textbbox((0, 0), TEXT, font=font)
tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
x, y = (W - tw) // 2 - bbox[0], (H - th) // 2 - bbox[1] - 20

# Bong do dai cheo 45 do
for i in range(1, 34):
    a = max(0, 120 - i * 3)
    d.text((x + i, y + i), TEXT, font=font, fill=(8, 8, 18, a))

# Chu gradient: render mask roi to mau theo hang
mask = Image.new("L", (W, H), 0)
ImageDraw.Draw(mask).text((x, y), TEXT, font=font, fill=255)
grad = Image.new("RGBA", (W, H))
top = (255, 210, 0)      # vang FFD200
bot = (255, 255, 240)    # trang am
y0, y1 = y, y + th
for row in range(H):
    t = 0 if row <= y0 else (1 if row >= y1 else (row - y0) / max(1, y1 - y0))
    grad.paste((int(top[0]+(bot[0]-top[0])*t), int(top[1]+(bot[1]-top[1])*t),
                int(top[2]+(bot[2]-top[2])*t), 255), (0, row, W, row + 1))
img.paste(grad, (0, 0), mask)
img.save("temp/title.png")
print("OK title.png")

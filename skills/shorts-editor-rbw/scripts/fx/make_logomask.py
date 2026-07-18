# -*- coding: utf-8 -*-
# Tao 18 khung mask: logo Roboworld trang phong to dan tren nen den (cho chuyen canh theo logo)
from PIL import Image

logo = Image.open("logo.png").convert("RGBA")
alpha = logo.split()[3]
W, H = 1080, 1920
N = 18
for i in range(1, N + 1):
    t = i / N
    scale = 0.18 + t * t * 6.0  # phong to tang toc dan, cuoi cung phu kin man
    w = max(2, int(logo.width * scale))
    h = max(2, int(logo.height * scale))
    a = alpha.resize((w, h), Image.LANCZOS)
    frame = Image.new("L", (W, H), 0)
    frame.paste(a, ((W - w) // 2, (H - h) // 2), a)
    frame.save("temp/lm_%02d.png" % i)
print("OK 18 mask frames")

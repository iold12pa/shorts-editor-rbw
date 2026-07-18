# -*- coding: utf-8 -*-
# Ghep anh san pham (khong nen) + bong do mem -> product.png
import os
from PIL import Image, ImageDraw, ImageFilter

SRC = os.path.expanduser("~/.claude/roboworld-assets/tai-nguyen-chung")
# tim anh SH1 chinh dien
path = None
for root, _d, files in os.walk(SRC):
    for f in files:
        if f == "正.png" and "SH1" in root:
            path = os.path.join(root, f)
            break
    if path:
        break
if not path:
    raise SystemExit("Khong tim thay anh SH1")

p = Image.open(path).convert("RGBA")
p.thumbnail((760, 1150))
W, H = 1080, 1500
img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
# bong elip mem duoi chan
sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
d = ImageDraw.Draw(sh)
cx, base = W // 2, 120 + p.height
d.ellipse((cx - p.width // 2 - 30, base - 34, cx + p.width // 2 + 30, base + 46), fill=(0, 0, 0, 150))
sh = sh.filter(ImageFilter.GaussianBlur(22))
img.alpha_composite(sh)
img.alpha_composite(p, ((W - p.width) // 2, 120))
img.save("temp/product.png")
print("OK product.png", p.size)

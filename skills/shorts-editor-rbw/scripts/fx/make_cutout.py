# -*- coding: utf-8 -*-
# Tach nen 75 khung hinh (robot) bang rembg -> cut9/c_XXX.png (RGBA, chi con robot)
import glob
import os

from rembg import remove, new_session

session = new_session("u2net")
files = sorted(glob.glob("temp/fg9/f_*.png"))
for i, f in enumerate(files, 1):
    out = "temp/cut9/c_%03d.png" % i
    if os.path.exists(out):
        continue
    with open(f, "rb") as fi:
        data = fi.read()
    with open(out, "wb") as fo:
        fo.write(remove(data, session=session))
    if i % 15 == 0:
        print("cutout %d/%d" % (i, len(files)), flush=True)
print("XONG cutout", len(files))

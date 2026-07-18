# -*- coding: utf-8 -*-
# Sinh 5 bo mask chuyen canh kieu LUMA WIPE (18 khung/bo) — nhu kho transition dung san
import math
import os

import numpy as np
from PIL import Image

W, H = 1080, 1920
N = 18
S = 0.16  # do mem cua mep quet
os.makedirs("temp/luma", exist_ok=True)

yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)

def save(name, L):
    L = (L - L.min()) / max(1e-6, (L.max() - L.min()))
    for i in range(1, N + 1):
        p = i / N
        m = np.clip((p * (1 + S) - L) / S, 0, 1) * 255
        Image.fromarray(m.astype(np.uint8), "L").save("temp/luma/%s_%02d.png" % (name, i))

# 1. Muc loang huu co (to hop song sin nhieu huong)
L = (np.sin(xx / 97) * np.sin(yy / 71) + np.sin((xx + yy) / 133) +
     np.sin(np.hypot(xx - 540, yy - 960) / 87))
save("inkblob", L)
# 2. Quet cheo mem
save("diagsoft", (xx + yy) / (W + H))
# 3. Iris tron mem tu tam
save("iris", np.hypot(xx - 540, yy - 960))
# 4. Rem ngang mem (blinds)
save("blinds", (yy % 240) / 240.0)
# 5. Song luon cheo
save("wave", (xx + 90 * np.sin(yy / 110)) / W)
print("OK 5 bo luma x", N, "khung")

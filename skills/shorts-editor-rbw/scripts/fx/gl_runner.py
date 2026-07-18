# -*- coding: utf-8 -*-
"""Chay shader GL-Transitions giua 2 clip -> chuoi khung PNG phan giao thoa.
Usage: python gl_runner.py <shader.glsl> <dirA_frames> <dirB_frames> <out_dir>
Cac khung A/B: f_01.png..f_18.png (cung kich thuoc). Output: o_01..o_18.png
"""
import glob
import os
import re
import struct
import sys

import moderngl
from PIL import Image

shader_path, dir_a, dir_b, out_dir = sys.argv[1:5]
os.makedirs(out_dir, exist_ok=True)
src = open(shader_path, encoding="utf-8", errors="replace").read()

W, H = 1080, 1920
ctx = moderngl.create_standalone_context()

VERT = """
#version 330
in vec2 in_pos;
out vec2 uv;
void main() { uv = in_pos * 0.5 + 0.5; gl_Position = vec4(in_pos, 0.0, 1.0); }
"""

# Doc uniform co gia tri mac dinh trong shader (chuan gl-transitions: `uniform float x; // = 0.5`)
defaults = []
for m in re.finditer(r"uniform\s+(float|int|bool|vec2|vec3|vec4)\s+(\w+)\s*;\s*//\s*=\s*([^\n]+)", src):
    typ, name, val = m.group(1), m.group(2), m.group(3).strip()
    defaults.append((typ, name, val))

FRAG = """
#version 330
uniform sampler2D u_from;
uniform sampler2D u_to;
uniform float progress;
uniform float ratio;
in vec2 uv;
out vec4 fragColor;
vec4 getFromColor(vec2 p) { return texture(u_from, p); }
vec4 getToColor(vec2 p) { return texture(u_to, p); }
%s
void main() { fragColor = transition(uv); }
""" % src

prog = ctx.program(vertex_shader=VERT, fragment_shader=FRAG)
prog["u_from"].value = 0
prog["u_to"].value = 1
if "ratio" in prog:
    prog["ratio"].value = W / H
for typ, name, val in defaults:
    if name not in prog:
        continue
    try:
        nums = [float(x) for x in re.findall(r"-?\d+\.?\d*", val)]
        if typ == "float":
            prog[name].value = nums[0]
        elif typ == "int":
            prog[name].value = int(nums[0])
        elif typ == "bool":
            prog[name].value = ("true" in val)
        else:
            prog[name].value = tuple(nums)
    except Exception as e:
        print("bo qua uniform", name, e)

vbo = ctx.buffer(struct.pack("8f", -1, -1, 1, -1, -1, 1, 1, 1))
vao = ctx.vertex_array(prog, [(vbo, "2f", "in_pos")])
fbo = ctx.simple_framebuffer((W, H), components=4)
fbo.use()

fa = sorted(glob.glob(os.path.join(dir_a, "f_*.png")))
fb = sorted(glob.glob(os.path.join(dir_b, "f_*.png")))
n = min(len(fa), len(fb))
for i in range(n):
    # PIL luu top-down; GL texture coi hang dau la v=0 (bottom) -> lat khi nap va lat lai khi doc
    ia = Image.open(fa[i]).convert("RGBA").transpose(Image.FLIP_TOP_BOTTOM)
    ib = Image.open(fb[i]).convert("RGBA").transpose(Image.FLIP_TOP_BOTTOM)
    ta = ctx.texture((W, H), 4, ia.tobytes())
    tb = ctx.texture((W, H), 4, ib.tobytes())
    ta.use(0)
    tb.use(1)
    prog["progress"].value = (i + 1) / (n + 1)
    ctx.clear(0, 0, 0, 1)
    vao.render(moderngl.TRIANGLE_STRIP)
    out = Image.frombytes("RGBA", (W, H), fbo.read(components=4)).transpose(Image.FLIP_TOP_BOTTOM)
    out.convert("RGB").save(os.path.join(out_dir, "o_%02d.png" % (i + 1)))
    ta.release()
    tb.release()
print("OK", os.path.basename(shader_path), n, "khung")

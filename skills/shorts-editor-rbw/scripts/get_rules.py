# -*- coding: utf-8 -*-
"""Trich DUNG PHAN can doc trong 1 file luat (references/*.md), theo KIEU DUNG —
them 23/07/2026 (Sep Huy yeu cau giai quyet goc van de "tot token/het session
limit", da tham khao ChatGPT + Gemini truoc khi chot huong lam — xem
PROMPT-HOI-Y-TO-CHUC-LUAT-2026-07-23.md).

Y TUONG (ca 2 AI + Claude dong thuan): gan THE (tag) cho TUNG MUC (heading)
trong file luat, thay vi doc nguyen ca file. File luat KHONG bi to chuc lai —
chi them 1 dong comment ngay duoi moi heading:

    ## Ten muc
    <!-- tags: kieu-1, kieu-3 -->
    noi dung muc nay...

Cach doc: 1 "khoi" = 1 heading (bat ky cap # nao) + toan bo noi dung TOI heading
tiep theo (bat ky cap nao). Khoi duoc IN RA neu:
    - KHONG co dong tag (MAC DINH AN TOAN — coi nhu "chung", luon lay) — quyet
      dinh nay co y: quen gan tag se KHONG lam mat noi dung (chi la khong duoc
      loc bot), khac han voi loc sai lam BO SOT luat can dung.
    - CO tag "chung" -> luon lay
    - CO tag "kieu-N" trung voi --kieu dang hoi -> lay
Khoi CO tag nhung KHONG trung (vd chi "kieu-1" ma dang hoi --kieu 2), hoac tag
dac biet "lich-su" (noi dung cu, khong con dung, chi tra cuu thu cong) -> BO.

Usage:
    python get_rules.py --file chon-kieu-dung.md --kieu 2
    python get_rules.py --file ffmpeg-recipes.md --kieu 3
    python get_rules.py --file chon-kieu-dung.md --kieu 1 --thong-ke   # chi in so dong/token tiet kiem, khong in noi dung
    python get_rules.py --file chon-kieu-dung.md --validate            # liet ke heading CHUA gan tag (khong chan, chi de biet)

--file nhan ten file trong references/ (vd "ffmpeg-recipes.md") hoac duong dan
day du. Co the lap lai --file nhieu lan de gop nhieu file 1 luot.
"""
import argparse
import os
import re
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

REF_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "references")

HEADING_RE = re.compile(r"^(#{1,6})\s+.*$")
TAG_RE = re.compile(r"^<!--\s*tags:\s*(.*?)\s*-->\s*$")
FENCE_RE = re.compile(r"^\s*```")


def _dong_la_heading(lines, i, trong_fence):
    """True neu dong i la heading Markdown THAT (khong phai comment '# ...' trong
    khoi code ```...```). BUG DA VA (23/07/2026, phat hien qua chay THAT tren
    ffmpeg-recipes.md): dong PowerShell comment nhu '# T_END = 6.2 ...' bat dau
    bang 1 dau '#' -> bi nham la heading H1, vo ranh gioi khoi, lam lot noi dung
    sai kieu ra ngoai (khoi bi tach doi thua ke tag None = "chung" = luon hien,
    du noi dung that thuoc phan chi danh cho kieu-2/kieu-3)."""
    return HEADING_RE.match(lines[i]) is not None and not trong_fence


def resolve_path(name):
    if os.path.exists(name):
        return name
    p = os.path.join(REF_DIR, name)
    if os.path.exists(p):
        return p
    sys.exit("Khong thay file: %s (da thu ca duong dan tuyet doi va trong %s)" % (name, REF_DIR))


def parse_blocks(path):
    """Tra ve list {heading, tags(list|None), body(list dong), line_no}.

    Bo qua heading GIA nam trong khoi code ```...``` (xem _dong_la_heading)."""
    lines = open(path, encoding="utf-8").read().splitlines()
    blocks = []
    i = 0
    trong_fence = False

    def buoc(idx):
        # cap nhat trang thai fence khi di qua dong idx
        nonlocal trong_fence
        if FENCE_RE.match(lines[idx]):
            trong_fence = not trong_fence

    # phan truoc heading dau tien (thuong la # Tieu de + mo ta) luon coi la "chung"
    while i < len(lines) and not _dong_la_heading(lines, i, trong_fence):
        buoc(i)
        i += 1
    if i > 0:
        blocks.append({"heading": None, "tags": ["chung"], "body": lines[:i], "line_no": 1})
    while i < len(lines):
        heading = lines[i]
        start = i
        buoc(i)
        i += 1
        tags = None
        if i < len(lines):
            m = TAG_RE.match(lines[i].strip())
            if m:
                tags = [t.strip() for t in m.group(1).split(",") if t.strip()]
                i += 1
        body_start = i
        while i < len(lines) and not _dong_la_heading(lines, i, trong_fence):
            buoc(i)
            i += 1
        blocks.append({"heading": heading, "tags": tags, "body": lines[body_start:i], "line_no": start + 1})
    return blocks


def khop(tags, kieu):
    if not tags:
        return True  # mac dinh an toan: khong gan tag = luon lay
    if "chung" in tags:
        return True
    if kieu and ("kieu-%s" % kieu) in tags:
        return True
    return False


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--file", action="append", required=True, help="ten file trong references/ hoac duong dan day du (lap lai de gop nhieu file)")
    ap.add_argument("--kieu", choices=["1", "2", "3"], help="chi lay muc gan tag 'kieu-N' nay hoac 'chung' (bo qua = chi lay 'chung')")
    ap.add_argument("--thong-ke", action="store_true", help="chi in so dong/uoc luong token tiet kiem duoc, khong in noi dung")
    ap.add_argument("--validate", action="store_true", help="liet ke heading CHUA gan tag trong file (khong chan gi, chi de ra soat dan)")
    a = ap.parse_args()

    if a.validate:
        for f in a.file:
            path = resolve_path(f)
            blocks = parse_blocks(path)
            chua_gan = [b for b in blocks if b["heading"] and b["tags"] is None]
            print("=== %s: %d/%d heading CHUA gan tag (mac dinh coi la 'chung', khong bi loc) ===" % (
                os.path.basename(path), len(chua_gan), sum(1 for b in blocks if b["heading"])))
            for b in chua_gan:
                print("  dong %4d: %s" % (b["line_no"], b["heading"]))
        return

    tong_dong_goc, tong_dong_lay = 0, 0
    ra = []
    for f in a.file:
        path = resolve_path(f)
        blocks = parse_blocks(path)
        for b in blocks:
            n = len(b["body"]) + (1 if b["heading"] else 0)
            tong_dong_goc += n
            if khop(b["tags"], a.kieu):
                tong_dong_lay += n
                if b["heading"]:
                    ra.append(b["heading"])
                ra.extend(b["body"])

    if a.thong_ke:
        giam = tong_dong_goc - tong_dong_lay
        pct = (giam / tong_dong_goc * 100) if tong_dong_goc else 0
        print("File: %s | kieu=%s" % (", ".join(a.file), a.kieu or "(khong loc, chi lay 'chung')"))
        print("Dong goc: %d -> dong lay: %d (giam %d dong, %.0f%%)" % (tong_dong_goc, tong_dong_lay, giam, pct))
        return

    print("\n".join(ra))


if __name__ == "__main__":
    main()

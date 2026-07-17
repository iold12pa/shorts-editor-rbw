# -*- coding: utf-8 -*-
"""Tai kho tai nguyen dung chung (logo/outro/nhac/SFX/anh SP) tu Google Drive cua Sep
ve cho luu ben tren may + TU KIEM DEM du/thieu tung file.

Usage:
    python tai_kho_tai_nguyen.py            # tai/tai tiep + kiem dem + don ve cho ben
    python tai_kho_tai_nguyen.py --check    # chi kiem dem cho ben so voi manifest, khong tai

Co che:
    1. gdown tai ca folder Drive vao thu muc TAM NGAN (%TEMP%/rbwkho — tranh loi duong dan
       Windows >260 ky tu khi de truc tiep vao duong dan sau). Co --continue: chay lai
       chi tai phan thieu, khong tai lai tu dau.
    2. Doc log gdown: moi dong "Processing file <id> <ten>" la 1 file Drive KHAI BAO co.
       So voi file THAT tren dia -> thieu file nao bao DICH DANH file do (loi hay gap:
       Google chan tam "many accesses" lam rot file giua chung).
    3. Du roi don ve cho ben ~/.claude/roboworld-assets/tai-nguyen-chung/ + ghi manifest.json
       (ten + size tung file) de lan sau doi chieu nhanh.

Exit code: 0 = kho day du; 2 = con thieu file (da in danh sach, doi 15-30 phut chay lai);
           1 = loi khac (gdown chua cai, mat mang...).
"""
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

DRIVE_URL = "https://drive.google.com/drive/folders/1eofLwPIE6XtoMPI6Wo19gf48KwM1OYIr"
DEST = os.path.expanduser("~/.claude/roboworld-assets/tai-nguyen-chung")
TMP = os.path.join(tempfile.gettempdir(), "rbwkho")  # ngan + co dinh de --continue dung duoc
MANIFEST = os.path.join(DEST, "manifest.json")


def list_files(root):
    out = {}
    for r, _d, files in os.walk(root):
        for f in files:
            p = os.path.join(r, f)
            out[os.path.relpath(p, root).replace("\\", "/")] = os.path.getsize(p)
    return out


def write_manifest(files):
    os.makedirs(DEST, exist_ok=True)
    data = {"nguon": DRIVE_URL, "so_file": len(files),
            "tong_mb": round(sum(files.values()) / 1048576, 1),
            "files": [{"path": k, "size": files[k]} for k in sorted(files)]}
    json.dump(data, open(MANIFEST, "w", encoding="utf-8"), ensure_ascii=False, indent=1)


def check_only():
    if not os.path.isdir(DEST):
        print("CHUA CO kho tai cho ben %s — chay script nay KHONG co --check de tai." % DEST)
        return 1
    files = {k: v for k, v in list_files(DEST).items() if k != "manifest.json"}
    if not os.path.exists(MANIFEST):
        print("Kho co %d file (%.1f MB) nhung chua co manifest — chay ban tai day du de sinh."
              % (len(files), sum(files.values()) / 1048576))
        return 0
    mf = json.load(open(MANIFEST, encoding="utf-8"))
    expect = {f["path"]: f["size"] for f in mf["files"]}
    missing = sorted(set(expect) - set(files))
    if missing:
        print("THIEU %d file so voi manifest:" % len(missing))
        for m in missing:
            print("  - %s" % m)
        return 2
    print("Kho DAY DU so voi manifest: %d file / %.1f MB." % (len(files), sum(files.values()) / 1048576))
    return 0


def main():
    if "--check" in sys.argv:
        sys.exit(check_only())

    os.makedirs(TMP, exist_ok=True)
    env = dict(os.environ, PYTHONUTF8="1")
    print("Tai kho tu Drive ve thu muc tam %s (chay lai chi tai phan thieu)..." % TMP)
    r = subprocess.run([sys.executable, "-m", "gdown", "--folder", "--continue", DRIVE_URL, "-O", TMP],
                       capture_output=True, text=True, encoding="utf-8", errors="replace",
                       env=env, timeout=3600)
    log = (r.stdout or "") + (r.stderr or "")

    # Danh sach file Drive KHAI BAO (moi file 1 dong "Processing file <id> <ten>")
    declared = re.findall(r"Processing file \S+ (.+)", log)
    if not declared:
        print("KHONG doc duoc danh sach file tu Drive. Loi gdown:\n%s" % log[-1500:])
        print("-> Kiem tra: gdown da cai chua (pip install -U gdown)? Link Drive con share"
              " 'Anyone with the link'? Mang co chan Google khong?")
        sys.exit(1)

    got = list_files(TMP)
    got_names = {}
    for k in got:
        base = os.path.basename(k)
        got_names[base] = got_names.get(base, 0) + 1
    missing = []
    declared_count = {}
    for name in declared:
        name = name.strip()
        declared_count[name] = declared_count.get(name, 0) + 1
    for name, cnt in sorted(declared_count.items()):
        have = got_names.get(name, 0)
        if have < cnt:
            missing.append("%s (Drive khai bao %d, tai duoc %d)" % (name, cnt, have))

    total_mb = sum(got.values()) / 1048576
    print("Drive khai bao %d file — tai duoc %d file / %.1f MB." % (len(declared), len(got), total_mb))

    # Don phan DA TAI DUOC ve cho ben ngay (ke ca khi con thieu — logo/nhac co san van dung duoc);
    # copy de merge, khong xoa thu gi co san o dich
    os.makedirs(DEST, exist_ok=True)
    moved = 0
    for rel, size in got.items():
        srcp = os.path.join(TMP, rel)
        dstp = os.path.join(DEST, rel)
        if os.path.exists(dstp) and os.path.getsize(dstp) == size:
            continue
        os.makedirs(os.path.dirname(dstp), exist_ok=True)
        shutil.copy2(srcp, dstp)
        moved += 1

    if missing:
        print("Da don %d file tai duoc ve %s (dung tam duoc)." % (len(got), DEST))
        print("\nTHIEU %d FILE (bao dich danh):" % len(missing))
        for m in missing:
            print("  - %s" % m)
        if re.search(r"many accesses|Cannot retrieve", log):
            print("\n-> Nguyen nhan: Google chan tam vi tai don dap. DOI 15-30 PHUT roi chay lai"
                  " script nay (co --continue, chi tai not phan thieu). Manifest CHUA ghi"
                  " (chi ghi khi kho day du).")
        sys.exit(2)

    write_manifest(got)
    print("XONG: kho day du %d file / %.1f MB tai %s (%d file moi/cap nhat)."
          % (len(got), total_mb, DEST, moved))
    print("Manifest da ghi: %s" % MANIFEST)
    sys.exit(0)


if __name__ == "__main__":
    main()

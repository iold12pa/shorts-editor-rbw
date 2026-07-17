# -*- coding: utf-8 -*-
"""Do va nang driver NVIDIA de render GPU (NVENC) — cho nguoi KHONG ranh ky thuat.

Usage:
    python cai_driver_nvidia.py --check   # CHI DO, khong tai/cai gi — de skill biet co can hoi nguoi dung khong
    python cai_driver_nvidia.py           # tai + cai (CHI chay sau khi nguoi dung da dong y)

--check in ra 1 trong cac dong (kem exit code):
    KHONG_CO_CARD        (0)  may khong co card NVIDIA -> khong lam gi, dung libx264 nhu cu
    GPU_SAN_SANG         (0)  NVENC chay duoc roi -> khong can cai gi
    CAN_NANG_DRIVER ...  (3)  co card nhung driver cu -> skill HOI nguoi dung 1 cau, OK thi chay ban cai
    KHONG_RO ...         (4)  co card nhung khong tu xac dinh duoc -> huong dan cai tay tu nvidia.com

Ban cai lam TU DONG het: tra dung ban driver theo ten card (API chinh thuc nvidia.com),
tai ve (~1GB), cai IM LANG chi rieng Display Driver (khong kem app phu), canh den khi xong.
Nguoi dung chi phai BAM "YES" 1 lan tren hop thoai xanh cua Windows (UAC — chot bao mat
bat buoc, khong phan mem nao duoc phep tu bam ho). Lo tay de troi hop thoai -> script tu
bat lai, toi da 3 lan.

Luat di kem (SKILL.md): CHI chay ban cai khi nguoi dung da OK; khong bao gio tu y cai.
"""
import json
import os
import re
import subprocess
import sys
import tempfile
import time
import urllib.request

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_PATH = os.path.join(SKILL_DIR, "config.json")
LOOKUP_SERIES = "https://www.nvidia.com/Download/API/lookupValueSearch.aspx?TypeID=2"
LOOKUP_PRODUCT = "https://www.nvidia.com/Download/API/lookupValueSearch.aspx?TypeID=3&ParentID=%s"
DRIVER_LOOKUP = ("https://gfwsl.geforce.com/services_toolkit/services/com/nvidia/services/"
                 "AjaxDriverService.php?func=DriverManualLookup&psid=%s&pfid=%s&osID=%s"
                 "&languageCode=1033&dch=1&upCRD=0&qnf=0")


def run(cmd, timeout=120):
    return subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8",
                          errors="replace", timeout=timeout, shell=False)


def find_ffmpeg():
    import shutil
    p = shutil.which("ffmpeg")
    if p:
        return p
    if os.path.exists(CONFIG_PATH):
        cfg = json.load(open(CONFIG_PATH, encoding="utf-8"))
        c = (cfg.get("ffmpeg_path") or "").strip()
        if c and os.path.exists(c):
            return c
    return None


def gpu_name_and_driver():
    """Tra (ten_card, ban_driver) hoac (None, None) neu khong co card NVIDIA."""
    try:
        r = run(["nvidia-smi", "--query-gpu=name,driver_version", "--format=csv,noheader"])
        if r.returncode == 0 and r.stdout.strip():
            name, ver = [x.strip() for x in r.stdout.strip().splitlines()[0].split(",")[:2]]
            return re.sub(r"^NVIDIA\s+", "", name), ver
    except FileNotFoundError:
        pass
    # nvidia-smi khong co -> hoi Windows xem co card NVIDIA khong (driver qua cu/loi)
    r = run(["powershell", "-NoProfile", "-Command",
             "(Get-CimInstance Win32_VideoController | Where-Object {$_.Name -match 'NVIDIA'}).Name"])
    name = (r.stdout or "").strip().splitlines()
    if name and name[0].strip():
        return re.sub(r"^NVIDIA\s+", "", name[0].strip()), None
    return None, None


def nvenc_ok(ffmpeg):
    if not ffmpeg:
        return False
    r = run([ffmpeg, "-hide_banner", "-loglevel", "error", "-f", "lavfi",
             "-i", "color=c=black:s=256x256:d=1", "-c:v", "h264_nvenc", "-f", "null", "-"])
    return r.returncode == 0


def is_laptop():
    r = run(["powershell", "-NoProfile", "-Command",
             "(Get-CimInstance Win32_SystemEnclosure).ChassisTypes"])
    types = set(re.findall(r"\d+", r.stdout or ""))
    return bool(types & {"8", "9", "10", "14", "30", "31", "32"})


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read().decode("utf-8", "replace")


def find_driver(gpu_name, laptop):
    """Tra (version, download_url) tu API chinh thuc nvidia.com theo ten card."""
    m = re.search(r"(GTX|RTX|MX|GT)\s*(\d)\d", gpu_name, re.I)
    series_xml = fetch(LOOKUP_SERIES)
    series = re.findall(r'<Name>([^<]+)</Name>\s*<Value>(\d+)</Value>', series_xml)
    cands = []
    for name, psid in series:
        if "Notebook" in name and not laptop:
            continue
        if "Notebook" not in name and laptop:
            continue
        if m and (m.group(1).upper() in name.upper()) and (m.group(2) in name):
            cands.append(psid)
    if not cands:  # khong doan duoc dong -> quet het dung loai may
        cands = [psid for name, psid in series if ("Notebook" in name) == laptop]
    for psid in cands:
        prod_xml = fetch(LOOKUP_PRODUCT % psid)
        prods = re.findall(r'<Name>([^<]+)</Name>\s*<Value>(\d+)</Value>', prod_xml)
        for pname, pfid in prods:
            if pname.strip().upper().replace("NVIDIA ", "") == gpu_name.strip().upper():
                for osid in ("135", "57"):  # Win11 truoc, Win10 sau
                    try:
                        data = json.loads(fetch(DRIVER_LOOKUP % (psid, pfid, osid)))
                        info = data["IDS"][0]["downloadInfo"]
                        if info.get("DownloadURL"):
                            return info["Version"], info["DownloadURL"]
                    except Exception:
                        continue
    return None, None


def download(url, dest):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=120) as r, open(dest, "wb") as f:
        total = int(r.headers.get("Content-Length") or 0)
        got, mark = 0, 0
        while True:
            chunk = r.read(1024 * 512)
            if not chunk:
                break
            f.write(chunk)
            got += len(chunk)
            if total and got * 10 // total > mark:
                mark = got * 10 // total
                print("  tai %d%%..." % (mark * 10), flush=True)
    return os.path.getsize(dest)


def installer_running():
    r = run(["tasklist", "/FI", "IMAGENAME eq setup.exe"])
    return "setup.exe" in (r.stdout or "")


def current_driver():
    try:
        r = run(["nvidia-smi", "--query-gpu=driver_version", "--format=csv,noheader"])
        return (r.stdout or "").strip()
    except Exception:
        return ""


def main():
    ffmpeg = find_ffmpeg()
    name, ver = gpu_name_and_driver()
    if not name:
        print("KHONG_CO_CARD — may khong co card NVIDIA, render dung libx264 nhu cu (khong sao ca).")
        sys.exit(0)
    if nvenc_ok(ffmpeg):
        print("GPU_SAN_SANG — NVENC chay tot roi, khong can cai gi. Card: %s, driver %s" % (name, ver))
        sys.exit(0)

    if "--check" in sys.argv:
        print("CAN_NANG_DRIVER | card: %s | driver hien tai: %s" % (name, ver or "khong ro/qua cu"))
        print("-> Skill HOI nguoi dung 1 cau; ho OK thi chay lai script nay KHONG co --check.")
        sys.exit(3)

    laptop = is_laptop()
    print("Do thay card %s (driver %s, %s) — dang tra ban driver moi nhat tu nvidia.com..."
          % (name, ver or "?", "laptop" if laptop else "PC"))
    new_ver, url = find_driver(name, laptop)
    if not url:
        print("KHONG_RO — khong tu tra duoc ban driver cho '%s'. Cai tay: vao nvidia.com/drivers,"
              " chon dung ten card, tai ban moi nhat, cai mac dinh." % name)
        sys.exit(4)

    dest = os.path.join(tempfile.gettempdir(), "nvidia-%s.exe" % new_ver)
    if not (os.path.exists(dest) and os.path.getsize(dest) > 100 * 1024 * 1024):
        print("Tai driver %s (~1GB, nguon chinh thuc nvidia.com)..." % new_ver)
        download(url, dest)
    print("Tai xong. Bat dau cai IM LANG (chi Display Driver, khong app phu).")

    for attempt in range(1, 4):
        print("\n>>> HOP THOAI XANH CUA WINDOWS SAP HIEN — NGUOI DUNG BAM 'YES' GIUP NHE! (lan %d/3)" % attempt,
              flush=True)
        run(["powershell", "-NoProfile", "-Command",
             "Start-Process -FilePath '%s' -ArgumentList '-s','-noreboot','Display.Driver' -Verb RunAs" % dest])
        deadline = time.time() + 240
        while time.time() < deadline:
            time.sleep(20)
            if current_driver() == new_ver:
                break
            if not installer_running():
                # chua thay installer chay -> co the hop thoai bi troi; cho them chut roi thu lai
                pass
        if current_driver() == new_ver:
            break
        if installer_running():
            # dang cai that -> cho them toi 10 phut
            deadline2 = time.time() + 600
            while time.time() < deadline2 and current_driver() != new_ver:
                time.sleep(20)
            break

    final = current_driver()
    if final == new_ver:
        ok = nvenc_ok(ffmpeg)
        print("\nXONG: driver %s da vao. NVENC: %s" % (final, "CHAY TOT — tu phien dung sau render nhanh 2-5 lan" if ok
                                                       else "van chua bat duoc (thu khoi dong lai may roi probe lai)"))
        sys.exit(0)
    print("\nCHUA CAI DUOC (driver van %s) — kha nang hop thoai Yes chua duoc bam du 3 lan."
          " Chay lai script nay khi nguoi dung san sang, hoac mo file %s cai tay." % (final or "?", dest))
    sys.exit(5)


if __name__ == "__main__":
    main()

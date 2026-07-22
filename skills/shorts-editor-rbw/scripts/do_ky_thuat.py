# -*- coding: utf-8 -*-
"""TANG DO — cham diem KY THUAT tung clip bang may, KHONG can API, KHONG ton tien.

Do 2 thu ma truoc day phai soi bang mat:
  1. DO NET      : clip mo hay ro (Laplacian variance)
  2. CHUYEN DONG : canh tinh ngat hay co chuyen dong

DA THU VA BO: nhan dien MAT NGUOI de tu dong hoa luat cam MC-cutaway.
  Ban Haar cascade cua OpenCV (thu 20/07/2026) KHONG dat: tren footage nha xuong that
  no vua BAT NHAM nep ao thanh mat, vua BO SOT mat nghieng — cham 47/70 clip "co mat
  truc dien", kiem lai bang mat thi phan lon la nhieu. Bo hon la giu, vi mot canh bao
  sai nhieu se bi nguoi dung quen di, roi den luc no bao dung thi cung khong ai tin.
  MediaPipe cai duoc nhung xung dot protobuf; OpenCV 4.5.3 chua co YuNet.
  -> Viec "co ai dang noi / nhin may quay khong" giao cho MAT AI GEMINI (truong
     'co_nguoi_dang_noi'), no lam dung viec do va con hieu duoc ca noi dung.

Vi tri trong day chuyen: chay TRUOC khi doc sheet / truoc khi goi mat AI Gemini.
Muc dich la LOC BOT clip khong dung duoc, de nguoi (va Gemini) chi phai xem phan con lai.

  Do (script nay)  ->  Hieu (Gemini / doc sheet)  ->  Quyet (chon canh, viet kich ban)

Cach dung:
    python do_ky_thuat.py --src "<folder chua clip>" --index "<...\\analysis\\index.json>"
    python do_ky_thuat.py --src "<folder>" --index "<index.json>" --khung 8 --lam-lai

  --khung    so khung lay mau moi clip (mac dinh 6)
  --lam-lai  do lai ca clip da co ket qua (mac dinh: bo qua, chay lai an toan)

Ghi vao index.json, moi clip them truong "do_ky_thuat":
    { "do_net": 148.2, "do_net_hang": 0.82, "chuyen_dong": 12.4,
      "mat_truc_dien": 0.33, "mat_nghieng": 0.17, "canh_bao": ["co-mat-truc-dien"] }

CANH BAO LA CO, KHONG PHAI AN QUYET DINH:
  - "mo"  co the la bokeh/motion blur co chu y -> nguoi xem lai roi quyet.
  - "co-mat-truc-dien" co the chi la khach vo tinh liec ong kinh.
  Script chi THU HEP viec phai xem, khong thay viec xem.
"""
import argparse
import json
import os
import subprocess
import sys
import tempfile

# Bao dam goi ffmpeg/ffprobe chay duoc tren MOI may (them 22/07/2026).
# Thieu ffmpeg thi bao bang tieng nguoi, khong de vo voi 'WinError 2'.
try:
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from chung_ffmpeg import nap_ffmpeg
    nap_ffmpeg()
except ImportError:
    pass


if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

try:
    import cv2
    import numpy as np
except ImportError:
    sys.exit('THIEU THU VIEN: chay  python -m pip install opencv-python "numpy<2"  roi thu lai.')

DUOI_VIDEO = (".mp4", ".mov", ".mts", ".avi", ".mkv", ".m4v")

# Nguong tuyet doi — hieu chinh tu so do that tren footage Roboworld (20/07/2026):
# canh duoc chon 148-153 · canh bi loai vi mo 54 va 9.
NET_MO = 60.0        # duoi muc nay: gan nhu chac chan mo
NET_HOI_MO = 100.0   # 60-100: dang ngo, nen xem lai
TINH = 3.0           # duoi muc nay: canh gan nhu dung yen


def _ffprobe_dai(path):
    try:
        return float(subprocess.check_output(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "default=nw=1:nk=1", path]).decode().strip())
    except Exception:
        return 0.0


def _lay_khung(path, n):
    """Lay n khung rai deu. Uu tien doc thang bang OpenCV; that bai thi nho ffmpeg."""
    khung = []
    cap = cv2.VideoCapture(path)
    if cap.isOpened():
        tong = int(cap.get(cv2.CAP_PROP_FRAME_COUNT) or 0)
        if tong > 0:
            for i in range(n):
                cap.set(cv2.CAP_PROP_POS_FRAMES, int(tong * (i + 0.5) / n))
                ok, f = cap.read()
                if ok and f is not None:
                    khung.append(f)
    cap.release()
    if len(khung) >= max(2, n // 2):
        return khung

    # Du phong: ffmpeg trich ra file tam (chac chan hon voi codec la)
    dai = _ffprobe_dai(path)
    if dai <= 0:
        return khung
    tmp = tempfile.mkdtemp(prefix="dokt_")
    try:
        for i in range(n):
            t = dai * (i + 0.5) / n
            o = os.path.join(tmp, "f%02d.png" % i)
            subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", "%.3f" % t,
                            "-i", path, "-frames:v", "1", o],
                           check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            if os.path.exists(o):
                img = cv2.imread(o)
                if img is not None:
                    khung.append(img)
        return khung
    finally:
        import shutil
        shutil.rmtree(tmp, ignore_errors=True)


_CASCADE = {}


def _cascade(ten):
    if ten not in _CASCADE:
        _CASCADE[ten] = cv2.CascadeClassifier(os.path.join(cv2.data.haarcascades, ten))
    return _CASCADE[ten]


def do_1_clip(path, so_khung=6):
    khung = _lay_khung(path, so_khung)
    if len(khung) < 2:
        return None

    xam = [cv2.cvtColor(k, cv2.COLOR_BGR2GRAY) for k in khung]
    nho = [cv2.resize(g, (320, int(320 * g.shape[0] / g.shape[1]))) for g in xam]

    # 1) DO NET — lay KHUNG NET NHAT, khong lay trung vi.
    # Ly do (bai hoc 20/07): cai can biet la "clip nay CO khoanh khac nao net dung duoc
    # khong", chu khong phai "ca clip co net deu khong". Clip 0107 trung vi chi 78 (bi
    # cham nham "hoi mo") nhung dung giay 6.5 net 148 — va do chinh la doan duoc chon dung.
    tung_khung = [float(cv2.Laplacian(g, cv2.CV_64F).var()) for g in xam]
    net = float(max(tung_khung))
    net_tb = float(np.median(tung_khung))

    # 2) CHUYEN DONG — chenh lech trung binh giua cac khung lien tiep
    dif = [float(np.mean(cv2.absdiff(nho[i], nho[i + 1]))) for i in range(len(nho) - 1)]
    chuyen_dong = float(np.mean(dif)) if dif else 0.0

    kq = {"do_net": round(net, 1),
          "do_net_trung_binh": round(net_tb, 1),
          "chuyen_dong": round(chuyen_dong, 2),
          "so_khung_do": len(xam)}

    cb = []
    if net < NET_MO:
        cb.append("mo")          # ca clip khong co lay 1 khoanh khac net
    elif net < NET_HOI_MO:
        cb.append("hoi-mo")
    if net_tb < NET_MO <= net:
        cb.append("net-tung-doan")   # co doan net, co doan mo -> phai chon dung doan
    if chuyen_dong < TINH:
        cb.append("canh-tinh")
    kq["canh_bao"] = cb
    return kq


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True, help="folder chua clip (quet ca thu muc con)")
    ap.add_argument("--index", required=True, help="duong dan index.json de ghi ket qua")
    ap.add_argument("--khung", type=int, default=6)
    ap.add_argument("--lam-lai", action="store_true")
    a = ap.parse_args()

    idx = {"clips": {}}
    if os.path.exists(a.index):
        idx = json.load(open(a.index, encoding="utf-8"))
    idx.setdefault("clips", {})

    # os.walk chu KHONG glob -> chay duoc ca khi duong dan chua ngoac vuong [ ]
    files = []
    for root, dirs, fs in os.walk(a.src):
        dirs[:] = [d for d in dirs if d.lower() != "workspace"]
        for f in fs:
            if f.lower().endswith(DUOI_VIDEO):
                files.append(os.path.join(root, f))
    files.sort()
    if not files:
        sys.exit("Khong thay clip nao trong: " + a.src)

    # index dinh danh clip theo "ten|size" — bam theo cach analyze_footage da dung
    theo_ten = {}
    for k, v in idx["clips"].items():
        theo_ten.setdefault(os.path.basename(v.get("file", k.split("|")[0])), k)

    print("Tim thay %d clip. Bat dau do (khong ton tien, khong goi API)...\n" % len(files))
    xong, bo_qua = 0, 0
    for p in files:
        ten = os.path.basename(p)
        khoa = theo_ten.get(ten) or ("%s|%d" % (ten, os.path.getsize(p)))
        muc = idx["clips"].setdefault(khoa, {"file": ten})
        if muc.get("do_ky_thuat") and not a.lam_lai:
            bo_qua += 1
            continue
        kq = do_1_clip(p, a.khung)
        if kq is None:
            print("  %-34s KHONG DOC DUOC" % ten[:34])
            continue
        muc["do_ky_thuat"] = kq
        xong += 1
        cb = ",".join(kq["canh_bao"]) or "-"
        print("  %-34s net %6.0f (tb %5.0f) | dong %5.1f | %s"
              % (ten[:34], kq["do_net"], kq["do_net_trung_binh"], kq["chuyen_dong"], cb))
        json.dump(idx, open(a.index, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    # Xep hang do net TUONG DOI trong chinh folder nay (canh quay toi van net hon canh mo)
    ds = [(k, v["do_ky_thuat"]["do_net"]) for k, v in idx["clips"].items() if v.get("do_ky_thuat")]
    ds.sort(key=lambda x: x[1])
    for i, (k, _) in enumerate(ds):
        idx["clips"][k]["do_ky_thuat"]["do_net_hang"] = round((i + 1) / len(ds), 2)
    json.dump(idx, open(a.index, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    def dem(co):
        return sum(1 for v in idx["clips"].values()
                   if v.get("do_ky_thuat") and co in v["do_ky_thuat"]["canh_bao"])

    tong_do = sum(1 for v in idx["clips"].values() if v.get("do_ky_thuat"))
    print("\nXONG: do moi %d clip, bo qua %d clip da co ket qua." % (xong, bo_qua))
    print("Canh bao tren %d clip: %d MO · %d HOI-MO · %d NET-TUNG-DOAN · %d CANH-TINH"
          % (tong_do, dem("mo"), dem("hoi-mo"), dem("net-tung-doan"), dem("canh-tinh")))
    print("")
    print("DOC KET QUA:")
    print("  mo            -> ca clip khong co khoanh khac nao net; gan nhu chac chan bo")
    print("  hoi-mo        -> dang ngo, xem lai truoc khi dung")
    print("  net-tung-doan -> CO doan net va CO doan mo -> phai chon dung doan, dung cat bua")
    print("  canh-tinh     -> gan nhu dung yen, hop lam nen chu hon lam canh chinh")
    print("Day la CO CANH BAO, khong phai an quyet dinh — bokeh/motion blur co chu y")
    print("cung bi cham 'mo'. Nguoi xem lai roi quyet.")
    print("Ghi vao:", a.index)


if __name__ == "__main__":
    main()

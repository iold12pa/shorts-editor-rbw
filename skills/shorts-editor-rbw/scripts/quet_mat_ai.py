# -*- coding: utf-8 -*-
"""Quet MAT AI Gemini ca folder footage: nen 720p (GPU) -> gui len -> hoi -> ghi index.json.

- Resume: clip da co truong 'gemini' trong index -> BO QUA (chay lai an toan).
- 429 (cham gioi han free) -> nghi lui dan (60s/120s/240s...), het 5 lan -> dung, chay lai sau.
- Xoa file tren cloud + file nen tam ngay sau moi clip.
- Ghi index sau MOI clip -> ngat giua chung khong mat gi.

Usage:
    python quet_mat_ai_folder.py --src "D:/.../30.Nha sach Trang An" \
        --index "D:/.../Workspace/analysis/index.json" [--model gemini-2.5-flash] [--limit N]
"""
import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
import time

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ENV = os.path.expanduser("~/.claude/abs6-secrets.env")
RATE = 26000
PRICE = {"gemini-2.5-flash": (0.30, 2.50)}

# HAN SU DUNG MODEL — Google tat model theo lich, tat roi thi moi lenh quet deu
# vo giua chung voi loi API kho hieu (404 NOT_FOUND), khong ai doan ra vi sao.
# Kiem tra o day de bao truoc bang tieng nguoi. Cap nhat lich tai:
#   https://ai.google.dev/gemini-api/docs/changelog
HAN_MODEL = {
    "gemini-2.5-flash": "2026-10-16",
}
# Da bi Google TAT (dung dua lai vao PRICE): gemini-2.0-flash (tat 01/06/2026),
# gemini-1.5-* (tat 2025). Ai truyen --model tro vao day se nhan canh bao ro rang.
MODEL_DA_TAT = {
    "gemini-2.0-flash": "01/06/2026",
    "gemini-2.0-flash-001": "01/06/2026",
    "gemini-1.5-flash": "2025",
    "gemini-1.5-pro": "2025",
}


def kiem_han_model(ten_model):
    """Bao truoc khi model sap/da bi Google tat — goi ngay dau moi lan chay."""
    import datetime
    if ten_model in MODEL_DA_TAT:
        sys.exit(
            "\n!!! MODEL '%s' DA BI GOOGLE TAT tu %s — khong goi duoc nua.\n"
            "    Doi sang model con song, vd: --model gemini-2.5-flash\n"
            % (ten_model, MODEL_DA_TAT[ten_model]))
    han = HAN_MODEL.get(ten_model)
    if not han:
        return
    try:
        ngay_het = datetime.date(*[int(x) for x in han.split("-")])
    except Exception:
        return
    con = (ngay_het - datetime.date.today()).days
    if con < 0:
        sys.exit(
            "\n!!! MODEL '%s' DA QUA HAN NGAY %s — Google co the da tat.\n"
            "    Neu lenh quet bao loi 404/NOT_FOUND thi dung la vi ly do nay.\n"
            "    Xem model con song: https://ai.google.dev/gemini-api/docs/models\n"
            % (ten_model, han))
    if con <= 90:
        print("\n[CANH BAO] Model '%s' se bi Google TAT ngay %s — con %d ngay.\n"
              "           Den ngay do moi lenh quet deu vo. Can doi model truoc do.\n"
              % (ten_model, han, con), flush=True)

PROMPT = """Bạn là biên tập viên video marketing cho công ty robot Roboworld (robot PUDU:
BellaBot phục vụ, robot giao hàng, lễ tân, vệ sinh, T300...). Xem kỹ clip (cả hình lẫn tiếng)
và trả về DUY NHẤT một JSON đúng cấu trúc:

{
 "co_robot": true/false,
 "robot_nhan_ra": "ten dong robot hoac 'khong ro'",
 "hanh_dong": "robot/nguoi dang lam gi (1 cau)",
 "boi_canh": "noi chon cu the",
 "co_nguoi_dang_noi": true/false,
 "chat_luong_hinh": "tot/kha/kem",
 "ly_do_chat_luong": "net/rung/mo/thieu sang...",
 "khoanh_khac": [
   {"t0": giay_bat_dau, "t1": giay_ket_thuc, "mo_ta": "chuyen gi xay ra", "diem_10": diem}
 ],
 "hook_tiem_nang": "canh nao trong clip du la/bat ngo de MO DAU video (hoac null)",
 "am_thanh": "nghe thay gi: nhac nen/tre em cuoi/MC noi dai y gi",
 "nen_dung_lam_shorts": true/false,
 "ly_do": "ngan gon",
 "tu_khoa": ["3-6 tag"],
 "mo_ta": "1-2 cau tom tat"
}

Yeu cau: "khoanh_khac" chon 2-5 khoang DANG DUNG NHAT de cat vao video ngan (t0/t1 la SO GIAY,
diem_10 la muc dang dung 1-10). Chi tra JSON."""


def load_key():
    if not os.path.exists(ENV):
        sys.exit("\n!!! CHUA CO FILE KEY: %s\n"
                 "    Nhap key bang hop thoai: python chuan_bi_may.py --nhap-key\n" % ENV)
    for ln in open(ENV, encoding="utf-8", errors="replace"):
        if ln.strip().startswith("GEMINI_API_KEY="):
            v = ln.strip().split("=", 1)[1].strip().strip('"').strip("'")
            if not v:
                sys.exit("\n!!! DONG GEMINI_API_KEY DANG TRONG trong %s\n"
                         "    Nhap lai: python chuan_bi_may.py --nhap-key\n" % ENV)
            return v
    sys.exit("\n!!! KHONG THAY GEMINI_API_KEY trong %s\n"
             "    Nhap key bang hop thoai: python chuan_bi_may.py --nhap-key\n" % ENV)


def kiem_key_song(client):
    """Goi 1 lenh nhe truoc khi nen/upload clip nao.

    Vi sao can (bai hoc 21-22/07/2026): key BI XOA ben Google van nam nguyen trong
    file, nen script cu chay binh thuong — nen clip, upload — roi moi vo o giua
    voi loi API tho kho hieu, mat cong va mat tien nen clip. Kiem truoc thi hong
    la biet ngay, bang tieng nguoi."""
    try:
        next(iter(client.models.list()), None)
    except Exception as e:
        t = str(e)
        if "API_KEY_INVALID" in t or "API key not valid" in t or "400" in t:
            sys.exit("\n!!! KEY GEMINI KHONG DUNG (co the da bi xoa ben Google).\n"
                     "    Tao key moi tai https://aistudio.google.com/apikey\n"
                     "    roi nhap bang: python chuan_bi_may.py --nhap-key\n")
        if "PERMISSION_DENIED" in t or "403" in t:
            sys.exit("\n!!! KEY GEMINI BI TU CHOI QUYEN (403).\n"
                     "    Thuong do key thuoc project chua bat Generative Language API,\n"
                     "    hoac project da bi go billing. Kiem tai https://aistudio.google.com/apikey\n")
        if "RESOURCE_EXHAUSTED" in t or "429" in t:
            sys.exit("\n!!! HET LUOT MIEN PHI HOM NAY (429) — goi Free tier ~20 luot/ngay.\n"
                     "    Doi sang mai chay tiep (script tu nho clip nao da quet roi),\n"
                     "    hoac gan the vao project de bo tran.\n")
        sys.exit("\n!!! KHONG GOI DUOC GEMINI: %s\n" % t[:300])


def run(cmd, timeout=900):
    return subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8",
                          errors="replace", timeout=timeout)


def nen_720p(src, dst):
    """Nen clip xuong 720p de gui nhanh (mat AI khong can 4K). Thu NVENC truoc, fail thi CPU."""
    for enc in (["-c:v", "h264_nvenc", "-preset", "p4", "-cq", "30"],
                ["-c:v", "libx264", "-preset", "veryfast", "-crf", "28"]):
        r = run(["ffmpeg", "-y", "-v", "error", "-i", src,
                 "-vf", "scale=-2:720", *enc, "-c:a", "aac", "-b:a", "96k", dst])
        if r.returncode == 0 and os.path.exists(dst) and os.path.getsize(dst) > 0:
            return True
    return False


def find_clip(src_root, relpath):
    for cand in (os.path.join(src_root, relpath),
                 os.path.join(src_root, "Nguồn video", relpath)):
        if os.path.exists(cand):
            return cand
    # cuoi cung: tim theo ten file
    base = os.path.basename(relpath)
    for root, _d, files in os.walk(src_root):
        if base in files:
            return os.path.join(root, base)
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True)
    ap.add_argument("--index", required=True)
    ap.add_argument("--model", default="gemini-2.5-flash")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--quet-ca-clip-mo", action="store_true",
                    help="quet ca clip da bi do_ky_thuat cham 'mo' (mac dinh: bo qua cho do ton tien)")
    ap.add_argument("--sleep", type=float, default=7.0)
    # Mac dinh 3 hinh/giay + do net THAP = ton dung bang 1 hinh/giay + do net mac dinh.
    # Muon quay ve cach cu: --fps 0 --do-net MEDIA_RESOLUTION_MEDIUM
    ap.add_argument("--fps", type=float, default=3.0,
                    help="so hinh/giay Gemini lay (0 = de mac dinh cua Google, tuc 1)")
    ap.add_argument("--do-net", default="MEDIA_RESOLUTION_LOW",
                    help="MEDIA_RESOLUTION_LOW (~100 token/khung) | _MEDIUM (~300)")
    a = ap.parse_args()

    kiem_han_model(a.model)

    from google import genai
    from google.genai import types
    client = genai.Client(api_key=load_key())
    kiem_key_song(client)
    pin, pout = PRICE.get(a.model, PRICE["gemini-2.5-flash"])

    idx = json.load(open(a.index, encoding="utf-8"))
    clips = idx.get("clips", {})
    todo = [(k, c) for k, c in clips.items() if not c.get("gemini")]
    da_co = len(clips) - len(todo)

    # NOI VOI TANG DO (luat 20/07/2026): clip da bi do_ky_thuat cham "mo" thi BO QUA,
    # dung ton tien hoi Gemini ve clip khong bao gio dung duoc. Chay do_ky_thuat.py truoc.
    bo_mo = 0
    if not a.quet_ca_clip_mo:
        loc = []
        for k, c in todo:
            dkt = c.get("do_ky_thuat")
            if dkt and "mo" in dkt.get("canh_bao", []):
                bo_mo += 1
                continue
            loc.append((k, c))
        todo = loc

    print("Folder: %s" % a.src, flush=True)
    print("Tong %d clip | da co mat AI: %d | bo qua vi MO: %d | can quet: %d"
          % (len(clips), da_co, bo_mo, len(todo)), flush=True)
    if bo_mo:
        print("  (muon quet ca clip mo thi them --quet-ca-clip-mo)", flush=True)
    if not any(c.get("do_ky_thuat") for c in clips.values()):
        print("  LUU Y: chua chay do_ky_thuat.py cho folder nay — nen chay truoc de loc bot,", flush=True)
        print("         do bang may mien phi, con hoi Gemini thi ton tien.", flush=True)
    if a.limit:
        todo = todo[:a.limit]

    done, spent, t_start = 0, 0.0, time.time()
    for k, c in todo:
        rel = k.split("|")[0]
        path = find_clip(a.src, rel)
        if not path:
            print("BO QUA (khong thay file): %s" % rel, flush=True)
            continue
        name = os.path.basename(path)
        tmp = os.path.join(tempfile.gettempdir(), "rbw_eye_%d.mp4" % os.getpid())
        try:
            if not nen_720p(path, tmp):
                print("LOI nen: %s" % name, flush=True)
                continue
            mb = os.path.getsize(tmp) / 1e6

            # upload + hoi, retry khi 429
            data, u, backoff, err = None, None, 60, None
            for attempt in range(5):
                try:
                    f = client.files.upload(file=tmp)
                    w = 0
                    while getattr(f.state, "name", str(f.state)) == "PROCESSING":
                        time.sleep(2); w += 2
                        f = client.files.get(name=f.name)
                        if w > 300:
                            raise RuntimeError("processing qua lau")
                    # ---- TANG SO KHUNG HINH/GIAY (luat Sep Huy 21/07/2026) ----
                    # Gemini MAC DINH chi lay 1 hinh/giay. Clip khong thoai thi Gemini la
                    # CON MAT DUY NHAT — 1 hinh/giay bo lot khoanh khac nhanh (be nhin robot,
                    # nhan vien tha tay, robot ne nguoi). Clip CO thoai thi moc cat da co
                    # loc_thoai_that lo, Gemini chi can hieu noi dung -> giu 1 hinh/giay cho re.
                    #
                    # DOI NGANG cho khoi ton them tien: ha media_resolution xuong THAP
                    # (~100 token/khung thay vi ~300) roi dung phan tiet kiem do de mua
                    # gap 3 so khung. Sep da xac nhan KHONG can doc chu nho tren man hinh
                    # robot, nen ha do net khong mat gi.
                    vm = types.VideoMetadata(fps=a.fps) if a.fps else None
                    phan = types.Part(file_data=types.FileData(
                        file_uri=f.uri, mime_type=f.mime_type), video_metadata=vm) if vm else f
                    r = client.models.generate_content(
                        model=a.model, contents=[phan, PROMPT],
                        config=types.GenerateContentConfig(
                            response_mime_type="application/json", temperature=0.2,
                            media_resolution=a.do_net))
                    try:
                        client.files.delete(name=f.name)
                    except Exception:
                        pass
                    m = re.search(r"\{.*\}", r.text or "", re.S)
                    data = json.loads(m.group(0)) if m else None
                    u = r.usage_metadata
                    break
                except Exception as e:
                    err = str(e)
                    if "429" in err or "RESOURCE_EXHAUSTED" in err:
                        if "PerDay" in err or "daily" in err.lower():
                            print("HET QUOTA NGAY — dung tai day, mai chay lai tu dong tiep.", flush=True)
                            return
                        print("  cham gioi han nhip, nghi %ds..." % backoff, flush=True)
                        time.sleep(backoff)
                        backoff = min(backoff * 2, 600)
                    else:
                        print("  loi (%s), thu lai sau 15s: %s" % (attempt + 1, err[:120]), flush=True)
                        time.sleep(15)
            if not data:
                print("LOI %s -> bo qua (chay lai sau): %s" % (name, (err or "?")[:120]), flush=True)
                continue

            pt = getattr(u, "prompt_token_count", 0) or 0
            ot = getattr(u, "candidates_token_count", 0) or 0
            vnd = (pt / 1e6 * pin + ot / 1e6 * pout) * RATE
            spent += vnd
            c["gemini"] = data
            c["gemini_meta"] = {"model": a.model, "tok_in": pt, "tok_out": ot,
                                "vnd": round(vnd), "luc": time.strftime("%Y-%m-%d %H:%M")}
            done += 1
            json.dump(idx, open(a.index, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
            best = max((kk.get("diem_10", 0) for kk in data.get("khoanh_khac", []) if isinstance(kk, dict)), default=0)
            print("OK  %-34s %5.1fMB  robot=%-5s q=%-4s best=%s/10  ~%dd  (%d/%d)" % (
                name, mb, data.get("co_robot"), data.get("chat_luong_hinh"),
                best, round(vnd), done, len(todo)), flush=True)
            time.sleep(a.sleep)
        finally:
            if os.path.exists(tmp):
                try: os.remove(tmp)
                except Exception: pass

    mins = (time.time() - t_start) / 60
    print("\nXONG: %d clip trong %.0f phut, chi phi ly thuyet ~%dd (gói free = 0d). Index: %s" % (
        done, mins, round(spent), a.index), flush=True)
    print("QUET XONG TAT CA" if done == len(todo) else "CON THIEU %d clip — chay lai script de quet tiep." % (len(todo) - done), flush=True)


if __name__ == "__main__":
    main()

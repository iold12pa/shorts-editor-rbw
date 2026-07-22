# Chốt chặn trước khi đẩy (git hooks)

File `pre-push` ở đây là **bản gốc** của chốt chặn. Nó chặn 4 tai nạn từng xảy ra thật:

| # | Chặn gì | Vì sao |
|---|---|---|
| 1 | Đẩy file ≥5MB | Repo phình, có ngày phải viết lại lịch sử (vụ 170MB) |
| 2 | Force push / viết lại lịch sử | Làm auto-update mọi máy gãy im lặng, phải gỡ-cài-lại từng máy |
| 3 | Sửa `skills/` mà quên tăng `version` | Luật mới nằm chết trên GitHub, không máy nào nhận (dính thật 21/07/2026) |
| 4 | Script dùng thư viện chưa khai báo trong `chuan_bi_may.py` | Máy quản trị chạy ngon, máy đồng nghiệp vỡ với `No module named ...` (Sếp Huy hỏi ra 22/07/2026) |

## ⚠️ Hook KHÔNG tự đi theo git

Thư mục `.git/hooks/` **không được git quản lý** — clone repo về máy mới là **không có hook nào cả**, mọi chốt chặn mất hiệu lực mà không có gì báo. Đó là lý do file này nằm ở đây.

## Máy quản trị mới (có quyền push) phải chạy 1 lần:

```bash
cp git-hooks/pre-push .git/hooks/pre-push
chmod +x .git/hooks/pre-push
```

Kiểm đã ăn chưa: `ls -la .git/hooks/pre-push` — thấy file là được.

Máy chỉ **dùng** plugin (không push) thì không cần.

## Sửa hook thì sửa ở đâu

Sửa `git-hooks/pre-push` (bản trong repo) **rồi copy đè** sang `.git/hooks/pre-push`. Làm ngược lại thì bản sửa chỉ nằm trên đúng một máy — chính là lỗi mà hook số 4 sinh ra để chặn.

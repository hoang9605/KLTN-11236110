# Đánh giá chuẩn hóa thực thể (Entity Normalization)

> **Nhãn gold là nhãn AI tiền gán, CHƯA được bác sĩ duyệt.** Số liệu dưới đây là tạm thời; cần duyệt `data/norm_gold_v1/ai_labels_test.tsv` rồi chạy lại trước khi đưa vào khóa luận.

- Gold: `data/norm_gold_v1/gold_test.jsonl` — đơn vị đánh giá là **dạng bề mặt duy nhất** (type-level); bảng mention-level trọng số theo tần suất trong split test.
- Thực thể lấy từ **nhãn gold NER** của split `test` VietMed-NER, nên lỗi NER không ảnh hưởng.
- Accuracy: quyết định duy nhất của hệ thống đúng; hệ thống từ chối (không trả mã) tính là sai.
- Top-k Accuracy = Recall@k: mã đúng nằm trong k ứng viên đầu (mỗi đề cập có một khái niệm gold).
- CI95: bootstrap 2000 lần theo dạng bề mặt.

## ICD-10 — mã đầy đủ

Linkable: 246 dạng (1148 đề cập); NIL: 66 dạng (319 đề cập).

| Phương pháp | Accuracy (type) | CI95 | Accuracy (mention) | Coverage | Precision khi trả lời | Từ chối đúng NIL |
|---|---:|---|---:|---:|---:|---:|
| Baseline: khớp chính xác tên danh mục | 0.069 | 0.040–0.102 | 0.092 | 0.069 | 1.000 | 0.985 |
| Baseline: fuzzy top-1 (WRatio, không ràng buộc) | 0.187 | 0.139–0.239 | 0.173 | 1.000 | 0.187 | 0.000 |
| Hệ thống: exact → synonym → fuzzy có ràng buộc | 0.187 | 0.140–0.239 | 0.176 | 0.199 | 0.939 | 0.985 |

| Xếp hạng ứng viên | Top-1 | Top-3 | Top-5 | Top-10 | MRR@10 |
|---|---:|---:|---:|---:|---:|
| Top-k Acc = Recall@k (type) | 0.260 | 0.329 | 0.346 | 0.386 | 0.299 |
| Top-k Acc = Recall@k (mention) | 0.238 | 0.318 | 0.327 | 0.472 | 0.290 |
| CI95 (type) | 0.207–0.320 | | 0.287–0.409 | 0.329–0.451 | |

## ICD-10 — nhóm 3 ký tự (category)

Linkable: 246 dạng (1148 đề cập); NIL: 66 dạng (319 đề cập).

| Phương pháp | Accuracy (type) | CI95 | Accuracy (mention) | Coverage | Precision khi trả lời | Từ chối đúng NIL |
|---|---:|---|---:|---:|---:|---:|
| Baseline: khớp chính xác tên danh mục | 0.069 | 0.040–0.102 | 0.092 | 0.069 | 1.000 | 0.985 |
| Baseline: fuzzy top-1 (WRatio, không ràng buộc) | 0.215 | 0.166–0.269 | 0.232 | 1.000 | 0.215 | 0.000 |
| Hệ thống: exact → synonym → fuzzy có ràng buộc | 0.187 | 0.140–0.239 | 0.176 | 0.199 | 0.939 | 0.985 |

| Xếp hạng ứng viên | Top-1 | Top-3 | Top-5 | Top-10 | MRR@10 |
|---|---:|---:|---:|---:|---:|
| Top-k Acc = Recall@k (type) | 0.289 | 0.362 | 0.370 | 0.411 | 0.326 |
| Top-k Acc = Recall@k (mention) | 0.296 | 0.377 | 0.380 | 0.540 | 0.349 |
| CI95 (type) | 0.233–0.351 | | 0.309–0.433 | 0.349–0.476 | |

## RxNorm — mã đầy đủ

Linkable: 47 dạng (305 đề cập); NIL: 81 dạng (422 đề cập).

| Phương pháp | Accuracy (type) | CI95 | Accuracy (mention) | Coverage | Precision khi trả lời | Từ chối đúng NIL |
|---|---:|---|---:|---:|---:|---:|
| Baseline/Hệ thống: RxNav khớp tên chính xác | 0.404 | 0.273–0.550 | 0.498 | 0.426 | 0.950 | 1.000 |
| Baseline: RxNav approximateTerm top-1 | 0.468 | 0.326–0.609 | 0.462 | 0.979 | 0.478 | 0.160 |
| Hệ thống (hiện = RxNav khớp chính xác + cache) | 0.404 | 0.273–0.550 | 0.498 | 0.426 | 0.950 | 1.000 |

| Xếp hạng ứng viên | Top-1 | Top-3 | Top-5 | Top-10 | MRR@10 |
|---|---:|---:|---:|---:|---:|
| Top-k Acc = Recall@k (type) | 0.489 | 0.532 | 0.532 | 0.532 | 0.511 |
| Top-k Acc = Recall@k (mention) | 0.518 | 0.528 | 0.528 | 0.528 | 0.523 |
| CI95 (type) | 0.347–0.630 | | 0.395–0.667 | 0.395–0.667 | |

## Lỗi của hệ thống (trả mã sai, mã đầy đủ)

| Ontology | Dạng | Tần suất | Hệ thống | Gold |
|---|---|---:|---|---|
| ICD-10 | u xơ tử cung | 19 | C53 | D25, D25.9 |
| RxNorm | carbonate | 2 | 1544139 | 1897 |
| ICD-10 | gãy xương khớp háng | 1 | S22.2 | S72.0, S32.4, S72 |
| ICD-10 | tiết sữa | 1 | O92.6 | NIL |
| ICD-10 | viêm thần kinh tọa | 1 | H46 | M54.3 |

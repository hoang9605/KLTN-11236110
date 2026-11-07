# Đánh giá chuẩn hóa thực thể (Entity Normalization)

> **Nhãn gold là nhãn AI tiền gán, CHƯA được bác sĩ duyệt.** Số liệu dưới đây là tạm thời; cần duyệt `data/norm_gold_v1/ai_labels_test.tsv` rồi chạy lại trước khi đưa vào khóa luận.

- Gold: `data/norm_gold_v1/gold_dev.jsonl` — đơn vị đánh giá là **dạng bề mặt duy nhất** (type-level); bảng mention-level trọng số theo tần suất trong split test.
- Thực thể lấy từ **nhãn gold NER** của split `test` VietMed-NER, nên lỗi NER không ảnh hưởng.
- Accuracy: quyết định duy nhất của hệ thống đúng; hệ thống từ chối (không trả mã) tính là sai.
- Top-k Accuracy = Recall@k: mã đúng nằm trong k ứng viên đầu (mỗi đề cập có một khái niệm gold).
- CI95: bootstrap 2000 lần theo dạng bề mặt.

## ICD-10 — mã đầy đủ

Linkable: 147 dạng (542 đề cập); NIL: 46 dạng (204 đề cập).

| Phương pháp | Accuracy (type) | CI95 | Accuracy (mention) | Coverage | Precision khi trả lời | Từ chối đúng NIL |
|---|---:|---|---:|---:|---:|---:|
| Baseline: khớp chính xác tên danh mục | 0.068 | 0.028–0.112 | 0.083 | 0.068 | 1.000 | 0.978 |
| Baseline: fuzzy top-1 (WRatio, không ràng buộc) | 0.197 | 0.135–0.264 | 0.190 | 1.000 | 0.197 | 0.000 |
| Hệ thống: exact → synonym → fuzzy có ràng buộc | 0.156 | 0.100–0.215 | 0.203 | 0.163 | 0.958 | 0.978 |

| Xếp hạng ứng viên | Top-1 | Top-3 | Top-5 | Top-10 | MRR@10 |
|---|---:|---:|---:|---:|---:|
| Top-k Acc = Recall@k (type) | 0.245 | 0.313 | 0.367 | 0.401 | 0.293 |
| Top-k Acc = Recall@k (mention) | 0.277 | 0.465 | 0.520 | 0.544 | 0.385 |
| CI95 (type) | 0.177–0.318 | | 0.289–0.449 | 0.325–0.484 | |

## ICD-10 — nhóm 3 ký tự (category)

Linkable: 147 dạng (542 đề cập); NIL: 46 dạng (204 đề cập).

| Phương pháp | Accuracy (type) | CI95 | Accuracy (mention) | Coverage | Precision khi trả lời | Từ chối đúng NIL |
|---|---:|---|---:|---:|---:|---:|
| Baseline: khớp chính xác tên danh mục | 0.068 | 0.028–0.112 | 0.083 | 0.068 | 1.000 | 0.978 |
| Baseline: fuzzy top-1 (WRatio, không ràng buộc) | 0.238 | 0.171–0.308 | 0.232 | 1.000 | 0.238 | 0.000 |
| Hệ thống: exact → synonym → fuzzy có ràng buộc | 0.156 | 0.100–0.215 | 0.203 | 0.163 | 0.958 | 0.978 |

| Xếp hạng ứng viên | Top-1 | Top-3 | Top-5 | Top-10 | MRR@10 |
|---|---:|---:|---:|---:|---:|
| Top-k Acc = Recall@k (type) | 0.286 | 0.374 | 0.415 | 0.449 | 0.338 |
| Top-k Acc = Recall@k (mention) | 0.319 | 0.526 | 0.544 | 0.572 | 0.425 |
| CI95 (type) | 0.214–0.364 | | 0.336–0.500 | 0.367–0.531 | |

## RxNorm — mã đầy đủ

Linkable: 37 dạng (78 đề cập); NIL: 91 dạng (280 đề cập).

| Phương pháp | Accuracy (type) | CI95 | Accuracy (mention) | Coverage | Precision khi trả lời | Từ chối đúng NIL |
|---|---:|---|---:|---:|---:|---:|
| Baseline/Hệ thống: RxNav khớp tên chính xác | 0.324 | 0.178–0.486 | 0.256 | 0.324 | 1.000 | 1.000 |
| Baseline: RxNav approximateTerm top-1 | 0.432 | 0.275–0.595 | 0.256 | 0.946 | 0.457 | 0.165 |
| Hệ thống (hiện = RxNav khớp chính xác + cache) | 0.324 | 0.178–0.486 | 0.256 | 0.324 | 1.000 | 1.000 |

| Xếp hạng ứng viên | Top-1 | Top-3 | Top-5 | Top-10 | MRR@10 |
|---|---:|---:|---:|---:|---:|
| Top-k Acc = Recall@k (type) | 0.459 | 0.514 | 0.514 | 0.514 | 0.482 |
| Top-k Acc = Recall@k (mention) | 0.321 | 0.359 | 0.359 | 0.359 | 0.338 |
| CI95 (type) | 0.300–0.615 | | 0.351–0.676 | 0.351–0.676 | |

## Lỗi của hệ thống (trả mã sai, mã đầy đủ)

| Ontology | Dạng | Tần suất | Hệ thống | Gold |
|---|---|---:|---|---|
| ICD-10 | chấn động | 1 | S06.0 | NIL |
| ICD-10 | rối loạn vận động | 1 | F44.4 | R27.8, G25.9 |

# Đánh giá chuẩn hóa thực thể (Entity Normalization)

> **Nhãn gold là nhãn AI tiền gán, CHƯA được bác sĩ duyệt.** Số liệu dưới đây là tạm thời; cần duyệt `data/norm_gold_v1/ai_labels_test.tsv` rồi chạy lại trước khi đưa vào khóa luận.

- Gold: `data/norm_gold_v1/gold_dev.jsonl` — đơn vị đánh giá là **dạng bề mặt duy nhất** (type-level); bảng mention-level trọng số theo tần suất trong split test.
- Thực thể lấy từ **nhãn gold NER** của split `test` VietMed-NER, nên lỗi NER không ảnh hưởng.
- Accuracy: quyết định duy nhất của hệ thống đúng; hệ thống từ chối (không trả mã) tính là sai.
- Hai chế độ: **thận trọng** (từ chối khi không chắc, ưu tiên precision) và **luôn trả lời** (lấy ứng viên top-1 khi không chắc; Accuracy = Top-1, nhưng mọi dạng NIL đều bị gán mã).
- Top-k Accuracy = Recall@k: mã đúng nằm trong k ứng viên đầu (mỗi đề cập có một khái niệm gold). Ứng viên: quyết định của hệ thống đứng đầu, sau đó ICD-10 theo TF-IDF n-gram ký tự, RxNorm theo RxNav approximateTerm.
- CI95: bootstrap 2000 lần theo dạng bề mặt.

## ICD-10 — mã đầy đủ

Linkable: 147 dạng (542 đề cập); NIL: 46 dạng (204 đề cập).

| Phương pháp | Accuracy (type) | CI95 | Accuracy (mention) | Coverage | Precision khi trả lời | Từ chối đúng NIL |
|---|---:|---|---:|---:|---:|---:|
| Baseline: khớp chính xác tên danh mục | 0.068 | 0.028–0.112 | 0.083 | 0.068 | 1.000 | 0.978 |
| Baseline: fuzzy top-1 (WRatio, không ràng buộc) | 0.197 | 0.135–0.264 | 0.190 | 1.000 | 0.197 | 0.000 |
| Hệ thống – chế độ thận trọng (exact → synonym → fuzzy có ràng buộc) | 0.796 | 0.734–0.858 | 0.917 | 0.796 | 1.000 | 0.978 |
| Hệ thống – chế độ luôn trả lời (thận trọng, nếu không thì ứng viên TF-IDF top-1) | 0.837 | 0.779–0.892 | 0.930 | 1.000 | 0.837 | 0.000 |

| Xếp hạng ứng viên | Top-1 | Top-3 | Top-5 | Top-10 | MRR@10 |
|---|---:|---:|---:|---:|---:|
| Top-k Acc = Recall@k (type) | 0.837 | 0.857 | 0.864 | 0.891 | 0.853 |
| Top-k Acc = Recall@k (mention) | 0.930 | 0.935 | 0.945 | 0.952 | 0.936 |
| CI95 (type) | 0.779–0.892 | | 0.808–0.918 | 0.840–0.938 | |

## ICD-10 — nhóm 3 ký tự (category)

Linkable: 147 dạng (542 đề cập); NIL: 46 dạng (204 đề cập).

| Phương pháp | Accuracy (type) | CI95 | Accuracy (mention) | Coverage | Precision khi trả lời | Từ chối đúng NIL |
|---|---:|---|---:|---:|---:|---:|
| Baseline: khớp chính xác tên danh mục | 0.068 | 0.028–0.112 | 0.083 | 0.068 | 1.000 | 0.978 |
| Baseline: fuzzy top-1 (WRatio, không ràng buộc) | 0.238 | 0.171–0.308 | 0.232 | 1.000 | 0.238 | 0.000 |
| Hệ thống – chế độ thận trọng (exact → synonym → fuzzy có ràng buộc) | 0.796 | 0.734–0.858 | 0.917 | 0.796 | 1.000 | 0.978 |
| Hệ thống – chế độ luôn trả lời (thận trọng, nếu không thì ứng viên TF-IDF top-1) | 0.864 | 0.807–0.916 | 0.937 | 1.000 | 0.864 | 0.000 |

| Xếp hạng ứng viên | Top-1 | Top-3 | Top-5 | Top-10 | MRR@10 |
|---|---:|---:|---:|---:|---:|
| Top-k Acc = Recall@k (type) | 0.864 | 0.891 | 0.905 | 0.912 | 0.880 |
| Top-k Acc = Recall@k (mention) | 0.937 | 0.945 | 0.956 | 0.958 | 0.944 |
| CI95 (type) | 0.807–0.916 | | 0.854–0.950 | 0.863–0.954 | |

## RxNorm — mã đầy đủ

Linkable: 37 dạng (78 đề cập); NIL: 91 dạng (280 đề cập).

| Phương pháp | Accuracy (type) | CI95 | Accuracy (mention) | Coverage | Precision khi trả lời | Từ chối đúng NIL |
|---|---:|---|---:|---:|---:|---:|
| Baseline: RxNav khớp tên chính xác | 0.324 | 0.178–0.486 | 0.256 | 0.324 | 1.000 | 1.000 |
| Baseline: RxNav approximateTerm top-1 | 0.432 | 0.275–0.595 | 0.256 | 0.946 | 0.457 | 0.165 |
| Hệ thống – chế độ thận trọng (exact → alias Việt→Anh → bỏ tiền tố → approx gần trùng) | 0.811 | 0.675–0.931 | 0.897 | 0.811 | 1.000 | 0.978 |
| Hệ thống – chế độ luôn trả lời (thận trọng, nếu không thì approximateTerm top-1) | 0.892 | 0.784–0.975 | 0.936 | 1.000 | 0.892 | 0.165 |

| Xếp hạng ứng viên | Top-1 | Top-3 | Top-5 | Top-10 | MRR@10 |
|---|---:|---:|---:|---:|---:|
| Top-k Acc = Recall@k (type) | 0.892 | 0.919 | 0.919 | 0.919 | 0.905 |
| Top-k Acc = Recall@k (mention) | 0.936 | 0.962 | 0.962 | 0.962 | 0.949 |
| CI95 (type) | 0.784–0.975 | | 0.821–1.000 | 0.821–1.000 | |

## Lỗi của hệ thống (trả mã sai, mã đầy đủ)

| Ontology | Dạng | Tần suất | Hệ thống | Gold |
|---|---|---:|---|---|
| RxNorm | protein | 4 | 8859 | NIL |
| ICD-10 | chấn động | 1 | S06.0 | NIL |
| RxNorm | carbohydrate | 1 | 2028 | NIL |

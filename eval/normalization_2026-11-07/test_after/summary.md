# Đánh giá chuẩn hóa thực thể (Entity Normalization)

> **Nhãn gold là nhãn AI tiền gán, CHƯA được bác sĩ duyệt.** Số liệu dưới đây là tạm thời; cần duyệt `data/norm_gold_v1/ai_labels_test.tsv` rồi chạy lại trước khi đưa vào khóa luận.

- Gold: `data/norm_gold_v1/gold_test.jsonl` — đơn vị đánh giá là **dạng bề mặt duy nhất** (type-level); bảng mention-level trọng số theo tần suất trong split test.
- Thực thể lấy từ **nhãn gold NER** của split `test` VietMed-NER, nên lỗi NER không ảnh hưởng.
- Accuracy: quyết định duy nhất của hệ thống đúng; hệ thống từ chối (không trả mã) tính là sai.
- Hai chế độ: **thận trọng** (từ chối khi không chắc, ưu tiên precision) và **luôn trả lời** (lấy ứng viên top-1 khi không chắc; Accuracy = Top-1, nhưng mọi dạng NIL đều bị gán mã).
- Top-k Accuracy = Recall@k: mã đúng nằm trong k ứng viên đầu (mỗi đề cập có một khái niệm gold). Ứng viên: quyết định của hệ thống đứng đầu, sau đó ICD-10 theo TF-IDF n-gram ký tự, RxNorm theo RxNav approximateTerm.
- CI95: bootstrap 2000 lần theo dạng bề mặt.

## ICD-10 — mã đầy đủ

Linkable: 246 dạng (1148 đề cập); NIL: 66 dạng (319 đề cập).

| Phương pháp | Accuracy (type) | CI95 | Accuracy (mention) | Coverage | Precision khi trả lời | Từ chối đúng NIL |
|---|---:|---|---:|---:|---:|---:|
| Baseline: khớp chính xác tên danh mục | 0.069 | 0.040–0.102 | 0.092 | 0.069 | 1.000 | 0.985 |
| Baseline: fuzzy top-1 (WRatio, không ràng buộc) | 0.187 | 0.139–0.239 | 0.173 | 1.000 | 0.187 | 0.000 |
| Hệ thống – chế độ thận trọng (exact → synonym → fuzzy có ràng buộc) | 0.354 | 0.297–0.412 | 0.531 | 0.354 | 1.000 | 0.985 |
| Hệ thống – chế độ luôn trả lời (thận trọng, nếu không thì ứng viên TF-IDF top-1) | 0.520 | 0.457–0.582 | 0.622 | 1.000 | 0.520 | 0.000 |

| Xếp hạng ứng viên | Top-1 | Top-3 | Top-5 | Top-10 | MRR@10 |
|---|---:|---:|---:|---:|---:|
| Top-k Acc = Recall@k (type) | 0.520 | 0.622 | 0.634 | 0.691 | 0.573 |
| Top-k Acc = Recall@k (mention) | 0.622 | 0.713 | 0.716 | 0.737 | 0.666 |
| CI95 (type) | 0.457–0.582 | | 0.574–0.694 | 0.633–0.746 | |

## ICD-10 — nhóm 3 ký tự (category)

Linkable: 246 dạng (1148 đề cập); NIL: 66 dạng (319 đề cập).

| Phương pháp | Accuracy (type) | CI95 | Accuracy (mention) | Coverage | Precision khi trả lời | Từ chối đúng NIL |
|---|---:|---|---:|---:|---:|---:|
| Baseline: khớp chính xác tên danh mục | 0.069 | 0.040–0.102 | 0.092 | 0.069 | 1.000 | 0.985 |
| Baseline: fuzzy top-1 (WRatio, không ràng buộc) | 0.215 | 0.166–0.269 | 0.232 | 1.000 | 0.215 | 0.000 |
| Hệ thống – chế độ thận trọng (exact → synonym → fuzzy có ràng buộc) | 0.354 | 0.297–0.412 | 0.531 | 0.354 | 1.000 | 0.985 |
| Hệ thống – chế độ luôn trả lời (thận trọng, nếu không thì ứng viên TF-IDF top-1) | 0.573 | 0.512–0.637 | 0.709 | 1.000 | 0.573 | 0.000 |

| Xếp hạng ứng viên | Top-1 | Top-3 | Top-5 | Top-10 | MRR@10 |
|---|---:|---:|---:|---:|---:|
| Top-k Acc = Recall@k (type) | 0.573 | 0.687 | 0.720 | 0.768 | 0.637 |
| Top-k Acc = Recall@k (mention) | 0.709 | 0.769 | 0.777 | 0.792 | 0.740 |
| CI95 (type) | 0.512–0.637 | | 0.665–0.776 | 0.715–0.820 | |

## RxNorm — mã đầy đủ

Linkable: 47 dạng (305 đề cập); NIL: 81 dạng (422 đề cập).

| Phương pháp | Accuracy (type) | CI95 | Accuracy (mention) | Coverage | Precision khi trả lời | Từ chối đúng NIL |
|---|---:|---|---:|---:|---:|---:|
| Baseline: RxNav khớp tên chính xác | 0.404 | 0.273–0.550 | 0.498 | 0.426 | 0.950 | 1.000 |
| Baseline: RxNav approximateTerm top-1 | 0.468 | 0.326–0.609 | 0.462 | 0.979 | 0.478 | 0.160 |
| Hệ thống – chế độ thận trọng (exact → alias Việt→Anh → bỏ tiền tố → approx gần trùng) | 0.638 | 0.500–0.775 | 0.889 | 0.660 | 0.968 | 0.975 |
| Hệ thống – chế độ luôn trả lời (thận trọng, nếu không thì approximateTerm top-1) | 0.681 | 0.547–0.809 | 0.895 | 0.979 | 0.696 | 0.160 |

| Xếp hạng ứng viên | Top-1 | Top-3 | Top-5 | Top-10 | MRR@10 |
|---|---:|---:|---:|---:|---:|
| Top-k Acc = Recall@k (type) | 0.681 | 0.702 | 0.702 | 0.702 | 0.691 |
| Top-k Acc = Recall@k (mention) | 0.895 | 0.902 | 0.902 | 0.902 | 0.898 |
| CI95 (type) | 0.547–0.809 | | 0.571–0.826 | 0.571–0.826 | |

## Lỗi của hệ thống (trả mã sai, mã đầy đủ)

| Ontology | Dạng | Tần suất | Hệ thống | Gold |
|---|---|---:|---|---|
| RxNorm | protein | 4 | 8859 | NIL |
| RxNorm | carbonate | 2 | 1544139 | 1897 |
| ICD-10 | tiết sữa | 1 | O92.6 | NIL |
| RxNorm | gel | 1 | 4718 | NIL |

# Chuẩn hóa thực thể: trước và sau cải thiện trên dev

> Nhãn gold là nhãn AI tiền gán, **chưa có bác sĩ duyệt**. Số liệu là tạm thời.

Các thay đổi chỉ được chọn và kiểm tra trên **dev** (split `validation`). Test chỉ chạy một lần sau cùng.
Từ điển được xây từ các dạng có trong train/dev, nên số trên dev là lạc quan; **số cần báo cáo là số trên test**.

| Ontology | Split | Accuracy trước → sau | CI95 sau | Accuracy (mention) | Precision khi trả lời | Từ chối đúng NIL | Top-10 = Recall@10 | MRR@10 |
|---|---|---|---|---|---|---|---|---|
| ICD-10 | dev | 0.156 → **0.796** | 0.734–0.858 | 0.203 → 0.917 | 0.958 → 1.000 | 0.978 → 0.978 | 0.401 → 0.891 | 0.293 → 0.853 |
| ICD-10 | test | 0.187 → **0.354** | 0.297–0.412 | 0.176 → 0.531 | 0.939 → 1.000 | 0.985 → 0.985 | 0.386 → 0.691 | 0.299 → 0.573 |
| RxNorm | dev | 0.324 → **0.811** | 0.675–0.931 | 0.256 → 0.897 | 1.000 → 1.000 | 1.000 → 0.978 | 0.514 → 0.919 | 0.482 → 0.905 |
| RxNorm | test | 0.404 → **0.638** | 0.500–0.775 | 0.498 → 0.889 | 0.950 → 0.968 | 1.000 → 0.975 | 0.532 → 0.702 | 0.511 → 0.691 |

## Hai chế độ của hệ thống sau cải thiện

| Ontology | Split | Chế độ | Accuracy (type) | CI95 | Accuracy (mention) | Precision khi trả lời | Từ chối đúng NIL |
|---|---|---|---|---|---|---|---|
| ICD-10 | dev | thận trọng | 0.796 | 0.734–0.858 | 0.917 | 1.000 | 0.978 |
| ICD-10 | dev | luôn trả lời | 0.837 | 0.779–0.892 | 0.930 | 0.837 | 0.000 |
| ICD-10 | test | thận trọng | 0.354 | 0.297–0.412 | 0.531 | 1.000 | 0.985 |
| ICD-10 | test | luôn trả lời | 0.520 | 0.457–0.582 | 0.622 | 0.520 | 0.000 |
| RxNorm | dev | thận trọng | 0.811 | 0.675–0.931 | 0.897 | 1.000 | 0.978 |
| RxNorm | dev | luôn trả lời | 0.892 | 0.784–0.975 | 0.936 | 0.892 | 0.165 |
| RxNorm | test | thận trọng | 0.638 | 0.500–0.775 | 0.889 | 0.968 | 0.975 |
| RxNorm | test | luôn trả lời | 0.681 | 0.547–0.809 | 0.895 | 0.696 | 0.160 |

Chi tiết từng lần chạy (kèm baseline và Top-1/3/5): `dev_before/`, `dev_after/`, `test_before/`, `test_after/` → `summary.md`.

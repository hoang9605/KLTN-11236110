# Báo Cáo Đánh Giá Mô Hình Medical NER trên VietMed-NER

## 1. Thông Tin Tập Dữ Liệu & Phân Chia (Splits)

- **Tập dữ liệu**: `leduckhai/VietMed-NER` (Hugging Face Hub)
- **Các split tìm thấy**: `['train', 'validation', 'test']`
- **Split sử dụng đánh giá**: `test` (split chính thức của dataset)
- **Số câu đánh giá**: **3497** câu
- **Loại bỏ dữ liệu âm thanh**: Đã gỡ bỏ cột `audio` để tối ưu tải và tránh lỗi torchcodec.
- **Đảm bảo không data leakage**: Sử dụng split test độc lập, không trùng với tập train đã dùng huấn luyện.

## 2. Kết Quả Đánh Giá Tầng 1: Nhãn Gốc (37 Nhãn BIO — Raw Model)

> Đánh giá span-level chuẩn `seqeval` trực tiếp từ checkpoint model gốc, trước khi qua mapping và các rule hậu xử lý.

- **Thời gian chạy**: 330.79s (94.59 ms/câu)
- **Micro F1**: **0.6572** (P: 0.5996, R: 0.7269)
- **Macro F1**: **0.6246**
- **Weighted F1**: **0.6732**

### Top 5 Nhãn Yếu Nhất (Tầng 1 theo F1):

| Hạng | Thực Thể | Precision | Recall | F1-Score | Support |
|:---:|:---|:---:|:---:|:---:|:---:|
| 1 | `PREVENTIVEMED` | 0.0261 | 0.5556 | 0.0499 | 18 |
| 2 | `MEDDEVICETECHNIQUE` | 0.2699 | 0.2346 | 0.2511 | 635 |
| 3 | `PERSONALCARE` | 0.2027 | 0.7895 | 0.3226 | 95 |
| 4 | `SURGERY` | 0.4272 | 0.3297 | 0.3722 | 276 |
| 5 | `UNITCALIBRATOR` | 0.3361 | 0.6381 | 0.4403 | 257 |


## 3. Kết Quả Đánh Giá Tầng 2: Schema Mục Tiêu (6 Nhãn — Full Pipeline)

> Đánh giá qua toàn bộ pipeline hoàn chỉnh (`MedicalNERPipeline.predict`), bao gồm tiền xử lý, ViHealthBERT, dosage extractor, filter & overlap resolution, và 2 rule patch (`blacklist` + `merge sốt cao`).

- **Strict Exact Match (Khớp chính xác cả nhãn và tọa độ span)**:
  - Micro F1: **0.6223** (P: 0.5642, R: 0.6938)
  - Macro F1: **0.6106**
  - Weighted F1: **0.6208**
- **Relaxed Match (Khớp nhãn và có giao nhau / overlap về vị trí span)**:
  - Micro F1: **0.7536** (P: 0.6832, R: 0.8401)
  - Macro F1: **0.7304**

### Bảng Chi Tiết Hiệu Năng 6 Nhãn Mục Tiêu (Strict vs Relaxed):

| Nhãn Mục Tiêu | Strict P | Strict R | Strict F1 | Relaxed P | Relaxed R | Relaxed F1 | Support |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **CONDITION** | 0.6310 | 0.7192 | **0.6722** | 0.7871 | 0.8971 | **0.8385** | 1467 |
| **DRUG** | 0.5732 | 0.8996 | **0.7002** | 0.6065 | 0.9519 | **0.7409** | 727 |
| **BODY_PART** | 0.5642 | 0.7222 | **0.6335** | 0.6782 | 0.8683 | **0.7616** | 1260 |
| **TEST** | 0.6647 | 0.7692 | **0.7132** | 0.7399 | 0.8562 | **0.7938** | 299 |
| **PROCEDURE** | 0.5237 | 0.4926 | **0.5077** | 0.7088 | 0.6667 | **0.6871** | 1143 |
| **DOSAGE** | 0.3333 | 0.6342 | **0.4370** | 0.4274 | 0.8132 | **0.5603** | 257 |


### Thứ Tự Nhãn Cần Cải Thiện Trong 6 Nhãn Mục Tiêu (theo Strict F1):

1. **DOSAGE**: Strict F1 = `0.4370` (P=`0.3333`, R=`0.6342`, Support=257)
2. **PROCEDURE**: Strict F1 = `0.5077` (P=`0.5237`, R=`0.4926`, Support=1143)
3. **BODY_PART**: Strict F1 = `0.6335` (P=`0.5642`, R=`0.7222`, Support=1260)
4. **CONDITION**: Strict F1 = `0.6722` (P=`0.6310`, R=`0.7192`, Support=1467)
5. **DRUG**: Strict F1 = `0.7002` (P=`0.5732`, R=`0.8996`, Support=727)
6. **TEST**: Strict F1 = `0.7132` (P=`0.6647`, R=`0.7692`, Support=299)


## 4. Benchmark Thời Gian Xử Lý (Latency)

- **Tổng thời gian xử lý**: 419.71 giây (3497 câu)
- **Thời gian trung bình (Mean)**: **119.80 ms / câu**
- **Trung vị (Median / P50)**: 114.62 ms / câu
- **Phân vị 90 (P90)**: 155.55 ms / câu
- **Phân vị 95 (P95)**: **175.06 ms / câu**
- **Phân vị 99 (P99)**: 243.05 ms / câu
- **Min / Max**: 37.28 ms / 699.31 ms

## 5. Danh Mục Các Tệp Kết Quả Chi Tiết

| Tệp Tin | Định Dạng | Mô Tả |
|:---|:---:|:---|
| [`raw_37label_report.json`](raw_37label_report.json) | JSON | Báo cáo chi tiết metrics seqeval cho toàn bộ 37 nhãn BIO gốc |
| [`raw_37label_report.txt`](raw_37label_report.txt) | Text | Bảng in dễ đọc báo cáo Tầng 1 |
| [`schema_6label_report.json`](schema_6label_report.json) | JSON | Báo cáo chi tiết metrics Tầng 2 (cả Strict Match và Relaxed Match) |
| [`schema_6label_report.txt`](schema_6label_report.txt) | Text | Bảng in so sánh Strict Match và Relaxed Match theo 6 nhãn |
| [`confusion_matrix.png`](confusion_matrix.png) | Image | Heatmap ma trận nhầm lẫn giữa 6 nhãn mục tiêu và NONE |
| [`top_error_cases.json`](top_error_cases.json) | JSON | Danh sách 20 câu có nhiều lỗi nhất |
| [`latency_report.json`](latency_report.json) | JSON | Báo cáo chi tiết thời gian xử lý và các mức phân vị latency |

---
*Báo cáo được tạo tự động bởi `eval/run_eval.py`.*
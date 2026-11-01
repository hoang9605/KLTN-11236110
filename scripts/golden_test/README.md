# Tập golden test end-to-end NER → RE (v1)

Mục tiêu: ~150 đoạn từ **split test** VietMed-NER (NER chưa từng thấy), được người duyệt xác nhận cả thực thể lẫn quan hệ, để đo:

1. NER strict / relaxed trên 6 nhãn;
2. RE khi dùng thực thể gold (chất lượng riêng bộ phân loại quan hệ);
3. RE end-to-end: quan hệ chỉ được tính đúng khi NER tìm đúng cả hai thực thể (nhãn + span) **và** RE gán đúng quan hệ.

Mọi micro-F1 kèm khoảng tin cậy 95% (bootstrap theo đoạn).

## Quy trình (chạy trên Windows từ thư mục gốc repo)

```powershell
# 1. Chọn ứng viên (đọc cache HF đã tải lúc chạy eval; hoặc tải bằng `datasets`)
.venv\Scripts\python.exe -X utf8 scripts/golden_test/build_candidates.py

# 2. Tạo phiếu Excel: bản đầy đủ cho người duyệt A, 30 đoạn chồng lấp cho người duyệt B
.venv\Scripts\python.exe -X utf8 scripts/golden_test/make_workbook.py --annotator A
.venv\Scripts\python.exe -X utf8 scripts/golden_test/make_workbook.py --annotator B --only-double

# 3. Người duyệt điền cột nền vàng, lưu thành file mới (vd. phieu_duyet_A_da_duyet.xlsx)

# 4. Nhập kết quả -> gold.jsonl (+ kappa nếu có phiếu B)
.venv\Scripts\python.exe -X utf8 scripts/golden_test/import_workbook.py `
    --workbook data/golden_test/v1/phieu_duyet_A_da_duyet.xlsx --annotator A `
    --second data/golden_test/v1/phieu_duyet_B_double_da_duyet.xlsx --second-annotator B

#    Nếu sửa NER làm xuất hiện cặp mới: duyệt lượt 2
.venv\Scripts\python.exe -X utf8 scripts/golden_test/make_workbook.py --annotator A `
    --candidates data/golden_test/v1/round2_candidates.jsonl --out data/golden_test/v1/phieu_luot2.xlsx
.venv\Scripts\python.exe -X utf8 scripts/golden_test/import_workbook.py `
    --candidates data/golden_test/v1/round2_candidates.jsonl --workbook data/golden_test/v1/phieu_luot2_da_duyet.xlsx --annotator A

# 5. Đánh giá
.venv\Scripts\python.exe -X utf8 scripts/golden_test/evaluate_e2e.py `
    --gold data/golden_test/v1/gold.jsonl data/golden_test/v1/gold_round2_candidates.jsonl `
    --re-model outputs/re_ai_baseline/seed42/model.joblib
```

Kết quả ở `data/golden_test/v1/eval/`: `summary.md`, `report.json`, `predictions.jsonl`, `re_gold_entities_pairs.jsonl`.

## Thiết kế và lý do

| Quyết định | Lý do |
|---|---|
| Lấy từ split **test**, loại đoạn trùng nội dung với train | Tránh rò rỉ dữ liệu: 600 mẫu RE cũ thuộc train mà NER đã học |
| Lấy mẫu có chủ đích: mỗi quan hệ ≥ 25 đoạn chứa cặp đúng kiểu, ưu tiên has_dosage, diagnosed_by | Bộ 600 mẫu ngẫu nhiên có 0 mẫu dương cho hai quan hệ này |
| Thêm 15 đoạn có thực thể nhưng không có cặp, 10 đoạn không có thực thể | Đo dự đoán dương sai của hệ thống khi chạy thật |
| Bỏ đoạn > 10 cặp ứng viên | Giữ khối lượng duyệt vừa sức một bác sĩ |
| NER điền sẵn từ nhãn gốc dataset; **nhãn RE để trống** | NER gốc là nhãn người gán; RE không điền sẵn bằng AI để tránh thiên lệch người duyệt |
| 30 đoạn duyệt độc lập bởi người thứ hai | Báo cáo Cohen's kappa — bằng chứng độ tin cậy của gold |
| Cặp mới sinh ra sau khi sửa NER đưa vào lượt 2 | Không tự đoán nhãn cho cặp chưa ai xem |
| Text gold = các token nối bằng một dấu cách | Offset trùng với văn bản `MedicalNERPipeline` trả về |

## Khi viết vào khóa luận

- Ghi rõ: tập lấy mẫu có chủ đích, nên phân bố quan hệ không phản ánh phân bố tự nhiên.
- Ghi số đoạn, số thực thể, số cặp dương/âm/CHUA_RO thực tế sau duyệt (`import_report.json`) và kappa.
- Nếu thiếu đoạn cho một quan hệ, `manifest.json` → `quota_shortfall` ghi số thật; báo cáo đúng số đó.
- Mô hình RE hiện tại chưa học diagnosed_by / has_dosage nên sẽ có recall 0 ở hai quan hệ này; đó là kết quả cần báo cáo, không phải lỗi của bộ đánh giá.

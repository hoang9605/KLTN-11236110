# Tập gold chuẩn hóa thực thể (v1)

Tập này dùng để đo chất lượng bước **chuẩn hóa thực thể**: gán CONDITION vào ICD-10 (danh mục của Bộ Y tế) và DRUG vào RxNorm.
Các chỉ số được tính gồm Accuracy, Top-k Accuracy, Recall@k và MRR.

> **Trạng thái:** nhãn trong `ai_labels_test.tsv` và `ai_labels_dev.tsv` là **nhãn AI tiền gán, chưa có người duyệt** (`human_verified: false`).
> Cần bác sĩ duyệt `phieu_duyet_chuan_hoa_test.xlsx` (bắt buộc, vì đây là số báo cáo) và `phieu_duyet_chuan_hoa_dev.xlsx` trước khi đưa số liệu vào khóa luận.

## Dữ liệu

| Tệp | Nội dung |
|---|---|
| `candidates_test.jsonl` | 440 dạng thực thể duy nhất trong split `test` của VietMed-NER (312 CONDITION, 128 DRUG), kèm tần suất và ngữ cảnh |
| `candidates_dev.jsonl`, `ai_labels_dev.tsv`, `gold_dev.jsonl`, `phieu_duyet_chuan_hoa_dev.xlsx` | 321 dạng từ split `validation` (193 CONDITION, 128 DRUG). 110 dạng trùng với test dùng lại nhãn test cho nhất quán. **Mọi tinh chỉnh từ điển và luật chỉ được chọn trên tập này** |
| `ai_labels_test.tsv` | `id <TAB> mã1,mã2,… hoặc NIL <TAB> ghi chú`. Mã đầu tiên là mã chính, các mã còn lại cũng được tính đúng |
| `gold_test.jsonl` | Bản ghép giữa ứng viên và nhãn, là đầu vào của `evaluate.py` |
| `phieu_duyet_chuan_hoa_test.xlsx` | Phiếu duyệt cho bác sĩ, các cột cần điền tô nền vàng |
| `manifest.json` | Nguồn dữ liệu, số lượng và độ trùng dạng giữa dev và test (77 CONDITION, 33 DRUG) |

## Thiết kế

- **Thực thể lấy từ nhãn gold NER**, không lấy từ đầu ra của mô hình. Nhờ vậy bước chuẩn hóa được đo độc lập với lỗi NER.
- **Đơn vị đánh giá là dạng bề mặt duy nhất** (type-level), là số chính. Kết quả theo mention, trọng số theo tần suất, được báo cáo kèm để thấy tác động thực tế.
- Nhãn **NIL** dùng cho các trường hợp không có khái niệm phù hợp trong ontology: từ chung chung ("triệu chứng", "thuốc"), nhóm thuốc ("thuốc tránh thai"), thứ không phải bệnh hay thuốc ("sữa mẹ", "di truyền"), và mảnh lỗi NER ("bị tiêu").
  Trên các dạng NIL, hệ thống được chấm theo tỉ lệ **từ chối đúng**.
- ICD-10 được chấm ở hai mức: mã đầy đủ và nhóm 3 ký tự. RxNorm ưu tiên mức hoạt chất (TTY=IN).
- Split `test` chỉ dùng để báo cáo. Mọi chỉnh sửa luật hay từ điển phải làm trên `dev`.

## Quy trình

```powershell
# 1. Tạo ứng viên (đã chạy)
.venv\Scripts\python.exe -X utf8 scripts/normalization_eval/build_candidates.py
# 2. Ghép nhãn -> gold
.venv\Scripts\python.exe -X utf8 scripts/normalization_eval/merge_labels.py `
    --candidates data/norm_gold_v1/candidates_test.jsonl --labels data/norm_gold_v1/ai_labels_test.tsv `
    --annotator "AI (Claude Opus 5.5)" --out data/norm_gold_v1/gold_test.jsonl
# 3. Bác sĩ duyệt phiếu, lưu thành ..._da_duyet.xlsx, rồi nhập lại
.venv\Scripts\python.exe -X utf8 scripts/normalization_eval/review_sheet.py import `
    --workbook data/norm_gold_v1/phieu_duyet_chuan_hoa_test_da_duyet.xlsx --out data/norm_gold_v1/reviewed_labels_test.tsv
.venv\Scripts\python.exe -X utf8 scripts/normalization_eval/merge_labels.py `
    --candidates data/norm_gold_v1/candidates_test.jsonl --labels data/norm_gold_v1/reviewed_labels_test.tsv `
    --annotator "<Tên bác sĩ>" --human-verified --out data/norm_gold_v1/gold_test.jsonl
# 4. Đánh giá (RxNorm cần mạng ở lần chạy đầu; sau đó dùng cache SQLite)
.venv\Scripts\python.exe -X utf8 scripts/normalization_eval/evaluate.py `
    --gold data/norm_gold_v1/gold_test.jsonl --out eval/normalization_<ngày>
```

## Cải thiện ngày 2026-11-07 (chọn trên dev, đo test một lần)

Kết quả: `eval/normalization_2026-11-07/comparison.md`.

- **RxNorm:**
  - Thêm từ điển Việt → Anh `normalization/data/rxnorm_vi_aliases.json` (31 mục, chỉ lấy dạng có trong train/dev; mỗi giá trị đã được kiểm tra là RxNav tra chính xác được).
  - Bỏ từ đứng đầu chỉ dạng bào chế ("viên nang", "thuốc", "vị"…).
  - Chấp nhận kết quả approximateTerm top-1 chỉ khi tên gần như trùng (ratio ≥ 90), để bắt lỗi chính tả.
- **ICD-10:**
  - Thêm 137 từ đồng nghĩa dân gian vào `icd10_synonyms.json` (chỉ lấy dạng có trong train/dev; 48 dạng cũng có trong test vì chúng xuất hiện ở cả hai nơi).
  - Thêm ràng buộc fuzzy: mọi từ nội dung của ứng viên phải có trong câu hỏi (so sánh bỏ dấu, ratio ≥ 80). Ràng buộc này xuất phát từ lỗi trên dev: "rối loạn vận động" bị gán F44.4.
  - Danh sách top-k chuyển sang TF-IDF n-gram ký tự 2–4, có đưa từ đồng nghĩa vào chỉ mục. Cách này được chọn vì trên dev tốt hơn WRatio, token_set_ratio và n-gram từ.
- **Không làm:**
  - Không thêm mục nào chỉ xuất hiện trong test. Ví dụ: magie, phốtpho, bạch phục linh, hoàng bá, u xơ tử cung.
  - Không sửa riêng các lỗi chỉ thấy trên test. Ba lỗi gán sai ICD-10 ở test ("u xơ tử cung", "gãy xương khớp háng", "viêm thần kinh tọa") hết nhờ ràng buộc chung ở trên.

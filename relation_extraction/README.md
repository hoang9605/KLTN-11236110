# RE thử nghiệm bằng dữ liệu AI

Mô-đun đã huấn luyện bằng nhãn AI trong `annotations_reviewed_600.jsonl` ngày 15/10/2026, theo lựa chọn của người dùng. Mô hình hiện tại là **TF-IDF ký tự + Logistic Regression**, chưa phải ViHealthBERT fine-tune cho RE. Checkpoint NER giữ nguyên.

## Chạy trên Windows PowerShell

Chạy từ thư mục gốc repository, dùng môi trường `.venv` hiện có với scikit-learn, numpy, joblib (đã có trong môi trường). Chế độ `--text` còn cần các thư viện NER trong `requirements.txt` và checkpoint NER tại `Model/vihealthbert-ner-vietmed-v2-final`.

Huấn luyện lại; dùng một thư mục output mới cho mỗi lần chạy:

```powershell
.venv\Scripts\python.exe -X utf8 -m relation_extraction train --data outputs/vietmed_600_RE_review/review_2026_10_15/annotations_reviewed_600.jsonl --output outputs/re_ai_baseline/my_run --allow-ai-labels --seed 42
```

Không truyền `--allow-ai-labels` sẽ từ chối bản nhãn chưa xác minh. Lựa chọn này cho phép thử nghiệm, không sửa `human_verified` hoặc `training_eligible` trong nguồn.

Chạy văn bản qua NER rồi RE:

```powershell
.venv\Scripts\python.exe -X utf8 -m relation_extraction predict --model outputs/re_ai_baseline/seed42/model.joblib --text "Bệnh nhân đau ở vùng bụng, được điều trị bằng phẫu thuật." --output outputs/re_ai_baseline/demo.json
```

Hoặc dùng JSON chứa `text` và `entities` có sẵn:

```powershell
.venv\Scripts\python.exe -X utf8 -m relation_extraction predict --model outputs/re_ai_baseline/seed42/model.joblib --input my_entities.json
```

Chấp nhận thực thể theo định dạng annotation (`id`, `label`, `start`, `end`, `text`) hoặc NER (`label`, `start_char`, `end_char`, `surface_text`). Offset là vị trí ký tự, end không bao gồm ký tự cuối. Văn bản phải khớp offset. Với NER, dùng chính `text` đã chuẩn hóa mà NER trả về.

API Python:

```python
from relation_extraction.model import RelationExtractor
from relation_extraction.pipeline import MedicalREPipeline

extractor = RelationExtractor.load("outputs/re_ai_baseline/seed42/model.joblib")
pipeline = MedicalREPipeline(extractor)  # Khởi tạo NER khi gọi predict lần đầu
result = pipeline.predict("Bệnh nhân đau ở vùng bụng.")
# Nếu đã có NER result:
# result = pipeline.from_ner_result(ner_result)
```

`relations` chứa cạnh dương; `relation_candidates` chứa cả âm và cặp không hỗ trợ. Head/tail tham chiếu ID trong `entities`. Với `diagnosed_by` và `has_dosage`, trả `label=null`, `status=unsupported`; không coi chúng là âm đã học. `score` là xác suất dương sau khi chuẩn hóa giữa nhãn hợp lệ và NO_RELATION; đây không phải xác suất y khoa được hiệu chỉnh. RE nhận các cặp cùng phát ngôn ngắn; không tự tách văn bản nhiều câu, giải quyết đồng tham chiếu hoặc nối các đoạn nguồn.

Chỉ nạp checkpoint joblib do bạn tạo hoặc tin cậy, vì định dạng này sử dụng pickle.

## Dữ liệu và kết quả seed 42

- 600 câu nguồn; 82 câu có ít nhất một cặp rõ nhãn.
- 178 cặp dùng: 137 âm, 20 located_at, 19 treated_by_procedure, 2 treated_by.
- Loại 62 CHUA_RO; không sinh mẫu âm từ quan hệ vắng mặt.
- 111/178 cặp nằm trong câu còn cờ cần duyệt. Giữ các cờ trong các file split.
- Chia nhóm theo hash văn bản NFC, chữ thường và khoảng trắng chuẩn hóa. Dành một nhóm cho mỗi nhãn vào train, sau đó phân bổ theo seed. Không chia từng cặp độc lập.
- Train: 58 nhóm / 137 cặp. Dev: 12 nhóm / 27 cặp. Test: 12 nhóm / 14 cặp.
- Không tinh chỉnh mô hình/ngưỡng theo dev hoặc test trong lần chạy này.

| Tập | Positive precision | Positive recall | Positive micro-F1 | Số quan hệ dương |
|---|---:|---:|---:|---:|
| Dev | 0,667 | 0,333 | 0,444 | 6 |
| Test | 0,750 | 0,600 | 0,667 | 5 |

Đây là phép đo **mức khớp nhãn AI với thực thể AI cung cấp**, không phải đánh giá gold hay end-to-end NER → RE. Không chốt thay quy trình đánh giá khóa luận. Hai mẫu treated_by đều ở train; chưa đánh giá được khả năng tổng quát của lớp này. Hai lớp còn lại không có positive trong nguồn. Macro-F1 trên đủ năm lớp trong JSON quy ước lớp không support bằng 0; phải đọc kèm support, không diễn giải thành đánh giá đủ năm lớp.

Nguồn là train VietMed-NER, có thể đã được NER học. Chia theo văn bản không chứng minh độc lập người nói/cuộc hội thoại khi metadata này không có. Không dùng số trên làm kết quả kiểm thử độc lập toàn hệ thống. Cần thêm nhãn để mở rộng phạm vi và đánh giá chắc chắn hơn.

## Tệp kết quả

Trong `outputs/re_ai_baseline/seed42/`:

- `model.joblib`: mô hình, vectorizer và metadata nguồn.
- `train.jsonl`, `dev.jsonl`, `test.jsonl`: cặp, ID nguồn, offset, cờ duyệt và nhóm chia.
- `report.json`: SHA-256 nguồn/schema, cấu hình, phiên bản, phân bố, metric và giới hạn.
- `dev_predictions.jsonl`, `test_predictions.jsonl`: dự đoán từng cặp để phân tích lỗi.
- `demo_ner_re.json`: lượt chạy thật NER → RE. Mô hình phát hiện hai cạnh treated_by_procedure trong câu minh họa nhưng bỏ sót located_at giữa “đau” và “vùng bụng”; demo chứng minh tích hợp chạy được, không chứng minh dự đoán hoàn hảo.

Kiểm thử:

```powershell
.venv\Scripts\python.exe -X utf8 -m pytest tests/test_relation_extraction.py -q
```

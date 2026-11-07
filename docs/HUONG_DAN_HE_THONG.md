# Hướng dẫn và giải thích hệ thống trích xuất thông tin y tế tiếng Việt

*Cập nhật 07/11/2026. Mọi con số trong tài liệu lấy từ các file kết quả trong repo; đường dẫn ghi ngay cạnh từng số.*

> **Đọc trước khi dùng số liệu:**
> - Nhãn gold của phần **chuẩn hóa**, nhãn huấn luyện **RE v2** và nhãn của **golden test RE** đều do AI gán, **chưa có bác sĩ duyệt**.
> - Số liệu NER không bị ảnh hưởng, vì dùng nhãn gốc của bộ dữ liệu VietMed-NER.
> - Trước khi nộp, cần nhờ bác sĩ duyệt các phiếu ở mục 8, rồi chạy lại đánh giá.

---

## 1. Hệ thống làm gì?

Hệ thống đọc một đoạn văn bản y tế tiếng Việt và trả về:
- **thông tin có cấu trúc:** bệnh, thuốc, bộ phận cơ thể, xét nghiệm, thủ thuật, liều;
- **mã chuẩn quốc tế:** ICD-10 cho bệnh, RxNorm cho thuốc;
- **quan hệ** giữa các thực thể;
- **đồ thị tri thức** gộp lại từ toàn bộ kho văn bản.

```
Văn bản y tế tiếng Việt
        │
        ▼
Tiền xử lý (chuẩn hóa khoảng trắng, tách từ, chia đoạn dài)      ner/
        │
        ▼
NER – ViHealthBERT fine-tune → 6 loại thực thể                    ner/
        │   (+ luật bổ sung nhận diện liều: "500mg", "2 viên/ngày")
        ▼
Chuẩn hóa thực thể → ICD-10 (CONDITION), RxNorm (DRUG)            normalization/
        │   (mỗi thực thể kèm top-5 mã gợi ý)
        ▼
Relation Extraction – mô hình học + luật (union)                   relation_extraction/, knowledge_graph/extract.py
        │
        ▼
Knowledge Graph – gộp nút theo mã chuẩn, cộng dồn cạnh             knowledge_graph/
        │
        ▼
Đầu ra: JSON, CSV, GraphML, trang HTML tương tác                   outputs/kg_test_2026-11-07/
```

Ví dụ với câu *"Bệnh nhân tăng huyết áp, kê Aspirin 81mg mỗi ngày."*:

| Bước | Kết quả |
|---|---|
| NER | `tăng huyết áp` (CONDITION), `Aspirin` (DRUG), `81mg` (DOSAGE) |
| Chuẩn hóa | `tăng huyết áp` → **ICD-10 I10**; `Aspirin` → **RxNorm 1191** |
| RE | `tăng huyết áp —treated_by→ Aspirin`, `Aspirin —has_dosage→ 81mg` |
| Knowledge Graph | nút `ICD-10:I10` nối tới nút `RxNorm:1191` |

---

## 2. Có train / validation / test không?

**Có.** Mỗi bước được tách dữ liệu riêng, và tập test **không bao giờ** được dùng để chỉnh hệ thống.

| Bước | Train (học / xây dựng) | Validation / dev (tinh chỉnh) | Test (chỉ báo cáo) |
|---|---|---|---|
| **NER** | split `train` của VietMed-NER | split `validation` | split `test`, **3.497 câu** |
| **Chuẩn hóa** | không học (luật + từ điển); từ điển chỉ lấy từ dạng có trong train/dev | 321 dạng thực thể của split `validation` | **440 dạng** của split `test` (312 bệnh, 128 thuốc) |
| **RE** | 600 câu gold v1 + 199 câu AI v2, đều thuộc split `train` | CV 5-fold theo nhóm văn bản (dùng để chọn phương pháp) | **golden test**: 150 đoạn từ split `test`, 121 cặp được chấm |

Đã kiểm tra bằng code: dữ liệu huấn luyện RE và golden test **trùng 0 câu**; RE v1 và v2 cũng trùng 0 câu (`outputs/re_ai_v2/report.json`).

---

## 3. Các chỉ số đánh giá: đọc thế nào?

| Chỉ số | Ý nghĩa | Dùng cho |
|---|---|---|
| **Precision (P)** | Trong những gì hệ thống tìm ra, bao nhiêu phần trăm đúng | NER, RE |
| **Recall (R)** | Trong những gì đúng ra phải tìm, hệ thống tìm được bao nhiêu phần trăm | NER, RE |
| **F1** | Trung bình điều hòa của P và R; cao chỉ khi cả hai cùng cao | NER, RE |
| **Strict / Relaxed** | Strict: thực thể phải đúng nhãn và đúng từng ký tự ranh giới. Relaxed: đúng nhãn và có giao nhau về vị trí | NER |
| **Accuracy** | Tỉ lệ thực thể được gán đúng mã. Hệ thống "không trả lời" bị tính là sai | Chuẩn hóa |
| **Top-k Accuracy** | Mã đúng có nằm trong k gợi ý đầu không | Chuẩn hóa |
| **Recall@k** | Ở đây **bằng Top-k Accuracy**, vì mỗi thực thể chỉ có một khái niệm đúng | Chuẩn hóa |
| **MRR** | Mã đúng trung bình đứng ở hạng mấy (1 = luôn đứng đầu) | Chuẩn hóa |
| **CI95** | Khoảng tin cậy 95%, tính bằng bootstrap. Khoảng càng rộng thì số càng ít chắc chắn, thường do ít dữ liệu | tất cả |
| **Type / mention** | Type: mỗi dạng chữ tính một lần. Mention: tính theo số lần xuất hiện ("loãng xương" 115 lần nặng gấp 115 lần) | Chuẩn hóa |
| **NIL** | Thực thể không có mã phù hợp (ví dụ "triệu chứng", "thuốc"). Hệ thống tốt nên **từ chối** những thực thể này | Chuẩn hóa |

---

## 4. Kết quả từng bước (trên tập test)

### 4.1. NER — `eval/results_2026-11-05/summary.md`

| Thiết lập | P | R | F1 |
|---|---:|---:|---:|
| Mô hình gốc, 37 nhãn BIO (micro) | 0.600 | 0.727 | **0.657** |
| Toàn pipeline, 6 nhãn, strict | 0.564 | 0.694 | **0.622** |
| Toàn pipeline, 6 nhãn, relaxed | 0.683 | 0.840 | **0.754** |

Nhãn yếu nhất là DOSAGE (strict F1 0.437) và PROCEDURE (0.508). Kết quả ablation (bỏ luật, bỏ nhận diện liều) nằm ở `eval/ablation_2026-11-06/summary.json`.

### 4.2. Chuẩn hóa — `eval/normalization_2026-11-07/comparison.md`

Hệ thống có **hai chế độ**:
- **Thận trọng** (mặc định): không chắc thì không trả mã, ưu tiên không gán nhầm.
- **Luôn trả lời**: không chắc thì lấy gợi ý top-1.

| | ICD-10 | RxNorm |
|---|---:|---:|
| Baseline khớp chính xác: Accuracy | 0.069 | 0.404 |
| Baseline fuzzy top-1: Accuracy | 0.187 | 0.468 |
| **Thận trọng: Accuracy (type)** | **0.354** (CI95 0.30–0.41) | **0.638** (0.50–0.78) |
| Thận trọng: Accuracy (mention) | 0.531 | 0.889 |
| Thận trọng: Precision khi trả mã | **1.000** | 0.968 |
| **Luôn trả lời: Accuracy (type)** | **0.520** | **0.681** |
| Top-1 / Top-5 / Top-10 (= Recall@k) | 0.520 / 0.634 / 0.691 | 0.681 / 0.702 / 0.702 |

**Vì sao ICD-10 còn thấp:**
- Gần 2/3 dạng bệnh trong test là từ ngữ đời thường chưa từng gặp, ví dụ "rong kinh", "khiếm thính", "cong chân".
- Danh mục Bộ Y tế lại dùng tên chính thức: "Kinh nguyệt nhiều…", "Nghe kém…".
- Dạng đã gặp trong train/dev đúng **84%**; dạng mới chỉ đúng **7%**.
- Ở chế độ thận trọng, hệ thống **không gán sai mã nào**: mọi lỗi đều là từ chối.

### 4.3. Relation Extraction — `outputs/re_ai_v2/summary.md`

| Phương pháp | CV 5-fold F1 (556 cặp) | Golden test P / R / F1 (121 cặp) |
|---|---:|---|
| Luật (viết từ hướng dẫn, không học) | 0.400 | 0.706 / 0.261 / 0.381 |
| Mô hình cũ (chỉ học gold v1) | 0.289 | 0.360 / 0.196 / 0.254 |
| Mô hình mới (học gold v1 + AI v2) | 0.400 | 0.429 / 0.326 / 0.370 |
| **Union: mô hình mới + luật** (chọn theo CV) | **0.482** | **0.468 / 0.478 / 0.473** (CI95 0.33–0.58) |

So với mô hình cũ, F1 trên golden test tăng từ **0.254 lên 0.473**. Quan hệ `has_dosage` vẫn yếu (F1 0.18), vì dữ liệu huấn luyện gần như không có liều thật (xem mục 5).

### 4.4. Knowledge Graph — `outputs/kg_test_2026-11-07/stats.md`

Chạy trên toàn bộ 3.496 câu (đã bỏ câu trùng) của split test, dùng thực thể do mô hình NER tìm ra, đúng như khi hệ thống chạy thật:
- **1.337 nút**, trong đó 108 có mã ICD-10/RxNorm;
- **293 cạnh** khác nhau, tổng cộng 391 lần xuất hiện.

| Quan hệ | Cạnh khác nhau | Lần xuất hiện |
|---|---:|---:|
| located_at (vị trí) | 246 | 341 |
| treated_by_procedure | 21 | 24 |
| treated_by | 16 | 16 |
| has_dosage | 7 | 7 |
| diagnosed_by | 3 | 3 |

Mở `outputs/kg_test_2026-11-07/kg.html` bằng trình duyệt để xem đồ thị: lọc theo quan hệ, tìm khái niệm, bấm vào nút để xem mã chuẩn và câu nguồn.

---

## 5. Bộ dữ liệu RE v2: cách tạo và cách kiểm tra

Thư mục `data/re_ai_v2/`, script `scripts/re_dataset/`.

1. **Chọn câu** (`build_candidates.py`):
   - Chỉ lấy split `train` của VietMed-NER; loại 600 câu đã có trong gold v1 và mọi câu trùng split test.
   - Thực thể lấy từ nhãn gold NER, bỏ thực thể chung chung ("thuốc", "điều trị"…) như pipeline làm.
   - Lấy mẫu theo từng loại quan hệ, ưu tiên loại hiếm: 172 câu.
   - Thêm **27 câu chọn có chủ đích**: câu có liều thật (chứa số hoặc đơn vị) hoặc có từ gợi ý điều trị. Lý do: lấy mẫu ngẫu nhiên gần như không ra mẫu dương cho `has_dosage` và `treated_by`.
2. **Gán nhãn lượt 1:** đọc từng câu, gán từng cặp theo `docs/RE_LABELS.md`:
   - `1` khi văn bản nói rõ quan hệ giữa **chính hai thực thể đó**;
   - `0` khi không có quan hệ;
   - `?` khi không rõ (bị loại khỏi huấn luyện).
   - Quy ước thêm, thống nhất với gold v1:
     - phòng bệnh không tính là điều trị (vắc xin cho covid → 0);
     - tác dụng phụ hoặc biến chứng do thuốc là nguyên nhân, không phải điều trị (→ 0);
     - thực phẩm chức năng và đông y → `?`;
     - đầu quan hệ chung chung ("triệu chứng", "bị bệnh") → `?`;
     - "cơ thể" không tính là một bộ phận cụ thể.
3. **Kiểm tra lượt 2:**
   - Script `merge_labels.py` kiểm tra mỗi câu được gán đúng một lần và số nhãn khớp số cặp.
   - Đối chiếu với baseline luật: rà lại từng câu trong **45 cặp bất đồng**, và giữ nguyên tất cả.
     - Luật bỏ sót phần lớn quan hệ vì văn nói không có từ gợi ý như "ở", "bằng".
     - Các cặp luật cho là dương mà nhãn là 0 đều có một đầu là thực thể rác do NER, ví dụ "cao", "kiểm soát", "nghiên cứu".
   - Kiểm tra các cặp thực thể giống nhau nhưng nhãn khác nhau giữa các câu: 7 trường hợp, đều do ngữ cảnh khác nhau. Ví dụ "chống viêm corticoid" là tên nhóm thuốc, còn "viêm phổi … corticoid" là điều trị thật.
   - Đọc lại toàn bộ **39 nhãn dương**, kèm ngữ cảnh.
4. **Kết quả:** 199 câu, 440 cặp. Bỏ 46 cặp `?`, còn 394 cặp dùng được:

   | Nhãn | Số cặp |
   |---|---:|
   | NO_RELATION | 355 |
   | located_at | 14 |
   | treated_by_procedure | 11 |
   | treated_by | 9 |
   | diagnosed_by | 5 |
   | has_dosage | **0** |

**Phát hiện quan trọng nên đưa vào khóa luận:** VietMed là lời nói từ podcast y tế. Thực thể DOSAGE trong nhãn gốc phần lớn là các từ như "cao", "rất nhiều", và quan hệ bệnh → thuốc rất hiếm. Đây là giới hạn của bộ dữ liệu, không phải lỗi của mô hình.

---

## 6. Cách chạy

Chạy từ thư mục gốc repo, trên Windows PowerShell:

```powershell
# Demo đầu–cuối trên vài câu mẫu
.venv\Scripts\python.exe -X utf8 scripts/demo_e2e.py

# Đánh giá NER trên split test
.venv\Scripts\python.exe -X utf8 -m eval.run_eval

# Đánh giá chuẩn hóa (gold test → kết quả)
.venv\Scripts\python.exe -X utf8 scripts/normalization_eval/evaluate.py --gold data/norm_gold_v1/gold_test.jsonl --out eval/normalization_<ngày>/test_after

# Huấn luyện và đánh giá RE (gold v1 + AI v2)
.venv\Scripts\python.exe -X utf8 scripts/re_dataset/train_eval.py --out outputs/re_ai_v2_<lần chạy>

# Dựng knowledge graph trên split test (chạy NER: vài chục phút)
.venv\Scripts\python.exe -X utf8 scripts/build_kg.py --split test --out outputs/kg_<tên>
# Đổi mô hình RE mà không chạy lại NER
.venv\Scripts\python.exe -X utf8 scripts/build_kg.py --from-results outputs/kg_test_2026-11-07/ner_results_re_v1.jsonl --rerun-re --out outputs/kg_<tên>

# Toàn bộ unit test (89 test)
.venv\Scripts\python.exe -X utf8 -m pytest tests -q
```

Dùng trong code Python:

```python
from ner.pipeline import MedicalNERPipeline
from relation_extraction.model import RelationExtractor
from relation_extraction.pipeline import MedicalREPipeline
from knowledge_graph import HybridRelationExtractor, KnowledgeGraph

re_pipe = MedicalREPipeline(HybridRelationExtractor(RelationExtractor.load("outputs/re_ai_v2/model.joblib")),
                            ner=MedicalNERPipeline(enable_normalization=True))
result = re_pipe.predict("Bệnh nhân tăng huyết áp, kê Aspirin 81mg mỗi ngày.", normalize=True)
# result["entities"][i]["normalized"]  -> mã quyết định (hoặc None)
# result["entities"][i]["candidates"]  -> top-5 mã gợi ý
# result["relations"]                  -> các quan hệ, kèm "source": "model" / "rule"
kg = KnowledgeGraph(); kg.add_document(result); kg.save("outputs/kg_demo")
```

---

## 7. Bản đồ thư mục

| Thư mục / file | Nội dung |
|---|---|
| `ner/`, `Model/` | Pipeline NER và checkpoint ViHealthBERT (trọng số tải riêng, xem `Model/README.md`) |
| `normalization/` | Chuẩn hóa ICD-10 (`icd10.py`), RxNorm (`rxnorm.py`), điều phối và top-k (`dispatcher.py`) |
| `normalization/data/icd10_synonyms.json` | 170 từ đồng nghĩa ICD-10 |
| `normalization/data/rxnorm_vi_aliases.json` | 31 tên thuốc Việt → Anh |
| `relation_extraction/` | Mô hình RE (TF-IDF + Logistic Regression), luật baseline, dữ liệu |
| `knowledge_graph/` | Bộ trích quan hệ union, dựng đồ thị, vẽ HTML (có `README.md` riêng) |
| `data/norm_gold_v1/` | Gold chuẩn hóa (dev + test) và phiếu duyệt Excel |
| `data/re_gold_v1/` | Gold RE v1 (600 câu, đã duyệt trên giấy) |
| `data/re_ai_v2/` | Dữ liệu RE v2: ứng viên, nhãn gọn, file annotation |
| `data/golden_test/v1/` | Golden test đầu–cuối (150 đoạn từ split test) |
| `eval/` | Kết quả đánh giá NER và chuẩn hóa |
| `outputs/re_ai_v2/` | Mô hình RE mới, báo cáo so sánh, dự đoán trên golden test |
| `outputs/kg_test_2026-11-07/` | Knowledge graph trên split test |
| `scripts/` | Script tạo dữ liệu, đánh giá, dựng KG |

---

## 8. Việc cần làm trước khi nộp

1. **Nhờ bác sĩ duyệt:**
   - `data/norm_gold_v1/phieu_duyet_chuan_hoa_test.xlsx` (bắt buộc) và `phieu_duyet_chuan_hoa_dev.xlsx`. Nhập lại bằng `review_sheet.py import`, xem `data/norm_gold_v1/README.md`.
   - Nhãn RE v2: `data/re_ai_v2/labels_main.txt`, `labels_targeted.txt`. Nếu bác sĩ sửa, chạy lại `merge_labels.py` rồi `train_eval.py`.
   - Golden test RE: `data/golden_test/v1/phieu_duyet_A_AI_de_xuat.xlsx`.
2. **Điền tên người duyệt** cho gold v1: `data/re_gold_v1/manifest.json` hiện ghi `CHUA_GHI_TEN`.
3. **Chạy lại đánh giá** sau khi có nhãn đã duyệt, rồi thay số vào báo cáo.
4. Viết rõ trong khóa luận phần nào dùng nhãn AI.

## 9. Nói gì với hội đồng về hạn chế

- **Nhãn:** phần chuẩn hóa và RE đánh giá trên nhãn AI. Đây là số tạm thời cho tới khi có chuyên gia duyệt. Đã tách train/dev/test và kiểm tra không trùng văn bản.
- **Dữ liệu:** VietMed là văn nói, nên quan hệ thuốc–liều và bệnh–thuốc hiếm. Tập RE nhỏ (556 cặp huấn luyện), nên khoảng tin cậy rộng (CI95 F1 0.33–0.58).
- **Chuẩn hóa:** bị giới hạn bởi khoảng cách giữa từ ngữ đời thường và thuật ngữ chuẩn. Hướng phát triển là tìm kiếm ngữ nghĩa bằng embedding và từ điển đồng nghĩa lớn hơn.
- **Knowledge Graph:**
  - Cạnh kế thừa lỗi của NER và RE. Ví dụ có cạnh sai "mất răng → vị trí → xương" do mô hình RE gán nhầm, và có nút là mảnh lỗi NER như "mất", "tiêu".
  - Chỉ 108/1.337 nút có mã chuẩn, vì nhiều thực thể là bộ phận cơ thể hay thủ thuật (chưa có ontology) hoặc chưa chuẩn hóa được.
- **Phạm vi:** RE chỉ xét cặp trong cùng một câu; không xử lý đồng tham chiếu; chưa có ontology cho BODY_PART, TEST, PROCEDURE.

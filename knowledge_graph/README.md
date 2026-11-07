# Knowledge Graph (đồ thị tri thức)

Bước cuối của pipeline: **văn bản → NER → chuẩn hóa ICD-10/RxNorm → RE → đồ thị**.

- **Nút** là khái niệm y tế.
  - Nếu chuẩn hóa đã có quyết định, các nút gộp theo **mã chuẩn**: "tiểu đường" và "đái tháo đường" thành một nút `ICD-10:E14`.
  - Nếu chưa, gộp theo loại thực thể cộng chữ đã chuẩn hóa: `CONDITION:rong kinh`. Nút loại này kèm mã gợi ý top-1.
- **Cạnh** là bộ ba `(đầu, quan hệ, cuối)`, cộng dồn qua mọi câu. Mỗi cạnh lưu số lần xuất hiện, nguồn (`model` hoặc `rule`), điểm trung bình và tối đa 3 câu nguồn.
- **Bỏ qua** các thực thể chung chung mà RE đã loại ("thuốc", "điều trị"…) và các CONDITION chung chung ("bị bệnh", "triệu chứng", "biến chứng"…; danh sách lấy từ train).

## Quan hệ: mô hình + luật

Mô hình RE (`outputs/re_gold_v1_baseline/seed42/model.joblib`, nhãn đã có người duyệt) chỉ hỗ trợ `located_at`, `treated_by_procedure` và `diagnosed_by`.
Hai quan hệ `treated_by` (bệnh → thuốc) và `has_dosage` (thuốc → liều) gần như không có mẫu huấn luyện, nên `HybridRelationExtractor` dùng **baseline luật** trong `relation_extraction/rules.py` cho hai quan hệ này. Baseline luật được viết từ hướng dẫn gán nhãn, không tinh chỉnh trên dữ liệu.
Trên đồ thị HTML, cạnh chỉ do luật sinh ra được vẽ nét đứt.

## Chạy

```powershell
# Toàn bộ split test VietMed-NER, thực thể từ mô hình NER (giống hệ thống thật)
.venv\Scripts\python.exe -X utf8 scripts/build_kg.py --split test --out outputs/kg_test_2026-11-07
# Dựng lại từ kết quả đã lưu (không chạy lại mô hình)
.venv\Scripts\python.exe -X utf8 scripts/build_kg.py --from-results outputs/kg_test_2026-11-07/results.jsonl --out outputs/kg_test_2026-11-07
# Văn bản tự do, mỗi dòng một đoạn
.venv\Scripts\python.exe -X utf8 scripts/build_kg.py --texts my_notes.txt --out outputs/kg_my_notes
```

Đầu ra: `kg.html` (mở bằng trình duyệt), `kg.json`, `triples.csv`, `nodes.csv`, `kg.graphml` (mở được bằng Gephi hoặc Cytoscape), `stats.md` và `results.jsonl`.

API Python:

```python
from knowledge_graph import KnowledgeGraph
kg = KnowledgeGraph()
kg.add_document(re_result)            # kết quả của MedicalREPipeline.predict(...)
kg.neighbors("ICD-10:M81.9")          # các cạnh nối với loãng xương
kg.find("tiểu đường")                 # tìm nút theo tên, mã hoặc cách viết
kg.save("outputs/kg"); kg.stats()
```

## Hạn chế

- Chất lượng cạnh phụ thuộc vào RE. Mô hình có F1 khoảng 0,5; cạnh do luật sinh ra chưa được đánh giá.
- RE chỉ xét các cặp trong cùng một câu, không xử lý đồng tham chiếu.
- Thực thể chưa chuẩn hóa không gộp được với các cách viết khác.

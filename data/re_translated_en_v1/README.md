# re_translated_en_v1 — dữ liệu RE tiếng Anh dịch sang tiếng Việt

Bộ này chỉ dùng để **thêm vào dữ liệu huấn luyện** trong một thí nghiệm. Không bao giờ dùng làm test.
Mọi bản ghi có `annotation_status: "TRANSLATED_AI"` và `human_verified: false`.

## Nguồn

| Nguồn | Dùng phần nào | Ghi chú bản quyền |
|---|---|---|
| BioText, Rosario & Hearst (ACL 2004), <https://biotext.berkeley.edu/data/dis_treat_data.html> | Câu có đúng một bệnh (DIS) và một điều trị (TREAT), nhãn TREAT_FOR_DIS, PREVENT, SIDE_EFF | Tác giả yêu cầu trích dẫn bài báo khi dùng |
| ADE corpus v2, Gurulingappa et al. (2012), <https://huggingface.co/datasets/ade-benchmark-corpus/ade_corpus_v2> | Cấu hình `drug_dosage_relation` | Giấy phép ghi "unknown" trên HuggingFace; chỉ dùng cho nghiên cứu |

Dữ liệu gốc tải về `data/external_en_raw/` (không đưa vào git): `scripts/re_dataset/translated_en.py download`.

## Cách làm

1. **Chọn câu** (`translated_en.py sample`, seed 42, cố định trước khi huấn luyện):
   - BioText: 100 câu TREAT_FOR_DIS, cộng toàn bộ câu PREVENT (52) và SIDE_EFF (17). Chỉ lấy câu có đúng một bệnh và một điều trị, tối đa 45 từ.
   - ADE: 60 câu thuốc–liều, tối đa 45 từ.
   - Kết quả là 229 câu, lưu trong `source_en.jsonl`. Thực thể được bọc thẻ `[D]…[/D]` (bệnh), `[T]…[/T]` (điều trị), `[R1]…[/R1]` (thuốc), `[Q1]…[/Q1]` (liều).
2. **Dịch** (`translations_vi.jsonl`):
   - Do AI (Claude Opus 5.5) dịch, giữ nguyên thẻ.
   - Viết theo văn phong VietMed-NER: chữ thường, không dấu câu, số viết bằng chữ (ví dụ "năm trăm mi li gam").
   - Bỏ các số liệu thống kê trong ngoặc.
   - Với BioText, người dịch ghi luôn loại của điều trị: DRUG hoặc PROCEDURE.
3. **Bỏ 30 câu** (lý do ghi trong `translations_vi.jsonl` và `manifest.json`):
   - điều trị chung chung, như "điều trị bằng thuốc" (giống thực thể chung chung bị loại ở gold v1);
   - thực phẩm chức năng, đông y hoặc thảo dược (quy ước `?`);
   - một điều trị gộp cả thuốc lẫn thủ thuật;
   - nhãn gốc trái với quy ước của dự án, ví dụ xạ trị *cho* ung thư phổi nhưng BioText gán là tác dụng phụ;
   - ADE nối mọi thuốc trong câu với một liều chỉ thuộc về một thuốc;
   - một câu trùng nguyên văn với câu khác.
4. **Dựng nhãn** (`translated_en.py build`): đọc thẻ để lấy vị trí ký tự, rồi kiểm tra bằng cùng bộ nạp với các bộ RE khác.
   - TREAT_FOR_DIS → `treated_by` (DRUG) hoặc `treated_by_procedure` (PROCEDURE).
   - PREVENT → `NO_RELATION` (quy ước: phòng bệnh không phải điều trị).
   - SIDE_EFF → `NO_RELATION` (tác dụng phụ là nguyên nhân, không phải điều trị).
   - Cặp thuốc–liều của ADE → `has_dosage`.

## Kết quả

199 câu, 205 cặp (`manifest.json`):

| Nhãn | Cặp |
|---|---:|
| treated_by | 41 |
| treated_by_procedure | 45 |
| has_dosage | 60 |
| NO_RELATION (điều trị–bệnh, từ PREVENT và SIDE_EFF) | 59 |

## Hạn chế

- Văn bản gốc là tóm tắt bài báo y khoa (PubMed), khác xa lời nói tư vấn sức khỏe của VietMed, dù đã viết lại theo văn phong lời nói.
- Bản dịch và loại DRUG/PROCEDURE do AI làm, chưa có người duyệt.
- Nhãn quan hệ lấy từ bộ gốc: BioText gán nhãn theo câu, có một người gán và không có hướng dẫn chi tiết (tác giả tự nêu là có chỗ không nhất quán).
- ADE gần như chỉ có cặp dương cho `has_dosage`.

Thí nghiệm và kết quả: `scripts/re_dataset/bert_re.py --extra-train`, `scripts/re_dataset/eval_augmented.py`, `outputs/re_benchmark_2026-11-08/augmented.md`.

# Phương pháp sinh dữ liệu và gán nhãn quan hệ (RE) bằng LLM

Ghi chép phương pháp để đưa vào báo cáo khóa luận (chương Phương pháp và phần Thực nghiệm dữ liệu).
Ngày lập: 2026-11-24. Mọi con số trong mục 8 được điền sau khi chạy pilot và có kết quả duyệt của chuyên gia.

Mã nguồn:

| Thành phần | File |
|---|---|
| Lược đồ, luật | `re_labels.json`, `relation/guideline.md`, `docs/SCHEMA_QUAN_HE.md` |
| Chia dữ liệu 8:1:1 | `scripts/re_dataset/build_split_811.py` → `data/re_vietmed_811_v1/` |
| Rule sinh, kiểu mẫu, kiểm tra V1–V8 | `re_v3/llm_rules.py` |
| Prompt | `re_v3/prompts/gen_v1.md` (sinh), `re_v3/prompts/verify_v1.md` (gán nhãn) |
| Sinh dữ liệu | `re_v3/synth_llm.py` |
| Gán nhãn câu thật | `re_v3/label_llm.py` |
| Kiểm tra bằng từ điển và công cụ K1–K7 | `re_v3/validate_kb.py` |
| Bảng duyệt chuyên gia và chấm điểm | `re_v3/expert_review.py` |
| Test | `tests/test_re_v3_synth_llm.py`, `tests/test_re_v3_validate_label.py` |

---

## 1. Tổng quan

Hai quy trình dùng chung một hướng dẫn gán nhãn, một lớp kiểm tra tự động và một bước duyệt của chuyên gia:

```
                ┌──────────── hướng dẫn gán nhãn đã khóa (guideline.md, 19–20/11/2026) ────────────┐
                ▼                                                                                  ▼
 (I) SINH DỮ LIỆU                                                          (II) GÁN NHÃN CÂU THẬT
 câu thật có cặp (train)                                                   câu thật có cặp (train/dev/test)
   │  LLM viết lại có điều kiện nhãn (gen_v1)                                │  LLM gán nhãn k = 3 lượt (verify_v1)
   │  Rule bằng code V1–V8                                                   │  Bỏ phiếu đa số (self-consistency)
   │  LLM gán nhãn mù (verify_v1) = nhãn đích?                               │
   └──────────────────────────┬──────────────────────────────────────────────┘
                              ▼
          Kiểm tra bằng từ điển và công cụ K1–K7 (không dùng LLM)
          ICD-10 · RxNorm · từ điển VietMed-NER · regex liều · mô hình NER · luật RE · bằng chứng kho
                              ▼
          Phân tầng: C (lỗi cứng, loại) · B (có cờ, chuyên gia duyệt 100%) · A (sạch, duyệt mẫu)
                              ▼
          Chuyên gia duyệt (CSV) → chấm: accuracy + CI95 Wilson, Cohen's kappa, hiệu quả của từng cờ
                              ▼
          Chỉ dữ liệu đã duyệt mới có human_verified = true và được dùng huấn luyện hay đánh giá
```

Nguyên tắc chung:

- **Không để LLM tự nhận dạng thực thể.** Thực thể lấy từ nhãn NER gốc của VietMed-NER, cặp ứng viên do code sinh theo lược đồ kiểu. LLM chỉ quyết định nhãn quan hệ.
- **Mọi nhãn của LLM đều phải qua kiểm tra độc lập trước khi tới chuyên gia.** Có hai lớp kiểm tra: rule bằng code, và từ điển hoặc công cụ có sẵn.
- **Dữ liệu sinh không bao giờ vào dev hay test.** Dev và test là câu thật, do LLM gán nhãn trước rồi chuyên gia duyệt **toàn bộ**.

## 2. Cơ sở: mỗi lựa chọn thiết kế dựa trên bằng chứng nào

| Lựa chọn thiết kế | Bằng chứng | Áp dụng |
|---|---|---|
| Dùng LLM làm người gán nhãn ban đầu, không thay hẳn con người | Ding et al. (ACL 2023): GPT-3 gán nhãn cho nhiều tác vụ, trong đó có RE và NER, với chi phí thấp hơn nhiều so với người. Gilardi et al. (PNAS 2023): ChatGPT zero-shot chính xác hơn crowd-worker ở 4/5 tác vụ phân loại. Zhao & Goto (2025): LLM hàng đầu tiến gần mô hình BERT SOTA trên khai phá văn bản y sinh, nhưng **chưa đạt mức chuyên gia** và hay không tuân theo hướng dẫn gán nhãn. | LLM gán trước, chuyên gia duyệt lại. Kết quả báo cáo dựa trên nhãn đã duyệt. |
| Đưa hướng dẫn vào prompt nhưng **chỉ phần liên quan** | Zhao & Goto (2025): hướng dẫn dài chèn nguyên văn làm LLM khó tìm đúng mục. Cách sửa của họ là truy xuất đúng mục hướng dẫn và suy luận hai bước. | Prompt chỉ chèn luật của quan hệ có trong câu. Gán nhãn theo hai bước: A (thực thể) rồi B (quan hệ), giống guideline. |
| Ràng buộc theo lược đồ kiểu thực thể | Xu et al. (2023): prompt ràng buộc theo kiểu thực thể giúp LLM làm RE và sinh dữ liệu RE ít mẫu tốt hơn. | Mỗi cặp chỉ có đúng một quan hệ khả dĩ. LLM chỉ chọn giữa quan hệ đó và NO_RELATION. |
| Self-consistency: hỏi nhiều lượt, lấy đa số | Wang et al. (ICLR 2023): lấy mẫu nhiều lời giải rồi bỏ phiếu đa số giúp tăng độ chính xác mà không cần huấn luyện thêm. | k = 3 lượt cho câu thật (lượt 1 nhiệt độ 0, lượt 2–3 nhiệt độ 0,7). |
| Dùng độ bất định để phân bổ công chuyên gia | Li et al., CoAnnotating (EMNLP 2023): chia việc giữa người và LLM theo độ bất định (entropy giữa các lượt, độ tự tin) tốt hơn chia ngẫu nhiên tới 21%. | Mẫu có lượt bất đồng hoặc có cờ K thì chuyên gia duyệt 100%. Mẫu sạch chỉ duyệt mẫu. |
| Sinh dữ liệu có nhãn bằng LLM rồi huấn luyện mô hình nhỏ | Tang et al. (2023): với văn bản lâm sàng, sinh dữ liệu có nhãn bằng LLM rồi fine-tune mô hình cục bộ tốt hơn gọi LLM trực tiếp, F1 RE tăng 75,86 → 83,59. | Dữ liệu sinh chỉ để huấn luyện ViHealthBERT-RE, không để đánh giá. |
| Viết lại có điều kiện nhãn (phản thực tế) và lọc lại bằng mô hình độc lập | Miao, Li & Qian (EMNLP 2023): sinh counterfactual cho RE, loại mẫu có nhãn dự đoán khác nhãn gắn trước. Cặp tối thiểu (minimal pairs) giúp mô hình học đúng tín hiệu thay vì lối tắt (Kaushik et al., ICLR 2020). | Mỗi câu seed được viết lại thành câu dương hoặc âm khó. Chỉ giữ khi lượt gán nhãn mù cho đúng nhãn đích. |
| Kiểm tra bằng nhiều nguồn yếu (luật, từ điển, mô hình) thay vì một nguồn | Ratner et al., Snorkel (VLDB 2017): gộp nhiều hàm gán nhãn nhiễu (heuristic, từ điển, mô hình) cho dữ liệu huấn luyện tốt. Mintz et al. (ACL 2009): giám sát xa, dùng tri thức có sẵn để xác nhận quan hệ. | Lớp K1–K7 dùng ICD-10, RxNorm, từ điển kho, regex, mô hình NER, luật RE và bằng chứng cùng xuất hiện trong kho. |
| Báo cáo độ tin cậy của nhãn | Cohen (1960): kappa. Wilson (1927): khoảng tin cậy cho tỉ lệ khi n nhỏ. Artstein & Poesio (2008): khảo sát về độ đồng thuận giữa người gán. | Báo cáo accuracy kèm CI95 Wilson theo từng quan hệ, kappa giữa AI và chuyên gia, kappa giữa luật và chuyên gia. |

## 3. Phương pháp gán nhãn (dùng cho câu thật, và làm lượt kiểm tra mù cho câu sinh)

1. **Đầu vào.**
   - Câu VietMed, cùng thực thể lấy từ nhãn NER gốc (đã ánh xạ sang 6 kiểu và bỏ thực thể chung chung).
   - Danh sách cặp ứng viên đúng kiểu, do `relation_extraction.data.candidates` sinh.
   - Dữ liệu là bản ghi giọng nói đã công khai, không chứa thông tin định danh bệnh nhân.
2. **Prompt** (`verify_v1.md`):
   - Bước A: gán VALID/INVALID cho từng thực thể theo bảng tiêu chí của guideline.
   - Bước B: gán nhãn cho từng cặp. Chỉ chèn luật của các quan hệ có trong câu.
   - Đầu ra là JSON, có `evidence` (cụm từ làm bằng chứng) và `reason` cho từng cặp.
3. **Self-consistency.**
   - k = 3 lượt. Nhãn cuối của mỗi thực thể và mỗi cặp là nhãn đa số. Số phiếu lưu ở `votes`, ví dụ "2/3".
   - Cặp có thực thể INVALID không được gán quan hệ, đúng theo guideline.
4. **Model.**
   - Mặc định `gpt-4o-2024-08-06`, cố định snapshot. Chế độ JSON, `seed` cố định.
   - Mọi request và response được lưu ở `re_v3/data/synthetic/llm_cache.jsonl`, kèm `system_fingerprint` và số token.
5. **Đưa vào kiểm tra K1–K7 (mục 5), rồi tới chuyên gia (mục 6).** Câu thật không bị loại tự động: lỗi cứng chỉ thành cờ để chuyên gia quyết định.

## 4. Phương pháp sinh dữ liệu

### 4.1 Seed

- Seed là 1407 câu thật có cặp ứng viên, thuộc **train** của split 8:1:1.
- Khi lập job, bỏ các cặp có thực thể nằm trong danh sách INVALID của guideline.
- Sau bước đó còn lại số cặp seed như sau:

| Quan hệ | Cặp seed |
|---|---:|
| located_at | 1982 |
| treated_by_procedure | 511 |
| treated_by | 386 |
| has_dosage | 160 |
| diagnosed_by | 108 |

### 4.2 Job và kiểu mẫu

Mỗi job gồm (câu seed, cặp đích, nhãn đích, kiểu mẫu, vai người nói).

- **28 kiểu mẫu**, mỗi kiểu ứng với một mục của guideline. Xem bảng ở `re_v3/SINH_LLM.md`, mục 2.2. Ví dụ:
  - `POS_NEGATED` của located_at: "không còn đau khớp gối" vẫn là dương.
  - `POS_FAILED` của treated_by: đã dùng thuốc mà không đỡ vẫn là dương.
  - `NEG_PREVENTION`, `NEG_SIDE_EFFECT`, `NEG_QUESTION`: các ca âm khó.
- **Tỉ lệ job:** mỗi quan hệ có hạn mức riêng cho dương và âm. Kiểu mẫu xoay vòng đều. Mỗi (seed, cặp) dùng tối đa 2 lần cho mỗi phân cực.

### 4.3 Sinh

Prompt `gen_v1.md`, nhiệt độ 0,8. Prompt có 6 quy tắc bắt buộc:

1. Giữ nguyên chữ và thẻ của hai thực thể đích.
2. Không thêm thực thể y khoa mới.
3. Văn phong VietMed: chữ thường, không dấu câu, số viết bằng chữ, 15–35 từ.
4. Câu mới phải khác câu gốc, và giữ chủ đề của câu gốc.
5. Nhãn đúng theo luật, nội dung vẫn hợp lý về y khoa.
6. Không làm được thì trả `skip`.

### 4.4 Rule kiểm tra bằng code V1–V8

| Mã | Kiểm tra | Lý do |
|---|---|---|
| V1 | Thẻ thực thể parse được, offset khớp | Bản ghi phải đọc được bằng bộ nạp của repo |
| V2 | Thực thể đích giữ nguyên | Nhãn gắn với đúng mention |
| V3 | Không có thực thể mới | Thực thể mới không có nhãn NER thật |
| V4 | Văn phong VietMed: độ dài, chữ thường, không dấu câu, không chữ số | Giữ đúng miền dữ liệu |
| V5 | Khác câu seed | Không chép lại câu gốc |
| V6 | Có từ đặc trưng của kiểu mẫu (vd. NEG_PREVENTION phải có "phòng/ngừa/tránh") | Đảm bảo câu đúng kiểu mẫu được yêu cầu |
| V7 | Kiểu cách xa: hai thực thể cách nhau ≥ 5 từ | Đúng kiểu mẫu |
| V8 | Không có 8-gram chung với dev/test mới và các tập test cũ | Chống rò rỉ dữ liệu test |

### 4.5 Gán nhãn mù và giữ hay loại

- Câu qua V1–V8 được gán nhãn theo **đúng phương pháp ở mục 3**, nhưng chỉ 1 lượt ở nhiệt độ 0, và **không cho biết nhãn đích**.
- Câu được giữ khi hai thực thể đích là VALID và nhãn mù của cặp đích trùng nhãn đích.
- Các cặp phụ trong câu lấy nhãn mù (`label_source = verifier`).

### 4.6 Kiểm tra K1–K7

Sau đó câu đi qua K1–K7. Câu tầng C bị loại trước khi tính vào hạn mức.

## 5. Kiểm tra bằng từ điển và công cụ (K1–K7)

Lớp này không dùng LLM. Nó chỉ dùng tài nguyên và công cụ đã có trong hệ thống của khóa luận, nên kiểm tra được **độc lập** với LLM.

| Mã | Đối tượng | Nguồn hoặc công cụ | Đạt khi |
|---|---|---|---|
| K1 | CONDITION | Danh mục ICD-10 của Bộ Y tế cùng bộ chuẩn hóa `normalization/icd10.py` (khớp chính xác, đồng nghĩa, fuzzy; chế độ strict) | Có mã ICD-10 |
| K2 | DRUG | RxNorm qua `normalization/rxnorm.py`: cache SQLite, bí danh Việt–Anh, RxNav khi bật `--online-rxnorm` | Có RxCUI |
| K3 | Mọi kiểu | Từ điển kiểu thực thể rút từ nhãn NER gốc VietMed-NER, 3 split, 1969 mention (`re_v3/data/kb/vietmed_entity_dictionary.json`) | Mention xuất hiện ≥ 2 lần và kiểu đang gán chiếm ≥ 50% |
| K4 | DOSAGE | Regex đơn vị liều (viên, mũi, mg, ml, lần, giọt…) cùng số lượng hoặc tần suất (một, hai, mỗi ngày…) | Có cả hai thành phần |
| K5 | Mọi kiểu | Mô hình NER ViHealthBERT của khóa luận (`Model/vihealthbert-ner-vietmed-v2-final`) chạy lại trên câu, bật bằng `--ner` | Mô hình nhận lại thực thể đúng kiểu |
| K6 | Cặp | Luật RE `relation_extraction/rules.py` (viết từ guideline, P ≈ 0,78) | Luật cho cùng nhãn |
| K7 | Cặp dương | Giám sát xa: cặp mention đã cùng xuất hiện trong một câu VietMed thật khác | Có ít nhất một câu hỗ trợ |

Ghi chú:

- Với BODY_PART, TEST và PROCEDURE, hệ thống chưa có ontology (FMA, LOINC, MeSH mới là stub). Vì vậy K3 là kiểm tra từ điển duy nhất cho ba kiểu này, và điều này cần ghi vào phần hạn chế.
- K6 và K7 chỉ là cờ mềm. Luật có recall thấp. Cặp dương có thể mới với kho nhưng vẫn đúng.

**Phân tầng:**

- **C (loại)**:
  - thực thể đích có mention gần như luôn là kiểu khác trong kho (< 20%), hoặc
  - has_dosage có DOSAGE đích không qua K4.

  Với câu thật thì không loại, chỉ ghi cờ.
- **B**: có cờ K, hoặc với câu thật có lượt self-consistency bất đồng. Chuyên gia duyệt 100%.
- **A**: sạch. Chuyên gia duyệt mẫu ngẫu nhiên:
  - pilot: 100%;
  - train: 20%;
  - dev và test: 100%, vì đây là tập vàng.

Sau khi chuyên gia duyệt, `expert_review.py` tính **hiệu quả của từng cờ**: tỉ lệ AI sai khi có cờ so với khi không có cờ. Đây là bằng chứng định lượng cho thấy lớp kiểm tra có tác dụng, hoặc cho thấy cờ nào cần bỏ.

## 6. Duyệt của chuyên gia

- **Bảng:** `*_expert_review.csv` (UTF-8, mở bằng Excel), mỗi dòng một cặp.
  - Có sẵn: câu đã đánh dấu đúng cặp, nhãn AI, số phiếu, bằng chứng, mã ICD-10 hoặc RxNorm, nhãn của luật, số câu hỗ trợ trong kho, các cờ K.
  - Tầng B xếp lên đầu.
- **Chuyên gia điền:**
  - `expert_entity_ok`: 1 nếu hai thực thể đúng kiểu, 0 nếu không;
  - `expert_label`: nhãn đúng theo guideline;
  - `expert_natural`: câu nghe như lời thật và hợp lý về y khoa (chỉ áp dụng cho dữ liệu sinh);
  - `expert_note`: trường hợp guideline chưa nói tới.
- **Độ nhất quán của chuyên gia:** sau 1 ngày, chuyên gia gán lại 30 cặp ngẫu nhiên, rồi tính kappa với chính lần gán trước (theo guideline, bước 5).
- **Chấm điểm:**

```powershell
.venv\Scripts\python.exe -X utf8 -m re_v3.expert_review <file csv đã điền>
```

  Đầu ra gồm:
  - accuracy của AI so với chuyên gia, kèm CI95 Wilson, theo từng tầng, quan hệ, phân cực và kiểu mẫu;
  - kappa giữa AI và chuyên gia, và giữa luật và chuyên gia;
  - tỉ lệ câu tự nhiên, tỉ lệ thực thể đúng;
  - hiệu quả của từng cờ K.

- **Chốt nhãn.** Nhãn cuối là nhãn của chuyên gia. Bản ghi đã duyệt được đổi thành `human_verified = true`. Tầng A ngoài mẫu duyệt vẫn là `LLM_LABELED`. Chỉ được dùng tầng này làm silver cho train, và chỉ khi accuracy đo được của tầng A đạt ngưỡng đặt trước (đề xuất ≥ 0,90).

## 7. Tái lập

- Prompt và rule có phiên bản (`PROMPT_VERSION`, các file `*_vN.md`). Mỗi vòng tinh chỉnh tạo file mới, không sửa đè bản cũ.
- Seed ngẫu nhiên cố định: split 20261124, sinh và gán nhãn 42.
- Mỗi lần chạy ghi `manifest.json` gồm model, nhiệt độ, số job, tỉ lệ giữ theo kiểu mẫu, lý do loại, các tầng, cờ và token.
- Cache phản hồi API giúp chạy lại không tốn tiền và lần lại được từng nhãn.

## 8. Bảng số liệu cần điền vào báo cáo

**Bảng 8.1. Phễu sinh dữ liệu (pilot và bản đủ)**

| Quan hệ | Job | Bỏ qua (skip) | Loại V1–V8 | Loại do gán nhãn mù | Loại K (C) | Giữ (A/B) |
|---|---:|---:|---:|---:|---:|---:|

**Bảng 8.2. Chất lượng nhãn theo chuyên gia**

| Tập | Quan hệ | n cặp | Accuracy AI [CI95] | Kappa AI–CG | Kappa luật–CG | Tự nhiên (sinh) |
|---|---|---:|---|---:|---:|---:|

**Bảng 8.3. Hiệu quả của lớp kiểm tra**

| Cờ | Số cặp có cờ | Tỉ lệ AI sai khi có cờ | Tỉ lệ AI sai khi không cờ |
|---|---:|---:|---:|

**Bảng 8.4. Tinh chỉnh prompt**

| Vòng | Prompt | Tỉ lệ giữ | Accuracy (CG) | Lỗi chính → sửa gì |
|---|---|---:|---:|---|

**Bảng 8.5. Self-consistency (câu thật)**

| Bảng | Nội dung |
|---|---|
| Tỉ lệ đồng thuận | Tỉ lệ cặp có 3/3 phiếu |
| So sánh accuracy | Accuracy của nhóm 3/3 so với nhóm 2/3 |

## 8b. Phương pháp gán nhãn câu thật bằng LLM: bản cuối và kết quả (cập nhật 25/11/2026)

Đây là một đóng góp của khóa luận: một **quy trình gán nhãn RE bằng LLM có kiểm chứng**. Quy trình được tinh chỉnh qua 4 vòng prompt, có thêm một bước Critic, và mọi vòng đều được đo bằng nhãn chuyên gia.

### 8b.1 Các bước của quy trình cuối (v4 + Critic)

| Bước | Làm gì | File | Cơ sở |
|---|---|---|---|
| 0. Cặp ứng viên | Code sinh cặp theo lược đồ kiểu, mỗi cặp có đúng một quan hệ khả dĩ. LLM không tự tìm thực thể. | `relation_extraction/data.py` | Xu et al. (2023) |
| 1. Bước A, kiểm thực thể | LLM gán VALID/INVALID cho từng thực thể NER. Cặp có thực thể INVALID bị bỏ. Luật v3 trở đi ghi «nếu không chắc thì VALID». | `prompts/verify_v4.md`, `llm_rules.ENTITY_RULES_V3` | Zhao & Goto (2025), suy luận hai bước |
| 2. Bước B, gán quan hệ | Mỗi cặp được gán nhãn quan hệ hoặc NO_RELATION, kèm `evidence` chép nguyên văn từ câu. Prompt chỉ chèn luật của các quan hệ có trong câu. | `llm_rules.RULESETS["v4"]` | Zhao & Goto (2025) |
| 3. Self-consistency thích ứng | Lượt 1 chạy ở nhiệt độ 0. Chỉ khi có dấu hiệu bất định mới gọi thêm lượt 2–3 ở nhiệt độ 0,7, rồi bỏ phiếu đa số. Trung bình 0,9–1,2 lượt gọi mỗi câu, thay vì 3. | `label_llm.py --adaptive` | Wang et al. (ICLR 2023) |
| 4. Kiểm tra K1–K7 | Dùng ICD-10, RxNorm, từ điển kho, regex liều, luật RE và bằng chứng trong kho để gắn cờ, rồi chia tầng A/B. | `validate_kb.py` | Ratner et al. (2017), Mintz et al. (2009) |
| 5. Critic | Một LLM mạnh hơn (gpt-5.4) xem lại **riêng từng cặp đáng nghi**, với HEAD/TAIL được đánh dấu trong câu và chỉ luật của quan hệ đó. Nhãn ban đầu được nêu trung lập để giảm thiên hướng đồng ý. Chỉ nhận FLIP khi confidence = high. | `critic.py`, `prompts/critic_v1.md` | Assi et al. (PromptEng'26), bước Extractor → Critic |
| 6. Chuyên gia | Duyệt 100% pilot, dev, test và tầng B của train, cộng 20% tầng A. Bỏ cặp đã chấm ở pilot, và gộp các mention trùng chữ trong cùng câu. | `expert_review.py`, `scripts/re_dataset/merge_pilot_gold.py` | Li et al., CoAnnotating (2023) |

**Cách chọn cặp cho Critic.** Việc chọn làm bằng code, không tốn API, theo các tiêu chí sau:
- cặp có votes không nhất trí;
- hoặc cặp đang là NO_RELATION nhưng có một trong các dấu hiệu:
  - K7: cặp đó dương ở câu khác trong kho;
  - K6: luật RE cho rằng dương;
  - chữ của TAIL nằm trong chữ của HEAD, ví dụ "xơ vữa động mạch" và "động mạch";
  - located_at với các bộ phận chuyên gia hay sửa: máu, tim, não, mạch, răng, xương.

Lý do: ở pilot, precision đã khoảng 0,94 nhưng recall chỉ khoảng 0,68, nên Critic tập trung vào các cặp âm có khả năng bị bỏ sót. Đây là điểm điều chỉnh so với Assi et al., vốn dùng Critic để giảm dương sai.

### 8b.2 Các vòng tinh chỉnh prompt (Bảng 8.4)

Mỗi vòng sửa đúng những lỗi chuyên gia chỉ ra ở pilot (353 cặp), rồi đo lại trên cùng bộ gold.

| Vòng | Thay đổi chính | Accuracy | F1 |
|---|---|---:|---:|
| v1 | Guideline gốc | 0,688 | 0,686 |
| v2 | Cho phép vị trí ngầm định theo kiến thức y khoa. treated_by loại thực phẩm chức năng và mỹ phẩm. «Cấp cứu» không phải thủ thuật. Thêm luật cho diagnosed_by. | 0,717 | 0,716 |
| v3 | Thu hẹp luật mảnh thực thể («không chắc thì VALID»). has_dosage không tính số viên trong vỉ hay lọ. | 0,745 | 0,749 |
| v4 | Thêm hai quyết định của chuyên gia: biến chứng ở cơ quan khác vẫn tính located_at; «máu» là vị trí hay không thì tùy bệnh. | 0,788 | 0,799 |
| v4 + Critic | Thêm bước 5 | **0,802** | **0,819** |

### 8b.3 Kết quả trên các tập độc lập (Bảng 8.2)

| Tập | Người duyệt | n cặp | Cấu hình | Accuracy [CI95] | P | R | F1 | Kappa AI–CG |
|---|---|---:|---|---|---:|---:|---:|---:|
| Dev | chuyên gia (bản v3) | 143 | v3 | 0,748 | 0,917 | 0,688 | 0,786 | 0,569 |
| Dev | | 143 | v4 | 0,734 | | | 0,774 | |
| Dev | | 143 | v4 + Critic | 0,804 | 0,895 | 0,802 | 0,846 | |
| **Test** | Huyền Minh, 25/11/2026 | 212 | v4 | 0,807 | 0,913 | 0,772 | 0,837 | |
| **Test** | | 212 | **v4 + Critic** | **0,835** [0,779–0,879] | 0,911 | 0,824 | **0,865** | 0,716 |
| Train (B + 20% A) | Nguyễn Hương Giang, 25/11/2026 | 1069 | v4 + Critic | 0,961 [0,947–0,971] | 0,979 | 0,943 | | 0,933 |

- Luật RE (K6) so với chuyên gia chỉ đạt kappa 0,17–0,21. LLM tốt hơn hẳn cách gán nhãn bằng luật.
- Critic tăng F1 trên cả hai tập độc lập: dev từ 0,774 lên 0,846, test từ 0,837 lên 0,865. Precision gần như giữ nguyên, phần tăng chủ yếu đến từ recall.
- Chuyên gia đánh giá các lần FLIP của Critic như sau: pilot 14 đúng và 9 sai, dev 13 đúng và 3 sai. Trên test, Critic FLIP 10 cặp.
- Accuracy trên train cao hơn dev và test. Có hai lý do: phiếu train bỏ các cặp pilot đã được dùng để sửa prompt, và gộp các mention trùng chữ. Vì vậy **số liệu báo cáo là số liệu của test**.
- Lỗi còn lại chủ yếu là bỏ sót located_at: trên test, trong các cặp AI ghi «KHÔNG ở», chỉ 41/58 là đúng. has_dosage (n = 7) và diagnosed_by (n = 3) có quá ít mẫu để kết luận.

### 8b.4 Hiệu quả của lớp kiểm tra K1–K7 (Bảng 8.3)

Bảng ghi tỉ lệ AI sai khi cặp có cờ và khi không có cờ.

| Cờ | Train (n = 1069), có cờ / không cờ | Test (n = 212), có cờ / không cờ |
|---|---|---|
| K1 ICD-10 | 0,039 / 0,040 | 0,149 / 0,197 |
| K2 RxNorm | 0,033 / 0,040 | **0,257 / 0,147** |
| K3 từ điển kho | 0,034 / 0,041 | 0,140 / 0,172 |
| K4 regex liều | 0,029 / 0,040 | **0,346 / 0,140** |
| K6 luật RE | 0,038 / 0,041 | 0,134 / 0,218 |
| K7 giám sát xa | 0,029 / 0,044 | 0,159 / 0,168 |
| SC (bất đồng giữa các lượt) | **0,059 / 0,033** | 0,185 / 0,158 |

- Phần lớn cờ K không phân biệt được cặp AI sai. Chỉ có SC (trên train) và K2, K4 (trên test) có tác dụng.
- Vì vậy, ở bản cuối, lớp K1–K7 được dùng như một **lớp kiểm tra trước khi tới chuyên gia và để chọn cặp cho Critic**, không phải bộ lọc tự động.
- Đây là một kết quả âm có giá trị, nên báo cáo trung thực: kiểm tra bằng từ điển ở mức thực thể không bắt được lỗi ở mức quan hệ.

### 8b.5 Chi phí

| Lần chạy | Model | Chi phí |
|---|---|---:|
| Train v4 (1407 câu) | gpt-5.4-mini | $4,92 |
| Train Critic (644 cặp) | gpt-5.4 | $3,37 |
| Test v4 (177 câu) | gpt-5.4-mini | $0,83 |
| Test Critic (75 cặp) | gpt-5.4 | $0,47 |

- Toàn bộ train + dev + test tốn dưới $12.
- Cache phản hồi giúp chạy lại không tốn tiền.

### 8b.6 Bộ dữ liệu sau duyệt

| Tập | File | Câu | Cặp | Nguồn nhãn |
|---|---|---:|---:|---|
| Train | `re_v3/data/silver/train_label_v4_critic/train_label_v4_critic_gold.jsonl` | 1407 | 1632 | 319 cặp chuyên gia pilot, 1210 cặp chuyên gia train, 103 cặp chỉ có nhãn LLM (trường `label_origin`) |
| Test | `re_v3/data/silver/test_label_v4_critic/test_label_v4_critic_expert_final.jsonl` | 95 có cặp (177 câu) | 212 | 100% chuyên gia |

## 9. Hạn chế

- **Lượt sinh và lượt kiểm tra mặc định cùng một model.** Hai lượt có thể sai theo cùng một kiểu. Vì vậy chất lượng báo cáo bằng accuracy do chuyên gia đo, không bằng tỉ lệ giữ. Có thể chạy thêm `--verify-model` bằng một model khác để so sánh.
- **BODY_PART, TEST và PROCEDURE chưa có ontology chuẩn,** nên K3 chỉ là từ điển rút từ kho. Kho đó cũng có lỗi NER, ví dụ "delta" bị gán DRUG.
- **K2 ở chế độ ngoại tuyến** chỉ tra được các thuốc đã có trong cache hoặc bí danh.
- **Câu sinh bám theo câu seed,** nên không thêm chủ đề mới ngoài phân bố của train.
- **Mỗi tập do một chuyên gia duyệt:** train do Nguyễn Hương Giang, test do Huyền Minh. Chưa có cặp nào được hai người cùng chấm, nên chưa đo được độ đồng thuận giữa các chuyên gia. Phiếu dev chưa ghi tên và ngày duyệt.
- **Prompt v2–v4 được sửa theo lỗi ở pilot,** nên số liệu pilot bị lạc quan. Dev và test là các tập độc lập, không dùng khi sửa prompt.

## 10. Tài liệu tham khảo

- Artstein, R., & Poesio, M. (2008). Inter-coder agreement for computational linguistics. *Computational Linguistics*, 34(4), 555–596.
- Cohen, J. (1960). A coefficient of agreement for nominal scales. *Educational and Psychological Measurement*, 20(1), 37–46.
- Ding, B., Qin, C., Liu, L., et al. (2023). Is GPT-3 a Good Data Annotator? *ACL 2023*. https://aclanthology.org/2023.acl-long.626
- Gilardi, F., Alizadeh, M., & Kubli, M. (2023). ChatGPT outperforms crowd workers for text-annotation tasks. *PNAS*, 120(30). https://arxiv.org/abs/2303.15056
- Kaushik, D., Hovy, E., & Lipton, Z. (2020). Learning the Difference that Makes a Difference with Counterfactually-Augmented Data. *ICLR 2020*.
- Li, M., Shi, T., Ziems, C., Kan, M.-Y., Chen, N., Liu, Z., & Yang, D. (2023). CoAnnotating: Uncertainty-Guided Work Allocation between Human and Large Language Models for Data Annotation. *EMNLP 2023*, 1487–1505. https://aclanthology.org/2023.emnlp-main.92
- Miao, X., Li, Y., & Qian, T. (2023). Generating Commonsense Counterfactuals for Stable Relation Extraction. *EMNLP 2023*, 5654–5668. https://aclanthology.org/2023.emnlp-main.344
- Mintz, M., Bills, S., Snow, R., & Jurafsky, D. (2009). Distant supervision for relation extraction without labeled data. *ACL-IJCNLP 2009*. https://aclanthology.org/P09-1113
- Ratner, A., Bach, S., Ehrenberg, H., Fries, J., Wu, S., & Ré, C. (2017). Snorkel: Rapid Training Data Creation with Weak Supervision. *PVLDB*, 11(3), 269–282. https://arxiv.org/abs/1711.10160
- Tang, R., Han, X., Jiang, X., & Hu, X. (2023). Does Synthetic Data Generation of LLMs Help Clinical Text Mining? arXiv:2303.04360. https://arxiv.org/abs/2303.04360
- Wang, X., Wei, J., Schuurmans, D., et al. (2023). Self-Consistency Improves Chain of Thought Reasoning in Language Models. *ICLR 2023*. https://arxiv.org/abs/2203.11171
- Wilson, E. B. (1927). Probable inference, the law of succession, and statistical inference. *JASA*, 22(158), 209–212.
- Xu, X., Zhu, Y., Wang, X., & Zhang, N. (2023). How to Unleash the Power of Large Language Models for Few-shot Relation Extraction? arXiv:2305.01555. https://arxiv.org/abs/2305.01555
- Zhao, Y., & Goto, K. (2025). Can Frontier LLMs Replace Annotators in Biomedical Text Mining? Analyzing Challenges and Exploring Solutions. arXiv:2503.03261. https://arxiv.org/abs/2503.03261
- Assi et al. (2026). Extractor–Critic prompting for information extraction. *PromptEng'26*. (Cần kiểm tra lại trích dẫn đầy đủ trước khi đưa vào báo cáo.)
- Bộ dữ liệu VietMed-NER: `leduckhai/VietMed-NER` (Hugging Face).

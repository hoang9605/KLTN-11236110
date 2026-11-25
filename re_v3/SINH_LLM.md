# (C) Sinh dữ liệu quan hệ bằng LLM

Phương pháp đầy đủ, cơ sở và tài liệu tham khảo cho báo cáo: [docs/PHUONG_PHAP_SINH_VA_GAN_NHAN_RE.md](../docs/PHUONG_PHAP_SINH_VA_GAN_NHAN_RE.md). Kiểm tra từ điển/công cụ K1–K7 chạy tự động sau bước giữ/loại (mục 2.4) và trước khi xuất CSV cho chuyên gia.

Ngày lập: 2026-11-24. Code: [synth_llm.py](synth_llm.py), rule: [llm_rules.py](llm_rules.py), prompt: [prompts/](prompts/), test: `tests/test_re_v3_synth_llm.py`.

## 1. Ý tưởng

Seed là **1407 câu thật có cặp ứng viên** trong train của split 8:1:1 (`data/re_vietmed_811_v1/train.jsonl`). Các câu này chưa có nhãn quan hệ, và cách làm dưới đây không cần chúng có nhãn.

Mỗi job gồm (câu seed, cặp đích, nhãn đích, kiểu mẫu). LLM được yêu cầu **viết lại** câu seed sao cho cặp đích mang đúng nhãn đích. Nhãn do ta định trước, LLM không tự đoán. Sau đó một lượt LLM khác gán nhãn **mù** (không thấy nhãn đích). Câu chỉ được giữ khi hai lượt khớp nhau.

```
câu seed (train) + cặp đích + nhãn đích + kiểu mẫu
        │
        ▼
  [1] LLM sinh  (prompts/gen_v1.md, nhiệt độ 0,8)
        │
        ▼
  [2] Rule bằng code V1–V8  ──✗──► loại, ghi lý do
        │
        ▼
  [3] LLM kiểm tra mù (prompts/verify_v1.md, nhiệt độ 0)
        │   gán VALID/INVALID cho mọi thực thể, nhãn cho mọi cặp
        ▼
  [4] Giữ khi: 2 thực thể đích VALID và nhãn mù = nhãn đích
        │
        ▼
  [5] CSV cho chuyên gia ──► chỉ dữ liệu đã duyệt mới được dùng huấn luyện
```

Vì sao làm như vậy:

- **Thực thể là của câu thật.** Cặp bệnh–bộ phận hay bệnh–thuốc vốn đã cùng xuất hiện trong lời nói thật. Nhờ vậy tránh được lỗi câu phản thực tế ("viêm phổi ở đầu gối") của cách thay thực thể ở (B).
- **Văn phong bám theo câu seed.** Cách này khắc phục điểm yếu của (B): câu template ngắn và sạch hơn lời nói thật.
- **Nhãn được kiểm hai lần.** Lần đầu là cue bằng code (V6), lần sau là LLM gán mù. Hai bước này độc lập với lượt sinh.

## 2. Bộ rule

### 2.1 Luật gán nhãn

Luật lấy từ `relation/guideline.md` (khóa ngày 19/11, bổ sung ngày 20/11), rút gọn trong `llm_rules.py`:

- `GENERAL_RULES`: chỉ gán điều câu nói ra, chỉ dùng chính câu đó, đúng mention, câu bị cắt, động vật hay thí nghiệm.
- `ENTITY_RULES`: tiêu chí VALID/INVALID cho 6 kiểu thực thể.
- `RELATION_RULES`: luật dương/âm của từng quan hệ (phủ định, phòng bệnh, tác dụng phụ, câu hỏi, giả định, liệt kê…).

Prompt sinh chỉ chèn luật của quan hệ đích. Prompt kiểm tra chèn luật của mọi quan hệ có mặt trong câu.

### 2.2 Kiểu mẫu

Mỗi kiểu mẫu ứng với một mục trong guideline, để dữ liệu phủ đủ các ca khó chứ không chỉ câu dễ:

| Quan hệ | Dương | Âm khó |
|---|---|---|
| located_at | POS_EXPLICIT, POS_ADJACENT, POS_NEGATED (phủ định vẫn dương), POS_LONG_GAP | NEG_OTHER_SITE (biến chứng ở chỗ khác), NEG_LIST_FAR (triệu chứng không đứng sát), NEG_COOCCUR |
| treated_by, treated_by_procedure | POS_EXPLICIT, POS_LONG_GAP, POS_CONDITIONAL (nếu… thì dùng), POS_FAILED (dùng mà không đỡ vẫn dương) | NEG_NOT_USED, NEG_PREVENTION, NEG_SIDE_EFFECT, NEG_QUESTION (hỏi chưa trả lời), NEG_COOCCUR |
| diagnosed_by | POS_EXPLICIT, POS_RESULT, POS_LONG_GAP | NEG_COOCCUR, NEG_OTHER_TARGET |
| has_dosage | POS_EXPLICIT, POS_LONG_GAP | NEG_OTHER_OWNER (lượng của thứ khác), NEG_STATISTIC |

Các kiểu mẫu được xoay vòng đều trong mỗi (quan hệ, phân cực). Vai người nói (bác sĩ tư vấn, bệnh nhân kể, người nhà hỏi, trả lời thính giả) được chọn ngẫu nhiên để tăng độ đa dạng.

### 2.3 Rule kiểm tra bằng code (`check_generation`)

| Mã | Kiểm tra | Lý do |
|---|---|---|
| V1 | Thẻ `[E1:KIỂU]…[/E1]` parse được, offset khớp, không chồng lấn | Bản ghi phải đọc được bằng bộ nạp của repo |
| V2 | Hai thực thể đích còn đủ, giữ nguyên chữ và kiểu | Nhãn gắn với đúng mention |
| V3 | Không có thực thể mới ngoài các thực thể của câu seed | Thực thể mới sẽ không có nhãn NER thật |
| V4 | 10–40 từ, chữ thường, không dấu câu, không chữ số | Văn phong VietMed |
| V5 | Khác câu seed | Không chép lại |
| V6 | Có từ đặc trưng của kiểu mẫu, ví dụ NEG_PREVENTION phải có "phòng/ngừa/tránh" | LLM không làm đúng kiểu thì nhãn đích dễ sai |
| V7 | POS_LONG_GAP: hai thực thể cách nhau ≥ 5 từ | Đúng kiểu mẫu |
| V8 | Không có 8-gram chung với dev/test mới và các tập test cũ | Chống rò rỉ |

Ngoài ra, trước khi gọi API, `plan_jobs` bỏ các cặp có thực thể nằm sẵn trong danh sách INVALID của guideline (`is_guideline_invalid`).

### 2.4 Quy tắc giữ hay loại

- Giữ khi **thực thể đích được kiểm tra là VALID** và **nhãn mù của cặp đích = nhãn đích**.
- Các cặp khác trong câu lấy nhãn mù (`label_source = verifier`). Cặp có thực thể INVALID bị bỏ.
- Mọi bản ghi có `annotation_status = SYNTHETIC_LLM`, `human_verified = false`, `training_eligible = false`. Hai trường này chỉ được đổi sau khi chuyên gia duyệt.

## 3. Prompt

- [prompts/gen_v1.md](prompts/gen_v1.md): sinh có điều kiện nhãn. Có 6 quy tắc bắt buộc. Nếu không làm được thì trả `skip = true`, vì bỏ qua tốt hơn sinh sai. Đầu ra JSON `{skip, skip_reason, tagged, evidence}`.
- [prompts/verify_v1.md](prompts/verify_v1.md): gán nhãn mù theo hai bước A/B của guideline. Đầu ra JSON gồm validity của từng thực thể và nhãn, bằng chứng của từng cặp.

Mỗi lần sửa prompt hoặc `llm_rules.py`, tạo file `_v2`, `_v3`… và đổi `PROMPT_VERSION` trong `synth_llm.py`. **Không sửa đè** bản cũ, vì phải tái lập được kết quả của từng vòng.

## 4. Quy trình: pilot → tinh chỉnh → chạy đủ

### Bước 1: dry-run, không gọi API

```powershell
.venv\Scripts\python.exe -X utf8 -m re_v3.synth_llm --pos 20 --neg 30 --dry-run --name pilot_v1
```

Đọc `re_v3/data/synthetic/pilot_v1/dry_run_prompts.md`, mỗi (quan hệ, phân cực) một prompt mẫu.

### Bước 2: pilot, mỗi quan hệ 20 dương + 30 âm (khoảng 250 câu)

```powershell
$env:OPENAI_API_KEY = "<khóa của bạn>"
.venv\Scripts\python.exe -X utf8 -m re_v3.synth_llm --pos 20 --neg 30 --name pilot_v1
```

Đầu ra trong `re_v3/data/synthetic/pilot_v1/`:

| File | Nội dung |
|---|---|
| `pilot_v1.jsonl` | Bản ghi đã giữ, đúng định dạng của repo |
| `results.jsonl` | Mọi job, kể cả job bị loại, kèm lý do và phản hồi thô |
| `pilot_v1.manifest.json` | Tỉ lệ giữ theo kiểu mẫu, lý do loại, token đã dùng |
| `pilot_v1_expert_review.csv` | Bảng cho chuyên gia, mỗi dòng một cặp |

Toàn bộ phản hồi API được cache trong `re_v3/data/synthetic/llm_cache.jsonl`. Chạy lại cùng prompt không tốn tiền.

### Bước 3: chuyên gia duyệt pilot

Mở CSV bằng Excel. Mỗi dòng có câu đã đánh dấu `[E1:…]…[/E1]` cho đúng cặp đang xét. Chuyên gia điền các cột:

| Cột | Điền |
|---|---|
| `expert_entity_ok` | 1 nếu cả hai thực thể đúng kiểu (VALID), 0 nếu không |
| `expert_label` | Nhãn đúng theo guideline: tên quan hệ hoặc NO_RELATION |
| `expert_natural` | 1 nếu câu nghe như lời người thật và hợp lý về y khoa, 0 nếu không |
| `expert_note` | Ghi chú khi gặp trường hợp guideline chưa nói tới |

Từ bảng duyệt, tính:

- **Precision nhãn** = tỉ lệ `expert_label == ai_label`, theo từng quan hệ và từng kiểu mẫu, kèm CI95 Wilson. Tính riêng cho cặp đích (`is_target = 1`) và cặp phụ.
- **Tỉ lệ câu tự nhiên**, tính theo `expert_natural`.
- **Cohen's kappa** giữa chuyên gia và AI.

### Bước 4: tinh chỉnh, sau mỗi vòng ghi một dòng vào bảng

| Vòng | Prompt | Tỉ lệ giữ | Precision (chuyên gia) | Tự nhiên | Lỗi chính → sửa gì |
|---|---|---:|---:|---:|---|
| 1 | v1 | | | | |

Những cách sửa thường gặp:

| Hiện tượng | Cách sửa |
|---|---|
| Lỗi lặp lại ở một kiểu mẫu | Thêm luật hoặc ví dụ vào `llm_rules.py`, hoặc bỏ hẳn kiểu mẫu đó |
| Tỉ lệ giữ thấp vì `V3_new_entity` | Nhấn mạnh quy tắc 2 trong prompt sinh |
| Tỉ lệ giữ thấp vì `VERIFY_DISAGREE` | Đọc `results.jsonl` để biết lượt sinh sai hay lượt kiểm tra sai |
| Câu không tự nhiên | Siết quy tắc 3 và 4 |

Sau mỗi lần sửa, chạy lại pilot với `--name pilot_v2`. Dừng khi đạt ngưỡng đặt trước, ví dụ precision cặp đích ≥ 0,90 cho mọi quan hệ và tỉ lệ tự nhiên ≥ 0,85, hoặc khi hai vòng liền không tăng.

### Bước 5: chạy đủ với prompt đã chốt

```powershell
.venv\Scripts\python.exe -X utf8 -m re_v3.synth_llm --pos 300 --neg 450 --name llm_v1
.venv\Scripts\python.exe -X utf8 -m re_v3.filter_synth re_v3/data/synthetic/llm_v1/llm_v1.jsonl
```

Sau khi chạy đủ, chuyên gia duyệt một mẫu ngẫu nhiên phân tầng theo (quan hệ, kiểu mẫu), khoảng 10%. Mục đích là kiểm tra precision đo được ở pilot vẫn giữ trên toàn bộ dữ liệu.

**Giới hạn seed.** Sau khi bỏ thực thể INVALID theo guideline, train có:

| Quan hệ | Cặp seed |
|---|---:|
| located_at | 1982 |
| treated_by_procedure | 511 |
| treated_by | 386 |
| has_dosage | 160 |
| diagnosed_by | 108 |

Mỗi cặp dùng tối đa 2 lần cho mỗi phân cực. Vì vậy với diagnosed_by và has_dosage, số job tối đa chỉ khoảng 216 và 320 cho mỗi phân cực. Muốn nhiều hơn thì tăng `max_uses` trong `plan_jobs`, hoặc chấp nhận hạn mức nhỏ hơn cho hai lớp này.

## 5. Chi phí ước lượng

Ước lượng theo giá GPT-4o mình biết (2,5 USD/1M token vào, 10 USD/1M token ra). Cần kiểm tra lại giá hiện tại.

| Lượt chạy | Job | Token | Chi phí |
|---|---:|---|---:|
| Pilot | 375 | ~1,3M vào, ~0,15M ra | ~5 USD |
| Chạy đủ (300/450) | ~4500–5000 | | ~50–60 USD |

## 6. Hạn chế cần ghi trong khóa luận

- **Lượt sinh và lượt kiểm tra mặc định cùng một model.** Hai lượt có thể cùng sai theo một kiểu. Nên chạy so sánh `--verify-model` bằng một model khác trên pilot, và báo cáo bằng precision do chuyên gia đo, không phải tỉ lệ giữ.
- **Câu sinh được neo vào câu seed,** nên phân bố chủ đề giống train. Đây là ưu điểm về miền, nhưng không thêm chủ đề mới.
- **Nhãn của các cặp phụ chỉ đến từ lượt kiểm tra,** không có điều kiện nhãn như cặp đích. Precision phải đo riêng cho hai loại cặp này.
- **Dữ liệu sinh không bao giờ vào dev hay test.** Đánh giá mô hình chỉ dùng dữ liệu thật đã được người duyệt.

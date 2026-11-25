# re_v3: pipeline RE làm lại bằng dữ liệu tổng hợp

Thư mục riêng cho RE v3. Mục tiêu là tăng số cặp dương bằng hai cách:

- sinh dữ liệu theo pattern đã gán nhãn;
- gán nhãn giả trên dữ liệu thật chưa có nhãn.

Toàn bộ code, dữ liệu sinh và kết quả của RE v3 nằm ở đây. Code dùng lại bộ nạp và luật trong `relation_extraction/`, không sửa module đó.

- Kế hoạch đầy đủ và tài liệu tham khảo: [KE_HOACH.md](KE_HOACH.md)
- Sơ đồ: [pipeline.svg](pipeline.svg)

## Cấu trúc

```
re_v3/
├── KE_HOACH.md          kế hoạch, chẩn đoán, nguồn
├── pipeline.svg         sơ đồ pipeline
├── config.py            đường dẫn, tỉ lệ dương, ngưỡng (một nơi duy nhất)
├── common.py            đọc/ghi jsonl, parse thẻ, kiểm tra bản ghi
├── mine_patterns.py     (A) khai thác pattern            ✅ chạy được
├── lexicon.json         từ điển thực thể theo nhóm chuyên khoa, dùng cho (B)
├── synth_pattern.py     (B) sinh theo pattern            ✅ chạy được
├── synth_llm.py         (C) sinh bằng LLM (OpenAI)       ✅ chạy được, xem SINH_LLM.md
├── llm_rules.py         rule + kiểu mẫu cho (C)
├── label_llm.py         gán nhãn câu thật bằng LLM (self-consistency)
├── validate_kb.py       kiểm tra từ điển/công cụ K1–K7 trước khi đưa chuyên gia
├── expert_review.py     bảng duyệt chuyên gia + chấm điểm
├── prompts/            prompt sinh và prompt kiểm tra
├── pseudo_label.py      (D) gán nhãn giả (silver)        ⏳ khung
├── augment.py           (E) augmentation nhẹ khi train   ⏳ khung
├── filter_synth.py      bộ lọc chung                     ✅ chạy được
├── run_ablation.py      huấn luyện 2 giai đoạn + ablation ⏳ khung
├── data/
│   ├── patterns/        đầu ra (A)
│   ├── synthetic/       đầu ra (B), (C) trước khi lọc
│   ├── silver/          đầu ra (D) trước khi lọc
│   └── filtered/        dữ liệu đã lọc, dùng để huấn luyện
└── outputs/             mô hình, log, bảng kết quả
```

## Chạy (PowerShell, từ thư mục gốc repo)

```powershell
.venv\Scripts\python.exe -X utf8 -m re_v3.mine_patterns
.venv\Scripts\python.exe -X utf8 -m re_v3.synth_pattern
.venv\Scripts\python.exe -X utf8 -m pytest tests/test_re_v3_synth_pattern.py -q
```

## (B) Sinh theo pattern: kết quả `data/synthetic/pattern_v1.jsonl` (seed 42)

Có ba cách sinh:

- **mention_replacement**: lấy câu seed thật, thay một thực thể bằng thực thể cùng kiểu, giữ nguyên nhãn.
- **template**: điền cặp thực thể cùng nhóm chuyên khoa vào pattern dương. Pattern lấy từ hai nguồn: khai thác từ seed và viết tay theo `docs/RE_LABELS.md`.
- **hard_negative**: sinh cặp âm khó:
  - tác dụng phụ, phòng bệnh;
  - phủ định;
  - thực thể gây nhiễu, tức trong cùng câu có một cặp dương và một cặp âm.

3.225 bản ghi, 4.497 cặp, tỉ lệ dương 0,25.

| Quan hệ | Dương | Âm |
|---|---:|---:|
| located_at | 225 | 1.083 |
| treated_by | 225 | 824 |
| treated_by_procedure | 225 | 702 |
| diagnosed_by | 224 | 682 |
| has_dosage | 225 | 82 |

Chi tiết số liệu ở `pattern_v1.manifest.json`, 40 mẫu ngẫu nhiên để xem nhanh ở `pattern_v1.preview.md`.

Các ràng buộc để nhãn không bị sai:

- **Cặp dương chỉ ghép thực thể cùng nhóm chuyên khoa** trong `lexicon.json`. Ví dụ không sinh câu "viêm phổi ở đầu gối".
- **Không thay thực thể DOSAGE trong câu seed.** Nhiều cặp has_dosage âm trong seed là âm vì mention liều là nhiễu NER ("nồng độ", "cao"). Thay bằng liều thật sẽ biến cặp thành dương, trong khi nhãn vẫn ghi âm.
- **Thực thể chỉ nằm trong cặp âm thì chỉ được thay khi mention gốc là thực thể thật**, tức có trong từ điển. Lý do giống trên: cặp có thể âm chính vì mention gốc là nhiễu NER.
- **Cặp dương đến từ mẫu gây nhiễu bị giới hạn ở 30% hạn mức dương**, để phần lớn cặp dương đến từ template dương đa dạng hơn.
- **Thuốc bôi không được điền vào template có "uống" hoặc "tiêm"**.

Hạn chế đã biết, cần kiểm tra bằng ablation và duyệt tay:

- **Câu template ngắn và sạch hơn nhiều so với lời nói VietMed thật.** Mô hình có thể học lối tắt kiểu "câu ngắn thì có nhãn".
- **Mẫu âm khó chiếm khoảng 64% số bản ghi nhưng chỉ có 4–7 template cho mỗi quan hệ**, nên lặp lại nhiều.
- **Nội dung y khoa có thể phi lý dù nhãn quan hệ vẫn đúng.** Ví dụ "suy tim thì không cần phải làm siêu âm tim".
- **has_dosage gần như toàn cặp dương** (225 dương / 82 âm). Trong khi đó, ở VietMed thật, has_dosage gần như luôn âm vì mention DOSAGE phần lớn là nhiễu.
- **Chưa duyệt tay.** File mẫu để duyệt là `data/filtered/pattern_v1_review.csv`, gồm 375 cặp; các cặp có cờ của luật được xếp lên đầu.

## Bộ lọc: `data/filtered/pattern_v1.jsonl`

```powershell
.venv\Scripts\python.exe -X utf8 -m re_v3.filter_synth re_v3/data/synthetic/pattern_v1.jsonl --scale 1
.venv\Scripts\python.exe -X utf8 -m re_v3.filter_synth re_v3/data/synthetic/pattern_v1.jsonl --scale 3
```

Thứ tự các bước lọc:

1. Kiểm tra định dạng bản ghi.
2. Kiểm tra rò rỉ: loại câu có chung 8-gram với random test hoặc golden test.
3. Loại câu trùng với nhau hoặc trùng câu seed.
4. Mỗi khung câu (thực thể thay bằng [KIỂU]) giữ tối đa 3 câu.
5. Đánh dấu chỗ luật cho nhãn khác. Bước này chỉ đánh dấu, không loại.
6. Cân bằng lại tỉ lệ dương.

Kết quả trên pattern_v1:

- Rò rỉ test: 0 câu.
- Vượt giới hạn khung câu: 296 câu bị loại.
- Cân bằng lại: 106 câu bị loại.
- Còn lại: 2.823 bản ghi, 3.749 cặp, tỉ lệ dương 0,25.

Bản rút gọn bằng `--scale`, giữ nguyên tỉ lệ dương:

| File | Số cặp | Cặp dương mỗi lớp (xấp xỉ) |
|---|---:|---:|
| `pattern_v1_x1.jsonl` | 566 | 27 |
| `pattern_v1_x3.jsonl` | 1.676 | 84 |

Về cờ của luật:

- **"Luật nói dương" trên mẫu âm khó** là đúng thiết kế. Các mẫu này cố ý chứa từ gợi ý, ví dụ "dùng … để phòng ngừa".
- **26 cặp âm sinh bằng thay thực thể bị luật cho là dương.** Tôi đã xem từng cặp: không cặp nào sai do bước thay thực thể. Phần lớn là luật bắn nhầm trên các thực thể bị NER VietMed gán sai kiểu, như DRUG "kiểm soát" hay TEST "chuyển hóa".

## Huấn luyện thử (+B, trộn một lần)

Dùng lại `scripts/re_dataset/bert_re.py --extra-train`, với cùng công thức và 3 seed như mô hình đang triển khai. Dữ liệu sinh chỉ dùng để huấn luyện. Sau đó chấm bằng `eval_augmented.py`, với quy tắc quyết định giữ như lần thử dữ liệu dịch.

```powershell
.venv-gpu\Scripts\python.exe -X utf8 scripts/re_dataset/bert_re.py --out re_v3/outputs/ablation_v1 --extra-train re_v3/data/filtered/pattern_v1_x1.jsonl --extra-prefix SP- --tag pattern_x1
.venv\Scripts\python.exe -X utf8 scripts/re_dataset/eval_augmented.py --out re_v3/outputs/ablation_v1 --name pattern_b --tags "pattern_x1=Pattern 1×" "pattern_x3=Pattern 3×" --title "RE v3: thêm dữ liệu sinh theo pattern" --variant-desc "thêm cặp sinh theo pattern từ re_v3/data/filtered (chỉ dùng để huấn luyện)"
```

Kết quả: `outputs/ablation_v1/pattern_b.md`.

### Kết quả +B 1× (2026-11-19)

Huấn luyện trên 556 cặp seed + 566 cặp sinh, 3 seed, mất 51 phút trên GTX 1650. Mọi tập test đều là nhãn AI.

| Tập | Gốc ∪ luật | +B 1× ∪ luật | Chênh F1 (KTC 95% ghép cặp) |
|---|---:|---:|---:|
| golden test v1.1 | 0,553 | **0,667** | +0,114 (+0,019 – +0,209) |
| golden test bản gốc | 0,494 | 0,590 | +0,096 (−0,016 – +0,194) |
| random test | 0,616 | **0,662** | +0,046 (−0,025 – +0,111) |

**Theo quy tắc định trước, +B 1× đạt điều kiện thay mô hình triển khai.**

Nhận xét:

- **Precision tăng rõ.** Xác suất trung bình mô hình gán cho các cặp âm giảm từ 0,17–0,24 xuống còn 0,07–0,10. Lần thêm dữ liệu dịch thì ngược lại, xác suất này tăng lên.
- **Trên random test, mô hình một mình lại giảm** (0,537 → 0,496). Lý do là bị mất 16 cặp dương. Kết quả chỉ tốt hơn khi hợp với luật.
- **Lớp tăng mạnh nhất là has_dosage và diagnosed_by.** treated_by_procedure trên random test giảm (0,438 → 0,364).
- **Chưa đổi mô hình triển khai.** Tốt nhất nên duyệt tay random test trước.

### So sánh 1× và 3× (2026-11-19)

Bản 3× dùng 556 cặp seed + 1.676 cặp sinh. Thời gian chạy 3 seed là 32, 66 và 33 phút.

| Tập | Gốc ∪ luật | +B 1× ∪ luật | +B 3× ∪ luật |
|---|---:|---:|---:|
| golden test v1.1 | 0,553 | **0,667** | 0,630 (+0,077; −0,018 – +0,175) |
| golden test bản gốc | 0,494 | 0,590 | **0,608** (+0,114; +0,026 – +0,206) |
| random test | 0,616 | **0,662** | 0,646 (+0,030; −0,033 – +0,092) |

- Cả hai bản đều đạt quy tắc quyết định.
- **Tăng dữ liệu sinh từ 1× lên 3× không giúp thêm.** Khi hợp với luật, 3× thấp hơn 1× trên golden test v1.1 và random test. 3× chỉ cao hơn trên golden test bản gốc.
- Khi chạy một mình, 3× tốt hơn 1× trên random test (0,547 so với 0,496), vì ít bị mất cặp dương hơn (13 so với 16 cặp).
- Lớp treated_by_procedure trên random test giảm ở cả hai bản (0,438 → 0,364 với 1× và 0,333 với 3×).
- **Nên dùng 1× nếu thay mô hình.** Chênh lệch giữa 1× và 3× nằm trong khoảng nhiễu. Bản 1× ít dữ liệu sinh hơn nên ít rủi ro học lối tắt từ template hơn.

Nếu tiến trình bị ngắt, `bert_re.py --extra-train` lưu kết quả sau từng seed vào `bert_aug_<tag>_partial.json` và tự chạy tiếp từ seed còn thiếu.

## Quy ước bắt buộc

- Mọi bản ghi sinh ra phải mang `annotation_status` là `SYNTHETIC_PATTERN`, `SYNTHETIC_LLM` hoặc `SILVER`, cùng với `human_verified: false`.
- Dữ liệu sinh **không bao giờ** vào tập test.
- Tập test giữ nguyên: `data/golden_test`, `data/re_test_random_v1`.
- Tỉ lệ dương của dữ liệu sinh nằm trong khoảng 20–25%, cấu hình bằng `config.TARGET_POSITIVE_RATIO`.
- Mọi bản ghi phải qua `filter_synth.py` trước khi vào `data/filtered/`.

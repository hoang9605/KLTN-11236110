# Kế hoạch làm lại pipeline RE (v3): synthetic data theo pattern + augmentation

Ngày lập: 2026-11-18. Trạng thái: kế hoạch, chưa code.

## 1. Hiện trạng (đọc từ repo)

| Nguồn | Câu | Cặp dương | Ghi chú |
|---|---:|---:|---|
| `data/re_gold_v1` (600 câu đã duyệt) | 600 | **25** (located_at 20, treated_by_procedure 4, diagnosed_by 1) | 137 NO_RELATION, 24 CHUA_RO; treated_by / has_dosage = 0 |
| `data/re_ai_v2` (nhãn AI) | 199 | 39 | chưa người duyệt |
| `data/re_translated_en_v1` (dịch EN→VI) | 199 | 146 | **làm giảm F1** trên cả 3 tập test |
| `data/re_test_random_v1` (test) | 200 | 72 / 391 cặp | nhãn AI, chưa người duyệt |

Kết quả tốt nhất hiện tại: ViHealthBERT ∪ luật, F1 0,616 trên random test; luật một mình đã đạt 0,598 (P 0,778).

Vấn đề gốc không nằm ở mô hình mà ở dữ liệu:

1. **Quá ít cặp dương**: 600 câu nhưng chỉ có 25 cặp dương. Ba trong năm lớp gần như không có mẫu, nên mô hình không học được.
2. **Dữ liệu dịch làm lệch phân bố**: thêm 12–20 cặp âm bị đoán thành dương, precision giảm (`outputs/re_benchmark_2026-11-08/augmented.md`). Có hai lý do:
   - Văn phong khác: tóm tắt PubMed, không phải lời nói như VietMed.
   - Tỉ lệ dương rất cao (~70%, trong khi VietMed ~15–18%), lại thiếu cặp âm khó.
3. **Tập test là nhãn AI**: con số F1 chưa đứng vững khi bảo vệ.

=> Dữ liệu sinh thêm phải **cùng miền** (lời nói VietMed), **giữ đúng tỉ lệ dương/âm**, và **có nhiều cặp âm khó**.

### Kết quả khai thác pattern (2026-11-19)

Nguồn: `re_v3/data/patterns/summary.md`. Seed gồm gold v1 và ai v2, tổng 556 cặp.

| Quan hệ | Cặp dương | Cặp âm |
|---|---:|---:|
| located_at | 34 | 154 |
| treated_by_procedure | 15 | 72 |
| treated_by | 9 | 123 |
| diagnosed_by | 6 | 63 |
| has_dosage | **0** | 80 |

Hệ quả: (B) chỉ khai thác được pattern dương từ seed cho located_at và treated_by_procedure.

- **has_dosage**: phải viết pattern dương bằng tay (từ `docs/RE_LABELS.md`, `rules.py`) hoặc lấy từ ADE đã dịch.
- **diagnosed_by, treated_by**: tương tự has_dosage.
- Cả ba lớp này đều cần (C) sinh bằng LLM nhiều hơn.

## 2. Tóm tắt tài liệu

- **Sinh dữ liệu bằng LLM cho RE ít mẫu**: Xu et al. 2023, *How to Unleash the Power of LLMs for Few-shot RE*. Prompt bị ràng buộc theo schema (kiểu thực thể), dữ liệu sinh ra dùng để fine-tune mô hình nhỏ, và đạt SOTA few-shot. Guo et al., IJCAI 2025 làm chặt hơn: decoding bị ràng buộc theo kiểu thực thể và **pattern từ vựng–cú pháp của từng quan hệ**. Hướng này khớp với "synthetic data based on labeled pattern".
- **GDA** (Hu et al., Findings ACL 2023): sinh câu mới giữ cấu trúc cú pháp, có gợi ý thực thể. Chỉ +2 F1 trong low-resource. Đừng kỳ vọng tăng quá lớn.
- **Thay thế thực thể (mention replacement)**: Dai & Adel 2020; Yaseen & Langer 2021 trên dữ liệu y sinh. Đơn giản và hiệu quả khi ít dữ liệu. Rủi ro là tạo câu **phản thực tế** (ví dụ "viêm phổi ở đầu gối"). *WHERE and WHICH* (2025) và *CAS* (Database 2025) giải quyết bằng cách giữ thẻ thực thể cố định và lọc bỏ mẫu không hợp lệ hoặc có quan hệ không còn tương đồng.
- **Delmas et al. 2023 (y sinh)**: dữ liệu tổng hợp bằng LLM mở, sinh có tối ưu độ đa dạng. Fine-tune trên dữ liệu này tốt hơn dữ liệu gốc nhiễu.

Bài học chung: **sinh → lọc → trộn có kiểm soát**. Bước lọc quan trọng ngang bước sinh.

## 3. Thiết kế pipeline dữ liệu mới

```
gold v1 + ai v2 (seed)
   │
   ├─(A) Khai thác pattern ──► pattern bank theo quan hệ (+ pattern âm)
   │
   ├─(B) Synthetic tầng 1: thay thế thực thể / ghép pattern (tất định)
   ├─(C) Synthetic tầng 2: LLM sinh câu theo pattern, kiểu VietMed
   ├─(D) Silver: gán nhãn giả trên VietMed-NER train chưa nhãn
   └─(E) Augmentation nhẹ: nhiễu kiểu ASR, chèn từ đệm
            │
            ▼
   Bộ lọc chung (offset, luật, mô hình, trùng lặp/rò rỉ test, kiểm tra tay 10%)
            │
            ▼
   Huấn luyện 2 giai đoạn: synthetic/silver → fine-tune trên gold
```

### (A) Khai thác pattern từ dữ liệu đã gán nhãn

Script mới: `scripts/re_dataset/mine_patterns.py`.

- Với mỗi cặp, lấy: kiểu (head, tail), thứ tự, khoảng cách token, **chuỗi giữa hai thực thể** và cửa sổ ±3 token.
- Gom thành pattern có slot, ví dụ:
  - `[COND] ở (vùng) [BODY]` → located_at
  - `[COND] (thì) phải uống [DRUG]` → treated_by
  - `xét nghiệm [TEST] (để) phát hiện [COND]` → diagnosed_by
  - `[DRUG] liều [DOSAGE]` → has_dosage
- Pattern âm phải gom riêng, vì đây là nguồn cặp âm khó:
  - phủ định: "không cải thiện với [DRUG]";
  - phòng bệnh;
  - tác dụng phụ: "[DRUG] gây [COND]";
  - hai BODY_PART nhưng chỉ một cái liên quan;
  - thực thể ở hai mệnh đề khác nhau.
- Đối chiếu với `relation_extraction/rules.py` (luật đang có P 0,78) để bổ sung trigger.
- Đầu ra `data/re_patterns_v1/patterns.jsonl`. Pattern ít mẫu (chỉ 1 lần xuất hiện) cần duyệt tay nhanh, khoảng 1–2 giờ.

### (B) Synthetic tầng 1: dựa trên pattern, không dùng LLM

Script mới: `scripts/re_dataset/synth_pattern.py`.

1. **Thay thế thực thể cùng kiểu** trong câu gold: giữ ngữ cảnh, chỉ đổi mention.
   - Từ điển thực thể lấy từ: thực thể NER trên VietMed train, cache RxNorm trong `normalization/data/`, ICD-10 trong `ICD-10/`.
   - **Ràng buộc hợp lý** để tránh câu phản thực tế: chỉ ghép bệnh–bộ phận đã cùng xuất hiện trong VietMed hoặc có trong knowledge graph `knowledge_graph/`; chỉ ghép thuốc–bệnh có cạnh trong KG hoặc nhóm ICD phù hợp.
2. **Ghép pattern**: đặt cặp thực thể hợp lệ vào pattern khác cùng nhãn, thêm tiền tố hoặc hậu tố lấy từ câu VietMed thật để giữ văn phong.
3. **Cặp âm phản chứng**: từ mỗi câu dương, sinh biến thể âm bằng phủ định, phòng bệnh hoặc chèn thực thể gây nhiễu.
   - Đây là phần sửa trực tiếp lỗi của bản dịch EN: mô hình phải thấy cặp gần giống dương nhưng là âm.
- Mục tiêu: mỗi lớp khoảng 150–300 cặp dương. Tổng tỉ lệ dương **~20–25%**, không được 70% như bản dịch.

### (C) Synthetic tầng 2: LLM sinh câu theo pattern

Script mới: `scripts/re_dataset/synth_llm.py`, tái dùng định dạng thẻ `[D]…[/D]` của `translated_en.py`.

- Prompt gồm:
  - định nghĩa quan hệ và quy ước của gold v1 (manifest: thực thể chung chung, câu hỏi, phủ định, TPCN);
  - 1 pattern và 3–5 câu seed thật;
  - yêu cầu văn phong VietMed: chữ thường, không dấu câu, số viết bằng chữ, có từ đệm "thì", "cái", "là", câu có thể bị cắt;
  - yêu cầu sinh **cả câu dương lẫn câu âm khó** cho cùng cặp kiểu.
- Đa dạng hóa: xoay vòng pattern, chủ đề (da liễu, tim mạch, nhi…) và người nói (bác sĩ, bệnh nhân). Đặt hạn mức cho mỗi pattern để không trùng lặp.
- Mỗi câu sinh ra được LLM gán nhãn lại ở lượt thứ hai, độc lập. Chỉ giữ câu mà hai lượt đồng ý.

### (D) Silver: gán nhãn giả trên dữ liệu thật chưa nhãn

Script mới: `scripts/re_dataset/pseudo_label.py`.

- Nguồn: VietMed-NER **train** (không lấy test), câu có cặp ứng viên đúng kiểu, loại các câu đã có trong gold, ai_v2 và golden test.
- Chỉ giữ cặp mà **luật và ViHealthBERT v1 đồng ý** với độ tin cậy cao: dương với p > 0,9, âm với p < 0,05.
- Đây là dữ liệu thật nên đúng văn phong. Điểm yếu là thiên về các mẫu dễ.

### (E) Augmentation nhẹ

Thêm vào quá trình huấn luyện, theo xác suất:

- chèn từ đệm hoặc lặp từ kiểu lời nói;
- xóa ngẫu nhiên token **nằm ngoài** đoạn giữa hai thực thể;
- đổi trigger đồng nghĩa ("ở" ↔ "tại", "uống" ↔ "dùng").

Không động vào token của thực thể. Sau mỗi phép biến đổi phải tính lại offset.

### Bộ lọc chung

Script mới: `scripts/re_dataset/filter_synth.py`. Mọi mẫu synthetic hoặc silver đều phải qua bộ lọc này.

1. Parse thẻ, kiểm tra offset bằng **cùng bộ nạp** `relation_extraction/data.py`.
2. Kiểm tra nhất quán: mẫu mà luật bắn ngược nhãn với độ tin cậy cao thì đưa ra để duyệt, không giữ.
3. Loại trùng gần (n-gram hoặc MinHash). **Kiểm tra rò rỉ** với golden test và random test: loại mọi câu có trùng 8-gram với câu test.
4. Lấy ngẫu nhiên 10% mỗi lớp để bạn duyệt tay (ước tính khoảng 2–3 giờ), ghi tỉ lệ đúng vào manifest để báo cáo chất lượng dữ liệu sinh.
5. Mọi bản ghi đều mang `annotation_status: SYNTHETIC_PATTERN | SYNTHETIC_LLM | SILVER`, `human_verified: false` và **không bao giờ vào tập test**.

## 4. Huấn luyện

Sửa `scripts/re_dataset/bert_re.py`:

- `--stage1-data` / `--stage2-data`: giai đoạn 1 học synthetic và silver, giai đoạn 2 fine-tune trên gold và ai_v2 với learning rate nhỏ hơn. Lần trước, trộn thẳng dữ liệu dịch đã làm hỏng kết quả, nên tách hai giai đoạn an toàn hơn.
- Phương án thay thế khi so sánh: trộn một lần với `--sample-weight` (gold 1,0; silver 0,5; synthetic 0,3).
- Ngưỡng riêng cho từng quan hệ, chọn bằng CV trên gold. Giữ lọc cặp theo kiểu thực thể và hợp với luật ở đầu ra.

## 5. Đánh giá: định trước, giống cách đã làm với bản dịch

- **Ưu tiên số 1: duyệt tay `re_test_random_v1`** (391 cặp). Không có bước này, mọi cải thiện vẫn chỉ là "khớp nhãn AI". Đây là việc đáng làm nhất cho khóa luận.
- Thí nghiệm ablation, 3 seed, paired bootstrap CI95, tái dùng `eval_augmented.py`:

| Biến thể | Dữ liệu thêm |
|---|---|
| baseline | (mô hình v1 hiện tại) |
| +B | synthetic pattern |
| +C | synthetic LLM |
| +D | silver |
| +B+C+D | tất cả, huấn luyện 2 giai đoạn |
| +B+C+D (trộn) | tất cả, trộn có trọng số |

- Quét kích thước dữ liệu synthetic: 1×, 3×, 5× số cặp thật.
- Quy tắc quyết định giữ nguyên: chỉ thay mô hình triển khai khi biến thể ∪ luật thắng trên cả golden test lẫn random test, và CI ghép cặp không nằm hẳn dưới 0.
- Báo cáo F1 theo từng lớp. Kỳ vọng thực tế: tăng chủ yếu ở treated_by, treated_by_procedure, diagnosed_by và has_dosage. Với located_at, luật đã mạnh nên có thể không tăng.

## 6. Thứ tự làm & ước lượng

| # | Việc | Thời gian |
|---|---|---|
| 1 | Duyệt tay random test (song song với các bước sau) | 4–6 giờ |
| 2 | `mine_patterns.py` + duyệt pattern bank | 0,5 ngày |
| 3 | `synth_pattern.py` + `filter_synth.py` | 1 ngày |
| 4 | Huấn luyện thử +B, so với baseline (kiểm tra nhanh hướng đi) | 0,5 ngày |
| 5 | `synth_llm.py` + lọc + duyệt 10% | 1 ngày |
| 6 | `pseudo_label.py` | 0,5 ngày |
| 7 | Huấn luyện 2 giai đoạn + ablation đủ | 1 ngày |
| 8 | Cập nhật README RE, manifest, chương báo cáo | 0,5 ngày |

**Điểm dừng sau bước 4**: nếu +B không cải thiện, hoặc làm giảm precision như bản dịch, thì xem lại tỉ lệ âm/dương và bộ lọc trước khi sinh bằng LLM.

## Nguồn

- Xu et al. 2023: https://arxiv.org/abs/2305.01555
- Guo et al. IJCAI 2025: https://www.ijcai.org/proceedings/2025/0897.pdf
- Hu et al., GDA, Findings ACL 2023: https://aclanthology.org/2023.findings-acl.649
- WHERE and WHICH (2025): https://arxiv.org/abs/2503.23673
- Yaseen & Langer 2021: https://arxiv.org/abs/2108.11703
- Delmas et al. 2023: https://arxiv.org/abs/2311.06364

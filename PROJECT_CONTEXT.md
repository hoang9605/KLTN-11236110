# Bối cảnh dự án: Medical NLP Pipeline (Khóa luận tốt nghiệp)

## Mục tiêu
Xây dựng pipeline trích xuất thông tin y tế từ văn bản lâm sàng tiếng Việt: NER → Normalization → Relation Extraction.

## Model đã có (KHÔNG train lại)
- Vị trí: `Model/vihealthbert-ner-vietmed-v2-final`
- Base model: `demdecuong/vihealthbert-base-syllable`
- Train trên: VietMed-NER (leduckhai/VietMed-NER), label set gốc 37 nhãn dạng BIO
- Bất kỳ agent nào làm việc trên pipeline này chỉ được dùng checkpoint có sẵn để inference, không fine-tune hay train mới trừ khi được yêu cầu rõ ràng.

## Schema thực thể mục tiêu (đã chốt — không tự đổi)
| Thực thể | Nhãn gốc VietMed map vào |
|---|---|
| CONDITION | DISEASESYMTOM |
| DRUG | DRUGCHEMICAL, PREVENTIVEMED |
| BODY_PART | ORGAN |
| TEST | DIAGNOSTICS |
| PROCEDURE | SURGERY, MEDDEVICETECHNIQUE, TREATMENT |
| DOSAGE | UNITCALIBRATOR |

Tất cả nhãn gốc khác (AGE, GENDER, DATETIME, OCCUPATION, LOCATION, ORGANIZATION, FOODDRINK, PERSONALCARE, TRANSPORTATION) → **loại bỏ hoàn toàn** khỏi output. Không giữ dưới dạng "OTHER".

Quyết định quan trọng: **không tách DISEASESYMTOM thành DISEASE/SYMPTOM riêng** — đây là thay đổi so với hướng dẫn ban đầu của GVHD, chọn vì giảm rủi ro lỗi mapping (xem lịch sử audit bên dưới).

## Quan hệ mục tiêu (5 loại)
| Quan hệ | Cặp thực thể |
|---|---|
| located_at | CONDITION – BODY_PART |
| treated_by | CONDITION – DRUG |
| treated_by_procedure | CONDITION – PROCEDURE |
| diagnosed_by | CONDITION – TEST |
| has_dosage | DRUG – DOSAGE |

## Normalization
- CONDITION → ICD-10 (danh mục Bộ Y tế, dạng Excel)
- DRUG → RxNorm
- Các ontology khác (FMA, MeSH, LOINC) không bắt buộc trong scope hiện tại.

## Lịch sử vấn đề đã phát hiện (từ audit codebase cũ — để tham khảo, không copy code cũ)
- Model tự tin gán "Bệnh nhân" là OCCUPATION (do đặc điểm dữ liệu train, không phải bug alignment) — lý do chính để loại bỏ nhãn OTHER khỏi output thay vì cố sửa model.
- `text.split()` thô làm dấu câu dính vào entity, phá vỡ cụm từ nhiều từ — phải tách token/dấu câu riêng.
- Special token (`<s>`, `</s>`, `[CLS]`, `[SEP]`) có thể bị gán nhãn ngẫu nhiên do không có gradient trong lúc train — phải loại trước khi decode.
- Fuzzy matching ICD-10 với threshold thấp (0.6) gây sai lệch mã bệnh nghiêm trọng — cần threshold cao hơn (~0.85+) và từ điển đồng nghĩa y khoa.
- Trên Windows, import `torch` có thể deadlock do xung đột OpenMP — cần set `KMP_DUPLICATE_LIB_OK=TRUE` và `OMP_NUM_THREADS=1` trước khi import.

## Nguyên tắc làm việc với agent trên dự án này
- Không tự đổi entity/relation schema đã chốt ở trên.
- Không tự chọn baseline/metric đánh giá — phần này do người làm khóa luận quyết định.
- Gặp trường hợp mơ hồ (entity lồng nhau, mapping không rõ, v.v.) → liệt kê và hỏi lại, không tự suy đoán.
- Viết code mới, không copy logic từ codebase cũ trừ khi được yêu cầu.

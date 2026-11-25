# Schema quan hệ

Tổng hợp từ `re_labels.json` (lược đồ máy đọc) và `relation/guideline.md` (hướng dẫn gán nhãn, khóa ngày 19/11/2026, bổ sung ngày 20/11/2026). Nếu có chỗ khác nhau, hai tài liệu gốc được ưu tiên.

## 1. Loại thực thể

| Nhãn | Nghĩa | Lấy từ nhãn VietMed-NER |
|---|---|---|
| CONDITION | Bệnh, triệu chứng, tổn thương, tình trạng bất thường | DISEASESYMTOM |
| DRUG | Thuốc, hoạt chất, vắc xin, kháng sinh, thực phẩm chức năng, thảo dược, vitamin, mỹ phẩm điều trị | DRUGCHEMICAL, PREVENTIVEMED |
| BODY_PART | Cơ quan, bộ phận, mô, dịch cơ thể | ORGAN |
| TEST | Xét nghiệm, chẩn đoán hình ảnh, thăm khám | DIAGNOSTICS |
| PROCEDURE | Thủ thuật, phương pháp điều trị cụ thể | SURGERY, MEDDEVICETECHNIQUE, TREATMENT |
| DOSAGE | Liều, lượng, hàm lượng, tần suất của thuốc khi dùng | UNITCALIBRATOR |

Trước khi gán quan hệ, mỗi thực thể được đánh dấu **VALID** (đúng kiểu) hoặc **INVALID** (sai kiểu, quá chung chung, không phải thực thể y khoa). Chỉ cặp có cả hai thực thể VALID mới được gán quan hệ. Tiêu chí VALID và INVALID của từng loại nằm ở bước A trong `relation/guideline.md`.

## 2. Năm quan hệ

Mỗi quan hệ có hướng cố định từ thực thể đầu (head) đến thực thể đuôi (tail). Mỗi kiểu cặp ứng với đúng một quan hệ, nên với một cặp cho trước, câu hỏi chỉ là "có quan hệ này hay NO_RELATION".

| Quan hệ | Head → Tail | Dương khi câu nói | Ví dụ dương |
|---|---|---|---|
| `located_at` | CONDITION → BODY_PART | Bệnh hoặc triệu chứng xảy ra ở bộ phận đó | "đau thắt lưng", "cục máu đông ở trong tim", "tê bì chân tay" |
| `treated_by` | CONDITION → DRUG | Thuốc được dùng hoặc chỉ định để chữa, giảm hay kiểm soát bệnh | "thuốc corticoid để điều trị cho bệnh gút", "uống thuốc huyết áp để kiểm soát huyết áp" |
| `treated_by_procedure` | CONDITION → PROCEDURE | Thủ thuật hay phương pháp được dùng để chữa, giảm hay kiểm soát bệnh | "phẫu thuật điều trị béo phì", "kích thích não sâu giúp cải thiện chậm cử động" |
| `diagnosed_by` | CONDITION → TEST | Xét nghiệm hay thăm khám được dùng để phát hiện, chẩn đoán hay theo dõi bệnh | "xét nghiệm sarscov2", "đọc điện tâm đồ kết luận có rung nhĩ" |
| `has_dosage` | DRUG → DOSAGE | Liều hay lượng đó là của chính thuốc đó | "uống hai viên đông trùng hạ thảo mỗi ngày", "tiêm hai mũi vắc xin" |
| `NO_RELATION` | mọi cặp trên | Câu không khẳng định quan hệ giữa hai thực thể | |

```
                 ┌── located_at ─────────────► BODY_PART
                 ├── treated_by ─────────────► DRUG ── has_dosage ──► DOSAGE
   CONDITION ────┤
                 ├── treated_by_procedure ───► PROCEDURE
                 └── diagnosed_by ───────────► TEST
```

Cặp có kiểu không nằm trong bảng, ví dụ CONDITION với CONDITION hay DRUG với BODY_PART, không tạo thành ứng viên.

## 3. Nguyên tắc gán

1. Chỉ gán điều mà câu nói ra, không gán điều đúng về y học.
2. Chỉ dùng chính câu đó, không suy từ câu trước, câu sau hay kiến thức bên ngoài.
3. Quan hệ phải nối đúng hai lượt đề cập đang xét.
4. Mỗi cặp có đúng một nhãn: tên quan hệ hoặc `NO_RELATION`. Không có nhãn "chưa rõ".

## 4. Quy định cho trường hợp khó

| Trường hợp | Nhãn |
|---|---|
| Bộ phận chỉ được nhắc cùng câu, không phải chỗ bệnh xảy ra ("rung nhĩ gây biến chứng ở não") | `located_at` âm |
| Liệt kê nhiều triệu chứng trước một bộ phận | Chỉ triệu chứng đứng sát bộ phận là dương, trừ khi câu nói rõ cả cụm cùng ở đó |
| Phủ định triệu chứng ("không bị đau khớp") | `located_at` vẫn dương |
| Câu nói không dùng hoặc không nên dùng X cho Y | `treated_by` / `treated_by_procedure` âm |
| Đã dùng X cho Y nhưng không hiệu quả | Dương, vì không xét kết quả điều trị |
| Dùng X để phòng Y khi chưa mắc Y | Âm |
| Phòng biến chứng hay tái phát của bệnh đang có ("người rung nhĩ uống thuốc kháng đông để phòng đột quỵ") | Dương với bệnh đang có (rung nhĩ), âm với biến chứng (đột quỵ) |
| Tác dụng phụ (thuốc gây ra bệnh) | Âm |
| Câu hỏi chưa có câu trả lời ("X có chữa được Y không") | Âm |
| Giả định hay hướng dẫn chung ("nếu bị Y thì dùng X") | Dương |
| Xét nghiệm và bệnh chỉ cùng xuất hiện trong câu | `diagnosed_by` âm |
| Lượng là của thứ khác hoặc là số liệu thống kê | `has_dosage` âm |
| Câu bị cắt mất phần nối hai thực thể | Dương nếu phần còn lại đủ rõ, nếu không thì âm |
| Nói về động vật hay thí nghiệm | Âm, trừ khi câu nói rõ là điều trị hay chẩn đoán |

## 5. Định dạng dữ liệu (JSONL, mỗi dòng một câu)

```json
{
  "id": "VM-TR-04211",
  "source_split": "train",
  "source_row_index": 4211,
  "text": "…",
  "entities": [
    {"id": "E1", "text": "đau", "label": "CONDITION", "start": 0, "end": 3, "validity": "VALID"},
    {"id": "E2", "text": "thắt lưng", "label": "BODY_PART", "start": 4, "end": 13, "validity": "VALID"}
  ],
  "relations": [
    {"head": "E1", "tail": "E2", "allowed_relation": "located_at", "label": "located_at"}
  ]
}
```

- `start` và `end` là vị trí ký tự trong `text`, `end` không tính.
- `allowed_relation` là quan hệ duy nhất mà kiểu cặp cho phép. `label` là `allowed_relation` hoặc `NO_RELATION`.
- Tập kiểm tra có thêm `label_v1`, là nhãn của lượt gán đầu trước khi chốt tiêu chí chặt.
- Dữ liệu sinh có thêm `method`, `annotation_status` (`SYNTHETIC_AUTO_VALIDATED` hoặc `SYNTHETIC_EXPERT_CHECKED`) và `parent_id`.

## 6. Lược đồ máy đọc (`re_labels.json`)

```json
{
  "entity_types": ["CONDITION", "DRUG", "BODY_PART", "TEST", "PROCEDURE", "DOSAGE"],
  "relations": [
    {"label": "located_at",           "head_type": "CONDITION", "tail_type": "BODY_PART"},
    {"label": "treated_by",           "head_type": "CONDITION", "tail_type": "DRUG"},
    {"label": "treated_by_procedure", "head_type": "CONDITION", "tail_type": "PROCEDURE"},
    {"label": "diagnosed_by",         "head_type": "CONDITION", "tail_type": "TEST"},
    {"label": "has_dosage",           "head_type": "DRUG",      "tail_type": "DOSAGE"}
  ],
  "negative_label": "NO_RELATION"
}
```

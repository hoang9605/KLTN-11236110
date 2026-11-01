# Tập nhãn Relation Extraction (RE)

Nguồn của năm quan hệ dương là `PROJECT_CONTEXT.md`. File `re_labels.json` là danh sách nhãn có thể đọc bằng máy. `NO_RELATION` là nhãn âm cho bài toán phân loại cặp thực thể, không phải quan hệ y khoa thứ sáu.

## Quan hệ và chiều gán nhãn

`head → tail` là chiều cố định của cặp thực thể. Dùng đúng sáu loại thực thể đầu ra của NER; không tách `CONDITION` thành bệnh và triệu chứng.

| Nhãn | Head → tail | Ý nghĩa | Ví dụ có quan hệ |
| --- | --- | --- | --- |
| `located_at` | `CONDITION → BODY_PART` | Tình trạng xuất hiện ở bộ phận cơ thể được nêu rõ. | “Khối u xuất hiện ở gan”: `khối u → gan`. |
| `treated_by` | `CONDITION → DRUG` | Thuốc được nêu là dùng để điều trị tình trạng. | “Đau đầu được điều trị bằng Paracetamol”: `đau đầu → Paracetamol`. |
| `treated_by_procedure` | `CONDITION → PROCEDURE` | Thủ thuật được nêu là dùng để điều trị tình trạng. | “Hẹp động mạch vành được điều trị bằng đặt stent”: `hẹp động mạch vành → đặt stent`. |
| `diagnosed_by` | `CONDITION → TEST` | Xét nghiệm hoặc phương pháp chẩn đoán được nêu là dùng để xác định tình trạng. | “Viêm phổi được xác nhận qua chụp X-quang”: `viêm phổi → chụp X-quang`. |
| `has_dosage` | `DRUG → DOSAGE` | Liều lượng được nêu là thuộc về thuốc. | “Paracetamol 500 mg”: `Paracetamol → 500 mg`. |

## Nhãn âm và quy tắc gán

- Chỉ tạo cặp ứng viên có `head_type` và `tail_type` trùng một hàng trong bảng. Cặp khác loại, như `BODY_PART → DRUG`, nằm ngoài phạm vi; không gán `NO_RELATION` cho chúng.
- Gán nhãn dương khi văn bản thể hiện rõ quan hệ giữa **chính hai thực thể đó**. Không suy ra quan hệ chỉ vì chúng cùng xuất hiện hoặc vì kiến thức y khoa bên ngoài.
- Gán `NO_RELATION` cho cặp ứng viên đúng loại nhưng văn bản không thể hiện quan hệ tương ứng. Ví dụ “Bệnh nhân đau đầu. Đơn thuốc cũ có Paracetamol” không đủ căn cứ để gán `treated_by` cho `đau đầu → Paracetamol`.
- Giữ nguyên chiều `head → tail` trong dữ liệu, kể cả khi thứ tự xuất hiện trong câu là ngược lại. Một văn bản có thể chứa nhiều cặp quan hệ; gán nhãn riêng cho từng cặp.
- Trường hợp thực thể lồng nhau, tham chiếu mơ hồ, hoặc không rõ liều thuộc thuốc nào cần đưa ra để rà soát, không tự gán nhãn theo suy đoán.

## Biểu diễn một mẫu dữ liệu

Các `head_id` và `tail_id` tham chiếu đến hai thực thể NER của cùng mẫu văn bản. Vị trí thực thể tiếp tục dùng `start_char` và `end_char` của NER.

```json
{
  "text": "Đau đầu được điều trị bằng Paracetamol 500 mg.",
  "entities": [
    {"id": "e1", "surface_text": "Đau đầu", "label": "CONDITION", "start_char": 0, "end_char": 7},
    {"id": "e2", "surface_text": "Paracetamol", "label": "DRUG", "start_char": 27, "end_char": 38},
    {"id": "e3", "surface_text": "500 mg", "label": "DOSAGE", "start_char": 39, "end_char": 45}
  ],
  "relations": [
    {"head_id": "e1", "tail_id": "e2", "label": "treated_by"},
    {"head_id": "e2", "tail_id": "e3", "label": "has_dosage"}
  ]
}
```

Khi tạo tập phân loại cặp, cặp ứng viên hợp lệ không nằm trong danh sách quan hệ dương nhận nhãn `NO_RELATION`.

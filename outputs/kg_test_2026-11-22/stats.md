# Đồ thị tri thức y tế

- Nguồn: `outputs/kg_test_2026-11-08/results.jsonl`; thực thể: **model**; quan hệ: ViHealthBERT (diagnosed_by, has_dosage, located_at, treated_by, treated_by_procedure) ∪ luật (mọi quan hệ; riêng  chỉ do luật)
- 3496 câu → **1337 nút** (108 có mã ICD-10/RxNorm), **498 cạnh** khác nhau (625 lần xuất hiện); 869 nút không có quan hệ.
- Nút được gộp theo mã chuẩn khi chuẩn hóa có quyết định, nếu không theo loại + chữ đã chuẩn hóa.

| Loại nút | Số nút |
|---|---:|
| CONDITION | 382 |
| PROCEDURE | 246 |
| DRUG | 239 |
| BODY_PART | 228 |
| DOSAGE | 176 |
| TEST | 66 |

| Quan hệ | Số cạnh khác nhau | Lần xuất hiện | Nguồn |
|---|---:|---:|---|
| located_at (vị trí) | 177 | 238 | model 238 |
| has_dosage (liều dùng) | 116 | 142 | model 142 |
| treated_by (điều trị bằng thuốc) | 97 | 126 | model 126 |
| treated_by_procedure (điều trị bằng thủ thuật) | 72 | 80 | model 80 |
| diagnosed_by (chẩn đoán bằng) | 36 | 39 | model 39 |

## 25 bộ ba xuất hiện nhiều nhất

| Đầu | Quan hệ | Cuối | Số lần | Nguồn |
|---|---|---|---:|---|
| thuyên tắc huyết | located_at | tĩnh mạch | 16 | model |
| thuyên tắc huyết khối | located_at | tĩnh mạch | 9 | model |
| ra máu | located_at | âm đạo | 5 | model |
| Loãng xương không đặc hiệu | treated_by | tầm soát | 5 | model |
| thính | treated_by | giả | 5 | model |
| vitamin D | has_dosage | nồng độ | 5 | model |
| vitamin D | has_dosage | cao | 5 | model |
| Loãng xương không đặc hiệu | treated_by | phòng ngừa | 4 | model |
| Loãng xương không đặc hiệu | treated_by | ức chế | 4 | model |
| tránh thai | has_dosage | tỷ lệ | 4 | model |
| Đau, không đặc hiệu | located_at | thần kinh | 4 | model |
| mất | located_at | răng | 4 | model |
| thuyên tắc huyết khối | treated_by | dự phòng | 4 | model |
| thuyên tắc huyết | treated_by | dự phòng | 4 | model |
| Thiếu máu không đặc hiệu | located_at | máu | 3 | model |
| polyp | treated_by_procedure | mổ | 3 | model |
| calcium | has_dosage | một | 3 | model |
| calcium | has_dosage | một người | 3 | model |
| hoại tử | located_at | xương hàm | 3 | model |
| Đau, không đặc hiệu | located_at | đại tràng | 3 | model |
| có thai | treated_by | nghi ngờ | 3 | model |
| Tiêu xương | treated_by_procedure | phục hồi | 3 | model |
| tiêu | located_at | xương | 3 | model |
| Tiêu xương | located_at | xương | 3 | model |
| sữa mẹ | has_dosage | cao | 3 | model |

## Hạn chế

- Chất lượng cạnh phụ thuộc RE: trên tập kiểm tra test_v2 (311 cặp, người chuyên môn gán) ViHealthBERT đạt micro F1 0,69 (KTC 95% 0,62–0,76) với precision 0,60, còn ViHealthBERT ∪ luật đạt 0,68 với precision 0,57, tức khoảng 4/10 cạnh có thể sai (relation/outputs/evaluation_test_v2_modes.json). `has_dosage` không có trong tập kiểm định nên chưa được đánh giá riêng; nhiều cạnh `has_dosage` nối tới cụm không phải liều (ví dụ 'nồng độ', 'cao').
- Thực thể chưa chuẩn hóa không gộp được với các cách viết khác (ví dụ 'rong kinh' và 'ra nhiều kinh' là hai nút).
- RE chỉ xét cặp trong cùng một câu; không xử lý đồng tham chiếu.

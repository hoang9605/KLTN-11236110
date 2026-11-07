# Đồ thị tri thức y tế

- Nguồn: `outputs/kg_test_2026-11-07/ner_results_re_v1.jsonl`; thực thể: **model**; quan hệ: mô hình (diagnosed_by, located_at, treated_by, treated_by_procedure) + luật (has_dosage)
- 3496 câu → **1337 nút** (108 có mã ICD-10/RxNorm), **293 cạnh** khác nhau (391 lần xuất hiện); 1058 nút không có quan hệ.
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
| located_at (vị trí) | 246 | 341 | model 292, rule 49 |
| treated_by_procedure (điều trị bằng thủ thuật) | 21 | 24 | model 23, rule 1 |
| treated_by (điều trị bằng thuốc) | 16 | 16 | rule 12, model 4 |
| has_dosage (liều dùng) | 7 | 7 | rule 7 |
| diagnosed_by (chẩn đoán bằng) | 3 | 3 | rule 3 |

## 25 bộ ba xuất hiện nhiều nhất

| Đầu | Quan hệ | Cuối | Số lần | Nguồn |
|---|---|---|---:|---|
| thuyên tắc huyết khối | located_at | tĩnh mạch | 9 | model, rule |
| Tiêu xương | located_at | xương | 8 | model |
| Đau, không đặc hiệu | located_at | răng | 6 | model |
| Tiêu xương | located_at | răng | 5 | model |
| Đau, không đặc hiệu | located_at | thần kinh | 5 | model, rule |
| ra máu | located_at | âm đạo | 4 | rule, model |
| Chảy máu chưa được phân loại ở nơi khác | located_at | đại tràng | 4 | model |
| mất răng | located_at | xương | 4 | model |
| mất | located_at | răng | 4 | model |
| rong huyết | located_at | máu | 3 | model |
| Loãng xương không đặc hiệu | located_at | xương | 3 | model |
| hoại tử | located_at | xương hàm | 3 | model |
| áp xe | located_at | đại tràng | 3 | model, rule |
| mọc | located_at | răng | 3 | rule, model |
| tiêu | located_at | xương | 3 | model |
| mất răng | located_at | xương hàm | 3 | model |
| mất răng | located_at | răng | 3 | model |
| bị tiêu | located_at | răng | 3 | model |
| Đau, không đặc hiệu | located_at | gáy | 3 | model |
| dị vật | located_at | đường sinh dục | 2 | model |
| rong kinh | located_at | máu | 2 | model |
| rong kinh | located_at | nội mạc | 2 | model |
| rong huyết | located_at | nội mạc | 2 | model |
| polyp | located_at | buồng tử cung | 2 | model |
| ung thư nội mạc | located_at | tử | 2 | model, rule |

## Hạn chế

- Chất lượng cạnh phụ thuộc RE: bộ trích mô hình + luật (union) có F1 khoảng 0,47–0,48 (CV và golden test, nhãn AI); `has_dosage` chỉ do luật sinh ra (F1 0,18 trên golden test).
- Thực thể chưa chuẩn hóa không gộp được với các cách viết khác (ví dụ 'rong kinh' và 'ra nhiều kinh' là hai nút).
- RE chỉ xét cặp trong cùng một câu; không xử lý đồng tham chiếu.

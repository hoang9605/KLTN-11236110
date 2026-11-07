# Relation Extraction: mô hình v2 (gold v1 + nhãn AI v2)

> Nhãn v2 và nhãn của golden test là nhãn AI, **chưa có bác sĩ duyệt**. Số liệu là tạm thời.

- Huấn luyện: v1 162 cặp {'NO_RELATION': 137, 'located_at': 20, 'treated_by_procedure': 4, 'diagnosed_by': 1}; v2 394 cặp {'NO_RELATION': 355, 'diagnosed_by': 5, 'treated_by_procedure': 11, 'located_at': 14, 'treated_by': 9}.
- Trùng văn bản v1–v2: 0; trùng giữa dữ liệu huấn luyện và golden test: 0.
- Golden test (split test VietMed, độc lập với dữ liệu huấn luyện): 121 cặp, {'NO_RELATION': 75, 'treated_by': 4, 'diagnosed_by': 10, 'located_at': 20, 'has_dosage': 10, 'treated_by_procedure': 2}.

- `rules`: luật viết từ hướng dẫn gán nhãn, không học. `model_v1`: TF-IDF + LogReg chỉ học v1 (mô hình đang dùng). `model_v2`: cùng công thức, học v1 + v2. `hybrid`: model_v2 cho quan hệ nó hỗ trợ, luật cho phần còn lại. `union`: dương nếu model_v2 hoặc luật nói dương.

### CV 5-fold theo nhóm văn bản trên v1 + v2 (556 cặp)

| Phương pháp | P | R | F1 | CI95 F1 |
|---|---:|---:|---:|---|
| rules | 0.478 | 0.344 | 0.400 | 0.277–0.508 |
| model_v1 | 0.424 | 0.219 | 0.289 | 0.158–0.408 |
| model_v2 | 0.394 | 0.406 | 0.400 | 0.293–0.513 |
| hybrid | 0.361 | 0.406 | 0.382 | 0.279–0.492 |
| union | 0.392 | 0.625 | 0.482 | 0.390–0.573 |

| Quan hệ | Support | F1 rules | F1 model_v1 | F1 model_v2 | F1 hybrid | F1 union |
|---|---:|---:|---:|---:|---:|---:|
| located_at | 34 | 0.607 | 0.305 | 0.354 | 0.354 | 0.516 |
| treated_by | 9 | 0.267 | 0.000 | 0.000 | 0.000 | 0.250 |
| treated_by_procedure | 15 | 0.300 | 0.435 | 0.600 | 0.600 | 0.647 |
| diagnosed_by | 6 | 0.000 | 0.000 | 0.600 | 0.600 | 0.353 |
| has_dosage | 0 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |

### Golden test (held-out, split test) (121 cặp)

| Phương pháp | P | R | F1 | CI95 F1 |
|---|---:|---:|---:|---|
| rules | 0.706 | 0.261 | 0.381 | 0.203–0.528 |
| model_v1 | 0.360 | 0.196 | 0.254 | 0.075–0.405 |
| model_v2 | 0.429 | 0.326 | 0.370 | 0.198–0.500 |
| hybrid | 0.444 | 0.348 | 0.390 | 0.226–0.516 |
| union | 0.468 | 0.478 | 0.473 | 0.333–0.576 |

| Quan hệ | Support | F1 rules | F1 model_v1 | F1 model_v2 | F1 hybrid | F1 union |
|---|---:|---:|---:|---:|---:|---:|
| located_at | 20 | 0.429 | 0.419 | 0.510 | 0.510 | 0.545 |
| treated_by | 4 | 0.444 | 0.000 | 0.667 | 0.667 | 0.600 |
| treated_by_procedure | 2 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| diagnosed_by | 10 | 0.462 | 0.000 | 0.000 | 0.000 | 0.462 |
| has_dosage | 10 | 0.182 | 0.000 | 0.000 | 0.182 | 0.182 |

**Cách được chọn theo CV (dùng cho knowledge graph): `union`.** Golden test chỉ để báo cáo.

Mô hình cuối (`model.joblib`) học trên toàn bộ 556 cặp; hỗ trợ: diagnosed_by, located_at, treated_by, treated_by_procedure.

# Thêm dữ liệu tiếng Anh dịch sang tiếng Việt vào huấn luyện RE

Gốc: ViHealthBERT 3 seed chỉ học trên dữ liệu VietMed (mô hình đang triển khai). Biến thể: cùng công thức, thêm cặp dịch từ `data/re_translated_en_v1` (chỉ dùng để huấn luyện). Nhãn mọi tập test là nhãn AI, chưa có bác sĩ duyệt.

| Tập | Hệ | P | R | F1 (KTC 95%) | Chênh F1 so với gốc (KTC 95% ghép cặp) |
|---|---|---:|---:|---:|---:|
| golden_test | rules | 0.722 | 0.333 | 0.456 (0.29–0.59) |  |
| golden_test | baseline | 0.586 | 0.436 | 0.500 (0.33–0.65) |  |
| golden_test | baseline+rules | 0.568 | 0.538 | 0.553 (0.40–0.67) |  |
| golden_test | biotext | 0.444 | 0.410 | 0.427 (0.29–0.56) | -0.073 (-0.185 – +0.035) |
| golden_test | biotext+rules | 0.489 | 0.564 | 0.524 (0.39–0.63) | -0.029 (-0.109 – +0.054) |
| golden_test | biotext_ade | 0.475 | 0.487 | 0.481 (0.35–0.60) | -0.019 (-0.126 – +0.103) |
| golden_test | biotext_ade+rules | 0.489 | 0.590 | 0.535 (0.41–0.64) | -0.018 (-0.100 – +0.074) |
| golden_test_v1_original | rules | 0.706 | 0.261 | 0.381 (0.20–0.53) |  |
| golden_test_v1_original | baseline | 0.615 | 0.348 | 0.444 (0.29–0.58) |  |
| golden_test_v1_original | baseline+rules | 0.571 | 0.435 | 0.494 (0.35–0.61) |  |
| golden_test_v1_original | biotext | 0.485 | 0.348 | 0.405 (0.27–0.53) | -0.039 (-0.165 – +0.084) |
| golden_test_v1_original | biotext+rules | 0.512 | 0.478 | 0.494 (0.36–0.60) | +0.000 (-0.092 – +0.094) |
| golden_test_v1_original | biotext_ade | 0.514 | 0.413 | 0.458 (0.33–0.57) | +0.014 (-0.107 – +0.151) |
| golden_test_v1_original | biotext_ade+rules | 0.511 | 0.500 | 0.505 (0.38–0.60) | +0.011 (-0.086 – +0.117) |
| random_test | rules | 0.778 | 0.486 | 0.598 (0.50–0.69) |  |
| random_test | baseline | 0.478 | 0.611 | 0.537 (0.44–0.62) |  |
| random_test | baseline+rules | 0.504 | 0.792 | 0.616 (0.54–0.69) |  |
| random_test | biotext | 0.416 | 0.583 | 0.486 (0.40–0.57) | -0.051 (-0.107 – +0.000) |
| random_test | biotext+rules | 0.468 | 0.806 | 0.592 (0.51–0.67) | -0.024 (-0.071 – +0.019) |
| random_test | biotext_ade | 0.439 | 0.597 | 0.506 (0.41–0.58) | -0.031 (-0.109 – +0.045) |
| random_test | biotext_ade+rules | 0.479 | 0.792 | 0.597 (0.52–0.67) | -0.019 (-0.079 – +0.034) |

F1 theo quan hệ (hệ ∪ luật):

| Tập | Quan hệ | Hỗ trợ | Gốc ∪ luật | biotext ∪ luật | biotext_ade ∪ luật |
|---|---|---:|---:|---:|---:|
| golden_test | located_at | 17 | 0.585 | 0.500 | 0.489 |
| golden_test | treated_by | 5 | 0.833 | 0.769 | 0.769 |
| golden_test | treated_by_procedure | 2 | 0.000 | 0.286 | 0.286 |
| golden_test | diagnosed_by | 9 | 0.500 | 0.615 | 0.615 |
| golden_test | has_dosage | 6 | 0.286 | 0.286 | 0.500 |
| golden_test_v1_original | located_at | 20 | 0.605 | 0.565 | 0.553 |
| golden_test_v1_original | treated_by | 4 | 0.600 | 0.545 | 0.545 |
| golden_test_v1_original | treated_by_procedure | 2 | 0.000 | 0.286 | 0.286 |
| golden_test_v1_original | diagnosed_by | 10 | 0.462 | 0.571 | 0.571 |
| golden_test_v1_original | has_dosage | 10 | 0.182 | 0.182 | 0.333 |
| random_test | located_at | 49 | 0.641 | 0.628 | 0.632 |
| random_test | treated_by | 6 | 0.714 | 0.857 | 0.750 |
| random_test | treated_by_procedure | 12 | 0.438 | 0.368 | 0.353 |
| random_test | diagnosed_by | 4 | 0.857 | 0.667 | 0.667 |
| random_test | has_dosage | 1 | 0.000 | 0.000 | 1.000 |

Chẩn đoán (mô hình một mình, so với gốc):

- golden_test, biotext: 12 cặp âm mới bị đoán dương (located_at 7, treated_by 2, treated_by_procedure 3), 2 cặp dương mới đoán đúng, 3 cặp dương bị mất; xác suất trung bình trên cặp âm 0.244 → 0.296
- golden_test, biotext_ade: 12 cặp âm mới bị đoán dương (located_at 7, treated_by 2, treated_by_procedure 3), 4 cặp dương mới đoán đúng, 2 cặp dương bị mất; xác suất trung bình trên cặp âm 0.244 → 0.292
- golden_test_v1_original, biotext: 11 cặp âm mới bị đoán dương (located_at 6, treated_by 2, treated_by_procedure 3), 3 cặp dương mới đoán đúng, 3 cặp dương bị mất; xác suất trung bình trên cặp âm 0.229 → 0.268
- golden_test_v1_original, biotext_ade: 11 cặp âm mới bị đoán dương (located_at 6, treated_by 2, treated_by_procedure 3), 5 cặp dương mới đoán đúng, 2 cặp dương bị mất; xác suất trung bình trên cặp âm 0.229 → 0.272
- random_test, biotext: 20 cặp âm mới bị đoán dương (located_at 12, treated_by_procedure 8), 2 cặp dương mới đoán đúng, 4 cặp dương bị mất; xác suất trung bình trên cặp âm 0.172 → 0.192
- random_test, biotext_ade: 20 cặp âm mới bị đoán dương (located_at 11, treated_by 2, treated_by_procedure 7), 6 cặp dương mới đoán đúng, 7 cặp dương bị mất; xác suất trung bình trên cặp âm 0.172 → 0.187

Quyết định (quy tắc định trước khi huấn luyện): change the deployed model only if variant ∪ rules beats baseline ∪ rules on both golden_test and random_test and neither paired 95% interval is entirely below zero

- BioText (điều trị, phòng bệnh, tác dụng phụ): giữ mô hình triển khai
- BioText + ADE (thêm thuốc–liều): giữ mô hình triển khai

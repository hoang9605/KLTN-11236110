# RE v3: thêm dữ liệu sinh theo pattern

Gốc: ViHealthBERT 3 seed chỉ học trên dữ liệu VietMed (mô hình đang triển khai). Biến thể: cùng công thức, thêm cặp sinh theo pattern từ re_v3/data/filtered (chỉ dùng để huấn luyện). Nhãn mọi tập test là nhãn AI, chưa có bác sĩ duyệt.

| Tập | Hệ | P | R | F1 (KTC 95%) | Chênh F1 so với gốc (KTC 95% ghép cặp) |
|---|---|---:|---:|---:|---:|
| golden_test | rules | 0.722 | 0.333 | 0.456 (0.29–0.59) |  |
| golden_test | baseline | 0.586 | 0.436 | 0.500 (0.33–0.65) |  |
| golden_test | baseline+rules | 0.568 | 0.538 | 0.553 (0.40–0.67) |  |
| golden_test | pattern_x1 | 0.840 | 0.538 | 0.656 (0.50–0.79) | +0.156 (+0.018 – +0.307) |
| golden_test | pattern_x1+rules | 0.727 | 0.615 | 0.667 (0.53–0.78) | +0.114 (+0.019 – +0.209) |
| golden_test | pattern_x3 | 0.778 | 0.538 | 0.636 (0.48–0.77) | +0.136 (+0.000 – +0.288) |
| golden_test | pattern_x3+rules | 0.676 | 0.590 | 0.630 (0.48–0.75) | +0.077 (-0.018 – +0.175) |
| golden_test_v1_original | rules | 0.706 | 0.261 | 0.381 (0.20–0.53) |  |
| golden_test_v1_original | baseline | 0.615 | 0.348 | 0.444 (0.29–0.58) |  |
| golden_test_v1_original | baseline+rules | 0.571 | 0.435 | 0.494 (0.35–0.61) |  |
| golden_test_v1_original | pattern_x1 | 0.833 | 0.435 | 0.571 (0.42–0.70) | +0.127 (-0.025 – +0.275) |
| golden_test_v1_original | pattern_x1+rules | 0.719 | 0.500 | 0.590 (0.44–0.71) | +0.096 (-0.016 – +0.194) |
| golden_test_v1_original | pattern_x3 | 0.852 | 0.500 | 0.630 (0.49–0.75) | +0.186 (+0.060 – +0.310) |
| golden_test_v1_original | pattern_x3+rules | 0.727 | 0.522 | 0.608 (0.48–0.72) | +0.114 (+0.026 – +0.206) |
| random_test | rules | 0.778 | 0.486 | 0.598 (0.50–0.69) |  |
| random_test | baseline | 0.478 | 0.611 | 0.537 (0.44–0.62) |  |
| random_test | baseline+rules | 0.504 | 0.792 | 0.616 (0.54–0.69) |  |
| random_test | pattern_x1 | 0.541 | 0.458 | 0.496 (0.38–0.61) | -0.041 (-0.149 – +0.054) |
| random_test | pattern_x1+rules | 0.612 | 0.722 | 0.662 (0.57–0.75) | +0.046 (-0.025 – +0.111) |
| random_test | pattern_x3 | 0.567 | 0.528 | 0.547 (0.44–0.65) | +0.010 (-0.092 – +0.112) |
| random_test | pattern_x3+rules | 0.593 | 0.708 | 0.646 (0.56–0.73) | +0.030 (-0.033 – +0.092) |

F1 theo quan hệ (hệ ∪ luật):

| Tập | Quan hệ | Hỗ trợ | Gốc ∪ luật | pattern_x1 ∪ luật | pattern_x3 ∪ luật |
|---|---|---:|---:|---:|---:|
| golden_test | located_at | 17 | 0.585 | 0.647 | 0.611 |
| golden_test | treated_by | 5 | 0.833 | 0.833 | 0.833 |
| golden_test | treated_by_procedure | 2 | 0.000 | 0.000 | 0.000 |
| golden_test | diagnosed_by | 9 | 0.500 | 0.714 | 0.615 |
| golden_test | has_dosage | 6 | 0.286 | 0.667 | 0.667 |
| golden_test_v1_original | located_at | 20 | 0.605 | 0.611 | 0.684 |
| golden_test_v1_original | treated_by | 4 | 0.600 | 0.600 | 0.600 |
| golden_test_v1_original | treated_by_procedure | 2 | 0.000 | 0.000 | 0.000 |
| golden_test_v1_original | diagnosed_by | 10 | 0.462 | 0.667 | 0.571 |
| golden_test_v1_original | has_dosage | 10 | 0.182 | 0.571 | 0.571 |
| random_test | located_at | 49 | 0.641 | 0.727 | 0.727 |
| random_test | treated_by | 6 | 0.714 | 0.667 | 0.571 |
| random_test | treated_by_procedure | 12 | 0.438 | 0.364 | 0.333 |
| random_test | diagnosed_by | 4 | 0.857 | 0.857 | 0.857 |
| random_test | has_dosage | 1 | 0.000 | 0.000 | 0.000 |

Chẩn đoán (mô hình một mình, so với gốc):

- golden_test, pattern_x1: 2 cặp âm mới bị đoán dương (located_at 1, treated_by_procedure 1), 6 cặp dương mới đoán đúng, 2 cặp dương bị mất; xác suất trung bình trên cặp âm 0.244 → 0.074
- golden_test, pattern_x3: 3 cặp âm mới bị đoán dương (located_at 2, treated_by_procedure 1), 6 cặp dương mới đoán đúng, 2 cặp dương bị mất; xác suất trung bình trên cặp âm 0.244 → 0.078
- golden_test_v1_original, pattern_x1: 2 cặp âm mới bị đoán dương (located_at 1, treated_by_procedure 1), 7 cặp dương mới đoán đúng, 3 cặp dương bị mất; xác suất trung bình trên cặp âm 0.229 → 0.068
- golden_test_v1_original, pattern_x3: 2 cặp âm mới bị đoán dương (located_at 1, treated_by_procedure 1), 8 cặp dương mới đoán đúng, 1 cặp dương bị mất; xác suất trung bình trên cặp âm 0.229 → 0.061
- random_test, pattern_x1: 14 cặp âm mới bị đoán dương (has_dosage 2, located_at 8, treated_by 2, treated_by_procedure 2), 5 cặp dương mới đoán đúng, 16 cặp dương bị mất; xác suất trung bình trên cặp âm 0.172 → 0.098
- random_test, pattern_x3: 17 cặp âm mới bị đoán dương (has_dosage 2, located_at 9, treated_by 2, treated_by_procedure 4), 7 cặp dương mới đoán đúng, 13 cặp dương bị mất; xác suất trung bình trên cặp âm 0.172 → 0.104

Quyết định (quy tắc định trước khi huấn luyện): change the deployed model only if variant ∪ rules beats baseline ∪ rules on both golden_test and random_test and neither paired 95% interval is entirely below zero

- Pattern 1×: thay mô hình triển khai
- Pattern 3×: thay mô hình triển khai

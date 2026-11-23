# Mô hình ViHealthBERT RE được triển khai so với benchmark

Mô hình: `vihealthbert-re-v1`, trung bình 3 seed [42, 43, 44], 556 cặp huấn luyện; chạy trên cpu.

| Tập | Cặp | Triển khai | Triển khai ∪ luật | Benchmark BERT | Benchmark BERT ∪ luật | Luật | Lệch CPU/GPU | ms/cặp |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| golden_test | 117 | 0.500 | 0.553 | 0.500 | 0.553 | 0.456 | 0/117 | 239.6 |
| golden_test_v1_original | 121 | 0.444 | 0.494 | 0.444 | 0.494 | 0.381 | 0/121 | 222.7 |
| random_test | 391 | 0.537 | 0.616 | 0.537 | 0.616 | 0.598 | 0/391 | 223.7 |

## Từng seed riêng lẻ (F1 một mình / hợp với luật)

| Tập | seed 42 | seed 43 | seed 44 |
|---|---:|---:|---:|
| golden_test | 0.450 / 0.506 | 0.444 / 0.519 | 0.431 / 0.533 |
| golden_test_v1_original | 0.429 / 0.478 | 0.395 / 0.465 | 0.348 / 0.450 |
| random_test | 0.486 / 0.571 | 0.578 / 0.638 | 0.528 / 0.611 |

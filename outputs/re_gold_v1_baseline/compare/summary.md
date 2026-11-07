# So sánh baseline RE (nhãn người duyệt xác nhận, 162 cặp)

| Thiết lập | Phương pháp | P | R | F1 | CI95 F1 |
|---|---|---:|---:|---:|---|
| seed42 dev (21 cặp) | rules | 1.000 | 0.333 | 0.500 | — |
| seed42 dev (21 cặp) | logreg | 0.500 | 0.333 | 0.400 | — |
| seed42 test (17 cặp) | rules | 1.000 | 0.500 | 0.667 | — |
| seed42 test (17 cặp) | logreg | 0.500 | 0.500 | 0.500 | — |
| CV 5-fold theo nhóm (162 cặp) | rules | 0.643 | 0.360 | 0.462 | 0.263–0.638 |
| CV 5-fold theo nhóm (162 cặp) | logreg | 0.714 | 0.400 | 0.513 | 0.286–0.694 |

## CV theo quan hệ (F1, support)

| Quan hệ | Luật | LogReg | Support |
|---|---:|---:|---:|
| located_at | 0.500 | 0.452 | 20 |
| treated_by | 0.000 | 0.000 | 0 |
| treated_by_procedure | 0.400 | 0.857 | 4 |
| diagnosed_by | 0.000 | 0.000 | 1 |
| has_dosage | 0.000 | 0.000 | 0 |

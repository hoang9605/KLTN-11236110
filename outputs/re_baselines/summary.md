# So sánh baseline RE (nhãn AI rà soát, 178 cặp)

| Thiết lập | Phương pháp | P | R | F1 | CI95 F1 |
|---|---|---:|---:|---:|---|
| seed42 dev (27 cặp) | rules | 0.333 | 0.167 | 0.222 | — |
| seed42 dev (27 cặp) | logreg | 0.667 | 0.333 | 0.444 | — |
| seed42 test (14 cặp) | rules | 0.000 | 0.000 | 0.000 | — |
| seed42 test (14 cặp) | logreg | 0.750 | 0.600 | 0.667 | — |
| CV 5-fold theo nhóm (178 cặp) | rules | 0.500 | 0.146 | 0.226 | 0.078–0.386 |
| CV 5-fold theo nhóm (178 cặp) | logreg | 0.558 | 0.707 | 0.624 | 0.484–0.761 |

## CV theo quan hệ (F1, support)

| Quan hệ | Luật | LogReg | Support |
|---|---:|---:|---:|
| located_at | 0.387 | 0.571 | 20 |
| treated_by | 0.000 | 0.000 | 2 |
| treated_by_procedure | 0.000 | 0.679 | 19 |
| diagnosed_by | 0.000 | 0.000 | 0 |
| has_dosage | 0.000 | 0.000 | 0 |

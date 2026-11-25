## 2026-11-24 23:40:13 — re_v3.label_llm

- Lệnh: `C:\Users\ASUS\dev\Code_Study\AI-KLTN\re_v3\label_llm.py --split train --name train_label_v4 --prompt-version v4 --model gpt-5.4-mini --max-usd 5 --a-fraction 0.2`
- prompt_version: "v4"
- model: "gpt-5.4-mini"
- split: "train"
- sentences: 1407
- labeled: 1407
- pairs: 1632
- labels: {"located_at|NO_RELATION": 666, "located_at|located_at": 613, "treated_by|NO_RELATION": 116, "treated_by|treated_by": 32, "treated_by_procedure|NO_RELATION": 87, "diagnosed_by|diagnosed_by": 24, "diagnosed_by|NO_RELATION": 12, "treated_by_procedure|treated_by_procedure": 61, "has_dosage|has_dosage": 13, "has_dosage|NO_RELATION": 8}
- tiers: {"B": 1178, "A": 229}
- budget_stopped_sentences: 0
- calls_per_sentence: 1.18
- usage: {"cache_hits": 461, "api_calls": 1659, "gpt-5.4-mini:prompt_tokens": 3504938, "gpt-5.4-mini:completion_tokens": 509965, "usd_this_run": 4.9235}
- File:
  - nhãn AI (jsonl): `C:\Users\ASUS\dev\Code_Study\AI-KLTN\re_v3\data\silver\train_label_v4\train_label_v4.jsonl`
  - Excel cho chuyên gia: `C:\Users\ASUS\dev\Code_Study\AI-KLTN\re_v3\data\silver\train_label_v4\train_label_v4_expert_review.xlsx`
  - manifest: `C:\Users\ASUS\dev\Code_Study\AI-KLTN\re_v3\data\silver\train_label_v4\train_label_v4.manifest.json`
  - phản hồi API thô: `C:\Users\ASUS\dev\Code_Study\AI-KLTN\re_v3\data\synthetic\llm_cache.jsonl`


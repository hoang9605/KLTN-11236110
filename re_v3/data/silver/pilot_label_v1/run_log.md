## 2026-11-24 19:57:07 — re_v3.label_llm

- Lệnh: `C:\Users\ASUS\dev\Code_Study\AI-KLTN\re_v3\label_llm.py --split train --limit 300 --name pilot_label_v1 --model gpt-5.4-mini --max-usd 3 --a-fraction 1.0`
- prompt_version: "v1"
- model: "gpt-5.4-mini"
- split: "train"
- sentences: 300
- labeled: 300
- pairs: 353
- labels: {"located_at|located_at": 99, "located_at|NO_RELATION": 168, "treated_by_procedure|treated_by_procedure": 10, "diagnosed_by|diagnosed_by": 9, "has_dosage|NO_RELATION": 4, "has_dosage|has_dosage": 2, "treated_by|treated_by": 15, "treated_by|NO_RELATION": 16, "treated_by_procedure|NO_RELATION": 28, "diagnosed_by|NO_RELATION": 2}
- tiers: {"B": 251, "A": 49}
- budget_stopped_sentences: 0
- calls_per_sentence: 1.49
- usage: {"cache_hits": 1, "api_calls": 446, "gpt-5.4-mini:prompt_tokens": 637681, "gpt-5.4-mini:completion_tokens": 143714, "usd_this_run": 1.125}
- File:
  - nhãn AI (jsonl): `C:\Users\ASUS\dev\Code_Study\AI-KLTN\re_v3\data\silver\pilot_label_v1\pilot_label_v1.jsonl`
  - Excel cho chuyên gia: `C:\Users\ASUS\dev\Code_Study\AI-KLTN\re_v3\data\silver\pilot_label_v1\pilot_label_v1_expert_review.xlsx`
  - manifest: `C:\Users\ASUS\dev\Code_Study\AI-KLTN\re_v3\data\silver\pilot_label_v1\pilot_label_v1.manifest.json`
  - phản hồi API thô: `C:\Users\ASUS\dev\Code_Study\AI-KLTN\re_v3\data\synthetic\llm_cache.jsonl`


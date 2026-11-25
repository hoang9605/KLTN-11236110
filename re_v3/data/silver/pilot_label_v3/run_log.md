## 2026-11-24 21:29:05 — re_v3.label_llm

- Lệnh: `C:\Users\ASUS\dev\Code_Study\AI-KLTN\re_v3\label_llm.py --split train --limit 300 --name pilot_label_v3 --prompt-version v3 --model gpt-5.4-mini --max-usd 2 --a-fraction 1.0`
- prompt_version: "v3"
- model: "gpt-5.4-mini"
- split: "train"
- sentences: 300
- labeled: 300
- pairs: 332
- labels: {"located_at|located_at": 121, "located_at|NO_RELATION": 133, "treated_by_procedure|treated_by_procedure": 9, "diagnosed_by|NO_RELATION": 2, "diagnosed_by|diagnosed_by": 9, "has_dosage|NO_RELATION": 4, "has_dosage|has_dosage": 2, "treated_by|treated_by": 9, "treated_by|NO_RELATION": 24, "treated_by_procedure|NO_RELATION": 19}
- tiers: {"B": 256, "A": 44}
- budget_stopped_sentences: 0
- calls_per_sentence: 1.51
- usage: {"api_calls": 454, "gpt-5.4-mini:prompt_tokens": 893187, "gpt-5.4-mini:completion_tokens": 141671, "usd_this_run": 1.3074}
- File:
  - nhãn AI (jsonl): `C:\Users\ASUS\dev\Code_Study\AI-KLTN\re_v3\data\silver\pilot_label_v3\pilot_label_v3.jsonl`
  - Excel cho chuyên gia: `C:\Users\ASUS\dev\Code_Study\AI-KLTN\re_v3\data\silver\pilot_label_v3\pilot_label_v3_expert_review.xlsx`
  - manifest: `C:\Users\ASUS\dev\Code_Study\AI-KLTN\re_v3\data\silver\pilot_label_v3\pilot_label_v3.manifest.json`
  - phản hồi API thô: `C:\Users\ASUS\dev\Code_Study\AI-KLTN\re_v3\data\synthetic\llm_cache.jsonl`


## 2026-11-24 21:25:46 — re_v3.label_llm

- Lệnh: `C:\Users\ASUS\dev\Code_Study\AI-KLTN\re_v3\label_llm.py --split train --limit 300 --name pilot_label_v2 --prompt-version v2 --model gpt-5.4-mini --max-usd 2 --a-fraction 1.0`
- prompt_version: "v2"
- model: "gpt-5.4-mini"
- split: "train"
- sentences: 300
- labeled: 300
- pairs: 297
- labels: {"located_at|located_at": 108, "located_at|NO_RELATION": 104, "treated_by_procedure|treated_by_procedure": 10, "diagnosed_by|diagnosed_by": 10, "has_dosage|NO_RELATION": 8, "treated_by|treated_by": 9, "treated_by|NO_RELATION": 23, "treated_by_procedure|NO_RELATION": 22, "diagnosed_by|NO_RELATION": 1, "has_dosage|has_dosage": 2}
- tiers: {"B": 255, "A": 45}
- budget_stopped_sentences: 0
- calls_per_sentence: 1.5
- usage: {"api_calls": 451, "gpt-5.4-mini:prompt_tokens": 832189, "gpt-5.4-mini:completion_tokens": 142049, "usd_this_run": 1.2634}
- File:
  - nhãn AI (jsonl): `C:\Users\ASUS\dev\Code_Study\AI-KLTN\re_v3\data\silver\pilot_label_v2\pilot_label_v2.jsonl`
  - Excel cho chuyên gia: `C:\Users\ASUS\dev\Code_Study\AI-KLTN\re_v3\data\silver\pilot_label_v2\pilot_label_v2_expert_review.xlsx`
  - manifest: `C:\Users\ASUS\dev\Code_Study\AI-KLTN\re_v3\data\silver\pilot_label_v2\pilot_label_v2.manifest.json`
  - phản hồi API thô: `C:\Users\ASUS\dev\Code_Study\AI-KLTN\re_v3\data\synthetic\llm_cache.jsonl`


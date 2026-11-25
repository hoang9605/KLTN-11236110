## 2026-11-25 02:27:08 — re_v3.label_llm

- Lệnh: `C:\Users\ASUS\dev\Code_Study\AI-KLTN\re_v3\label_llm.py --split test --name test_label_v4 --model gpt-5.4-mini --prompt-version v4 --max-usd 2 --a-fraction 1.0`
- prompt_version: "v4"
- model: "gpt-5.4-mini"
- split: "test"
- sentences: 177
- labeled: 177
- pairs: 212
- labels: {"located_at|NO_RELATION": 64, "has_dosage|has_dosage": 6, "located_at|located_at": 98, "treated_by|NO_RELATION": 19, "treated_by_procedure|NO_RELATION": 11, "diagnosed_by|diagnosed_by": 1, "diagnosed_by|NO_RELATION": 2, "treated_by_procedure|treated_by_procedure": 7, "treated_by|treated_by": 3, "has_dosage|NO_RELATION": 1}
- tiers: {"B": 154, "A": 23}
- budget_stopped_sentences: 0
- calls_per_sentence: 1.56
- usage: {"api_calls": 277, "gpt-5.4-mini:prompt_tokens": 592466, "gpt-5.4-mini:completion_tokens": 84756, "usd_this_run": 0.8258}
- File:
  - nhãn AI (jsonl): `C:\Users\ASUS\dev\Code_Study\AI-KLTN\re_v3\data\silver\test_label_v4\test_label_v4.jsonl`
  - Excel cho chuyên gia: `C:\Users\ASUS\dev\Code_Study\AI-KLTN\re_v3\data\silver\test_label_v4\test_label_v4_expert_review.xlsx`
  - manifest: `C:\Users\ASUS\dev\Code_Study\AI-KLTN\re_v3\data\silver\test_label_v4\test_label_v4.manifest.json`
  - phản hồi API thô: `C:\Users\ASUS\dev\Code_Study\AI-KLTN\re_v3\data\synthetic\llm_cache.jsonl`


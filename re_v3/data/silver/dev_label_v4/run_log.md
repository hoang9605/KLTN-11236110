## 2026-11-24 23:15:24 — re_v3.label_llm

- Lệnh: `C:\Users\ASUS\dev\Code_Study\AI-KLTN\re_v3\label_llm.py --split dev --name dev_label_v4 --prompt-version v4 --model gpt-5.4-mini --max-usd 1.5 --a-fraction 1.0`
- prompt_version: "v4"
- model: "gpt-5.4-mini"
- split: "dev"
- sentences: 177
- labeled: 177
- pairs: 139
- labels: {"located_at|located_at": 61, "treated_by_procedure|treated_by_procedure": 10, "located_at|NO_RELATION": 49, "treated_by_procedure|NO_RELATION": 8, "treated_by|NO_RELATION": 10, "treated_by|treated_by": 1}
- tiers: {"B": 145, "A": 32}
- budget_stopped_sentences: 0
- calls_per_sentence: 0.9
- usage: {"cache_hits": 94, "api_calls": 159, "gpt-5.4-mini:prompt_tokens": 357954, "gpt-5.4-mini:completion_tokens": 47013, "usd_this_run": 0.48}
- File:
  - nhãn AI (jsonl): `C:\Users\ASUS\dev\Code_Study\AI-KLTN\re_v3\data\silver\dev_label_v4\dev_label_v4.jsonl`
  - Excel cho chuyên gia: `C:\Users\ASUS\dev\Code_Study\AI-KLTN\re_v3\data\silver\dev_label_v4\dev_label_v4_expert_review.xlsx`
  - manifest: `C:\Users\ASUS\dev\Code_Study\AI-KLTN\re_v3\data\silver\dev_label_v4\dev_label_v4.manifest.json`
  - phản hồi API thô: `C:\Users\ASUS\dev\Code_Study\AI-KLTN\re_v3\data\synthetic\llm_cache.jsonl`


## 2026-11-24 21:34:28 — re_v3.label_llm

- Lệnh: `C:\Users\ASUS\dev\Code_Study\AI-KLTN\re_v3\label_llm.py --split dev --name dev_label_v3 --prompt-version v3 --model gpt-5.4-mini --max-usd 2 --a-fraction 1.0`
- prompt_version: "v3"
- model: "gpt-5.4-mini"
- split: "dev"
- sentences: 177
- labeled: 177
- pairs: 143
- labels: {"located_at|located_at": 61, "treated_by_procedure|treated_by_procedure": 10, "located_at|NO_RELATION": 50, "treated_by_procedure|NO_RELATION": 8, "treated_by|NO_RELATION": 13, "treated_by|treated_by": 1}
- tiers: {"B": 145, "A": 32}
- budget_stopped_sentences: 0
- calls_per_sentence: 1.44
- usage: {"api_calls": 255, "gpt-5.4-mini:prompt_tokens": 495434, "gpt-5.4-mini:completion_tokens": 68835, "usd_this_run": 0.6813}
- File:
  - nhãn AI (jsonl): `C:\Users\ASUS\dev\Code_Study\AI-KLTN\re_v3\data\silver\dev_label_v3\dev_label_v3.jsonl`
  - Excel cho chuyên gia: `C:\Users\ASUS\dev\Code_Study\AI-KLTN\re_v3\data\silver\dev_label_v3\dev_label_v3_expert_review.xlsx`
  - manifest: `C:\Users\ASUS\dev\Code_Study\AI-KLTN\re_v3\data\silver\dev_label_v3\dev_label_v3.manifest.json`
  - phản hồi API thô: `C:\Users\ASUS\dev\Code_Study\AI-KLTN\re_v3\data\synthetic\llm_cache.jsonl`


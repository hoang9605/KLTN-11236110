r"""Gom số liệu của quy trình gán nhãn RE bằng LLM (re_v3, 24-25/11/2026) vào một file JSON cho báo cáo.

Chỉ đọc kết quả đã có (manifest, phiếu chuyên gia đã chấm, so_sanh_voi_chuyen_gia.json), không gọi API.

  .venv\Scripts\python.exe -X utf8 scripts/re_dataset/summarize_labeling.py
Ghi ra outputs/re_811_gold/labeling_summary.json
"""
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
S = ROOT / "re_v3" / "data" / "silver"
OUT = ROOT / "outputs" / "re_811_gold" / "labeling_summary.json"


def J(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def JL(p):
    return [json.loads(x) for x in Path(p).read_text(encoding="utf-8").splitlines() if x.strip()]


def cmp(name):
    d = J(S / name / "so_sanh_voi_chuyen_gia.json")
    return d.get("metrics", d)


def pick(m):
    return {k: m[k] for k in ("n", "acc", "precision", "recall", "f1") if k in m}


def man(name):
    return J(S / name / f"{name}.manifest.json")


def score(name):
    d = J(S / name / f"{name}_score.json")
    return {"all": d["ai_accuracy"]["ALL"], "precision": d["ai_precision"], "recall": d["ai_recall"],
            "kappa_ai": d["kappa_ai_vs_expert"], "kappa_rule": d["kappa_rule_vs_expert"],
            "flags": d["flag_effectiveness"], "reviewer": d.get("reviewer"),
            "by_relation": {k.split("=", 1)[1]: v for k, v in d["ai_accuracy"].items()
                            if k.startswith("relation=") and "|" not in k},
            "by_relation_polarity": {k.split("=", 1)[1]: v for k, v in d["ai_accuracy"].items()
                                     if k.startswith("relation=") and "|" in k}}


def flips(stats):
    return {k[5:]: v for k, v in stats.items() if k.startswith("flip:")}


def main():
    p4c, d4c, t4c = cmp("pilot_label_v4_critic"), cmp("dev_label_v4_critic"), cmp("test_label_v4_critic")
    rounds = [("v1", cmp("pilot_label_v2")["v1"]), ("v2", cmp("pilot_label_v2")["pilot_label_v2"]),
              ("v3", cmp("pilot_label_v3")["pilot_label_v3"]), ("v4", p4c["pilot_label_v4"]),
              ("v4_critic", p4c["pilot_label_v4_critic"])]
    runs = {n: man(n) for n in ("train_label_v4", "train_label_v4_critic", "dev_label_v4", "dev_label_v4_critic",
                                "pilot_label_v4_critic", "test_label_v4", "test_label_v4_critic")}
    gold_train = JL(S / "train_label_v4_critic" / "train_label_v4_critic_gold.jsonl")
    gold_test = JL(S / "test_label_v4_critic" / "test_label_v4_critic_expert_final.jsonl")
    split = J(ROOT / "data" / "re_vietmed_811_v1" / "manifest.json")
    merge = J(S / "train_label_v4_critic" / "merge_pilot_gold.json")
    out = {
        "split": {k: {x: v[x] for x in ("sentences", "sentences_with_pairs", "pairs", "pairs_by_type", "from_original_split")}
                  for k, v in split["splits"].items()},
        "split_seed": split["seed"],
        "prompt_rounds_pilot": [{"version": k, **pick(v)} for k, v in rounds],
        "dev": {"v3": pick(d4c.get("ai_in_sheet", {})), "v4": pick(d4c["dev_label_v4"]), "v4_critic": pick(d4c["dev_label_v4_critic"])},
        "test": {"v4": pick(t4c["test_label_v4"]), "v4_critic": pick(t4c["test_label_v4_critic"])},
        "test_score": score("test_label_v4_critic"),
        "train_score": score("train_label_v4_critic"),
        "runs": {n: {"model": m.get("model"), "sentences": m.get("sentences"), "pairs": m.get("pairs"),
                     "calls_per_sentence": m.get("calls_per_sentence"), "tiers": m.get("tiers"),
                     "selected": m.get("selected"), "why": m.get("why"),
                     "flips": flips(m.get("stats") or {}), "low_conf_ignored": (m.get("stats") or {}).get("flip_low_conf_ignored"),
                     "usd": m["usage"]["usd_this_run"], "api_calls": m["usage"].get("api_calls")} for n, m in runs.items()},
        "merge_pilot": merge,
        "dataset": {
            "train": {"sentences": len(gold_train), "pairs": sum(len(r["relations"]) for r in gold_train),
                      "labels": dict(Counter(x["label"] for r in gold_train for x in r["relations"])),
                      "origin": dict(Counter(x.get("label_origin") for r in gold_train for x in r["relations"]))},
            "test": {"sentences_with_pairs": len(gold_test), "pairs": sum(len(r["relations"]) for r in gold_test),
                     "labels": dict(Counter(x["label"] for r in gold_test for x in r["relations"])),
                     "human_verified": sum(r["human_verified"] for r in gold_test)},
        },
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps({k: out[k] for k in ("prompt_rounds_pilot", "dev", "test", "dataset")}, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()

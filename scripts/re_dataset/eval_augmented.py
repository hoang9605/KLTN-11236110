r"""Score the translated-English augmentation experiment against the deployed recipe.

Baseline  = ViHealthBERT trained on the VietMed pairs only (bert_deployed_predictions.json,
            the model in Model/vihealthbert-re-v1; same hyper-parameters and seeds).
Variants  = the same recipe plus translated English pairs (bert_aug_<tag>_predictions.json
            from bert_re.py --extra-train). Relations with no positive training pair are
            reported as NO_RELATION, as the deployed extractor does.

Each is scored alone and in union with the rules on the three evaluation sets. The
difference in positive micro-F1 (variant - baseline) gets a paired bootstrap over sentence
groups (1000 resamples, seed 13): the same resampled sentences score both systems.
The decision rule was fixed before training: the deployed model changes only if the
variant ∪ rules is better on BOTH the golden test (v1.1) and the random test and neither
paired interval lies entirely below zero.
Output: <out>/augmented.json, <out>/augmented.md

    .venv\Scripts\python.exe -X utf8 scripts/re_dataset/eval_augmented.py --out outputs/re_benchmark_2026-11-08
"""
import argparse
import json
import random
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from benchmark import block, load_data, union  # noqa: E402
from relation_extraction.data import NEGATIVE, RELATIONS  # noqa: E402
from relation_extraction.rules import RuleRelationExtractor  # noqa: E402
from train_eval import score  # noqa: E402

TEST_NAMES = {"v1_1": "golden_test", "v1": "golden_test_v1_original", "random_v1": "random_test"}
TAGS = {"biotext": "BioText (điều trị, phòng bệnh, tác dụng phụ)", "biotext_ade": "BioText + ADE (thêm thuốc–liều)"}


def labels(pairs, prob, supported):
    return [p["allowed_relation"] if prob[p["uid"]] >= 0.5 and p["allowed_relation"] in supported else NEGATIVE
            for p in pairs]


def paired(pairs, a, b, n=1000, seed=13):
    groups = defaultdict(list)
    for p, x, y in zip(pairs, a, b):
        groups[p["group"]].append((p["label"], x, y))
    keys, rng, d = list(groups), random.Random(seed), []
    for _ in range(n):
        s = [r for _ in keys for r in groups[keys[rng.randrange(len(keys))]]]
        g = [r[0] for r in s]
        d.append(score(g, [r[1] for r in s])["positive_micro"]["f1"] - score(g, [r[2] for r in s])["positive_micro"]["f1"])
    d.sort()
    return [round(d[int(.025 * n)], 3), round(d[int(.975 * n) - 1], 3)]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--tags", nargs="+", metavar="TAG=MÔ_TẢ",
                    help="biến thể cần chấm (mặc định: biotext, biotext_ade)")
    ap.add_argument("--name", default="augmented", help="tên file kết quả: <out>/<name>.json, <name>.md")
    ap.add_argument("--title", default="Thêm dữ liệu tiếng Anh dịch sang tiếng Việt vào huấn luyện RE")
    ap.add_argument("--variant-desc", default="thêm cặp dịch từ `data/re_translated_en_v1` (chỉ dùng để huấn luyện)")
    a = ap.parse_args()
    if a.tags:
        TAGS.clear()
        TAGS.update(dict(t.split("=", 1) if "=" in t else (t, t) for t in a.tags))
    out = Path(a.out)
    _, tests = load_data()
    rules = RuleRelationExtractor()
    base = json.loads((out / "bert_deployed_predictions.json").read_text(encoding="utf-8"))
    base_supported = set(base["meta"]["supported_relations"])
    variants = {}
    for tag in TAGS:
        f = out / f"bert_aug_{tag}_predictions.json"
        if f.exists():
            variants[tag] = json.loads(f.read_text(encoding="utf-8"))
    report = {"baseline": "bert_deployed_predictions.json", "variants": {t: v["meta"] for t, v in variants.items()},
              "decision_rule": "change the deployed model only if variant ∪ rules beats baseline ∪ rules on both golden_test "
                               "and random_test and neither paired 95% interval is entirely below zero", "sets": {}}
    for key, pairs in tests.items():
        rule = [r["label"] for r in rules.predict_pairs(pairs)]
        b = labels(pairs, base["prob"], base_supported)
        preds = {"baseline": b, "baseline+rules": union(b, rule), "rules": rule}
        for tag, v in variants.items():
            sup = {k.split(":")[0] for k, c in v["meta"]["extra_by_label"].items() if not k.endswith(NEGATIVE)} | base_supported
            y = labels(pairs, v["prob"], sup)
            preds[tag] = y
            preds[f"{tag}+rules"] = union(y, rule)
        sc = block(pairs, preds)
        diffs = {}
        for tag in variants:
            diffs[tag] = {"alone": paired(pairs, preds[tag], preds["baseline"]),
                          "with_rules": paired(pairs, preds[f"{tag}+rules"], preds["baseline+rules"])}
        diag = {}
        neg = [p for p in pairs if p["label"] == NEGATIVE]
        for tag, v in variants.items():
            y = preds[tag]
            new_fp = [p for p, x, z in zip(pairs, y, b) if x != NEGATIVE and z == NEGATIVE and p["label"] == NEGATIVE]
            diag[tag] = {"new_false_positives": len(new_fp),
                         "new_false_positives_by_relation": dict(Counter(p["allowed_relation"] for p in new_fp)),
                         "new_true_positives": sum(x != NEGATIVE and z == NEGATIVE and p["label"] != NEGATIVE
                                                   for p, x, z in zip(pairs, y, b)),
                         "lost_true_positives": sum(x == NEGATIVE and z != NEGATIVE and p["label"] != NEGATIVE
                                                    for p, x, z in zip(pairs, y, b)),
                         "mean_prob_on_negatives": round(sum(v["prob"][p["uid"]] for p in neg) / len(neg), 3),
                         "mean_prob_on_negatives_baseline": round(sum(base["prob"][p["uid"]] for p in neg) / len(neg), 3)}
        report["sets"][TEST_NAMES[key]] = {"pairs": len(pairs), "scores": sc, "paired_diff_ci95": diffs, "diagnostics": diag}
    decision = {}
    for tag in variants:
        ok = all(report["sets"][s]["scores"][f"{tag}+rules"]["positive_micro"]["f1"]
                 > report["sets"][s]["scores"]["baseline+rules"]["positive_micro"]["f1"]
                 and report["sets"][s]["paired_diff_ci95"][tag]["with_rules"][1] >= 0
                 for s in ("golden_test", "random_test"))
        decision[tag] = "thay mô hình triển khai" if ok else "giữ mô hình triển khai"
    report["decision"] = decision
    (out / f"{a.name}.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    def f(x):
        return f"{x:.3f}"
    L = [f"# {a.title}", "",
         "Gốc: ViHealthBERT 3 seed chỉ học trên dữ liệu VietMed (mô hình đang triển khai). "
         f"Biến thể: cùng công thức, {a.variant_desc}. "
         "Nhãn mọi tập test là nhãn AI, chưa có bác sĩ duyệt.", "",
         "| Tập | Hệ | P | R | F1 (KTC 95%) | Chênh F1 so với gốc (KTC 95% ghép cặp) |", "|---|---|---:|---:|---:|---:|"]
    for name, s in report["sets"].items():
        for m in ["rules", "baseline", "baseline+rules"] + [x for t in variants for x in (t, f"{t}+rules")]:
            pm = s["scores"][m]["positive_micro"]
            ci = s["scores"][m]["positive_micro_f1_ci95"]
            ref = "baseline+rules" if m.endswith("+rules") else "baseline"
            dd = ""
            t = m[:-6] if m.endswith("+rules") else m
            if t in variants:
                d = pm["f1"] - s["scores"][ref]["positive_micro"]["f1"]
                c = s["paired_diff_ci95"][t]["with_rules" if m.endswith("+rules") else "alone"]
                dd = f"{d:+.3f} ({c[0]:+.3f} – {c[1]:+.3f})"
            L.append(f"| {name} | {m} | {f(pm['precision'])} | {f(pm['recall'])} | {f(pm['f1'])} ({ci[0]:.2f}–{ci[1]:.2f}) | {dd} |")
    L += ["", "F1 theo quan hệ (hệ ∪ luật):", "", "| Tập | Quan hệ | Hỗ trợ | Gốc ∪ luật | " + " | ".join(f"{t} ∪ luật" for t in variants) + " |",
          "|---|---|---:|---:|" + "---:|" * len(variants)]
    for name, s in report["sets"].items():
        for rel in RELATIONS:
            r0 = s["scores"]["baseline+rules"]["per_relation"][rel]
            if not r0["support"]:
                continue
            L.append(f"| {name} | {rel} | {r0['support']} | {f(r0['f1'])} | "
                     + " | ".join(f(s["scores"][f"{t}+rules"]["per_relation"][rel]["f1"]) for t in variants) + " |")
    L += ["", "Chẩn đoán (mô hình một mình, so với gốc):", ""]
    for name, s in report["sets"].items():
        for tag, d in s["diagnostics"].items():
            L.append(f"- {name}, {tag}: {d['new_false_positives']} cặp âm mới bị đoán dương "
                     f"({', '.join(f'{k} {v}' for k, v in sorted(d['new_false_positives_by_relation'].items()))}), "
                     f"{d['new_true_positives']} cặp dương mới đoán đúng, {d['lost_true_positives']} cặp dương bị mất; "
                     f"xác suất trung bình trên cặp âm {d['mean_prob_on_negatives_baseline']} → {d['mean_prob_on_negatives']}")
    L += ["", "Quyết định (quy tắc định trước khi huấn luyện): " + report["decision_rule"], ""]
    L += [f"- {TAGS[t]}: {d}" for t, d in decision.items()]
    (out / f"{a.name}.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    print("\n".join(L))


if __name__ == "__main__":
    main()

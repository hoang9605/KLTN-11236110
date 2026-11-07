"""So sánh baseline luật và TF-IDF+LogReg cho RE trên cùng dữ liệu (nhãn AI rà soát, 178 cặp).

  python scripts/re_compare_baselines.py [--data ...annotations_reviewed_600.jsonl]

(a) split seed 42 như relation_extraction/README.md; (b) cross-validation 5-fold theo nhóm văn bản,
gộp dự đoán ngoài fold; CI95 bootstrap theo nhóm (1000 lần). Luật không học từ dữ liệu.
"""
import argparse, json, random, sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from relation_extraction.data import NEGATIVE, RELATIONS, load_pairs, split_pairs  # noqa: E402
from relation_extraction.model import RelationExtractor  # noqa: E402
from relation_extraction.rules import RuleRelationExtractor  # noqa: E402


def score(gold, pred):
    out, tot = {}, Counter()
    for rel in RELATIONS:
        tp = sum(g == rel and p == rel for g, p in zip(gold, pred))
        fp = sum(g != rel and p == rel for g, p in zip(gold, pred))
        fn = sum(g == rel and p != rel for g, p in zip(gold, pred))
        tot.update(tp=tp, fp=fp, fn=fn)
        out[rel] = prf(tp, fp, fn)
    return {"positive_micro": prf(tot["tp"], tot["fp"], tot["fn"]), "per_relation": out}


def prf(tp, fp, fn):
    p = tp / (tp + fp) if tp + fp else 0.0; r = tp / (tp + fn) if tp + fn else 0.0
    return {"precision": round(p, 3), "recall": round(r, 3), "f1": round(2 * p * r / (p + r), 3) if p + r else 0.0,
            "tp": tp, "fp": fp, "fn": fn, "support": tp + fn}


def bootstrap(rows, n=1000, seed=13):
    groups = defaultdict(list)
    for r in rows: groups[r["group"]].append(r)
    keys, rng, vals = list(groups), random.Random(seed), []
    for _ in range(n):
        s = [x for _ in keys for x in groups[keys[rng.randrange(len(keys))]]]
        vals.append(score([x["gold"] for x in s], [x["pred"] for x in s])["positive_micro"]["f1"])
    vals.sort(); return [round(vals[int(.025 * n)], 3), round(vals[int(.975 * n) - 1], 3)]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", default=str(ROOT / "outputs/vietmed_600_RE_review/review_2026_10_15/annotations_reviewed_600.jsonl"))
    ap.add_argument("--out", default=str(ROOT / "outputs/re_baselines"))
    a = ap.parse_args()
    pairs, audit = load_pairs(a.data, allow_ai=True)
    ents = {}
    for line in Path(a.data).read_text(encoding="utf-8-sig").splitlines():
        if line.strip():
            r = json.loads(line); ents[r["id"]] = r["entities"]
    for p in pairs:
        # dùng đúng đối tượng head/tail trong danh sách để kiểm tra thực thể chen giữa
        p["entities"] = [p["head"] if e["id"] == p["head"]["id"] else p["tail"] if e["id"] == p["tail"]["id"] else e
                         for e in ents[p["sample_id"]]]
    rules = RuleRelationExtractor()
    human = all(p["human_verified"] and p["training_eligible"] for p in pairs)
    source_vi = "người duyệt xác nhận" if human else "AI rà soát, chưa bác sĩ xác nhận"
    report = {"data": a.data, "audit": audit, "label_source": source_vi,
              "pairs": len(pairs), "labels": dict(Counter(p["label"] for p in pairs))}

    split = split_pairs(pairs, seed=42)
    lr = RelationExtractor(seed=42).fit(split["train"])
    report["seed42_split"] = {}
    for name in ("dev", "test"):
        gold = [p["label"] for p in split[name]]
        lp = [x["label"] or "UNSUPPORTED" for x in lr.predict_pairs(split[name])]
        rp = [x["label"] for x in rules.predict_pairs(split[name])]
        report["seed42_split"][name] = {"pairs": len(gold), "logreg": score(gold, lp), "rules": score(gold, rp)}

    groups = sorted({p["group"] for p in pairs}); random.Random(42).shuffle(groups)
    fold_of = {g: i % 5 for i, g in enumerate(groups)}
    oof = {"logreg": [], "rules": []}
    for k in range(5):
        tr = [p for p in pairs if fold_of[p["group"]] != k]; te = [p for p in pairs if fold_of[p["group"]] == k]
        if not te: continue
        try:
            m = RelationExtractor(seed=42).fit(tr); lp = [x["label"] or "UNSUPPORTED" for x in m.predict_pairs(te)]
        except ValueError:
            lp = [NEGATIVE] * len(te)
        rp = [x["label"] for x in rules.predict_pairs(te)]
        for p, l, r in zip(te, lp, rp):
            oof["logreg"].append({"group": p["group"], "gold": p["label"], "pred": l})
            oof["rules"].append({"group": p["group"], "gold": p["label"], "pred": r})
    report["cv5_grouped"] = {m: {**score([x["gold"] for x in rows], [x["pred"] for x in rows]),
                                 "positive_micro_f1_ci95": bootstrap(rows)} for m, rows in oof.items()}
    out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
    (out / "report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    L = [f"# So sánh baseline RE (nhãn {report['label_source']}, {report['pairs']} cặp)", "",
         "| Thiết lập | Phương pháp | P | R | F1 | CI95 F1 |", "|---|---|---:|---:|---:|---|"]
    for name in ("dev", "test"):
        for m in ("rules", "logreg"):
            s = report["seed42_split"][name][m]["positive_micro"]
            L.append(f"| seed42 {name} ({report['seed42_split'][name]['pairs']} cặp) | {m} | {s['precision']:.3f} | {s['recall']:.3f} | {s['f1']:.3f} | — |")
    for m in ("rules", "logreg"):
        d = report["cv5_grouped"][m]; s = d["positive_micro"]
        L.append(f"| CV 5-fold theo nhóm ({report['pairs']} cặp) | {m} | {s['precision']:.3f} | {s['recall']:.3f} | {s['f1']:.3f} | {d['positive_micro_f1_ci95'][0]:.3f}–{d['positive_micro_f1_ci95'][1]:.3f} |")
    L += ["", "## CV theo quan hệ (F1, support)", "", "| Quan hệ | Luật | LogReg | Support |", "|---|---:|---:|---:|"]
    for rel in RELATIONS:
        r = report["cv5_grouped"]["rules"]["per_relation"][rel]; l = report["cv5_grouped"]["logreg"]["per_relation"][rel]
        L.append(f"| {rel} | {r['f1']:.3f} | {l['f1']:.3f} | {r['support']} |")
    (out / "summary.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    print("\n".join(L))


if __name__ == "__main__":
    main()

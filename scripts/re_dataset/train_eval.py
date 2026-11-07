r"""Train the RE model on gold v1 + AI v2 and compare it with the earlier model and the rules.

Data
  v1   data/re_gold_v1/annotations_gold_v1.jsonl  (600 train sentences, paper-reviewed)
  v2   data/re_ai_v2/annotations_ai_v2.jsonl      (199 train sentences, AI labels, two passes)
  held-out test: data/golden_test/v1 (150 passages of the VietMed *test* split; AI labels
       from an earlier session, independent of v2). Only pairs whose two entities were
       judged correct (verdict DUNG) and whose label is not CHUA_RO are scored.

Methods
  rules     relation_extraction.rules (written from the guideline, never fitted)
  model_v1  TF-IDF + LogReg trained on v1 only (the current deployed model's recipe)
  model_v2  same recipe trained on v1 + v2
  hybrid    model_v2 for relations it supports, rules for the rest
  union     positive when model_v2 or the rules say positive (rules alone where model_v2 is unsupported)
  The KG extractor is the method with the best CV F1; the golden test is reported, never used to choose.

Evaluation: 5-fold CV grouped by normalized text over v1+v2 (model_v1 sees only the v1
part of each training fold), and the held-out golden test. Positive micro P/R/F1, per
relation, bootstrap CI95 over text groups.

    .venv\Scripts\python.exe -X utf8 scripts/re_dataset/train_eval.py --out outputs/re_ai_v2
"""
import argparse
import json
import os
import random
import sys
from collections import Counter, defaultdict
from pathlib import Path

os.environ.setdefault("OMP_NUM_THREADS", "1")
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from relation_extraction.data import NEGATIVE, RELATIONS, load_pairs, mark_pair, text_group  # noqa: E402
from relation_extraction.model import RelationExtractor  # noqa: E402
from relation_extraction.rules import RuleRelationExtractor  # noqa: E402

V1 = ROOT / "data/re_gold_v1/annotations_gold_v1.jsonl"
V2 = ROOT / "data/re_ai_v2/annotations_ai_v2.jsonl"
GT = ROOT / "data/golden_test/v1"
METHODS = ("rules", "model_v1", "model_v2", "hybrid", "union")


def prf(tp, fp, fn):
    p = tp / (tp + fp) if tp + fp else 0.0
    r = tp / (tp + fn) if tp + fn else 0.0
    return {"precision": round(p, 3), "recall": round(r, 3), "f1": round(2 * p * r / (p + r), 3) if p + r else 0.0,
            "tp": tp, "fp": fp, "fn": fn, "support": tp + fn}


def score(gold, pred):
    out, tot = {}, Counter()
    for rel in RELATIONS:
        tp = sum(g == rel and p == rel for g, p in zip(gold, pred))
        fp = sum(g != rel and p == rel for g, p in zip(gold, pred))
        fn = sum(g == rel and p != rel for g, p in zip(gold, pred))
        tot.update(tp=tp, fp=fp, fn=fn)
        out[rel] = prf(tp, fp, fn)
    return {"positive_micro": prf(tot["tp"], tot["fp"], tot["fn"]), "per_relation": out}


def bootstrap(rows, n=1000, seed=13):
    groups = defaultdict(list)
    for r in rows:
        groups[r["group"]].append(r)
    keys, rng, vals = list(groups), random.Random(seed), []
    for _ in range(n):
        s = [x for _ in keys for x in groups[keys[rng.randrange(len(keys))]]]
        vals.append(score([x["gold"] for x in s], [x["pred"] for x in s])["positive_micro"]["f1"])
    vals.sort()
    return [round(vals[int(.025 * n)], 3), round(vals[int(.975 * n) - 1], 3)]


def attach_entities(pairs, path):
    ents = {}
    for line in Path(path).read_text(encoding="utf-8-sig").splitlines():
        if line.strip():
            r = json.loads(line)
            ents[r["id"]] = r["entities"]
    for p in pairs:  # the rules need the sentence's other entities to detect blockers
        p["entities"] = [p["head"] if e["id"] == p["head"]["id"] else p["tail"] if e["id"] == p["tail"]["id"] else e
                         for e in ents[p["sample_id"]]]


def golden_pairs():
    cands = {json.loads(l)["id"]: json.loads(l) for l in (GT / "candidates.jsonl").read_text(encoding="utf-8").splitlines()}
    out, audit = [], Counter()
    for line in (GT / "ai_labels.jsonl").read_text(encoding="utf-8").splitlines():
        lab = json.loads(line)
        c = cands[lab["id"]]
        ents = {e["id"]: e for e in c["entities"]}
        ok = {k for k, v in lab["entities"].items() if v["verdict"] == "DUNG"}
        for rel in c["relations"]:
            label = lab["relations"].get(rel["id"], {}).get("label")
            if label in (None, "CHUA_RO"):
                audit["skip_unlabelled_or_unclear"] += 1; continue
            if not {rel["head"], rel["tail"]} <= ok:
                audit["skip_entity_not_DUNG"] += 1; continue
            h, t = ents[rel["head"]], ents[rel["tail"]]
            out.append({"sample_id": c["id"], "group": text_group(c["text"]), "text": c["text"], "head": h, "tail": t,
                        "allowed_relation": rel["allowed_relation"], "label": label,
                        "features": mark_pair(c["text"], h, t),
                        "entities": [ents[k] for k in ok if k in ents]})
    audit["pairs"] = len(out)
    return out, dict(audit)


def predict_all(models, rules, pairs):
    preds = {"rules": [x["label"] for x in rules.predict_pairs(pairs)]}
    for name in ("model_v1", "model_v2"):
        m = models.get(name)
        preds[name] = [x["label"] or "UNSUPPORTED" for x in m.predict_pairs(pairs)] if m else [NEGATIVE] * len(pairs)
    hyb = []
    m2 = models.get("model_v2")
    for p, mv, rv in zip(pairs, preds["model_v2"], preds["rules"]):
        supported = m2 is not None and p["allowed_relation"] in m2.supported_relations
        hyb.append(mv if supported else rv)
    preds["hybrid"] = hyb
    preds["union"] = [mv if mv not in (NEGATIVE, "UNSUPPORTED") else rv
                      for mv, rv in zip(preds["model_v2"], preds["rules"])]
    return preds


def fit(pairs):
    try:
        return RelationExtractor(seed=42).fit(pairs)
    except ValueError:
        return None


def table(block, title, n_pairs):
    L = [f"### {title} ({n_pairs} cặp)", "", "| Phương pháp | P | R | F1 | CI95 F1 |", "|---|---:|---:|---:|---|"]
    for m in METHODS:
        s = block[m]["positive_micro"]
        ci = block[m]["positive_micro_f1_ci95"]
        L.append(f"| {m} | {s['precision']:.3f} | {s['recall']:.3f} | {s['f1']:.3f} | {ci[0]:.3f}–{ci[1]:.3f} |")
    L += ["", "| Quan hệ | Support | " + " | ".join(f"F1 {m}" for m in METHODS) + " |",
          "|---|---:|" + "---:|" * len(METHODS)]
    for rel in RELATIONS:
        sup = block["rules"]["per_relation"][rel]["support"]
        L.append(f"| {rel} | {sup} | " + " | ".join(f"{block[m]['per_relation'][rel]['f1']:.3f}" for m in METHODS) + " |")
    return L + [""]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)

    v1, audit1 = load_pairs(V1, allow_ai=True)
    v2, audit2 = load_pairs(V2, allow_ai=True)
    attach_entities(v1, V1)
    attach_entities(v2, V2)
    for p in v1:
        p["source"] = "v1"
    for p in v2:
        p["source"] = "v2"
    both = v1 + v2
    overlap = {p["group"] for p in v1} & {p["group"] for p in v2}
    gold_test, gt_audit = golden_pairs()
    leak = {p["group"] for p in both} & {p["group"] for p in gold_test}
    rules = RuleRelationExtractor()
    report = {"data": {"v1": audit1, "v2": audit2, "v1_v2_text_overlap": len(overlap),
                       "train_test_text_overlap": len(leak), "golden_test": gt_audit,
                       "labels_v1": dict(Counter(p["label"] for p in v1)),
                       "labels_v2": dict(Counter(p["label"] for p in v2)),
                       "labels_golden_test": dict(Counter(p["label"] for p in gold_test))}}

    groups = sorted({p["group"] for p in both})
    random.Random(42).shuffle(groups)
    fold = {g: i % 5 for i, g in enumerate(groups)}
    oof = {m: [] for m in METHODS}
    for k in range(5):
        tr = [p for p in both if fold[p["group"]] != k]
        te = [p for p in both if fold[p["group"]] == k]
        models = {"model_v1": fit([p for p in tr if p["source"] == "v1"]), "model_v2": fit(tr)}
        preds = predict_all(models, rules, te)
        for m in METHODS:
            oof[m] += [{"group": p["group"], "gold": p["label"], "pred": y} for p, y in zip(te, preds[m])]
    report["cv5"] = {m: {**score([x["gold"] for x in rows], [x["pred"] for x in rows]),
                         "positive_micro_f1_ci95": bootstrap(rows)} for m, rows in oof.items()}

    final = {"model_v1": fit(v1), "model_v2": fit(both)}
    preds = predict_all(final, rules, gold_test)
    gold = [p["label"] for p in gold_test]
    report["golden_test"] = {m: {**score(gold, preds[m]),
                                 "positive_micro_f1_ci95": bootstrap(
                                     [{"group": p["group"], "gold": p["label"], "pred": y}
                                      for p, y in zip(gold_test, preds[m])])} for m in METHODS}
    with open(out / "golden_test_predictions.jsonl", "w", encoding="utf-8") as fh:
        for i, p in enumerate(gold_test):
            fh.write(json.dumps({"sample_id": p["sample_id"], "head": p["head"]["text"], "tail": p["tail"]["text"],
                                 "allowed_relation": p["allowed_relation"], "gold_ai": p["label"],
                                 **{m: preds[m][i] for m in METHODS}}, ensure_ascii=False) + "\n")

    best = max(("rules", "model_v2", "hybrid", "union"), key=lambda m: report["cv5"][m]["positive_micro"]["f1"])
    report["selected_by_cv"] = best
    model = final["model_v2"]
    model.metadata = {"label_source": "AI_provisional", "allow_ai_labels": True,
                      "training_data": [str(V1.relative_to(ROOT)), str(V2.relative_to(ROOT))],
                      "model": "character TF-IDF (2,5), balanced LogisticRegression C=1, threshold=0.5",
                      "pairs": len(both), "labels": dict(Counter(p["label"] for p in both)),
                      "supported_relations": model.supported_relations,
                      "note": "v1 paper-reviewed by a human (reviewer name not recorded); v2 AI-labelled, not yet reviewed"}
    model.save(out / "model.joblib")
    report["final_model"] = model.metadata
    (out / "report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    L = ["# Relation Extraction: mô hình v2 (gold v1 + nhãn AI v2)", "",
         "> Nhãn v2 và nhãn của golden test là nhãn AI, **chưa có bác sĩ duyệt**. Số liệu là tạm thời.", "",
         f"- Huấn luyện: v1 {len(v1)} cặp {dict(Counter(p['label'] for p in v1))}; "
         f"v2 {len(v2)} cặp {dict(Counter(p['label'] for p in v2))}.",
         f"- Trùng văn bản v1–v2: {len(overlap)}; trùng giữa dữ liệu huấn luyện và golden test: {len(leak)}.",
         f"- Golden test (split test VietMed, độc lập với dữ liệu huấn luyện): {len(gold_test)} cặp, "
         f"{dict(Counter(gold))}.", "",
         "- `rules`: luật viết từ hướng dẫn gán nhãn, không học. `model_v1`: TF-IDF + LogReg chỉ học v1 (mô hình đang dùng). "
         "`model_v2`: cùng công thức, học v1 + v2. `hybrid`: model_v2 cho quan hệ nó hỗ trợ, luật cho phần còn lại. "
         "`union`: dương nếu model_v2 hoặc luật nói dương.", ""]
    L += table(report["cv5"], "CV 5-fold theo nhóm văn bản trên v1 + v2", len(both))
    L += table(report["golden_test"], "Golden test (held-out, split test)", len(gold_test))
    L += [f"**Cách được chọn theo CV (dùng cho knowledge graph): `{best}`.** Golden test chỉ để báo cáo.", "",
          f"Mô hình cuối (`model.joblib`) học trên toàn bộ {len(both)} cặp; hỗ trợ: {', '.join(model.supported_relations)}."]
    (out / "summary.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    print("\n".join(L))


if __name__ == "__main__":
    main()

r"""RE benchmark: every baseline and model on the same data, folds and test set.

Data: gold v1 + RE v2 (train split, 5-fold CV grouped by normalized text, the same
fold assignment as train_eval.py) and the held-out golden test (VietMed test split).
Each pair has exactly one type-allowed relation, so every method answers
"positive (that relation) or NO_RELATION".

Baselines (no learning)
  majority     always NO_RELATION (the majority class)
  cooccur      every type-compatible pair in a sentence is positive
  nearest      positive iff the tail is the closest entity of its type to the head
               and the head the closest of its type to the tail (mutual nearest)
  rules        guideline rules, relation_extraction/rules.py
Learned (fitted on the training folds only)
  feat_lr      hand-built features (relation, distance, order, words between, entity
               types in between) + balanced LogisticRegression
  tfidf_svm    character TF-IDF (2,5) on the marked sentence + balanced LinearSVC
  tfidf_lr     character TF-IDF (2,5) + balanced LogisticRegression (the current model)
  bert         ViHealthBERT with typed entity markers (scripts/re_dataset/bert_re.py,
               run on GPU; merged here from its predictions file if present)
Combinations
  tfidf_lr+rules, bert+rules   union: positive when either says positive

    .venv\Scripts\python.exe -X utf8 scripts/re_dataset/benchmark.py --out outputs/re_benchmark_2026-11-08
"""
import argparse
import json
import random
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from train_eval import (V1, V2, attach_entities, bootstrap, golden_pairs, score)  # noqa: E402
from relation_extraction.data import NEGATIVE, RELATIONS, load_pairs  # noqa: E402
from relation_extraction.model import RelationExtractor  # noqa: E402
from relation_extraction.rules import RuleRelationExtractor  # noqa: E402

RANDOM_TEST = Path(__file__).resolve().parents[2] / "data/re_test_random_v1/annotations.jsonl"
BASELINES = ("majority", "cooccur", "nearest", "rules")
LEARNED = ("feat_lr", "tfidf_svm", "tfidf_lr")
NAMES = {
    "majority": "Luôn NO_RELATION", "cooccur": "Đồng xuất hiện (mọi cặp đúng kiểu)",
    "nearest": "Ghép cặp gần nhất hai chiều", "rules": "Luật từ hướng dẫn",
    "feat_lr": "Đặc trưng thủ công + LogReg", "tfidf_svm": "TF-IDF ký tự + SVM",
    "tfidf_lr": "TF-IDF ký tự + LogReg", "bert": "ViHealthBERT + marker",
    "tfidf_lr+rules": "TF-IDF + LogReg ∪ luật", "bert+rules": "ViHealthBERT ∪ luật",
}


def load_data():
    v1, _ = load_pairs(V1, allow_ai=True)
    v2, _ = load_pairs(V2, allow_ai=True)
    attach_entities(v1, V1)
    attach_entities(v2, V2)
    for p in v1:
        p["source"] = "v1"
    for p in v2:
        p["source"] = "v2"
    both = v1 + v2
    tests = {"v1_1": golden_pairs("ai_labels_v1_1.jsonl")[0], "v1": golden_pairs("ai_labels.jsonl")[0]}
    if RANDOM_TEST.exists():  # natural-distribution test set, scripts/re_dataset/build_random_test.py
        rt, _ = load_pairs(RANDOM_TEST, allow_ai=True)
        attach_entities(rt, RANDOM_TEST)
        tests["random_v1"] = rt
    for p in both + [p for t in tests.values() for p in t]:
        p["uid"] = pair_uid(p)
    return both, tests


def pair_uid(p):
    return f"{p['sample_id']}:{p['head']['id']}:{p['tail']['id']}:{p['allowed_relation']}"


def folds(pairs, k=5, seed=42):
    """Same assignment as train_eval.py: sorted groups, shuffled with seed 42, i % 5."""
    groups = sorted({p["group"] for p in pairs})
    random.Random(seed).shuffle(groups)
    fold = {g: i % k for i, g in enumerate(groups)}
    return [fold[p["group"]] for p in pairs]


# ---------------- baselines ----------------
def nearest(p):
    ents = p.get("entities") or [p["head"], p["tail"]]
    h, t = p["head"], p["tail"]

    def dist(a, b):
        return max(a["start"], b["start"]) - min(a["end"], b["end"])
    d = dist(h, t)
    closer_tail = any(e["label"] == t["label"] and e["id"] != t["id"] and dist(h, e) < d for e in ents)
    closer_head = any(e["label"] == h["label"] and e["id"] != h["id"] and dist(e, t) < d for e in ents)
    return p["allowed_relation"] if not (closer_tail or closer_head) else NEGATIVE


# ---------------- feature LR ----------------
def _w(s):
    return re.findall(r"\w+", s.lower())


def pair_features(p):
    h, t = p["head"], p["tail"]
    first, second = sorted((h, t), key=lambda e: e["start"])
    between = _w(p["text"][first["end"]:second["start"]])
    f = {f"rel={p['allowed_relation']}": 1, f"order={'ht' if first is h else 'th'}": 1,
         f"gap={min(len(between), 10)}": 1, "gap_num": min(len(between), 20) / 20}
    for w in between[:12]:
        f[f"bw={w}"] = 1
    for w in between[:2]:
        f[f"bw_first={w}"] = 1
    for e in p.get("entities") or []:
        if first["end"] <= e["start"] and e["end"] <= second["start"]:
            f[f"ent_between={e['label']}"] = 1
    before = _w(p["text"][:first["start"]])[-2:]
    for w in before:
        f[f"before={w}"] = 1
    return f


class FeatLR:
    def fit(self, pairs):
        from sklearn.feature_extraction import DictVectorizer
        from sklearn.linear_model import LogisticRegression
        self.v = DictVectorizer()
        y = [p["label"] != NEGATIVE for p in pairs]
        self.m = LogisticRegression(class_weight="balanced", max_iter=3000, C=1.0)
        self.m.fit(self.v.fit_transform([pair_features(p) for p in pairs]), y)
        self.seen = {p["allowed_relation"] for p in pairs if p["label"] != NEGATIVE}
        return self

    def predict(self, pairs):
        pr = self.m.predict_proba(self.v.transform([pair_features(p) for p in pairs]))[:, 1]
        return [p["allowed_relation"] if s >= 0.5 and p["allowed_relation"] in self.seen else NEGATIVE
                for p, s in zip(pairs, pr)]


class TfidfSVM:
    def fit(self, pairs):
        from sklearn.feature_extraction.text import TfidfVectorizer
        from sklearn.svm import LinearSVC
        self.v = TfidfVectorizer(analyzer="char", ngram_range=(2, 5), sublinear_tf=True, max_features=50000)
        self.m = LinearSVC(class_weight="balanced", C=1.0, random_state=42)
        self.m.fit(self.v.fit_transform([p["features"] for p in pairs]), [p["label"] for p in pairs])
        return self

    def predict(self, pairs):
        out = self.m.predict(self.v.transform([p["features"] for p in pairs]))
        return [y if y in (NEGATIVE, p["allowed_relation"]) else NEGATIVE for p, y in zip(pairs, out)]


def tfidf_lr(train):
    m = RelationExtractor(seed=42).fit(train)

    def pred(pairs):
        return [x["label"] if x["label"] else NEGATIVE for x in m.predict_pairs(pairs)]
    return pred


def predict_methods(train, test, rules):
    preds = {"majority": [NEGATIVE] * len(test),
             "cooccur": [p["allowed_relation"] for p in test],
             "nearest": [nearest(p) for p in test],
             "rules": [x["label"] for x in rules.predict_pairs(test)]}
    preds["feat_lr"] = FeatLR().fit(train).predict(test)
    preds["tfidf_svm"] = TfidfSVM().fit(train).predict(test)
    preds["tfidf_lr"] = tfidf_lr(train)(test)
    return preds


def union(a, b):
    return [x if x != NEGATIVE else y for x, y in zip(a, b)]


def block(pairs, preds):
    gold = [p["label"] for p in pairs]
    return {m: {**score(gold, y), "positive_micro_f1_ci95": bootstrap(
        [{"group": p["group"], "gold": p["label"], "pred": v} for p, v in zip(pairs, y)])}
        for m, y in preds.items()}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--bert", default=None, help="bert_predictions.json from bert_re.py (default: <out>/bert_predictions.json)")
    a = ap.parse_args()
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    both, tests = load_data()
    fl = folds(both)
    rules = RuleRelationExtractor()

    oof = {m: [None] * len(both) for m in BASELINES + LEARNED}
    for k in range(5):
        tr = [p for p, f in zip(both, fl) if f != k]
        idx = [i for i, f in enumerate(fl) if f == k]
        preds = predict_methods(tr, [both[i] for i in idx], rules)
        for m, ys in preds.items():
            for i, y in zip(idx, ys):
                oof[m][i] = y
    gts = {v: predict_methods(both, t, rules) for v, t in tests.items()}

    bert_path = Path(a.bert) if a.bert else out / "bert_predictions.json"
    bert_meta = None
    if bert_path.exists():
        b = json.loads(bert_path.read_text(encoding="utf-8"))
        oof["bert"] = [b["cv"][p["uid"]] for p in both]
        for v, t in tests.items():
            if all(p["uid"] in b["golden_test"] for p in t):
                gts[v]["bert"] = [b["golden_test"][p["uid"]] for p in t]
            else:
                print(f"bert: no predictions for test set {v} (rerun bert_re.py --final-only)")
        bert_meta = b.get("meta")
    for d in [oof] + list(gts.values()):
        d["tfidf_lr+rules"] = union(d["tfidf_lr"], d["rules"])
        if "bert" in d:
            d["bert+rules"] = union(d["bert"], d["rules"])
    test, gt = tests["v1_1"], gts["v1_1"]

    report = {"data": {"cv_pairs": len(both), "cv_labels": dict(Counter(p["label"] for p in both)),
                       "golden_test_pairs": len(test), "golden_test_labels": dict(Counter(p["label"] for p in test)),
                       "label_source": "v1 người duyệt + v2 AI; golden test nhãn AI (chưa bác sĩ duyệt)"},
              "names": NAMES, "bert_meta": bert_meta,
              "positive_rate": {"cv": round(sum(p["label"] != NEGATIVE for p in both) / len(both), 3),
                                **{f"golden_test_{v}": round(sum(p["label"] != NEGATIVE for p in t) / len(t), 3) for v, t in tests.items()}},
              "cv5": block(both, oof), "golden_test": block(test, gt),
              "golden_test_v1_original": block(tests["v1"], gts["v1"]),
              "golden_test_note": "golden_test = nhãn v1.1 (rà theo quy ước gold v1/RE v2); golden_test_v1_original = nhãn AI gốc"}
    if "random_v1" in tests:
        rt = tests["random_v1"]
        report["random_test"] = block(rt, gts["random_v1"])
        report["data"]["random_test_pairs"] = len(rt)
        report["data"]["random_test_labels"] = dict(Counter(p["label"] for p in rt))
        report["random_test_note"] = ("data/re_test_random_v1: 200 câu lấy ngẫu nhiên đều từ split test (không hạn mức), "
                                      "nhãn AI một lượt + đối chiếu luật, mù dự đoán mô hình")
    (out / "benchmark.json").write_text(json.dumps(report, ensure_ascii=False, indent=1), encoding="utf-8")

    order = [m for m in NAMES if m in report["cv5"]]
    L = ["# RE benchmark (CV 5 fold theo nhóm + golden test)", "",
         "> Nhãn v2 và golden test là nhãn AI, chưa có bác sĩ duyệt.", "",
         f"Tỉ lệ cặp dương: CV {report['positive_rate']['cv']}, golden test v1.1 {report['positive_rate']['golden_test_v1_1']} "
         f"({len(test)} cặp), bản gốc {report['positive_rate']['golden_test_v1']} ({len(tests['v1'])} cặp). GT = golden test v1.1.", "",
         "| Phương pháp | CV P | CV R | CV F1 | CV CI95 | GT P | GT R | GT F1 | GT CI95 |", "|---|---:|---:|---:|---|---:|---:|---:|---|"]
    for m in order:
        c, g = report["cv5"][m], report["golden_test"][m]
        L.append(f"| {NAMES[m]} | {c['positive_micro']['precision']:.3f} | {c['positive_micro']['recall']:.3f} | "
                 f"{c['positive_micro']['f1']:.3f} | {c['positive_micro_f1_ci95'][0]:.3f}–{c['positive_micro_f1_ci95'][1]:.3f} | "
                 f"{g['positive_micro']['precision']:.3f} | {g['positive_micro']['recall']:.3f} | {g['positive_micro']['f1']:.3f} | "
                 f"{g['positive_micro_f1_ci95'][0]:.3f}–{g['positive_micro_f1_ci95'][1]:.3f} |")
    L += ["", "| Quan hệ | Support GT | " + " | ".join(m for m in order) + " |", "|---|---:|" + "---:|" * len(order)]
    for rel in RELATIONS:
        L.append(f"| {rel} | {report['golden_test']['rules']['per_relation'][rel]['support']} | "
                 + " | ".join(f"{report['golden_test'][m]['per_relation'][rel]['f1']:.3f}" for m in order) + " |")
    L += ["", "| Phương pháp | GT bản gốc F1 | GT v1.1 F1 |", "|---|---:|---:|"]
    for m in order:
        L.append(f"| {NAMES[m]} | {report['golden_test_v1_original'][m]['positive_micro']['f1']:.3f} | {report['golden_test'][m]['positive_micro']['f1']:.3f} |")
    if "random_test" in report:
        rt = tests["random_v1"]
        L += ["", f"## RE test-random ({len(rt)} cặp, tỉ lệ dương {report['positive_rate']['golden_test_random_v1']})", "",
              "| Phương pháp | P | R | F1 | CI95 |", "|---|---:|---:|---:|---|"]
        for m in order:
            if m in report["random_test"]:
                s = report["random_test"][m]
                L.append(f"| {NAMES[m]} | {s['positive_micro']['precision']:.3f} | {s['positive_micro']['recall']:.3f} | "
                         f"{s['positive_micro']['f1']:.3f} | {s['positive_micro_f1_ci95'][0]:.3f}–{s['positive_micro_f1_ci95'][1]:.3f} |")
        L += ["", "| Quan hệ | Support | " + " | ".join(m for m in order if m in report["random_test"]) + " |",
              "|---|---:|" + "---:|" * len([m for m in order if m in report["random_test"]])]
        for rel in RELATIONS:
            L.append(f"| {rel} | {report['random_test']['rules']['per_relation'][rel]['support']} | "
                     + " | ".join(f"{report['random_test'][m]['per_relation'][rel]['f1']:.3f}" for m in order if m in report["random_test"]) + " |")
    (out / "summary.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    print("\n".join(L))


if __name__ == "__main__":
    main()

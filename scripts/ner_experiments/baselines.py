r"""Non-neural NER baselines on VietMed-NER: train on `train`, tune on `validation`,
score `test` once.

1. dictionary: longest-match lookup of every entity phrase seen in train (lower-cased),
   labelled with its most frequent type; phrases seen more often outside an entity
   than inside one are dropped (tuned threshold on validation).
2. crf: linear-chain CRF (sklearn-crfsuite, L-BFGS) with syllable features in a +-2
   window; c1/c2 chosen by validation micro-F1 (raw 18 types).

    .venv\Scripts\python.exe -X utf8 scripts/ner_experiments/baselines.py --out eval/ner_baselines_2026-11-08
"""
import argparse
import itertools
import time
from collections import Counter, defaultdict

from common_ner import load, save, score, score_both
from seqeval.metrics.sequence_labeling import get_entities


# ---------------- dictionary ----------------
def build_dictionary(train):
    inside = defaultdict(Counter)
    for words, tags in train:
        for typ, s, e in get_entities(tags):
            inside[tuple(w.lower() for w in words[s:e + 1])][typ] += 1
    # how often each phrase occurs as plain text (not as that entity)
    occ = Counter()
    maxlen = max(len(k) for k in inside)
    for words, _ in train:
        low = [w.lower() for w in words]
        for n in range(1, maxlen + 1):
            for i in range(len(low) - n + 1):
                k = tuple(low[i:i + n])
                if k in inside:
                    occ[k] += 1
    return inside, occ, maxlen


def dict_predict(words, lex, maxlen):
    low = [w.lower() for w in words]
    tags = ["O"] * len(words)
    i = 0
    while i < len(words):
        for n in range(min(maxlen, len(words) - i), 0, -1):
            k = tuple(low[i:i + n])
            if k in lex:
                typ = lex[k]
                tags[i] = f"B-{typ}"
                for j in range(i + 1, i + n):
                    tags[j] = f"I-{typ}"
                i += n
                break
        else:
            i += 1
    return tags


def dictionary(train, val, test):
    inside, occ, maxlen = build_dictionary(train)
    best = None
    for thr in (0.0, 0.2, 0.3, 0.4, 0.5, 0.6):
        lex = {k: c.most_common(1)[0][0] for k, c in inside.items()
               if sum(c.values()) / max(occ[k], 1) > thr}
        f = score([t for _, t in val], [dict_predict(w, lex, maxlen) for w, _ in val], with_ci=False)["micro"]["f1"]
        print(f"  dictionary thr={thr}: val F1 {f:.4f}")
        if best is None or f > best[0]:
            best = (f, thr, lex)
    f, thr, lex = best
    pred = [dict_predict(w, lex, maxlen) for w, _ in test]
    return {"params": {"min_entity_ratio": thr, "entries": len(lex)}, "validation_micro_f1": f,
            "test": score_both([t for _, t in test], pred)}


# ---------------- CRF ----------------
def shape(w):
    if w.isdigit():
        return "digit"
    if any(c.isdigit() for c in w):
        return "alnum"
    if w.isupper():
        return "upper"
    if w[:1].isupper():
        return "title"
    return "lower"


def word2features(words, i):
    w = words[i]
    lw = w.lower()
    f = {"bias": 1.0, "w": lw, "shape": shape(w), "len": min(len(w), 8),
         "pre2": lw[:2], "suf2": lw[-2:], "suf3": lw[-3:]}
    for d in (-2, -1, 1, 2):
        j = i + d
        if 0 <= j < len(words):
            f[f"w[{d}]"] = words[j].lower()
            f[f"shape[{d}]"] = shape(words[j])
        else:
            f[f"w[{d}]"] = "<pad>"
    if i > 0:
        f["bi[-1]"] = words[i - 1].lower() + "_" + lw
    if i + 1 < len(words):
        f["bi[+1]"] = lw + "_" + words[i + 1].lower()
    return f


def feats(data):
    return [[word2features(w, i) for i in range(len(w))] for w, _ in data]


def crf(train, val, test, grid):
    import sklearn_crfsuite
    Xtr, ytr = feats(train), [t for _, t in train]
    Xva, Xte = feats(val), feats(test)
    best = None
    for c1, c2 in grid:
        t0 = time.time()
        m = sklearn_crfsuite.CRF(algorithm="lbfgs", c1=c1, c2=c2, max_iterations=200, all_possible_transitions=True)
        m.fit(Xtr, ytr)
        f = score([t for _, t in val], m.predict(Xva), with_ci=False)["micro"]["f1"]
        print(f"  crf c1={c1} c2={c2}: val F1 {f:.4f} ({time.time() - t0:.0f}s)")
        if best is None or f > best[0]:
            best = (f, (c1, c2), m)
    f, (c1, c2), m = best
    return {"params": {"c1": c1, "c2": c2, "max_iterations": 200, "features": "syllable, shape, affixes, +-2 window, bigrams"},
            "validation_micro_f1": f, "test": score_both([t for _, t in test], m.predict(Xte))}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--quick", action="store_true", help="one CRF setting only")
    a = ap.parse_args()
    train, val, test = load("train"), load("validation"), load("test")
    print(f"train {len(train)}, validation {len(val)}, test {len(test)} sentences")
    res = {"data": {"train": len(train), "validation": len(val), "test": len(test)}}
    print("dictionary baseline")
    res["dictionary"] = dictionary(train, val, test)
    grid = [(0.1, 0.1)] if a.quick else list(itertools.product((0.05, 0.1, 0.3), (0.01, 0.1, 0.3)))
    print("CRF baseline")
    res["crf"] = crf(train, val, test, grid)
    for k in ("dictionary", "crf"):
        t = res[k]["test"]
        print(f"{k}: test raw micro-F1 {t['raw']['micro']['f1']:.4f}, target(6) micro-F1 {t['target']['micro']['f1']:.4f}")
    save(res, f"{a.out}/baselines.json")


if __name__ == "__main__":
    main()

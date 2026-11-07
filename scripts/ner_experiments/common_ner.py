"""Shared data and scoring for the NER baseline experiments.

Every model is trained on VietMed-NER `train`, tuned/selected on `validation` and
scored once on `test` with the same function, so the numbers are comparable:

- raw level: the dataset's 18 entity types (37 BIO tags), seqeval entity-level,
  same scorer as eval/evaluate_tier1.py;
- target level: tags mapped to the 6 thesis types (ner/config.py VIETMED_TO_TARGET)
  before scoring, i.e. model-only quality on the schema the pipeline uses.

CI95: bootstrap over sentences (1000 resamples, seed 0) on micro-F1.
"""
import json
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts" / "golden_test"))

from common import load_split, map_tag  # noqa: E402
from seqeval.metrics import classification_report  # noqa: E402
from seqeval.metrics.sequence_labeling import get_entities  # noqa: E402

SPLITS = ("train", "validation", "test")


def norm_tag(t):
    t = str(t).strip()
    return "O" if t in ("0", "O", "") else t


def load(split):
    """List of (words, raw BIO tags); rows whose lengths differ are dropped."""
    rows, _ = load_split(split)
    out = []
    for r in rows:
        if len(r["words"]) == len(r["labels"]) and r["words"]:
            out.append((list(r["words"]), [norm_tag(t) for t in r["labels"]]))
    return out


def to_target(tags):
    return [map_tag(t) for t in tags]


def label_list(data):
    labels = sorted({t for _, tags in data for t in tags if t != "O"})
    return ["O"] + labels


def _micro(gold, pred):
    """Entity-level micro P/R/F1 counts with seqeval's entity extraction."""
    tp = fp = fn = 0
    for g, p in zip(gold, pred):
        ge, pe = set(get_entities(g)), set(get_entities(p))
        tp += len(ge & pe)
        fp += len(pe - ge)
        fn += len(ge - pe)
    return tp, fp, fn


def _f1(tp, fp, fn):
    p = tp / (tp + fp) if tp + fp else 0.0
    r = tp / (tp + fn) if tp + fn else 0.0
    return p, r, (2 * p * r / (p + r) if p + r else 0.0)


def bootstrap_ci(gold, pred, n=1000, seed=0):
    rng = random.Random(seed)
    per = [_micro([g], [p]) for g, p in zip(gold, pred)]
    idx = range(len(per))
    vals = []
    for _ in range(n):
        s = [per[rng.choice(idx)] for _ in idx]
        vals.append(_f1(sum(x[0] for x in s), sum(x[1] for x in s), sum(x[2] for x in s))[2])
    vals.sort()
    return [round(vals[int(0.025 * n)], 4), round(vals[int(0.975 * n) - 1], 4)]


def score(gold, pred, with_ci=True):
    """seqeval report (per type + averages) plus our micro counts and CI95."""
    rep = classification_report(gold, pred, output_dict=True, zero_division=0)
    rep = {k: {m: (float(v) if m != "support" else int(v)) for m, v in d.items()} for k, d in rep.items()}
    tp, fp, fn = _micro(gold, pred)
    out = {"report": rep, "micro": {"tp": tp, "fp": fp, "fn": fn,
                                    **dict(zip(("precision", "recall", "f1"), _f1(tp, fp, fn)))}}
    if with_ci:
        out["micro_f1_ci95"] = bootstrap_ci(gold, pred)
    return out


def score_both(gold_raw, pred_raw, with_ci=True):
    return {"raw": score(gold_raw, pred_raw, with_ci),
            "target": score([to_target(t) for t in gold_raw], [to_target(t) for t in pred_raw], with_ci)}


def save(obj, path):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=1), encoding="utf-8")

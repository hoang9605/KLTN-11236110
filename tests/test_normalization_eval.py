"""Metric arithmetic for scripts/normalization_eval/evaluate.py on a hand-checked toy set."""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts" / "normalization_eval"))
from evaluate import aggregate, icd_category, score_items  # noqa: E402


def row(gold, system, cands, freq=1):
    return {"gold_codes": gold, "nil": not gold, "freq": freq,
            "pred": {"exact": None, "fuzzy1": cands[0] if cands else None, "system": system,
                     "always": cands[0] if cands else None},
            "candidates": cands}


ROWS = [
    row(["K58", "K58.9"], "K58", ["K58", "K59"], freq=3),   # correct, rank 1
    row(["R42"], None, ["H81.1", "R42"]),                    # abstains, gold at rank 2
    row(["D25"], "C53", ["C53", "C54"]),                     # wrong link, gold not retrieved
    row([], None, ["R52"], freq=2),                          # NIL, correct abstention
]


def test_type_level():
    agg = aggregate(score_items(ROWS), weighted=False)
    assert agg["n_linkable"] == 3 and agg["n_nil"] == 1
    assert agg["system"]["accuracy"] == pytest.approx(1 / 3)
    assert agg["system"]["coverage"] == pytest.approx(2 / 3)
    assert agg["system"]["precision_answered"] == pytest.approx(1 / 2)
    assert agg["system"]["nil_correct_abstention"] == 1.0
    assert agg["top1_acc"] == pytest.approx(1 / 3)
    assert agg["top3_acc"] == pytest.approx(2 / 3)
    assert agg["recall@3"] == agg["top3_acc"]
    assert agg["mrr@10"] == pytest.approx((1 + 0.5) / 3)
    assert agg["fuzzy1"]["nil_correct_abstention"] == 0.0
    # always-answer: accuracy equals Top-1, full coverage, every NIL form gets a code
    assert agg["always"]["accuracy"] == agg["top1_acc"]
    assert agg["always"]["coverage"] == 1.0
    assert agg["always"]["nil_correct_abstention"] == 0.0


def test_mention_level_weights_by_freq():
    agg = aggregate(score_items(ROWS), weighted=True)
    assert agg["system"]["accuracy"] == pytest.approx(3 / 5)
    assert agg["top3_acc"] == pytest.approx(4 / 5)


def test_category_level():
    assert icd_category("B26.0†") == "B26"
    rows = [row(["K52.9"], "K52.3", ["K52.3"])]
    assert aggregate(score_items(rows), False)["system"]["accuracy"] == 0.0
    assert aggregate(score_items(rows, category=True), False)["system"]["accuracy"] == 1.0

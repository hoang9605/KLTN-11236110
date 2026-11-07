"""RE benchmark baselines, label agreement and the NER experiment scorer."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts" / "re_dataset"))
sys.path.insert(0, str(ROOT / "scripts" / "ner_experiments"))

from agreement import kappa  # noqa: E402
from benchmark import nearest, union  # noqa: E402
from common_ner import score, to_target  # noqa: E402

NEG = "NO_RELATION"


def ent(i, label, start, end):
    return {"id": i, "label": label, "start": start, "end": end}


def test_nearest_requires_mutual_closest():
    # "đau ở bụng và lưng": đau(0-3) bụng(7-11) lưng(15-19)
    pain, belly, back = ent("E1", "CONDITION", 0, 3), ent("E2", "BODY_PART", 7, 11), ent("E3", "BODY_PART", 15, 19)
    ents = [pain, belly, back]
    near = {"head": pain, "tail": belly, "allowed_relation": "located_at", "entities": ents}
    far = {"head": pain, "tail": back, "allowed_relation": "located_at", "entities": ents}
    assert nearest(near) == "located_at"
    assert nearest(far) == NEG


def test_union_keeps_first_positive():
    assert union(["located_at", NEG, NEG], [NEG, "treated_by", NEG]) == ["located_at", "treated_by", NEG]


def test_kappa_hand_computed():
    a = ["x", "x", "y", "y"]
    b = ["x", "y", "y", "y"]
    po, k = kappa(a, b)
    # po = 3/4; pe = (2*1 + 2*3)/16 = 0.5; kappa = (0.75-0.5)/0.5
    assert po == 0.75 and abs(k - 0.5) < 1e-9


def test_ner_score_counts_and_target_mapping():
    gold = [["B-DISEASESYMTOM", "I-DISEASESYMTOM", "O", "B-ORGAN"]]
    pred = [["B-DISEASESYMTOM", "I-DISEASESYMTOM", "O", "O"]]
    m = score(gold, pred, with_ci=False)["micro"]
    assert (m["tp"], m["fp"], m["fn"]) == (1, 0, 1)
    assert to_target(gold[0]) == ["B-CONDITION", "I-CONDITION", "O", "B-BODY_PART"]

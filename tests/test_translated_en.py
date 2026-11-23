import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts/re_dataset"))

from translated_en import parse_marked  # noqa: E402

from relation_extraction.data import load_pairs  # noqa: E402

DATA = ROOT / "data/re_translated_en_v1/annotations.jsonl"


def test_parse_marked_offsets():
    plain, spans = parse_marked("điều trị [D]ung thư phổi[/D] bằng [T]hóa trị[/T]")
    assert plain == "điều trị ung thư phổi bằng hóa trị"
    assert plain[slice(*spans["D"])] == "ung thư phổi"
    assert plain[slice(*spans["T"])] == "hóa trị"


def test_parse_marked_numbered_markers():
    plain, spans = parse_marked("uống [Q1]năm mi li gam[/Q1] [R1]aspirin[/R1] và [Q2]liều cao[/Q2]")
    assert {k: plain[slice(*v)] for k, v in spans.items()} == {"Q1": "năm mi li gam", "R1": "aspirin", "Q2": "liều cao"}


@pytest.mark.parametrize("bad", ["[D]ung thư", "ung thư[/D]", "[D]a[/D] [D]b[/D]"],
                         ids=["unclosed", "closing_only", "used_twice"])
def test_parse_marked_rejects_broken_markers(bad):
    with pytest.raises(ValueError):
        parse_marked(bad)


@pytest.mark.skipif(not DATA.exists(), reason="translated data not built")
def test_translated_data_is_marked_as_unverified_training_only():
    rows = [json.loads(x) for x in DATA.read_text(encoding="utf-8").splitlines() if x.strip()]
    assert rows and all(r["human_verified"] is False and r["annotation_status"] == "TRANSLATED_AI" for r in rows)
    pairs, _ = load_pairs(DATA, allow_ai=True)  # offsets, types and directions pass the normal loader
    assert len(pairs) == sum(len(r["relations"]) for r in rows)
    with pytest.raises(ValueError):
        load_pairs(DATA)  # never loaded silently as verified data

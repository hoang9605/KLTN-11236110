"""re_v3.validate_kb (K1–K7), re_v3.expert_review, re_v3.label_llm (self-consistency) — không gọi API."""
import argparse
import csv

import pytest

from re_v3 import label_llm as L
from re_v3 import validate_kb as V
from re_v3.expert_review import apply_review, cohen_kappa, read_review, score_rows, wilson, write_xlsx


def _ent(text, eid, label, surface):
    s = text.index(surface)
    return {"id": eid, "label": label, "start": s, "end": s + len(surface), "text": surface}


TEXT = "bác sĩ cho uống hai viên paracetamol mỗi ngày vì bị đau đầu"
ENTS = [_ent(TEXT, "E1", "DOSAGE", "hai viên"), _ent(TEXT, "E2", "DRUG", "paracetamol"),
        _ent(TEXT, "E3", "CONDITION", "đau đầu")]


@pytest.fixture(scope="module")
def kb():
    return V.KBValidator()


def test_dosage_regex():
    assert V.DOSAGE_UNITS.search("hai viên") and V.DOSAGE_AMOUNT.search("hai viên")
    assert V.DOSAGE_UNITS.search("ngày hai lần") and V.DOSAGE_AMOUNT.search("ngày hai lần")
    assert not V.DOSAGE_UNITS.search("cao")
    assert not V.DOSAGE_UNITS.search("mức độ")


def test_entity_checks_use_dictionaries(kb):
    c = kb.entity_checks(ENTS[2])
    assert c["K1"]["pass"] and c["K1"]["icd10"]["code"]          # đau đầu có mã ICD-10
    c = kb.entity_checks(ENTS[0])
    assert c["K4"]["pass"]
    bad = dict(ENTS[0], text="mức độ")
    assert not kb.entity_checks(bad)["K4"]["pass"]


def test_has_dosage_with_non_dosage_is_hard_fail(kb):
    text = "uống paracetamol thì mức độ đau giảm"
    ents = [_ent(text, "E1", "DRUG", "paracetamol"), _ent(text, "E2", "DOSAGE", "mức độ")]
    rec = {"text": text, "entities": ents,
           "relations": [{"head": "E1", "tail": "E2", "allowed_relation": "has_dosage", "label": "has_dosage"}]}
    v = kb.validate(rec, target={"head": "E1", "tail": "E2", "relation": "has_dosage"})
    assert v["tier"] == "C" and any(f.startswith("K4_not_dosage") for f in v["flags"])


def test_validate_good_record_and_rule_check(kb):
    rec = {"text": TEXT, "entities": ENTS,
           "relations": [{"head": "E2", "tail": "E1", "allowed_relation": "has_dosage", "label": "has_dosage"}]}
    v = kb.validate(rec, target={"head": "E2", "tail": "E1", "relation": "has_dosage"})
    assert v["tier"] in ("A", "B")
    assert "K6" in v["pairs"][0] and "K7" in v["pairs"][0]


def test_wilson_and_kappa():
    p, lo, hi = wilson(45, 50)
    assert lo < p < hi and round(p, 2) == 0.9
    assert cohen_kappa(["a", "b", "a"], ["a", "b", "a"]) == 1.0


def test_expert_xlsx_roundtrip(tmp_path, kb):
    from openpyxl import load_workbook
    rec = {"id": "X1", "text": TEXT, "entities": [dict(e, validity="VALID") for e in ENTS], "parent_id": "P",
           "relations": [{"head": "E3", "tail": "E2", "allowed_relation": "treated_by", "label": "NO_RELATION",
                          "label_source": "llm_majority", "votes": "2/2"}]}
    rec["entities"][0]["validity"] = "INVALID"
    rec["kb_validation"] = kb.validate(rec)
    path = tmp_path / "r_expert_review.xlsx"
    write_xlsx(path, [rec], with_entities=True)
    wb = load_workbook(path)
    ws = wb["Quan hệ"]
    assert ws["C2"].value == "đau đầu" and "KHÔNG" in ws["G2"].value
    assert "paracetamol" in ws["G2"].value and "«" in str(ws["B2"].value)
    assert wb["Thực thể"]["C2"].value == "hai viên"
    ws["I2"] = 0                       # chuyên gia: AI sai -> nhãn đúng là treated_by
    wb["Thực thể"]["G2"] = 1           # đồng ý "hai viên" không hợp lệ (ví dụ)
    wb["Hướng dẫn"]["B3"] = "Người duyệt thử"
    wb["Hướng dẫn"]["B4"] = "24/11/2026"
    wb.save(path)
    reviewer, rel, ent, syn = read_review(path)
    s = score_rows(rel, ent, syn)
    assert s["reviewed"] == 1 and s["ai_accuracy"]["ALL"]["correct"] == 0 and s["ai_recall"] == 0.0
    final = apply_review([rec], reviewer, rel, ent, syn)
    assert final[0]["relations"][0]["label"] == "treated_by" and final[0]["human_verified"] is True
    assert final[0]["reviewer"]["name"] == "Người duyệt thử"


class FakeVoter:
    def __init__(self, labels):
        self.labels, self.i = labels, 0

    def __call__(self, messages, model, temperature, seed):
        lab = self.labels[self.i % len(self.labels)]
        self.i += 1
        return {"entities": [{"id": e["id"], "validity": "VALID"} for e in ENTS],
                "pairs": [{"pair_id": "R1", "label": lab, "evidence": "vì bị đau đầu"}]}


def test_self_consistency_majority_and_disagreement():
    row = {"id": "VMR-TR-1", "source": "x", "source_split": "train", "source_row_index": 0, "split": "train",
           "text": TEXT, "entities": ENTS,
           "pairs": [{"id": "R1", "head": "E3", "tail": "E2", "allowed_relation": "treated_by"}]}
    args = argparse.Namespace(k=3, temperature=0.7, model="fake", seed=1)
    tpl = L.load_prompt("verify")
    res = L.label_row(row, FakeVoter(["treated_by", "treated_by", "NO_RELATION"]), tpl, args)
    rel = res["record"]["relations"][0]
    assert rel["label"] == "treated_by" and rel["votes"] == "2/3"
    assert res["record"]["self_consistency"]["pair_disagree"] == ["R1"]
    res = L.label_row(row, FakeVoter(["treated_by"]), tpl, args)
    assert res["record"]["relations"][0]["votes"] == "3/3"


class CountingVoter(FakeVoter):
    pass


def _row():
    return {"id": "VMR-TR-1", "source": "x", "source_split": "train", "source_row_index": 0, "split": "train",
            "text": TEXT, "entities": ENTS,
            "pairs": [{"id": "R1", "head": "E3", "tail": "E2", "allowed_relation": "treated_by"}]}


def test_adaptive_calls_only_when_needed():
    from relation_extraction.rules import predict_pair
    row = _row()
    ents = {e["id"]: e for e in ENTS}
    rule = predict_pair(TEXT, ents["E3"], ents["E2"], "treated_by", ENTS)
    args = argparse.Namespace(k=3, temperature=0.7, model="fake", seed=1, adaptive=True)
    tpl = L.load_prompt("verify")
    # lượt 1 trùng luật và là âm -> 1 lần gọi
    if rule == "NO_RELATION":
        v = FakeVoter(["NO_RELATION"])
        L.label_row(row, v, tpl, args)
        assert v.i == 1
    # lượt 1 dương, lượt 2 đồng ý -> 2 lần gọi
    v = FakeVoter(["treated_by", "treated_by"])
    res = L.label_row(row, v, tpl, args)
    assert v.i == 2 and res["record"]["relations"][0]["votes"] == "2/2"
    # lượt 1 và 2 bất đồng -> 3 lần gọi
    v = FakeVoter(["treated_by", "NO_RELATION", "treated_by"])
    res = L.label_row(row, v, tpl, args)
    assert v.i == 3 and res["record"]["relations"][0]["votes"] == "2/3"


def test_budget_cap_stops_new_calls(tmp_path, monkeypatch):
    from re_v3 import synth_llm as S
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    llm = S.LLM(tmp_path / "cache.jsonl", max_usd=0.01)
    llm.spent = 0.02
    with pytest.raises(S.BudgetExceeded):
        llm([{"role": "user", "content": "x"}], "gpt-4o", 0.0, 1)
    assert round(llm.cost("gpt-4o", 1_000_000, 0), 2) == 2.5
    res = L.label_row(_row(), llm, L.load_prompt("verify"),
                      argparse.Namespace(k=3, temperature=0.7, model="gpt-4o", seed=1, adaptive=True))
    assert res["status"] == "BUDGET"

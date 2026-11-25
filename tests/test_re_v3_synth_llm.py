"""re_v3.synth_llm: rule V1–V8 và luồng sinh → kiểm tra → bản ghi, với LLM giả (không gọi API)."""
import argparse
import random

from re_v3 import llm_rules as R
from re_v3 import synth_llm as S
from re_v3.common import check_record

SEED_TEXT = "dạo này hay bị đau ở thắt lưng thì có uống thuốc giảm đau"
def _ent(eid, label, surface):
    start = SEED_TEXT.index(surface)
    return {"id": eid, "label": label, "start": start, "end": start + len(surface), "text": surface}


SEED_ENTS = [_ent("E1", "CONDITION", "đau"), _ent("E2", "BODY_PART", "thắt lưng"),
             _ent("E3", "DRUG", "thuốc giảm đau")]


def job(variant="POS_EXPLICIT", label="located_at"):
    return {"job_id": "located_at-POS-0000", "relation": "located_at", "polarity": "POS" if label != "NO_RELATION" else "NEG",
            "variant": variant, "target_label": label, "seed_id": "VMR-TR-00001", "seed_text": SEED_TEXT,
            "seed_entities": SEED_ENTS, "head": "E1", "tail": "E2", "speaker": R.SPEAKERS[0]}


GOOD = "mấy hôm nay thì em hay bị [E1:CONDITION]đau[/E1] ở cái vùng [E2:BODY_PART]thắt lưng[/E2] nhất là lúc mà ngồi lâu á bác sĩ"


def check(tagged, j=None):
    return R.check_generation(j or job(), tagged, set(), 8)[2]


def test_seed_offsets_fixture():
    for e in SEED_ENTS:
        assert SEED_TEXT[e["start"]:e["end"]] == e["text"]


def test_good_generation_passes():
    assert check(GOOD) == []


def test_rules_reject_bad_generations():
    assert check(GOOD.replace("[/E1]", ""))[0].startswith("V1")
    assert "V2_missing:E2" in check(GOOD.replace("[E2:BODY_PART]thắt lưng[/E2]", "lưng"))
    assert "V3_new_entity:E4" in check(GOOD + " uống [E4:DRUG]paracetamol[/E4]")
    assert "V4_punct" in check(GOOD + ".")
    assert "V4_digit" in check(GOOD.replace("mấy hôm", "3 hôm"))
    assert "V4_uppercase" in check(GOOD.replace("em hay", "Em hay"))
    assert any(e.startswith("V4_length") for e in check("[E1:CONDITION]đau[/E1] [E2:BODY_PART]thắt lưng[/E2]"))
    assert "V5_copy" in check(R.tag_sentence(SEED_TEXT, SEED_ENTS))
    assert "V6_cue:POS_NEGATED" in check(GOOD, job("POS_NEGATED"))
    assert any(e.startswith("V7_gap") for e in check(GOOD, job("POS_LONG_GAP")))


def test_leak_rule():
    from re_v3.common import words
    w = words(R.parse_tagged(GOOD)[0])
    grams = {tuple(w[0:8])}
    assert "V8_leak" in R.check_generation(job(), GOOD, grams, 8)[2]


class FakeLLM:
    """Trả lời giả: lượt sinh trả GOOD, lượt kiểm tra trả nhãn do test chọn."""

    def __init__(self, target_label="located_at", validity="VALID"):
        self.target_label, self.validity = target_label, validity

    def __call__(self, messages, model, temperature, seed):
        if "Câu gốc:" in messages[1]["content"]:
            return {"skip": False, "skip_reason": "", "tagged": GOOD, "evidence": "đau ở cái vùng thắt lưng"}
        return {"entities": [{"id": "E1", "validity": "VALID"}, {"id": "E2", "validity": self.validity}],
                "pairs": [{"pair_id": "R1", "label": self.target_label, "evidence": "đau ở thắt lưng"}]}


ARGS = argparse.Namespace(gen_model="fake", verify_model="fake", gen_temperature=0.8, seed=1)


def run(fake, j=None):
    tpl = S.load_prompt("gen"), S.load_prompt("verify")
    return S.run_job(j or job(), fake, tpl[0], tpl[1], ARGS, (set(), 8))


def test_accept_and_record_is_valid():
    res = run(FakeLLM())
    assert res["status"] == "ACCEPT", res["reasons"]
    rec = S.to_record(res, 1, ARGS)
    check_record(rec)
    assert rec["relations"] == [{"head": "E1", "tail": "E2", "allowed_relation": "located_at", "label": "located_at",
                                 "label_source": "target+verifier", "evidence": "đau ở thắt lưng"}]
    assert rec["human_verified"] is False and rec["training_eligible"] is False


def test_reject_when_blind_label_disagrees():
    assert run(FakeLLM("NO_RELATION"))["reasons"] == ["VERIFY_DISAGREE:NO_RELATION"]


def test_reject_when_target_entity_invalid():
    assert run(FakeLLM(validity="INVALID"))["reasons"] == ["VERIFY_TARGET_INVALID"]


def test_prompts_render_without_missing_fields():
    tpl = S.load_prompt("gen")
    msgs = S.gen_messages(job(), tpl)
    assert "$" not in msgs[0]["content"] + msgs[1]["content"]
    text, ents = R.parse_tagged(GOOD)
    pairs = [{"id": "R1", "head": "E1", "tail": "E2", "allowed_relation": "located_at"}]
    vmsgs = S.verify_messages(text, ents, pairs, S.load_prompt("verify"))
    assert "$" not in vmsgs[0]["content"] + vmsgs[1]["content"]
    assert "located_at" in vmsgs[0]["content"] and "has_dosage (DRUG" not in vmsgs[0]["content"]


def test_plan_only_uses_train_and_rotates_variants():
    seeds = S.load_seeds()
    assert seeds and all(s["split"] == "train" for s in seeds)
    jobs = S.plan_jobs(seeds, 8, 10, random.Random(0))
    for rel, variants in R.VARIANTS.items():
        pos = {j["variant"] for j in jobs if j["relation"] == rel and j["polarity"] == "POS"}
        assert pos == {v[0] for v in variants if v[1] == "POS"}
    assert all(j["target_label"] == "NO_RELATION" for j in jobs if j["polarity"] == "NEG")

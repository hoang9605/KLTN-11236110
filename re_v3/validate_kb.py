r"""Kiểm tra bằng từ điển và công cụ (K1–K7), chạy TRƯỚC khi đưa dữ liệu cho chuyên gia.

Dùng cho cả dữ liệu sinh (synth_llm) và câu thật do LLM gán nhãn (label_llm).
Không có bước nào gọi LLM: chỉ dùng tài nguyên và công cụ có sẵn trong repo.

Mức thực thể
  K1 CONDITION → ICD-10 (Bộ Y tế, normalization.icd10, chế độ strict): có mã hay không.
  K2 DRUG      → RxNorm (normalization.rxnorm: cache SQLite + bí danh Việt–Anh, RxNav nếu --online-rxnorm).
  K3 Từ điển kiểu thực thể rút từ nhãn NER gốc của VietMed-NER (cả 3 split, 9267 câu):
     mention có xuất hiện ≥ 2 lần và kiểu đang gán chiếm ≥ 50% số lần xuất hiện.
     Đây là từ điển duy nhất có cho BODY_PART / TEST / PROCEDURE (repo chưa có ontology cho 3 kiểu này).
  K4 DOSAGE    → phải có đơn vị liều (viên, mũi, mg…) và số lượng hoặc tần suất (một, hai, mỗi ngày…).
  K5 Mô hình NER ViHealthBERT (Model/vihealthbert-ner-vietmed-v2-final, --ner) chạy lại trên câu:
     thực thể có được nhận lại đúng kiểu không (có chồng lấn ký tự). Bật bằng --ner vì chậm.
Mức cặp
  K6 Luật RE của repo (relation_extraction.rules.predict_pair) có cho cùng nhãn không.
  K7 Bằng chứng từ kho (giám sát xa, Mintz et al. 2009): cặp mention (head, tail) đã cùng xuất hiện
     trong ít nhất một câu VietMed thật khác với câu seed hay chưa.

Phân tầng (để phân bổ công chuyên gia):
  C  lỗi cứng → loại, không đưa chuyên gia:
       - thực thể đích kiểu X nhưng từ điển K3 cho thấy mention gần như luôn là kiểu khác (< 20%)
       - has_dosage có DOSAGE đích không qua K4
  B  còn cờ mềm (K1/K2/K3/K5 không khớp với thực thể đích, K6 bất đồng, K7 không có bằng chứng
     cho cặp dương) → chuyên gia duyệt 100%
  A  qua hết → chuyên gia duyệt mẫu ngẫu nhiên
"""
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

import requests

from relation_extraction.data import NEGATIVE, candidates
from relation_extraction.rules import predict_pair

from . import config
from .common import norm

KB_DIR = config.HERE / "data" / "kb"
DICT_PATH = KB_DIR / "vietmed_entity_dictionary.json"

DOSAGE_UNITS = re.compile(
    r"\b(viên|mũi|liều|mg|miligam|milligram|mcg|microgram|gam|gram|g|ml|mililit|lít|cc|giọt|gói|ống|"
    r"chai|lọ|nhát|nang|thìa|muỗng|cữ|lần|đơn vị|iu|ui|xịt|miếng|cốc|ly)\b")
DOSAGE_AMOUNT = re.compile(
    r"\b(một|hai|ba|bốn|tư|năm|lăm|sáu|bảy|tám|chín|mười|mươi|mốt|trăm|nghìn|ngàn|nửa|rưỡi|vài|mấy|"
    r"mỗi|hằng|hàng|ngày|tuần|tháng|sáng|tối|đủ)\b")

SOFT_ENTITY_CHECKS = ("K1", "K2", "K3", "K5")


# ---------------------------------------------------------------------------
# K3: từ điển kiểu thực thể từ VietMed-NER
# ---------------------------------------------------------------------------
def build_entity_dictionary(path=DICT_PATH):
    sys.path.insert(0, str(config.ROOT / "scripts" / "golden_test"))
    from common import entities_from_bio, load_split  # noqa: E402
    counts = defaultdict(Counter)
    sources = {}
    for split in ("train", "validation", "test"):
        rows, src = load_split(split)
        sources[split] = src
        for row in rows:
            if len(row["words"]) != len(row["labels"]):
                continue
            _, ents = entities_from_bio(row["words"], row["labels"])
            for e in ents:
                counts[norm(e["text"])][e["label"]] += 1
    data = {"_note": "Số lần mỗi mention được gán từng kiểu trong nhãn NER gốc VietMed-NER (3 split), đã ánh xạ sang 6 kiểu đích.",
            "sources": sources, "mentions": {k: dict(v) for k, v in sorted(counts.items())}}
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=0), encoding="utf-8")
    return data["mentions"]


def load_entity_dictionary(path=DICT_PATH):
    if not Path(path).exists():
        return build_entity_dictionary(path)
    return json.loads(Path(path).read_text(encoding="utf-8"))["mentions"]


# ---------------------------------------------------------------------------
# K7: chỉ mục cặp cùng xuất hiện trong câu thật
# ---------------------------------------------------------------------------
def build_pair_index(split_dir=config.ROOT / "data" / "re_vietmed_811_v1"):
    """(head mention, tail mention, quan hệ) -> tập id câu thật chứa cặp đó (mọi split, chỉ dùng mention)."""
    index = defaultdict(set)
    for name in ("train", "dev", "test"):
        for line in (Path(split_dir) / f"{name}.jsonl").read_text(encoding="utf-8").splitlines():
            row = json.loads(line)
            ents = {e["id"]: e for e in row["entities"]}
            for p in row["pairs"]:
                index[(norm(ents[p["head"]]["text"]), norm(ents[p["tail"]]["text"]), p["allowed_relation"])].add(row["id"])
    return index


# ---------------------------------------------------------------------------
# Bộ kiểm tra
# ---------------------------------------------------------------------------
class _Offline(requests.Session):
    def get(self, *a, **k):
        raise requests.ConnectionError("offline")


class KBValidator:
    def __init__(self, use_ner=False, online_rxnorm=False, log_dir=KB_DIR):
        from normalization.icd10 import ICD10Normalizer
        from normalization.rxnorm import RxNormNormalizer
        self.icd = ICD10Normalizer()
        self.rx = RxNormNormalizer(session=None if online_rxnorm else _Offline(), max_retries=1,
                                   unmatched_log_path=Path(log_dir) / "unmatched_drugs.log")
        self.online_rxnorm = online_rxnorm
        self.dictionary = load_entity_dictionary()
        self.pairs = build_pair_index()
        self.ner = None
        if use_ner:
            from ner.pipeline import MedicalNERPipeline
            self.ner = MedicalNERPipeline(enable_normalization=False)
        self._memo = {}

    # --- mức thực thể ---
    def _norm(self, kind, surface):
        key = (kind, norm(surface))
        if key not in self._memo:
            res = (self.icd if kind == "ICD" else self.rx).normalize(surface)
            self._memo[key] = None if res is None else {"code": res.code, "name": res.label_standard,
                                                        "method": res.match_method}
        return self._memo[key]

    def entity_checks(self, e):
        out = {}
        if e["label"] == "CONDITION":
            hit = self._norm("ICD", e["text"])
            out["K1"] = {"pass": hit is not None, "icd10": hit}
        if e["label"] == "DRUG":
            hit = self._norm("RX", e["text"])
            out["K2"] = {"pass": hit is not None, "rxnorm": hit, "online": self.online_rxnorm}
        dist = self.dictionary.get(norm(e["text"]), {})
        total = sum(dist.values())
        share = dist.get(e["label"], 0) / total if total else 0.0
        out["K3"] = {"pass": total >= 2 and share >= 0.5, "count": total, "type_share": round(share, 2),
                     "hard_fail": total >= 2 and share < 0.2, "distribution": dist}
        if e["label"] == "DOSAGE":
            t = norm(e["text"])
            out["K4"] = {"pass": bool(DOSAGE_UNITS.search(t) and DOSAGE_AMOUNT.search(t))}
        return out

    def ner_checks(self, text, entities):
        if self.ner is None:
            return {}
        pred = self.ner.predict(text, normalize=False)["entities"]
        res = {}
        for e in entities:
            same = [p for p in pred if p["label"] == e["label"]
                    and p["start_char"] < e["end"] and e["start"] < p["end_char"]]
            res[e["id"]] = {"pass": bool(same), "predicted": [p["surface_text"] for p in same]}
        return res

    # --- mức bản ghi ---
    def validate(self, record, target=None, exclude_ids=()):
        """record: định dạng repo (text, entities, relations). target: {head, tail, relation} hoặc None."""
        ents = {e["id"]: e for e in record["entities"]}
        ent_checks = {eid: self.entity_checks(e) for eid, e in ents.items()}
        for eid, r in self.ner_checks(record["text"], record["entities"]).items():
            ent_checks[eid]["K5"] = r
        pair_checks = []
        for rel in record["relations"]:
            h, t = ents[rel["head"]], ents[rel["tail"]]
            rule = predict_pair(record["text"], h, t, rel["allowed_relation"], record["entities"])
            support = self.pairs.get((norm(h["text"]), norm(t["text"]), rel["allowed_relation"]), set())
            support = sorted(support - set(exclude_ids))
            pair_checks.append({"head": rel["head"], "tail": rel["tail"], "relation": rel["allowed_relation"],
                                "label": rel["label"],
                                "K6": {"pass": rule == rel["label"], "rule_label": rule},
                                "K7": {"pass": bool(support), "support": len(support), "examples": support[:3]}})
        tier, flags = self._tier(record, ent_checks, pair_checks, target)
        return {"entities": ent_checks, "pairs": pair_checks, "tier": tier, "flags": flags}

    @staticmethod
    def _tier(record, ent_checks, pair_checks, target):
        flags, hard = [], []
        focus = {target["head"], target["tail"]} if target else set(ent_checks)
        for eid in focus:
            c = ent_checks[eid]
            if c["K3"]["hard_fail"]:
                hard.append(f"K3_type_mismatch:{eid}")
            if "K4" in c and not c["K4"]["pass"] and (target is None or target["relation"] == "has_dosage"):
                hard.append(f"K4_not_dosage:{eid}")
            flags += [f"{k}_fail:{eid}" for k in SOFT_ENTITY_CHECKS if k in c and not c[k]["pass"]]
        for p in pair_checks:
            is_target = target and (p["head"], p["tail"]) == (target["head"], target["tail"])
            if target and not is_target:
                continue
            if not p["K6"]["pass"]:
                flags.append(f"K6_rule_disagree:{p['head']}-{p['tail']}")
            if p["label"] != NEGATIVE and not p["K7"]["pass"]:
                flags.append(f"K7_no_corpus_support:{p['head']}-{p['tail']}")
        if hard:
            return "C", hard + flags
        return ("B" if flags else "A"), flags


def pairs_for(text, entities):
    return [{"id": f"R{i}", "head": c["head"]["id"], "tail": c["tail"]["id"], "allowed_relation": c["allowed_relation"]}
            for i, c in enumerate(candidates(text, entities), 1)]


if __name__ == "__main__":
    m = build_entity_dictionary()
    print(f"Từ điển: {len(m)} mention -> {DICT_PATH}")

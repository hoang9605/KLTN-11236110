"""Baseline luật cho RE — viết từ hướng dẫn gán nhãn (docs/RE_LABELS.md), KHÔNG tinh chỉnh trên dữ liệu.

Mỗi cặp ứng viên (head, tail) đúng kiểu được dự đoán dương khi:
  - khoảng cách giữa hai thực thể <= MAX_GAP từ, và
  - đoạn chữ nằm giữa hai thực thể chứa một từ gợi ý của quan hệ đó
    (located_at còn chấp nhận BODY_PART đứng ngay sau CONDITION; has_dosage chấp nhận DOSAGE ngay sau DRUG),
  - và không có thực thể cùng loại với head/tail chen giữa (tránh nối nhầm sang cụm khác).
"""
import re

from .data import NEGATIVE, candidates

MAX_GAP = {"located_at": 4, "treated_by": 8, "treated_by_procedure": 8, "diagnosed_by": 8, "has_dosage": 3}
CUES = {
    "located_at": ["ở", "tại", "vùng", "trong", "của", "phía", "bên", "khu vực", "chỗ", "lan"],
    "treated_by": ["điều trị", "chữa", "trị", "bằng", "dùng", "uống", "tiêm", "bôi", "kê", "cho thuốc", "sử dụng"],
    "treated_by_procedure": ["điều trị", "chữa", "trị", "bằng", "phương pháp", "can thiệp", "tiến hành", "thực hiện", "sử dụng"],
    "diagnosed_by": ["chẩn đoán", "phát hiện", "xác định", "cho thấy", "thấy", "qua", "bằng", "kiểm tra", "tầm soát", "làm"],
    "has_dosage": [],
}
ADJACENT_OK = {"located_at": ("head", "tail"), "has_dosage": ("head", "tail")}  # head trước, tail ngay sau


def _words(s):
    return re.findall(r"\w+", s.lower())


def _has_cue(between, cues):
    b = " " + " ".join(_words(between)) + " "
    return any(f" {c} " in b for c in cues)


def predict_pair(text, head, tail, allowed, entities):
    first, second = sorted((head, tail), key=lambda e: e["start"])
    between = text[first["end"]:second["start"]]
    gap = len(_words(between))
    if gap > MAX_GAP[allowed]:
        return NEGATIVE
    blockers = {head["label"], tail["label"]}
    if any(e is not head and e is not tail and e["label"] in blockers
           and first["end"] <= e["start"] and e["end"] <= second["start"] for e in entities):
        return NEGATIVE
    if gap == 0 and allowed in ADJACENT_OK and first is head:
        return allowed
    return allowed if CUES[allowed] and _has_cue(between, CUES[allowed]) else NEGATIVE


class RuleRelationExtractor:
    supported_relations = sorted(MAX_GAP)
    metadata = {"label_source": "rules"}

    def predict_pairs(self, pairs):
        out = []
        for p in pairs:
            ents = p.get("entities") or [p["head"], p["tail"]]
            lab = predict_pair(p["text"], p["head"], p["tail"], p["allowed_relation"], ents)
            out.append({"label": lab, "score": 1.0 if lab != NEGATIVE else 0.0, "status": "predicted"})
        return out

    def predict(self, text, entities):
        pairs = candidates(text, entities)
        for p in pairs:
            p["entities"] = entities
        return [{"head": p["head"]["id"], "tail": p["tail"]["id"], "allowed_relation": p["allowed_relation"], **r}
                for p, r in zip(pairs, self.predict_pairs(pairs))]

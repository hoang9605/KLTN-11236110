"""Schema validation, explicit annotation loading and text-grouped splitting."""
import hashlib
import json
import random
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path

SCHEMA_PATH = Path(__file__).resolve().parents[1] / "re_labels.json"
SCHEMA = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
RELATIONS = {r["label"]: (r["head_type"], r["tail_type"]) for r in SCHEMA["relations"]}
NEGATIVE = SCHEMA["negative_label"]

# Thực thể chung chung bị loại khỏi gold RE v1 (quy ước người duyệt 05/11/2026).
# NER vẫn giữ chúng (nhãn nguồn TREATMENT/DIAGNOSTICS...), nhưng RE không sinh cặp cho chúng
# để đầu vào lúc suy luận khớp với dữ liệu huấn luyện. Nguồn duy nhất cho cả
# scripts/apply_paper_review.py và MedicalREPipeline.
GENERIC_ENTITIES = {
    "PROCEDURE": frozenset({"điều trị", "trị liệu", "điều trị giảm cân", "tập luyện"}),
    "DRUG": frozenset({"thuốc", "tân dược", "thuốc nền", "hoạt chất"}),
    "TEST": frozenset({"khám", "đánh giá", "chẩn đoán", "chuẩn đoán", "khảo sát", "thăm khám",
                       "khám bệnh", "tái khám", "thăm dò", "đo"}),
}


def is_generic(entity):
    text = unicodedata.normalize("NFC", entity.get("text") or entity.get("surface_text") or "")
    return " ".join(text.casefold().split()) in GENERIC_ENTITIES.get(entity.get("label"), ())


def text_group(text):
    normalized = " ".join(unicodedata.normalize("NFC", text).casefold().split())
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()


def validate_entities(text, entities):
    seen = set()
    for entity in entities:
        if entity["id"] in seen:
            raise ValueError("Duplicate entity ID")
        seen.add(entity["id"])
        start, end = entity["start"], entity["end"]
        if not isinstance(start, int) or not isinstance(end, int) or not 0 <= start < end <= len(text):
            raise ValueError("Invalid entity offsets")
        if entity["label"] not in SCHEMA["entity_types"]:
            raise ValueError("Unknown entity type")
        if entity.get("text", text[start:end]) != text[start:end]:
            raise ValueError("Entity surface does not match offsets")
    ordered = sorted(entities, key=lambda e: e["start"])
    if any(a["end"] > b["start"] for a, b in zip(ordered, ordered[1:])):
        raise ValueError("Overlapping entity spans are outside the flat RE scope")


def mark_pair(text, head, tail):
    spans = [(head["start"], head["end"], "HEAD", head["label"]),
             (tail["start"], tail["end"], "TAIL", tail["label"])]
    for start, end, role, label in sorted(spans, reverse=True):
        text = text[:start] + f"[{role}_{label}]" + text[start:end] + f"[/{role}]" + text[end:]
    return text


def candidates(text, entities):
    validate_entities(text, entities)
    result = []
    for head in entities:
        for tail in entities:
            for label, types in RELATIONS.items():
                if (head["label"], tail["label"]) == types:
                    result.append({"text": text, "head": head, "tail": tail,
                                   "allowed_relation": label, "features": mark_pair(text, head, tail)})
    return result


def load_pairs(path, allow_ai=False):
    """Keep only explicitly annotated pairs; never infer negatives from absent edges."""
    pairs = []
    audit = Counter()
    ids = set()
    for line in Path(path).read_text(encoding="utf-8-sig").splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        sid = row["id"]
        if sid in ids:
            raise ValueError(f"Duplicate sample ID: {sid}")
        ids.add(sid)
        audit["samples"] += 1
        human = row.get("human_verified") is True
        eligible = row.get("training_eligible") is True
        if not (human and eligible) and not allow_ai:
            raise ValueError(f"{sid}: requires explicit allow_ai=True for provisional annotations")
        validate_entities(row["text"], row["entities"])
        entities = {e["id"]: e for e in row["entities"]}
        seen = set()
        for relation in row["relations"]:
            key = (relation["head"], relation["tail"])
            if key in seen or any(e not in entities for e in key):
                raise ValueError(f"{sid}: duplicate pair or missing endpoint")
            seen.add(key)
            head, tail = (entities[e] for e in key)
            allowed = next((r for r, types in RELATIONS.items()
                            if types == (head["label"], tail["label"])), None)
            if allowed is None or relation.get("allowed_relation", allowed) != allowed:
                raise ValueError(f"{sid}: invalid relation direction/types")
            label = relation["label"]
            if label == "CHUA_RO":
                audit["unknown_pairs_excluded"] += 1
                continue
            if label not in (allowed, NEGATIVE):
                raise ValueError(f"{sid}: incompatible label {label}")
            flags = row.get("review_flags", [])
            audit["included_pairs_with_review_flags"] += bool(flags)
            pairs.append({"sample_id": sid, "group": text_group(row["text"]),
                          "text": row["text"], "head": head, "tail": tail,
                          "allowed_relation": allowed, "label": label,
                          "features": mark_pair(row["text"], head, tail),
                          "human_verified": human, "training_eligible": eligible,
                          "review_flags": flags, "source_split": row.get("source_split"),
                          "source_row_index": row.get("source_row_index")})
    audit["included_pairs"] = len(pairs)
    audit["samples_with_included_pairs"] = len({p["sample_id"] for p in pairs})
    return pairs, dict(audit)


def split_pairs(pairs, seed=42):
    """70/15/15 by normalized text; reserve one group per label in train first.

    Labels are used only to establish training coverage, before fitting. This
    does not promise held-out support for rare labels or speaker independence.
    """
    groups = defaultdict(list)
    for pair in pairs:
        groups[pair["group"]].append(pair)
    keys = sorted(groups)
    if len(keys) < 3:
        raise ValueError("At least three distinct text groups are required")
    random.Random(seed).shuffle(keys)
    by_label = defaultdict(set)
    for key in keys:
        for pair in groups[key]:
            by_label[pair["label"]].add(key)
    reserved = set()
    for label in sorted(by_label, key=lambda label: (len(by_label[label]), label)):
        if not reserved & by_label[label]:
            reserved.add(next(key for key in keys if key in by_label[label]))
    remaining = [key for key in keys if key not in reserved]
    holdout = max(1, round(len(keys) * 0.15))
    if len(remaining) < 2 * holdout:
        raise ValueError("Not enough groups for train label coverage and dev/test")
    assigned = {"dev": remaining[:holdout], "test": remaining[holdout:2 * holdout],
                "train": [key for key in keys if key in reserved] + remaining[2 * holdout:]}
    return {split: [p for key in assigned[split] for p in groups[key]] for split in ("train", "dev", "test")}

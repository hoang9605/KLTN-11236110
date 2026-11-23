"""(B) Sinh dữ liệu RE theo pattern, không dùng LLM.

Ba phương pháp, mọi bản ghi đều có annotation_status = SYNTHETIC_PATTERN:

1. mention_replacement: lấy câu seed thật (gold v1 + ai v2) và thay MỘT thực thể bằng
   thực thể cùng kiểu trong re_v3/lexicon.json. Ngữ cảnh và nhãn giữ nguyên.
   - Thực thể nằm trong cặp dương: chỉ thay khi thực thể mới cùng nhóm chuyên khoa với
     mọi đối tác dương của nó (ràng buộc hợp lý).
   - Thực thể chỉ nằm trong cặp âm: thay bằng bất kỳ thực thể cùng kiểu nào.
2. template: điền cặp thực thể cùng nhóm vào pattern dương. Pattern dương gồm hai nguồn:
   - pattern ngắn khai thác được từ seed (data/patterns/pair_contexts.jsonl);
   - pattern viết tay theo docs/RE_LABELS.md và relation_extraction/rules.CUES.
   Câu được bọc thêm từ đệm đầu/cuối kiểu lời nói.
3. hard_negative: cặp âm khó, cùng kiểu và cùng nhóm nhưng không có quan hệ:
   - tác dụng phụ, phòng bệnh;
   - phủ định (theo quy ước gold v1: phủ định -> NO_RELATION);
   - thực thể gây nhiễu (một cặp dương và một cặp âm trong cùng câu).

Sau khi sinh: loại câu trùng (theo text_group), rồi lấy mẫu bớt các bản ghi chỉ có cặp âm
sao cho tỉ lệ dương nằm trong config.TARGET_POSITIVE_RATIO.

Đầu ra:
  data/synthetic/pattern_v1.jsonl
  data/synthetic/pattern_v1.manifest.json
  data/synthetic/pattern_v1.preview.md

Chạy: .venv\\Scripts\\python.exe -X utf8 -m re_v3.synth_pattern
"""
import argparse
import json
import random
from collections import Counter, defaultdict
from pathlib import Path

from relation_extraction.data import NEGATIVE, RELATIONS, is_generic, text_group

from . import config
from .common import check_record, norm, read_jsonl, write_jsonl

LEXICON_PATH = config.HERE / "lexicon.json"
STATUS = "SYNTHETIC_PATTERN"
DISTRACTOR_SHARE = 0.3
ORAL_VERBS = {"uống", "tiêm"}

# Slot H = head, T = tail. H2/T2 là thực thể thứ hai cùng kiểu, dùng cho mẫu gây nhiễu.
# pairs: (head_slot, tail_slot, có quan hệ hay không)
HANDWRITTEN = {
    "located_at": [
        "{H} ở {T}", "bị {H} ở vùng {T}", "{H} tại {T}", "{T} bị {H}", "{T} của mình nó bị {H}",
        "{H} trong {T}", "{H} ở cái {T}", "cái {T} của chúng ta nó bị {H}", "{H} {T}",
        "{H} xuất hiện ở {T}", "{H} ở phía {T}",
    ],
    "treated_by": [
        "{H} thì phải uống {T}", "điều trị {H} bằng {T}", "dùng {T} để điều trị {H}",
        "{T} để điều trị cho {H}", "bác sĩ kê {T} cho bệnh nhân bị {H}", "{H} được điều trị bằng {T}",
        "người bị {H} đều phải sử dụng {T}", "uống {T} để chữa {H}", "{H} thì bác sĩ cho dùng {T}",
        "tiêm {T} để trị {H}",
    ],
    "treated_by_procedure": [
        "{H} thì phương pháp {T}", "điều trị {H} bằng phương pháp {T}", "{T} giúp cải thiện {H}",
        "người bệnh {H} đã được {T}", "tiến hành {T} cho người bị {H}", "{H} thì phải {T}",
        "{T} để điều trị {H}", "chữa {H} bằng {T}", "can thiệp {T} cho người bệnh {H}",
    ],
    "diagnosed_by": [
        "{T} để phát hiện {H}", "chẩn đoán {H} qua {T}", "làm {T} thì thấy {H}", "{T} cho thấy {H}",
        "xác định {H} bằng {T}", "tầm soát {H} bằng {T}", "{T} dương tính với {H}",
        "đi {T} thì phát hiện ra {H}", "kiểm tra {H} bằng {T}", "{T} {H}",
    ],
    "has_dosage": [
        "{H} {T}", "uống {H} {T}", "{H} liều {T}", "dùng {H} mỗi lần {T}", "{H} với liều {T}",
        "tiêm {H} {T}", "bác sĩ cho {H} {T}", "{H} khoảng {T}",
    ],
}

HARD_NEGATIVES = {
    "located_at": [
        ("{H} không liên quan gì đến {T}", [("H", "T", False)]),
        ("{H} chứ không phải ở {T}", [("H", "T", False)]),
        ("{H} thì không ảnh hưởng tới {T}", [("H", "T", False)]),
        ("{H} ở {T} chứ không phải ở {T2}", [("H", "T", True), ("H", "T2", False)]),
        ("bị {H} ở {T} còn {T2} thì vẫn bình thường", [("H", "T", True), ("H", "T2", False)]),
    ],
    "treated_by": [
        ("{T} có thể gây ra {H}", [("H", "T", False)]),
        ("tác dụng phụ của {T} là {H}", [("H", "T", False)]),
        ("dùng {T} để phòng ngừa {H}", [("H", "T", False)]),
        ("{H} không cải thiện với {T}", [("H", "T", False)]),
        ("{H} mà uống {T} cũng không đỡ", [("H", "T", False)]),
        ("bị {H} và trước đây có dùng {T}", [("H", "T", False)]),
        ("{H} thì uống {T} còn {H2} thì không cần", [("H", "T", True), ("H2", "T", False)]),
    ],
    "treated_by_procedure": [
        ("{T} có thể gây ra {H}", [("H", "T", False)]),
        ("sau khi {T} thì bị {H}", [("H", "T", False)]),
        ("{H} không cải thiện sau khi {T}", [("H", "T", False)]),
        ("{T} để dự phòng {H}", [("H", "T", False)]),
        ("{H} thì phải {T} còn {H2} thì chỉ cần theo dõi", [("H", "T", True), ("H2", "T", False)]),
    ],
    "diagnosed_by": [
        ("{T} không phát hiện được {H}", [("H", "T", False)]),
        ("{H} thì không cần phải làm {T}", [("H", "T", False)]),
        ("{H} thì không chẩn đoán bằng {T} được", [("H", "T", False)]),
        ("{T} để phát hiện {H} chứ không phát hiện được {H2}", [("H", "T", True), ("H2", "T", False)]),
    ],
    "has_dosage": [
        ("{H} {T} còn {H2} thì", [("H", "T", True), ("H2", "T", False)]),
        ("uống {H} {T} rồi mới uống {H2}", [("H", "T", True), ("H2", "T", False)]),
        ("{H} thì không nên dùng quá {T}", [("H", "T", True)]),
        ("không biết {H} là bao nhiêu còn {H2} thì {T}", [("H2", "T", True), ("H", "T", False)]),
    ],
}


class Lexicon:
    def __init__(self, path=LEXICON_PATH):
        data = json.loads(Path(path).read_text(encoding="utf-8"))
        self.groups = data["groups"]
        self.dosage_drugs = data["dosage_drugs"]
        self.topical_drugs = data.get("topical_drugs", [])
        self.dosages = data["dosages"]
        self.prefixes = data["prefixes"]
        self.suffixes = data["suffixes"]
        self.groups_of = defaultdict(set)          # (label, norm text) -> {group}
        self.by_type = defaultdict(set)            # label -> {text}
        for g, types in self.groups.items():
            for label, items in types.items():
                for t in items:
                    self.groups_of[(label, norm(t))].add(g)
                    self.by_type[label].add(t)
        for t in self.dosage_drugs:
            self.by_type["DRUG"].add(t)
        for t in self.dosages:
            self.by_type["DOSAGE"].add(t)
        self.by_type = {k: sorted(v) for k, v in self.by_type.items()}

    def groups_for(self, entity):
        return self.groups_of.get((entity["label"], norm(entity["text"])), set())

    def pick(self, rng, group, label, exclude=()):
        if label == "DOSAGE":
            pool = self.dosages
        elif group is None:
            pool = self.by_type[label]
        else:
            pool = self.groups[group].get(label, [])
        pool = [t for t in pool if norm(t) not in {norm(x) for x in exclude}]
        return rng.choice(pool) if pool else None


def make_record(rid, method, text, entities, relations, **meta):
    row = {"id": rid, "source": "re_v3.synth_pattern", "method": method, "text": text,
           "entities": entities, "relations": relations, "annotation_status": STATUS,
           "annotator": "re_v3/synth_pattern.py (tự động, chưa người duyệt)",
           "human_verified": False, "training_eligible": False, "review_flags": []}
    row.update(meta)
    check_record(row)
    return row


def render(template, fills, prefix="", suffix=""):
    """Điền slot vào template; trả về text và offset từng slot."""
    parts = template.split("{")
    text, spans = (prefix + " " if prefix else "") + parts[0], {}
    for part in parts[1:]:
        slot, rest = part.split("}", 1)
        start = len(text)
        text += fills[slot]
        spans[slot] = (start, len(text))
        text += rest
    return text + (" " + suffix if suffix else ""), spans


# ---------- 1. mention replacement ----------

def replace_entity(row, eid, new_text):
    ent = next(e for e in row["entities"] if e["id"] == eid)
    delta = len(new_text) - (ent["end"] - ent["start"])
    text = row["text"][:ent["start"]] + new_text + row["text"][ent["end"]:]
    entities = []
    for e in row["entities"]:
        e = {k: e[k] for k in ("id", "label", "start", "end")}
        if e["id"] == eid:
            e["end"] = e["start"] + len(new_text)
        elif e["start"] >= ent["end"]:
            e["start"] += delta
            e["end"] += delta
        e["text"] = text[e["start"]:e["end"]]
        entities.append(e)
    return text, entities


def mention_replacement(seed_rows, lex, rng, per_sentence):
    out = []
    for row in seed_rows:
        relations = [{"head": r["head"], "tail": r["tail"], "allowed_relation": r["allowed_relation"],
                      "label": r["label"]} for r in row["relations"] if r["label"] != "CHUA_RO"]
        if not relations:
            continue
        ents = {e["id"]: e for e in row["entities"]}
        involved = {x for r in relations for x in (r["head"], r["tail"])}
        options = []
        for eid in sorted(involved):
            e = ents[eid]
            # Không thay DOSAGE: nhiều cặp has_dosage âm trong seed là âm vì mention liều là nhiễu
            # ("nồng độ", "cao"). Thay bằng liều thật sẽ biến chúng thành dương mà nhãn vẫn là âm.
            if is_generic(e) or e["label"] not in lex.by_type or e["label"] == "DOSAGE":
                continue
            partners = [ents[r["tail"] if r["head"] == eid else r["head"]]
                        for r in relations if eid in (r["head"], r["tail"]) and r["label"] != NEGATIVE]
            if partners:
                # nhóm hợp lệ = nhóm mà mọi đối tác dương đều thuộc về
                groups = set.intersection(*(lex.groups_for(p) for p in partners))
                if not groups:
                    continue
                options.append((eid, sorted(groups)))
            elif norm(e["text"]) in {norm(t) for t in lex.by_type[e["label"]]}:
                # Thực thể chỉ ở cặp âm: chỉ thay khi mention gốc là thực thể thật (có trong từ điển).
                # Nếu mention gốc là nhiễu NER (TEST "nghiên cứu"), cặp âm có thể âm vì nhiễu đó,
                # và thay bằng thực thể thật sẽ làm sai nhãn.
                options.append((eid, [None]))
        if not options:
            continue
        rng.shuffle(options)
        made = 0
        for attempt in range(per_sentence * 3):
            if made >= per_sentence:
                break
            eid, groups = options[attempt % len(options)]
            e = ents[eid]
            new = lex.pick(rng, rng.choice(groups), e["label"], exclude=[e["text"]])
            if not new:
                continue
            text, entities = replace_entity({"text": row["text"], "entities": row["entities"]}, eid, new)
            out.append(("mention_replacement", text, entities, relations,
                        {"parent_id": row["id"], "replaced": {"entity": eid, "old": e["text"], "new": new}}))
            made += 1
    return out


# ---------- 2 + 3. template ----------

def mined_templates(contexts):
    """Pattern dương ngắn từ seed -> template '{H} ở {T}' (giữ thứ tự xuất hiện)."""
    seen = defaultdict(set)
    for c in contexts:
        if not c["positive"] or c["pattern"] == "<LONG>" or any(w.startswith("[") for w in c["between"]):
            continue
        mid = " ".join(c["between"])
        first, second = ("{H}", "{T}") if c["order"] == "H…T" else ("{T}", "{H}")
        seen[c["relation"]].add(f"{first} {mid} {second}" if mid else f"{first} {second}")
    return {rel: sorted(t) for rel, t in seen.items()}


def slot_label(slot, relation):
    head, tail = RELATIONS[relation]
    return head if slot.startswith("H") else tail


def fill(template, pairs, relation, lex, rng):
    slots = sorted({p.split("}")[0] for p in template.split("{")[1:]})
    if relation == "has_dosage":
        group = None
    else:
        group = rng.choice(sorted(lex.groups))
    fills = {}
    for slot in slots:
        label = slot_label(slot, relation)
        if relation == "has_dosage" and label == "DRUG":
            pool = [d for d in lex.dosage_drugs if d not in fills.values()]
            fills[slot] = rng.choice(pool)
        else:
            exclude = list(fills.values())
            if label == "DRUG" and ORAL_VERBS & set(template.split()):
                exclude += lex.topical_drugs          # tránh "uống kem bôi"
            fills[slot] = lex.pick(rng, group, label, exclude=exclude)
        if fills[slot] is None:
            return None
    prefix, suffix = rng.choice(lex.prefixes), rng.choice(lex.suffixes)
    text, spans = render(template, fills, prefix, suffix)
    entities = []
    ids = {}
    for i, slot in enumerate(sorted(spans, key=lambda s: spans[s][0]), 1):
        s, e = spans[slot]
        ids[slot] = f"E{i}"
        entities.append({"id": f"E{i}", "label": slot_label(slot, relation), "start": s, "end": e,
                         "text": text[s:e]})
    relations = [{"head": ids[h], "tail": ids[t], "allowed_relation": relation,
                  "label": relation if pos else NEGATIVE} for h, t, pos in pairs]
    return text, entities, relations, {"group": group, "template": template}


def templates(contexts, lex, rng, positives_per_relation, hard_negative_ratio, existing_pos):
    out = []
    mined = mined_templates(contexts)
    for relation in sorted(RELATIONS):
        pos_tpls = sorted(set(HANDWRITTEN[relation]) | set(mined.get(relation, [])))
        have = existing_pos[relation]
        # Mẫu âm khó trước. Mẫu gây nhiễu cũng chứa một cặp dương, nên tính vào hạn mức dương.
        # Cặp dương từ mẫu gây nhiễu bị giới hạn ở DISTRACTOR_SHARE hạn mức, để phần lớn cặp
        # dương đến từ template dương đa dạng hơn. has_dosage không có mẫu âm thuần (mọi mẫu âm
        # đều cần một thuốc khác giữ liều), nên âm của has_dosage chủ yếu đến từ thay thực thể.
        pure = [(t, p) for t, p in HARD_NEGATIVES[relation] if not any(x[2] for x in p)]
        cap = have + int(positives_per_relation * DISTRACTOR_SHARE)
        for _ in range(int(positives_per_relation * hard_negative_ratio)):
            choices = HARD_NEGATIVES[relation] if have < cap else pure
            if not choices:
                break
            tpl, pairs = rng.choice(choices)
            r = fill(tpl, pairs, relation, lex, rng)
            if r:
                out.append(("hard_negative", *r[:3], r[3]))
                have += sum(1 for x in pairs if x[2])
        need, tries = positives_per_relation - have, 0
        while need > 0 and tries < positives_per_relation * 20:
            tries += 1
            r = fill(rng.choice(pos_tpls), [("H", "T", True)], relation, lex, rng)
            if r:
                out.append(("template", *r[:3], r[3]))
                need -= 1
    return out


# ---------- tổng hợp ----------

def pair_counts(rows):
    pos, neg = Counter(), Counter()
    for r in rows:
        for rel in r["relations"]:
            (pos if rel["label"] != NEGATIVE else neg)[rel["allowed_relation"]] += 1
    return pos, neg


def ratio(rows):
    pos, neg = pair_counts(rows)
    total = sum(pos.values()) + sum(neg.values())
    return sum(pos.values()) / total if total else 0.0


def balance(rows, rng, target):
    """Đưa tỉ lệ dương (theo cặp) vào khoảng target.

    - Quá thấp: bỏ bớt bản ghi chỉ có cặp âm, tới ngưỡng dưới.
    - Quá cao: bỏ bớt bản ghi 'template' chỉ có cặp dương, tới ngưỡng trên, lấy từ quan hệ nhiều dương nhất,
      để giữ cân bằng giữa các lớp. Bản ghi thật đã thay thực thể và mẫu âm khó được giữ.
    """
    rows = list(rows)
    if ratio(rows) < target[0]:
        neg_only = [r for r in rows if all(x["label"] == NEGATIVE for x in r["relations"])]
        rng.shuffle(neg_only)
        drop = set()
        pos_n = sum(1 for r in rows for x in r["relations"] if x["label"] != NEGATIVE)
        total_n = sum(len(r["relations"]) for r in rows)
        for r in neg_only:
            if pos_n / total_n >= target[0]:
                break
            drop.add(r["id"])
            total_n -= len(r["relations"])
        return [r for r in rows if r["id"] not in drop]
    if ratio(rows) > target[1]:
        removable = defaultdict(list)
        for r in rows:
            if r["method"] == "template":
                removable[r["relations"][0]["allowed_relation"]].append(r)
        for lst in removable.values():
            rng.shuffle(lst)
        pos, _ = pair_counts(rows)
        pos_n = sum(pos.values())
        total_n = sum(len(r["relations"]) for r in rows)
        drop = set()
        while pos_n / total_n > target[1]:
            rel = max((k for k in removable if removable[k]), key=lambda k: pos[k], default=None)
            if rel is None:
                break
            r = removable[rel].pop()
            drop.add(r["id"])
            pos[rel] -= 1
            pos_n -= 1
            total_n -= 1
        return [r for r in rows if r["id"] not in drop]
    return rows


def generate(seed=config.SEED, positives_per_relation=250, per_sentence=5, hard_negative_ratio=2.0,
             target=config.TARGET_POSITIVE_RATIO, lexicon=None):
    rng = random.Random(seed)
    lex = lexicon or Lexicon()
    seed_rows = [r for path in config.SEED_FILES for r in read_jsonl(path)]
    contexts = read_jsonl(config.PATTERNS_DIR / "pair_contexts.jsonl")

    raw = mention_replacement(seed_rows, lex, rng, per_sentence)
    mr_pos = Counter(rel["allowed_relation"] for *_, rels, _ in raw for rel in rels if rel["label"] != NEGATIVE)
    raw += templates(contexts, lex, rng, positives_per_relation, hard_negative_ratio, mr_pos)

    seen = {text_group(r["text"]) for r in seed_rows}
    rows, audit = [], Counter()
    for method, text, entities, relations, meta in raw:
        g = text_group(text)
        if g in seen:
            audit["skip_duplicate_text"] += 1
            continue
        seen.add(g)
        rows.append(make_record(f"SP-{len(rows) + 1:05d}", method, text, entities, relations, **meta))
    before = len(rows)
    rows = balance(rows, rng, target)
    audit["dropped_for_positive_ratio"] = before - len(rows)
    rows.sort(key=lambda r: r["id"])
    return rows, dict(audit)


def preview(rows, rng, n=40):
    sample = rng.sample(rows, min(n, len(rows)))
    lines = ["# Xem nhanh pattern_v1 (mẫu ngẫu nhiên)", "",
             "| ID | Cách sinh | Câu | Cặp |", "|---|---|---|---|"]
    for r in sorted(sample, key=lambda r: r["id"]):
        ents = {e["id"]: e["text"] for e in r["entities"]}
        pairs = "; ".join(f"{ents[x['head']]} → {ents[x['tail']]}: {x['label']}" for x in r["relations"])
        lines.append(f"| {r['id']} | {r['method']} | {r['text']} | {pairs} |")
    return "\n".join(lines) + "\n"


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--out", default=str(config.SYNTHETIC_DIR / "pattern_v1.jsonl"))
    ap.add_argument("--seed", type=int, default=config.SEED)
    ap.add_argument("--positives-per-relation", type=int, default=250)
    ap.add_argument("--per-sentence", type=int, default=5, help="số biến thể thay thực thể mỗi câu seed")
    ap.add_argument("--hard-negative-ratio", type=float, default=2.0,
                    help="số mẫu âm khó mỗi quan hệ = tỉ lệ này × positives-per-relation")
    args = ap.parse_args()
    if not (config.PATTERNS_DIR / "pair_contexts.jsonl").exists():
        raise SystemExit("Chưa có pair_contexts.jsonl, chạy trước: python -m re_v3.mine_patterns")

    rows, audit = generate(args.seed, args.positives_per_relation, args.per_sentence, args.hard_negative_ratio)
    out = Path(args.out)
    write_jsonl(out, rows)
    pos, neg = pair_counts(rows)
    manifest = {
        "script": "re_v3/synth_pattern.py", "seed": args.seed, "args": vars(args),
        "seed_files": [str(p.relative_to(config.ROOT)) for p in config.SEED_FILES],
        "lexicon": str(LEXICON_PATH.relative_to(config.ROOT)),
        "records": len(rows), "pairs": sum(pos.values()) + sum(neg.values()),
        "positive_ratio": round(ratio(rows), 3), "target_positive_ratio": list(config.TARGET_POSITIVE_RATIO),
        "positives_by_relation": dict(sorted(pos.items())), "negatives_by_relation": dict(sorted(neg.items())),
        "records_by_method": dict(Counter(r["method"] for r in rows)), "audit": audit,
        "warning": "Dữ liệu tự sinh, chưa người duyệt, chưa qua filter_synth.py. Không dùng làm test.",
    }
    out.with_suffix(".manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=1), encoding="utf-8")
    out.with_suffix(".preview.md").write_text(preview(rows, random.Random(args.seed)), encoding="utf-8")
    print(json.dumps({k: manifest[k] for k in ("records", "pairs", "positive_ratio", "positives_by_relation",
                                                "negatives_by_relation", "records_by_method", "audit")},
                     ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()

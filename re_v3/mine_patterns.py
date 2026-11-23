"""(A) Khai thác pattern từ dữ liệu seed đã gán nhãn.

Với mỗi cặp có nhãn (bỏ CHUA_RO), lấy chuỗi từ nằm giữa hai thực thể. Thực thể khác
chen giữa được thay bằng [KIỂU]. Sau đó gom theo (quan hệ, nhãn, thứ tự, chuỗi giữa).

Đầu ra:
  data/patterns/pair_contexts.jsonl  ngữ cảnh từng cặp (dùng cho synth_pattern.py)
  data/patterns/patterns.jsonl       pattern đã gom, kèm số lần và ví dụ
  data/patterns/summary.md           bảng tóm tắt để duyệt tay

Chạy: .venv\\Scripts\\python.exe -X utf8 -m re_v3.mine_patterns
"""
import argparse
from collections import Counter, defaultdict
from pathlib import Path

from relation_extraction.data import NEGATIVE, load_pairs
from relation_extraction.rules import CUES

from . import config
from .common import read_jsonl, words, write_jsonl


def between_pattern(text, first, second, entities, head):
    """Chuỗi giữa hai thực thể; thực thể khác chen giữa thay bằng [KIỂU]."""
    parts, pos = [], first["end"]
    for e in sorted(entities, key=lambda e: e["start"]):
        if e is first or e is second or not (first["end"] <= e["start"] and e["end"] <= second["start"]):
            continue
        parts += words(text[pos:e["start"]]) + [f"[{e['label']}]"]
        pos = e["end"]
    parts += words(text[pos:second["start"]])
    return parts


def pair_context(pair, entities):
    text, head, tail = pair["text"], pair["head"], pair["tail"]
    first, second = sorted((head, tail), key=lambda e: e["start"])
    between = between_pattern(text, first, second, entities, head)
    order = "H…T" if first is head else "T…H"
    left = words(text[:first["start"]])[-config.CONTEXT_WORDS:]
    right = words(text[second["end"]:])[:config.CONTEXT_WORDS]
    key = " ".join(between) if len(between) <= config.MAX_BETWEEN_WORDS else "<LONG>"
    rel = pair["allowed_relation"]
    cues = [c for c in CUES.get(rel, []) if f" {c} " in f" {' '.join(between)} "]
    return {
        "sample_id": pair["sample_id"], "relation": rel, "label": pair["label"],
        "positive": pair["label"] != NEGATIVE, "order": order,
        "head": {k: head[k] for k in ("text", "label", "start", "end")},
        "tail": {k: tail[k] for k in ("text", "label", "start", "end")},
        "between": between, "gap": len(between), "pattern": key,
        "left": left, "right": right, "rule_cues": cues,
        "human_verified": pair["human_verified"], "text": text,
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--out", default=str(config.PATTERNS_DIR))
    args = ap.parse_args()

    contexts = []
    for path in config.SEED_FILES:
        pairs, audit = load_pairs(path, allow_ai=True)
        rows = {r["id"]: r["entities"] for r in read_jsonl(path)}
        for p in pairs:
            ents = rows[p["sample_id"]]
            head = next(e for e in ents if e["id"] == p["head"]["id"])
            tail = next(e for e in ents if e["id"] == p["tail"]["id"])
            contexts.append(pair_context({**p, "head": head, "tail": tail}, ents))
        print(f"{path.parent.name}: {audit['included_pairs']} cặp, bỏ {audit.get('unknown_pairs_excluded', 0)} CHUA_RO")

    groups = defaultdict(list)
    for c in contexts:
        groups[(c["relation"], c["label"], c["order"], c["pattern"])].append(c)

    patterns = []
    for (rel, label, order, pat), items in groups.items():
        patterns.append({
            "relation": rel, "label": label, "positive": label != NEGATIVE, "order": order,
            "between": pat, "count": len(items),
            "rule_cues": sorted({cue for c in items for cue in c["rule_cues"]}),
            "examples": [{"sample_id": c["sample_id"], "head": c["head"]["text"], "tail": c["tail"]["text"],
                          "text": c["text"]} for c in items[:3]],
            "review": "single" if len(items) == 1 else "ok",
        })
    patterns.sort(key=lambda p: (p["relation"], not p["positive"], -p["count"], p["between"]))

    out = Path(args.out)
    write_jsonl(out / "pair_contexts.jsonl", contexts)
    write_jsonl(out / "patterns.jsonl", patterns)

    by_rel = Counter((c["relation"], c["positive"]) for c in contexts)
    lines = ["# Pattern bank RE v3 (tự sinh bởi mine_patterns.py)", "",
             "Nguồn: " + ", ".join(p.parent.name for p in config.SEED_FILES) + ". CHUA_RO đã bị loại.", "",
             "| Quan hệ | Cặp dương | Cặp âm | Pattern dương | Pattern âm |", "|---|---:|---:|---:|---:|"]
    for rel in sorted({c["relation"] for c in contexts}):
        pp = sum(1 for p in patterns if p["relation"] == rel and p["positive"])
        pn = sum(1 for p in patterns if p["relation"] == rel and not p["positive"])
        lines.append(f"| {rel} | {by_rel[(rel, True)]} | {by_rel[(rel, False)]} | {pp} | {pn} |")
    for rel in sorted({c["relation"] for c in contexts}):
        for positive in (True, False):
            sel = [p for p in patterns if p["relation"] == rel and p["positive"] == positive][:15]
            if not sel:
                continue
            lines += ["", f"## {rel} — {'dương' if positive else 'âm'}", "",
                      "| Số lần | Thứ tự | Chuỗi giữa | Ví dụ (head → tail) |", "|---:|---|---|---|"]
            for p in sel:
                ex = p["examples"][0]
                between = p["between"] or "(liền kề)"
                lines.append(f"| {p['count']} | {p['order']} | `{between}` | {ex['head']} → {ex['tail']} |")
    (out / "summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"{len(contexts)} ngữ cảnh cặp, {len(patterns)} pattern -> {out}")
    for (rel, pos), n in sorted(by_rel.items()):
        print(f"  {rel:22s} {'dương' if pos else 'âm  '} {n}")


if __name__ == "__main__":
    main()

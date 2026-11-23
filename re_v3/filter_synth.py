"""Bộ lọc chung cho dữ liệu synthetic/silver trước khi đưa vào huấn luyện.

Các bước, theo thứ tự:
  1. check_record: định dạng, offset, kiểu thực thể, annotation_status, human_verified=false.
  2. Rò rỉ test: loại câu có chung một n-gram từ (n = config.LEAK_NGRAM) với câu bất kỳ trong
     config.TEST_FILES. Loại luôn câu trùng y hệt câu test.
  3. Trùng lặp: loại câu trùng (text_group), kể cả trùng với seed. Mỗi "khung" câu (thực thể
     thay bằng [KIỂU]) giữ tối đa config.MAX_PER_SKELETON câu, để bớt lặp template.
  4. Đối chiếu luật (chỉ đánh dấu, không loại): bản ghi nào có cặp mà luật cho nhãn khác thì ghi
     filter_flags. Mẫu âm khó cố ý chứa từ gợi ý ("dùng … để phòng ngừa"), nên luật bắn nhầm
     trên mẫu âm khó là đúng thiết kế. Recall của luật thấp, nên luật nói âm cũng không có nghĩa
     là nhãn dương sai. Cờ chỉ dùng để ưu tiên khi duyệt tay.
  5. Cân bằng lại tỉ lệ dương nếu bước 2–3 làm lệch (dùng lại synth_pattern.balance).
  6. --scale K (tùy chọn): lấy mẫu phân tầng theo quan hệ, còn khoảng K × config.SEED_PAIRS cặp, giữ tỉ lệ dương.
  7. Lấy mẫu duyệt tay: config.MANUAL_REVIEW_FRACTION mỗi (quan hệ, nhãn, cách sinh), ưu tiên
     bản ghi có cờ. Ghi ra CSV để mở bằng Excel.

Đầu ra (trong --out-dir, tên theo file đầu vào):
  <tên>.jsonl, <tên>.manifest.json, <tên>_review.csv, và <tên>_x<K>.jsonl nếu có --scale

Chạy: .venv\\Scripts\\python.exe -X utf8 -m re_v3.filter_synth re_v3/data/synthetic/pattern_v1.jsonl --scale 1
"""
import argparse
import csv
import json
import random
from collections import Counter, defaultdict
from pathlib import Path

from relation_extraction.data import NEGATIVE, text_group
from relation_extraction.rules import predict_pair

from . import config
from .common import check_record, read_jsonl, words, write_jsonl
from .synth_pattern import balance, pair_counts, ratio


def ngrams(text, n):
    w = words(text)
    return {tuple(w[i:i + n]) for i in range(len(w) - n + 1)}


def test_index(paths=None, n=config.LEAK_NGRAM):
    grams, groups = set(), set()
    for path in paths or config.TEST_FILES:
        for row in read_jsonl(path):
            grams |= ngrams(row["text"], n)
            groups.add(text_group(row["text"]))
    return grams, groups


def skeleton(row):
    text = row["text"]
    for e in sorted(row["entities"], key=lambda e: -e["start"]):
        text = text[:e["start"]] + f"[{e['label']}]" + text[e["end"]:]
    return " ".join(text.split())


def rule_flags(row):
    ents = {e["id"]: e for e in row["entities"]}
    flags = []
    for rel in row["relations"]:
        rule = predict_pair(row["text"], ents[rel["head"]], ents[rel["tail"]], rel["allowed_relation"],
                            row["entities"])
        if rule != rel["label"]:
            kind = "rule_says_positive" if rule != NEGATIVE else "rule_says_negative"
            flags.append(f"{kind}:{rel['head']}->{rel['tail']}")
    return flags


def subsample(rows, n_pairs, rng):
    """Lấy mẫu theo bản ghi, phân tầng theo quan hệ chính của bản ghi, giữ tỉ lệ dương."""
    total = sum(len(r["relations"]) for r in rows)
    if n_pairs >= total:
        return rows
    frac = n_pairs / total
    strata = defaultdict(list)
    for r in rows:
        has_pos = any(x["label"] != NEGATIVE for x in r["relations"])
        strata[(r["relations"][0]["allowed_relation"], has_pos)].append(r)
    keep = []
    for key in sorted(strata):
        lst = strata[key][:]
        rng.shuffle(lst)
        keep += lst[:max(1, round(len(lst) * frac))]
    return sorted(keep, key=lambda r: r["id"])


def review_sample(rows, rng, fraction=config.MANUAL_REVIEW_FRACTION):
    strata = defaultdict(list)
    for r in rows:
        for i, rel in enumerate(r["relations"]):
            strata[(rel["allowed_relation"], rel["label"] != NEGATIVE, r.get("method", ""))].append((r, i))
    out = []
    for key in sorted(strata):
        items = strata[key][:]
        rng.shuffle(items)
        items.sort(key=lambda x: not x[0].get("filter_flags"))   # có cờ lên trước
        out += items[:max(1, round(len(items) * fraction))]
    return out


def write_review_csv(path, sample):
    with open(path, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(["id", "method", "relation", "head", "tail", "label", "text", "flags",
                    "dung_nhan (1/0)", "ghi_chu"])
        for r, i in sample:
            rel = r["relations"][i]
            ents = {e["id"]: e["text"] for e in r["entities"]}
            w.writerow([r["id"], r.get("method", ""), rel["allowed_relation"], ents[rel["head"]], ents[rel["tail"]],
                        rel["label"], r["text"], ";".join(r.get("filter_flags", [])), "", ""])


def run(rows, rng, test_paths=None, scale=None):
    grams, test_groups = test_index(test_paths)
    seed_groups = {text_group(r["text"]) for p in config.SEED_FILES for r in read_jsonl(p)}
    audit, kept, seen, per_skel = Counter(), [], set(), Counter()
    for row in rows:
        try:
            check_record(row)
        except (ValueError, KeyError) as e:
            audit["drop_invalid"] += 1
            continue
        g = text_group(row["text"])
        if g in test_groups or ngrams(row["text"], config.LEAK_NGRAM) & grams:
            audit["drop_test_leak"] += 1
            continue
        if g in seen or g in seed_groups:
            audit["drop_duplicate"] += 1
            continue
        sk = skeleton(row)
        if per_skel[sk] >= config.MAX_PER_SKELETON:
            audit["drop_skeleton_cap"] += 1
            continue
        seen.add(g)
        per_skel[sk] += 1
        row = {**row, "filter_flags": rule_flags(row)}
        kept.append(row)
    before = len(kept)
    kept = balance(kept, rng, config.TARGET_POSITIVE_RATIO)
    audit["drop_rebalance"] = before - len(kept)
    scaled = subsample(kept, int(scale * config.SEED_PAIRS), rng) if scale else None
    return kept, scaled, dict(audit)


def summary(rows):
    pos, neg = pair_counts(rows)
    return {"records": len(rows), "pairs": sum(pos.values()) + sum(neg.values()),
            "positive_ratio": round(ratio(rows), 3),
            "positives_by_relation": dict(sorted(pos.items())), "negatives_by_relation": dict(sorted(neg.items())),
            "records_by_method": dict(Counter(r.get("method") for r in rows)),
            "records_with_rule_flags": sum(bool(r.get("filter_flags")) for r in rows),
            "rule_flags_by_kind_and_method": dict(Counter(
                f"{f.split(':')[0]}|{r.get('method')}" for r in rows for f in r.get("filter_flags", [])))}


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("inputs", nargs="+", type=Path)
    ap.add_argument("--out-dir", type=Path, default=config.FILTERED_DIR)
    ap.add_argument("--scale", type=float, help="ghi thêm bản lấy mẫu còn khoảng K × số cặp seed")
    ap.add_argument("--seed", type=int, default=config.SEED)
    args = ap.parse_args()
    rows = [r for p in args.inputs for r in read_jsonl(p)]
    rng = random.Random(args.seed)
    kept, scaled, audit = run(rows, rng, scale=args.scale)
    name = "+".join(p.stem for p in args.inputs)
    out = args.out_dir / f"{name}.jsonl"
    write_jsonl(out, kept)
    sample = review_sample(kept, random.Random(args.seed))
    write_review_csv(args.out_dir / f"{name}_review.csv", sample)
    manifest = {"script": "re_v3/filter_synth.py", "inputs": [str(p) for p in args.inputs], "seed": args.seed,
                "input_records": len(rows), "audit": audit,
                "test_files": [str(p.relative_to(config.ROOT)) for p in config.TEST_FILES],
                "leak_ngram": config.LEAK_NGRAM, "max_per_skeleton": config.MAX_PER_SKELETON,
                "kept": summary(kept), "review_sample_pairs": len(sample)}
    if scaled is not None:
        tag = f"x{args.scale:g}"
        write_jsonl(args.out_dir / f"{name}_{tag}.jsonl", scaled)
        manifest[f"scaled_{tag}"] = summary(scaled)
        (args.out_dir / f"{name}_{tag}.manifest.json").write_text(json.dumps(
            {"from": str(out), "scale": args.scale, "seed": args.seed, **summary(scaled)},
            ensure_ascii=False, indent=1), encoding="utf-8")
    (args.out_dir / f"{name}.manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=1),
                                                         encoding="utf-8")
    print(json.dumps(manifest, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()

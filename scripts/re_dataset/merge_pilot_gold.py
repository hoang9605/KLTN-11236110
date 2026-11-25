r"""Gộp nhãn chuyên gia của pilot (300 câu train đã chấm) vào kết quả gán nhãn train, rồi xuất phiếu
chỉ gồm các cặp CHƯA được chuyên gia chấm (tầng B + 20% tầng A). Không gọi API.

  .venv\Scripts\python.exe -X utf8 scripts\re_dataset\merge_pilot_gold.py train_label_v4_critic [hậu_tố_tên_file]
"""
import copy
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(Path(__file__).parent))
from compare_prompt_versions import SILVER, gold_rows  # noqa: E402
from re_v3 import config  # noqa: E402
from re_v3.common import read_jsonl, write_jsonl  # noqa: E402
from re_v3.expert_review import write_xlsx  # noqa: E402


def propagate(final_path, map_path):
    """Áp nhãn chuyên gia của dòng đại diện sang các mention trùng chữ đã gộp (dedup_map.json)."""
    recs = read_jsonl(final_path)
    dedup = json.loads(Path(map_path).read_text(encoding="utf-8"))
    n = 0
    for rec in recs:
        rels = {f'{x["head"]}-{x["tail"]}': x for x in rec["relations"]}
        for rep, others in dedup.get(rec["id"], {}).items():
            for o in others:
                if rep in rels and o in rels:
                    for k in ("label", "ai_label", "expert_note"):
                        if k in rels[rep]:
                            rels[o][k] = rels[rep][k]
                    rels[o]["label_propagated_from"] = rep
                    n += 1
    write_jsonl(final_path, recs)
    print(f"đã áp nhãn cho {n} mention trùng chữ")


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--propagate":
        return propagate(sys.argv[2], sys.argv[3])
    name = sys.argv[1] if len(sys.argv) > 1 else "train_label_v4_critic"
    d = SILVER / name
    recs = read_jsonl(d / f"{name}.jsonl")
    gold = {r["key"]: r["gold"] for r in gold_rows(SILVER / "pilot_label_v1" / "pilot_label_v1_expert_review.xlsx")}
    st = Counter()
    for rec in recs:
        for x in rec["relations"]:
            k = (rec["id"], x["head"], x["tail"])
            if k in gold:
                st["expert_pilot"] += 1
                if x["label"] != gold[k]:
                    st["changed"] += 1
                    x["label_before_expert"] = x["label"]
                x["label"], x["label_source"], x["expert_reviewed"] = gold[k], "expert_pilot_v1", True
    write_jsonl(d / f"{name}_merged.jsonl", recs)
    # Gộp mention trùng chữ: cùng câu, cùng chữ head/tail, cùng nhãn AI -> chỉ đưa 1 dòng lên phiếu.
    # dedup_map.json ghi các mention bị gộp; sau khi chuyên gia chấm, chạy --propagate để áp kết quả.
    ents_text = lambda rec: {e["id"]: e["text"] for e in rec["entities"]}  # noqa: E731
    todo, dedup = [], {}
    for rec in recs:
        r = copy.deepcopy(rec)
        txt, seen, keep = ents_text(r), {}, []
        for x in r["relations"]:
            if x.get("expert_reviewed"):
                continue
            k = (txt[x["head"]], txt[x["tail"]], x["label"])
            if k in seen:
                dedup.setdefault(r["id"], {}).setdefault(seen[k], []).append(f'{x["head"]}-{x["tail"]}')
                st["merged_same_text_mentions"] += 1
                continue
            seen[k] = f'{x["head"]}-{x["tail"]}'
            keep.append(x)
        r["relations"] = keep
        if keep:
            todo.append(r)
    (d / "dedup_map.json").write_text(json.dumps(dedup, ensure_ascii=False, indent=1), encoding="utf-8")
    write_xlsx(d / f"{name}_expert_review{sys.argv[2] if len(sys.argv) > 2 else ''}.xlsx", todo, a_fraction=0.2, seed=config.SEED,
               title="Duyệt nhãn quan hệ y khoa: train v4 + Critic (đã bỏ các cặp chuyên gia chấm ở pilot)")
    st["pairs_left_for_review_pool"] = sum(len(r["relations"]) for r in todo)
    (d / "merge_pilot_gold.json").write_text(json.dumps(dict(st), ensure_ascii=False, indent=1), encoding="utf-8")
    print(dict(st))


if __name__ == "__main__":
    main()

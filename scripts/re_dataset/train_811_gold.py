r"""Thực nghiệm RE trên split 8:1:1 với nhãn đã được chuyên gia duyệt (25/11/2026).

  train: re_v3/data/silver/train_label_v4_critic/train_label_v4_critic_gold.jsonl
         (319 cặp chuyên gia ở pilot + 1210 cặp chuyên gia ở phiếu train + 103 cặp chỉ có nhãn LLM)
  dev:   re_v3/data/silver/dev_label_v3: nhãn chuyên gia lấy từ phiếu dev_label_v3_expert_review.xlsx
         (phiếu chưa ghi tên người duyệt, nên dev chỉ dùng để báo cáo, không đánh dấu human_verified)
  test:  re_v3/data/silver/test_label_v4_critic/test_label_v4_critic_expert_final.jsonl (100% chuyên gia)

Siêu tham số cố định từ trước, không chỉnh theo dev hay test: giống bert_re.py (10 epoch, lr 3e-5,
batch 16, 3 seed, lấy trung bình xác suất, ngưỡng 0,5).

  # baseline, chạy bằng CPU, vài giây
  .venv\Scripts\python.exe -X utf8 scripts/re_dataset/train_811_gold.py baselines --out outputs/re_811_gold
  # một mô hình BERT (cần GPU, chạy trong .venv-gpu); xác suất được lưu sau mỗi seed để chạy tiếp được
  .venv-gpu\Scripts\python.exe -X utf8 scripts/re_dataset/train_811_gold.py bert --base demdecuong/vihealthbert-base-syllable --tag vihealthbert --out outputs/re_811_gold
  # gộp bảng
  .venv\Scripts\python.exe -X utf8 scripts/re_dataset/train_811_gold.py table --out outputs/re_811_gold
"""
import argparse
import json
import os
import sys
import tempfile
import time
from collections import Counter
from pathlib import Path

os.environ.setdefault("KMP_DUPLICATE_LIB_OK", "TRUE")
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(Path(__file__).parent))

from relation_extraction.data import NEGATIVE, load_pairs  # noqa: E402
from train_eval import attach_entities, bootstrap, score  # noqa: E402

SILVER = ROOT / "re_v3" / "data" / "silver"
TRAIN = SILVER / "train_label_v4_critic" / "train_label_v4_critic_gold.jsonl"
TEST = SILVER / "test_label_v4_critic" / "test_label_v4_critic_expert_final.jsonl"
DEV_DIR = SILVER / "dev_label_v3"


def dev_records():
    """Nhãn chuyên gia của dev (phiếu v3), áp lên bản ghi dev_label_v3; không ghi đè file nào."""
    from re_v3.common import read_jsonl
    from re_v3.expert_review import apply_review, read_review, score_rows
    _, rel, ent, syn = read_review(DEV_DIR / "dev_label_v3_expert_review.xlsx")
    score_rows(rel, ent, syn)
    reviewer = {"name": None, "date": None, "note": "phiếu dev chưa ghi tên người duyệt"}
    return apply_review(read_jsonl(DEV_DIR / "dev_label_v3.jsonl"), reviewer, rel, ent, syn)


def _pairs_from_records(recs, name):
    # Bỏ cặp có thực thể INVALID (bước A) giống quy trình gán nhãn; load_pairs đọc từ file.
    keep = []
    for r in recs:
        inval = {e["id"] for e in r["entities"] if e.get("validity") == "INVALID"}
        r = dict(r, relations=[x for x in r["relations"] if x["head"] not in inval and x["tail"] not in inval])
        if r["relations"]:
            keep.append(r)
    tmp = Path(tempfile.gettempdir()) / f"re811_{name}.jsonl"
    tmp.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in keep), encoding="utf-8")
    pairs, _ = load_pairs(tmp, allow_ai=True)
    attach_entities(pairs, tmp)
    for p in pairs:
        p["uid"] = f"{p['sample_id']}:{p['head']['id']}:{p['tail']['id']}:{p['allowed_relation']}"
    return pairs


def load_all():
    from re_v3.common import read_jsonl
    return {"train": _pairs_from_records(read_jsonl(TRAIN), "train"),
            "dev": _pairs_from_records(dev_records(), "dev"),
            "test": _pairs_from_records(read_jsonl(TEST), "test")}


def evaluate(pairs, pred):
    gold = [p["label"] for p in pairs]
    s = score(gold, pred)
    s["positive_micro_f1_ci95"] = bootstrap([{"group": p["group"], "gold": p["label"], "pred": y}
                                             for p, y in zip(pairs, pred)])
    s["accuracy"] = round(sum(g == y for g, y in zip(gold, pred)) / len(gold), 3)
    return s


def run_baselines(a, data):
    from benchmark import predict_methods
    from relation_extraction.rules import RuleRelationExtractor
    out = {}
    for split in ("dev", "test"):
        preds = predict_methods(data["train"], data[split], RuleRelationExtractor())
        out[split] = {m: {"pred": dict(zip((p["uid"] for p in data[split]), y)), "score": evaluate(data[split], y)}
                      for m, y in preds.items()}
    Path(a.out).mkdir(parents=True, exist_ok=True)
    (Path(a.out) / "baselines.json").write_text(json.dumps(out, ensure_ascii=False, indent=0), encoding="utf-8")
    for split in out:
        for m, v in out[split].items():
            print(split, m, v["score"]["positive_micro"]["f1"])


def run_bert(a, data):
    import torch
    from transformers import AutoTokenizer
    from bert_re import train_predict
    from relation_extraction.bert_model import add_markers
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    tok = AutoTokenizer.from_pretrained(a.base)
    start_ids = add_markers(tok)
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    part = out / f"bert_{a.tag}_partial.json"
    per_seed = json.loads(part.read_text(encoding="utf-8"))["per_seed"] if part.exists() else {}
    train = data["train"]
    if a.extra:
        from re_v3.common import read_jsonl
        extra = _pairs_from_records(read_jsonl(a.extra), f"extra_{a.tag}")
        train = train + extra
        print(f"[{a.tag}] thêm {len(extra)} cặp từ {a.extra} (chỉ dùng để huấn luyện)", flush=True)
    t0 = time.time()
    for seed in a.seeds:
        if str(seed) in per_seed:
            print(f"[{a.tag}] seed {seed} đã có, bỏ qua", flush=True)
            continue
        ts = time.time()
        if a.save_model:
            from relation_extraction.bert_model import save_member
            (dv, te), model = train_predict(a, tok, start_ids, train, [data["dev"], data["test"]], seed, device, keep=True)
            save_member(model, tok, a.save_model, seed)
            del model
            torch.cuda.empty_cache()
        else:
            dv, te = train_predict(a, tok, start_ids, train, [data["dev"], data["test"]], seed, device)
        per_seed[str(seed)] = {"dev": [round(v, 6) for v in dv], "test": [round(v, 6) for v in te],
                               "seconds": round(time.time() - ts)}
        part.write_text(json.dumps({"base": a.base, "per_seed": per_seed}, ensure_ascii=False), encoding="utf-8")
        print(f"[{a.tag}] seed {seed} xong sau {time.time() - ts:.0f}s", flush=True)
    res = {"meta": {"base": a.base, "tag": a.tag, "seeds": a.seeds, "epochs": a.epochs, "lr": a.lr, "batch": a.batch,
                    "max_len": a.max_len, "seed_aggregation": "mean probability, threshold 0.5",
                    "device": torch.cuda.get_device_name(0) if device.type == "cuda" else "cpu",
                    "seconds_per_seed": {s: v["seconds"] for s, v in per_seed.items()},
                    "train_pairs": len(train), "extra": str(a.extra) if a.extra else None,
                    "date": time.strftime("%Y-%m-%d")}}
    for split in ("dev", "test"):
        prob = [sum(per_seed[str(s)][split][i] for s in a.seeds) / len(a.seeds) for i in range(len(data[split]))]
        pred = [p["allowed_relation"] if v >= 0.5 else NEGATIVE for p, v in zip(data[split], prob)]
        res[split] = {"prob": dict(zip((p["uid"] for p in data[split]), prob)), "score": evaluate(data[split], pred)}
        print(split, res[split]["score"]["positive_micro"])
    (out / f"bert_{a.tag}.json").write_text(json.dumps(res, ensure_ascii=False, indent=0), encoding="utf-8")
    if a.save_model:
        from relation_extraction.bert_model import save_config
        from relation_extraction.data import RELATIONS
        save_config(a.save_model, {
            "name": "ViHealthBERT-RE", "base": a.base, "max_len": a.max_len, "threshold": 0.5, "seeds": a.seeds,
            "seed_aggregation": "mean probability, threshold 0.5", "epochs": a.epochs, "lr": a.lr, "batch": a.batch,
            "class_weight": "n_neg/n_pos", "pooling": "head/tail start markers",
            "supported_relations": sorted({p["allowed_relation"] for p in train if p["label"] != NEGATIVE}),
            "all_relations": sorted(RELATIONS), "train_pairs": len(train),
            "train_positives": sum(p["label"] != NEGATIVE for p in train),
            "train_data": "re_v3/data/silver/train_label_v4_critic/train_label_v4_critic_gold.jsonl (phép chia 8:1:1, LLM gán, chuyên gia duyệt 1529/1632 cặp)",
            "label_source": "llm_v4_critic_expert_reviewed", "human_verified": False,
            "dev_f1": res["dev"]["score"]["positive_micro"]["f1"], "test_f1": res["test"]["score"]["positive_micro"]["f1"],
            "scores": f"{out}/bert_{a.tag}.json", "torch": torch.__version__,
            "trained_on": torch.cuda.get_device_name(0) if device.type == "cuda" else "cpu",
            "seconds": round(time.time() - t0), "date": time.strftime("%Y-%m-%d")})
        print(f"[{a.tag}] đã lưu mô hình vào {a.save_model}")
    print(f"[{a.tag}] tổng {time.time() - t0:.0f}s")


def all_preds(a, data, split):
    """uid -> nhãn dự đoán cho mọi phương pháp đã chạy, cộng nhãn của LLM (trước khi chuyên gia duyệt)."""
    out = Path(a.out)
    P = {}
    b = json.loads((out / "baselines.json").read_text(encoding="utf-8"))
    for m, v in b[split].items():
        P[m] = v["pred"]
    for f in sorted(out.glob("bert_*.json")):
        if f.name.endswith("_partial.json"):
            continue
        r = json.loads(f.read_text(encoding="utf-8"))
        rel = {p["uid"]: p["allowed_relation"] for p in data[split]}
        P[r["meta"]["tag"]] = {u: (rel[u] if v >= 0.5 else NEGATIVE) for u, v in r[split]["prob"].items()}
    if split == "test":
        from re_v3.common import read_jsonl
        llm = {}
        for rec in read_jsonl(SILVER / "test_label_v4_critic" / "test_label_v4_critic.jsonl"):
            for x in rec["relations"]:
                llm[f"{rec['id']}:{x['head']}:{x['tail']}:{x['allowed_relation']}"] = x["label"]
        P["llm_v4_critic"] = {p["uid"]: llm.get(p["uid"], NEGATIVE) for p in data[split]}
    return P


def paired_diff(pairs, pa, pb, n=1000, seed=13):
    """Bootstrap ghép cặp theo câu cho F1(a) - F1(b), cùng các mẫu lặp cho hai phương pháp."""
    import random
    from collections import defaultdict
    groups = defaultdict(list)
    for p in pairs:
        groups[p["group"]].append(p)
    keys, rng, vals = list(groups), random.Random(seed), []
    for _ in range(n):
        s = [x for _ in keys for x in groups[keys[rng.randrange(len(keys))]]]
        g = [x["label"] for x in s]
        fa = score(g, [pa[x["uid"]] for x in s])["positive_micro"]["f1"]
        fb = score(g, [pb[x["uid"]] for x in s])["positive_micro"]["f1"]
        vals.append(fa - fb)
    vals.sort()
    return [round(vals[int(.025 * n)], 3), round(vals[int(.975 * n) - 1], 3)]


def compare(a, data):
    res = {}
    for split in ("dev", "test"):
        P = all_preds(a, data, split)
        pairs = data[split]
        gold = [p["label"] for p in pairs]
        res[split] = {m: {"score": evaluate(pairs, [v[p["uid"]] for p in pairs])} for m, v in P.items()}
        ref = a.ref if a.ref in P else None
        if ref:
            for m in P:
                if m != ref:
                    res[split][m]["diff_ref_minus_this_ci95"] = paired_diff(pairs, P[ref], P[m])
        res[split]["_ref"] = ref
        res[split]["_gold_positive"] = sum(g != NEGATIVE for g in gold)
    (Path(a.out) / "compare.json").write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
    for split in res:
        for m, v in res[split].items():
            if not m.startswith("_"):
                print(split, m, v["score"]["positive_micro"]["f1"], v["score"]["positive_micro_f1_ci95"], v.get("diff_ref_minus_this_ci95"))


def table(a, data):
    out = Path(a.out)
    rows = []
    b = json.loads((out / "baselines.json").read_text(encoding="utf-8")) if (out / "baselines.json").exists() else {}
    for m in (b.get("test") or {}):
        rows.append((m, b["dev"][m]["score"], b["test"][m]["score"]))
    for f in sorted(out.glob("bert_*.json")):
        if f.name.endswith("_partial.json"):
            continue
        r = json.loads(f.read_text(encoding="utf-8"))
        rows.append((r["meta"]["tag"], r["dev"]["score"], r["test"]["score"]))
    stats = {s: {"pairs": len(v), "labels": dict(Counter(p["label"] for p in v))} for s, v in data.items()}
    lines = ["| Phương pháp | Dev P | Dev R | Dev F1 | Test P | Test R | Test F1 [CI95] |", "|---|---:|---:|---:|---:|---:|---|"]
    for m, d, t in rows:
        dm, tm = d["positive_micro"], t["positive_micro"]
        ci = t.get("positive_micro_f1_ci95") or ["", ""]
        ci_s = f"[{ci[0]}–{ci[1]}]"
        lines.append(f"| {m} | {dm['precision']} | {dm['recall']} | {dm['f1']} | {tm['precision']} | {tm['recall']} | {tm['f1']} {ci_s} |")
    md = "\n".join(lines)
    (out / "bang_ket_qua.md").write_text(md + "\n\n" + json.dumps(stats, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(md)
    print(json.dumps(stats, ensure_ascii=False))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=("baselines", "bert", "table", "stats", "compare"))
    ap.add_argument("--ref", default="vihealthbert", help="phương pháp làm mốc cho bootstrap ghép cặp")
    ap.add_argument("--out", default="outputs/re_811_gold")
    ap.add_argument("--base", default="demdecuong/vihealthbert-base-syllable")
    ap.add_argument("--tag", default="vihealthbert")
    ap.add_argument("--seeds", type=int, nargs="+", default=[42, 43, 44])
    ap.add_argument("--epochs", type=int, default=10)
    ap.add_argument("--lr", type=float, default=3e-5)
    ap.add_argument("--batch", type=int, default=16)
    ap.add_argument("--max-len", type=int, default=192)
    ap.add_argument("--save-model", metavar="DIR", help="lưu trọng số mọi seed và re_config.json để hệ thống nạp")
    ap.add_argument("--extra", type=Path, help="dữ liệu bổ sung chỉ để huấn luyện, vd dữ liệu sinh đã lọc rò rỉ")
    a = ap.parse_args()
    data = load_all()
    if a.cmd == "stats":
        print({s: (len(v), dict(Counter(p["label"] for p in v))) for s, v in data.items()})
    elif a.cmd == "compare":
        compare(a, data)
    elif a.cmd == "baselines":
        run_baselines(a, data)
    elif a.cmd == "bert":
        run_bert(a, data)
    else:
        table(a, data)


if __name__ == "__main__":
    main()

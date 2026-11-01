"""Đánh giá end-to-end NER -> RE trên tập golden test đã duyệt.

  .venv\\Scripts\\python.exe -X utf8 scripts/golden_test/evaluate_e2e.py ^
      --gold data/golden_test/v1/gold.jsonl --re-model outputs/re_ai_baseline/seed42/model.joblib

Báo cáo:
  1. NER: strict (khớp nhãn + span) và relaxed (khớp nhãn, span giao nhau), theo nhãn và micro.
  2. RE với thực thể gold: tách riêng chất lượng bộ phân loại quan hệ (bỏ cặp CHUA_RO).
  3. RE end-to-end: quan hệ dự đoán từ thực thể do NER tìm ra; đúng khi head, tail (nhãn + span chính xác)
     và tên quan hệ đều khớp một quan hệ dương gold.
  Mọi micro-F1 kèm khoảng tin cậy 95% bootstrap theo đoạn (1000 lần).
Đoạn có cặp CHUA_RO: các cặp đó bị bỏ khỏi cả gold và dự đoán ở mục 2 và 3.
"""
import argparse
import json
import os
import random
import sys
from collections import Counter, defaultdict
from pathlib import Path

os.environ.setdefault("KMP_DUPLICATE_LIB_OK", "TRUE")
os.environ.setdefault("OMP_NUM_THREADS", "1")
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from common import ENTITY_TYPES, NEGATIVE, RELATIONS, UNKNOWN, ROOT, read_jsonl  # noqa: E402


def prf(tp, fp, fn):
    p = tp / (tp + fp) if tp + fp else 0.0
    r = tp / (tp + fn) if tp + fn else 0.0
    return {"precision": round(p, 4), "recall": round(r, 4), "f1": round(2 * p * r / (p + r), 4) if p + r else 0.0,
            "tp": tp, "fp": fp, "fn": fn}


def ner_counts(gold, pred):
    """Per-sample counts: {(mode,label): [tp,fp,fn]} for strict and relaxed (one-to-one greedy)."""
    c = defaultdict(lambda: [0, 0, 0])
    gs = {(e["label"], e["start"], e["end"]) for e in gold}
    ps = {(e["label"], e["start"], e["end"]) for e in pred}
    for lab in ENTITY_TYPES:
        g = {x for x in gs if x[0] == lab}; p = {x for x in ps if x[0] == lab}
        tp = len(g & p); c[("strict", lab)] = [tp, len(p) - tp, len(g) - tp]
        used, tpr = set(), 0
        for x in sorted(p, key=lambda t: t[1]):
            m = next((y for y in sorted(g, key=lambda t: t[1]) if y not in used and x[1] < y[2] and y[1] < x[2]), None)
            if m: used.add(m); tpr += 1
        c[("relaxed", lab)] = [tpr, len(p) - tpr, len(g) - tpr]
    return c


def micro(counts_list, mode):
    tp = fp = fn = 0
    for c in counts_list:
        for (m, _), (a, b, d) in c.items():
            if m == mode: tp += a; fp += b; fn += d
    return prf(tp, fp, fn)


def bootstrap(per_sample, fn, n=1000, seed=13):
    rng = random.Random(seed); vals = []
    for _ in range(n):
        s = [per_sample[rng.randrange(len(per_sample))] for _ in per_sample]
        vals.append(fn(s))
    vals.sort()
    return [round(vals[int(0.025 * n)], 4), round(vals[int(0.975 * n) - 1], 4)]


def triples(entities, relations, pos_only=True):
    ent = {e["id"]: e for e in entities}
    out = set()
    for r in relations:
        if r["label"] in (None, NEGATIVE, UNKNOWN) and pos_only:
            continue
        h, t = ent[r["head"]], ent[r["tail"]]
        out.add(((h["label"], h["start"], h["end"]), (t["label"], t["start"], t["end"]), r["label"]))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--gold", nargs="+", default=[str(ROOT / "data/golden_test/v1/gold.jsonl")])
    ap.add_argument("--re-model", default=str(ROOT / "outputs/re_ai_baseline/seed42/model.joblib"))
    ap.add_argument("--out", default=str(ROOT / "data/golden_test/v1/eval"))
    ap.add_argument("--predictions", help="JSONL dự đoán có sẵn (id,text,entities,relations) thay vì chạy NER+RE; vẫn chấm mục 2 nếu có --re-model")
    a = ap.parse_args()
    gold = [r for f in a.gold for r in read_jsonl(f)]
    if not gold:
        sys.exit("gold rỗng: cần duyệt và import trước")
    out = Path(a.out); out.mkdir(parents=True, exist_ok=True)

    extractor = None
    if a.re_model and Path(a.re_model).exists():
        from relation_extraction.model import RelationExtractor
        extractor = RelationExtractor.load(a.re_model)
    if a.predictions:
        preds = {r["id"]: r for r in read_jsonl(a.predictions)}
    else:
        if extractor is None:
            sys.exit(f"không tìm thấy mô hình RE: {a.re_model}")
        from ner.pipeline import MedicalNERPipeline
        from relation_extraction.pipeline import MedicalREPipeline
        re_pipe = MedicalREPipeline(extractor, ner=MedicalNERPipeline(enable_normalization=False))
        preds = {}
        for g in gold:
            res = re_pipe.predict(g["text"])
            if res["text"] != g["text"]:
                raise SystemExit(f"{g['id']}: văn bản NER trả về khác gold, offset không so được")
            preds[g["id"]] = {"id": g["id"], "text": res["text"],
                              "entities": [{k: e[k] for k in ("id", "label", "start", "end", "text")} for e in res["entities"]],
                              "relations": [{k: r.get(k) for k in ("head", "tail", "allowed_relation", "label", "score", "status")}
                                            for r in res["relation_candidates"]]}
        with open(out / "predictions.jsonl", "w", encoding="utf-8") as f:
            for p in preds.values(): f.write(json.dumps(p, ensure_ascii=False) + "\n")

    # 1. NER
    ner_per = [ner_counts(g["entities"], preds[g["id"]]["entities"]) for g in gold]
    ner = {}
    for mode in ("strict", "relaxed"):
        per_label = {}
        for lab in ENTITY_TYPES:
            t = [sum(c[(mode, lab)][i] for c in ner_per) for i in range(3)]
            per_label[lab] = {**prf(*t), "support": t[0] + t[2]}
        ner[mode] = {"micro": micro(ner_per, mode), "micro_f1_ci95": bootstrap(ner_per, lambda s, m=mode: micro(s, m)["f1"]),
                     "per_label": per_label}

    # 2. RE with gold entities
    re_gold = None
    if extractor is not None:
        per, rows = [], []
        for g in gold:
            pr = {(r["head"], r["tail"]): r for r in extractor.predict(g["text"], g["entities"])}
            c = Counter()
            for r in g["relations"]:
                if r["label"] == UNKNOWN: continue
                p = pr.get((r["head"], r["tail"]), {})
                plab = p.get("label") or "UNSUPPORTED"
                gpos, ppos = r["label"] != NEGATIVE, plab not in (NEGATIVE, "UNSUPPORTED")
                rel = r["allowed_relation"]
                c[(rel, "tp")] += gpos and ppos; c[(rel, "fp")] += (not gpos) and ppos; c[(rel, "fn")] += gpos and not ppos
                rows.append({"id": g["id"], "head": r["head"], "tail": r["tail"], "gold": r["label"], "pred": plab, "score": p.get("score")})
            per.append(c)
        def re_micro(s):
            return prf(*(sum(c[(rel, k)] for c in s for rel in RELATIONS) for k in ("tp", "fp", "fn")))
        re_gold = {"micro": re_micro(per), "micro_f1_ci95": bootstrap(per, lambda s: re_micro(s)["f1"]),
                   "per_relation": {rel: {**prf(*(sum(c[(rel, k)] for c in per) for k in ("tp", "fp", "fn"))),
                                          "gold_positive": sum(1 for g in gold for r in g["relations"] if r["allowed_relation"] == rel and r["label"] == rel),
                                          "supported_by_model": rel in extractor.supported_relations} for rel in RELATIONS}}
        with open(out / "re_gold_entities_pairs.jsonl", "w", encoding="utf-8") as f:
            for r in rows: f.write(json.dumps(r, ensure_ascii=False) + "\n")

    # 3. End-to-end
    per = []
    for g in gold:
        unknown = triples(g["entities"], [{**r, "label": r["allowed_relation"]}
                                          for r in g["relations"] if r["label"] == UNKNOWN])
        gt = triples(g["entities"], g["relations"])
        pt = triples(preds[g["id"]]["entities"], preds[g["id"]]["relations"]) - unknown
        c = Counter()
        for rel in RELATIONS:
            gr = {x for x in gt if x[2] == rel}; pr_ = {x for x in pt if x[2] == rel}
            c[(rel, "tp")] = len(gr & pr_); c[(rel, "fp")] = len(pr_ - gr); c[(rel, "fn")] = len(gr - pr_)
        per.append(c)
    def e2e_micro(s):
        return prf(*(sum(c[(rel, k)] for c in s for rel in RELATIONS) for k in ("tp", "fp", "fn")))
    e2e = {"micro": e2e_micro(per), "micro_f1_ci95": bootstrap(per, lambda s: e2e_micro(s)["f1"]),
           "per_relation": {rel: prf(*(sum(c[(rel, k)] for c in per) for k in ("tp", "fp", "fn"))) for rel in RELATIONS}}

    report = {"gold_files": a.gold, "samples": len(gold),
              "gold_entities": dict(Counter(e["label"] for g in gold for e in g["entities"])),
              "gold_relations": dict(Counter(r["label"] for g in gold for r in g["relations"])),
              "re_model": a.re_model if extractor is not None else None, "predictions_file": a.predictions,
              "ner": ner, "re_with_gold_entities": re_gold, "re_end_to_end": e2e,
              "notes": ["Tập lấy mẫu có chủ đích theo quan hệ; không suy ra phân bố tự nhiên.",
                        "Quan hệ mô hình chưa hỗ trợ (status=unsupported) được tính là không dự đoán (FN nếu gold dương).",
                        "CI95 bootstrap theo đoạn, 1000 lần, seed 13."]}
    (out / "report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    L = [f"# Đánh giá golden test end-to-end ({len(gold)} đoạn)", "",
         "| Hạng mục | P | R | F1 | CI95 F1 |", "|---|---:|---:|---:|---|"]
    def line(name, d): return f"| {name} | {d['micro']['precision']:.3f} | {d['micro']['recall']:.3f} | {d['micro']['f1']:.3f} | {d['micro_f1_ci95'][0]:.3f}–{d['micro_f1_ci95'][1]:.3f} |"
    L += [line("NER strict", ner["strict"]), line("NER relaxed", ner["relaxed"])]
    if re_gold: L.append(line("RE, thực thể gold", re_gold))
    L += [line("RE end-to-end", e2e), "", "## RE end-to-end theo quan hệ", "", "| Quan hệ | TP | FP | FN | F1 |", "|---|---:|---:|---:|---:|"]
    L += [f"| {rel} | {d['tp']} | {d['fp']} | {d['fn']} | {d['f1']:.3f} |" for rel, d in e2e["per_relation"].items()]
    (out / "summary.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    print("\n".join(L))


if __name__ == "__main__":
    main()

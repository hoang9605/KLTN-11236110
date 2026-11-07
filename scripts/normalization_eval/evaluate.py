r"""Evaluate entity normalization (CONDITION -> ICD-10, DRUG -> RxNorm) on a gold set.

Metrics (per ontology, on linkable items = gold has >= 1 code):
  Accuracy      the system's single decision (`normalize`) is an accepted code;
                abstaining counts as wrong.
  Top-k Acc     an accepted code is among the first k of `candidates()`.
  Recall@k      = Top-k Acc here, because each mention has one gold concept
                (alternates are equally acceptable codings of that concept).
                Reported under both names for the thesis table.
  MRR@10        mean reciprocal rank of the first accepted code.
  Coverage / Precision of decisions, and on NIL items the correct-abstention rate.
  ICD-10 also at category level (first 3 characters, e.g. K58.9 -> K58).

Two weightings: type-level (each unique surface form counts once, primary) and
mention-level (weighted by corpus frequency). 95% CIs by bootstrap over forms.

Baselines (same gold, same candidate pool):
  exact   ICD-10: catalog exact name match only. RxNorm: RxNav exact name lookup.
  fuzzy1  top-1 of plain string retrieval with no safeguards and no abstention
          (ICD-10: rapidfuzz WRatio over catalog names; RxNorm: RxNav approximateTerm).
  system  the pipeline normalizers. ICD-10: exact -> synonyms -> guarded fuzzy, abstains.
          RxNorm: exact name -> Vietnamese alias -> prefix strip -> near-identical approx.
  always  "always answer" mode (EntityNormalizationPipeline(mode="always")): the system
          decision when confident, else the top retrieval candidate. Never abstains, so its
          Accuracy equals Top-1 and NIL items are always answered (wrongly).
  Candidate lists for Top-k come from `candidates()`: the system decision first, then
  ICD-10 TF-IDF character n-gram retrieval / RxNav approximateTerm.

Usage:
    .venv\Scripts\python.exe -X utf8 scripts/normalization_eval/evaluate.py ^
        --gold data/norm_gold_v1/gold_test.jsonl --out eval/normalization_2026-11-07
"""
import argparse
import json
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from rapidfuzz import fuzz, process  # noqa: E402

from normalization.icd10 import ICD10Normalizer, normalize_vietnamese_text  # noqa: E402
from normalization.rxnorm import RxNormNormalizer, clean_drug_name  # noqa: E402

KS = (1, 3, 5, 10)
METHODS = ("exact", "fuzzy1", "system", "always")
SYSTEM_NAMES = {
    "ICD-10": {"exact": "Baseline: khớp chính xác tên danh mục",
               "fuzzy1": "Baseline: fuzzy top-1 (WRatio, không ràng buộc)",
               "system": "Hệ thống – chế độ thận trọng (exact → synonym → fuzzy có ràng buộc)",
               "always": "Hệ thống – chế độ luôn trả lời (thận trọng, nếu không thì ứng viên TF-IDF top-1)"},
    "RxNorm": {"exact": "Baseline: RxNav khớp tên chính xác",
               "fuzzy1": "Baseline: RxNav approximateTerm top-1",
               "system": "Hệ thống – chế độ thận trọng (exact → alias Việt→Anh → bỏ tiền tố → approx gần trùng)",
               "always": "Hệ thống – chế độ luôn trả lời (thận trọng, nếu không thì approximateTerm top-1)"},
}


def icd_category(code):
    return code.replace("*", "").replace("†", "")[:3]


def predict(item, icd, rx):
    """Return {method: code|None} decisions and the system's ranked candidate codes."""
    surface = item["surface"]
    if item["ontology"] == "ICD-10":
        clean = normalize_vietnamese_text(surface)
        exact = icd.exact_map.get(clean, {}).get("code")
        best = process.extractOne(clean, icd.catalog_names, scorer=fuzz.WRatio) if clean else None
        fuzzy1 = icd.catalog_entries[best[2]]["code"] if best else None
        sys_res = icd.normalize(surface)
        cands = [c.code for c in icd.candidates(surface, k=max(KS))]
    else:
        clean = clean_drug_name(surface)
        exact = rx._fetch_rxcui(clean) if clean else None
        approx = rx._approximate(clean) if clean else []
        fuzzy1 = approx[0]["rxcui"] if approx else None
        sys_res = rx.normalize(surface)
        cands = [c.code for c in rx.candidates(surface, k=max(KS))]
    return {"exact": exact, "fuzzy1": fuzzy1, "system": sys_res.code if sys_res else None,
            "always": cands[0] if cands else None}, cands


def hit(code, gold, category):
    if code is None:
        return False
    if category:
        return icd_category(code) in {icd_category(g) for g in gold}
    return code in gold


def first_rank(cands, gold, category):
    for i, c in enumerate(cands, 1):
        if hit(c, gold, category):
            return i
    return None


def score_items(rows, category=False):
    """Per-item 0/1 outcomes used by both the point estimate and the bootstrap."""
    out = []
    for r in rows:
        gold = r["gold_codes"]
        o = {"w": r["freq"], "nil": r["nil"]}
        for m in METHODS:
            pred = r["pred"][m]
            o[f"{m}_answered"] = pred is not None
            o[f"{m}_correct"] = (not r["nil"]) and hit(pred, gold, category)
        rank = None if r["nil"] else first_rank(r["candidates"], gold, category)
        o["rank"] = rank
        out.append(o)
    return out


def aggregate(outs, weighted):
    def w(o):
        return o["w"] if weighted else 1
    link = [o for o in outs if not o["nil"]]
    nil = [o for o in outs if o["nil"]]
    W = sum(w(o) for o in link) or 1
    WN = sum(w(o) for o in nil) or 1
    res = {"n_linkable": len(link), "n_nil": len(nil),
           "mentions_linkable": sum(o["w"] for o in link), "mentions_nil": sum(o["w"] for o in nil)}
    for m in METHODS:
        answered = sum(w(o) for o in link if o[f"{m}_answered"])
        correct = sum(w(o) for o in link if o[f"{m}_correct"])
        res[m] = {
            "accuracy": correct / W,
            "coverage": answered / W,
            "precision_answered": correct / answered if answered else 0.0,
            "nil_correct_abstention": sum(w(o) for o in nil if not o[f"{m}_answered"]) / WN,
        }
    for k in KS:
        res[f"top{k}_acc"] = sum(w(o) for o in link if o["rank"] and o["rank"] <= k) / W
        res[f"recall@{k}"] = res[f"top{k}_acc"]
    res["mrr@10"] = sum(w(o) * (1.0 / o["rank"]) for o in link if o["rank"]) / W
    return res


def bootstrap(outs, weighted, n=2000, seed=13):
    rng = random.Random(seed)
    keys = [("system", "accuracy"), ("exact", "accuracy"), ("fuzzy1", "accuracy"), ("always", "accuracy"),
            ("top1_acc",), ("top5_acc",), ("top10_acc",)]
    samples = {k: [] for k in keys}
    for _ in range(n):
        s = [outs[rng.randrange(len(outs))] for _ in outs]
        agg = aggregate(s, weighted)
        for k in keys:
            samples[k].append(agg[k[0]][k[1]] if len(k) == 2 else agg[k[0]])
    ci = {}
    for k, v in samples.items():
        v.sort()
        ci[".".join(k)] = [v[int(0.025 * n)], v[int(0.975 * n) - 1]]
    return ci


def fmt(x):
    return f"{x:.3f}"


def summary_md(report, gold_path, verified):
    L = ["# Đánh giá chuẩn hóa thực thể (Entity Normalization)", ""]
    if not verified:
        L += ["> **Nhãn gold là nhãn AI tiền gán, CHƯA được bác sĩ duyệt.** Số liệu dưới đây là tạm thời; "
              "cần duyệt `data/norm_gold_v1/ai_labels_test.tsv` rồi chạy lại trước khi đưa vào khóa luận.", ""]
    L += [f"- Gold: `{gold_path}` — đơn vị đánh giá là **dạng bề mặt duy nhất** (type-level); "
          "bảng mention-level trọng số theo tần suất trong split test.",
          "- Thực thể lấy từ **nhãn gold NER** của split `test` VietMed-NER, nên lỗi NER không ảnh hưởng.",
          "- Accuracy: quyết định duy nhất của hệ thống đúng; hệ thống từ chối (không trả mã) tính là sai.",
          "- Hai chế độ: **thận trọng** (từ chối khi không chắc, ưu tiên precision) và **luôn trả lời** "
          "(lấy ứng viên top-1 khi không chắc; Accuracy = Top-1, nhưng mọi dạng NIL đều bị gán mã).",
          "- Top-k Accuracy = Recall@k: mã đúng nằm trong k ứng viên đầu (mỗi đề cập có một khái niệm gold). "
          "Ứng viên: quyết định của hệ thống đứng đầu, sau đó ICD-10 theo TF-IDF n-gram ký tự, RxNorm theo RxNav approximateTerm.",
          "- CI95: bootstrap 2000 lần theo dạng bề mặt.", ""]
    for onto, block in report["results"].items():
        for level in ("code", "category") if onto == "ICD-10" else ("code",):
            r = block[level]["type"]
            rm = block[level]["mention"]
            ci = block[level]["ci95_type"]
            title = "mã đầy đủ" if level == "code" else "nhóm 3 ký tự (category)"
            L += [f"## {onto} — {title}", "",
                  f"Linkable: {r['n_linkable']} dạng ({r['mentions_linkable']} đề cập); "
                  f"NIL: {r['n_nil']} dạng ({r['mentions_nil']} đề cập).", "",
                  "| Phương pháp | Accuracy (type) | CI95 | Accuracy (mention) | Coverage | Precision khi trả lời | Từ chối đúng NIL |",
                  "|---|---:|---|---:|---:|---:|---:|"]
            names = SYSTEM_NAMES[onto]
            for m in METHODS:
                name = names[m]
                c = ci[f"{m}.accuracy"]
                L.append(f"| {name} | {fmt(r[m]['accuracy'])} | {fmt(c[0])}–{fmt(c[1])} | "
                         f"{fmt(rm[m]['accuracy'])} | {fmt(r[m]['coverage'])} | "
                         f"{fmt(r[m]['precision_answered'])} | {fmt(r[m]['nil_correct_abstention'])} |")
            L += ["", "| Xếp hạng ứng viên | Top-1 | Top-3 | Top-5 | Top-10 | MRR@10 |", "|---|---:|---:|---:|---:|---:|",
                  "| Top-k Acc = Recall@k (type) | " + " | ".join(fmt(r[f"top{k}_acc"]) for k in KS) + f" | {fmt(r['mrr@10'])} |",
                  "| Top-k Acc = Recall@k (mention) | " + " | ".join(fmt(rm[f"top{k}_acc"]) for k in KS) + f" | {fmt(rm['mrr@10'])} |",
                  f"| CI95 (type) | {fmt(ci['top1_acc'][0])}–{fmt(ci['top1_acc'][1])} | | "
                  f"{fmt(ci['top5_acc'][0])}–{fmt(ci['top5_acc'][1])} | {fmt(ci['top10_acc'][0])}–{fmt(ci['top10_acc'][1])} | |", ""]
    L += ["## Lỗi của hệ thống (trả mã sai, mã đầy đủ)", "", "| Ontology | Dạng | Tần suất | Hệ thống | Gold |", "|---|---|---:|---|---|"]
    for e in report["system_wrong_links"][:40]:
        L.append(f"| {e['ontology']} | {e['form']} | {e['freq']} | {e['pred']} | {', '.join(e['gold']) or 'NIL'} |")
    return "\n".join(L) + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--gold", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)

    rows = [json.loads(l) for l in Path(a.gold).read_text(encoding="utf-8").splitlines() if l.strip()]
    verified = all(r.get("human_verified") for r in rows)
    icd, rx = ICD10Normalizer(), RxNormNormalizer()
    for r in rows:
        r["pred"], r["candidates"] = predict(r, icd, rx)

    report = {"gold": a.gold, "human_verified": verified, "ks": KS, "results": {}}
    for onto in ("ICD-10", "RxNorm"):
        sub = [r for r in rows if r["ontology"] == onto]
        block = {}
        for level in ("code", "category") if onto == "ICD-10" else ("code",):
            outs = score_items(sub, category=(level == "category"))
            block[level] = {"type": aggregate(outs, False), "mention": aggregate(outs, True),
                            "ci95_type": bootstrap(outs, False)}
        report["results"][onto] = block

    wrong = [{"ontology": r["ontology"], "form": r["form"], "freq": r["freq"],
              "pred": r["pred"]["system"], "gold": r["gold_codes"]}
             for r in rows if r["pred"]["system"] and not hit(r["pred"]["system"], r["gold_codes"], False)]
    report["system_wrong_links"] = sorted(wrong, key=lambda e: -e["freq"])

    with open(out / "predictions.jsonl", "w", encoding="utf-8") as fh:
        for r in rows:
            fh.write(json.dumps({k: r[k] for k in ("id", "ontology", "form", "freq", "gold_codes", "nil",
                                                   "pred", "candidates")}, ensure_ascii=False) + "\n")
    (out / "report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    md = summary_md(report, a.gold, verified)
    (out / "summary.md").write_text(md, encoding="utf-8")
    print(md)


if __name__ == "__main__":
    main()

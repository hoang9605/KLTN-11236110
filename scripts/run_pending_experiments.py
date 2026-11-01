"""Các thí nghiệm cần chạy mô hình NER trên máy có checkpoint + cache VietMed-NER.

  .venv\\Scripts\\python.exe -X utf8 scripts/run_pending_experiments.py            # tất cả (~45-50 phút)
  .venv\\Scripts\\python.exe -X utf8 scripts/run_pending_experiments.py --only qual   # chỉ câu bệnh án viết (~1 phút)
  .venv\\Scripts\\python.exe -X utf8 scripts/run_pending_experiments.py --only ablation [--limit 500]

1. ablation: Tầng 2 trên split test với từng luật hậu xử lý bị tắt (cũng là lần chạy lại sau khi thêm
   luật Rule 1b DRUG->TEST, nên cấu hình "full" thay cho số 0,6223 cũ).
2. qual: chạy NER (+ chuẩn hóa nếu có mạng) + RE trên 24 câu văn phong bệnh án tự soạn, xuất bảng
   để sinh viên tự ghi lỗi.
Kết quả: outputs/pending_experiments/
"""
import argparse, json, os, sys, time
from pathlib import Path

os.environ.setdefault("KMP_DUPLICATE_LIB_OK", "TRUE")
os.environ.setdefault("OMP_NUM_THREADS", "1")
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
OUT = ROOT / "outputs" / "pending_experiments"

ABLATIONS = {
    "full": [],
    "no_dosage_rules": ["dosage"],
    "no_drug_blacklist": ["blacklist"],
    "no_labtest_relabel": ["labtest"],
    "no_severity_merge": ["severity"],
    "model_plus_mapping_only": ["dosage", "blacklist", "labtest", "severity"],
}


def patch(pipe, off):
    pp, dx = pipe.postprocessor, pipe.dosage_extractor
    if "dosage" in off: dx.merge_with_model_entities = lambda ents, text: list(ents)
    if "blacklist" in off: pp.filter_drug_blacklist = lambda ents: ents
    if "labtest" in off: pp.relabel_lab_tests_from_drug = lambda ents: ents
    if "severity" in off: pp.merge_severity_into_condition = lambda ents, text: ents
    return pipe


def run_ablation(limit):
    from ner.pipeline import MedicalNERPipeline
    from eval.data_loader import load_vietmed_test_split
    from eval.evaluate_tier2 import run_tier2_evaluation
    ds = load_vietmed_test_split("test")
    rows = []
    for name, off in ABLATIONS.items():
        print(f"\n=== ABLATION {name} (tắt: {off or 'không'}) ===")
        pipe = patch(MedicalNERPipeline(enable_normalization=False), off)
        res = run_tier2_evaluation(dataset=ds, pipeline=pipe, output_dir=OUT / "ablation" / name, limit=limit)
        s, r = res["strict_report"], res["relaxed_report"]
        rows.append({"config": name, "disabled": off,
                     "strict_micro": s["micro avg"], "relaxed_micro": r["micro avg"],
                     "strict_per_label_f1": {k: v.get("f1-score") for k, v in s.items() if "avg" not in k and isinstance(v, dict)}})
    (OUT / "ablation_summary.json").write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")
    labels = ["CONDITION", "DRUG", "BODY_PART", "TEST", "PROCEDURE", "DOSAGE"]
    L = ["| Cấu hình | Strict P | Strict R | Strict F1 | Relaxed F1 | " + " | ".join(labels) + " |",
         "|---|---:|---:|---:|---:|" + "---:|" * len(labels)]
    for r in rows:
        s = r["strict_micro"]
        L.append(f"| {r['config']} | {s['precision']:.4f} | {s['recall']:.4f} | {s['f1-score']:.4f} | {r['relaxed_micro']['f1-score']:.4f} | "
                 + " | ".join(f"{(r['strict_per_label_f1'].get(l) or 0):.3f}" for l in labels) + " |")
    (OUT / "ablation_summary.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    print("\n".join(L))


def run_qual(normalize):
    from ner.pipeline import MedicalNERPipeline
    from relation_extraction.model import RelationExtractor
    from relation_extraction.pipeline import MedicalREPipeline
    sents = [l.strip() for l in (ROOT / "data/qualitative/written_clinical_sentences.txt").read_text(encoding="utf-8").splitlines()
             if l.strip() and not l.startswith("#")]
    ner = MedicalNERPipeline(enable_normalization=normalize)
    model = ROOT / "outputs/re_ai_baseline/seed42/model.joblib"
    re_pipe = MedicalREPipeline(RelationExtractor.load(model), ner=ner) if model.exists() else None
    results, L = [], ["| # | Câu | Thực thể (nhãn) | Quan hệ dự đoán | Lỗi sinh viên ghi nhận |", "|---:|---|---|---|---|"]
    for i, s in enumerate(sents, 1):
        res = re_pipe.from_ner_result(ner.predict(s, normalize=normalize)) if re_pipe else ner.predict(s, normalize=normalize)
        results.append(res)
        ents = {e.get("id"): e for e in res["entities"]}
        et = "; ".join(f"{e['surface_text']} ({e['label']}{', ' + e['normalized']['code'] if e.get('normalized') and e['normalized'].get('code') else ''})" for e in res["entities"])
        rel = "; ".join(f"{ents[r['head']]['surface_text']} →{r['label']}→ {ents[r['tail']]['surface_text']}" for r in res.get("relations", []))
        L.append(f"| {i} | {s} | {et} | {rel} |  |")
    (OUT / "qualitative_written.json").write_text(json.dumps(results, ensure_ascii=False, indent=2, default=str), encoding="utf-8")
    (OUT / "qualitative_written.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    print("\n".join(L))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", choices=["ablation", "qual"])
    ap.add_argument("--limit", type=int)
    ap.add_argument("--normalize", action="store_true", help="bật tra ICD-10/RxNorm cho câu bệnh án viết (cần mạng cho RxNav)")
    a = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    t = time.time()
    if a.only in (None, "qual"): run_qual(a.normalize)
    if a.only in (None, "ablation"): run_ablation(a.limit)
    print(f"\nXong sau {time.time() - t:.0f}s. Kết quả: {OUT}")


if __name__ == "__main__":
    main()

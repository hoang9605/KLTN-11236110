"""Ablation NER trên split test: đo đóng góp của luật liều và các luật hậu xử lý.

  python -X utf8 scripts/run_ner_ablation.py --out eval/ablation_2026-11-06

Cấu hình (mọi cấu hình vẫn giữ lọc schema và giải quyết chồng lấn):
  full          : pipeline đầy đủ (giống eval/run_eval.py tầng 2)
  no_dosage     : bỏ DosageExtractor (chỉ dùng DOSAGE của mô hình)
  no_rules      : bỏ Luật 1, 1b, 2
  model_only    : bỏ cả luật liều lẫn Luật 1, 1b, 2
Không tinh chỉnh gì theo kết quả; chỉ đo.
"""
import argparse
import json
import os
import sys
from pathlib import Path

os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("KMP_DUPLICATE_LIB_OK", "TRUE")
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from eval.data_loader import load_vietmed_test_split  # noqa: E402
from eval.evaluate_tier2 import run_tier2_evaluation  # noqa: E402
from ner.pipeline import MedicalNERPipeline  # noqa: E402


def identity(entities, *args, **kwargs):
    return entities


def configure(pipe, name):
    pp, dx = pipe.postprocessor, pipe.dosage_extractor
    if name in ("no_dosage", "model_only"):
        dx.merge_with_model_entities = identity
    if name in ("no_rules", "model_only"):
        pp.filter_drug_blacklist = identity
        pp.relabel_lab_tests_from_drug = identity
        pp.merge_severity_into_condition = identity


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(ROOT / "eval/ablation_2026-11-06"))
    ap.add_argument("--configs", nargs="+", default=["no_dosage", "no_rules", "model_only"])
    a = ap.parse_args()
    dataset = load_vietmed_test_split("test")
    summary = {}
    for name in a.configs:
        pipe = MedicalNERPipeline(enable_normalization=False)
        configure(pipe, name)
        out = Path(a.out) / name
        run_tier2_evaluation(dataset=dataset, pipeline=pipe, output_dir=out)
        rep = json.loads((out / "schema_6label_report.json").read_text(encoding="utf-8"))
        summary[name] = {mode: {k: v for k, v in rep[mode].items()} for mode in rep}
        print(f"[ABLATION] {name}: strict micro F1 = {rep['strict_exact_match']['micro avg']['f1-score']}")
    (Path(a.out) / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()

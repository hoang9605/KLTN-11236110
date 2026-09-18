"""Tier 2 Evaluation: Full pipeline 6-label target schema evaluation on VietMed-NER test split."""

import argparse
import json
import logging
import sys
import time
from pathlib import Path

_project_root = Path(__file__).resolve().parent.parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))
from typing import Any, Dict, List, Optional

import numpy as np

from ner.config import TARGET_LABELS
from ner.logger import get_logger
from ner.pipeline import MedicalNERPipeline
from eval.data_loader import extract_gold_spans_target_schema, load_vietmed_test_split
from eval.metrics import (
    compute_confusion_matrix_and_plot,
    evaluate_spans_relaxed,
    evaluate_spans_strict,
    find_top_error_cases,
    format_classification_report_text,
    to_serializable,
)


def run_tier2_evaluation(
    dataset=None,
    pipeline: Optional[MedicalNERPipeline] = None,
    output_dir: Optional[Path] = None,
    limit: Optional[int] = None,
    silence_debug_logs: bool = True,
) -> Dict[str, Any]:
    """Execute Tier 2 evaluation across the test split and generate all artifacts."""
    output_dir = Path(output_dir) if output_dir else Path("eval/results")
    output_dir.mkdir(parents=True, exist_ok=True)

    if dataset is None:
        print("[TIER 2] Loading official test split from leduckhai/VietMed-NER...")
        dataset = load_vietmed_test_split("test")

    if limit is not None and limit > 0:
        dataset = dataset.select(range(min(limit, len(dataset))))

    total_samples = len(dataset)
    print(f"[TIER 2] Dataset ready with {total_samples} test sentences.")

    if silence_debug_logs:
        pipe_logger = get_logger()
        pipe_logger.logger.setLevel(logging.WARNING)
        for h in pipe_logger.logger.handlers:
            h.setLevel(logging.WARNING)

    if pipeline is None:
        print("[TIER 2] Initializing MedicalNERPipeline (enable_normalization=False for evaluation benchmark)...")
        pipeline = MedicalNERPipeline(enable_normalization=False)

    texts: List[str] = []
    gold_entities_list: List[List[Dict[str, Any]]] = []
    pred_entities_list: List[List[Dict[str, Any]]] = []
    latencies_ms: List[float] = []

    print("[TIER 2] Running full pipeline inference on test sentences...")
    t_start = time.perf_counter()

    for idx, item in enumerate(dataset):
        words = item["words"]
        labels = item["labels"]
        text = item["text"]
        texts.append(text)

        gold_spans = extract_gold_spans_target_schema(words, labels, text)
        gold_entities_list.append(gold_spans)

        t0 = time.perf_counter()
        result = pipeline.predict(text)
        t1 = time.perf_counter()
        latencies_ms.append((t1 - t0) * 1000.0)

        pred_entities_list.append(result.get("entities", []))

        if (idx + 1) % 500 == 0 or (idx + 1) == total_samples:
            elapsed_now = time.perf_counter() - t_start
            print(f"[TIER 2] Processed {idx + 1}/{total_samples} samples ({elapsed_now:.1f}s elapsed)...")

    total_elapsed = time.perf_counter() - t_start
    print(f"[TIER 2] Pipeline evaluation finished in {total_elapsed:.2f}s.")

    strict_report = evaluate_spans_strict(gold_entities_list, pred_entities_list, labels=TARGET_LABELS)
    relaxed_report = evaluate_spans_relaxed(gold_entities_list, pred_entities_list, labels=TARGET_LABELS)

    strict_text = format_classification_report_text(strict_report, title="Tier 2 Strict Exact Match Span Report (6 Labels)")
    relaxed_text = format_classification_report_text(relaxed_report, title="Tier 2 Relaxed Overlap Match Span Report (6 Labels)")

    combined_text = f"{strict_text}\n\n{relaxed_text}\n"
    combined_dict = {
        "strict_exact_match": strict_report,
        "relaxed_overlap_match": relaxed_report,
    }

    json_path = output_dir / "schema_6label_report.json"
    txt_path = output_dir / "schema_6label_report.txt"

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(to_serializable(combined_dict), f, ensure_ascii=False, indent=2)
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(combined_text)

    print(f"[TIER 2] Saved schema 6-label JSON report to {json_path}")
    print(f"[TIER 2] Saved schema 6-label Text report to {txt_path}")

    cm_png_path = output_dir / "confusion_matrix.png"
    compute_confusion_matrix_and_plot(gold_entities_list, pred_entities_list, cm_png_path, labels=TARGET_LABELS)
    print(f"[TIER 2] Saved confusion matrix heatmap to {cm_png_path}")

    top_errors = find_top_error_cases(texts, gold_entities_list, pred_entities_list, top_k=20)
    errors_path = output_dir / "top_error_cases.json"
    with open(errors_path, "w", encoding="utf-8") as f:
        json.dump(to_serializable(top_errors), f, ensure_ascii=False, indent=2)
    print(f"[TIER 2] Saved top {len(top_errors)} error cases to {errors_path}")

    lat_arr = np.array(latencies_ms)
    latency_report = {
        "total_samples": total_samples,
        "total_time_seconds": round(total_elapsed, 2),
        "mean_latency_ms": round(float(np.mean(lat_arr)), 2),
        "median_latency_ms": round(float(np.median(lat_arr)), 2),
        "p90_latency_ms": round(float(np.percentile(lat_arr, 90)), 2),
        "p95_latency_ms": round(float(np.percentile(lat_arr, 95)), 2),
        "p99_latency_ms": round(float(np.percentile(lat_arr, 99)), 2),
        "min_latency_ms": round(float(np.min(lat_arr)), 2),
        "max_latency_ms": round(float(np.max(lat_arr)), 2),
    }
    latency_path = output_dir / "latency_report.json"
    with open(latency_path, "w", encoding="utf-8") as f:
        json.dump(to_serializable(latency_report), f, ensure_ascii=False, indent=2)
    print(f"[TIER 2] Saved latency report to {latency_path}")

    return {
        "strict_report": strict_report,
        "relaxed_report": relaxed_report,
        "latency_report": latency_report,
        "top_errors": top_errors,
        "total_samples": total_samples,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Evaluate Tier 2: Target Schema 6 Labels")
    parser.add_argument("--limit", type=int, default=None, help="Limit samples")
    args = parser.parse_args()

    run_tier2_evaluation(limit=args.limit)

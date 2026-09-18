"""Master Evaluation Runner for VietMed-NER."""

import argparse
import json
import os
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional
_project_root = Path(__file__).resolve().parent.parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))



from eval.data_loader import check_and_get_splits, load_vietmed_test_split
from eval.evaluate_tier1 import run_tier1_evaluation
from eval.evaluate_tier2 import run_tier2_evaluation


def generate_summary_markdown(
    tier1_res: Optional[Dict[str, Any]],
    tier2_res: Optional[Dict[str, Any]],
    output_dir: Path,
    splits: List[str],
    total_samples: int,
) -> Path:
    """Generate consolidated markdown report of all evaluation results."""
    summary_path = output_dir / "summary.md"
    lines = []

    lines.append("# Báo Cáo Đánh Giá Mô Hình Medical NER trên VietMed-NER\n")
    lines.append("## 1. Thông Tin Tập Dữ Liệu & Phân Chia (Splits)\n")
    lines.append(f"- **Tập dữ liệu**: `leduckhai/VietMed-NER` (Hugging Face Hub)")
    lines.append(f"- **Các split tìm thấy**: `{splits}`")
    lines.append(f"- **Split sử dụng đánh giá**: `test` (split chính thức của dataset)")
    lines.append(f"- **Số câu đánh giá**: **{total_samples}** câu")
    lines.append(f"- **Loại bỏ dữ liệu âm thanh**: Đã gỡ bỏ cột `audio` để tối ưu tải và tránh lỗi torchcodec.")
    lines.append(f"- **Đảm bảo không data leakage**: Sử dụng split test độc lập, không trùng với tập train đã dùng huấn luyện.\n")

    if tier1_res:
        t1_dict = tier1_res["report_dict"]
        t1_elapsed = tier1_res["elapsed_sec"]
        lines.append("## 2. Kết Quả Đánh Giá Tầng 1: Nhãn Gốc (37 Nhãn BIO — Raw Model)\n")
        lines.append("> Đánh giá span-level chuẩn `seqeval` trực tiếp từ checkpoint model gốc, trước khi qua mapping và các rule hậu xử lý.\n")
        lines.append(f"- **Thời gian chạy**: {t1_elapsed:.2f}s ({t1_elapsed / total_samples * 1000:.2f} ms/câu)")
        lines.append(f"- **Micro F1**: **{t1_dict.get('micro avg', {}).get('f1-score', 0.0):.4f}** (P: {t1_dict.get('micro avg', {}).get('precision', 0.0):.4f}, R: {t1_dict.get('micro avg', {}).get('recall', 0.0):.4f})")
        lines.append(f"- **Macro F1**: **{t1_dict.get('macro avg', {}).get('f1-score', 0.0):.4f}**")
        lines.append(f"- **Weighted F1**: **{t1_dict.get('weighted avg', {}).get('f1-score', 0.0):.4f}**\n")

        t1_classes = [(k, v) for k, v in t1_dict.items() if not k.endswith("avg")]
        t1_classes.sort(key=lambda x: x[1].get("f1-score", 0.0))
        lines.append("### Top 5 Nhãn Yếu Nhất (Tầng 1 theo F1):\n")
        lines.append("| Hạng | Thực Thể | Precision | Recall | F1-Score | Support |")
        lines.append("|:---:|:---|:---:|:---:|:---:|:---:|")
        for rank, (cls_name, metrics) in enumerate(t1_classes[:5], 1):
            lines.append(
                f"| {rank} | `{cls_name}` | {metrics.get('precision', 0.0):.4f} | {metrics.get('recall', 0.0):.4f} | {metrics.get('f1-score', 0.0):.4f} | {metrics.get('support', 0)} |"
            )
        lines.append("\n")

    if tier2_res:
        t2_strict = tier2_res["strict_report"]
        t2_relaxed = tier2_res["relaxed_report"]
        lat = tier2_res["latency_report"]

        lines.append("## 3. Kết Quả Đánh Giá Tầng 2: Schema Mục Tiêu (6 Nhãn — Full Pipeline)\n")
        lines.append("> Đánh giá qua toàn bộ pipeline hoàn chỉnh (`MedicalNERPipeline.predict`), bao gồm tiền xử lý, ViHealthBERT, dosage extractor, filter & overlap resolution, và 2 rule patch (`blacklist` + `merge sốt cao`).\n")
        lines.append(f"- **Strict Exact Match (Khớp chính xác cả nhãn và tọa độ span)**:")
        lines.append(f"  - Micro F1: **{t2_strict.get('micro avg', {}).get('f1-score', 0.0):.4f}** (P: {t2_strict.get('micro avg', {}).get('precision', 0.0):.4f}, R: {t2_strict.get('micro avg', {}).get('recall', 0.0):.4f})")
        lines.append(f"  - Macro F1: **{t2_strict.get('macro avg', {}).get('f1-score', 0.0):.4f}**")
        lines.append(f"  - Weighted F1: **{t2_strict.get('weighted avg', {}).get('f1-score', 0.0):.4f}**")
        lines.append(f"- **Relaxed Match (Khớp nhãn và có giao nhau / overlap về vị trí span)**:")
        lines.append(f"  - Micro F1: **{t2_relaxed.get('micro avg', {}).get('f1-score', 0.0):.4f}** (P: {t2_relaxed.get('micro avg', {}).get('precision', 0.0):.4f}, R: {t2_relaxed.get('micro avg', {}).get('recall', 0.0):.4f})")
        lines.append(f"  - Macro F1: **{t2_relaxed.get('macro avg', {}).get('f1-score', 0.0):.4f}**\n")

        lines.append("### Bảng Chi Tiết Hiệu Năng 6 Nhãn Mục Tiêu (Strict vs Relaxed):\n")
        lines.append("| Nhãn Mục Tiêu | Strict P | Strict R | Strict F1 | Relaxed P | Relaxed R | Relaxed F1 | Support |")
        lines.append("|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|")
        for lbl in ["CONDITION", "DRUG", "BODY_PART", "TEST", "PROCEDURE", "DOSAGE"]:
            s = t2_strict.get(lbl, {})
            r = t2_relaxed.get(lbl, {})
            lines.append(
                f"| **{lbl}** | {s.get('precision', 0.0):.4f} | {s.get('recall', 0.0):.4f} | **{s.get('f1-score', 0.0):.4f}** | "
                f"{r.get('precision', 0.0):.4f} | {r.get('recall', 0.0):.4f} | **{r.get('f1-score', 0.0):.4f}** | {s.get('support', 0)} |"
            )
        lines.append("\n")

        t2_classes = [(lbl, t2_strict[lbl]) for lbl in ["CONDITION", "DRUG", "BODY_PART", "TEST", "PROCEDURE", "DOSAGE"]]
        t2_classes.sort(key=lambda x: x[1].get("f1-score", 0.0))
        lines.append("### Thứ Tự Nhãn Cần Cải Thiện Trong 6 Nhãn Mục Tiêu (theo Strict F1):\n")
        for rank, (cls_name, metrics) in enumerate(t2_classes, 1):
            lines.append(
                f"{rank}. **{cls_name}**: Strict F1 = `{metrics.get('f1-score', 0.0):.4f}` (P=`{metrics.get('precision', 0.0):.4f}`, R=`{metrics.get('recall', 0.0):.4f}`, Support={metrics.get('support', 0)})"
            )
        lines.append("\n")

        lines.append("## 4. Benchmark Thời Gian Xử Lý (Latency)\n")
        lines.append(f"- **Tổng thời gian xử lý**: {lat['total_time_seconds']} giây ({lat['total_samples']} câu)")
        lines.append(f"- **Thời gian trung bình (Mean)**: **{lat['mean_latency_ms']:.2f} ms / câu**")
        lines.append(f"- **Trung vị (Median / P50)**: {lat['median_latency_ms']:.2f} ms / câu")
        lines.append(f"- **Phân vị 90 (P90)**: {lat['p90_latency_ms']:.2f} ms / câu")
        lines.append(f"- **Phân vị 95 (P95)**: **{lat['p95_latency_ms']:.2f} ms / câu**")
        lines.append(f"- **Phân vị 99 (P99)**: {lat['p99_latency_ms']:.2f} ms / câu")
        lines.append(f"- **Min / Max**: {lat['min_latency_ms']:.2f} ms / {lat['max_latency_ms']:.2f} ms\n")

    lines.append("## 5. Danh Mục Các Tệp Kết Quả Chi Tiết\n")
    lines.append("| Tệp Tin | Định Dạng | Mô Tả |")
    lines.append("|:---|:---:|:---|")
    lines.append("| [`raw_37label_report.json`](raw_37label_report.json) | JSON | Báo cáo chi tiết metrics seqeval cho toàn bộ 37 nhãn BIO gốc |")
    lines.append("| [`raw_37label_report.txt`](raw_37label_report.txt) | Text | Bảng in dễ đọc báo cáo Tầng 1 |")
    lines.append("| [`schema_6label_report.json`](schema_6label_report.json) | JSON | Báo cáo chi tiết metrics Tầng 2 (cả Strict Match và Relaxed Match) |")
    lines.append("| [`schema_6label_report.txt`](schema_6label_report.txt) | Text | Bảng in so sánh Strict Match và Relaxed Match theo 6 nhãn |")
    lines.append("| [`confusion_matrix.png`](confusion_matrix.png) | Image | Heatmap ma trận nhầm lẫn giữa 6 nhãn mục tiêu và NONE |")
    lines.append("| [`top_error_cases.json`](top_error_cases.json) | JSON | Danh sách 20 câu có nhiều lỗi nhất |")
    lines.append("| [`latency_report.json`](latency_report.json) | JSON | Báo cáo chi tiết thời gian xử lý và các mức phân vị latency |")
    lines.append("\n---\n*Báo cáo được tạo tự động bởi `eval/run_eval.py`.*")

    content = "\n".join(lines)
    with open(summary_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"[SUMMARY] Generated summary report to {summary_path}")
    return summary_path

def main():
    parser = argparse.ArgumentParser(description="VietMed-NER Full Evaluation Suite")
    parser.add_argument("--limit", type=int, default=None, help="Limit number of test samples")
    parser.add_argument("--device", type=str, default=None, help="Device (cpu or cuda)")
    parser.add_argument("--output-dir", type=str, default="eval/results", help="Results directory")
    parser.add_argument("--tier1-only", action="store_true", help="Run only Tier 1")
    parser.add_argument("--tier2-only", action="store_true", help="Run only Tier 2")
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    splits = check_and_get_splits()
    print(f"Dataset splits found on Hub: {splits}")
    if "test" not in splits:
        print("ERROR: Official test split not found! Stopping.")
        sys.exit(1)

    print("Loading test split (dropping audio)...")
    dataset = load_vietmed_test_split("test")
    if args.limit and args.limit > 0:
        dataset = dataset.select(range(min(args.limit, len(dataset))))

    total_samples = len(dataset)
    print(f"Total test sentences for evaluation: {total_samples}")

    tier1_res = None
    tier2_res = None

    if not args.tier2_only:
        print("\n" + "=" * 50)
        print("STAGE 1: TIER 1 EVALUATION (RAW 37 LABELS)")
        print("=" * 50)
        tier1_res = run_tier1_evaluation(
            dataset=dataset,
            device=args.device,
            output_dir=output_dir,
        )

    if not args.tier1_only:
        print("\n" + "=" * 50)
        print("STAGE 2: TIER 2 EVALUATION (TARGET SCHEMA 6 LABELS)")
        print("=" * 50)
        tier2_res = run_tier2_evaluation(
            dataset=dataset,
            output_dir=output_dir,
        )

    print("\n" + "=" * 50)
    print("STAGE 3: GENERATING SUMMARY REPORT")
    print("=" * 50)
    generate_summary_markdown(
        tier1_res=tier1_res,
        tier2_res=tier2_res,
        output_dir=output_dir,
        splits=splits,
        total_samples=total_samples,
    )
    print("\nEVALUATION COMPLETED SUCCESSFULLY!")


if __name__ == "__main__":
    main()


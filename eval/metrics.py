"""Metrics, span matching, confusion matrix, and error analysis for evaluation."""

import json
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from ner.config import TARGET_LABELS


def to_serializable(obj: Any) -> Any:
    """Recursively convert numpy types and non-JSON-serializable values to native Python types."""
    if isinstance(obj, dict):
        return {str(k): to_serializable(v) for k, v in obj.items()}
    elif isinstance(obj, (list, tuple)):
        return [to_serializable(v) for v in obj]
    elif hasattr(obj, "item"):
        return obj.item()
    elif isinstance(obj, np.integer):
        return int(obj)
    elif isinstance(obj, np.floating):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    return obj



def evaluate_spans_strict(
    gold_entities_list: List[List[Dict[str, Any]]],
    pred_entities_list: List[List[Dict[str, Any]]],
    labels: Optional[Any] = None,
) -> Dict[str, Any]:
    """Calculate strict exact-match span-level precision, recall, and F1.
    
    A match requires exact match on (label, start_char, end_char).
    """
    if labels is None:
        labels_list = sorted(list(TARGET_LABELS))
    else:
        labels_list = sorted(list(labels)) if isinstance(labels, set) else list(labels)

    counts = {lbl: {"tp": 0, "fp": 0, "fn": 0, "support": 0} for lbl in labels_list}

    for golds, preds in zip(gold_entities_list, pred_entities_list):
        gold_tuples = {(g["label"], g["start_char"], g["end_char"]) for g in golds}
        pred_tuples = {(p["label"], p["start_char"], p["end_char"]) for p in preds}

        for g in golds:
            if g["label"] in counts:
                counts[g["label"]]["support"] += 1

        matched_golds = set()
        for p_tup in pred_tuples:
            lbl, s_c, e_c = p_tup
            if lbl not in counts:
                continue
            if p_tup in gold_tuples:
                counts[lbl]["tp"] += 1
                matched_golds.add(p_tup)
            else:
                counts[lbl]["fp"] += 1

        for g_tup in gold_tuples:
            lbl, s_c, e_c = g_tup
            if lbl in counts and g_tup not in matched_golds:
                counts[lbl]["fn"] += 1

    report: Dict[str, Any] = {}
    total_tp = sum(counts[lbl]["tp"] for lbl in labels_list)
    total_fp = sum(counts[lbl]["fp"] for lbl in labels_list)
    total_fn = sum(counts[lbl]["fn"] for lbl in labels_list)
    total_support = sum(counts[lbl]["support"] for lbl in labels_list)

    for lbl in labels_list:
        tp = counts[lbl]["tp"]
        fp = counts[lbl]["fp"]
        fn = counts[lbl]["fn"]
        supp = counts[lbl]["support"]

        prec = tp / (tp + fp) if (tp + fp) > 0 else 0.0
        rec = tp / (tp + fn) if (tp + fn) > 0 else 0.0
        f1 = (2 * prec * rec) / (prec + rec) if (prec + rec) > 0 else 0.0

        report[lbl] = {
            "precision": round(prec, 4),
            "recall": round(rec, 4),
            "f1-score": round(f1, 4),
            "support": supp,
            "tp": tp,
            "fp": fp,
            "fn": fn,
        }

    micro_p = total_tp / (total_tp + total_fp) if (total_tp + total_fp) > 0 else 0.0
    micro_r = total_tp / (total_tp + total_fn) if (total_tp + total_fn) > 0 else 0.0
    micro_f1 = (2 * micro_p * micro_r) / (micro_p + micro_r) if (micro_p + micro_r) > 0 else 0.0
    report["micro avg"] = {
        "precision": round(micro_p, 4),
        "recall": round(micro_r, 4),
        "f1-score": round(micro_f1, 4),
        "support": total_support,
    }

    macro_p = float(np.mean([report[lbl]["precision"] for lbl in labels]))
    macro_r = float(np.mean([report[lbl]["recall"] for lbl in labels]))
    macro_f1 = float(np.mean([report[lbl]["f1-score"] for lbl in labels]))
    report["macro avg"] = {
        "precision": round(macro_p, 4),
        "recall": round(macro_r, 4),
        "f1-score": round(macro_f1, 4),
        "support": total_support,
    }

    if total_support > 0:
        w_p = sum(report[lbl]["precision"] * report[lbl]["support"] for lbl in labels) / total_support
        w_r = sum(report[lbl]["recall"] * report[lbl]["support"] for lbl in labels) / total_support
        w_f1 = sum(report[lbl]["f1-score"] * report[lbl]["support"] for lbl in labels) / total_support
    else:
        w_p, w_r, w_f1 = 0.0, 0.0, 0.0

    report["weighted avg"] = {
        "precision": round(w_p, 4),
        "recall": round(w_r, 4),
        "f1-score": round(w_f1, 4),
        "support": total_support,
    }
    return report


def evaluate_spans_relaxed(
    gold_entities_list: List[List[Dict[str, Any]]],
    pred_entities_list: List[List[Dict[str, Any]]],
    labels: Optional[Any] = None,
) -> Dict[str, Any]:
    """Calculate relaxed span-level precision, recall, and F1 where span overlap counts as match."""
    if labels is None:
        labels_list = sorted(list(TARGET_LABELS))
    else:
        labels_list = sorted(list(labels)) if isinstance(labels, set) else list(labels)

    counts = {lbl: {"tp": 0, "fp": 0, "fn": 0, "support": 0} for lbl in labels_list}

    for golds, preds in zip(gold_entities_list, pred_entities_list):
        for g in golds:
            if g["label"] in counts:
                counts[g["label"]]["support"] += 1

        matched_gold_indices = set()
        matched_pred_indices = set()

        for p_idx, p in enumerate(preds):
            p_lbl = p["label"]
            if p_lbl not in counts:
                continue
            for g_idx, g in enumerate(golds):
                if g_idx in matched_gold_indices:
                    continue
                if g["label"] == p_lbl:
                    if max(p["start_char"], g["start_char"]) < min(p["end_char"], g["end_char"]):
                        counts[p_lbl]["tp"] += 1
                        matched_gold_indices.add(g_idx)
                        matched_pred_indices.add(p_idx)
                        break

        for p_idx, p in enumerate(preds):
            if p_idx not in matched_pred_indices and p["label"] in counts:
                counts[p["label"]]["fp"] += 1

        for g_idx, g in enumerate(golds):
            if g_idx not in matched_gold_indices and g["label"] in counts:
                counts[g["label"]]["fn"] += 1

    report: Dict[str, Any] = {}
    total_tp = sum(counts[lbl]["tp"] for lbl in labels_list)
    total_fp = sum(counts[lbl]["fp"] for lbl in labels_list)
    total_fn = sum(counts[lbl]["fn"] for lbl in labels_list)
    total_support = sum(counts[lbl]["support"] for lbl in labels_list)

    for lbl in labels_list:
        tp = counts[lbl]["tp"]
        fp = counts[lbl]["fp"]
        fn = counts[lbl]["fn"]
        supp = counts[lbl]["support"]
        prec = tp / (tp + fp) if (tp + fp) > 0 else 0.0
        rec = tp / (tp + fn) if (tp + fn) > 0 else 0.0
        f1 = (2 * prec * rec) / (prec + rec) if (prec + rec) > 0 else 0.0

        report[lbl] = {
            "precision": round(prec, 4),
            "recall": round(rec, 4),
            "f1-score": round(f1, 4),
            "support": supp,
            "tp": tp,
            "fp": fp,
            "fn": fn,
        }

    micro_p = total_tp / (total_tp + total_fp) if (total_tp + total_fp) > 0 else 0.0
    micro_r = total_tp / (total_tp + total_fn) if (total_tp + total_fn) > 0 else 0.0
    micro_f1 = (2 * micro_p * micro_r) / (micro_p + micro_r) if (micro_p + micro_r) > 0 else 0.0
    report["micro avg"] = {
        "precision": round(micro_p, 4),
        "recall": round(micro_r, 4),
        "f1-score": round(micro_f1, 4),
        "support": total_support,
    }

    report["macro avg"] = {
        "precision": round(float(np.mean([report[lbl]["precision"] for lbl in labels])), 4),
        "recall": round(float(np.mean([report[lbl]["recall"] for lbl in labels])), 4),
        "f1-score": round(float(np.mean([report[lbl]["f1-score"] for lbl in labels])), 4),
        "support": total_support,
    }

    return report


def format_classification_report_text(report: Dict[str, Any], title: str = "Classification Report") -> str:
    """Format dictionary report into standard aligned text table."""
    lines = [f"{title}\n", "=" * 70]
    header = f"{'Category':<22} {'Precision':<12} {'Recall':<12} {'F1-Score':<12} {'Support':<10}"
    lines.append(header)
    lines.append("-" * 70)

    category_keys = [k for k in report.keys() if not k.endswith("avg")]
    avg_keys = [k for k in report.keys() if k.endswith("avg")]

    for k in category_keys:
        m = report[k]
        lines.append(
            f"{k:<22} {m['precision']:<12.4f} {m['recall']:<12.4f} {m['f1-score']:<12.4f} {m['support']:<10}"
        )

    lines.append("-" * 70)
    for k in avg_keys:
        m = report[k]
        lines.append(
            f"{k:<22} {m['precision']:<12.4f} {m['recall']:<12.4f} {m['f1-score']:<12.4f} {m['support']:<10}"
        )
    lines.append("=" * 70)
    return "\n".join(lines)


def compute_confusion_matrix_and_plot(
    gold_entities_list: List[List[Dict[str, Any]]],
    pred_entities_list: List[List[Dict[str, Any]]],
    output_png_path: Path,
    labels: Optional[Any] = None,
) -> Dict[str, Any]:
    """Build confusion matrix for 6 target categories + [NONE], and plot heatmap."""
    if labels is None:
        labels_list = sorted(list(TARGET_LABELS))
    else:
        labels_list = sorted(list(labels)) if isinstance(labels, set) else list(labels)

    extended_labels = labels_list + ["NONE"]
    label_to_idx = {lbl: i for i, lbl in enumerate(extended_labels)}
    cm = np.zeros((len(extended_labels), len(extended_labels)), dtype=int)

    for golds, preds in zip(gold_entities_list, pred_entities_list):
        matched_gold = set()
        matched_pred = set()

        for p_idx, p in enumerate(preds):
            p_lbl = p["label"]
            best_overlap = 0
            best_g_idx = None

            for g_idx, g in enumerate(golds):
                overlap = max(0, min(p["end_char"], g["end_char"]) - max(p["start_char"], g["start_char"]))
                if overlap > best_overlap:
                    best_overlap = overlap
                    best_g_idx = g_idx

            if best_g_idx is not None and best_overlap > 0:
                g_lbl = golds[best_g_idx]["label"]
                if g_lbl in label_to_idx and p_lbl in label_to_idx:
                    cm[label_to_idx[g_lbl], label_to_idx[p_lbl]] += 1
                    matched_gold.add(best_g_idx)
                    matched_pred.add(p_idx)

        for g_idx, g in enumerate(golds):
            if g_idx not in matched_gold:
                g_lbl = g["label"]
                if g_lbl in label_to_idx:
                    cm[label_to_idx[g_lbl], label_to_idx["NONE"]] += 1

        for p_idx, p in enumerate(preds):
            if p_idx not in matched_pred:
                p_lbl = p["label"]
                if p_lbl in label_to_idx:
                    cm[label_to_idx["NONE"], label_to_idx[p_lbl]] += 1

    fig, ax = plt.subplots(figsize=(10, 8), dpi=300)
    cax = ax.matshow(cm, cmap=plt.cm.Blues, alpha=0.85)

    for i in range(len(extended_labels)):
        for j in range(len(extended_labels)):
            val = cm[i, j]
            color = "white" if val > (cm.max() / 2.0) else "black"
            ax.text(j, i, str(val), va="center", ha="center", color=color, fontsize=9, fontweight="bold")

    fig.colorbar(cax)
    ax.set_xticks(range(len(extended_labels)))
    ax.set_yticks(range(len(extended_labels)))
    ax.set_xticklabels(extended_labels, rotation=45, ha="left", fontsize=9)
    ax.set_yticklabels(extended_labels, fontsize=9)
    ax.set_xlabel("Predicted Category", fontsize=11, fontweight="bold", labelpad=10)
    ax.set_ylabel("Gold Category", fontsize=11, fontweight="bold", labelpad=10)
    ax.set_title("VietMed-NER Target Schema Confusion Matrix (6 Labels + NONE)", fontsize=13, fontweight="bold", pad=20)

    plt.tight_layout()
    output_png_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_png_path)
    plt.close()

    return {
        "labels": extended_labels,
        "matrix": cm.tolist(),
    }


def find_top_error_cases(
    texts: List[str],
    gold_entities_list: List[List[Dict[str, Any]]],
    pred_entities_list: List[List[Dict[str, Any]]],
    top_k: int = 20,
) -> List[Dict[str, Any]]:
    """Identify top K sentences with highest number of entity errors."""
    scored_cases = []

    for idx, (text, golds, preds) in enumerate(zip(texts, gold_entities_list, pred_entities_list)):
        gold_tuples = {(g["label"], g["start_char"], g["end_char"], g["surface_text"]) for g in golds}
        pred_tuples = {(p["label"], p["start_char"], p["end_char"], p["surface_text"]) for p in preds}

        missed = gold_tuples - pred_tuples
        spurious = pred_tuples - gold_tuples

        error_count = len(missed) + len(spurious)
        if error_count == 0:
            continue

        summary_parts = []
        if missed:
            missed_str = ", ".join(f"[{lbl}] '{txt}'" for lbl, _, _, txt in missed)
            summary_parts.append(f"Missed {len(missed)}: {missed_str}")
        if spurious:
            spurious_str = ", ".join(f"[{lbl}] '{txt}'" for lbl, _, _, txt in spurious)
            summary_parts.append(f"Spurious {len(spurious)}: {spurious_str}")

        scored_cases.append({
            "index": idx,
            "error_count": error_count,
            "text": text,
            "gold_entities": golds,
            "predicted_entities": preds,
            "error_summary": "; ".join(summary_parts),
        })

    scored_cases.sort(key=lambda x: x["error_count"], reverse=True)
    return scored_cases[:top_k]



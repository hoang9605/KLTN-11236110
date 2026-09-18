"""Tier 1 Evaluation: Raw 37 BIO labels evaluation on VietMed-NER test split using seqeval."""

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



import torch
from seqeval.metrics import classification_report
from transformers import AutoModelForTokenClassification, AutoTokenizer

from ner.config import MAX_POSITION_EMBEDDINGS, SPECIAL_TOKENS, resolve_model_path
from eval.data_loader import load_vietmed_test_split, normalize_bio_tag
from eval.metrics import to_serializable


def predict_raw_bio_batch(
    sentences_words: List[List[str]],
    tokenizer: Any,
    model: Any,
    device: torch.device,
    id2label: Dict[int, str],
) -> List[List[str]]:
    """Predict word-level raw 37 BIO tags for a list of tokenized sentences using first subtoken."""
    bos_tok = tokenizer.bos_token or "<s>"
    eos_tok = tokenizer.eos_token or "</s>"
    all_pred_bios: List[List[str]] = []

    total = len(sentences_words)
    for sent_idx, words in enumerate(sentences_words):
        if not words:
            all_pred_bios.append([])
            continue

        subtokens: List[str] = []
        subtoken_word_map: List[Optional[int]] = []

        for word_idx, w in enumerate(words):
            pieces = tokenizer.tokenize(w)
            if not pieces:
                pieces = [tokenizer.unk_token]
            for p in pieces:
                subtokens.append(p)
                subtoken_word_map.append(word_idx)

        full_tokens = [bos_tok] + subtokens + [eos_tok]
        full_word_map = [None] + subtoken_word_map + [None]

        if len(full_tokens) > MAX_POSITION_EMBEDDINGS:
            full_tokens = full_tokens[: MAX_POSITION_EMBEDDINGS - 1] + [eos_tok]
            full_word_map = full_word_map[: MAX_POSITION_EMBEDDINGS - 1] + [None]

        input_ids = tokenizer.convert_tokens_to_ids(full_tokens)
        input_tensor = torch.tensor([input_ids], dtype=torch.long, device=device)

        with torch.no_grad():
            outputs = model(input_tensor)
            logits = outputs.logits[0]
            pred_ids = torch.argmax(logits, dim=-1)

        word_preds: Dict[int, str] = {}
        for tok_idx, w_idx in enumerate(full_word_map):
            if w_idx is None:
                continue
            tok_str = full_tokens[tok_idx]
            if tok_str in SPECIAL_TOKENS:
                continue
            if w_idx not in word_preds:
                pid = pred_ids[tok_idx].item()
                word_preds[w_idx] = id2label.get(pid, "O")

        pred_bio = [word_preds.get(i, "O") for i in range(len(words))]
        all_pred_bios.append(pred_bio)

        if (sent_idx + 1) % 200 == 0 or (sent_idx + 1) == total:
            print(f"[TIER 1] Processed {sent_idx + 1}/{total} samples...")

    return all_pred_bios


def run_tier1_evaluation(
    dataset=None,
    model_path: Optional[Path] = None,
    device: Optional[str] = None,
    output_dir: Optional[Path] = None,
    limit: Optional[int] = None,
) -> Dict[str, Any]:
    """Execute Tier 1 evaluation and write reports to output_dir."""
    output_dir = Path(output_dir) if output_dir else Path("eval/results")
    output_dir.mkdir(parents=True, exist_ok=True)

    if dataset is None:
        print("[TIER 1] Loading official test split from leduckhai/VietMed-NER...")
        dataset = load_vietmed_test_split("test")

    if limit is not None and limit > 0:
        dataset = dataset.select(range(min(limit, len(dataset))))

    total_samples = len(dataset)
    print(f"[TIER 1] Dataset ready with {total_samples} test sentences.")

    dev = torch.device(device) if device else torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"[TIER 1] Using inference device: {dev}")

    resolved_path = resolve_model_path(model_path)
    tokenizer = AutoTokenizer.from_pretrained(str(resolved_path), use_fast=False)
    model = AutoModelForTokenClassification.from_pretrained(str(resolved_path))
    model.to(dev)
    model.eval()

    id2label = {int(k): v for k, v in model.config.id2label.items()}

    print("[TIER 1] Running raw model inference across all test samples...")
    t0 = time.perf_counter()

    sentences_words = [item["words"] for item in dataset]
    y_true = [[normalize_bio_tag(lbl) for lbl in item["labels"]] for item in dataset]
    y_pred = predict_raw_bio_batch(sentences_words, tokenizer, model, dev, id2label)

    elapsed = time.perf_counter() - t0
    print(f"[TIER 1] Inference finished in {elapsed:.2f}s ({elapsed/total_samples*1000:.2f} ms/sample).")

    report_dict = classification_report(y_true, y_pred, output_dict=True, digits=4)
    report_text = classification_report(y_true, y_pred, output_dict=False, digits=4)

    json_path = output_dir / "raw_37label_report.json"
    txt_path = output_dir / "raw_37label_report.txt"

    report_dict = to_serializable(report_dict)
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(report_dict, f, ensure_ascii=False, indent=2)

    with open(txt_path, "w", encoding="utf-8") as f:
        f.write("Tier 1 Raw 37-Label Evaluation Report (seqeval span-level)\n")
        f.write(f"Total Sentences: {total_samples}\n")
        f.write(f"Inference Time: {elapsed:.2f}s\n\n")
        f.write(report_text)

    print(f"[TIER 1] Saved json report to {json_path}")
    print(f"[TIER 1] Saved text report to {txt_path}")
    return {
        "report_dict": report_dict,
        "report_text": report_text,
        "elapsed_sec": elapsed,
        "total_samples": total_samples,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Evaluate Tier 1: Raw 37 BIO Labels")
    parser.add_argument("--limit", type=int, default=None, help="Limit samples")
    parser.add_argument("--device", type=str, default=None, help="Device (cpu/cuda)")
    args = parser.parse_args()

    run_tier1_evaluation(limit=args.limit, device=args.device)

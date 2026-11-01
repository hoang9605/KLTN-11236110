"""python -m relation_extraction train|predict --help"""
import argparse
import hashlib
import json
import os
import platform
from collections import Counter
from pathlib import Path

# Set before sklearn/torch native libraries are imported on Windows.
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("KMP_DUPLICATE_LIB_OK", "TRUE")

import sklearn

from .data import load_pairs, split_pairs, RELATIONS, SCHEMA_PATH
from .model import RelationExtractor, evaluate
from .pipeline import MedicalREPipeline


def write_json(path, data):
    Path(path).write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def write_jsonl(path, data):
    Path(path).write_text("".join(json.dumps(row, ensure_ascii=False) + "\n" for row in data), encoding="utf-8")


def train(args):
    output = Path(args.output)
    if output.exists() and any(output.iterdir()):
        raise ValueError("Output directory is nonempty; choose a new run directory")
    pairs, audit = load_pairs(args.data, allow_ai=args.allow_ai_labels)
    splits = split_pairs(pairs, args.seed)
    model = RelationExtractor(args.seed).fit(splits["train"])
    provisional = any(not (p["human_verified"] and p["training_eligible"]) for p in pairs)
    metadata = {"label_source": "AI_provisional" if provisional else "human_verified",
                "allow_ai_labels": args.allow_ai_labels, "source": str(Path(args.data).resolve()),
                "source_sha256": hashlib.sha256(Path(args.data).read_bytes()).hexdigest(),
                "schema_sha256": hashlib.sha256(SCHEMA_PATH.read_bytes()).hexdigest(),
                "seed": args.seed, "python": platform.python_version(), "sklearn": sklearn.__version__,
                "model": "character TF-IDF (2,5), balanced LogisticRegression C=1, threshold=0.5",
                "split_policy": "70/15/15 normalized-text groups; one group per label reserved for train",
                "supported_relations": model.supported_relations,
                "unsupported_relations": sorted(set(RELATIONS) - set(model.supported_relations)),
                "limitations": ["AI label agreement, not expert gold accuracy",
                                "Review flags retained; definite pairs from flagged samples included",
                                "Unknown/unannotated pairs excluded, never converted to negatives",
                                "Source VietMed train; not an independent NER/end-to-end benchmark",
                                "Text grouping does not establish speaker/conversation independence",
                                "Rare or absent labels cannot be meaningfully evaluated",
                                "Exploratory diagnostics, not a finalized thesis evaluation protocol"]}
    model.metadata = metadata
    output.mkdir(parents=True, exist_ok=True)
    model.save(output / "model.joblib")
    report = {"metadata": metadata, "data_audit": audit, "splits": {}, "evaluation": {}}
    for split, examples in splits.items():
        write_jsonl(output / f"{split}.jsonl", examples)
        report["splits"][split] = {"pairs": len(examples), "text_groups": len({p["group"] for p in examples}),
                                    "labels": dict(Counter(p["label"] for p in examples)),
                                    "pairs_with_review_flags": sum(bool(p["review_flags"]) for p in examples)}
        predictions = model.predict_pairs(examples)
        if split != "train":
            report["evaluation"][split] = evaluate([p["label"] for p in examples], [p["label"] for p in predictions])
            write_jsonl(output / f"{split}_predictions.jsonl", [
                {"sample_id": p["sample_id"], "head": p["head"]["id"], "tail": p["tail"]["id"],
                 "gold_ai_label": p["label"], "prediction": prediction}
                for p, prediction in zip(examples, predictions)])
    write_json(output / "report.json", report)
    print(json.dumps(report, ensure_ascii=False, indent=2))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    trainer = sub.add_parser("train")
    trainer.add_argument("--data", required=True)
    trainer.add_argument("--output", required=True)
    trainer.add_argument("--allow-ai-labels", action="store_true")
    trainer.add_argument("--seed", type=int, default=42)
    predictor = sub.add_parser("predict")
    predictor.add_argument("--model", required=True)
    source = predictor.add_mutually_exclusive_group(required=True)
    source.add_argument("--text", help="Run existing NER then RE")
    source.add_argument("--input", help="JSON object containing text and entities (annotation or NER format)")
    predictor.add_argument("--output")
    args = parser.parse_args()
    if args.command == "train":
        train(args)
    else:
        pipeline = MedicalREPipeline(RelationExtractor.load(args.model))
        result = (pipeline.from_ner_result(json.loads(Path(args.input).read_text(encoding="utf-8-sig")))
                  if args.input else pipeline.predict(args.text))
        if args.output:
            write_json(args.output, result)
        print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

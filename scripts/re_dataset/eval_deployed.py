r"""Score the saved ViHealthBERT RE model (the one the pipeline and knowledge graph load)
on the same three evaluation sets as benchmark.py, alone and in union with the rules.

It loads the model through relation_extraction.bert_model.load_extractor on CPU, i.e.
the deployed code path, and checks its labels against the GPU predictions written at
training time (bert_deployed_predictions.json): any difference would mean the save/load
or the CPU path changed the model.

The deployed extractor averages the same three seeds as the benchmark's "bert" row, so
its scores should match the benchmark up to GPU non-determinism between training runs.
Each seed alone is also scored (from the training-time probabilities), to show how much
a single seed varies. Output: <out>/deployed.json, <out>/deployed.md

    .venv\Scripts\python.exe -X utf8 scripts/re_dataset/eval_deployed.py --out outputs/re_benchmark_2026-11-08
"""
import argparse
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from benchmark import block, load_data, union  # noqa: E402
from relation_extraction.bert_model import load_extractor  # noqa: E402
from relation_extraction.data import NEGATIVE  # noqa: E402
from relation_extraction.rules import RuleRelationExtractor  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
TEST_NAMES = {"v1_1": "golden_test", "v1": "golden_test_v1_original", "random_v1": "random_test"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default=str(ROOT / "Model/vihealthbert-re-v1"))
    ap.add_argument("--out", required=True)
    ap.add_argument("--device", default="cpu")
    a = ap.parse_args()
    out = Path(a.out)
    ext = load_extractor(a.model, device=a.device)
    rules = RuleRelationExtractor()
    _, tests = load_data()
    gpu_path = out / "bert_deployed_predictions.json"
    gpu_all = json.loads(gpu_path.read_text(encoding="utf-8")) if gpu_path.exists() else {}
    gpu = gpu_all.get("golden_test", {})
    per_seed = gpu_all.get("prob_per_seed", {})
    bench = json.loads((out / "benchmark.json").read_text(encoding="utf-8"))
    report = {"model": a.model, "config": ext.config, "device": a.device, "sets": {}}
    for key, pairs in tests.items():
        t0 = time.time()
        res = ext.predict_pairs(pairs)
        secs = time.time() - t0
        bert = [r["label"] if r["status"] == "predicted" else NEGATIVE for r in res]
        rule = [r["label"] for r in rules.predict_pairs(pairs)]
        scores = block(pairs, {"bert_deployed": bert, "bert_deployed+rules": union(bert, rule)})
        seeds = {}
        for s, prob in per_seed.items():
            if all(p["uid"] in prob for p in pairs):
                y = [p["allowed_relation"] if prob[p["uid"]] >= 0.5 and p["allowed_relation"] in ext.supported_relations
                     else NEGATIVE for p in pairs]
                sc = block(pairs, {"alone": y, "with_rules": union(y, rule)})
                seeds[s] = {k: v["positive_micro"]["f1"] for k, v in sc.items()}
        diff = sum(1 for p, y in zip(pairs, bert) if p["uid"] in gpu and gpu[p["uid"]] != y)
        name = TEST_NAMES[key]
        report["sets"][name] = {
            "pairs": len(pairs), **scores,
            "benchmark_3seed": {m: bench[name][m]["positive_micro"] for m in ("bert", "bert+rules", "rules")},
            "single_seed_f1": seeds, "cpu_vs_gpu_label_differences": diff, "gpu_predictions_checked": sum(p["uid"] in gpu for p in pairs),
            "cpu_seconds": round(secs, 1), "ms_per_pair": round(1000 * secs / max(len(pairs), 1), 1)}
    (out / "deployed.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    def f(x):
        return f"{x:.3f}"
    L = ["# Mô hình ViHealthBERT RE được triển khai so với benchmark", "",
         f"Mô hình: `{Path(a.model).name}`, trung bình {len(ext.config['seeds'])} seed {ext.config['seeds']}, "
         f"{ext.config['train_pairs']} cặp huấn luyện; chạy trên {a.device}.", "",
         "| Tập | Cặp | Triển khai | Triển khai ∪ luật | Benchmark BERT | Benchmark BERT ∪ luật | Luật | Lệch CPU/GPU | ms/cặp |",
         "|---|---:|---:|---:|---:|---:|---:|---:|---:|"]
    for name, s in report["sets"].items():
        b = s["benchmark_3seed"]
        L.append(f"| {name} | {s['pairs']} | {f(s['bert_deployed']['positive_micro']['f1'])} | "
                 f"{f(s['bert_deployed+rules']['positive_micro']['f1'])} | {f(b['bert']['f1'])} | {f(b['bert+rules']['f1'])} | "
                 f"{f(b['rules']['f1'])} | {s['cpu_vs_gpu_label_differences']}/{s['gpu_predictions_checked']} | {s['ms_per_pair']} |")
    L += ["", "## Từng seed riêng lẻ (F1 một mình / hợp với luật)", "", "| Tập | " + " | ".join(f"seed {s}" for s in per_seed) + " |",
          "|---|" + "---:|" * len(per_seed)]
    for name, s in report["sets"].items():
        L.append(f"| {name} | " + " | ".join(f"{f(v['alone'])} / {f(v['with_rules'])}" for v in s["single_seed_f1"].values()) + " |")
    (out / "deployed.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    print("\n".join(L))


if __name__ == "__main__":
    main()

r"""Build the medical knowledge graph: text -> NER -> normalization -> RE -> merged graph.

Sources (pick one):
  --split test|validation|train   VietMed-NER sentences (deduplicated, empty ones skipped)
  --texts file.txt                one text per line
  --from-results results.jsonl    reuse per-sentence results of an earlier run (no models)

Entities:
  --entities model (default)  the NER model, i.e. what the deployed system would produce
  --entities gold             VietMed-NER gold spans (isolates RE + normalization quality)

Relations: the learned RE model alone (--re-mode fallback: rules only for relations the model does not support;
the model supports all five, so rules are not used). --re-mode union adds rule positives (lower on test_v2: 0.682 vs 0.693).
Default model: ViHealthBERT-RE (Model/vihealthbert-re-vietmed-811), ViHealthBERT with entity markers,
trained by scripts/re_dataset/train_811_gold.py --save-model on the 8:1:1 RE split (LLM-labelled, expert-reviewed),
scored in outputs/re_811_gold/compare.json. --re-model Model/vihealthbert-re-v1 gives the
earlier model, --re-model outputs/re_ai_v2/model.joblib the TF-IDF model. --rules-only uses rules everywhere.

Outputs in --out: results.jsonl, kg.json, triples.csv, nodes.csv, kg.graphml, kg.html, stats.md

    .venv\Scripts\python.exe -X utf8 scripts/build_kg.py --split test --out outputs/kg_test_2026-11-07
    .venv\Scripts\python.exe -X utf8 scripts/build_kg.py --from-results outputs/kg_test_2026-11-07/results.jsonl --rerun-re --out outputs/kg_test_2026-11-08
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
sys.path.insert(0, str(ROOT / "scripts" / "golden_test"))

from knowledge_graph import HybridRelationExtractor, KnowledgeGraph  # noqa: E402
from knowledge_graph.visualize import RELATION_VI, write_html  # noqa: E402

DEFAULT_RE_MODEL = ROOT / "Model/vihealthbert-re-vietmed-811"  # ViHealthBERT-RE trên phép chia 8:1:1 do chuyên gia duyệt; outputs/re_811_gold/compare.json


def iter_texts(a):
    if a.texts:
        for i, line in enumerate(Path(a.texts).read_text(encoding="utf-8").splitlines()):
            if line.strip():
                yield f"line-{i}", line.strip(), None
        return
    from common import entities_from_bio, load_split, text_group
    rows, _ = load_split(a.split)
    seen = set()
    for i, r in enumerate(rows):
        if len(r["words"]) != len(r["labels"]):
            continue
        text, ents = entities_from_bio(r["words"], r["labels"])
        g = text_group(text)
        if not text.strip() or g in seen:
            continue
        seen.add(g)
        yield f"{a.split}-{i}", text, ents


def make_re(a):
    from relation_extraction.pipeline import MedicalREPipeline
    model = None
    if not a.rules_only:
        from relation_extraction.bert_model import load_extractor
        try:
            model = load_extractor(a.re_model)
        except FileNotFoundError as e:
            sys.exit(f"{e}\nDùng --re-model outputs/re_ai_v2/model.joblib cho mô hình TF-IDF, hoặc --rules-only.")
    return MedicalREPipeline(HybridRelationExtractor(model, mode=a.re_mode))


def make_runner(a):
    re_pipe = make_re(a)
    if a.entities == "gold":
        from normalization.dispatcher import EntityNormalizationPipeline
        norm = EntityNormalizationPipeline()

        def run(text, gold):
            ents = [{"surface_text": e["text"], "label": e["label"], "start_char": e["start"],
                     "end_char": e["end"], "confidence": 1.0} for e in gold]
            return re_pipe.from_ner_result({"text": text, "entities": norm.normalize_entities(ents)})
        return run, re_pipe.extractor.metadata

    from ner.pipeline import MedicalNERPipeline
    ner = MedicalNERPipeline(enable_normalization=True)

    def run(text, _gold):
        return re_pipe.from_ner_result(ner.predict(text, normalize=True))
    return run, re_pipe.extractor.metadata


def stats_md(kg, meta, a):
    s = kg.stats()
    data = kg.to_dict()
    names = {n["key"]: n["name"] for n in data["nodes"]}
    src = args_source(a)
    L = ["# Đồ thị tri thức y tế", "",
         f"- Nguồn: {src}; thực thể: **{a.entities}**; quan hệ: "
         + ("chỉ luật" if a.rules_only else
            f"{'ViHealthBERT' if meta.get('model_name') == 'vihealthbert-entity-marker' else 'mô hình TF-IDF'} "
            f"({', '.join(meta['model_relations'])}) ∪ luật (mọi quan hệ; riêng {', '.join(meta['rule_relations'])} chỉ do luật)"),
         f"- {s['documents']} câu → **{s['nodes']} nút** ({s['normalized_nodes']} có mã ICD-10/RxNorm), "
         f"**{s['edges']} cạnh** khác nhau ({s['edge_mentions']} lần xuất hiện); {s['isolated_nodes']} nút không có quan hệ.",
         "- Nút được gộp theo mã chuẩn khi chuẩn hóa có quyết định, nếu không theo loại + chữ đã chuẩn hóa.", "",
         "| Loại nút | Số nút |", "|---|---:|"]
    L += [f"| {t} | {c} |" for t, c in sorted(s["nodes_by_type"].items(), key=lambda kv: -kv[1])]
    L += ["", "| Quan hệ | Số cạnh khác nhau | Lần xuất hiện | Nguồn |", "|---|---:|---:|---|"]
    for rel in sorted(s["edges_by_relation"], key=lambda r: -s["edges_by_relation"][r]):
        es = [e for e in data["edges"] if e["relation"] == rel]
        srcs = {}
        for e in es:
            for k, v in e["sources"].items():
                srcs[k] = srcs.get(k, 0) + v
        L.append(f"| {rel} ({RELATION_VI.get(rel, rel)}) | {len(es)} | {sum(e['count'] for e in es)} | "
                 + ", ".join(f"{k} {v}" for k, v in srcs.items()) + " |")
    L += ["", "## 25 bộ ba xuất hiện nhiều nhất", "", "| Đầu | Quan hệ | Cuối | Số lần | Nguồn |", "|---|---|---|---:|---|"]
    for e in data["edges"][:25]:
        L.append(f"| {names[e['head']]} | {e['relation']} | {names[e['tail']]} | {e['count']} | {', '.join(e['sources'])} |")
    L += ["", "## Hạn chế", "",
          ("- Chất lượng cạnh phụ thuộc RE: trên tập kiểm tra test_v2 (311 cặp, người chuyên môn gán) ViHealthBERT đạt micro F1 0,69 (KTC 95% 0,62–0,76) với precision 0,60, còn ViHealthBERT ∪ luật đạt 0,68 với precision 0,57, tức khoảng 4/10 cạnh có thể sai (relation/outputs/evaluation_test_v2_modes.json). `has_dosage` không có trong tập kiểm định nên chưa được đánh giá riêng; nhiều cạnh `has_dosage` nối tới cụm không phải liều (ví dụ 'nồng độ', 'cao')."
           if meta.get("model_name") == "vihealthbert-entity-marker" else
           "- Chất lượng cạnh phụ thuộc RE: bộ trích mô hình + luật (union) có F1 khoảng 0,47–0,48 (CV và golden test, nhãn AI); `has_dosage` chỉ do luật sinh ra (F1 0,18 trên golden test)."),
          "- Thực thể chưa chuẩn hóa không gộp được với các cách viết khác (ví dụ 'rong kinh' và 'ra nhiều kinh' là hai nút).",
          "- RE chỉ xét cặp trong cùng một câu; không xử lý đồng tham chiếu."]
    return "\n".join(L) + "\n"


def args_source(a):
    return f"`{a.from_results}`" if a.from_results else (f"`{a.texts}`" if a.texts else f"VietMed-NER split `{a.split}`")


def main():
    ap = argparse.ArgumentParser()
    src = ap.add_mutually_exclusive_group(required=True)
    src.add_argument("--split", choices=["train", "validation", "test"])
    src.add_argument("--texts")
    src.add_argument("--from-results")
    ap.add_argument("--entities", choices=["model", "gold"], default="model")
    ap.add_argument("--re-model", default=str(DEFAULT_RE_MODEL),
                    help="thư mục mô hình ViHealthBERT (có re_config.json) hoặc file .joblib TF-IDF")
    ap.add_argument("--rules-only", action="store_true")
    ap.add_argument("--re-mode", choices=["union", "fallback"], default="fallback",
                    help="fallback (mặc định): luật chỉ cho quan hệ mô hình không hỗ trợ, tức mô hình đứng một mình; "
                         "union: dương nếu mô hình hoặc luật nói dương (thấp hơn trên test_v2)")
    ap.add_argument("--rerun-re", action="store_true",
                    help="với --from-results: giữ thực thể đã lưu, chạy lại RE (ví dụ sau khi đổi mô hình RE)")
    ap.add_argument("--limit", type=int, help="chỉ xử lý N câu đầu (thử nhanh)")
    ap.add_argument("--min-count", type=int, default=1, help="ngưỡng số lần xuất hiện mặc định trong kg.html")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    if a.entities == "gold" and a.texts:
        ap.error("--entities gold cần --split (văn bản tự do không có nhãn gold)")
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)

    kg = KnowledgeGraph()
    meta = {"model_relations": [], "rule_relations": []}
    if a.from_results:
        re_pipe = make_re(a) if a.rerun_re else None
        rows = [json.loads(l) for l in Path(a.from_results).read_text(encoding="utf-8").splitlines() if l.strip()]
        fh = open(out / "results.jsonl", "w", encoding="utf-8") if a.rerun_re else None
        for r in rows:
            result = r["result"]
            if re_pipe is not None:
                ents = [{k: v for k, v in e.items() if k != "re_excluded"} for e in result["entities"]]
                result = re_pipe.from_ner_result({"text": result["text"], "entities": ents})
                r = {"id": r["id"], "extractor": re_pipe.extractor.metadata, "result": result}
                fh.write(json.dumps(r, ensure_ascii=False, default=str) + "\n")
            kg.add_document(result, doc_id=r["id"])
            meta = r.get("extractor", meta)
        if fh:
            fh.close()
    else:
        run, meta = make_runner(a)
        with open(out / "results.jsonl", "w", encoding="utf-8") as fh:
            for n, (doc_id, text, gold) in enumerate(iter_texts(a)):
                if a.limit and n >= a.limit:
                    break
                result = run(text, gold)
                kg.add_document(result, doc_id=doc_id)
                fh.write(json.dumps({"id": doc_id, "extractor": meta, "result": result},
                                    ensure_ascii=False, default=str) + "\n")
                if (n + 1) % 200 == 0:
                    print(f"  {n + 1} câu, {len(kg.nodes)} nút, {len(kg.edges)} cạnh", flush=True)
    kg.save(out)
    write_html(kg, out / "kg.html", min_count=a.min_count)
    md = stats_md(kg, meta, a)
    (out / "stats.md").write_text(md, encoding="utf-8")
    print(md)


if __name__ == "__main__":
    main()

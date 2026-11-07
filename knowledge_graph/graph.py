"""Aggregate per-document NER/RE results into a merged knowledge graph."""
import csv
import json
from collections import Counter
from pathlib import Path

from normalization.icd10 import normalize_vietnamese_text

ENTITY_TYPES = ("CONDITION", "DRUG", "BODY_PART", "TEST", "PROCEDURE", "DOSAGE")
MAX_EXAMPLES = 3
# CONDITION mentions that name no specific disease. Taken from the most frequent CONDITION
# forms of the VietMed-NER train split; RE's own generic list covers only DRUG/PROCEDURE/TEST.
GENERIC_CONDITIONS = frozenset(normalize_vietnamese_text(w) for w in (
    "bị", "bệnh", "bị bệnh", "mắc bệnh", "bệnh lý", "bệnh lý nền", "bệnh nền", "bệnh lý thông thường",
    "triệu chứng", "biến chứng", "di chứng", "hội chứng", "rối loạn", "viêm", "tổn thương", "mãn tính",
    "tái phát", "tử vong", "lây nhiễm", "lây lan", "lây truyền", "di truyền", "quan hệ", "bẩm sinh", "chậm",
    "mầm bệnh", "vi khuẩn", "virus", "ký sinh", "chủng", "đại dịch",
))


def is_generic_condition(entity):
    text = entity.get("surface_text") or entity.get("text") or ""
    return entity.get("label") == "CONDITION" and normalize_vietnamese_text(text) in GENERIC_CONDITIONS


def node_key(entity):
    """Merge key: the standard code when normalization made a decision, else type + text.

    'tiểu đường' and 'đái tháo đường' both normalized to E14 become one node 'ICD-10:E14';
    an unnormalized 'đau dữ dội' stays 'CONDITION:đau dữ dội'.
    """
    norm = entity.get("normalized")
    if norm and norm.get("code"):
        return f"{norm['ontology']}:{norm['code']}"
    text = entity.get("surface_text") or entity.get("text") or ""
    return f"{entity['label']}:{normalize_vietnamese_text(text)}"


class KnowledgeGraph:
    def __init__(self):
        self.nodes = {}
        self.edges = {}
        self.documents = 0

    # ------------------------------------------------------------------ build
    def add_document(self, result, doc_id=None, include_isolated=True, skip_generic=True):
        """Add one MedicalREPipeline result ({text, entities, relations}).

        Entities excluded from RE as generic ('thuốc', 'điều trị') are not added, nor (with
        skip_generic) generic conditions such as 'bị bệnh' or 'triệu chứng', with their edges.
        include_isolated=False keeps only entities that take part in a relation.
        """
        doc_id = doc_id if doc_id is not None else self.documents
        self.documents += 1
        ents = {e["id"]: e for e in result["entities"]
                if not e.get("re_excluded") and not (skip_generic and is_generic_condition(e))}
        in_relation = {r[s] for r in result.get("relations", []) for s in ("head", "tail")}
        keys = {}
        for eid, e in ents.items():
            if not include_isolated and eid not in in_relation:
                continue
            keys[eid] = self._add_node(e, doc_id)
        for r in result.get("relations", []):
            if r["head"] in keys and r["tail"] in keys:
                self._add_edge(keys[r["head"]], r, keys[r["tail"]], result["text"], doc_id)

    def _add_node(self, e, doc_id):
        key = node_key(e)
        norm = e.get("normalized")
        node = self.nodes.get(key)
        if node is None:
            node = self.nodes[key] = {
                "key": key, "type": e["label"],
                "name": norm["label_standard"] if norm else (e.get("surface_text") or e.get("text")),
                "ontology": norm["ontology"] if norm else None, "code": norm["code"] if norm else None,
                "suggested_code": None, "mentions": 0, "surfaces": Counter(), "documents": set(),
            }
        node["mentions"] += 1
        node["surfaces"][e.get("surface_text") or e.get("text")] += 1
        node["documents"].add(doc_id)
        if not norm and node["suggested_code"] is None:
            cands = e.get("candidates") or []
            if cands:
                node["suggested_code"] = f"{cands[0]['code']} {cands[0]['label_standard']}"
        return key

    def _add_edge(self, head, r, tail, text, doc_id):
        key = (head, r["label"], tail)
        edge = self.edges.get(key)
        if edge is None:
            edge = self.edges[key] = {"head": head, "relation": r["label"], "tail": tail, "count": 0,
                                      "sources": Counter(), "scores": [], "documents": set(), "examples": []}
        edge["count"] += 1
        edge["sources"][r.get("source", "model")] += 1
        if r.get("score") is not None:
            edge["scores"].append(float(r["score"]))
        edge["documents"].add(doc_id)
        if len(edge["examples"]) < MAX_EXAMPLES and text not in edge["examples"]:
            edge["examples"].append(text)

    # ------------------------------------------------------------------ query
    def neighbors(self, key, relation=None):
        """Edges touching `key` (either direction), most frequent first."""
        out = [e for e in self.edges.values()
               if key in (e["head"], e["tail"]) and (relation is None or e["relation"] == relation)]
        return sorted(out, key=lambda e: -e["count"])

    def find(self, text):
        """Nodes whose name, code or any surface form contains `text` (case-insensitive)."""
        q = normalize_vietnamese_text(text)
        return [n for n in self.nodes.values()
                if q in normalize_vietnamese_text(n["name"] or "") or q == (n["code"] or "").lower()
                or any(q in normalize_vietnamese_text(s) for s in n["surfaces"])]

    def stats(self):
        return {
            "documents": self.documents, "nodes": len(self.nodes), "edges": len(self.edges),
            "edge_mentions": sum(e["count"] for e in self.edges.values()),
            "nodes_by_type": dict(Counter(n["type"] for n in self.nodes.values())),
            "normalized_nodes": sum(1 for n in self.nodes.values() if n["code"]),
            "edges_by_relation": dict(Counter(e["relation"] for e in self.edges.values())),
            "edge_mentions_by_source": dict(sum((e["sources"] for e in self.edges.values()), Counter())),
            "isolated_nodes": len(set(self.nodes) - {k for e in self.edges.values() for k in (e["head"], e["tail"])}),
        }

    # ------------------------------------------------------------------ export
    def _node_out(self, n):
        return {**n, "surfaces": dict(n["surfaces"].most_common()), "documents": len(n["documents"])}

    def _edge_out(self, e):
        scores = e["scores"]
        return {"head": e["head"], "relation": e["relation"], "tail": e["tail"], "count": e["count"],
                "documents": len(e["documents"]), "sources": dict(e["sources"]),
                "mean_score": sum(scores) / len(scores) if scores else None, "examples": e["examples"]}

    def to_dict(self):
        return {"stats": self.stats(),
                "nodes": [self._node_out(n) for n in sorted(self.nodes.values(), key=lambda n: -n["mentions"])],
                "edges": [self._edge_out(e) for e in sorted(self.edges.values(), key=lambda e: -e["count"])]}

    def to_networkx(self):
        import networkx as nx
        g = nx.MultiDiGraph()
        for n in self.nodes.values():
            out = self._node_out(n)
            g.add_node(n["key"], **{k: v for k, v in out.items() if k not in ("key", "surfaces") and v is not None},
                       surfaces="; ".join(out["surfaces"]))
        for e in self.edges.values():
            out = self._edge_out(e)
            g.add_edge(e["head"], e["tail"], key=e["relation"], relation=e["relation"], count=out["count"],
                       documents=out["documents"], sources=json.dumps(out["sources"]),
                       mean_score=out["mean_score"] if out["mean_score"] is not None else -1.0)
        return g

    def save(self, out_dir):
        """Write kg.json, triples.csv, nodes.csv and kg.graphml into out_dir."""
        import networkx as nx
        out = Path(out_dir)
        out.mkdir(parents=True, exist_ok=True)
        data = self.to_dict()
        (out / "kg.json").write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        names = {n["key"]: n["name"] for n in data["nodes"]}
        with open(out / "triples.csv", "w", encoding="utf-8-sig", newline="") as fh:
            w = csv.writer(fh)
            w.writerow(["head_key", "head_name", "relation", "tail_key", "tail_name", "count", "documents",
                        "sources", "mean_score", "example"])
            for e in data["edges"]:
                w.writerow([e["head"], names[e["head"]], e["relation"], e["tail"], names[e["tail"]], e["count"],
                            e["documents"], json.dumps(e["sources"]),
                            "" if e["mean_score"] is None else f"{e['mean_score']:.3f}",
                            e["examples"][0] if e["examples"] else ""])
        with open(out / "nodes.csv", "w", encoding="utf-8-sig", newline="") as fh:
            w = csv.writer(fh)
            w.writerow(["key", "type", "name", "ontology", "code", "suggested_code", "mentions", "documents", "surfaces"])
            for n in data["nodes"]:
                w.writerow([n["key"], n["type"], n["name"], n["ontology"] or "", n["code"] or "",
                            n["suggested_code"] or "", n["mentions"], n["documents"], "; ".join(n["surfaces"])])
        nx.write_graphml(self.to_networkx(), out / "kg.graphml")
        return data

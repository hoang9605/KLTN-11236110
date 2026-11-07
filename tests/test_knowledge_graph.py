"""Knowledge graph: node merging by code, edge aggregation, generic filtering, exports, hybrid RE."""
import json

import networkx as nx

from knowledge_graph import HybridRelationExtractor, KnowledgeGraph, node_key
from knowledge_graph.visualize import write_html


def ent(eid, label, text, start, code=None, onto="ICD-10", name=None):
    return {"id": eid, "label": label, "surface_text": text, "text": text, "start": start,
            "end": start + len(text),
            "normalized": {"ontology": onto, "code": code, "label_standard": name or text,
                           "match_method": "synonym", "match_score": 1.0} if code else None}


DOC1 = {"text": "Bệnh nhân tiểu đường, uống metformin.",
        "entities": [ent("E1", "CONDITION", "tiểu đường", 10, "E14", name="Bệnh đái tháo đường"),
                     ent("E2", "DRUG", "metformin", 27, "6809", onto="RxNorm")],
        "relations": [{"head": "E1", "tail": "E2", "label": "treated_by", "score": 1.0, "source": "rule"}]}
DOC2 = {"text": "Người bị đái tháo đường dùng metformin.",
        "entities": [ent("E1", "CONDITION", "đái tháo đường", 9, "E14", name="Bệnh đái tháo đường"),
                     ent("E2", "DRUG", "metformin", 29, "6809", onto="RxNorm"),
                     ent("E3", "CONDITION", "bị bệnh", 0)],
        "relations": [{"head": "E1", "tail": "E2", "label": "treated_by", "score": 0.8, "source": "model"}]}


def build():
    kg = KnowledgeGraph()
    kg.add_document(DOC1, doc_id="d1")
    kg.add_document(DOC2, doc_id="d2")
    return kg


def test_node_key_prefers_code():
    assert node_key(DOC1["entities"][0]) == "ICD-10:E14"
    assert node_key({"label": "CONDITION", "surface_text": "Đau  Dữ dội", "normalized": None}) == "CONDITION:đau dữ dội"


def test_synonyms_merge_and_edges_aggregate():
    kg = build()
    node = kg.nodes["ICD-10:E14"]
    assert node["mentions"] == 2 and set(node["surfaces"]) == {"tiểu đường", "đái tháo đường"}
    edge = kg.edges[("ICD-10:E14", "treated_by", "RxNorm:6809")]
    assert edge["count"] == 2 and dict(edge["sources"]) == {"rule": 1, "model": 1}
    assert len(edge["examples"]) == 2
    assert kg.neighbors("RxNorm:6809")[0]["relation"] == "treated_by"
    assert [n["key"] for n in kg.find("tiểu đường")] == ["ICD-10:E14"]


def test_generic_condition_skipped():
    kg = build()
    assert "CONDITION:bị bệnh" not in kg.nodes
    kg2 = KnowledgeGraph()
    kg2.add_document(DOC2, skip_generic=False)
    assert "CONDITION:bị bệnh" in kg2.nodes


def test_stats_and_exports(tmp_path):
    kg = build()
    s = kg.stats()
    assert s["nodes"] == 2 and s["edges"] == 1 and s["edge_mentions"] == 2 and s["isolated_nodes"] == 0
    data = kg.save(tmp_path)
    assert json.loads((tmp_path / "kg.json").read_text(encoding="utf-8"))["stats"] == data["stats"]
    assert "treated_by" in (tmp_path / "triples.csv").read_text(encoding="utf-8-sig")
    g = nx.read_graphml(tmp_path / "kg.graphml")
    assert g.number_of_nodes() == 2 and g.number_of_edges() == 1
    html = write_html(kg, tmp_path / "kg.html").read_text(encoding="utf-8")
    assert "vis-network@9.1.9" in html and "ICD-10:E14" in html and "</script>" in html


class _FakeModel:
    supported_relations = ["located_at"]
    metadata = {"label_source": "human_verified"}

    def predict(self, text, entities):
        return [{"head": "E1", "tail": "E2", "allowed_relation": "treated_by", "label": None, "score": None,
                 "status": "unsupported"}]


class _FakeRules:
    supported_relations = ["has_dosage", "located_at", "treated_by"]

    def predict(self, text, entities):
        return [{"head": "E1", "tail": "E2", "allowed_relation": "treated_by", "label": "treated_by",
                 "score": 1.0, "status": "predicted"}]


def test_hybrid_fills_unsupported_with_rules():
    h = HybridRelationExtractor(_FakeModel(), rules=_FakeRules())
    out = h.predict("x", [])
    assert out[0]["label"] == "treated_by" and out[0]["source"] == "rule"
    assert h.metadata["rule_relations"] == ["has_dosage", "treated_by"]
    assert h.metadata["model_relations"] == ["located_at"]


class _NegModel:
    supported_relations = ["located_at"]
    metadata = {"label_source": "AI_provisional"}

    def predict(self, text, entities):
        return [{"head": "E1", "tail": "E2", "allowed_relation": "located_at", "label": "NO_RELATION",
                 "score": 0.2, "status": "predicted"}]


class _PosRules:
    supported_relations = ["located_at"]

    def predict(self, text, entities):
        return [{"head": "E1", "tail": "E2", "allowed_relation": "located_at", "label": "located_at",
                 "score": 1.0, "status": "predicted"}]


def test_union_takes_rule_positive_fallback_does_not():
    union = HybridRelationExtractor(_NegModel(), rules=_PosRules()).predict("x", [])[0]
    assert union["label"] == "located_at" and union["source"] == "rule"
    fallback = HybridRelationExtractor(_NegModel(), rules=_PosRules(), mode="fallback").predict("x", [])[0]
    assert fallback["label"] == "NO_RELATION" and fallback["source"] == "model"


def test_invalid_mode():
    import pytest
    with pytest.raises(ValueError):
        HybridRelationExtractor(None, mode="maybe")

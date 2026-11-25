"""Đồ thị tri thức trong bộ nhớ, dựng từ mọi văn bản trong CSDL và cập nhật sau mỗi lần phân tích."""
import csv
import io
import threading

from knowledge_graph import KnowledgeGraph


class KGService:
    def __init__(self, db):
        self.db = db
        self.lock = threading.RLock()
        self.kg = KnowledgeGraph()

    def rebuild(self):
        kg = KnowledgeGraph()
        for doc_id, result in self.db.iter_results():
            kg.add_document(result, doc_id=doc_id)
        with self.lock:
            self.kg = kg
        return kg.stats()

    def add(self, doc_id, result):
        with self.lock:
            self.kg.add_document(result, doc_id=doc_id)

    def stats(self):
        with self.lock:
            return self.kg.stats()

    def subgraph(self, limit=200, min_count=1, relation=None, node_type=None, center=None):
        """Các cạnh hay gặp nhất (lọc theo quan hệ / loại nút / một nút trung tâm) cùng các nút của chúng."""
        with self.lock:
            kg = self.kg
            edges = [e for e in kg.edges.values() if e["count"] >= min_count
                     and (relation is None or e["relation"] == relation)
                     and (center is None or center in (e["head"], e["tail"]))
                     and (node_type is None or node_type in (kg.nodes[e["head"]]["type"], kg.nodes[e["tail"]]["type"]))]
            edges.sort(key=lambda e: (-e["count"], e["head"], e["tail"]))
            edges = edges[:limit]
            keys = {k for e in edges for k in (e["head"], e["tail"])}
            if center in kg.nodes:
                keys.add(center)
            nodes = sorted((kg._node_out(kg.nodes[k]) for k in keys), key=lambda n: -n["mentions"])
            return {"stats": kg.stats(), "nodes": nodes, "edges": [kg._edge_out(e) for e in edges]}

    def search(self, q, limit=30):
        with self.lock:
            found = sorted(self.kg.find(q), key=lambda n: -n["mentions"])[:limit]
            return [self.kg._node_out(n) for n in found]

    def node(self, key):
        with self.lock:
            n = self.kg.nodes.get(key)
            if n is None:
                return None
            names = {k: v["name"] for k, v in self.kg.nodes.items()}
            edges = [{**self.kg._edge_out(e), "head_name": names[e["head"]], "tail_name": names[e["tail"]]}
                     for e in self.kg.neighbors(key)]
            return {"node": self.kg._node_out(n), "edges": edges}

    def export_json(self):
        with self.lock:
            return self.kg.to_dict()

    def export_triples_csv(self):
        data = self.export_json()
        names = {n["key"]: n["name"] for n in data["nodes"]}
        buf = io.StringIO()
        w = csv.writer(buf)
        w.writerow(["head_key", "head_name", "relation", "tail_key", "tail_name", "count", "documents", "mean_score"])
        for e in data["edges"]:
            w.writerow([e["head"], names[e["head"]], e["relation"], e["tail"], names[e["tail"]], e["count"],
                        e["documents"], "" if e["mean_score"] is None else f"{e['mean_score']:.3f}"])
        return "﻿" + buf.getvalue()

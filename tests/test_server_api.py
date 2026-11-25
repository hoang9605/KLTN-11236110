"""API của dịch vụ triển khai (server/), chạy với pipeline giả và SQLite tạm (không cần trọng số mô hình)."""
import json
from dataclasses import replace

import numpy as np
import pytest
from fastapi.testclient import TestClient

from server.config import Settings
from server.main import create_app


def fake_result(text):
    i = text.find("đau đầu")
    j = text.find("Paracetamol")
    ents = []
    if i >= 0:
        ents.append({"id": "E1", "surface_text": "đau đầu", "text": "đau đầu", "label": "CONDITION", "start": i,
                     "end": i + 7, "confidence": np.float32(0.9),
                     "normalized": {"ontology": "ICD-10", "code": "R51", "label_standard": "Đau đầu",
                                    "match_method": "synonym", "match_score": 1.0}})
    if j >= 0:
        ents.append({"id": "E2", "surface_text": "Paracetamol", "text": "Paracetamol", "label": "DRUG", "start": j,
                     "end": j + 11, "confidence": 0.95, "normalized": None})
    rels = [{"head": "E1", "tail": "E2", "label": "treated_by", "score": 0.8, "source": "model",
             "allowed_relation": "treated_by", "status": "predicted"}] if len(ents) == 2 else []
    return {"text": text, "entities": ents, "relations": rels, "relation_candidates": rels, "score": float("nan")}


class FakeExtractor:
    supported_relations = ["treated_by"]
    metadata = {"label_source": "fake"}


class FakePipe:
    extractor = FakeExtractor()

    def __init__(self):
        self.calls = []

    def predict(self, text, normalize=False):
        self.calls.append((text, normalize))
        return fake_result(text)


@pytest.fixture
def make_client(tmp_path):
    def make(factory=FakePipe, **kw):
        s = replace(Settings(), database_url=f"sqlite:///{(tmp_path / 'db.sqlite').as_posix()}", **kw)
        return TestClient(create_app(s, pipeline_factory=factory, load_in_background=False))
    return make


def test_analyze_saves_document_and_updates_graph(make_client):
    pipe = FakePipe()
    with make_client(lambda: pipe) as c:
        h = c.get("/api/health").json()
        assert h["status"] == "ready" and h["database"] is True
        r = c.post("/api/analyze", json={"text": "  Bệnh nhân đau đầu, uống Paracetamol.  "})
        assert r.status_code == 200
        body = r.json()
        assert pipe.calls == [("Bệnh nhân đau đầu, uống Paracetamol.", True)]
        assert body["entities"][0]["confidence"] == pytest.approx(0.9)  # numpy -> float
        assert body["score"] is None  # NaN -> null
        assert body["document_id"] == 1
        docs = c.get("/api/documents").json()
        assert docs["total"] == 1 and docs["items"][0]["n_relations"] == 1
        assert c.get("/api/documents/1").json()["result"]["relations"][0]["label"] == "treated_by"
        g = c.get("/api/kg").json()
        assert g["stats"]["edges"] == 1
        assert {n["key"] for n in g["nodes"]} == {"ICD-10:R51", "DRUG:paracetamol"}
        assert c.get("/api/kg/search", params={"q": "đau"}).json()[0]["key"] == "ICD-10:R51"
        node = c.get("/api/kg/node", params={"key": "ICD-10:R51"}).json()
        assert node["edges"][0]["tail_name"] == "Paracetamol"
        assert "treated_by" in c.get("/api/kg/export", params={"format": "csv"}).text


def test_save_false_does_not_store(make_client):
    with make_client() as c:
        assert c.post("/api/analyze", json={"text": "đau đầu", "save": False}).json()["document_id"] is None
        assert c.get("/api/documents").json()["total"] == 0


def test_batch_and_validation(make_client):
    with make_client(max_batch=3) as c:
        r = c.post("/api/analyze/batch", json={"texts": ["đau đầu", "  ", "Paracetamol"]})
        assert r.status_code == 200 and len(r.json()["results"]) == 2
        assert c.post("/api/analyze/batch", json={"texts": ["a"] * 4}).status_code == 422
        assert c.post("/api/analyze", json={"text": ""}).status_code == 422
        assert c.post("/api/analyze", json={"text": "   "}).status_code == 422
        assert c.post("/api/analyze", json={"text": "a" * 2001}).status_code == 422


def test_model_load_error_is_reported(make_client):
    def broken():
        raise FileNotFoundError("thiếu model_seed42.safetensors")
    with make_client(broken) as c:
        h = c.get("/api/health").json()
        assert h["status"] == "error" and "safetensors" in h["error"]
        assert c.post("/api/analyze", json={"text": "đau đầu"}).status_code == 503
        assert c.get("/api/kg").status_code == 200  # dữ liệu đã lưu vẫn xem được


def test_seed_file_loaded_when_db_empty(make_client, tmp_path):
    seed = tmp_path / "results.jsonl"
    rows = [{"id": f"test-{i}", "result": fake_result("Bệnh nhân đau đầu, uống Paracetamol.")} for i in range(3)]
    seed.write_text("\n".join(json.dumps(r, ensure_ascii=False, default=float) for r in rows), encoding="utf-8")
    with make_client(seed_file=str(seed), load_models=False) as c:
        assert c.get("/api/health").json()["status"] == "disabled"
        docs = c.get("/api/documents", params={"source": "seed"}).json()
        assert docs["total"] == 3
        edge = c.get("/api/kg").json()["edges"][0]
        assert edge["count"] == 3 and edge["documents"] == 3
        doc_id = docs["items"][0]["id"]
        assert c.delete(f"/api/documents/{doc_id}").status_code == 200
        assert c.get(f"/api/documents/{doc_id}").status_code == 404

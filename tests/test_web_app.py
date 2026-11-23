"""API của giao diện demo, chạy với pipeline giả (không cần trọng số mô hình)."""
import numpy as np
from fastapi.testclient import TestClient

from web.app import MAX_CHARS, create_app


class FakePipe:
    def __init__(self):
        self.calls = []

    def predict(self, text, normalize=False):
        self.calls.append((text, normalize))
        return {"text": text, "entities": [{"id": "E1", "text": "đau", "label": "CONDITION", "start": 0, "end": 3,
                                            "confidence": np.float32(0.5), "normalized": None}],
                "relations": [], "score": float("nan")}


def client(factory):
    return TestClient(create_app(factory, load_in_background=False))


def test_analyze_returns_pipeline_result_as_plain_json():
    pipe = FakePipe()
    c = client(lambda: pipe)
    assert c.get("/api/health").json()["status"] == "ready"
    r = c.post("/api/analyze", json={"text": "  đau bụng  ", "normalize": False})
    assert r.status_code == 200
    body = r.json()
    assert pipe.calls == [("đau bụng", False)]  # cắt khoảng trắng, chuyển cờ chuẩn hóa
    assert body["entities"][0]["confidence"] == 0.5  # numpy -> float
    assert body["score"] is None  # NaN -> null
    assert isinstance(body["elapsed_ms"], int)


def test_analyze_rejects_empty_and_too_long_text():
    c = client(FakePipe)
    assert c.post("/api/analyze", json={"text": ""}).status_code == 422
    assert c.post("/api/analyze", json={"text": "   "}).status_code == 422
    assert c.post("/api/analyze", json={"text": "a" * (MAX_CHARS + 1)}).status_code == 422


def test_model_load_error_is_reported_not_crashing():
    def broken():
        raise FileNotFoundError("thiếu model_seed42.safetensors")
    c = client(broken)
    h = c.get("/api/health").json()
    assert h["status"] == "error" and "safetensors" in h["error"]
    assert c.post("/api/analyze", json={"text": "đau bụng"}).status_code == 503


def test_static_ui_is_served():
    r = client(FakePipe).get("/")
    assert r.status_code == 200 and "Phân tích" in r.text

r"""Backend cho giao diện demo: phục vụ web/ và API phân tích văn bản bằng pipeline đầy đủ
(NER ViHealthBERT -> chuẩn hóa ICD-10/RxNorm -> RE ViHealthBERT; luật chỉ dùng cho quan hệ mô hình không hỗ trợ).

    .venv\Scripts\python.exe -X utf8 web/app.py            # http://127.0.0.1:8770
    .venv\Scripts\python.exe -X utf8 web/app.py --port 8000

API:
    GET  /api/health   -> {"status": "loading" | "ready" | "error", ...}
    POST /api/analyze  {"text": "...", "normalize": true} -> kết quả như MedicalREPipeline.predict, thêm elapsed_ms

Mô hình nạp ở luồng nền khi khởi động (khoảng 10-20 giây); trong lúc đó /api/analyze trả 503.
Các yêu cầu được xử lý lần lượt (một khóa), vì pipeline không an toàn khi chạy song song.
"""
import argparse
import json
import math
import os
import sys
import threading
import time
from pathlib import Path

os.environ.setdefault("KMP_DUPLICATE_LIB_OK", "TRUE")
WEB = Path(__file__).resolve().parent
ROOT = WEB.parent
sys.path.insert(0, str(ROOT))

from fastapi import FastAPI, HTTPException  # noqa: E402
from fastapi.responses import JSONResponse  # noqa: E402
from fastapi.staticfiles import StaticFiles  # noqa: E402
from pydantic import BaseModel, Field  # noqa: E402

MAX_CHARS = 2000
RE_MODEL = ROOT / "Model/vihealthbert-re-vietmed-811"


class AnalyzeRequest(BaseModel):
    text: str = Field(min_length=1, max_length=MAX_CHARS)
    normalize: bool = True


def default_pipeline():
    from knowledge_graph import HybridRelationExtractor
    from ner.pipeline import MedicalNERPipeline
    from relation_extraction.bert_model import load_extractor
    from relation_extraction.pipeline import MedicalREPipeline
    # fallback: luật chỉ cho quan hệ mô hình không hỗ trợ; mô hình hỗ trợ cả năm quan hệ nên thực chất là
    # mô hình đứng một mình, như trong báo cáo và đồ thị (union thấp hơn trên test_v2: 0,682 so với 0,693)
    return MedicalREPipeline(HybridRelationExtractor(load_extractor(str(RE_MODEL)), mode="fallback"),
                             ner=MedicalNERPipeline(enable_normalization=True))


def jsonable(obj):
    """numpy / float NaN -> kiểu JSON chuẩn."""
    def conv(o):
        if hasattr(o, "item"):
            return o.item()
        return str(o)
    data = json.loads(json.dumps(obj, ensure_ascii=False, default=conv))

    def clean(x):
        if isinstance(x, float) and (math.isnan(x) or math.isinf(x)):
            return None
        if isinstance(x, dict):
            return {k: clean(v) for k, v in x.items()}
        if isinstance(x, list):
            return [clean(v) for v in x]
        return x
    return clean(data)


def create_app(pipeline_factory=default_pipeline, load_in_background=True):
    app = FastAPI(title="Trích xuất thông tin y tế tiếng Việt", docs_url="/api/docs", openapi_url="/api/openapi.json")
    state = {"status": "loading", "pipe": None, "error": None, "load_seconds": None}
    lock = threading.Lock()

    def load():
        t0 = time.time()
        try:
            state["pipe"] = pipeline_factory()
            state["status"] = "ready"
        except Exception as e:  # mô hình thiếu trọng số, lỗi nạp...
            state["status"], state["error"] = "error", f"{type(e).__name__}: {e}"
        state["load_seconds"] = round(time.time() - t0, 1)

    if load_in_background:
        threading.Thread(target=load, daemon=True).start()
    else:
        load()

    @app.get("/api/health")
    def health():
        return {"status": state["status"], "error": state["error"], "load_seconds": state["load_seconds"],
                "max_chars": MAX_CHARS}

    @app.post("/api/analyze")
    def analyze(req: AnalyzeRequest):
        if state["status"] != "ready":
            raise HTTPException(503, state["error"] or "Mô hình đang được nạp, thử lại sau vài giây.")
        text = req.text.strip()
        if not text:
            raise HTTPException(422, "Văn bản rỗng.")
        with lock:
            t0 = time.time()
            result = state["pipe"].predict(text, normalize=req.normalize)
            result["elapsed_ms"] = round(1000 * (time.time() - t0))
        return JSONResponse(jsonable(result))

    app.mount("/", StaticFiles(directory=str(WEB), html=True), name="web")
    return app


if __name__ == "__main__":
    import uvicorn
    ap = argparse.ArgumentParser()
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--port", type=int, default=8770)
    a = ap.parse_args()
    uvicorn.run(create_app(), host=a.host, port=a.port)

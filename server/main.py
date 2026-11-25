r"""API và giao diện web: văn bản lâm sàng tiếng Việt -> NER -> chuẩn hóa ICD-10/RxNorm -> RE -> đồ thị tri thức.
Một tiến trình phục vụ cả API (/api/...) lẫn giao diện React đã build (STATIC_DIR), dữ liệu lưu trong SQLite.

    uvicorn server.main:app --host 0.0.0.0 --port 8000      # trong container
    .venv\Scripts\python.exe -X utf8 -m uvicorn server.main:app --port 8000   # cục bộ

Tài liệu OpenAPI: /api/docs
"""
import json
import logging
import threading
import time
from contextlib import asynccontextmanager
from pathlib import Path
from typing import List, Optional

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse, Response
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from . import __version__
from .config import ROOT, get_settings
from .db import Database
from .engine import Engine, build_pipeline
from .kg_service import KGService
from .seed import seed_if_empty

log = logging.getLogger("server")
ENTITY_TYPES = ["CONDITION", "DRUG", "BODY_PART", "TEST", "PROCEDURE", "DOSAGE"]
RELATIONS = {"located_at": ["CONDITION", "BODY_PART"], "treated_by": ["CONDITION", "DRUG"],
             "treated_by_procedure": ["CONDITION", "PROCEDURE"], "diagnosed_by": ["CONDITION", "TEST"],
             "has_dosage": ["DRUG", "DOSAGE"]}


def create_app(settings=None, pipeline_factory=None, load_in_background=True):
    settings = settings or get_settings()
    db = Database(settings.database_url)
    kg = KGService(db)
    factory = pipeline_factory or (lambda: build_pipeline(settings))
    engine = Engine(factory)
    started = time.time()

    class AnalyzeRequest(BaseModel):
        text: str = Field(min_length=1, max_length=settings.max_chars)
        normalize: bool = True
        save: bool = True

    class BatchRequest(BaseModel):
        texts: List[str] = Field(min_length=1, max_length=settings.max_batch)
        normalize: bool = True
        save: bool = True

    def init_data():
        db.create_all()
        try:
            n = seed_if_empty(db, settings.seed_file)
            if n:
                log.info("seeded %d documents from %s", n, settings.seed_file)
        except Exception:
            log.exception("seeding failed")
        log.info("knowledge graph: %s", kg.rebuild())

    @asynccontextmanager
    async def lifespan(_app):
        init_data()
        if settings.load_models:
            engine.start(background=load_in_background)
        else:
            engine.status, engine.error = "disabled", "LOAD_MODELS=false: chỉ phục vụ dữ liệu đã lưu."
        yield

    app = FastAPI(title="Hệ thống trích xuất thông tin y tế tiếng Việt", version=__version__, lifespan=lifespan,
                  docs_url="/api/docs", openapi_url="/api/openapi.json", redoc_url=None)
    if settings.cors_origins:
        app.add_middleware(CORSMiddleware, allow_origins=list(settings.cors_origins), allow_methods=["*"],
                           allow_headers=["*"])
    app.state.engine, app.state.db, app.state.kg = engine, db, kg

    def require_ready():
        if not engine.ready:
            raise HTTPException(503, engine.error or "Mô hình đang được nạp, thử lại sau vài giây.")

    def run(text, normalize, save):
        text = text.strip()
        if not text:
            raise HTTPException(422, "Văn bản rỗng.")
        result, elapsed = engine.analyze(text, normalize)
        doc_id = None
        if save:
            doc = db.add(result, elapsed_ms=elapsed)
            doc_id = doc.id
            kg.add(doc_id, result)
        return {**result, "elapsed_ms": elapsed, "document_id": doc_id}

    # ------------------------------------------------------------------ hệ thống
    @app.get("/api/health", tags=["system"])
    def health():
        """Trạng thái mô hình (loading | ready | error | disabled) và CSDL. Dùng cho healthcheck."""
        return {"status": engine.status, "error": engine.error, "load_seconds": engine.load_seconds,
                "database": db.ping(), "version": __version__, "uptime_seconds": round(time.time() - started)}

    @app.get("/api/info", tags=["system"])
    def info():
        return {"version": __version__, "entity_types": ENTITY_TYPES, "relations": RELATIONS,
                "max_chars": settings.max_chars, "max_batch": settings.max_batch,
                "models": {"ner": settings.ner_model, "re": settings.re_model, "device": settings.device or "auto"},
                "pipeline": engine.metadata(), "requests_served": engine.requests,
                "documents": db.count(), "kg": kg.stats()}

    @app.get("/api/samples", tags=["system"])
    def samples():
        path = ROOT / "web" / "samples.json"
        if not path.exists():
            return []
        return [s["text"] for s in json.loads(path.read_text(encoding="utf-8"))]

    # ------------------------------------------------------------------ phân tích
    @app.post("/api/analyze", tags=["analyze"])
    def analyze(req: AnalyzeRequest):
        """Phân tích một đoạn văn bản; save=true lưu vào lịch sử và cập nhật đồ thị tri thức."""
        require_ready()
        return JSONResponse(run(req.text, req.normalize, req.save))

    @app.post("/api/analyze/batch", tags=["analyze"])
    def analyze_batch(req: BatchRequest):
        require_ready()
        too_long = [i for i, t in enumerate(req.texts) if len(t) > settings.max_chars]
        if too_long:
            raise HTTPException(422, f"Văn bản {too_long} dài quá {settings.max_chars} ký tự.")
        texts = [t for t in req.texts if t.strip()]
        if not texts:
            raise HTTPException(422, "Không có văn bản nào.")
        return JSONResponse({"results": [run(t, req.normalize, req.save) for t in texts]})

    # ------------------------------------------------------------------ lịch sử
    @app.get("/api/documents", tags=["documents"])
    def list_documents(limit: int = Query(20, ge=1, le=200), offset: int = Query(0, ge=0),
                       q: Optional[str] = None, source: Optional[str] = None):
        total, rows = db.list(limit=limit, offset=offset, q=q, source=source)
        return {"total": total, "items": [r.summary() for r in rows]}

    @app.get("/api/documents/{doc_id}", tags=["documents"])
    def get_document(doc_id: int):
        doc = db.get(doc_id)
        if doc is None:
            raise HTTPException(404, "Không tìm thấy văn bản.")
        return doc.full()

    @app.delete("/api/documents/{doc_id}", tags=["documents"])
    def delete_document(doc_id: int):
        if not db.delete(doc_id):
            raise HTTPException(404, "Không tìm thấy văn bản.")
        threading.Thread(target=kg.rebuild, daemon=True).start()  # gỡ đóng góp của văn bản khỏi đồ thị
        return {"deleted": doc_id}

    # ------------------------------------------------------------------ đồ thị tri thức
    @app.get("/api/kg", tags=["knowledge graph"])
    def kg_graph(limit: int = Query(150, ge=1, le=2000), min_count: int = Query(1, ge=1),
                 relation: Optional[str] = None, type: Optional[str] = None, center: Optional[str] = None):
        """Đồ thị con: các cạnh xuất hiện nhiều nhất cùng các nút của chúng."""
        return kg.subgraph(limit=limit, min_count=min_count, relation=relation, node_type=type, center=center)

    @app.get("/api/kg/stats", tags=["knowledge graph"])
    def kg_stats():
        return kg.stats()

    @app.get("/api/kg/search", tags=["knowledge graph"])
    def kg_search(q: str = Query(min_length=1), limit: int = Query(30, ge=1, le=200)):
        return kg.search(q, limit)

    @app.get("/api/kg/node", tags=["knowledge graph"])
    def kg_node(key: str):
        """Một nút (khóa dạng 'ICD-10:E14' hoặc 'CONDITION:đau đầu') và mọi cạnh nối với nó."""
        out = kg.node(key)
        if out is None:
            raise HTTPException(404, "Không có nút này.")
        return out

    @app.get("/api/kg/export", tags=["knowledge graph"])
    def kg_export(format: str = Query("json", pattern="^(json|csv)$")):
        if format == "csv":
            return Response(kg.export_triples_csv(), media_type="text/csv; charset=utf-8",
                            headers={"Content-Disposition": "attachment; filename=triples.csv"})
        return JSONResponse(kg.export_json(), headers={"Content-Disposition": "attachment; filename=kg.json"})

    @app.post("/api/kg/rebuild", tags=["knowledge graph"])
    def kg_rebuild():
        return kg.rebuild()

    static = Path(settings.static_dir)
    if (static / "index.html").exists():
        app.mount("/assets", StaticFiles(directory=static / "assets", check_dir=False), name="assets")

        @app.get("/{path:path}", include_in_schema=False)
        def spa(path: str):
            """Giao diện một trang: tệp tĩnh nếu có, còn lại trả index.html để React Router xử lý."""
            if path.startswith("api/"):
                raise HTTPException(404, "Không có điểm cuối này.")
            f = (static / path).resolve()
            if path and f.is_file() and static.resolve() in f.parents:
                return FileResponse(f)
            return FileResponse(static / "index.html")

    return app


logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
app = create_app()  # CSDL và mô hình chỉ được mở khi ứng dụng khởi động (lifespan)

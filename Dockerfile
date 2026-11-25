# MedKG bản demo: một container chạy FastAPI, phục vụ cả API lẫn giao diện React, dữ liệu lưu trong SQLite.
# Trọng số mô hình KHÔNG nằm trong image: gắn thư mục Model/ vào /models khi chạy (xem docker-compose.yml).

# --- build giao diện React ---
FROM node:22-alpine AS ui
WORKDIR /ui
COPY frontend/package.json frontend/package-lock.json ./
RUN npm ci --no-audit --no-fund
COPY frontend/tsconfig.json frontend/vite.config.ts frontend/index.html ./
COPY frontend/public ./public
COPY frontend/src ./src
RUN npm run build

# --- API + mô hình (PyTorch CPU) ---
FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONIOENCODING=utf-8 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    HF_HUB_OFFLINE=1 \
    TRANSFORMERS_OFFLINE=1 \
    MODEL_DIR=/models \
    DATABASE_URL=sqlite:////data/medkg.db \
    STATIC_DIR=/app/frontend/dist \
    SEED_FILE=/app/seed/results.jsonl
WORKDIR /app

RUN pip install torch==2.14.0 --index-url https://download.pytorch.org/whl/cpu
COPY server/requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

COPY ner ./ner
COPY normalization ./normalization
COPY relation_extraction ./relation_extraction
COPY knowledge_graph ./knowledge_graph
COPY ICD-10 ./ICD-10
COPY re_labels.json ./re_labels.json
COPY web/samples.json ./web/samples.json
COPY outputs/kg_test_2026-11-25/results.jsonl ./seed/results.jsonl
COPY server ./server
COPY --from=ui /ui/dist ./frontend/dist

RUN useradd --create-home --uid 1000 app \
    && mkdir -p /app/logs /models /data \
    && chown -R app:app /app/logs /app/normalization /data
USER app
VOLUME /data

EXPOSE 8000
HEALTHCHECK --interval=20s --timeout=5s --start-period=30s --retries=5 \
    CMD python -c "import urllib.request,sys; sys.exit(0 if urllib.request.urlopen('http://127.0.0.1:8000/api/health', timeout=4).status == 200 else 1)"
CMD ["uvicorn", "server.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]

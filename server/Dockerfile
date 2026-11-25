# Dịch vụ API: FastAPI + PyTorch CPU. Ngữ cảnh build là thư mục gốc của repo (xem deploy/docker-compose.yml).
# Trọng số mô hình KHÔNG nằm trong image: gắn thư mục Model/ vào /models khi chạy.
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONIOENCODING=utf-8 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    HF_HUB_OFFLINE=1 \
    TRANSFORMERS_OFFLINE=1 \
    MODEL_DIR=/models \
    SEED_FILE=/app/seed/results.jsonl

WORKDIR /app

RUN pip install torch==2.14.0 --index-url https://download.pytorch.org/whl/cpu
COPY server/requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

# chỉ mã suy luận và dữ liệu cần lúc chạy (danh sách cho phép ở .dockerignore)
COPY ner ./ner
COPY normalization ./normalization
COPY relation_extraction ./relation_extraction
COPY knowledge_graph ./knowledge_graph
COPY ICD-10 ./ICD-10
COPY re_labels.json ./re_labels.json
COPY web/samples.json ./web/samples.json
COPY outputs/kg_test_2026-11-25/results.jsonl ./seed/results.jsonl
COPY server ./server

RUN useradd --create-home --uid 1000 app \
    && mkdir -p /app/logs /models \
    && chown -R app:app /app/logs /app/normalization
USER app

EXPOSE 8000
HEALTHCHECK --interval=20s --timeout=5s --start-period=30s --retries=5 \
    CMD python -c "import urllib.request,sys; sys.exit(0 if urllib.request.urlopen('http://127.0.0.1:8000/api/health', timeout=4).status == 200 else 1)"

# một worker: mô hình (~2,5 GB RAM) nạp một lần, yêu cầu suy luận được xếp hàng tuần tự
CMD ["uvicorn", "server.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1", "--proxy-headers"]

# Triển khai hệ thống MedKG bằng Docker

MedKG đọc văn bản lâm sàng tiếng Việt và trích ra thông tin theo bốn bước: **NER** (ViHealthBERT) → **chuẩn hóa** (mã ICD-10 của Bộ Y tế, mã RxNorm) → **trích xuất quan hệ** (ViHealthBERT-RE, trung bình 3 seed) → **đồ thị tri thức**. Hệ thống có giao diện web, REST API và cơ sở dữ liệu lưu lịch sử phân tích.

## Kiến trúc

```
 Trình duyệt ──► web  (Nginx 1.27 + React 18/TypeScript/Vite, Cytoscape.js)   cổng 8080
                  │  /api/*  reverse proxy
                  ▼
                 api  (FastAPI + Uvicorn, Python 3.12, PyTorch 2.14 CPU, Transformers)
                  │   ├─ ner/                  NER ViHealthBERT + hậu xử lý
                  │   ├─ normalization/        ICD-10 (Excel BYT) · RxNorm (SQLite cache + RxNav API)
                  │   ├─ relation_extraction/  ViHealthBERT-RE 3 seed
                  │   └─ knowledge_graph/      đồ thị tri thức trong bộ nhớ
                  ▼
                 db   (PostgreSQL 16; bảng documents, kết quả dạng JSONB)
```

| Thành phần | Công nghệ | Vai trò |
|---|---|---|
| `web` | Nginx, React 18, TypeScript, Vite, React Router, Cytoscape.js | Giao diện 4 trang (Phân tích, Lịch sử, Đồ thị tri thức, Hệ thống), chuyển `/api` sang `api` |
| `api` | FastAPI, Uvicorn, SQLAlchemy 2, PyTorch CPU, Transformers | Nạp mô hình một lần, phục vụ suy luận, lưu kết quả, dựng đồ thị |
| `db` | PostgreSQL 16 | Lưu văn bản và kết quả, giữ qua các lần khởi động lại (volume `pgdata`) |

Mã nguồn: `server/` (API), `frontend/` (giao diện), `deploy/` (compose). Trọng số mô hình **không** nằm trong image mà được gắn vào lúc chạy (chỉ đọc) để image nhẹ (~1,5 GB thay vì ~4 GB) và đổi mô hình không cần build lại.

## Yêu cầu

- Docker Engine 24+ có Compose v2 (Docker Desktop trên Windows/macOS).
- RAM ≥ 6 GB cho container `api` (NER + 3 mô hình RE ≈ 2,5 GB khi chạy). Trên Docker Desktop: Settings → Resources → Memory ≥ 8 GB.
- Thư mục mô hình có:
  - `vihealthbert-ner-vietmed-v2-final/` (`model.safetensors`, `config.json`, `vocab.txt`, `bpe.codes`…)
  - `vihealthbert-re-vietmed-811/` (`model_seed42/43/44.safetensors`, `re_config.json`…)

## Chạy

```powershell
cd deploy
Copy-Item .env.example .env      # Linux: cp .env.example .env
# sửa .env: POSTGRES_PASSWORD, MODEL_DIR (trên máy dự án: ../Code/Model)
docker compose up -d --build
docker compose ps                 # đợi api "healthy"
docker compose logs -f api        # nạp mô hình khoảng 30-60 giây
```

Mở <http://localhost:8080>. Tài liệu API (Swagger): <http://localhost:8080/api/docs>.

Lần đầu khởi động, `api` tự nạp 3.496 câu test VietMed-NER đã phân tích sẵn (`outputs/kg_test_2026-11-25/results.jsonl`) vào CSDL để đồ thị tri thức có dữ liệu ngay. Muốn bỏ, đặt `SEED_FILE=` (để trống) trong `.env` trước lần chạy đầu.

Trong lúc mô hình đang nạp, giao diện báo "Đang nạp mô hình…" và `/api/analyze` trả 503. Lịch sử và đồ thị vẫn xem được.

## Cấu hình (`deploy/.env`)

| Biến | Mặc định | Ý nghĩa |
|---|---|---|
| `POSTGRES_PASSWORD` | (bắt buộc) | Mật khẩu CSDL |
| `MODEL_DIR` | `../Model` | Thư mục mô hình trên máy chủ, gắn vào `/models` |
| `NER_MODEL`, `RE_MODEL` | `vihealthbert-ner-vietmed-v2-final`, `vihealthbert-re-vietmed-811` | Tên thư mục con trong `MODEL_DIR` |
| `DEVICE` | `cpu` | `cpu` hoặc `cuda` (cần image và runtime GPU, xem dưới) |
| `TORCH_THREADS` | `4` | Số luồng CPU cho PyTorch |
| `API_MEMORY` | `6g` | Giới hạn RAM của container `api` |
| `LOAD_MODELS` | `true` | `false`: không nạp mô hình, chỉ xem lịch sử và đồ thị (máy yếu) |
| `SEED_FILE` | `/app/seed/results.jsonl` | Dữ liệu nạp sẵn khi CSDL trống |
| `WEB_PORT` | `8080` | Cổng công khai |

## REST API

| Phương thức | Đường dẫn | Mô tả |
|---|---|---|
| GET | `/api/health` | Trạng thái mô hình (`loading`/`ready`/`error`/`disabled`) và CSDL |
| GET | `/api/info` | Lược đồ thực thể/quan hệ, mô hình, thống kê |
| POST | `/api/analyze` | `{"text": "...", "normalize": true, "save": true}` → thực thể, mã chuẩn, quan hệ |
| POST | `/api/analyze/batch` | `{"texts": [...]}` (tối đa 20) |
| GET | `/api/documents?q=&source=&limit=&offset=` | Lịch sử phân tích |
| GET / DELETE | `/api/documents/{id}` | Xem / xóa một văn bản (đồ thị được dựng lại) |
| GET | `/api/kg?limit=&min_count=&relation=&type=&center=` | Đồ thị con để vẽ |
| GET | `/api/kg/search?q=` · `/api/kg/node?key=` | Tìm nút, xem lân cận |
| GET | `/api/kg/export?format=json\|csv` | Xuất toàn bộ đồ thị |

Ví dụ:

```powershell
Invoke-RestMethod -Method Post -Uri http://localhost:8080/api/analyze -ContentType "application/json; charset=utf-8" `
  -Body ([Text.Encoding]::UTF8.GetBytes('{"text":"Bệnh nhân tăng huyết áp, kê Aspirin 81mg mỗi ngày."}'))
```

## Vận hành

```powershell
docker compose ps
docker compose logs -f api
docker compose restart api                       # nạp lại mô hình (ví dụ sau khi đổi RE_MODEL)
docker compose exec api python -m server.seed /app/seed/results.jsonl --force   # nạp thêm dữ liệu
docker compose exec db pg_dump -U medkg medkg > backup.sql                        # sao lưu CSDL
docker compose down                              # dừng (giữ dữ liệu)
docker compose down -v                           # dừng và XÓA dữ liệu CSDL
```

Triển khai lên máy chủ khác: sao chép repo cùng thư mục mô hình (hoặc đẩy image lên registry với `TAG=1.0.0 docker compose build` rồi `docker compose push`), tạo `deploy/.env` và chạy `docker compose up -d`. Muốn có HTTPS thì đặt reverse proxy (Caddy, Traefik, Nginx + Let's Encrypt) trước cổng `WEB_PORT`.

**GPU (tùy chọn):** đổi dòng cài torch trong `server/Dockerfile` sang bản CUDA (`--index-url https://download.pytorch.org/whl/cu126`), đặt `DEVICE=cuda` và thêm vào service `api`: `deploy.resources.reservations.devices: [{driver: nvidia, count: 1, capabilities: [gpu]}]` (cần NVIDIA Container Toolkit).

## Phát triển không dùng Docker

```powershell
.venv\Scripts\python.exe -m pip install "sqlalchemy>=2.0"
.venv\Scripts\python.exe -X utf8 -m server.seed outputs/kg_test_2026-11-25/results.jsonl   # tùy chọn
.venv\Scripts\python.exe -X utf8 -m uvicorn server.main:app --port 8000                    # SQLite: outputs/server.db
cd frontend; npm install; npm run dev                                                       # http://localhost:5173
.venv\Scripts\python.exe -X utf8 -m pytest tests/test_server_api.py
```

## Giới hạn

- Suy luận chạy tuần tự trên một worker (pipeline không an toàn khi chạy song song); trên CPU mỗi câu mất khoảng 1–3 giây.
- Chuẩn hóa RxNorm gọi RxNav API (cần Internet) khi tên thuốc chưa có trong bộ đệm; không có mạng thì thuốc mới sẽ không được gán mã.
- Chưa có xác thực người dùng: chỉ nên mở trong mạng nội bộ hoặc đặt sau reverse proxy có đăng nhập.

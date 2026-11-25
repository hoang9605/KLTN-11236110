# Chạy hệ thống demo MedKG bằng Docker

MedKG đọc văn bản lâm sàng tiếng Việt và trích ra thông tin theo bốn bước: **NER** (ViHealthBERT), **gán mã** ICD-10 và RxNorm, **trích xuất quan hệ** (ViHealthBERT-RE, trung bình 3 seed) và **đồ thị tri thức**. Bản demo chạy trong **một container**: FastAPI phục vụ cả giao diện React lẫn API, dữ liệu lưu trong một tệp SQLite.

```
Trình duyệt ──HTTP :8080──► container medkg (FastAPI + PyTorch CPU)
                              ├─ giao diện web đã build (React, Vite, Cytoscape.js)
                              ├─ API /api/...
                              ├─ NER · gán mã ICD-10/RxNorm · RE · đồ thị tri thức
                              ├─ /data/medkg.db (SQLite, trên volume)
                              └─ /models (thư mục mô hình, gắn chỉ đọc)
```

## Yêu cầu

- Docker Desktop (Windows/macOS) hoặc Docker Engine có Compose v2.
- RAM trống khoảng 3 GB cho container (mô hình dùng khoảng 2 GB).
- Thư mục mô hình có `vihealthbert-ner-vietmed-v2-final/` và `vihealthbert-re-vietmed-811/` (kèm các tệp `.safetensors`).

## Chạy

Ở thư mục gốc của repo:

```powershell
$env:MODEL_DIR = "./Code/Model"     # chỉ cần trên máy dự án; mặc định là ./Model
docker compose up -d --build
```

Mở <http://localhost:8080>. Tài liệu API: <http://localhost:8080/api/docs>. Mô hình nạp khoảng 40 giây, trong lúc đó giao diện báo "Đang nạp mô hình…" nhưng lịch sử và đồ thị vẫn xem được. Lần chạy đầu, hệ thống tự nạp 3.496 câu test VietMed-NER đã phân tích sẵn để đồ thị có dữ liệu ngay.

Biến tùy chọn: `PORT` (mặc định 8080), `TORCH_THREADS` (mặc định 4), `MODEL_DIR`.

## API chính

| Phương thức | Đường dẫn | Mô tả |
|---|---|---|
| GET | `/api/health` | Trạng thái mô hình (`loading`/`ready`/`error`) |
| POST | `/api/analyze` | `{"text": "...", "normalize": true, "save": true}` → thực thể, mã chuẩn, quan hệ |
| GET | `/api/documents` | Lịch sử phân tích (`q`, `source`, `limit`, `offset`) |
| GET | `/api/kg` · `/api/kg/search?q=` · `/api/kg/node?key=` | Đồ thị tri thức |
| GET | `/api/kg/export?format=json\|csv` | Xuất đồ thị |

## Vận hành

```powershell
docker compose logs -f              # xem nhật ký
docker compose restart              # nạp lại mô hình
docker compose down                 # dừng, giữ dữ liệu
docker compose down -v              # dừng và xóa dữ liệu SQLite
```

## Chạy không cần Docker (phát triển)

```powershell
cd frontend; npm install; npm run build; cd ..
.venv\Scripts\python.exe -m pip install "sqlalchemy>=2.0"
.venv\Scripts\python.exe -X utf8 -m uvicorn server.main:app --port 8000   # http://localhost:8000
.venv\Scripts\python.exe -X utf8 -m pytest tests/test_server_api.py
```

## Giới hạn

Đây là bản demo. Yêu cầu phân tích được xử lý tuần tự, chưa có đăng nhập (chỉ nên mở trong mạng nội bộ), và gán mã RxNorm cho thuốc chưa có trong bộ đệm cần Internet.

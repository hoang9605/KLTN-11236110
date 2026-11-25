import { useEffect, useState } from "react";
import { api, Health } from "../api";

const STACK = [
  ["Giao diện", "React 18 + TypeScript, Vite, Cytoscape.js; FastAPI phục vụ bản đã build"],
  ["API", "FastAPI + Uvicorn (Python 3.12), tài liệu OpenAPI tại /api/docs"],
  ["Mô hình", "PyTorch + Transformers: ViHealthBERT-NER, ViHealthBERT-RE (trung bình 3 seed)"],
  ["Chuẩn hóa", "ICD-10 (danh mục Bộ Y tế) · RxNorm (bộ đệm SQLite + RxNav API)"],
  ["Lưu trữ", "SQLite qua SQLAlchemy 2"],
  ["Triển khai", "Docker Compose, một container"],
];

export default function SystemPage({ health }: { health: Health | null }) {
  const [info, setInfo] = useState<Record<string, unknown> | null>(null);
  useEffect(() => {
    api.info().then(setInfo).catch(() => setInfo(null));
  }, [health?.status]);

  return (
    <div className="system">
      <section className="panel">
        <h2>Trạng thái</h2>
        <table>
          <tbody>
            <tr><th>Mô hình</th><td>{health?.status ?? "—"} {health?.load_seconds != null && <span className="sub">(nạp {health.load_seconds} s)</span>}</td></tr>
            {health?.error && <tr><th>Lỗi</th><td className="error">{health.error}</td></tr>}
            <tr><th>Cơ sở dữ liệu</th><td>{health ? (health.database ? "kết nối tốt" : "mất kết nối") : "—"}</td></tr>
            <tr><th>Phiên bản</th><td>{health?.version ?? "—"}</td></tr>
            <tr><th>Thời gian chạy</th><td>{health ? `${Math.round(health.uptime_seconds / 60)} phút` : "—"}</td></tr>
          </tbody>
        </table>
        <p className="row">
          <a className="button" href="/api/docs" target="_blank" rel="noreferrer">Tài liệu API (Swagger)</a>
        </p>
      </section>
      <section className="panel">
        <h2>Công nghệ</h2>
        <table>
          <tbody>
            {STACK.map(([k, v]) => (
              <tr key={k}><th>{k}</th><td>{v}</td></tr>
            ))}
          </tbody>
        </table>
      </section>
      <section className="panel full">
        <h2>Thông tin chi tiết (/api/info)</h2>
        <pre>{info ? JSON.stringify(info, null, 2) : "…"}</pre>
      </section>
    </div>
  );
}

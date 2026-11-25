import { useEffect, useState } from "react";
import { NavLink, Route, Routes } from "react-router-dom";
import { api, Health } from "./api";
import AnalyzePage from "./pages/AnalyzePage";
import HistoryPage from "./pages/HistoryPage";
import GraphPage from "./pages/GraphPage";
import SystemPage from "./pages/SystemPage";

const STATUS_TEXT: Record<string, string> = {
  ready: "Mô hình sẵn sàng",
  loading: "Đang nạp mô hình…",
  error: "Lỗi nạp mô hình",
  disabled: "Chế độ chỉ xem",
  offline: "Mất kết nối API",
};

export default function App() {
  const [health, setHealth] = useState<Health | null>(null);
  const [offline, setOffline] = useState(false);

  useEffect(() => {
    let timer: number;
    const poll = async () => {
      try {
        const h = await api.health();
        setHealth(h);
        setOffline(false);
        timer = window.setTimeout(poll, h.status === "loading" ? 2000 : 15000);
      } catch {
        setOffline(true);
        timer = window.setTimeout(poll, 4000);
      }
    };
    poll();
    return () => window.clearTimeout(timer);
  }, []);

  const status = offline ? "offline" : health?.status ?? "loading";

  return (
    <div className="shell">
      <header className="top">
        <div className="brand">
          <span className="logo" aria-hidden>
            ✚
          </span>
          <div>
            <strong>MedKG</strong>
            <small>Trích xuất thực thể, quan hệ & chuẩn hóa thông tin y tế tiếng Việt</small>
          </div>
        </div>
        <nav>
          <NavLink to="/" end>
            Phân tích
          </NavLink>
          <NavLink to="/history">Lịch sử</NavLink>
          <NavLink to="/graph">Đồ thị tri thức</NavLink>
          <NavLink to="/system">Hệ thống</NavLink>
        </nav>
        <span className={`pill ${status}`} title={health?.error ?? ""}>
          <i />
          {STATUS_TEXT[status]}
        </span>
      </header>
      <main>
        <Routes>
          <Route path="/" element={<AnalyzePage ready={status === "ready"} />} />
          <Route path="/history" element={<HistoryPage />} />
          <Route path="/graph" element={<GraphPage />} />
          <Route path="/system" element={<SystemPage health={health} />} />
          <Route path="*" element={<p className="empty">Không tìm thấy trang.</p>} />
        </Routes>
      </main>
    </div>
  );
}

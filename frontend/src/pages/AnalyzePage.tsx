import { useEffect, useState } from "react";
import { AnalyzeResult, api } from "../api";
import ResultView from "../components/ResultView";

const MAX_CHARS = 2000;

export default function AnalyzePage({ ready }: { ready: boolean }) {
  const [text, setText] = useState("Bệnh nhân bị đau đầu, uống Paracetamol 500mg 2 viên/ngày.");
  const [normalize, setNormalize] = useState(true);
  const [save, setSave] = useState(true);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<AnalyzeResult | null>(null);
  const [samples, setSamples] = useState<string[]>([]);

  useEffect(() => {
    api.samples().then(setSamples).catch(() => setSamples([]));
  }, []);

  const run = async (t = text) => {
    if (!t.trim()) return;
    setBusy(true);
    setError(null);
    try {
      setResult(await api.analyze(t, normalize, save));
    } catch (e) {
      setError((e as Error).message);
    } finally {
      setBusy(false);
    }
  };

  return (
    <div className="split">
      <aside className="panel">
        <h2>Văn bản đầu vào</h2>
        <textarea
          value={text}
          maxLength={MAX_CHARS}
          onChange={(e) => setText(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === "Enter" && (e.ctrlKey || e.metaKey)) run();
          }}
          placeholder="Nhập ghi chú lâm sàng tiếng Việt…"
        />
        <div className="row">
          <button onClick={() => run()} disabled={busy || !ready || !text.trim()}>
            {busy ? "Đang phân tích…" : "Phân tích"}
          </button>
          <button className="ghost" onClick={() => { setText(""); setResult(null); }}>
            Xóa
          </button>
          <span className="sub right">
            {text.length}/{MAX_CHARS}
          </span>
        </div>
        <div className="row">
          <label className="opt">
            <input type="checkbox" checked={normalize} onChange={(e) => setNormalize(e.target.checked)} />
            Chuẩn hóa ICD-10 / RxNorm
          </label>
          <label className="opt">
            <input type="checkbox" checked={save} onChange={(e) => setSave(e.target.checked)} />
            Lưu vào lịch sử & đồ thị
          </label>
        </div>
        {!ready && <p className="status">Mô hình chưa sẵn sàng — nút phân tích sẽ bật khi nạp xong.</p>}
        {error && <p className="status error">{error}</p>}
        {samples.length > 0 && (
          <div className="examples">
            <h2>Câu ví dụ</h2>
            {samples.map((s) => (
              <button key={s} className="example" onClick={() => { setText(s); if (ready) run(s); }}>
                {s}
              </button>
            ))}
          </div>
        )}
      </aside>
      <section>
        {result ? (
          <ResultView result={result} />
        ) : (
          <div className="panel placeholder">
            <h2>Kết quả</h2>
            <p className="empty">
              Pipeline: <b>NER</b> (ViHealthBERT) → <b>chuẩn hóa</b> (ICD-10 Bộ Y tế, RxNorm) → <b>trích xuất quan hệ</b>{" "}
              (ViHealthBERT-RE, 3 seed) → <b>đồ thị tri thức</b>. Nhập văn bản và bấm “Phân tích” (Ctrl+Enter).
            </p>
          </div>
        )}
      </section>
    </div>
  );
}

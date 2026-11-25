import { useCallback, useEffect, useState } from "react";
import { AnalyzeResult, api, DocSummary } from "../api";
import ResultView from "../components/ResultView";

const PAGE = 20;

export default function HistoryPage() {
  const [items, setItems] = useState<DocSummary[]>([]);
  const [total, setTotal] = useState(0);
  const [page, setPage] = useState(0);
  const [q, setQ] = useState("");
  const [query, setQuery] = useState("");
  const [source, setSource] = useState("");
  const [selected, setSelected] = useState<(DocSummary & { result: AnalyzeResult }) | null>(null);
  const [error, setError] = useState<string | null>(null);

  const load = useCallback(async () => {
    try {
      const r = await api.documents({ limit: PAGE, offset: page * PAGE, q: query, source });
      setItems(r.items);
      setTotal(r.total);
      setError(null);
    } catch (e) {
      setError((e as Error).message);
    }
  }, [page, query, source]);

  useEffect(() => {
    load();
  }, [load]);

  const open = async (id: number) => setSelected(await api.document(id));
  const remove = async (id: number) => {
    if (!window.confirm(`Xóa văn bản #${id} khỏi lịch sử và đồ thị tri thức?`)) return;
    await api.deleteDocument(id);
    if (selected?.id === id) setSelected(null);
    load();
  };
  const pages = Math.max(1, Math.ceil(total / PAGE));

  return (
    <div className="split wide-left">
      <section className="panel">
        <div className="panel-head">
          <h2>Lịch sử phân tích ({total})</h2>
        </div>
        <form
          className="row"
          onSubmit={(e) => {
            e.preventDefault();
            setPage(0);
            setQuery(q);
          }}
        >
          <input className="grow" value={q} onChange={(e) => setQ(e.target.value)} placeholder="Tìm trong văn bản…" />
          <select value={source} onChange={(e) => { setPage(0); setSource(e.target.value); }}>
            <option value="">Mọi nguồn</option>
            <option value="user">Người dùng</option>
            <option value="seed">Dữ liệu nạp sẵn</option>
          </select>
          <button type="submit">Tìm</button>
        </form>
        {error && <p className="status error">{error}</p>}
        <div className="table-wrap">
          <table>
            <thead>
              <tr>
                <th>#</th>
                <th>Văn bản</th>
                <th>TT</th>
                <th>QH</th>
                <th />
              </tr>
            </thead>
            <tbody>
              {items.map((d) => (
                <tr key={d.id} className={`click ${selected?.id === d.id ? "hl-row" : ""}`} onClick={() => open(d.id)}>
                  <td className="sub">{d.id}</td>
                  <td>
                    <div className="clip">{d.text}</div>
                    <div className="sub">
                      {new Date(d.created_at).toLocaleString("vi-VN")} · {d.source === "seed" ? "nạp sẵn" : "người dùng"}
                      {d.elapsed_ms != null && ` · ${d.elapsed_ms} ms`}
                    </div>
                  </td>
                  <td>{d.n_entities}</td>
                  <td>{d.n_relations}</td>
                  <td>
                    <button className="ghost small" onClick={(e) => { e.stopPropagation(); remove(d.id); }} title="Xóa">
                      ✕
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        {items.length === 0 && <p className="empty">Chưa có văn bản nào.</p>}
        <div className="row pager">
          <button className="ghost" disabled={page === 0} onClick={() => setPage(page - 1)}>
            ‹ Trước
          </button>
          <span className="sub">
            Trang {page + 1}/{pages}
          </span>
          <button className="ghost" disabled={page + 1 >= pages} onClick={() => setPage(page + 1)}>
            Sau ›
          </button>
        </div>
      </section>
      <section>
        {selected ? (
          <ResultView result={selected.result} />
        ) : (
          <div className="panel placeholder">
            <p className="empty">Chọn một văn bản để xem kết quả.</p>
          </div>
        )}
      </section>
    </div>
  );
}

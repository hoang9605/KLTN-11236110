import { useState } from "react";
import { AnalyzeResult, Entity } from "../api";
import { ENTITY_COLOR, ENTITY_LABEL, METHOD_LABEL, RELATION_LABEL } from "../labels";

const surface = (e: Entity) => e.surface_text ?? e.text ?? "";

function Annotated({ result, hover, setHover }: { result: AnalyzeResult; hover: string | null; setHover: (id: string | null) => void }) {
  const ents = [...result.entities].sort((a, b) => a.start - b.start);
  const parts: JSX.Element[] = [];
  let pos = 0;
  ents.forEach((e) => {
    if (e.start < pos) return; // thực thể chồng lấn: bỏ qua phần sau
    if (e.start > pos) parts.push(<span key={`t${pos}`}>{result.text.slice(pos, e.start)}</span>);
    const color = ENTITY_COLOR[e.label] ?? "#555";
    parts.push(
      <mark
        key={e.id}
        className={`ent ${e.re_excluded ? "muted" : ""} ${hover === e.id ? "hl" : ""}`}
        style={{ background: `${color}1a`, borderColor: color }}
        onMouseEnter={() => setHover(e.id)}
        onMouseLeave={() => setHover(null)}
        title={`${ENTITY_LABEL[e.label] ?? e.label}${e.normalized ? ` · ${e.normalized.ontology} ${e.normalized.code}` : ""}`}
      >
        {result.text.slice(e.start, e.end)}
        <sub style={{ color }}>{e.label}</sub>
      </mark>,
    );
    pos = e.end;
  });
  if (pos < result.text.length) parts.push(<span key="tend">{result.text.slice(pos)}</span>);
  return <p className="annot">{parts}</p>;
}

export function Tag({ label }: { label: string }) {
  return (
    <span className="tag" style={{ background: ENTITY_COLOR[label] ?? "#555" }}>
      {label}
    </span>
  );
}

export default function ResultView({ result }: { result: AnalyzeResult }) {
  const [hover, setHover] = useState<string | null>(null);
  const [tab, setTab] = useState<"table" | "json">("table");
  const byId = Object.fromEntries(result.entities.map((e) => [e.id, e]));

  return (
    <div className="results">
      <section className="panel">
        <div className="panel-head">
          <h2>Văn bản đã gán nhãn</h2>
          <span className="sub">
            {result.entities.length} thực thể · {result.relations.length} quan hệ
            {result.elapsed_ms != null && ` · ${result.elapsed_ms} ms`}
            {result.document_id != null && ` · đã lưu #${result.document_id}`}
          </span>
        </div>
        <Annotated result={result} hover={hover} setHover={setHover} />
        <div className="legend">
          {Object.entries(ENTITY_LABEL).map(([k, v]) => (
            <span key={k}>
              <i style={{ background: ENTITY_COLOR[k] }} />
              {v}
            </span>
          ))}
        </div>
      </section>

      <section className="panel">
        <div className="panel-head">
          <h2>Quan hệ</h2>
        </div>
        {result.relations.length === 0 ? (
          <p className="empty">Không tìm thấy quan hệ.</p>
        ) : (
          result.relations.map((r, i) => (
            <div className="rel" key={i} onMouseEnter={() => setHover(r.head)} onMouseLeave={() => setHover(null)}>
              <Tag label={byId[r.head]?.label} />
              <span className="name">{byId[r.head] ? surface(byId[r.head]) : r.head}</span>
              <span className="arrow">
                —<b>{RELATION_LABEL[r.label] ?? r.label}</b>→
              </span>
              <Tag label={byId[r.tail]?.label} />
              <span className="name">{byId[r.tail] ? surface(byId[r.tail]) : r.tail}</span>
              <span className="src">
                {r.source === "rule" ? "luật" : "mô hình"}
                {r.score != null && (
                  <>
                    {" "}
                    {r.score.toFixed(2)}
                    <span className="bar">
                      <b style={{ width: `${Math.round(r.score * 100)}%` }} />
                    </span>
                  </>
                )}
              </span>
            </div>
          ))
        )}
      </section>

      <section className="panel">
        <div className="panel-head">
          <h2>Thực thể & chuẩn hóa</h2>
          <div className="tabs">
            <button className={tab === "table" ? "on" : ""} onClick={() => setTab("table")}>
              Bảng
            </button>
            <button className={tab === "json" ? "on" : ""} onClick={() => setTab("json")}>
              JSON
            </button>
          </div>
        </div>
        {tab === "json" ? (
          <pre>{JSON.stringify(result, null, 2)}</pre>
        ) : result.entities.length === 0 ? (
          <p className="empty">Không có thực thể.</p>
        ) : (
          <div className="table-wrap">
            <table>
              <thead>
                <tr>
                  <th>Thực thể</th>
                  <th>Loại</th>
                  <th>Độ tin cậy</th>
                  <th>Mã chuẩn</th>
                </tr>
              </thead>
              <tbody>
                {result.entities.map((e) => (
                  <tr key={e.id} className={hover === e.id ? "hl-row" : ""} onMouseEnter={() => setHover(e.id)} onMouseLeave={() => setHover(null)}>
                    <td>
                      <b>{surface(e)}</b>
                      {e.re_excluded && <div className="sub">bỏ qua khi tìm quan hệ (thực thể chung)</div>}
                    </td>
                    <td>
                      <Tag label={e.label} />
                    </td>
                    <td>{e.confidence != null ? e.confidence.toFixed(2) : "—"}</td>
                    <td>
                      {e.normalized ? (
                        <>
                          <span className="code">
                            {e.normalized.ontology} {e.normalized.code}
                          </span>{" "}
                          {e.normalized.label_standard}
                          <div className="sub">
                            {METHOD_LABEL[e.normalized.match_method ?? ""] ?? e.normalized.match_method}
                            {e.normalized.match_score != null && ` · ${e.normalized.match_score.toFixed(2)}`}
                          </div>
                        </>
                      ) : (
                        <span className="sub">chưa chuẩn hóa</span>
                      )}
                      {!e.normalized && e.candidates && e.candidates.length > 0 && (
                        <details>
                          <summary>{e.candidates.length} mã gợi ý</summary>
                          <ol>
                            {e.candidates.map((c) => (
                              <li key={c.rank}>
                                <span className="code">{c.code}</span> {c.label_standard}{" "}
                                <span className="sub">({c.match_score?.toFixed(2)})</span>
                              </li>
                            ))}
                          </ol>
                        </details>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </section>
    </div>
  );
}

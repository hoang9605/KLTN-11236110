import cytoscape, { Core } from "cytoscape";
import { useEffect, useRef, useState } from "react";
import { api, KGEdge, KGNode, KGStats } from "../api";
import { Tag } from "../components/ResultView";
import { ENTITY_COLOR, ENTITY_LABEL, ENTITY_TYPES, RELATION_LABEL, RELATIONS } from "../labels";

type Graph = { stats: KGStats; nodes: KGNode[]; edges: KGEdge[] };

export default function GraphPage() {
  const box = useRef<HTMLDivElement>(null);
  const cy = useRef<Core | null>(null);
  const [graph, setGraph] = useState<Graph | null>(null);
  const [limit, setLimit] = useState(120);
  const [minCount, setMinCount] = useState(2);
  const [relation, setRelation] = useState("");
  const [type, setType] = useState("");
  const [center, setCenter] = useState<string>("");
  const [q, setQ] = useState("");
  const [hits, setHits] = useState<KGNode[]>([]);
  const [detail, setDetail] = useState<{ node: KGNode; edges: KGEdge[] } | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    api
      .kg({ limit, min_count: center ? 1 : minCount, relation, type, center })
      .then((g) => {
        setGraph(g);
        setError(null);
      })
      .catch((e) => setError((e as Error).message));
  }, [limit, minCount, relation, type, center]);

  useEffect(() => {
    if (!box.current || !graph) return;
    const maxM = Math.max(1, ...graph.nodes.map((n) => n.mentions));
    const maxC = Math.max(1, ...graph.edges.map((e) => e.count));
    cy.current?.destroy();
    const inst = cytoscape({
      container: box.current,
      elements: [
        ...graph.nodes.map((n) => ({
          data: {
            id: n.key,
            label: n.code ? `${n.name.length > 28 ? n.name.slice(0, 27) + "…" : n.name}\n${n.code}` : n.name,
            color: ENTITY_COLOR[n.type] ?? "#888",
            size: 18 + 34 * Math.sqrt(n.mentions / maxM),
            center: n.key === center ? 1 : 0,
          },
        })),
        ...graph.edges.map((e, i) => ({
          data: {
            id: `e${i}`,
            source: e.head,
            target: e.tail,
            label: RELATION_LABEL[e.relation] ?? e.relation,
            width: 1 + 5 * (e.count / maxC),
            rule: e.sources.rule && !e.sources.model ? 1 : 0,
          },
        })),
      ],
      style: [
        {
          selector: "node",
          style: {
            "background-color": "data(color)",
            width: "data(size)",
            height: "data(size)",
            label: "data(label)",
            "font-size": 10,
            "text-wrap": "wrap",
            "text-valign": "bottom",
            "text-margin-y": 4,
            color: "#1d2433",
            "text-outline-color": "#fff",
            "text-outline-width": 2,
          },
        },
        { selector: "node[center = 1]", style: { "border-width": 4, "border-color": "#ffd43b" } },
        { selector: "node:selected", style: { "border-width": 3, "border-color": "#13294b" } },
        {
          selector: "edge",
          style: {
            width: "data(width)",
            "line-color": "#b8c2d3",
            "target-arrow-color": "#b8c2d3",
            "target-arrow-shape": "triangle",
            "curve-style": "bezier",
            label: "data(label)",
            "font-size": 8,
            color: "#6b7385",
            "text-rotation": "autorotate",
            "text-background-color": "#fff",
            "text-background-opacity": 0.8,
            "text-background-padding": "1px",
          },
        },
        { selector: "edge[rule = 1]", style: { "line-style": "dashed" } },
      ],
      layout: { name: "cose", animate: false, nodeRepulsion: () => 9000, idealEdgeLength: () => 90, padding: 20 },
      wheelSensitivity: 0.25,
      minZoom: 0.1,
      maxZoom: 2.5,
    });
    inst.on("tap", "node", (evt) => {
      api.kgNode(evt.target.id()).then(setDetail).catch(() => setDetail(null));
    });
    cy.current = inst;
    return () => inst.destroy();
  }, [graph, center]);

  const search = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!q.trim()) return setHits([]);
    setHits(await api.kgSearch(q.trim()));
  };
  const focus = (key: string) => {
    setCenter(key);
    setHits([]);
    api.kgNode(key).then(setDetail);
  };

  return (
    <div className="graph-layout">
      <aside className="panel graph-side">
        <h2>Đồ thị tri thức</h2>
        {graph && (
          <div className="stats">
            <div><b>{graph.stats.documents.toLocaleString("vi-VN")}</b><span>văn bản</span></div>
            <div><b>{graph.stats.nodes.toLocaleString("vi-VN")}</b><span>nút</span></div>
            <div><b>{graph.stats.edges.toLocaleString("vi-VN")}</b><span>cạnh</span></div>
            <div><b>{graph.stats.normalized_nodes.toLocaleString("vi-VN")}</b><span>nút có mã</span></div>
          </div>
        )}
        <form onSubmit={search} className="row">
          <input className="grow" value={q} onChange={(e) => setQ(e.target.value)} placeholder="Tìm nút: tiểu đường, E11, aspirin…" />
          <button type="submit">Tìm</button>
        </form>
        {hits.length > 0 && (
          <ul className="hits">
            {hits.map((n) => (
              <li key={n.key} onClick={() => focus(n.key)}>
                <Tag label={n.type} /> {n.name} <span className="sub">{n.code ?? ""} · {n.mentions} lần</span>
              </li>
            ))}
          </ul>
        )}
        {center && (
          <p className="row">
            <span className="sub">Đang xem lân cận của <b>{center}</b></span>
            <button className="ghost small" onClick={() => setCenter("")}>Bỏ lọc</button>
          </p>
        )}
        <label className="field">
          Quan hệ
          <select value={relation} onChange={(e) => setRelation(e.target.value)}>
            <option value="">Tất cả</option>
            {RELATIONS.map((r) => (
              <option key={r} value={r}>{RELATION_LABEL[r]} ({r})</option>
            ))}
          </select>
        </label>
        <label className="field">
          Loại nút
          <select value={type} onChange={(e) => setType(e.target.value)}>
            <option value="">Tất cả</option>
            {ENTITY_TYPES.map((t) => (
              <option key={t} value={t}>{ENTITY_LABEL[t]}</option>
            ))}
          </select>
        </label>
        <label className="field">
          Số lần xuất hiện tối thiểu: <b>{minCount}</b>
          <input type="range" min={1} max={10} value={minCount} disabled={!!center} onChange={(e) => setMinCount(+e.target.value)} />
        </label>
        <label className="field">
          Số cạnh tối đa: <b>{limit}</b>
          <input type="range" min={20} max={600} step={20} value={limit} onChange={(e) => setLimit(+e.target.value)} />
        </label>
        <div className="row">
          <a className="button ghost" href="/api/kg/export?format=json">Tải kg.json</a>
          <a className="button ghost" href="/api/kg/export?format=csv">Tải triples.csv</a>
        </div>
        <div className="legend">
          {ENTITY_TYPES.map((t) => (
            <span key={t}><i style={{ background: ENTITY_COLOR[t] }} />{ENTITY_LABEL[t]}</span>
          ))}
          <span>– – cạnh chỉ do luật</span>
        </div>
        {error && <p className="status error">{error}</p>}
      </aside>
      <section className="panel graph-canvas">
        <div ref={box} className="cy" />
        {graph && graph.edges.length === 0 && (
          <p className="empty overlay">{center ? "Nút này chưa có quan hệ nào trong đồ thị." : "Không có cạnh nào thỏa bộ lọc."}</p>
        )}
      </section>
      {detail && (
        <aside className="panel graph-detail">
          <div className="panel-head">
            <h2>Chi tiết nút</h2>
            <button className="ghost small" onClick={() => setDetail(null)}>✕</button>
          </div>
          <p>
            <Tag label={detail.node.type} /> <b>{detail.node.name}</b>
          </p>
          <p className="sub">
            {detail.node.code ? `${detail.node.ontology} ${detail.node.code}` : detail.node.suggested_code ? `gợi ý: ${detail.node.suggested_code}` : "chưa chuẩn hóa"}
            {" · "}
            {detail.node.mentions} lần nhắc · {detail.node.documents} văn bản
          </p>
          <p className="sub">Cách viết: {Object.keys(detail.node.surfaces).slice(0, 8).join(", ")}</p>
          <button className="ghost small" onClick={() => focus(detail.node.key)}>Xem lân cận trên đồ thị</button>
          <h2 className="mt">Quan hệ ({detail.edges.length})</h2>
          <ul className="edges">
            {detail.edges.slice(0, 40).map((e, i) => (
              <li key={i}>
                <span className={e.head === detail.node.key ? "self" : "link"} onClick={() => e.head !== detail.node.key && focus(e.head)}>{e.head_name}</span>{" "}
                <span className="sub">—{RELATION_LABEL[e.relation] ?? e.relation}→</span>{" "}
                <span className={e.tail === detail.node.key ? "self" : "link"} onClick={() => e.tail !== detail.node.key && focus(e.tail)}>{e.tail_name}</span>{" "}
                <span className="sub">×{e.count}</span>
                {e.examples[0] && <div className="example-text">“{e.examples[0]}”</div>}
              </li>
            ))}
          </ul>
        </aside>
      )}
    </div>
  );
}

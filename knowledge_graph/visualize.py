"""Standalone interactive HTML view of a KnowledgeGraph (vis-network from a pinned CDN build).

Open the written file in a browser: filter by relation and minimum edge count, search a
concept, click a node to see its code, surface forms and the sentences behind each edge.
"""
import json
from pathlib import Path

VIS_NETWORK = "https://unpkg.com/vis-network@9.1.9/standalone/umd/vis-network.min.js"
COLORS = {"CONDITION": "#d1495b", "DRUG": "#00798c", "BODY_PART": "#edae49",
          "TEST": "#66a182", "PROCEDURE": "#8d6cab", "DOSAGE": "#7a7a7a"}
RELATION_VI = {"located_at": "vị trí", "treated_by": "điều trị bằng thuốc",
               "treated_by_procedure": "điều trị bằng thủ thuật", "diagnosed_by": "chẩn đoán bằng",
               "has_dosage": "liều dùng"}

TEMPLATE = """<!doctype html>
<html lang="vi"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Đồ thị tri thức y tế</title>
<script src="__VIS__"></script>
<style>
:root{--bg:#fafaf8;--fg:#1d1d1f;--muted:#6b6b6b;--panel:#fff;--line:#e3e3df}
@media (prefers-color-scheme:dark){:root{--bg:#141416;--fg:#ececec;--muted:#a0a0a0;--panel:#1e1e22;--line:#33333a}}
*{box-sizing:border-box}body{margin:0;font:14px/1.45 system-ui,-apple-system,"Segoe UI",sans-serif;background:var(--bg);color:var(--fg)}
header{padding:12px 16px;border-bottom:1px solid var(--line);display:flex;flex-wrap:wrap;gap:12px;align-items:center}
h1{font-size:16px;margin:0 12px 0 0}.ctl{display:flex;gap:6px;align-items:center;color:var(--muted)}
input[type=search]{padding:5px 8px;border:1px solid var(--line);border-radius:6px;background:var(--panel);color:var(--fg)}
main{display:flex;height:calc(100vh - 58px)}#net{flex:1;min-width:0}
aside{width:340px;max-width:40vw;border-left:1px solid var(--line);padding:12px 14px;overflow:auto;background:var(--panel)}
.legend span{display:inline-flex;align-items:center;gap:4px;margin-right:8px}.dot{width:10px;height:10px;border-radius:50%}
.muted{color:var(--muted)}.edge{border-top:1px solid var(--line);padding:6px 0}.ex{font-size:12px;color:var(--muted);margin:2px 0 0 8px}
code{font-size:12px}@media (max-width:700px){main{flex-direction:column;height:auto}#net{height:65vh}aside{width:auto;max-width:none;border-left:0;border-top:1px solid var(--line)}}
</style></head><body>
<header><h1>Đồ thị tri thức y tế</h1>
<span class="ctl" id="rels"></span>
<label class="ctl">Cạnh xuất hiện ≥ <input id="min" type="number" min="1" value="__MIN__" style="width:56px"></label>
<input id="q" type="search" placeholder="Tìm khái niệm hoặc mã…">
<span class="legend" id="legend"></span></header>
<main><div id="net"></div><aside id="info"><p class="muted">__STATS__</p><p class="muted">Bấm vào một nút để xem mã chuẩn, các cách viết và câu nguồn.</p></aside></main>
<script>
const DATA = __DATA__, COLORS = __COLORS__, REL = __REL__;
const byKey = Object.fromEntries(DATA.nodes.map(n => [n.key, n]));
const relSel = new Set(Object.keys(DATA.stats.edges_by_relation));
const relBox = document.getElementById('rels');
for (const r of relSel) { const l = document.createElement('label'); l.className = 'ctl';
  l.innerHTML = `<input type=checkbox checked value="${r}">${REL[r] || r}`; relBox.appendChild(l); }
document.getElementById('legend').innerHTML = Object.entries(COLORS).map(([t, c]) => `<span><i class="dot" style="background:${c}"></i>${t}</span>`).join('');
const nodes = new vis.DataSet(), edges = new vis.DataSet();
const net = new vis.Network(document.getElementById('net'), {nodes, edges}, {
  physics: {solver: 'forceAtlas2Based', stabilization: {iterations: 200}},
  nodes: {shape: 'dot', font: {size: 13}}, edges: {arrows: 'to', font: {size: 10, align: 'middle'}, smooth: {type: 'dynamic'}},
  interaction: {hover: true}});
function esc(s) { return String(s ?? '').replace(/[&<>"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c])); }
function render() {
  const min = +document.getElementById('min').value || 1, q = document.getElementById('q').value.trim().toLowerCase();
  const es = DATA.edges.filter(e => relSel.has(e.relation) && e.count >= min);
  let keep = new Set(es.flatMap(e => [e.head, e.tail]));
  if (q) { const hit = new Set(DATA.nodes.filter(n => (n.name + ' ' + (n.code || '') + ' ' + Object.keys(n.surfaces).join(' ')).toLowerCase().includes(q)).map(n => n.key));
    keep = new Set(es.filter(e => hit.has(e.head) || hit.has(e.tail)).flatMap(e => [e.head, e.tail])); hit.forEach(k => keep.add(k)); }
  nodes.clear(); edges.clear();
  nodes.add([...keep].map(k => { const n = byKey[k]; return {id: k, label: n.code ? `${n.name}\\n${n.code}` : n.name,
    color: COLORS[n.type], size: 8 + 4 * Math.sqrt(n.mentions), borderWidth: n.code ? 1 : 3, shapeProperties: {borderDashes: n.code ? false : [4, 3]},
    title: `${n.type} · ${n.mentions} lần nhắc` }; }));
  edges.add(es.filter(e => keep.has(e.head) && keep.has(e.tail)).map((e, i) => ({id: i, from: e.head, to: e.tail,
    label: `${REL[e.relation] || e.relation} (${e.count})`, width: 1 + Math.log2(e.count), dashes: !e.sources.model,
    title: `nguồn: ${Object.entries(e.sources).map(([s, c]) => s + '×' + c).join(', ')}`})));
}
net.on('click', p => { if (!p.nodes.length) return; const n = byKey[p.nodes[0]];
  const es = DATA.edges.filter(e => e.head === n.key || e.tail === n.key);
  document.getElementById('info').innerHTML = `<h2 style="font-size:15px;margin:0 0 4px">${esc(n.name)}</h2>
   <div class=muted>${n.type} · ${n.code ? esc(n.ontology + ' ' + n.code) : 'chưa chuẩn hóa' + (n.suggested_code ? ' · gợi ý: ' + esc(n.suggested_code) : '')}</div>
   <p>${n.mentions} lần nhắc trong ${n.documents} câu. Cách viết: ${Object.entries(n.surfaces).map(([s, c]) => esc(s) + ' (' + c + ')').join(', ')}</p>
   ${es.map(e => `<div class=edge><b>${esc(byKey[e.head].name)}</b> → ${esc(REL[e.relation] || e.relation)} → <b>${esc(byKey[e.tail].name)}</b>
     <span class=muted>×${e.count}, ${Object.keys(e.sources).join('+')}</span>${e.examples.map(x => `<div class=ex>“${esc(x)}”</div>`).join('')}</div>`).join('') || '<p class=muted>Không có quan hệ.</p>'}`; });
relBox.addEventListener('change', ev => { ev.target.checked ? relSel.add(ev.target.value) : relSel.delete(ev.target.value); render(); });
document.getElementById('min').addEventListener('input', render); document.getElementById('q').addEventListener('input', render);
render();
</script></body></html>
"""


def write_html(kg, path, min_count=1, title_stats=None):
    data = kg.to_dict()
    for n in data["nodes"]:
        n.pop("documents_list", None)
    s = data["stats"]
    stats = title_stats or (f"{s['documents']} câu · {s['nodes']} khái niệm ({s['normalized_nodes']} có mã chuẩn) · "
                            f"{s['edges']} quan hệ khác nhau ({s['edge_mentions']} lần xuất hiện). "
                            "Viền đứt: chưa chuẩn hóa. Cạnh đứt: chỉ do luật sinh ra.")
    html = (TEMPLATE.replace("__VIS__", VIS_NETWORK).replace("__MIN__", str(min_count))
            .replace("__STATS__", stats)
            .replace("__COLORS__", json.dumps(COLORS)).replace("__REL__", json.dumps(RELATION_VI, ensure_ascii=False))
            .replace("__DATA__", json.dumps(data, ensure_ascii=False).replace("</", "<\\/")))
    Path(path).write_text(html, encoding="utf-8")
    return path

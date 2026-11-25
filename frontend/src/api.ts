export type Normalized = {
  ontology: string;
  code: string;
  label_standard: string;
  match_method?: string;
  match_score?: number;
};

export type Entity = {
  id: string;
  surface_text?: string;
  text?: string;
  label: string;
  start: number;
  end: number;
  confidence?: number;
  normalized?: Normalized | null;
  candidates?: (Normalized & { rank: number })[];
  re_excluded?: string;
};

export type Relation = {
  head: string;
  tail: string;
  label: string;
  score?: number | null;
  source?: string;
};

export type AnalyzeResult = {
  text: string;
  entities: Entity[];
  relations: Relation[];
  elapsed_ms?: number;
  document_id?: number | null;
};

export type DocSummary = {
  id: number;
  created_at: string;
  source: string;
  external_id: string | null;
  text: string;
  n_entities: number;
  n_relations: number;
  elapsed_ms: number | null;
};

export type KGNode = {
  key: string;
  type: string;
  name: string;
  ontology: string | null;
  code: string | null;
  suggested_code: string | null;
  mentions: number;
  surfaces: Record<string, number>;
  documents: number;
};

export type KGEdge = {
  head: string;
  relation: string;
  tail: string;
  count: number;
  documents: number;
  sources: Record<string, number>;
  mean_score: number | null;
  examples: string[];
  head_name?: string;
  tail_name?: string;
};

export type KGStats = {
  documents: number;
  nodes: number;
  edges: number;
  edge_mentions: number;
  nodes_by_type: Record<string, number>;
  normalized_nodes: number;
  edges_by_relation: Record<string, number>;
};

export type Health = {
  status: "loading" | "ready" | "error" | "disabled";
  error: string | null;
  load_seconds: number | null;
  database: boolean;
  version: string;
  uptime_seconds: number;
};

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(path, {
    ...init,
    headers: { "Content-Type": "application/json", ...(init?.headers ?? {}) },
  });
  if (!res.ok) {
    let msg = `${res.status} ${res.statusText}`;
    try {
      const body = await res.json();
      if (typeof body.detail === "string") msg = body.detail;
      else if (Array.isArray(body.detail)) msg = body.detail.map((d: { msg: string }) => d.msg).join("; ");
    } catch {
      /* không phải JSON */
    }
    throw new Error(msg);
  }
  return res.json() as Promise<T>;
}

const qs = (p: Record<string, string | number | undefined | null>) =>
  new URLSearchParams(
    Object.entries(p)
      .filter(([, v]) => v !== undefined && v !== null && v !== "")
      .map(([k, v]) => [k, String(v)]),
  ).toString();

export const api = {
  health: () => request<Health>("/api/health"),
  info: () => request<Record<string, unknown>>("/api/info"),
  samples: () => request<string[]>("/api/samples"),
  analyze: (text: string, normalize: boolean, save: boolean) =>
    request<AnalyzeResult>("/api/analyze", { method: "POST", body: JSON.stringify({ text, normalize, save }) }),
  documents: (p: { limit: number; offset: number; q?: string; source?: string }) =>
    request<{ total: number; items: DocSummary[] }>(`/api/documents?${qs(p)}`),
  document: (id: number) => request<DocSummary & { result: AnalyzeResult }>(`/api/documents/${id}`),
  deleteDocument: (id: number) => request<{ deleted: number }>(`/api/documents/${id}`, { method: "DELETE" }),
  kg: (p: { limit: number; min_count: number; relation?: string; type?: string; center?: string }) =>
    request<{ stats: KGStats; nodes: KGNode[]; edges: KGEdge[] }>(`/api/kg?${qs(p)}`),
  kgSearch: (q: string) => request<KGNode[]>(`/api/kg/search?${qs({ q })}`),
  kgNode: (key: string) => request<{ node: KGNode; edges: KGEdge[] }>(`/api/kg/node?${qs({ key })}`),
};

"""Shared helpers for the end-to-end NER -> RE golden test set.

Gold text = the source words joined by single spaces, so character offsets match
the text MedicalNERPipeline returns (it only collapses whitespace).
"""
import hashlib
import json
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCHEMA = json.loads((ROOT / "re_labels.json").read_text(encoding="utf-8"))
RELATIONS = {r["label"]: (r["head_type"], r["tail_type"]) for r in SCHEMA["relations"]}
NEGATIVE = SCHEMA["negative_label"]
UNKNOWN = "CHUA_RO"
ENTITY_TYPES = SCHEMA["entity_types"]

# Same mapping as ner/config.py (VIETMED_TO_TARGET); read from source to stay in sync.
def _load_mapping():
    import ast
    tree = ast.parse((ROOT / "ner" / "config.py").read_text(encoding="utf-8"))
    for node in tree.body:
        if isinstance(node, ast.AnnAssign) and getattr(node.target, "id", "") == "VIETMED_TO_TARGET":
            return ast.literal_eval(node.value)
    raise RuntimeError("VIETMED_TO_TARGET not found in ner/config.py")

VIETMED_TO_TARGET = _load_mapping()
HF_CACHE = Path.home() / ".cache" / "huggingface" / "datasets" / "leduckhai___viet_med-ner"


def text_group(text):
    norm = " ".join(unicodedata.normalize("NFC", text).casefold().split())
    return hashlib.sha256(norm.encode("utf-8")).hexdigest()


def load_split(split, arrow_path=None):
    """Load a VietMed-NER split from the local HF arrow cache (preferred) or `datasets`."""
    cols = ["text", "words", "labels"]
    path = Path(arrow_path) if arrow_path else None
    if path is None and HF_CACHE.exists():
        found = sorted(HF_CACHE.rglob(f"viet_med-ner-{split}.arrow"))
        path = found[-1] if found else None
    if path is not None and path.exists():
        import pyarrow as pa
        with pa.memory_map(str(path), "r") as stream:
            try:
                table = pa.ipc.open_stream(stream).read_all()
            except pa.ArrowInvalid:
                table = pa.ipc.open_file(stream).read_all()
        return table.select(cols).to_pylist(), {"source": str(path), "fingerprint": path.parent.name}
    from datasets import load_dataset
    ds = load_dataset("leduckhai/VietMed-NER", split=split)
    ds = ds.remove_columns([c for c in ds.column_names if c not in cols])
    return ds.to_list(), {"source": "datasets.load_dataset", "fingerprint": ds._fingerprint}


def map_tag(tag):
    tag = str(tag).strip()
    if tag in ("0", "O") or "-" not in tag:
        return "O"
    prefix, ent = tag.split("-", 1)
    if prefix not in ("B", "I") or ent not in VIETMED_TO_TARGET:
        return "O"
    return f"{prefix}-{VIETMED_TO_TARGET[ent]}"


def entities_from_bio(words, labels):
    """Return (text, entities) with character offsets on ' '.join(words)."""
    text, starts, pos = " ".join(words), [], 0
    for w in words:
        starts.append(pos)
        pos += len(w) + 1
    ents, cur = [], None
    for i, (w, raw) in enumerate(zip(words, labels)):
        tag = map_tag(raw)
        s, e = starts[i], starts[i] + len(w)
        if tag == "O":
            cur = None
            continue
        prefix, typ = tag.split("-", 1)
        if prefix == "B" or cur is None or cur["label"] != typ:
            cur = {"label": typ, "start": s, "end": e, "token_start": i, "token_end": i + 1}
            ents.append(cur)
        else:
            cur["end"], cur["token_end"] = e, i + 1
    for n, ent in enumerate(ents, 1):
        ent["id"] = f"E{n}"
        ent["text"] = text[ent["start"]:ent["end"]]
    return text, [{k: e[k] for k in ("id", "text", "label", "start", "end", "token_start", "token_end")} for e in ents]


def candidate_pairs(entities):
    pairs = []
    for h in entities:
        for t in entities:
            for rel, types in RELATIONS.items():
                if (h["label"], t["label"]) == types:
                    pairs.append({"head": h["id"], "tail": t["id"], "allowed_relation": rel})
    for n, p in enumerate(pairs, 1):
        p["id"] = f"R{n}"
    return pairs


def marked(text, head, tail):
    spans = sorted([(head["start"], head["end"], "⟦", "⟧"), (tail["start"], tail["end"], "⟪", "⟫")], reverse=True)
    for s, e, a, b in spans:
        text = text[:s] + a + text[s:e] + b + text[e:]
    return text


def read_jsonl(path):
    return [json.loads(l) for l in Path(path).read_text(encoding="utf-8-sig").splitlines() if l.strip()]


def write_jsonl(path, rows):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows), encoding="utf-8")


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

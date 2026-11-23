"""Steps 4-5: write the batches that Claude sub-agents process, and check what they return.

  k3_bNN.jsonl   one sentence per line, with its K1 phrases -> sub-agent writes k3_bNN.out.jsonl:
     {"sentence_id", "literal_en", "k3": "plausible"|"implausible", "k3_rationale",
      "k1": [{"unit_id", "literal_en", "standard_term_en": str|null, "is_medical_expression": bool}]}
  k2_bNN.jsonl   one K2 triple without evidence (not has_dosage) per line -> k2_bNN.out.jsonl:
     {"unit_id", "query", "result": "supported"|"not_found"|"contradicted", "url", "snippet"}

  make:  .venv\\Scripts\\python.exe -X utf8 -m relation.validate.batches make
  check: .venv\\Scripts\\python.exe -X utf8 -m relation.validate.batches check
"""
import json
import sys
from collections import defaultdict

from .units import OUT, load

BATCH = OUT / "batches"
K3_BATCHES = 8
K2_BATCHES = 4


def status(evidence):
    s = defaultdict(set)
    for e in evidence:
        s[e["unit_id"]].add(e["result"])
    return {u: ("contradicted" if "contradicted" in r else "supported" if "supported" in r else "not_found")
            for u, r in s.items()}


def write(name, rows):
    with open(BATCH / name, "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")


def make():
    BATCH.mkdir(parents=True, exist_ok=True)
    units = {u["unit_id"]: u for u in load(OUT / "units.jsonl")}
    terms = {v["vi"]: v for v in json.loads((OUT / "en_terms.json").read_text(encoding="utf-8")).values()}
    st = status(load(OUT / "evidence.jsonl"))
    sent_units = {r["sentence_id"]: r["unit_ids"] for r in load(OUT / "sentence_units.jsonl")}

    k3 = []
    for sid, uids in sent_units.items():
        s = next(units[u] for u in uids if units[u]["kind"] == "K3")
        rep = s["replaced"]
        k3.append({"sentence_id": sid, "method": s["method"], "text_vi": s["text_vi"],
                   "parent_text_vi": s["parent_text"],
                   "replaced": {"old_vi": rep["old"], "new_vi": rep["new"]} if rep else None,
                   "k1": [{"unit_id": u, "phrase_vi": units[u]["phrase_vi"]} for u in uids if units[u]["kind"] == "K1"]})
    for i in range(K3_BATCHES):
        write(f"k3_b{i + 1:02d}.jsonl", k3[i::K3_BATCHES])

    k2 = [{"unit_id": u["unit_id"], "head_en": terms[u["head_vi"]]["en"], "relation": u["relation"],
           "tail_en": terms[u["tail_vi"]]["en"], "head_vi": u["head_vi"], "tail_vi": u["tail_vi"]}
          for u in units.values()
          if u["kind"] == "K2" and st.get(u["unit_id"]) == "not_found" and u["relation"] != "has_dosage"
          and terms[u["head_vi"]]["en"] and terms[u["tail_vi"]]["en"]]
    for i in range(K2_BATCHES):
        write(f"k2_b{i + 1:02d}.jsonl", k2[i::K2_BATCHES])
    print({"k3_sentences": len(k3), "k2_triples": len(k2)})


def check():
    bad = 0
    for f in sorted(BATCH.glob("k?_b??.jsonl")):
        want = [json.loads(l) for l in open(f, encoding="utf-8")]
        out = f.with_suffix(".out.jsonl")
        if not out.exists():
            print(f.name, "missing output"); bad += 1; continue
        got = {}
        for l in open(out, encoding="utf-8"):
            if l.strip():
                r = json.loads(l)
                got[r.get("sentence_id") or r.get("unit_id")] = r
        key = "sentence_id" if f.name.startswith("k3") else "unit_id"
        miss = [w[key] for w in want if w[key] not in got]
        errs = []
        for w in want:
            r = got.get(w[key])
            if not r:
                continue
            if key == "sentence_id":
                if r.get("k3") not in ("plausible", "implausible"):
                    errs.append(w[key])
                elif {k["unit_id"] for k in w["k1"]} - {k.get("unit_id") for k in r.get("k1", [])}:
                    errs.append(w[key])
            elif r.get("result") not in ("supported", "not_found", "contradicted") or \
                    (r["result"] != "not_found" and not r.get("url")):
                errs.append(w[key])
        print(f.name, len(want), "missing", len(miss), "invalid", len(errs), errs[:5])
        bad += bool(miss or errs)
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    {"make": make, "check": check}[sys.argv[1]]()

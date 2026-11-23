"""Step 3: look up evidence for K1 and K2 units in sources that can be queried by a script.

  K1 collocation (phrase in Vietnamese, the language the sentence is spoken in):
    vietmed_corpus   phrase occurs in a real VietMed-NER sentence (train/validation/test text)
    icd10_moh_vi     phrase occurs in a disease name of the MoH ICD-10 catalogue (TÊN BỆNH)
  K2 relation (English terms from en_terms.json):
    medrt            treated_by: RxClass MED-RT may_treat / may_prevent (supported) or CI_with (contradicted)
    rxnorm_strength  has_dosage with a strength in mg: the drug exists in RxNorm at that strength (SCD/SBD names)
    biotext / ade    head and tail English terms occur in the same sentence of the English corpora
  Units without a result here are left for the web search (WHO / NIH) in step 4.

Every lookup writes one line to evidence.jsonl (all fields in English):
  {"unit_id", "kind", "source", "query", "result": supported|not_found|contradicted, "url", "snippet"}

Run: .venv\\Scripts\\python.exe -X utf8 -m relation.validate.evidence
"""
import json
import re
import sqlite3
import sys
import time
from pathlib import Path

import pandas as pd
import requests

from .to_english import ICD_FILE
from .units import HERE, OUT, load

ROOT = HERE.parent
sys.path.insert(0, str(ROOT / "scripts" / "golden_test"))
from common import load_split  # noqa: E402

RXNAV = "https://rxnav.nlm.nih.gov/REST"
CACHE = OUT / "rxnav_cache.db"
# English dosage term -> pattern a matching RxNorm product name must contain (dose form / unit).
# Frequencies ("once daily") apply to a drug given systemically: an oral or injectable product.
DOSE_FORMS = {"tablet": r"Tablet", "ampoule": r"Inject|Ampule", "sachet": r"Granule|Powder|Packet|Oral Suspension",
              "units": r"\bUNT\b", "daily": r"Oral|Inject", "one dose": r"Oral|Inject"}


def norm(s):
    return re.sub(r"\s+", " ", re.sub(r"[^\w\s]", " ", s.lower())).strip()


def contains_phrase(text, phrase):
    return f" {phrase} " in f" {text} "


class RxNav:
    def __init__(self):
        self.db = sqlite3.connect(CACHE)
        self.db.execute("create table if not exists c (url text primary key, body text)")

    def get(self, path):
        url = f"{RXNAV}{path}"
        row = self.db.execute("select body from c where url=?", (url,)).fetchone()
        if row:
            return json.loads(row[0])
        for attempt in range(4):
            try:
                r = requests.get(url, timeout=20)
                if r.status_code == 200:
                    body = r.json()
                    self.db.execute("insert or replace into c values (?,?)", (url, json.dumps(body)))
                    self.db.commit()
                    return body
            except requests.RequestException:
                pass
            time.sleep(1.5 * (attempt + 1))
        return None

    def medrt(self, rxcui):
        """{rela: [disease names]} for one ingredient."""
        out = {}
        for rela in ("may_treat", "may_prevent", "CI_with"):
            body = self.get(f"/rxclass/class/byRxcui.json?rxcui={rxcui}&relaSource=MEDRT&relas={rela}") or {}
            items = (body.get("rxclassDrugInfoList") or {}).get("rxclassDrugInfo", [])
            out[rela] = sorted({i["rxclassMinConceptItem"]["className"] for i in items})
        return out

    def strengths(self, rxcui):
        body = self.get(f"/rxcui/{rxcui}/related.json?tty=SCD+SBD") or {}
        names = []
        for g in (body.get("relatedGroup") or {}).get("conceptGroup", []) or []:
            names += [p["name"] for p in g.get("conceptProperties", []) or []]
        return names


def disease_match(term, names):
    """English condition term vs MED-RT disease names (MeSH headings)."""
    t = set(norm(term).replace("disease", "").split())
    for n in names:
        w = set(norm(n).replace("disease", "").split())
        if t and (t <= w or w <= t):
            return n
    return None


def main():
    units = load(OUT / "units.jsonl")
    terms = json.loads((OUT / "en_terms.json").read_text(encoding="utf-8"))
    by_text = {}
    for k, v in terms.items():
        by_text.setdefault(v["vi"], v)

    corpus = [norm(r["text"]) for s in ("train", "validation", "test") for r in load_split(s)[0]]
    icd = pd.read_excel(ICD_FILE, sheet_name="ICD10", header=2, usecols=["TÊN BỆNH"])
    icd_vi = [norm(str(x)) for x in icd["TÊN BỆNH"].dropna().unique()]
    biotext = [norm(l) for l in open(ROOT / "data/external_en_raw/biotext/sentences_with_roles_and_relations",
                                     encoding="utf-8", errors="ignore")]
    ade = [norm(t) for t in pd.read_parquet(ROOT / "data/external_en_raw/ade/drug_dosage.parquet")["text"]]
    rx = RxNav()

    rows = []

    def ev(u, source, query, result, url=None, snippet=None):
        rows.append({"unit_id": u["unit_id"], "kind": u["kind"], "source": source, "query": query,
                     "result": result, "url": url, "snippet": snippet})

    for u in units:
        if u["kind"] == "K1":
            p = norm(u["phrase_vi"])
            n = sum(contains_phrase(t, p) for t in corpus)
            if n:
                ex = next(t for t in corpus if contains_phrase(t, p))
                ev(u, "vietmed_corpus", p, "supported", "https://huggingface.co/datasets/leduckhai/VietMed-NER",
                   f"{n} occurrence(s) in VietMed-NER, e.g. \"{ex[:160]}\"")
            hit = next((t for t in icd_vi if contains_phrase(t, p)), None)
            if hit:
                ev(u, "icd10_moh_vi", p, "supported", None, f"MoH ICD-10 disease name: \"{hit}\"")
            if not n and not hit:
                ev(u, "local", p, "not_found")
        elif u["kind"] == "K2":
            if u["seed_verified"]:
                ev(u, "seed_human_label", f"{u['head_vi']} {u['relation']} {u['tail_vi']}", "supported", None,
                   "same mention pair carries this relation in the human-reviewed seed")
                continue
            h = by_text.get(u["head_vi"], {})
            t = by_text.get(u["tail_vi"], {})
            he, te = h.get("en"), t.get("en")
            if not he or not te:
                ev(u, "to_english", f"{u['head_vi']} | {u['tail_vi']}", "not_found", None,
                   "entity is generic or has no English term")
                continue
            q = f"{he} {u['relation']} {te}"
            found = False
            if u["relation"] == "treated_by" and t.get("code_system") == "RxNorm":
                m = rx.medrt(t["code"])
                url = f"{RXNAV}/rxclass/class/byRxcui.json?rxcui={t['code']}&relaSource=MEDRT"
                ci = disease_match(he, m["CI_with"])
                ok = disease_match(he, m["may_treat"] + m["may_prevent"])
                if ci:
                    ev(u, "medrt", q, "contradicted", url, f"MED-RT: {te} CI_with \"{ci}\""); found = True
                elif ok:
                    ev(u, "medrt", q, "supported", url, f"MED-RT: {te} may_treat/may_prevent \"{ok}\""); found = True
                else:
                    ev(u, "medrt", q, "not_found", url,
                       f"MED-RT may_treat for {te}: {', '.join(m['may_treat'][:12]) or 'none'}")
            if u["relation"] == "has_dosage" and h.get("code_system") == "RxNorm":
                mg = re.match(r"(\d+) mg", te)
                form = next((pat for key, pat in DOSE_FORMS.items() if key in te), None)
                if form and not mg:
                    names = rx.strengths(h["code"])
                    hit = next((n for n in names if re.search(form, n, re.I)), None)
                    url = f"{RXNAV}/rxcui/{h['code']}/related.json?tty=SCD+SBD"
                    ev(u, "rxnorm_dose_form", q, "supported" if hit else "not_found", url,
                       f"RxNorm product: \"{hit}\"" if hit else f"no RxNorm product of {he} matching /{form}/")
                    found = found or bool(hit)
                if mg:
                    names = rx.strengths(h["code"])
                    hit = next((n for n in names if re.search(rf"\b{mg.group(1)} MG\b", n)), None)
                    url = f"{RXNAV}/rxcui/{h['code']}/related.json?tty=SCD+SBD"
                    if hit:
                        ev(u, "rxnorm_strength", q, "supported", url, f"RxNorm product: \"{hit}\""); found = True
                    else:
                        ev(u, "rxnorm_strength", q, "not_found", url,
                           f"no RxNorm product of {he} at {te}; e.g. {', '.join(names[:5])}")
            a, b = norm(he), norm(te)
            for name, sents in (("biotext", biotext), ("ade", ade)):
                s = next((x for x in sents if contains_phrase(x, a) and contains_phrase(x, b)), None)
                if s:
                    ev(u, name, q, "supported", None, f"\"{s[:200]}\""); found = True
            if not found:
                ev(u, "local", q, "not_found")

    with open(OUT / "evidence.jsonl", "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    status = {}
    for u in units:
        if u["kind"] == "K3":
            continue
        rs = [r["result"] for r in rows if r["unit_id"] == u["unit_id"]]
        s = "contradicted" if "contradicted" in rs else "supported" if "supported" in rs else "not_found"
        status[s, u["kind"]] = status.get((s, u["kind"]), 0) + 1
    print({f"{k}:{s}": n for (s, k), n in sorted(status.items())})


if __name__ == "__main__":
    main()

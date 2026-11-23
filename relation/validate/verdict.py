"""Step 6: combine evidence into one verdict per synthetic sentence, and write the expert review sheet.

Unit results
  K1 supported    a source has the phrase (VietMed corpus, MoH ICD-10 names), or the Claude judge says it is a
                  valid medical expression (source "claude_judge"); otherwise collocation_not_found.
  K2 supported    any source supports it (seed human label, MED-RT, RxNorm, BioText/ADE, WHO/NIH web search);
                  contradicted if a source contradicts it; unmapped if an entity has no English term.
  K3              plausible / implausible from the Claude judge, on a literal English translation.
Sentence verdict: VALID only if every K1 and K2 unit is supported and K3 is plausible; INVALID otherwise, with the
most severe reason: contradicted > implausible_context > collocation_not_found > relation_not_found > unmapped_entity.

Outputs (relation/data/synth/validate/):
  verdicts.jsonl, invalid.jsonl, summary.json, expert_review.xlsx (+ expert_review_key.json)
Expert sheet = every INVALID with a "not found" reason (they may be correct sentences) + 20% of VALID + 10% of
INVALID with a "wrong" reason, all chosen with a fixed seed. The two samples measure the precision of the verdicts.

Run: .venv\\Scripts\\python.exe -X utf8 -m relation.validate.verdict
"""
import json
import random
from collections import Counter, defaultdict

from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.worksheet.datavalidation import DataValidation

from .batches import BATCH
from .units import OUT, SYNTH, load

SEED = 20261121
SEVERITY = ["contradicted", "implausible_context", "collocation_not_found", "relation_not_found", "unmapped_entity"]
NOT_FOUND = {"collocation_not_found", "relation_not_found", "unmapped_entity"}
VALID_SAMPLE, WRONG_SAMPLE = 0.20, 0.10
NEGATIVE = "NO_RELATION"


def outputs(prefix, key):
    got = {}
    for f in sorted(BATCH.glob(f"{prefix}_b??.out.jsonl")):
        for line in open(f, encoding="utf-8"):
            if line.strip():
                r = json.loads(line)
                got[r[key]] = r
    return got


def main():
    pool = {r["id"]: r for r in load(SYNTH / "pool.jsonl")}
    units = {u["unit_id"]: u for u in load(OUT / "units.jsonl")}
    sent_units = {r["sentence_id"]: r["unit_ids"] for r in load(OUT / "sentence_units.jsonl")}
    evidence = defaultdict(list)
    for e in load(OUT / "evidence.jsonl"):
        evidence[e["unit_id"]].append(e)
    for uid, r in outputs("k2", "unit_id").items():
        evidence[uid].append({"unit_id": uid, "kind": "K2", "source": "web_who_nih", "query": r.get("query"),
                              "result": r["result"], "url": r.get("url"), "snippet": r.get("snippet")})
    judge = outputs("k3", "sentence_id")
    k1_judge = {k["unit_id"]: k for j in judge.values() for k in j.get("k1", [])}

    def unit_result(uid, sid):
        u, ev = units[uid], evidence.get(uid, [])
        if u["kind"] == "K1":
            if any(e["result"] == "supported" for e in ev):
                return "supported"
            j = k1_judge.get(uid)
            return "supported" if j and j.get("is_medical_expression") else "collocation_not_found"
        if u["kind"] == "K2":
            rs = {e["result"] for e in ev}
            if "contradicted" in rs:
                return "contradicted"
            if "supported" in rs:
                return "supported"
            if any(e["source"] == "to_english" for e in ev):
                return "unmapped_entity"
            return "relation_not_found"
        j = judge.get(sid)
        if not j:
            return "missing_judgement"
        return "supported" if j["k3"] == "plausible" else "implausible_context"

    verdicts, missing = [], 0
    for sid, row in pool.items():
        results = {uid: unit_result(uid, sid) for uid in sent_units[sid]}
        if "missing_judgement" in results.values():
            missing += 1
        bad = [r for r in results.values() if r in SEVERITY]
        reason = min(bad, key=SEVERITY.index) if bad else None
        j = judge.get(sid, {})
        verdicts.append({"sentence_id": sid, "method": row["method"],
                         "verdict": "INVALID" if reason or "missing_judgement" in results.values() else "VALID",
                         "reason": reason or ("missing_judgement" if "missing_judgement" in results.values() else None),
                         "units": results, "literal_en": j.get("literal_en"), "k3_rationale": j.get("k3_rationale")})
    if missing:
        print(f"WARNING: {missing} sentences have no K3 judgement yet")

    with open(OUT / "verdicts.jsonl", "w", encoding="utf-8") as f:
        for v in verdicts:
            f.write(json.dumps(v, ensure_ascii=False) + "\n")
    with open(OUT / "invalid.jsonl", "w", encoding="utf-8") as f:
        for v in verdicts:
            if v["verdict"] == "INVALID":
                f.write(json.dumps({**pool[v["sentence_id"]], "reason": v["reason"]}, ensure_ascii=False) + "\n")

    summary = {"sentences": len(verdicts), "verdict": dict(Counter(v["verdict"] for v in verdicts)),
               "reason": dict(Counter(v["reason"] for v in verdicts if v["reason"])),
               "by_method": {m: dict(Counter(v["verdict"] for v in verdicts if v["method"] == m))
                             for m in sorted({v["method"] for v in verdicts})},
               "valid_pairs_by_label": dict(sorted(Counter(
                   f"{x['allowed_relation']}:{'neg' if x['label'] == NEGATIVE else 'pos'}"
                   for v in verdicts if v["verdict"] == "VALID" for x in pool[v["sentence_id"]]["relations"]).items()))}

    # ---- expert sheet ----
    rng = random.Random(SEED)
    valid = [v for v in verdicts if v["verdict"] == "VALID"]
    wrong = [v for v in verdicts if v["reason"] in ("contradicted", "implausible_context")]
    notfound = [v for v in verdicts if v["reason"] in NOT_FOUND | {"missing_judgement"}]
    pick = ([(v, "all_not_found") for v in notfound]
            + [(v, "sample_valid") for v in rng.sample(valid, round(len(valid) * VALID_SAMPLE))]
            + [(v, "sample_wrong") for v in rng.sample(wrong, round(len(wrong) * WRONG_SAMPLE))])
    rng.shuffle(pick)
    summary["expert_sheet"] = dict(Counter(why for _, why in pick))
    write_sheet(pick, pool, units, evidence)
    (OUT / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=1))


def write_sheet(pick, pool, units, evidence):
    wb = Workbook()
    ws = wb.active
    ws.title = "review"
    cols = ["row", "sentence_id", "method", "parent_sentence_vi", "synthetic_sentence_vi", "literal_translation_en",
            "replaced (old -> new)", "pairs + labels", "K1 collocations", "K2 relations", "K3 context",
            "evidence (source | url | snippet)", "system_verdict", "system_reason",
            "expert_decision", "fixed_pairs", "expert_note"]
    ws.append(cols)
    for c in ws[1]:
        c.font = Font(bold=True, color="FFFFFF")
        c.fill = PatternFill("solid", fgColor="305496")
        c.alignment = Alignment(wrap_text=True, vertical="top")
    key = []
    for i, (v, why) in enumerate(pick, 1):
        row = pool[v["sentence_id"]]
        ents = {e["id"]: e for e in row["entities"]}
        pairs = "\n".join(f"{x['head']}-{x['tail']}: {ents[x['head']]['text']} -> {ents[x['tail']]['text']} = {x['label']}"
                          for x in row["relations"])
        k1, k2, evs = [], [], []
        for uid, res in v["units"].items():
            u = units[uid]
            if u["kind"] == "K1":
                k1.append(f"{u['phrase_vi']}: {res}")
            elif u["kind"] == "K2":
                k2.append(f"{u['head_vi']} {u['relation']} {u['tail_vi']}: {res}")
            for e in evidence.get(uid, []):
                if e["result"] != "not_found" or e["source"] not in ("local",):
                    evs.append(" | ".join(str(x) for x in (e["source"], e["result"], e.get("url") or "", e.get("snippet") or "")))
        rep = row.get("replaced")
        ws.append([i, row["id"], row["method"], row.get("parent_text") or "", row["text"], v.get("literal_en") or "",
                   f"{rep['old']} -> {rep['new']}" if rep else "", pairs, "\n".join(k1), "\n".join(k2),
                   f"{v['units'].get(next((u for u in v['units'] if u.startswith('K3')), ''), '')}: {v.get('k3_rationale') or ''}",
                   "\n".join(evs[:8]), v["verdict"], v["reason"] or "", "", "", ""])
        key.append({"row": i, "sentence_id": row["id"], "selected_as": why})
    dv = DataValidation(type="list", formula1='"KEEP,FIX_LABEL,DROP"', allow_blank=True)
    ws.add_data_validation(dv)
    dv.add(f"O2:O{len(pick) + 1}")
    widths = [5, 10, 14, 40, 40, 40, 20, 40, 28, 34, 34, 60, 10, 18, 14, 24, 24]
    for col, w in zip("ABCDEFGHIJKLMNOPQ", widths):
        ws.column_dimensions[col].width = w
    for r in ws.iter_rows(min_row=2):
        for c in r:
            c.alignment = Alignment(wrap_text=True, vertical="top")
    ws.freeze_panes = "F2"
    guide = wb.create_sheet("guide")
    for line in [
        "expert_decision: KEEP = sentence and labels are correct; DROP = sentence is not natural / not medically "
        "correct; FIX_LABEL = sentence is fine but a pair label is wrong -> write the corrected pairs in fixed_pairs.",
        "fixed_pairs format: E1-E2=located_at; E1-E3=NO_RELATION  (only the pairs you change)",
        "Relations: located_at, treated_by, treated_by_procedure, diagnosed_by, has_dosage, NO_RELATION",
        "system_reason *_not_found means no source was found, not that the sentence is wrong: please check carefully.",
    ]:
        guide.append([line])
    guide.column_dimensions["A"].width = 140
    wb.save(OUT / "expert_review.xlsx")
    (OUT / "expert_review_key.json").write_text(json.dumps(key, indent=0), encoding="utf-8")


if __name__ == "__main__":
    main()

r"""Bước Critic (phản biện) sau khi LLM gán nhãn: xem lại từng cặp đáng nghi, KEEP hoặc FLIP.

Cơ sở: Assi et al. (PromptEng'26) dùng Critic sau Extractor để giảm dương sai (1089 → 452). Ở đây
pilot cho thấy precision đã ~0,94 nhưng recall ~0,68, nên Critic xem chủ yếu các cặp ÂM có dấu hiệu
bị bỏ sót, cộng các cặp mà các lượt gọi bất đồng. Chọn cặp bằng code (không tốn API):
  - nhãn NO_RELATION và (K7: cặp này từng dương ở câu khác trong corpus; K6: luật RE nói dương;
    chữ của TAIL nằm trong chữ của HEAD, vd "xơ vữa động mạch" → "động mạch";
    located_at với bộ phận hay bị chuyên gia sửa: máu, tim, não, mạch, răng, xương);
  - hoặc votes không nhất trí.
Mỗi cặp một lượt gọi, prompt ngắn chỉ chứa luật của quan hệ đó (prompts/critic_v1.md). Nhãn ban đầu
được nêu trung lập ("người gán nhãn đã chọn") để giảm thiên hướng đồng ý. Chỉ nhận FLIP khi
confidence = high (trừ khi --accept-low).

  .venv\Scripts\python.exe -X utf8 -m re_v3.critic pilot_label_v4 --model gpt-5.4 --max-usd 1
Ghi ra re_v3/data/silver/<name>_critic/ (jsonl, manifest, Excel cho chuyên gia, cờ CRITIC_FLIP).
"""
import argparse
import json
from collections import Counter
from concurrent.futures import ThreadPoolExecutor

from relation_extraction.data import NEGATIVE

from . import config
from . import llm_rules as R
from .common import read_jsonl, write_jsonl
from .expert_review import write_xlsx
from .run_log import log_run
from .synth_llm import LLM, BudgetExceeded, load_prompt

OUT_DIR = config.SILVER_DIR
HOT_BODY = ("máu", "tim", "não", "mạch", "răng", "xương")
TYPE_VI = {"CONDITION": "bệnh/triệu chứng", "DRUG": "thuốc", "BODY_PART": "bộ phận", "TEST": "xét nghiệm",
           "PROCEDURE": "thủ thuật", "DOSAGE": "liều"}


def select(rec):
    """Trả về [(chỉ số quan hệ, [lý do])] cho các cặp cần Critic xem."""
    ents = {e["id"]: e for e in rec["entities"]}
    kbp = {(p["head"], p["tail"]): p for p in rec.get("kb_validation", {}).get("pairs", [])}
    out = []
    for i, x in enumerate(rec["relations"]):
        n, k = x["votes"].split("/")
        why = []
        if n != k:
            why.append("SC")
        if x["label"] == NEGATIVE:
            kb = kbp.get((x["head"], x["tail"]), {})
            if kb.get("K7", {}).get("support", 0) > 0:
                why.append("K7")
            if kb.get("K6", {}).get("rule_label", NEGATIVE) != NEGATIVE:
                why.append("K6")
            h, t = ents[x["head"]]["text"], ents[x["tail"]]["text"]
            if t in h:
                why.append("in_name")
            if x["allowed_relation"] == "located_at" and any(w in t.split() for w in HOT_BODY):
                why.append("hot_body")
        if why:
            out.append((i, why))
    return out


def tag_pair(text, h, t):
    spans = sorted([(h["start"], h["end"], "HEAD"), (t["start"], t["end"], "TAIL")])
    s, last = [], 0
    for a, b, name in spans:
        s += [text[last:a], f"[{name}]", text[a:b], f"[/{name}]"]
        last = b
    return "".join(s + [text[last:]])


def messages(rec, x, tpl, version):
    rs = R.RULESETS[version]
    ents = {e["id"]: e for e in rec["entities"]}
    h, t = ents[x["head"]], ents[x["tail"]]
    f = {"general_rules": rs["general"], "relation_rule": rs["relation"][x["allowed_relation"]],
         "tagged": tag_pair(rec["text"], h, t), "head": h["text"], "tail": t["text"],
         "head_type": TYPE_VI.get(h["label"], h["label"]), "tail_type": TYPE_VI.get(t["label"], t["label"]),
         "relation": x["allowed_relation"], "label": x["label"], "evidence": x.get("evidence") or "(không có)"}
    return [{"role": "system", "content": tpl[0].substitute(f)}, {"role": "user", "content": tpl[1].substitute(f)}]


def apply(rec, i, why, resp, accept_low, stats):
    x = rec["relations"][i]
    stats["checked"] += 1
    if not resp or "_bad_json" in resp:
        stats["no_response"] += 1
        return
    lab = resp.get("label") if resp.get("label") in (x["allowed_relation"], NEGATIVE) else x["label"]
    x["critic"] = {"why": why, "decision": resp.get("decision"), "label": lab, "confidence": resp.get("confidence"),
                   "evidence": resp.get("evidence"), "rule": resp.get("rule")}
    if lab == x["label"]:
        return
    if resp.get("confidence") != "high" and not accept_low:
        stats["flip_low_conf_ignored"] += 1
        return
    stats[f"flip:{x['label']}->{lab}"] += 1
    x["label_before_critic"], x["label"], x["label_source"] = x["label"], lab, "critic_flip"
    if lab != NEGATIVE and resp.get("evidence"):
        x["evidence"] = resp["evidence"]
    kv = rec.setdefault("kb_validation", {})
    kv.setdefault("flags", []).append(f"CRITIC_FLIP:{x['head']}-{x['tail']}")
    kv["tier"] = "B"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("name", help="thư mục kết quả gán nhãn, vd pilot_label_v4")
    ap.add_argument("--model", default="gpt-5.4")
    ap.add_argument("--rules", default="v4")
    ap.add_argument("--max-usd", type=float, default=1.0)
    ap.add_argument("--seed", type=int, default=config.SEED)
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--accept-low", action="store_true", help="nhận cả FLIP có confidence low")
    args = ap.parse_args()

    recs = read_jsonl(OUT_DIR / args.name / f"{args.name}.jsonl")
    jobs = [(r, i, why) for r in recs for i, why in select(r)]
    llm = LLM(config.SYNTHETIC_DIR / "llm_cache.jsonl", max_usd=args.max_usd)
    tpl = load_prompt("critic", "v1")

    def run(job):
        rec, i, _ = job
        try:
            return llm(messages(rec, rec["relations"][i], tpl, args.rules), args.model, 0.0, args.seed)
        except BudgetExceeded:
            return None

    with ThreadPoolExecutor(args.workers) as pool:
        resps = list(pool.map(run, jobs))
    stats = Counter()
    for (rec, i, why), resp in zip(jobs, resps):
        apply(rec, i, why, resp, args.accept_low, stats)
    for r in recs:
        r["annotator"] = r.get("annotator", "") + f" + critic_v1 {args.model}"

    out = f"{args.name}_critic"
    d = OUT_DIR / out
    d.mkdir(parents=True, exist_ok=True)
    files = {"jsonl": d / f"{out}.jsonl", "xlsx": d / f"{out}_expert_review.xlsx", "manifest": d / f"{out}.manifest.json"}
    write_jsonl(files["jsonl"], recs)
    write_xlsx(files["xlsx"], recs, a_fraction=1.0, seed=args.seed, title=f"Duyệt nhãn quan hệ y khoa: {out}")
    manifest = {"source": args.name, "model": args.model, "rules": args.rules, "prompt_version": "critic_v1",
                "pairs": sum(len(r["relations"]) for r in recs), "selected": len(jobs),
                "why": dict(Counter(w for _, _, why in jobs for w in why)), "stats": dict(stats),
                "usage": {"usd_this_run": round(llm.spent, 4), "api_calls": llm.usage.get("api_calls", 0)}}
    files["manifest"].write_text(json.dumps(manifest, ensure_ascii=False, indent=1), encoding="utf-8")
    log_run("re_v3.critic", args, manifest, d, files)
    print(json.dumps(manifest, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()

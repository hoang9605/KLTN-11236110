r"""Gán nhãn RE cho câu VietMed thật bằng LLM (OpenAI API), rồi kiểm tra K1–K7, rồi đưa chuyên gia.

Phương pháp (xem docs/PHUONG_PHAP_SINH_VA_GAN_NHAN_RE.md):
  1. Thực thể lấy từ nhãn NER gốc (không để LLM tự NER). Cặp ứng viên sinh bằng code theo lược đồ.
  2. Prompt = hướng dẫn gán nhãn đã khóa (prompts/verify_vN.md), chỉ chèn luật của các quan hệ có trong câu.
  3. Self-consistency thích ứng (Wang et al. 2023; Aggarwal et al. 2023): lượt 1 (nhiệt độ 0) cho mọi câu;
     lượt 2 (nhiệt độ 0,7) chỉ khi câu đáng nghi (có cặp dương hoặc luật RE bất đồng); lượt 3 chỉ khi
     lượt 1 và 2 bất đồng. Nhãn cuối = đa số. --no-adaptive để luôn gọi đủ k lượt.
  4. Kiểm tra bằng từ điển và công cụ K1–K7 (validate_kb.py).
  5. Phân tầng: B = có lượt bất đồng hoặc có cờ K → chuyên gia duyệt hết; A = còn lại → duyệt mẫu.
     (Phân bổ theo độ bất định như CoAnnotating, Li et al. 2023.)

Chạy:
  .venv\Scripts\python.exe -X utf8 -m re_v3.label_llm --split dev --dry-run
  .venv\Scripts\python.exe -X utf8 -m re_v3.label_llm --split train --limit 300 --name pilot_label_v1
  .venv\Scripts\python.exe -X utf8 -m re_v3.label_llm --split test --name test_label_v1 --a-fraction 1.0
"""
import argparse
import json
import random
from collections import Counter
from concurrent.futures import ThreadPoolExecutor

from relation_extraction.data import NEGATIVE
from relation_extraction.rules import predict_pair

from . import config
from .common import read_jsonl, write_jsonl
from .expert_review import write_xlsx
from .run_log import log_run
from .synth_llm import (DEFAULT_MODEL, LLM, PROMPT_VERSION, SPLIT_DIR, BudgetExceeded, load_prompt,
                        verify_messages)

OUT_DIR = config.SILVER_DIR


def vote(responses, entities, pairs):
    """Gộp k phản hồi: đa số cho validity của từng thực thể và nhãn của từng cặp."""
    ents_v, pairs_v, evidence = {}, {}, {}
    for e in entities:
        c = Counter(next((x.get("validity") for x in r.get("entities", []) if x.get("id") == e["id"]), None)
                    for r in responses)
        ents_v[e["id"]] = c
    for p in pairs:
        c = Counter()
        for r in responses:
            hit = next((x for x in r.get("pairs", []) if x.get("pair_id") == p["id"]), None)
            lab = hit.get("label") if hit else None
            if lab not in (p["allowed_relation"], NEGATIVE):
                lab = None
            c[lab] += 1
            if hit and lab and hit.get("evidence"):
                evidence.setdefault((p["id"], lab), hit["evidence"])
        pairs_v[p["id"]] = c
    return ents_v, pairs_v, evidence


def _labels(resp):
    return {(x.get("pair_id"), x.get("label")) for x in resp.get("pairs", [])} | \
           {(x.get("id"), x.get("validity")) for x in resp.get("entities", [])}


def disagree(a, b):
    return _labels(a) != _labels(b)


def suspicious(row, resp):
    """Lượt 1 đáng nghi khi có cặp dương, hoặc luật RE của repo cho nhãn khác LLM ở bất kỳ cặp nào."""
    ents = {e["id"]: e for e in row["entities"]}
    got = {x.get("pair_id"): x.get("label") for x in resp.get("pairs", [])}
    for p in row["pairs"]:
        lab = got.get(p["id"])
        if lab and lab != NEGATIVE:
            return True
        rule = predict_pair(row["text"], ents[p["head"]], ents[p["tail"]], p["allowed_relation"], row["entities"])
        if rule != (lab or NEGATIVE):
            return True
    return False


def label_row(row, llm, tpl, args):
    try:
        return _label_row(row, llm, tpl, args)
    except BudgetExceeded:
        return {"row": row, "status": "BUDGET"}


def _label_row(row, llm, tpl, args):
    pairs = row["pairs"]
    msgs = verify_messages(row["text"], row["entities"], pairs, tpl, getattr(args, "prompt_version", "v1"))
    responses = []

    def ask(i):
        r = llm(msgs, args.model, 0.0 if i == 0 else args.temperature, args.seed + i)
        if r is not None and "_bad_json" not in r:
            responses.append(r)
        return r

    if getattr(args, "adaptive", False):
        # Gọi thích ứng (tiết kiệm API): lượt 1 cho mọi câu; lượt 2 chỉ khi câu đáng nghi
        # (có cặp dương, hoặc luật RE bất đồng với LLM); lượt 3 chỉ khi lượt 1 và 2 bất đồng.
        if ask(0) is None:
            return {"row": row, "status": "DRY_RUN"}
        if responses and suspicious(row, responses[0]):
            ask(1)
            if len(responses) == 2 and disagree(responses[0], responses[1]):
                ask(2)
    else:
        for i in range(args.k):
            if ask(i) is None:
                return {"row": row, "status": "DRY_RUN"}
    if not responses:
        return {"row": row, "status": "BAD_JSON"}
    ents_v, pairs_v, evidence = vote(responses, row["entities"], pairs)
    n = len(responses)
    entities = []
    for e in row["entities"]:
        top, cnt = ents_v[e["id"]].most_common(1)[0]
        entities.append(dict({k: e[k] for k in ("id", "label", "start", "end", "text")},
                             validity=top or "INVALID", validity_votes=f"{cnt}/{n}"))
    valid = {e["id"] for e in entities if e["validity"] == "VALID"}
    relations, pair_dis = [], []
    for p in pairs:
        if p["head"] not in valid or p["tail"] not in valid:
            continue
        top, cnt = pairs_v[p["id"]].most_common(1)[0]
        top = top or NEGATIVE
        if cnt < n:
            pair_dis.append(p["id"])
        relations.append({"head": p["head"], "tail": p["tail"], "allowed_relation": p["allowed_relation"],
                          "label": top, "label_source": "llm_majority", "votes": f"{cnt}/{n}",
                          "evidence": evidence.get((p["id"], top), "")})
    ent_disagree = [e["id"] for e in entities if not e["validity_votes"].startswith(f"{n}/")]
    rec = {"id": row["id"], "source": row["source"], "source_split": row["source_split"],
           "source_row_index": row["source_row_index"], "split": row["split"], "text": row["text"],
           "entities": entities, "relations": relations,
           "annotation_status": "LLM_LABELED", "annotator": f"re_v3/label_llm.py prompt {getattr(args, 'prompt_version', 'v1')}, {args.model}, k={args.k}",
           "human_verified": False, "self_consistency": {"k": n, "pair_disagree": pair_dis, "entity_disagree": ent_disagree},
           "parent_id": row["id"]}
    return {"row": row, "status": "OK", "record": rec}


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--split", choices=("train", "dev", "test"), default="train")
    ap.add_argument("--limit", type=int, default=0, help="số câu (lấy ngẫu nhiên có seed), 0 = tất cả câu có cặp")
    ap.add_argument("--name", default="pilot_label_v1")
    ap.add_argument("--model", default=DEFAULT_MODEL)
    ap.add_argument("--prompt-version", default=PROMPT_VERSION, choices=("v1", "v2", "v3", "v4"),
                    help="bộ luật + prompt verify_vN.md (v2: chỉnh theo chuyên gia chấm pilot v1)")
    ap.add_argument("--k", type=int, default=3, help="số lượt self-consistency khi tắt --adaptive")
    ap.add_argument("--no-adaptive", dest="adaptive", action="store_false",
                    help="tắt gọi thích ứng: luôn gọi đủ k lượt cho mọi câu (tốn API gấp k lần)")
    ap.add_argument("--temperature", type=float, default=0.7)
    ap.add_argument("--seed", type=int, default=config.SEED)
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--ner", action="store_true")
    ap.add_argument("--online-rxnorm", action="store_true")
    ap.add_argument("--a-fraction", type=float, default=None,
                    help="tỉ lệ tầng A đưa chuyên gia; mặc định 1.0 cho dev/test, 0.2 cho train")
    ap.add_argument("--dry-run", action="store_true", help="không gọi API: ghi prompt mẫu và đếm số câu")
    ap.add_argument("--check", action="store_true",
                    help="gọi API cho đúng 1 câu: kiểm tra khóa, xem phản hồi, ước tính chi phí cả lần chạy")
    ap.add_argument("--max-usd", type=float, default=5.0,
                    help="trần chi phí cho lần chạy này (USD); chạm trần thì dừng gọi, chạy lại sẽ dùng cache")
    ap.add_argument("--price-in", type=float, help="giá USD / 1M token vào (mặc định theo bảng PRICES)")
    ap.add_argument("--price-out", type=float, help="giá USD / 1M token ra")
    args = ap.parse_args()
    price = (args.price_in, args.price_out) if args.price_in is not None and args.price_out is not None else None

    rows = [r for r in read_jsonl(SPLIT_DIR / f"{args.split}.jsonl") if r["pairs"]]
    if args.limit:
        rows = sorted(random.Random(args.seed).sample(rows, min(args.limit, len(rows))), key=lambda r: r["id"])
    out_dir = OUT_DIR / args.name
    out_dir.mkdir(parents=True, exist_ok=True)
    tpl = load_prompt("verify", args.prompt_version)
    if args.dry_run:
        msgs = verify_messages(rows[0]["text"], rows[0]["entities"], rows[0]["pairs"], tpl, args.prompt_version)
        (out_dir / "dry_run_prompt.md").write_text(f"## system\n\n{msgs[0]['content']}\n\n## user\n\n{msgs[1]['content']}\n",
                                                   encoding="utf-8")
        print(f"{len(rows)} câu, {sum(len(r['pairs']) for r in rows)} cặp. Prompt mẫu: {out_dir / 'dry_run_prompt.md'}")
        return

    llm = LLM(config.SYNTHETIC_DIR / "llm_cache.jsonl", max_usd=args.max_usd, price=price)
    if args.check:
        row = rows[0]
        msgs = verify_messages(row["text"], row["entities"], row["pairs"], tpl, args.prompt_version)
        before = dict(llm.usage)
        resp = llm(msgs, args.model, 0.0, args.seed)
        pt = llm.usage.get(f"{args.model}:prompt_tokens", 0) - before.get(f"{args.model}:prompt_tokens", 0)
        ct = llm.usage.get(f"{args.model}:completion_tokens", 0) - before.get(f"{args.model}:completion_tokens", 0)
        print("Câu:", row["text"])
        print("Phản hồi:", json.dumps(resp, ensure_ascii=False, indent=1))
        if pt == 0:
            print("(lấy từ cache, không tốn token; đổi --seed hoặc câu khác để đo token thật)")
            return
        one = llm.cost(args.model, pt, ct)
        per_pair_in = pt / max(1, len(row["pairs"]))
        calls = 1.6 if args.adaptive else args.k      # thích ứng: ước khoảng 1,6 lượt/câu (chưa đo, xem manifest sau pilot)
        total = sum(llm.cost(args.model, pt - per_pair_in * (len(row["pairs"]) - len(r["pairs"])), ct) for r in rows) * calls
        print(f"Một lượt gọi: {pt} token vào, {ct} token ra, ~{one:.4f} USD")
        print(f"Ước tính cả lần chạy ({len(rows)} câu, ~{calls} lượt/câu): ~{total:.2f} USD "
              f"(trần hiện tại --max-usd {args.max_usd})")
        return
    with ThreadPoolExecutor(args.workers) as pool:
        results = list(pool.map(lambda r: label_row(r, llm, tpl, args), rows))
    stopped = [r["row"]["id"] for r in results if r["status"] == "BUDGET"]
    if stopped:
        (out_dir / "chua_gan_do_het_ngan_sach.txt").write_text("\n".join(stopped), encoding="utf-8")

    from .validate_kb import KBValidator
    kb = KBValidator(use_ner=args.ner, online_rxnorm=args.online_rxnorm)
    records = []
    for res in results:
        if res["status"] != "OK":
            continue
        rec = res["record"]
        v = kb.validate(rec, target=None, exclude_ids=[rec["id"]])
        sc = rec["self_consistency"]
        v["flags"] += [f"SC_pair_disagree:{p}" for p in sc["pair_disagree"]]
        v["flags"] += [f"SC_entity_disagree:{e}" for e in sc["entity_disagree"]]
        # câu thật không bị loại: lỗi cứng chỉ là dấu hiệu thực thể INVALID, chuyên gia quyết định
        v["tier"] = "B" if v["flags"] else "A"
        rec["kb_validation"] = v
        records.append(rec)

    a_frac = args.a_fraction if args.a_fraction is not None else (1.0 if args.split in ("dev", "test") else 0.2)
    write_jsonl(out_dir / f"{args.name}.jsonl", records)
    xlsx = out_dir / f"{args.name}_expert_review.xlsx"
    review = write_xlsx(xlsx, records, a_fraction=a_frac, seed=args.seed,
                        title=f"Duyệt nhãn quan hệ y khoa: {args.split}, {args.name}")
    rels = Counter(f"{x['allowed_relation']}|{x['label']}" for r in records for x in r["relations"])
    manifest = {
        "prompt_version": args.prompt_version, "model": args.model, "k": args.k, "adaptive": args.adaptive,
        "calls_per_sentence": round(llm.usage.get("api_calls", 0) / max(1, len(rows)), 2), "temperature": args.temperature,
        "seed": args.seed, "split": args.split, "sentences": len(rows), "labeled": len(records),
        "failed": dict(Counter(r["status"] for r in results if r["status"] != "OK")),
        "pairs": sum(len(r["relations"]) for r in records), "labels": dict(rels),
        "pair_unanimous_rate": round(sum(x["votes"].split("/")[0] == x["votes"].split("/")[1]
                                         for r in records for x in r["relations"]) /
                                     max(1, sum(len(r["relations"]) for r in records)), 3),
        "tiers": dict(Counter(r["kb_validation"]["tier"] for r in records)),
        "flags": dict(Counter(f.split(":")[0] for r in records for f in r["kb_validation"]["flags"])),
        "expert_a_fraction": a_frac,
        "expert_rows": {f"tier={t}|sample={s}": n for (t, s), n in review.items()},
        "usage": dict(llm.usage),
    }
    manifest["budget_stopped_sentences"] = len(stopped)
    (out_dir / f"{args.name}.manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=1), encoding="utf-8")
    log_run("re_v3.label_llm", args, manifest, out_dir, {
        "nhãn AI (jsonl)": out_dir / f"{args.name}.jsonl", "Excel cho chuyên gia": xlsx,
        "manifest": out_dir / f"{args.name}.manifest.json", "phản hồi API thô": llm.cache_path})
    print(json.dumps(manifest, ensure_ascii=False, indent=1))
    print(f"\nĐã chi ~{llm.spent:.2f} USD trong lần chạy này. Kết quả: {out_dir}")
    print(f"Excel cho chuyên gia: {xlsx}")
    if stopped:
        print(f"CHẠM TRẦN NGÂN SÁCH: còn {len(stopped)} câu chưa gán. Chạy lại cùng lệnh với --max-usd lớn hơn; "
              "phần đã gán lấy từ cache, không tốn thêm.")


if __name__ == "__main__":
    main()

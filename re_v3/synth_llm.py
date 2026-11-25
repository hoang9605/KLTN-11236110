r"""(C) Sinh dữ liệu RE bằng LLM (OpenAI API), seed là các câu có cặp trong train của split 8:1:1.

Cách sinh: viết lại có điều kiện nhãn. Mỗi job = (câu seed, cặp đích, nhãn đích, kiểu mẫu).
  1. LLM sinh (prompts/gen_vN.md) viết lại câu seed sao cho cặp đích mang đúng nhãn đích.
     Nhãn đến từ yêu cầu, không phải do LLM tự đoán, nên câu seed không cần có nhãn trước.
  2. Rule bằng code V1–V8 (llm_rules.check_generation): thẻ, giữ thực thể, không thêm thực thể,
     văn phong, khác câu gốc, từ đặc trưng của kiểu mẫu, khoảng cách, rò rỉ dev/test.
  3. LLM kiểm tra (prompts/verify_vN.md) gán nhãn MÙ: không thấy nhãn đích, gán mọi thực thể
     (VALID/INVALID) và mọi cặp ứng viên trong câu mới.
  4. Giữ câu khi: hai thực thể đích VALID và nhãn mù của cặp đích = nhãn đích.
     Các cặp khác trong câu lấy nhãn mù (label_source = verifier); cặp có thực thể INVALID bị bỏ.
  5. Xuất CSV cho chuyên gia duyệt. Dữ liệu chỉ được dùng huấn luyện sau khi chuyên gia duyệt.

Seed chỉ lấy từ train. Dev/test của split và các tập test cũ chỉ dùng để kiểm tra rò rỉ.

Chạy (PowerShell, từ gốc repo):
  # xem prompt, không gọi API
  .venv\Scripts\python.exe -X utf8 -m re_v3.synth_llm --pos 4 --neg 6 --dry-run
  # pilot: 20 dương + 30 âm mỗi quan hệ
  $env:OPENAI_API_KEY = "..."
  .venv\Scripts\python.exe -X utf8 -m re_v3.synth_llm --pos 20 --neg 30 --name pilot_v1
  # chạy đủ sau khi đã chốt prompt
  .venv\Scripts\python.exe -X utf8 -m re_v3.synth_llm --pos 300 --neg 450 --name llm_v1
"""
import argparse
import hashlib
import json
import os
import random
import threading
import time
import urllib.error
import urllib.request
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from string import Template

from relation_extraction.data import NEGATIVE, RELATIONS, candidates, is_guideline_invalid

from . import config, llm_rules as R
from .common import read_jsonl, write_jsonl
from .expert_review import write_xlsx
from .run_log import log_run
from .filter_synth import test_index

PROMPT_VERSION = "v1"
PROMPTS_DIR = config.HERE / "prompts"
SPLIT_DIR = config.ROOT / "data" / "re_vietmed_811_v1"
SEED_FILE = SPLIT_DIR / "train.jsonl"
LEAK_FILES = [SPLIT_DIR / "dev.jsonl", SPLIT_DIR / "test.jsonl", *config.TEST_FILES]
DEFAULT_MODEL = "gpt-4o-2024-08-06"
API_URL = os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1").rstrip("/") + "/chat/completions"


# ---------------------------------------------------------------------------
# Prompt
# ---------------------------------------------------------------------------
def load_prompt(kind, version=PROMPT_VERSION):
    raw = (PROMPTS_DIR / f"{kind}_{version}.md").read_text(encoding="utf-8")
    system, user = raw.split("=== USER ===", 1)
    return Template(system.strip()), Template(user.strip())


def gen_messages(job, tpl):
    v = R.variant(job["relation"], job["variant"])
    ents = {e["id"]: e for e in job["seed_entities"]}
    h, t = ents[job["head"]], ents[job["tail"]]
    fields = {
        "general_rules": R.GENERAL_RULES, "relation_rules": R.RELATION_RULES[job["relation"]],
        "variant_code": v["code"], "variant_desc": v["desc"], "variant_example": v["example"],
        "seed_tagged": R.tag_sentence(job["seed_text"], job["seed_entities"]),
        "head_id": h["id"], "head_text": h["text"], "head_type": h["label"],
        "tail_id": t["id"], "tail_text": t["text"], "tail_type": t["label"],
        "relation": job["relation"], "target_label": job["target_label"], "speaker": job["speaker"],
    }
    return [{"role": "system", "content": tpl[0].substitute(fields)},
            {"role": "user", "content": tpl[1].substitute(fields)}]


def verify_messages(text, entities, pairs, tpl, version="v1"):
    rs = R.RULESETS[version]
    present = sorted({p["allowed_relation"] for p in pairs}, key=list(RELATIONS).index)
    by_id = {e["id"]: e for e in entities}
    pair_list = "\n".join(
        f'{p["id"]}: [{p["head"]}] "{by_id[p["head"]]["text"]}" → [{p["tail"]}] "{by_id[p["tail"]]["text"]}"'
        f' | quan hệ có thể: {p["allowed_relation"]}' for p in pairs)
    fields = {"entity_rules": rs["entity"], "general_rules": rs["general"],
              "relation_rules": "\n\n".join(rs["relation"][r] for r in present),
              "tagged": R.tag_sentence(text, entities), "pair_list": pair_list}
    return [{"role": "system", "content": tpl[0].substitute(fields)},
            {"role": "user", "content": tpl[1].substitute(fields)}]


# ---------------------------------------------------------------------------
# OpenAI + cache
# ---------------------------------------------------------------------------
# Giá USD cho 1 triệu token (vào, ra). Theo bảng giá OpenAI mà mình biết; KIỂM TRA LẠI trên
# https://openai.com/api/pricing trước khi chạy, hoặc truyền --price-in / --price-out.
PRICES = {
    "gpt-4o-2024-08-06": (2.50, 10.00), "gpt-4o": (2.50, 10.00),
    "gpt-4o-mini": (0.15, 0.60), "gpt-4o-mini-2024-07-18": (0.15, 0.60),
    "gpt-4.1": (2.00, 8.00), "gpt-4.1-mini": (0.40, 1.60),
    # theo các trang tổng hợp giá 2026 (chưa đối chiếu trang chính thức)
    "gpt-5.4-mini": (0.75, 4.50), "gpt-5.4": (2.50, 15.00), "gpt-5.5": (5.00, 30.00),
}
REASONING_EFFORT = os.environ.get("RE_REASONING_EFFORT", "low")


def is_reasoning(model):
    return model.startswith(("gpt-5", "gpt-6", "o1", "o3", "o4"))


class BudgetExceeded(RuntimeError):
    """Đã chạm trần --max-usd: không gọi API thêm. Phần đã gọi vẫn nằm trong cache."""


def load_dotenv(path=config.ROOT / ".env"):
    """Đọc OPENAI_API_KEY từ file .env ở gốc repo (đã có trong .gitignore) nếu biến môi trường chưa có."""
    if os.environ.get("OPENAI_API_KEY") or not Path(path).exists():
        return
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        k, _, v = line.partition("=")
        if k.strip() == "OPENAI_API_KEY" and v.strip():
            os.environ["OPENAI_API_KEY"] = v.strip().strip('"').strip("'")


class LLM:
    """Gọi Chat Completions, JSON mode. Mọi phản hồi được cache theo hash(model, nhiệt độ, messages).

    max_usd: trần chi phí cho LẦN CHẠY này (chỉ tính lượt gọi thật, không tính cache). Khi chạm trần,
    mọi lượt gọi mới ném BudgetExceeded; chạy lại cùng lệnh sẽ dùng cache cho phần đã xong.
    """

    def __init__(self, cache_path, dry_run=False, max_usd=None, price=None):
        self.cache_path = Path(cache_path)
        self.dry_run = dry_run
        self.lock = threading.Lock()
        self.cache = {}
        self.usage = Counter()
        self.max_usd = max_usd
        self.price = price            # (in, out) USD / 1M token; None = tra PRICES theo model
        self.spent = 0.0
        if self.cache_path.exists():
            for row in read_jsonl(self.cache_path):
                self.cache[row["key"]] = row
        load_dotenv()
        self.key = os.environ.get("OPENAI_API_KEY")
        if not dry_run and not self.key:
            raise SystemExit("Chưa có OPENAI_API_KEY: đặt biến môi trường hoặc ghi vào file .env ở gốc repo "
                             "(OPENAI_API_KEY=sk-...). Dùng --dry-run để chỉ xem prompt.")

    def cost(self, model, prompt_tokens, completion_tokens):
        pin, pout = self.price or PRICES.get(model, PRICES["gpt-4o"])
        return (prompt_tokens * pin + completion_tokens * pout) / 1e6

    def __call__(self, messages, model, temperature, seed):
        payload = {"model": model, "messages": messages, "response_format": {"type": "json_object"}}
        if is_reasoning(model):
            # gpt-5.x / o-series: không nhận temperature, seed; độ ngẫu nhiên giữa các lượt là mặc định của model
            payload["reasoning_effort"] = REASONING_EFFORT
        else:
            payload.update(temperature=temperature, seed=seed)
        # khóa cache luôn gồm temperature + seed, để các lượt self-consistency không trùng nhau trong cache
        key_src = dict(payload, _temperature=temperature, _seed=seed)
        key = hashlib.sha256(json.dumps(key_src, ensure_ascii=False, sort_keys=True).encode()).hexdigest()
        if key in self.cache:
            self.usage["cache_hits"] += 1
            return json.loads(self.cache[key]["content"])
        if self.dry_run:
            return None
        if self.max_usd is not None and self.spent >= self.max_usd:
            raise BudgetExceeded(f"đã chi {self.spent:.2f} USD >= trần {self.max_usd} USD")
        req = urllib.request.Request(API_URL, data=json.dumps(payload).encode("utf-8"), method="POST",
                                     headers={"Authorization": f"Bearer {self.key}", "Content-Type": "application/json"})
        for attempt in range(6):
            try:
                with urllib.request.urlopen(req, timeout=120) as resp:
                    body = json.loads(resp.read().decode("utf-8"))
                break
            except urllib.error.HTTPError as exc:
                if exc.code in (429, 500, 502, 503, 504) and attempt < 5:
                    time.sleep(2 ** attempt + random.random())
                    continue
                raise RuntimeError(f"OpenAI HTTP {exc.code}: {exc.read().decode('utf-8', 'replace')[:500]}")
            except (urllib.error.URLError, TimeoutError):
                if attempt < 5:
                    time.sleep(2 ** attempt + random.random())
                    continue
                raise
        content = body["choices"][0]["message"]["content"]
        u = body.get("usage", {})
        row = {"key": key, "model": body.get("model", model), "system_fingerprint": body.get("system_fingerprint"),
               "content": content, "usage": u, "request": payload}
        with self.lock:
            self.cache[key] = row
            self.usage["api_calls"] += 1
            self.usage[f"{model}:prompt_tokens"] += u.get("prompt_tokens", 0)
            self.usage[f"{model}:completion_tokens"] += u.get("completion_tokens", 0)
            self.spent += self.cost(model, u.get("prompt_tokens", 0), u.get("completion_tokens", 0))
            self.usage["usd_this_run"] = round(self.spent, 4)
            self.cache_path.parent.mkdir(parents=True, exist_ok=True)
            with self.cache_path.open("a", encoding="utf-8") as fh:
                fh.write(json.dumps(row, ensure_ascii=False) + "\n")
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            return {"_bad_json": content}


# ---------------------------------------------------------------------------
# Lập job
# ---------------------------------------------------------------------------
def load_seeds(path=SEED_FILE):
    seeds = []
    for row in read_jsonl(path):
        if row.get("split") != "train":
            raise ValueError(f"{row['id']}: seed phải thuộc train")
        if row["pairs"]:
            seeds.append(row)
    return seeds


def plan_jobs(seeds, n_pos, n_neg, rng, oversample=1.5, max_uses=2):
    """Mỗi quan hệ: n_pos job dương và n_neg job âm (nhân oversample vì sẽ có job bị loại).

    Kiểu mẫu xoay vòng đều. Mỗi (câu seed, cặp) dùng tối đa max_uses lần cho mỗi phân cực.
    """
    by_rel = defaultdict(list)
    for s in seeds:
        ents = {e["id"]: e for e in s["entities"]}
        for p in s["pairs"]:
            if is_guideline_invalid(ents[p["head"]]) or is_guideline_invalid(ents[p["tail"]]):
                continue                     # thực thể đã biết là INVALID theo guideline: khỏi tốn API
            by_rel[p["allowed_relation"]].append((s, p))
    jobs = []
    for rel in RELATIONS:
        pool = sorted(by_rel[rel], key=lambda sp: (sp[0]["id"], sp[1]["id"]))
        for polarity, n in (("POS", n_pos), ("NEG", n_neg)):
            codes = [v[0] for v in R.VARIANTS[rel] if v[1] == polarity]
            want = int(round(n * oversample))
            order = []
            for _ in range(max_uses):
                rng.shuffle(pool)
                order += pool
            for i, (s, p) in enumerate(order[:want]):
                jobs.append({
                    "job_id": f"{rel}-{polarity}-{i:04d}", "relation": rel, "polarity": polarity,
                    "variant": codes[i % len(codes)],
                    "target_label": rel if polarity == "POS" else NEGATIVE,
                    "seed_id": s["id"], "seed_text": s["text"], "seed_entities": s["entities"],
                    "head": p["head"], "tail": p["tail"], "speaker": rng.choice(R.SPEAKERS),
                })
    return jobs


# ---------------------------------------------------------------------------
# Chạy một job
# ---------------------------------------------------------------------------
def run_job(job, llm, tpl_gen, tpl_ver, args, leak):
    try:
        return _run_job(job, llm, tpl_gen, tpl_ver, args, leak)
    except BudgetExceeded:
        return {"job": job, "status": "BUDGET", "reasons": ["BUDGET"]}


def _run_job(job, llm, tpl_gen, tpl_ver, args, leak):
    out = {"job": job, "status": None, "reasons": []}
    gen = llm(gen_messages(job, tpl_gen), args.gen_model, args.gen_temperature, args.seed)
    if gen is None:
        out["status"] = "DRY_RUN"
        return out
    out["generation"] = gen
    if "_bad_json" in gen or not isinstance(gen.get("tagged", ""), str):
        out.update(status="REJECT", reasons=["GEN_BAD_JSON"])
        return out
    if gen.get("skip"):
        out.update(status="SKIP", reasons=[f"GEN_SKIP:{gen.get('skip_reason', '')}"])
        return out
    text, ents, errors = R.check_generation(job, gen.get("tagged", ""), *leak)
    if errors:
        out.update(status="REJECT", reasons=errors, text=text)
        return out
    pairs = [{"id": f"R{i}", "head": c["head"]["id"], "tail": c["tail"]["id"], "allowed_relation": c["allowed_relation"]}
             for i, c in enumerate(candidates(text, ents), 1)]
    ver = llm(verify_messages(text, ents, pairs, tpl_ver), args.verify_model, 0.0, args.seed)
    out.update(text=text, entities=ents, pairs=pairs, verification=ver)
    if ver is None or "_bad_json" in ver:
        out.update(status="REJECT", reasons=["VERIFY_BAD_JSON"])
        return out
    validity = {e.get("id"): e.get("validity") for e in ver.get("entities", [])}
    labels = {p.get("pair_id"): p for p in ver.get("pairs", [])}
    target = next(p for p in pairs if p["head"] == job["head"] and p["tail"] == job["tail"]
                  and p["allowed_relation"] == job["relation"])
    if any(validity.get(e["id"]) not in ("VALID", "INVALID") for e in ents) or any(p["id"] not in labels for p in pairs):
        out.update(status="REJECT", reasons=["VERIFY_INCOMPLETE"])
        return out
    if validity[job["head"]] != "VALID" or validity[job["tail"]] != "VALID":
        out.update(status="REJECT", reasons=["VERIFY_TARGET_INVALID"])
        return out
    got = labels[target["id"]].get("label")
    if got != job["target_label"]:
        out.update(status="REJECT", reasons=[f"VERIFY_DISAGREE:{got}"])
        return out
    out["status"] = "ACCEPT"
    out["target_pair"] = target["id"]
    return out


def to_record(res, idx, args):
    job, ents = res["job"], res["entities"]
    validity = {e["id"]: e["validity"] for e in res["verification"]["entities"]}
    labels = {p["pair_id"]: p for p in res["verification"]["pairs"]}
    relations = []
    for p in res["pairs"]:
        if validity[p["head"]] != "VALID" or validity[p["tail"]] != "VALID":
            continue
        is_target = p["id"] == res["target_pair"]
        lab = labels[p["id"]].get("label")
        if lab not in (p["allowed_relation"], NEGATIVE):
            lab = NEGATIVE
        relations.append({"head": p["head"], "tail": p["tail"], "allowed_relation": p["allowed_relation"],
                          "label": job["target_label"] if is_target else lab,
                          "label_source": "target+verifier" if is_target else "verifier",
                          "evidence": labels[p["id"]].get("evidence", "")})
    return {
        "id": f"SL-{idx:05d}", "source": "re_v3.synth_llm", "method": "llm_rewrite", "variant": job["variant"],
        "text": res["text"],
        "entities": [dict(e, validity=validity[e["id"]]) for e in ents],
        "relations": relations,
        "target": {"head": job["head"], "tail": job["tail"], "relation": job["relation"], "label": job["target_label"]},
        "generation_evidence": res["generation"].get("evidence", ""),
        "annotation_status": "SYNTHETIC_LLM",
        "annotator": f"re_v3/synth_llm.py prompt {PROMPT_VERSION}, gen {args.gen_model}, verify {args.verify_model}",
        "human_verified": False, "training_eligible": False, "review_flags": [],
        "parent_id": job["seed_id"], "job_id": job["job_id"],
    }


# ---------------------------------------------------------------------------
# Đầu ra
# ---------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--pos", type=int, default=20, help="số câu dương cần giữ cho mỗi quan hệ")
    ap.add_argument("--neg", type=int, default=30, help="số câu âm khó cần giữ cho mỗi quan hệ")
    ap.add_argument("--oversample", type=float, default=1.5)
    ap.add_argument("--relations", nargs="*", default=list(RELATIONS))
    ap.add_argument("--name", default="pilot_v1")
    ap.add_argument("--gen-model", default=DEFAULT_MODEL)
    ap.add_argument("--verify-model", default=DEFAULT_MODEL)
    ap.add_argument("--gen-temperature", type=float, default=0.8)
    ap.add_argument("--seed", type=int, default=config.SEED)
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--dry-run", action="store_true", help="chỉ ghi prompt của vài job đầu, không gọi API")
    ap.add_argument("--max-usd", type=float, default=5.0,
                    help="trần chi phí cho lần chạy này (USD); chạm trần thì dừng gọi, chạy lại sẽ dùng cache")
    ap.add_argument("--no-kb", action="store_true", help="bỏ qua kiểm tra từ điển/công cụ K1–K7 (không khuyến nghị)")
    ap.add_argument("--ner", action="store_true", help="bật K5: chạy lại mô hình NER trên câu sinh")
    ap.add_argument("--online-rxnorm", action="store_true", help="K2 gọi RxNav khi cache không có")
    ap.add_argument("--a-fraction", type=float, default=1.0, help="tỉ lệ bản ghi tầng A đưa chuyên gia (pilot: 1.0)")
    args = ap.parse_args()

    rng = random.Random(args.seed)
    jobs = [j for j in plan_jobs(load_seeds(), args.pos, args.neg, rng, args.oversample)
            if j["relation"] in args.relations]
    out_dir = config.SYNTHETIC_DIR / args.name
    out_dir.mkdir(parents=True, exist_ok=True)
    write_jsonl(out_dir / "jobs.jsonl", jobs)
    tpl_gen, tpl_ver = load_prompt("gen"), load_prompt("verify")

    if args.dry_run:
        sample = []
        for rel in args.relations:
            for pol in ("POS", "NEG"):
                sample += [j for j in jobs if j["relation"] == rel and j["polarity"] == pol][:1]
        with open(out_dir / "dry_run_prompts.md", "w", encoding="utf-8") as fh:
            for j in sample:
                msgs = gen_messages(j, tpl_gen)
                fh.write(f"# {j['job_id']} ({j['variant']}, nhãn {j['target_label']})\n\n## system\n\n"
                         f"{msgs[0]['content']}\n\n## user\n\n{msgs[1]['content']}\n\n---\n\n")
        print(f"{len(jobs)} job đã lập. Prompt mẫu: {out_dir / 'dry_run_prompts.md'}")
        return

    llm = LLM(config.SYNTHETIC_DIR / "llm_cache.jsonl", max_usd=args.max_usd)
    leak = (test_index(LEAK_FILES, config.LEAK_NGRAM)[0], config.LEAK_NGRAM)
    with ThreadPoolExecutor(args.workers) as pool:
        results = list(pool.map(lambda j: run_job(j, llm, tpl_gen, tpl_ver, args, leak), jobs))

    # giữ tối đa --pos / --neg câu mỗi quan hệ, theo thứ tự job (đã xáo)
    quota = {(r, p): (args.pos if p == "POS" else args.neg) for r in RELATIONS for p in ("POS", "NEG")}
    from .validate_kb import KBValidator
    kb = None if args.no_kb else KBValidator(use_ner=args.ner, online_rxnorm=args.online_rxnorm)
    kept, accepted_extra, records, kb_rejected = Counter(), 0, [], []
    for res in results:
        if res["status"] != "ACCEPT":
            continue
        k = (res["job"]["relation"], res["job"]["polarity"])
        if kept[k] >= quota[k]:
            accepted_extra += 1
            continue
        rec = to_record(res, len(records) + len(kb_rejected) + 1, args)
        if kb is not None:
            rec["kb_validation"] = kb.validate(rec, target=rec["target"], exclude_ids=[rec["parent_id"]])
            if rec["kb_validation"]["tier"] == "C":           # lỗi cứng: loại trước khi tới chuyên gia
                res["status"], res["reasons"] = "KB_REJECT", rec["kb_validation"]["flags"]
                kb_rejected.append(rec)
                continue
        else:
            rec["kb_validation"] = {"tier": "B", "flags": ["KB_SKIPPED"], "entities": {}, "pairs": []}
        kept[k] += 1
        records.append(rec)

    write_jsonl(out_dir / f"{args.name}.jsonl", records)
    write_jsonl(out_dir / f"{args.name}.kb_rejected.jsonl", kb_rejected)
    write_jsonl(out_dir / "results.jsonl", results)
    xlsx = out_dir / f"{args.name}_expert_review.xlsx"
    review = write_xlsx(xlsx, records, a_fraction=args.a_fraction, title=f"Duyệt dữ liệu sinh: {args.name}")

    status = Counter((r["job"]["relation"], r["job"]["polarity"], r["status"]) for r in results)
    reasons = Counter(reason.split(":")[0] for r in results for reason in r["reasons"])
    by_variant = Counter((r["job"]["relation"], r["job"]["variant"], r["status"]) for r in results)
    manifest = {
        "prompt_version": PROMPT_VERSION, "gen_model": args.gen_model, "verify_model": args.verify_model,
        "gen_temperature": args.gen_temperature, "seed": args.seed, "seed_file": str(SEED_FILE),
        "leak_files": [str(p) for p in LEAK_FILES], "jobs": len(jobs), "records": len(records),
        "accepted_over_quota": accepted_extra, "kb_rejected": len(kb_rejected),
        "tiers": dict(Counter(r["kb_validation"]["tier"] for r in records)),
        "kb_flags": dict(Counter(f.split(":")[0] for r in records for f in r["kb_validation"]["flags"])),
        "expert_rows": {f"tier={t}|sample={s_}": n for (t, s_), n in review.items()},
        "status": {"|".join(k): v for k, v in sorted(status.items())},
        "accept_rate_by_variant": {
            f"{rel}|{var}": round(by_variant[(rel, var, "ACCEPT")] /
                                  max(1, sum(v for (r2, v2, _), v in by_variant.items() if (r2, v2) == (rel, var))), 3)
            for rel, var in sorted({(r, v) for r, v, _ in by_variant})},
        "reject_reasons": dict(reasons.most_common()),
        "kept": {"|".join(k): v for k, v in sorted(kept.items())},
        "pairs_in_records": dict(Counter(f"{x['allowed_relation']}|{x['label']}" for r in records for x in r["relations"])),
        "usage": dict(llm.usage),
    }
    (out_dir / f"{args.name}.manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=1), encoding="utf-8")
    log_run("re_v3.synth_llm", args, manifest, out_dir, {
        "dữ liệu sinh (jsonl)": out_dir / f"{args.name}.jsonl", "Excel cho chuyên gia": xlsx,
        "bị loại ở K1–K7": out_dir / f"{args.name}.kb_rejected.jsonl", "mọi job": out_dir / "results.jsonl",
        "manifest": out_dir / f"{args.name}.manifest.json", "phản hồi API thô": llm.cache_path})
    print(json.dumps({k: manifest[k] for k in ("jobs", "records", "kept", "tiers", "kb_rejected", "reject_reasons", "usage")},
                     ensure_ascii=False, indent=1))
    print(f"Excel cho chuyên gia: {xlsx}")
    short = [k for k, v in quota.items() if kept[k] < v and k[0] in args.relations]
    if short:
        print("Chưa đủ hạn mức (tăng --oversample hoặc sửa prompt):", short)


if __name__ == "__main__":
    main()

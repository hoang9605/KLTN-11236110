"""Nhật ký các lần chạy gọi LLM (sinh và gán nhãn), để lần lại được và đưa vào báo cáo.

Mỗi lần chạy ghi:
  re_v3/data/run_log.jsonl           một dòng JSON / lần chạy (mọi lần chạy, mọi script)
  <thư mục đầu ra>/run_log.md        bản dễ đọc của lần chạy đó (ghi nối tiếp nếu chạy lại)
Phản hồi thô của API (request + response, token, system_fingerprint) nằm ở re_v3/data/synthetic/llm_cache.jsonl.
"""
import getpass
import json
import platform
import sys
import time
from pathlib import Path

from . import config

GLOBAL_LOG = config.HERE / "data" / "run_log.jsonl"


def log_run(script, args, manifest, out_dir, files):
    entry = {
        "time": time.strftime("%Y-%m-%d %H:%M:%S"), "script": script, "command": " ".join(sys.argv),
        "user": getpass.getuser(), "python": platform.python_version(),
        "args": {k: v for k, v in vars(args).items()}, "out_dir": str(out_dir),
        "files": {k: str(v) for k, v in files.items()},
        "summary": {k: manifest.get(k) for k in (
            "prompt_version", "model", "gen_model", "verify_model", "split", "sentences", "labeled", "jobs", "records",
            "pairs", "labels", "tiers", "kb_rejected", "budget_stopped_sentences", "calls_per_sentence", "usage")
            if k in manifest},
    }
    GLOBAL_LOG.parent.mkdir(parents=True, exist_ok=True)
    with GLOBAL_LOG.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(entry, ensure_ascii=False) + "\n")
    lines = [f"## {entry['time']} — {script}", "", f"- Lệnh: `{entry['command']}`"]
    for k, v in entry["summary"].items():
        lines.append(f"- {k}: {json.dumps(v, ensure_ascii=False)}")
    lines.append("- File:")
    lines += [f"  - {k}: `{v}`" for k, v in entry["files"].items()]
    with (Path(out_dir) / "run_log.md").open("a", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n\n")
    return entry

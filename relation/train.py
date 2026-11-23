r"""Huấn luyện ViHealthBERT RE trên seed đã duyệt, có hoặc không có dữ liệu sinh (chạy trong .venv-gpu).

Cùng công thức với scripts/re_dataset/bert_re.py, định trước, không tinh chỉnh trên dev hay test:
10 epoch, lr 3e-5, batch 16, warmup 10%, weight decay 0,01, trọng số lớp n_neg/n_pos, max length 192,
ba seed 42/43/44, xác suất trung bình qua ba seed, ngưỡng 0,5.

Cấu hình: x0 (chỉ seed), x1 (seed + relation/data/synth/x1.jsonl), x3 (seed + x3.jsonl),
v1 (seed + synth/validated/x1.jsonl), vall (seed + synth/validated/pool.jsonl).
Mỗi cấu hình dự đoán cả dev và test, lưu sau từng seed để chạy tiếp được nếu bị ngắt.
Chỉ chọn cấu hình bằng dev (relation/evaluate.py); test chỉ được chấm cho cấu hình đã chọn.
Cặp đánh giá là cặp có hai thực thể VALID theo nhãn, tức mô hình được đánh giá với bộ lọc thực thể đúng.

    .venv-gpu\Scripts\python.exe -X utf8 -m relation.train --configs x0 x1 x3
Đầu ra: relation/outputs/train/<config>.json

Lưu mô hình dùng trong pipeline (cùng dữ liệu, siêu tham số và seed với cấu hình đã chọn trên dev):
    .venv-gpu\Scripts\python.exe -X utf8 -m relation.train --configs vall --save-model Model/vihealthbert-re-vietmed-validated
Khi có --save-model, kết quả dự đoán ghi vào <config>_saved.json để đối chiếu với lần chạy đã chấm.
"""
import argparse
import json
import os
import sys
import time
from pathlib import Path

os.environ.setdefault("KMP_DUPLICATE_LIB_OK", "TRUE")
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts" / "re_dataset"))

import torch  # noqa: E402
from transformers import AutoTokenizer  # noqa: E402

from bert_re import train_predict  # noqa: E402
from relation_extraction.bert_model import add_markers, save_config, save_member  # noqa: E402
from relation_extraction.data import RELATIONS  # noqa: E402
from relation_extraction.data import NEGATIVE, mark_pair  # noqa: E402

HERE = Path(__file__).resolve().parent
DATA = HERE / "data"
OUT = HERE / "outputs" / "train"
# x1 / x3: dữ liệu sinh chưa validate; v1 / vall: đã qua relation/validate và chuyên gia duyệt
# (v1 = cùng số cặp với seed, vall = toàn bộ pool đã duyệt, ít hơn x3 vì không đủ câu hợp lệ).
SYNTH = {"x0": None, "x1": DATA / "synth" / "x1.jsonl", "x3": DATA / "synth" / "x3.jsonl",
         "v1": DATA / "synth" / "validated" / "x1.jsonl", "vall": DATA / "synth" / "validated" / "pool.jsonl"}


def load(path):
    return [json.loads(l) for l in Path(path).read_text(encoding="utf-8").splitlines() if l.strip()]


def pairs_of(rows):
    out = []
    for r in rows:
        E = {e["id"]: e for e in r["entities"]}
        for x in r["relations"]:
            h, t = E[x["head"]], E[x["tail"]]
            out.append({"uid": f"{r['id']}:{x['head']}:{x['tail']}:{x['allowed_relation']}", "sample_id": r["id"],
                        "allowed_relation": x["allowed_relation"], "label": x["label"],
                        "features": mark_pair(r["text"], h, t)})
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--configs", nargs="+", default=["x0", "x1", "x3"], choices=sorted(SYNTH))
    ap.add_argument("--base", default="demdecuong/vihealthbert-base-syllable")
    ap.add_argument("--seeds", type=int, nargs="+", default=[42, 43, 44])
    ap.add_argument("--epochs", type=int, default=10)
    ap.add_argument("--lr", type=float, default=3e-5)
    ap.add_argument("--batch", type=int, default=16)
    ap.add_argument("--max-len", type=int, default=192)
    ap.add_argument("--save-model")
    a = ap.parse_args()
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    tok = AutoTokenizer.from_pretrained(a.base)
    start_ids = add_markers(tok)
    seed_pairs = pairs_of(load(DATA / "seed.jsonl"))
    dev, test = pairs_of(load(DATA / "dev.jsonl")), pairs_of(load(DATA / "test.jsonl"))
    OUT.mkdir(parents=True, exist_ok=True)
    for cfg in a.configs:
        extra = pairs_of(load(SYNTH[cfg])) if SYNTH[cfg] else []
        train = seed_pairs + extra
        path = OUT / (f"{cfg}_saved.json" if a.save_model else f"{cfg}.json")
        res = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}
        if res.get("train_pairs") != len(train):
            res = {}
        res.update({"config": cfg, "train_pairs": len(train), "seed_pairs": len(seed_pairs), "synthetic_pairs": len(extra),
                    "train_positives": sum(p["label"] != NEGATIVE for p in train), "base": a.base, "epochs": a.epochs,
                    "lr": a.lr, "batch": a.batch, "max_len": a.max_len, "seeds": a.seeds,
                    "device": torch.cuda.get_device_name(0) if device.type == "cuda" else "cpu"})
        res.setdefault("dev", {}); res.setdefault("test", {}); res.setdefault("seconds", {})
        t0 = time.time()
        for s in a.seeds:
            if str(s) in res["dev"]:
                print(f"[{cfg}] seed {s} đã có, bỏ qua", flush=True)
                continue
            st = time.time()
            if a.save_model:
                (pd, pt), model = train_predict(a, tok, start_ids, train, [dev, test], s, device, keep=True)
                save_member(model, tok, ROOT / a.save_model, s)
                del model
                torch.cuda.empty_cache()
            else:
                pd, pt = train_predict(a, tok, start_ids, train, [dev, test], s, device)
            res["dev"][str(s)] = {p["uid"]: round(v, 6) for p, v in zip(dev, pd)}
            res["test"][str(s)] = {p["uid"]: round(v, 6) for p, v in zip(test, pt)}
            res["seconds"][str(s)] = round(time.time() - st)
            path.write_text(json.dumps(res, ensure_ascii=False), encoding="utf-8")
            print(f"[{cfg}] seed {s} xong sau {time.time() - t0:.0f}s", flush=True)
        if a.save_model and all(str(s) in res["dev"] for s in a.seeds):
            save_config(ROOT / a.save_model, {
                "name": "ViHealthBERT-RE", "base": a.base, "max_len": a.max_len, "threshold": 0.5, "seeds": a.seeds,
                "seed_aggregation": "mean probability, threshold 0.5", "epochs": a.epochs, "lr": a.lr, "batch": a.batch,
                "class_weight": "n_neg/n_pos", "pooling": "head/tail start markers",
                "supported_relations": sorted({p["allowed_relation"] for p in train if p["label"] != NEGATIVE}),
                "all_relations": sorted(RELATIONS), "train_config": cfg, "train_pairs": len(train),
                "seed_pairs": len(seed_pairs), "synthetic_pairs": len(extra), "train_positives": res["train_positives"],
                "train_data": "relation/data/seed.jsonl (AI gán, người chuyên môn duyệt)" + (
                    f" + {SYNTH[cfg].relative_to(ROOT).as_posix()} (dữ liệu sinh"
                    + (", đã validate tự động và chuyên gia duyệt mẫu)" if "validated" in SYNTH[cfg].parts else ")")
                    if SYNTH[cfg] else ""),
                "label_source": "ai_labeled_expert_reviewed+synthetic_pattern"
                                + ("_validated" if SYNTH[cfg] and "validated" in SYNTH[cfg].parts else ""),
                "human_verified": False, "seed_expert_reviewed": True,
                "selection": "cấu hình có macro F1 cao nhất trên tập kiểm định (relation/outputs/evaluation.json)",
                "test_scores": "relation/outputs/evaluation_test_v2.json", "torch": torch.__version__,
                "trained_on": res["device"], "seconds": sum(res["seconds"].values()), "date": time.strftime("%Y-%m-%d")})
            print(f"đã lưu mô hình vào {ROOT / a.save_model}", flush=True)
    print("done", flush=True)


if __name__ == "__main__":
    main()

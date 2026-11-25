r"""Đường cong huấn luyện (loss, F1 trên dev) và so sánh hàm loss cho ViHealthBERT-RE (chạy trong .venv-gpu).

Cùng dữ liệu và công thức với mô hình triển khai (relation/train.py, cấu hình vall): ViHealthBERT,
marker đầu/cuối thực thể, AdamW lr 3e-5, weight decay 0,01, warmup 10% + giảm tuyến tính, batch 16,
max length 192, 10 epoch, cắt gradient 1,0, fp16. Chỉ thay hàm loss:

  wce      CrossEntropy có trọng số lớp [1, n_neg/n_pos]       (mô hình đang triển khai)
  ce       CrossEntropy không trọng số                          (đối chứng)
  focal    Focal loss γ = 2, α = trọng số lớp như wce           (Lin et al., ICCV 2017)
  wce_ls   wce + label smoothing 0,1                            (Szegedy et al., CVPR 2016; Müller et al., NeurIPS 2019)

Ghi lại: loss train từng bước, loss train trung bình mỗi epoch, loss dev (CE không trọng số, để các
hàm loss so được với nhau) và P/R/F1 micro + macro F1 trên dev sau mỗi epoch, ngưỡng 0,5.
Tập test KHÔNG được chấm ở đây: đường cong chỉ dùng dev, đúng quy tắc chọn mô hình của khóa luận.

    .venv-gpu\Scripts\python.exe -X utf8 -m relation.train_curves --losses wce ce focal wce_ls --seeds 42
    .venv\Scripts\python.exe -X utf8 -m relation.plot_curves
Đầu ra: relation/outputs/curves/<loss>_seed<N>.json (lưu sau mỗi epoch, chạy tiếp được nếu bị ngắt).
"""
import argparse
import json
import math
import os
import random
import sys
import time
from pathlib import Path

os.environ.setdefault("KMP_DUPLICATE_LIB_OK", "TRUE")
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import numpy as np  # noqa: E402
import torch  # noqa: E402
from torch import nn  # noqa: E402
from torch.nn import functional as F  # noqa: E402
from transformers import AutoTokenizer, get_linear_schedule_with_warmup  # noqa: E402

from relation.train import DATA, SYNTH, load, pairs_of  # noqa: E402
from relation_extraction.bert_model import PairClassifier, add_markers, batches, encode  # noqa: E402
from relation_extraction.data import NEGATIVE, RELATIONS  # noqa: E402

OUT = Path(__file__).resolve().parent / "outputs" / "curves"
LOSSES = ("wce", "ce", "focal", "wce_ls")


class FocalLoss(nn.Module):
    """FL(p_t) = -α_t (1 - p_t)^γ log p_t (Lin et al. 2017), chuẩn hóa theo tổng α_t như CE có trọng số."""

    def __init__(self, alpha, gamma=2.0):
        super().__init__()
        self.register_buffer("alpha", alpha)
        self.gamma = gamma

    def forward(self, logits, y):
        logp = F.log_softmax(logits, dim=-1).gather(1, y[:, None]).squeeze(1)
        a = self.alpha[y]
        return -(a * (1 - logp.exp()) ** self.gamma * logp).sum() / a.sum()


def make_loss(name, w):
    if name == "wce":
        return nn.CrossEntropyLoss(weight=w)
    if name == "ce":
        return nn.CrossEntropyLoss()
    if name == "focal":
        return FocalLoss(w, gamma=2.0)
    if name == "wce_ls":
        return nn.CrossEntropyLoss(weight=w, label_smoothing=0.1)
    raise ValueError(name)


def evaluate(model, items, dev, pad, device):
    """Loss dev (CE không trọng số) và P/R/F1 ở ngưỡng 0,5."""
    model.eval()
    probs, total, n = [0.0] * len(items), 0.0, 0
    with torch.no_grad():
        for ids, att, hp, tp, y, idx in batches(items, 64, pad):
            with torch.autocast(device_type=device.type, dtype=torch.float16, enabled=device.type == "cuda"):
                logits = model(ids.to(device), att.to(device), hp.to(device), tp.to(device))
            logits = logits.float()
            total += F.cross_entropy(logits, y.to(device), reduction="sum").item()
            n += len(y)
            for i, p in zip(idx, logits.softmax(-1)[:, 1].tolist()):
                probs[i] = p
    gold = [p["label"] != NEGATIVE for p in dev]
    pred = [p >= 0.5 for p in probs]
    tp_ = sum(g and q for g, q in zip(gold, pred))
    prec = tp_ / max(1, sum(pred))
    rec = tp_ / max(1, sum(gold))
    f1 = 2 * prec * rec / max(1e-9, prec + rec)
    per = {}
    for rel in RELATIONS:
        ix = [i for i, p in enumerate(dev) if p["allowed_relation"] == rel]
        g = [gold[i] for i in ix]
        q = [pred[i] for i in ix]
        t = sum(a and b for a, b in zip(g, q))
        if sum(g):
            pr, rc = t / max(1, sum(q)), t / sum(g)
            per[rel] = round(2 * pr * rc / max(1e-9, pr + rc), 4)
    return {"dev_loss": round(total / max(1, n), 5), "precision": round(prec, 4), "recall": round(rec, 4),
            "f1": round(f1, 4), "macro_f1": round(sum(per.values()) / max(1, len(per)), 4), "f1_by_relation": per}


def run(a, tok, start_ids, train, dev, loss_name, seed, device):
    path = OUT / f"{loss_name}_seed{seed}.json"
    if path.exists() and json.loads(path.read_text(encoding="utf-8")).get("done"):
        print(f"[{loss_name}] seed {seed} đã có, bỏ qua", flush=True)
        return
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    model = PairClassifier.from_base(a.base, len(tok)).to(device)
    tr = encode(tok, train, a.max_len, start_ids)
    dv = encode(tok, dev, a.max_len, start_ids)
    npos = sum(x[3] for x in tr)
    w = torch.tensor([1.0, (len(tr) - npos) / max(npos, 1)], device=device)
    lossf = make_loss(loss_name, w).to(device)
    steps_per_epoch = math.ceil(len(tr) / a.batch)
    steps = steps_per_epoch * a.epochs
    opt = torch.optim.AdamW(model.parameters(), lr=a.lr, weight_decay=0.01)
    sch = get_linear_schedule_with_warmup(opt, int(0.1 * steps), steps)
    scaler = torch.amp.GradScaler("cuda", enabled=device.type == "cuda")
    rng = random.Random(seed)
    pad = tok.pad_token_id
    log = {"loss": loss_name, "seed": seed, "config": a.config, "train_pairs": len(tr), "train_positives": npos,
           "dev_pairs": len(dv), "class_weight": [round(x, 4) for x in w.tolist()], "epochs": a.epochs,
           "lr": a.lr, "batch": a.batch, "max_len": a.max_len, "steps_per_epoch": steps_per_epoch,
           "device": torch.cuda.get_device_name(0) if device.type == "cuda" else "cpu",
           "step_loss": [], "lr_trace": [], "epochs_log": [], "done": False}
    log["epochs_log"].append(dict(epoch=0, train_loss=None, **evaluate(model, dv, dev, pad, device)))
    t0 = time.time()
    for ep in range(1, a.epochs + 1):
        model.train()
        ep_losses = []
        for ids, att, hp, tp, y, _ in batches(tr, a.batch, pad, rng):
            with torch.autocast(device_type=device.type, dtype=torch.float16, enabled=device.type == "cuda"):
                logits = model(ids.to(device), att.to(device), hp.to(device), tp.to(device))
            loss = lossf(logits.float(), y.to(device))
            opt.zero_grad()
            scaler.scale(loss).backward()
            scaler.unscale_(opt)
            nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            scaler.step(opt)
            scaler.update()
            sch.step()
            ep_losses.append(loss.item())
            log["step_loss"].append(round(loss.item(), 5))
            log["lr_trace"].append(sch.get_last_lr()[0])
        ev = evaluate(model, dv, dev, pad, device)
        log["epochs_log"].append(dict(epoch=ep, train_loss=round(sum(ep_losses) / len(ep_losses), 5), **ev))
        log["seconds"] = round(time.time() - t0)
        path.write_text(json.dumps(log, ensure_ascii=False), encoding="utf-8")
        print(f"[{loss_name}] seed {seed} epoch {ep}: train {log['epochs_log'][-1]['train_loss']:.4f} "
              f"dev_loss {ev['dev_loss']:.4f} F1 {ev['f1']:.3f} macro {ev['macro_f1']:.3f} ({time.time() - t0:.0f}s)",
              flush=True)
    log["done"] = True
    path.write_text(json.dumps(log, ensure_ascii=False), encoding="utf-8")
    del model
    torch.cuda.empty_cache()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--losses", nargs="+", default=list(LOSSES), choices=LOSSES)
    ap.add_argument("--seeds", type=int, nargs="+", default=[42])
    ap.add_argument("--config", default="vall", choices=sorted(SYNTH))
    ap.add_argument("--base", default="demdecuong/vihealthbert-base-syllable")
    ap.add_argument("--epochs", type=int, default=10)
    ap.add_argument("--lr", type=float, default=3e-5)
    ap.add_argument("--batch", type=int, default=16)
    ap.add_argument("--max-len", type=int, default=192)
    a = ap.parse_args()
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    tok = AutoTokenizer.from_pretrained(a.base)
    start_ids = add_markers(tok)
    train = pairs_of(load(DATA / "seed.jsonl")) + (pairs_of(load(SYNTH[a.config])) if SYNTH[a.config] else [])
    dev = pairs_of(load(DATA / "dev.jsonl"))
    OUT.mkdir(parents=True, exist_ok=True)
    for loss_name in a.losses:
        for s in a.seeds:
            run(a, tok, start_ids, train, dev, loss_name, s, device)
    print("done", flush=True)


if __name__ == "__main__":
    main()

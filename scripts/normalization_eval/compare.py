r"""Before/after comparison table for normalization runs (dev and test).

    .venv\Scripts\python.exe -X utf8 scripts/normalization_eval/compare.py --root eval/normalization_2026-11-07
"""
import argparse
import json
from pathlib import Path


def load(d):
    return json.loads((Path(d) / "report.json").read_text(encoding="utf-8"))


def f(x):
    return f"{x:.3f}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    a = ap.parse_args()
    root = Path(a.root)
    runs = {(s, w): load(root / f"{s}_{w}") for s in ("dev", "test") for w in ("before", "after")}
    verified = all(r["human_verified"] for r in runs.values())
    L = ["# Chuẩn hóa thực thể: trước và sau cải thiện trên dev", ""]
    if not verified:
        L += ["> Nhãn gold là nhãn AI tiền gán, **chưa có bác sĩ duyệt**. Số liệu là tạm thời.", ""]
    L += ["Các thay đổi chỉ được chọn và kiểm tra trên **dev** (split `validation`). Test chỉ chạy một lần sau cùng.",
          "Từ điển được xây từ các dạng có trong train/dev, nên số trên dev là lạc quan; **số cần báo cáo là số trên test**.", "",
          "| Ontology | Split | Accuracy trước → sau | CI95 sau | Accuracy (mention) | Precision khi trả lời | Từ chối đúng NIL | Top-10 = Recall@10 | MRR@10 |",
          "|---|---|---|---|---|---|---|---|---|"]
    for onto in ("ICD-10", "RxNorm"):
        for split in ("dev", "test"):
            b = runs[(split, "before")]["results"][onto]["code"]
            x = runs[(split, "after")]["results"][onto]["code"]
            bt, xt, bm, xm = b["type"], x["type"], b["mention"], x["mention"]
            ci = x["ci95_type"]["system.accuracy"]
            L.append(f"| {onto} | {split} | {f(bt['system']['accuracy'])} → **{f(xt['system']['accuracy'])}** | "
                     f"{f(ci[0])}–{f(ci[1])} | {f(bm['system']['accuracy'])} → {f(xm['system']['accuracy'])} | "
                     f"{f(bt['system']['precision_answered'])} → {f(xt['system']['precision_answered'])} | "
                     f"{f(bt['system']['nil_correct_abstention'])} → {f(xt['system']['nil_correct_abstention'])} | "
                     f"{f(bt['top10_acc'])} → {f(xt['top10_acc'])} | {f(bt['mrr@10'])} → {f(xt['mrr@10'])} |")
    L += ["", "## Hai chế độ của hệ thống sau cải thiện", "",
          "| Ontology | Split | Chế độ | Accuracy (type) | CI95 | Accuracy (mention) | Precision khi trả lời | Từ chối đúng NIL |",
          "|---|---|---|---|---|---|---|---|"]
    for onto in ("ICD-10", "RxNorm"):
        for split in ("dev", "test"):
            x = runs[(split, "after")]["results"][onto]["code"]
            for m, name in (("system", "thận trọng"), ("always", "luôn trả lời")):
                if m not in x["type"]:
                    continue
                t_, m_ = x["type"][m], x["mention"][m]
                ci = x["ci95_type"][f"{m}.accuracy"]
                L.append(f"| {onto} | {split} | {name} | {f(t_['accuracy'])} | {f(ci[0])}–{f(ci[1])} | "
                         f"{f(m_['accuracy'])} | {f(t_['precision_answered'])} | {f(t_['nil_correct_abstention'])} |")
    L += ["", "Chi tiết từng lần chạy (kèm baseline và Top-1/3/5): `dev_before/`, `dev_after/`, `test_before/`, `test_after/` → `summary.md`."]
    out = root / "comparison.md"
    out.write_text("\n".join(L) + "\n", encoding="utf-8")
    print("\n".join(L))


if __name__ == "__main__":
    main()

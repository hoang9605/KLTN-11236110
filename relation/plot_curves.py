r"""Vẽ ảnh loss và F1 từ relation/outputs/curves/*.json (đầu ra của relation/train_curves.py).

    .venv\Scripts\python.exe -X utf8 -m relation.plot_curves
Đầu ra (PNG 200 dpi, dùng cho tài liệu và báo cáo Word):
  relation/figures/h_loss_buoc_wce.png      loss train theo bước + trung bình trượt, mô hình triển khai (wce)
  relation/figures/h_loss_train_dev_wce.png loss train và loss dev theo epoch (wce)
  relation/figures/h_loss_dev_so_sanh.png   loss dev theo epoch, 4 hàm loss
  relation/figures/h_f1_dev_so_sanh.png     macro F1 dev theo epoch, 4 hàm loss
  relation/figures/h_lr_lich.png            lịch learning rate (warmup 10% + giảm tuyến tính)
  relation/outputs/curves/summary.json      bảng số liệu theo epoch (bản bảng của các hình)
"""
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = Path(__file__).resolve().parent
CURVES = HERE / "outputs" / "curves"
FIG = HERE / "figures"

# bảng màu phân loại đã kiểm tra bằng validate_palette (thứ tự cố định theo hàm loss, không đổi theo hạng)
COLORS = {"wce": "#2a78d6", "ce": "#eb6834", "focal": "#1baf7a", "wce_ls": "#eda100"}
STYLES = {"wce": "-", "ce": "--", "focal": "-.", "wce_ls": ":"}
MARKERS = {"wce": "o", "ce": "s", "focal": "^", "wce_ls": "D"}
NAMES = {"wce": "CE có trọng số (triển khai)", "ce": "CE không trọng số", "focal": "Focal (γ=2)",
         "wce_ls": "CE có trọng số + label smoothing 0,1"}
INK, INK2, GRID, SURFACE = "#0b0b0b", "#52514e", "#e4e3df", "#fcfcfb"


def style(ax, title, xlabel, ylabel):
    ax.set_facecolor(SURFACE)
    ax.set_title(title, loc="left", fontsize=11, color=INK, pad=10)
    ax.set_xlabel(xlabel, color=INK2, fontsize=9)
    ax.set_ylabel(ylabel, color=INK2, fontsize=9)
    ax.grid(True, color=GRID, linewidth=0.6)
    ax.set_axisbelow(True)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color(GRID)
    ax.tick_params(colors=INK2, labelsize=8)


def ema(xs, alpha=0.05):
    out, m = [], None
    for x in xs:
        m = x if m is None else alpha * x + (1 - alpha) * m
        out.append(m)
    return out


def load(seed=42):
    runs = {}
    for name in COLORS:
        p = CURVES / f"{name}_seed{seed}.json"
        if p.exists():
            runs[name] = json.loads(p.read_text(encoding="utf-8"))
    return runs


def save(fig, name):
    FIG.mkdir(parents=True, exist_ok=True)
    fig.patch.set_facecolor(SURFACE)
    fig.tight_layout()
    fig.savefig(FIG / name, dpi=200)
    plt.close(fig)


def end_label(ax, x, y, text, color):
    ax.annotate(text, (x, y), xytext=(6, 0), textcoords="offset points", va="center", fontsize=8, color=INK2)
    ax.plot([x], [y], marker="o", markersize=4, color=color, markeredgecolor=SURFACE, markeredgewidth=1.5)


def main():
    runs = load()
    if not runs:
        raise SystemExit("Chưa có relation/outputs/curves/*.json; chạy relation.train_curves trước.")
    summary = {}
    for name, r in runs.items():
        summary[name] = {"done": r["done"], "class_weight": r["class_weight"], "epochs": r["epochs_log"]}
        best = max(r["epochs_log"][1:], key=lambda e: e["macro_f1"], default=None)
        summary[name]["best_dev_epoch"] = best and {"epoch": best["epoch"], "macro_f1": best["macro_f1"], "f1": best["f1"]}
    (CURVES / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=1), encoding="utf-8")

    if "wce" in runs:
        r = runs["wce"]
        spe = r["steps_per_epoch"]
        x = [(i + 1) / spe for i in range(len(r["step_loss"]))]
        fig, ax = plt.subplots(figsize=(7.2, 3.6))
        ax.plot(x, r["step_loss"], color=COLORS["wce"], alpha=0.25, linewidth=0.8, label="Loss từng bước")
        sm = ema(r["step_loss"])
        ax.plot(x, sm, color=COLORS["wce"], linewidth=2, label="Trung bình trượt (EMA 0,05)")
        end_label(ax, x[-1], sm[-1], f"{sm[-1]:.3f}", COLORS["wce"])
        style(ax, "Loss huấn luyện theo bước, CE có trọng số (seed 42)", "Epoch", "Loss (CE có trọng số)")
        ax.legend(frameon=False, fontsize=8, labelcolor=INK2)
        save(fig, "h_loss_buoc_wce.png")

        ep = [e for e in r["epochs_log"] if e["train_loss"] is not None]
        fig, ax = plt.subplots(figsize=(7.2, 3.6))
        ax.plot([e["epoch"] for e in ep], [e["train_loss"] for e in ep], color=COLORS["wce"], linewidth=2,
                marker="o", markersize=5, label="Train (CE có trọng số, hàm được tối ưu)")
        ax.plot([e["epoch"] for e in r["epochs_log"]], [e["dev_loss"] for e in r["epochs_log"]], color=COLORS["ce"],
                linewidth=2, linestyle="--", marker="s", markersize=5, label="Dev (CE không trọng số)")
        best = min(r["epochs_log"][1:], key=lambda e: e["dev_loss"], default=None)
        if best:
            ax.annotate(f"dev thấp nhất: epoch {best['epoch']}", (best["epoch"], best["dev_loss"]), xytext=(0, -16),
                        textcoords="offset points", ha="center", fontsize=8, color=INK2)
        style(ax, "Loss train và loss dev theo epoch (seed 42)", "Epoch", "Loss")
        ax.set_xticks(range(0, r["epochs"] + 1))
        ax.legend(frameon=False, fontsize=8, labelcolor=INK2)
        save(fig, "h_loss_train_dev_wce.png")

        fig, ax = plt.subplots(figsize=(7.2, 3.0))
        ax.plot(x, r["lr_trace"], color=COLORS["wce"], linewidth=2)
        style(ax, "Lịch learning rate: warmup 10% rồi giảm tuyến tính về 0", "Epoch", "Learning rate")
        ax.ticklabel_format(axis="y", style="sci", scilimits=(-5, -5))
        save(fig, "h_lr_lich.png")

    for key, fname, title, ylabel in (
            ("dev_loss", "h_loss_dev_so_sanh.png", "Loss dev theo epoch, so sánh hàm loss (seed 42)", "Loss dev (CE không trọng số)"),
            ("macro_f1", "h_f1_dev_so_sanh.png", "Macro F1 trên dev theo epoch, so sánh hàm loss (seed 42)", "Macro F1 (ngưỡng 0,5)")):
        fig, ax = plt.subplots(figsize=(7.2, 3.8))
        for name, r in runs.items():
            ep = r["epochs_log"] if key == "dev_loss" else r["epochs_log"][1:]
            xs, ys = [e["epoch"] for e in ep], [e[key] for e in ep]
            ax.plot(xs, ys, color=COLORS[name], linestyle=STYLES[name], marker=MARKERS[name], markersize=5,
                    linewidth=2, label=NAMES[name])
            end_label(ax, xs[-1], ys[-1], f"{ys[-1]:.3f}", COLORS[name])
        style(ax, title, "Epoch", ylabel)
        ax.set_xticks(range(0, max(r["epochs"] for r in runs.values()) + 1))
        ax.legend(frameon=False, fontsize=8, labelcolor=INK2)
        save(fig, fname)
    print(json.dumps({k: v["best_dev_epoch"] for k, v in summary.items()}, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()

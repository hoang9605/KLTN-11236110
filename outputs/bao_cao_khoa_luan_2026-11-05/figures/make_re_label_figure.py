"""Hình 3.2: quy trình gán nhãn quan hệ bằng mô hình ngôn ngữ lớn và duyệt của chuyên gia (25/11/2026).

Cùng phong cách với make_review_figures.py (thang xám, Arial). Số liệu đọc từ
outputs/re_811_gold/labeling_summary.json.

Chạy từ gốc repo:
    .venv/Scripts/python.exe -X utf8 outputs/bao_cao_khoa_luan_2026-11-05/figures/make_re_label_figure.py
"""
import json
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import FancyBboxPatch  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parent))
from f4p_style import FigureStyle, apply_publication_style, finalize_figure  # noqa: E402

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent
apply_publication_style(FigureStyle(font_size=16, axes_linewidth=2.5))
K1, K3 = "#272727", "#767676"
F1, F2, F3 = "#FFFFFF", "#F2F2F2", "#E0E0E0"
RV = json.loads((ROOT / "outputs/re_811_gold/labeling_summary.json").read_text(encoding="utf-8"))


def n(x):
    return f"{x:,}".replace(",", ".")


def rbox(ax, x, y, w, h, fc=F2, ec=K1, lw=2.0, ls="-", r=0.15):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={r}", fc=fc, ec=ec, lw=lw, ls=ls))


def txt(ax, x, y, s, size=15, color=K1, weight="normal", ha="center", va="center"):
    ax.text(x, y, s, fontsize=size, color=color, weight=weight, ha=ha, va=va, linespacing=1.35)


def arr(ax, x0, y0, x1, y1, color=K1, ls="-"):
    ax.annotate("", xy=(x1, y1), xytext=(x0, y0),
                arrowprops=dict(arrowstyle="-|>", color=color, lw=2.0, ls=ls, shrinkA=0, shrinkB=0, mutation_scale=18))


tr, trc = RV["runs"]["train_label_v4"], RV["runs"]["train_label_v4_critic"]
flips = sum(trc["flips"].values())
steps = [
    ("Sinh cặp ứng viên", "Thực thể lấy từ nhãn NER gốc, chương trình ghép cặp theo lược đồ kiểu,\nmỗi cặp chỉ có một quan hệ hợp lệ hoặc NO_RELATION",
     f"{n(RV['split']['train']['sentences_with_pairs'])} câu huấn luyện\ncó cặp ứng viên"),
    ("Gán nhãn hai bước", "Bước A đánh VALID hoặc INVALID cho thực thể, bước B gán nhãn cặp kèm bằng chứng.\nLượt đầu với temperature 0, thêm hai lượt rồi bỏ phiếu khi câu có dấu hiệu bất định",
     f"gpt-5.4-mini\n{str(tr['calls_per_sentence']).replace('.', ',')} lượt gọi mỗi câu"),
    ("Kiểm tra bằng từ điển và công cụ", "ICD-10, RxNorm, từ điển kiểu thực thể, biểu thức liều, rule-based\nvà câu khác trong kho, gắn cờ và chia tầng duyệt",
     "Không dùng mô hình\nngôn ngữ lớn"),
    ("Phản biện", "Chỉ xem lại cặp đáng nghi, nhãn ban đầu được nêu trung lập,\nđổi nhãn khi bước phản biện có độ tin cậy cao",
     f"gpt-5.4, xem lại {n(trc['selected'])} cặp\nvà đổi nhãn {flips} cặp"),
    ("Duyệt của chuyên gia", "Chuyên gia ghi 0 khi nhãn sai, nhãn sai được đảo.\nDuyệt toàn bộ tập kiểm định, tập kiểm tra và phần có cờ của tập huấn luyện",
     f"{n(RV['dataset']['train']['origin']['expert_pilot'] + RV['dataset']['train']['origin']['expert_train'])} cặp huấn luyện\ncó nhãn chuyên gia"),
]
H, GAP, W = 2.25, 0.75, 16.0
total = len(steps) * H + (len(steps) - 1) * GAP
fig = plt.figure(figsize=(12, 12 * (total + 0.4) / 22.4))
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, 22.4)
ax.set_ylim(0, total + 0.4)
ax.axis("off")
for i, (name, desc, note) in enumerate(steps):
    y = total + 0.2 - (i + 1) * H - i * GAP
    rbox(ax, 0.2, y, W, H, fc=F3 if i in (1, 3) else F2)
    txt(ax, 0.55, y + H - 0.5, f"{i + 1}. {name}", size=17, weight="bold", ha="left")
    txt(ax, 0.55, y + 0.85, desc, size=14, ha="left")
    rbox(ax, W + 0.6, y + 0.35, 22.4 - W - 0.8, H - 0.7, fc=F1, ec=K3, ls="--", r=0.1)
    txt(ax, W + 0.6 + (22.4 - W - 0.8) / 2, y + H / 2, note.replace(", ", ",\n", 1), size=13.5, color=K1)
    if i < len(steps) - 1:
        arr(ax, 0.2 + W / 2, y, 0.2 + W / 2, y - GAP)
    if i in (1, 3):
        arr(ax, W + 0.2, y + H / 2, W + 0.6, y + H / 2, color=K3, ls="--")
finalize_figure(fig, OUT / "h3_2_quy_trinh_gan_nhan", formats=["png", "pdf"], dpi=300, pad=0.08)
print("wrote h3_2_quy_trinh_gan_nhan")

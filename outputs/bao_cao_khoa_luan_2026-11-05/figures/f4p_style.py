"""Phong cách hình theo figures4papers (github.com/ChenLiu-1996/figures4papers).

Cài lại đúng API mà repo mô tả trong scientific-figure-making/references/api.md:
FigureStyle, apply_publication_style, finalize_figure và bảng màu PALETTE với vai trò
màu của repo (xanh cho phương pháp đề xuất, xanh lá cho cải thiện, đỏ cho baseline,
xám trung tính cho nền). Kích thước chữ được thu theo tỉ lệ của repo (16 pt, nét trục 2,5
ở khổ 12 x 8 inch) về khổ khoảng 6,4 inch mà khóa luận dùng.
"""
from dataclasses import dataclass, field
from pathlib import Path

import matplotlib.pyplot as plt

PALETTE = {
    "blue_main": "#0F4D92",
    "blue_secondary": "#3775BA",
    "green_1": "#DDF3DE",
    "green_2": "#AADCA9",
    "green_3": "#8BCF8B",
    "red_1": "#F6CFCB",
    "red_2": "#E9A6A1",
    "red_strong": "#B64342",
    "neutral": "#CFCECE",
    "highlight": "#FFD700",
    "teal": "#42949E",
    "violet": "#9A4D8E",
}
# Bản in đen trắng: giữ vai trò màu của figures4papers nhưng ánh xạ sang thang xám,
# các nhóm được phân biệt bằng độ đậm, kiểu nét và hình điểm đánh dấu.
GRAYSCALE = True
PALETTE_COLOR = dict(PALETTE)
if GRAYSCALE:
    PALETTE = {
        "blue_main": "#1a1a1a", "blue_secondary": "#4d4d4d", "green_1": "#f2f2f2", "green_2": "#d0d0d0",
        "green_3": "#b3b3b3", "red_1": "#e6e6e6", "red_2": "#bdbdbd", "red_strong": "#808080",
        "neutral": "#d4d4d4", "highlight": "#b3b3b3", "teal": "#4d4d4d", "violet": "#a6a6a6",
    }
DEFAULT_COLORS = [PALETTE[k] for k in ("blue_main", "green_3", "red_strong", "teal", "violet", "neutral")]


@dataclass
class FigureStyle:
    font_size: float = 10
    axes_linewidth: float = 1.4
    use_tex: bool = False
    font_family: tuple = field(default_factory=lambda: ("Arial", "DejaVu Sans", "Helvetica", "sans-serif"))


def apply_publication_style(style: FigureStyle | None = None) -> None:
    """Tắt trục trên và phải, chú giải không khung, đặt font và tùy chọn xuất vector."""
    s = style or FigureStyle()
    plt.rcParams.update({
        "font.family": "sans-serif", "font.sans-serif": list(s.font_family), "font.size": s.font_size,
        "axes.labelsize": s.font_size, "axes.titlesize": s.font_size, "legend.fontsize": s.font_size - 1,
        "xtick.labelsize": s.font_size - 1, "ytick.labelsize": s.font_size - 1,
        "axes.linewidth": s.axes_linewidth, "xtick.major.width": s.axes_linewidth, "ytick.major.width": s.axes_linewidth,
        "axes.spines.top": False, "axes.spines.right": False, "legend.frameon": False,
        "text.usetex": s.use_tex, "pdf.fonttype": 42, "ps.fonttype": 42, "svg.fonttype": "none",
        "axes.prop_cycle": plt.cycler(color=DEFAULT_COLORS), "savefig.dpi": 300,
        "text.color": "#1f1f1e", "axes.labelcolor": "#1f1f1e", "axes.edgecolor": "#1f1f1e",
        "xtick.color": "#1f1f1e", "ytick.color": "#1f1f1e", "axes.grid": False,
    })


def finalize_figure(fig, out_path, formats=None, dpi=300, close=True, pad=0.05, **kwargs):
    """Lưu hình ra một hoặc nhiều định dạng và trả về danh sách đường dẫn đã lưu."""
    out = Path(out_path)
    if formats is None:
        formats = [out.suffix.lstrip(".")] if out.suffix else ["pdf", "svg", "eps"]
    base = out.with_suffix("")
    base.parent.mkdir(parents=True, exist_ok=True)
    saved = []
    for fmt in formats:
        p = base.with_suffix("." + fmt)
        fig.savefig(p, dpi=dpi, bbox_inches="tight", pad_inches=pad, facecolor="white", **kwargs)
        saved.append(p)
    if close:
        plt.close(fig)
    return saved

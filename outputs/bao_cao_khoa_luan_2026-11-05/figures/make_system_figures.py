r"""Sơ đồ phân tích, thiết kế và triển khai hệ thống (mục 3.5), theo kiểu UML của các sơ đồ mẫu.

    .venv\Scripts\python.exe -X utf8 outputs/bao_cao_khoa_luan_2026-11-05/figures/make_system_figures.py

Vẽ bằng matplotlib theo phong cách figures4papers ở thang xám (bản in đen trắng). Tọa độ tính bằng inch
để chữ có cùng cỡ ở mọi hình. Trong hình không dùng tên lớp, tên tệp hay tên hàm của mã nguồn.
"""
import math
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import Ellipse, FancyArrowPatch, FancyBboxPatch, Rectangle  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parent))
from f4p_style import FigureStyle, apply_publication_style, finalize_figure  # noqa: E402

OUT = Path(__file__).resolve().parent
INK, MUTED = "#1a1a1a", "#5f5e5a"
FILL = {"w": "#ffffff", "l": "#f2f2f2", "m": "#e0e0e0", "d": "#c8c8c8"}
FS = 8.6
apply_publication_style(FigureStyle(font_size=FS, axes_linewidth=1.0))


# ------------------------------------------------------------------ khung vẽ và phần tử cơ bản
def canvas(w, h):
    fig = plt.figure(figsize=(w, h))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, w)
    ax.set_ylim(0, h)
    ax.set_aspect("equal")
    ax.axis("off")
    return fig, ax


def save(fig, name):
    finalize_figure(fig, OUT / name, formats=["png", "pdf"], dpi=300, pad=0.04)
    print("wrote", name)


def text(ax, x, y, s, size=FS, weight="normal", color=INK, ha="center", va="center", style="normal", **kw):
    ax.text(x, y, s, fontsize=size, fontweight=weight, color=color, ha=ha, va=va, fontstyle=style,
            linespacing=1.25, zorder=6, **kw)


def rbox(ax, x, y, w, h, title=None, body=None, fill="w", ls="-", lw=1.1, r=0.06, tsize=FS, bsize=FS - 0.8,
         weight="bold", align="center", z=2):
    """Hộp bo góc; (x, y) là góc dưới trái. Tiêu đề in đậm, phần thân chữ thường bên dưới."""
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={r}", fc=FILL[fill], ec=INK,
                                lw=lw, ls=ls, zorder=z))
    cx = x + w / 2 if align == "center" else x + 0.1
    if title and body:
        text(ax, cx, y + h - 0.2, title, weight=weight, size=tsize, ha=align)
        text(ax, cx, y + (h - 0.34) / 2, body, size=bsize, color=INK, ha=align)
    elif title:
        text(ax, cx, y + h / 2, title, weight=weight, size=tsize, ha=align)
    return (x, y, w, h)


def frame(ax, x, y, w, h, label, ls="--", fill=None, lsize=FS, z=0):
    """Khung bao (ranh giới hệ thống, máy chủ, gói) với nhãn ở góc trên trái."""
    ax.add_patch(Rectangle((x, y), w, h, fc=FILL[fill] if fill else "none", ec=INK, lw=1.0, ls=ls, zorder=z))
    text(ax, x + 0.1, y + h - 0.16, label, weight="bold", size=lsize, ha="left")


def arrow(ax, p, q, label=None, ls="-", head="-|>", lw=1.0, rad=0.0, lpos=0.5, loff=(0, 0.11), lsize=FS - 1,
          lha="center", color=INK, z=4, shrink=0, hollow=False):
    kw = dict(ec=color, fc="white") if hollow else dict(color=color)
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle=head, mutation_scale=14 if hollow else 9, lw=lw, ls=ls,
                                 connectionstyle=f"arc3,rad={rad}", shrinkA=shrink, shrinkB=shrink, zorder=z, **kw))
    if label:
        mx, my = p[0] + (q[0] - p[0]) * lpos + loff[0], p[1] + (q[1] - p[1]) * lpos + loff[1]
        text(ax, mx, my, label, size=lsize, ha=lha,
             bbox=dict(fc="white", ec="none", pad=0.6, alpha=0.95))


def poly(ax, pts, label=None, ls="-", lpos=None, lsize=FS - 1, head="-|>", loff=(0, 0.1), lha="center"):
    """Mũi tên gấp khúc qua các điểm."""
    xs, ys = zip(*pts)
    ax.plot(xs[:-1] + (xs[-1],), ys[:-1] + (ys[-1],), color="none")
    for a, b in zip(pts[:-2], pts[1:-1]):
        ax.plot([a[0], b[0]], [a[1], b[1]], color=INK, lw=1.0, ls=ls, zorder=4, solid_capstyle="butt")
    arrow(ax, pts[-2], pts[-1], ls=ls, head=head)
    if label:
        i = lpos if lpos is not None else 0
        a, b = pts[i], pts[i + 1]
        text(ax, (a[0] + b[0]) / 2 + loff[0], (a[1] + b[1]) / 2 + loff[1], label, size=lsize, ha=lha,
             bbox=dict(fc="white", ec="none", pad=0.6))


def actor(ax, x, y, name, s=1.0):
    """Tác nhân hình người, (x, y) là chân."""
    k = 0.22 * s
    ax.add_patch(Ellipse((x, y + 3.1 * k), 0.85 * k, 0.85 * k, fc="white", ec=INK, lw=1.1, zorder=5))
    ax.plot([x, x], [y + 2.65 * k, y + 1.25 * k], color=INK, lw=1.1, zorder=5)
    ax.plot([x - 0.8 * k, x + 0.8 * k], [y + 2.2 * k, y + 2.2 * k], color=INK, lw=1.1, zorder=5)
    ax.plot([x - 0.65 * k, x, x + 0.65 * k], [y, y + 1.25 * k, y], color=INK, lw=1.1, zorder=5)
    text(ax, x, y - 0.17, name, weight="bold")


def usecase(ax, x, y, w, h, s, fill="w"):
    ax.add_patch(Ellipse((x, y), w, h, fc=FILL[fill], ec=INK, lw=1.1, zorder=3))
    text(ax, x, y, s)
    return (x, y, w, h)


def ell_pt(e, toward):
    """Điểm trên viền elip (x, y, w, h) theo hướng tới điểm toward."""
    x, y, w, h = e
    dx, dy = toward[0] - x, toward[1] - y
    t = 1 / math.sqrt((dx / (w / 2)) ** 2 + (dy / (h / 2)) ** 2)
    return (x + dx * t, y + dy * t)


def cylinder(ax, x, y, w, h, title, body=None, fill="l"):
    e = 0.12
    ax.add_patch(Rectangle((x, y + e / 2), w, h - e, fc=FILL[fill], ec="none", zorder=2))
    ax.plot([x, x], [y + e / 2, y + h - e / 2], color=INK, lw=1.1, zorder=3)
    ax.plot([x + w, x + w], [y + e / 2, y + h - e / 2], color=INK, lw=1.1, zorder=3)
    ax.add_patch(Ellipse((x + w / 2, y + e / 2), w, e, fc=FILL[fill], ec=INK, lw=1.1, zorder=2.5))
    ax.add_patch(Rectangle((x + 0.01, y + e / 2), w - 0.02, 0.07, fc=FILL[fill], ec="none", zorder=2.6))
    ax.add_patch(Ellipse((x + w / 2, y + h - e / 2), w, e, fc=FILL[fill], ec=INK, lw=1.1, zorder=3))
    if body:
        text(ax, x + w / 2, y + h - 0.3, title, weight="bold")
        text(ax, x + w / 2, y + (h - 0.4) / 2, body, size=FS - 0.8)
    else:
        text(ax, x + w / 2, y + h / 2 - 0.04, title, weight="bold")


def mid(b, side):
    x, y, w, h = b
    return {"l": (x, y + h / 2), "r": (x + w, y + h / 2), "t": (x + w / 2, y + h), "b": (x + w / 2, y)}[side]


def at(b, side, f):
    """Điểm trên cạnh side của hộp, f là tỉ lệ dọc theo cạnh (0 đến 1)."""
    x, y, w, h = b
    return {"l": (x, y + h * f), "r": (x + w, y + h * f), "t": (x + w * f, y + h), "b": (x + w * f, y)}[side]


# ------------------------------------------------------------------ sơ đồ tuần tự
class Seq:
    def __init__(self, ax, names, x0, x1, top, bottom, box_w=1.05, box_h=0.46):
        self.ax, self.top, self.bottom = ax, top, bottom
        n = len(names)
        self.x = [x0 + i * (x1 - x0) / (n - 1) for i in range(n)]
        for x, s in zip(self.x, names):
            rbox(ax, x - box_w / 2, top - box_h, box_w, box_h, s, fill="l", tsize=FS - 0.6, r=0.04)
            ax.plot([x, x], [top - box_h, bottom], color=MUTED, lw=0.8, ls=(0, (4, 3)), zorder=1)

    def act(self, i, y0, y1, dx=0.0):
        self.ax.add_patch(Rectangle((self.x[i] - 0.055 + dx, y1), 0.11, y0 - y1, fc="white", ec=INK, lw=0.9, zorder=3))

    def msg(self, i, j, y, s, ret=False, dx_i=0.055, dx_j=0.055, lsize=FS - 1.1):
        xi, xj = self.x[i], self.x[j]
        if i == j:  # tự gọi
            p = xi + dx_i
            self.ax.plot([p, p + 0.32, p + 0.32], [y, y, y - 0.17], color=INK, lw=0.9, zorder=4)
            arrow(self.ax, (p + 0.32, y - 0.17), (p + 0.02, y - 0.17))
            text(self.ax, p + 0.4, y - 0.08, s, size=lsize, ha="left")
            return
        sgn = 1 if xj > xi else -1
        a, b = xi + sgn * dx_i, xj - sgn * dx_j
        arrow(self.ax, (a, y), (b, y), ls=(0, (4, 2.5)) if ret else "-", head="->" if ret else "-|>", lw=0.9)
        text(self.ax, (a + b) / 2, y + 0.09, s, size=lsize, bbox=dict(fc="white", ec="none", pad=0.3))

    def fragment(self, x0, x1, y0, y1, kind, guard, split=None, guard2=None):
        ax = self.ax
        ax.add_patch(Rectangle((x0, y1), x1 - x0, y0 - y1, fc="none", ec=INK, lw=0.9, zorder=2))
        tw = 0.12 + 0.075 * len(kind)
        ax.add_patch(plt.Polygon([(x0, y0), (x0 + tw, y0), (x0 + tw, y0 - 0.13), (x0 + tw - 0.07, y0 - 0.21),
                                  (x0, y0 - 0.21)], closed=True, fc="white", ec=INK, lw=0.9, zorder=2.5))
        text(ax, x0 + 0.06, y0 - 0.1, kind, size=FS - 1.2, weight="bold", ha="left")
        text(ax, x0 + tw + 0.08, y0 - 0.1, f"[{guard}]", size=FS - 1.2, ha="left", style="italic")
        if split is not None:
            ax.plot([x0, x1], [split, split], color=INK, lw=0.9, ls=(0, (4, 3)), zorder=2)
            text(ax, x0 + 0.08, split - 0.12, f"[{guard2}]", size=FS - 1.2, ha="left", style="italic")


# ================================================================== Hình 3.7: use case tổng quát
def fig_use_case():
    W, H = 6.6, 4.95
    fig, ax = canvas(W, H)
    frame(ax, 1.6, 0.02, 4.95, 4.88, "Hệ thống MedKG", ls="-")
    user, admin = (0.75, 2.75), (0.75, 0.3)
    actor(ax, *user, "Người dùng")
    actor(ax, *admin, "Quản trị viên")
    cx, w, h = 4.15, 2.95, 0.4
    names = ["Phân tích một văn bản", "Phân tích theo lô", "Xem và tìm kiếm lịch sử", "Xóa văn bản đã lưu",
             "Khám phá đồ thị tri thức", "Xuất đồ thị tri thức", "Xem trạng thái hệ thống"]
    hand = (user[0] + 0.2, user[1] + 0.49)
    for i, s in enumerate(names):
        y = 4.35 - i * 0.5
        usecase(ax, cx, y, w, h, s)
        ax.plot([hand[0], cx - w / 2], [hand[1], y], color=INK, lw=0.9, zorder=2)
    ahand = (admin[0] + 0.2, admin[1] + 0.49)
    for y, s in ((0.85, "Nạp dữ liệu có sẵn"), (0.33, "Cấu hình và triển khai")):
        usecase(ax, cx, y, w, h, s, fill="l")
        ax.plot([ahand[0], cx - w / 2], [ahand[1], y], color=INK, lw=0.9, zorder=2)
    # quản trị viên kế thừa người dùng (mũi tên tam giác rỗng)
    arrow(ax, (admin[0], admin[1] + 0.86), (user[0], user[1] - 0.32), head="-|>", hollow=True)
    text(ax, admin[0] + 0.08, 1.75, "kế thừa", size=FS - 1.4, style="italic", ha="left")
    save(fig, "ht_uc_tong_quat.png")


# ================================================================== Hình 3.9: kiến trúc tổng thể
def fig_architecture():
    W, H = 6.6, 4.6
    fig, ax = canvas(W, H)
    client = rbox(ax, 0.1, 3.7, 1.4, 0.8, "Trình duyệt", "giao diện một trang\nReact, TypeScript", fill="l")
    frame(ax, 1.95, 0.1, 4.55, 4.45, "Máy chủ Docker", ls="--")
    web = rbox(ax, 2.2, 3.55, 2.1, 0.75, "Máy chủ web", "Nginx, tệp giao diện tĩnh,\nchuyển tiếp yêu cầu API")
    rbox(ax, 2.2, 1.0, 2.1, 2.2, fill="w")
    text(ax, 3.25, 3.0, "Dịch vụ API", weight="bold")
    text(ax, 3.25, 2.8, "FastAPI, Uvicorn, PyTorch", size=FS - 0.8)
    for i, s in enumerate(["Nhận diện thực thể", "Gán mã ICD-10, RxNorm", "Trích xuất quan hệ", "Đồ thị tri thức",
                           "Lưu trữ kết quả"]):
        rbox(ax, 2.35, 2.38 - i * 0.27, 1.8, 0.22, s, fill="l", weight="normal", tsize=FS - 1, r=0.03)
    cylinder(ax, 4.75, 1.4, 1.45, 1.05, "Cơ sở dữ liệu", "PostgreSQL\nvăn bản, kết quả")
    models = rbox(ax, 4.65, 0.25, 1.65, 0.7, "Thư mục mô hình", "ViHealthBERT NER, RE\ngắn chỉ đọc", fill="m", ls="--")
    rx = rbox(ax, 0.1, 1.6, 1.3, 0.75, "Dịch vụ RxNav", "tra mã thuốc\nqua Internet", fill="m", ls="--")
    arrow(ax, mid(client, "r"), (2.2, 4.1), "HTTP", loff=(0, 0.13))
    arrow(ax, mid(web, "b"), (3.25, 3.2), "chuyển tiếp yêu cầu API", loff=(0.12, 0.0), lha="left", lsize=FS - 1.4)
    arrow(ax, (4.3, 1.95), (4.75, 1.95), "SQL", loff=(0, 0.11), lsize=FS - 1.4)
    poly(ax, [(3.25, 1.0), (3.25, 0.6), mid(models, "l")], "nạp khi khởi động", lpos=1, loff=(0.05, 0.1),
         lsize=FS - 1.4)
    arrow(ax, (2.2, 1.97), mid(rx, "r"), "tên thuốc chưa\ncó trong bộ đệm", loff=(0.0, -0.27), lsize=FS - 1.8)
    save(fig, "ht_kien_truc.png")


# ================================================================== Hình 3.10: luồng dữ liệu
def fig_dfd():
    W, H = 6.6, 4.85
    fig, ax = canvas(W, H)
    PW, PH = 1.45, 0.62

    def proc(x, y, n, s):
        return rbox(ax, x, y, PW, PH, n, s, fill="w", r=0.15, tsize=FS - 0.6, bsize=FS - 1)

    def ext(x, y, s, w=1.15):
        return rbox(ax, x, y, w, PH, s, fill="m", r=0.0, tsize=FS - 0.6)

    def store(x, y, n, s, w=1.55, h=0.38):
        ax.add_patch(Rectangle((x, y), w, h, fc=FILL["l"], ec="none", zorder=1))
        ax.plot([x, x + w], [y + h, y + h], color=INK, lw=1.0)
        ax.plot([x, x + w], [y, y], color=INK, lw=1.0)
        ax.plot([x + 0.32, x + 0.32], [y, y + h], color=INK, lw=1.0)
        text(ax, x + 0.16, y + h / 2, n, weight="bold", size=FS - 1)
        text(ax, x + 0.32 + (w - 0.32) / 2, y + h / 2, s, size=FS - 1.5)
        return (x, y, w, h)

    r1, r2, r3 = 3.55, 2.3, 1.05
    xs = [1.45, 3.2, 4.95]
    user = ext(0.05, r1, "Người dùng")
    p1 = proc(xs[0], r1, "1. Tiếp nhận", "kiểm tra văn bản")
    p2 = proc(xs[1], r1, "2. Nhận diện", "thực thể")
    p3 = proc(xs[2], r1, "3. Gán mã", "ICD-10, RxNorm")
    p5 = proc(xs[0], r2, "5. Lưu kết quả", "và trả về")
    p4 = proc(xs[1], r2, "4. Trích xuất", "quan hệ")
    p6 = proc(xs[0], r3, "6. Cập nhật", "đồ thị tri thức")
    p7 = proc(xs[1], r3, "7. Truy vấn", "lịch sử, đồ thị")
    user2 = ext(5.2, r3, "Người dùng")
    d2 = store(xs[1] - 0.05, 4.4, "D2", "mô hình NER")
    d3 = store(xs[2] - 0.05, 4.4, "D3", "ICD-10, bộ đệm\nRxNorm", w=1.6, h=0.42)
    d4 = store(5.0, r2 + 0.12, "D4", "mô hình RE", w=1.5)
    d1 = store(0.0, r2 + 0.12, "D1", "văn bản,\nkết quả", w=1.2, h=0.42)
    d5 = store(xs[0], 0.12, "D5", "đồ thị trong\nbộ nhớ", w=PW, h=0.42)
    s = FS - 1.6
    arrow(ax, mid(user, "r"), mid(p1, "l"), "văn bản", loff=(0, 0.1), lsize=s)
    arrow(ax, mid(p1, "r"), mid(p2, "l"), "văn bản\nhợp lệ", loff=(0, 0.17), lsize=s)
    arrow(ax, mid(p2, "r"), mid(p3, "l"), "thực thể", loff=(0, 0.1), lsize=s)
    arrow(ax, (xs[1] + PW / 2, 4.4), mid(p2, "t"), "trọng số", loff=(0.3, 0.0), lsize=s)
    arrow(ax, (xs[2] + 0.75, 4.4), mid(p3, "t"), "tra mã", loff=(0.27, 0.0), lsize=s)
    arrow(ax, mid(p2, "b"), mid(p4, "t"), "thực thể", loff=(0.3, 0.0), lsize=s)
    arrow(ax, at(p3, "b", 0.3), at(p4, "r", 0.85), "mã chuẩn", loff=(0.38, 0.12), lsize=s)
    arrow(ax, mid(d4, "l"), (xs[1] + PW, d4[1] + 0.19), "trọng số", loff=(0.0, -0.13), lsize=s)
    arrow(ax, mid(p4, "l"), mid(p5, "r"), "kết quả\nđầy đủ", loff=(0, 0.17), lsize=s)
    poly(ax, [at(p5, "t", 0.3), (xs[0] + PW * 0.3, 3.3), (0.62, 3.3), mid(user, "b")], "kết quả", lpos=1,
         loff=(0, 0.09), lsize=s)
    arrow(ax, mid(p5, "l"), (1.2, d1[1] + 0.21), "bản ghi", loff=(0, 0.12), lsize=s)
    arrow(ax, mid(p5, "b"), mid(p6, "t"), "kết quả", loff=(0.3, 0.0), lsize=s)
    poly(ax, [(0.6, d1[1]), (0.6, r3 + PH / 2), mid(p6, "l")], "dựng lại khi\nkhởi động", lpos=0,
         loff=(0.42, 0.0), lsize=s - 0.2)
    arrow(ax, mid(p6, "b"), mid(d5, "t"), "bộ ba", loff=(0.25, 0.0), lsize=s)
    poly(ax, [mid(d5, "r"), (xs[1] + 0.45, 0.33), at(p7, "b", 0.3)], "nút, cạnh", lpos=0, loff=(0.1, 0.09), lsize=s)
    poly(ax, [(0.3, d1[1]), (0.3, 0.04), (xs[1] + 1.05, 0.04), at(p7, "b", 0.72)], "lịch sử", lpos=1,
         loff=(1.25, 0.09), lsize=s)
    arrow(ax, at(user2, "l", 0.72), at(p7, "r", 0.72), "yêu cầu", loff=(0, 0.1), lsize=s)
    arrow(ax, at(p7, "r", 0.28), at(user2, "l", 0.28), "kết quả", loff=(0, -0.11), lsize=s)
    save(fig, "ht_luong_du_lieu.png")


# ================================================================== Hình 3.11: thành phần dịch vụ API
def fig_backend():
    W, H = 6.6, 4.75
    fig, ax = canvas(W, H)
    cw, gap, x0 = 1.48, 0.12, 0.2
    cx = [x0 + i * (cw + gap) for i in range(4)]

    def comp(c0, c1, y, s, fill):
        x = cx[c0]
        w = cx[c1] + cw - x
        return rbox(ax, x, y + 0.12, w, 0.52, s, fill=fill, weight="normal", tsize=FS - 0.5)

    ys = {"L": 3.62, "S": 2.47, "N": 1.32, "I": 0.17}
    for key, name, fill in (("L", "Lớp giao tiếp", "l"), ("S", "Lớp dịch vụ", "l"), ("N", "Lớp xử lý ngôn ngữ", None),
                            ("I", "Hạ tầng", None)):
        frame(ax, 0.05, ys[key], 6.5, 0.98, name, ls="-", fill=fill)
    L = [comp(i, i, ys["L"], s, "w") for i, s in enumerate(["Phân tích", "Hệ thống", "Lịch sử", "Đồ thị tri thức"])]
    eng = comp(0, 1, ys["S"], "Bộ điều phối suy luận\n(khóa tuần tự, nạp mô hình ở luồng nền)", "w")
    repo = comp(2, 2, ys["S"], "Kho dữ liệu", "w")
    kgs = comp(3, 3, ys["S"], "Dịch vụ đồ thị", "w")
    N = [comp(i, i, ys["N"], s, "l") for i, s in enumerate(["Nhận diện thực thể", "Trích xuất quan hệ", "Gán mã",
                                                             "Đồ thị tri thức"])]
    torch = comp(0, 1, ys["I"], "PyTorch, Transformers", "m")
    rx = comp(2, 2, ys["I"], "RxNav", "m")
    sql = comp(3, 3, ys["I"], "SQLAlchemy, PostgreSQL", "m")
    d = (0, (4, 2.5))

    def down(a, fa, b, fb):
        arrow(ax, at(a, "b", fa), at(b, "t", fb), ls=d, head="->", lw=0.8)
    down(L[0], 0.5, eng, 0.25)
    down(L[1], 0.5, eng, 0.75)
    down(L[2], 0.5, repo, 0.5)
    down(L[3], 0.5, kgs, 0.5)
    down(eng, 0.25, N[0], 0.5)
    down(eng, 0.75, N[1], 0.5)
    down(eng, 0.92, N[2], 0.3)
    down(kgs, 0.5, N[3], 0.5)
    down(N[0], 0.5, torch, 0.25)
    down(N[1], 0.5, torch, 0.75)
    down(N[2], 0.5, rx, 0.5)
    arrow(ax, mid(kgs, "l"), mid(repo, "r"), ls=d, head="->", lw=0.8)
    poly(ax, [at(repo, "r", 0.2), (cx[3] - 0.06, repo[1] + 0.1), (cx[3] - 0.06, sql[1] + 0.26), (cx[3], sql[1] + 0.26)],
         ls=d, head="->")
    text(ax, 3.3, 4.68, "mũi tên nét đứt: thành phần gọi tới thành phần được trỏ", size=FS - 1.6, style="italic",
         color=MUTED)
    save(fig, "ht_thanh_phan_api.png")


# ================================================================== Hình 3.12: thành phần giao diện
def fig_frontend():
    W, H = 6.6, 3.7
    fig, ax = canvas(W, H)
    rbox(ax, 2.0, 3.0, 2.6, 0.6, "Ứng dụng", "định tuyến trang, theo dõi trạng thái mô hình", fill="m",
         bsize=FS - 1.2)
    pages = ["Trang phân tích", "Trang lịch sử", "Trang đồ thị\ntri thức", "Trang hệ thống"]
    pb = [rbox(ax, 0.1 + i * 1.64, 1.85, 1.45, 0.62, s, fill="w", tsize=FS - 0.5) for i, s in enumerate(pages)]
    for b in pb:
        arrow(ax, (3.3, 3.0), mid(b, "t"), lw=0.9)
    shared = [("Khung hiển thị kết quả", "tô màu thực thể, bảng mã,\ndanh sách quan hệ"),
              ("Lớp gọi API", "gửi yêu cầu, đọc lỗi,\nkiểu dữ liệu"),
              ("Thư viện vẽ đồ thị", "Cytoscape.js,\nbố cục lực đẩy")]
    sb = [rbox(ax, 0.25 + i * 2.15, 0.55, 1.95, 0.8, a, b, fill="l", bsize=FS - 1.3, tsize=FS - 0.6)
          for i, (a, b) in enumerate(shared)]
    links = [(0, 0, 0.3, 0.3), (1, 0, 0.3, 0.75), (0, 1, 0.7, 0.2), (1, 1, 0.7, 0.4), (2, 1, 0.3, 0.6),
             (3, 1, 0.3, 0.85), (2, 2, 0.7, 0.4)]
    for p, s_, fp, fs in links:
        arrow(ax, at(pb[p], "b", fp), at(sb[s_], "t", fs), ls=(0, (4, 2.5)), head="->", lw=0.8)
    rbox(ax, 2.35, 0.03, 1.9, 0.3, "Dịch vụ API", fill="m", tsize=FS - 0.6, r=0.03)
    arrow(ax, mid(sb[1], "b"), (3.3, 0.33), "HTTP, JSON", loff=(0.5, 0.02), lsize=FS - 1.4)
    save(fig, "ht_thanh_phan_giao_dien.png")


# ================================================================== Hình 3.16: trạng thái mô hình
def fig_state():
    W, H = 6.6, 3.5
    fig, ax = canvas(W, H)

    def state(x, y, w, h, name, body):
        b = rbox(ax, x, y, w, h, fill="w", r=0.14)
        text(ax, x + w / 2, y + h - 0.18, name, weight="bold")
        ax.plot([x, x + w], [y + h - 0.34, y + h - 0.34], color=INK, lw=0.9)
        text(ax, x + w / 2, y + (h - 0.34) / 2, body, size=FS - 1.4)
        return b

    ax.add_patch(Ellipse((0.25, 2.2), 0.2, 0.2, fc=INK, ec=INK))
    load = state(0.85, 1.75, 1.55, 0.95, "Đang nạp", "phân tích trả 503\nlịch sử, đồ thị\nvẫn dùng được")
    ready = state(3.35, 2.35, 1.55, 0.95, "Sẵn sàng", "mọi chức năng\nphân tích tuần tự\ntheo khóa")
    err = state(3.35, 0.65, 1.55, 0.95, "Lỗi", "phân tích trả 503\nkèm thông báo lỗi")
    off = state(0.85, 0.1, 1.55, 0.95, "Tắt mô hình", "chỉ xem lịch sử\nvà đồ thị")
    arrow(ax, (0.35, 2.2), mid(load, "l"), "[bật nạp]", loff=(0, 0.13), lsize=FS - 1.4)
    poly(ax, [(0.25, 2.1), (0.25, 0.57), mid(off, "l")], "[tắt nạp]", lpos=0, loff=(0.0, 0), lsize=FS - 1.4)
    arrow(ax, at(load, "r", 0.75), mid(ready, "l"), "nạp xong", loff=(-0.05, 0.12), lsize=FS - 1.4)
    arrow(ax, at(load, "r", 0.25), mid(err, "l"), "ngoại lệ, ví dụ\nthiếu trọng số", loff=(-0.05, -0.05),
          lsize=FS - 1.4)
    ax.add_patch(Ellipse((6.05, 1.95), 0.24, 0.24, fc="white", ec=INK, lw=1.0))
    ax.add_patch(Ellipse((6.05, 1.95), 0.14, 0.14, fc=INK, ec=INK))
    arrow(ax, mid(ready, "r"), (5.95, 2.03), "dừng\ncontainer", loff=(0.05, 0.12), lsize=FS - 1.4)
    arrow(ax, mid(err, "r"), (5.95, 1.87), "khởi động\nlại", loff=(0.05, -0.12), lsize=FS - 1.4)
    save(fig, "ht_trang_thai.png")


# ================================================================== Hình 3.17: lớp chính
def fig_class():
    W, H = 6.6, 5.05
    fig, ax = canvas(W, H)
    CW = 1.95
    cols = [0.05, 2.33, 4.6]
    lh = 0.165

    def cls(c, top, name, attrs, ops, fill="w"):
        x = cols[c]
        h = 0.3 + lh * len(attrs) + 0.08 + lh * len(ops) + 0.08
        ax.add_patch(Rectangle((x, top - h), CW, h, fc=FILL[fill], ec=INK, lw=1.0, zorder=2))
        text(ax, x + CW / 2, top - 0.15, name, weight="bold", size=FS - 0.6)
        y1 = top - 0.3
        ax.plot([x, x + CW], [y1, y1], color=INK, lw=0.9, zorder=3)
        for i, a in enumerate(attrs):
            text(ax, x + 0.07, y1 - 0.04 - lh * (i + 0.5), a, size=FS - 1.7, ha="left")
        y2 = y1 - lh * len(attrs) - 0.08
        ax.plot([x, x + CW], [y2, y2], color=INK, lw=0.9, zorder=3)
        for i, o in enumerate(ops):
            text(ax, x + 0.07, y2 - 0.04 - lh * (i + 0.5), o, size=FS - 1.7, ha="left")
        return (x, top - h, CW, h)

    eng = cls(0, 5.0, "Bộ điều phối suy luận", ["- trạng thái, lỗi", "- thời gian nạp", "- khóa"],
              ["+ nạp()", "+ khởi động(nền)", "+ phân tích(văn bản)"])
    pipe = cls(0, 3.45, "Luồng trích xuất", ["- bỏ thực thể chung"], ["+ phân tích(văn bản)"])
    ner = cls(0, 2.3, "Luồng NER", ["- tiền xử lý, mô hình", "- quy tắc liều, hậu xử lý"], ["+ nhận diện(văn bản)"])
    norm = cls(0, 0.92, "Bộ gán mã", ["- ICD-10, RxNorm"], ["+ gán mã(thực thể)"])
    kgs = cls(1, 5.0, "Dịch vụ đồ thị", ["- đồ thị hiện tại", "- khóa"],
              ["+ dựng lại()", "+ thêm(mã, kết quả)", "+ đồ thị con(bộ lọc)", "+ tìm(chữ)", "+ lân cận(nút)"])
    kg = cls(1, 3.3, "Đồ thị tri thức", ["- nút, cạnh"], ["+ thêm văn bản(kết quả)"], fill="l")
    hyb = cls(1, 2.3, "Bộ trích xuất lai", ["- chế độ"], ["+ dự đoán(văn bản, thực thể)"])
    bert = cls(1, 1.2, "Mô hình ViHealthBERT RE", ["- ba mô hình theo seed", "- ngưỡng 0,5"],
               ["+ dự đoán cặp(các cặp)"])
    repo = cls(2, 5.0, "Kho dữ liệu", ["- kết nối"],
               ["+ thêm(kết quả)", "+ liệt kê(trang, từ khóa)", "+ lấy(mã)", "+ xóa(mã)", "+ duyệt kết quả()"])
    doc = cls(2, 3.3, "Văn bản", ["- mã, thời điểm, nguồn", "- nội dung", "- số thực thể, số quan hệ",
                                   "- thời gian xử lý", "- kết quả JSON"], [], fill="l")
    rules = cls(2, 1.2, "Bộ quy tắc RE", ["- năm quy tắc"], ["+ dự đoán(văn bản, thực thể)"], fill="l")

    def comp(a, b, pa, pb, label=None):
        """Quan hệ hợp thành: hình thoi đặc ở phía lớp chứa a."""
        p, q = at(a, *pa), at(b, *pb)
        ax.plot([p[0], q[0]], [p[1], q[1]], color=INK, lw=0.9, zorder=3)
        dx, dy = q[0] - p[0], q[1] - p[1]
        L = math.hypot(dx, dy)
        ux, uy = dx / L, dy / L
        k = 0.085
        pts = [p, (p[0] + ux * k - uy * k * 0.55, p[1] + uy * k + ux * k * 0.55), (p[0] + 2 * ux * k, p[1] + 2 * uy * k),
               (p[0] + ux * k + uy * k * 0.55, p[1] + uy * k - ux * k * 0.55)]
        ax.add_patch(plt.Polygon(pts, closed=True, fc=INK, ec=INK, zorder=5))

    comp(eng, pipe, ("b", 0.5), ("t", 0.5))
    comp(pipe, ner, ("b", 0.5), ("t", 0.5))
    comp(ner, norm, ("b", 0.5), ("t", 0.5))
    comp(pipe, hyb, ("r", 0.3), ("l", 0.6))
    comp(hyb, bert, ("b", 0.5), ("t", 0.5))
    comp(hyb, rules, ("r", 0.4), ("l", 0.55))
    comp(kgs, kg, ("b", 0.5), ("t", 0.5))
    arrow(ax, at(kgs, "r", 0.5), at(repo, "l", 0.5), ls=(0, (4, 2.5)), head="->", lw=0.9)
    arrow(ax, mid(repo, "b"), mid(doc, "t"), head="->", lw=0.9)
    text(ax, repo[0] + CW / 2 + 0.08, (repo[1] + 3.3) / 2, "1 .. *", size=FS - 1.6, ha="left")
    save(fig, "ht_lop.png")


# ================================================================== Hình 3.19: mô hình dữ liệu đồ thị tri thức
def fig_kg_model():
    W, H = 6.6, 3.45
    fig, ax = canvas(W, H)
    s1 = rbox(ax, 0.05, 2.75, 2.35, 0.55, "Câu 1", "“tiểu đường uống metformin”", fill="l", bsize=FS - 1)
    s2 = rbox(ax, 0.05, 1.98, 2.35, 0.55, "Câu 2", "“đái tháo đường dùng metformin”", fill="l", bsize=FS - 1)

    def node(x, y, title, sub):
        ax.add_patch(Ellipse((x, y), 1.75, 0.72, fc="white", ec=INK, lw=1.2, zorder=3))
        text(ax, x, y + 0.1, title, weight="bold")
        text(ax, x, y - 0.13, sub, size=FS - 1.4)
        return (x, y, 1.75, 0.72)
    a = node(3.45, 2.52, "ICD-10 E14", "Bệnh đái tháo đường")
    b = node(5.7, 2.52, "RxNorm 6809", "metformin")
    arrow(ax, ell_pt(a, b[:2]), ell_pt(b, a[:2]))
    text(ax, 4.57, 2.98, "treated_by", size=FS - 1)
    text(ax, 4.57, 2.08, "2 lần, 2 văn bản", size=FS - 1.6, style="italic")
    arrow(ax, mid(s1, "r"), (2.62, 2.62), ls=(0, (4, 2.5)), head="->", lw=0.8)
    arrow(ax, mid(s2, "r"), (2.62, 2.4), ls=(0, (4, 2.5)), head="->", lw=0.8)

    def panel(x, title, lines):
        rbox(ax, x, 0.05, 3.15, 1.6, fill="w")
        text(ax, x + 1.575, 1.45, title, weight="bold")
        for i, s in enumerate(lines):
            text(ax, x + 0.15, 1.17 - i * 0.22, "● " + s, size=FS - 1.3, ha="left")
    panel(0.05, "Nút", ["khóa là mã chuẩn, nếu chưa gán mã thì", "   là loại kèm chữ đã chuẩn hóa",
                         "tên hiển thị, loại thực thể", "các cách viết đã gặp và số lần",
                         "số lượt đề cập, số văn bản, mã gợi ý"])
    panel(3.4, "Cạnh", ["khóa là bộ ba nút đầu, quan hệ, nút đuôi", "số lần xuất hiện, số văn bản",
                         "số lần theo nguồn mô hình hoặc quy tắc", "điểm trung bình",
                         "tối đa ba câu nguồn làm ví dụ"])
    save(fig, "ht_mo_hinh_do_thi.png")


# ================================================================== Hình 3.20: triển khai
def fig_deploy():
    W, H = 6.6, 4.8
    fig, ax = canvas(W, H)

    def node3d(x, y, w, h, label, fill="w", d=0.12):
        ax.add_patch(plt.Polygon([(x, y + h), (x + d, y + h + d), (x + w + d, y + h + d), (x + w, y + h)], closed=True,
                                 fc=FILL["m"], ec=INK, lw=1.0, zorder=1))
        ax.add_patch(plt.Polygon([(x + w, y), (x + w + d, y + d), (x + w + d, y + h + d), (x + w, y + h)], closed=True,
                                 fc=FILL["d"], ec=INK, lw=1.0, zorder=1))
        ax.add_patch(Rectangle((x, y), w, h, fc=FILL[fill], ec=INK, lw=1.0, zorder=1))
        text(ax, x + 0.08, y + h - 0.2, label, weight="bold", ha="left", size=FS - 0.6)

    node3d(0.05, 3.3, 1.35, 0.85, "«thiết bị»\nMáy người dùng", fill="l")
    text(ax, 0.72, 3.5, "trình duyệt", size=FS - 1.2)
    node3d(0.05, 0.6, 1.35, 0.85, "«dịch vụ ngoài»\nRxNav", fill="m")
    text(ax, 0.72, 0.8, "tra mã thuốc", size=FS - 1.2)
    node3d(1.8, 0.1, 4.6, 4.3, "«máy chủ» Docker Engine", fill="l")
    ax.add_patch(Rectangle((1.95, 1.35), 4.3, 2.6, fc="none", ec=INK, lw=0.9, ls=(0, (4, 3))))
    text(ax, 2.03, 3.83, "mạng nội bộ của Compose", size=FS - 1.4, style="italic", ha="left")

    def cont(x, y, w, h, name, body):
        return rbox(ax, x, y, w, h, name, body, fill="w", r=0.03, tsize=FS - 0.4, bsize=FS - 1.4)
    web = cont(2.1, 2.65, 1.85, 0.95, "«container» web", "Nginx 1.27\ncổng 8080 ra ngoài, 80 bên trong")
    api = cont(4.25, 2.65, 1.85, 0.95, "«container» api", "Python 3.12, PyTorch CPU\ncổng 8000 nội bộ\ngiới hạn 6 GB RAM")
    db = cont(4.25, 1.5, 1.85, 0.8, "«container» db", "PostgreSQL 16\ncổng 5432 nội bộ")
    pg = rbox(ax, 4.25, 0.35, 1.85, 0.42, "«volume» dữ liệu CSDL", fill="m", tsize=FS - 1.3, r=0.03, weight="normal")
    md = rbox(ax, 2.1, 1.75, 1.85, 0.42, "«thư mục» mô hình, chỉ đọc", fill="m", tsize=FS - 1.3, r=0.03,
              weight="normal", ls="--")
    nc = rbox(ax, 2.1, 0.35, 1.85, 0.42, "«volume» bộ đệm RxNorm", fill="m", tsize=FS - 1.3, r=0.03, weight="normal")
    arrow(ax, (1.4, 3.75), at(web, "l", 0.62), "HTTP :8080", loff=(0, 0.13), lsize=FS - 1.4)
    arrow(ax, mid(web, "r"), mid(api, "l"), "/api", loff=(0, 0.1), lsize=FS - 1.4)
    arrow(ax, mid(api, "b"), mid(db, "t"), "SQL :5432", loff=(0.38, 0), lsize=FS - 1.4)
    arrow(ax, mid(db, "b"), mid(pg, "t"), head="-", lw=0.9)
    poly(ax, [at(api, "l", 0.2), (4.07, at(api, "l", 0.2)[1]), (4.07, mid(md, "r")[1]), mid(md, "r")], head="-")
    poly(ax, [at(api, "l", 0.08), (4.15, at(api, "l", 0.08)[1]), (4.15, mid(nc, "r")[1]), mid(nc, "r")], head="-")
    poly(ax, [at(api, "t", 0.8), (5.73, 4.65), (1.6, 4.65), (1.6, 1.02), (1.4, 1.02)], "HTTPS", lpos=1,
         loff=(0, 0.1), lsize=FS - 1.4)
    text(ax, 3.02, 1.5, "kiểm tra sức khỏe: web, api, db", size=FS - 1.6, style="italic", color=MUTED)
    save(fig, "ht_trien_khai.png")


# ================================================================== Hình 3.21: quy trình đóng gói và khởi chạy
def fig_build():
    W, H = 6.6, 3.65
    fig, ax = canvas(W, H)
    for name, y in (("Đóng gói", 2.45), ("Khởi chạy", 1.27), ("Vận hành", 0.05)):
        ax.add_patch(Rectangle((0.05, y), 6.5, 1.12, fc="none", ec=INK, lw=0.9))
        ax.add_patch(Rectangle((0.05, y), 0.42, 1.12, fc=FILL["m"], ec=INK, lw=0.9))
        text(ax, 0.26, y + 0.56, name, weight="bold", rotation=90, size=FS - 0.6)

    def step(x, y, s, w=1.35, h=0.62, fill="w"):
        return rbox(ax, x, y, w, h, s, fill=fill, weight="normal", tsize=FS - 1.2, r=0.08)
    src = step(0.65, 2.7, "mã nguồn\nhệ thống")
    nb = step(2.2, 3.0, "cài gói Node,\nbiên dịch giao diện", w=1.5, h=0.48)
    ng = step(3.9, 3.0, "image web\nNginx", w=1.3, h=0.48, fill="l")
    py = step(2.2, 2.52, "cài PyTorch CPU,\nthư viện Python", w=1.5, h=0.42)
    im = step(3.9, 2.52, "image api", w=1.3, h=0.42, fill="l")
    reg = step(5.45, 2.65, "kho image\n(tùy chọn)", w=1.0, h=0.62, fill="m")
    arrow(ax, at(src, "r", 0.8), mid(nb, "l"))
    arrow(ax, at(src, "r", 0.2), mid(py, "l"))
    arrow(ax, mid(nb, "r"), mid(ng, "l"))
    arrow(ax, mid(py, "r"), mid(im, "l"))
    arrow(ax, mid(ng, "r"), at(reg, "l", 0.8), ls=(0, (4, 2.5)), head="->")
    arrow(ax, mid(im, "r"), at(reg, "l", 0.2), ls=(0, (4, 2.5)), head="->")
    up = step(0.65, 1.52, "tạo tệp cấu hình,\nchạy compose up")
    s1 = step(2.2, 1.52, "db khởi động,\nkiểm tra sức khỏe", w=1.5)
    s2 = step(3.9, 1.52, "api tạo bảng, nạp\ndữ liệu, dựng đồ thị", w=1.3)
    s3 = step(5.45, 1.52, "nạp mô hình\nkhoảng 38 giây", w=1.0)
    for a, b in ((up, s1), (s1, s2), (s2, s3)):
        arrow(ax, mid(a, "r"), mid(b, "l"))
    o1 = step(0.65, 0.3, "api sẵn sàng,\nweb nhận truy cập", w=1.4)
    o2 = step(2.3, 0.3, "phân tích, lưu,\ncập nhật đồ thị", w=1.4)
    o3 = step(3.95, 0.3, "sao lưu CSDL,\nxem nhật ký", w=1.25)
    o4 = step(5.45, 0.3, "dừng,\ngiữ dữ liệu", w=1.0)
    poly(ax, [mid(s3, "b"), (5.95, 1.2), (1.35, 1.2), mid(o1, "t")])
    for a, b in ((o1, o2), (o2, o3), (o3, o4)):
        arrow(ax, mid(a, "r"), mid(b, "l"))
    save(fig, "ht_dong_goi.png")


# ================================================================== use case phân rã (kiểu mẫu: tác nhân, use case chính, các use case con)
def uc_decomp(name, actor_name, main, subs, H=None):
    """subs: danh sách (chữ, 'include' | 'extend'). Use case chính ở giữa, các use case con xếp cột bên phải."""
    n = len(subs)
    H = H or max(2.6, 0.62 * n + 0.75)
    W = 6.6
    fig, ax = canvas(W, H)
    frame(ax, 1.05, 0.05, 5.5, H - 0.1, main, ls="-")
    cy = (H - 0.25) / 2
    actor(ax, 0.45, cy - 0.45, actor_name)
    m = usecase(ax, 2.35, cy, 1.95, 0.6, main)
    ax.plot([0.65, m[0] - m[2] / 2], [cy + 0.05, cy], color=INK, lw=0.9)
    top = H - 0.55
    step = (top - 0.4) / max(1, n - 1) if n > 1 else 0
    dash = (0, (4, 2.5))
    for i, (s, kind) in enumerate(subs):
        y = top - i * step if n > 1 else cy
        u = usecase(ax, 5.05, y, 2.65, 0.5, s, fill="l" if kind == "include" else "m")
        left = (u[0] - u[2] / 2, u[1])
        src = ell_pt(m, left)
        if kind == "include":
            arrow(ax, src, left, ls=dash, head="->", label="«include»", lsize=FS - 1.9, lpos=0.72, loff=(0, 0.0))
        else:
            arrow(ax, left, src, ls=dash, head="->", label="«extend»", lsize=FS - 1.9, lpos=0.28, loff=(0, 0.0))
    save(fig, name)


def fig_uc_analyze():
    uc_decomp("ht_uc_phan_tich.png", "Người dùng", "Phân tích văn bản",
              [("Nhập văn bản hoặc chọn câu ví dụ", "include"), ("Kiểm tra độ dài văn bản", "include"),
               ("Nhận diện thực thể", "include"), ("Trích xuất quan hệ", "include"),
               ("Gán mã ICD-10, RxNorm", "extend"), ("Lưu vào lịch sử và đồ thị", "extend"),
               ("Phân tích theo lô", "extend")])


def fig_uc_history():
    uc_decomp("ht_uc_lich_su.png", "Người dùng", "Quản lý lịch sử phân tích",
              [("Xem danh sách văn bản đã phân tích", "include"), ("Tìm kiếm theo nội dung", "include"),
               ("Lọc theo nguồn văn bản", "include"), ("Xem lại kết quả chi tiết", "include"),
               ("Xóa văn bản khỏi lịch sử", "extend")])


def fig_uc_graph():
    uc_decomp("ht_uc_do_thi.png", "Người dùng", "Khám phá đồ thị tri thức",
              [("Xem thống kê đồ thị", "include"), ("Lọc theo quan hệ, loại nút", "include"),
               ("Tìm nút theo tên, mã, cách viết", "include"), ("Xem lân cận và câu nguồn", "include"),
               ("Xuất đồ thị ra JSON, CSV", "extend")])


def fig_uc_admin():
    uc_decomp("ht_uc_quan_tri.png", "Quản trị viên", "Quản trị hệ thống",
              [("Cấu hình biến môi trường", "include"), ("Khởi chạy bằng Docker Compose", "include"),
               ("Theo dõi trạng thái và nhật ký", "include"), ("Nạp dữ liệu có sẵn", "extend"),
               ("Sao lưu cơ sở dữ liệu", "extend")])


# ================================================================== biểu đồ hoạt động theo làn
class Act:
    """Các làn dọc có tiêu đề; nút được đặt theo tâm (x, y)."""

    def __init__(self, ax, lanes, W, H, head=0.34):
        self.ax = ax
        n = len(lanes)
        lw = (W - 0.1) / n
        self.cx = []
        ax.add_patch(Rectangle((0.05, 0.05), W - 0.1, H - 0.1, fc="none", ec=INK, lw=1.3))
        for i, s in enumerate(lanes):
            x = 0.05 + i * lw
            ax.add_patch(Rectangle((x, H - 0.05 - head), lw, head, fc=FILL["m"], ec=INK, lw=1.1))
            if i:
                ax.plot([x, x], [0.05, H - 0.05], color=INK, lw=1.1)
            text(ax, x + lw / 2, H - 0.05 - head / 2, s, weight="bold")
            self.cx.append(x + lw / 2)

    def start(self, lane, y):
        self.ax.add_patch(Ellipse((self.cx[lane], y), 0.2, 0.2, fc=INK, ec=INK, zorder=4))
        return (self.cx[lane] - 0.1, y - 0.1, 0.2, 0.2)

    def end(self, lane, y, dx=0.0):
        x = self.cx[lane] + dx
        self.ax.add_patch(Ellipse((x, y), 0.24, 0.24, fc="white", ec=INK, lw=1.1, zorder=4))
        self.ax.add_patch(Ellipse((x, y), 0.14, 0.14, fc=INK, ec=INK, zorder=5))
        return (x - 0.12, y - 0.12, 0.24, 0.24)

    def node(self, lane, y, s, w=1.75, h=0.44, dx=0.0):
        x = self.cx[lane] + dx
        return rbox(self.ax, x - w / 2, y - h / 2, w, h, s, fill="w", weight="normal", tsize=FS - 1.1, r=0.1, z=3)

    def decide(self, lane, y, s, w=1.15, h=0.6, dx=0.0):
        x = self.cx[lane] + dx
        self.ax.add_patch(plt.Polygon([(x, y + h / 2), (x + w / 2, y), (x, y - h / 2), (x - w / 2, y)], closed=True,
                                      fc="white", ec=INK, lw=1.1, zorder=3))
        text(self.ax, x, y, s, size=FS - 1.5)
        return (x - w / 2, y - h / 2, w, h)

    def go(self, pts, label=None, lpos=0, loff=(0.1, 0.08), lha="left"):
        if len(pts) == 2:
            arrow(self.ax, pts[0], pts[1], head="->", lw=1.0)
        else:
            poly(self.ax, pts, head="->")
        if label:
            a, b = pts[lpos], pts[lpos + 1]
            text(self.ax, a[0] + loff[0], a[1] + loff[1] if a[1] == b[1] else a[1] - 0.12, label, size=FS - 1.2,
                 weight="bold", ha=lha)


def fig_act_analyze():
    W, H = 6.6, 7.75
    fig, ax = canvas(W, H)
    a = Act(ax, ["Người dùng", "Dịch vụ API", "Luồng xử lý và CSDL"], W, H)
    U, S, N = 0, 1, 2
    st = a.start(U, 7.05)
    u1 = a.node(U, 6.50, "Nhập văn bản, chọn\ngán mã và lưu kết quả")
    u2 = a.node(U, 5.85, "Bấm Phân tích")
    s1 = a.node(S, 5.85, "Kiểm tra độ dài\nvăn bản")
    d1 = a.decide(S, 5.10, "Hợp lệ?")
    d2 = a.decide(S, 4.25, "Mô hình\nsẵn sàng?")
    ue = a.node(U, 4.67, "Hiển thị thông báo lỗi")
    e1 = a.end(U, 4.00)
    n1 = a.node(N, 4.25, "Nhận diện thực thể\nbằng ViHealthBERT")
    n2 = a.node(N, 3.60, "Gán mã ICD-10,\nRxNorm")
    n3 = a.node(N, 2.95, "Trích xuất quan hệ\nbằng ViHealthBERT-RE")
    d3 = a.decide(S, 2.95, "Lưu kết quả?")
    n4 = a.node(N, 2.25, "Lưu bản ghi vào\ncơ sở dữ liệu")
    n5 = a.node(N, 1.65, "Cập nhật đồ thị\ntri thức")
    s2 = a.node(S, 1.05, "Trả kết quả JSON")
    u3 = a.node(U, 1.05, "Xem thực thể, mã\nvà quan hệ", w=1.6)
    e2 = a.end(U, 0.35)
    a.go([mid(st, "b"), mid(u1, "t")])
    a.go([mid(u1, "b"), mid(u2, "t")])
    a.go([mid(u2, "r"), mid(s1, "l")])
    a.go([mid(s1, "b"), mid(d1, "t")])
    a.go([mid(d1, "b"), mid(d2, "t")], "Đ", loff=(0.08, 0))
    a.go([mid(d1, "l"), (a.cx[U], 5.10), mid(ue, "t")], "S", lpos=0, loff=(-0.25, 0.08))
    a.go([mid(d2, "l"), (a.cx[U] + 0.5, 4.25), (a.cx[U] + 0.5, ue[1])], "S", lpos=0, loff=(-0.25, 0.08))
    a.go([mid(ue, "b"), mid(e1, "t")])
    a.go([mid(d2, "r"), mid(n1, "l")], "Đ", loff=(0.12, 0.08))
    a.go([mid(n1, "b"), mid(n2, "t")])
    a.go([mid(n2, "b"), mid(n3, "t")])
    a.go([mid(n3, "l"), mid(d3, "r")])
    a.go([mid(d3, "b"), (a.cx[S], 2.25), mid(n4, "l")], "Đ", lpos=0, loff=(0.08, 0))
    a.go([mid(d3, "l"), (a.cx[S] - 0.95, 2.95), (a.cx[S] - 0.95, 1.5), (a.cx[S] - 0.4, 1.5), (a.cx[S] - 0.4, s2[1] + s2[3])],
         "S", lpos=0, loff=(-0.25, 0.08))
    a.go([mid(n4, "b"), mid(n5, "t")])
    a.go([mid(n5, "b"), (a.cx[N], 1.05), mid(s2, "r")])
    a.go([mid(s2, "l"), mid(u3, "r")])
    a.go([mid(u3, "b"), mid(e2, "t")])
    save(fig, "ht_act_phan_tich.png")


def fig_act_graph():
    W, H = 6.6, 6.9
    fig, ax = canvas(W, H)
    a = Act(ax, ["Người dùng", "Giao diện web", "Dịch vụ API"], W, H)
    U, G, S = 0, 1, 2
    st = a.start(U, 6.2)
    u1 = a.node(U, 5.65, "Mở trang\nĐồ thị tri thức")
    s1 = a.node(S, 5.65, "Lấy đồ thị con theo\nbộ lọc mặc định")
    g1 = a.node(G, 5.0, "Vẽ đồ thị bằng\nbố cục lực đẩy")
    u2 = a.node(U, 4.35, "Nhập từ khóa hoặc\nchọn bộ lọc")
    s2 = a.node(S, 4.35, "Tìm nút theo tên,\nmã, cách viết")
    d1 = a.decide(G, 3.6, "Có nút\nkhớp?")
    g2 = a.node(G, 2.85, "Hiển thị danh sách\nnút khớp")
    u3 = a.node(U, 2.85, "Chọn một nút")
    s3 = a.node(S, 2.2, "Lấy lân cận và đồ thị\ncon quanh nút")
    g3 = a.node(G, 1.55, "Vẽ lân cận, hiện bảng\nchi tiết và câu nguồn")
    d2 = a.decide(U, 1.55, "Xuất dữ\nliệu?")
    s4 = a.node(S, 0.6, "Trả kg.json hoặc\ntriples.csv")
    e = a.end(U, 0.6)
    a.go([mid(st, "b"), mid(u1, "t")])
    a.go([mid(u1, "r"), mid(s1, "l")])
    a.go([mid(s1, "b"), (a.cx[S], 5.0), mid(g1, "r")])
    a.go([mid(g1, "l"), (a.cx[U], 5.0), mid(u2, "t")])
    a.go([mid(u2, "r"), mid(s2, "l")])
    a.go([mid(s2, "b"), (a.cx[S], 3.6), mid(d1, "r")])
    a.go([mid(d1, "b"), mid(g2, "t")], "Đ", loff=(0.08, 0))
    a.go([mid(d1, "l"), (a.cx[U] + 0.35, 3.6), (a.cx[U] + 0.35, u2[1])], "S", lpos=0, loff=(-0.25, 0.08))
    a.go([mid(g2, "l"), mid(u3, "r")])
    a.go([mid(u3, "b"), (a.cx[U], 2.2), mid(s3, "l")])
    a.go([mid(s3, "b"), (a.cx[S], 1.55), mid(g3, "r")])
    a.go([mid(g3, "l"), mid(d2, "r")])
    a.go([mid(d2, "b"), (a.cx[U], 0.95), (a.cx[S], 0.95), mid(s4, "t")], "Đ", lpos=0, loff=(0.08, 0))
    a.go([mid(s4, "l"), mid(e, "r")])
    a.go([mid(d2, "l"), (0.25, 1.55), (0.25, 0.6), mid(e, "l")], "S", lpos=0, loff=(-0.05, 0.08), lha="right")
    save(fig, "ht_act_do_thi.png")


def fig_act_startup():
    W, H = 6.6, 7.3
    fig, ax = canvas(W, H)
    a = Act(ax, ["Quản trị viên", "Docker Compose", "Dịch vụ API"], W, H)
    A, C, S = 0, 1, 2
    st = a.start(A, 6.6)
    a1 = a.node(A, 6.05, "Tạo tệp cấu hình,\nchạy compose up")
    c1 = a.node(C, 6.05, "Khởi động cơ sở\ndữ liệu")
    d1 = a.decide(C, 5.3, "Kiểm tra sức\nkhỏe đạt?")
    c2 = a.node(C, 4.5, "Khởi động API")
    s1 = a.node(S, 4.5, "Tạo bảng nếu\nchưa có")
    d2 = a.decide(S, 3.8, "CSDL\ntrống?")
    s2 = a.node(S, 3.1, "Nạp 3.496 kết quả\ncó sẵn", dx=0.0)
    s3 = a.node(S, 2.45, "Dựng đồ thị tri thức\ntừ CSDL")
    s4 = a.node(S, 1.8, "Nạp NER, RE ba seed\nở luồng nền")
    d3 = a.decide(S, 1.05, "Nạp thành\ncông?")
    c3 = a.node(C, 1.05, "Khởi động web,\nnhận truy cập")
    a2 = a.node(A, 1.8, "Xem nhật ký,\nsửa cấu hình")
    e = a.end(C, 0.35)
    a.go([mid(st, "b"), mid(a1, "t")])
    a.go([mid(a1, "r"), mid(c1, "l")])
    a.go([mid(c1, "b"), mid(d1, "t")])
    a.go([mid(d1, "r"), (a.cx[C] + 0.95, 5.3), (a.cx[C] + 0.95, 6.05), mid(c1, "r")], "S", lpos=0,
         loff=(0.05, 0.08))
    text(ax, a.cx[C] + 0.72, 5.68, "chờ, thử lại", size=FS - 1.8, style="italic", rotation=90)
    a.go([mid(d1, "b"), mid(c2, "t")], "Đ", loff=(0.08, 0))
    a.go([mid(c2, "r"), mid(s1, "l")])
    a.go([mid(s1, "b"), mid(d2, "t")])
    a.go([mid(d2, "b"), mid(s2, "t")], "Đ", loff=(0.08, 0))
    a.go([mid(d2, "r"), (a.cx[S] + 0.95, 3.8), (a.cx[S] + 0.95, 2.45), mid(s3, "r")], "S", lpos=0,
         loff=(0.05, 0.08))
    a.go([mid(s2, "b"), mid(s3, "t")])
    a.go([mid(s3, "b"), mid(s4, "t")])
    a.go([mid(s4, "b"), mid(d3, "t")])
    a.go([mid(d3, "l"), mid(c3, "r")], "Đ", loff=(-0.25, 0.08))
    a.go([mid(d3, "b"), (a.cx[S], 0.15), (a.cx[A], 0.15), mid(a2, "b")], "S", lpos=0,
         loff=(0.08, 0))
    a.go([mid(c3, "b"), mid(e, "t")])
    poly(ax, [mid(a2, "t"), (a.cx[A], 2.6), (a.cx[A] - 0.98, 2.6), (a.cx[A] - 0.98, 6.05), mid(a1, "l")], head="->")
    text(ax, a.cx[A] - 0.85, 4.3, "chạy lại", size=FS - 1.8, style="italic", rotation=90)
    save(fig, "ht_act_khoi_dong.png")


# ================================================================== sơ đồ tuần tự, thông điệp đánh số như mẫu
def fig_seq_analyze():
    W, H = 6.7, 7.4
    fig, ax = canvas(W, H)
    names = ["Người dùng", "Giao diện\nweb", "Dịch vụ\nAPI", "Bộ điều phối\nsuy luận", "Luồng xử lý\nngôn ngữ",
             "Cơ sở\ndữ liệu", "Dịch vụ\nđồ thị"]
    s = Seq(ax, names, 0.5, 6.2, 7.35, 0.05, box_w=0.86, box_h=0.5)
    X = s.x
    st = 0.3
    y = 6.6
    s.msg(0, 1, y, "1. Nhập văn bản")
    web0 = y
    y -= st
    s.msg(1, 2, y, "2. POST /api/analyze")
    api0 = y
    y -= st
    s.msg(2, 2, y, "2.1 Kiểm tra độ dài")
    y -= 0.42
    alt_top = y
    y -= 0.42
    s.msg(2, 1, y, "2.2 Lỗi 503", ret=True)
    y -= 0.25
    split = y
    y -= 0.42
    s.msg(2, 3, y, "3. Phân tích văn bản")
    eng0 = y
    y -= st
    s.msg(3, 3, y, "3.1 Giữ khóa")
    y -= 0.38
    s.msg(3, 4, y, "4. NER, gán mã, RE")
    nlp0 = y
    y -= st
    s.msg(4, 4, y, "4.1 Chạy ba bước")
    y -= 0.38
    s.msg(4, 3, y, "4.2 Thực thể, quan hệ", ret=True)
    s.act(4, nlp0, y)
    y -= st
    s.msg(3, 3, y, "3.2 Nhả khóa")
    y -= 0.38
    s.msg(3, 2, y, "3.3 Kết quả", ret=True)
    s.act(3, eng0, y)
    y -= 0.25
    opt_top = y
    y -= 0.42
    s.msg(2, 5, y, "5. Thêm bản ghi")
    y -= st
    s.msg(5, 2, y, "5.1 Mã bản ghi", ret=True)
    y -= st
    s.msg(2, 6, y, "6. Thêm bộ ba vào đồ thị")
    y -= 0.2
    s.fragment(X[2] - 0.3, X[6] + 0.45, opt_top, y, "opt", "lưu kết quả")
    y -= 0.12
    s.fragment(X[1] - 0.3, X[6] + 0.5, alt_top, y, "alt", "mô hình chưa sẵn sàng", split=split,
               guard2="mô hình sẵn sàng")
    y -= 0.3
    s.msg(2, 1, y, "2.3 Kết quả JSON", ret=True)
    s.act(2, api0, y)
    y -= st
    s.msg(1, 0, y, "1.1 Hiển thị kết quả", ret=True)
    s.act(1, web0, y)
    save(fig, "ht_seq_phan_tich.png")


def fig_seq_startup():
    W, H = 6.7, 6.3
    fig, ax = canvas(W, H)
    s = Seq(ax, ["Docker\nCompose", "Cơ sở\ndữ liệu", "Dịch vụ\nAPI", "Luồng nạp\nmô hình", "Giao diện\nweb"],
            0.55, 6.05, 6.25, 0.05, box_w=0.95, box_h=0.5)
    X = s.x
    st = 0.3
    y = 5.5
    s.msg(0, 1, y, "1. Khởi động db")
    db0 = y
    y -= st
    s.msg(1, 1, y, "1.1 Kiểm tra sức khỏe đạt")
    y -= 0.42
    s.msg(0, 2, y, "2. Khởi động api")
    api0 = y
    y -= st
    s.msg(2, 1, y, "2.1 Tạo bảng nếu chưa có")
    y -= 0.25
    opt_top = y
    y -= 0.42
    s.msg(2, 1, y, "2.2 Nạp 3.496 kết quả")
    y -= 0.2
    s.fragment(X[1] - 0.35, X[2] + 0.35, opt_top, y, "opt", "dữ liệu trống")
    y -= 0.3
    s.msg(2, 1, y, "2.3 Đọc mọi kết quả")
    y -= st
    s.msg(2, 2, y, "2.4 Dựng đồ thị tri thức")
    y -= 0.42
    s.msg(2, 3, y, "3. Bắt đầu luồng nền")
    ld0 = y
    y -= st
    s.msg(3, 3, y, "3.1 Nạp NER, RE ba seed")
    y -= 0.42
    s.msg(0, 4, y, "4. Khởi động web")
    web0 = y
    y -= st
    s.msg(3, 2, y, "3.2 Trạng thái sẵn sàng", ret=True)
    s.act(3, ld0, y)
    y -= 0.25
    loop_top = y
    y -= 0.42
    s.msg(4, 2, y, "5. GET /api/health")
    y -= st
    s.msg(2, 4, y, "5.1 Trạng thái, thời gian nạp", ret=True)
    y -= 0.2
    s.fragment(X[2] - 0.35, X[4] + 0.45, loop_top, y, "loop", "2 giây khi đang nạp, 15 giây khi sẵn sàng")
    y -= 0.1
    s.act(1, db0, y)
    s.act(2, api0, y)
    s.act(4, web0, y)
    save(fig, "ht_seq_khoi_dong.png")


def fig_seq_graph():
    W, H = 6.6, 4.55
    fig, ax = canvas(W, H)
    s = Seq(ax, ["Người dùng", "Trang đồ thị", "Dịch vụ API", "Dịch vụ đồ thị"], 0.6, 5.9, 4.5, 0.05, box_w=1.1)
    st = 0.25
    y = 3.75
    s.msg(0, 1, y, "1. Nhập từ khóa “tiểu đường”")
    p0 = y
    y -= st
    s.msg(1, 2, y, "2. GET /api/kg/search")
    y -= st
    s.msg(2, 3, y, "2.1 Tìm theo tên, mã, cách viết")
    y -= st
    s.msg(3, 2, y, "2.2 Nút khớp", ret=True)
    y -= st
    s.msg(2, 1, y, "2.3 Danh sách nút", ret=True)
    y -= 0.35
    s.msg(0, 1, y, "3. Chọn nút ICD-10 E14")
    y -= st
    s.msg(1, 2, y, "4. GET /api/kg/node")
    y -= st
    s.msg(2, 3, y, "4.1 Lân cận của nút")
    y -= st
    s.msg(3, 2, y, "4.2 Nút, cạnh, câu ví dụ", ret=True)
    y -= st
    s.msg(2, 1, y, "4.3 Chi tiết nút", ret=True)
    y -= 0.35
    s.msg(1, 2, y, "5. GET /api/kg?center=E14")
    y -= st
    s.msg(2, 3, y, "5.1 Lọc, giới hạn số cạnh")
    y -= st
    s.msg(3, 2, y, "5.2 Nút, cạnh, thống kê", ret=True)
    y -= st
    s.msg(2, 1, y, "5.3 Đồ thị con", ret=True)
    y -= st
    s.msg(1, 1, y, "5.4 Tính bố cục, vẽ")
    y -= 0.38
    s.msg(1, 0, y, "3.1 Đồ thị và bảng chi tiết", ret=True)
    s.act(1, p0, y)
    save(fig, "ht_seq_do_thi.png")


# ================================================================== cơ sở dữ liệu dạng bảng PK/kiểu như mẫu
def fig_erd():
    W, H = 6.6, 5.4
    fig, ax = canvas(W, H)
    lh = 0.2

    def table(x, top, w, name, rows, fill="w"):
        """rows: (khóa, 'tên: Kiểu'). Đầu bảng tô xám, cột khóa bên trái như mẫu."""
        h = 0.3 + lh * len(rows) + 0.08
        ax.add_patch(Rectangle((x, top - h), w, h, fc=FILL[fill], ec=INK, lw=1.3, zorder=2))
        ax.add_patch(Rectangle((x, top - 0.3), w, 0.3, fc=FILL["m"], ec=INK, lw=1.3, zorder=2))
        text(ax, x + w / 2, top - 0.15, name, weight="bold", size=FS - 0.2)
        ax.plot([x + 0.48, x + 0.48], [top - h, top - 0.3], color=INK, lw=0.8, zorder=3)
        for i, (k, f) in enumerate(rows):
            yy = top - 0.3 - 0.04 - lh * (i + 0.5)
            text(ax, x + 0.24, yy, k, size=FS - 1.6, weight="bold")
            text(ax, x + 0.55, yy, f, size=FS - 1.6, ha="left")
        return (x, top - h, w, h)

    doc = table(0.05, 5.3, 2.2, "documents", [
        ("PK", "id: Int"), ("", "created_at: DateTime"), ("", "source: String"), ("", "external_id: String"),
        ("", "text: Text"), ("", "n_entities: Int"), ("", "n_relations: Int"), ("", "elapsed_ms: Int"),
        ("", "result: JSONB")])
    res = table(2.6, 5.3, 1.85, "result (JSONB)", [("", "text: String"), ("", "elapsed_ms: Int"),
                                                     ("", "re_metadata: Object")], fill="l")
    ent = table(2.6, 4.05, 1.85, "entities[ ]", [("PK", "id: String"), ("", "text: String"), ("", "label: String"),
                                                  ("", "start, end: Int"), ("", "confidence: Float"),
                                                  ("", "re_excluded: String")], fill="l")
    rel = table(2.6, 2.2, 1.85, "relations[ ]", [("FK", "head: String"), ("FK", "tail: String"),
                                                   ("", "label: String"), ("", "score: Float"),
                                                   ("", "source: String")], fill="l")
    norm = table(4.75, 4.05, 1.72, "normalized", [("", "ontology: String"), ("", "code: String"),
                                                  ("", "label_standard: String"), ("", "match_method: String"),
                                                  ("", "match_score: Float")], fill="l")
    cand = table(4.75, 2.5, 1.72, "candidates[ ]", [("", "rank: Int"), ("", "code: String"),
                                                     ("", "label_standard: String"), ("", "match_score: Float")],
                 fill="l")
    rc = table(4.75, 1.15, 1.72, "relation_candidates[ ]", [("FK", "head, tail: String"),
                                                             ("", "allowed_relation: String"),
                                                             ("", "label, status: String")], fill="l")

    def crow(p, q, one_at_p=True):
        """Đường quan hệ một-nhiều: gạch đơn ở phía một, chân quạ ở phía nhiều."""
        ax.plot([p[0], q[0]], [p[1], q[1]], color=INK, lw=0.9, zorder=1)
        dx, dy = q[0] - p[0], q[1] - p[1]
        L = math.hypot(dx, dy)
        ux, uy = dx / L, dy / L
        nx, ny = -uy, ux
        a = (p[0] + ux * 0.08, p[1] + uy * 0.08)
        ax.plot([a[0] + nx * 0.07, a[0] - nx * 0.07], [a[1] + ny * 0.07, a[1] - ny * 0.07], color=INK, lw=0.9)
        b = (q[0] - ux * 0.13, q[1] - uy * 0.13)
        for k in (-1, 0, 1):
            ax.plot([b[0], q[0] + nx * 0.07 * k], [b[1], q[1] + ny * 0.07 * k], color=INK, lw=0.9)

    def one(p, q):
        ax.plot([p[0], q[0]], [p[1], q[1]], color=INK, lw=0.9, zorder=1)
        for t in (0.08, 0.13):
            for pt, sgn in ((p, 1), (q, -1)):
                dx, dy = q[0] - p[0], q[1] - p[1]
                L = math.hypot(dx, dy)
                ux, uy = dx / L * sgn, dy / L * sgn
                c = (pt[0] + ux * t, pt[1] + uy * t)
                ax.plot([c[0] - uy * 0.07, c[0] + uy * 0.07], [c[1] + ux * 0.07, c[1] - ux * 0.07], color=INK, lw=0.9)

    ry = doc[1] + 0.04 + lh * 0.5 + 0.04
    poly(ax, [(doc[0] + doc[2], ry), (2.42, ry), (2.42, res[1] + res[3] / 2), (2.6, res[1] + res[3] / 2)], head="-")
    text(ax, 2.33, (ry + res[1] + res[3] / 2) / 2, "1 : 1", size=FS - 1.8, rotation=90)
    crow(mid(res, "b"), mid(ent, "t"))
    poly(ax, [at(res, "l", 0.2), (2.52, at(res, "l", 0.2)[1]), (2.52, mid(rel, "l")[1]), (2.6, mid(rel, "l")[1])],
         head="-")
    crow(at(ent, "r", 0.7), at(norm, "l", 0.8))
    crow(at(ent, "r", 0.3), at(cand, "l", 0.6))
    poly(ax, [at(res, "r", 0.5), (6.56, at(res, "r", 0.5)[1]), (6.56, mid(rc, "r")[1]), mid(rc, "r")], head="-")
    text(ax, 1.15, 1.6, "Các bảng nền xám là cấu trúc lồng bên trong\ncột result kiểu JSONB, không phải bảng riêng.",
         size=FS - 1.6, style="italic", color=MUTED)
    save(fig, "ht_csdl.png")


if __name__ == "__main__":
    for f in (fig_use_case, fig_uc_analyze, fig_uc_history, fig_uc_graph, fig_uc_admin, fig_act_analyze, fig_act_graph,
              fig_act_startup, fig_architecture, fig_dfd, fig_backend, fig_frontend, fig_seq_analyze, fig_seq_startup,
              fig_seq_graph, fig_state, fig_class, fig_erd, fig_kg_model, fig_deploy, fig_build):
        f()

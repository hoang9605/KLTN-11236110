"""Các hình vẽ lại theo góp ý trên bản v16 (18/11/2026).

Phong cách figures4papers (f4p_style.py): khổ 12 inch, Arial, cỡ chữ gốc 16, thang xám
để in đen trắng. Mọi con số đọc từ tệp kết quả của dự án.

Chạy từ gốc repo:
    .venv/Scripts/python.exe -X utf8 outputs/bao_cao_khoa_luan_2026-11-05/figures/make_review_figures.py
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
K1, K2, K3, K4 = "#272727", "#4D4D4D", "#767676", "#CFCECE"
F1, F2, F3 = "#FFFFFF", "#F2F2F2", "#E0E0E0"  # nền ô: trắng, xám rất nhạt, xám nhạt


def J(p):
    return json.loads((ROOT / p).read_text(encoding="utf-8"))


def n(x):
    return f"{x:,}".replace(",", ".")


def save(fig, name):
    finalize_figure(fig, OUT / name, formats=["png", "pdf"], dpi=300, pad=0.08)
    print("wrote", name)


def canvas(w, h, xmax, ymax):
    fig = plt.figure(figsize=(w, h))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, xmax)
    ax.set_ylim(0, ymax)
    ax.axis("off")
    return fig, ax


def rbox(ax, x, y, w, h, fc=F2, ec=K1, lw=2.0, ls="-", r=0.12):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={r}", fc=fc, ec=ec, lw=lw, ls=ls))


def txt(ax, x, y, s, size=15, color=K1, weight="normal", ha="center", va="center", **kw):
    ax.text(x, y, s, fontsize=size, color=color, weight=weight, ha=ha, va=va, **kw)


def arr(ax, x0, y0, x1, y1, color=K1, lw=2.0, ls="-", style="-|>", rad=0.0):
    ax.annotate("", xy=(x1, y1), xytext=(x0, y0),
                arrowprops=dict(arrowstyle=style, color=color, lw=lw, ls=ls, shrinkA=0, shrinkB=0,
                                connectionstyle=f"arc3,rad={rad}", mutation_scale=18))


# ======================================================================
# Hình 2.1: một câu ví dụ đi qua ba bước, trong đó bước NER được mở ra thành gán nhãn BIO cho từng từ
# rồi giải mã thành thực thể có vị trí ký tự (gộp hai hình cũ h1_1_luong_ba_buoc và h1_bio_gan_nhan
# theo góp ý trên bản v19). Đầu ra thật của hệ thống cho câu này: đau → R52.9, Paracetamol → RxNorm 161.
# ======================================================================
sent = "Bệnh nhân đau dạ dày, kê Paracetamol 500mg."
words = ["Bệnh", "nhân", "đau", "dạ", "dày", "kê", "Paracetamol", "500mg"]
labels = ["O", "O", "B-CONDITION", "B-BODY_PART", "I-BODY_PART", "O", "B-DRUG", "B-DOSAGE"]
starts, pos = [], 0
for w in words:
    pos = sent.index(w, pos)
    starts.append(pos)
    pos += len(w)
D = 2.0  # độ dời lên của bước 2 và bước 3 so với hình cũ
fig, ax = canvas(12, 10.0, 24, 21.6)
LX = 0.2  # cột nhãn bước
BX = 5.0  # mép trái của nội dung
RW = 18.8  # bề rộng vùng nội dung
for y, a, b in [(20.6, "Đầu vào", "văn bản thô"), (17.6, "Bước 1. NER", "gán nhãn BIO rồi giải mã"),
                (8.6 + D, "Bước 2. Chuẩn hóa", "gán mã chuẩn"), (3.6 + D, "Bước 3. RE", "nối thực thể thành quan hệ")]:
    txt(ax, LX, y + 0.35, a, 17, weight="bold", ha="left")
    txt(ax, LX, y - 0.45, b, 14, K3, ha="left")
rbox(ax, BX, 19.9, RW, 1.4, fc=F2)
txt(ax, BX + RW / 2, 20.6, f"“{sent}”", 18, weight="bold")
# bước 1a: từ và nhãn BIO, ô rộng theo độ dài từ để nhãn dài không tràn
gap, base = 0.17, 1.75
k = (RW - len(words) * base - (len(words) - 1) * gap) / sum(len(w) for w in words)
cx, cwid, x = [], [], BX
for i, (w, lab) in enumerate(zip(words, labels)):
    cw = base + k * len(w)
    cx.append(x)
    cwid.append(cw)
    rbox(ax, x, 17.4, cw, 1.1, fc=F1 if lab == "O" else F3)
    txt(ax, x + cw / 2, 17.95, w, 14, weight="bold")
    txt(ax, x + cw / 2, 17.05, f"từ {i + 1}", 10.5, K3)
    txt(ax, x + cw / 2, 16.35, lab, 10 if lab != "O" else 13, K1 if lab != "O" else K3, family="Consolas",
        weight="bold" if lab != "O" else "normal")
    x += cw + gap
txt(ax, BX - 0.25, 17.95, "từ", 12.5, K3, ha="right")
txt(ax, BX - 0.25, 16.35, "nhãn BIO", 12.5, K3, ha="right")
# bước 1b: giải mã thành thực thể có vị trí ký tự
spans = [(2, 2, "CONDITION"), (3, 4, "BODY_PART"), (6, 6, "DRUG"), (7, 7, "DOSAGE")]
ew, eg = 4.4, 0.4
for j, (a, b, typ) in enumerate(spans):
    xa, xb = cx[a] + 0.1, cx[b] + cwid[b] - 0.1
    ax.plot([xa, xa, xb, xb], [15.95, 15.7, 15.7, 15.95], color=K1, lw=2.0)
    ex = BX + j * (ew + eg)
    ax.plot([(xa + xb) / 2, ex + ew / 2], [15.7, 14.95], color=K1, lw=2.0)
    text = " ".join(words[a:b + 1])
    rbox(ax, ex, 12.9, ew, 2.05, fc=F1)
    txt(ax, ex + ew / 2, 14.4, text, 17, weight="bold")
    txt(ax, ex + ew / 2, 13.75, typ, 12.5, K2, family="Consolas")
    txt(ax, ex + ew / 2, 13.2, f"ký tự {starts[a]} đến {starts[b] + len(words[b])}", 12, K3)
txt(ax, BX - 0.25, 13.9, "thực thể", 12.5, K3, ha="right")
# bước 2: chuẩn hóa
nw = 9.2
for x, a, b, c in [(BX, "đau", "ICD-10  R52.9", "Đau, không đặc hiệu"), (BX + 9.6, "Paracetamol", "RxNorm  161", "acetaminophen")]:
    rbox(ax, x, 7.5 + D, nw, 2.2, fc=F1)
    txt(ax, x + 0.5, 9.0 + D, a, 17, weight="bold", ha="left")
    arr(ax, x + 0.5 + (1.3 if a == "đau" else 3.6), 9.0 + D, x + (3.0 if a == "đau" else 5.3), 9.0 + D, lw=1.8)
    txt(ax, x + (3.3 if a == "đau" else 5.6), 9.0 + D, b, 17, weight="bold", ha="left")
    txt(ax, x + 0.5, 8.05 + D, c, 14, K3, ha="left")
txt(ax, BX + nw / 2, 7.0 + D, "chỉ CONDITION và DRUG được gán mã", 12.5, K3, style="italic")
# bước 3: RE, bộ ba (thực thể đầu, quan hệ, thực thể đuôi) kèm cách đọc
triples = [("đau", "located_at", "dạ dày", "đau ở dạ dày"),
           ("đau", "treated_by", "Paracetamol", "đau được điều trị bằng Paracetamol"),
           ("Paracetamol", "has_dosage", "500mg", "Paracetamol dùng liều 500mg")]
for xx, s in [(BX + 1.6, "Thực thể đầu"), (BX + 6.8, "Quan hệ"), (BX + 11.9, "Thực thể đuôi")]:
    txt(ax, xx, 6.0 + D, s, 13, K3)
txt(ax, BX + 14.4, 6.0 + D, "Cách đọc", 13, K3, ha="left")
for k3, (h, r, t, read) in enumerate(triples):
    y = 4.9 + D - k3 * 1.45
    rbox(ax, BX, y - 0.5, 3.2, 1.0, fc=F1)
    txt(ax, BX + 1.6, y, h, 16, weight="bold")
    arr(ax, BX + 3.2, y, BX + 10.3, y, lw=2.2)
    txt(ax, BX + 6.8, y + 0.32, r, 14, K1, family="Consolas", weight="bold")
    rbox(ax, BX + 10.3, y - 0.5, 3.2, 1.0, fc=F1)
    txt(ax, BX + 11.9, y, t, 16, weight="bold")
    txt(ax, BX + 14.4, y, read, 14, K2, ha="left", style="italic")
for y0, y1 in [(19.9, 18.55), (12.9, 9.7 + D), (7.5 + D, 6.45 + D)]:
    arr(ax, 14.4, y0, 14.4, y1, color=K3, lw=2.2)
ax.set_ylim(3.2, 21.5)
save(fig, "h1_1_luong_ba_buoc_bio.png")

# ======================================================================
# Hình 2.2: kiến trúc ViHealthBERT cho gán nhãn chuỗi, khổ hẹp chữ lớn để in rõ, nhãn tiếng Việt
# xác suất là đầu ra thật của mô hình cho subword "đau"
# ======================================================================
top5 = [("B-DISEASESYMTOM", 0.9972), ("I-DISEASESYMTOM", 0.0004), ("B-ORGAN", 0.0002), ("I-ORGAN", 0.0001), ("O", 0.0001)]
fig, ax = canvas(8, 7.8, 16, 15.6)
# cột trái: subword đầu vào, lớp embedding, bộ mã hóa
txt(ax, 0.2, 15.1, "Subword đầu vào", 13, K3, ha="left")
toks = ["<s>", "bệnh", "nhân", "đau", "…", "</s>"]
for i, t in enumerate(toks):
    x = 0.2 + i * 1.22
    hl = t == "đau"
    rbox(ax, x, 13.45, 1.12, 0.95, fc=K1 if hl else F1, ec=K1, lw=1.6, r=0.08)
    txt(ax, x + 0.56, 13.92, t, 13, "white" if hl else K1, weight="bold" if hl else "normal")
txt(ax, 0.2 + 3 * 1.22 + 0.56, 12.95, "x$_i$", 14)
arr(ax, 3.86, 12.65, 3.86, 12.15)
rbox(ax, 0.2, 10.55, 7.3, 1.6, fc=F2)
txt(ax, 3.85, 11.65, "Lớp embedding", 14.5, weight="bold")
txt(ax, 3.85, 10.95, "e$_i$ = embedding từ(x$_i$) + embedding vị trí(i)", 12, K2)
arr(ax, 3.86, 10.55, 3.86, 10.05)
rbox(ax, 0.2, 3.25, 7.3, 6.8, fc=F1, lw=2.4)
txt(ax, 3.85, 9.5, "Bộ mã hóa ViHealthBERT", 14.5, weight="bold")
txt(ax, 3.85, 8.9, "PhoBERT-base học thêm trên văn bản y tế", 11.5, K3)
inner = [("Tự chú ý nhiều đầu", F3), ("Cộng và chuẩn hóa lớp", F2), ("Mạng truyền thẳng", F3), ("Cộng và chuẩn hóa lớp", F2)]
for k, (lab, fc) in enumerate(inner):
    y = 7.55 - k * 1.08
    rbox(ax, 0.75, y, 5.2, 0.82, fc=fc, lw=1.5, r=0.08)
    txt(ax, 3.35, y + 0.41, lab, 12.5)
for k in range(3):
    arr(ax, 3.35, 7.55 - k * 1.08, 3.35, 7.55 - k * 1.08 - 0.26, lw=1.4)
ax.plot([6.2, 6.4, 6.4, 6.2], [8.37, 8.37, 4.31, 4.31], color=K1, lw=1.8)
txt(ax, 6.95, 6.35, "× 12", 15, weight="bold")
txt(ax, 3.85, 3.75, "kích thước ẩn 768, 12 đầu chú ý", 11.5, K3)
# huấn luyện
rbox(ax, 0.2, 0.55, 7.3, 2.15, fc=F1, ls="--", lw=1.6, r=0.08)
txt(ax, 3.85, 2.05, "Huấn luyện: L = − log p$_i$[y$_i$]", 12.5)
txt(ax, 3.85, 1.25, "AdamW cập nhật W, b và toàn bộ bộ mã hóa", 11.5, K2, style="italic")
# cột phải: vector ẩn, lớp tuyến tính, softmax, nhãn dự đoán
rbox(ax, 8.6, 12.9, 7.1, 1.5, fc=F2, r=0.08)
txt(ax, 12.15, 13.9, "Vector ẩn của lớp cuối", 13.5, weight="bold")
txt(ax, 12.15, 13.25, r"h$_i$ $\in\mathbb{R}^{768}$", 13, K2)
ax.plot([7.5, 8.05, 8.05], [6.65, 6.65, 13.65], color=K1, lw=2.0)
arr(ax, 8.05, 13.65, 8.6, 13.65)
arr(ax, 12.15, 12.9, 12.15, 12.35)
rbox(ax, 8.6, 10.2, 7.1, 2.15, fc=K4, r=0.08)
txt(ax, 12.15, 11.8, "Lớp tuyến tính", 13.5, weight="bold")
txt(ax, 12.15, 11.15, "z$_i$ = W$^{\\top}$h$_i$ + b", 13.5)
txt(ax, 12.15, 10.55, r"W $\in\mathbb{R}^{768\times37}$", 12.5, K2)
arr(ax, 12.15, 10.2, 12.15, 9.55)
txt(ax, 12.5, 9.85, "softmax", 12, K2, style="italic", ha="left")
txt(ax, 12.15, 9.05, r"p$_i$ = softmax(z$_i$) $\in\mathbb{R}^{37}$", 13, weight="bold")
txt(ax, 12.15, 8.45, "5 nhãn có xác suất cao nhất trong 37 nhãn", 11.5, K3)
bx = fig.add_axes([12.2 / 16, 4.15 / 15.6, 3.3 / 16, 3.7 / 15.6])
names = [a for a, _ in top5][::-1]
vals = [v for _, v in top5][::-1]
bx.barh(range(5), vals, color=[F1] * 4 + [K1], edgecolor=K1, linewidth=1.3, height=0.6)
bx.set_yticks(range(5), names, fontsize=11, family="Consolas")
bx.set_xlim(0, 1.0)
bx.set_xticks([0, 0.5, 1], ["0", "0,5", "1"], fontsize=11)
bx.tick_params(length=0)
bx.spines["left"].set_visible(False)
bx.spines["bottom"].set_linewidth(1.5)
bx.text(vals[-1] - 0.03, 4, "0,9972", fontsize=11, color="white", ha="right", va="center", weight="bold")
arr(ax, 13.85, 3.75, 13.85, 2.75)
rbox(ax, 8.6, 0.55, 7.1, 2.15, fc=F2, r=0.08)
txt(ax, 12.15, 2.0, "ŷ$_i$ = argmax p$_i$ = B-DISEASESYMTOM", 12.5, weight="bold")
txt(ax, 12.15, 1.2, "ánh xạ sang loại mục tiêu CONDITION", 11.5, K2)
ax.set_ylim(0.3, 15.5)
save(fig, "h1_3_kien_truc_vihealthbert.png")

# ======================================================================
# Hình 1.4: lược đồ quan hệ i2b2/VA 2010 (trái) và lược đồ quan hệ của đề tài (phải)
# ======================================================================
fig, ax = canvas(12, 6.4, 24, 12.8)


def node(x, y, w, label, sub=None, fc=F1, h=1.3):
    rbox(ax, x - w / 2, y - h / 2, w, h, fc=fc)
    if sub:
        txt(ax, x, y + 0.22, label, 15, weight="bold")
        txt(ax, x, y - 0.33, sub, 11.5, K2, family="Consolas")
    else:
        txt(ax, x, y, label, 15, weight="bold")


txt(ax, 5.3, 12.2, "i2b2/VA 2010: 3 nhóm khái niệm, 8 quan hệ", 15.5, weight="bold")
txt(ax, 17.6, 12.2, "Đề tài: 6 loại thực thể, 5 quan hệ", 15.5, weight="bold")
ax.plot([11.3, 11.3], [0.6, 12.4], color=K4, lw=2)
# trái
node(2.0, 9.3, 3.4, "Điều trị", "treatment", fc=F2)
node(2.0, 3.3, 3.4, "Xét nghiệm", "test", fc=F2)
node(8.6, 6.3, 3.4, "Vấn đề", "problem", fc=F2)
arr(ax, 3.7, 9.0, 6.9, 6.8, lw=2.6)
arr(ax, 3.7, 3.6, 6.9, 5.8, lw=2.6)
txt(ax, 0.3, 7.3, "TrAP  được dùng cho", 12.5, K1, weight="bold", ha="left")
txt(ax, 0.3, 6.75, "TrIP, TrWP, TrCP, TrNAP", 11.5, K3, ha="left")
txt(ax, 0.3, 5.5, "TeRP  phát hiện", 12.5, K1, weight="bold", ha="left")
txt(ax, 0.3, 4.95, "TeCP", 11.5, K3, ha="left")
ax.annotate("", xy=(9.6, 6.95), xytext=(7.6, 6.95),
            arrowprops=dict(arrowstyle="-|>", color=K3, lw=1.6, connectionstyle="arc3,rad=-1.4", mutation_scale=15))
txt(ax, 8.6, 8.85, "PIP", 11.5, K3)
txt(ax, 0.3, 0.6, "Chữ đậm: quan hệ được đề tài kế thừa. Chữ xám: quan hệ không dùng.", 11, K3, ha="left")
# phải: CONDITION bên trái, bốn thực thể đuôi xếp thành cột, DOSAGE nối với DRUG
C = (13.4, 6.7)
node(*C, 3.6, "CONDITION", fc=F3)
tails = {"BODY_PART": 10.6, "PROCEDURE": 8.0, "TEST": 5.4, "DRUG": 2.8}
TX = 21.6
for t, y in tails.items():
    node(TX, y, 3.8, t)
node(13.4, 2.8, 3.6, "DOSAGE")
edges = [("located_at", "BODY_PART", ":"), ("treated_by_procedure", "PROCEDURE", "-"), ("diagnosed_by", "TEST", "-"), ("treated_by", "DRUG", "-")]
for rel, t, ls in edges:
    y = tails[t]
    x0, y0, x1, y1 = C[0] + 1.8, C[1], TX - 1.9, y
    arr(ax, x0, y0, x1, y1, lw=2.4, ls=ls)
    tx = x0 + (x1 - x0) * 0.45
    ty = y0 + (y1 - y0) * 0.45
    ax.text(tx, ty, rel, fontsize=11.5, color=K1, family="Consolas", weight="bold", ha="center", va="center",
            bbox=dict(fc="white", ec="none", pad=1.5))
arr(ax, TX - 1.9, 2.8, 13.4 + 1.8, 2.8, lw=2.4, ls="--")
ax.text(17.6, 2.8, "has_dosage", fontsize=11.5, color=K1, family="Consolas", weight="bold", ha="center", va="center",
        bbox=dict(fc="white", ec="none", pad=1.5))
txt(ax, 11.8, 0.6, "Nét liền: kế thừa từ i2b2/VA 2010.  Nét đứt: từ n2c2 2018.", 11, K3, ha="left")
txt(ax, 11.8, 0.05, "Nét chấm: đề tài bổ sung.  Mũi tên đi từ thực thể đầu tới thực thể đuôi.", 11, K3, ha="left")
ax.set_ylim(-0.4, 12.7)
save(fig, "h1_4_luoc_do_quan_he.png")

# ======================================================================
# Hình 2.1: từ ba phần chia của VietMed-NER tới các bộ dữ liệu và vai trò của chúng
# ======================================================================
X = J("outputs/bao_cao_khoa_luan_2026-11-05/extra.json")
normMan = J("data/norm_gold_v1/manifest.json")
rsel = J("relation/data/selection.json")
rsyn = J("relation/data/synth/manifest.json")
vman = J("relation/data/synth/validated/manifest.json")  # dữ liệu sinh đã kiểm tra (relation/validate/)
rev = J("relation/outputs/evaluation.json")
rev2 = J("relation/outputs/evaluation_test_v2.json")
sz = X["splits"]["split_sizes"]
forms = lambda sp: normMan["splits"][sp]["CONDITION"]["unique_forms"] + normMan["splits"][sp]["DRUG"]["unique_forms"]  # noqa: E731
STY = {"human": ("-", 2.6), "review": ((0, (6, 2, 1, 2)), 2.2), "llm": ("--", 2.0), "auto": (":", 2.2)}
fig, ax = canvas(12, 8.0, 24, 16.0)
rbox(ax, 6.0, 14.2, 12.0, 1.5, fc=K1)
txt(ax, 12.0, 14.95, f"VietMed-NER  ·  {n(sz['train'] + sz['validation'] + sz['test'])} câu có nhãn thực thể", 16, "white", weight="bold")
cols = [
    (4.0, "Tập train", sz["train"], [
        ("Dữ liệu quan hệ huấn luyện", f"{rsel['seed']['sentences']} câu · {n(rsyn['seed_pairs'])} cặp", "review"),
        ("Tập kiểm định quan hệ", f"{rsel['dev']['sentences']} câu · {rev['dev'][rev['chosen']]['pairs']} cặp", "review"),
        ("Dữ liệu sinh đã kiểm tra", f"{n(vman['pool']['pairs'])} cặp · người duyệt {vman['expert_decisions']['KEEP'] + vman['expert_decisions']['DROP']} câu mẫu", "auto")],
     "Huấn luyện và chọn cấu hình\nmô hình RE"),
    (12.0, "Tập validation", sz["validation"], [
        ("Tập đánh giá gán mã,\nphần dev", f"{forms('dev')} tên bệnh và thuốc", "llm")],
     "Chọn tên gọi khác và ngưỡng\ncho bước gán mã"),
    (20.0, "Tập test", sz["test"], [
        ("Tập test quan hệ", f"{rsel['test']['sentences']} câu · {rev2['pairs']} cặp", "human"),
        ("Tập đánh giá gán mã,\nphần test", f"{forms('test')} tên bệnh và thuốc", "llm")],
     "Đánh giá NER, RE, gán mã\nvà dựng đồ thị tri thức"),
]
cw = 7.4
for x, name, size, ds, use in cols:
    arr(ax, 12.0 + (x - 12.0) * 0.45, 14.2, x, 12.75, lw=2.2, color=K2)
    rbox(ax, x - cw / 2, 11.35, cw, 1.4, fc=F3)
    txt(ax, x, 12.25, name, 16, weight="bold")
    txt(ax, x, 11.7, f"{n(size)} câu", 13, K2)
    for k, (dn, dd, src) in enumerate(ds):
        y = 9.5 - k * 2.25
        ls, lw = STY[src]
        rbox(ax, x - cw / 2 + 0.3, y - 0.95, cw - 0.6, 1.9, fc=F1, ls=ls, lw=lw)
        two = "\n" in dn
        txt(ax, x, y + (0.38 if two else 0.3), dn, 14 if two else 15, weight="bold", linespacing=1.1)
        txt(ax, x, y - (0.62 if two else 0.4), dd, 12.5, K2)
    ax.plot([x, x], [11.35, 10.45], color=K3, lw=1.6)
    txt(ax, x, 2.9, use, 13, K1, style="italic", linespacing=1.2)
# câu của dữ liệu quan hệ huấn luyện và tập kiểm định lấy từ cả train lẫn validation
arr(ax, 12.0 - cw / 2, 11.75, 4.0 + cw / 2 - 0.3, 9.5, color=K3, lw=1.6, ls="--")
arr(ax, 12.0 - cw / 2, 11.55, 4.0 + cw / 2 - 0.3, 7.25, color=K3, lw=1.6, ls="--")
txt(ax, 12.0, 1.75, "Viền liền: người có chuyên môn y khoa gán, có nhãn gợi ý của LLM.   Viền chấm gạch: LLM gán hai lượt, người duyệt.", 11.5, K2)
txt(ax, 12.0, 1.2, "Viền đứt: LLM gán, chưa được bác sĩ duyệt.   Viền chấm: sinh từ câu huấn luyện, kiểm tra tự động, người duyệt một mẫu.", 11.5, K2)
ax.set_ylim(0.8, 15.9)
save(fig, "h2_1_cac_tap_du_lieu.png")

# ======================================================================
# Ví dụ 2.1: hai mẫu của bộ RE-600 đặt cạnh nhau thành hai cột
# ======================================================================
ex = X["examples"][:2]
fig, ax = canvas(12, 6.55, 24, 15.2)


def wrap(s, width):
    out, line = [], ""
    for w in s.split():
        if len(line) + len(w) + 1 > width:
            out.append(line)
            line = w
        else:
            line = (line + " " + w).strip()
    out.append(line)
    return out


for c, e in enumerate(ex):
    x0 = 0.2 + c * 12.1
    W = 11.6
    rbox(ax, x0, 2.2, W, 12.7, fc=F1, lw=2.2)
    txt(ax, x0 + 0.4, 14.25, f"Mẫu {e['id']}", 16, weight="bold", ha="left")
    lines = wrap(f"“{e['text']}”", 50)
    for k, l in enumerate(lines):
        txt(ax, x0 + 0.4, 13.45 - k * 0.55, l, 12.5, K2, ha="left", style="italic")
    y = 13.45 - len(lines) * 0.55 - 0.45
    txt(ax, x0 + 0.4, y, "Thực thể", 13.5, weight="bold", ha="left")
    txt(ax, x0 + 8.4, y, "Vị trí ký tự", 13.5, weight="bold", ha="left")
    ax.plot([x0 + 0.4, x0 + W - 0.4], [y - 0.35, y - 0.35], color=K1, lw=1.2)
    y -= 0.85
    for eid, typ, t, s0, s1 in e["entities"]:
        txt(ax, x0 + 0.4, y, f"{eid}", 12.5, K3, ha="left")
        txt(ax, x0 + 1.3, y, t, 12.5, K1, ha="left", weight="bold")
        txt(ax, x0 + 5.6, y, typ, 11, K2, ha="left", family="Consolas")
        txt(ax, x0 + 8.4, y, f"{s0} đến {s1}", 12.5, K1, ha="left")
        y -= 0.62
    y -= 0.35
    txt(ax, x0 + 0.4, y, "Cặp ứng viên", 13.5, weight="bold", ha="left")
    txt(ax, x0 + 8.4, y, "Nhãn", 13.5, weight="bold", ha="left")
    ax.plot([x0 + 0.4, x0 + W - 0.4], [y - 0.35, y - 0.35], color=K1, lw=1.2)
    y -= 0.85
    for rid, h, t, lab in e["relations"]:
        txt(ax, x0 + 0.4, y, f"{h} → {t}", 12.5, K1, ha="left")
        txt(ax, x0 + 8.4, y, lab, 12, K1, ha="left", family="Consolas", weight="bold" if lab != "NO_RELATION" else "normal")
        y -= 0.62
    for ch in e["changes"]:
        rid = ch["relation"]
        r = next(r for r in e["relations"] if r[0] == rid)
        y -= 0.3
        for k, l in enumerate(wrap(f"Khi duyệt, nhãn của cặp {r[1]} → {r[2]} được sửa từ {ch['before']} thành {ch['after']}.", 58)):
            txt(ax, x0 + 0.4, y - k * 0.55, l, 11.5, K2, ha="left", style="italic")
ax.set_ylim(2.0, 15.1)
save(fig, "vd2_1_mau_re600.png")

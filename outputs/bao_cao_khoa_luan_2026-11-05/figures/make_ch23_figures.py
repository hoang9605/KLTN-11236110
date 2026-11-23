"""Vẽ các sơ đồ của Chương 1, 2 và 3 theo phong cách figures4papers (xem f4p_style.py).

Mọi con số đọc từ tệp kết quả của dự án. Hình 1.1 dùng đúng đầu ra mà hệ thống trả về
cho câu ví dụ (chạy MedicalREPipeline ngày 15/11/2026).

Chạy từ gốc repo:
    .venv/Scripts/python.exe -X utf8 outputs/bao_cao_khoa_luan_2026-11-05/figures/make_ch23_figures.py
"""
import json
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import FancyBboxPatch  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parent))
from f4p_style import PALETTE, FigureStyle, apply_publication_style, finalize_figure  # noqa: E402

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent
BLUE, RED, TEAL, VIOLET = PALETTE["blue_main"], PALETTE["red_strong"], PALETTE["teal"], PALETTE["violet"]
INK, MUTED, LINE = "#1f1f1e", "#5f5e5a", "#9a9999"
# nền nhạt và viền đậm cho từng vai trò màu của figures4papers
# bản in đen trắng: nền xám nhạt khác độ đậm, viền đen; nhãn LLM dùng viền nét đứt
TINT = {
    "blue": ("#ffffff", "#1a1a1a"), "red": ("#e6e6e6", "#1a1a1a"), "green": ("#f2f2f2", "#4d4d4d"),
    "teal": ("#f2f2f2", "#4d4d4d"), "violet": ("#d9d9d9", "#4d4d4d"), "gray": ("#f2f2f2", "#808080"),
}
LS = {"red": "--"}
ENT_TINT = {"CONDITION": "violet", "BODY_PART": "teal", "DRUG": "blue", "DOSAGE": "gray", "TEST": "green", "PROCEDURE": "gray"}
apply_publication_style(FigureStyle(font_size=10, axes_linewidth=1.2))


def J(p):
    return json.loads((ROOT / p).read_text(encoding="utf-8"))


def n(x):
    return f"{x:,}".replace(",", ".")


def save(fig, name):
    finalize_figure(fig, OUT / name, formats=["png", "pdf"], dpi=300, pad=0.05)
    print("wrote", name)


def canvas(w, h):
    fig, ax = plt.subplots(figsize=(w, h))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    return fig, ax


def box(ax, x, y, w, h, title, body="", tint="gray", size=9.5, body_size=8.3, mono=False, lw=1.3, align="center"):
    fill, edge = TINT[tint]
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=0.015", fc=fill, ec=edge, lw=lw, ls=LS.get(tint, "-")))
    tx = x + w / 2 if align == "center" else x + 0.015
    if body:
        ax.text(tx, y + h * 0.68, title, ha=align, va="center", fontsize=size, weight="bold", color=INK)
        ax.text(tx, y + h * 0.30, body, ha=align, va="center", fontsize=body_size, color=MUTED,
                family="Consolas" if mono else None, linespacing=1.3)
    else:
        ax.text(tx, y + h / 2, title, ha=align, va="center", fontsize=size, weight="bold", color=INK, linespacing=1.3)


def arrow(ax, x0, y0, x1, y1, color=LINE, lw=1.2, text=None, tsize=7.8, tcolor=MUTED, toff=(0.008, 0), rad=0.0):
    ax.annotate("", xy=(x1, y1), xytext=(x0, y0),
                arrowprops=dict(arrowstyle="-|>", color=color, lw=lw, shrinkA=0, shrinkB=0, connectionstyle=f"arc3,rad={rad}"))
    if text:
        ax.text((x0 + x1) / 2 + toff[0], (y0 + y1) / 2 + toff[1], text, fontsize=tsize, color=tcolor, va="center", ha="left")


def step_label(ax, y, text):
    ax.text(0.0, y, text, ha="left", va="center", fontsize=9, weight="bold", color=BLUE)


X = J("outputs/bao_cao_khoa_luan_2026-11-05/extra.json")
reGold = J("outputs/re_gold_v1_baseline/compare/report.json")
re2 = J("outputs/re_ai_v2/report.json")
bench = J("outputs/re_benchmark_2026-11-08/benchmark.json")
normMan = J("data/norm_gold_v1/manifest.json")
gold = J("data/re_gold_v1/manifest.json")
rev = J("outputs/vietmed_600_RE_review/review_2026_10_15/stats.json")
sz = X["splits"]["split_sizes"]
forms = lambda sp: normMan["splits"][sp]["CONDITION"]["unique_forms"] + normMan["splits"][sp]["DRUG"]["unique_forms"]  # noqa: E731

# ---------- Hình 1.1: một câu đi qua ba bước ----------
fig, ax = canvas(6.4, 4.5)
xl = 0.17
step_label(ax, 0.93, "Đầu vào")
box(ax, xl, 0.88, 0.83, 0.10, "“Bệnh nhân đau dạ dày, kê Paracetamol 500mg.”", tint="gray", size=10)
step_label(ax, 0.72, "1. NER")
ents = [("đau", "CONDITION"), ("dạ dày", "BODY_PART"), ("Paracetamol", "DRUG"), ("500mg", "DOSAGE")]
ew, eg = 0.195, 0.017
for i, (t, lab) in enumerate(ents):
    box(ax, xl + i * (ew + eg), 0.665, ew, 0.11, t, lab, ENT_TINT[lab], size=9.5, body_size=7.6, mono=True)
step_label(ax, 0.51, "2. Chuẩn hóa")
box(ax, xl, 0.45, 0.40, 0.12, "đau  →  ICD-10 R52.9", "Đau, không đặc hiệu", "violet", size=9.2, body_size=8)
box(ax, xl + 0.43, 0.45, 0.40, 0.12, "Paracetamol  →  RxNorm 161", "acetaminophen", "blue", size=9.2, body_size=8)
step_label(ax, 0.23, "3. RE")
nodes = {"đau": (0.32, 0.30, "CONDITION"), "dạ dày": (0.32, 0.10, "BODY_PART"),
         "Paracetamol": (0.78, 0.30, "DRUG"), "500mg": (0.78, 0.10, "DOSAGE")}
nw, nh = 0.20, 0.075
for t, (cx, cy, lab) in nodes.items():
    box(ax, cx - nw / 2, cy - nh / 2, nw, nh, t, tint=ENT_TINT[lab], size=9)
arrow(ax, 0.32, 0.30 - nh / 2, 0.32, 0.10 + nh / 2, color=INK, text="located_at, điểm 0,997")
arrow(ax, 0.32 + nw / 2, 0.30, 0.78 - nw / 2, 0.30, color=INK)
ax.text(0.55, 0.325, "treated_by, điểm 0,964", ha="center", fontsize=7.8, color=MUTED)
arrow(ax, 0.78, 0.30 - nh / 2, 0.78, 0.10 + nh / 2, color=INK, text="has_dosage,\ntheo quy tắc")
for y0, y1 in [(0.88, 0.775), (0.665, 0.57)]:
    arrow(ax, 0.585, y0, 0.585, y1, color=LINE)
arrow(ax, 0.585, 0.45, 0.585, 0.355, color=LINE)
ax.set_ylim(0.04, 1.0)
save(fig, "h1_1_vi_du_dau_ra.png")

# ---------- Hình 1.2: quan hệ i2b2/VA 2010 đối chiếu với quan hệ của đề tài ----------
# Theo figures4papers: preset font 16, khổ 12 inch, Arial, xám trung tính của repo
# (#272727, #4D4D4D, #767676, #CFCECE), không khung, tight_layout(pad=2), 300 dpi.
from matplotlib.path import Path as MPath  # noqa: E402
from matplotlib.patches import PathPatch  # noqa: E402
apply_publication_style(FigureStyle(font_size=16, axes_linewidth=2.5))
K1, K2, K3, K4 = "#272727", "#4D4D4D", "#767676", "#CFCECE"
groups = [
    ("ĐIỀU TRỊ → VẤN ĐỀ SỨC KHỎE", ["cải thiện", "làm xấu đi", "gây ra", "được dùng cho", "không được dùng cho"]),
    ("XÉT NGHIỆM → VẤN ĐỀ SỨC KHỎE", ["phát hiện", "được làm để khảo sát"]),
    ("VẤN ĐỀ → VẤN ĐỀ SỨC KHỎE", ["chỉ ra"]),
]
links = {"được dùng cho": ["treated_by", "treated_by_procedure"], "phát hiện": ["diagnosed_by"]}
fig, ax = plt.subplots(figsize=(12, 5.6))
ax.set_xlim(0, 12)
ax.set_ylim(0, 11.2)
ax.axis("off")
ax.text(0.0, 10.85, "i2b2/VA 2010", fontsize=17, weight="bold", color=K1, va="center")
ax.text(8.2, 10.85, "Đề tài", fontsize=17, weight="bold", color=K1, va="center")
y, pos = 10.0, {}
for gname, rels in groups:
    ax.text(0.0, y, gname, fontsize=12, color=K3, va="center", weight="bold")
    ax.plot([0.0, 5.0], [y - 0.35, y - 0.35], color=K4, linewidth=1.5)
    y -= 0.95
    for r in rels:
        kept = r in links
        ax.text(0.25, y, r, fontsize=16, va="center", color=K1 if kept else K3, weight="bold" if kept else "normal")
        if kept:
            ax.plot(4.95, y, "o", color=K1, markersize=8)
        pos[r] = y
        y -= 0.72
    y -= 0.25
targets = {"treated_by": pos["được dùng cho"] + 0.55, "treated_by_procedure": pos["được dùng cho"] - 0.55, "diagnosed_by": pos["phát hiện"]}
y_end = y
for t, ty in targets.items():
    ax.add_patch(FancyBboxPatch((8.2, ty - 0.42), 3.75, 0.84, boxstyle="round,pad=0,rounding_size=0.42", fc=K1, ec=K1))
    ax.text(10.075, ty, t, fontsize=15, color="white", ha="center", va="center", family="Consolas", weight="bold")
for r, ts in links.items():
    for t in ts:
        y0, y1 = pos[r], targets[t]
        path = MPath([(4.95, y0), (6.6, y0), (6.6, y1), (8.2, y1)], [MPath.MOVETO, MPath.CURVE4, MPath.CURVE4, MPath.CURVE4])
        ax.add_patch(PathPatch(path, fc="none", ec=K1, linewidth=2.5))
ax.set_ylim(y_end + 0.3, 11.2)
fig.tight_layout(pad=2)
save(fig, "h1_2_i2b2_quan_he.png")
apply_publication_style(FigureStyle(font_size=10, axes_linewidth=1.2))

# ---------- Hình 2.1: ba phần chia của VietMed-NER và các bộ dữ liệu lấy từ mỗi phần ----------
fig, ax = canvas(6.4, 3.9)
lanes = [
    ("Tập train", f"{n(sz['train'])} câu", "Huấn luyện RE", 0.70, [
        ("RE-600", f"600 đoạn, {reGold['pairs']} cặp", "blue"),
        ("RE bổ sung", f"{re2['data']['v2']['samples']} câu, {re2['data']['v2']['included_pairs']} cặp", "red")]),
    ("Tập validation", f"{n(sz['validation'])} câu", "Chọn tham số", 0.40, [
        ("Chuẩn hóa dev", f"{forms('dev')} dạng bệnh và thuốc", "red")]),
    ("Tập test", f"{n(sz['test'])} câu", "Báo cáo kết quả", 0.10, [
        ("Test hạn mức", f"150 đoạn, {bench['data']['golden_test_pairs']} cặp", "red"),
        ("Test RE ngẫu nhiên", f"200 câu, {bench['data']['random_test_pairs']} cặp", "red"),
        ("Chuẩn hóa test", f"{forms('test')} dạng", "red")]),
]
lh = 0.26
for name, cnt, use, y, ds in lanes:
    ax.add_patch(FancyBboxPatch((0, y), 1.0, lh, boxstyle="round,pad=0,rounding_size=0.01", fc="#fafafa", ec="#d9d9d9", lw=0.8))
    ax.text(0.015, y + lh * 0.70, name, fontsize=9.2, weight="bold", color=INK, va="center")
    ax.text(0.015, y + lh * 0.45, cnt, fontsize=8.2, color=MUTED, va="center")
    ax.text(0.015, y + lh * 0.20, use, fontsize=8.2, color=BLUE, weight="bold", va="center")
    w = 0.25
    for i, (t, b, tint) in enumerate(ds):
        box(ax, 0.215 + i * (w + 0.012), y + 0.035, w, lh - 0.07, t, b, tint, size=8.6, body_size=7.6)
hs = [plt.Rectangle((0, 0), 1, 1, fc=TINT[k][0], ec=TINT[k][1], ls=LS.get(k, "-")) for k in ("blue", "red")]
ax.legend(hs, ["Nhãn do người duyệt chốt", "Nhãn LLM chưa được bác sĩ duyệt"], loc="upper center",
          bbox_to_anchor=(0.5, 0.06), ncol=2, fontsize=8.5, handlelength=1.6)
ax.set_ylim(-0.02, 0.99)
save(fig, "h2_1_nguon_du_lieu.png")

# ---------- Hình 2.2: bốn vòng gán nhãn, xen kẽ LLM và người duyệt ----------
fig, ax = canvas(6.4, 2.3)
ax.text(0.0, 0.78, "LLM", fontsize=9.5, weight="bold", color=RED, va="center")
ax.text(0.0, 0.25, "Người duyệt", fontsize=9.5, weight="bold", color=BLUE, va="center")
ax.plot([0.12, 1.0], [0.515, 0.515], color="#d9d9d9", lw=0.8, ls="--")
steps = [(0.15, 0.60, "1. Đề xuất nhãn", "kèm bằng chứng", "red"),
         (0.365, 0.09, "2. Sửa nhãn", "trên 600 mẫu", "blue"),
         (0.58, 0.60, "3. Rà soát lại", f"thực thể\n{n(rev['entities_before'])} → {n(rev['entities_after'])}", "red"),
         (0.795, 0.09, "4. Chốt RE-600", f"{reGold['pairs']} cặp\ndùng được", "blue")]
bw, bh = 0.205, 0.32
for x, y, t, b, tint in steps:
    box(ax, x, y, bw, bh, t, b, tint, size=9, body_size=8)
for (x0, y0, *_), (x1, y1, *_) in zip(steps, steps[1:]):
    if y0 > y1:
        arrow(ax, x0 + bw, y0 + 0.04, x1 + 0.03, y1 + bh, color=INK)
    else:
        arrow(ax, x0 + bw, y0 + bh - 0.04, x1 + 0.03, y1, color=INK)
ax.set_ylim(0.03, 0.97)
save(fig, "h2_2_quy_trinh_gan_nhan.png")

# ---------- Hình 3.1: luồng xử lý và dữ liệu truyền giữa các bước ----------
fig, ax = canvas(6.4, 6.0)
cx, W, H = 0.30, 0.42, 0.075


def stage(y, title, cls, tint):
    box(ax, cx, y, W, H, title, cls, tint, size=9.2, body_size=7.8)


ax.add_patch(FancyBboxPatch((cx - 0.03, 0.535), 0.98 - cx + 0.03, 0.375, boxstyle="round,pad=0,rounding_size=0.01", fc="none", ec=BLUE, lw=1, ls="--"))
ax.text(cx - 0.035, 0.89, "Phần NER", fontsize=8.5, color=BLUE, ha="right")
box(ax, cx, 0.94, W, 0.05, "Văn bản tiếng Việt", tint="gray", size=9)
ys = [0.82, 0.71, 0.60]
stage(0.835, "1. Tiền xử lý", "tách từ và chia đoạn", "blue")
stage(0.725, "2. Suy luận NER", "ViHealthBERT gán nhãn BIO", "blue")
stage(0.615, "3. Quy tắc liều và hậu xử lý", "sửa lỗi đã biết, giải mã thực thể", "blue")
arrow(ax, cx + W / 2, 0.94, cx + W / 2, 0.835 + H)
arrow(ax, cx + W / 2, 0.835, cx + W / 2, 0.725 + H, text="đoạn từ kèm vị trí ký tự")
arrow(ax, cx + W / 2, 0.725, cx + W / 2, 0.615 + H, text="thực thể thô, độ tin cậy")
yb = 0.385
box(ax, 0.0, yb, 0.40, 0.085, "4. Chuẩn hóa mã", "tra danh mục theo loại thực thể", "green", size=9.2, body_size=7.8)
box(ax, 0.58, yb, 0.42, 0.085, "5. Sinh cặp và phân loại RE", "lọc thực thể, ghép cặp đúng kiểu", "red", size=9.2, body_size=7.8)
arrow(ax, cx + 0.06, 0.615, 0.20, yb + 0.085)
arrow(ax, cx + W - 0.06, 0.615, 0.79, yb + 0.085)
ax.text(0.50, 0.565, "6 loại thực thể kèm span", fontsize=7.8, color=MUTED, ha="center")
ax.text(0.20, yb - 0.035, "CONDITION sang ICD-10, DRUG sang RxNorm", fontsize=7.6, color=MUTED, ha="center")
ax.text(0.79, yb - 0.035, "5 quan hệ, mô hình ViHealthBERT", fontsize=7.6, color=MUTED, ha="center")
box(ax, cx, 0.17, W, 0.085, "Bản ghi có cấu trúc", "thực thể, mã chuẩn, quan hệ", "gray", size=9.2, body_size=7.8)
arrow(ax, 0.20, yb - 0.06, cx + 0.08, 0.255)
arrow(ax, 0.79, yb - 0.06, cx + W - 0.08, 0.255)
box(ax, cx, 0.02, W, 0.085, "6. Đồ thị tri thức", "gộp khái niệm trùng mã thành một nút", "violet", size=9.2, body_size=7.8)
arrow(ax, cx + W / 2, 0.17, cx + W / 2, 0.105, text="gộp bộ ba của nhiều văn bản")
ax.set_ylim(0.0, 1.0)
save(fig, "h3_1_luong_xu_ly.png")

# ---------- Hình 3.2: cấu trúc thư mục lõi và mẫu thiết kế ----------
fig, ax = canvas(6.4, 3.9)
pk = [
    ("ner/", "Mẫu Pipeline", "blue", ["pipeline.py  MedicalNERPipeline", "preprocessor.py  TextPreprocessor", "predictor.py  ModelNERPredictor",
                                      "dosage_extractor.py  DosageExtractor", "postprocessor.py  PostProcessor", "config.py"]),
    ("normalization/", "Mẫu Strategy", "green", ["base.py  BaseNormalizer", "icd10.py  ICD10Normalizer", "rxnorm.py  RxNormNormalizer",
                                                 "stubs.py  FMA, LOINC, MeSH", "dispatcher.py  chọn theo loại", "data/  danh mục, alias"]),
    ("relation_extraction/", "Facade và Strategy", "red", ["pipeline.py  MedicalREPipeline", "data.py  sinh cặp ứng viên", "rules.py  RuleRelationExtractor",
                                                         "bert_model.py  BertRelationExtractor", "model.py  TF-IDF và LogReg"]),
    ("knowledge_graph/", "Gộp kết quả", "violet", ["extract.py  HybridRelationExtractor", "graph.py  KnowledgeGraph", "visualize.py"]),
]
cw, gx, top = 0.235, 0.02, 0.80
for i, (name, pat, tint, files) in enumerate(pk):
    x = i * (cw + gx)
    fill, edge = TINT[tint]
    ax.add_patch(FancyBboxPatch((x, 0.03), cw, top - 0.03, boxstyle="round,pad=0,rounding_size=0.012", fc=fill, ec=edge, lw=1.3))
    ax.text(x + 0.012, top - 0.04, name, fontsize=8.6 if len(name) < 16 else 7.0, weight="bold", family="Consolas", va="center")
    ax.text(x + 0.012, top - 0.095, pat, fontsize=8.4, color=edge, weight="bold", va="center")
    for j, fl in enumerate(files):
        fn, _, cl = fl.partition("  ")
        yy = top - 0.165 - j * 0.098
        ax.text(x + 0.012, yy, fn, fontsize=6.9, family="Consolas", va="center", color=INK)
        if cl:
            ax.text(x + 0.012, yy - 0.04, cl, fontsize=6.9, va="center", color=MUTED)
ax.set_ylim(0.01, 0.82)
save(fig, "h3_2_to_chuc_ma_nguon.png")

# ---------- Hình 3.3: các ngưỡng chia chunk ----------
ratio_mean, ratio_max = 1.013, 1.417   # đo trên 3.497 câu của tập test bằng tokenizer của mô hình NER
fig, ax = plt.subplots(figsize=(6.4, 2.6))
words = [0, 160]
ax.plot(words, [w * ratio_max for w in words], color=INK, lw=1.8, ls="--", label="Trường hợp nặng nhất, 1,42 subword mỗi từ")
ax.plot(words, [w * ratio_mean for w in words], color=BLUE, lw=1.8, label="Trung bình, 1,01 subword mỗi từ")
ax.axhline(256, color=INK, lw=1.2)
ax.text(2, 262, "Giới hạn của mô hình, 256 subword", fontsize=8.2, color=INK)
ax.axhline(200, color=MUTED, lw=1.0, ls="--")
ax.text(2, 206, "Mức an toàn trong cấu hình, 200 subword", fontsize=8.2, color=MUTED)
for x, lab, c in [(15, "15", PALETTE["neutral"]), (35, "35", TEAL), (120, "120", VIOLET), (140, "140", RED)]:
    ax.axvline(x, color=c if x != 15 else "#8f8e8e", lw=1.2, ls=":")
    ax.text(x + 1, 285, lab, fontsize=8.5, color=INK, weight="bold")
ax.annotate("140 từ ≈ 198 subword", xy=(140, 140 * ratio_max), xytext=(92, 228), fontsize=8, color=RED,
            arrowprops=dict(arrowstyle="-|>", color=RED, lw=1))
ax.set_xlim(0, 160)
ax.set_ylim(0, 300)
ax.set_xlabel("Số từ trong một đoạn con")
ax.set_ylabel("Số subword")
ax.legend(loc="lower right", fontsize=8)
save(fig, "h3_3_chia_chunk.png")

# ---------- Hình 0.1: sáu loại thực thể mục tiêu ----------
types6 = [
    ("Bệnh, triệu chứng", "CONDITION", "đau đầu, viêm phổi", "Gán mã ICD-10"),
    ("Thuốc", "DRUG", "Paracetamol, metformin", "Gán mã RxNorm"),
    ("Bộ phận cơ thể", "BODY_PART", "dạ dày, gan", "Không chuẩn hóa mã"),
    ("Xét nghiệm", "TEST", "chụp X-quang, men gan", "Không chuẩn hóa mã"),
    ("Thủ thuật", "PROCEDURE", "đặt stent, phẫu thuật", "Không chuẩn hóa mã"),
    ("Liều dùng", "DOSAGE", "500 mg, 2 viên/ngày", "Tách giá trị, đơn vị và tần suất"),
]
fig, ax = canvas(6.4, 3.2)
cw, ch, gx, gy = 0.32, 0.43, 0.02, 0.06
for i, (vi, lab, ex, norm) in enumerate(types6):
    r, c = divmod(i, 3)
    x, y = c * (cw + gx), 0.53 - r * (ch + gy)
    fill, edge = TINT[ENT_TINT[lab]]
    ax.add_patch(FancyBboxPatch((x, y), cw, ch, boxstyle="round,pad=0,rounding_size=0.015", fc=fill, ec=edge, lw=1.3))
    ax.text(x + 0.02, y + ch - 0.075, vi, fontsize=9.2, weight="bold", color=INK, va="center")
    ax.text(x + 0.02, y + ch - 0.165, lab, fontsize=8.6, family="Consolas", color=edge, weight="bold", va="center")
    ax.text(x + 0.02, y + ch - 0.255, ", ".join(f"“{w}”" for w in ex.split(", ")), fontsize=8, color=MUTED, va="center")
    ax.text(x + 0.02, y + 0.06, norm, fontsize=7.6, color=INK, va="center", style="italic")
ax.set_ylim(0.01, 0.98)
save(fig, "h0_1_sau_loai_thuc_the.png")

# ---------- Hình: loại dự đoán tại hai token đặc biệt trước khi giải mã BIO ----------
toks = ["<s>", "Bệnh", "nhân", "đau", "dạ", "dày", "</s>"]
labs = ["?", "O", "O", "B-CONDITION", "B-BODY_PART", "I-BODY_PART", "?"]
fig, ax = canvas(6.4, 2.5)
n_t = len(toks)
tw, gap, x0 = 0.103, 0.010, 0.215
rows = {"tok": 0.74, "lab": 0.44, "ent": 0.10}
ax.text(0.0, 0.815, "Chuỗi đưa\nvào mô hình", fontsize=8.6, color=MUTED, va="center", linespacing=1.3)
ax.text(0.0, 0.505, "Nhãn dự đoán\ntại mỗi vị trí", fontsize=8.6, color=MUTED, va="center", linespacing=1.3)
for i, (t, l) in enumerate(zip(toks, labs)):
    x = x0 + i * (tw + gap)
    special = t.startswith("<")
    tint = "gray" if special else "blue"
    box(ax, x, rows["tok"], tw, 0.15, t, tint=tint, size=9.5 if not special else 9, mono=special)
    ltint = "gray" if special else ENT_TINT.get(l.split("-", 1)[-1], "gray") if l != "O" else "gray"
    fill, edge = TINT[ltint]
    ax.add_patch(FancyBboxPatch((x, rows["lab"]), tw, 0.13, boxstyle="round,pad=0,rounding_size=0.012",
                                fc="white" if special or l == "O" else fill, ec=edge, lw=1.0, ls="--" if special else "-"))
    ax.text(x + tw / 2, rows["lab"] + 0.065, l, ha="center", va="center", fontsize=5.2 if len(l) > 9 else 8.5,
            family="Consolas", color=MUTED if special else INK)
    arrow(ax, x + tw / 2, rows["tok"], x + tw / 2, rows["lab"] + 0.13, color=LINE, lw=0.9)
    if special:
        ax.plot([x + 0.01, x + tw - 0.01], [rows["lab"] + 0.01, rows["lab"] + 0.12], color=RED, lw=1.6)
        ax.plot([x + 0.01, x + tw - 0.01], [rows["lab"] + 0.12, rows["lab"] + 0.01], color=RED, lw=1.6)
ax.text(x0 + tw / 2, rows["lab"] - 0.06, "loại bỏ", ha="center", fontsize=8, color=RED)
ax.text(x0 + 6 * (tw + gap) + tw / 2, rows["lab"] - 0.06, "loại bỏ", ha="center", fontsize=8, color=RED)
# kết quả giải mã BIO
xs = lambda i: x0 + i * (tw + gap)  # noqa: E731
box(ax, xs(3), rows["ent"], tw, 0.14, "đau", "CONDITION", "red", size=9, body_size=5.8, mono=True)
box(ax, xs(4), rows["ent"], 2 * tw + gap, 0.14, "dạ dày", "BODY_PART", "teal", size=9, body_size=7, mono=True)
ax.text(0.0, 0.17, "Thực thể sau\ngiải mã BIO", fontsize=8.6, color=MUTED, va="center", linespacing=1.3)
for i in (3, 4, 5):
    arrow(ax, xs(i) + tw / 2, rows["lab"], xs(i) + tw / 2, rows["ent"] + 0.14, color=LINE, lw=0.9)
ax.set_ylim(0.05, 1.0)
save(fig, "h_token_dac_biet.png")

# ---------- Hình: mô hình RE đang dùng, ViHealthBERT nhiều seed hợp với rule-based ----------
meta = J("outputs/re_benchmark_2026-11-08/benchmark.json")["bert_meta"]
seeds = meta["seeds"]
fig, ax = canvas(6.4, 3.3)
# cột 1: câu đã chèn marker
box(ax, 0.0, 0.50, 0.20, 0.36, "Cặp ứng viên\nđã chèn marker",
    "[HEAD_CONDITION]\nđau [/HEAD] ở\n[TAIL_BODY_PART]\nvùng bụng [/TAIL]", "blue", size=8.4, body_size=6.6, mono=True)
# cột 2: các encoder theo seed
ys = [0.74, 0.58, 0.42][: len(seeds)]
for i, (s, y) in enumerate(zip(seeds, ys)):
    box(ax, 0.25, y, 0.30, 0.13, f"ViHealthBERT, seed {s}", "[h_head ; h_tail] → lớp tuyến tính", "violet", size=8, body_size=6.6)
    arrow(ax, 0.20, 0.68, 0.25, y + 0.065, lw=0.9)
    arrow(ax, 0.55, y + 0.065, 0.60, 0.62, lw=0.9)
ax.text(0.40, 0.375, f"lấy trung bình xác suất của {len(seeds)} seed", ha="center", fontsize=7.4, color=MUTED, style="italic")
# cột 3: trung bình và ngưỡng
box(ax, 0.60, 0.54, 0.16, 0.16, "Xác suất\ntrung bình", "dương khi ≥ 0,5", "teal", size=8.4, body_size=7)
# hàng dưới: rule-based
box(ax, 0.25, 0.07, 0.51, 0.15, "Rule-based", "từ gợi ý, khoảng cách và thực thể chen giữa", "gray", size=8.6, body_size=7)
ax.plot([0.10, 0.10], [0.50, 0.145], color=LINE, lw=0.9)
arrow(ax, 0.10, 0.145, 0.25, 0.145, lw=0.9)
# cột 4: hợp hai nguồn
box(ax, 0.81, 0.36, 0.19, 0.18, "Hợp (union)", "dương khi một trong\nhai nguồn dương", "red", size=8.6, body_size=6.8)
arrow(ax, 0.76, 0.62, 0.86, 0.54, lw=0.9)
arrow(ax, 0.76, 0.145, 0.86, 0.36, lw=0.9)
box(ax, 0.81, 0.07, 0.19, 0.15, "Quan hệ", "kèm nguồn mô hình\nhoặc rule-based", "blue", size=8.6, body_size=6.6)
arrow(ax, 0.905, 0.36, 0.905, 0.22, lw=0.9)
ax.set_ylim(0.03, 0.92)
save(fig, "h3_5_mo_hinh_re.png")

# ---------- Hình: câu ví dụ thành bản ghi có cấu trúc (đầu ra thật của hệ thống) ----------
apply_publication_style(FigureStyle(font_size=16, axes_linewidth=2.5))
K1, K2, K3, K4 = "#272727", "#4D4D4D", "#767676", "#CFCECE"
fig, ax = plt.subplots(figsize=(12, 6.4))
ax.set_xlim(0, 12)
ax.set_ylim(1.2, 10)
ax.axis("off")
fig.subplots_adjust(left=0.02, right=0.99, top=0.98, bottom=0.02)
rend = fig.canvas.get_renderer()
ax.text(0, 9.55, "VĂN BẢN ĐẦU VÀO", fontsize=12, color=K3, weight="bold", va="center")
pieces = [("Bệnh nhân", None), ("đau", "CONDITION"), ("dạ dày", "BODY_PART"), (",", None), ("kê", None),
          ("Paracetamol", "DRUG"), ("500mg", "DOSAGE"), (".", None)]
x, ys = 0.0, 8.7
inv = ax.transData.inverted()
for t, lab in pieces:
    if t not in (",", ".") and x > 0:
        x += 0.22
    txt = ax.text(x, ys, t, fontsize=20, va="center", color=K1, weight="bold" if lab else "normal")
    bb = txt.get_window_extent(renderer=rend)
    x0, _ = inv.transform((bb.x0, bb.y0))
    x1, _ = inv.transform((bb.x1, bb.y1))
    if lab:
        ax.plot([x0, x1], [ys - 0.42, ys - 0.42], color=K1, linewidth=3)
        ax.text((x0 + x1) / 2, ys - 0.8, lab, fontsize=11, color=K2, ha="center", va="center", family="Consolas")
    x = x1
ax.annotate("", xy=(0.5, 6.55), xytext=(0.5, 7.55), arrowprops=dict(arrowstyle="-|>", color=K1, lw=2.5))
ax.text(0.75, 7.05, "hệ thống trích xuất", fontsize=13, color=K3, va="center", style="italic")
ax.text(0, 6.15, "BẢN GHI CÓ CẤU TRÚC", fontsize=12, color=K3, weight="bold", va="center")
# bảng thực thể
cols = [0.0, 1.9, 3.95]
rows = [("Thực thể", "Loại", "Mã chuẩn"),
        ("đau", "Tình trạng bệnh", "ICD-10 R52.9, Đau không đặc hiệu"),
        ("dạ dày", "Bộ phận cơ thể", "Không chuẩn hóa mã"),
        ("Paracetamol", "Thuốc", "RxNorm 161, acetaminophen"),
        ("500mg", "Liều dùng", "Không chuẩn hóa mã")]
y = 5.45
for i, r in enumerate(rows):
    head = i == 0
    for cx, val in zip(cols, r):
        ax.text(cx, y, val, fontsize=14 if head else 15, va="center", weight="bold" if head or cx == 0 else "normal",
                color=K1 if (head or cx == 0 or "ICD" in val or "RxNorm" in val) else K2)
    ax.plot([0, 8.0], [y - 0.42, y - 0.42], color=K1 if head else K4, linewidth=2 if head else 1.2)
    y -= 0.95
# bảng quan hệ
rx = 8.45
ax.text(rx, 5.45, "Quan hệ", fontsize=14, weight="bold", va="center", color=K1)
ax.plot([rx, 12], [5.03, 5.03], color=K1, linewidth=2)
rels = [("đau", "dạ dày", "located_at"), ("đau", "Paracetamol", "treated_by"), ("Paracetamol", "500mg", "has_dosage")]
y = 4.4
for h, t, r in rels:
    ax.text(rx, y + 0.18, f"{h}  →  {t}", fontsize=15, va="center", color=K1, weight="bold")
    ax.text(rx, y - 0.32, r, fontsize=13, va="center", color=K2, family="Consolas")
    ax.plot([rx, 12], [y - 0.72, y - 0.72], color=K4, linewidth=1.2)
    y -= 1.27
save(fig, "h_ban_ghi_cau_truc.png")
apply_publication_style(FigureStyle(font_size=10, axes_linewidth=1.2))

# ---------- Hình: lớp phân loại 768 x 37 trên một subword (xác suất thật của mô hình cho "đau") ----------
apply_publication_style(FigureStyle(font_size=16, axes_linewidth=2.5))
K1, K2, K3, K4 = "#272727", "#4D4D4D", "#767676", "#CFCECE"
top5 = [("B-DISEASESYMTOM", 0.9972), ("I-DISEASESYMTOM", 0.0004), ("B-ORGAN", 0.0002), ("I-ORGAN", 0.0001), ("O", 0.0001)]
fig = plt.figure(figsize=(12, 5.4))
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, 12)
ax.set_ylim(0, 5.4)
ax.axis("off")


def strip(x, y, n, w, h, label, sub):
    """vector vẽ thành dải ô dọc, chỉ vẽ vài ô và dấu ba chấm"""
    cells = [0, 1, 2, None, n - 1]
    ch = h / len(cells)
    for i, c in enumerate(cells):
        yy = y + h - (i + 1) * ch
        if c is None:
            for k in (-1, 0, 1):
                ax.plot(x + w / 2, yy + ch / 2 + k * ch * 0.25, "o", color=K2, markersize=3)
        else:
            ax.add_patch(plt.Rectangle((x, yy), w, ch, fc="#F2F2F2", ec=K1, lw=1.5))
    ax.text(x + w / 2, y + h + 0.3, label, ha="center", va="center", fontsize=14, weight="bold", color=K1)
    ax.text(x + w / 2, y - 0.3, sub, ha="center", va="center", fontsize=12, color=K3)


ym, hm = 1.75, 2.6
ax.add_patch(FancyBboxPatch((0.0, ym + 0.95), 1.15, 0.7, boxstyle="round,pad=0,rounding_size=0.12", fc=K1, ec=K1))
ax.text(0.575, ym + 1.3, "đau", ha="center", va="center", fontsize=16, color="white", weight="bold")
ax.text(0.575, ym + 0.6, "subword", ha="center", fontsize=12, color=K3)
ax.add_patch(FancyBboxPatch((1.55, ym + 0.35), 1.6, 1.9, boxstyle="round,pad=0,rounding_size=0.12", fc="#F2F2F2", ec=K1, lw=2))
ax.text(2.35, ym + 1.55, "ViHealthBERT", ha="center", va="center", fontsize=13, weight="bold", color=K1)
ax.text(2.35, ym + 1.0, "12 lớp\nbộ mã hóa", ha="center", va="center", fontsize=12, color=K2, linespacing=1.3)
strip(3.6, ym, 768, 0.45, hm, "h", "768 chiều")
ax.add_patch(plt.Rectangle((4.55, ym + 0.2), 1.45, hm - 0.4, fc="#CFCECE", ec=K1, lw=2))
ax.text(5.275, ym + hm / 2 + 0.2, "W", ha="center", va="center", fontsize=20, weight="bold", color=K1)
ax.text(5.275, ym + hm / 2 - 0.35, "768 × 37", ha="center", va="center", fontsize=13, color=K1)
strip(6.45, ym, 37, 0.45, hm, "z", "37 điểm số")
for x0, x1 in [(1.15, 1.55), (3.15, 3.6), (4.05, 4.55), (6.0, 6.45)]:
    ax.annotate("", xy=(x1, ym + 1.3), xytext=(x0, ym + 1.3), arrowprops=dict(arrowstyle="-|>", color=K1, lw=2))
ax.annotate("", xy=(7.75, ym + 1.3), xytext=(6.95, ym + 1.3), arrowprops=dict(arrowstyle="-|>", color=K1, lw=2))
ax.text(7.35, ym + 0.95, "softmax", ha="center", fontsize=12, color=K2, style="italic")
# xác suất thật của 5 nhãn cao nhất
bx = fig.add_axes([0.80, 0.33, 0.185, 0.5])
names = [n for n, _ in top5][::-1]
vals = [v for _, v in top5][::-1]
bars = bx.barh(range(5), vals, color=["#FFFFFF"] * 4 + [K1], edgecolor=K1, linewidth=1.5, height=0.62)
bx.set_yticks(range(5), names, fontsize=11, family="Consolas")
bx.set_xlim(0, 1.25)
bx.set_xticks([0, 0.5, 1], ["0", "0,5", "1"], fontsize=11)
bx.tick_params(length=0)
bx.spines["left"].set_visible(False)
for i, v in enumerate(vals):
    bx.text(v + 0.03, i, f"{v:.4f}".replace(".", ","), va="center", fontsize=11, color=K1)
bx.set_title("Xác suất, 5 trên 37 nhãn", fontsize=12, color=K1, pad=8)
# vòng huấn luyện
ax.text(9.1, 0.95, "so với nhãn chuẩn → hàm mất mát cross-entropy", ha="center", fontsize=12, color=K2)
ax.annotate("", xy=(2.35, ym + 0.35), xytext=(9.1, 0.75),
            arrowprops=dict(arrowstyle="-|>", color=K3, lw=1.8, ls="--", connectionstyle="angle,angleA=180,angleB=90,rad=0"))
ax.text(4.6, 0.45, "AdamW cập nhật W và toàn bộ bộ mã hóa", ha="center", fontsize=12, color=K2, style="italic")
save(fig, "h_lop_phan_loai_768x37.png")
apply_publication_style(FigureStyle(font_size=10, axes_linewidth=1.2))

# ---------- Hình 3.3: các vùng quy tắc chia đoạn con theo số từ (ner/preprocessor.py) ----------
apply_publication_style(FigureStyle(font_size=16, axes_linewidth=2.5))
K1, K2, K3, K4 = "#272727", "#4D4D4D", "#767676", "#CFCECE"
fig, ax = plt.subplots(figsize=(12, 4.6))
zones = [(0, 15, "#FFFFFF", "Chưa tách"),
         (15, 35, "#E6E6E6", "Tách ở dấu kết thúc câu\nnếu phần còn lại\ncó từ 15 từ trở lên"),
         (35, 120, "#CFCECE", "Tách ở dấu kết thúc câu"),
         (120, 140, "#767676", "Tách thêm ở\ndấu phẩy, chấm phẩy")]
for a, b, c, lab in zones:
    ax.add_patch(plt.Rectangle((a, 0), b - a, 1, fc=c, ec=K1, lw=2))
    ax.text((a + b) / 2, 1.18, lab, ha="center", va="bottom", fontsize=12.5, color=K1, linespacing=1.25)
ax.plot([140, 140], [-0.15, 1.15], color=K1, lw=5)
ax.text(141.5, 0.5, "Cắt cứng", va="center", fontsize=13, weight="bold", color=K1)
# căn cứ từ dữ liệu: độ dài câu và số subword ở trường hợp nặng nhất (1,417 subword mỗi từ)
ax.annotate("", xy=(0, -0.35), xytext=(34, -0.35), arrowprops=dict(arrowstyle="<->", color=K2, lw=1.8))
ax.text(17, -0.55, "99% câu của tập test\ncó tối đa 34 từ", ha="center", va="top", fontsize=12, color=K2, linespacing=1.25)
ax.text(140, -0.35, "140 từ × 1,42 ≈ 198 subword,\ndưới mức an toàn 200\nvà giới hạn 256 của mô hình", ha="center", va="top",
        fontsize=12, color=K2, linespacing=1.25)
ax.set_xlim(-2, 162)
ax.set_ylim(-1.75, 2.05)
ax.set_yticks([])
ax.spines["left"].set_visible(False)
ax.spines["bottom"].set_position(("data", -1.75))
ax.set_xticks([0, 15, 35, 120, 140])
ax.set_xlabel("Số từ đã gom vào đoạn con hiện tại")
fig.tight_layout(pad=2)
save(fig, "h3_3_chia_chunk.png")
apply_publication_style(FigureStyle(font_size=10, axes_linewidth=1.2))

"""Vẽ các hình của Chương 4 từ đúng các tệp kết quả mà build_report.js đọc.

Chạy từ gốc repo:
    .venv/Scripts/python.exe -X utf8 outputs/bao_cao_khoa_luan_2026-11-05/figures/make_ch4_figures.py

Phong cách: figures4papers (ChenLiu-1996/figures4papers), cài trong f4p_style.py,
xuất PNG và PDF 300 dpi theo finalize_figure, bảng màu theo vai trò của repo
(xanh đậm cho phương pháp đề xuất, đỏ cho baseline, xanh ngọc và tím cho nhóm phụ);
mọi cột đều có nhãn giá trị trực tiếp.
"""
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import sys  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parent))
from f4p_style import PALETTE, FigureStyle, apply_publication_style, finalize_figure  # noqa: E402
from matplotlib.ticker import FuncFormatter  # noqa: E402

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent

C1, C2, C3, C4 = PALETTE["blue_main"], PALETTE["red_strong"], PALETTE["teal"], PALETTE["violet"]
GRAY, INK, MUTED = PALETTE["neutral"], "#1f1f1e", "#5f5e5a"
SEQ = ["#ececec", "#d4d4d4", "#b8b8b8", "#999999", "#777777", "#4d4d4d", "#262626"]

apply_publication_style(FigureStyle(font_size=10, axes_linewidth=1.2))


def J(p):
    return json.loads((ROOT / p).read_text(encoding="utf-8"))


def vn(x, d=2):
    return f"{x:.{d}f}".replace(".", ",")


def save(fig, name):
    finalize_figure(fig, OUT / name, formats=["png", "pdf"], dpi=300, pad=0.05)
    print("wrote", name)


def clean(ax, grid_axis="x"):
    fmt = FuncFormatter(lambda v, _: f"{v:g}".replace(".", ",").replace("-", "−"))
    (ax.xaxis if grid_axis == "x" else ax.yaxis).set_major_formatter(fmt)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.grid(axis="y" if grid_axis == "x" else "x", visible=False)
    ax.tick_params(length=0)


def hbar_labels(ax, bars, vals, d=2, pad=0.008):
    for b, v in zip(bars, vals):
        ax.text(b.get_width() + pad, b.get_y() + b.get_height() / 2, vn(v, d), va="center", fontsize=8, color=INK)


LABELS6 = ["CONDITION", "DRUG", "BODY_PART", "TEST", "PROCEDURE", "DOSAGE"]
RELS = ["located_at", "treated_by", "treated_by_procedure", "diagnosed_by", "has_dosage"]
MAP = {"DISEASESYMTOM": "CONDITION", "DRUGCHEMICAL": "DRUG", "PREVENTIVEMED": "DRUG", "ORGAN": "BODY_PART",
       "DIAGNOSTICS": "TEST", "SURGERY": "PROCEDURE", "MEDDEVICETECHNIQUE": "PROCEDURE", "TREATMENT": "PROCEDURE",
       "UNITCALIBRATOR": "DOSAGE"}
NER_DIR = "eval/results_2026-11-05"

# ---------- Hình 4.1: F1 của mô hình gốc trên 18 loại ----------
t1 = J(f"{NER_DIR}/raw_37label_report.json")
rows = sorted([(k, v) for k, v in t1.items() if not k.endswith("avg")], key=lambda kv: kv[1]["f1-score"])
fig, ax = plt.subplots(figsize=(6.3, 4.6))
vals = [v["f1-score"] for _, v in rows]
cols = [C1 if k in MAP else GRAY for k, _ in rows]
bars = ax.barh(range(len(rows)), vals, color=cols, height=0.68)
ax.set_yticks(range(len(rows)), [f"{k}  (n={v['support']})" for k, v in rows])
hbar_labels(ax, bars, vals)
ax.set_xlim(0, 1.05)
ax.set_xlabel("F1 theo thực thể (seqeval)")
clean(ax)
ax.legend(handles=[plt.Rectangle((0, 0), 1, 1, color=C1), plt.Rectangle((0, 0), 1, 1, color=GRAY)],
          labels=["Được ánh xạ sang sáu loại mục tiêu", "Bị loại khỏi lược đồ"], loc="lower right")
save(fig, "h4_1_ner_18_loai.png")

# ---------- Hình 4.2: strict và relaxed theo sáu loại ----------
s6 = J(f"{NER_DIR}/schema_6label_report.json")
st, rl = s6["strict_exact_match"], s6["relaxed_overlap_match"]
order = sorted(LABELS6, key=lambda k: st[k]["f1-score"])
fig, ax = plt.subplots(figsize=(6.3, 3.2))
y = range(len(order))
h = 0.38
b1 = ax.barh([i + h / 2 for i in y], [rl[k]["f1-score"] for k in order], height=h, color=C2, label="Khớp nới lỏng: chấp nhận span giao nhau")
b2 = ax.barh([i - h / 2 for i in y], [st[k]["f1-score"] for k in order], height=h, color=C1, label="Khớp chặt: khớp đúng span và loại")
hbar_labels(ax, b1, [rl[k]["f1-score"] for k in order])
hbar_labels(ax, b2, [st[k]["f1-score"] for k in order])
ax.set_yticks(list(y), [f"{k}  (n={st[k]['support']})" for k in order])
ax.set_xlim(0, 1.0)
ax.set_xlabel("F1 của toàn luồng xử lý trên tập test")
clean(ax)
h_, l_ = ax.get_legend_handles_labels()
ax.legend(h_[::-1], l_[::-1], loc="upper center", ncol=2, bbox_to_anchor=(0.45, -0.2))
save(fig, "h4_2_ner_strict_relaxed.png")

# ---------- Hình 4.3: so với baseline NER theo loại ----------
nb = J("eval/ner_baselines_2026-11-08/baselines.json")
ni = J("eval/ner_baselines_2026-11-08/inherited_checkpoint.json")
series = [("Từ điển", nb["dictionary"]["test"]["target"], C2), ("CRF", nb["crf"]["test"]["target"], C3),
          ("ViHealthBERT", ni["scores"]["test"]["target"], C1)]
cats = LABELS6 + ["Micro"]
fig, ax = plt.subplots(figsize=(6.3, 4.2))
h = 0.26
for j, (name, tg, c) in enumerate(series):
    v = [tg["report"][k]["f1-score"] for k in LABELS6] + [tg["micro"]["f1"]]
    pos = [i + (1 - j) * h for i in range(len(cats))]
    bars = ax.barh(pos, v, height=h, color=c, label=name)
    lo, hi = tg["micro_f1_ci95"]
    hbar_labels(ax, bars[:-1], v[:-1])
    ax.text(hi + 0.008, pos[-1], vn(v[-1]), va="center", fontsize=8, color=INK)
    ax.errorbar([tg["micro"]["f1"]], [pos[-1]], xerr=[[tg["micro"]["f1"] - lo], [hi - tg["micro"]["f1"]]],
                fmt="none", ecolor=INK, elinewidth=0.9, capsize=2)
ax.set_yticks(range(len(cats)), cats)
ax.invert_yaxis()
ax.set_xlim(0, 1.0)
ax.set_xlabel("F1 trên tập test, chỉ phần mô hình. Thanh đen ở dòng Micro là CI95")
clean(ax)
h_, l_ = ax.get_legend_handles_labels()
ax.legend(h_[::-1], l_[::-1], loc="upper center", ncol=3, bbox_to_anchor=(0.45, -0.16))
save(fig, "h4_3_ner_baseline.png")

# ---------- Hình 4.4: đường Top-k của chuẩn hóa ----------
ND = "eval/normalization_2026-11-07"
na = {s: J(f"{ND}/{s}_after/report.json") for s in ("dev", "test")}
nbf = {s: J(f"{ND}/{s}_before/report.json") for s in ("dev", "test")}
ks = [1, 3, 5, 10]
lab_pos = []


def spread(ys, gap):
    idx = sorted(range(len(ys)), key=lambda i: ys[i])
    out = list(ys)
    for a, b in zip(idx, idx[1:]):
        if out[b] - out[a] < gap:
            out[b] = out[a] + gap
    return out

fig, ax = plt.subplots(figsize=(6.3, 3.0))
for (onto, lv, name, c, m) in [("ICD-10", "category", "ICD-10, nhóm 3 ký tự", C2, "s"),
                               ("ICD-10", "code", "ICD-10, mã đầy đủ", C1, "o"),
                               ("RxNorm", "code", "RxNorm", C3, "^")]:
    t = na["test"]["results"][onto][lv]["type"]
    v = [t[f"top{k}_acc"] for k in ks]
    ax.plot(ks, v, color=c, marker=m, markersize=5, linewidth=1.8, label=name)
    lab_pos.append((f"{name}: {vn(v[-1])}", v[-1]))
for (txt, y0), yy in zip(lab_pos, spread([y0 for _, y0 in lab_pos], 0.035)):
    ax.text(10.4, yy, txt, va="center", fontsize=8.5, color=INK)
ax.set_xticks(ks, [f"Top-{k}" for k in ks])
ax.set_xlim(0.6, 15.5)
ax.set_ylim(0.3, 0.9)
ax.set_ylabel("Độ chính xác Top-k")
clean(ax, grid_axis="y")
ax.spines["bottom"].set_bounds(1, 10)
save(fig, "h4_4_chuan_hoa_topk.png")

# ---------- Hình 4.5: trước và sau cải tiến, dev và test ----------
fig, axes = plt.subplots(1, 2, figsize=(6.3, 2.7), sharey=True)
for ax, onto in zip(axes, ["ICD-10", "RxNorm"]):
    xs = range(2)
    w = 0.36
    bef = [nbf[s]["results"][onto]["code"]["type"]["system"]["accuracy"] for s in ("dev", "test")]
    aft = [na[s]["results"][onto]["code"]["type"]["system"]["accuracy"] for s in ("dev", "test")]
    bb = ax.bar([x - w / 2 for x in xs], bef, width=w, color=GRAY, label="Trước cải tiến")
    ba = ax.bar([x + w / 2 for x in xs], aft, width=w, color=C1, label="Sau cải tiến")
    for b, v in list(zip(bb, bef)) + list(zip(ba, aft)):
        ax.text(b.get_x() + b.get_width() / 2, v + 0.015, vn(v), ha="center", fontsize=8)
    ax.set_xticks(list(xs), ["Dev", "Test"])
    ax.set_title(onto, fontsize=10)
    ax.set_ylim(0, 1.0)
    clean(ax, grid_axis="y")
axes[0].set_ylabel("Độ chính xác, chế độ strict")
axes[1].legend(loc="upper right")
save(fig, "h4_5_chuan_hoa_dev_test.png")

# ---------- Hình 4.6: forest plot mười phương pháp RE ----------
bench = J("outputs/re_benchmark_2026-11-08/benchmark.json")
bench["names"] = {k: v.replace(" ∪ luật", " hợp với rule-based").replace("Luật từ hướng dẫn", "Rule-based").replace(" (mọi cặp đúng kiểu)", "") for k, v in bench["names"].items()}
BM = [m for m in bench["names"] if m in bench["cv5"]]
fig, ax = plt.subplots(figsize=(6.3, 3.9))
order = BM[::-1]
for i, m in enumerate(order):
    for part, c, mk, dy, lab in [("cv5", C2, "s", 0.17, "Kiểm định chéo 5 phần"),
                                ("random_test", C1, "o", -0.17, "Test ngẫu nhiên")]:
        pm = bench[part][m]["positive_micro"]["f1"]
        lo, hi = bench[part][m]["positive_micro_f1_ci95"]
        ax.plot([lo, hi], [i + dy, i + dy], color=c, linewidth=1.6, solid_capstyle="round")
        ax.plot([pm], [i + dy], marker=mk, color=c, markersize=5.5, markeredgecolor="white", markeredgewidth=0.8,
                label=lab if i == 0 else None)
    v = bench["random_test"][m]["positive_micro"]["f1"]
    ax.text(1.0, i - 0.17, vn(v, 3), va="center", fontsize=8, color=INK)
ax.set_yticks(range(len(order)), [bench["names"][m] for m in order])
ax.set_xlim(0, 1.06)
ax.set_xlabel("Micro-F1 trên lớp dương và CI95. Cột số bên phải là F1 trên test ngẫu nhiên")
clean(ax)
ax.legend(loc="lower center", ncol=2, bbox_to_anchor=(0.45, 1.0))
save(fig, "h4_6_re_forest.png")

# ---------- Hình 4.7: heatmap F1 theo quan hệ trên test ngẫu nhiên ----------
rt = bench["random_test"]
ms = [m for m in BM if m != "majority"]
fig, ax = plt.subplots(figsize=(6.3, 3.9))
import numpy as np  # noqa: E402
from matplotlib.colors import LinearSegmentedColormap  # noqa: E402

M = np.array([[rt[m]["per_relation"][k]["f1"] for k in RELS] for m in ms])
cmap = LinearSegmentedColormap.from_list("seqgray", ["#ffffff"] + SEQ)
ax.imshow(M, cmap=cmap, vmin=0, vmax=1, aspect="auto")
for i in range(M.shape[0]):
    for j in range(M.shape[1]):
        ax.text(j, i, vn(M[i, j]), ha="center", va="center", fontsize=8.5, color="white" if M[i, j] > 0.55 else INK)
ax.set_xticks(range(len(RELS)), [f"{k}\nn={rt['rules']['per_relation'][k]['support']}" for k in RELS], fontsize=8)
ax.set_yticks(range(len(ms)), [bench["names"][m] for m in ms])
ax.grid(False)
for s in ax.spines.values():
    s.set_visible(False)
ax.tick_params(length=0)
ax.xaxis.tick_top()
save(fig, "h4_7_re_theo_quan_he.png")

# ---------- Hình 4.8: chênh lệch khi thêm dữ liệu dịch ----------
aug = J("outputs/re_benchmark_2026-11-08/augmented.json")
fig, ax = plt.subplots(figsize=(6.3, 2.3))
items = []
for tag, name in [("biotext", "Thêm BioText"), ("biotext_ade", "Thêm BioText và ADE")]:
    for st_, sname, c, mk in [("golden_test", "test hạn mức sau rà soát", C2, "s"), ("random_test", "test ngẫu nhiên", C1, "o")]:
        sc = aug["sets"][st_]["scores"]
        d = sc[f"{tag}+rules"]["positive_micro"]["f1"] - sc["baseline+rules"]["positive_micro"]["f1"]
        lo, hi = aug["sets"][st_]["paired_diff_ci95"][tag]["with_rules"]
        items.append((f"{name}, {sname}", d, lo, hi, c, mk))
for i, (lab, d, lo, hi, c, mk) in enumerate(items[::-1]):
    ax.plot([lo, hi], [i, i], color=c, linewidth=1.6, solid_capstyle="round")
    ax.plot([d], [i], marker=mk, color=c, markersize=5.5, markeredgecolor="white", markeredgewidth=0.8)
    ax.text(hi + 0.006, i, vn(d, 3), va="center", fontsize=8)
ax.axvline(0, color=MUTED, linewidth=0.9)
ax.set_yticks(range(len(items)), [x[0] for x in items[::-1]])
ax.set_xlabel("Chênh lệch F1 so với mô hình gốc, cả hai đều hợp với rule-based")
clean(ax)
save(fig, "h4_8_du_lieu_dich.png")

# ---------- Hình 4.9: lần xuất hiện của cạnh theo quan hệ, đồ thị mới so với đồ thị dựng bằng mô hình RE cũ ----------
kg = J("outputs/kg_test_2026-11-22/kg.json")
kg_old = J("outputs/kg_test_2026-11-08/kg.json")
occ = lambda g, k: sum(e["count"] for e in g["edges"] if e["relation"] == k)  # noqa: E731
fig, ax = plt.subplots(figsize=(6.3, 2.6))
order = sorted(RELS, key=lambda k: occ(kg, k))
h = 0.38
for i, k in enumerate(order):
    a, b = occ(kg_old, k), occ(kg, k)
    ax.barh(i + h / 2, a, color=C2, height=h, label="Mô hình RE cũ hợp với rule-based" if i == 0 else None)
    ax.barh(i - h / 2, b, color=C1, height=h, label="Mô hình RE mới" if i == 0 else None)
    ax.text(a + 3, i + h / 2, str(a), va="center", fontsize=7.5)
    ax.text(b + 3, i - h / 2, str(b), va="center", fontsize=7.5)
ax.set_yticks(range(len(order)), order)
ax.set_xlim(0, max(max(occ(kg, k), occ(kg_old, k)) for k in RELS) * 1.2)
ax.set_xlabel("Số lần xuất hiện của cạnh trong đồ thị dựng trên tập test")
clean(ax)
ax.legend(loc="lower right", fontsize=7.5)
save(fig, "h4_9_kg_canh.png")

# ---------- Hình 4.3: ma trận nhầm lẫn, vẽ lại ----------
# eval/metrics.py chỉ lưu ảnh (eval/results_2026-11-05/confusion_matrix.png), không lưu số;
# các ô dưới đây chép từ ảnh đó. Thứ tự gốc: BODY_PART, CONDITION, DOSAGE, DRUG, PROCEDURE, TEST, NONE.
CM_ORDER = ["BODY_PART", "CONDITION", "DOSAGE", "DRUG", "PROCEDURE", "TEST", "NONE"]
CM = [[1138, 77, 7, 10, 2, 0, 78], [150, 1324, 1, 8, 4, 5, 124], [8, 1, 212, 5, 0, 0, 36],
      [2, 6, 5, 695, 11, 2, 20], [116, 21, 4, 149, 791, 9, 196], [24, 2, 0, 1, 19, 255, 10],
      [175, 241, 260, 273, 248, 75, 0]]
show = LABELS6 + ["NONE"]
ix = [CM_ORDER.index(k) for k in show]
M = np.array([[CM[i][j] for j in ix] for i in ix], dtype=float)
fig, ax = plt.subplots(figsize=(6.3, 5.0))
ax.imshow(np.log1p(M), cmap=cmap, aspect="auto")
for i in range(7):
    for j in range(7):
        v = int(M[i, j])
        ax.text(j, i, f"{v:,}".replace(",", "."), ha="center", va="center", fontsize=8.5,
                color="white" if np.log1p(M[i, j]) > 0.62 * np.log1p(M.max()) else INK)
names = show
ax.set_xticks(range(7), names, rotation=30, ha="left", fontsize=8.5)
ax.set_yticks(range(7), names, fontsize=8.5)
ax.xaxis.tick_top()
ax.set_xlabel("Dự đoán")
ax.xaxis.set_label_position("top")
ax.set_ylabel("Nhãn chuẩn")
ax.grid(False)
for s in ax.spines.values():
    s.set_visible(False)
ax.tick_params(length=0)
save(fig, "h4_3b_ma_tran_nham_lan.png")

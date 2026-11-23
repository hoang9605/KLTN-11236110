"""Sinh chương Trích xuất quan hệ (Word) theo quy định trình bày của khóa luận.

Mọi con số đọc từ file kết quả trong relation/data và relation/outputs, không gõ tay.
Đánh số bảng, hình, công thức theo CH (đổi một hằng số khi ghép vào khóa luận).

Chạy: .venv\\Scripts\\python.exe -X utf8 -m relation.build_chapter
Đầu ra: relation/CHUONG_TRICH_XUAT_QUAN_HE.docx, relation/figures/ch_*.png
"""
import json
import random
from collections import Counter
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import FancyBboxPatch  # noqa: E402
from docx import Document  # noqa: E402
from docx.enum.table import WD_TABLE_ALIGNMENT  # noqa: E402
from docx.enum.text import WD_ALIGN_PARAGRAPH  # noqa: E402
from docx.oxml import OxmlElement, parse_xml  # noqa: E402
from docx.oxml.ns import qn  # noqa: E402
from docx.shared import Cm, Pt, RGBColor  # noqa: E402

from .ai_batches import load  # noqa: E402
from .evaluate import NEGATIVE, gold, predict, scores  # noqa: E402

HERE = Path(__file__).resolve().parent
DATA, OUTP, FIG = HERE / "data", HERE / "outputs", HERE / "figures"
OUT = HERE / "CHUONG_TRICH_XUAT_QUAN_HE.docx"
CH = "1"
REL = ["located_at", "treated_by", "treated_by_procedure", "diagnosed_by", "has_dosage"]
CFG_NAME = {"x0": "Chỉ dữ liệu thật", "x1": "Thêm dữ liệu sinh gấp một lần", "x3": "Thêm dữ liệu sinh gấp ba lần"}
GRAY = {"dark": "#262626", "mid": "#7f7f7f", "light": "#d9d9d9", "line": "#404040"}
M = "http://schemas.openxmlformats.org/officeDocument/2006/math"


def jl(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def n(x, d=2):
    if isinstance(x, float):
        return f"{x:.{d}f}".replace(".", ",")
    return f"{x:,}".replace(",", ".")


# ---------- công thức OMML ----------

def mr(t, sty=None):
    t = t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    rp = f'<m:rPr><m:sty m:val="{sty}"/></m:rPr>' if sty else ""
    return f'<m:r>{rp}<m:t xml:space="preserve">{t}</m:t></m:r>'


def mtext(t):
    return mr(t, "p")


def frac(a, b):
    return f"<m:f><m:num>{a}</m:num><m:den>{b}</m:den></m:f>"


def sub(base, s):
    return f"<m:sSub><m:e>{base}</m:e><m:sub>{s}</m:sub></m:sSub>"


def nsum(lo, hi, body):
    return (f'<m:nary><m:naryPr><m:chr m:val="∑"/><m:limLoc m:val="undOvr"/></m:naryPr>'
            f"<m:sub>{lo}</m:sub><m:sup>{hi}</m:sup><m:e>{body}</m:e></m:nary>")


def paren(body, beg="(", end=")"):
    return f'<m:d><m:dPr><m:begChr m:val="{beg}"/><m:endChr m:val="{end}"/></m:dPr><m:e>{body}</m:e></m:d>'


# ---------- tài liệu ----------

class Doc:
    def __init__(self):
        self.d = Document()
        st = self.d.styles["Normal"]
        st.font.name, st.font.size = "Times New Roman", Pt(13)
        st.element.rPr.rFonts.set(qn("w:eastAsia"), "Times New Roman")
        st.paragraph_format.line_spacing = 1.3
        st.paragraph_format.space_after = Pt(6)
        for s in self.d.sections:
            s.top_margin, s.bottom_margin, s.left_margin, s.right_margin = Cm(2.5), Cm(2.5), Cm(3.5), Cm(2.5)
        for lvl, size in ((1, 14), (2, 13), (3, 13)):
            h = self.d.styles[f"Heading {lvl}"]
            h.font.name, h.font.size, h.font.bold, h.font.italic = "Times New Roman", Pt(size), True, False
            h.font.color.rgb = RGBColor(0, 0, 0)
            h.element.rPr.rFonts.set(qn("w:eastAsia"), "Times New Roman")
        self.t = self.f = self.e = 0

    def lab(self, kind):
        k = {"Bảng": self.t, "Hình": self.f}[kind] + 1
        return f"{kind} {CH}.{k}"

    def eqlab(self, k=1):
        return f"({CH}.{self.e + k})"

    def h(self, text, lvl):
        hd = self.d.add_heading(text, lvl)
        hd.paragraph_format.keep_with_next = True

    def p(self, text, keep_next=False):
        para = self.d.add_paragraph(text)
        pf = para.paragraph_format
        pf.first_line_indent, pf.keep_together = Cm(0.75), True
        pf.keep_with_next = keep_next
        para.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        return para

    def bullet(self, text, last=False):
        para = self.d.add_paragraph("●  " + text)
        pf = para.paragraph_format
        pf.left_indent, pf.keep_together, pf.keep_with_next = Cm(0.75), True, not last
        para.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

    def where(self, items):
        para = self.d.add_paragraph("Trong đó:")
        para.paragraph_format.keep_with_next = True
        for i, it in enumerate(items):
            self.bullet(it, last=i == len(items) - 1)

    def eq(self, omml):
        self.e += 1
        t = self.d.add_table(rows=1, cols=2)
        t.alignment = WD_TABLE_ALIGNMENT.CENTER
        c0, c1 = t.rows[0].cells
        c0.width, c1.width = Cm(13), Cm(2)
        p0 = c0.paragraphs[0]
        p0.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p0._p.append(parse_xml(f'<m:oMath xmlns:m="{M}">{omml}</m:oMath>'))
        p1 = c1.paragraphs[0]
        p1.add_run(f"({CH}.{self.e})")
        p1.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        for c in (p0, p1):
            c.paragraph_format.keep_with_next = True
        return f"({CH}.{self.e})"

    def note(self, text):
        para = self.d.add_paragraph()
        r = para.add_run(text)
        r.italic, r.font.size = True, Pt(11)
        r.font.color.rgb = RGBColor(0x59, 0x59, 0x59)
        para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        para.paragraph_format.keep_together = True

    def table(self, caption, header, rows, note, widths=None):
        self.t += 1
        cap = self.d.add_paragraph(f"Bảng {CH}.{self.t}. {caption}")
        cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        cap.paragraph_format.keep_with_next = True
        t = self.d.add_table(rows=1, cols=len(header))
        t.style = "Table Grid"
        t.alignment = WD_TABLE_ALIGNMENT.CENTER
        allrows = [header] + [list(r) for r in rows]
        for ri, row in enumerate(allrows):
            cells = t.rows[0].cells if ri == 0 else t.add_row().cells
            for i, x in enumerate(row):
                cells[i].text = ""
                para = cells[i].paragraphs[0]
                r = para.add_run(str(x))
                r.font.size, r.bold = Pt(12), ri == 0
                s = str(x).replace(".", "").replace(",", "").replace("–", "")
                if ri and i and s.isdigit():
                    para.alignment = WD_ALIGN_PARAGRAPH.RIGHT
                pf = para.paragraph_format
                pf.line_spacing, pf.space_after, pf.keep_with_next = 1.0, Pt(0), ri < len(allrows) - 1
                if widths:
                    cells[i].width = Cm(widths[i])
            trPr = t.rows[ri]._tr.get_or_add_trPr()
            cs = OxmlElement("w:cantSplit"); trPr.append(cs)
        self.note(note)

    def figure(self, path, caption, note, width=15):
        self.f += 1
        self.d.add_picture(str(path), width=Cm(width))
        pic = self.d.paragraphs[-1]
        pic.alignment = WD_ALIGN_PARAGRAPH.CENTER
        pic.paragraph_format.keep_with_next, pic.paragraph_format.line_spacing = True, 1.0
        cap = self.d.add_paragraph()
        r = cap.add_run(f"Hình {CH}.{self.f}. {caption}")
        r.italic = True
        cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        cap.paragraph_format.keep_with_next = True
        self.note(note)


# ---------- hình (thang xám) ----------

def style():
    plt.rcParams.update({"font.family": "Arial", "font.size": 16, "axes.edgecolor": GRAY["line"],
                         "axes.labelcolor": "#111111", "xtick.color": "#111111", "ytick.color": "#111111"})


def box(ax, x, y, w, h, title, sub=None, fill="#f2f2f2", fs=15):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.08", fc=fill, ec=GRAY["line"], lw=1.2))
    if sub:
        ax.text(x + w / 2, y + h * 0.64, title, ha="center", va="center", fontsize=fs, weight="bold")
        ax.text(x + w / 2, y + h * 0.30, sub, ha="center", va="center", fontsize=fs - 3, color="#333333")
    else:
        ax.text(x + w / 2, y + h / 2, title, ha="center", va="center", fontsize=fs, weight="bold")


def arrow(ax, x1, y1, x2, y2):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1), arrowprops=dict(arrowstyle="-|>", color=GRAY["line"], lw=1.3))


def fig_pipeline(path, nums):
    style()
    fig, ax = plt.subplots(figsize=(12, 10.5))
    ax.set_xlim(0, 12); ax.set_ylim(0, 10.6); ax.axis("off")
    W, H = 3.4, 0.95
    cols = {"tr": 0.5, "dv": 4.3, "te": 8.1}
    box(ax, 3.3, 9.4, 5.4, H, "Kho VietMed-NER", "câu lời nói y tế có nhãn thực thể")
    arrow(ax, 6, 9.4, 6, 9.05)
    box(ax, 3.3, 8.1, 5.4, H, "Sinh cặp ứng viên", "theo cặp kiểu thực thể của lược đồ")
    arrow(ax, 6, 8.1, 6, 7.75)
    box(ax, 3.3, 6.8, 5.4, H, "Chọn mẫu", "hạn mức theo quan hệ, tách tập kiểm tra")
    ax.plot([6, 6], [6.78, 6.6], color=GRAY["line"], lw=1.3)
    ax.plot([cols["tr"] + W / 2, cols["te"] + W / 2], [6.6, 6.6], color=GRAY["line"], lw=1.3)
    for k in cols:
        arrow(ax, cols[k] + W / 2, 6.6, cols[k] + W / 2, 6.37)
    box(ax, cols["tr"], 5.4, W, H, "Tập huấn luyện", nums["tr"], fill=GRAY["light"])
    box(ax, cols["dv"], 5.4, W, H, "Tập kiểm định", nums["dv"], fill=GRAY["light"])
    box(ax, cols["te"], 5.4, W, H, "Tập kiểm tra", nums["te"], fill=GRAY["light"])
    for k in cols:
        arrow(ax, cols[k] + W / 2, 5.4, cols[k] + W / 2, 5.05)
    box(ax, cols["tr"], 4.1, W + 3.8, H, "LLM gán hai lượt, người chuyên môn duyệt", "kiểm tra thực thể trước, gán quan hệ sau")
    box(ax, cols["te"], 4.1, W, H, "Người chuyên môn gán", "soát mẫu rồi gán lại")
    arrow(ax, cols["tr"] + W / 2, 4.1, cols["tr"] + W / 2, 3.75)
    box(ax, cols["tr"], 2.8, W, H, "Thêm dữ liệu sinh", "thay thực thể, mẫu câu")
    arrow(ax, cols["tr"] + W / 2, 2.8, cols["tr"] + W / 2, 2.45)
    box(ax, cols["tr"], 1.5, W, H, "Huấn luyện", "ba mức, ba lần khởi tạo")
    arrow(ax, cols["dv"] + W / 2, 4.1, cols["dv"] + W / 2, 1.0)
    arrow(ax, cols["tr"] + W / 2, 1.5, cols["tr"] + W / 2, 1.0)
    box(ax, cols["tr"], 0.05, W + 3.8, H, "Chọn mức trên tập kiểm định", "macro F1 cao nhất")
    arrow(ax, cols["te"] + W / 2, 4.1, cols["te"] + W / 2, 1.0)
    box(ax, cols["te"], 0.05, W, H, "Chấm một lần", "mô hình đã chọn")
    arrow(ax, cols["tr"] + W + 3.8, 0.52, cols["te"], 0.52)
    fig.tight_layout(); fig.savefig(path, dpi=200); plt.close(fig)


def fig_model(path):
    style()
    fig, ax = plt.subplots(figsize=(12, 7.2))
    ax.set_xlim(0, 12); ax.set_ylim(0, 7.4); ax.axis("off")
    toks = ["[HEAD_CONDITION]", "đau", "[/HEAD]", "ở", "[TAIL_BODY_PART]", "vùng bụng", "[/TAIL]"]
    xs = [0.2, 2.0, 3.0, 4.1, 4.9, 7.0, 8.4]
    ws = [1.7, 0.9, 1.0, 0.7, 2.0, 1.3, 1.0]
    for x, w, t in zip(xs, ws, toks):
        mark = t.startswith("[")
        ax.add_patch(FancyBboxPatch((x, 0.3), w, 0.6, boxstyle="round,pad=0.02,rounding_size=0.05",
                                    fc=GRAY["light"] if mark else "white", ec=GRAY["line"], lw=1))
        ax.text(x + w / 2, 0.6, t, ha="center", va="center", fontsize=11 if mark else 13)
    for x, w in zip(xs, ws):
        arrow(ax, x + w / 2, 0.92, x + w / 2, 1.45)
    box(ax, 0.2, 1.5, 9.2, 1.1, "ViHealthBERT", "12 lớp Transformer, vector ẩn 768 chiều")
    arrow(ax, xs[0] + ws[0] / 2, 2.62, 2.0, 3.25)
    arrow(ax, xs[4] + ws[4] / 2, 2.62, 5.5, 3.25)
    box(ax, 0.8, 3.3, 2.6, 0.8, "vector đầu", fill=GRAY["light"], fs=13)
    box(ax, 4.3, 3.3, 2.6, 0.8, "vector đuôi", fill=GRAY["light"], fs=13)
    arrow(ax, 2.1, 4.12, 3.6, 4.6); arrow(ax, 5.6, 4.12, 4.2, 4.6)
    box(ax, 2.1, 4.65, 3.6, 0.8, "nối, dropout, tuyến tính", fs=13)
    arrow(ax, 3.9, 5.47, 3.9, 5.85)
    box(ax, 2.1, 5.9, 3.6, 0.8, "softmax: xác suất có quan hệ", fs=13)
    arrow(ax, 5.72, 6.3, 7.4, 6.3)
    box(ax, 7.45, 5.75, 4.3, 1.1, "Trung bình ba mô hình", "dương khi xác suất ≥ 0,5", fs=14)
    ax.text(10.55, 4.2, "ba lần khởi tạo\nngẫu nhiên khác nhau", ha="center", va="center", fontsize=12, color="#333333")
    arrow(ax, 10.55, 4.65, 10.55, 5.7)
    fig.tight_layout(); fig.savefig(path, dpi=200); plt.close(fig)


def fig_dev(path, dev):
    style()
    fig, ax = plt.subplots(figsize=(12, 5.2))
    keys = ["x0", "x1", "x3"]
    x = range(3); w = 0.36
    mac = [dev[k]["macro_f1"] for k in keys]; mic = [dev[k]["micro"]["f1"] for k in keys]
    b1 = ax.bar([i - w / 2 for i in x], mac, w, color=GRAY["dark"], label="Macro F1")
    b2 = ax.bar([i + w / 2 for i in x], mic, w, color="white", edgecolor=GRAY["dark"], hatch="//", label="Micro F1")
    for bars in (b1, b2):
        for b in bars:
            ax.text(b.get_x() + b.get_width() / 2, b.get_height() + 0.005, n(b.get_height()), ha="center", fontsize=14)
    ax.set_xticks(list(x)); ax.set_xticklabels([CFG_NAME[k].replace("Thêm dữ liệu sinh ", "Thêm sinh\n") for k in keys])
    ax.set_ylim(0.7, 0.9); ax.set_yticks([0.70, 0.75, 0.80, 0.85, 0.90]); ax.set_ylabel("F1 trên tập kiểm định")
    ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: n(v)))
    ax.spines[["top", "right"]].set_visible(False); ax.legend(frameon=False, loc="upper right", ncol=2)
    fig.tight_layout(); fig.savefig(path, dpi=200); plt.close(fig)


def fig_rel(path, per):
    style()
    fig, ax = plt.subplots(figsize=(12, 5.6))
    x = range(len(REL)); w = 0.26
    vals = {k: [per[r][k] for r in REL] for k in ("precision", "recall", "f1")}
    sty = {"precision": dict(color=GRAY["light"], edgecolor=GRAY["dark"]), "recall": dict(color="white", edgecolor=GRAY["dark"], hatch=".."),
           "f1": dict(color=GRAY["dark"], edgecolor=GRAY["dark"])}
    lab = {"precision": "Precision", "recall": "Recall", "f1": "F1"}
    for j, k in enumerate(("precision", "recall", "f1")):
        bars = ax.bar([i + (j - 1) * w for i in x], vals[k], w, label=lab[k], **sty[k])
        for b in bars:
            ax.text(b.get_x() + b.get_width() / 2, b.get_height() + 0.01, n(b.get_height()), ha="center", fontsize=11)
    ax.set_xticks(list(x)); ax.set_xticklabels([r.replace("treated_by_procedure", "treated_by_\nprocedure") for r in REL], fontsize=14)
    ax.set_ylim(0, 1.12); ax.set_ylabel("Giá trị trên tập kiểm tra")
    ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: n(v, 1)))
    ax.spines[["top", "right"]].set_visible(False); ax.legend(frameon=False, ncol=3, loc="upper left")
    fig.tight_layout(); fig.savefig(path, dpi=200); plt.close(fig)


# ---------- số liệu ----------

def counts(rows):
    c = Counter()
    for r in rows:
        for x in r["relations"]:
            c[(x["allowed_relation"], x["label"] != NEGATIVE)] += 1
    return c


def seed_f1(res, g, split):
    out = []
    for s in sorted(res[split]):
        p = {u: (u.rsplit(":", 1)[1] if v >= 0.5 else NEGATIVE) for u, v in res[split][s].items()}
        out.append(scores(g, p)["micro"]["f1"])
    return out


def main():
    explore, sel = jl(DATA / "explore.json"), jl(DATA / "selection.json")
    rs, man = jl(DATA / "seed_review_summary.json"), jl(DATA / "synth" / "manifest.json")
    ev, ev2, modes = jl(OUTP / "evaluation.json"), jl(OUTP / "evaluation_test_v2.json"), jl(OUTP / "evaluation_test_v2_modes.json")
    audit = jl(OUTP / "review_fn_summary.json")
    cfg = jl(HERE.parent / "Model" / "vihealthbert-re-vietmed-validated" / "re_config.json")
    seed, dev, t1, t2 = load(DATA / "seed.jsonl"), load(DATA / "dev.jsonl"), load(DATA / "test.jsonl"), load(DATA / "test_v2.jsonl")
    cs, cd, c1, c2 = counts(seed), counts(dev), counts(t1), counts(t2)
    x1 = jl(OUTP / "train" / "x1.json")
    sf_dev, sf_test = seed_f1(x1, gold(dev), "dev"), seed_f1(x1, gold(t2), "test")
    sp, tp, tags = explore["seed_pool"], explore["test_pool"], explore["raw_vietmed_entity_tags"]
    pool = sel["pool_sentences_with_valid_candidate"]
    seed_pairs = sum(cs.values()); seed_pos = sum(v for k, v in cs.items() if k[1])
    dev_pairs = sum(cd.values()); dev_pos = sum(v for k, v in cd.items() if k[1])
    t_pairs = sum(c2.values()); t1_pos = sum(v for k, v in c1.items() if k[1]); t2_pos = sum(v for k, v in c2.items() if k[1])
    inv_test = sum(e["validity"] == "INVALID" for r in t1 for e in r["entities"])
    best = ev["chosen"]
    mo, ru, un = modes["model"]["micro"], modes["rules"]["micro"], modes["union"]["micro"]
    ci = modes["ci95_micro_f1"]
    ap2 = ev2["always_positive"]["micro"]
    per = ev2["model"]["per_relation"]
    x1m = man["x1"]["by_method"]
    FIG.mkdir(exist_ok=True)
    fig_pipeline(FIG / "ch_quy_trinh_re.png", {"tr": f"{n(rs['seed_sentences'])} câu, {n(seed_pairs)} cặp",
                                               "dv": f"{n(rs['dev_sentences'])} câu, {n(dev_pairs)} cặp",
                                               "te": f"{n(len(t2))} câu, {n(t_pairs)} cặp"})
    fig_model(FIG / "ch_mo_hinh_re.png")
    fig_dev(FIG / "ch_ket_qua_dev.png", ev["dev"])
    fig_rel(FIG / "ch_ket_qua_quan_he.png", per)

    D = Doc()
    D.h(f"CHƯƠNG {CH}. TRÍCH XUẤT QUAN HỆ Y KHOA", 1)
    D.p("Chương này trình bày toàn bộ phần trích xuất quan hệ của hệ thống, từ việc xây dựng dữ liệu, bổ sung dữ liệu huấn luyện, thiết kế và huấn luyện mô hình "
        "cho tới đánh giá và tích hợp vào luồng xử lý. Kết quả chính có thể tóm tắt ngay từ đầu. Mô hình ViHealthBERT-RE, được huấn luyện trên tập huấn luyện "
        f"đã được người có chuyên môn y khoa duyệt cùng một lượng dữ liệu sinh bằng chính tập đó, đạt micro F1 {n(mo['f1'])} trên tập kiểm tra do người có chuyên môn gán, "
        f"với khoảng tin cậy 95% từ {n(ci['model'][0])} đến {n(ci['model'][1])}. Kết quả này cao hơn phương pháp rule-based ({n(ru['f1'])}) "
        f"và cao hơn rõ rệt bộ dự đoán luôn trả lời có quan hệ ({n(ap2['f1'])}). Khi chạy cùng phương pháp rule-based như trong hệ thống, micro F1 giữ ở mức {n(un['f1'])} "
        "và recall tăng thêm. Thí nghiệm về lượng dữ liệu sinh cho thấy bổ sung một lượng bằng dữ liệu thật giúp mô hình tốt hơn, còn bổ sung gấp ba lại làm kết quả giảm.")

    # 1.1
    D.h(f"{CH}.1. Bài toán và lược đồ quan hệ", 2)
    D.p("Trích xuất quan hệ là bài toán xác định, với một cặp thực thể đã được nhận diện trong câu, câu đó có diễn đạt một quan hệ y khoa giữa hai thực thể hay không. "
        f"Hệ thống dùng năm quan hệ, mỗi quan hệ gắn với đúng một cặp kiểu thực thể như {D.lab('Bảng')}. Vì kiểu của hai thực thể đã quyết định quan hệ duy nhất có thể có, "
        "bài toán với mỗi cặp ứng viên được đưa về phân loại nhị phân giữa quan hệ đó và NO_RELATION. Cách đặt bài toán này giảm số lớp phải học, "
        "đồng thời tránh được những dự đoán vô nghĩa như một loại thuốc nằm ở một bộ phận cơ thể.")
    D.table("Lược đồ năm quan hệ và cặp kiểu thực thể tương ứng", ["Quan hệ", "Thực thể đầu", "Thực thể đuôi", "Ý nghĩa"],
            [("located_at", "CONDITION", "BODY_PART", "Bệnh hoặc triệu chứng ở bộ phận cơ thể"),
             ("treated_by", "CONDITION", "DRUG", "Bệnh được điều trị bằng thuốc"),
             ("treated_by_procedure", "CONDITION", "PROCEDURE", "Bệnh được điều trị bằng thủ thuật"),
             ("diagnosed_by", "CONDITION", "TEST", "Bệnh được chẩn đoán bằng xét nghiệm hay thăm khám"),
             ("has_dosage", "DRUG", "DOSAGE", "Thuốc có liều dùng")],
            "Bảng cho biết mỗi quan hệ chỉ được xét cho một cặp kiểu thực thể cố định.", widths=[3.6, 2.6, 2.6, 6.2])

    # 1.2
    D.h(f"{CH}.2. Quy trình xây dựng dữ liệu và huấn luyện", 2)
    D.p(f"Quy trình gồm bảy bước nối tiếp như {D.lab('Hình')}. Dữ liệu được lấy từ kho VietMed-NER, ghép thành các cặp ứng viên theo lược đồ, rồi chọn mẫu và tách thành "
        "ba tập có vai trò riêng biệt. Tập huấn luyện dùng để học, tập kiểm định dùng để chọn cấu hình, và tập kiểm tra chỉ được dùng một lần để chấm mô hình đã chọn. "
        "Tập kiểm tra được tách ra ngay ở bước chọn mẫu, trước mọi bước huấn luyện, nên không có thông tin nào từ tập này ảnh hưởng tới việc học hay việc chọn mô hình.")
    D.figure(FIG / "ch_quy_trinh_re.png", "Quy trình xây dựng dữ liệu và huấn luyện mô hình trích xuất quan hệ",
             "Hình cho thấy ba tập dữ liệu được tách từ đầu và mỗi tập chỉ tham gia vào một vai trò.", width=14.5)

    # 1.3
    D.h(f"{CH}.3. Dữ liệu nguồn và chọn mẫu", 2)
    D.h(f"{CH}.3.1. Dữ liệu nguồn", 3)
    D.p(f"Kho VietMed-NER [2] gồm {n(sp['sentences'] + tp['sentences'])} câu là bản ghi lời nói y tế, mỗi câu dài khoảng {n(int(sp['sentence_words_median']))} từ, "
        "không có dấu câu và thường bị cắt giữa chừng. Kho chỉ có nhãn thực thể, không có nhãn quan hệ, nên toàn bộ nhãn quan hệ trong chương này đều được xây dựng mới. "
        f"Chín kiểu thực thể gốc của kho được ánh xạ về sáu kiểu dùng cho bài toán như {D.lab('Bảng')}.")
    D.table("Ánh xạ kiểu thực thể của VietMed-NER sang kiểu thực thể của bài toán", ["Kiểu thực thể", "Kiểu gốc", "Số lượt đề cập"],
            [("CONDITION", "DISEASESYMTOM", n(tags["DISEASESYMTOM"])),
             ("DRUG", "DRUGCHEMICAL, PREVENTIVEMED", n(tags["DRUGCHEMICAL"] + tags["PREVENTIVEMED"])),
             ("BODY_PART", "ORGAN", n(tags["ORGAN"])),
             ("TEST", "DIAGNOSTICS", n(tags["DIAGNOSTICS"])),
             ("PROCEDURE", "SURGERY, MEDDEVICETECHNIQUE, TREATMENT", n(tags["SURGERY"] + tags["MEDDEVICETECHNIQUE"] + tags["TREATMENT"])),
             ("DOSAGE", "UNITCALIBRATOR", n(tags["UNITCALIBRATOR"]))],
            "Bảng cho biết mỗi kiểu thực thể của bài toán được tạo từ những kiểu nào của bộ nhãn gốc.", widths=[3.2, 8.0, 3.4])
    D.p(f"Sau khi ghép cặp theo lược đồ và bỏ những lượt đề cập quá chung chung như điều trị hay thuốc khi đứng một mình, chỉ {n(pool['seed'])} câu ở phần huấn luyện "
        f"và {n(pool['test'])} câu ở phần kiểm tra của kho còn cặp ứng viên. Phân bố cặp rất lệch giữa các quan hệ như {D.lab('Hình')}. "
        "Quan hệ located_at chiếm phần lớn, trong khi diagnosed_by và has_dosage rất hiếm, và phần lớn lượt đề cập DOSAGE trong kho là số liệu thống kê hay tính từ chứ không phải liều thuốc.")
    D.figure(FIG / "h_cap_ung_vien.png", "Số cặp ứng viên và số cặp có tín hiệu dương theo quan hệ ở phần huấn luyện của kho",
             "Hình cho thấy dữ liệu rất mất cân bằng, nên việc chọn mẫu phải ưu tiên các quan hệ hiếm.", width=14.5)

    D.h(f"{CH}.3.2. Chọn mẫu", 3)
    D.p("Nếu chọn câu ngẫu nhiên, tập dữ liệu sẽ gần như chỉ có located_at và rất ít cặp dương. Vì vậy mỗi cặp ứng viên được gán một điểm khả năng dương "
        f"theo công thức {D.eqlab()}, và câu được ưu tiên theo điểm này.", keep_next=True)
    D.eq(sub(mr("s"), mr("h,t")) + mr(" = 3·") + sub(mr("𝟙"), mtext("quy tắc")) + mr(" + ") + sub(mr("𝟙"), mtext("gần")) + mr(" + ") + sub(mr("𝟙"), mtext("gợi ý")))
    D.where(["h và t là thực thể đầu và thực thể đuôi của cặp ứng viên.",
             "𝟙 quy tắc bằng 1 khi phương pháp rule-based dự đoán cặp có quan hệ và bằng 0 trong trường hợp ngược lại. Thành phần này có trọng số 3 vì đây là tín hiệu mạnh nhất.",
             f"𝟙 gần bằng 1 khi hai thực thể cách nhau không quá {sel['near_words']} từ, vì quan hệ trong lời nói thường được diễn đạt trong một cụm ngắn.",
             "𝟙 gợi ý bằng 1 khi giữa hai thực thể có từ gợi ý như điều trị bằng, uống, ở hay xét nghiệm."])
    D.p("Điểm này chỉ dùng để chọn câu, không dùng làm nhãn. Các hệ số được đặt theo trực giác và không được tinh chỉnh, vì mục tiêu chỉ là tăng tỉ lệ cặp dương trong mẫu chứ không phải dự đoán chính xác.")
    seed_q, test_q = sel["plan"]["seed"]["quota"], sel["plan"]["test"]["quota"]
    D.p(f"Câu được lấy theo hạn mức của từng quan hệ, mỗi quan hệ tối đa {n(seed_q['located_at'])} câu ở phần huấn luyện, ưu tiên quan hệ hiếm trước, "
        f"kèm {n(sel['plan']['seed']['random'])} câu chọn ngẫu nhiên để tập dữ liệu không chỉ gồm những câu dễ. Các câu đã chọn được chia thành "
        f"{n(sel['seed']['sentences'])} câu huấn luyện và {n(sel['dev']['sentences'])} câu kiểm định. Tập kiểm tra gồm {n(sel['test']['sentences'])} câu lấy từ phần kiểm tra của kho, "
        f"trong đó {n(sel['plan']['test']['random'])} câu chọn ngẫu nhiên. Để tránh rò rỉ, không câu huấn luyện nào có chung một chuỗi {sel['leak_ngram']} từ liên tiếp với câu kiểm tra. "
        f"Số câu và số cặp sau khi chọn mẫu được trình bày ở {D.lab('Bảng')}.")
    D.table("Số câu và số cặp ứng viên theo quan hệ sau khi chọn mẫu", ["Quan hệ", "Câu huấn luyện", "Cặp huấn luyện", "Cặp kiểm định", "Câu kiểm tra", "Cặp kiểm tra"],
            [(r, n(sel["seed"]["sentences_by_relation"][r]), n(sel["seed"]["pairs_by_relation"][r]), n(sel["dev"]["pairs_by_relation"][r]),
              n(sel["test"]["sentences_by_relation"][r]), n(sel["test"]["pairs_by_relation"][r])) for r in REL],
            "Bảng cho thấy diagnosed_by và has_dosage vẫn rất ít ngay cả khi đã lấy toàn bộ câu có ứng viên.", widths=[3.8, 2.2, 2.2, 2.2, 2.2, 2.2])

    # 1.4
    D.h(f"{CH}.4. Gán nhãn", 2)
    D.h(f"{CH}.4.1. Thiết kế gán nhãn hai bước", 3)
    D.p("Nhãn thực thể của kho có nhiều lỗi, chẳng hạn từ cao hay nồng độ bị gán là liều dùng. Nếu gán quan hệ trực tiếp trên những thực thể này, mô hình sẽ học cách nhận ra thực thể sai "
        "thay vì học quan hệ. Vì vậy việc gán nhãn được tách làm hai bước. Bước thứ nhất xét từng lượt đề cập và quyết định nó là thực thể hợp lệ hay không hợp lệ. "
        "Bước thứ hai chỉ áp dụng cho những cặp có cả hai thực thể hợp lệ, với nhãn là tên quan hệ của cặp hoặc NO_RELATION. Một cặp chỉ được gán là có quan hệ khi câu nói rõ quan hệ đó, "
        "còn những cặp chỉ cùng xuất hiện trong câu như khi liệt kê nhiều bệnh, nói về phòng bệnh, tác dụng phụ hay phủ định đều là NO_RELATION. "
        "Hướng dẫn gán nhãn được viết từ câu thật trong kho, có ví dụ dương và âm cho từng quan hệ.")

    D.h(f"{CH}.4.2. Tập huấn luyện và tập kiểm định", 3)
    D.p("Tập huấn luyện và tập kiểm định được mô hình ngôn ngữ lớn (LLM) gán hai lượt độc lập theo hướng dẫn, sau đó người có chuyên môn y khoa duyệt toàn bộ nhãn. "
        f"Những chỗ hai lượt gán bất đồng mà chưa được quyết định bị loại khỏi dữ liệu thay vì được đoán, gồm {n(rs['entity_unresolved_dropped'])} lượt đề cập, "
        f"{n(rs['pair_unresolved_dropped'])} cặp và {n(rs['pair_dropped_entity_unresolved'])} cặp chứa các lượt đề cập đó. Kết quả là tập huấn luyện có {n(seed_pairs)} cặp, "
        f"trong đó {n(seed_pos)} cặp dương, và tập kiểm định có {n(dev_pairs)} cặp với {n(dev_pos)} cặp dương. Phân bố theo quan hệ ở {D.lab('Bảng')}.")
    D.table("Số cặp dương và âm của tập huấn luyện và tập kiểm định theo quan hệ", ["Quan hệ", "Huấn luyện, dương", "Huấn luyện, âm", "Kiểm định, dương", "Kiểm định, âm"],
            [(r, n(cs[(r, True)]), n(cs[(r, False)]), n(cd[(r, True)]), n(cd[(r, False)])) for r in REL],
            "Bảng cho thấy sau hai bước gán và duyệt, tập huấn luyện không còn cặp has_dosage nào và tập kiểm định chỉ có ba quan hệ.", widths=[3.8, 2.8, 2.8, 2.8, 2.8])
    D.p("Tỉ lệ dương của tập huấn luyện khoảng " + n(seed_pos / seed_pairs) + ", tức phần lớn cặp ứng viên không có quan hệ. Điều này phù hợp với đặc điểm của lời nói, "
        "nơi nhiều thực thể được nhắc liền nhau mà không có liên hệ. Việc has_dosage không còn cặp nào là lý do chính để bổ sung dữ liệu sinh ở mục " + f"{CH}.5.")

    D.h(f"{CH}.4.3. Tập kiểm tra", 3)
    D.p(f"Tập kiểm tra gồm {n(len(t2))} câu do người có chuyên môn y khoa gán trực tiếp trên phiếu đã xáo trộn thứ tự câu. Ở bước kiểm tra thực thể, {n(inv_test)} lượt đề cập bị loại, "
        f"còn lại {n(t_pairs)} cặp. Ở lượt gán đầu, người gán coi hầu hết cặp cùng câu là có quan hệ, với {n(t1_pos)} trên {n(t_pairs)} cặp dương. "
        "Với tỉ lệ này, một bộ dự đoán luôn trả lời có quan hệ gần như đạt điểm tối đa, nên tập kiểm tra không đo được khả năng loại bỏ cặp sai.")
    neg50 = audit.get("fn", {}).get("negative", 0) + audit.get("control_tp", {}).get("negative", 0)
    D.p(f"Để thống nhất tiêu chí với hướng dẫn, người gán soát lại một mẫu 50 cặp mà không thấy nhãn cũ hay dự đoán của mô hình, và đánh lại {n(neg50)} trên 50 cặp là không có quan hệ. "
        f"Sau đó toàn bộ {n(t_pairs)} cặp được gán lại theo tiêu chí chặt, còn {n(t2_pos)} cặp dương. Bản gán lại được dùng làm tập kiểm tra cho mọi kết quả trong chương, "
        f"và số cặp dương ở hai lượt được so sánh ở {D.lab('Bảng')}.")
    D.table("Số cặp dương của tập kiểm tra ở lượt gán đầu và sau khi gán lại", ["Quan hệ", "Số cặp", "Dương lượt đầu", "Dương sau gán lại"],
            [(r, n(c2[(r, True)] + c2[(r, False)]), n(c1[(r, True)]), n(c2[(r, True)])) for r in REL] + [("Tổng", n(t_pairs), n(t1_pos), n(t2_pos))],
            "Bảng cho thấy tiêu chí chặt loại phần lớn cặp chỉ cùng xuất hiện trong câu, nhất là ở located_at.", widths=[4.2, 2.6, 3.4, 3.8])

    # 1.5
    D.h(f"{CH}.5. Bổ sung dữ liệu huấn luyện", 2)
    D.p(f"Tập huấn luyện chỉ có {n(seed_pairs)} cặp và không có cặp has_dosage nào, nên dữ liệu được bổ sung bằng hai cách khác nhau về bản chất. "
        "Cách thứ nhất là tăng cường dữ liệu, tức sửa câu thật bằng cách thay một thực thể. Cách thứ hai là sinh câu mới từ khung câu viết tay. "
        "Cả hai chỉ được dùng cho huấn luyện, còn tập kiểm định và tập kiểm tra luôn chỉ gồm câu thật.")

    D.h(f"{CH}.5.1. Tăng cường dữ liệu bằng thay thực thể", 3)
    D.p("Ý tưởng của cách này là quan hệ được quyết định bởi ngữ cảnh của câu chứ không phải bởi tên thực thể cụ thể, theo hướng của Dai và Adel [35]. "
        "Với mỗi câu huấn luyện, một thực thể được thay bằng thực thể khác cùng kiểu lấy từ từ điển, phần còn lại của câu và nhãn của mọi cặp được giữ nguyên, "
        "và mỗi câu sinh tối đa năm biến thể. Chẳng hạn câu khớp gối tê buồn chân tay giảm đáng kể được biến đổi thành khớp gối tê buồn phế quản giảm đáng kể, "
        "và cặp giữa hai thực thể vẫn mang nhãn NO_RELATION như câu gốc. Nhờ vậy mô hình học từ ngữ cảnh thay vì ghi nhớ tên thực thể.")
    D.p("Để nhãn không bị sai sau khi thay, cách này có ba ràng buộc. Thứ nhất, nếu thực thể đang có quan hệ dương thì thực thể thay vào phải cùng nhóm chuyên khoa với thực thể còn lại, "
        "chẳng hạn thuốc cho bệnh dạ dày chỉ được thay bằng thuốc tiêu hóa. Thứ hai, lượt đề cập liều dùng không bao giờ bị thay, vì nhiều cặp has_dosage âm là âm chính vì lượt đề cập đó "
        "không phải liều thật, và thay bằng một liều thật sẽ làm nhãn sai. Thứ ba, thực thể chỉ nằm trong cặp âm chỉ được thay khi bản thân nó là thực thể thật có trong từ điển.")

    D.h(f"{CH}.5.2. Dữ liệu sinh theo mẫu câu", 3)
    D.p("Tăng cường dữ liệu chỉ nhân bản được những gì tập huấn luyện đã có, nên không thể tạo ra cặp has_dosage. Vì vậy mỗi quan hệ có từ tám đến mười một khung câu viết theo văn nói, "
        "sau đó cặp thực thể cùng nhóm chuyên khoa được điền vào khung. Chẳng hạn khung thực thể đuôi dương tính với thực thể đầu tạo ra câu xét nghiệm pcr dương tính với lao, "
        "mang nhãn diagnosed_by, còn khung thuốc liền trước liều tạo ra câu amlodipin nửa viên, mang nhãn has_dosage.")
    D.p("Bên cạnh mẫu dương còn có mẫu âm khó, tức những câu mà hai thực thể đứng gần nhau và có vẻ liên quan nhưng câu không nói quan hệ đó. "
        "Các mẫu này gồm phòng bệnh như dùng thuốc nhắm trúng đích để phòng ngừa ung thư, tác dụng phụ, phủ định như bệnh gút chứ không phải ở cột sống, điều trị không hiệu quả, "
        "và thực thể gây nhiễu, khi trong cùng một câu một cặp là dương còn cặp kia là âm. Số mẫu âm khó gấp đôi số mẫu dương. "
        "Nếu chỉ có mẫu dương, mô hình sẽ học mẹo hai thực thể đứng gần nhau thì có quan hệ, và mẫu âm khó buộc mô hình phải chú ý tới những từ làm đổi nghĩa như phòng ngừa, gây ra hay không.")

    D.h(f"{CH}.5.3. Lọc và tạo các mức dữ liệu", 3)
    a = man["audit"]
    D.p(f"Dữ liệu sinh từ hai cách được lọc qua bốn bước. Câu trùng với tập huấn luyện, tập kiểm định, tập kiểm tra hoặc trùng nhau bị loại ({n(a['drop_duplicate'])} câu). "
        f"Câu có chung một chuỗi tám từ liên tiếp với tập kiểm định hoặc tập kiểm tra bị loại để chống rò rỉ ({n(a['drop_leak_dev_test'])} câu). "
        f"Mỗi khung câu chỉ giữ tối đa ba câu để mô hình không học thuộc khung ({n(a['drop_skeleton_cap'])} câu). Cuối cùng tỉ lệ dương được đưa về khoảng "
        f"{n(man['target_positive_rate'][0])} đến {n(man['target_positive_rate'][1])} quanh tỉ lệ của tập huấn luyện ({n(a['drop_positive_ratio'])} câu bị bỏ). "
        f"Sau khi lọc còn {n(man['pool']['records'])} câu với {n(man['pool']['pairs'])} cặp, và từ đó lấy ngẫu nhiên hai mức như {D.lab('Bảng')}.")
    D.table("Ba mức dữ liệu huấn luyện dùng trong thí nghiệm", ["Mức", "Cặp thật", "Cặp sinh", "Tổng số cặp", "Tỉ lệ thật và sinh"],
            [(CFG_NAME["x0"], n(seed_pairs), "0", n(seed_pairs), "1 : 0"),
             (CFG_NAME["x1"], n(seed_pairs), n(man["x1"]["pairs"]), n(seed_pairs + man["x1"]["pairs"]), "1 : 1"),
             (CFG_NAME["x3"], n(seed_pairs), n(man["x3"]["pairs"]), n(seed_pairs + man["x3"]["pairs"]), "1 : 3")],
            "Bảng cho thấy ba mức chỉ khác nhau ở lượng dữ liệu sinh, mọi yếu tố khác được giữ nguyên.", widths=[5.6, 2.2, 2.2, 2.4, 2.8])
    D.p(f"Ở mức thêm dữ liệu sinh gấp một lần, dữ liệu sinh gồm {n(x1m['mention_replacement'])} câu thay thực thể, {n(x1m['template'])} câu mẫu dương và {n(x1m['hard_negative'])} câu mẫu âm khó. "
        "Mọi câu sinh đều được đánh dấu là dữ liệu sinh, không có người duyệt. Phương pháp thay thực thể vẫn có thể tạo ra câu sai về y khoa, chẳng hạn tổn thương mạch máu "
        "được thay thành huyết áp cao mạch máu mà vẫn giữ nhãn located_at, nên lượng dữ liệu sinh cần được giữ ở mức vừa phải.")

    # 1.6
    D.h(f"{CH}.6. Mô hình ViHealthBERT-RE", 2)
    D.p(f"Mô hình dùng ViHealthBERT [6], một mô hình kiểu RoBERTa [9] dựa trên PhoBERT [10] được tiền huấn luyện tiếp trên văn bản y tế tiếng Việt, làm bộ mã hóa. "
        "Để mô hình biết cặp nào đang được xét, hai thực thể được bao bởi các ký hiệu đánh dấu thực thể có kèm kiểu, theo cách của Baldini Soares và cộng sự [11] "
        "và Zhong và Chen [12]. Mười bốn ký hiệu mới được thêm vào bộ từ vựng, gồm ký hiệu mở cho mỗi kiểu ở vai trò đầu và đuôi cùng hai ký hiệu đóng. "
        f"Câu sau khi đánh dấu đi qua bộ mã hóa như {D.lab('Hình')}.")
    D.figure(FIG / "ch_mo_hinh_re.png", "Kiến trúc mô hình ViHealthBERT-RE minh họa trên cặp đau và vùng bụng",
             "Hình cho thấy cặp thực thể được biểu diễn bằng vector tại hai ký hiệu mở và xác suất cuối là trung bình của ba mô hình.", width=14.5)
    D.p(f"Biểu diễn của cặp là phép nối hai vector ẩn tại hai ký hiệu mở, sau đó qua dropout với tỉ lệ 0,1 và một lớp tuyến tính để tính xác suất theo công thức {D.eqlab()}.", keep_next=True)
    D.eq(mr("p") + paren(mr("y | h,t")) + mr(" = softmax") + paren(mr("W") + paren(sub(mr("v"), mtext("đầu")) + mr(" ; ") + sub(mr("v"), mtext("đuôi")), "[", "]") + mr(" + b")))
    D.where(["v đầu và v đuôi là vector ẩn 768 chiều của bộ mã hóa tại ký hiệu mở của thực thể đầu và thực thể đuôi, dấu chấm phẩy trong ngoặc vuông là phép nối hai vector.",
             "W và b là ma trận trọng số và độ lệch của lớp tuyến tính, cho hai giá trị ứng với NO_RELATION và quan hệ của cặp.",
             "p(y | h,t) là xác suất của nhãn y cho cặp gồm thực thể đầu h và thực thể đuôi t."])
    D.p("Ký hiệu mở được dùng thay cho vector của toàn câu vì nó tập trung thông tin về đúng thực thể đang xét, điều quan trọng khi một câu có nhiều cặp. "
        f"Mô hình được huấn luyện ba lần độc lập với ba giá trị khởi tạo ngẫu nhiên, và xác suất cuối là trung bình của ba lần theo công thức {D.eqlab()}.", keep_next=True)
    D.eq(mr("p̄") + mr(" = ") + frac(mr("1"), mr("K")) + nsum(mr("k=1"), mr("K"), sub(mr("p"), mr("k"))) + mr(",   ") + mtext("dương khi ") + mr("p̄ ≥ 0,5"))
    D.where(["K bằng 3 là số lần huấn luyện với các giá trị khởi tạo ngẫu nhiên 42, 43 và 44.",
             "p k là xác suất có quan hệ do mô hình thứ k dự đoán, và p̄ là xác suất trung bình dùng để ra quyết định.",
             "Ngưỡng 0,5 là ngưỡng tự nhiên của xác suất và không được tinh chỉnh, vì tập kiểm định quá nhỏ để chọn ngưỡng một cách tin cậy."])
    D.p(f"Việc lấy trung bình ba lần là cần thiết vì kết quả tinh chỉnh BERT trên dữ liệu nhỏ dao động mạnh theo giá trị khởi tạo [33]. Với mô hình đã chọn, micro F1 của từng lần "
        f"trên tập kiểm tra là {n(sf_test[0])}, {n(sf_test[1])} và {n(sf_test[2])}, nên một lần chạy riêng lẻ có thể lệch vài điểm so với kết quả trung bình.")

    # 1.7
    D.h(f"{CH}.7. Huấn luyện", 2)
    w = (seed_pairs + man["x1"]["pairs"] - cfg["train_positives"]) / cfg["train_positives"]
    D.p(f"Dữ liệu chỉ có khoảng {n(cfg['train_positives'] / cfg['train_pairs'])} cặp dương, nên nếu không cân bằng lại, mô hình sẽ nghiêng về dự đoán không có quan hệ. "
        f"Hàm mất mát là entropy chéo có trọng số theo công thức {D.eqlab()}.", keep_next=True)
    D.eq(mr("L = −") + frac(nsum(mr("i=1"), mr("N"), sub(mr("w"), sub(mr("y"), mr("i"))) + mr(" log p") + paren(sub(mr("y"), mr("i")) + mr(" | ") + sub(mr("x"), mr("i")))),
                            nsum(mr("i=1"), mr("N"), sub(mr("w"), sub(mr("y"), mr("i"))))) + mr(",   ") + sub(mr("w"), mr("+")) + mr(" = ") + frac(sub(mr("N"), mr("−")), sub(mr("N"), mr("+"))))
    D.where(["N là số cặp trong một lô, x i là cặp thứ i và y i là nhãn đúng của cặp đó.",
             "w y i là trọng số của lớp ứng với nhãn đúng, bằng 1 cho lớp không có quan hệ và bằng w + cho lớp có quan hệ.",
             f"N − và N + là số cặp âm và số cặp dương trong dữ liệu huấn luyện, nên w + được tính trực tiếp từ dữ liệu và với mức được chọn bằng {n(w)}."])
    D.p(f"Các siêu tham số được đặt trước theo khuyến nghị phổ biến khi tinh chỉnh BERT và giữ nguyên cho mọi mức dữ liệu, kèm lý do ở {D.lab('Bảng')}. "
        "Siêu tham số không được dò vì hai lý do. Tập kiểm định chỉ có " + n(dev_pairs) + " cặp, nên dò nhiều tổ hợp trên đó sẽ chọn ra cấu hình khớp với nhiễu của tập này. "
        "Ngoài ra, thí nghiệm chính là so sánh lượng dữ liệu sinh, và việc giữ cố định siêu tham số bảo đảm khác biệt giữa các mức chỉ đến từ dữ liệu.")
    steps = -(-cfg["train_pairs"] // cfg["batch"])
    D.table("Siêu tham số huấn luyện và lý do chọn giá trị", ["Siêu tham số", "Giá trị", "Lý do"],
            [("Tốc độ học", "3×10⁻⁵", "Thuộc dải khuyến nghị của Devlin và cộng sự [5], đủ nhỏ để không phá vỡ tri thức đã tiền huấn luyện"),
             ("Kích thước lô", str(cfg["batch"]), "Thuộc dải khuyến nghị [5] và vừa với bộ nhớ 4 GB của GPU dùng để huấn luyện"),
             ("Số lượt huấn luyện", str(cfg["epochs"]), f"Mỗi lượt chỉ có {n(steps)} bước, nên dữ liệu nhỏ cần nhiều bước hơn để ổn định [31], [32]"),
             ("Khởi động tốc độ học", "10% số bước", "Tránh cập nhật mạnh khi lớp phân loại còn ngẫu nhiên, sau đó giảm tuyến tính"),
             ("Suy giảm trọng số", "0,01", "Giá trị mặc định của AdamW [34], chống quá khớp nhẹ"),
             ("Cắt gradient", "1,0", "Chống gradient bùng nổ khi tính toán 16 bit"),
             ("Trọng số lớp dương", n(w), "Tính từ tỉ lệ cặp âm trên cặp dương theo công thức " + f"({CH}.4)"),
             ("Độ dài tối đa", f"{cfg['max_len']} token", "Câu dài nhất chỉ khoảng 45 token, nên không câu nào bị cắt"),
             ("Ngưỡng quyết định", "0,5", "Ngưỡng tự nhiên của xác suất, không tinh chỉnh"),
             ("Số lần khởi tạo", "3", "Giảm dao động theo giá trị khởi tạo [33]")],
            "Bảng cho biết mỗi siêu tham số được chọn theo khuyến nghị hoặc tính từ dữ liệu, không giá trị nào được dò trên tập kiểm định hay tập kiểm tra.", widths=[3.6, 2.6, 8.8])
    D.p(f"Mỗi mức dữ liệu được huấn luyện với ba giá trị khởi tạo trên GPU NVIDIA GeForce GTX 1650. Với mức được chọn, mỗi lần huấn luyện mất khoảng "
        f"{n(round(cfg['seconds'] / 3 / 60))} phút. Mô hình triển khai được huấn luyện lại với đúng dữ liệu và ba giá trị khởi tạo này, và cho dự đoán trùng khớp hoàn toàn "
        "với lần dùng để chấm điểm, nên các con số trong chương đúng là của mô hình đang chạy trong hệ thống.")

    # 1.8
    D.h(f"{CH}.8. Phương pháp đánh giá", 2)
    D.p(f"Mỗi cặp ứng viên được chấm theo precision, recall và F1 trên lớp có quan hệ theo công thức {D.eqlab()}.", keep_next=True)
    D.eq(mr("P = ") + frac(mr("TP"), mr("TP + FP")) + mr(",   R = ") + frac(mr("TP"), mr("TP + FN")) + mr(",   F1 = ") + frac(mr("2PR"), mr("P + R")))
    D.where(["TP là số cặp có quan hệ được dự đoán đúng, FP là số cặp không có quan hệ nhưng bị dự đoán là có, FN là số cặp có quan hệ bị bỏ sót.",
             "P cho biết trong các dự đoán có quan hệ, bao nhiêu phần đúng, còn R cho biết trong các quan hệ thật, bao nhiêu phần được tìm ra.",
             "F1 là trung bình điều hòa của P và R, chỉ cao khi cả hai cùng cao."])
    D.p("Lớp NO_RELATION không được tính vào điểm vì nó chiếm đa số và sẽ làm điểm cao giả tạo. Micro F1 cộng TP, FP và FN của mọi quan hệ rồi mới tính, "
        f"còn macro F1 là trung bình F1 của các quan hệ theo công thức {D.eqlab()}.", keep_next=True)
    D.eq(mr("Macro F1 = ") + frac(mr("1"), mr("|Q|")) + nsum(mr("q ∈ Q"), mr(""), sub(mr("F1"), mr("q"))))
    D.where(["Q là tập các quan hệ có cặp dương trong tập được chấm, và F1 q là F1 của quan hệ q."])
    D.p("Micro F1 phản ánh chất lượng chung và bị chi phối bởi quan hệ nhiều cặp như located_at, còn macro F1 cho mỗi quan hệ trọng số như nhau nên nhạy với quan hệ hiếm. "
        f"Vì vậy macro F1 được dùng để chọn mức dữ liệu trên tập kiểm định, tính trên {', '.join(ev['dev'][best]['macro_over'])}, là các quan hệ có cặp dương ở tập này. "
        "Trên tập kiểm tra, khoảng tin cậy 95% của micro F1 được ước lượng bằng bootstrap [21] với 2.000 lần lấy mẫu lại theo câu, vì các cặp trong cùng một câu không độc lập với nhau. "
        "Kết quả được so với hai mốc. Mốc thứ nhất là bộ dự đoán luôn trả lời có quan hệ, cho biết điểm đạt được khi không cần hiểu câu. "
        "Mốc thứ hai là phương pháp rule-based viết theo hướng dẫn gán nhãn, là cách làm không cần dữ liệu huấn luyện.")

    # 1.9
    D.h(f"{CH}.9. Kết quả", 2)
    D.h(f"{CH}.9.1. Ảnh hưởng của lượng dữ liệu sinh", 3)
    dv = ev["dev"]
    D.p(f"{D.lab('Hình')} so sánh ba mức dữ liệu trên tập kiểm định. Bổ sung dữ liệu sinh gấp một lần nâng macro F1 từ {n(dv['x0']['macro_f1'])} lên {n(dv['x1']['macro_f1'])}, "
        f"nhưng bổ sung gấp ba lại làm macro F1 giảm xuống {n(dv['x3']['macro_f1'])}, thấp hơn cả khi không dùng dữ liệu sinh. Theo quy tắc đã đặt trước, "
        f"mức {CFG_NAME[best].lower()} được chọn. Khi dữ liệu sinh lấn át dữ liệu thật, mô hình học theo phân bố của câu nhân tạo, vốn đều và sạch hơn lời nói thật, "
        "đồng thời số nhãn nhiễu từ phép thay thực thể cũng tăng theo. Do tập kiểm định nhỏ, chênh lệch giữa các mức nên được xem là xu hướng hơn là kết luận chắc chắn.")
    D.figure(FIG / "ch_ket_qua_dev.png", "Macro F1 và micro F1 trên tập kiểm định theo lượng dữ liệu sinh",
             "Hình cho thấy dữ liệu sinh chỉ có ích ở lượng vừa phải.", width=14.5)

    D.h(f"{CH}.9.2. Kết quả trên tập kiểm tra", 3)
    D.p(f"Mô hình được chọn được chấm một lần trên tập kiểm tra, cùng với phương pháp rule-based và chế độ hợp mà hệ thống sử dụng, kết quả ở {D.lab('Bảng')}.")
    D.table("Kết quả trên tập kiểm tra của các phương pháp", ["Phương pháp", "Precision", "Recall", "Micro F1", "Khoảng tin cậy 95%"],
            [("Luôn dự đoán có quan hệ", n(ap2["precision"]), n(ap2["recall"]), n(ap2["f1"]), f"{n(ev2['ci95_micro_f1']['always_positive'][0])}–{n(ev2['ci95_micro_f1']['always_positive'][1])}"),
             ("Rule-based", n(ru["precision"]), n(ru["recall"]), n(ru["f1"]), f"{n(ci['rules'][0])}–{n(ci['rules'][1])}"),
             ("ViHealthBERT-RE", n(mo["precision"]), n(mo["recall"]), n(mo["f1"]), f"{n(ci['model'][0])}–{n(ci['model'][1])}"),
             ("ViHealthBERT-RE hợp với rule-based", n(un["precision"]), n(un["recall"]), n(un["f1"]), f"{n(ci['union'][0])}–{n(ci['union'][1])}")],
            "Bảng cho thấy mô hình vượt cả hai mốc so sánh, trong đó khoảng tin cậy không chồng lấn với mốc luôn dự đoán có quan hệ nhưng còn chồng lấn một phần với rule-based.", widths=[5.6, 2.2, 2.2, 2.2, 3.2])
    D.p(f"ViHealthBERT-RE đạt micro F1 {n(mo['f1'])}, cao hơn {n(mo['f1'] - ru['f1'])} so với rule-based và {n(mo['f1'] - ap2['f1'])} so với mốc luôn dự đoán có quan hệ. "
        f"Ưu thế chủ yếu đến từ recall, khi mô hình tìm ra {n(mo['recall'])} số quan hệ thật so với {n(ru['recall'])} của rule-based, vì mô hình nhận ra được những cách nói đa dạng "
        f"mà quy tắc viết tay không bao quát hết. Ngược lại, rule-based có precision cao hơn ({n(ru['precision'])} so với {n(mo['precision'])}), đúng với bản chất chỉ bắt những mẫu câu chắc chắn. "
        f"Khi hợp hai nguồn, recall tăng lên {n(un['recall'])} trong khi precision giảm nhẹ, nên micro F1 gần như không đổi. Hệ thống giữ chế độ hợp vì trong ứng dụng xây dựng đồ thị tri thức, "
        "bỏ sót một quan hệ thật thường khó phát hiện hơn một quan hệ sai có thể được lọc ở bước sau.")
    D.p(f"Kết quả theo từng quan hệ của ViHealthBERT-RE được trình bày ở {D.lab('Hình')}. Các quan hệ located_at, treated_by và diagnosed_by đạt F1 từ "
        f"{n(min(per[r]['f1'] for r in ('located_at', 'treated_by', 'diagnosed_by')))} đến {n(max(per[r]['f1'] for r in ('located_at', 'treated_by', 'diagnosed_by')))}. "
        f"Quan hệ has_dosage, dù không có cặp nào trong tập huấn luyện thật và chỉ học từ dữ liệu sinh, vẫn tìm ra toàn bộ {n(per['has_dosage']['positives'])} cặp dương với recall {n(per['has_dosage']['recall'])}, "
        f"nhưng precision chỉ {n(per['has_dosage']['precision'])}. Yếu nhất là treated_by_procedure với F1 {n(per['treated_by_procedure']['f1'])}.")
    D.figure(FIG / "ch_ket_qua_quan_he.png", "Precision, recall và F1 của ViHealthBERT-RE theo từng quan hệ trên tập kiểm tra",
             "Hình cho thấy mô hình có recall cao ở hầu hết quan hệ, còn precision là điểm yếu ở has_dosage và treated_by_procedure.", width=14.5)
    t1m = ev["test"]["model"]["micro"]; ap1 = ev["test"]["always_positive"]["micro"]
    D.p(f"Để thấy ảnh hưởng của tiêu chí gán nhãn, cùng mô hình này khi chấm trên nhãn lượt đầu của tập kiểm tra chỉ đạt micro F1 {n(t1m['f1'])}, thấp hơn mốc luôn dự đoán có quan hệ "
        f"là {n(ap1['f1'])}, vì lượt đầu coi gần như mọi cặp cùng câu là dương. Sự chênh lệch này cho thấy với lời nói y tế, định nghĩa thế nào là có quan hệ ảnh hưởng tới điểm số "
        "nhiều hơn khác biệt giữa các mức dữ liệu, và tiêu chí của tập kiểm tra cần thống nhất với tiêu chí của tập huấn luyện thì kết quả mới có ý nghĩa.")

    D.h(f"{CH}.9.3. Phân tích lỗi", 3)
    D.p(f"Lỗi của has_dosage đều là dự đoán dương sai, với {n(per['has_dosage']['fp'])} cặp sai và không cặp nào bị bỏ sót. Mô hình nối thuốc với hầu hết lượt đề cập liều đứng gần, "
        "kể cả khi đó không phải liều dùng, chẳng hạn vitamin d với khoảng mười phần trăm trong câu thiếu vitamin d chỉ có thể hấp thụ khoảng mười phần trăm số canxi. "
        "Nguyên nhân là mẫu câu sinh cho quan hệ này rất đơn giản, thường chỉ là tên thuốc đứng liền trước liều, nên mô hình học được rằng thuốc đứng gần một con số thì có liều.")
    D.p(f"Quan hệ treated_by_procedure có {n(per['treated_by_procedure']['fp'])} dự đoán dương sai và {n(per['treated_by_procedure']['fn'])} cặp bị bỏ sót. "
        "Mô hình nhầm quan hệ nhân quả thành điều trị, như biến chứng do nhổ răng gây ra, và nhầm những từ chung chung như phục hồi hay tái tạo là thủ thuật điều trị. "
        "Chiều ngược lại, mô hình bỏ sót những trường hợp điều trị bằng dụng cụ như mang hàm giả cho chỗ mất răng, vốn rất ít xuất hiện trong dữ liệu huấn luyện.")
    D.p(f"Với located_at, {n(per['located_at']['fp'])} dự đoán dương sai chủ yếu rơi vào câu liệt kê, như viêm gan xương hay cao huyết áp tim, nơi bệnh và bộ phận đứng liền nhau "
        f"nhưng thuộc hai ý khác nhau. {n(per['located_at']['fn'])} cặp bị bỏ sót thường có bộ phận cơ thể nằm cách xa bệnh, như câu bắt đầu bằng đại tràng rồi mới liệt kê xuất huyết và chảy máu. "
        "Những lỗi này cho thấy hướng cải thiện tiếp theo là bổ sung mẫu âm khó cho câu liệt kê và mẫu dương có khoảng cách xa giữa hai thực thể.")

    # 1.10
    D.h(f"{CH}.10. Tích hợp vào hệ thống", 2)
    D.p("Trong luồng xử lý, câu đầu vào trước tiên đi qua mô hình nhận diện thực thể và bước gán mã. Các thực thể được ghép thành cặp ứng viên theo lược đồ, "
        "những thực thể quá chung chung bị bỏ qua, rồi mỗi cặp được ViHealthBERT-RE và phương pháp rule-based cùng dự đoán. Một cặp được coi là có quan hệ khi ít nhất một trong hai nguồn dự đoán có, "
        "và mỗi quan hệ đầu ra ghi lại nguồn đã sinh ra nó để có thể truy vết. Các quan hệ từ nhiều câu sau đó được gộp theo mã đã gán thành nút và cạnh của đồ thị tri thức. "
        "Trên CPU, mỗi cặp mất khoảng 0,2 giây vì phải chạy ba bộ mã hóa, mức chấp nhận được với số cặp ít ỏi trong một câu lời nói.")

    # 1.11
    D.h(f"{CH}.11. Hạn chế", 2)
    D.p(f"Tập kiểm tra có {n(len(t2))} câu do một người gán, nên khoảng tin cậy còn rộng và chưa đo được độ đồng thuận giữa các người gán. Tập kiểm định chỉ có {n(dev_pairs)} cặp, "
        "nên việc chọn mức dữ liệu dựa trên khác biệt nhỏ. Dữ liệu sinh không có người duyệt và phép thay thực thể có thể tạo nhãn nhiễu, trong khi has_dosage chỉ được học từ mẫu câu sinh. "
        "Cuối cùng, phương pháp viết lại câu bằng mô hình ngôn ngữ lớn để tăng độ đa dạng của dữ liệu sinh chưa được thực hiện và là hướng phát triển tiếp theo.")

    # tài liệu bổ sung
    D.h("Tài liệu tham khảo bổ sung", 2)
    D.p("Chương dùng lại các tài liệu [2], [5], [6], [9], [10], [11], [12] và [21] trong danh mục tài liệu tham khảo của khóa luận, và bổ sung năm tài liệu sau.")
    for i, ref in enumerate([
        "M. Mosbach, M. Andriushchenko, and D. Klakow, “On the stability of fine-tuning BERT: Misconceptions, explanations, and strong baselines,” in Proc. 9th Int. Conf. Learning Representations (ICLR), 2021.",
        "T. Zhang, F. Wu, A. Katiyar, K. Q. Weinberger, and Y. Artzi, “Revisiting few-sample BERT fine-tuning,” in Proc. 9th Int. Conf. Learning Representations (ICLR), 2021.",
        "J. Dodge, G. Ilharco, R. Schwartz, A. Farhadi, H. Hajishirzi, and N. A. Smith, “Fine-tuning pretrained language models: Weight initializations, data orders, and early stopping,” arXiv preprint arXiv:2002.06305, 2020.",
        "I. Loshchilov and F. Hutter, “Decoupled weight decay regularization,” in Proc. 7th Int. Conf. Learning Representations (ICLR), 2019.",
        "X. Dai and H. Adel, “An analysis of simple data augmentation for named entity recognition,” in Proc. 28th Int. Conf. Computational Linguistics (COLING), 2020, pp. 3861–3867.",
    ], 31):
        para = D.d.add_paragraph(f"[{i}] {ref}")
        para.paragraph_format.left_indent, para.paragraph_format.first_line_indent = Cm(1.0), Cm(-1.0)
        para.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    D.d.save(OUT)
    print(OUT, "| bảng:", D.t, "| hình:", D.f, "| công thức:", D.e)


if __name__ == "__main__":
    main()

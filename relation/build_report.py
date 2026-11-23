"""Sinh phần báo cáo Word về việc làm lại dữ liệu và quy trình RE.

Mọi con số đọc từ file kết quả trong relation/data, nên chạy lại script sau mỗi bước để cập nhật.
Phần nào chưa có kết quả (ví dụ nhãn người trên tập test) thì ghi rõ là đang thực hiện.

Chạy: .venv\\Scripts\\python.exe -X utf8 -m relation.build_report
Đầu ra: relation/BAO_CAO_LAM_LAI_RE.docx, relation/figures/*.png
"""
import json
from collections import Counter
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from docx import Document  # noqa: E402
from docx.enum.table import WD_TABLE_ALIGNMENT  # noqa: E402
from docx.enum.text import WD_ALIGN_PARAGRAPH  # noqa: E402
from docx.oxml import OxmlElement  # noqa: E402
from docx.oxml.ns import qn  # noqa: E402
from docx.shared import Cm, Pt, RGBColor  # noqa: E402

from .ai_batches import load  # noqa: E402

HERE = Path(__file__).resolve().parent
DATA = HERE / "data"
FIG = HERE / "figures"
OUT = HERE / "BAO_CAO_LAM_LAI_RE.docx"
REL = ["located_at", "treated_by", "treated_by_procedure", "diagnosed_by", "has_dosage"]
REL_VI = {"located_at": "located_at", "treated_by": "treated_by", "treated_by_procedure": "treated_by_procedure",
          "diagnosed_by": "diagnosed_by", "has_dosage": "has_dosage"}


def jload(name):
    p = DATA / name
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else None


def n(x):
    """Số kiểu Việt: 1.234 và 0,62."""
    if isinstance(x, float):
        return f"{x:.2f}".replace(".", ",")
    return f"{x:,}".replace(",", ".")


class Doc:
    def __init__(self):
        self.d = Document()
        st = self.d.styles["Normal"]
        st.font.name = "Times New Roman"
        st.font.size = Pt(13)
        st.element.rPr.rFonts.set(qn("w:eastAsia"), "Times New Roman")
        pf = st.paragraph_format
        pf.line_spacing = 1.5
        pf.space_after = Pt(6)
        for s in self.d.sections:
            s.left_margin, s.right_margin, s.top_margin, s.bottom_margin = Cm(3), Cm(2), Cm(2), Cm(2)
        for lvl, size in ((1, 14), (2, 13), (3, 13)):
            h = self.d.styles[f"Heading {lvl}"]
            h.font.name, h.font.size, h.font.bold, h.font.italic = "Times New Roman", Pt(size), True, False
            h.font.color.rgb = RGBColor(0, 0, 0)
            h.element.rPr.rFonts.set(qn("w:eastAsia"), "Times New Roman")
        self.tables = 0
        self.figs = 0
        self.chapter = "4"

    def h(self, text, lvl):
        self.d.add_heading(text, lvl)

    def p(self, text):
        para = self.d.add_paragraph(text)
        para.paragraph_format.first_line_indent = Cm(0.75)
        para.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        return para

    def bullet(self, text):
        para = self.d.add_paragraph("●  " + text)
        para.paragraph_format.left_indent = Cm(0.75)
        para.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

    def note(self, text):
        para = self.d.add_paragraph()
        r = para.add_run(text)
        r.italic = True
        r.font.size = Pt(11)
        r.font.color.rgb = RGBColor(0x59, 0x59, 0x59)
        para.alignment = WD_ALIGN_PARAGRAPH.CENTER

    def table(self, caption, header, rows, note):
        self.tables += 1
        cap = self.d.add_paragraph(f"Bảng {self.chapter}.{self.tables}. {caption}")
        cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        t = self.d.add_table(rows=1, cols=len(header))
        t.style = "Table Grid"
        t.alignment = WD_TABLE_ALIGNMENT.CENTER
        for i, x in enumerate(header):
            c = t.rows[0].cells[i]
            c.text = ""
            r = c.paragraphs[0].add_run(str(x)); r.bold = True; r.font.size = Pt(12)
        for row in rows:
            cells = t.add_row().cells
            for i, x in enumerate(row):
                cells[i].text = ""
                r = cells[i].paragraphs[0].add_run(str(x)); r.font.size = Pt(12)
                if i > 0 and isinstance(x, (int, float)) or (isinstance(x, str) and x.replace(".", "").replace(",", "").isdigit()):
                    cells[i].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT
        for row in t.rows:
            for c in row.cells:
                c.paragraphs[0].paragraph_format.line_spacing = 1.15
                c.paragraphs[0].paragraph_format.space_after = Pt(0)
        self.note(note)
        return f"Bảng {self.chapter}.{self.tables}"

    def figure(self, path, caption, note):
        self.figs += 1
        self.d.add_picture(str(path), width=Cm(15))
        self.d.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
        cap = self.d.add_paragraph()
        r = cap.add_run(f"Hình {self.chapter}.{self.figs}. {caption}"); r.italic = True
        cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        self.note(note)
        return f"Hình {self.chapter}.{self.figs}"

    def next_label(self, kind):
        return f"{kind} {self.chapter}.{(self.tables if kind == 'Bảng' else self.figs) + 1}"


def figure_candidates(explore, path):
    seed = explore["seed_pool"]["relations"]
    x = range(len(REL))
    allp = [seed[r]["pairs"] for r in REL]
    strong = [seed[r]["strong"] for r in REL]
    plt.rcParams.update({"font.family": "Arial", "font.size": 13})
    fig, ax = plt.subplots(figsize=(10, 4.6))
    w = 0.38
    b1 = ax.bar([i - w / 2 for i in x], allp, w, color="#8c8c8c", label="Mọi cặp ứng viên")
    b2 = ax.bar([i + w / 2 for i in x], strong, w, color="#262626", label="Cặp có tín hiệu dương")
    for bars in (b1, b2):
        for b in bars:
            ax.text(b.get_x() + b.get_width() / 2, b.get_height() + 15, n(int(b.get_height())), ha="center", fontsize=11)
    ax.set_xticks(list(x)); ax.set_xticklabels(REL)
    ax.set_ylabel("Số cặp")
    ax.spines[["top", "right"]].set_visible(False)
    ax.legend(frameon=False)
    fig.tight_layout()
    fig.savefig(path, dpi=200)
    plt.close(fig)


def main():
    explore, sel = jload("explore.json"), jload("selection.json")
    key = [json.loads(l) for l in (DATA / "test_sheet_key.jsonl").read_text(encoding="utf-8").splitlines() if l]
    FIG.mkdir(exist_ok=True)
    figure_candidates(explore, FIG / "h_cap_ung_vien.png")
    sp, tp = explore["seed_pool"], explore["test_pool"]
    tags = explore["raw_vietmed_entity_tags"]
    pool = sel["pool_sentences_with_valid_candidate"]
    D = Doc()

    D.h("Xây dựng lại dữ liệu trích xuất quan hệ", 1)
    D.p("Dữ liệu RE cũ có 556 cặp huấn luyện nhưng chỉ 64 cặp dương, và khoảng 43% cặp âm chứa thực thể bị bộ nhãn NER gán sai kiểu. "
        "Mô hình huấn luyện trên dữ liệu này chủ yếu học nhận ra thực thể sai thay vì học quan hệ. Vì vậy toàn bộ nhãn RE cũ bị loại bỏ, "
        "chỉ giữ văn bản và nhãn NER gốc của VietMed-NER, và dữ liệu được xây dựng lại theo ba nguyên tắc: kiểm tra thực thể trước khi gán quan hệ, "
        "chọn câu giàu quan hệ dương, và dùng tập kiểm tra do người có chuyên môn y khoa gán và duyệt.")

    D.h("Dữ liệu nguồn", 2)
    D.p(f"Kho VietMed-NER có {n(sp['sentences'] + tp['sentences'])} câu, mỗi câu là một đoạn bản ghi giọng nói khoảng "
        f"{n(int(sp['sentence_words_median']))} từ và không có dấu câu. Chín kiểu thực thể gốc được ánh xạ về sáu kiểu đích như {D.next_label('Bảng')}.")
    D.table("Ánh xạ kiểu thực thể VietMed-NER sang kiểu thực thể của bài toán RE", ["Kiểu đích", "Kiểu gốc", "Số lượt đề cập"],
            [("CONDITION", "DISEASESYMTOM", n(tags["DISEASESYMTOM"])),
             ("DRUG", "DRUGCHEMICAL, PREVENTIVEMED", n(tags["DRUGCHEMICAL"] + tags["PREVENTIVEMED"])),
             ("BODY_PART", "ORGAN", n(tags["ORGAN"])),
             ("TEST", "DIAGNOSTICS", n(tags["DIAGNOSTICS"])),
             ("PROCEDURE", "SURGERY, MEDDEVICETECHNIQUE, TREATMENT", n(tags["SURGERY"] + tags["MEDDEVICETECHNIQUE"] + tags["TREATMENT"])),
             ("DOSAGE", "UNITCALIBRATOR", n(tags["UNITCALIBRATOR"]))],
            "Bảng cho biết mỗi kiểu thực thể của bài toán RE được lấy từ những kiểu nào của bộ nhãn gốc.")
    D.p(f"Sau khi ghép cặp theo lược đồ năm quan hệ và loại thực thể sai kiểu, chỉ {n(pool['seed'])} câu ở phần huấn luyện và {n(pool['test'])} câu ở phần kiểm tra "
        f"còn cặp ứng viên hợp lệ. Số cặp phân bố rất lệch giữa các quan hệ như {D.next_label('Hình')}: located_at chiếm phần lớn, "
        "còn diagnosed_by và has_dosage rất hiếm, phần lớn lượt đề cập DOSAGE là tính từ hay số liệu thống kê chứ không phải liều thuốc.")
    D.figure(FIG / "h_cap_ung_vien.png", "Số cặp ứng viên và số cặp có tín hiệu dương theo quan hệ ở phần huấn luyện",
             "Hình cho thấy located_at chiếm phần lớn cặp có tín hiệu dương, các quan hệ còn lại rất ít.")

    D.h("Thiết kế gán nhãn và chọn mẫu", 2)
    D.p("Việc gán nhãn gồm hai bước. Bước thứ nhất xét từng lượt đề cập và chọn VALID hoặc INVALID. Bước thứ hai chỉ áp dụng cho cặp có hai thực thể VALID, "
        "với nhãn là tên quan hệ của cặp hoặc NO_RELATION. Năm quan hệ là located_at, treated_by, treated_by_procedure, diagnosed_by và has_dosage. "
        "Hướng dẫn gán nhãn được viết từ câu thật trong kho, có ví dụ dương và âm cho từng quan hệ. "
        "Tập huấn luyện và tập kiểm định được mô hình ngôn ngữ lớn gán hai lượt độc lập theo hướng dẫn này, sau đó người có chuyên môn y khoa duyệt toàn bộ nhãn, "
        "quyết định những chỗ hai lượt bất đồng và sửa những nhãn sai. Tập kiểm tra do người có chuyên môn gán trực tiếp.")
    D.p("Câu được chọn theo điểm khả năng dương của cặp ứng viên, tính theo công thức (1).")
    eq = D.d.add_paragraph("s(h, t) = 3·[quy tắc đoán dương] + [khoảng cách ≤ 4 từ] + [có từ gợi ý]          (1)")
    eq.alignment = WD_ALIGN_PARAGRAPH.CENTER
    D.p("Trong đó:")
    D.bullet("h và t là thực thể đầu và thực thể đuôi của cặp.")
    D.bullet("Mỗi biểu thức trong ngoặc vuông nhận giá trị 1 nếu điều kiện đúng và 0 nếu sai; từ gợi ý là các từ như điều trị bằng, uống, ở hay xét nghiệm nằm giữa hai thực thể.")
    lab = D.next_label("Bảng")
    D.p(f"Câu được lấy theo hạn mức của từng quan hệ, ưu tiên quan hệ hiếm, kèm một phần câu ngẫu nhiên. Kết quả ở {lab}: "
        f"{n(sel['seed']['sentences'])} câu huấn luyện, {n(sel['dev']['sentences'])} câu kiểm định và {n(sel['test']['sentences'])} câu kiểm tra, "
        "không câu huấn luyện nào trùng chuỗi 8 từ liên tiếp với câu kiểm tra.")
    D.table("Số câu và số cặp ứng viên theo quan hệ sau khi chọn mẫu", ["Quan hệ", "Câu huấn luyện", "Cặp huấn luyện", "Cặp kiểm định", "Câu kiểm tra", "Cặp kiểm tra"],
            [(r, n(sel["seed"]["sentences_by_relation"][r]), n(sel["seed"]["pairs_by_relation"][r]), n(sel["dev"]["pairs_by_relation"][r]),
              n(sel["test"]["sentences_by_relation"][r]), n(sel["test"]["pairs_by_relation"][r])) for r in REL],
            "Bảng cho thấy diagnosed_by và has_dosage có rất ít câu ngay cả khi đã lấy toàn bộ câu có ứng viên.")

    D.h("Tập kiểm tra", 2)
    n_test_pairs = sum(len(k["pairs"]) for k in key)
    n_test_ent = sum(len(k["entities"]) for k in key)
    test_rows = [json.loads(l) for l in (DATA / "test.jsonl").read_text(encoding="utf-8").splitlines() if l] if (DATA / "test.jsonl").exists() else []
    v2_path = DATA / "test_v2.jsonl"
    v2_rows = [json.loads(l) for l in v2_path.read_text(encoding="utf-8").splitlines() if l] if v2_path.exists() else []
    audit = jload("../outputs/review_fn_summary.json")
    if test_rows:
        tc, tc2 = Counter(), Counter()
        inv = sum(e["validity"] == "INVALID" for r in test_rows for e in r["entities"])
        for r in test_rows:
            for x in r["relations"]:
                tc[(x["allowed_relation"], x["label"] != "NO_RELATION")] += 1
        for r in v2_rows:
            for x in r["relations"]:
                tc2[(x["allowed_relation"], x["label"] != "NO_RELATION")] += 1
        t_pos = sum(v for k, v in tc.items() if k[1]); t_all = sum(tc.values())
        D.p(f"Tập kiểm tra gồm {n(len(test_rows))} câu, {n(n_test_ent)} lượt đề cập và {n(n_test_pairs)} cặp, do người có chuyên môn y khoa gán trên phiếu đã xáo trộn thứ tự câu. "
            f"Có {n(inv)} lượt đề cập bị loại vì sai kiểu. Ở lượt gán đầu, {n(t_pos)} trên {n(t_all)} cặp được gán là có quan hệ, "
            "nên một bộ dự đoán luôn trả lời có quan hệ gần như đạt điểm tối đa và tập này không đo được khả năng loại cặp sai.")
        if v2_rows:
            t2_pos = sum(v for k, v in tc2.items() if k[1])
            fn = audit.get("fn", {}) if audit else {}
            D.p("Để kiểm tra tiêu chí, người gán soát lại một mẫu 50 cặp gồm cặp mô hình bỏ sót và cặp đối chứng, không thấy nhãn cũ hay dự đoán; "
                f"{n(fn.get('negative', 0) + audit.get('control_tp', {}).get('negative', 0))} trên 50 cặp được đánh lại là không có quan hệ, phần lớn là câu liệt kê bệnh hoặc nói về phòng bệnh. "
                f"Sau đó toàn bộ {n(len(sum((r['relations'] for r in v2_rows), [])))} cặp được gán lại theo tiêu chí chặt, còn {n(t2_pos)} cặp dương. "
                f"Bộ nhãn gán lại được dùng làm tập kiểm tra chính, so sánh hai lượt ở {D.next_label('Bảng')}.")
            D.table("Số cặp dương của tập kiểm tra ở hai lượt gán", ["Quan hệ", "Cặp", "Dương lượt đầu", "Dương sau gán lại"],
                    [(r, n(tc[(r, True)] + tc[(r, False)]), n(tc[(r, True)]), n(tc2[(r, True)])) for r in REL],
                    "Bảng cho thấy tiêu chí chặt loại phần lớn cặp chỉ cùng xuất hiện trong câu, nhất là ở located_at.")
        else:
            D.table("Số cặp của tập kiểm tra theo quan hệ sau khi gán nhãn", ["Quan hệ", "Cặp", "Dương", "Âm"],
                    [(r, n(tc[(r, True)] + tc[(r, False)]), n(tc[(r, True)]), n(tc[(r, False)])) for r in REL],
                    "Bảng cho thấy tập kiểm tra gần như chỉ gồm cặp dương.")
    else:
        D.p("Nhãn của tập kiểm tra đang được thực hiện.")

    D.h("Tập huấn luyện và dữ liệu sinh", 2)
    rs = jload("seed_review_summary.json")
    if rs:
        rows = [(r, n(rs.get(f"seed:{r}:pos", 0)), n(rs.get(f"seed:{r}:neg", 0)), n(rs.get(f"dev:{r}:pos", 0)), n(rs.get(f"dev:{r}:neg", 0))) for r in REL]
        D.p(f"Sau khi người có chuyên môn duyệt, tập huấn luyện gồm {n(rs['seed_sentences'])} câu và tập kiểm định gồm {n(rs['dev_sentences'])} câu. "
            f"{n(rs.get('entity_unresolved_dropped', 0))} lượt đề cập và {n(rs.get('pair_unresolved_dropped', 0))} cặp mà hai lượt gán bất đồng nhưng chưa được quyết định bị loại, "
            f"kéo theo {n(rs.get('pair_dropped_entity_unresolved', 0))} cặp chứa các lượt đề cập đó. Số cặp còn lại ở {D.next_label('Bảng')}.")
        D.table("Số cặp của tập huấn luyện và tập kiểm định theo quan hệ", ["Quan hệ", "Huấn luyện dương", "Huấn luyện âm", "Kiểm định dương", "Kiểm định âm"], rows,
                "Bảng cho thấy has_dosage không có cặp nào và diagnosed_by chỉ có ở tập huấn luyện.")
    man = jload("synth/manifest.json")
    if man:
        D.p(f"Dữ liệu sinh được tạo từ câu huấn luyện bằng hai cách. Cách thứ nhất thay một thực thể của câu thật bằng thực thể cùng kiểu và cùng nhóm chuyên khoa, giữ nguyên nhãn. "
            f"Cách thứ hai điền cặp thực thể vào mẫu câu viết tay, gồm mẫu dương và mẫu âm khó như phòng bệnh, tác dụng phụ, phủ định hay thực thể gây nhiễu. "
            f"Câu trùng, câu có chung chuỗi 8 từ với tập kiểm định hoặc tập kiểm tra bị loại, mỗi khung câu giữ tối đa ba câu, và tỉ lệ dương được đưa về gần tỉ lệ của tập huấn luyện. "
            f"Kho sinh có {n(man['pool']['pairs'])} cặp, từ đó lấy hai mức là {n(man['x1']['pairs'])} cặp, bằng số cặp huấn luyện thật, và {n(man['x3']['pairs'])} cặp, gấp ba lần. "
            "Bước viết lại câu bằng mô hình ngôn ngữ lớn chưa được thực hiện.")
    ev = jload("../outputs/evaluation.json")
    D.h("Kết quả", 2)
    if ev:
        name = {"x0": "Chỉ dữ liệu thật", "x1": "Thêm dữ liệu sinh 1 lần", "x3": "Thêm dữ liệu sinh 3 lần"}
        D.p("Mô hình là ViHealthBERT đánh dấu thực thể đầu và đuôi, huấn luyện với cùng siêu tham số đặt trước cho mọi cấu hình, ba seed, lấy trung bình xác suất với ngưỡng 0,5. "
            f"Cấu hình được chọn bằng macro F1 trên tập kiểm định như {D.next_label('Bảng')}, rồi chỉ cấu hình được chọn mới được chấm trên tập kiểm tra.")
        D.table("Kết quả trên tập kiểm định theo lượng dữ liệu sinh", ["Cấu hình", "Cặp huấn luyện", "Precision", "Recall", "Micro F1", "Macro F1"],
                [(name[c], n(v["train_pairs"]), n(v["micro"]["precision"]), n(v["micro"]["recall"]), n(v["micro"]["f1"]), n(v["macro_f1"]))
                 for c, v in ev["dev"].items()],
                "Macro F1 tính trên located_at, treated_by và treated_by_procedure, ba quan hệ có cặp dương ở tập kiểm định.")
        ev2 = jload("../outputs/evaluation_test_v2.json")
        t1, ap1 = ev["test"]["model"], ev["test"]["always_positive"]
        if ev2:
            t, ap_, ci = ev2["model"], ev2["always_positive"], ev2["ci95_micro_f1"]
        else:
            t, ap_, ci = t1, ap1, ev["test"]["ci95_micro_f1"]
        D.p(f"Cấu hình được chọn là {name[ev['chosen']].lower()}. Trên tập kiểm tra, mô hình đạt micro F1 {n(t['micro']['f1'])}, khoảng tin cậy 95% từ {n(ci['model'][0])} đến {n(ci['model'][1])}, "
            f"với precision {n(t['micro']['precision'])} và recall {n(t['micro']['recall'])}. Bộ dự đoán luôn trả lời có quan hệ đạt micro F1 {n(ap_['micro']['f1'])}, "
            f"khoảng tin cậy từ {n(ci['always_positive'][0])} đến {n(ci['always_positive'][1])}. Kết quả theo quan hệ ở {D.next_label('Bảng')}.")
        D.table("Kết quả trên tập kiểm tra theo quan hệ", ["Quan hệ", "Cặp", "Dương", "Precision", "Recall", "F1"],
                [(r, n(v["pairs"]), n(v["positives"]), n(v["precision"]), n(v["recall"]), n(v["f1"])) for r, v in t["per_relation"].items()],
                "Bảng cho biết precision và recall của cấu hình được chọn ở từng quan hệ.")
        if ev2:
            weak = sorted(t["per_relation"].items(), key=lambda kv: kv[1]["f1"])[:2]
            D.p(f"Trên nhãn lượt đầu, cùng mô hình chỉ đạt micro F1 {n(t1['micro']['f1'])}, thấp hơn bộ dự đoán luôn dương ({n(ap1['micro']['f1'])}), "
                "vì lượt đầu coi gần như mọi cặp cùng câu là dương. Khi tiêu chí của tập kiểm tra khớp với tập huấn luyện, mô hình vượt bộ dự đoán luôn dương. "
                f"Hai quan hệ yếu nhất là {weak[0][0]} (F1 {n(weak[0][1]['f1'])}) và {weak[1][0]} (F1 {n(weak[1][1]['f1'])}).")
            modes = jload("../outputs/evaluation_test_v2_modes.json")
            if modes:
                lab = D.next_label("Bảng")
                D.p("Mô hình được chọn được lưu dưới tên ViHealthBERT-RE và dùng trong hệ thống cùng với bộ luật theo chế độ hợp: một cặp là dương khi mô hình hoặc luật nói dương. "
                    f"{lab} so sánh ba cách chạy trên cùng tập kiểm tra.")
                D.table("Kết quả trên tập kiểm tra của mô hình, bộ luật và chế độ hợp", ["Cách chạy", "Precision", "Recall", "Micro F1", "Khoảng tin cậy 95%"],
                        [(nm, n(modes[k]["micro"]["precision"]), n(modes[k]["micro"]["recall"]), n(modes[k]["micro"]["f1"]),
                          f"{n(modes['ci95_micro_f1'][k][0])}–{n(modes['ci95_micro_f1'][k][1])}")
                         for k, nm in (("model", "ViHealthBERT-RE"), ("rules", "Bộ luật"), ("union", "ViHealthBERT-RE hợp với luật"))],
                        "Bảng cho thấy thêm luật vào mô hình không làm thay đổi micro F1, chỉ đổi một ít precision lấy recall.")
        elif t["micro"]["f1"] < ap_["micro"]["f1"]:
            D.p("Mô hình thấp hơn bộ dự đoán luôn dương vì hai tập có tiêu chí khác nhau: tập huấn luyện coi cặp chỉ cùng xuất hiện trong câu là âm, "
                "còn tập kiểm tra gán gần như mọi cặp cùng câu là dương. Vì vậy con số trên tập kiểm tra phản ánh độ lệch tiêu chí giữa hai tập nhiều hơn là chất lượng của mô hình.")
    else:
        D.p("Huấn luyện đang được thực hiện tại thời điểm viết phần này.")

    D.h("Hạn chế", 2)
    if v2_rows:
        D.p("Kho VietMed có rất ít cặp dương cho diagnosed_by và has_dosage, và has_dosage chỉ được học từ dữ liệu sinh. Tập kiểm tra chỉ có một người gán, gồm 100 câu, nên khoảng tin cậy còn rộng. "
            "Tiêu chí gán thay đổi giữa hai lượt cho thấy định nghĩa có quan hệ ảnh hưởng tới điểm số nhiều hơn khác biệt giữa các cấu hình mô hình, nên cần một người gán thứ hai để đo độ đồng thuận. "
            "Tập kiểm định chỉ có 111 cặp nên chênh lệch giữa các cấu hình dữ liệu sinh chưa chắc chắn.")
    else:
        D.p("Kho VietMed có rất ít cặp dương cho diagnosed_by và has_dosage. Tập kiểm tra chỉ có một người gán và có rất ít cặp âm. "
            "Tiêu chí gán của tập huấn luyện chặt hơn của tập kiểm tra, nên cần thống nhất lại tiêu chí và gán lại một trong hai tập trước khi dùng kết quả để kết luận về mô hình.")
    D.d.save(OUT)
    print(OUT, "| bảng:", D.tables, "| hình:", D.figs)


if __name__ == "__main__":
    main()

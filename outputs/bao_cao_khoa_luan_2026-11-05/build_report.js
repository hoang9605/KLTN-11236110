// Sinh báo cáo khóa luận (Word). Mọi số liệu đọc trực tiếp từ tệp kết quả trong repo.
const fs = require("fs");
const path = require("path");
const {
  Document, Packer, Paragraph, TextRun, HeadingLevel, AlignmentType, Table, TableRow, TableCell,
  WidthType, ShadingType, BorderStyle, LevelFormat, TableOfContents, Footer, PageNumber, PageBreak,
  ImageRun, HighlightColor,
} = require("docx");

const ROOT = process.argv[2];
const OUT = process.argv[3];
const NER_DIR = process.argv[4]; // thư mục kết quả NER chạy lại
const J = (p) => JSON.parse(fs.readFileSync(path.join(ROOT, p), "utf8"));
const exists = (p) => fs.existsSync(path.join(ROOT, p));

// ---------- số liệu ----------
const nerNew = { t1: J(`${NER_DIR}/raw_37label_report.json`), t2: J(`${NER_DIR}/schema_6label_report.json`), lat: J(`${NER_DIR}/latency_report.json`) };
const nerOld = { t1: J("eval/results/raw_37label_report.json"), t2: J("eval/results/schema_6label_report.json"), lat: J("eval/results/latency_report.json") };
const gold = J("data/re_gold_v1/manifest.json");
const reGold = J("outputs/re_gold_v1_baseline/compare/report.json");
const reGoldRun = J("outputs/re_gold_v1_baseline/seed42/report.json");
const reAi = J("outputs/re_baselines/report.json");
const gt = J("data/golden_test/v1/manifest.json");
const icd = J("outputs/bao_cao_khoa_luan_2026-11-05/icd10_check.json");
const reviewStats = J("outputs/vietmed_600_RE_review/review_2026_10_15/stats.json");
const trainArgs = J("docs/ner_training_args.json");
const demoOld = J("outputs/re_ai_baseline/seed42/demo_ner_re.json");
const demo = J("outputs/re_gold_v1_baseline/demo_ner_re.json");
const X = J("outputs/bao_cao_khoa_luan_2026-11-05/extra.json");
const icdBefore = J("outputs/bao_cao_khoa_luan_2026-11-05/icd10_check_before_fix.json");
const ABL_DIR = "eval/ablation_2026-11-06";
const abl = exists(`${ABL_DIR}/summary.json`) ? J(`${ABL_DIR}/summary.json`) : null;
const modelCfg = J("Model/vihealthbert-ner-vietmed-v2-final/config.json");
// Bổ sung 07/11/2026: tập gold chuẩn hóa, RE v2, knowledge graph (đều là nhãn AI, chưa bác sĩ duyệt)
const NORM_DIR = "eval/normalization_2026-11-07";
const normA = { dev: J(`${NORM_DIR}/dev_after/report.json`), test: J(`${NORM_DIR}/test_after/report.json`) };
const normB = { dev: J(`${NORM_DIR}/dev_before/report.json`), test: J(`${NORM_DIR}/test_before/report.json`) };
const normMan = J("data/norm_gold_v1/manifest.json");
const re2 = J("outputs/re_ai_v2/report.json");
const KG_DIR = "outputs/kg_test_2026-11-07";
const kg = J(`${KG_DIR}/kg.json`);
const kgS = kg.stats;
const normPred = fs.readFileSync(path.join(ROOT, `${NORM_DIR}/test_after/predictions.jsonl`), "utf8").split(/\r?\n/).filter((l) => l.trim()).map((l) => JSON.parse(l));
const icdMiss = normPred.filter((r) => r.ontology === "ICD-10" && !r.nil && r.pred.system === null);
const icdMissTop = icdMiss.filter((r) => r.candidates.some((c) => r.gold_codes.includes(c))).length;
const nc = (onto, split = "test", which = normA, level = "code") => which[split].results[onto][level].type;
const ncm = (onto, split = "test", which = normA) => which[split].results[onto].code.mention;
const nci = (onto, key, split = "test", which = normA, level = "code") => which[split].results[onto][level].ci95_type[key];
const ci = (a) => `${rp(a[0])}–${rp(a[1])}`;
const RM = { rules: "Luật (baseline)", model_v1: "Mô hình v1 (chỉ gold v1)", model_v2: "Mô hình v2 (gold v1 + AI v2)", hybrid: "Mô hình v2, luật cho quan hệ chưa học", union: "Mô hình v2 ∪ luật (chọn theo CV)" };
const re2pm = (part, m) => re2[part][m].positive_micro;
const re2u = re2pm("golden_test", "union"), re2v1 = re2pm("golden_test", "model_v1"), re2cvu = re2pm("cv5", "union");
const re2lab = re2.data.labels_v2;
const re2pos = Object.entries(re2lab).filter(([k]) => k !== "NO_RELATION").reduce((a, [, v]) => a + v, 0);
const gtLab = re2.data.labels_golden_test;
const gtPos = Object.entries(gtLab).filter(([k]) => k !== "NO_RELATION").reduce((a, [, v]) => a + v, 0);
const kgRel = (k) => kg.edges.filter((e) => e.relation === k);
const kgName = Object.fromEntries(kg.nodes.map((x) => [x.key, x.name]));
// Bổ sung 08/11/2026: baseline RE/NER, tập test ngẫu nhiên, golden test v1.1, đồng thuận nhãn
const agree = J("outputs/re_ai_v2/agreement.json");
const rtMan = J("data/re_test_random_v1/manifest.json");
const gtChanges = fs.readFileSync(path.join(ROOT, "data/golden_test/v1/ai_labels_v1_1_changes.csv"), "utf8").replace(/^﻿/, "")
  .split(/\r?\n/).slice(1).filter((l) => l.trim()).map((l) => { const m = l.match(/^([^,]*),([^,]*),([^,]*),([^,]*),(.*)$/); return { id: m[1], rel: m[2], before: m[3], after: m[4], reason: m[5].replace(/^"|"$/g, "").replace(/""/g, "\"") }; });
const BENCH_DIR = "outputs/re_benchmark_2026-11-08";
const bench = J(`${BENCH_DIR}/benchmark.json`);
const hasBert = !!bench.cv5.bert;
const bp = (part, m) => bench[part][m].positive_micro;
const bci = (part, m) => ci(bench[part][m].positive_micro_f1_ci95);
const BM = Object.keys(bench.names).filter((m) => bench.cv5[m]);
const rtLab = bench.data.random_test_labels;
const rtPos = Object.entries(rtLab).filter(([k]) => k !== "NO_RELATION").reduce((a, [, v]) => a + v, 0);
const NERB_DIR = "eval/ner_baselines_2026-11-08";
const nerBase = exists(`${NERB_DIR}/baselines.json`) ? J(`${NERB_DIR}/baselines.json`) : null;
const nerInh = exists(`${NERB_DIR}/inherited_checkpoint.json`) ? J(`${NERB_DIR}/inherited_checkpoint.json`) : null;
const nerSelf = exists("eval/ner_selftrained_2026-11-08/run_vihealthbert-base-syllable.json") ? J("eval/ner_selftrained_2026-11-08/run_vihealthbert-base-syllable.json") : null;
const nTests = X.tests.length;
const LABELS6 = ["CONDITION", "DRUG", "BODY_PART", "TEST", "PROCEDURE", "DOSAGE"];
const RELS = ["located_at", "treated_by", "treated_by_procedure", "diagnosed_by", "has_dosage"];
const nTypes = Object.keys(nerNew.t1).filter((k) => !k.endsWith("avg")).length;

const f = (x, d = 4) => (x === undefined || x === null ? "—" : Number(x).toFixed(d).replace(".", ","));
const pct = (x, d = 1) => (100 * x).toFixed(d).replace(".", ",") + "%";
const n = (x) => Number(x).toLocaleString("de-DE"); // 3.497
const relCount = (obj, k) => (obj && obj[k]) || 0;
const rp = (x) => f(x, 3);

// ---------- định dạng ----------
const FONT = "Times New Roman";
const BODY = 26; // 13pt
const CONTENT_W = 11906 - 1701 - 1134; // A4, lề trái 3 cm, lề phải 2 cm
const PYTEST = process.env.PYTEST_SUMMARY || "[[Chưa có kết quả pytest]]";
const border = { style: BorderStyle.SINGLE, size: 4, color: "999999" };
const borders = { top: border, bottom: border, left: border, right: border };

function runs(text, base = {}) {
  const parts = String(text).split(/(\*\*[^*]+\*\*|\[\[[^\]]+\]\]|`[^`]+`)/).filter((s) => s !== "");
  return parts.map((s) => {
    if (s.startsWith("**")) return new TextRun({ text: s.slice(2, -2), bold: true, font: FONT, ...base });
    if (s.startsWith("[[")) return new TextRun({ text: s.slice(2, -2), shading: { fill: "FFFF00", type: ShadingType.CLEAR, color: "auto" }, font: FONT, ...base });
    if (s.startsWith("`")) return new TextRun({ text: s.slice(1, -1), font: "Consolas", size: (base.size || BODY) - 4 });
    return new TextRun({ text: s, font: FONT, ...base });
  });
}
const P = (t, o = {}) => new Paragraph({ children: runs(t, o.run || {}), alignment: o.align || AlignmentType.JUSTIFIED, spacing: { after: 120, line: 312 }, indent: o.noIndent ? undefined : { firstLine: 567 }, ...(o.p || {}) });
const PN = (t, o = {}) => P(t, { ...o, noIndent: true });
const H1 = (t) => new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun({ text: t, font: FONT })], pageBreakBefore: true });
const H2 = (t) => new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun({ text: t, font: FONT })] });
const H3 = (t) => new Paragraph({ heading: HeadingLevel.HEADING_3, children: [new TextRun({ text: t, font: FONT })] });
const B = (t, lvl = 0) => new Paragraph({ numbering: { reference: "bullets", level: lvl }, children: runs(t), alignment: AlignmentType.JUSTIFIED, spacing: { after: 60, line: 300 } });
const NUM = (t, ref = "num1") => new Paragraph({ numbering: { reference: ref, level: 0 }, children: runs(t), alignment: AlignmentType.JUSTIFIED, spacing: { after: 60, line: 300 } });
const CAP = (t) => new Paragraph({ children: runs(t, { italics: true, size: 24 }), alignment: AlignmentType.CENTER, spacing: { before: 60, after: 200 } });
const NOTE = (t) => new Paragraph({ children: runs(t, { size: 24 }), shading: { fill: "EEF3F8", type: ShadingType.CLEAR, color: "auto" }, border: { left: { style: BorderStyle.SINGLE, size: 18, color: "2E5A88", space: 6 } }, spacing: { before: 120, after: 160, line: 288 }, indent: { left: 200, right: 200 } });
const CODE = (lines) => lines.map((l, i) => new Paragraph({ children: [new TextRun({ text: l, font: "Consolas", size: 19 })], shading: { fill: "F4F4F4", type: ShadingType.CLEAR, color: "auto" }, spacing: { before: i === 0 ? 80 : 0, after: i === lines.length - 1 ? 160 : 0, line: 240 }, indent: { left: 200 } }));

function T(headers, rows, widths0, opt = {}) {
  const raw = widths0.reduce((a, b) => a + b, 0);
  const widths = widths0.map((w) => Math.floor((w * CONTENT_W) / raw));
  widths[widths.length - 1] += CONTENT_W - widths.reduce((a, b) => a + b, 0);
  const total = CONTENT_W;
  const cell = (txt, i, head) => new TableCell({
    borders, width: { size: widths[i], type: WidthType.DXA },
    shading: head ? { fill: "D9E2F3", type: ShadingType.CLEAR, color: "auto" } : undefined,
    margins: { top: 50, bottom: 50, left: 90, right: 90 },
    children: [new Paragraph({ children: runs(String(txt), { size: opt.size || 22, bold: !!head }), alignment: (!head && opt.right && opt.right.includes(i)) ? AlignmentType.RIGHT : AlignmentType.LEFT })],
  });
  return new Table({
    width: { size: total, type: WidthType.DXA }, columnWidths: widths,
    rows: [new TableRow({ tableHeader: true, children: headers.map((h, i) => cell(h, i, true)) }),
      ...rows.map((r) => new TableRow({ children: r.map((c, i) => cell(c, i, false)) }))],
  });
}

// ---------- nội dung (bản mở rộng 06/11/2026) ----------
const s = nerNew.t2.strict_exact_match, r = nerNew.t2.relaxed_overlap_match;
const so = nerOld.t2.strict_exact_match, ro = nerOld.t2.relaxed_overlap_match;
const t1 = nerNew.t1;
const sameNer = Math.abs(s["micro avg"]["f1-score"] - so["micro avg"]["f1-score"]) < 1e-9;
const cvL = reGold.cv5_grouped.logreg, cvR = reGold.cv5_grouped.rules;
const cvLa = reAi.cv5_grouped.logreg, cvRa = reAi.cv5_grouped.rules;
const ga = gold.after.relations, gb = gold.before.relations;
const posAfter = RELS.reduce((a, k) => a + relCount(ga, k), 0);
const posBefore = RELS.reduce((a, k) => a + relCount(gb, k), 0);
const sp = reGoldRun.splits;
const removedGeneric = Object.entries(gold.removed_generic_entities).sort((a, b) => b[1] - a[1]);
const removedTotal = removedGeneric.reduce((a, [, v]) => a + v, 0);
const icdOk = icd.coded_mentions - icd.wrong_mentions - icd.doubt_mentions;
const icdBeforeOk = icdBefore.coded_mentions - icdBefore.wrong_mentions - icdBefore.doubt_mentions;
const posSplit = (k) => RELS.reduce((a, x) => a + (sp[k].labels[x] || 0), 0);
const S6 = X.s600;
const REFS = [];
let refCounter = 0;
const newList = () => { const id = "nl" + (++refCounter); REFS.push(id); return id; };
const REFLIST = (items) => { REFS.push("refs"); return items.map((t) => NUM(t, "refs")); };
const LIST = (items) => { const id = newList(); return items.map((t) => NUM(t, id)); };
const MATH = (t) => new Paragraph({ children: runs(t, { italics: true }), alignment: AlignmentType.CENTER, spacing: { before: 80, after: 120 } });
// rp được khai báo sớm hơn (dùng ở phần số liệu)
const SUM = (t) => new Paragraph({ children: [new TextRun({ text: "Tóm lược. ", bold: true, font: FONT, size: 25 }), ...runs(t, { size: 25 })], shading: { fill: "F2F5F9", type: ShadingType.CLEAR, color: "auto" }, border: { top: { style: BorderStyle.SINGLE, size: 6, color: "2E5A88", space: 4 }, bottom: { style: BorderStyle.SINGLE, size: 6, color: "2E5A88", space: 4 } }, spacing: { before: 120, after: 240, line: 300 }, alignment: AlignmentType.JUSTIFIED });

const A = [
  ["A1", "Kết quả NER cũ (17/09) chạy trước khi thêm Luật 1b (01/11)", "Ngày tệp eval/results; git log ner/config.py", "Số NER có thể không khớp mã hiện tại", sameNer ? "Đã chạy lại 05/11: kết quả không đổi" : "Đã chạy lại 05/11; dùng số mới"],
  ["A2", "Tài liệu ghi “37 loại nhãn”, thực tế là 37 nhãn BIO của 18 loại", "raw_37label_report.json có 18 loại", "Mô tả sai trong luận văn", "Báo cáo dùng “18 loại, 37 nhãn BIO”"],
  ["A3", "PROJECT_OVERVIEW.md ghi RE “chưa thực hiện”", "Có module relation_extraction/", "Tài liệu lỗi thời", "Cần cập nhật PROJECT_OVERVIEW.md"],
  ["A4", "relation_extraction/README.md báo số trên nhãn AI (178 cặp)", `Gold v1: ${reGold.pairs} cặp`, "Dễ trích nhầm số cũ", "Dùng số gold v1 (Chương 5)"],
  ["A5", "Tiêu đề re_compare_baselines.py ghi cứng “nhãn AI, 178 cặp”", "scripts/re_compare_baselines.py", "Báo cáo sai nguồn nhãn", "Đã sửa 05/11: đọc nguồn và số cặp từ dữ liệu"],
  ["A6", "NER sinh thực thể chung (“điều trị”, “thuốc”) mà gold RE đã xóa", "Demo cũ nối “đau” → “điều trị”", "Lệch phân phối train/inference cho RE", "Đã sửa 06/11: lọc ở đầu vào RE, có kiểm thử"],
  ["A7", "ICD-10 fuzzy gán mã sai (huyết áp cao → Z01.3 …)", "Bảng 5.10", `${icdBefore.wrong_mentions} mention sai trên gold v1`, `Đã sửa 06/11: 2 ràng buộc + 6 alias; còn ${icd.wrong_mentions} sai`],
  ["A8", "Thông tin người duyệt gold v1 là giá trị tạm", `manifest: ${gold.reviewer}`, "Không chứng minh được việc duyệt", "Cần điền tên/ngày thật"],
  ["A9", "Golden test chưa được bác sĩ duyệt", "Chỉ có ai_labels.jsonl (AI tiền gán), chưa có gold.jsonl", "Kết quả RE trên golden test là tạm thời", "07/11: có kết quả trên nhãn AI (5.4.3); cần duyệt"],
  ["A10", "Bộ RE lấy từ split train của NER", "source_split = train", "Không dùng làm test độc lập", "Đã ghi ở 6.6"],
  ["A11", `Dev/test RE quá nhỏ (${posSplit("dev")}/${posSplit("test")} cặp dương)`, "Bảng 5.17", "F1 một lần chia không tin cậy", "Báo cáo kèm CV và CI95"],
  ["A12", "summary.md cũ khẳng định “đảm bảo không data leakage”", "eval/run_eval.py", "Phát biểu quá mạnh", "Viết lại thành mức độ đã kiểm soát (6.6)"],
  ["A13", "Điểm benchmark Bảng 2.3 chép từ tài liệu nội bộ", "docs/BAO_CAO_RE_2026-10-02.md", "Có thể sai lệch", "Cần đối chiếu bài báo gốc"],
  ["A14", "Danh sách thực thể chung cụ thể do người soát đề xuất", "relation_extraction/data.py", "Quyết định gán nhãn", "Người duyệt cần xác nhận danh sách"],
  ["A15", "Không rõ checkpoint NER được chọn trên validation hay test", "training_args.bin: eval_strategy=epoch, không ghi tập", "Có thể làm NER F1 trên test lạc quan", "08/11: baseline chỉ học train cũng tụt validation→test như checkpoint; chênh lệch do validation gần train (5.2.5). Vẫn chưa rõ tập chọn checkpoint"],
  ["A16", "Quy ước CONDITION chung chung chưa được hỏi", "manifest.conventions.generic_condition", "“bệnh”, “biến chứng” vẫn tham gia cặp", "Cần chốt với GVHD"],
  ["A17", "MAX_SUBTOKENS_PER_CHUNK = 200 được import nhưng không dùng", "ner/config.py, ner/preprocessor.py", "Văn bản dài có thể bị cắt ở 258 subtoken", "Chưa sửa; ghi ở 4.2"],
  ["A18", "“\\n” trong tập kết thúc câu nhưng bộ tách token bỏ khoảng trắng", "ner/preprocessor.py", "Xuống dòng không tách câu", "Chưa sửa; ghi ở 4.2"],
  ["A19", "Alias ICD-10 mới rút ra từ chính bộ đo", "Mục 5.3.2", "Kết quả sau sửa lạc quan", "07/11: đã có tập gold dev/test riêng (5.3.3)"],
  ["A20", "Golden test chưa áp quy ước xóa thực thể chung", "data/golden_test/v1/", "Hai bộ không nhất quán", "07/11: nhãn AI tiền gán đã xóa thực thể chung (verdict XOA)"],
  ["A21", "Tập gold chuẩn hóa dev/test do AI gán", "data/norm_gold_v1, human_verified = false", "Accuracy/Top-k là tạm thời", "Cần bác sĩ duyệt phiếu Excel rồi chạy lại"],
  ["A22", "Bộ RE v2 (199 câu) do AI gán, hai lượt", "data/re_ai_v2, human_verified = false", "Mô hình RE v2 học từ nhãn chưa duyệt", "Ghi rõ nguồn nhãn; cần duyệt"],
  ["A23", "RE v2 và nhãn golden test cùng do AI gán", "Cùng một người gán (AI) và cùng hướng dẫn", "Sai lệch có hệ thống của người gán không bị phát hiện", "Ghi là hạn chế (6.7); chỉ người duyệt độc lập mới loại được"],
  ["A24", "Từ điển chuẩn hóa thêm 137 alias từ train/dev", "normalization/data/icd10_synonyms.json", "Kết quả dev lạc quan", "Chỉ báo cáo test; test không dùng để chọn alias"],
  ["A26", "Golden test bị làm giàu cặp dương (lấy mẫu theo hạn mức)", "Baseline “mọi cặp dương” đạt F1 cao hơn mô hình", "F1 golden test không so được với dữ liệu tự nhiên", "08/11: thêm tập test ngẫu nhiên; báo cáo kèm baseline (5.4.3)"],
  ["A27", "Nhãn golden test lệch quy ước gold v1", "17 cặp (vitamin d → cao, “thuốc” chung chung…)", "Chấm mô hình theo quy ước khác lúc học", "08/11: bản v1.1, giữ bản gốc, báo cáo cả hai"],
  ["A28", "Mô hình RE tốt nhất chưa vào pipeline/KG", "KG dùng TF-IDF ∪ luật", "Đồ thị kém hơn khả năng hiện có", "Ghi ở 7.3; cần lưu mô hình BERT"],
  ["A25", "KG chứa cạnh sai và nút là mảnh NER", "kg.html, ví dụ “mất răng → xương”", "Đồ thị chưa dùng làm tri thức tin cậy", "Ghi rõ ở 5.6; mỗi cạnh giữ câu nguồn và nguồn dự đoán"],
];

const C = [];
const add = (...xs) => xs.flat().forEach((x) => C.push(x));

// ===== Trang bìa, mục lục =====
add(
  new Paragraph({ children: runs("[[TÊN TRƯỜNG]]", { size: 28, bold: true }), alignment: AlignmentType.CENTER, spacing: { before: 600 } }),
  new Paragraph({ children: runs("[[TÊN KHOA]]", { size: 28, bold: true }), alignment: AlignmentType.CENTER, spacing: { after: 1600 } }),
  new Paragraph({ children: runs("BÁO CÁO KHÓA LUẬN TỐT NGHIỆP", { size: 32, bold: true }), alignment: AlignmentType.CENTER, spacing: { after: 400 } }),
  new Paragraph({ children: runs("HỆ THỐNG TRÍCH XUẤT THỰC THỂ, QUAN HỆ VÀ CHUẨN HÓA THÔNG TIN Y TẾ TỪ VĂN BẢN TIẾNG VIỆT", { size: 36, bold: true }), alignment: AlignmentType.CENTER, spacing: { after: 1600 } }),
  new Paragraph({ children: runs("Sinh viên thực hiện: [[Họ và tên — MSSV]]", { size: 26 }), alignment: AlignmentType.CENTER }),
  new Paragraph({ children: runs("Giảng viên hướng dẫn: [[Học hàm, họ và tên]]", { size: 26 }), alignment: AlignmentType.CENTER }),
  new Paragraph({ children: runs("Phiên bản báo cáo: 07/11/2026", { size: 26 }), alignment: AlignmentType.CENTER, spacing: { after: 1200 } }),
  new Paragraph({ children: runs("[[Thành phố]], tháng 11 năm 2026", { size: 26, italics: true }), alignment: AlignmentType.CENTER }),
  new Paragraph({ children: [new PageBreak()] }),
  new Paragraph({ children: runs("MỤC LỤC", { size: 30, bold: true }), alignment: AlignmentType.CENTER, spacing: { after: 200 } }),
  new TableOfContents("Mục lục", { hyperlink: true, headingStyleRange: "1-3" }),
  NOTE("Mục lục được Word tạo tự động. Nếu chưa hiện, nhấp chuột phải vào mục lục và chọn **Update Field** → **Update entire table**."),
);

// ===== Kết luận chính (đặt trước để người đọc nắm ngay) =====
const LEAD = (t) => P(t, { p: { spacing: { after: 160, line: 312 } } });
add(
  H1("KẾT LUẬN CHÍNH"),
  P("Tài liệu này viết theo lối tường thuật: nêu kết luận trước, sau đó là bằng chứng. Sáu kết luận dưới đây tóm tắt toàn bộ khóa luận; mỗi kết luận dẫn tới chương có số liệu chi tiết."),
  LEAD(`**Một. Hệ thống chạy được từ đầu đến cuối, từ văn bản tới đồ thị tri thức.** Pipeline nhận văn bản tiếng Việt, trả về thực thể có vị trí ký tự, mã ICD-10/RxNorm kèm danh sách ${"top-k"} ứng viên, quan hệ, và gộp tất cả thành một knowledge graph. Trên ${n(nerNew.lat.total_samples)} câu test của VietMed-NER, NER đạt strict micro-F1 ${f(s["micro avg"]["f1-score"])} và relaxed ${f(r["micro avg"]["f1-score"])}; lần chạy lại ngày 05/11/2026 trùng khớp tuyệt đối với lần chạy ngày 17/09/2026.${nerBase && nerInh ? ` Phần mô hình vượt hai baseline NER tự huấn luyện (từ điển ${f(nerBase.dictionary.test.target.micro.f1, 3)}, CRF ${f(nerBase.crf.test.target.micro.f1, 3)}, ViHealthBERT ${f(nerInh.scores.test.target.micro.f1, 3)} trên sáu loại).` : ""} Đồ thị dựng từ chính tập test có ${n(kgS.nodes)} nút và ${kgS.edges} cạnh. Chi tiết ở Chương 4 và 5.`),
  LEAD(`**Hai. Chuẩn hóa mã được đo trên tập dev/test riêng, và bài toán khó nằm ở khoảng cách giữa lời nói và danh mục.** Trên ${nc("ICD-10").n_linkable} dạng CONDITION của split test có mã gold, chế độ thận trọng đạt Accuracy ${rp(nc("ICD-10").system.accuracy)} với precision ${rp(nc("ICD-10").system.precision_answered)} khi trả lời; chế độ luôn trả lời đạt ${rp(nc("ICD-10").always.accuracy)}; mã đúng nằm trong 10 ứng viên đầu ở ${pct(nc("ICD-10").top10_acc)} trường hợp (Recall@10). RxNorm đạt Accuracy ${rp(nc("RxNorm").system.accuracy)}. Baseline khớp chính xác tên danh mục chỉ đạt ${rp(nc("ICD-10").exact.accuracy)} với ICD-10. Chi tiết ở 5.3.3.`),
  LEAD(`**Ba. Dữ liệu quan hệ là nút thắt, không phải mô hình.** Bộ 600 đoạn sau khi người duyệt chốt quy ước chỉ còn ${posAfter} cặp dương, không có cặp has_dosage và treated_by nào. Bổ sung ${re2.data.v2.samples} câu gán nhãn AI (bộ RE v2) có chủ đích tìm thuốc và liều vẫn chỉ thêm ${re2pos} cặp dương, và không có cặp has_dosage nào: lời nói y tế hầu như không có cụm liều thật. Chi tiết ở Chương 3.`),
  LEAD(`**Bốn. ViHealthBERT là mô hình RE tốt nhất, nhưng chỉ vượt baseline luật khi kết hợp với chính luật, và con số còn tạm thời.** Trên cùng dữ liệu và cùng 5 fold CV, ViHealthBERT có đánh dấu thực thể đạt positive micro-F1 ${rp(bp("cv5", "bert").f1)}, so với ${rp(bp("cv5", "rules").f1)} của luật và ${rp(bp("cv5", "tfidf_lr").f1)} của mô hình TF-IDF. Hợp ViHealthBERT với luật là phương pháp duy nhất đứng đầu hoặc ngang đầu trên cả ba tập đánh giá: ${rp(bp("cv5", "bert+rules").f1)} trên CV, ${rp(bp("golden_test", "bert+rules").f1)} trên golden test và ${rp(bp("random_test", "bert+rules").f1)} trên tập test ngẫu nhiên, nơi luật một mình đạt ${rp(bp("random_test", "rules").f1)}. Khoảng tin cậy vẫn chồng lấn với luật. Hai quan hệ hiếm (diagnosed_by, has_dosage) gần như chỉ được luật bắt. Nhãn RE v2 và hai tập test là nhãn AI, chưa có bác sĩ duyệt. Chi tiết ở 5.4.3.`),
  LEAD(`**Năm. Quy ước nhãn quyết định kết luận so sánh, và soát lại hệ thống tìm ra lỗi thật.** Trước khi duyệt, Logistic Regression vượt luật rất xa (F1 ${rp(cvLa.positive_micro.f1)} so với ${rp(cvRa.positive_micro.f1)}); sau khi loại các cặp nối với từ chung “điều trị”, khoảng cách gần như biến mất (${rp(cvL.positive_micro.f1)} so với ${rp(cvR.positive_micro.f1)}). Bước khớp gần đúng ICD-10 từng gán sai ${icdBefore.wrong_mentions} mention (ví dụ “huyết áp cao” thành Z01.3 “Đo huyết áp”). Các lỗi đã được sửa, có kiểm thử, ${nTests}/${nTests} ca kiểm thử đạt; ${A.length} điểm cần lưu ý được ghi ở Phụ lục A.`),
  LEAD("**Sáu. Việc còn thiếu được nêu rõ.** Ba bộ nhãn mới (chuẩn hóa dev/test, RE v2, golden test) là nhãn AI có cờ `human_verified = false`; mọi số đo trên chúng là tạm thời cho tới khi bác sĩ duyệt phiếu Excel đã chuẩn bị sẵn. Chưa có kết quả RE end-to-end trên thực thể do NER sinh ra, và chưa xác minh được checkpoint NER được chọn trên tập nào (Chương 7)."),
);

// ===== Danh mục từ viết tắt =====
add(
  H1("DANH MỤC TỪ VIẾT TẮT VÀ THUẬT NGỮ"),
  T(["Viết tắt / thuật ngữ", "Ý nghĩa"], [
    ["NER", "Named Entity Recognition — nhận diện thực thể có tên"],
    ["RE", "Relation Extraction — trích xuất quan hệ giữa các thực thể"],
    ["BIO", "Lược đồ gán nhãn chuỗi Begin / Inside / Outside"],
    ["ICD-10", "International Classification of Diseases, phiên bản 10 — phân loại bệnh quốc tế"],
    ["RxNorm / RxCUI", "Danh mục thuốc chuẩn của Thư viện Y khoa Quốc gia Hoa Kỳ / mã định danh khái niệm thuốc"],
    ["FMA, LOINC, MeSH", "Các ontology giải phẫu, xét nghiệm và tiêu đề chủ đề y học (chưa triển khai)"],
    ["ViHealthBERT", "Mô hình ngôn ngữ tiền huấn luyện cho văn bản y tế tiếng Việt"],
    ["TF-IDF", "Term Frequency – Inverse Document Frequency — trọng số đặc trưng văn bản"],
    ["LogReg", "Logistic Regression — hồi quy logistic"],
    ["P, R, F1", "Precision, Recall và trung bình điều hòa của hai đại lượng"],
    ["Strict / relaxed", "Khớp chính xác span và loại / khớp loại và span giao nhau"],
    ["Micro / macro", "Cộng dồn trên mọi lớp / trung bình không trọng số giữa các lớp"],
    ["CI95", "Khoảng tin cậy 95%"],
    ["CV", "Cross-validation — kiểm định chéo"],
    ["Gold", "Dữ liệu nhãn chuẩn dùng làm đáp án"],
    ["Golden test", "Tập kiểm thử end-to-end có nhãn người duyệt, lấy từ split test"],
    ["Mention", "Một lần xuất hiện cụ thể của thực thể trong văn bản"],
    ["Span", "Đoạn ký tự [start, end) của một thực thể trong văn bản"],
    ["Head / tail", "Thực thể đầu / cuối của một quan hệ có hướng"],
    ["CHUA_RO", "Trạng thái tạm cho cặp chưa đủ căn cứ gán nhãn; không phải lớp mô hình"],
    ["NO_RELATION", "Nhãn âm cho cặp đúng kiểu nhưng không có quan hệ"],
    ["Checkpoint", "Bộ trọng số mô hình đã huấn luyện được lưu lại"],
    ["Ablation", "Thí nghiệm bỏ lần lượt từng thành phần để đo đóng góp của nó"],
    ["Dev / validation", "Tập dùng để chọn và tinh chỉnh; khác test, là tập chỉ chạy một lần để báo cáo"],
    ["Accuracy (chuẩn hóa)", "Tỉ lệ dạng có mã đúng mà quyết định duy nhất của hệ thống trùng mã gold; từ chối tính là sai"],
    ["Top-k Accuracy / Recall@k", "Tỉ lệ mã gold nằm trong k ứng viên đầu; trùng nhau khi mỗi đề cập có một khái niệm gold"],
    ["MRR", "Mean Reciprocal Rank — trung bình nghịch đảo thứ hạng của mã đúng"],
    ["NIL", "Đề cập không có mã đúng trong danh mục; hệ thống đúng khi từ chối"],
    ["Union (RE)", "Cặp dương khi mô hình hoặc luật dự đoán dương"],
    ["KG", "Knowledge Graph — đồ thị tri thức: nút là khái niệm, cạnh là quan hệ"],
    ["Nhãn AI", "Nhãn do mô hình ngôn ngữ gán, có cờ human_verified = false, chưa có người duyệt"],
  ], [2600, 7038]),
  CAP("Bảng 0.1. Từ viết tắt và thuật ngữ dùng trong báo cáo."),
);

// ===== Tóm tắt =====
add(
  H1("TÓM TẮT"),
  P(`Khóa luận xây dựng một hệ thống xử lý văn bản y tế tiếng Việt gồm ba thành phần: nhận diện thực thể (NER), trích xuất quan hệ (RE) và chuẩn hóa thực thể sang mã chuẩn (ICD-10 cho bệnh, RxNorm cho thuốc). Hệ thống nhận diện sáu loại thực thể (CONDITION, DRUG, BODY_PART, TEST, PROCEDURE, DOSAGE) và năm quan hệ có hướng (located_at, treated_by, treated_by_procedure, diagnosed_by, has_dosage).`),
  P(`Thành phần NER dùng checkpoint ViHealthBERT đã tinh chỉnh trên VietMed-NER, kết hợp luật nhận diện liều thuốc và các luật hậu xử lý. Trên ${n(nerNew.lat.total_samples)} câu của tập test chính thức, toàn bộ pipeline đạt micro-F1 **${f(s["micro avg"]["f1-score"])}** khi khớp chính xác (strict) và **${f(r["micro avg"]["f1-score"])}** khi chấp nhận span giao nhau (relaxed); thời gian xử lý trung bình **${f(nerNew.lat.mean_latency_ms, 1)} ms/câu** trên CPU.${nerBase && nerInh ? ` So với hai baseline tự huấn luyện trên cùng dữ liệu, phần mô hình ViHealthBERT đạt micro-F1 ${f(nerInh.scores.test.target.micro.f1, 3)} trên sáu loại mục tiêu, vượt baseline từ điển (${f(nerBase.dictionary.test.target.micro.f1, 3)}) và CRF (${f(nerBase.crf.test.target.micro.f1, 3)}) với khoảng tin cậy không chồng lấn.` : ""}${abl ? ` Thí nghiệm ablation cho thấy so với chỉ dùng mô hình, các luật bổ sung làm strict micro-F1 thay đổi ${(s["micro avg"]["f1-score"] - abl.model_only.strict_exact_match["micro avg"]["f1-score"] >= 0 ? "+" : "")}${f(s["micro avg"]["f1-score"] - abl.model_only.strict_exact_match["micro avg"]["f1-score"])}.` : ""}`),
  P(`Với RE, khóa luận xây dựng bộ dữ liệu quan hệ 600 đoạn từ VietMed-NER theo quy trình gán nhãn nhiều vòng (AI đề xuất → AI rà soát → người duyệt). Bộ gold v1 sau duyệt còn ${reGold.pairs} cặp được dùng, trong đó chỉ ${posAfter} cặp dương. Mô hình TF-IDF ký tự + Logistic Regression đạt positive micro-F1 ${rp(cvL.positive_micro.f1)} (CI95 ${rp(cvL.positive_micro_f1_ci95[0])}–${rp(cvL.positive_micro_f1_ci95[1])}) qua cross-validation 5 fold theo nhóm văn bản, so với ${rp(cvR.positive_micro.f1)} của baseline luật. Khoảng tin cậy chồng lấn nhau, nên chưa đủ bằng chứng khẳng định mô hình học máy tốt hơn luật; ưu thế lớn trước khi duyệt (${rp(cvLa.positive_micro.f1)} so với ${rp(cvRa.positive_micro.f1)}) chủ yếu đến từ các cặp nối với từ chung “điều trị”.`),
  P(`Bổ sung ngày 07–08/11/2026, khóa luận xây thêm ${re2.data.v2.samples} câu dữ liệu quan hệ (RE v2) từ split train, một tập test ${rtMan.chosen_sentences} câu lấy ngẫu nhiên từ split test, và so sánh mười phương pháp RE trên cùng một khung: bốn baseline không học (lớp đa số, đồng xuất hiện, ghép cặp gần nhất, luật), ba mô hình cổ điển, ViHealthBERT có đánh dấu thực thể và hai cách kết hợp với luật. ViHealthBERT đạt F1 ${rp(bp("cv5", "bert").f1)} trong cross-validation, cao nhất trong các phương pháp đơn lẻ; ViHealthBERT hợp với luật đạt ${rp(bp("random_test", "bert+rules").f1)} trên tập test ngẫu nhiên (luật: ${rp(bp("random_test", "rules").f1)}). Thí nghiệm cũng cho thấy tập golden test lấy mẫu theo hạn mức có ${pct(bench.positive_rate.golden_test_v1)} cặp dương, đủ để baseline “mọi cặp đều dương” đạt F1 ${rp(bp("golden_test_v1_original", "cooccur").f1)}. Nhãn mới là nhãn AI chưa được bác sĩ duyệt, nên các con số này là tạm thời.`),
  P(`Bước chuẩn hóa được đánh giá trên tập gold riêng gồm ${normMan.splits.dev.CONDITION.unique_forms + normMan.splits.dev.DRUG.unique_forms} dạng (dev, split validation) và ${normMan.splits.test.CONDITION.unique_forms + normMan.splits.test.DRUG.unique_forms} dạng (test). Cải tiến chỉ được chọn trên dev. Trên test, ICD-10 đạt Accuracy ${rp(nc("ICD-10").system.accuracy)} ở chế độ thận trọng (precision ${rp(nc("ICD-10").system.precision_answered)} khi trả lời), ${rp(nc("ICD-10").always.accuracy)} ở chế độ luôn trả lời, Top-5 Accuracy ${rp(nc("ICD-10").top5_acc)} và Recall@10 ${rp(nc("ICD-10")["recall@10"])}; RxNorm đạt Accuracy ${rp(nc("RxNorm").system.accuracy)}. Trước đó, quá trình soát phát hiện ${icdBefore.wrong_mentions} mention bị gán mã sai do bước so khớp gần đúng và đã sửa bằng các ràng buộc an toàn. Cuối cùng, kết quả của toàn bộ split test được gộp thành knowledge graph ${n(kgS.nodes)} nút, ${kgS.edges} cạnh, có trang HTML để tra cứu.`),
  P("Đóng góp chính của khóa luận là pipeline tái lập được từ văn bản tới đồ thị tri thức, các bộ dữ liệu quan hệ và chuẩn hóa có quy ước, nguồn nhãn và lịch sử thay đổi minh bạch, cùng phân tích trung thực về giới hạn dữ liệu."),
  PN("**Từ khóa:** nhận diện thực thể y tế, trích xuất quan hệ, chuẩn hóa ICD-10, RxNorm, ViHealthBERT, tiếng Việt."),
);

// ===== CHƯƠNG 1 =====
add(
  H1("CHƯƠNG 1. MỞ ĐẦU"),
  H2("1.1. Bối cảnh và động lực"),
  P("Phần lớn thông tin lâm sàng như bệnh án, phiếu khám, tóm tắt ra viện hay lời dặn của bác sĩ được ghi dưới dạng văn bản tự do. Dạng dữ liệu này dễ viết nhưng khó khai thác bằng máy: không thể thống kê, tìm kiếm theo khái niệm hay liên thông giữa các hệ thống nếu chưa chuyển sang dạng có cấu trúc. Việc trích xuất thông tin tự động giúp chuyển một câu như “bệnh nhân đau dạ dày, kê Paracetamol 500mg” thành các bản ghi có cấu trúc: tình trạng bệnh kèm mã ICD-10, thuốc kèm mã RxNorm, liều dùng và quan hệ giữa chúng."),
  P("Dữ liệu có cấu trúc mở ra nhiều ứng dụng: gợi ý mã bệnh cho hồ sơ bệnh án điện tử và thanh toán bảo hiểm y tế; thống kê dịch tễ theo bệnh hoặc theo thuốc; tìm kiếm hồ sơ theo khái niệm thay vì theo từ khóa; và làm nền cho các hệ thống hỗ trợ quyết định lâm sàng như cảnh báo liều hoặc tương tác thuốc. Trong mọi ứng dụng đó, chỉ nhận diện thực thể là chưa đủ. Một đơn có hai thuốc và hai liều cần biết liều nào thuộc thuốc nào; một câu nhắc nhiều bệnh và nhiều thuốc cần biết thuốc nào được dùng cho bệnh nào. Đây là vai trò của trích xuất quan hệ."),
  P("Đối với tiếng Việt, tài nguyên xử lý ngôn ngữ y tế còn hạn chế. Bộ dữ liệu VietMed-NER cung cấp nhãn thực thể cho lời nói y tế, nhưng chưa có bộ dữ liệu công khai cho các quan hệ lâm sàng mà đề tài quan tâm. Danh mục ICD-10 tiếng Việt của Bộ Y tế có sẵn nhưng tên bệnh trong danh mục khác xa cách nói hằng ngày (“huyết áp cao” so với “Bệnh lý tăng huyết áp”). Vì vậy, bên cạnh việc xây dựng hệ thống, khóa luận cần tự tạo dữ liệu quan hệ, xây từ điển đồng nghĩa và đánh giá cẩn trọng giới hạn của dữ liệu đó."),
  H2("1.2. Mục tiêu"),
  P("Khóa luận có năm mục tiêu. Mục tiêu thứ nhất là một pipeline NER nhận diện sáu loại thực thể y tế từ văn bản tiếng Việt, xử lý được dấu câu, văn bản dài và cụm liều thuốc. Mục tiêu thứ hai là chuẩn hóa CONDITION sang ICD-10 theo danh mục của Bộ Y tế và DRUG sang RxNorm, với nguyên tắc không gán mã còn hơn gán sai, đồng thời trả về danh sách top-k ứng viên cho người dùng chọn. Mục tiêu thứ ba là dữ liệu và mô hình RE cho năm quan hệ có hướng, được so sánh với baseline luật trên cùng dữ liệu. Mục tiêu thứ tư là gộp kết quả của nhiều văn bản thành một knowledge graph tra cứu được. Mục tiêu thứ năm là đánh giá từng thành phần bằng quy trình tái lập được, có tách train/dev/test, baseline, khoảng tin cậy và phân tích lỗi trên dữ liệu thật."),
  H2("1.3. Phạm vi"),
  P("Đề tài giữ sáu loại thực thể và năm quan hệ đã chốt (Bảng 1.1). CONDITION gộp cả bệnh và triệu chứng; quyết định không tách DISEASE/SYMPTOM được đưa ra để giảm rủi ro lỗi ánh xạ, vì nhãn nguồn DISEASESYMTOM vốn gộp hai khái niệm. Quan hệ chỉ xét trong cùng một câu hoặc một phát ngôn ngắn; không xử lý quan hệ liên câu, đồng tham chiếu, thực thể lồng nhau hay giao diện bệnh viện. Knowledge graph được dựng bằng cách gộp các bộ ba (thực thể, quan hệ, thực thể) đã trích; khóa luận không làm suy luận trên đồ thị và không đối chiếu đồ thị với tri thức y khoa bên ngoài. BODY_PART, TEST và PROCEDURE chưa được chuẩn hóa mã (chỉ có giao diện chờ cho FMA, LOINC, MeSH); DOSAGE được giữ dưới dạng cấu trúc giá trị–đơn vị–tần suất."),
  T(["Quan hệ", "Head → Tail", "Ý nghĩa", "Ví dụ"], [
    ["located_at", "CONDITION → BODY_PART", "Tình trạng xuất hiện ở bộ phận cơ thể", "khối u → gan"],
    ["treated_by", "CONDITION → DRUG", "Thuốc được nêu để điều trị tình trạng", "đau đầu → Paracetamol"],
    ["treated_by_procedure", "CONDITION → PROCEDURE", "Thủ thuật được nêu để điều trị", "hẹp động mạch vành → đặt stent"],
    ["diagnosed_by", "CONDITION → TEST", "Xét nghiệm/phương pháp xác định tình trạng", "viêm phổi → chụp X-quang"],
    ["has_dosage", "DRUG → DOSAGE", "Liều thuộc về thuốc", "Paracetamol → 500 mg"],
  ], [1900, 2300, 3200, 2238]),
  CAP("Bảng 1.1. Năm quan hệ mục tiêu (nguồn: re_labels.json, docs/RE_LABELS.md). NO_RELATION là nhãn âm cho cặp đúng kiểu."),
  H2("1.4. Câu hỏi nghiên cứu"),
  ...LIST([
    "Mô hình RE học từ dữ liệu có cải thiện so với baseline luật trên cùng bộ dữ liệu không?",
    "Lỗi NER làm chất lượng RE toàn hệ thống thay đổi như thế nào?",
    "Các bước xử lý bổ sung (luật liều, hậu xử lý) và chuẩn hóa mã đem lại lợi ích gì, đồng thời tạo ra lỗi gì?",
  ]),
  P("Khóa luận không đặt trước một ngưỡng F1 cần đạt. Đóng góp có thể nằm ở bộ dữ liệu được kiểm duyệt, quy trình tái lập và phân tích lỗi, kể cả khi mô hình không vượt baseline."),
  H2("1.5. Đóng góp"),
  P("Đóng góp đầu tiên là một pipeline NER → chuẩn hóa → RE chạy được từ đầu đến cuối, trả về JSON có vị trí ký tự, độ tin cậy và mã chuẩn. Đóng góp thứ hai là bộ dữ liệu quan hệ 600 đoạn có quy ước gán nhãn, lịch sử thay đổi của từng mẫu và tệp manifest có mã băm SHA-256, để mọi con số có thể truy về đúng phiên bản dữ liệu. Đóng góp thứ ba là công cụ xây tập golden test end-to-end từ split test, gồm 150 đoạn ứng viên, phiếu duyệt Excel và phép tính kappa. Đóng góp thứ tư là bộ đánh giá có khoảng tin cậy bootstrap, ablation các luật NER và phân tích lỗi trên dữ liệu thật. Đóng góp thứ năm là tập gold chuẩn hóa dev/test và bộ RE v2, đều gắn nhãn nguồn rõ ràng là nhãn AI chưa duyệt, kèm phiếu duyệt Excel để bác sĩ xác nhận. Đóng góp thứ sáu là mô-đun knowledge graph gộp nút theo mã chuẩn, xuất JSON/CSV/GraphML và trang HTML tương tác. Đóng góp cuối cùng là kết quả soát toàn bộ số liệu, luồng xử lý và mã nguồn (Phụ lục A), kèm các bản sửa lỗi đã kiểm thử."),
  H2("1.6. Phương pháp thực hiện"),
  P("Khóa luận đi theo quy trình: (1) xác định bài toán và schema; (2) kế thừa checkpoint NER, xây lại suy luận và đánh giá; (3) xây chuẩn hóa ICD-10/RxNorm; (4) tạo dữ liệu quan hệ bằng quy trình AI đề xuất – người duyệt; (5) xây baseline luật và mô hình học máy cho RE; (6) xây tập gold chuẩn hóa dev/test và bổ sung dữ liệu RE v2, cải tiến trên dev và đo trên test một lần; (7) gộp kết quả thành knowledge graph; (8) đánh giá từng thành phần, chạy ablation và phân tích lỗi; (9) soát lại toàn bộ số liệu và mã nguồn trước khi viết báo cáo. Mọi số liệu trong báo cáo được chương trình đọc trực tiếp từ tệp kết quả, không chép tay."),
  H2("1.7. Bố cục báo cáo"),
  P("Chương 2 trình bày cơ sở lý thuyết và nghiên cứu liên quan. Chương 3 mô tả dữ liệu và quy trình gán nhãn. Chương 4 trình bày thiết kế và cài đặt hệ thống. Chương 5 báo cáo kết quả thực nghiệm. Chương 6 phân tích lỗi và thảo luận. Chương 7 kết luận và nêu hướng phát triển. Các phụ lục gồm kết quả soát lỗi, hướng dẫn tái lập, danh mục tệp, hướng dẫn gán nhãn, danh sách cặp quan hệ, bảng mã ICD-10, dự đoán RE, ví dụ JSON, danh sách kiểm thử và phần câu hỏi thường gặp."),
);

// ===== CHƯƠNG 2 =====
add(
  H1("CHƯƠNG 2. CƠ SỞ LÝ THUYẾT VÀ NGHIÊN CỨU LIÊN QUAN"),
  SUM("Chương này trình bày các khái niệm mà các chương sau sử dụng: gán nhãn chuỗi BIO, encoder Transformer, trích xuất quan hệ bằng dấu đánh dấu thực thể, chuẩn hóa mã, TF-IDF với hồi quy logistic, so khớp chuỗi gần đúng và các phép thống kê đánh giá. Điểm quan trọng nhất cho phần sau là tính chất của token_set_ratio (mục 2.6): phép đo cho điểm tối đa khi tập từ của chuỗi này là tập con của chuỗi kia, và đây là nguyên nhân của các lỗi gán mã ICD-10."),
  H2("2.1. Nhận diện thực thể có tên"),
  H3("2.1.1. Định nghĩa bài toán"),
  P("Cho một câu gồm các từ w₁, w₂, …, wₙ, bài toán NER tìm tập các đoạn liên tiếp (span) cùng loại thực thể của chúng. Cách phổ biến là quy về gán nhãn chuỗi: mỗi từ nhận một nhãn cho biết nó bắt đầu (B-X), nằm trong (I-X) hay nằm ngoài (O) một thực thể loại X. Với K loại thực thể, lược đồ BIO có 2K+1 nhãn. VietMed-NER có 18 loại thực thể nên mô hình phân loại 37 nhãn BIO. Một biến thể khác là BIOES, thêm nhãn E (kết thúc) và S (thực thể một từ); dự án dùng BIO theo dữ liệu nguồn."),
  T(["Từ", "Bệnh", "nhân", "đau", "ở", "vùng", "bụng"], [["Nhãn BIO", "O", "O", "B-CONDITION", "O", "B-BODY_PART", "I-BODY_PART"]], [1600, 1300, 1300, 1600, 1100, 1500, 1500], { size: 20 }),
  CAP("Bảng 2.1. Ví dụ minh họa gán nhãn BIO theo sáu loại mục tiêu (câu tự soạn)."),
  P("Giải mã BIO thành span cần xử lý các chuỗi không hợp lệ, chẳng hạn I-X đứng sau O hoặc sau B-Y khác loại. Cách thường dùng là coi I-X đó như bắt đầu một thực thể mới. Sau khi có span ở mức từ, hệ thống chuyển sang vị trí ký tự [start, end) trong văn bản để các bước sau (chuẩn hóa, RE, giao diện) dùng chung một hệ tọa độ."),
  H3("2.1.2. Các hướng tiếp cận"),
  P("Các hệ thống NER đầu tiên dùng luật và từ điển: dễ giải thích nhưng khó bao phủ biến thể ngôn ngữ. Giai đoạn học máy thống kê dùng mô hình Markov ẩn và Conditional Random Fields (CRF). CRF mô hình hóa xác suất có điều kiện của cả chuỗi nhãn với đặc trưng thủ công (hình thái từ, từ điển, ngữ cảnh), và nhờ mô hình hóa chuyển tiếp nhãn nên ít sinh chuỗi BIO không hợp lệ. Giai đoạn học sâu thay đặc trưng thủ công bằng biểu diễn học được, điển hình là BiLSTM-CRF. Hiện nay, cách phổ biến nhất là tinh chỉnh một encoder Transformer tiền huấn luyện (họ BERT) với một lớp phân loại tuyến tính cho từng token."),
  H3("2.1.3. Đặc thù tiếng Việt và miền y tế"),
  P("Tiếng Việt viết theo âm tiết, một từ có thể gồm nhiều âm tiết (“dạ dày”, “đái tháo đường”). Mô hình có thể làm việc ở mức âm tiết hoặc cần bước tách từ trước. ViHealthBERT bản syllable làm việc trực tiếp trên âm tiết, nên hệ thống chỉ cần tách theo khoảng trắng và dấu câu. Miền y tế có thêm các khó khăn: tên thuốc và hoạt chất mượn tiếng nước ngoài, viết tắt, cụm bệnh dài lồng bộ phận cơ thể (“viêm loét dạ dày tá tràng”), và trong văn bản nói còn có lỗi phiên âm, câu bị cắt giữa chừng."),
  H3("2.1.4. Đánh giá NER"),
  P("Chất lượng NER được đo ở mức thực thể. **Strict match** chỉ tính đúng khi khớp cả loại và vị trí bắt đầu–kết thúc. **Relaxed match** chấp nhận dự đoán cùng loại có span giao với span gold, mỗi gold được ghép tối đa một lần. Với TP, FP, FN là số dự đoán đúng, dự đoán thừa và gold bị bỏ sót:"),
  MATH("P = TP / (TP + FP);   R = TP / (TP + FN);   F1 = 2·P·R / (P + R)"),
  P("Micro-F1 cộng dồn TP/FP/FN trên mọi loại nên chịu ảnh hưởng của loại nhiều mẫu; macro-F1 là trung bình F1 của các loại, coi mọi loại như nhau; weighted-F1 lấy trung bình theo support. Thư viện seqeval là chuẩn thông dụng cho đánh giá mức thực thể trên nhãn BIO; dự án dùng seqeval cho tầng 1 và tự cài đặt strict/relaxed cho tầng 2 (eval/metrics.py)."),
  H2("2.2. Mô hình ngôn ngữ tiền huấn luyện"),
  H3("2.2.1. Kiến trúc Transformer và cơ chế tự chú ý"),
  P("Transformer encoder gồm nhiều lớp giống nhau; mỗi lớp có khối tự chú ý nhiều đầu (multi-head self-attention) và mạng truyền thẳng. Với ma trận truy vấn Q, khóa K và giá trị V được chiếu tuyến tính từ biểu diễn đầu vào, phép chú ý được tính:"),
  MATH("Attention(Q, K, V) = softmax(Q·Kᵀ / √dₖ) · V"),
  P("Mỗi vị trí vì vậy tổng hợp thông tin từ mọi vị trí khác trong câu, với trọng số học được. Nhiều đầu chú ý chạy song song cho phép mô hình học nhiều kiểu quan hệ ngữ cảnh khác nhau. Vì phép chú ý không có khái niệm thứ tự, mô hình cộng thêm embedding vị trí; số vị trí tối đa là giới hạn độ dài đầu vào."),
  H3("2.2.2. BERT, RoBERTa và tiền huấn luyện"),
  P("BERT tiền huấn luyện encoder Transformer trên văn bản lớn bằng nhiệm vụ mô hình ngôn ngữ có che (masked language model): che ngẫu nhiên một phần token và yêu cầu mô hình đoán lại. RoBERTa giữ kiến trúc nhưng thay đổi quy trình tiền huấn luyện (bỏ nhiệm vụ dự đoán câu tiếp theo, dữ liệu và thời gian lớn hơn). PhoBERT là mô hình kiểu RoBERTa cho tiếng Việt; ViHealthBERT tiếp tục tiền huấn luyện trên văn bản y tế tiếng Việt."),
  T(["Thuộc tính", "Giá trị trong checkpoint NER"], [
    ["Kiến trúc", modelCfg.architectures.join(", ")], ["Loại mô hình", modelCfg.model_type],
    ["Số lớp encoder", String(modelCfg.num_hidden_layers)], ["Kích thước ẩn", String(modelCfg.hidden_size)],
    ["Số đầu chú ý", String(modelCfg.num_attention_heads)], ["Kích thước lớp truyền thẳng", String(modelCfg.intermediate_size)],
    ["Số vị trí tối đa", String(modelCfg.max_position_embeddings)], ["Kích thước từ vựng", n(modelCfg.vocab_size)],
    ["Dropout ẩn", String(modelCfg.hidden_dropout_prob).replace(".", ",")], ["Số nhãn đầu ra", String(Object.keys(modelCfg.id2label || {}).length)],
  ], [4000, 5638]),
  CAP("Bảng 2.2. Cấu hình kiến trúc checkpoint NER (nguồn: Model/vihealthbert-ner-vietmed-v2-final/config.json)."),
  H3("2.2.3. Tách subword và căn chỉnh nhãn"),
  P("Mô hình không làm việc trực tiếp trên từ mà trên subword do bộ tách BPE (Byte-Pair Encoding) tạo ra; checkpoint dùng tệp bpe.codes và vocab.txt. Một âm tiết hiếm có thể bị tách thành nhiều subword. Khi tinh chỉnh cho NER, nhãn thường gắn vào subword đầu tiên của mỗi từ; khi suy luận, nhãn của từ lấy theo subword đầu tiên. Các token đặc biệt <s> và </s> được thêm ở đầu và cuối chuỗi; dự đoán tại các vị trí này phải bị loại trước khi giải mã."),
  H3("2.2.4. Tinh chỉnh cho gán nhãn chuỗi"),
  P("Với bài toán gán nhãn chuỗi, một lớp tuyến tính W ∈ ℝ^(768×37) được đặt trên biểu diễn của từng subword, theo sau là softmax. Hàm mất mát là cross-entropy trung bình trên các vị trí có nhãn. Toàn bộ tham số encoder và lớp phân loại được cập nhật bằng AdamW với learning rate nhỏ."),
  H2("2.3. Trích xuất quan hệ"),
  H3("2.3.1. Định nghĩa"),
  P("Cho văn bản x và hai thực thể eₕ (head), eₜ (tail) trong x, bài toán RE dự đoán nhãn r ∈ R ∪ {NO_RELATION}, với R là tập quan hệ. Trong dự án, R gồm năm quan hệ có hướng và mỗi cặp kiểu (loại head, loại tail) chỉ ứng với một quan hệ dương hợp lệ, nên bài toán thực chất là phân loại nhị phân có điều kiện theo kiểu cặp: có hay không có quan hệ tương ứng."),
  H3("2.3.2. Các hướng tiếp cận"),
  P("Cách đơn giản nhất là luật và mẫu: dùng từ gợi ý và khoảng cách, ví dụ “X được điều trị bằng Y”. Luật dễ giải thích và không cần dữ liệu huấn luyện, nhưng bỏ sót nhiều cách diễn đạt. Hướng học máy cổ điển dùng đặc trưng thủ công như từ giữa hai thực thể, loại thực thể, khoảng cách và đường đi cú pháp, rồi đưa vào bộ phân loại tuyến tính hoặc SVM. Mạng nơ-ron CNN và RNN thay đặc trưng thủ công bằng biểu diễn học được trên chuỗi có đánh dấu vị trí tương đối với hai thực thể."),
  P("Hướng hiện đại nhất dùng encoder tiền huấn luyện và chèn dấu đánh dấu quanh head và tail. Nghiên cứu “Matching the Blanks” cho thấy lấy biểu diễn tại marker mở là lựa chọn tốt. PURE dùng marker có kèm loại thực thể (typed markers) trong một pipeline NER → RE và đạt kết quả mạnh trên ACE và SciERC. Mô hình chung (joint) học NER và RE cùng lúc để giảm lan truyền lỗi, nhưng phức tạp hơn và cần nhiều dữ liệu hơn. Với dữ liệu nhỏ như của đề tài, pipeline tách rời là lựa chọn thực tế: NER có thể kế thừa, còn RE được đánh giá riêng trên thực thể gold."),
  H3("2.3.3. Trích xuất quan hệ lâm sàng"),
  P("Thử thách i2b2/VA 2010 định nghĩa các quan hệ giữa problem, treatment và test: treatment cải thiện, làm xấu, gây ra, được dùng cho hoặc không được dùng cho problem; test phát hiện hoặc được làm để khảo sát problem; problem chỉ ra problem. Quan hệ treated_by và diagnosed_by của đề tài gần với nhóm “treatment được dùng cho problem” và “test phát hiện problem”, nhưng gộp và đơn giản hơn. Thử thách n2c2 2018 Track 2 nối thuốc với các thuộc tính (hàm lượng, liều, tần suất, đường dùng, lý do dùng, tác dụng phụ); quan hệ has_dosage tương ứng một phần với nhóm thuộc tính này. Cả hai thử thách đều cho thấy khoảng cách lớn giữa đánh giá trên thực thể gold và đánh giá end-to-end."),
  H3("2.3.4. Mất cân bằng lớp và đánh giá RE"),
  P("Số cặp ứng viên tăng theo bình phương số thực thể, trong khi số cặp có quan hệ ít, nên dữ liệu RE thường mất cân bằng mạnh. Các cách xử lý gồm cân bằng trọng số lớp, lấy mẫu âm, và giới hạn cặp ứng viên theo kiểu. Chỉ số chính là positive micro-F1 trên các nhãn dương; một dự đoán dương trên cặp gold NO_RELATION là FP. Khi đánh giá end-to-end, cạnh chỉ đúng khi cả hai đầu mút khớp chính xác (span và loại) và nhãn quan hệ đúng; cạnh gold mất một đầu mút do NER bỏ sót là FN."),
  H2("2.4. Chuẩn hóa thực thể"),
  H3("2.4.1. Bài toán"),
  P("Chuẩn hóa (entity normalization, entity linking) gán cho mỗi mention một khái niệm trong ontology, ví dụ “cao huyết áp” → I10. Khó khăn chính là khoảng cách giữa cách nói và tên chuẩn, sự nhập nhằng (“nhồi máu” có thể là nhồi máu cơ tim, não, lách…) và mức chi tiết của mã. Các cách tiếp cận gồm: khớp chính xác với từ điển; khớp qua từ đồng nghĩa và luật biến đổi; khớp gần đúng theo độ tương tự chuỗi; và mô hình học biểu diễn để so sánh mention với tên khái niệm. Dự án dùng ba cách đầu, có thứ tự ưu tiên rõ ràng."),
  H3("2.4.2. ICD-10"),
  P("ICD-10 tổ chức mã theo chương (chữ cái đầu), nhóm ba ký tự (ví dụ I10 bệnh tăng huyết áp, I21 nhồi máu cơ tim cấp) và phân nhóm bốn ký tự sau dấu chấm (ví dụ M54.5 đau cột sống thắt lưng). Dự án dùng danh mục ICD-10 tiếng Việt do Bộ Y tế ban hành (tệp Excel trong thư mục `ICD-10/`, kèm văn bản PDF)."),
  H3("2.4.3. RxNorm"),
  P("RxNorm là danh mục thuốc chuẩn của Thư viện Y khoa Quốc gia Hoa Kỳ. Mỗi khái niệm (hoạt chất, thuốc lâm sàng, thuốc biệt dược, …) có mã RxCUI. Dịch vụ REST RxNav cho phép tra RxCUI từ tên thuốc và lấy tên chuẩn. RxNorm chủ yếu chứa thuốc lưu hành tại Hoa Kỳ, nên tên thuốc tiếng Việt, thảo dược và thực phẩm chức năng thường không có mã."),
  H2("2.5. TF-IDF và hồi quy logistic"),
  P("TF-IDF biểu diễn văn bản bằng vector trọng số của các đặc trưng (từ hoặc n-gram ký tự). Trọng số tăng theo tần suất trong văn bản (tf) và giảm theo số văn bản chứa đặc trưng (df). Thư viện scikit-learn dùng dạng làm trơn:"),
  MATH("idf(t) = ln((1 + N) / (1 + df(t))) + 1;   w(t, d) = tf′(t, d) · idf(t),   tf′ = 1 + ln(tf) khi dùng sublinear_tf"),
  P("Vector của mỗi văn bản được chuẩn hóa L2. N-gram ký tự (2–5 ký tự) bền với lỗi chính tả, biến thể dấu và từ ghép, phù hợp khi dữ liệu nhỏ. Hồi quy logistic đa lớp ước lượng xác suất mỗi lớp bằng softmax của tổ hợp tuyến tính các đặc trưng, huấn luyện bằng cực tiểu cross-entropy có chuẩn hóa L2 (tham số C). Tùy chọn class_weight = “balanced” gán trọng số w_c = N / (K · N_c) cho lớp c, giúp lớp ít mẫu không bị lấn át."),
  H2("2.6. So khớp chuỗi gần đúng"),
  P("Thư viện RapidFuzz cung cấp các độ tương tự dựa trên khoảng cách chỉnh sửa. `ratio(a, b)` là độ tương tự chuẩn hóa theo phép chèn/xóa, bằng 100 khi hai chuỗi giống hệt. `token_set_ratio` tách từ, tính phần giao I và phần riêng của mỗi chuỗi, rồi lấy giá trị lớn nhất của ratio giữa I với I∪riêng(a), I với I∪riêng(b), và giữa hai chuỗi hợp. Hệ quả quan trọng: **nếu tập từ của một chuỗi là tập con của chuỗi kia thì token_set_ratio = 100**, bất kể chuỗi dài có thêm những từ nào. Đây là nguyên nhân của các lỗi gán mã được phân tích ở Chương 6. Hệ số Jaccard |A∩B| / |A∪B| giữa hai tập từ được dùng làm ràng buộc phụ."),
  H2("2.7. Thống kê đánh giá"),
  P("**Kiểm định chéo theo nhóm.** Dữ liệu được chia thành k phần; mỗi lần dùng một phần để đánh giá, phần còn lại để huấn luyện. Khi nhiều mẫu có chung nguồn (ví dụ nhiều cặp trong cùng một câu), phải chia theo nhóm để mẫu cùng nhóm không nằm ở cả hai phía, tránh đánh giá lạc quan. Dự đoán của mọi fold được gộp lại để tính một chỉ số chung."),
  P("**Khoảng tin cậy bootstrap.** Lấy mẫu lại có hoàn lại các nhóm (không phải từng cặp) B lần, mỗi lần tính lại F1; khoảng tin cậy 95% là phân vị 2,5% và 97,5% của B giá trị. Phương pháp không giả định phân phối và phản ánh đúng độ bất định khi support nhỏ."),
  P("**Độ đồng thuận giữa người gán nhãn.** Hệ số Cohen’s kappa hiệu chỉnh mức đồng ý ngẫu nhiên:"),
  MATH("κ = (pₒ − pₑ) / (1 − pₑ)"),
  P("trong đó pₒ là tỉ lệ đồng ý quan sát được và pₑ là tỉ lệ đồng ý kỳ vọng nếu hai người gán ngẫu nhiên theo phân phối nhãn của mình. Công cụ golden test đã cài đặt phép tính này cho 30 đoạn được duyệt chéo."),
  H2("2.8. Nghiên cứu liên quan và benchmark tham khảo"),
  T(["Công trình / Benchmark", "Thiết lập", "Điểm công bố", "Vai trò"], [
    ["VietMed-NER (NAACL 2025 Industry)", "NER lời nói y tế tiếng Việt, 18 loại thực thể", "—", "Nguồn dữ liệu chính"],
    ["ViHealthBERT (LREC 2022)", "Encoder y tế tiếng Việt", "—", "Mô hình nền NER"],
    ["PhoBERT (Findings EMNLP 2020)", "Encoder RoBERTa tiếng Việt", "—", "Nền tảng của ViHealthBERT"],
    ["PhoNER_COVID19 (NAACL 2021)", "NER tiếng Việt miền COVID-19", "—", "NER y tế tiếng Việt viết"],
    ["PURE (NAACL 2021), ACE05, BERT-base", "Pipeline + typed markers", "Strict Rel+ F1 63,9%", "Cơ sở thiết kế RE"],
    ["i2b2/VA 2010", "RE trên gold concepts", "Best F1 0,737", "Quan hệ problem–treatment/test"],
    ["n2c2 2018, Track 2", "Thuốc–thuộc tính, gold concepts / end-to-end", "Lenient micro-F1 0,9630 / 0,8905", "Tách RE độc lập và toàn pipeline"],
  ], [2700, 2700, 2000, 2238]),
  CAP("Bảng 2.3. Công trình liên quan. Các điểm thuộc corpus, ngôn ngữ và cách chấm khác nên không so sánh trực tiếp."),
  NOTE("Các con số trong Bảng 2.3 được lấy từ tài liệu nội bộ docs/BAO_CAO_RE_2026-10-02.md. Cần đối chiếu lại với bài báo gốc trước khi nộp (Phụ lục A, mục A13)."),
  P("So với các công trình trên, khóa luận có ba điểm khác: dữ liệu là lời nói y tế tiếng Việt chứ không phải bệnh án viết; dữ liệu quan hệ phải tự xây và rất nhỏ; và trọng tâm là pipeline tái lập được cùng phân tích giới hạn, thay vì tối đa hóa điểm số trên một benchmark có sẵn."),
);

// ===== CHƯƠNG 3 =====
const mapRows = [
  ["CONDITION", "DISEASESYMTOM"], ["DRUG", "DRUGCHEMICAL, PREVENTIVEMED"], ["BODY_PART", "ORGAN"],
  ["TEST", "DIAGNOSTICS"], ["PROCEDURE", "SURGERY, MEDDEVICETECHNIQUE, TREATMENT"], ["DOSAGE", "UNITCALIBRATOR"],
  ["(loại bỏ)", "AGE, GENDER, DATETIME, OCCUPATION, LOCATION, ORGANIZATION, FOODDRINK, PERSONALCARE, TRANSPORTATION"],
];
const flagDesc = {
  CONTEXT_OR_TRANSCRIPT: "Thiếu ngữ cảnh, câu bị cắt hoặc lỗi phiên âm", GENERIC_INTERVENTION: "Can thiệp chung chung (“điều trị”, “thuốc”)",
  ONTOLOGY_SCOPE: "Phạm vi loại thực thể (mỹ phẩm, thực phẩm, chất nội sinh)", UNRESOLVED_RE: "Quan hệ chưa kết luận được",
  SCOPE_CONFIRMATION: "Cần xác nhận phạm vi nhãn", GENERIC_MENTION: "Bệnh/triệu chứng chung chung (“bệnh”, “biến chứng”)",
  SYMPTOM_SCOPE: "Ranh giới triệu chứng", PHYSIOLOGY_VS_DISEASE: "Sinh lý bình thường hay bệnh lý", DOSAGE_CONTEXT: "Liều không rõ thuộc thuốc nào",
};
const exampleTable = (ex) => [
  PN(`**${ex.id}.** “${ex.text}”`),
  T(["ID", "Loại", "Văn bản", "Vị trí"], ex.entities.map((e) => [e[0], e[1], e[2], `${e[3]}–${e[4]}`]), [800, 1800, 4800, 2238], { size: 20 }),
  ...(ex.relations.length ? [T(["Cặp", "Head → Tail", "Nhãn gold v1"], ex.relations.map((x) => [x[0], `${x[1]} → ${x[2]}`, x[3]]), [800, 5600, 3238], { size: 20 })] : []),
  ...(ex.changes.length ? [PN(`Thay đổi khi duyệt: ${ex.changes.map((c) => c.op === "relabel" ? `${c.relation}: ${c.before} → ${c.after}` : c.op === "delete_entity" ? `xóa ${c.entity} “${c.text}”` : `xóa ${c.relation} (${c.before})`).join("; ")}.`, { run: { size: 22, italics: true } })] : []),
];
add(
  H1("CHƯƠNG 3. DỮ LIỆU"),
  SUM(`Khóa luận dùng năm bộ dữ liệu, đều bắt nguồn từ VietMed-NER: chính VietMed-NER để đánh giá NER (${n(X.splits.split_sizes.test)} câu test); bộ 600 đoạn gán nhãn quan hệ có người duyệt (gold v1, ${reGold.pairs} cặp dùng được, ${posAfter} cặp dương); bộ RE v2 ${re2.data.v2.samples} câu gán nhãn AI (${re2.data.v2.included_pairs} cặp, ${re2pos} dương); tập golden test 150 đoạn từ split test (nhãn AI tiền gán, ${re2.data.golden_test.pairs} cặp dùng được); và tập gold chuẩn hóa dev/test (nhãn AI). Kết luận của chương: dữ liệu đủ để đánh giá NER và chuẩn hóa, nhưng dữ liệu quan hệ quá thưa để kết luận chắc chắn về RE; nguyên nhân nằm ở bản chất của lời nói y tế, không phải ở quy trình gán nhãn.`),
  H2("3.1. VietMed-NER"),
  H3("3.1.1. Mô tả"),
  P(`VietMed-NER (leduckhai/VietMed-NER trên Hugging Face) là bộ dữ liệu nhận diện thực thể trên bản chép lời của lời nói y tế tiếng Việt. Dữ liệu được gán ${nTypes} loại thực thể theo lược đồ BIO (37 nhãn), gồm các loại y khoa (bệnh/triệu chứng, thuốc/hóa chất, cơ quan, chẩn đoán, phẫu thuật, thiết bị/kỹ thuật, điều trị, đơn vị đo, y học dự phòng, chăm sóc cá nhân) và các loại phi y khoa (tuổi, giới tính, thời gian, nghề nghiệp, địa điểm, tổ chức, thực phẩm, phương tiện).`),
  T(["Split", "Số câu", "Số từ trung bình/câu", "Vai trò trong khóa luận"], ["train", "validation", "test"].map((k) => [k, n(X.splits.split_sizes[k]), f(X.splits.mean_words[k], 1), k === "train" ? "Nguồn của 600 đoạn RE và RE v2; NER đã học" : k === "validation" ? "Dev cho chuẩn hóa (chọn alias, ngưỡng)" : "Đánh giá NER, chuẩn hóa; nguồn golden test và KG"]), [1700, 1700, 2600, 3638], { right: [1, 2] }),
  CAP("Bảng 3.1. Các split của VietMed-NER (đếm từ bản cache Hugging Face, fingerprint e3d0393c…)."),
  P("Lưu ý quan trọng: đây là văn bản chép lời nói (hội thoại, chương trình tư vấn sức khỏe, quảng cáo sản phẩm), không phải bệnh án viết. Mỗi dòng là một đoạn ngắn khoảng 22–24 từ, thường bị cắt giữa câu, không có dấu câu, có lỗi phiên âm (“mặc đổ dầu” thay vì “mặt đổ dầu”, “phẫu thuốc” thay vì “phẫu thuật”) và nhiều nội dung ngoài lâm sàng (mỹ phẩm, thực phẩm chức năng). Kết quả trên VietMed-NER vì vậy chưa chứng minh chất lượng trên bệnh án bệnh viện."),
  H3("3.1.2. Chất lượng nhãn nguồn"),
  P("Khi phân tích lỗi (mục 6.1), một số nhãn gold của VietMed-NER không nhất quán, ví dụ “polyp” được gán ORGAN (cơ quan) và “nhân xơ” được gán ORGAN, trong khi các cụm bệnh tương tự ở câu khác được gán DISEASESYMTOM. Những trường hợp này làm giảm điểm của cả mô hình lẫn pipeline mà không phản ánh lỗi thật, và là một giới hạn của việc dùng VietMed-NER làm thước đo."),
  H2("3.2. Ánh xạ sang sáu loại thực thể mục tiêu"),
  T(["Loại mục tiêu", "Nhãn gốc VietMed-NER"], mapRows, [2200, 7438]),
  CAP("Bảng 3.2. Ánh xạ nhãn (nguồn: ner/config.py, VIETMED_TO_TARGET)."),
  P("Ánh xạ này có ba hệ quả. Thứ nhất, TREATMENT được gộp vào PROCEDURE nên các từ chung như “điều trị” cũng thành PROCEDURE. Thứ hai, UNITCALIBRATOR rộng hơn khái niệm liều thuốc (gồm cả số đo, mức độ, tỉ lệ), nên DOSAGE có precision thấp. Thứ ba, PREVENTIVEMED (vắc-xin) được gộp vào DRUG; điều này có lợi cho chuẩn hóa thuốc nhưng làm các câu về tiêm phòng sinh cặp CONDITION–DRUG mà theo quy ước là phòng ngừa, không phải điều trị. Các loại phi y khoa bị loại hoàn toàn thay vì giữ dưới nhãn OTHER, vì mô hình có xu hướng tự tin gán “bệnh nhân” là OCCUPATION — một đặc điểm dữ liệu huấn luyện chứ không phải lỗi căn chỉnh."),
  H2("3.3. Bộ dữ liệu quan hệ 600 đoạn"),
  H3("3.3.1. Nguồn và quy trình gán nhãn"),
  P("600 đoạn (mã VM600-001 đến VM600-600) được chọn ngẫu nhiên từ split train của VietMed-NER. Thực thể lấy từ nhãn gốc đã ánh xạ sáu loại; cặp ứng viên được sinh theo đúng kiểu và chiều trong schema. Quy trình gán nhãn gồm bốn vòng:"),
  ...LIST([
    "**Bản đề xuất AI** (annotations_draft.jsonl): gán nhãn quan hệ ban đầu, kèm bằng chứng và lý do cho từng cặp.",
    "**Phiếu duyệt DOCX**: sáu phiếu, mỗi phiếu 100 mẫu, có hướng dẫn đánh dấu sửa/xóa/bổ sung cho bác sĩ, và công cụ đọc ngược phiếu đã sửa (scripts/import_physician_review.py).",
    `**AI rà soát lần hai** (15/10/2026): thực thể giảm từ ${n(reviewStats.entities_before)} xuống ${n(reviewStats.entities_after)} (${reviewStats.change_events.remove_entity} thao tác xóa, ${reviewStats.change_events.add_entity} bổ sung, ${reviewStats.change_events.edit_entity} sửa); ${reviewStats.changed_samples} mẫu thay đổi; ${reviewStats.pending_samples} mẫu còn cờ cần phân xử.`,
    `**Người duyệt trên giấy** (05/11/2026): đồng ý bản rà soát và 40 đề xuất sửa nhãn; chốt các quy ước ở Bảng 3.5. Kết quả là bộ **gold v1** (data/re_gold_v1/annotations_gold_v1.jsonl), ${gold.samples_changed} mẫu thay đổi so với bản rà soát.`,
  ]),
  NOTE(`Thông tin người duyệt trong manifest hiện là “${gold.reviewer}” / “${gold.reviewed_at}”. Cần điền họ tên, chức danh người duyệt và ngày duyệt thật rồi chạy lại scripts/apply_paper_review.py trước khi nộp. Chỉ có một người duyệt nên chưa đo được độ đồng thuận giữa người gán nhãn.`),
  P("Việc dùng AI để đề xuất nhãn giúp giảm thời gian của người duyệt, nhưng tạo nguy cơ người duyệt bị “neo” theo đề xuất. Để kiểm soát, mọi bản ghi đều giữ trạng thái `human_verified` và `training_eligible`; bộ nạp dữ liệu (relation_extraction/data.py) từ chối bản chưa xác minh trừ khi người dùng bật cờ `--allow-ai-labels` một cách tường minh, và báo cáo luôn ghi rõ nguồn nhãn của từng kết quả."),
  H3("3.3.2. Thống kê văn bản"),
  T(["Chỉ số", "Giá trị"], [
    ["Số đoạn", "600"], ["Số từ trung bình / trung vị / lớn nhất", `${f(S6.words_mean, 1)} / ${S6.words_median} / ${S6.words_max}`],
    ["Số thực thể trung bình mỗi đoạn (gold v1)", f(S6.ent_mean, 2)], ["Số đoạn không có thực thể mục tiêu", String(S6.no_entity)],
    ["Số đoạn có ít nhất một cặp ứng viên", String(S6.with_pairs)],
    ["Cặp ứng viên theo kiểu (gồm CHUA_RO)", Object.entries(S6.pair_type_count).map(([k, v]) => `${k}: ${v}`).join("; ")],
  ], [4600, 5038]),
  CAP("Bảng 3.3. Thống kê 600 đoạn sau khi duyệt."),
  P(`Hơn một phần ba số đoạn (${S6.no_entity}/600) không có thực thể mục tiêu nào, và chỉ ${S6.with_pairs} đoạn có cặp ứng viên. Phần lớn cặp là located_at (CONDITION–BODY_PART), vì bệnh và bộ phận cơ thể thường xuất hiện cùng nhau trong lời tư vấn. Không có cặp DRUG–DOSAGE nào, vì chỉ có ${gold.after.entities.DOSAGE} thực thể DOSAGE trong cả 600 đoạn.`),
  H3("3.3.3. Cờ rà soát"),
  T(["Cờ", "Ý nghĩa", "Số lần"], Object.entries(S6.ai_flags).sort((a, b) => b[1] - a[1]).map(([k, v]) => [k, flagDesc[k] || "", v]), [3000, 5000, 1638], { right: [2] }),
  CAP("Bảng 3.4. Các cờ do vòng AI rà soát gắn (một đoạn có thể có nhiều cờ). Sau khi người duyệt chốt quy ước, cờ được chuyển sang trường ai_review_flags để lưu lịch sử."),
  H3("3.3.4. Quy ước gán nhãn"),
  B("Gán nhãn dương chỉ khi văn bản thể hiện rõ quan hệ giữa chính hai thực thể đó; không suy ra từ việc cùng xuất hiện hay từ kiến thức y khoa bên ngoài."),
  B("Giữ nguyên cụm bệnh/triệu chứng đầy đủ trong một CONDITION (“viêm loét dạ dày”, “thiếu máu cơ tim”); không tạo located_at với bộ phận đã nằm trong cụm."),
  B("Phòng ngừa (vắc-xin, kem chống nắng), nguyên nhân và tác dụng phụ không phải quan hệ điều trị."),
  B("Không truyền quan hệ sang lần nhắc khác của cùng thực thể (không xử lý đồng tham chiếu)."),
  B("CHUA_RO là trạng thái tạm, không phải lớp mô hình; cặp CHUA_RO bị loại khỏi huấn luyện và đánh giá, không tự chuyển thành NO_RELATION."),
  T(["Quy ước", "Quyết định của người duyệt (05/11/2026)"], Object.entries({
    "Thực thể chung chung PROCEDURE/DRUG/TEST": gold.conventions.generic_entities,
    "Câu hỏi chưa khẳng định": gold.conventions.question,
    "Phủ định": gold.conventions.negation,
    "Thực phẩm chức năng, đông y, lỗi phiên âm": gold.conventions.out_of_scope,
    "CONDITION chung chung": gold.conventions.generic_condition,
  }), [3300, 6338]),
  CAP("Bảng 3.5. Các quy ước được chốt khi duyệt (nguồn: data/re_gold_v1/manifest.json). Hướng dẫn đầy đủ có ví dụ ở Phụ lục D."),
  P(`Quy ước xóa thực thể chung chung loại bỏ ${removedTotal} thực thể: ${removedGeneric.map(([k, v]) => `${k.split(":")[1]} (${k.split(":")[0]}, ${v})`).join("; ")}. Danh sách cụ thể được lưu một nơi duy nhất (relation_extraction/data.py, GENERIC_ENTITIES) và được dùng chung cho việc tạo gold lẫn bước suy luận RE.`),
  H3("3.3.5. Thống kê nhãn trước và sau duyệt"),
  T(["Nhãn", "Bản AI rà soát (15/10)", "Gold v1 (05/11)"], [
    ...RELS.map((k) => [k, relCount(gb, k), relCount(ga, k)]),
    ["Tổng cặp dương", posBefore, posAfter],
    ["NO_RELATION", relCount(gb, "NO_RELATION"), relCount(ga, "NO_RELATION")],
    ["CHUA_RO (loại khỏi huấn luyện)", relCount(gb, "CHUA_RO"), relCount(ga, "CHUA_RO")],
    ["Cặp dùng được (dương + âm)", reAi.pairs, reGold.pairs],
    ["Số đoạn có ít nhất một cặp dùng được", reAi.audit.samples_with_included_pairs, reGold.audit.samples_with_included_pairs],
  ], [3900, 2869, 2869], { right: [1, 2] }),
  CAP("Bảng 3.6. Phân bố nhãn quan hệ trước và sau khi duyệt."),
  T(["Loại thực thể", "Bản AI rà soát", "Gold v1"], LABELS6.map((k) => [k, gold.before.entities[k] || 0, gold.after.entities[k] || 0]), [3900, 2869, 2869], { right: [1, 2] }),
  CAP("Bảng 3.7. Số thực thể theo loại trong 600 đoạn."),
  P(`Sau duyệt, bộ dữ liệu còn rất ít cặp dương: located_at ${relCount(ga, "located_at")}, treated_by_procedure ${relCount(ga, "treated_by_procedure")}, diagnosed_by ${relCount(ga, "diagnosed_by")}, treated_by ${relCount(ga, "treated_by")}, has_dosage ${relCount(ga, "has_dosage")}. treated_by_procedure giảm từ ${relCount(gb, "treated_by_procedure")} xuống ${relCount(ga, "treated_by_procedure")} vì ${relCount(gb, "treated_by_procedure") - relCount(ga, "treated_by_procedure")} cặp trước đây nối với từ chung “điều trị”, “trị liệu”, “tập luyện”. treated_by mất cả hai cặp: một cặp nối với “thuốc” chung chung, cặp còn lại (“chống viêm corticoid”) được sửa thành NO_RELATION vì “viêm” là công dụng của thuốc chứ không phải bệnh của người bệnh. Bộ này phù hợp làm dữ liệu train/dev thăm dò, không đủ để đánh giá cả năm quan hệ.`),
  H3("3.3.6. Ví dụ mẫu dữ liệu"),
  P("Bốn mẫu dưới đây được trích nguyên văn từ gold v1 để minh họa cấu trúc dữ liệu và các quy ước: một quan hệ located_at rõ ràng, một ca tác dụng phụ, một thủ thuật có lỗi phiên âm và một ca diagnosed_by hiếm hoi."),
  ...X.examples.flatMap(exampleTable),
  CAP("Ví dụ 3.1. Mẫu dữ liệu gold v1 (vị trí ký tự, end không bao gồm)."),
  H2("3.4. Tập golden test end-to-end (v1)"),
  P(`Để có tập đánh giá độc lập, khóa luận chọn ${gt.samples} đoạn từ **split test** (NER chưa thấy khi huấn luyện), loại đoạn trùng nội dung với train và đoạn có hơn ${gt.params.max_pairs} cặp ứng viên. Việc lấy mẫu có chủ đích: mỗi quan hệ có ít nhất ${gt.params.min_per_relation} đoạn chứa cặp đúng kiểu, thêm ${gt.params.no_pair} đoạn có thực thể nhưng không có cặp và ${gt.params.no_entity} đoạn không có thực thể để đo dự đoán dương sai. ${gt.params.double} đoạn được chọn cho người duyệt thứ hai để tính Cohen’s kappa.`),
  T(["Quan hệ", "Số đoạn chứa cặp đúng kiểu", "Số cặp ứng viên"], RELS.map((k) => [k, gt.passages_with_pair_type[k], gt.candidate_pairs[k]]), [3900, 2869, 2869], { right: [1, 2] }),
  CAP("Bảng 3.8. Độ phủ cặp ứng viên trong golden test v1 (nguồn: data/golden_test/v1/manifest.json)."),
  T(["Thành phần", "Số đoạn"], [["Chọn theo hạn mức quan hệ", gt.selection.quota], ["Lấp ngẫu nhiên", gt.selection.random_fill], ["Có thực thể, không có cặp", gt.selection.no_candidate_pair], ["Không có thực thể mục tiêu", gt.selection.no_target_entity]], [6000, 3638], { right: [1] }),
  CAP("Bảng 3.9. Cách lấy mẫu golden test v1."),
  P("Thiết kế phiếu duyệt: NER được điền sẵn từ nhãn gốc của dataset (do người gán), còn nhãn RE để trống để không gây thiên lệch cho người duyệt. Nếu người duyệt sửa NER làm xuất hiện cặp mới, các cặp đó được đưa vào lượt duyệt thứ hai thay vì tự đoán nhãn. Văn bản gold là các token nối bằng một dấu cách để offset trùng với văn bản mà MedicalNERPipeline trả về."),
  P(`Vì người duyệt chưa có thời gian, toàn bộ 150 đoạn đã được AI tiền gán (data/golden_test/v1/ai_labels.jsonl): mỗi thực thể nhận kết luận ĐÚNG/SỬA/XÓA (thực thể chung chung như “triệu chứng”, “điều trị” bị XÓA theo cùng quy ước với gold v1) và mỗi cặp nhận nhãn quan hệ, NO_RELATION hoặc CHUA_RO. Khi đánh giá RE, chỉ giữ cặp mà cả hai thực thể được kết luận ĐÚNG và nhãn không phải CHUA_RO: còn ${re2.data.golden_test.pairs} cặp (${re2.data.golden_test.skip_entity_not_DUNG} cặp bị loại do thực thể không ĐÚNG, ${re2.data.golden_test.skip_unlabelled_or_unclear} cặp CHUA_RO).`),
  T(["Nhãn", "Số cặp"], [...RELS.map((k) => [k, relCount(gtLab, k)]), ["Tổng cặp dương", gtPos], ["NO_RELATION", relCount(gtLab, "NO_RELATION")]], [6000, 3638], { right: [1] }),
  CAP("Bảng 3.10. Nhãn quan hệ của golden test v1 dùng cho đánh giá (nhãn AI tiền gán; nguồn: outputs/re_ai_v2/report.json)."),
  NOTE("Trạng thái hiện tại: golden test v1 có nhãn AI tiền gán nhưng **chưa có bản bác sĩ đã duyệt (gold.jsonl)**. Các kết quả trên golden test ở mục 5.4 vì vậy là tạm thời. Đánh giá dùng thực thể gold (đã duyệt bởi AI), nên đây là RE với thực thể gold, chưa phải RE end-to-end trên thực thể do NER sinh ra."),
  H3("3.4.1. Hai vấn đề phát hiện khi so với baseline, và bản v1.1"),
  P(`Khi đưa các baseline tầm thường vào so sánh (mục 5.4.3), golden test bộc lộ hai vấn đề. Thứ nhất, tập này bị **làm giàu cặp dương**: vì đoạn văn được chọn theo hạn mức quan hệ, ${pct(bench.positive_rate.golden_test_v1)} cặp là dương, trong khi tỉ lệ này trong dữ liệu huấn luyện là ${pct(bench.positive_rate.cv)}. Ở tỉ lệ đó, chỉ cần đoán mọi cặp đúng kiểu là dương cũng đạt F1 ${rp(bench.golden_test_v1_original.cooccur.positive_micro.f1)}. Thứ hai, nhãn AI của golden test được gán ở một phiên trước RE v2 và **không theo đúng một số quy ước** của người duyệt gold v1: chẳng hạn “vitamin d → cao” được gán has_dosage dù “cao” chỉ mức độ, hay cặp nối với DRUG chung chung “thuốc” vẫn được giữ.`),
  P(`Bản v1.1 (data/golden_test/v1/ai_labels_v1_1.jsonl, tạo bởi scripts/golden_test/relabel_consistency.py) đọc lại toàn bộ ${re2.data.golden_test.pairs} cặp chỉ dựa trên văn bản và quy ước, không xem dự đoán của mô hình trên từng cặp, và sửa ${gtChanges.length} cặp (Bảng 3.11). Bản gốc được giữ nguyên và các kết quả được báo cáo trên cả hai bản. Lượt rà này được làm sau khi đã thấy kết quả tổng hợp theo quan hệ, nên vẫn có nguy cơ thiên lệch; vì lý do này, khóa luận xây thêm một tập test thứ hai lấy mẫu ngẫu nhiên (mục 3.6).`),
  T(["Đoạn", "Cặp", "Trước → sau", "Lý do"], gtChanges.map((c) => [c.id, c.rel, `${c.before} → ${c.after}`, c.reason]), [900, 600, 2600, 5538], { size: 17 }),
  CAP(`Bảng 3.11. ${gtChanges.length} thay đổi của golden test v1.1 (XOA = cặp bị loại khỏi đánh giá, như cách gold v1 xử lý thực thể chung chung và sản phẩm ngoài phạm vi).`),
  H2("3.5. Bộ dữ liệu quan hệ bổ sung RE v2 (nhãn AI)"),
  H3("3.5.1. Lý do và cách chọn câu"),
  P(`Gold v1 chỉ có ${posAfter} cặp dương và không có treated_by, has_dosage, nên mô hình không học được hai quan hệ này. Để có thêm dữ liệu mà không chờ người duyệt, khóa luận xây bộ RE v2 từ split train của VietMed-NER. Ràng buộc chống rò rỉ: loại mọi câu trùng nội dung (sau chuẩn hóa) với gold v1 hoặc với split test; kiểm tra lại sau khi tạo cho thấy trùng lặp v1–v2 là ${re2.data.v1_v2_text_overlap} và train–test là ${re2.data.train_test_text_overlap}. Thực thể chung chung bị bỏ trước khi sinh cặp (cùng danh sách GENERIC_ENTITIES), mỗi câu tối đa 6 cặp.`),
  P("Câu được chọn theo hai đợt. Đợt chính (172 câu, 383 cặp) lấy mẫu ngẫu nhiên có hạn mức theo kiểu cặp: 60 câu có cặp CONDITION–DRUG, 50 câu CONDITION–TEST, 45 câu CONDITION–PROCEDURE, 45 câu DRUG–DOSAGE và 30 câu CONDITION–BODY_PART, seed 20261107. Đợt có chủ đích (27 câu, 57 cặp) chỉ lấy câu có liều thật (số kèm mg, ml, viên, lần/ngày…) hoặc có từ gợi ý điều trị (“uống”, “dùng thuốc”, “điều trị bằng”), vì đợt chính cho thấy DOSAGE trong VietMed-NER gần như luôn là từ chỉ mức độ (“cao”, “rất nhiều”) chứ không phải liều."),
  H3("3.5.2. Quy trình gán nhãn hai lượt"),
  P("Nhãn do AI (Claude Opus 5.5) gán theo đúng hướng dẫn docs/RE_LABELS.md và các quy ước của gold v1 (Bảng 3.5), mỗi cặp một nhãn: quan hệ, NO_RELATION hoặc CHUA_RO (? — thiếu ngữ cảnh, bị loại khỏi huấn luyện). Lượt hai không gán lại từ đầu mà kiểm tra theo ba cách độc lập với lượt một:"),
  ...LIST([
    "**Đối chiếu với baseline luật**: rà lại câu chứa từng cặp mà nhãn AI khác dự đoán của luật (45 cặp). Sau khi đọc lại, cả 45 nhãn được giữ nguyên.",
    "**Kiểm tra nhất quán giữa các câu**: tìm cặp cùng chữ head–tail nhưng nhãn khác nhau ở các câu khác nhau (7 trường hợp). Cả 7 đều do ngữ cảnh khác nhau (một câu khẳng định, một câu nói về nguyên nhân), nên được giữ.",
    "**Đọc lại toàn bộ nhãn dương** (39 cặp) cùng ngữ cảnh. Một cặp ở đợt chính được sửa để thống nhất với cặp tương đương ở đợt có chủ đích (thuốc chống đông cho bệnh nhân rung nhĩ → treated_by).",
  ]),
  P(`Một script kiểm tra số nhãn khớp số cặp của từng câu trước khi ghi dữ liệu. Mọi bản ghi mang annotation_status = “AI_LABELED_TWO_PASS”, human_verified = false, training_eligible = false; bộ nạp dữ liệu chỉ nhận chúng khi bật cờ --allow-ai-labels.`),
  T(["Nhãn", "Gold v1 (người duyệt)", "RE v2 (AI)", "Gộp dùng huấn luyện"], [
    ...RELS.map((k) => [k, relCount(re2.data.labels_v1, k), relCount(re2lab, k), relCount(re2.final_model.labels, k)]),
    ["NO_RELATION", relCount(re2.data.labels_v1, "NO_RELATION"), relCount(re2lab, "NO_RELATION"), relCount(re2.final_model.labels, "NO_RELATION")],
    ["Cặp dùng được", re2.data.v1.included_pairs, re2.data.v2.included_pairs, re2.final_model.pairs],
    ["CHUA_RO (loại)", re2.data.v1.unknown_pairs_excluded, re2.data.v2.unknown_pairs_excluded, re2.data.v1.unknown_pairs_excluded + re2.data.v2.unknown_pairs_excluded],
    ["Số câu", re2.data.v1.samples, re2.data.v2.samples, re2.data.v1.samples + re2.data.v2.samples],
  ], [2700, 2300, 2300, 2338], { right: [1, 2, 3] }),
  CAP("Bảng 3.12. Phân bố nhãn của gold v1, RE v2 và bộ gộp dùng để huấn luyện mô hình RE cuối (nguồn: outputs/re_ai_v2/report.json)."),
  P(`Kết quả quan trọng nhất của đợt gán nhãn này là một phát hiện về dữ liệu: dù có hạn mức 45 câu DRUG–DOSAGE và một đợt tìm liều có chủ đích, RE v2 vẫn có ${relCount(re2lab, "has_dosage")} cặp has_dosage dương. Trong lời tư vấn sức khỏe, thuốc hầu như không đi kèm liều cụ thể, còn thực thể DOSAGE do ánh xạ UNITCALIBRATOR chủ yếu là từ chỉ mức độ. treated_by tăng từ 0 lên ${relCount(re2lab, "treated_by")} cặp, đủ để mô hình bắt đầu hỗ trợ quan hệ này nhưng chưa đủ để học ổn định.`),
  H3("3.5.3. Độ tin cậy của nhãn AI: đối chiếu với người duyệt"),
  P("Câu hỏi tự nhiên là nhãn AI đáng tin đến mức nào. Bộ 600 đoạn cho phép trả lời một phần, vì cùng một tập có ba phiên bản nhãn: bản AI nháp, bản AI rà soát (15/10/2026) và gold v1 sau khi người duyệt chốt. Bảng 3.13 so mỗi bản AI với gold v1 trên các cặp có mặt ở cả hai bản (ghép theo vị trí ký tự của hai thực thể) và không phải CHUA_RO."),
  T(["So sánh", "Cặp so được", "Đồng thuận", "Cohen’s kappa", "Kappa dương/âm", "Cặp AI bị loại khi duyệt"], [
    ["Bản AI nháp ↔ gold v1", agree.ai_draft_vs_gold_v1], ["Bản AI rà soát ↔ gold v1", agree.ai_review_vs_gold_v1],
  ].map(([k, v]) => [k, v.compared, pct(v.observed_agreement), f(v.cohen_kappa, 3), f(v.binary.cohen_kappa, 3), `${v.dropped_from_ai}/${v.ai_pairs}`]), [2600, 1200, 1200, 1300, 1400, 1938], { size: 20, right: [1, 2, 3, 4, 5] }),
  CAP("Bảng 3.13. Đồng thuận giữa nhãn AI và nhãn người duyệt trên bộ 600 đoạn (nguồn: outputs/re_ai_v2/agreement.json, scripts/re_dataset/agreement.py)."),
  P(`Trên các cặp còn giữ, AI và người duyệt gần như luôn đồng ý (kappa ${f(agree.ai_review_vs_gold_v1.cohen_kappa, 2)} với bản rà soát). Con số này cần đọc cùng hai lưu ý. Một, người duyệt nhìn thấy nhãn AI khi duyệt, nên đây là cận trên của độ đồng thuận với một người gán độc lập. Hai, khác biệt lớn không nằm ở nhãn quan hệ mà ở **thực thể**: ${agree.ai_draft_vs_gold_v1.dropped_from_ai} trên ${agree.ai_draft_vs_gold_v1.ai_pairs} cặp của bản nháp bị loại vì người duyệt xóa thực thể chung chung (“điều trị”, “thuốc”, “khám”). Nói cách khác, AI gán nhãn quan hệ khá nhất quán khi thực thể đã đúng, còn quy ước về thực thể là chỗ cần con người quyết định. Đây là cơ sở để dùng nhãn AI cho RE v2 và các tập test, với điều kiện áp đúng các quy ước thực thể mà người duyệt đã chốt.`),
  H2("3.6. Tập RE test ngẫu nhiên (nhãn AI)"),
  P(`Để có một phép đo không bị làm giàu cặp dương, khóa luận lấy thêm ${rtMan.chosen_sentences} câu **ngẫu nhiên đều** từ split test của VietMed-NER (scripts/re_dataset/build_random_test.py, seed ${rtMan.seed}), không theo hạn mức quan hệ nào. Nguồn chọn là ${rtMan.pool_sentences_with_pairs} câu có ít nhất một cặp đúng kiểu, sau khi loại các câu thuộc golden test, câu trùng với train và câu lặp; thực thể chung chung bị bỏ như ở RE v2. Phân bố kiểu cặp của mẫu (Bảng 3.14) bám sát phân bố của toàn bộ nguồn chọn, tức đúng với dữ liệu thật.`),
  T(["Kiểu cặp", "Toàn bộ nguồn chọn", "Mẫu 200 câu", "Cặp dương trong mẫu"], RELS.map((k) => [k, rtMan.pool_pairs_by_type[k] || 0, rtMan.pairs_by_type[k] || 0, relCount(rtLab, k)]).concat([["Tổng", rtMan.pool_pairs, rtMan.chosen_pairs, rtPos]]), [2800, 2300, 2200, 2338], { right: [1, 2, 3] }),
  CAP("Bảng 3.14. Tập RE test ngẫu nhiên (nguồn: data/re_test_random_v1/manifest.json và annotations.jsonl)."),
  P(`Nhãn do AI gán một lượt theo đúng hướng dẫn và quy ước của RE v2, trước khi chạy bất kỳ mô hình nào trên tập này. Lượt kiểm tra thứ hai đối chiếu với baseline luật: cả 47 cặp lệch với luật được đọc lại và giữ nguyên. Sau khi loại ${relCount(rtLab, "CHUA_RO") || (rtMan.chosen_pairs - bench.data.random_test_pairs)} cặp CHUA_RO (câu bị cắt, “uống thuốc”/“cho thuốc” chung chung, thực phẩm chức năng, lỗi phiên âm), tập còn ${bench.data.random_test_pairs} cặp với tỉ lệ dương ${pct(bench.positive_rate.golden_test_random_v1)}. Tập này nhỏ và có rất ít diagnosed_by, has_dosage (${relCount(rtLab, "diagnosed_by")} và ${relCount(rtLab, "has_dosage")} cặp dương), nhưng phản ánh đúng những gì hệ thống gặp khi chạy trên văn bản thật.`),
  H2("3.7. Tập gold chuẩn hóa dev/test (nhãn AI)"),
  P(`Để đo chuẩn hóa bằng Accuracy và Top-k như đề cương yêu cầu, khóa luận xây tập gold mã riêng thay vì đo trên bộ RE. Đơn vị là **dạng bề mặt duy nhất** sau chuẩn hóa (chữ thường, gộp khoảng trắng) của thực thể gold CONDITION và DRUG trong VietMed-NER; mỗi dạng có một mã gold hoặc NIL. Đánh giá theo đề cập (mention) được tính thêm bằng cách nhân với tần suất. Dev lấy từ split validation, test từ split test; thực thể lấy từ nhãn gold NER nên lỗi NER không ảnh hưởng phép đo này.`),
  T(["Split", "Nguồn HF", "CONDITION: dạng / đề cập", "DRUG: dạng / đề cập", "ICD-10 có mã / NIL", "RxNorm có mã / NIL"], ["dev", "test"].map((k) => [k, normMan.splits[k].hf_split, `${normMan.splits[k].CONDITION.unique_forms} / ${n(normMan.splits[k].CONDITION.mentions)}`, `${normMan.splits[k].DRUG.unique_forms} / ${normMan.splits[k].DRUG.mentions}`, `${nc("ICD-10", k).n_linkable} / ${nc("ICD-10", k).n_nil}`, `${nc("RxNorm", k).n_linkable} / ${nc("RxNorm", k).n_nil}`]), [900, 1300, 2000, 1800, 1800, 1838], { size: 20, right: [2, 3, 4, 5] }),
  CAP("Bảng 3.15. Tập gold chuẩn hóa (nguồn: data/norm_gold_v1/manifest.json và báo cáo đánh giá)."),
  P(`Cách gán nhãn: mỗi dạng được trình bày kèm tần suất và tối đa ba câu ngữ cảnh; AI gán một hoặc nhiều mã (mã đầu là mã chính, các mã sau cũng được tính đúng) hoặc NIL, có ghi chú. NIL dùng cho từ chung chung (“triệu chứng”, “thuốc”), nhóm thuốc (“thuốc tránh thai”), thứ không phải bệnh hay thuốc (“sữa mẹ”, “di truyền”) và mảnh lỗi NER (“bị tiêu”); trên các dạng NIL, hệ thống được chấm theo tỉ lệ từ chối đúng. ICD-10 được chấm ở hai mức, mã đầy đủ và nhóm 3 ký tự; RxNorm ưu tiên mức hoạt chất (TTY = IN). ${normMan.dev_test_form_overlap.CONDITION} dạng CONDITION và ${normMan.dev_test_form_overlap.DRUG} dạng DRUG xuất hiện ở cả dev và test; các dạng này dùng chung nhãn để hai tập nhất quán.`),
  NOTE("Toàn bộ nhãn là nhãn AI, human_verified = false. Phiếu duyệt data/norm_gold_v1/phieu_duyet_chuan_hoa_{dev,test}.xlsx đã sẵn cho bác sĩ đánh dấu Đồng ý / Sửa mã; script review_sheet.py đọc ngược phiếu và đánh giá được chạy lại bằng một lệnh (Phụ lục B)."),
  H2("3.8. Tổng hợp train / dev / test theo từng bước"),
  P("Bảng 3.16 trả lời câu hỏi “mỗi bước dùng tập nào để học, tập nào để chọn và tập nào để báo cáo”. Nguyên tắc chung: mọi lựa chọn (ngưỡng, alias, cách kết hợp mô hình) được ra trên train hoặc dev; test chỉ được chạy sau khi đã chốt."),
  T(["Bước", "Train (học)", "Dev (chọn, tinh chỉnh)", "Test (báo cáo)", "Nguồn nhãn"], [
    ["NER", "VietMed-NER train (checkpoint kế thừa; baseline từ điển và CRF tự huấn luyện)", "Kế thừa: không rõ (A15); baseline: split validation", `VietMed-NER test, ${n(nerNew.lat.total_samples)} câu`, "Người gán của dataset"],
    ["Chuẩn hóa ICD-10 / RxNorm", "Không học tham số; từ điển chỉ lấy dạng có trong train/dev", `Split validation, ${normMan.splits.dev.CONDITION.unique_forms + normMan.splits.dev.DRUG.unique_forms} dạng`, `Split test, ${normMan.splits.test.CONDITION.unique_forms + normMan.splits.test.DRUG.unique_forms} dạng, chạy một lần`, "AI, chưa duyệt"],
    ["RE", `Gold v1 + RE v2, ${re2.final_model.pairs} cặp (từ split train)`, "CV 5 fold theo nhóm trên chính bộ train", `Golden test v1.1 (${bench.data.golden_test_pairs} cặp) và test ngẫu nhiên (${bench.data.random_test_pairs} cặp), đều từ split test`, "v1: người duyệt; v2 và hai tập test: AI"],
    ["Knowledge graph", "—", "—", `Dựng trên ${n(kgS.documents)} câu split test`, "Dự đoán của hệ thống"],
  ], [1700, 2300, 2000, 2100, 1538], { size: 19 }),
  CAP("Bảng 3.16. Vai trò train/dev/test của từng bước."),
  H2("3.9. Hạn chế của dữ liệu"),
  P(`Dữ liệu có sáu hạn chế. Thứ nhất, đây là lời nói y tế chứ không phải bệnh án: câu ngắn, bị cắt và có lỗi phiên âm. Thứ hai, các bộ RE lấy từ split train nên không dùng được làm test end-to-end, và việc chia theo văn bản không bảo đảm độc lập người nói. Thứ ba, số cặp dương rất ít: gold v1 có ${posAfter}, RE v2 thêm ${re2pos}, và không có cặp has_dosage nào trong dữ liệu huấn luyện. Thứ tư, gold v1 chỉ có một người duyệt và chưa đo kappa; nhãn ban đầu do AI đề xuất nên có nguy cơ người duyệt bị neo theo đề xuất. Thứ năm, bốn bộ mới (RE v2, golden test, test ngẫu nhiên, gold chuẩn hóa) là nhãn AI chưa duyệt, và dữ liệu huấn luyện RE v2 cùng hai tập test do cùng một người gán (AI) theo cùng hướng dẫn, nên sai lệch có hệ thống của người gán sẽ không lộ ra khi đánh giá (mục 6.7). Thứ sáu, golden test bị làm giàu cặp dương do lấy mẫu theo hạn mức, nên F1 trên tập này không so trực tiếp được với F1 trên dữ liệu tự nhiên; tập test ngẫu nhiên được thêm vào để bù. Mỗi hạn chế đều được tính đến khi diễn giải kết quả ở Chương 5 và 6.`),
);

// ===== CHƯƠNG 4 =====
add(
  H1("CHƯƠNG 4. THIẾT KẾ VÀ CÀI ĐẶT HỆ THỐNG"),
  SUM("Hệ thống gồm tám bước nối tiếp, chia thành ba gói Python độc lập. Ba nguyên tắc chi phối thiết kế: mọi thực thể giữ vị trí ký tự trong cùng một văn bản để các bước sau dùng chung tọa độ; chuẩn hóa và RE là hai nhánh độc lập để lỗi ở nhánh này không chặn nhánh kia; và hệ thống luôn phân biệt “không có” với “không biết” (không gán mã, trạng thái unsupported, thực thể bị bỏ qua có đánh dấu)."),
  H2("4.1. Kiến trúc tổng thể"),
  P("Hệ thống được tổ chức thành ba gói Python độc lập: `ner/`, `normalization/` và `relation_extraction/`, cùng gói `eval/` cho đánh giá và thư mục `scripts/` cho công cụ dữ liệu. Lớp `MedicalNERPipeline` (ner/pipeline.py) là điểm vào cho NER và chuẩn hóa; `MedicalREPipeline` (relation_extraction/pipeline.py) nhận kết quả NER và bổ sung quan hệ. Chuẩn hóa và RE là hai nhánh song song: lỗi tra mã không làm RE dừng, và RE không phụ thuộc vào việc thực thể có mã hay không."),
  T(["Bước", "Mô-đun", "Đầu vào → Đầu ra"], [
    ["1. Tiền xử lý", "ner/preprocessor.py", "Văn bản thô → văn bản chuẩn hóa khoảng trắng, danh sách token có offset, các chunk theo câu"],
    ["2. Suy luận NER", "ner/predictor.py", "Chunk → thực thể thô theo 37 nhãn BIO, ánh xạ sang 6 loại, kèm độ tin cậy"],
    ["3. Luật liều lượng", "ner/dosage_extractor.py", "Văn bản + thực thể → bổ sung/gộp DOSAGE (giá trị, đơn vị, dạng, tần suất)"],
    ["4. Hậu xử lý", "ner/postprocessor.py", "Lọc schema, Luật 1/1b/2, giải quyết chồng lấn theo độ tin cậy"],
    ["5. Chuẩn hóa", "normalization/dispatcher.py", "CONDITION → ICD-10; DRUG → RxNorm; BODY_PART/TEST/PROCEDURE → stub; DOSAGE bỏ qua"],
    ["6. Lọc đầu vào RE", "relation_extraction/pipeline.py", "Bỏ thực thể chung chung khỏi bước sinh cặp (vẫn giữ trong đầu ra)"],
    ["7. Sinh cặp RE", "relation_extraction/data.py", "Thực thể → cặp (head, tail) đúng kiểu/chiều, chèn marker"],
    ["8. Phân loại quan hệ", "relation_extraction/model.py, rules.py, knowledge_graph/extract.py", "Cặp → nhãn quan hệ hoặc NO_RELATION, điểm tin cậy, trạng thái, nguồn (model/rule)"],
    ["9. Knowledge graph", "knowledge_graph/graph.py, visualize.py", "Kết quả nhiều văn bản → nút gộp theo mã, cạnh gộp theo bộ ba; JSON/CSV/GraphML/HTML"],
  ], [1800, 2900, 4938]),
  CAP("Bảng 4.1. Luồng xử lý đầu–cuối."),
  T(["Gói / tệp", "Số dòng", "Thành phần chính"], [
    ["ner/config.py", "137", "Schema 6 loại, bảng ánh xạ, danh sách luật, giới hạn độ dài"],
    ["ner/preprocessor.py", "171", "WordToken, TextChunk, TextPreprocessor (normalize_whitespace, tokenize_words, chunk_tokens)"],
    ["ner/predictor.py", "237", "ModelNERPredictor (predict_chunk, _map_tag_to_target, _decode_bio_spans)"],
    ["ner/dosage_extractor.py", "348", "DosageExtractor (extract_regex_dosages, _parse_dosage_components, merge_with_model_entities)"],
    ["ner/postprocessor.py", "293", "PostProcessor (filter_schema, filter_drug_blacklist, relabel_lab_tests_from_drug, merge_severity_into_condition, filter_and_resolve_overlaps)"],
    ["ner/pipeline.py", "185", "MedicalNERPipeline (predict, normalize_entities)"],
    ["ner/logger.py", "158", "NERPipelineLogger: nhật ký theo giai đoạn"],
    ["normalization/icd10.py", "428", "ICD10Normalizer (_load_catalog, _load_synonyms, normalize, _fuzzy_search, candidates)"],
    ["normalization/rxnorm.py", "352", "RxNormNormalizer (alias Việt→Anh, bỏ tiền tố dạng bào chế, approximateTerm có ngưỡng, cache SQLite)"],
    ["normalization/dispatcher.py", "197", "EntityNormalizationPipeline: định tuyến theo loại, chế độ strict/always, top-k ứng viên"],
    ["normalization/base.py, stubs.py", "93", "NormalizedResult, BaseNormalizer, FMA/LOINC/MeSH stub"],
    ["relation_extraction/data.py", "≈150", "Schema, GENERIC_ENTITIES, candidates, mark_pair, load_pairs, split_pairs"],
    ["relation_extraction/model.py", "79", "RelationExtractor (TF-IDF + LogReg), evaluate"],
    ["relation_extraction/rules.py", "65", "RuleRelationExtractor"],
    ["relation_extraction/pipeline.py", "≈40", "MedicalREPipeline"],
    ["eval/*.py", "≈1.000", "Đánh giá tầng 1/tầng 2, metric, ma trận nhầm lẫn, độ trễ"],
    ["knowledge_graph/*.py", "337", "HybridRelationExtractor, KnowledgeGraph (add_document, neighbors, find, save), write_html"],
    ["scripts/normalization_eval/*.py", "573", "Tạo ứng viên, ghép nhãn, đánh giá Accuracy/Top-k/MRR, phiếu duyệt"],
    ["scripts/re_dataset/*.py", "432", "Chọn câu RE v2, ghép nhãn, huấn luyện và so sánh trên CV + golden test"],
  ], [3000, 900, 5738], { size: 20, right: [1] }),
  CAP("Bảng 4.2. Các mô-đun chính (số dòng đếm ngày 05/11/2026; các tệp chuẩn hóa và ba dòng cuối đếm lại ngày 07/11/2026)."),
  H2("4.2. Tiền xử lý"),
  P("Văn bản được chuẩn hóa khoảng trắng (thay khoảng trắng không ngắt và tab, gộp nhiều dấu cách, giới hạn dòng trống) mà không sửa số, đơn vị hay ký hiệu y khoa. Sau đó văn bản được tách token bằng biểu thức chính quy `\\w+|[^\\w\\s]`, trong đó mỗi dấu câu là một token riêng để không dính vào thực thể (“dạ dày,” → “dạ”, “dày”, “,”). Mỗi token giữ vị trí ký tự trong văn bản đã chuẩn hóa."),
  P("Văn bản dài được chia thành chunk theo số token: tách ở dấu kết thúc câu (“.”, “!”, “?”, “;”) khi chunk đã có từ 35 token (hoặc 15 token nếu phần còn lại đủ dài), tách ở dấu ngắt mệnh đề khi đạt 120 token, và cắt cứng ở 140 token; không bao giờ tách giữa một token. Ở bước suy luận, nếu chuỗi subword của chunk vượt 258 vị trí (max_position_embeddings) thì bị cắt và ghi cảnh báo."),
  ...CODE([
    "chunk_tokens(tokens, max_words=120):",
    "  cur = []",
    "  for i, tok in enumerate(tokens):",
    "    cur.append(tok)",
    "    end = tok in {'.', '!', '?', ';'};  clause = tok in {',', ':', '-', '–', '—'}",
    "    if (end and len(cur) >= 35) or (end and len(cur) >= 15 and còn >= 15 token)",
    "       or (clause and len(cur) >= max_words) or len(cur) >= max_words + 20 or i là token cuối:",
    "      phát chunk(cur, start=cur[0].start, end=cur[-1].end);  cur = []",
  ]),
  CAP("Mã giả 4.1. Chia chunk (ner/preprocessor.py)."),
  NOTE("Khi soát mã nguồn phát hiện hai điểm khác với mô tả cũ: hằng số MAX_SUBTOKENS_PER_CHUNK = 200 được khai báo và import nhưng không dùng — việc chia thực tế theo số token như trên; và “\\n” có trong tập dấu kết thúc câu nhưng biểu thức tách token bỏ qua mọi khoảng trắng nên xuống dòng không bao giờ kích hoạt tách câu (Phụ lục A, A17–A18). Với dữ liệu VietMed-NER (trung bình 22 từ/câu) hai điểm này không ảnh hưởng kết quả, nhưng cần xử lý khi áp dụng cho văn bản dài."),
  H2("4.3. Mô hình NER"),
  P("Checkpoint `vihealthbert-ner-vietmed-v2-final` là mô hình kế thừa, không được huấn luyện lại trong khóa luận. Siêu tham số đọc từ training_args.bin (bằng unpickler không thực thi mã) được tổng hợp ở Bảng 4.3."),
  T(["Tham số", "Giá trị"], [
    ["Mô hình nền", trainArgs.base_model], ["Dữ liệu", trainArgs.dataset],
    ["Learning rate", trainArgs.learning_rate === 5e-5 ? "5 × 10⁻⁵" : String(trainArgs.learning_rate)], ["Số epoch tối đa", String(trainArgs.num_train_epochs)],
    ["Batch size (train/eval)", `${trainArgs.per_device_train_batch_size}/${trainArgs.per_device_eval_batch_size}`],
    ["Weight decay", String(trainArgs.weight_decay).replace(".", ",")], ["Scheduler / warmup", `${trainArgs.lr_scheduler_type} / ${trainArgs.warmup_steps}`],
    ["Optimizer", trainArgs.optim], ["fp16", String(trainArgs.fp16)], ["Seed", String(trainArgs.seed)],
    ["Chọn checkpoint", `${trainArgs.eval_strategy}; load_best_model_at_end=${trainArgs.load_best_model_at_end}; metric=${trainArgs.metric_for_best_model}`],
    ["Chưa ghi nhận", trainArgs.not_recorded_here.join("; ")],
  ], [3000, 6638]),
  CAP("Bảng 4.3. Cấu hình huấn luyện checkpoint NER (nguồn: docs/ner_training_args.json)."),
  P("Khi suy luận, mỗi token được tách thành subword bằng tokenizer của checkpoint; <s> và </s> được thêm ở hai đầu. Mô hình trả logits cho từng subword; softmax cho xác suất và nhãn có xác suất cao nhất. Các vị trí token đặc biệt bị loại trước khi giải mã BIO, vì không có gradient ở các vị trí này lúc huấn luyện nên nhãn có thể ngẫu nhiên. Nhãn của một từ lấy theo subword đầu tiên; độ tin cậy của từ là trung bình xác suất của các subword. Nhãn gốc được ánh xạ sang sáu loại (loại khác thành O) trước khi giải mã thành span."),
  ...CODE([
    "predict_chunk(chunk):",
    "  subs, word_of = [], []",
    "  for w_idx, word in enumerate(chunk.words):",
    "    for piece in tokenizer.tokenize(word.text) or [unk]:  subs.append(piece); word_of.append(w_idx)",
    "  ids = ['<s>'] + subs + ['</s>']  (cắt ở 258 nếu dài hơn)",
    "  probs = softmax(model(ids).logits);  conf, pred = max(probs)",
    "  bỏ vị trí đặc biệt; gom theo từ:",
    "  tag[w] = map6(id2label[pred của subword đầu]);  conf[w] = mean(conf các subword)",
    "  return decode_bio(chunk.words, tag, conf)   # span ký tự + độ tin cậy trung bình",
  ]),
  CAP("Mã giả 4.2. Suy luận NER cho một chunk (ner/predictor.py)."),
  H2("4.4. Luật nhận diện liều lượng"),
  P("DosageExtractor dùng biểu thức chính quy cho ba thành phần: giá trị số (kể cả “nửa”, “một”, “hai”, “ba”, khoảng “1-2”), đơn vị hàm lượng/thể tích (mg, mcg, g, ml, l, UI, IU, %, mg/ml, …) hoặc dạng bào chế (viên, ống, gói, chai, lọ, giọt, nang, …), và tần suất (“/ngày”, “2 lần/ngày”, “ngày 3 lần”, “3 lần mỗi ngày”, “cách 8 giờ”, “sáng … tối …”). Mẫu tổng hợp bắt được cụm như “500mg 2 viên/ngày” và tách thành giá trị, đơn vị, tần suất. Các cụm do luật tìm được được gộp với thực thể UNITCALIBRATOR của mô hình; khi chồng lấn, cụm đầy đủ hơn được giữ."),
  T(["Văn bản", "Thành phần trích được"], [["500mg", "giá trị 500, đơn vị mg"], ["2 viên/ngày", "giá trị 2, dạng viên, tần suất /ngày"], ["ngày 3 lần", "tần suất"], ["cách 8 giờ", "tần suất"]], [3500, 6138]),
  CAP("Bảng 4.4. Ví dụ cụm liều mà luật nhận diện (từ bộ kiểm thử tests/test_ner_pipeline.py và mẫu FREQ_PATTERN)."),
  H2("4.5. Hậu xử lý"),
  B("**Lọc schema**: chỉ giữ sáu loại mục tiêu."),
  B("**Luật 1**: bỏ thực thể DRUG trùng khớp (không phân biệt hoa thường) với các từ hành động “chỉ định”, “can thiệp”, “kê đơn”, “điều trị”, thường bị gán DRUG vì đứng cạnh tên thuốc trong dữ liệu huấn luyện."),
  B("**Luật 1b**: đổi DRUG thành TEST nếu là tên xét nghiệm đã biết (men tim, men gan, troponin, HbA1c, CRP, CK-MB, creatinin, ure, công thức máu, đường huyết). Luật được thêm sau khi thấy “men tim”, “Troponin T” trong nhật ký thuốc không tra được mã RxNorm."),
  B("**Luật 2**: gộp tính từ mức độ (“cao”, “nhẹ”, “nặng”, “vừa”, “nhẹ nhàng”) bị gán DOSAGE vào CONDITION đứng ngay trước, cách đúng một dấu cách (“sốt cao”); độ tin cậy là trung bình của hai thực thể."),
  B("**Giải quyết chồng lấn**: sắp xếp theo độ tin cậy rồi độ dài span giảm dần, lần lượt nhận thực thể nếu không chồng lấn với thực thể đã nhận; kết quả được sắp lại theo vị trí."),
  ...CODE([
    "filter_and_resolve_overlaps(ents, text):",
    "  ents = filter_schema(ents)                 # 6 loại",
    "  ents = filter_drug_blacklist(ents)         # Luật 1",
    "  ents = relabel_lab_tests_from_drug(ents)   # Luật 1b",
    "  ents = merge_severity_into_condition(ents, text)  # Luật 2",
    "  kept = []",
    "  for e in sorted(ents, key=(-conf, -(end-start))):",
    "    if không chồng lấn với mọi k trong kept: kept.append(e)",
    "  return sorted(kept, key=start)",
  ]),
  CAP("Mã giả 4.3. Hậu xử lý (ner/postprocessor.py)."),
  H2("4.6. Chuẩn hóa mã"),
  H3("4.6.1. ICD-10"),
  P("Danh mục Excel của Bộ Y tế được đọc một lần và lưu vào cache (12.218 mã, 12.059 tên bệnh duy nhất sau chuẩn hóa). Tên được chuẩn hóa (chữ thường, bỏ dấu câu, gộp khoảng trắng) trước khi so khớp. Quy trình tra theo thứ tự ưu tiên:"),
  ...LIST([
    "Khớp chính xác với tên trong danh mục.",
    "Từ điển đồng nghĩa: alias trực tiếp (33 alias sau bản sửa ngày 06/11/2026, 170 alias sau bản cải tiến ngày 07/11/2026 — 137 alias thêm vào chỉ lấy từ dạng có trong train/dev) và mẫu biến đổi (“ung thư X” → “u ác của X”, “u lành X” → “u lành của X”).",
    "Khớp gần đúng bằng rapidfuzz token_set_ratio với ngưỡng ≥ 0,85, kèm sáu ràng buộc an toàn (Bảng 4.5).",
    "Không đạt thì trả về không có mã — thiết kế ưu tiên không gán mã hơn là gán sai.",
  ]),
  T(["Ràng buộc", "Mục đích", "Ví dụ bị chặn"], [
    ["Tỉ lệ độ dài ≥ 0,60", "Tránh khớp chuỗi rất ngắn với tên dài", "“viêm” với tên dài chứa “viêm”"],
    ["Jaccard ≥ 0,40 khi cả hai ≤ 3 từ", "Tránh nhầm triệu chứng gần giống", "“đau bụng” với “đau lưng”"],
    ["Bỏ từ định tính rồi so lại", "Tránh khớp chỉ nhờ “không xác định”, “bệnh”", "“bệnh abc” với “bệnh … không xác định”"],
    ["**Từ đầu cụm của ứng viên phải có trong truy vấn** (06/11)", "Tránh tập con khác nghĩa", "“huyết áp cao” với “đo huyết áp”; “đa xơ cứng” với “gan xơ cứng”"],
    ["**Tập con thực sự với chuỗi ngắn ≤ 2 từ bị từ chối** (06/11)", "Từ thêm quyết định bệnh", "“nhồi máu” với “nhồi máu lách”; “đậu mùa bò” với “đậu mùa”"],
    ["**Mọi từ nội dung của ứng viên phải có trong truy vấn** (07/11; so sánh bỏ dấu, ratio ≥ 80; bỏ qua từ đệm như “bệnh”, “không xác định”, “cấp”, “mạn tính”)", "Ứng viên không được thêm khái niệm mà người nói không nhắc", "“rối loạn vận động” với “rối loạn vận động phân ly” (F44.4)"],
  ], [3200, 3000, 3438], { size: 20 }),
  CAP("Bảng 4.5. Các ràng buộc an toàn của bước khớp gần đúng (normalization/icd10.py, _fuzzy_search)."),
  ...CODE([
    "normalize(surface):",
    "  q = clean(surface)",
    "  if q in exact_map:            return (code, 'exact', 1.0)",
    "  if q in direct_aliases:       return (alias.code, 'synonym', 1.0)",
    "  for pattern in synonym_patterns: if match → tra lại (exact / u ác của cơ quan / fuzzy)",
    "  best = extractOne(q, catalog, token_set_ratio, cutoff=85)",
    "  if best và qua mọi ràng buộc ở Bảng 4.5: return (best.code, 'fuzzy', score)",
    "  return None",
  ]),
  CAP("Mã giả 4.4. Chuẩn hóa ICD-10."),
  H3("4.6.2. RxNorm"),
  P("Tên thuốc được làm sạch (bỏ hàm lượng, dạng bào chế) rồi tra qua RxNav REST (`/REST/rxcui.json`, lấy tên chuẩn qua `/REST/rxcui/{id}/property.json`), timeout 5 giây, thử lại tối đa 3 lần với backoff lũy thừa. Kết quả (kể cả không tìm thấy) được lưu vào cache SQLite để chạy lại không cần mạng; thuốc không tra được được ghi vào unmatched_drugs.log để bổ sung luật hoặc từ điển."),
  P("Bản cải tiến ngày 07/11/2026 (chọn trên dev) thêm ba bước trước khi bỏ cuộc. Thứ nhất, từ điển Việt → Anh gồm 31 mục (normalization/data/rxnorm_vi_aliases.json, ví dụ “canxi” → calcium, “sắt” → iron, “đông trùng hạ thảo” → Cordyceps sinensis), chỉ lấy dạng có trong train/dev và mỗi giá trị đều đã được kiểm tra là RxNav tra chính xác được. Thứ hai, bỏ từ đứng đầu chỉ dạng bào chế hoặc vật chứa (“viên nang”, “chai”, “thuốc”, “hoạt chất”, “vị”…) rồi tra lại. Thứ ba, gọi `/REST/approximateTerm.json` và chỉ chấp nhận ứng viên top-1 khi tên gần như trùng (ratio ≥ 90), để bắt lỗi chính tả mà không đoán bừa; mười ứng viên đầu của approximateTerm được giữ làm danh sách top-k."),
  H3("4.6.3. Các loại chưa chuẩn hóa và điều phối"),
  P("BODY_PART (FMA), TEST (LOINC) và PROCEDURE (MeSH) có lớp stub kế thừa BaseNormalizer, trả về không có mã với phương thức “not_implemented”, để mở rộng sau mà không đổi giao diện. DOSAGE bỏ qua chuẩn hóa. EntityNormalizationPipeline định tuyến từng thực thể theo loại, nạp lười (lazy) từng normalizer, bắt mọi ngoại lệ để một lỗi tra mã không làm hỏng cả kết quả, và ghi nhật ký thời gian xử lý từng thực thể."),
  H3("4.6.4. Hai chế độ trả lời và danh sách top-k"),
  P("Thiết kế “không gán mã còn hơn gán sai” cho precision cao nhưng để trống nhiều thực thể. Vì người dùng khác nhau cần khác nhau, bộ điều phối có hai chế độ. Chế độ **thận trọng** (strict, mặc định) chỉ gán mã khi một trong các bước exact, đồng nghĩa hoặc fuzzy có ràng buộc ra quyết định. Chế độ **luôn trả lời** (always) dùng quyết định đó nếu có, nếu không thì lấy ứng viên xếp hạng đầu; chế độ này phù hợp khi luôn có người xác nhận phía sau."),
  P("Ở cả hai chế độ, mỗi thực thể CONDITION và DRUG còn mang trường `candidates` gồm k ứng viên (mặc định k = 5), mỗi ứng viên có thứ hạng, mã, tên chuẩn, cách khớp và điểm. Ứng viên đầu là quyết định của hệ thống nếu có. Phần còn lại, với ICD-10, xếp hạng bằng TF-IDF n-gram ký tự 2–4 (analyzer char_wb) trên tên trong danh mục cộng với các alias, khử trùng theo mã; cách này được chọn vì trên dev tốt hơn WRatio, token_set_ratio và n-gram từ. Với RxNorm, ứng viên lấy từ approximateTerm. Ứng viên do xếp hạng sinh ra có match_method = “retrieval”, nên chế độ thận trọng không bao giờ coi chúng là quyết định."),
  ...CODE([
    "_decide(normalizer, surface, top_k, mode):",
    "  cands = normalizer.candidates(surface, k=max(top_k, 1))   # quyết định (nếu có) đứng đầu",
    "  if not cands: return None, []",
    "  if mode == 'always' or cands[0].match_method != 'retrieval': decision = cands[0]",
    "  else: decision = None          # chế độ thận trọng không nhận ứng viên xếp hạng",
    "  return decision, cands[:top_k]",
  ]),
  CAP("Mã giả 4.5. Quyết định và danh sách top-k (normalization/dispatcher.py)."),
  H2("4.7. Trích xuất quan hệ"),
  H3("4.7.1. Lọc thực thể chung và sinh cặp"),
  P("Trước khi sinh cặp, MedicalREPipeline đánh dấu các thực thể thuộc danh sách GENERIC_ENTITIES (so khớp sau chuẩn hóa Unicode NFC, chữ thường, gộp khoảng trắng) bằng trường `re_excluded = \"generic_entity\"`. Các thực thể này vẫn có trong đầu ra (để chuẩn hóa và hiển thị) nhưng không tham gia sinh cặp, nhờ đó đầu vào RE lúc suy luận khớp với quy ước của dữ liệu huấn luyện. Có thể tắt bằng tham số `skip_generic=False`."),
  P("Với mỗi đoạn, mọi cặp (head, tail) có kiểu trùng một dòng của schema được sinh thành ứng viên, giữ đúng chiều kể cả khi head đứng sau tail trong câu. Trước đó, thực thể được kiểm tra: ID không trùng, offset hợp lệ, loại thuộc schema, văn bản khớp offset và không có span chồng lấn. Cặp được biểu diễn bằng cách chèn marker có loại thực thể quanh hai đầu mút, chèn từ cuối về đầu để không làm lệch offset:"),
  ...CODE(["[HEAD_CONDITION]đau[/HEAD] ở [TAIL_BODY_PART]vùng bụng[/TAIL], được điều trị bằng phẫu thuật."]),
  H3("4.7.2. Baseline luật"),
  P("Baseline luật (relation_extraction/rules.py) được viết từ hướng dẫn gán nhãn, không tinh chỉnh trên dữ liệu. Một cặp được dự đoán dương khi thỏa cả ba điều kiện: khoảng cách giữa hai thực thể không vượt ngưỡng; đoạn chữ ở giữa chứa từ gợi ý của quan hệ (hoặc tail đứng ngay sau head với located_at và has_dosage); và không có thực thể cùng loại với head hoặc tail chen giữa."),
  T(["Quan hệ", "Khoảng cách tối đa (từ)", "Từ gợi ý"], [
    ["located_at", "4", "ở, tại, vùng, trong, của, phía, bên, khu vực, chỗ, lan; hoặc liền kề"],
    ["treated_by", "8", "điều trị, chữa, trị, bằng, dùng, uống, tiêm, bôi, kê, cho thuốc, sử dụng"],
    ["treated_by_procedure", "8", "điều trị, chữa, trị, bằng, phương pháp, can thiệp, tiến hành, thực hiện, sử dụng"],
    ["diagnosed_by", "8", "chẩn đoán, phát hiện, xác định, cho thấy, thấy, qua, bằng, kiểm tra, tầm soát, làm"],
    ["has_dosage", "3", "(không có từ gợi ý; chỉ liền kề)"],
  ], [2400, 2000, 5238], { size: 20 }),
  CAP("Bảng 4.6. Tham số baseline luật."),
  H3("4.7.3. Mô hình học máy"),
  P(`Mô hình chính hiện tại là TF-IDF n-gram ký tự (2–5, sublinear tf, tối đa 50.000 đặc trưng) trên câu có marker, kết hợp Logistic Regression cân bằng lớp (C = 1, max_iter = 2.000). Với mỗi cặp, điểm của nhãn dương hợp lệ p⁺ và của NO_RELATION p⁻ được chuẩn hóa thành s = p⁺ / (p⁺ + p⁻); cặp được dự đoán dương khi s ≥ 0,5. Quan hệ không có mẫu dương trong tập train được trả về trạng thái “unsupported” (label = null) thay vì coi là âm. Môi trường: Python ${reGoldRun.metadata.python}, scikit-learn ${reGoldRun.metadata.sklearn}.`),
  NOTE("Kế hoạch ban đầu là tinh chỉnh ViHealthBERT có typed markers cho RE. Với chỉ " + posAfter + " cặp dương sau duyệt, mô hình encoder lớn khó học ổn định và khó đánh giá; đây là lý do chọn mô hình tuyến tính nhẹ làm mô hình chính ở giai đoạn này. Mã sinh cặp và marker đã tương thích với hướng encoder khi có thêm dữ liệu."),
  P(`Mô hình RE cuối (outputs/re_ai_v2/model.joblib) giữ nguyên kiến trúc trên nhưng học trên ${re2.final_model.pairs} cặp của gold v1 và RE v2, nên hỗ trợ bốn quan hệ: ${re2.final_model.supported_relations.join(", ")}. has_dosage vẫn chưa có mẫu dương nên mô hình trả về unsupported cho quan hệ này.`),
  P(`Khi đã có thêm RE v2, khóa luận thử lại hướng encoder (scripts/re_dataset/bert_re.py). Câu có marker được đưa vào ViHealthBERT (demdecuong/vihealthbert-base-syllable); 12 marker loại thực thể được thêm vào bộ từ vựng như token đặc biệt. Biểu diễn của cặp là nối trạng thái ẩn tại marker mở đầu của head và của tail, như Baldini Soares và cộng sự (2019) và Zhong và Chen (2021), qua dropout và một lớp tuyến tính hai lớp (NO_RELATION / dương). Vì mỗi cặp chỉ có một quan hệ hợp lệ theo kiểu thực thể, “dương” chính là quan hệ đó. Siêu tham số được cố định trước khi chạy: ${bench.bert_meta.epochs} epoch, learning rate ${String(bench.bert_meta.lr).replace(".", ",")}, batch ${bench.bert_meta.batch}, độ dài tối đa ${bench.bert_meta.max_len}, trọng số lớp dương bằng tỉ lệ âm/dương. Mỗi cấu hình chạy ${bench.bert_meta.seeds.length} seed, xác suất được lấy trung bình và ngưỡng là 0,5. Huấn luyện trên GPU ${bench.bert_meta.device}.`),
  H3("4.7.4. Kết hợp mô hình với luật"),
  P("Mô hình và luật mạnh ở những chỗ khác nhau: luật có precision cao với các mẫu câu điển hình (“đau ở vùng bụng”), còn mô hình bắt được cách nói không có từ gợi ý. Lớp HybridRelationExtractor (knowledge_graph/extract.py) kết hợp hai nguồn theo một trong hai chế độ. Ở chế độ **fallback**, mô hình quyết định với quan hệ nó hỗ trợ, luật chỉ dùng cho quan hệ mô hình trả về unsupported (has_dosage). Ở chế độ **union**, một cặp là dương khi mô hình hoặc luật nói dương. Với mô hình TF-IDF, chế độ union được chọn làm mặc định vì có F1 cao nhất trong cross-validation; golden test không được dùng để chọn. Với ViHealthBERT, CV không phân biệt được mô hình một mình và union (mục 5.4.3). Mỗi dự đoán mang trường `source` (“model” hoặc “rule”) để người dùng và đồ thị biết cạnh đến từ đâu."),
  ...CODE([
    "predict(text, entities):",
    "  rule = {(head, tail, rel): p  for p in rules.predict(text, entities)}",
    "  for p in model.predict(text, entities):",
    "    r = rule[(p.head, p.tail, p.rel)]",
    "    if p.status == 'unsupported' or (mode == 'union' and p không dương and r dương):",
    "      yield r với source = 'rule'",
    "    else:",
    "      yield p với source = 'model'",
  ]),
  CAP("Mã giả 4.6. Kết hợp mô hình và luật (knowledge_graph/extract.py)."),
  H3("4.7.5. Chia dữ liệu và chống rò rỉ"),
  P("Các cặp được nhóm theo văn bản đã chuẩn hóa (NFC, chữ thường, gộp khoảng trắng) bằng SHA-256; mọi cặp cùng nhóm nằm cùng một tập. Tỉ lệ 70/15/15; trước khi chia, mỗi nhãn được dành một nhóm trong train để mô hình có lớp đó. Cross-validation 5 fold cũng chia theo nhóm; khoảng tin cậy 95% tính bằng bootstrap 1.000 lần theo nhóm. Cặp CHUA_RO bị loại; không tự sinh mẫu âm từ cặp vắng mặt."),
  ...CODE([
    "split_pairs(pairs, seed):",
    "  groups = gom pairs theo sha256(normalize(text));  keys = shuffle(sorted(groups), seed)",
    "  reserved = {}",
    "  for label theo thứ tự ít nhóm nhất: nếu chưa có nhóm nào của label trong reserved → thêm nhóm đầu tiên",
    "  remaining = keys \\ reserved;  h = round(0.15 · |keys|)",
    "  dev = remaining[:h];  test = remaining[h:2h];  train = reserved ∪ remaining[2h:]",
  ]),
  CAP("Mã giả 4.7. Chia dữ liệu RE theo nhóm (relation_extraction/data.py)."),
  H2("4.8. Định dạng đầu ra và ví dụ"),
  P("Kết quả là JSON gồm `text`, `entities` (surface_text, label, start_char, end_char, confidence, normalized, và re_excluded nếu có) và với RE thêm `relations` (cạnh dương), `relation_candidates` (mọi cặp, kèm nhãn, điểm và trạng thái) cùng `re_metadata` (nguồn nhãn, quan hệ được hỗ trợ, thực thể bị bỏ qua). Ví dụ thật từ lượt chạy NER → RE với mô hình gold v1:"),
  ...CODE([`Văn bản: "${demo.text}"`, ...demo.entities.map((e) => `  ${e.id} [${e.label}] "${e.surface_text}" (${e.start_char}–${e.end_char}, conf=${e.confidence})${e.re_excluded ? "  ← bỏ qua khi sinh cặp (thực thể chung)" : ""}`),
    ...demo.relation_candidates.map((c) => `  ${c.head} → ${c.tail} (${c.allowed_relation}): ${c.label}${c.score !== undefined && c.score !== null ? ", score=" + Number(c.score).toFixed(3) : ""}`)]),
  CAP("Ví dụ 4.1. Đầu ra demo với mô hình gold v1 (outputs/re_gold_v1_baseline/demo_ner_re.json)."),
  P(`So sánh với lượt chạy cũ dùng mô hình huấn luyện trên nhãn AI (outputs/re_ai_baseline/seed42/demo_ner_re.json): mô hình cũ nối “đau” với cả “điều trị” lẫn “phẫu thuật” và bỏ sót located_at giữa “đau” và “vùng bụng”. Sau khi lọc thực thể chung và huấn luyện trên gold v1, hệ thống trả về đúng hai quan hệ mong đợi. Đây là một ví dụ minh họa, không phải bằng chứng thống kê.`),
  H2("4.9. Kiểm thử phần mềm"),
  P(`Bộ kiểm thử pytest gồm bảy tệp với ${nTests} ca (danh sách đầy đủ ở Phụ lục J): test_ner_pipeline.py (tách từ, dấu câu, ánh xạ 6 nhãn, liều “500mg 2 viên/ngày”, câu rỗng, câu không y tế, văn bản dài), test_normalization.py (“đau bụng” → R10 không nhầm “đau lưng”, các ca sai trong audit cũ, các ca tập con khác nghĩa phát hiện ngày 05/11, RxNorm có mock, cache, stub), test_end_to_end_pipeline.py (toàn luồng, bật/tắt chuẩn hóa) và test_relation_extraction.py (opt-in nhãn AI, loại CHUA_RO, kiểm tra offset/chiều/ID, chia nhóm không rò, marker giữ chiều, lưu/nạp mô hình, metric đếm tay, lọc thực thể chung). Hai tệp thêm ngày 07/11/2026: test_normalization_eval.py (đếm tay Accuracy, coverage, precision khi trả lời, từ chối đúng NIL, Top-k và MRR, cả chế độ luôn trả lời) và test_knowledge_graph.py (gộp nút theo mã, cộng dồn cạnh, lọc CONDITION chung, xuất JSON/CSV/GraphML/HTML, chế độ union và fallback). test_normalization.py có thêm các ca top-k, alias thuốc, approximateTerm có ngưỡng và hai chế độ.`),
  H2("4.10. Các quyết định thiết kế quan trọng"),
  T(["Vấn đề gặp phải", "Quyết định"], [
    ["Mô hình tự tin gán “bệnh nhân” là OCCUPATION", "Loại hẳn các loại phi y khoa thay vì giữ nhãn OTHER"],
    ["`text.split()` làm dấu câu dính vào thực thể", "Tách token bằng biểu thức chính quy, dấu câu là token riêng"],
    ["Token đặc biệt mang nhãn ngẫu nhiên", "Loại vị trí đặc biệt trước khi giải mã BIO"],
    ["Fuzzy ICD-10 ngưỡng 0,6 gán sai nghiêm trọng", "Ngưỡng 0,85 + từ điển đồng nghĩa + các ràng buộc an toàn"],
    ["Import torch trên Windows có thể treo do OpenMP", "Đặt KMP_DUPLICATE_LIB_OK=TRUE, OMP_NUM_THREADS=1 trước khi import"],
    ["Nhãn AI có thể bị nhầm là gold", "Cờ human_verified/training_eligible; opt-in tường minh khi dùng nhãn AI"],
    ["Cặp chưa duyệt bị coi là âm", "Không sinh âm từ cặp vắng mặt; CHUA_RO bị loại"],
  ], [4600, 5038], { size: 20 }),
  CAP("Bảng 4.7. Các quyết định thiết kế (nguồn: PROJECT_CONTEXT.md và lịch sử dự án)."),
  H2("4.11. Knowledge graph"),
  P("Knowledge graph (đồ thị tri thức) là bước cuối của pipeline: kết quả của từng văn bản là một danh sách bộ ba (thực thể đầu, quan hệ, thực thể cuối); đồ thị gộp các bộ ba của mọi văn bản lại, sao cho cùng một khái niệm chỉ là một nút dù được nói theo nhiều cách. Câu “tiểu đường uống metformin” và câu “đái tháo đường dùng metformin” vì vậy cùng tạo một cạnh ICD-10:E14 → treated_by → RxNorm:6809, với số lần xuất hiện bằng 2."),
  T(["Thành phần", "Cách làm"], [
    ["Khóa của nút", "“ontology:mã” khi chuẩn hóa có quyết định (ICD-10:E14, RxNorm:6809); nếu không thì “loại:chữ đã chuẩn hóa” (BODY_PART:xương). Gợi ý top-1 không được dùng làm khóa để tránh gộp sai"],
    ["Thuộc tính nút", "Tên hiển thị (tên chuẩn nếu có mã), các cách viết đã gặp và số lần, số đề cập, số văn bản, mã gợi ý"],
    ["Cạnh", "Gộp theo (đầu, quan hệ, cuối): số lần, số văn bản, số lần theo nguồn model/rule, điểm trung bình, tối đa 3 câu ví dụ"],
    ["Lọc", "Bỏ CONDITION chung chung (“bệnh”, “bị bệnh”, “triệu chứng”, “biến chứng”, “vi khuẩn”…) để chúng không thành nút trung tâm giả; thực thể chung của RE đã bị bỏ từ bước 6"],
    ["Truy vấn", "neighbors(nút), find(chữ), stats()"],
    ["Xuất", "kg.json, triples.csv, nodes.csv, kg.graphml (mở bằng Gephi, networkx), kg.html"],
  ], [2200, 7438], { size: 20 }),
  CAP("Bảng 4.8. Thiết kế knowledge graph (knowledge_graph/graph.py)."),
  P("Trang kg.html nhúng sẵn dữ liệu đồ thị và tải thư viện vis-network 9.1.9 từ unpkg, nên chỉ cần mở bằng trình duyệt có mạng. Trang có bộ lọc theo quan hệ và theo số lần xuất hiện tối thiểu, ô tìm kiếm, và bảng chi tiết hiện câu nguồn khi bấm vào nút hoặc cạnh. Nút chưa có mã vẽ viền đứt, cạnh chỉ do luật sinh ra vẽ nét đứt, để người xem phân biệt phần chắc chắn với phần cần kiểm tra. Đồ thị được dựng bằng scripts/build_kg.py từ một split của VietMed-NER, từ tệp văn bản, hoặc từ kết quả đã lưu (chạy lại RE mà không chạy lại NER)."),
);

// ===== CHƯƠNG 5 =====
const nerRow = (rep, k) => [f(rep[k].precision), f(rep[k].recall), f(rep[k]["f1-score"])];
const t1rows = Object.entries(t1).filter(([k]) => !k.endsWith("avg")).sort((a, b) => b[1].support - a[1].support);
add(
  H1("CHƯƠNG 5. THỰC NGHIỆM VÀ KẾT QUẢ"),
  SUM(`NER đạt strict micro-F1 ${f(s["micro avg"]["f1-score"])}, relaxed ${f(r["micro avg"]["f1-score"])}, khoảng ${f(nerNew.lat.median_latency_ms, 0)} ms/câu; phần mô hình vượt baseline từ điển và CRF trên sáu loại mục tiêu. Trên tập gold chuẩn hóa test, ICD-10 đạt Accuracy ${rp(nc("ICD-10").system.accuracy)} (thận trọng) và ${rp(nc("ICD-10").always.accuracy)} (luôn trả lời), Recall@10 ${rp(nc("ICD-10")["recall@10"])}; RxNorm đạt Accuracy ${rp(nc("RxNorm").system.accuracy)}. RE trên gold v1 đạt F1 ${rp(cvL.positive_micro.f1)} với LogReg và ${rp(cvR.positive_micro.f1)} với luật, chênh lệch không có ý nghĩa thống kê; sau khi thêm RE v2, ViHealthBERT hợp với luật đạt F1 ${rp(bp("random_test", "bert+rules").f1)} trên tập test ngẫu nhiên, so với ${rp(bp("random_test", "rules").f1)} của luật và ${rp(bp("random_test", "cooccur").f1)} của baseline đồng xuất hiện. Knowledge graph trên split test có ${n(kgS.nodes)} nút, ${kgS.edges} cạnh. Mọi số trên tập nhãn AI là tạm thời.`),
  H2("5.1. Môi trường và giao thức"),
  P(`Toàn bộ thực nghiệm chạy trên CPU (PyTorch 2.14.0+cpu, Transformers 5.17.0, Python ${reGoldRun.metadata.python}, scikit-learn ${reGoldRun.metadata.sklearn}), hệ điều hành Windows 11. [[Bổ sung cấu hình CPU/RAM của máy chạy.]] Đánh giá NER được chạy lại ngày 05/11/2026 với mã nguồn hiện tại; kết quả nằm trong ${NER_DIR}/. Ablation chạy ngày 06/11/2026 trong ${ABL_DIR}/.`),
  T(["Thành phần", "Dữ liệu đánh giá", "Chỉ số chính"], [
    ["NER tầng 1", `VietMed-NER test, ${n(nerNew.lat.total_samples)} câu, ${nTypes} loại gốc`, "seqeval micro/macro/weighted F1"],
    ["NER tầng 2", "Cùng dữ liệu, 6 loại mục tiêu, toàn pipeline", "Strict và relaxed micro/macro F1, theo loại"],
    ["Ablation NER", "Cùng dữ liệu", "Strict/relaxed micro F1 khi bỏ từng nhóm luật"],
    ["Baseline NER", "Train để học, validation để chọn, test một lần", "Micro-F1 18 loại và 6 loại, CI95"],
    ["Chuẩn hóa ICD-10 (khảo sát)", `${icd.condition_mentions} mention CONDITION của gold v1`, "Tỉ lệ có mã, tỉ lệ mã đúng (kiểm tra tay)"],
    ["Chuẩn hóa ICD-10 / RxNorm", `Gold chuẩn hóa: dev ${normMan.splits.dev.CONDITION.unique_forms + normMan.splits.dev.DRUG.unique_forms} dạng, test ${normMan.splits.test.CONDITION.unique_forms + normMan.splits.test.DRUG.unique_forms} dạng (nhãn AI)`, "Accuracy, coverage, precision khi trả lời, từ chối đúng NIL, Top-k = Recall@k, MRR@10, CI95"],
    ["RE", `Gold v1, ${reGold.pairs} cặp`, "Positive micro-F1, CV 5 fold theo nhóm, CI95"],
    ["RE (gold v1 + RE v2)", `${re2.final_model.pairs} cặp train (CV); golden test v1.1 ${bench.data.golden_test_pairs} cặp; test ngẫu nhiên ${bench.data.random_test_pairs} cặp (nhãn AI)`, "Positive micro-F1 theo quan hệ, CI95, mười phương pháp"],
    ["RE end-to-end", "Thực thể do NER sinh ra", "Chưa có"],
    ["Knowledge graph", `${n(kgS.documents)} câu split test`, "Số nút, cạnh, phân bố theo quan hệ và nguồn"],
  ], [2200, 4300, 3138], { size: 20 }),
  CAP("Bảng 5.1. Giao thức đánh giá."),
  H2("5.2. Kết quả NER"),
  H3("5.2.1. Tầng 1: mô hình gốc trên nhãn VietMed-NER"),
  P(`Đánh giá trực tiếp đầu ra checkpoint bằng seqeval trên ${nTypes} loại thực thể gốc, trước ánh xạ và luật: micro-F1 **${f(t1["micro avg"]["f1-score"])}** (P ${f(t1["micro avg"].precision)}, R ${f(t1["micro avg"].recall)}), macro-F1 ${f(t1["macro avg"]["f1-score"])}, weighted-F1 ${f(t1["weighted avg"]["f1-score"])}, trên ${n(t1["micro avg"].support)} thực thể gold.`),
  T(["Loại gốc", "P", "R", "F1", "Support", "Ánh xạ"], t1rows.map(([k, v]) => [k, f(v.precision), f(v.recall), f(v["f1-score"]), v.support, ({ DISEASESYMTOM: "CONDITION", DRUGCHEMICAL: "DRUG", PREVENTIVEMED: "DRUG", ORGAN: "BODY_PART", DIAGNOSTICS: "TEST", SURGERY: "PROCEDURE", MEDDEVICETECHNIQUE: "PROCEDURE", TREATMENT: "PROCEDURE", UNITCALIBRATOR: "DOSAGE" })[k] || "(loại bỏ)"]), [2600, 1200, 1200, 1200, 1300, 2138], { right: [1, 2, 3, 4], size: 20 }),
  CAP("Bảng 5.2. Kết quả tầng 1 theo từng loại gốc, sắp theo support."),
  P(`Các loại y khoa nhiều mẫu như DISEASESYMTOM (F1 ${f(t1.DISEASESYMTOM["f1-score"])}), ORGAN (${f(t1.ORGAN["f1-score"])}) và DRUGCHEMICAL (${f(t1.DRUGCHEMICAL["f1-score"])}) đạt kết quả khá. Các loại yếu nhất là PREVENTIVEMED (${f(t1.PREVENTIVEMED["f1-score"])}, chỉ ${t1.PREVENTIVEMED.support} mẫu), MEDDEVICETECHNIQUE (${f(t1.MEDDEVICETECHNIQUE["f1-score"])}) và SURGERY (${f(t1.SURGERY["f1-score"])}) — cả hai đều được gộp vào PROCEDURE, giải thích vì sao PROCEDURE yếu ở tầng 2.`),
  H3("5.2.2. Tầng 2: toàn pipeline trên sáu loại mục tiêu"),
  T(["Loại", "Strict P", "Strict R", "Strict F1", "Relaxed P", "Relaxed R", "Relaxed F1", "Support"], [
    ...LABELS6.map((k) => [k, ...nerRow(s, k), ...nerRow(r, k), s[k].support]),
    ["**Micro**", ...nerRow(s, "micro avg"), ...nerRow(r, "micro avg"), s["micro avg"].support],
    ["**Macro**", ...nerRow(s, "macro avg"), ...nerRow(r, "macro avg"), ""],
  ], [1500, 1100, 1100, 1100, 1100, 1100, 1100, 1538], { right: [1, 2, 3, 4, 5, 6, 7], size: 20 }),
  CAP(`Bảng 5.3. Kết quả NER toàn pipeline trên ${n(nerNew.lat.total_samples)} câu test (nguồn: ${NER_DIR}/schema_6label_report.json).`),
  T(["Loại", "TP strict", "FP strict", "FN strict", "TP relaxed", "FP relaxed", "FN relaxed"], LABELS6.map((k) => [k, s[k].tp, s[k].fp, s[k].fn, r[k].tp, r[k].fp, r[k].fn]), [1800, 1300, 1300, 1300, 1300, 1300, 1338], { right: [1, 2, 3, 4, 5, 6], size: 20 }),
  CAP("Bảng 5.4. Số đếm TP/FP/FN theo loại."),
  P(`TEST (${f(s.TEST["f1-score"])}) và DRUG (${f(s.DRUG["f1-score"])}) có strict F1 cao nhất; DOSAGE (${f(s.DOSAGE["f1-score"])}) và PROCEDURE (${f(s.PROCEDURE["f1-score"])}) thấp nhất. Khoảng cách giữa strict và relaxed (micro ${f(s["micro avg"]["f1-score"])} so với ${f(r["micro avg"]["f1-score"])}) cho thấy nhiều lỗi là lệch ranh giới span chứ không phải sai loại: chuyển từ strict sang relaxed, TP tăng từ ${n(s.CONDITION.tp + s.DRUG.tp + s.BODY_PART.tp + s.TEST.tp + s.PROCEDURE.tp + s.DOSAGE.tp)} lên ${n(r.CONDITION.tp + r.DRUG.tp + r.BODY_PART.tp + r.TEST.tp + r.PROCEDURE.tp + r.DOSAGE.tp)}. DRUG có recall cao (${f(s.DRUG.recall)}) nhưng precision thấp (${f(s.DRUG.precision)}): mô hình gán DRUG cho nhiều cụm không phải thuốc, kể cả cụm mà gold gán loại phi y khoa (thực phẩm, chăm sóc cá nhân) đã bị loại khỏi schema.`),
  sameNer
    ? NOTE(`Kết quả chạy lại ngày 05/11/2026 trùng khớp tuyệt đối với báo cáo cũ ngày 17/09/2026 (strict micro-F1 ${f(so["micro avg"]["f1-score"])}). Luật 1b thêm ngày 01/11/2026 không kích hoạt trên tập test.`)
    : NOTE(`So với báo cáo cũ ngày 17/09/2026 (strict micro-F1 ${f(so["micro avg"]["f1-score"])}), kết quả chạy lại là ${f(s["micro avg"]["f1-score"])}. Luận văn nên dùng số mới.`),
);
if (exists(`${NER_DIR}/confusion_matrix.png`)) {
  add(new Paragraph({ alignment: AlignmentType.CENTER, children: [new ImageRun({ type: "png", data: fs.readFileSync(path.join(ROOT, `${NER_DIR}/confusion_matrix.png`)), transformation: { width: 460, height: 380 } })] }),
    CAP("Hình 5.1. Ma trận nhầm lẫn giữa sáu loại mục tiêu và NONE, ghép theo span giao nhau lớn nhất."));
}
const ablNames = { full: "Đầy đủ", no_dosage: "Bỏ luật liều", no_rules: "Bỏ Luật 1, 1b, 2", model_only: "Chỉ mô hình" };
const ablData = abl ? { full: nerNew.t2, ...abl } : null;
add(
  H3("5.2.3. Ablation các luật NER"),
  P("Để trả lời câu hỏi nghiên cứu 3, pipeline được chạy lại trên cùng tập test với từng nhóm luật bị tắt (scripts/run_ner_ablation.py). Mọi cấu hình đều giữ lọc schema và giải quyết chồng lấn. Không có tinh chỉnh nào dựa trên kết quả này."),
  ...(ablData ? [
    T(["Cấu hình", "Strict P", "Strict R", "Strict F1", "Relaxed F1", "Δ strict F1 so với đầy đủ"], Object.keys(ablNames).filter((k) => ablData[k]).map((k) => { const a = ablData[k].strict_exact_match["micro avg"], b = ablData[k].relaxed_overlap_match["micro avg"]; const d = a["f1-score"] - s["micro avg"]["f1-score"]; return [ablNames[k], f(a.precision), f(a.recall), f(a["f1-score"]), f(b["f1-score"]), (d >= 0 ? "+" : "") + f(d)]; }), [2400, 1300, 1300, 1300, 1300, 2038], { right: [1, 2, 3, 4, 5], size: 20 }),
    CAP("Bảng 5.5. Ablation trên micro-F1 (nguồn: eval/ablation_2026-11-06/)."),
    T(["Loại", ...Object.keys(ablNames).filter((k) => ablData[k]).map((k) => ablNames[k])], LABELS6.map((lab) => [lab, ...Object.keys(ablNames).filter((k) => ablData[k]).map((k) => f(ablData[k].strict_exact_match[lab]["f1-score"]))]), [2000, 1900, 1900, 1900, 1938], { right: [1, 2, 3, 4], size: 20 }),
    CAP("Bảng 5.6. Strict F1 theo loại trong từng cấu hình ablation."),
    P(ablText()),
  ] : [NOTE("[[Kết quả ablation chưa có khi dựng báo cáo; chạy scripts/run_ner_ablation.py rồi dựng lại.]]")]),
  H3("5.2.4. Thời gian xử lý"),
  T(["Chỉ số", "05/11/2026 (ms/câu)", "17/09/2026 (ms/câu)"], [["Trung bình", f(nerNew.lat.mean_latency_ms, 2), f(nerOld.lat.mean_latency_ms, 2)], ["Trung vị (P50)", f(nerNew.lat.median_latency_ms, 2), f(nerOld.lat.median_latency_ms, 2)], ["P90", f(nerNew.lat.p90_latency_ms, 2), f(nerOld.lat.p90_latency_ms, 2)], ["P95", f(nerNew.lat.p95_latency_ms, 2), f(nerOld.lat.p95_latency_ms, 2)], ["P99", f(nerNew.lat.p99_latency_ms, 2), f(nerOld.lat.p99_latency_ms, 2)], ["Nhỏ nhất / lớn nhất", `${f(nerNew.lat.min_latency_ms, 2)} / ${f(nerNew.lat.max_latency_ms, 2)}`, `${f(nerOld.lat.min_latency_ms, 2)} / ${f(nerOld.lat.max_latency_ms, 2)}`], ["Tổng thời gian (giây)", f(nerNew.lat.total_time_seconds, 1), f(nerOld.lat.total_time_seconds, 1)]], [3600, 3000, 3038], { right: [1, 2] }),
  CAP("Bảng 5.7. Độ trễ toàn pipeline NER (tắt chuẩn hóa), CPU, xử lý tuần tự từng câu."),
  P("Kết quả nhận diện của hai lần đo giống hệt nhau, nên chênh lệch độ trễ nhiều khả năng do tải máy hoặc môi trường chạy khác nhau. Đây là độ trễ trên một máy cá nhân; không nên coi là cam kết hiệu năng. Với độ trễ trung vị khoảng 100 ms/câu, hệ thống đủ nhanh cho xử lý tương tác từng văn bản, nhưng xử lý hàng loạt lớn nên dùng batch và GPU."),
  ...(nerBase ? [
    H3("5.2.5. So sánh với baseline NER"),
    P(`Để đặt checkpoint vào bối cảnh, khóa luận huấn luyện hai baseline trên split train, chọn siêu tham số trên split validation và chấm split test một lần (scripts/ner_experiments/). Baseline **từ điển** gán nhãn bằng khớp dài nhất mọi cụm thực thể đã thấy trong train với loại xuất hiện nhiều nhất (${n(nerBase.dictionary.params.entries)} mục sau khi bỏ cụm thường xuất hiện ngoài thực thể). Baseline **CRF** là CRF chuỗi tuyến tính với đặc trưng âm tiết, hình dạng chữ, tiền tố/hậu tố và cửa sổ ±2 (c1 = ${nerBase.crf.params.c1}, c2 = ${nerBase.crf.params.c2}, chọn trên validation). Checkpoint ViHealthBERT được chấm bằng cùng hàm, chỉ phần mô hình, không có luật hậu xử lý.${nerSelf ? " Ngoài ra, khóa luận tự tinh chỉnh lại ViHealthBERT từ mô hình nền với epoch được chọn trên validation." : ""}`),
    T(["Mô hình", "18 loại gốc: P", "R", "F1", "CI95", "6 loại mục tiêu: F1", "CI95"], [
      ["Từ điển (train)", nerBase.dictionary.test], ["CRF", nerBase.crf.test],
      ...(nerSelf ? [[`ViHealthBERT tự tinh chỉnh (seed ${nerSelf.meta.kept_seed})`, nerSelf.runs.find((r) => r.seed === nerSelf.meta.kept_seed).scores.test]] : []),
      ...(nerInh ? [["ViHealthBERT checkpoint kế thừa", nerInh.scores.test]] : []),
    ].map(([k, t]) => [k, f(t.raw.micro.precision), f(t.raw.micro.recall), f(t.raw.micro.f1), ci(t.raw.micro_f1_ci95), f(t.target.micro.f1), ci(t.target.micro_f1_ci95)]), [3000, 1100, 900, 900, 1300, 1300, 1138], { size: 19, right: [1, 2, 3, 5] }),
    CAP(`Bảng 5.8. NER chỉ mô hình trên ${n(nerBase.data.test)} câu test, micro-F1 theo thực thể (seqeval), CI95 bootstrap theo câu (nguồn: ${NERB_DIR}/).`),
    T(["Loại", "Từ điển", "CRF", ...(nerInh ? ["ViHealthBERT kế thừa"] : [])], LABELS6.map((k) => [k, f(nerBase.dictionary.test.target.report[k]["f1-score"], 3), f(nerBase.crf.test.target.report[k]["f1-score"], 3), ...(nerInh ? [f(nerInh.scores.test.target.report[k]["f1-score"], 3)] : [])]), [3000, 2200, 2200, 2238], { size: 20, right: [1, 2, 3] }),
    CAP("Bảng 5.9. F1 theo loại mục tiêu trên test, chỉ mô hình."),
    ...(nerInh ? [
      P(`Trên sáu loại mà hệ thống dùng, ViHealthBERT vượt rõ cả hai baseline: micro-F1 ${f(nerInh.scores.test.target.micro.f1, 3)} (CI95 ${ci(nerInh.scores.test.target.micro_f1_ci95)}) so với ${f(nerBase.dictionary.test.target.micro.f1, 3)} của từ điển và ${f(nerBase.crf.test.target.micro.f1, 3)} của CRF, và các khoảng tin cậy không chồng lấn. Ưu thế đến từ recall (${f(nerInh.scores.test.target.micro.recall, 3)} so với ${f(nerBase.dictionary.test.target.micro.recall, 3)} và ${f(nerBase.crf.test.target.micro.recall, 3)}): mô hình ngôn ngữ nhận ra được cách nói chưa xuất hiện trong train, điều mà từ điển và CRF dựa trên từ vựng không làm được. Đổi lại, precision của nó thấp hơn (${f(nerInh.scores.test.target.micro.precision, 3)}). Ngoại lệ là TEST, nơi từ điển tốt nhất (${f(nerBase.dictionary.test.target.report.TEST["f1-score"], 3)}), vì tên xét nghiệm là một tập từ vựng nhỏ và lặp lại.`),
      P(`Trên 18 loại gốc thì khác: từ điển (${f(nerBase.dictionary.test.raw.micro.f1, 3)}) ngang ViHealthBERT (${f(nerInh.scores.test.raw.micro.f1, 3)}), CI95 chồng lấn. Lý do là các loại phi y khoa (giới tính, tuổi, thời gian, nghề nghiệp) chiếm nhiều mẫu và gần như luôn là cùng một nhóm từ (“bệnh nhân”, “ba má”, “tháng”). Điểm số gộp trên 18 loại vì vậy che mất khoảng cách thật ở phần y khoa; đây là thêm một lý do để báo cáo ở cấp sáu loại mục tiêu.`),
      P(`Bảng 5.8 còn trả lời câu hỏi bỏ ngỏ ở A15. Checkpoint đạt micro-F1 ${f(nerInh.scores.validation.raw.micro.f1, 3)} trên validation nhưng ${f(nerInh.scores.test.raw.micro.f1, 3)} trên test, chênh hơn 20 điểm, nên có thể nghi checkpoint đã được chọn hoặc học trên validation. Nhưng hai baseline chỉ học trên train cũng tụt y như vậy (từ điển ${f(nerBase.dictionary.validation_micro_f1, 3)} → ${f(nerBase.dictionary.test.raw.micro.f1, 3)}, CRF ${f(nerBase.crf.validation_micro_f1, 3)} → ${f(nerBase.crf.test.raw.micro.f1, 3)}). Nguyên nhân là **split validation của VietMed-NER rất gần train**: 7,5% câu validation có chung một cụm 8 từ với train, so với 0,3% ở test, và riêng việc tra từ điển cụm đã thấy trong train đã đạt 0,91 trên validation. Chênh lệch vì vậy chủ yếu do phân bố, không phải bằng chứng rò rỉ; nhưng nó cũng có nghĩa là **validation không phải tập dev tốt** để dự đoán kết quả trên test, kể cả cho bước chuẩn hóa (mục 5.3.3).`),
    ] : []),
  ] : []),
  H2("5.3. Kết quả chuẩn hóa mã"),
  H3("5.3.1. Trước khi sửa"),
  P(`Chưa có tập gold mã ICD-10. Để có ước lượng ban đầu, bộ chuẩn hóa được chạy trên ${icdBefore.condition_mentions} mention CONDITION (${icdBefore.unique} cụm khác nhau) của bộ gold v1, sau đó từng mã được kiểm tra thủ công. Phiên bản trước khi sửa tra được mã cho ${icdBefore.coded_mentions} mention (${pct(icdBefore.coded_mentions / icdBefore.condition_mentions)}): ${icdBefore.by_method.exact || 0} khớp chính xác, ${icdBefore.by_method.synonym || 0} qua đồng nghĩa, ${icdBefore.by_method.fuzzy || 0} qua khớp gần đúng. Trong số đó ${icdBeforeOk} hợp lý, **${icdBefore.wrong_mentions} sai** và ${icdBefore.doubt_mentions} nghi vấn.`),
  T(["Cụm CONDITION", "Số lần", "Mã gán", "Tên chuẩn", "Cách khớp", "Nhận xét"], icdBefore.items.filter((o) => o.verdict !== "hợp lý").map((o) => [o.text, o.mentions, o.code, o.label, `${o.method} (${f(o.score, 2)})`, `${o.verdict}: ${o.note}`]), [1700, 800, 900, 2100, 1300, 2838], { size: 20 }),
  CAP("Bảng 5.10. Các mã ICD-10 sai hoặc nghi vấn trước khi sửa (nguồn: icd10_check_before_fix.json)."),
  H3("5.3.2. Sau khi sửa"),
  P(`Bản sửa ngày 06/11/2026 thêm hai ràng buộc an toàn cho bước khớp gần đúng (Bảng 4.5) và sáu alias (huyết áp cao, huyết áp tăng cao → I10; rối loạn mỡ máu → E78; mỡ máu cao → E78.5; đa xơ cứng → G35; đậu mùa bò → B08.0). Riêng hai ràng buộc đã tự chặn cả năm mã sai, kể cả khi không có alias. Kết quả mới: ${icd.coded_mentions} mention có mã (${pct(icd.coded_mentions / icd.condition_mentions)}), gồm ${icd.by_method.exact || 0} chính xác, ${icd.by_method.synonym || 0} đồng nghĩa, ${icd.by_method.fuzzy || 0} gần đúng; ${icdOk} hợp lý, ${icd.wrong_mentions} sai, ${icd.doubt_mentions} nghi vấn.`),
  T(["Chỉ số", "Trước sửa", "Sau sửa"], [["Mention có mã", `${icdBefore.coded_mentions} (${pct(icdBefore.coded_mentions / icdBefore.condition_mentions)})`, `${icd.coded_mentions} (${pct(icd.coded_mentions / icd.condition_mentions)})`], ["Mã hợp lý", icdBeforeOk, icdOk], ["Mã sai", icdBefore.wrong_mentions, icd.wrong_mentions], ["Mã nghi vấn", icdBefore.doubt_mentions, icd.doubt_mentions], ["Tỉ lệ mã hợp lý trong số có mã", pct(icdBeforeOk / icdBefore.coded_mentions), pct(icdOk / icd.coded_mentions)], ["Khớp gần đúng", icdBefore.by_method.fuzzy || 0, icd.by_method.fuzzy || 0]], [4200, 2700, 2738], { right: [1, 2] }),
  CAP("Bảng 5.11. Chuẩn hóa ICD-10 trên gold v1 trước và sau bản sửa (chi tiết từng mã ở Phụ lục G)."),
  T(["Cụm", "Trước", "Sau"], [...icd.changed.map((c) => [c.text, c.before, c.after]), ...icd.removed_codes.map((c) => [c.text, c.code, "(không gán)"])], [4000, 2800, 2838]),
  CAP("Bảng 5.12. Các mã thay đổi sau bản sửa."),
  NOTE("Hai lưu ý khi diễn giải: (1) việc kiểm tra mã do người soát hệ thống thực hiện, không phải chuyên gia mã hóa bệnh; (2) các alias mới được rút ra từ chính bộ dữ liệu dùng để đo, nên kết quả “0 mã sai” sau sửa là lạc quan và không phải đánh giá độc lập. Hai ràng buộc an toàn là quy tắc tổng quát, nhưng cũng được thiết kế sau khi thấy lỗi trên bộ này. Cần một tập gold mã ICD-10 riêng để đánh giá khách quan."),
  P("Tỉ lệ có mã thấp vì nhiều CONDITION là triệu chứng khẩu ngữ (“tê bì kiến bò”, “khô ngứa bong tróc”), cụm chung (“bệnh”, “biến chứng”) hoặc tên không có trong danh mục. Đây là hành vi mong muốn của thiết kế ưu tiên không gán mã: một mã sai nguy hiểm hơn một mention không có mã."),
  P("Phép kiểm tra ở 5.3.1–5.3.2 trả lời câu hỏi “mã gán ra có đúng không”, nhưng không đo được mã bị bỏ sót và dùng chính bộ dữ liệu đã dùng để sửa. Mục 5.3.3 đo lại trên tập gold riêng."),
  H3("5.3.3. Đánh giá trên tập gold chuẩn hóa dev/test"),
  P(`Giao thức: mọi cải tiến (137 alias ICD-10, 31 alias thuốc, ràng buộc phủ từ, bước approximateTerm, cách xếp hạng top-k) được chọn khi chỉ nhìn kết quả trên dev; test được chạy một lần sau khi đã chốt. Không có mục từ điển nào chỉ xuất hiện trong test được thêm vào. Số chính là theo dạng (mỗi dạng bề mặt tính một lần); số theo đề cập trọng số theo tần suất. Hai baseline là khớp chính xác tên danh mục và fuzzy top-1 không ràng buộc (rapidfuzz WRatio).`),
  T(["Phương pháp", "Accuracy", "CI95", "Accuracy (đề cập)", "Coverage", "Precision khi trả lời", "Từ chối đúng NIL"], [
    ["exact", "Baseline: khớp chính xác"], ["fuzzy1", "Baseline: fuzzy top-1"], ["system", "**Hệ thống – thận trọng**"], ["always", "Hệ thống – luôn trả lời"],
  ].map(([k, lab]) => [lab, rp(nc("ICD-10")[k].accuracy), ci(nci("ICD-10", `${k}.accuracy`)), rp(ncm("ICD-10")[k].accuracy), rp(nc("ICD-10")[k].coverage), rp(nc("ICD-10")[k].precision_answered), rp(nc("ICD-10")[k].nil_correct_abstention)]), [2600, 1100, 1300, 1200, 1100, 1200, 1138], { size: 19, right: [1, 3, 4, 5, 6] }),
  CAP(`Bảng 5.13. ICD-10 trên test, mã đầy đủ: ${nc("ICD-10").n_linkable} dạng có mã (${n(nc("ICD-10").mentions_linkable)} đề cập), ${nc("ICD-10").n_nil} dạng NIL. Nguồn: ${NORM_DIR}/test_after/report.json.`),
  T(["Phương pháp", "Accuracy", "CI95", "Accuracy (đề cập)", "Coverage", "Precision khi trả lời", "Từ chối đúng NIL"], [
    ["exact", "Baseline: khớp chính xác"], ["fuzzy1", "Baseline: fuzzy top-1"], ["system", "**Hệ thống – thận trọng**"], ["always", "Hệ thống – luôn trả lời"],
  ].map(([k, lab]) => [lab, rp(nc("RxNorm")[k].accuracy), ci(nci("RxNorm", `${k}.accuracy`)), rp(ncm("RxNorm")[k].accuracy), rp(nc("RxNorm")[k].coverage), rp(nc("RxNorm")[k].precision_answered), rp(nc("RxNorm")[k].nil_correct_abstention)]), [2600, 1100, 1300, 1200, 1100, 1200, 1138], { size: 19, right: [1, 3, 4, 5, 6] }),
  CAP(`Bảng 5.14. RxNorm trên test: ${nc("RxNorm").n_linkable} dạng có mã (${nc("RxNorm").mentions_linkable} đề cập), ${nc("RxNorm").n_nil} dạng NIL.`),
  T(["Mức", "Top-1", "Top-3", "Top-5", "Top-10", "MRR@10", "CI95 Top-5"], [
    ["ICD-10 mã đầy đủ", "ICD-10", "code"], ["ICD-10 nhóm 3 ký tự", "ICD-10", "category"], ["RxNorm", "RxNorm", "code"],
  ].map(([lab, o, lv]) => { const t = nc(o, "test", normA, lv); return [lab, rp(t.top1_acc), rp(t.top3_acc), rp(t.top5_acc), rp(t.top10_acc), rp(t["mrr@10"]), ci(nci(o, "top5_acc", "test", normA, lv))]; }), [2600, 1100, 1100, 1100, 1100, 1200, 1438], { size: 20, right: [1, 2, 3, 4, 5] }),
  CAP("Bảng 5.15. Top-k Accuracy (= Recall@k, vì mỗi đề cập có một khái niệm gold) và MRR@10 trên test, theo dạng."),
  T(["Ontology", "Split", "Accuracy trước → sau", "Top-10 trước → sau", "Precision khi trả lời trước → sau"], ["ICD-10", "RxNorm"].flatMap((o) => ["dev", "test"].map((sp2) => [o, sp2, `${rp(nc(o, sp2, normB).system.accuracy)} → **${rp(nc(o, sp2).system.accuracy)}**`, `${rp(nc(o, sp2, normB).top10_acc)} → ${rp(nc(o, sp2).top10_acc)}`, `${rp(nc(o, sp2, normB).system.precision_answered)} → ${rp(nc(o, sp2).system.precision_answered)}`])), [1500, 1000, 2600, 2200, 2338], { size: 20 }),
  CAP(`Bảng 5.16. Trước và sau bản cải tiến 07/11/2026, chế độ thận trọng (nguồn: ${NORM_DIR}/comparison.md).`),
  P(`Ba kết quả đáng chú ý. Thứ nhất, khoảng cách dev–test rất lớn với ICD-10 (Accuracy ${rp(nc("ICD-10", "dev").system.accuracy)} trên dev so với ${rp(nc("ICD-10").system.accuracy)} trên test). Có hai nguyên nhân cộng dồn: từ điển được học từ các dạng có trong train/dev, và bản thân split validation rất gần train (mục 5.2.5), nên dev ước lượng quá cao khả năng gặp lại cách nói đã biết. Con số cần trích dẫn là con số trên test. Thứ hai, chế độ thận trọng giữ precision ${rp(nc("ICD-10").system.precision_answered)} khi trả lời và từ chối đúng ${pct(nc("ICD-10").system.nil_correct_abstention)} dạng NIL; chế độ luôn trả lời tăng Accuracy lên ${rp(nc("ICD-10").always.accuracy)} nhưng gán mã cho mọi dạng NIL. Thứ ba, khi đưa cho người dùng 10 ứng viên, mã đúng có mặt trong ${pct(nc("ICD-10").top10_acc)} trường hợp, và ở mức nhóm 3 ký tự là ${pct(nc("ICD-10", "test", normA, "category").top10_acc)}; vì vậy hệ thống phù hợp với kịch bản gợi ý mã cho người nhập liệu chọn.`),
  P(`So với baseline, hệ thống thận trọng gấp khoảng ${(nc("ICD-10").system.accuracy / nc("ICD-10").exact.accuracy).toFixed(0)} lần khớp chính xác và gần gấp đôi fuzzy top-1 với ICD-10, trong khi fuzzy top-1 có precision chỉ ${rp(nc("ICD-10").fuzzy1.precision_answered)}: không có ràng buộc, khớp gần đúng sai nhiều hơn đúng. Với RxNorm, accuracy theo đề cập (${rp(ncm("RxNorm").system.accuracy)}) cao hơn hẳn theo dạng vì các thuốc phổ biến (vitamin, canxi, sắt) tra được, còn đuôi dài là tên thảo dược và thực phẩm chức năng. Trên test, hệ thống thận trọng chỉ gán sai ${normA.test.system_wrong_links.length} dạng: ${normA.test.system_wrong_links.map((w) => `“${w.form}” → ${w.pred}${w.gold.length ? ` (gold ${w.gold.join(", ")})` : " (gold NIL)"}`).join("; ")}.`),
  NOTE("Nhãn gold dev/test là nhãn AI chưa có bác sĩ duyệt. Ngoài ra, 48 trong 137 alias ICD-10 mới cũng xuất hiện trong test vì chúng có cả ở train/dev; chúng không được chọn bằng test, nhưng làm Accuracy test cao hơn so với một tập test hoàn toàn chưa thấy. Các con số ở mục này cần được tính lại sau khi phiếu duyệt được bác sĩ xác nhận."),
  H2("5.4. Kết quả trích xuất quan hệ"),
  H3("5.4.1. Chia tập seed 42"),
  T(["Tập", "Số nhóm", "Số cặp", "Phân bố nhãn"], ["train", "dev", "test"].map((k) => [k, sp[k].text_groups, sp[k].pairs, Object.entries(sp[k].labels).map(([a, b]) => `${a}: ${b}`).join("; ")]), [1200, 1300, 1300, 5838]),
  CAP("Bảng 5.17. Chia tập theo nhóm văn bản trên gold v1."),
  T(["Tập", "Phương pháp", "P", "R", "F1"], ["dev", "test"].flatMap((k) => ["rules", "logreg"].map((m) => [`${k} (${reGold.seed42_split[k].pairs} cặp)`, m === "rules" ? "Luật" : "TF-IDF + LogReg", rp(reGold.seed42_split[k][m].positive_micro.precision), rp(reGold.seed42_split[k][m].positive_micro.recall), rp(reGold.seed42_split[k][m].positive_micro.f1)])), [2500, 2600, 1500, 1500, 1538], { right: [2, 3, 4] }),
  CAP("Bảng 5.18. Positive micro-F1 trên dev/test seed 42."),
  P(`Dev chỉ có ${posSplit("dev")} cặp dương và test có ${posSplit("test")} cặp dương, nên một dự đoán đúng hay sai làm F1 thay đổi rất mạnh. Kết quả trên một lần chia không đủ tin cậy để so sánh phương pháp; dự đoán từng cặp được liệt kê ở Phụ lục H.`),
  H3("5.4.2. Cross-validation 5 fold theo nhóm"),
  T(["Dữ liệu", "Phương pháp", "P", "R", "F1", "CI95 F1"], [
    [`Gold v1 (${reGold.pairs} cặp)`, "Luật", rp(cvR.positive_micro.precision), rp(cvR.positive_micro.recall), rp(cvR.positive_micro.f1), `${rp(cvR.positive_micro_f1_ci95[0])}–${rp(cvR.positive_micro_f1_ci95[1])}`],
    [`Gold v1 (${reGold.pairs} cặp)`, "TF-IDF + LogReg", rp(cvL.positive_micro.precision), rp(cvL.positive_micro.recall), rp(cvL.positive_micro.f1), `${rp(cvL.positive_micro_f1_ci95[0])}–${rp(cvL.positive_micro_f1_ci95[1])}`],
    [`Nhãn AI rà soát (${reAi.pairs} cặp)`, "Luật", rp(cvRa.positive_micro.precision), rp(cvRa.positive_micro.recall), rp(cvRa.positive_micro.f1), `${rp(cvRa.positive_micro_f1_ci95[0])}–${rp(cvRa.positive_micro_f1_ci95[1])}`],
    [`Nhãn AI rà soát (${reAi.pairs} cặp)`, "TF-IDF + LogReg", rp(cvLa.positive_micro.precision), rp(cvLa.positive_micro.recall), rp(cvLa.positive_micro.f1), `${rp(cvLa.positive_micro_f1_ci95[0])}–${rp(cvLa.positive_micro_f1_ci95[1])}`],
  ], [2600, 2000, 1000, 1000, 1000, 2038], { right: [2, 3, 4] }),
  CAP("Bảng 5.19. Cross-validation 5 fold theo nhóm, gộp dự đoán ngoài fold; CI95 bootstrap 1.000 lần theo nhóm."),
  T(["Quan hệ", "Support", "TP/FP/FN luật", "F1 luật", "TP/FP/FN LogReg", "F1 LogReg"], RELS.map((k) => [k, cvL.per_relation[k].support, `${cvR.per_relation[k].tp}/${cvR.per_relation[k].fp}/${cvR.per_relation[k].fn}`, rp(cvR.per_relation[k].f1), `${cvL.per_relation[k].tp}/${cvL.per_relation[k].fp}/${cvL.per_relation[k].fn}`, rp(cvL.per_relation[k].f1)]), [2400, 1100, 1700, 1200, 1900, 1338], { right: [1, 2, 3, 4, 5], size: 20 }),
  CAP("Bảng 5.20. Kết quả theo từng quan hệ (cross-validation, gold v1)."),
  P(`Trên gold v1, LogReg đạt F1 ${rp(cvL.positive_micro.f1)} và luật đạt ${rp(cvR.positive_micro.f1)}; hai khoảng tin cậy chồng lấn rộng. Với located_at (${cvL.per_relation.located_at.support} cặp dương), luật (${rp(cvR.per_relation.located_at.f1)}) còn nhỉnh hơn LogReg (${rp(cvL.per_relation.located_at.f1)}); LogReg chỉ vượt rõ ở treated_by_procedure, nhưng lớp này chỉ có ${cvL.per_relation.treated_by_procedure.support} cặp. Cả hai phương pháp đều có recall thấp (${rp(cvR.positive_micro.recall)} và ${rp(cvL.positive_micro.recall)}).`),
  P(`Trên bộ nhãn AI trước khi duyệt, LogReg từng vượt luật rõ rệt (${rp(cvLa.positive_micro.f1)} so với ${rp(cvRa.positive_micro.f1)}). Phần lớn khoảng cách đó biến mất sau khi loại các cặp nối với từ chung “điều trị”: các cặp này rất dễ học bằng n-gram ký tự (chuỗi “điều trị” luôn nằm trong marker tail), nhưng không mang thông tin lâm sàng. Đây là phát hiện quan trọng nhất của phần RE: **chất lượng và quy ước nhãn quyết định kết luận so sánh nhiều hơn lựa chọn mô hình**.`),
  H3("5.4.3. So sánh với baseline trên ba tập đánh giá"),
  P(`Mục này đặt mọi phương pháp vào cùng một khung: cùng dữ liệu huấn luyện (gold v1 + RE v2, ${bench.data.cv_pairs} cặp), cùng 5 fold CV theo nhóm văn bản, và cùng hai tập test lấy từ split test là golden test v1.1 (${bench.data.golden_test_pairs} cặp, tỉ lệ dương ${pct(bench.positive_rate.golden_test_v1_1)}) và test ngẫu nhiên (${bench.data.random_test_pairs} cặp, tỉ lệ dương ${pct(bench.positive_rate.golden_test_random_v1)}). Bốn baseline không học gì: luôn đoán NO_RELATION (lớp đa số); đồng xuất hiện (mọi cặp đúng kiểu là dương); ghép cặp gần nhất hai chiều (dương khi không có thực thể cùng loại nào gần hơn ở cả hai phía); và luật viết từ hướng dẫn. Ba mô hình học máy cổ điển học trên fold train: đặc trưng thủ công (quan hệ, khoảng cách, thứ tự, từ ở giữa, loại thực thể chen giữa) + LogReg; TF-IDF ký tự + SVM; TF-IDF ký tự + LogReg (mô hình đang dùng).${hasBert ? ` Mô hình học sâu là ViHealthBERT có đánh dấu thực thể (mục 4.7.3), trung bình xác suất của ${bench.bert_meta.seeds.length} seed.` : ""} Cuối cùng là hai cách kết hợp với luật theo kiểu union. Mọi siêu tham số được cố định trước; không phương pháp nào được chỉnh trên hai tập test.`),
  T(["Phương pháp", "CV F1", "CV CI95", "Golden v1.1 F1", "Ngẫu nhiên P", "Ngẫu nhiên R", "Ngẫu nhiên F1", "Ngẫu nhiên CI95"], BM.map((m) => [bench.names[m], rp(bp("cv5", m).f1), bci("cv5", m), rp(bp("golden_test", m).f1), rp(bp("random_test", m).precision), rp(bp("random_test", m).recall), rp(bp("random_test", m).f1), bci("random_test", m)]), [2700, 800, 1150, 1000, 900, 900, 900, 1288], { size: 17, right: [1, 3, 4, 5, 6] }),
  CAP(`Bảng 5.21. Positive micro-F1 trên CV (${bench.cv5.rules.positive_micro.support} cặp dương), golden test v1.1 (${bench.golden_test.rules.positive_micro.support} cặp dương) và test ngẫu nhiên (${bench.random_test.rules.positive_micro.support} cặp dương). Nguồn: ${BENCH_DIR}/benchmark.json.`),
  T(["Quan hệ", "Support", ...BM.filter((m) => m !== "majority").map((m) => m)], RELS.map((k) => [k, bench.random_test.rules.per_relation[k].support, ...BM.filter((m) => m !== "majority").map((m) => rp(bench.random_test[m].per_relation[k].f1))]), [1900, 700, ...BM.filter((m) => m !== "majority").map(() => 800)], { size: 15, right: BM.map((_, i) => i + 1) }),
  CAP("Bảng 5.22. F1 theo quan hệ trên test ngẫu nhiên (tên phương pháp viết tắt như trong benchmark.json; Bảng 5.21 có tên đầy đủ)."),
  T(["Phương pháp", "Golden bản gốc F1", "Golden v1.1 F1"], BM.map((m) => [bench.names[m], rp(bp("golden_test_v1_original", m).f1), rp(bp("golden_test", m).f1)]), [5000, 2300, 2338], { size: 19, right: [1, 2] }),
  CAP(`Bảng 5.23. Ảnh hưởng của lượt rà quy ước golden test (${gtChanges.length} cặp sửa, mục 3.4.1).`),
  P(`Kết quả quan trọng nhất là **thứ hạng của các phương pháp cổ điển không ổn định giữa các tập đánh giá**. Trên CV, TF-IDF + LogReg ngang luật (${rp(bp("cv5", "tfidf_lr").f1)} và ${rp(bp("cv5", "rules").f1)}). Trên test ngẫu nhiên, nó tụt xuống ${rp(bp("random_test", "tfidf_lr").f1)}, thấp hơn cả baseline ghép cặp gần nhất (${rp(bp("random_test", "nearest").f1)}), vì precision chỉ còn ${rp(bp("random_test", "tfidf_lr").precision)}: n-gram ký tự học thuộc mặt chữ của các cặp đã thấy, nên khi gặp câu từ bản ghi khác thì đoán dương bừa. Ngược lại, luật, viết từ hướng dẫn chứ không học từ dữ liệu, đạt ${rp(bp("random_test", "rules").f1)} với precision ${rp(bp("random_test", "rules").precision)}. Với khoảng ${bench.cv5.rules.positive_micro.support} cặp dương huấn luyện, một mô hình chỉ dựa vào từ vựng không vượt được tri thức viết sẵn trong luật.`),
  P(`ViHealthBERT là ngoại lệ. Đây là phương pháp đơn lẻ tốt nhất trên CV (${rp(bp("cv5", "bert").f1)}, CI95 ${bci("cv5", "bert")}, precision ${rp(bp("cv5", "bert").precision)}), và giữ được mức ${rp(bp("random_test", "bert").f1)} trên test ngẫu nhiên thay vì sụp như TF-IDF: mô hình ngôn ngữ tiền huấn luyện có tri thức về tiếng Việt mà n-gram ký tự không có. Tuy vậy, một mình nó vẫn chưa vượt luật trên dữ liệu tự nhiên (${rp(bp("random_test", "bert").f1)} so với ${rp(bp("random_test", "rules").f1)}). Hai nguồn bổ sung cho nhau rõ rệt: luật có precision cao ở located_at với các mẫu câu điển hình, còn ViHealthBERT bắt được treated_by và treated_by_procedure, nơi luật gần như bất lực (Bảng 5.22: treated_by_procedure ${rp(bench.random_test.bert.per_relation.treated_by_procedure.f1)} so với ${rp(bench.random_test.rules.per_relation.treated_by_procedure.f1)}). Hợp hai nguồn nâng recall lên ${rp(bp("random_test", "bert+rules").recall)} và cho F1 ${rp(bp("random_test", "bert+rules").f1)}, cao nhất trên cả golden test v1.1 (${rp(bp("golden_test", "bert+rules").f1)}) lẫn test ngẫu nhiên.`),
  P(`Ba điều cần nói rõ khi diễn giải. Thứ nhất, trên CV, ViHealthBERT một mình (${rp(bp("cv5", "bert").f1)}) và hợp với luật (${rp(bp("cv5", "bert+rules").f1)}) gần như bằng nhau, nên CV không đủ để chọn giữa hai cách; lý do chọn union là một lý do có trước khi xem test: mô hình không có mẫu has_dosage và có rất ít diagnosed_by, nên chỉ luật xử lý được hai quan hệ này. Thứ hai, khoảng tin cậy của ViHealthBERT ∪ luật trên test ngẫu nhiên (${bci("random_test", "bert+rules")}) chồng lấn với luật (${bci("random_test", "rules")}); chênh lệch chưa có ý nghĩa thống kê. Thứ ba, trên golden test, các baseline tầm thường đạt điểm cao bất thường (Bảng 5.23) vì tập này bị làm giàu cặp dương; chỉ số trên tập này phải luôn được đọc cạnh baseline đồng xuất hiện. Mô hình đang dùng trong pipeline và knowledge graph vẫn là TF-IDF ∪ luật; chuyển sang ViHealthBERT ∪ luật là việc đầu tiên trong hướng phát triển (mục 7.3).`),
  NOTE("Nhãn RE v2 và nhãn của hai tập test là nhãn AI chưa có bác sĩ duyệt, do cùng một người gán (AI) theo cùng hướng dẫn. Nếu người gán có thiên lệch có hệ thống, mô hình học thiên lệch đó và hai tập test sẽ không phát hiện ra. Hai tập test dùng thực thể gold, nên đây là RE với thực thể gold, chưa phải RE end-to-end."),
  H3("5.4.4. RE end-to-end"),
  P("Chưa có kết quả định lượng: cần nhãn quan hệ trên thực thể do NER sinh ra, tức golden test đã duyệt cả NER lẫn RE. Công cụ đánh giá (scripts/golden_test/evaluate_e2e.py) đã sẵn sàng, tính ba chỉ số: NER strict/relaxed trên 6 loại, RE với thực thể gold và RE end-to-end (cạnh chỉ đúng khi NER tìm đúng cả hai thực thể và RE gán đúng quan hệ), kèm CI95 bootstrap theo đoạn."),
  H2("5.5. Kiểm thử"),
  P(PYTEST),
  H2("5.6. Knowledge graph trên split test"),
  P(`Đồ thị được dựng từ toàn bộ ${n(kgS.documents)} câu khác nhau của split test VietMed-NER, với thực thể do NER sinh ra (đúng như khi hệ thống chạy thật), chuẩn hóa ở chế độ thận trọng và RE union. Kết quả có ${n(kgS.nodes)} nút, trong đó ${kgS.normalized_nodes} nút có mã ICD-10 hoặc RxNorm, và ${kgS.edges} cạnh khác nhau ứng với ${kgS.edge_mentions} lần xuất hiện. ${n(kgS.isolated_nodes)} nút không có cạnh nào: phần lớn câu chỉ nhắc một thực thể hoặc không có cặp đúng kiểu.`),
  T(["Quan hệ", "Số cạnh khác nhau", "Số lần xuất hiện", "Từ mô hình", "Từ luật"], RELS.map((k) => { const es = kgRel(k); const src = (x) => es.reduce((a, e) => a + (e.sources[x] || 0), 0); return [k, es.length, es.reduce((a, e) => a + e.count, 0), src("model"), src("rule")]; }), [2600, 1800, 1800, 1700, 1738], { right: [1, 2, 3, 4] }),
  CAP(`Bảng 5.24. Cạnh của knowledge graph theo quan hệ (nguồn: ${KG_DIR}/kg.json).`),
  T(["Loại nút", "Số nút"], Object.entries(kgS.nodes_by_type).sort((a, b) => b[1] - a[1]).map(([k, v]) => [k, v]), [6000, 3638], { right: [1] }),
  CAP("Bảng 5.25. Số nút theo loại thực thể."),
  T(["Đầu", "Quan hệ", "Cuối", "Số lần", "Nguồn"], kg.edges.slice(0, 12).map((e) => [kgName[e.head], e.relation, kgName[e.tail], e.count, Object.keys(e.sources).join(", ")]), [2800, 1800, 2200, 900, 1938], { size: 19, right: [3] }),
  CAP("Bảng 5.26. Mười hai bộ ba xuất hiện nhiều nhất (tên nút là tên chuẩn khi có mã, nếu không là chữ gốc)."),
  P(`located_at chiếm ${pct(kgS.edges_by_relation.located_at / kgS.edges)} số cạnh, cao hơn tỉ lệ của nó trong các cặp dương huấn luyện (${pct(relCount(re2.final_model.labels, "located_at") / (re2.final_model.pairs - relCount(re2.final_model.labels, "NO_RELATION")))}), vì CONDITION và BODY_PART cùng xuất hiện trong câu nhiều hơn hẳn các cặp kiểu khác. Bảng 5.26 cho thấy cả điểm tốt lẫn lỗi. Điểm tốt: các cách nói khác nhau được gộp về một nút có mã, ví dụ nút “Đau, không đặc hiệu” (R52.9) gom “đau” và “đau nhức”, và mỗi cạnh giữ câu nguồn để kiểm tra. Lỗi có hai nguồn. Lỗi NER sinh nút là mảnh từ: “mất”, “tiêu”, “mọc” là phần còn lại của “mất răng”, “tiêu xương”, “mọc răng” khi NER cắt sai. Lỗi RE sinh cạnh sai về nghĩa: “mất răng → located_at → xương” xuất hiện vì câu nói về tiêu xương hàm sau khi mất răng. Cạnh đúng và cạnh sai đều có số lần xuất hiện nhỏ, nên bộ lọc “số lần tối thiểu” trên trang HTML chỉ giúp được một phần.`),
  NOTE(`Đồ thị là đầu ra của hệ thống, không phải tri thức đã kiểm chứng: chất lượng cạnh bị chặn trên bởi RE (F1 khoảng ${rp(re2u.f1)} trên golden test với thực thể gold) và còn thấp hơn khi thực thể do NER sinh ra. Đồ thị phù hợp để khám phá dữ liệu và tìm câu nguồn, chưa phù hợp để trả lời câu hỏi y khoa.`),
);

// ===== CHƯƠNG 6 =====
const errEx = X.ner_errors.slice(0, 4);
const reErr = X.re_preds.filter((p) => p.gold !== p.pred);
add(
  H1("CHƯƠNG 6. PHÂN TÍCH LỖI VÀ THẢO LUẬN"),
  SUM("Lỗi NER chủ yếu là lệch ranh giới span và nhãn gold nguồn không nhất quán, không phải nhầm loại. Trên bộ khảo sát cũ, mọi mã sai đến từ khớp gần đúng và đã có quy tắc chặn tổng quát; trên tập gold test, lỗi chủ yếu là bỏ sót cách nói dân gian chứ không phải gán sai. Lỗi RE phản ánh dữ liệu thưa: mô hình bỏ sót quan hệ có cách diễn đạt không điển hình và gán nhầm khi cụm bệnh đã chứa bộ phận cơ thể. Chương kết thúc bằng câu trả lời cho ba câu hỏi nghiên cứu."),
  H2("6.1. Lỗi NER"),
  H3("6.1.1. Theo loại thực thể"),
  P(`DOSAGE là loại yếu nhất (strict F1 ${f(s.DOSAGE["f1-score"])}) và nguyên nhân chủ yếu nằm ở precision (${f(s.DOSAGE.precision)}). Nhãn gốc UNITCALIBRATOR bao gồm cả số đo, mức độ và tỉ lệ, còn luật liều bổ sung thêm các cụm mà gold không gán. Vì định nghĩa DOSAGE của đề tài hẹp hơn nhãn nguồn, một phần con số này phản ánh sự lệch định nghĩa chứ không phải lỗi nhận diện.`),
  P(`PROCEDURE đứng thứ hai từ dưới lên (strict F1 ${f(s.PROCEDURE["f1-score"])}). Loại này gộp ba nhãn gốc, trong đó MEDDEVICETECHNIQUE và SURGERY vốn có F1 tầng 1 thấp (${f(t1.MEDDEVICETECHNIQUE["f1-score"])} và ${f(t1.SURGERY["f1-score"])}). Ranh giới của thủ thuật trong văn nói rất mơ hồ: cùng một câu có thể nói “mổ”, “mổ nội soi” và “cắt nhiệt”, và gold không nhất quán khi chọn cụm nào là thực thể.`),
  P(`BODY_PART (strict F1 ${f(s.BODY_PART["f1-score"])}) thường bị tách nhỏ, ví dụ “nội mạc” và “tử cung” thay vì “nội mạc tử cung”, hoặc lẫn với cụm bệnh chứa bộ phận. DRUG có recall cao nhưng precision thấp vì văn bản nói chứa nhiều thảo dược, thực phẩm chức năng và mỹ phẩm, mà mô hình gán DRUG còn gold thì gán loại phi y khoa.`),
  H3("6.1.2. Phân tích các câu lỗi nhiều nhất"),
  P("Bảng 6.1 liệt kê các câu có nhiều lỗi nhất trên tập test (top_error_cases.json). Nhiều lỗi thuộc ba dạng: (a) lệch ranh giới span — mô hình tách cụm dài thành nhiều mảnh; (b) cụm bệnh chứa bộ phận cơ thể, nơi gold và dự đoán chọn cách cắt khác nhau; (c) nhãn gold không nhất quán, ví dụ “polyp” và “nhân xơ” được gold gán BODY_PART (từ ORGAN) trong khi mô hình gán CONDITION — trong các trường hợp này dự đoán của mô hình có thể hợp lý hơn gold."),
  T(["#", "Câu (rút gọn)", "Tóm tắt lỗi"], errEx.map((e) => [e.index, e.text.length > 110 ? e.text.slice(0, 110) + "…" : e.text, typeof e.error_summary === "string" ? e.error_summary : JSON.stringify(e.error_summary)]), [700, 4300, 4638], { size: 19 }),
  CAP("Bảng 6.1. Các câu test có nhiều lỗi NER nhất (nguồn: top_error_cases.json)."),
  ...errEx.slice(0, 2).flatMap((e) => [
    PN(`**Câu ${e.index}:** “${e.text}”`),
    T(["Gold", "Dự đoán"], (() => { const g = e.gold_entities.map((x) => `[${x.label}] ${x.surface_text}`), p = e.predicted_entities.map((x) => `[${x.label}] ${x.surface_text}`); const m = Math.max(g.length, p.length); return Array.from({ length: m }, (_, i) => [g[i] || "", p[i] || ""]); })(), [4819, 4819], { size: 20 }),
  ]),
  CAP("Ví dụ 6.1. So sánh gold và dự đoán cho hai câu lỗi nhiều nhất."),
  P("Ở câu đầu tiên, mô hình nhận đúng mọi khái niệm nhưng cắt span khác gold: “rối loạn” thay vì “rối loạn chức năng”, “nội mạc” + “tử cung” thay vì “nội mạc tử cung”, và gán “polyp” là CONDITION trong khi gold gán BODY_PART. Theo strict match, câu này tạo 4 FN và 6 FP dù phần lớn thông tin được nhận ra. Đây là lý do cần báo cáo cả relaxed match và phân tích lỗi định tính bên cạnh con số tổng."),
  H2("6.2. Lỗi chuẩn hóa ICD-10"),
  P("Mọi mã sai trong Bảng 5.10 đều đến từ bước khớp gần đúng `token_set_ratio`. Như đã trình bày ở mục 2.6, phép đo này cho điểm 100 khi tập từ của chuỗi ngắn là tập con của chuỗi dài: “nhồi máu” khớp “nhồi máu lách”, “đậu mùa bò” khớp “đậu mùa”. Khi hai tập từ gần như là tập con của nhau, điểm vẫn cao: “huyết áp cao” khớp “đo huyết áp” (0,87), “đa xơ cứng” khớp “gan xơ cứng” (0,86). Ngưỡng 0,85 vì vậy không đủ để chặn các trường hợp chung từ khóa nhưng khác nghĩa."),
  P("Nhận xét về cấu trúc tên bệnh tiếng Việt dẫn tới bản sửa: từ đầu cụm (head word) thường quyết định loại khái niệm (“đo” huyết áp là thủ thuật, “gan” xơ cứng là bệnh gan), còn các từ sau là bổ nghĩa. Yêu cầu từ đầu cụm của ứng viên phải xuất hiện trong truy vấn chặn được nhóm lỗi thứ nhất. Nhóm lỗi thứ hai (tập con với chuỗi ngắn) được chặn bằng cách từ chối khi chuỗi ngắn hơn chỉ có một hoặc hai từ, vì khi đó các từ thêm vào gần như chắc chắn thay đổi bệnh. Hai quy tắc được kiểm thử bằng 18 ca cũ (đều giữ nguyên) và các ca mới (tests/test_normalization.py, test_fuzzy_subset_false_matches_rejected)."),
  P("Một ca còn nghi vấn là “rối loạn vận động” → F44.4 (rối loạn vận động phân ly). Trong ngữ cảnh Parkinson, rối loạn vận động thường không phải rối loạn phân ly; nhưng không có ngữ cảnh thì không thể quyết định. Đây là giới hạn cơ bản của chuẩn hóa không dùng ngữ cảnh. Ca này cũng là lý do của ràng buộc phủ từ thêm ngày 07/11 (Bảng 4.5): khi không có ngữ cảnh, ứng viên không được thêm khái niệm (“phân ly”) mà người nói không nhắc."),
  P(`Trên tập gold chuẩn hóa test, lỗi chủ yếu là bỏ sót chứ không phải gán sai: chế độ thận trọng chỉ trả lời ${pct(nc("ICD-10").system.coverage)} dạng ICD-10 có mã, nhưng mọi câu trả lời đều đúng. Đọc lại các dạng bị bỏ sót cho thấy chúng chủ yếu là cụm ngắn (trung vị 3 từ) thuộc hai nhóm. Nhóm thứ nhất là cách nói dân gian không có tên tương ứng trong danh mục và chưa có trong từ điển vì không xuất hiện ở train/dev: “có thai” (Z33), “rong kinh” (N92.0), “ra máu” (R58), “khiếm thính” (H91.9). Nhóm thứ hai là tên ngắn mà mục danh mục gần nhất có thêm từ bổ nghĩa, nên ràng buộc phủ từ từ chối: “viêm gan” với B19.9, “điếc” với H91.9, “mất răng” với K08.1. Trong ${icdMiss.length} dạng bị bỏ sót, ${icdMissTop} dạng vẫn có mã đúng trong 10 ứng viên, nên người dùng chọn được; phần còn lại cần từ điển lớn hơn hoặc mô hình ngữ nghĩa. Với RxNorm, các lỗi gán sai còn lại (“protein”, “gel”, “carbonate”) là từ tiếng Anh có trong RxNorm nhưng trong câu nói về thực phẩm hoặc mỹ phẩm, tức lại là vấn đề ngữ cảnh.`),
  H2("6.3. Lỗi trích xuất quan hệ"),
  P(`Trên dev/test seed 42, mô hình LogReg có ${reErr.length} dự đoán khác gold trong tổng số ${X.re_preds.length} cặp (Bảng 6.2). Nhóm lớn nhất là các cặp gold NO_RELATION có kiểu treated_by (CONDITION–DRUG) nhận trạng thái unsupported, vì train không có cặp treated_by dương — không tính là lỗi FP nhưng cho thấy hệ thống chưa thể xử lý quan hệ thuốc–bệnh.`),
  T(["Đoạn", "Head → Tail", "Gold", "Dự đoán", "Nhận xét"], reErr.map((p) => [p.id, `${p.head} → ${p.tail}`, p.gold, p.pred === null ? "unsupported" : p.pred, p.pred === null ? "Lớp chưa học" : p.gold === "NO_RELATION" ? "Dương giả" : "Bỏ sót"]), [1300, 3200, 1700, 1700, 1738], { size: 20 }),
  CAP("Bảng 6.2. Các dự đoán RE khác gold trên dev/test seed 42."),
  P("Lỗi bỏ sót xảy ra khi cách nối không điển hình. Trong “gáy nó mới đau”, bộ phận đứng trước bệnh và không có từ “ở”. Trong “cục máu đông ở trong tim”, khoảng cách giữa hai thực thể xa hơn các mẫu train. Trong “tê bì nhiều ở cái bàn tay không ạ”, câu hỏi được quy ước tính như khẳng định, nhưng mô hình chưa thấy đủ mẫu câu hỏi để học."),
  P("Lỗi dương giả có hai dạng. Dạng thứ nhất là cụm CONDITION đã chứa bộ phận: với “chức năng gan bị giảm” → “gan”, mô hình dự đoán located_at trong khi quy ước cụm đầy đủ yêu cầu NO_RELATION. Mô hình n-gram ký tự không biết rằng chữ “gan” ở tail đã nằm trong head. Dạng thứ hai là CONDITION chung chung và quan hệ nhân quả ngược: “biến chứng” → “phẫu thuật” bị dự đoán treated_by_procedure, trong khi văn bản nói phẫu thuật có thể gây biến chứng. Cả hai dạng đều có thể giảm bằng đặc trưng chỉ rõ head có chứa văn bản của tail hay không, và bằng mẫu âm có chủ đích cho quan hệ nhân quả."),
  H2("6.4. Trả lời các câu hỏi nghiên cứu"),
  P(`**Câu hỏi 1** (học máy có tốt hơn luật?): tùy loại học máy, và chưa có ý nghĩa thống kê. Trên gold v1, khoảng tin cậy hai phương pháp chồng lấn (${rp(cvR.positive_micro_f1_ci95[0])}–${rp(cvR.positive_micro_f1_ci95[1])} so với ${rp(cvL.positive_micro_f1_ci95[0])}–${rp(cvL.positive_micro_f1_ci95[1])}) và chỉ có ${posAfter} cặp dương. Kết quả có giá trị ở chỗ cho thấy ưu thế của mô hình trên nhãn AI chủ yếu do học từ chung, và quy ước nhãn ảnh hưởng mạnh tới kết luận. Khi thêm RE v2, mô hình một mình vẫn chưa vượt luật (F1 golden test ${rp(re2pm("golden_test", "model_v2").f1)} so với ${rp(re2pm("golden_test", "rules").f1)}), nhưng hợp hai nguồn cho kết quả tốt nhất cả trong CV (${rp(re2cvu.f1)}) lẫn trên golden test (${rp(re2u.f1)}). Benchmark mở rộng (mục 5.4.3) làm rõ hơn: mô hình chỉ dựa vào mặt chữ (TF-IDF) không ổn định và tụt dưới luật trên dữ liệu tự nhiên (${rp(bp("random_test", "tfidf_lr").f1)} so với ${rp(bp("random_test", "rules").f1)}); ViHealthBERT tốt nhất trên CV (${rp(bp("cv5", "bert").f1)}) và hợp với luật cho kết quả cao nhất trên cả hai tập test (${rp(bp("random_test", "bert+rules").f1)} trên test ngẫu nhiên). Câu trả lời thực tế vì vậy là: một mô hình ngôn ngữ tiền huấn luyện cộng luật là cách tốt nhất hiện có, nhưng với khoảng ${bench.cv5.rules.positive_micro.support} cặp dương huấn luyện thì chưa phương pháp nào vượt luật có ý nghĩa thống kê.`),
  P("**Câu hỏi 2** (ảnh hưởng của lỗi NER): chưa đo được định lượng, vì cần golden test đã duyệt. Phân tích định tính: với strict NER F1 khoảng 0,62 và nhiều lỗi lệch ranh giới, xác suất cả hai đầu mút của một cạnh đều khớp chính xác thấp hơn đáng kể; ngoài ra NER sinh thực thể chung chung mà gold RE không có, nay đã được lọc ở đầu vào RE. RE end-to-end vì vậy chắc chắn thấp hơn RE trên thực thể gold. Knowledge graph trên split test (5.6) cho bằng chứng định tính: phần lớn nút vô nghĩa như “mất”, “tiêu” là mảnh NER, và các cạnh nối với chúng sai dù RE gán đúng kiểu quan hệ cho cặp mà nó nhận được."),
  P(`**Câu hỏi 3** (lợi ích và tác hại của bước bổ sung): ${abl ? ablText(true) : "chưa có kết quả ablation."} Với chuẩn hóa, khớp chính xác và đồng nghĩa luôn cho mã hợp lý, còn khớp gần đúng là nguồn duy nhất của mã sai; sau bản sửa, khớp gần đúng còn ${icd.by_method.fuzzy || 0} mention.`),
  H2("6.5. Lệch quy ước giữa NER và dữ liệu RE"),
  P("Gold v1 đã xóa các thực thể chung chung như “điều trị” (PROCEDURE) và “thuốc” (DRUG), nhưng pipeline NER vẫn sinh ra chúng (TREATMENT → PROCEDURE; Luật 1 chỉ chặn “điều trị” khi bị gán DRUG). Trước bản sửa, RE nối “đau” với “điều trị” (mục 4.8). Bản sửa ngày 06/11/2026 lọc các thực thể này ở đầu vào RE thay vì ở NER, vì xóa chúng khỏi NER sẽ làm giảm recall NER trên VietMed-NER (gold nguồn vẫn gán TREATMENT cho “điều trị”). Danh sách được giữ ở một nơi duy nhất và có kiểm thử."),
  H2("6.6. Tính độc lập của dữ liệu đánh giá"),
  P("Khóa luận không khẳng định đánh giá hoàn toàn không rò rỉ. Thay vào đó, các nguồn rò rỉ đã biết được liệt kê để người đọc tự đánh giá mức tin cậy. Bộ RE 600 đoạn lấy từ split train của VietMed-NER, tức NER đã học các câu này, nên không được dùng làm test end-to-end. Việc chia theo văn bản chuẩn hóa không bảo đảm độc lập người nói hay cuộc hội thoại, vì dữ liệu không có metadata này."),
  P("Với NER, checkpoint được chọn theo F1 trên tập đánh giá sau mỗi epoch, nhưng training_args.bin không ghi tập đó là validation hay test. Nếu là test thì kết quả NER trên test bị lạc quan; điểm này cần được xác minh với nguồn huấn luyện checkpoint. Ngoài ra, một số luật hậu xử lý được rút ra khi phân tích lỗi, và top_error_cases.json được tạo từ split test, nên cần ghi rõ nguồn gốc của từng luật. Với chuẩn hóa, alias và ràng buộc mới được thiết kế sau khi thấy lỗi trên gold v1, nên kết quả sau sửa trên chính bộ này là lạc quan."),
  H2("6.7. Nhãn AI và giới hạn của các kết quả mới"),
  P("Ba bộ dữ liệu thêm ngày 07/11/2026 (gold chuẩn hóa, RE v2, nhãn golden test) do AI gán vì người duyệt không có thời gian. Quyết định này đánh đổi độ tin cậy lấy khả năng có số đo theo đúng đề cương. Để sự đánh đổi minh bạch, khóa luận giữ bốn nguyên tắc: mọi bản ghi mang human_verified = false; bộ nạp dữ liệu từ chối nhãn AI nếu không bật cờ tường minh; mọi bảng kết quả trên các bộ này ghi chú “nhãn AI”; và phiếu duyệt Excel cho bác sĩ đã được chuẩn bị, kèm lệnh chạy lại toàn bộ đánh giá sau khi duyệt."),
  P("Rủi ro lớn nhất không phải nhãn AI sai ngẫu nhiên mà là sai có hệ thống. RE v2 (dữ liệu huấn luyện) và golden test (dữ liệu đánh giá) được gán bởi cùng một người gán theo cùng hướng dẫn. Nếu người gán luôn hiểu một quy ước theo cùng một cách lệch, mô hình sẽ học cách hiểu đó và golden test sẽ chấm nó là đúng; F1 sẽ cao hơn thực tế. Kiểm tra hai lượt chỉ giảm được lỗi ngẫu nhiên. Chỉ một người duyệt độc lập mới loại được rủi ro này, vì vậy việc duyệt golden test được xếp ưu tiên đầu ở Chương 7."),
  H2("6.8. Ý nghĩa và khả năng ứng dụng"),
  P("Ở trạng thái hiện tại, hệ thống phù hợp làm công cụ hỗ trợ: gợi ý thực thể và mã bệnh cho người nhập liệu xác nhận, hoặc tiền xử lý cho tìm kiếm và thống kê, nơi sai sót có thể được kiểm tra. Hệ thống chưa phù hợp để tự động ra quyết định lâm sàng. Danh sách top-k ứng viên mã và trang knowledge graph có câu nguồn được thiết kế cho đúng kịch bản người xác nhận này. Thiết kế ưu tiên không gán mã, trạng thái “unsupported” cho quan hệ chưa học và trường re_excluded giúp người dùng phân biệt “không có” với “không biết” — một yêu cầu quan trọng trong miền y tế."),
);

// ===== CHƯƠNG 7 =====
add(
  H1("CHƯƠNG 7. KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN"),
  H2("7.1. Kết luận"),
  P(`Khóa luận đã xây dựng pipeline trích xuất thông tin y tế tiếng Việt chạy từ đầu đến cuối. NER đạt strict micro-F1 ${f(s["micro avg"]["f1-score"])} và relaxed ${f(r["micro avg"]["f1-score"])} trên ${n(nerNew.lat.total_samples)} câu test với khoảng ${f(nerNew.lat.mean_latency_ms, 0)} ms/câu trên CPU. Chuẩn hóa ưu tiên độ chính xác: trên tập gold test, ICD-10 đạt Accuracy ${rp(nc("ICD-10").system.accuracy)} với precision ${rp(nc("ICD-10").system.precision_answered)} khi trả lời, gấp khoảng năm lần baseline khớp chính xác; chế độ luôn trả lời đạt ${rp(nc("ICD-10").always.accuracy)} và mã đúng nằm trong 10 ứng viên ở ${pct(nc("ICD-10").top10_acc)} trường hợp; RxNorm đạt ${rp(nc("RxNorm").system.accuracy)}. Với RE, khóa luận xây dựng bộ gold v1 600 đoạn có người duyệt, bộ RE v2 ${re2.data.v2.samples} câu nhãn AI, tập test ngẫu nhiên ${rtMan.chosen_sentences} câu và một benchmark mười phương pháp; ViHealthBERT tốt nhất trong CV (F1 ${rp(bp("cv5", "bert").f1)}) và hợp với luật đạt ${rp(bp("random_test", "bert+rules").f1)} trên test ngẫu nhiên, nhỉnh hơn luật (${rp(bp("random_test", "rules").f1)}). Kết quả cho thấy dữ liệu quan hệ trong lời nói y tế rất thưa và quy ước nhãn quyết định kết luận so sánh. Cuối cùng, kết quả được gộp thành knowledge graph ${n(kgS.nodes)} nút, ${kgS.edges} cạnh, có trang HTML để tra cứu câu nguồn.`),
  P(`Quá trình soát lại toàn bộ số liệu, luồng xử lý và mã nguồn trước khi viết báo cáo phát hiện ${A.length} điểm cần lưu ý (Phụ lục A), trong đó các lỗi đã sửa đều có kiểm thử, các điểm còn lại được ghi rõ là hạn chế hoặc việc cần làm.`),
  H2("7.2. Hạn chế"),
  P(`Hạn chế lớn nhất là miền dữ liệu: hệ thống được đánh giá trên lời nói y tế chép lại, chưa trên bệnh án bệnh viện. Hạn chế thứ hai là dữ liệu RE nhỏ: gold v1 có ${posAfter} cặp dương, RE v2 thêm ${re2pos}, không có has_dosage nào để học; gold v1 có một người duyệt và chưa đo kappa. Hạn chế thứ ba là thứ hạng các phương pháp RE còn phụ thuộc tập đánh giá và chưa có chênh lệch nào có ý nghĩa thống kê; mô hình tốt nhất (ViHealthBERT ∪ luật) chưa được đưa vào pipeline. Hạn chế thứ tư là nguồn nhãn: tập gold chuẩn hóa, RE v2 và golden test là nhãn AI chưa duyệt, và RE v2 cùng golden test do cùng một người gán, nên các con số trên chúng là tạm thời; RE end-to-end trên thực thể do NER sinh ra chưa được đo. Hạn chế thứ năm là checkpoint NER kế thừa, chưa ghi nhận tập dùng để chọn checkpoint, F1 validation tốt nhất, epoch được chọn và phần cứng huấn luyện. Cuối cùng, chuẩn hóa không dùng ngữ cảnh, và RxNorm không bao phủ thuốc, thảo dược Việt Nam.`),
  H2("7.3. Hướng phát triển"),
  ...LIST([
    "Đưa ViHealthBERT ∪ luật vào pipeline và knowledge graph thay cho TF-IDF ∪ luật (cần lưu mô hình cuối và nạp lúc suy luận), vì đây là phương pháp tốt nhất trên cả hai tập test (mục 5.4.3).",
    "Bác sĩ duyệt nhãn AI của golden test v1 (150 đoạn từ split test), tính kappa trên 30 đoạn chồng lấp và chạy đánh giá end-to-end; đây là việc ưu tiên đầu vì loại được rủi ro sai lệch có hệ thống (6.7).",
    "Bác sĩ duyệt phiếu gold chuẩn hóa test (bắt buộc) và dev, rồi chạy lại đánh giá; bổ sung từ điển đồng nghĩa theo các dạng bị bỏ sót ở dev.",
    "Duyệt RE v2 và huấn luyện lại; tìm nguồn văn bản có đơn thuốc thật cho has_dosage, vì VietMed-NER hầu như không có cụm liều; khi đủ dữ liệu, tinh chỉnh ViHealthBERT với typed markers và so sánh với baseline hiện tại.",
    "Thay xếp hạng TF-IDF bằng mô hình embedding đa ngôn ngữ cho top-k ICD-10, và dùng ngữ cảnh câu khi chuẩn hóa.",
    "Xây Web/API demo (FastAPI) nhận văn bản và trả JSON cùng đồ thị; chuẩn hóa thêm nút BODY_PART/TEST/PROCEDURE để đồ thị gộp tốt hơn.",
    "Chia chunk theo số subword thực tế và xử lý xuống dòng để dùng cho văn bản dài (A17–A18).",
    "Thử nghiệm trên văn bản bệnh án thật nếu có nguồn dữ liệu được phép sử dụng; cân nhắc danh mục thuốc Việt Nam thay cho RxNorm.",
  ]),
);

// ===== TÀI LIỆU THAM KHẢO =====
add(
  H1("TÀI LIỆU THAM KHẢO"),
  ...REFLIST([
    "Le-Duc K. và cộng sự. Medical Spoken Named Entity Recognition. NAACL 2025 Industry Track. https://aclanthology.org/2025.naacl-industry.59/",
    "VietMed-NER dataset. https://huggingface.co/datasets/leduckhai/VietMed-NER",
    "Minh N. và cộng sự. ViHealthBERT: Pre-trained Language Models for Vietnamese in Health Text Mining. LREC 2022. https://aclanthology.org/2022.lrec-1.35/",
    "Nguyen D. Q., Nguyen A. T. PhoBERT: Pre-trained language models for Vietnamese. Findings of EMNLP 2020.",
    "Truong T. H. và cộng sự. COVID-19 Named Entity Recognition for Vietnamese. NAACL 2021.",
    "Vaswani A. và cộng sự. Attention Is All You Need. NeurIPS 2017.",
    "Devlin J. và cộng sự. BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding. NAACL 2019.",
    "Liu Y. và cộng sự. RoBERTa: A Robustly Optimized BERT Pretraining Approach. arXiv:1907.11692, 2019.",
    "Lafferty J., McCallum A., Pereira F. Conditional Random Fields: Probabilistic Models for Segmenting and Labeling Sequence Data. ICML 2001.",
    "Lample G. và cộng sự. Neural Architectures for Named Entity Recognition. NAACL 2016.",
    "Baldini Soares L. và cộng sự. Matching the Blanks: Distributional Similarity for Relation Learning. ACL 2019.",
    "Zhong Z., Chen D. A Frustratingly Easy Approach for Entity and Relation Extraction (PURE). NAACL 2021. https://aclanthology.org/2021.naacl-main.5/",
    "Uzuner Ö. và cộng sự. 2010 i2b2/VA challenge on concepts, assertions, and relations in clinical text. JAMIA 2011. https://pmc.ncbi.nlm.nih.gov/articles/PMC3168320/",
    "Henry S. và cộng sự. 2018 n2c2 shared task on adverse drug events and medication extraction in electronic health records. JAMIA 2020. https://pmc.ncbi.nlm.nih.gov/articles/PMC7489085/",
    "Cohen J. A Coefficient of Agreement for Nominal Scales. Educational and Psychological Measurement, 1960.",
    "Efron B., Tibshirani R. An Introduction to the Bootstrap. Chapman & Hall, 1993.",
    "Pedregosa F. và cộng sự. Scikit-learn: Machine Learning in Python. JMLR, 2011.",
    "Wolf T. và cộng sự. Transformers: State-of-the-Art Natural Language Processing. EMNLP 2020 (System Demonstrations).",
    "Nakayama H. seqeval: A Python framework for sequence labeling evaluation. https://github.com/chakki-works/seqeval, 2018.",
    "RapidFuzz. https://github.com/rapidfuzz/RapidFuzz",
    "Bộ Y tế. Danh mục ICD-10 (tệp ICD-10/phu-lu-c-1-danh-mu-c-icd-10-thay-the-dmdc-phie-n-ba-n-6.xlsx và ICD-10/06-byt-kem.pdf). [[Ghi số hiệu, ngày ban hành văn bản]]",
    "National Library of Medicine. RxNorm và RxNav REST API. https://lhncbc.nlm.nih.gov/RxNav/",
  ]),
  NOTE("Tên tác giả, tiêu đề và nơi công bố của mọi tài liệu cần được đối chiếu với trang gốc và trình bày theo quy định trích dẫn của trường trước khi nộp."),
);

// ===== PHỤ LỤC A =====
add(
  H1("PHỤ LỤC A. KẾT QUẢ SOÁT SỐ LIỆU, LUỒNG XỬ LÝ VÀ MÃ NGUỒN"),
  P("Bảng dưới đây tổng hợp các điểm không nhất quán được phát hiện khi đối chiếu tài liệu, số liệu và mã nguồn ngày 05–07/11/2026. Mọi số liệu trong báo cáo được đọc trực tiếp từ tệp kết quả bằng chương trình (outputs/bao_cao_khoa_luan_2026-11-05/build_report.js), không chép tay. Các phép đo NER được chạy lại để xác nhận."),
  T(["ID", "Vấn đề", "Bằng chứng", "Ảnh hưởng", "Trạng thái"], A, [600, 2900, 2100, 2000, 2038], { size: 19 }),
  CAP("Bảng A.1. Danh sách vấn đề đã soát."),
  H2("A.1. Chi tiết hai bản sửa"),
  P("**Bản sửa A7 (normalization/icd10.py, normalization/data/icd10_synonyms.json).** Thêm hai ràng buộc vào `_fuzzy_search`: từ đầu cụm của ứng viên (bỏ qua “bệnh”, “lý”, “chứng”) phải xuất hiện trong truy vấn với ratio ≥ 80; và từ chối khi một tập từ là tập con thực sự của tập kia và tập ngắn hơn có tối đa hai từ. Thêm sáu alias. Kiểm thử: test_fuzzy_subset_false_matches_rejected; toàn bộ ca cũ của test_normalization.py vẫn đạt."),
  P("**Bản sửa A6 (relation_extraction/data.py, relation_extraction/pipeline.py, scripts/apply_paper_review.py).** Chuyển danh sách thực thể chung vào `GENERIC_ENTITIES` và hàm `is_generic`; MedicalREPipeline bỏ các thực thể này khỏi bước sinh cặp, đánh dấu `re_excluded` và liệt kê trong `re_metadata.generic_entities_skipped`; apply_paper_review.py dùng chung danh sách. Gold v1 sinh lại giống hệt từng byte. Kiểm thử: test_pipeline_skips_generic_entities_like_gold_v1."),
);

// ===== PHỤ LỤC B, C =====
add(
  H1("PHỤ LỤC B. HƯỚNG DẪN TÁI LẬP"),
  P("Chạy từ thư mục gốc repository trên Windows PowerShell, dùng môi trường `.venv`. Trọng số NER đặt tại Model/vihealthbert-ner-vietmed-v2-final/model.safetensors (xem Model/README.md)."),
  ...CODE([
    "pip install -r requirements.txt",
    "# Kiểm thử",
    ".venv\\Scripts\\python.exe -X utf8 -m pytest tests -q",
    "# Đánh giá NER (khoảng 6–7 phút trên CPU)",
    `.venv\\Scripts\\python.exe -X utf8 eval/run_eval.py --output-dir ${NER_DIR}`,
    "# Ablation NER (khoảng 20 phút)",
    `.venv\\Scripts\\python.exe -X utf8 scripts/run_ner_ablation.py --out ${ABL_DIR}`,
    "# Tạo gold v1 từ kết quả duyệt",
    ".venv\\Scripts\\python.exe -X utf8 scripts/apply_paper_review.py --reviewer \"<tên>\" --reviewed-at <YYYY-MM-DD>",
    "# Huấn luyện RE trên gold v1",
    ".venv\\Scripts\\python.exe -X utf8 -m relation_extraction train --data data/re_gold_v1/annotations_gold_v1.jsonl --output outputs/re_gold_v1_baseline/seed42 --seed 42",
    "# So sánh luật và LogReg (CV 5 fold, CI95)",
    ".venv\\Scripts\\python.exe -X utf8 scripts/re_compare_baselines.py --data data/re_gold_v1/annotations_gold_v1.jsonl --out outputs/re_gold_v1_baseline/compare",
    "# Demo NER → RE",
    ".venv\\Scripts\\python.exe -X utf8 -m relation_extraction predict --model outputs/re_gold_v1_baseline/seed42/model.joblib --text \"Bệnh nhân đau ở vùng bụng, được điều trị bằng phẫu thuật.\"",
    "# Golden test (sau khi duyệt phiếu)",
    ".venv\\Scripts\\python.exe -X utf8 scripts/golden_test/import_workbook.py --workbook <phiếu đã duyệt> --annotator A",
    ".venv\\Scripts\\python.exe -X utf8 scripts/golden_test/evaluate_e2e.py --gold data/golden_test/v1/gold.jsonl --re-model outputs/re_gold_v1_baseline/seed42/model.joblib",
    "# Đánh giá chuẩn hóa trên tập gold (dev để chọn, test để báo cáo)",
    ".venv\\Scripts\\python.exe -X utf8 scripts/normalization_eval/evaluate.py --gold data/norm_gold_v1/gold_test.jsonl --out eval/normalization_<ngày>/test",
    "# Ghép nhãn RE v2, huấn luyện và so sánh 5 phương pháp (CV + golden test)",
    ".venv\\Scripts\\python.exe -X utf8 scripts/re_dataset/merge_labels.py --candidates data/re_ai_v2/candidates.jsonl --labels data/re_ai_v2/labels_main.txt --candidates data/re_ai_v2/candidates_targeted.jsonl --labels data/re_ai_v2/labels_targeted.txt --out data/re_ai_v2/annotations_ai_v2.jsonl",
    ".venv\\Scripts\\python.exe -X utf8 scripts/re_dataset/train_eval.py --out outputs/re_ai_v2",
    "# Baseline NER (từ điển, CRF; khoảng 30 phút CPU)",
    "cd scripts/ner_experiments; ..\\..\\.venv\\Scripts\\python.exe -X utf8 baselines.py --out ../../eval/ner_baselines_2026-11-08",
    "# Tập RE test ngẫu nhiên, golden test v1.1, đồng thuận nhãn",
    ".venv\\Scripts\\python.exe -X utf8 scripts/re_dataset/build_random_test.py --n 200",
    ".venv\\Scripts\\python.exe -X utf8 scripts/golden_test/relabel_consistency.py",
    ".venv\\Scripts\\python.exe -X utf8 scripts/re_dataset/agreement.py --out outputs/re_ai_v2/agreement.json",
    "# ViHealthBERT cho RE (GPU, môi trường .venv-gpu có PyTorch CUDA; khoảng 2 giờ trên GTX 1650)",
    `.venv-gpu\\Scripts\\python.exe -X utf8 scripts/re_dataset/bert_re.py --out ${BENCH_DIR}`,
    "# Benchmark RE mười phương pháp",
    `.venv\\Scripts\\python.exe -X utf8 scripts/re_dataset/benchmark.py --out ${BENCH_DIR}`,
    "# Knowledge graph trên split test (NER chạy khoảng 10 phút trên CPU)",
    `.venv\\Scripts\\python.exe -X utf8 scripts/build_kg.py --split test --out ${KG_DIR}`,
    "# Dựng lại báo cáo (cần Node.js và gói docx)",
    "node outputs/bao_cao_khoa_luan_2026-11-05/build_report.js <repo> <file.docx> eval/results_2026-11-05",
    "# Hướng dẫn đọc và giải thích toàn hệ thống: docs/HUONG_DAN_HE_THONG.md",
  ]),
  H1("PHỤ LỤC C. DANH MỤC TỆP KẾT QUẢ"),
  T(["Tệp", "Nội dung"], [
    [`${NER_DIR}/`, "Kết quả NER chạy lại 05/11/2026 (tầng 1, tầng 2, độ trễ, ma trận nhầm lẫn, câu lỗi nhiều nhất)"],
    [`${ABL_DIR}/`, "Ablation NER 06/11/2026"],
    ["eval/results/", "Kết quả NER cũ 17/09/2026 (giữ để đối chiếu)"],
    ["data/re_gold_v1/annotations_gold_v1.jsonl", `Gold v1, 600 đoạn; SHA-256 ${gold.output_sha256.slice(0, 16)}…`],
    ["data/re_gold_v1/manifest.json", "Nguồn, quy ước, thống kê trước/sau, người duyệt"],
    ["data/re_gold_v1/decisions_applied.csv", "40 đề xuất và quyết định cuối đã áp"],
    ["outputs/vietmed_600_RE_review/review_2026_10_15/", `Bản AI rà soát lần hai; SHA-256 ${gold.source_sha256.slice(0, 16)}…`],
    ["outputs/re_gold_v1_baseline/seed42/", "Mô hình RE, các split, dự đoán, report.json"],
    ["outputs/re_gold_v1_baseline/compare/", "So sánh luật/LogReg, CV 5 fold, CI95"],
    ["outputs/re_gold_v1_baseline/demo_ner_re.json", "Demo NER → RE với mô hình gold v1"],
    ["outputs/re_baselines/", "So sánh tương tự trên nhãn AI (trước duyệt)"],
    ["data/golden_test/v1/", "Ứng viên golden test, phiếu duyệt Excel, manifest"],
    ["data/norm_gold_v1/", "Gold chuẩn hóa dev/test (nhãn AI), phiếu duyệt Excel, manifest"],
    [`${NORM_DIR}/`, "Đánh giá chuẩn hóa trước/sau cải tiến trên dev và test, comparison.md"],
    ["data/re_ai_v2/", "Bộ RE v2: ứng viên, tệp nhãn hai lượt, annotations_ai_v2.jsonl"],
    ["outputs/re_ai_v2/", "Mô hình RE cuối (model.joblib), report.json, summary.md, dự đoán golden test"],
    ["data/golden_test/v1/ai_labels.jsonl", "Nhãn AI tiền gán cho golden test"],
    [`${KG_DIR}/`, "Knowledge graph: kg.html, kg.json, triples.csv, nodes.csv, kg.graphml, stats.md"],
    [`${BENCH_DIR}/`, "Benchmark RE: benchmark.json, summary.md, bert_predictions.json, nhật ký ViHealthBERT"],
    ["data/re_test_random_v1/", "Tập RE test ngẫu nhiên: ứng viên, labels.txt, annotations.jsonl, manifest"],
    ["data/golden_test/v1/ai_labels_v1_1.jsonl", "Golden test v1.1 và ai_labels_v1_1_changes.csv (17 thay đổi)"],
    ["outputs/re_ai_v2/agreement.json", "Đồng thuận nhãn AI với người duyệt trên bộ 600 đoạn"],
    [`${NERB_DIR}/`, "Baseline NER (từ điển, CRF) và điểm checkpoint kế thừa cùng hàm chấm"],
    ["docs/HUONG_DAN_HE_THONG.md", "Hướng dẫn và giải thích toàn hệ thống"],
    ["outputs/bao_cao_khoa_luan_2026-11-05/", "icd10_check*.json, extra.json, pytest_collect.txt, build_report.js"],
  ], [4300, 5338], { size: 20 }),
);

// ===== PHỤ LỤC D: Hướng dẫn gán nhãn =====
add(
  H1("PHỤ LỤC D. HƯỚNG DẪN GÁN NHÃN QUAN HỆ"),
  P("Hướng dẫn tổng hợp từ docs/RE_LABELS.md, hướng dẫn phiếu duyệt và các quy ước chốt ngày 05/11/2026. Ví dụ được trích từ gold v1."),
  H2("D.1. Nguyên tắc chung"),
  ...LIST([
    "Sửa thực thể trước, sau đó mới xét quan hệ. Nếu sửa thực thể thì phải xét lại mọi cặp liên quan.",
    "Chỉ xét cặp có kiểu và chiều đúng schema; cặp khác kiểu không gán NO_RELATION mà nằm ngoài phạm vi.",
    "Gán dương khi văn bản thể hiện rõ quan hệ giữa chính hai thực thể; giữ nguyên chiều head → tail kể cả khi thứ tự trong câu ngược lại.",
    "Gán NO_RELATION khi văn bản không thể hiện quan hệ tương ứng; đồng xuất hiện không đủ căn cứ.",
    "Gán CHUA_RO khi thiếu ngữ cảnh, câu bị cắt, hoặc chưa có quy ước; CHUA_RO không đi vào huấn luyện.",
    "Gán nhãn theo văn bản, không xác nhận tính đúng y khoa của phát biểu nguồn.",
  ]),
  H2("D.2. Ví dụ theo quy ước"),
  T(["Quy ước", "Ví dụ (mã mẫu)", "Nhãn"], [
    ["Quan hệ dương rõ ràng", "“tê bì kiến bò ở chân tay” (VM600-514): tê bì kiến bò → chân tay", "located_at"],
    ["Thủ thuật điều trị", "“người bệnh parkinson mà cần phẫu thuốc kích thích não sâu” (VM600-410)", "treated_by_procedure"],
    ["Phương pháp chẩn đoán", "“da nhạy cảm … sử dụng … nghiệm pháp kích thích” (VM600-377)", "diagnosed_by"],
    ["Tác dụng phụ ≠ điều trị", "“biến chứng của việc sử dụng chống viêm corticoid … chảy máu dạ dày” (VM600-132)", "NO_RELATION"],
    ["Phòng ngừa ≠ điều trị", "“tiêm vắcxin chống covid” (VM600-561)", "NO_RELATION"],
    ["Cụm CONDITION đã chứa bộ phận", "“thiếu máu cơ tim” → “tim” (VM600-509)", "NO_RELATION"],
    ["Không truyền sang lần nhắc khác", "Lần nhắc thứ hai “khô ngứa bong tróc đó” → “da” (VM600-199 R4)", "NO_RELATION"],
    ["Câu hỏi tính như khẳng định", "“có tê bì nhiều ở cái bàn tay không ạ” (VM600-464)", "located_at"],
    ["Phủ định", "“triệu chứng … không cải thiện với các thuốc” (VM600-557)", "NO_RELATION (cặp bị xóa do “thuốc” chung)"],
    ["Thực thể chung chung", "“điều trị”, “thuốc”, “khám”, “đánh giá”", "Xóa thực thể và cặp"],
    ["Ngoài phạm vi", "Viên nang đông trùng hạ thảo (VM600-586); lỗi phiên âm “mặc đổ dầu” (VM600-375)", "Xóa cặp"],
  ], [2600, 5038, 2000], { size: 20 }),
  CAP("Bảng D.1. Ví dụ áp dụng quy ước."),
  H2("D.3. Định dạng dữ liệu"),
  P("Mỗi dòng JSONL là một đoạn với các trường: id, source_split, source_row_index, text, words, labels (BIO sáu loại), source_labels (BIO gốc), entities (id, label, text, start, end, token_start, token_end), relations (id, head, tail, label, allowed_relation, evidence, rationale), human_verified, training_eligible, reviewer, reviewed_at, ai_review_flags, gold_v1_changes. Vị trí là chỉ số ký tự Python Unicode, end không bao gồm."),
);

// ===== PHỤ LỤC E, F: danh sách cặp =====
add(
  H1("PHỤ LỤC E. DANH SÁCH CẶP QUAN HỆ DƯƠNG TRONG GOLD V1"),
  T(["#", "Mẫu", "Quan hệ", "Head → Tail", "Văn bản"], X.positives.map((p, i) => [i + 1, p.id, p.rel, `${p.head} → ${p.tail}`, p.text]), [500, 1300, 1900, 2300, 3638], { size: 18 }),
  CAP(`Bảng E.1. ${X.positives.length} cặp dương của gold v1.`),
  H1("PHỤ LỤC F. CÁC CẶP CÒN CHUA_RO VÀ CÁC QUYẾT ĐỊNH DUYỆT"),
  T(["#", "Mẫu", "Kiểu cặp", "Head → Tail", "Văn bản"], X.chua_ro.map((p, i) => [i + 1, p.id, p.rel, `${p.head} → ${p.tail}`, p.text]), [500, 1300, 1900, 2300, 3638], { size: 18 }),
  CAP(`Bảng F.1. ${X.chua_ro.length} cặp còn CHUA_RO (bị loại khỏi huấn luyện và đánh giá).`),
  T(["Nhóm", "Mẫu / cặp", "Head → Tail", "Nhãn cũ", "Quyết định"], X.decisions.map((d) => [d.nhom, `${d.sample_id} ${d.relation_id}`, `${d.head} → ${d.tail}`, d.nhan_hien_tai, d.quyet_dinh_bac_si === "GENERIC_RULE" ? "Xóa (thực thể chung)" : d.quyet_dinh_bac_si === "DELETE" ? "Xóa cặp" : d.quyet_dinh_bac_si]), [2000, 1700, 2900, 1500, 1538], { size: 18 }),
  CAP("Bảng F.2. 40 quyết định duyệt đã áp (nguồn: data/re_gold_v1/decisions_applied.csv)."),
);

// ===== PHỤ LỤC G: ICD =====
add(
  H1("PHỤ LỤC G. BẢNG MÃ ICD-10 TRÊN GOLD V1"),
  T(["Cụm CONDITION", "Số lần", "Mã", "Tên chuẩn", "Cách khớp", "Đánh giá", "Trước sửa"], icd.items.map((o) => [o.text, o.mentions, o.code, o.label, `${o.method} (${f(o.score, 2)})`, o.verdict, o.before && o.before !== o.code ? o.before : (o.before ? "=" : "(không có)")]), [1800, 700, 900, 2600, 1300, 1100, 1238], { size: 18 }),
  CAP(`Bảng G.1. ${icd.items.length} cụm CONDITION có mã sau bản sửa (nguồn: icd10_check.json).`),
);

// ===== PHỤ LỤC H: RE predictions =====
add(
  H1("PHỤ LỤC H. DỰ ĐOÁN RE TỪNG CẶP TRÊN DEV/TEST SEED 42"),
  T(["Tập", "Mẫu", "Head → Tail", "Gold", "Dự đoán", "Điểm"], X.re_preds.map((p) => [p.split, p.id, `${p.head} → ${p.tail}`, p.gold, p.pred === null ? "unsupported" : p.pred, p.score === null ? "—" : f(p.score, 3)]), [800, 1300, 3300, 1700, 1700, 838], { size: 18, right: [5] }),
  CAP(`Bảng H.1. ${X.re_preds.length} cặp dev/test với mô hình TF-IDF + LogReg huấn luyện trên gold v1.`),
);

// ===== PHỤ LỤC I: JSON =====
add(
  H1("PHỤ LỤC I. VÍ DỤ ĐẦU RA JSON ĐẦY ĐỦ"),
  ...CODE(["{", `  "text": ${JSON.stringify(demo.text)},`, "  \"entities\": [", ...demo.entities.map((e, i, a) => "    " + JSON.stringify({ id: e.id, surface_text: e.surface_text, label: e.label, start_char: e.start_char, end_char: e.end_char, confidence: e.confidence, ...(e.re_excluded ? { re_excluded: e.re_excluded } : {}) }) + (i < a.length - 1 ? "," : "")), "  ],", "  \"relations\": [", ...demo.relations.map((x, i, a) => "    " + JSON.stringify({ head: x.head, tail: x.tail, label: x.label, score: Number(x.score.toFixed(4)), status: x.status }) + (i < a.length - 1 ? "," : "")), "  ],", `  "re_metadata": ${JSON.stringify(demo.re_metadata)}`, "}"]),
  CAP("Ví dụ I.1. Đầu ra NER → RE (rút gọn trường trùng lặp)."),
);

// ===== PHỤ LỤC J: tests =====
add(
  H1("PHỤ LỤC J. DANH SÁCH CA KIỂM THỬ"),
  T(["#", "Tệp", "Ca kiểm thử"], X.tests.map((t, i) => { const [file, ...rest] = t.split("::"); return [i + 1, file.replace("tests/", ""), rest.join("::")]; }), [600, 3000, 6038], { size: 18 }),
  CAP(`Bảng J.1. ${nTests} ca kiểm thử pytest (thu thập bằng pytest --collect-only).`),
);

// ===== PHỤ LỤC K: FAQ =====
const QA = (q, a) => [PN(`**Hỏi: ${q}**`, { p: { spacing: { before: 160, after: 60 }, keepNext: true } }), P(`Đáp: ${a}`)];
add(
  H1("PHỤ LỤC K. CÂU HỎI THƯỜNG GẶP"),
  P("Phụ lục này dự đoán các câu hỏi mà người đọc hoặc hội đồng có thể đặt ra, và trả lời dựa trên số liệu trong báo cáo."),
  ...QA("Khóa luận có tự huấn luyện mô hình NER không?", "Không. Checkpoint NER là thành phần kế thừa, được tinh chỉnh từ ViHealthBERT trên VietMed-NER trước khi khóa luận bắt đầu phần đánh giá. Khóa luận xây lại suy luận, luật bổ sung, đánh giá và ablation, và công bố rõ cấu hình huấn luyện đọc được (Bảng 4.3) cùng những thông tin chưa ghi nhận."),
  ...QA("Có tinh chỉnh ViHealthBERT cho RE không?", `Có, sau khi bổ sung RE v2. Với riêng gold v1 (${posAfter} cặp dương) thì encoder lớn khó học và không đánh giá được tin cậy, nên giai đoạn đầu dùng mô hình tuyến tính. Khi có ${bench.cv5.rules.positive_micro.support} cặp dương, ViHealthBERT có đánh dấu thực thể đạt F1 ${rp(bp("cv5", "bert").f1)} trong CV, cao nhất trong các phương pháp đơn lẻ, và hợp với luật đạt ${rp(bp("random_test", "bert+rules").f1)} trên tập test ngẫu nhiên. Siêu tham số được cố định trước, ${bench.bert_meta.seeds.length} seed, không chỉnh trên test.`),
  ...QA("Baseline là gì và vì sao cần nhiều baseline đến vậy?", `Baseline là phương pháp đơn giản dùng làm mốc. Khóa luận dùng baseline ở mọi bước: từ điển và CRF cho NER (Bảng 5.8), khớp chính xác và fuzzy top-1 cho chuẩn hóa (Bảng 5.13–5.14), và bốn baseline không học cho RE (Bảng 5.21). Baseline tầm thường như “mọi cặp đều dương” đặc biệt quan trọng: nó cho thấy golden test bị làm giàu cặp dương (F1 ${rp(bp("golden_test_v1_original", "cooccur").f1)}), điều mà nếu chỉ so mô hình với luật sẽ không phát hiện ra.`),
  ...QA("Có tách train, validation và test không?", `Có, cho từng bước (Bảng 3.16). NER báo cáo trên split test chính thức. Chuẩn hóa chọn mọi cải tiến trên split validation (dev) và chạy test một lần. RE học trên dữ liệu lấy từ split train, chọn phương pháp bằng cross-validation theo nhóm văn bản, và báo cáo trên golden test lấy từ split test.`),
  ...QA("Kết quả RE có nghĩa là mô hình học máy tốt hơn luật không?", `Phụ thuộc vào mô hình. TF-IDF + LogReg ngang luật trong CV nhưng thua rõ trên tập test ngẫu nhiên (${rp(bp("random_test", "tfidf_lr").f1)} so với ${rp(bp("random_test", "rules").f1)}). ViHealthBERT tốt nhất trong CV (${rp(bp("cv5", "bert").f1)}) và hợp với luật đạt ${rp(bp("random_test", "bert+rules").f1)} trên test ngẫu nhiên, nhưng khoảng tin cậy vẫn chồng lấn với luật. Kết luận đúng là học sâu cộng luật là cách tốt nhất hiện có, chưa có ý nghĩa thống kê.`),
  ...QA("Nhãn do AI gán, vậy có đáng tin không?", "Phải tách hai trường hợp. Gold v1 do AI đề xuất nhưng người duyệt đã chốt quy ước và đồng ý với bản rà soát cùng 40 đề xuất sửa. Ba bộ thêm ngày 07/11 (gold chuẩn hóa, RE v2, nhãn golden test) là nhãn AI chưa có người duyệt: được kiểm tra hai lượt và mang cờ human_verified = false, nhưng số đo trên chúng là tạm thời. Rủi ro lớn nhất là RE v2 và golden test do cùng một người gán (mục 6.7). Phiếu duyệt Excel và lệnh chạy lại đã sẵn sàng."),
  ...QA("Có rò rỉ dữ liệu giữa huấn luyện và đánh giá không?", "Có một số nguồn rò rỉ đã biết, và chúng được liệt kê ở mục 6.6 thay vì bị bỏ qua. Đánh giá NER dùng split test chính thức nhưng chưa xác minh được tập dùng để chọn checkpoint. Bộ RE lấy từ split train và đã kiểm tra không trùng câu với split test. Golden test lấy từ split test và đã loại các đoạn trùng nội dung với train. Từ điển chuẩn hóa chỉ lấy dạng có trong train/dev, nhưng một phần dạng đó cũng xuất hiện trong test."),
  ...QA("Vì sao Accuracy chuẩn hóa ICD-10 chỉ khoảng 0,35?", `Vì chế độ mặc định chỉ trả lời khi chắc chắn: nó trả lời ${pct(nc("ICD-10").system.coverage)} dạng có mã và đúng ${pct(nc("ICD-10").system.precision_answered)} trong số đó. Phần còn lại là cách nói dân gian không có tên tương ứng trong danh mục (“có thai”, “rong kinh”). Chế độ luôn trả lời đạt ${rp(nc("ICD-10").always.accuracy)}, và mã đúng nằm trong 10 ứng viên ở ${pct(nc("ICD-10").top10_acc)} trường hợp. Baseline khớp chính xác chỉ đạt ${rp(nc("ICD-10").exact.accuracy)}.`),
  ...QA("Top-k Accuracy và Recall@k khác nhau thế nào?", "Top-k Accuracy là tỉ lệ đề cập có mã đúng trong k ứng viên đầu. Recall@k là tỉ lệ mã gold được tìm thấy trong k ứng viên đầu. Khi mỗi đề cập có đúng một khái niệm gold, như trong tập gold của khóa luận, hai chỉ số bằng nhau; báo cáo ghi cả hai tên để khớp đề cương."),
  ...QA("Kết quả “0 mã sai” sau bản sửa có đáng tin không?", "Chỉ một phần, vì các ràng buộc và alias được thiết kế sau khi thấy lỗi trên chính bộ dữ liệu đó. Tập gold chuẩn hóa test (5.3.3) là phép đo độc lập hơn: ở đó chế độ thận trọng có precision 1,000 với ICD-10, tức không có mã sai, nhưng nhãn gold là nhãn AI chưa duyệt."),
  ...QA("Knowledge graph dùng để làm gì?", `Để xem toàn bộ dữ liệu dưới dạng các khái niệm và quan hệ: bệnh nào thường đi với bộ phận nào, thuốc nào được nhắc cho bệnh nào, kèm câu nguồn để kiểm tra. Đồ thị trên split test có ${n(kgS.nodes)} nút và ${kgS.edges} cạnh. Đây là đầu ra của hệ thống nên còn cạnh sai; nó dùng để khám phá dữ liệu, chưa dùng để trả lời câu hỏi y khoa.`),
  ...QA("Hệ thống có dùng được trong bệnh viện không?", "Chưa, nếu là ra quyết định tự động. Hệ thống phù hợp làm công cụ gợi ý có người xác nhận, và danh sách top-k mã cùng câu nguồn trên đồ thị được thiết kế cho kịch bản đó. Lý do: chưa đánh giá trên bệnh án thật, F1 NER khoảng 0,62 theo strict match, RE mới bắt đầu học quan hệ thuốc–bệnh và chưa học được thuốc–liều."),
  ...QA("Đóng góp của khóa luận nằm ở đâu nếu điểm số không cao?", "Ở bốn điểm: một pipeline tái lập được từ văn bản tới đồ thị tri thức; các bộ dữ liệu quan hệ và chuẩn hóa tiếng Việt có quy ước và nguồn nhãn minh bạch; một bộ đánh giá đủ chỉ số theo đề cương (P/R/F1, Accuracy, Top-k, Recall@k, CI95, baseline); và một phân tích trung thực cho thấy quy ước nhãn, chứ không phải lựa chọn mô hình, quyết định kết luận trên dữ liệu thưa."),
  ...QA("Nếu có thêm một tháng thì làm gì trước?", "Để bác sĩ duyệt golden test (có kết quả đã xác nhận và kappa) và tập gold chuẩn hóa test; sau đó duyệt RE v2 và huấn luyện lại; cuối cùng tìm nguồn văn bản có đơn thuốc thật cho has_dosage. Thứ tự này ưu tiên độ tin cậy của phép đo trước khi cải thiện mô hình."),
);

function ablText(short) {
  const m = (k) => abl[k].strict_exact_match["micro avg"]["f1-score"];
  const full = s["micro avg"]["f1-score"];
  const d = (k) => full - m(k);
  const sg = (x) => (x >= 0 ? "+" : "") + f(x);
  const dosD = s.DOSAGE["f1-score"] - abl.no_dosage.strict_exact_match.DOSAGE["f1-score"];
  const txt = `So với chỉ dùng mô hình (strict micro-F1 ${f(m("model_only"))}), pipeline đầy đủ thay đổi ${sg(d("model_only"))}; riêng luật liều đóng góp ${sg(d("no_dosage"))} (DOSAGE strict F1 thay đổi ${sg(dosD)}) và nhóm Luật 1/1b/2 đóng góp ${sg(d("no_rules"))}.`;
  const fd = s.DOSAGE, nd = abl.no_dosage.strict_exact_match.DOSAGE;
  const detail = ` Trên tập test, luật liều chỉ thêm ${fd.tp - nd.tp} TP và ${fd.fp - nd.fp} FP cho DOSAGE (${nd.tp} → ${fd.tp} TP, ${nd.fp} → ${fd.fp} FP): văn bản nói hầu như không chứa cụm liều dạng “500mg 2 viên/ngày” mà luật được thiết kế để bắt, còn phần lớn DOSAGE gold là đơn vị đo nói chung. Nhóm Luật 1/1b/2 có tác động ngược chiều theo loại: DRUG strict F1 tăng ${sg(s.DRUG["f1-score"] - abl.no_rules.strict_exact_match.DRUG["f1-score"])} (Luật 1 bỏ từ hành động bị gán DRUG), nhưng DOSAGE giảm ${f(abl.no_rules.strict_exact_match.DOSAGE["f1-score"] - s.DOSAGE["f1-score"])} và CONDITION giảm ${f(abl.no_rules.strict_exact_match.CONDITION["f1-score"] - s.CONDITION["f1-score"])}, vì Luật 2 gộp các từ như “cao”, “nặng” vào CONDITION trong khi gold VietMed-NER gán chúng là UNITCALIBRATOR. Đây là ví dụ rõ về một luật đúng với định nghĩa của đề tài nhưng bị phạt bởi quy ước của dữ liệu nguồn. Như vậy luật liều có giá trị cho văn bản đơn thuốc nhưng gần như không ảnh hưởng điểm trên VietMed-NER, và các luật hậu xử lý chỉ cải thiện rất nhỏ. Không có kiểm định thống kê cho các chênh lệch này.`;
  return short ? txt : txt + detail;
}

// ---------- tài liệu ----------
const heading = (size, before, after) => ({ run: { font: FONT, size, bold: true, color: "000000" }, paragraph: { spacing: { before, after }, keepNext: true, keepLines: true } });
const doc = new Document({
  creator: "", title: "Báo cáo khóa luận", features: { updateFields: true },
  styles: {
    default: { document: { run: { font: FONT, size: BODY } } },
    paragraphStyles: [
      { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true, ...heading(32, 240, 240), paragraph: { spacing: { before: 240, after: 240 }, keepNext: true, alignment: AlignmentType.CENTER, outlineLevel: 0 } },
      { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true, ...heading(28, 240, 120), paragraph: { spacing: { before: 240, after: 120 }, keepNext: true, outlineLevel: 1 } },
      { id: "TOC1", name: "toc 1", basedOn: "Normal", next: "Normal", run: { font: FONT, size: 26, bold: true }, paragraph: { spacing: { before: 120, after: 40 } } },
      { id: "TOC2", name: "toc 2", basedOn: "Normal", next: "Normal", run: { font: FONT, size: 26 }, paragraph: { spacing: { before: 0, after: 20 }, indent: { left: 360 } } },
      { id: "TOC3", name: "toc 3", basedOn: "Normal", next: "Normal", run: { font: FONT, size: 24, italics: true }, paragraph: { spacing: { before: 0, after: 0 }, indent: { left: 720 } } },
      { id: "Heading3", name: "Heading 3", basedOn: "Normal", next: "Normal", quickFormat: true, run: { font: FONT, size: 26, bold: true, italics: true }, paragraph: { spacing: { before: 180, after: 100 }, keepNext: true, outlineLevel: 2 } },
    ],
  },
  numbering: {
    config: [
      { reference: "bullets", levels: [{ level: 0, format: LevelFormat.BULLET, text: "•", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 720, hanging: 360 } } } }, { level: 1, format: LevelFormat.BULLET, text: "–", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 1440, hanging: 360 } } } }] },
      ...REFS.map((ref, i) => ({ reference: ref, levels: [{ level: 0, format: LevelFormat.DECIMAL, text: ref === "refs" ? "[%1]" : "%1.", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 720, hanging: 500 } } } }] })),
    ],
  },
  sections: [{
    properties: { page: { size: { width: 11906, height: 16838 }, margin: { top: 1134, bottom: 1134, left: 1701, right: 1134 } } },
    footers: { default: new Footer({ children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ children: [PageNumber.CURRENT], font: FONT, size: 22 })] })] }) },
    children: C,
  }],
});

// thay chỗ kết quả pytest nếu có
Packer.toBuffer(doc).then((buf) => { fs.writeFileSync(OUT, buf); console.log("written", OUT, buf.length); });

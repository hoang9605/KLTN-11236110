// Sinh báo cáo khóa luận (Word). Mọi số liệu đọc trực tiếp từ tệp kết quả trong repo.
const fs = require("fs");
const path = require("path");
const {
  Document, Packer, Paragraph, TextRun, HeadingLevel, AlignmentType, Table, TableRow, TableCell,
  WidthType, ShadingType, BorderStyle, LevelFormat, TableOfContents, Footer, PageNumber, PageBreak,
  ImageRun, HighlightColor, NumberFormat, TabStopType, Bookmark, InternalHyperlink, TableLayoutType, Math: OMath, MathRun, MathFraction, MathRadical, MathSubScript, MathSuperScript, MathRoundBrackets, PageReference, LeaderType,
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
const demo = J("outputs/re_demo_2026-11-22.json"); // pipeline NER → RE với Model/vihealthbert-re-vietmed-validated
const X = J("outputs/bao_cao_khoa_luan_2026-11-05/extra.json");
const icdBefore = J("outputs/bao_cao_khoa_luan_2026-11-05/icd10_check_before_fix.json");
const ABL_DIR = "eval/ablation_2026-11-06";
const abl = exists(`${ABL_DIR}/summary.json`) ? J(`${ABL_DIR}/summary.json`) : null;
const modelCfg = J("Model/vihealthbert-ner-vietmed-v2-final/config.json");
// Bổ sung 07/11/2026: tập gold chuẩn hóa, RE v2, knowledge graph (đều là nhãn LLM, chưa bác sĩ duyệt)
const NORM_DIR = "eval/normalization_2026-11-07";
const normA = { dev: J(`${NORM_DIR}/dev_after/report.json`), test: J(`${NORM_DIR}/test_after/report.json`) };
const normB = { dev: J(`${NORM_DIR}/dev_before/report.json`), test: J(`${NORM_DIR}/test_before/report.json`) };
const normMan = J("data/norm_gold_v1/manifest.json");
const re2 = J("outputs/re_ai_v2/report.json");
const KG_DIR = "outputs/kg_test_2026-11-22"; // ViHealthBERT-RE, dữ liệu sinh đã kiểm tra (Model/vihealthbert-re-vietmed-validated), đứng một mình, cùng thực thể NER với bản 07/11
const kg = J(`${KG_DIR}/kg.json`);
const kgS = kg.stats;
const KG_OLD_DIR = "outputs/kg_test_2026-11-08"; // mô hình RE cũ (ViHealthBERT 3 seed) ∪ luật, giữ để so sánh
const kgOld = J(`${KG_OLD_DIR}/kg.json`);
const kgOldS = kgOld.stats;
const kgPrev = J("outputs/kg_test_2026-11-21/kg.json"); // mô hình RE dữ liệu sinh chưa kiểm tra (Model/vihealthbert-re-vietmed)
const kgPrevShared = (() => { const a = new Set(kgPrev.edges.map((e) => `${e.head}|${e.relation}|${e.tail}`)); return kg.edges.filter((e) => a.has(`${e.head}|${e.relation}|${e.tail}`)).length; })();
const kgNames = (g) => Object.fromEntries(g.nodes.map((x) => [x.key, x.name]));
const kgShared = (() => { const a = new Set(kgOld.edges.map((e) => `${e.head}|${e.relation}|${e.tail}`)); return kg.edges.filter((e) => a.has(`${e.head}|${e.relation}|${e.tail}`)).length; })();
const kgToBone = (g) => { const nm = kgNames(g); return g.edges.filter((e) => e.relation === "located_at" && nm[e.tail] === "xương").length; };
const kgEdgeCount = (g, h, rel, t) => { const nm = kgNames(g); const e = g.edges.find((x) => nm[x.head] === h && x.relation === rel && nm[x.tail] === t); return e ? e.count : 0; };
const normPred = fs.readFileSync(path.join(ROOT, `${NORM_DIR}/test_after/predictions.jsonl`), "utf8").split(/\r?\n/).filter((l) => l.trim()).map((l) => JSON.parse(l));
const icdMiss = normPred.filter((r) => r.ontology === "ICD-10" && !r.nil && r.pred.system === null);
const icdMissTop = icdMiss.filter((r) => r.candidates.some((c) => r.gold_codes.includes(c))).length;
const nc = (onto, split = "test", which = normA, level = "code") => which[split].results[onto][level].type;
const ncm = (onto, split = "test", which = normA) => which[split].results[onto].code.mention;
const nci = (onto, key, split = "test", which = normA, level = "code") => which[split].results[onto][level].ci95_type[key];
const ci = (a) => `${rp(a[0])}–${rp(a[1])}`;
const RM = { rules: "Luật (baseline)", model_v1: "Mô hình v1 (chỉ gold v1)", model_v2: "Mô hình v2 (gold v1 + LLM v2)", hybrid: "Mô hình v2, luật cho quan hệ chưa học", union: "Mô hình v2 ∪ luật (chọn theo CV)" };
const re2pm = (part, m) => re2[part][m].positive_micro;
const re2u = re2pm("golden_test", "union"), re2v1 = re2pm("golden_test", "model_v1"), re2cvu = re2pm("cv5", "union");
const re2lab = re2.data.labels_v2;
const re2pos = Object.entries(re2lab).filter(([k]) => k !== "NO_RELATION").reduce((a, [, v]) => a + v, 0);
const gtLab = re2.data.labels_golden_test;
const gtPos = Object.entries(gtLab).filter(([k]) => k !== "NO_RELATION").reduce((a, [, v]) => a + v, 0);
const kgRel = (k) => kg.edges.filter((e) => e.relation === k);
const kgOcc2 = (g, k) => g.edges.filter((e) => e.relation === k).reduce((a, e) => a + e.count, 0);
const kgName = Object.fromEntries(kg.nodes.map((x) => [x.key, x.name]));
// Bổ sung 08/11/2026: baseline RE/NER, tập test ngẫu nhiên, golden test v1.1, đồng thuận nhãn
const agree = J("outputs/re_ai_v2/agreement.json");
const rtMan = J("data/re_test_random_v1/manifest.json");
const gtChanges = fs.readFileSync(path.join(ROOT, "data/golden_test/v1/ai_labels_v1_1_changes.csv"), "utf8").replace(/^﻿/, "")
  .split(/\r?\n/).slice(1).filter((l) => l.trim()).map((l) => { const m = l.match(/^([^,]*),([^,]*),([^,]*),([^,]*),(.*)$/); return { id: m[1], rel: m[2], before: m[3], after: m[4], reason: m[5].replace(/^"|"$/g, "").replace(/""/g, "\"") }; });
const BENCH_DIR = "outputs/re_benchmark_2026-11-08";
const bench = J(`${BENCH_DIR}/benchmark.json`);
const dep = J(`${BENCH_DIR}/deployed.json`); // mô hình đã lưu, nạp lại trên CPU (scripts/re_dataset/eval_deployed.py)
const depSets = Object.values(dep.sets);
const depPairs = depSets.reduce((a, s) => a + s.pairs, 0);
const depDiff = depSets.reduce((a, s) => a + s.cpu_vs_gpu_label_differences, 0);
const depMs = depSets.reduce((a, s) => a + s.ms_per_pair * s.pairs, 0) / depPairs;
const depSeedRT = Object.values(dep.sets.random_test.single_seed_f1).map((v) => v.with_rules);
const depSeedFirst = dep.sets.random_test.single_seed_f1[String(dep.config.seeds[0])].with_rules;
// Thí nghiệm thêm dữ liệu tiếng Anh dịch (scripts/re_dataset/translated_en.py, eval_augmented.py)
const trMan = J("data/re_translated_en_v1/manifest.json");
const aug = J(`${BENCH_DIR}/augmented.json`);
const AUGT = Object.keys(aug.variants); // ["biotext", "biotext_ade"]
const augName = { biotext: "+ BioText", biotext_ade: "+ BioText + ADE" };
const augPos = (tag) => Object.entries(aug.variants[tag].extra_by_label).filter(([k]) => !k.endsWith("NO_RELATION")).reduce((a, [, v]) => a + v, 0);
const augRate = (tag) => (dep.config.train_positives + augPos(tag)) / (dep.config.train_pairs + aug.variants[tag].extra_pairs);
const as = (set, m) => aug.sets[set].scores[m].positive_micro;
const aci = (set, m) => ci(aug.sets[set].scores[m].positive_micro_f1_ci95);
const adf = (set, tag) => { const d = as(set, `${tag}+rules`).f1 - as(set, "baseline+rules").f1; const c = aug.sets[set].paired_diff_ci95[tag].with_rules; const sg = (x) => `${x >= 0 ? "+" : "−"}${rp(Math.abs(x))}`; return `${sg(d)} (KTC ${sg(c[0])} đến ${sg(c[1])})`; };
const adg = (set, tag) => aug.sets[set].diagnostics[tag];
const trSkip = trMan.skipped.length;
const trCount = (k) => trMan.pairs[k] || 0;
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
const CONTENT_W = 11906 - 1985 - 1418; // A4, lề trên/dưới 2,5 cm, trái 3,5 cm, phải 2,5 cm theo quy định viết báo cáo của Khoa
const pyRes = JSON.parse(fs.readFileSync(path.join(__dirname, "pytest_result.json"), "utf8"));
// ===== Dữ liệu và kết quả RE làm lại (thư mục relation/, 19-21/11/2026); nhãn RE cũ không còn được dùng =====
const JL = (p) => fs.readFileSync(path.join(ROOT, p), "utf8").split(/\r?\n/).filter((l) => l.trim()).map((l) => JSON.parse(l));
const RX = {
  sel: J("relation/data/selection.json"),
  syn: J("relation/data/synth/manifest.json"),
  agSeed: J("relation/data/ai_agreement_seed.json"),
  agTest1: J("relation/data/ai_agreement_test.json"),
  agTest2: J("relation/data/ai_agreement_test_v2.json"),
  rev: J("relation/data/seed_review_summary.json"),
  ev: J("relation/outputs/evaluation.json"),
  ev2: J("relation/outputs/evaluation_test_v2_rules.json"),
  fn: J("relation/outputs/review_fn_summary.json"),
  test: JL("relation/data/test_v2.jsonl"),
  // kiểm tra dữ liệu sinh (relation/validate/, 21-22/11/2026)
  val: J("relation/data/synth/validate/summary.json"),
  vman: J("relation/data/synth/validated/manifest.json"),
  abl: J("relation/outputs/evaluation_validated_ablation.json"),
};
const RX_REL = ["located_at", "treated_by", "treated_by_procedure", "diagnosed_by", "has_dosage"];
const rxMentions = RX.test.reduce((a, r) => a + r.entities.length, 0);
const rxInvalid = RX.test.reduce((a, r) => a + r.entities.filter((e) => e.validity === "INVALID").length, 0);
const rxPairs = RX.ev2.pairs, rxPos = RX.ev2.positives;
const rxPosV1 = (rel) => RX.test.reduce((a, r) => a + r.relations.filter((x) => x.allowed_relation === rel && x.label_v1 !== "NO_RELATION").length, 0);
const rxPosV1All = RX_REL.reduce((a, k) => a + rxPosV1(k), 0);
const rxM = (k) => RX.ev2[k].micro; // model, rules, model+rules, always_positive
const rxR = (k, rel) => RX.ev2[k].per_relation[rel];
const rxCI = (k) => RX.ev2.ci95_micro_f1[k];
const rxDev = RX.ev.dev;
const rxSel = rxDev[RX.ev.chosen]; // cấu hình chọn trên tập kiểm định (vall)
const RX_CFG = [["x0", "chỉ dữ liệu thật"], ["x1", "sinh chưa kiểm tra, một lần"], ["x3", "sinh chưa kiểm tra, ba lần"], ["v1", "sinh đã kiểm tra, một lần"], ["vall", "toàn bộ dữ liệu sinh đã kiểm tra"]];
const rxVP = RX.vman.verdict_precision;
const rxAblT = (c) => RX.abl.results.test_v2[c];
const rxPct = (x) => `${f(x * 100, 1)}%`;
// soát lại tiêu chí trên mẫu 50 cặp (relation/review_fn.py): số cặp được người gán kết luận và số cặp còn là dương
const rxAudit = { sample: 50, judged: RX.fn.fn.judged + RX.fn.control_tp.judged, stillPositive: RX.fn.fn.positive + RX.fn.control_tp.positive, control: RX.fn.control_tp.judged };
// số liệu của bộ dữ liệu quan hệ cũ, đo khi rà soát trước khi làm lại (docs/KE_HOACH_LAM_LAI_RE.md)
const RX_OLD = { pairs: 556, pos: 64, wrongTypeNeg: 43 };
const border = { style: BorderStyle.SINGLE, size: 4, color: "000000" };
const borders = { top: border, bottom: border, left: border, right: border };

// ---- đổi tên "gold" khi hiển thị: tên bộ dữ liệu và nghĩa chung "nhãn đúng" ----
// Chỉ đổi chữ hiển thị; tên tệp và biến trong mã (re_gold_v1, gold.jsonl, gold_codes) giữ nguyên.
const GOLD_MAP = [
  [/(?<![\w./])([Gg])olden test v1\.1/g, "tập test hạn mức sau rà soát"],
  [/(?<![\w./])([Gg])olden test/g, "tập test hạn mức"],
  [/(?<![\w./])([Gg])old v1/g, "bộ 600 đoạn khảo sát"],
  [/(?<![\w./])([Gg])old chuẩn hóa/g, "tập đánh giá chuẩn hóa"],
  [/(?<![\w./])(n)hãn gold(?![\w/]|\.\w)/g, "nhãn chuẩn"],
  [/(?<![\w./])(t)hực thể gold(?![\w/]|\.\w)/g, "thực thể chuẩn"],
  [/(?<![\w./])(m)ã gold(?![\w/]|\.\w)/g, "mã đúng"],
  [/(?<![\w./])(s)pan gold(?![\w/]|\.\w)/g, "span chuẩn"],
  [/(?<![\w./])(k)hái niệm gold(?![\w/]|\.\w)/g, "khái niệm chuẩn"],
  [/(?<![\w./])(c)ạnh gold(?![\w/]|\.\w)/g, "cạnh chuẩn"],
  [/(?<![\w./])(g)old(?![\w/(-]|\.\w)/g, "nhãn chuẩn"],
];
// ---- thuật ngữ Anh sang Việt khi hiển thị (góp ý 15/11): chỉ giữ tiếng Anh cho từ không thay được
// (NER, RE, BERT, embedding, vector, token, span, F1, train/dev/test...) và các từ người viết chọn giữ:
// baseline, precision, recall, rule-based, fuzzy matching, confusion matrix.
// Không đổi trong `mã`, đường dẫn, định danh có dấu gạch dưới, và trong ngoặc ngay sau thuật ngữ Việt.
const VB = "(?<![\\w./_(\\-])", VA = "(?![\\w/_\\-]|\\.\\w)";
const VI_MAP = [
  ["[Pp]ositive micro-F1", "micro-F1 trên lớp dương"],
  ["[Ss]trict F1", "F1 khớp chặt"],
  ["[Ss]trict micro-F1", "micro-F1 khớp chặt"],
  ["[Rr]elaxed micro-F1", "micro-F1 khớp nới lỏng"],
  ["[Ss]plit (train|dev|test|validation)", "tập $1"],
  ["[Ss]plits?", "phần chia"],
  ["[Ee]nd-to-end", "đầu cuối"],
  ["[Pp]ipelines?", "luồng xử lý"],
  ["[Cc]andidates?", "ứng viên"],
  ["[Aa]lias(?:es)?", "tên gọi khác"],
  ["[Cc]lass weights?", "trọng số lớp"],
  ["[Kk]nowledge graphs?", "đồ thị tri thức"],
  ["[Aa]blation", "thử nghiệm lược bỏ"],
  ["[Ee]xact match", "khớp chính xác"],
  ["[Ss]trict match", "khớp chặt"],
  ["[Rr]elaxed match", "khớp nới lỏng"],
  ["[Mm]entions?", "lượt đề cập"],
  ["[Cc]heckpoints?", "mô hình"],
  ["[Ff]ine-tun(?:e|ed|ing)", "tinh chỉnh"],
  ["[Pp]re-train(?:ed|ing)?", "tiền huấn luyện"],
  ["[Cc]ross-validation", "kiểm định chéo"],
  ["[Ee]ncoders?", "bộ mã hóa"],
  ["[Ee]ntity markers?", "ký hiệu đánh dấu thực thể"],
  ["[Tt]yped markers?", "ký hiệu đánh dấu kèm loại"],
  ["[Mm]arkers?", "ký hiệu đánh dấu"],
  ["[Oo]ntology", "hệ khái niệm chuẩn"],
  ["[Oo]ntologies", "hệ khái niệm chuẩn"],
  ["[Tt]op-k [Aa]ccuracy", "độ chính xác Top-k"],
  ["[Aa]ccuracy", "độ chính xác"],
  ["[Ll]earning rate", "tốc độ học"],
  ["[Bb]atch size", "kích thước lô"],
  ["[Bb]atch(?= \\d)", "kích thước lô"],
  ["[Ee]pochs?", "vòng huấn luyện"],
  ["[Ff]olds?", "phần"],
  ["[Cc]hunks?", "đoạn con"],
  ["[Bb]enchmarks?", "bộ đánh giá chuẩn"],
  ["[Hh]ead(?! attention)", "thực thể đầu"],
  ["[Tt]ail", "thực thể đuôi"],
  ["[Cc]overage", "độ bao phủ"],
  ["[Ll]oss", "hàm mất mát"],
  ["[Rr]egularization", "điều chuẩn"],
  ["[Ii]nference", "suy luận"],
  ["[Dd]atasets?", "bộ dữ liệu"],
  ["[Cc]orpus", "kho ngữ liệu"],
  ["[Dd]ictionary", "từ điển"],
  ["[Ss]ynonyms?(?! \\()", "từ đồng nghĩa"],
  ["[Ll]uật", "quy tắc"],
  ["[Ww]eight decay", "suy giảm trọng số"],
  ["[Oo]ptimizer", "bộ tối ưu"],
  ["[Hh]ead attention", "đầu chú ý"],
  ["[Rr]etrieval", "truy hồi"],
].map(([k, v]) => [new RegExp(VB + "(" + k + ")" + VA, "g"), v]);
const viTerms = (t) => String(t).split(/(`[^`]+`|\(⁠[^()]*\))/).map((seg) => /^(`|\(⁠)/.test(seg) ? seg : VI_MAP.reduce((x, [re, rep]) => x.replace(re, (...a) => {
  const m = a[0]; let out = rep.replace("$1", a[2] || "");
  const off = a[a.length - 2], src = a[a.length - 1];
  // chỉ viết hoa khi thuật ngữ đứng đầu câu hoặc đầu ô, tránh "đạt Độ chính xác" giữa câu
  const atStart = typeof off === "number" && /(^|[.!?:]\s+|\n)\s*$/.test(String(src).slice(0, off));
  return atStart && m[0] === m[0].toUpperCase() && m[0] !== m[0].toLowerCase() ? out[0].toUpperCase() + out.slice(1) : out;
}), seg)).join("").replace(/⁠/g, "").replace(/([Hh])àm hàm mất mát/g, "$1àm mất mát").replace(/Accuracy\/Top-k/g, "Độ chính xác và Top-k").replace(/\(Accuracy, /g, "(độ chính xác, ").replace(/thực thể đầu → thực thể đuôi/gi, (m) => m[0] === "T" ? "Thực thể đầu → thực thể đuôi" : m);
const renameGold = (t) => {
  let x = String(t);
  if (/^\s*Gold\s*$/.test(x)) return x; // giữ mục "Gold" trong danh mục từ viết tắt
  // "RE v2" là tên phiên bản nội bộ, trong báo cáo gọi là bộ RE bổ sung; viết hoa khi đứng đầu câu
  x = x.replace(/(^|[.:]\s+|\()?(?:([Bb])ộ )?RE v2(?![\w/])/g, (m, pre, b) => {
    const head = (pre !== undefined && pre !== "(") || (b && b === "B");
    return (pre || "") + (head ? "Bộ" : "bộ") + " RE bổ sung";
  }).replace(/([Mm])ô hình v2/g, "$1ô hình TF-IDF").replace(/bổ sung dữ liệu bộ RE bổ sung/g, "bổ sung dữ liệu quan hệ").replace(/dữ liệu bộ RE bổ sung/g, "bộ RE bổ sung").replace(/bộ RE bổ sung bổ sung/g, "bộ RE bổ sung thêm")
    // nhãn dữ liệu viết tiếng Anh thống nhất với NO_RELATION
    .replace(/\bCHUA_RO\b/g, "UNCLEAR").replace(/\bXOA\b/g, "REMOVED");
  for (const [re, rep] of GOLD_MAP) x = x.replace(re, (m, c) => (c && c === c.toUpperCase() ? rep[0].toUpperCase() + rep.slice(1) : rep));
  x = x.replace(/([Cc]hế độ) strict/g, "$1 chặt").replace(/([Cc]hế độ) always/g, "$1 luôn gán mã").replace(/fp16/g, "số thực 16 bit");
  x = viTerms(x);
  return x.replace(/\b([Tt])ập tập /g, "$1ập ").replace(/\b([Bb])ộ bộ /g, "$1ộ ").replace(/nhãn nhãn chuẩn/g, "nhãn chuẩn").replace(/([Tt])ập đánh giá chuẩn hóa chuẩn hóa/g, "$1ập đánh giá chuẩn hóa");
};
function runs(text, base = {}) {
  const parts = renameGold(text).split(/(\*\*[^*]+\*\*|\[\[[^\]]+\]\]|`[^`]+`)/).filter((s) => s !== "");
  return parts.flatMap((s) => {
    if (s.startsWith("**")) return new TextRun({ text: s.slice(2, -2), bold: true, font: FONT, ...base });
    if (s.startsWith("[[")) return new TextRun({ text: s.slice(2, -2), shading: { fill: "FFFF00", type: ShadingType.CLEAR, color: "auto" }, font: FONT, ...base });
    if (s.startsWith("`")) return new TextRun({ text: s.slice(1, -1), font: "Consolas", size: (base.size || BODY) - 4 });
    return linkRuns(s, { font: FONT, ...base });
  });
}
// ---- liên kết nội bộ: mỗi tham chiếu trong văn bản nhảy tới đúng mục, bảng, hình, công thức, tài liệu ----
const anchorId = (kind, key) => `${kind}_${String(key).replace(/[^0-9A-Za-z]/g, "_")}`;
const KIND = { "Bảng": "tab", "Hình": "fig", "Mã giả": "alg", "Ví dụ": "ex" };
const REF_RE = /((?:[Mm]ục|[Tt]iểu mục) \d+(?:\.\d+)+|Chương \d|Phụ lục [A-J](?:\.\d)?|(?:Bảng|Hình|Mã giả|Ví dụ) [0-9A-J]+\.\d+|công thức (?:\(\d+\.\d+\)(?:, | và )?)+|\[\d{1,2}\])/;
const refAnchor = (m) => {
  let r;
  if ((r = m.match(/^(?:[Mm]ục|[Tt]iểu mục) (\d+(?:\.\d+)+)$/))) return anchorId("sec", r[1]);
  if ((r = m.match(/^Chương (\d)$/))) return anchorId("chap", r[1]);
  if ((r = m.match(/^Phụ lục ([A-J](?:\.\d)?)$/))) return anchorId("app", r[1]);
  if ((r = m.match(/^(Bảng|Hình|Mã giả|Ví dụ) ([0-9A-J]+\.\d+)$/))) return anchorId(KIND[r[1]], r[2]);
  if ((r = m.match(/^\[(\d{1,2})\]$/))) return anchorId("ref", r[1]);
  return null;
};
const LINK_ON = { on: true };
function linkRuns(text, base) {
  if (!LINK_ON.on) return new TextRun({ text, ...base });
  const out = [];
  String(text).split(REF_RE).filter((x) => x !== "").forEach((seg) => {
    if (/^công thức \(/.test(seg)) {
      // "công thức (2.1), (2.2) và (2.3)": mỗi số dẫn tới đúng công thức
      seg.split(/(\(\d+\.\d+\))/).filter((x) => x).forEach((x) => {
        const n = x.match(/^\((\d+\.\d+)\)$/);
        out.push(n ? new InternalHyperlink({ anchor: anchorId("eq", n[1]), children: [new TextRun({ text: x, ...base })] }) : new TextRun({ text: x, ...base }));
      });
      return;
    }
    const a = REF_RE.test(seg) && seg.match(REF_RE)[0] === seg ? refAnchor(seg) : null;
    out.push(a ? new InternalHyperlink({ anchor: a, children: [new TextRun({ text: seg, ...base })] }) : new TextRun({ text: seg, ...base }));
  });
  return out;
}
// đánh dấu đích: tiêu đề, tên bảng/hình, công thức, mục tài liệu
const headAnchor = (t) => {
  let r;
  if ((r = t.match(/^CHƯƠNG (\d)\./))) return anchorId("chap", r[1]);
  if ((r = t.match(/^Phụ lục ([A-J](?:\.\d)?):/))) return anchorId("app", r[1]);
  if ((r = t.match(/^(\d+\.\d+(?:\.\d+)*)\.\s/))) return anchorId("sec", r[1]);
  return null;
};
const headKids = (t0) => { const t = renameGold(t0); const a = headAnchor(t); const run = new TextRun({ text: t, font: FONT }); return [a ? new Bookmark({ id: a, children: [run] }) : run]; };
// ---- lần đầu dùng một từ viết tắt hay thuật ngữ trong thân bài: ghi kèm tên đầy đủ hoặc giải thích ----
const FIRST_USE = [
  ["NER", "Named Entity Recognition"],
  ["RE", "Relation Extraction"],
  ["ICD-10", "International Classification of Diseases, 10th Revision"],
  ["RxCUI", "RxNorm Concept Unique Identifier"],
  ["BIO", "Begin, Inside, Outside"],
  ["CRF", "Conditional Random Fields, trường ngẫu nhiên có điều kiện"],
  ["BiLSTM-CRF", "Bidirectional Long Short-Term Memory – Conditional Random Fields, mạng bộ nhớ dài-ngắn hai chiều kết hợp trường ngẫu nhiên có điều kiện"],
  ["TF-IDF", "Term Frequency, Inverse Document Frequency"],
  ["RoBERTa", "Robustly Optimized BERT Pretraining Approach"],
  ["MRR", "Mean Reciprocal Rank"],
  ["FMA", "Foundational Model of Anatomy"],
  ["LOINC", "Logical Observation Identifiers Names and Codes"],
  ["MeSH", "Medical Subject Headings"],
  ["PURE", "Princeton University Relation Extraction"],
  ["ADE", "Adverse Drug Event"],
  ["n2c2", "National NLP Clinical Challenges"],
  ["micro-F1", "F1 tính gộp trên mọi lớp"],
  ["NIL", "không có mã phù hợp trong danh mục"],
  ["tập test hạn mức", "tập test chọn đoạn theo hạn mức số cặp của từng quan hệ"],
  ["span", "đoạn ký tự liên tiếp trong văn bản"],
  ["subword", "mảnh con của một từ"],
  ["đồ thị tri thức", "knowledge graph"],
  ["khớp chặt", "strict match, khớp đúng cả span lẫn loại"],
  ["khớp nới lỏng", "relaxed match, chấp nhận span giao nhau"],
  ["thử nghiệm lược bỏ", "ablation"],
  ["ký hiệu đánh dấu thực thể", "entity marker"],
  ["lượt đề cập", "mention"],
  ["self-attention", "cơ chế tự chú ý"],
  ["logits", "điểm số trước hàm softmax"],
];
const FIRST_SEEN = new Set();
const FIRST_LOG = [];
const LETTER = "0-9A-Za-zÀ-ỹ_";
const FIRST_RE = FIRST_USE.map(([k, v]) => [k, v, new RegExp(`(?<![${LETTER}-])${k.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")}(?![${LETTER}-])`, "i")]);
// thuật ngữ dài kiểm tra trước để "entity marker" không bị "marker" chiếm chỗ
FIRST_RE.sort((a, b) => b[0].length - a[0].length);
// 19/11/2026: không chèn giải thích trong ngoặc vào thân bài nữa, mọi thuật ngữ được giải thích ở Danh mục các từ viết tắt
// Quy định của Khoa: chữ viết tắt lần đầu xuất hiện phải viết đầy đủ trước, kèm chữ viết tắt trong ngoặc đơn,
// ví dụ "nhận diện thực thể có tên (NER)". Chỉ áp dụng cho chữ viết tắt thật, không chú thích tiếng Anh.
const ABBR_FIRST = [
  ["BiLSTM-CRF", "mạng bộ nhớ dài-ngắn hai chiều kết hợp trường ngẫu nhiên có điều kiện"],
  ["ICD-10", "phân loại bệnh quốc tế phiên bản 10"],
  ["TF-IDF", "trọng số tần suất từ và nghịch đảo tần suất văn bản"],
  ["NER", "nhận diện thực thể có tên"],
  ["RE", "trích xuất quan hệ"],
  ["CRF", "trường ngẫu nhiên có điều kiện"],
  ["BIO", "bắt đầu, bên trong, bên ngoài"],
  ["MRR", "trung bình nghịch đảo thứ hạng"],
  ["LLM", "mô hình ngôn ngữ lớn"],
  ["RxCUI", "mã định danh khái niệm thuốc trong RxNorm"],
  ["ADE", "biến cố bất lợi do thuốc"],
].map(([k, v]) => [k, v, new RegExp(`(?<![0-9A-Za-zÀ-ỹ_-])${k.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")}(?![0-9A-Za-zÀ-ỹ_-])`)]);
const ABBR_SEEN = new Set();
const expandFirst = (t) => {
  let txt = String(t);
  for (const [k, v, re] of ABBR_FIRST) {
    if (ABBR_SEEN.has(k)) continue;
    const m = txt.match(re);
    if (!m) continue;
    ABBR_SEEN.add(k);
    if (/^\s*\(/.test(txt.slice(m.index + k.length))) continue; // đã có ngoặc ngay sau
    const atStart = /(^|[.!?]\s+)$/.test(txt.slice(0, m.index));
    const full = atStart ? v[0].toUpperCase() + v.slice(1) : v;
    txt = txt.slice(0, m.index) + `${full} (${k})` + txt.slice(m.index + k.length);
  }
  return txt;
};
const expandFirstOld = (t) => {
  let txt = String(t);
  for (const [k, v, re] of FIRST_RE) {
    if (FIRST_SEEN.has(k)) continue;
    const m = txt.match(re);
    if (!m) continue;
    FIRST_SEEN.add(k);
    const after = txt.slice(m.index + m[0].length);
    if (/^\s*\(/.test(after)) continue; // đã có giải thích ngay sau
    if (/(gọi là|gọi tắt là|tức là|còn gọi là|đặt tên là)\s*$/.test(txt.slice(0, m.index))) continue; // văn bản đã tự giải thích
    // khi một thuật ngữ dài đã mở rộng, không mở rộng phần con nằm trong nó lần này
    txt = txt.slice(0, m.index + m[0].length) + ` (⁠${v})` + after;
    FIRST_LOG.push(`${k}: …${txt.slice(Math.max(0, m.index - 40), m.index + m[0].length + v.length + 40)}…`);
    if (k.includes(" ")) for (const part of k.split(" ")) FIRST_SEEN.has(part) || null;
  }
  return txt;
};
const plain = (t) => String(t).replace(/\*\*/g, ""); // không in đậm rải rác trong đoạn văn
const P = (t, o = {}) => new Paragraph({ children: runs(o.noExpand ? plain(t) : expandFirst(renameGold(plain(t))), o.run || {}), alignment: o.align || AlignmentType.JUSTIFIED, spacing: { before: 120, after: 0, line: 312 }, indent: o.noIndent ? undefined : { firstLine: 425 }, widowControl: true, ...(o.p || {}) }); // theo kiểu Normal của mẫu: không thụt dòng đầu
const PN = (t, o = {}) => P(t, { ...o, noIndent: true });
const H1 = (t) => new Paragraph({ heading: HeadingLevel.HEADING_1, children: headKids(t), pageBreakBefore: true });
const H2 = (t) => new Paragraph({ heading: HeadingLevel.HEADING_2, children: headKids(t) });
const H3 = (t) => new Paragraph({ heading: HeadingLevel.HEADING_3, children: headKids(t) });
const H4 = (t) => new Paragraph({ heading: HeadingLevel.HEADING_4, children: headKids(t) }); // mục cấp 4, không đưa vào mục lục
const HA = (t, newPage) => new Paragraph({ heading: HeadingLevel.HEADING_2, children: headKids(t), pageBreakBefore: newPage });
const B = (t, lvl = 0) => new Paragraph({ numbering: { reference: "bullets", level: lvl }, widowControl: true, children: runs(expandFirst(renameGold(plain(t)))), alignment: AlignmentType.JUSTIFIED, spacing: { before: 120, after: 0, line: 312 } });
const NUM = (t, ref = "num1") => new Paragraph({ numbering: { reference: ref, level: 0 }, widowControl: true, children: runs(ref === "refs" ? plain(t) : expandFirst(renameGold(plain(t)))), alignment: AlignmentType.JUSTIFIED, spacing: ref === "refs" ? { before: 119, after: 0, line: 240 } : { before: 120, after: 0, line: 312 } });
const CAP = (t0) => {
  const t = String(t0).replace(/^(Bảng|Hình) ([0-9A-Z]+\.\d+)[:.] /, "$1 $2. ").replace(/\.$/, "");
  const kind = /^Bảng [0-9A-Z]+\.\d+\./.test(t) ? "BangCaption" : /^Hình [0-9A-Z]+\.\d+\./.test(t) ? "HinhCaption" : "OtherCaption";
  // theo bản mẫu: tên hình in nghiêng đặt dưới hình, tên bảng chữ thường đặt trên bảng
  const lm = t.match(/^((Bảng|Hình|Ví dụ|Mã giả) ([0-9A-J]+\.\d+)\.)(.*)$/s);
  LINK_ON.on = false;
  const rest = lm ? runs(lm[4], { size: 26 }) : runs(t, { size: 26 });
  LINK_ON.on = true;
  const kids = lm ? [new Bookmark({ id: anchorId(KIND[lm[2]], lm[3]), children: [new TextRun({ text: lm[1], font: FONT, size: 26 })] }), ...rest] : rest;
  const para = new Paragraph({ style: kind, children: kids, alignment: AlignmentType.CENTER, keepNext: true, keepLines: true, spacing: { before: kind === "BangCaption" ? 200 : 80, after: kind === "BangCaption" ? 80 : 120, line: 276 } });
  para.__tableCaption = kind === "BangCaption";
  return para;
};
const NOTE = (t) => P(t); // ghi chú trình bày như đoạn văn thường
// Ghi chú mục đích đặt ngay dưới bảng/hình: in nghiêng, chữ xám, cỡ 11.
// Mã giả theo chuẩn thuật toán: tên ở trên giữa hai đường kẻ, dòng function có kiểu dữ liệu, các dòng đánh số,
// từ khóa in đậm, lề thụt theo cấp và chú thích ▷ in nghiêng; đường kẻ đóng ở dòng cuối.
// Ký hiệu toán trong mã giả và dòng giải thích dùng Cambria Math, vì Times New Roman trên một số máy
// thiếu glyph và Word thay bằng ký tự lạ (ví dụ ∈ hiện thành chữ Ả Rập, ▷ hiện thành ô vuông).
const SYM_RE = /([←∈∉∪∩∅≥≤≠⊕⟨⟩▷√…∖·−⁺⁻])/;
const symRuns = (text, base) => String(text).split(SYM_RE).filter((x) => x).map((x) => SYM_RE.test(x) && x.length === 1 ? new TextRun({ ...base, text: x, font: "Cambria Math" }) : new TextRun({ ...base, text: x }));
const ALGO_KW = /\b(end function|end for|end while|end if|function|for each|for|while|if|then|else|do|to|return|and|or|not|NIL|true|false)\b/g;
const algoRuns = (t) => {
  // mã giả theo chuẩn algorithmicx: từ khóa in đậm, chú thích sau ▷ in nghiêng màu xám
  const cut = t.indexOf(" ▷ ");
  const code = cut < 0 ? t : t.slice(0, cut);
  const note = cut < 0 ? "" : viTerms(t.slice(cut + 3));
  const base = { font: FONT, size: 24 };
  const out = [];
  let last = 0;
  code.replace(ALGO_KW, (m, _k, i) => { if (i > last) out.push(...symRuns(code.slice(last, i), base)); out.push(new TextRun({ ...base, text: m, bold: true })); last = i + m.length; return m; });
  if (last < code.length) out.push(...symRuns(code.slice(last), base));
  if (note) out.push(new TextRun({ ...base, text: "   " }), new TextRun({ ...base, text: "▷", font: "Cambria Math", color: "595959" }), new TextRun({ ...base, text: ` ${note}`, italics: true, color: "595959" }));
  return out;
};
const RULE = { style: BorderStyle.SINGLE, size: 8, color: "000000", space: 2 };
const ALGO = (cap, input, output, lines) => {
  const m = viTerms(cap).match(/^(Mã giả [0-9A-Z]+\.\d+\.)\s*(.*)$/);
  const head = new Paragraph({ style: "OtherCaption", keepNext: true, alignment: AlignmentType.LEFT, border: { top: RULE, bottom: { ...RULE, size: 4 } }, spacing: { before: 200, after: 60, line: 276 },
    children: [new Bookmark({ id: anchorId("alg", m[1].replace(/^Mã giả |\.$/g, "")), children: [new TextRun({ text: m[1], bold: true, font: FONT, size: 26 })] }), new TextRun({ text: ` ${m[2]}`, font: FONT, size: 26 })] });
  const io = (input == null ? [] : [["Input:", input], ["Output:", output]]).map(([k, v]) => new Paragraph({ keepNext: true, spacing: { before: 0, after: 0, line: 276 }, indent: { left: 900, hanging: 900 }, tabStops: [{ type: TabStopType.LEFT, position: 900 }],
    children: [new TextRun({ text: k, bold: true, font: FONT, size: 24 }), new TextRun({ text: "\t", font: FONT }), ...algoRuns(viTerms(v))] }));
  const body = lines.map((l, i) => {
    const lvl = (l.match(/^ */)[0].length) / 2;
    const pos = 500 + lvl * 400;
    return new Paragraph({ keepNext: i < lines.length - 1 && (lines.length <= 10 || i < 3 || i >= lines.length - 3), keepLines: true, widowControl: true, spacing: { before: i === 0 ? 60 : 0, after: i === lines.length - 1 ? 60 : 0, line: 276 },
      indent: { left: pos, hanging: pos }, tabStops: [{ type: TabStopType.LEFT, position: pos }],
      border: i === lines.length - 1 ? { bottom: RULE } : undefined,
      children: [new TextRun({ text: `${i + 1}:`, font: FONT, size: 22, color: "595959" }), new TextRun({ text: "\t", font: FONT }), ...algoRuns(l.trim())] });
  });
  return [head, ...io, ...body];
};
// Ký hiệu dạng x_c được in với c là chỉ số dưới.
const subRuns = (t, base) => String(t).split(/(_[a-z0-9](?![A-Za-z0-9_]))/).filter((x) => x).flatMap((x) => x.startsWith("_") ? [new TextRun({ ...base, text: x.slice(1), subScript: true })] : symRuns(x, base));
// Công thức đánh số: công thức căn giữa, số thứ tự căn phải; WH là một dòng giải thích ký hiệu.
const mr = (t) => new MathRun(t);
const frac = (a, b) => new MathFraction({ numerator: [].concat(a).map((x) => (typeof x === "string" ? mr(x) : x)), denominator: [].concat(b).map((x) => (typeof x === "string" ? mr(x) : x)) });
const sub = (a, b) => new MathSubScript({ children: [mr(a)], subScript: [mr(b)] });
const sup = (a, b) => new MathSuperScript({ children: [mr(a)], superScript: [mr(b)] });
const MATHS = {
  1: () => [mr("P = "), frac("TP", "TP + FP")],
  2: () => [mr("R = "), frac("TP", "TP + FN")],
  3: () => [mr("F1 = "), frac("2 · P · R", "P + R")],
  4: () => [mr("Attention(Q, K, V) = softmax"), new MathRoundBrackets({ children: [frac([mr("Q · "), sup("K", "T")], [new MathRadical({ children: [sub("d", "k")] })])] }), mr(" · V")],
  5: () => [mr("idf(t) = ln"), new MathRoundBrackets({ children: [frac("1 + N", "1 + df(t)")] }), mr(" + 1")],
  6: () => [mr("w(t, d) = "), new MathRoundBrackets({ children: [mr("1 + ln tf(t, d)")] }), mr(" · idf(t)")],
  7: () => [sub("w", "c"), mr(" = "), frac("N", [mr("K · "), sub("N", "c")])],
  8: () => [mr("J(A, B) = "), frac("|A ∩ B|", "|A ∪ B|")],
  9: () => [mr("κ = "), frac([sub("p", "o"), mr(" − "), sub("p", "e")], [mr("1 − "), sub("p", "e")])],
  10: () => [mr("s(h, t) = 3 · [quy tắc đoán dương] + [khoảng cách ≤ 4 từ] + [có từ gợi ý]")],
};
// tên công thức cho Danh mục công thức: mỗi dòng danh mục là liên kết tới bookmark eq_n kèm trường PAGEREF lấy số trang
// (trường TC với TOC \f làm Word treo khi cập nhật nên không dùng)
const EQ_NAMES = {
  1: "Precision", 2: "Recall", 3: "F1", 4: "Cơ chế tự chú ý trong Transformer", 5: "Nghịch đảo tần suất văn bản",
  6: "Trọng số TF-IDF của một từ trong văn bản", 7: "Trọng số lớp theo tần suất", 8: "Hệ số Jaccard",
  9: "Hệ số kappa của Cohen", 10: "Điểm khả năng dương của một cặp ứng viên",
};
// số hiển thị theo chương như quy định của Khoa: (2.1)…(2.9) ở Chương 2, (3.1) ở Chương 3
const EQ_LABEL = { 1: "2.1", 2: "2.2", 3: "2.3", 4: "2.4", 5: "2.5", 6: "2.6", 7: "2.7", 8: "2.8", 9: "2.9", 10: "3.1" };
const EQ = (formula, num) => new Paragraph({ keepNext: true, spacing: { before: 120, after: 120 }, tabStops: [{ type: TabStopType.CENTER, position: Math.round(CONTENT_W / 2) }, { type: TabStopType.RIGHT, position: CONTENT_W }],
  children: [new TextRun({ text: "\t", font: FONT }), new OMath({ children: MATHS[num]() }), new TextRun({ text: "\t", font: FONT }), new Bookmark({ id: anchorId("eq", EQ_LABEL[num]), children: [new TextRun({ text: `(${EQ_LABEL[num]})`, font: FONT, size: 26 })] })] });
const WH = (t, last = false) => new Paragraph({ numbering: { reference: "bullets", level: 0 }, keepLines: true, widowControl: true, children: subRuns(renameGold(t), { font: FONT }), alignment: AlignmentType.JUSTIFIED, spacing: { before: 40, after: 0, line: 312 } });
const DESC = (t) => new Paragraph({ keepLines: true, children: runs(plain(t), { italics: true, color: "595959", size: 22 }), alignment: AlignmentType.CENTER, spacing: { before: 60, after: 200, line: 276 } });
// Bảng: tên bảng (add() tự đưa lên trên bảng), bảng, rồi ghi chú mục đích bên dưới.
// Dòng "Nguồn: ..." đặt ngay dưới bảng/hình lấy hoặc tổng hợp từ tài liệu khác (quy định của Khoa)
const SRC = (t) => new Paragraph({ keepNext: true, keepLines: true, children: runs(t, { italics: true, size: 22 }), alignment: AlignmentType.CENTER, spacing: { before: 60, after: 0 } });
const TB = (cap, table, desc, src) => [table, CAP(cap), ...(src ? [SRC(src)] : []), DESC(desc)];
const FIG_DIR = "outputs/bao_cao_khoa_luan_2026-11-05/figures";
const pngSize = (buf) => ({ w: buf.readUInt32BE(16), h: buf.readUInt32BE(20) });
// Hình: ảnh rộng theo khổ trang, tên hình bên dưới, rồi ghi chú mục đích.
const FIG = (file, cap, desc, width0 = 560, src) => {
  const width = Math.min(width0, Math.floor((CONTENT_W / 1440) * 96)); // không rộng hơn vùng chữ
  const buf = fs.readFileSync(path.join(ROOT, file.includes("/") ? file : `${FIG_DIR}/${file}`));
  const { w, h } = pngSize(buf);
  return [new Paragraph({ alignment: AlignmentType.CENTER, keepNext: true, spacing: { before: 160, after: 0, line: 240 }, children: [new ImageRun({ type: "png", data: buf, transformation: { width, height: Math.round((width * h) / w) } })] }), CAP(cap), ...(src ? [SRC(src)] : []), DESC(desc)];
};
const ci2 = (a) => `${rp(a[0])} đến ${rp(a[1])}`;
const CODE = (lines) => lines.map((l, i) => new Paragraph({ keepNext: i < lines.length - 1 && (lines.length <= 10 || i < 3 || i >= lines.length - 3), keepLines: true, children: [new TextRun({ text: l, font: "Consolas", size: 22 })], shading: { fill: "F4F4F4", type: ShadingType.CLEAR, color: "auto" }, spacing: { before: i === 0 ? 80 : 0, after: i === lines.length - 1 ? 160 : 0, line: 240 }, indent: { left: 200 } }));

function T(headers, rows, widths0, opt = {}) {
  const raw = widths0.reduce((a, b) => a + b, 0);
  const total = opt.total || CONTENT_W;
  const widths = widths0.map((w) => Math.floor((w * total) / raw));
  widths[widths.length - 1] += total - widths.reduce((a, b) => a + b, 0);
  // bảng ngắn giữ trọn một trang; bảng dài được nối trang (lặp dòng tiêu đề), nhưng tiêu đề luôn đi cùng hai dòng đầu và hai dòng cuối không bị tách
  // ước lượng chiều cao bảng theo số dòng chữ trong mỗi ô (chữ 12pt rộng trung bình ~110 dxa); bảng cao hơn khoảng một phần ba trang được nối trang
  const cellLines = (txt, w) => Math.max(1, Math.ceil(String(txt).length * 110 / Math.max(300, w - 180)));
  const estPt = [headers, ...rows].reduce((s, r) => s + 6 + 12.6 * Math.max(...r.map((c, i) => cellLines(c, widths[i]))), 0);
  const short = opt.keep !== undefined ? opt.keep : rows.length <= 2 || estPt <= 180;
  const kn = (r) => short || r < 1 || r >= rows.length - 1;
  const cell = (txt, i, head, r = -1) => new TableCell({
    borders, width: { size: widths[i], type: WidthType.DXA },
    margins: { top: 50, bottom: 50, left: 90, right: 90 },
    children: [new Paragraph({ keepNext: head ? true : kn(r), keepLines: true, spacing: { before: 20, after: 20, line: 252 }, children: runs(String(txt), { size: 24, bold: !!head }), alignment: opt.center ? AlignmentType.CENTER : (!head && opt.right && opt.right.includes(i)) ? AlignmentType.RIGHT : AlignmentType.LEFT })],
  });
  return new Table({
    width: { size: total, type: WidthType.DXA }, columnWidths: widths, layout: TableLayoutType.FIXED, // cột cố định: chuỗi dài tự xuống dòng thay vì đẩy bảng ra ngoài lề
    rows: [new TableRow({ tableHeader: true, cantSplit: true, children: headers.map((h, i) => cell(h, i, true)) }),
      ...rows.map((r, ri) => new TableRow({ cantSplit: true, children: r.map((c, i) => cell(c, i, false, ri)) }))],
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
const REFLIST = (items) => { REFS.push("refs"); return items.map((t, i) => new Paragraph({ numbering: { reference: "refs", level: 0 }, children: [new Bookmark({ id: anchorId("ref", i + 1), children: [new TextRun({ text: plain(t), font: FONT })] })], alignment: AlignmentType.JUSTIFIED, spacing: { before: 119, after: 0, line: 240 } })); };
const LIST = (items) => { const id = newList(); return items.map((t) => NUM(t, id)); };
const MATH = (t) => new Paragraph({ children: runs(t, { italics: true }), alignment: AlignmentType.CENTER, spacing: { before: 80, after: 120 } });
// rp được khai báo sớm hơn (dùng ở phần số liệu)
const SUM = (t) => P(t); // đoạn mở đầu chương, không đóng khung

const A_RAW = [
  ["A1", "Kết quả NER cũ (17/09) chạy trước khi thêm Luật 1b (01/11)", "Ngày tệp eval/results; git log ner/config.py", "Số NER có thể không khớp mã hiện tại", sameNer ? "Đã chạy lại 05/11: kết quả không đổi" : "Đã chạy lại 05/11; dùng số mới"],
  ["A2", "Tài liệu ghi “37 loại nhãn”, thực tế là 37 nhãn BIO của 18 loại", "raw_37label_report.json có 18 loại", "Mô tả sai trong luận văn", "Báo cáo dùng “18 loại, 37 nhãn BIO”"],
  ["A3", "PROJECT_OVERVIEW.md ghi RE “chưa thực hiện”", "Có module relation_extraction/", "Tài liệu lỗi thời", "Cần cập nhật PROJECT_OVERVIEW.md"],
  ["A4", "relation_extraction/README.md báo số trên nhãn LLM (178 cặp)", `Gold v1: ${reGold.pairs} cặp`, "Dễ trích nhầm số cũ", "Dùng số gold v1 (Chương 4)"],
  ["A5", "Tiêu đề re_compare_baselines.py ghi cứng “nhãn LLM, 178 cặp”", "scripts/re_compare_baselines.py", "Báo cáo sai nguồn nhãn", "Đã sửa 05/11: đọc nguồn và số cặp từ dữ liệu"],
  ["A6", "NER sinh thực thể chung (“điều trị”, “thuốc”) mà gold RE đã xóa", "Demo cũ nối “đau” → “điều trị”", "Lệch phân phối train/inference cho RE", "Đã sửa 06/11: lọc ở đầu vào RE, có kiểm thử"],
  ["A7", "ICD-10 fuzzy gán mã sai (huyết áp cao → Z01.3 …)", "Bảng 4.2", `${icdBefore.wrong_mentions} mention sai trên gold v1`, `Đã sửa 06/11: 2 ràng buộc + 6 alias; còn ${icd.wrong_mentions} sai`],
  ["A8", "Thông tin người duyệt gold v1 là giá trị tạm", `manifest: ${gold.reviewer}`, "Không chứng minh được việc duyệt", "Cần điền tên/ngày thật"],
  ["A9", "Golden test chưa được bác sĩ duyệt", "Chỉ có ai_labels.jsonl (LLM tiền gán), chưa có gold.jsonl", "Kết quả RE trên golden test là tạm thời", "07/11: có kết quả trên nhãn LLM (4.4.2); cần duyệt"],
  ["A10", "Bộ RE lấy từ split train của NER", "source_split = train", "Không dùng làm test độc lập", "Đã ghi ở 5.6"],
  ["A11", `Dev/test RE quá nhỏ (${posSplit("dev")}/${posSplit("test")} cặp dương)`, "Phụ lục H", "F1 một lần chia không tin cậy", "Báo cáo kèm CV và CI95"],
  ["A12", "summary.md cũ khẳng định “đảm bảo không data leakage”", "eval/run_eval.py", "Phát biểu quá mạnh", "Viết lại thành mức độ đã kiểm soát (5.6)"],
  ["A13", "Điểm benchmark Bảng 2.2 chép từ tài liệu nội bộ", "docs/BAO_CAO_RE_2026-10-02.md", "Có thể sai lệch", "Cần đối chiếu bài báo gốc"],
  ["A14", "Danh sách thực thể chung cụ thể do người soát đề xuất", "relation_extraction/data.py", "Quyết định gán nhãn", "Người duyệt cần xác nhận danh sách"],
  ["A15", "Không rõ checkpoint NER được chọn trên validation hay test", "training_args.bin: eval_strategy=epoch, không ghi tập", "Có thể làm NER F1 trên test lạc quan", "08/11: baseline chỉ học train cũng tụt validation→test như checkpoint; chênh lệch do validation gần train (4.1.5). Vẫn chưa rõ tập chọn checkpoint"],
  ["A16", "Quy ước CONDITION chung chung chưa được hỏi", "manifest.conventions.generic_condition", "“bệnh”, “biến chứng” vẫn tham gia cặp", "Cần chốt với GVHD"],
  ["A17", "MAX_SUBTOKENS_PER_CHUNK = 200 được import nhưng không dùng", "ner/config.py, ner/preprocessor.py", "Văn bản dài có thể bị cắt ở 258 subtoken", "Chưa sửa; ghi ở 3.2"],
  ["A18", "“\\n” trong tập kết thúc câu nhưng bộ tách token bỏ khoảng trắng", "ner/preprocessor.py", "Xuống dòng không tách câu", "Chưa sửa; ghi ở 3.2"],
  ["A19", "Alias ICD-10 mới rút ra từ chính bộ đo", "Mục 4.2.1", "Kết quả sau sửa lạc quan", "07/11: đã có tập gold dev/test riêng (4.2.2)"],
  ["A20", "Golden test chưa áp quy ước xóa thực thể chung", "data/golden_test/v1/", "Hai bộ không nhất quán", "07/11: nhãn LLM tiền gán đã xóa thực thể chung (verdict XOA)"],
  ["A21", "Tập gold chuẩn hóa dev/test do LLM gán", "data/norm_gold_v1, human_verified = false", "Accuracy/Top-k là tạm thời", "Cần bác sĩ duyệt phiếu Excel rồi chạy lại"],
  ["A22", "Bộ RE v2 (199 câu) do LLM gán, hai lượt", "data/re_ai_v2, human_verified = false", "Mô hình RE v2 học từ nhãn chưa duyệt", "Ghi rõ nguồn nhãn; cần duyệt"],
  ["A23", "RE v2 và nhãn golden test cùng do LLM gán", "Cùng một người gán (LLM) và cùng hướng dẫn", "Sai lệch có hệ thống của người gán không bị phát hiện", "Ghi là hạn chế (5.7); chỉ người duyệt độc lập mới loại được"],
  ["A24", "Từ điển chuẩn hóa thêm 137 alias từ train/dev", "normalization/data/icd10_synonyms.json", "Kết quả dev lạc quan", "Chỉ báo cáo test; test không dùng để chọn alias"],
  ["A26", "Golden test bị làm giàu cặp dương (lấy mẫu theo hạn mức)", "Baseline “mọi cặp dương” đạt F1 cao hơn mô hình", "F1 golden test không so được với dữ liệu tự nhiên", "08/11: thêm tập test ngẫu nhiên; báo cáo kèm baseline (4.4.2)"],
  ["A27", "Nhãn golden test lệch quy ước gold v1", "17 cặp (vitamin d → cao, “thuốc” chung chung…)", "Chấm mô hình theo quy ước khác lúc học", "08/11: bản rà soát, giữ bản gốc, báo cáo cả hai"],
  ["A28", "Mô hình RE tốt nhất chưa vào pipeline/KG", "KG dùng TF-IDF ∪ luật", "Đồ thị kém hơn khả năng hiện có", "08/11: lưu ViHealthBERT 3 seed, đưa vào pipeline, dựng lại KG (3.7.3, 4.6)"],
  ["A30", "Dữ liệu dịch từ tiếng Anh không cải thiện RE", `${aug.variants.biotext_ade.extra_pairs} cặp BioText/ADE dịch; chênh F1 ∪ luật trên test ngẫu nhiên ${adf("random_test", "biotext_ade")}`, "Không vá được dữ liệu ít bằng dữ liệu khác miền", "Giữ mô hình triển khai theo quy tắc định trước; báo cáo kết quả âm và nguyên nhân (4.3.4)"],
  ["A29", "Một seed ViHealthBERT dao động mạnh", `F1 ∪ luật trên test ngẫu nhiên ${rp(Math.min(...depSeedRT))}–${rp(Math.max(...depSeedRT))} giữa ba seed`, "Mô hình một seed có thể kém hơn luật", "Triển khai đúng phương pháp đã chấm: trung bình ba seed"],
  ["A25", "KG chứa cạnh sai và nút là mảnh NER", "kg.html, ví dụ “mất răng → xương”", "Đồ thị chưa dùng làm tri thức tin cậy", "Ghi rõ ở 4.6; mỗi cạnh giữ câu nguồn và nguồn dự đoán"],
  ["A31", "Tập kiểm tra RE gán lại theo tiêu chí chặt có dùng nhãn gợi ý của LLM", `kappa ${f(RX.agTest2.kappa, 3)} với nhãn LLM độc lập`, "Tập kiểm tra không độc lập với nhãn LLM", "Ghi rõ ở mục 3.3.3.4 và 4.7.4; cần người gán thứ hai"],
  ["A32", "has_dosage không có cặp nào trong tập huấn luyện thật", "relation/data/seed_review_summary.json", "Quan hệ chỉ học từ dữ liệu sinh, precision thấp", "Ghi ở mục 4.3.2 và 4.6.3"],
  ["A33", "Chưa có đánh giá RE trên thực thể do NER sinh ra", "Kế hoạch có, chưa chạy", "Chưa đo được ảnh hưởng của lỗi NER lên RE", "Ghi ở mục 4.3.4"],
  ["A35", "Bước kiểm tra dữ liệu sinh dựa một phần vào LLM", `người duyệt đồng ý ${pct(rxVP.sample_valid.rate)} câu Valid nhưng chỉ ${pct(rxVP.sample_wrong.rate)} câu bị LLM loại`, "Khoảng một phần mười câu chỉ qua kiểm tra tự động có thể còn sai", "Ghi ở mục 3.3.3.7; câu Invalid chỉ được giữ khi người duyệt đồng ý"],
  ["A34", "Đồ thị dựng bằng mô hình RE mới chứa nhiều cạnh nối thực thể sai kiểu", `${kgS.edges} cạnh so với ${kgOldS.edges} của đồ thị cũ`, "Bộ lọc thực thể của hệ thống chỉ là danh sách chặn", "Ghi ở mục 4.5; cần bộ phân loại thực thể hợp lệ"],
];
// bỏ các dòng về bộ dữ liệu quan hệ cũ (đã thay bằng dữ liệu làm lại ở relation/), đánh số lại
const A_OLD_RE = new Set(["A4", "A5", "A6", "A8", "A9", "A10", "A11", "A16", "A20", "A22", "A23", "A26", "A27", "A28", "A29", "A30"]);
const A = A_RAW.filter((r) => !A_OLD_RE.has(r[0])).map((r, i) => [`A${i + 1}`, ...r.slice(1)]);

const C = [];
// tên bảng đặt phía trên bảng (quy cách trình bày khóa luận)
const add = (...xs) => xs.flat().forEach((x) => {
  if (x && x.__tableCaption && C.length && C[C.length - 1] instanceof Table) C.splice(C.length - 1, 0, x);
  else C.push(x);
});

// ===== Phần đầu theo mẫu (bìa chèn sau bằng apply_template.py) =====
const COVER = J("outputs/bao_cao_khoa_luan_2026-11-05/thong_tin_bia.json");
const FRONT_W = 11906 - 1985 - 1418; // lề phần đầu theo mẫu
add(
  H1("MỤC LỤC"),
  new TableOfContents("Mục lục", { hyperlink: true, headingStyleRange: "1-3" }),
  H1("LỜI CAM ĐOAN"),
  P(`Tôi xin cam đoan khóa luận tốt nghiệp “${COVER.ten_de_tai}” là công trình nghiên cứu của riêng tôi, được thực hiện dưới sự hướng dẫn của ${COVER.gvhd_trong_cam_doan || COVER.giang_vien_huong_dan}. Các số liệu và kết quả trình bày trong khóa luận được sinh trực tiếp từ mã nguồn và tệp kết quả đi kèm, trung thực và chưa từng được công bố trong công trình nào khác. Các tài liệu, dữ liệu và mô hình của người khác được sử dụng đều được trích dẫn đầy đủ.`),
  P("Một số bộ dữ liệu trong khóa luận được gán nhãn tự động bằng mô hình ngôn ngữ lớn; nguồn gốc và mức độ kiểm định của từng bộ được trình bày tại mục 3.3 và trong phần hạn chế."),
  new Paragraph({ children: runs(`Hà Nội, ngày      tháng     năm ${COVER.nam}`, { italics: true }), alignment: AlignmentType.RIGHT, spacing: { before: 360 } }),
  new Paragraph({ children: runs("Sinh viên", { bold: true }), alignment: AlignmentType.RIGHT, indent: { right: 1100 } }),
  new Paragraph({ children: runs("(ký, ghi rõ họ tên)", { italics: true }), alignment: AlignmentType.RIGHT, indent: { right: 850 } }),
  new Paragraph({ children: runs(COVER.ky_ten ?? COVER.ten_sinh_vien, { bold: true }), alignment: AlignmentType.RIGHT, indent: { right: 900 }, spacing: { before: 1200 } }),
  H1("LỜI CẢM ƠN"),
  ...(COVER.loi_cam_on ? [P(COVER.loi_cam_on)] : []),
);

// ===== Danh mục từ viết tắt =====
add(
  H1("DANH MỤC CÁC TỪ VIẾT TẮT"),
  T(["Từ viết tắt", "Ý nghĩa"], [
    ["NER", "Nhận diện thực thể có tên (Named Entity Recognition)"],
    ["RE", "Trích xuất quan hệ giữa các thực thể (Relation Extraction)"],
    ["BIO", "Lược đồ gán nhãn chuỗi gồm Begin, Inside và Outside"],
    ["ICD-10", "Phân loại bệnh quốc tế, phiên bản 10 (International Classification of Diseases)"],
    ["RxNorm", "Danh mục thuốc chuẩn của Thư viện Y khoa Quốc gia Hoa Kỳ"],
    ["RxCUI", "Mã định danh khái niệm thuốc trong RxNorm (RxNorm Concept Unique Identifier)"],
    ["FMA", "Mô hình nền tảng về giải phẫu học (Foundational Model of Anatomy)"],
    ["LOINC", "Danh mục mã chuẩn cho xét nghiệm và quan sát lâm sàng (Logical Observation Identifiers Names and Codes)"],
    ["MeSH", "Bộ tiêu đề chủ đề y học (Medical Subject Headings)"],
    ["CRF", "Trường ngẫu nhiên có điều kiện (Conditional Random Fields)"],
    ["BiLSTM-CRF", "Mạng bộ nhớ dài-ngắn hai chiều kết hợp trường ngẫu nhiên có điều kiện (Bidirectional Long Short-Term Memory – Conditional Random Fields)"],
    ["RoBERTa", "Biến thể của BERT được huấn luyện trước theo cách tối ưu hơn (Robustly Optimized BERT Pretraining Approach)"],
    ["PURE", "Phương pháp trích xuất thực thể và quan hệ của Đại học Princeton (Princeton University Relation Extraction)"],
    ["n2c2", "Chuỗi thử thách xử lý ngôn ngữ tự nhiên lâm sàng của Hoa Kỳ (National NLP Clinical Challenges)"],
    ["ADE", "Biến cố bất lợi do thuốc (Adverse Drug Event)"],
    ["Âm tiết", "Đơn vị phát âm của tiếng Việt, viết tách nhau bằng khoảng trắng, một từ có thể gồm nhiều âm tiết (syllable)"],
    ["Subword", "Mảnh con của một từ do bộ tách từ của mô hình tạo ra"],
    ["Self-attention", "Cơ chế tự chú ý, cho phép mỗi token tổng hợp thông tin từ mọi token khác trong câu"],
    ["Logits", "Điểm số mô hình gán cho từng lớp trước khi đưa qua hàm softmax"],
    ["Ký hiệu đánh dấu thực thể", "Ký hiệu chèn vào câu để đánh dấu vị trí thực thể đầu và thực thể đuôi (marker)"],
    ["ViHealthBERT", "Mô hình ngôn ngữ pre-train cho văn bản y tế tiếng Việt"],
    ["TF-IDF", "Trọng số tần suất từ và nghịch đảo tần suất văn bản (Term Frequency, Inverse Document Frequency)"],
    ["P, R, F1", "Precision, recall và trung bình điều hòa của hai đại lượng này"],
    ["Khớp chặt", "Cách chấm yêu cầu khớp đúng cả span lẫn loại thực thể (⁠strict match)"],
    ["Khớp nới lỏng", "Cách chấm chấp nhận dự đoán cùng loại có span giao với span chuẩn (⁠relaxed match)"],
    ["Micro, macro", "Gộp chỉ số bằng cách cộng dồn trên mọi lớp, hoặc lấy trung bình không trọng số giữa các lớp"],
    ["CI95", "Khoảng tin cậy 95%"],
    ["Gold", "Nhãn chuẩn dùng làm đáp án khi chấm điểm, trong báo cáo gọi là nhãn chuẩn"],
    ["Lượt đề cập", "Một lần xuất hiện cụ thể của thực thể trong văn bản (⁠mention)"],
    ["Span", "Đoạn ký tự từ vị trí bắt đầu tới vị trí kết thúc của một thực thể"],
    ["Thực thể đầu, thực thể đuôi", "Hai đầu của một quan hệ có hướng (⁠head, tail)"],
    ["VALID, INVALID", "Kết luận ở bước kiểm tra thực thể, cho biết lượt đề cập đúng kiểu hay sai kiểu"],
    ["NO_RELATION", "Nhãn âm cho cặp đúng kiểu nhưng không có quan hệ"],
    ["Thử nghiệm lược bỏ", "Thí nghiệm lần lượt bỏ từng thành phần để đo đóng góp của thành phần đó (⁠ablation)"],
    ["Dev", "Tập dùng để chọn tham số, khác với test là tập chỉ chạy một lần để báo cáo"],
    ["Độ chính xác Top-k", "Tỉ lệ mã đúng nằm trong k ứng viên đầu tiên, còn gọi là Recall@k"],
    ["MRR", "Trung bình nghịch đảo thứ hạng của mã đúng (Mean Reciprocal Rank)"],
    ["NIL", "Đề cập không có mã đúng trong danh mục, hệ thống được tính đúng khi từ chối gán mã"],
    ["Baseline", "Phương pháp đơn giản dùng làm mốc so sánh cho phương pháp đề xuất"],
    ["Rule-based", "Cách tiếp cận dựa trên quy tắc viết tay thay vì học từ dữ liệu"],
    ["Fuzzy matching", "So khớp mờ, cho phép hai chuỗi khác nhau một phần vẫn được coi là khớp"],
    ["token_set_ratio", "Độ đo so khớp mờ dựa trên tập từ chung của hai chuỗi, thang 0 đến 100"],
    ["Token", "Đơn vị văn bản mà mô hình xử lý, có thể là một từ, một dấu câu hoặc một mảnh từ"],
    ["Embedding", "Vector số biểu diễn một token hay một vị trí, được mô hình học trong quá trình huấn luyện"],
    ["Transformer", "Kiến trúc mạng nơ-ron dựa trên cơ chế tự chú ý, nền tảng của BERT"],
    ["Dropout", "Kỹ thuật tạm bỏ ngẫu nhiên một phần nơ-ron khi huấn luyện để giảm quá khớp"],
    ["Seed", "Giá trị khởi tạo cho bộ sinh số ngẫu nhiên, quyết định trọng số ban đầu và thứ tự dữ liệu khi huấn luyện"],
    ["Bootstrap", "Phương pháp lấy mẫu lại có hoàn lại để ước lượng khoảng tin cậy của một chỉ số"],
    ["Train, validation, test", "Ba phần chia của bộ dữ liệu, lần lượt dùng để huấn luyện, chọn tham số và đánh giá"],
    ["Dữ liệu sinh", "Cặp quan hệ được tạo tự động từ câu huấn luyện bằng cách thay thực thể hoặc điền vào mẫu câu"],
    ["KG", "Đồ thị tri thức với nút là khái niệm và cạnh là quan hệ (Knowledge Graph)"],
    ["LLM", "Mô hình ngôn ngữ lớn (Large Language Model)"],
    ["Nhãn LLM", "Nhãn do mô hình ngôn ngữ lớn gán tự động theo hướng dẫn, chưa được chuyên gia y tế kiểm định"],
  ], [2600, 7038], { total: FRONT_W, size: 26 }),
  H1("DANH MỤC BẢNG"),
  P("Bảng được đánh số theo chương, ví dụ Bảng 2.1 là bảng đầu tiên trong Chương 2.", { noIndent: true, align: AlignmentType.CENTER, run: { italics: true } }),
  new TableOfContents("Danh mục bảng", { hyperlink: true, stylesWithLevels: [{ styleName: "BangCaption", level: 4 }] }),
  H1("DANH MỤC HÌNH"),
  P("Hình được đánh số theo chương, ví dụ Hình 2.1 là hình đầu tiên trong Chương 2.", { noIndent: true, align: AlignmentType.CENTER, run: { italics: true } }),
  new TableOfContents("Danh mục hình", { hyperlink: true, stylesWithLevels: [{ styleName: "HinhCaption", level: 4 }] }),
  H1("DANH MỤC CÔNG THỨC"),
  P("Công thức được đánh số theo chương, ví dụ công thức (2.1) là công thức đầu tiên trong Chương 2.", { noIndent: true, align: AlignmentType.CENTER, run: { italics: true } }),
  ...Object.entries(EQ_NAMES).map(([k, name]) => new Paragraph({
    style: "TOC4", tabStops: [{ type: TabStopType.RIGHT, position: FRONT_W, leader: LeaderType.DOT }],
    children: [new InternalHyperlink({ anchor: anchorId("eq", EQ_LABEL[k]), children: [new TextRun({ text: `Công thức (${EQ_LABEL[k]}). ${name}`, font: FONT })] }), new TextRun({ text: "\t", font: FONT }), new PageReference(anchorId("eq", EQ_LABEL[k]), { hyperlink: true })],
  })),
);
const FRONT = C.splice(0, C.length); // hết phần đầu (số trang La Mã)

// Mở đầu gói gọn trong một trang: dẫn nhập và tên đề tài, phương pháp, kết quả chính, lưu ý về nguồn nhãn
const SUMMARY = [
  P("Các văn bản y tế như diễn biến bệnh, kết luận khám hay lời dặn của bác sĩ chứa nhiều thông tin có giá trị nhưng phần lớn được ghi dưới dạng văn bản tự do, nên máy tính chưa thể thống kê hay tìm kiếm theo khái niệm. Xuất phát từ nhu cầu đó, khóa luận thực hiện đề tài “Hệ thống trích xuất thực thể, quan hệ và chuẩn hóa thông tin y tế từ văn bản tiếng Việt”, với mục đích xây dựng và đánh giá một hệ thống nhận văn bản y tế tiếng Việt và trả về các thực thể y tế, mã chuẩn của từng thực thể cùng quan hệ giữa chúng."),
  P("Hệ thống gồm ba thành phần là NER, RE và chuẩn hóa thực thể sang ICD-10 cho bệnh và RxNorm cho thuốc. Hệ thống nhận diện sáu loại thực thể và năm quan hệ có hướng, rồi gộp kết quả của nhiều văn bản thành một knowledge graph. Phần NER dùng mô hình ViHealthBERT đã được tinh chỉnh trên bộ VietMed-NER, kết hợp quy tắc nhận diện liều lượng và một bước hậu xử lý. Vì tiếng Việt chưa có bộ dữ liệu quan hệ công khai phù hợp, khóa luận tự xây dựng dữ liệu quan hệ theo hướng dẫn hai bước, kiểm tra thực thể trước rồi mới gán quan hệ, gồm 600 câu huấn luyện và kiểm định cùng 100 câu kiểm tra."),
  P(`Trên ${n(nerNew.lat.total_samples)} câu của tập test, luồng NER đạt micro-F1 ${f(s["micro avg"]["f1-score"], 3)} khi yêu cầu trùng cả vị trí lẫn loại và ${f(r["micro avg"]["f1-score"], 3)} khi chấp nhận vị trí giao nhau, với ${f(nerNew.lat.mean_latency_ms, 0)} ms mỗi câu trên CPU${nerBase && nerInh ? `, trong đó riêng mô hình đạt ${f(nerInh.scores.test.target.micro.f1, 3)}, cao hơn hai baseline tra từ điển với ${f(nerBase.dictionary.test.target.micro.f1, 3)} và CRF với ${f(nerBase.crf.test.target.micro.f1, 3)}` : ""}. Với RE, ViHealthBERT đạt F1 ${rp(rxM("model").f1)} trên tập kiểm tra, cao hơn rule-based với ${rp(rxM("rules").f1)} và chênh lệch có ý nghĩa thống kê. Ở chế độ strict, mọi mã ICD-10 hệ thống đưa ra đều đúng, nhưng độ chính xác trên toàn bộ tên bệnh chỉ đạt ${rp(nc("ICD-10").system.accuracy)} vì nhiều tên bệnh không được gán mã, trong khi mã đúng nằm trong mười ứng viên đầu ở ${pct(nc("ICD-10").top10_acc)} trường hợp và độ chính xác RxNorm đạt ${rp(nc("RxNorm").system.accuracy)}. Knowledge graph dựng từ tập test có ${n(kgS.nodes)} thực thể và ${kgS.edges} quan hệ khác nhau.`),
];

// ===== MỞ ĐẦU: dẫn nhập, tên đề tài, mục đích, phương pháp và kết quả chính (1-2 trang theo quy định) =====
add(
  H1("MỞ ĐẦU"),
  ...SUMMARY,
);

// ===== CHƯƠNG 1. TỔNG QUAN VỀ ĐỀ TÀI (tách từ phần Mở đầu cũ theo bố cục của Trường) =====
add(
  H1("CHƯƠNG 1. TỔNG QUAN VỀ ĐỀ TÀI"),
  SUM("Chương này trình bày lý do chọn đề tài, mục đích, đối tượng và phạm vi nghiên cứu, ý nghĩa khoa học và thực tiễn của đề tài, sau đó chỉ ra các vấn đề mà khóa luận tập trung giải quyết cùng bố cục của báo cáo."),
  H2("1.1. Lý do chọn đề tài"),
  P("Hồ sơ y tế ở Việt Nam đang được số hóa nhanh. Thông tư 13/2025/TT-BYT [27] hướng dẫn việc triển khai hồ sơ bệnh án điện tử, và theo Bộ Y tế, đến ngày 31/12/2025 cả nước đã có 1.188 trong tổng số hơn 1.650 cơ sở khám, chữa bệnh triển khai bệnh án điện tử [28]. Tuy nhiên, số hóa mới thay đổi cách lưu trữ, còn những phần giàu thông tin nhất như diễn biến bệnh, kết luận khám và lời dặn của bác sĩ vẫn chủ yếu được ghi dưới dạng văn bản tự do. Dạng dữ liệu này dễ viết nhưng khó khai thác bằng máy, bởi nếu chưa được chuyển sang dạng có cấu trúc thì không thể thống kê, tìm kiếm theo khái niệm hay liên thông giữa các hệ thống. Trích xuất thông tin tự động giải quyết vấn đề này bằng cách biến một câu như “bệnh nhân đau dạ dày, kê Paracetamol 500mg” thành các bản ghi có cấu trúc, gồm tình trạng bệnh kèm mã ICD-10, thuốc kèm mã RxNorm, liều dùng và quan hệ giữa chúng."),
  P("Để làm được việc đó, nhận diện từng thực thể riêng lẻ là chưa đủ. Chẳng hạn, khi một đơn thuốc kê hai thuốc với hai liều khác nhau, hệ thống phải xác định được liều nào thuộc thuốc nào. Tương tự, khi một câu nhắc tới nhiều bệnh và nhiều thuốc, hệ thống phải biết thuốc nào được dùng để điều trị bệnh nào. Bài toán nối các thực thể lại với nhau như vậy được gọi là RE. Chỉ khi có đủ thực thể, mã chuẩn và quan hệ, dữ liệu mới dùng được cho các ứng dụng như gợi ý mã bệnh, thống kê theo bệnh hoặc theo thuốc và tìm kiếm hồ sơ theo khái niệm. Quá trình biến câu ví dụ trên thành bản ghi có cấu trúc được minh họa chi tiết ở Hình 2.1 trong Chương 2."),
  P("Đề tài được lựa chọn vì hai lý do. Về nhu cầu, lượng văn bản y tế tiếng Việt tăng nhanh theo quá trình triển khai bệnh án điện tử, trong khi việc đọc và gán mã thủ công tốn nhiều thời gian và dễ sai. Về khoảng trống nghiên cứu, các bộ dữ liệu y tế tiếng Việt đã công bố mới dừng ở nhãn thực thể hoặc ý định câu hỏi, nên bài toán nối thực thể thành quan hệ và gán mã chuẩn cho cách nói thường ngày của tiếng Việt vẫn còn bỏ ngỏ, như phân tích ở mục 1.5."),
  H2("1.2. Mục đích nghiên cứu"),
  P("Hệ thống làm việc với sáu loại thực thể là tình trạng bệnh hoặc triệu chứng, thuốc, bộ phận cơ thể, xét nghiệm, thủ thuật và liều dùng, lần lượt mang nhãn CONDITION, DRUG, BODY_PART, TEST, PROCEDURE và DOSAGE."),
  P("Từ bối cảnh trên, khóa luận hướng tới năm mục tiêu cụ thể. Trước hết, hệ thống cần nhận diện được sáu loại thực thể này trong văn bản y tế tiếng Việt, kể cả khi văn bản dài hơn giới hạn đầu vào của mô hình hoặc chứa các cụm liều thuốc. Tiếp theo, mỗi tình trạng bệnh cần được gán mã ICD-10 và mỗi thuốc cần được gán mã RxNorm. Ở bước này khóa luận ưu tiên độ tin cậy, nghĩa là hệ thống chỉ gán mã khi đủ chắc chắn và trong các trường hợp còn lại sẽ trả về danh sách ứng viên để người dùng tự chọn. Mục tiêu thứ ba là xây dựng dữ liệu và mô hình RE cho năm quan hệ có hướng, sau đó so sánh mô hình với baseline rule-based. Mục tiêu thứ tư là gộp kết quả trích xuất từ nhiều văn bản thành một knowledge graph để tra cứu. Cuối cùng, mọi thành phần đều được đánh giá bằng một quy trình tái lập được, có baseline để so sánh và có phân tích lỗi đi kèm."),
  H2("1.3. Đối tượng và phạm vi nghiên cứu"),
  P("Đối tượng nghiên cứu của khóa luận là văn bản y tế tiếng Việt và ba bài toán xử lý trên loại văn bản này, gồm NER, RE và chuẩn hóa thực thể sang hai danh mục chuẩn là ICD-10 cho bệnh và RxNorm cho thuốc. Dữ liệu thực nghiệm là lời nói y tế đã được chép thành văn bản trong bộ VietMed-NER, cùng các bộ dữ liệu quan hệ và chuẩn hóa do khóa luận xây dựng từ bộ này."),
  P("Về phạm vi, đề tài giới hạn ở sáu loại thực thể nêu trên và năm quan hệ có hướng giữa chúng. Quan hệ located_at nối một tình trạng bệnh với bộ phận cơ thể nơi tình trạng đó xuất hiện, treated_by nối tình trạng bệnh với thuốc dùng để điều trị, còn treated_by_procedure nối tình trạng bệnh với thủ thuật điều trị. Quan hệ diagnosed_by nối tình trạng bệnh với xét nghiệm dùng để phát hiện nó, và has_dosage nối một thuốc với liều dùng của thuốc đó. Định nghĩa chi tiết kèm ví dụ của từng quan hệ được trình bày ở Bảng 2.1. Nhãn CONDITION gộp cả bệnh lẫn triệu chứng vì nhãn gốc của VietMed-NER vốn đã gộp hai khái niệm này. Quan hệ chỉ được xét trong cùng một câu hoặc một phát ngôn ngắn, nên khóa luận không xử lý quan hệ liên câu, đồng tham chiếu hay thực thể lồng nhau. Knowledge graph chỉ gộp các bộ ba đã trích xuất, không suy luận thêm và không đối chiếu với tri thức y khoa bên ngoài. Cuối cùng, bộ phận cơ thể, xét nghiệm và thủ thuật chưa được gán mã chuẩn, còn liều dùng được giữ dưới dạng giá trị, đơn vị và tần suất."),
  H2("1.4. Ý nghĩa khoa học và thực tiễn"),
  P("Về mặt khoa học, khóa luận có hai đóng góp. Đóng góp thứ nhất là các bộ dữ liệu quan hệ và chuẩn hóa mã cho văn bản y tế tiếng Việt, có quy ước gán nhãn và ghi rõ nguồn nhãn của từng bộ, trong bối cảnh tiếng Việt chưa có bộ dữ liệu quan hệ lâm sàng nào được công bố. Đóng góp thứ hai là một khung đánh giá có baseline, khoảng tin cậy, phân tích lỗi và thử nghiệm lược bỏ. Trong thử nghiệm này, quy tắc liều lượng và bước hậu xử lý lần lượt được bỏ khỏi luồng NER để đo phần đóng góp của từng thành phần. Mọi số liệu trong báo cáo đều có thể tái lập từ dữ liệu và mô hình đi kèm, nhờ đó người khác có thể so sánh trên cùng điều kiện."),
  P("Về mặt thực tiễn, khóa luận xây dựng một luồng xử lý chạy được từ văn bản tới knowledge graph, có giao diện minh họa. Với mỗi văn bản đầu vào, hệ thống trả về các thực thể kèm vị trí ký tự bắt đầu và kết thúc trong văn bản gốc, mã ICD-10 hoặc RxNorm của từng thực thể, và các quan hệ giữa những thực thể đó. Hệ thống có thể dùng làm công cụ hỗ trợ, chẳng hạn gợi ý thực thể và mã bệnh để người nhập liệu xác nhận, hoặc làm bước tiền xử lý cho tìm kiếm và thống kê theo bệnh và theo thuốc. Nguyên tắc chỉ gán mã khi đủ chắc chắn và trả về danh sách ứng viên trong các trường hợp còn lại phù hợp với miền y tế, nơi một mã sai gây hại nhiều hơn một mã còn để trống."),
  H2("1.5. Các vấn đề đề tài tập trung giải quyết"),
  P("Với tiếng Việt, đề tài gặp ba khó khăn về tài nguyên. Thứ nhất, bộ VietMed-NER đã có nhãn thực thể cho lời nói y tế nhưng chưa có nhãn quan hệ. Các bộ dữ liệu y tế tiếng Việt khác đã được công bố như PhoNER_COVID19 [23], ViMQ [29] hay ViMedNER [30] cũng chỉ gán nhãn thực thể hoặc ý định của câu hỏi, và theo tìm hiểu của khóa luận, hiện chưa có bộ dữ liệu quan hệ lâm sàng tiếng Việt nào được công bố. Thứ hai, danh mục ICD-10 của Bộ Y tế dùng tên bệnh theo văn phong hành chính, trong khi người bệnh và bác sĩ nói theo cách thường ngày, ví dụ “huyết áp cao” thay cho “bệnh lý tăng huyết áp”. Thứ ba, RxNorm là danh mục thuốc của Hoa Kỳ nên nhiều tên thuốc lưu hành ở Việt Nam không có trong đó. Do vậy, ngoài việc xây dựng hệ thống, khóa luận phải tự tạo dữ liệu quan hệ, xây từ điển alias để nối cách nói thường ngày với tên chuẩn, và xây dựng một quy trình đánh giá phù hợp với dữ liệu có kích thước nhỏ."),
  P("Từ ba khó khăn này, khóa luận tập trung trả lời ba câu hỏi nghiên cứu sau."),
  ...LIST([
    "Mô hình RE học từ dữ liệu có tốt hơn baseline rule-based trên cùng bộ dữ liệu hay không?",
    "Lỗi NER ảnh hưởng tới chất lượng RE của toàn hệ thống như thế nào?",
    "Các bước xử lý bổ sung như luật liều lượng, hậu xử lý và chuẩn hóa mã đem lại lợi ích gì và tạo ra những lỗi gì?",
  ]),
  P("Ba câu hỏi này gắn trực tiếp với các mục tiêu ở mục 1.2. Câu hỏi thứ nhất kiểm chứng mục tiêu xây dựng dữ liệu và mô hình RE, bằng cách so sánh mô hình học từ dữ liệu với một baseline rule-based trên cùng tập kiểm tra. Câu hỏi thứ hai gắn với mục tiêu ghép các thành phần thành một luồng xử lý hoàn chỉnh, vì chất lượng của luồng phụ thuộc vào cách lỗi lan từ bước này sang bước sau. Câu hỏi thứ ba gắn với mục tiêu đánh giá có baseline và phân tích lỗi, nhằm làm rõ phần đóng góp của từng bước bổ sung. Mỗi câu hỏi được trả lời bằng thực nghiệm ở Chương 4 và được tổng kết ở mục 4.7.1."),
  H2("1.6. Bố cục báo cáo"),
  P("Ngoài phần Mở đầu và Kết luận, khóa luận gồm bốn chương, trong đó mỗi chương chuyển kết quả cho chương sau. Chương 1 giới thiệu tổng quan về đề tài. Chương 2 trình bày cơ sở lý thuyết của ba bài toán NER, RE và chuẩn hóa mã, các độ đo dùng để đánh giá và các nghiên cứu liên quan. Chương 3 trình bày phương pháp nghiên cứu, gồm công cụ và giao thức đánh giá, quy trình thực hiện, các bộ dữ liệu cùng độ tin cậy của từng nguồn nhãn, và thiết kế của hệ thống. Chương 4 báo cáo kết quả thực nghiệm của từng thành phần và của cả luồng xử lý, sau đó phân tích lỗi để giải thích kết quả và thảo luận ý nghĩa của hệ thống. Phần Phụ lục cung cấp hướng dẫn tái lập, hướng dẫn gán nhãn quan hệ và các bảng dữ liệu chi tiết."),
);

// ===== CHƯƠNG 2. CƠ SỞ LÝ THUYẾT (mỗi công thức có đoạn giải thích ký hiệu) =====
add(
  H1("CHƯƠNG 2. CƠ SỞ LÝ THUYẾT VÀ NGHIÊN CỨU LIÊN QUAN"),
  SUM("Chương này trình bày các khái niệm nền tảng được sử dụng ở các chương sau: gán nhãn BIO, Transformer, RE bằng đánh dấu thực thể, chuẩn hóa mã, TF-IDF kết hợp Logistic Regression, fuzzy matching và các phép thống kê đánh giá. Đáng chú ý, token_set_ratio đạt điểm tối đa khi tập từ của chuỗi này là tập con của chuỗi kia, dẫn đến các lỗi gán mã ICD-10 phân tích ở mục 4.6.2."),
  P("Hình 2.1 minh họa mối liên hệ giữa ba bài toán trên câu ví dụ ở mục 1.1: NER xác định thực thể, chuẩn hóa gán mã cho thực thể, còn RE nối các thực thể thành quan hệ. Vì đầu ra của bước trước là đầu vào của bước sau, lỗi NER có thể ảnh hưởng đến cả chuỗi; do đó, khóa luận đánh giá riêng từng bước và toàn bộ quy trình."),
  ...FIG("h1_1_luong_ba_buoc_bio.png", "Hình 2.1. Ví dụ ba bước NER, chuẩn hóa mã, RE để trở thành bản ghi có cấu trúc", "Hình cho thấy đầu ra của mỗi bước là đầu vào của bước kế tiếp, và mỗi quan hệ là một bộ ba gồm thực thể đầu, tên quan hệ và thực thể đuôi.", 500),
  H2("2.1. Nhận diện thực thể có tên"),
  H3("2.1.1. Định nghĩa bài toán"),
  P("Cho một câu gồm các từ w₁, w₂, …, wₙ, bài toán NER tìm các đoạn từ liên tiếp, gọi là span, cùng với loại thực thể của mỗi đoạn. Cách phổ biến là đưa bài toán về gán nhãn chuỗi theo lược đồ BIO [1], trong đó mỗi từ nhận một nhãn cho biết nó bắt đầu một thực thể loại X với nhãn B-X, nằm bên trong thực thể đó với nhãn I-X, hoặc nằm ngoài mọi thực thể với nhãn O. Như vậy, với K loại thực thể, lược đồ BIO có 2K + 1 nhãn. VietMed-NER [2] có 18 loại thực thể nên mô hình phải phân loại 37 nhãn BIO. Bước 1 trong Hình 2.1 minh họa cách gán nhãn này trên câu ví dụ theo sáu loại thực thể mục tiêu của khóa luận, từ nhãn của từng từ cho tới các thực thể thu được sau khi giải mã."),
  P("Khi giải mã chuỗi nhãn BIO thành span, hệ thống phải xử lý các chuỗi không hợp lệ, chẳng hạn một nhãn I-X đứng ngay sau O hoặc sau một nhãn B-Y khác loại. Cách thường dùng là coi nhãn I-X đó như điểm bắt đầu của một thực thể mới. Kết quả giải mã lúc này mới chỉ cho biết mỗi thực thể gồm những từ nào trong câu, chẳng hạn “dạ dày” ở Hình 2.1 gồm từ thứ tư và từ thứ năm. Vì các bước sau đều làm việc trên văn bản gốc, hệ thống đổi chỉ số từ này sang vị trí ký tự bắt đầu và kết thúc, ở ví dụ trên là đoạn ký tự từ vị trí 14 đến 20. Nhờ đó, các bước chuẩn hóa, RE và giao diện đều dùng chung một hệ tọa độ."),
  H3("2.1.2. Các hướng tiếp cận"),
  P("Các hướng tiếp cận NER phát triển qua bốn giai đoạn. Các hệ thống đầu tiên dùng quy tắc viết tay và từ điển, dễ giải thích nhưng không theo kịp sự đa dạng của ngôn ngữ, ví dụ một từ điển có “tăng huyết áp” sẽ bỏ sót “huyết áp cao”. Giai đoạn thứ hai dùng học máy thống kê, tiêu biểu là CRF [3]. Mô hình này học xác suất của cả chuỗi nhãn từ các đặc trưng do người thiết kế, ví dụ từ có viết hoa hay không, có nằm trong từ điển hay không, và nhờ học cả bước chuyển giữa hai nhãn liền kề nên hiếm khi sinh ra chuỗi BIO sai. Giai đoạn thứ ba thay đặc trưng thủ công bằng biểu diễn do mạng nơ-ron tự học, tiêu biểu là BiLSTM-CRF [4]."),
  P("Ở giai đoạn hiện nay, cách làm phổ biến nhất là tinh chỉnh một mô hình Transformer đã được huấn luyện trước trên lượng văn bản lớn, ví dụ BERT [5], bằng cách đặt thêm một lớp phân loại lên biểu diễn của từng token. Khóa luận đi theo hướng này."),
  H3("2.1.3. Đặc thù tiếng Việt trong lĩnh vực y tế"),
  P("Tiếng Việt được viết theo âm tiết, và một từ có thể gồm nhiều âm tiết như “dạ dày” hay “đái tháo đường”. Do đó mô hình hoặc làm việc trực tiếp ở mức âm tiết, hoặc cần thêm một bước tách từ. Phiên bản mức âm tiết của ViHealthBERT [6] làm việc trực tiếp trên âm tiết, nên hệ thống chỉ cần tách theo khoảng trắng và dấu câu. Bên cạnh đó, văn bản trong lĩnh vực y tế còn có nhiều khó khăn riêng, như tên thuốc và hoạt chất mượn tiếng nước ngoài, từ viết tắt và các cụm bệnh dài lồng tên bộ phận cơ thể như “viêm loét dạ dày tá tràng”. Với văn bản chép lời nói, hệ thống còn phải đối mặt với lỗi phiên âm và câu bị cắt giữa chừng."),
  H3("2.1.4. Đánh giá NER"),
  P("Chất lượng NER được đo ở mức thực thể theo hai cách. Strict match chỉ tính một dự đoán là đúng khi nó trùng cả loại lẫn vị trí bắt đầu và kết thúc với thực thể gold. Relaxed match dễ hơn, chấp nhận mọi dự đoán cùng loại có span giao với span gold, với điều kiện mỗi thực thể gold chỉ được ghép tối đa một lần. Từ kết quả ghép, ba đại lượng precision, recall và F1 được tính theo các công thức (2.1), (2.2) và (2.3)."),
  EQ("P = TP / (TP + FP)", 1),
  EQ("R = TP / (TP + FN)", 2),
  EQ("F1 = 2 · P · R / (P + R)", 3),
  PN("Trong đó:", { p: { keepNext: true } }),
  WH("P là precision, tức tỉ lệ dự đoán đúng trong số các thực thể mà hệ thống đưa ra."),
  WH("R là recall, tức tỉ lệ thực thể chuẩn mà hệ thống tìm lại được."),
  WH("F1 là trung bình điều hòa của P và R, chỉ cao khi cả P lẫn R cùng cao."),
  WH("TP là số thực thể dự đoán đúng, FP là số dự đoán thừa, FN là số thực thể chuẩn bị bỏ sót.", true),
  P("Khi có nhiều loại thực thể, khóa luận dùng micro-F1, tức cộng dồn TP, FP và FN của mọi loại rồi mới tính, và chấm bằng thư viện seqeval theo cách chấm mức thực thể của CoNLL-2003 [7]."),
  H2("2.2. Mô hình ngôn ngữ pre-train"),
  H3("2.2.1. Kiến trúc Transformer và cơ chế self-attention"),
  P("Encoder Transformer [8] gồm nhiều lớp giống nhau xếp chồng, trong đó mỗi lớp có một khối multi-head self-attention và một mạng truyền thẳng. Khối self-attention cho phép mỗi vị trí trong câu nhìn vào mọi vị trí còn lại, và được tính theo công thức (2.4)."),
  EQ("Attention(Q, K, V) = softmax(Q · Kᵀ / √dₖ) · V", 4),
  PN("Trong đó:", { p: { keepNext: true } }),
  WH("Q là ma trận query, mỗi hàng là vector truy vấn của một vị trí trong câu."),
  WH("K là ma trận key và Kᵀ là ma trận chuyển vị của K."),
  WH("V là ma trận value, chứa thông tin sẽ được tổng hợp."),
  WH("dₖ là số chiều của mỗi vector key."),
  WH("softmax là hàm đưa một dãy điểm số về các xác suất có tổng bằng 1.", true),
  P("Cả ba ma trận Q, K và V đều được tính từ biểu diễn đầu vào qua các phép nhân ma trận học được. Tích Q · Kᵀ cho điểm tương đồng giữa vector truy vấn của mỗi vị trí với vector khóa của mọi vị trí khác, phép chia cho √dₖ giữ các điểm này không quá lớn khi số chiều tăng, và softmax đổi điểm thành trọng số. Nhờ vậy, mỗi vị trí nhận về tổng có trọng số của các vector giá trị, tức là gom thông tin từ cả câu, phần nào liên quan nhiều thì được lấy nhiều."),
  P("Nhiều head attention chạy song song cho phép mô hình học cùng lúc nhiều kiểu quan hệ ngữ cảnh khác nhau. Do phép attention bản thân không phân biệt thứ tự từ, mô hình cộng thêm một position embedding cho mỗi vị trí, và số vị trí tối đa này cũng chính là giới hạn độ dài đầu vào của mô hình."),
  H3("2.2.2. BERT, PhoBERT và ViHealthBERT"),
  P("BERT [5] pre-train encoder Transformer trên lượng văn bản lớn bằng nhiệm vụ masked language model, tức là che ngẫu nhiên một phần token và yêu cầu mô hình đoán lại. RoBERTa [9] giữ nguyên kiến trúc nhưng cải tiến quy trình pre-train, bỏ nhiệm vụ dự đoán câu tiếp theo và dùng nhiều dữ liệu, nhiều thời gian huấn luyện hơn. Dựa trên cách làm này, PhoBERT [10] là mô hình kiểu RoBERTa dành cho tiếng Việt, và ViHealthBERT tiếp tục pre-train PhoBERT trên văn bản y tế tiếng Việt."),
  P("Các mô hình này không làm việc trực tiếp trên từ mà trên subword do bộ tách Byte-Pair Encoding tạo ra, nên một âm tiết hiếm có thể bị tách thành nhiều subword. Khi fine-tune cho NER, nhãn của mỗi từ được gắn vào subword đầu tiên của nó, và khi suy luận, nhãn của từ cũng được lấy theo subword đầu tiên. Hai token đặc biệt <s> và </s> được thêm vào đầu và cuối chuỗi, và dự đoán tại hai vị trí này phải bị loại trước khi giải mã BIO. Hình 2.2 minh họa kiến trúc này khi được dùng cho bài toán gán nhãn chuỗi."),
  ...FIG("h1_3_kien_truc_vihealthbert.png", "Hình 2.2. Kiến trúc ViHealthBERT kèm lớp phân loại tuyến tính", "Hình cho thấy một subword đi qua bộ mã hóa và lớp phân loại để thành phân bố xác suất trên 37 nhãn BIO, với xác suất do chính mô hình của hệ thống tính ra.", 566),
  P("Để tinh chỉnh cho gán nhãn chuỗi, một lớp tuyến tính được đặt lên biểu diễn của từng subword, theo sau là hàm softmax. Ma trận trọng số W của lớp này có kích thước 768 × 37, trong đó 768 là kích thước vector biểu diễn theo kiến trúc BERT-base, còn 37 là số nhãn BIO tính theo công thức 2K + 1 ở mục 2.1.1 với K bằng 18 loại thực thể của VietMed-NER. Với subword thứ i, bộ mã hóa biến embedding eᵢ thành vector hᵢ, lớp phân loại tính zᵢ = Wᵀhᵢ + b, rồi hàm softmax biến zᵢ thành phân bố xác suất pᵢ trên 37 nhãn. Nhãn dự đoán là nhãn có xác suất lớn nhất, còn khi huấn luyện, hàm mất mát cross-entropy −log pᵢ[yᵢ] được tối ưu bằng AdamW trên toàn bộ tham số của bộ mã hóa và lớp phân loại."),
  H2("2.3. Trích xuất quan hệ"),
  H3("2.3.1. Định nghĩa"),
  P("Cho một văn bản X cùng hai thực thể trong X là thực thể đầu eₕ và thực thể đuôi eₜ, bài toán RE dự đoán một nhãn r thuộc R ∪ {NO_RELATION}, trong đó R là tập năm quan hệ của đề tài ở Bảng 2.1 và NO_RELATION là nhãn của cặp không có quan hệ. Vì mỗi kiểu cặp thực thể chỉ ứng với đúng một quan hệ, bài toán thực chất là phân loại nhị phân, tức chỉ cần quyết định cặp đó có quan hệ tương ứng hay không."),
  ...TB("Bảng 2.1. Năm quan hệ mục tiêu cùng kiểu thực thể, ý nghĩa và ví dụ", T(["Quan hệ", "Kiểu thực thể đầu và đuôi", "Ý nghĩa", "Ví dụ"], [
    ["located_at", "CONDITION, BODY_PART", "Tình trạng xuất hiện ở bộ phận cơ thể", "“khối u ở gan”"],
    ["treated_by", "CONDITION, DRUG", "Thuốc được nêu để điều trị tình trạng", "“đau đầu dùng Paracetamol”"],
    ["treated_by_procedure", "CONDITION, PROCEDURE", "Thủ thuật được nêu để điều trị tình trạng", "“hẹp động mạch vành được đặt stent”"],
    ["diagnosed_by", "CONDITION, TEST", "Xét nghiệm hoặc phương pháp xác định tình trạng", "“viêm phổi phát hiện qua chụp X-quang”"],
    ["has_dosage", "DRUG, DOSAGE", "Liều thuộc về thuốc", "“Paracetamol 500 mg”"],
  ], [2700, 2300, 2500, 2138]), "Bảng xác định kiểu thực thể và chiều của từng quan hệ trong lược đồ."),
  H3("2.3.2. Các hướng tiếp cận"),
  P("Cách đơn giản nhất là rule-based, dùng từ gợi ý và khoảng cách giữa hai thực thể, ví dụ mẫu “X được điều trị bằng Y”. Phương pháp rule-based dễ giải thích và không cần dữ liệu huấn luyện, nhưng bỏ sót nhiều cách diễn đạt. Hướng học máy cổ điển dùng đặc trưng thủ công như từ nằm giữa hai thực thể, loại thực thể, khoảng cách và đường đi cú pháp, rồi đưa vào một bộ phân loại tuyến tính hoặc SVM. Sau đó, các mạng nơ-ron CNN và RNN thay đặc trưng thủ công bằng biểu diễn học được trên chuỗi có đánh dấu vị trí tương đối so với hai thực thể."),
  P("Hướng hiện đại nhất dùng encoder pre-train và chèn entity marker quanh head và tail, tức là đặt các token đặc biệt như [E1] và [/E1] ngay trước và sau mỗi thực thể để mô hình biết cặp nào đang được xét. Nghiên cứu Matching the Blanks [11] cho thấy lấy biểu diễn tại marker mở đầu của mỗi thực thể là một lựa chọn tốt. Tiếp nối hướng này, PURE [12] dùng ký hiệu đánh dấu có kèm loại thực thể, trong một pipeline chạy NER trước rồi mới tới RE, và đạt kết quả mạnh trên hai bộ dữ liệu ACE và SciERC. Các mô hình joint học NER và RE cùng lúc để giảm lan truyền lỗi, nhưng phức tạp hơn và cần nhiều dữ liệu hơn. Với lượng dữ liệu nhỏ như của đề tài, pipeline tách rời là lựa chọn thực tế hơn, vì NER có thể kế thừa từ mô hình sẵn có còn RE được đánh giá riêng trên thực thể gold."),
  H3("2.3.3. Trích xuất quan hệ lâm sàng"),
  P("Hai thử thách quốc tế là căn cứ chính để đề tài chọn các quan hệ. Thử thách i2b2/VA 2010 [13] chia khái niệm lâm sàng thành ba nhóm là vấn đề sức khỏe, điều trị và xét nghiệm, rồi định nghĩa các quan hệ giữa chúng. Hình 2.3 đối chiếu các quan hệ đó với quan hệ của đề tài. Quan hệ treated_by và diagnosed_by của đề tài tương ứng với hai nhánh điều trị dùng cho vấn đề và xét nghiệm phát hiện vấn đề, nhưng được gộp lại cho đơn giản. Track 2 của thử thách n2c2 2018 [14] nối thuốc với các thuộc tính như liều, tần suất và đường dùng, và quan hệ has_dosage của đề tài ứng với phần liều trong nhóm này."),
  P(`Cả hai thử thách còn cho thấy một điều mà khóa luận cũng gặp lại ở Chương 4. Tại n2c2 2018, hệ thống tốt nhất đạt micro-F1 0,9630 khi được cho sẵn thực thể đúng, nhưng chỉ còn 0,8905 khi phải tự nhận diện thực thể trước rồi mới tìm quan hệ. Nói cách khác, chất lượng RE trên toàn chuỗi luôn bị giới hạn bởi chất lượng NER.`),
  P(`Các con số của n2c2 2018 cao hơn nhiều so với kết quả RE của khóa luận ở Chương 4, nhưng hai bên không so sánh trực tiếp được vì ba lý do. Thứ nhất, n2c2 2018 có 505 bản tóm tắt ra viện với 59.810 quan hệ, trong đó 36.384 quan hệ dùng để huấn luyện [14], còn dữ liệu huấn luyện thật của RE trong khóa luận chỉ có ${RX_REL.reduce((a, k) => a + (RX.rev[`seed:${k}:pos`] || 0), 0)} cặp dương. Thứ hai, sáu trong tám quan hệ của n2c2 2018 nối thuốc với các thuộc tính thường đứng ngay cạnh tên thuốc, trong khi các quan hệ của khóa luận được diễn đạt đa dạng hơn [14]. Thứ ba, n2c2 dùng bệnh án tiếng Anh được viết theo khuôn mẫu, còn VietMed-NER là lời nói được chép lại, có câu bị cắt và lỗi phiên âm. Vì vậy, con số của n2c2 chỉ nên được xem là mức tham khảo cho một bài toán có nhiều dữ liệu hơn. Dù vậy, hai thử thách này vẫn hữu ích cho khóa luận ở hai điểm. Lược đồ quan hệ của chúng cho thấy những kiểu quan hệ thường được quan tâm trong văn bản lâm sàng, từ đó làm căn cứ để chọn năm quan hệ của đề tài, còn cách chúng tách đánh giá trên thực thể đúng khỏi đánh giá đầu cuối gợi ý cho khóa luận cách trình bày kết quả.`),
  ...FIG("h1_4_luoc_do_quan_he.png", "Hình 2.3. Lược đồ quan hệ của thử thách i2b2/VA 2010 và lược đồ quan hệ của đề tài", "Hình cho thấy đề tài kế thừa và điều chỉnh các quan hệ của i2b2/VA, đồng thời bổ sung has_dosage và located_at.", 566, "Nguồn: lược đồ i2b2/VA 2010 tổng hợp từ [13], lược đồ của đề tài do tác giả đề xuất."),
  H3("2.3.4. Mất cân bằng lớp và đánh giá RE"),
  P("Số cặp candidate tăng theo bình phương số thực thể trong khi số cặp thực sự có quan hệ lại ít, vì vậy dữ liệu RE thường mất cân bằng mạnh. Các cách xử lý phổ biến là dùng class weight, lấy mẫu lại các cặp âm và giới hạn cặp candidate theo kiểu thực thể. Chỉ số chính của bài toán là micro-F1 tính trên các nhãn dương, trong đó một dự đoán dương trên cặp có nhãn gold NO_RELATION được tính là FP. Khi đánh giá end-to-end, một cạnh chỉ được tính đúng khi cả hai thực thể đầu mút khớp chính xác về span và loại, đồng thời nhãn quan hệ cũng đúng. Ngược lại, nếu NER bỏ sót một đầu mút thì cạnh gold tương ứng bị tính là FN."),
  H2("2.4. Chuẩn hóa thực thể"),
  H3("2.4.1. Bài toán"),
  P("Chuẩn hóa thực thể, còn gọi là entity normalization hay entity linking, gán cho mỗi mention, tức mỗi lần một thực thể xuất hiện trong văn bản, một khái niệm trong ontology, ví dụ đưa “cao huyết áp” về mã I10. Khó khăn chính nằm ở khoảng cách giữa cách nói thường ngày và tên chuẩn, ở sự nhập nhằng khi “nhồi máu” có thể là nhồi máu cơ tim, nhồi máu não hay nhồi máu lách, và ở mức độ chi tiết khác nhau của mã. Các cách tiếp cận gồm exact match với từ điển, so khớp qua alias và luật biến đổi, fuzzy matching theo độ tương tự chuỗi, và mô hình học biểu diễn để so sánh mention với tên khái niệm. Khóa luận dùng ba cách đầu theo một thứ tự ưu tiên rõ ràng."),
  H3("2.4.2. ICD-10"),
  P("ICD-10 tổ chức mã theo ba cấp. Cấp đầu là chương, được xác định bởi chữ cái đầu tiên. Cấp thứ hai là nhóm ba ký tự, ví dụ “I10” cho bệnh tăng huyết áp và “I21” cho nhồi máu cơ tim cấp. Cấp cuối là phân nhóm bốn ký tự với một chữ số sau dấu chấm, ví dụ “M54.5” cho đau cột sống thắt lưng. Khóa luận dùng danh mục ICD-10 tiếng Việt do Bộ Y tế ban hành [15]."),
  H3("2.4.3. RxNorm"),
  P("RxNorm là danh mục thuốc chuẩn của Thư viện Y khoa Quốc gia Hoa Kỳ [16], trong đó mỗi khái niệm như hoạt chất, thuốc lâm sàng hay thuốc biệt dược đều có một RxCUI. Dịch vụ RxNav [17] cung cấp API để tra mã RxCUI từ tên thuốc và lấy tên chuẩn tương ứng. Tuy nhiên, RxNorm chủ yếu chứa thuốc lưu hành tại Hoa Kỳ, nên tên thuốc tiếng Việt, thảo dược và thực phẩm chức năng thường không có mã."),
  H2("2.5. TF-IDF và Logistic Regression"),
  P("TF-IDF biểu diễn mỗi văn bản bằng một vector trọng số của các đặc trưng, có thể là từ hoặc n-gram ký tự. Trọng số của một đặc trưng tăng khi nó xuất hiện nhiều trong văn bản đang xét và giảm khi nó xuất hiện trong nhiều văn bản khác. Thư viện scikit-learn [18] tính trọng số này theo dạng làm trơn ở hai công thức (2.5) và (2.6)."),
  EQ("idf(t) = ln[(1 + N) / (1 + df(t))] + 1", 5),
  EQ("w(t, d) = [1 + ln tf(t, d)] · idf(t)", 6),
  PN("Trong đó:", { p: { keepNext: true } }),
  WH("t là một đặc trưng, d là một văn bản."),
  WH("N là tổng số văn bản trong tập huấn luyện."),
  WH("df(t) là số văn bản có chứa đặc trưng t."),
  WH("tf(t, d) là số lần đặc trưng t xuất hiện trong văn bản d."),
  WH("idf(t) là trọng số nghịch đảo tần suất văn bản của t, càng lớn khi t càng hiếm."),
  WH("w(t, d) là trọng số cuối cùng của đặc trưng t trong văn bản d.", true),
  P("Số 1 được cộng vào cả tử và mẫu của idf để tránh chia cho 0 khi một đặc trưng chưa từng xuất hiện, còn phép lấy logarit của tf, gọi là sublinear tf, làm giảm ảnh hưởng của các đặc trưng lặp lại quá nhiều lần. Như vậy, một đặc trưng có trọng số cao khi nó xuất hiện nhiều trong văn bản đang xét nhưng hiếm trong toàn bộ tập dữ liệu. Sau cùng, vector của mỗi văn bản được chuẩn hóa về độ dài 1 theo chuẩn L2."),
  P("N-gram ký tự có độ dài từ 2 đến 5 bền vững trước lỗi chính tả, biến thể dấu và từ ghép, nên phù hợp khi dữ liệu nhỏ. Trên vector này, Logistic Regression ước lượng xác suất của mỗi lớp bằng hàm softmax áp lên một tổ hợp tuyến tính của các đặc trưng, và được huấn luyện bằng cách cực tiểu hóa cross-entropy có thêm thành phần regularization L2. Tham số C điều khiển mức regularization, trong đó C càng nhỏ thì mô hình càng bị ép đơn giản. Để lớp ít mẫu không bị lấn át, khóa luận dùng class weight dạng balanced, gán cho mỗi lớp c một trọng số theo công thức (2.7)."),
  EQ("w_c = N / (K · N_c)", 7),
  PN("Trong đó:", { p: { keepNext: true } }),
  WH("w_c là trọng số của lớp c trong hàm loss."),
  WH("N là tổng số mẫu huấn luyện."),
  WH("K là số lớp."),
  WH("N_c là số mẫu thuộc lớp c.", true),
  P("Lớp càng ít mẫu thì trọng số càng lớn, nhờ đó mỗi lỗi trên lớp hiếm bị phạt nặng hơn trong quá trình huấn luyện. Khi số mẫu của các lớp bằng nhau, mọi trọng số đều bằng 1."),
  H2("2.6. Fuzzy matching"),
  P("Các độ đo tương tự chuỗi phổ biến được xây dựng dựa trên khoảng cách chỉnh sửa Levenshtein [19]. Độ đo ratio giữa hai chuỗi được chuẩn hóa về thang 0 đến 100, trong đó 100 nghĩa là hai chuỗi giống hệt nhau. Độ đo token_set_ratio phức tạp hơn. Trước hết, nó tách mỗi chuỗi thành tập từ, sau đó tìm phần giao giữa hai tập và phần riêng của từng chuỗi, rồi lấy giá trị ratio lớn nhất giữa phần giao với từng chuỗi đầy đủ. Hệ quả quan trọng là nếu tập từ của một chuỗi nằm trọn trong tập từ của chuỗi kia thì token_set_ratio luôn bằng 100, bất kể chuỗi dài hơn có thêm những từ nào. Đây chính là nguyên nhân của các lỗi gán mã được phân tích ở mục 4.6.2."),
  P("Để hạn chế hệ quả trên, khóa luận dùng thêm hệ số Jaccard [20] giữa hai tập từ làm ràng buộc phụ, được tính theo công thức (2.8)."),
  EQ("J(A, B) = |A ∩ B| / |A ∪ B|", 8),
  PN("Trong đó:", { p: { keepNext: true } }),
  WH("A và B là tập từ của hai chuỗi cần so sánh."),
  WH("|A ∩ B| là số từ chung của hai chuỗi."),
  WH("|A ∪ B| là tổng số từ khác nhau xuất hiện trong ít nhất một chuỗi."),
  WH("J(A, B) là hệ số Jaccard, nằm trong khoảng từ 0 đến 1.", true),
  P("Hệ số J bằng 1 khi hai chuỗi có cùng tập từ và giảm dần khi một chuỗi có thêm nhiều từ mà chuỗi kia không có. Vì vậy, khác với token_set_ratio, hệ số Jaccard phạt trường hợp chuỗi ngắn chỉ là một phần nhỏ của chuỗi dài."),
  H2("2.7. Thống kê đánh giá"),
  P("Khóa luận dùng ba công cụ thống kê để đánh giá kết quả một cách đáng tin cậy khi dữ liệu nhỏ. Công cụ thứ nhất là tách riêng tập kiểm định khỏi tập kiểm tra. Mọi lựa chọn như cấu hình dữ liệu, ngưỡng hay từ điển đều được đưa ra trên tập kiểm định, còn tập kiểm tra chỉ được chạy một lần sau khi mọi lựa chọn đã chốt, nếu không kết quả sẽ lạc quan một cách giả tạo. Khi nhiều mẫu có chung nguồn, chẳng hạn nhiều cặp thực thể trong cùng một câu, việc chia phải theo câu để các mẫu cùng câu không nằm ở cả hai phía."),
  P("Công cụ thứ hai là khoảng tin cậy bootstrap [21]. Từ tập đánh giá, khóa luận lấy mẫu lại có hoàn lại theo câu chứ không theo từng cặp, lặp lại B lần và mỗi lần tính lại F1. Khoảng tin cậy 95% khi đó là đoạn nằm giữa phân vị 2,5% và phân vị 97,5% của B giá trị F1 thu được. Phương pháp này không đòi hỏi giả định về phân phối, nên phản ánh đúng độ bất định của kết quả khi support nhỏ."),
  P("Công cụ thứ ba là hệ số Cohen’s kappa [22], dùng để đo độ đồng thuận giữa hai người gán nhãn sau khi đã loại phần đồng ý do ngẫu nhiên, theo công thức (2.9)."),
  EQ("κ = (pₒ − pₑ) / (1 − pₑ)", 9),
  PN("Trong đó:", { p: { keepNext: true } }),
  WH("κ là hệ số Cohen’s kappa."),
  WH("pₒ là tỉ lệ mẫu mà hai người gán cùng một nhãn."),
  WH("pₑ là tỉ lệ đồng ý kỳ vọng nếu cả hai người gán ngẫu nhiên theo phân phối nhãn của riêng mình.", true),
  P("Tử số đo phần đồng ý vượt trên mức ngẫu nhiên, còn mẫu số là phần vượt tối đa có thể đạt được. Do đó κ bằng 1 khi hai người đồng ý hoàn toàn, bằng 0 khi mức đồng ý chỉ ngang ngẫu nhiên và có thể âm khi họ đồng ý còn ít hơn ngẫu nhiên. Khóa luận dùng κ để đo độ đồng thuận giữa hai lượt gán nhãn của bộ dữ liệu quan hệ và giữa nhãn của người với nhãn của mô hình ngôn ngữ lớn."),
  H2("2.8. Nghiên cứu liên quan và benchmark tham khảo"),
  P("Bảng 2.2 tóm tắt các công trình và benchmark có liên quan trực tiếp tới đề tài, kèm vai trò của từng công trình đối với khóa luận."),
  P("Riêng với tiếng Việt, các công trình xử lý văn bản y tế hiện tập trung chủ yếu vào nhận diện thực thể. PhoNER_COVID19 [23] gán nhãn thực thể cho tin tức về dịch COVID-19, ViMedNER [30] xây dựng dữ liệu thực thể y khoa từ văn bản tiếng Việt, ViMQ [29] gán nhãn ý định và thực thể cho câu hỏi của người bệnh, còn ViHealthBERT [6] cung cấp mô hình tiền huấn luyện trên văn bản y tế. Các công trình này tạo nền tảng tốt cho bước NER, nhưng chưa có công trình nào xây dựng dữ liệu quan hệ giữa các thực thể y tế hay chuẩn hóa thực thể sang danh mục mã chuẩn cho tiếng Việt. Đây chính là khoảng trống mà khóa luận hướng tới."),
  P("So với các công trình trên, khóa luận có ba điểm khác biệt. Thứ nhất, dữ liệu là lời nói y tế tiếng Việt chứ không phải bệnh án viết. Thứ hai, dữ liệu quan hệ được khóa luận tự xây dựng theo một hướng dẫn gán nhãn riêng. Thứ ba, trọng tâm của khóa luận là một luồng xử lý hoàn chỉnh từ văn bản tới đồ thị tri thức cùng quy trình đánh giá chặt chẽ, thay vì tối đa hóa điểm số trên một bộ đánh giá chuẩn có sẵn. Từ các điểm khác biệt này, khóa luận chọn hướng tiếp cận kết hợp mô hình tiền huấn luyện với quy tắc chuyên biệt, đồng thời tự xây dựng dữ liệu quan hệ và quy trình đánh giá phù hợp với dữ liệu nhỏ."),
  ...TB("Bảng 2.2. Các công trình liên quan và vai trò của chúng đối với khóa luận", T(["Công trình hoặc benchmark", "Thiết lập", "Kết quả công bố", "Vai trò trong khóa luận"], [
    ["VietMed-NER [2], NAACL 2025 Industry", "NER trên lời nói y tế tiếng Việt, 18 loại thực thể", "Không áp dụng", "Nguồn dữ liệu chính"],
    ["ViHealthBERT [6], LREC 2022", "Encoder y tế tiếng Việt", "Không áp dụng", "Mô hình nền cho NER và RE"],
    ["PhoBERT [10], Findings EMNLP 2020", "Encoder kiểu RoBERTa cho tiếng Việt", "Không áp dụng", "Nền tảng của ViHealthBERT"],
    ["PhoNER_COVID19 [23], NAACL 2021", "NER tiếng Việt miền COVID-19", "Không áp dụng", "NER y tế trên văn bản viết"],
    ["PURE [12], NAACL 2021, ACE05", "Pipeline với typed marker", "Strict F1 quan hệ 63,9%", "Cơ sở thiết kế RE"],
    ["i2b2/VA 2010 [13]", "RE trên khái niệm gold", "F1 tốt nhất 0,737", "Quan hệ problem với treatment và test"],
    ["n2c2 2018 [14], Track 2", "Thuốc và thuộc tính, trên khái niệm gold và end-to-end", "Micro-F1 lenient 0,9630 và 0,8905", "Tách đánh giá RE độc lập với toàn pipeline"],
  ], [2700, 2700, 2000, 2238]), "Bảng dùng để định vị khóa luận so với các công trình trước, lưu ý rằng các kết quả thuộc corpus, ngôn ngữ và cách chấm khác nhau nên không so sánh trực tiếp được.", "Nguồn: tác giả tổng hợp từ các tài liệu được trích dẫn trong bảng."),
  P("Tóm lại, các khái niệm trong chương này là nền tảng trực tiếp cho thiết kế ở Chương 3. Lược đồ BIO và cách giải mã thành span được dùng ở bước suy luận NER, còn kiến trúc Transformer của ViHealthBERT là bộ mã hóa chung cho cả NER lẫn RE. Cách đánh dấu thực thể đầu và thực thể đuôi là cơ sở của mô hình RE, trong khi TF-IDF được dùng để xếp hạng ứng viên mã ICD-10. Tính chất của token_set_ratio và hệ số Jaccard giải thích các ràng buộc an toàn của bước gán mã, và các công cụ thống kê như khoảng tin cậy bootstrap và hệ số kappa được dùng xuyên suốt phần đánh giá ở Chương 4. Nhờ đó, mỗi lựa chọn thiết kế ở chương sau đều có căn cứ lý thuyết rõ ràng."),
);

// ===== CHƯƠNG 2 (viết lại 12/11/2026) =====
const mapRows = [
  ["CONDITION", "DISEASESYMTOM"], ["DRUG", "DRUGCHEMICAL, PREVENTIVEMED"], ["BODY_PART", "ORGAN"],
  ["TEST", "DIAGNOSTICS"], ["PROCEDURE", "SURGERY, MEDDEVICETECHNIQUE, TREATMENT"], ["DOSAGE", "UNITCALIBRATOR"],
  ["Bị loại bỏ", "AGE, GENDER, DATETIME, OCCUPATION, LOCATION, ORGANIZATION, FOODDRINK, PERSONALCARE, TRANSPORTATION"],
];
const changeText = (c) => c.op === "relabel" ? `nhãn của cặp ${c.relation} được sửa từ ${c.before} thành ${c.after}` : c.op === "delete_entity" ? `thực thể ${c.entity} “${c.text}” bị xóa` : `cặp ${c.relation} bị xóa`;
const exampleTable = (ex) => [
  PN(`Mẫu ${ex.id}: “${ex.text}”`),
  T(["ID", "Loại", "Văn bản", "Vị trí ký tự"], ex.entities.map((e) => [e[0], e[1], e[2], `${e[3]} đến ${e[4]}`]), [800, 1800, 4800, 2238], { size: 20 }),
  ...(ex.relations.length ? [T(["Cặp", "Head", "Tail", "Nhãn gold v1"], ex.relations.map((x) => [x[0], x[1], x[2], x[3]]), [800, 3200, 2800, 2838], { size: 20 })] : []),
  ...(ex.changes.length ? [PN(`Khi duyệt, ${ex.changes.map(changeText).join(" và ")}.`, { run: { size: 22, italics: true } })] : []),
];
const nForms = (sp) => normMan.splits[sp].CONDITION.unique_forms + normMan.splits[sp].DRUG.unique_forms;
add(
  H1("CHƯƠNG 3. PHƯƠNG PHÁP NGHIÊN CỨU VÀ THIẾT KẾ HỆ THỐNG"),
  SUM("Chương này trình bày cách khóa luận được thực hiện. Mục 3.1 nêu phương pháp nghiên cứu, công cụ, giao thức đánh giá và lý do chọn từng chỉ số. Mục 3.2 tóm tắt quy trình thực hiện qua bốn giai đoạn. Mục 3.3 mô tả các bộ dữ liệu dùng để huấn luyện và đánh giá cùng độ tin cậy của từng nguồn nhãn, còn mục 3.4 trình bày kiến trúc và cách cài đặt từng bước xử lý của hệ thống."),
  H2("3.1. Phương pháp và công cụ nghiên cứu"),
  P("Khóa luận sử dụng phương pháp nghiên cứu thực nghiệm. Mỗi thành phần của hệ thống được xây dựng rồi so sánh với ít nhất một baseline trên cùng dữ liệu và cùng chỉ số, kết quả được kèm khoảng tin cậy để biết chênh lệch có đủ lớn so với dao động do mẫu nhỏ hay không, và mọi con số tổng hợp đều đi cùng phân tích định tính trên từng trường hợp lỗi cụ thể. Mục này trình bày môi trường và công cụ thực nghiệm, sau đó nêu dữ liệu đánh giá, chỉ số chính và lý do chọn chỉ số cho từng thành phần."),
  P(`Toàn bộ suy luận và đánh giá được chạy trên CPU của máy tính cá nhân dùng Windows 11, với Python ${reGoldRun.metadata.python}, PyTorch 2.14, Transformers [24] và scikit-learn ${reGoldRun.metadata.sklearn}. Riêng mô hình ViHealthBERT cho RE được huấn luyện trên GPU NVIDIA GeForce GTX 1650 có 4 GB bộ nhớ. Bảng 3.1 tóm tắt dữ liệu và chỉ số dùng cho từng thành phần, và đây cũng là khung để đọc các kết quả ở Chương 4.`),
  P("Mỗi chỉ số trong Bảng 3.1 được chọn theo đúng câu hỏi mà thành phần đó cần trả lời. Với NER, khóa luận đo F1 ở mức thực thể thay vì độ chính xác ở mức token, vì phần lớn token mang nhãn O, nên một mô hình chỉ đoán O vẫn đạt độ chính xác token rất cao mà không tìm được thực thể nào. F1 kết hợp precision và recall, nhờ đó phản ánh cả lỗi đưa ra thực thể thừa lẫn lỗi bỏ sót. Khớp chặt là thước đo chính vì bước chuẩn hóa và bước RE dùng đúng vị trí ký tự của thực thể, còn khớp nới lỏng được báo cáo kèm để tách lỗi sai ranh giới khỏi lỗi sai hoàn toàn. Các loại được gộp theo micro-F1 vì mục tiêu là chất lượng trên toàn bộ thực thể hệ thống gặp phải, trong đó loại xuất hiện nhiều cần có trọng số lớn hơn loại hiếm."),
  P("Với chuẩn hóa mã, độ chính xác được tính trên mọi dạng, kể cả dạng không có mã đúng trong danh mục, và ở những dạng này hệ thống chỉ được tính đúng khi từ chối gán mã. Do chế độ strict được phép không trả lời, khóa luận báo cáo thêm precision khi trả lời để cho biết mức tin cậy của những mã mà hệ thống thực sự đưa ra. Top-k và MRR đo một cách dùng khác, khi hệ thống gợi ý danh sách để người nhập liệu chọn. Top-k là tỉ lệ mã đúng nằm trong k ứng viên đầu, được báo cáo với k bằng 1, 3, 5 và 10 để thấy lợi ích tăng thêm khi danh sách dài ra, còn MRR tính trên mười ứng viên đầu và cho điểm cao hơn khi mã đúng đứng gần đầu danh sách."),
  ...TB("Bảng 3.1. Dữ liệu và chỉ số đánh giá của từng thành phần", T(["Thành phần", "Dữ liệu đánh giá", "Chỉ số chính"], [
    ["NER", `Tập test VietMed-NER gồm ${n(nerNew.lat.total_samples)} câu, chấm trên ${nTypes} loại gốc và sáu loại mục tiêu`, "Precision, recall và F1 theo strict match và relaxed match"],
    ["Baseline NER và ablation", "Học trên train, chọn trên validation và chấm test một lần", "Micro-F1 kèm khoảng tin cậy 95%"],
    ["Chuẩn hóa ICD-10 và RxNorm", `Tập gold chuẩn hóa gồm ${normMan.splits.dev.CONDITION.unique_forms + normMan.splits.dev.DRUG.unique_forms} dạng ở dev và ${normMan.splits.test.CONDITION.unique_forms + normMan.splits.test.DRUG.unique_forms} dạng ở test`, "Accuracy, Top-k, MRR và tỉ lệ từ chối đúng"],
    ["RE", `Tập kiểm định ${RX.sel.dev.sentences} câu để chọn cấu hình, tập kiểm tra ${RX.test.length} câu với ${rxPairs} cặp lấy từ split test`, "Micro-F1 trên các nhãn dương và F1 theo từng quan hệ, kèm khoảng tin cậy 95%"],
    ["Knowledge graph", `${n(kgS.documents)} câu của split test`, "Số nút, số cạnh và nguồn sinh ra cạnh"],
  ], [2300, 4000, 3338], { size: 20 }), "Bảng giúp người đọc biết mỗi kết quả trong Chương 4 được đo trên tập dữ liệu nào và bằng chỉ số gì."),
  P(`Với RE, chỉ số chính là micro-F1 trên các nhãn dương, tức không tính nhãn NO_RELATION. Cặp âm chiếm ${pct(1 - RX.syn.seed_positive_rate)} dữ liệu huấn luyện và ${pct(1 - rxPos / rxPairs)} tập kiểm tra, nên độ chính xác hoặc F1 có tính cả lớp âm vẫn cao ngay cả khi mô hình không tìm được quan hệ nào. Vì số cặp dương nhỏ, mọi F1 đều đi kèm khoảng tin cậy 95% tính bằng bootstrap theo câu, và khóa luận chỉ kết luận một phương pháp tốt hơn phương pháp khác khi khoảng tin cậy của chênh lệch không chứa 0. Để chọn cấu hình, khóa luận dùng macro-F1 trên tập kiểm định nhằm tránh để located_at át các quan hệ hiếm. Cuối cùng, độ đồng thuận gán nhãn được đo bằng Cohen’s kappa thay vì tỉ lệ đồng ý thô, vì khi phần lớn cặp cùng mang một nhãn thì hai người gán ngẫu nhiên cũng đồng ý ở tỉ lệ rất cao.`),
  H2("3.2. Quy trình thực hiện"),
  P("Khóa luận được thực hiện qua bốn giai đoạn nối tiếp nhau. Giai đoạn đầu tiên là chuẩn bị dữ liệu. Nhãn của VietMed-NER được ánh xạ sang sáu loại thực thể mục tiêu, dữ liệu quan hệ được xây dựng lại theo hướng dẫn hai bước với tập huấn luyện, tập kiểm định, tập kiểm tra và dữ liệu sinh, sau đó khóa luận xây tập đánh giá chuẩn hóa. Toàn bộ giai đoạn này được trình bày ở mục 3.3."),
  P("Giai đoạn thứ hai là thiết kế và cài đặt luồng xử lý theo thứ tự tiền xử lý, NER, quy tắc liều lượng, hậu xử lý, chuẩn hóa mã, RE và đồ thị tri thức, như trình bày ở mục 3.4. Giai đoạn thứ ba là đánh giá từng thành phần và cả luồng xử lý theo giao thức ở mục 3.1, trong đó tham số được chọn trên train hoặc dev, còn kết quả báo cáo được đo trên các tập test. Giai đoạn cuối cùng là phân tích lỗi. Những lỗi có tính hệ thống được đưa ngược lại giai đoạn thiết kế dưới dạng quy tắc tổng quát, chẳng hạn bản sửa bước fuzzy matching ICD-10 ở mục 4.6.2."),
  H2("3.3. Dữ liệu"),
  P("Mục này mô tả các bộ dữ liệu mà khóa luận sử dụng để huấn luyện và đánh giá. Tất cả đều bắt nguồn từ bộ VietMed-NER, nhưng khác nhau về nguồn nhãn, mục đích và độ tin cậy. Kết luận chính của mục là dữ liệu đủ để đánh giá NER và chuẩn hóa mã, nhưng dữ liệu quan hệ còn quá thưa để kết luận chắc chắn về RE, và nguyên nhân nằm ở bản chất của lời nói y tế chứ không phải ở quy trình gán nhãn. Hình 3.1 cho thấy các bộ dữ liệu được tạo ra từ ba split của VietMed-NER như thế nào và mỗi bộ dùng vào việc gì."),
  P("Điểm quan trọng nhất trong Hình 3.1 là sự tách biệt giữa các split. Dữ liệu huấn luyện và kiểm định của RE lấy từ split train và validation, dữ liệu dùng để chọn tham số cho bước gán mã lấy từ split validation, còn mọi tập dùng để báo cáo kết quả đều lấy từ split test. Nhờ đó, không có câu nào vừa được dùng để học vừa được dùng để chấm điểm."),
  H3("3.3.1. VietMed-NER"),
  H4("3.3.1.1. Mô tả"),
  P(`VietMed-NER là bộ dữ liệu NER trên bản chép lời của lời nói y tế tiếng Việt, được công bố trên Hugging Face. Dữ liệu được gán ${nTypes} loại thực thể theo lược đồ BIO với 37 nhãn. Các loại này gồm hai nhóm. Nhóm y khoa có bệnh và triệu chứng, thuốc và hóa chất, cơ quan, chẩn đoán, phẫu thuật, thiết bị và kỹ thuật, điều trị, đơn vị đo, y học dự phòng và chăm sóc cá nhân. Nhóm phi y khoa có tuổi, giới tính, thời gian, nghề nghiệp, địa điểm, tổ chức, thực phẩm và phương tiện. Bảng 3.2 trình bày kích thước của ba split và vai trò của từng split trong khóa luận.`),
  ...FIG("h2_1_cac_tap_du_lieu.png", "Hình 3.1. Nguồn gốc và mục đích sử dụng của các bộ dữ liệu trong khóa luận, phân biệt theo nguồn nhãn", "Hình giúp người đọc theo dõi nguồn, người gán nhãn và mục đích sử dụng của từng bộ dữ liệu.", 560),
  ...TB("Bảng 3.2. Kích thước và vai trò của ba split trong VietMed-NER", T(["Split", "Số câu", "Số từ trung bình mỗi câu", "Vai trò trong khóa luận"], ["train", "validation", "test"].map((k) => [k, n(X.splits.split_sizes[k]), f(X.splits.mean_words[k], 1), k === "train" ? "Nguồn câu huấn luyện và kiểm định của dữ liệu quan hệ, đồng thời là dữ liệu mà checkpoint NER đã học" : k === "validation" ? "Tập dev để chọn alias và ngưỡng cho chuẩn hóa, đồng thời góp câu cho dữ liệu quan hệ" : "Đánh giá NER, chuẩn hóa và RE, đồng thời là nguồn của knowledge graph"]), [1500, 1300, 2200, 4638], { right: [1, 2] }), "Bảng cho biết mỗi split được dùng vào việc gì, qua đó đảm bảo tập test chỉ dùng để báo cáo kết quả."),
  P("Cần lưu ý rằng đây là văn bản chép lại lời nói trong hội thoại, chương trình tư vấn sức khỏe và quảng cáo sản phẩm, chứ không phải bệnh án viết. Mỗi dòng là một đoạn ngắn khoảng 22 đến 24 từ, thường bị cắt giữa câu và không có dấu câu. Dữ liệu còn chứa lỗi phiên âm, chẳng hạn “phẫu thuốc” thay cho “phẫu thuật”, và nhiều nội dung ngoài lâm sàng như mỹ phẩm hay thực phẩm chức năng. Vì vậy, kết quả trên VietMed-NER chưa đủ để chứng minh chất lượng của hệ thống trên bệnh án tại bệnh viện."),
  H4("3.3.1.2. Chất lượng nhãn nguồn"),
  P("Khi phân tích lỗi ở mục 4.6.1, khóa luận phát hiện một số nhãn gold của VietMed-NER không nhất quán. Ví dụ, “polyp” và “nhân xơ” được gán ORGAN trong một số câu, trong khi các cụm bệnh tương tự ở câu khác lại được gán DISEASESYMTOM. Những trường hợp này làm giảm điểm của cả mô hình lẫn pipeline mà không phản ánh lỗi thật, vì vậy khóa luận dùng thêm phân tích định tính bên cạnh chỉ số tổng hợp."),
  H3("3.3.2. Ánh xạ sang sáu loại thực thể mục tiêu"),
  P("Khóa luận chỉ quan tâm tới sáu loại thực thể phục vụ chuẩn hóa và RE, nên các nhãn gốc được ánh xạ như trong Bảng 3.3. Các loại còn lại như tuổi, giới tính, thời gian, nghề nghiệp hay địa điểm vẫn có giá trị cho những ứng dụng khác, nhưng không tham gia vào quan hệ nào của lược đồ và không có danh mục mã chuẩn tương ứng, nên được loại khỏi phạm vi của đề tài."),
  ...TB("Bảng 3.3. Ánh xạ từ nhãn gốc của VietMed-NER sang sáu loại thực thể mục tiêu", T(["Loại mục tiêu", "Nhãn gốc VietMed-NER"], mapRows, [2200, 7438]), "Bảng dùng để giải thích vì sao một số loại mục tiêu như PROCEDURE và DOSAGE có phạm vi rộng hơn tên gọi của chúng."),
  P("Cách ánh xạ này kéo theo ba hệ quả. Thứ nhất, TREATMENT được gộp vào PROCEDURE nên các từ chung như “điều trị” cũng trở thành PROCEDURE. Thứ hai, UNITCALIBRATOR rộng hơn khái niệm liều thuốc vì bao gồm cả số đo, mức độ và tỉ lệ, do đó DOSAGE có precision thấp. Thứ ba, PREVENTIVEMED, vốn chủ yếu là vắc-xin, được gộp vào DRUG. Việc này có lợi cho chuẩn hóa thuốc nhưng làm các câu về tiêm phòng sinh ra cặp CONDITION và DRUG, trong khi theo quy ước đó là phòng ngừa chứ không phải điều trị. Ngoài ra, các loại phi y khoa bị loại hẳn thay vì giữ dưới một nhãn chung, vì mô hình có xu hướng tự tin gán “bệnh nhân” là OCCUPATION, một đặc điểm của dữ liệu huấn luyện chứ không phải lỗi căn chỉnh."),
  H3("3.3.3. Bộ dữ liệu quan hệ"),
  H4("3.3.3.1. Lý do xây dựng lại dữ liệu quan hệ"),
  P(`Ở giai đoạn đầu, khóa luận gán nhãn quan hệ trực tiếp cho các cặp thực thể lấy từ nhãn NER của VietMed-NER. Bộ dữ liệu thu được có ${RX_OLD.pairs} cặp huấn luyện nhưng chỉ ${RX_OLD.pos} cặp dương, và khi rà soát lại, khoảng ${RX_OLD.wrongTypeNeg}% cặp âm chứa ít nhất một thực thể bị gán sai kiểu, chẳng hạn động từ “kiểm soát” bị gán là thuốc. Mô hình học trên dữ liệu như vậy chủ yếu học cách nhận ra thực thể sai thay vì học quan hệ giữa hai thực thể đúng.`),
  P(`Vì vậy, toàn bộ nhãn quan hệ cũ bị loại bỏ, chỉ giữ văn bản và nhãn NER gốc của VietMed-NER, và dữ liệu được xây dựng lại theo ba nguyên tắc. Nguyên tắc thứ nhất là kiểm tra thực thể trước khi gán quan hệ. Nguyên tắc thứ hai là ưu tiên những câu có nhiều khả năng chứa quan hệ dương để dữ liệu bớt thưa. Nguyên tắc thứ ba là tập kiểm tra do người có chuyên môn y khoa gán.`),
  H4("3.3.3.2. Hướng dẫn gán nhãn hai bước"),
  P("Hướng dẫn gán nhãn được viết mới từ câu thật trong kho và được khóa trước khi bắt đầu gán. Việc gán gồm hai bước. Ở bước thứ nhất, người gán xét từng lượt đề cập và chọn VALID nếu thực thể đúng kiểu, hoặc INVALID nếu thực thể sai kiểu, quá chung chung hay không phải khái niệm y khoa. Chẳng hạn, “huyết áp” là CONDITION hợp lệ khi mang nghĩa bệnh tăng huyết áp nhưng không hợp lệ khi chỉ con số đo, còn các động từ như “kiểm soát” hay “phục hồi” không được coi là thuốc hay thủ thuật. Ở bước thứ hai, chỉ những cặp có cả hai thực thể VALID mới được gán nhãn, với nhãn là tên quan hệ của cặp hoặc NO_RELATION."),
  P("Người gán chỉ dựa vào điều mà chính câu đó nói ra, không dùng kiến thức y khoa bên ngoài để bù cho phần câu bị cắt, và câu không đủ căn cứ thì được gán NO_RELATION. Hướng dẫn có định nghĩa, ví dụ dương và ví dụ âm cho từng quan hệ, cùng quyết định cho các trường hợp mơ hồ như tác dụng phụ, phòng bệnh, phủ định và câu hỏi. Nội dung chính của hướng dẫn được tóm tắt ở Phụ lục C."),
  H4("3.3.3.3. Chọn câu theo điểm khả năng dương"),
  P(`Sau khi ghép cặp theo lược đồ năm quan hệ và loại các thực thể nằm trong danh sách hay bị gán sai kiểu, chỉ ${n(RX.sel.pool_sentences_with_valid_candidate.seed)} câu thuộc phần train và validation cùng ${RX.sel.pool_sentences_with_valid_candidate.test} câu thuộc phần test còn cặp ứng viên. Hình 3.2 cho thấy số cặp phân bố rất lệch giữa các quan hệ. Quan hệ located_at chiếm phần lớn, còn diagnosed_by và has_dosage rất hiếm, vì phần lớn lượt đề cập DOSAGE trong lời nói là tính từ hay số liệu thống kê chứ không phải liều thuốc.`),
  P("Vì chưa có nhãn, khóa luận ước lượng khả năng một cặp ứng viên là dương bằng điểm theo công thức (3.1), rồi lấy điểm của câu là tổng điểm các cặp trong câu."),
  EQ("s(h, t) = 3·[quy tắc đoán dương] + [khoảng cách ≤ 4 từ] + [có từ gợi ý]", 10),
  PN("Trong đó:", { p: { keepNext: true } }),
  WH("h và t là thực thể đầu và thực thể đuôi của cặp ứng viên."),
  WH("Mỗi biểu thức trong ngoặc vuông nhận giá trị 1 nếu điều kiện đúng và 0 nếu sai. Quy tắc đoán dương là baseline rule-based ở mục 3.4.7.2, còn từ gợi ý là các từ như “điều trị bằng”, “uống”, “ở” hay “xét nghiệm” nằm giữa hai thực thể.", true),
  P("Tín hiệu từ quy tắc nhận hệ số 3 vì quy tắc đòi hỏi đồng thời khoảng cách ngắn, từ gợi ý và không có thực thể chen giữa, nên là tín hiệu mạnh nhất, còn hai tín hiệu đơn lẻ chỉ dùng để xếp hạng phụ. Hệ số 3 và ngưỡng 4 từ được đặt trước theo cách quy tắc được thiết kế và không được tinh chỉnh, vì điểm này chỉ dùng để chọn câu chứ không dùng làm nhãn."),
  P(`Câu được chọn theo hạn mức của từng quan hệ, ưu tiên quan hệ hiếm để located_at không lấn át, kèm một phần câu chọn ngẫu nhiên để mô hình vẫn thấy phân bố tự nhiên và cặp âm thật. Từ phần train và validation, khóa luận chọn ${RX.sel.seed.sentences + RX.sel.dev.sentences} câu, trong đó ${RX.sel.dev.sentences} câu được tách ra làm tập kiểm định. Tập kiểm tra gồm ${RX.sel.test.sentences} câu lấy từ phần test, trong đó ${RX.sel.test.reasons.random} câu được chọn ngẫu nhiên. Không câu nào của tập huấn luyện có chung chuỗi ${RX.sel.leak_ngram} từ liên tiếp với câu của tập kiểm tra. Bảng 3.4 cho thấy kể cả khi đã lấy toàn bộ câu có ứng viên, diagnosed_by và has_dosage vẫn chỉ có rất ít câu.`),
  ...FIG("relation/figures/h_cap_ung_vien.png", "Hình 3.2. Số cặp ứng viên và số cặp có tín hiệu dương theo quan hệ trong kho câu của phần train và validation", "Hình cho thấy located_at chiếm phần lớn cặp có tín hiệu dương, các quan hệ còn lại rất hiếm, nên câu cần được chọn có chủ đích thay vì lấy ngẫu nhiên.", 560),
  ...TB("Bảng 3.4. Số câu và số cặp ứng viên theo quan hệ sau khi chọn mẫu, trước bước kiểm tra thực thể", T(["Quan hệ", "Câu huấn luyện", "Cặp huấn luyện", "Cặp kiểm định", "Câu kiểm tra", "Cặp kiểm tra"], RX_REL.map((k) => [k, RX.sel.seed.sentences_by_relation[k], n(RX.sel.seed.pairs_by_relation[k]), RX.sel.dev.pairs_by_relation[k], RX.sel.test.sentences_by_relation[k], RX.sel.test.pairs_by_relation[k]]), [2600, 1400, 1400, 1400, 1400, 1438], { size: 22, right: [1, 2, 3, 4, 5] }), "Bảng cho thấy diagnosed_by và has_dosage có rất ít câu ngay cả khi đã lấy toàn bộ câu có ứng viên, nên hai quan hệ này khó học từ dữ liệu thật."),
  H4("3.3.3.4. Tập kiểm tra"),
  P(`Tập kiểm tra gồm ${RX.test.length} câu với ${rxMentions} lượt đề cập, được người có chuyên môn y khoa gán trên phiếu đã xáo trộn thứ tự câu, không hiển thị dự đoán của quy tắc hay nhãn của mô hình ngôn ngữ lớn. Ở bước kiểm tra thực thể, ${rxInvalid} lượt đề cập bị loại vì sai kiểu, còn lại ${rxPairs} cặp có hai thực thể hợp lệ. Ở lượt gán đầu, người gán coi gần như mọi cặp cùng xuất hiện trong câu là có quan hệ, với ${rxPosV1All} trên ${rxPairs} cặp dương. Với tỉ lệ như vậy, một bộ dự đoán luôn trả lời có quan hệ gần như đạt điểm tối đa, nên tập này không đo được khả năng loại cặp sai của mô hình.`),
  P(`Để kiểm tra tiêu chí, người gán soát lại một mẫu ${rxAudit.sample} cặp gồm những cặp mô hình bỏ sót và các cặp đối chứng mà không nhìn thấy nhãn cũ hay dự đoán. Người gán đưa ra kết luận cho ${rxAudit.judged} cặp, và cả ${rxAudit.judged} cặp đều được đánh lại là không có quan hệ, kể cả ${rxAudit.control} cặp đối chứng. Phần lớn các cặp này nằm trong câu liệt kê bệnh hoặc câu nói về phòng bệnh. Từ đó, tiêu chí được chốt chặt hơn, theo đó việc hai thực thể cùng xuất hiện trong câu chưa đủ để gán quan hệ. Toàn bộ ${rxPairs} cặp sau đó được gán lại theo tiêu chí chặt, trong đó người gán xem nhãn gợi ý do mô hình ngôn ngữ lớn đưa ra rồi xác nhận hoặc sửa từng cặp, và còn lại ${rxPos} cặp dương. Bộ nhãn gán lại là tập kiểm tra chính của khóa luận, và Bảng 3.5 so sánh số cặp dương ở hai lượt gán.`),
  P(`Lượt gán lại có tham khảo nhãn gợi ý do mô hình ngôn ngữ lớn đưa ra, và trên ${RX.agTest2.pairs} cặp mà cả hai nguồn đều coi hai thực thể là hợp lệ, hệ số kappa giữa nhãn gán lại và nhãn do mô hình ngôn ngữ lớn gán độc lập đạt ${f(RX.agTest2.kappa, 3)}.`),
  ...TB("Bảng 3.5. Số cặp dương của tập kiểm tra theo quan hệ ở lượt gán đầu và sau khi gán lại theo tiêu chí chặt", T(["Quan hệ", "Số cặp", "Dương ở lượt đầu", "Dương sau khi gán lại"], [...RX_REL.map((k) => [k, rxR("model", k).pairs, rxPosV1(k), rxR("model", k).positives]), ["Tổng", rxPairs, rxPosV1All, rxPos]], [3200, 2000, 2200, 2238], { size: 22, right: [1, 2, 3] }), "Bảng cho thấy tiêu chí chặt loại phần lớn các cặp chỉ cùng xuất hiện trong câu, nhất là ở located_at."),
  H4("3.3.3.5. Tập huấn luyện và tập kiểm định"),
  P(`Tập huấn luyện và tập kiểm định được mô hình ngôn ngữ lớn gán hai lượt độc lập theo cùng hướng dẫn. Hai lượt đồng thuận cao, với kappa ${f(RX.agSeed.entity_kappa, 3)} ở bước kiểm tra thực thể và ${f(RX.agSeed.pair_kappa, 3)} ở bước gán quan hệ. Người có chuyên môn y khoa sau đó duyệt các nhãn mà hai lượt thống nhất và không phải sửa nhãn nào. Những chỗ hai lượt bất đồng mà chưa được quyết định bị loại, gồm ${RX.rev.entity_unresolved_dropped} lượt đề cập và ${RX.rev.pair_unresolved_dropped} cặp, kéo theo ${RX.rev.pair_dropped_entity_unresolved} cặp chứa các lượt đề cập đó. Bảng 3.6 cho thấy has_dosage không còn cặp nào và diagnosed_by chỉ có ở tập huấn luyện, nên hai quan hệ này được bổ sung bằng dữ liệu sinh như trình bày ở mục 3.3.3.6.`),
  H4("3.3.3.6. Dữ liệu sinh"),
  P(`Để bù cho các quan hệ hiếm, khóa luận sinh thêm dữ liệu từ câu huấn luyện, không bao giờ từ câu kiểm định hay kiểm tra, theo hai cách. Cách thứ nhất thay một thực thể của câu thật bằng thực thể khác cùng kiểu và cùng nhóm chuyên khoa, giữ nguyên nhãn. Cách thứ hai điền cặp thực thể vào các mẫu câu viết tay, gồm mẫu dương và mẫu âm khó như câu nói về phòng bệnh, tác dụng phụ, phủ định hay có thực thể gây nhiễu. Sau đó, câu trùng và câu có chung chuỗi ${RX.sel.leak_ngram} từ với tập kiểm định hoặc tập kiểm tra bị loại, mỗi khung câu chỉ giữ tối đa ba câu, và tỉ lệ dương được đưa về khoảng ${pct(RX.syn.target_positive_rate[0], 0)} đến ${pct(RX.syn.target_positive_rate[1], 0)}, gần tỉ lệ ${pct(RX.syn.seed_positive_rate)} của tập huấn luyện.`),
  ...TB("Bảng 3.6. Số cặp dương và cặp âm của tập huấn luyện và tập kiểm định theo quan hệ", T(["Quan hệ", "Huấn luyện dương", "Huấn luyện âm", "Kiểm định dương", "Kiểm định âm"], RX_REL.map((k) => [k, RX.rev[`seed:${k}:pos`] || 0, RX.rev[`seed:${k}:neg`] || 0, RX.rev[`dev:${k}:pos`] || 0, RX.rev[`dev:${k}:neg`] || 0]), [3000, 1650, 1650, 1650, 1688], { size: 22, right: [1, 2, 3, 4] }), "Bảng cho thấy has_dosage không có cặp nào và diagnosed_by chỉ xuất hiện ở tập huấn luyện."),
  P(`Kho sinh ban đầu có ${n(RX.syn.pool.pairs)} cặp, từ đó khóa luận lấy hai mức chưa kiểm tra là ${n(RX.syn.x1.pairs)} cặp, bằng số cặp huấn luyện thật, và ${n(RX.syn.x3.pairs)} cặp, gấp ba lần. Đây cũng là nguồn duy nhất cung cấp mẫu has_dosage cho mô hình. Vì câu sinh được ghép tự động, một phần câu có thể sai về y khoa, chẳng hạn khi thực thể mới không đi được với các từ xung quanh. Mục 3.3.3.7 trình bày bước kiểm tra kho sinh trước khi đưa vào huấn luyện.`),
  H4("3.3.3.7. Kiểm tra dữ liệu sinh"),
  P(`Mỗi câu sinh được tách thành ba đơn vị kiểm tra. Đơn vị thứ nhất là cụm từ mới tạo ra quanh thực thể được thay, như “đau thận” hay “viêm đầu gối”, được tra trong kho VietMed-NER và danh mục ICD-10 của Bộ Y tế. Đơn vị thứ hai là bộ ba quan hệ mang nhãn dương, được tra trong các nguồn tri thức MED-RT, RxNorm [16], BioText [25], ADE [26] và trang thông tin của WHO và NIH. Đơn vị thứ ba là cả câu, được dịch sát nghĩa sang tiếng Anh để LLM chấm xem câu có hợp lý về y khoa hay không. Câu chỉ được coi là Valid khi qua cả ba đơn vị, còn lại là Invalid kèm lý do nặng nhất. Trên ${n(RX.val.sentences)} câu của kho sinh, ${n(RX.val.verdict.VALID)} câu được coi là Valid và ${n(RX.val.verdict.INVALID)} câu là Invalid, trong đó ${n(RX.val.reason.implausible_context)} câu bị loại vì ngữ cảnh không hợp lý.`),
  P(`Người có chuyên môn y khoa sau đó duyệt ${n(RX.vman.expert_decisions.KEEP + RX.vman.expert_decisions.DROP)} câu trên một phiếu chỉ có hai cột cần điền, một cột cho câu và một cột cho quan hệ, mỗi cột nhận 1 cho Valid và 2 cho Invalid. Mẫu duyệt gồm ${rxVP.sample_valid.rows} câu Valid chọn ngẫu nhiên, ${rxVP.sample_wrong.rows} câu bị loại vì ngữ cảnh và toàn bộ ${rxVP.all_not_found.rows} câu không tìm được bằng chứng. Người duyệt đồng ý với ${pct(rxVP.sample_valid.rate)} số câu mà hệ thống coi là Valid, nhưng chỉ đồng ý với ${pct(rxVP.sample_wrong.rate)} số câu mà hệ thống loại vì ngữ cảnh. Như vậy, khi hệ thống kết luận một câu là Valid thì kết luận đó thường đúng, còn kết luận Invalid của LLM ở đơn vị câu quá khắt khe và không đáng tin. Vì lý do này, các câu Invalid mà người duyệt giữ lại được đưa trở lại kho, còn các câu Invalid không được duyệt thì bị bỏ.`),
  P(`Sau khi cân bằng lại tỉ lệ dương, kho đã kiểm tra còn ${n(RX.vman.pool.records)} câu với ${n(RX.vman.pool.pairs)} cặp, trong đó ${n(RX.vman.pool.by_status.SYNTHETIC_EXPERT_CHECKED)} câu đã qua người duyệt và ${n(RX.vman.pool.by_status.SYNTHETIC_AUTO_VALIDATED)} câu chỉ qua kiểm tra tự động. Theo tỉ lệ đồng ý ${pct(rxVP.sample_valid.rate)} ở trên, phần chỉ qua kiểm tra tự động có thể vẫn còn khoảng một phần mười số câu sai. Từ kho này, khóa luận lấy hai mức là ${n(RX.vman.x1.pairs)} cặp, bằng số cặp huấn luyện thật, và toàn bộ ${n(RX.vman.pool.pairs)} cặp, vì kho không đủ câu hợp lệ cho mức gấp ba lần.`),
  H3("3.3.4. Tập gold chuẩn hóa"),
  P("Để đo chuẩn hóa bằng Accuracy và Top-k Accuracy như đề cương yêu cầu, khóa luận xây dựng một tập đánh giá riêng thay vì đo trên bộ dữ liệu quan hệ. Đơn vị đánh giá là dạng bề mặt duy nhất, tức là chuỗi thực thể sau khi đưa về chữ thường và gộp khoảng trắng, của các thực thể gold CONDITION và DRUG trong VietMed-NER. Mỗi dạng có một mã gold hoặc nhãn NIL khi không có mã phù hợp. Kết quả theo đề cập được tính thêm bằng cách nhân với tần suất xuất hiện của mỗi dạng. Tập dev lấy từ split validation và tập test lấy từ split test, như trình bày trong Bảng 3.7."),
  P(`Khi gán nhãn, mỗi dạng được trình bày kèm tần suất và tối đa ba câu ngữ cảnh. LLM gán một hoặc nhiều mã, trong đó mã đầu tiên là mã chính và các mã sau cũng được tính là đúng, hoặc gán NIL kèm ghi chú. Nhãn NIL dành cho từ chung chung như “triệu chứng”, nhóm thuốc như “thuốc tránh thai”, những thứ không phải bệnh hay thuốc như “sữa mẹ”, và các mảnh lỗi NER như “bị tiêu”. `),
  P(`Trên các dạng NIL, hệ thống được chấm theo tỉ lệ từ chối đúng. ICD-10 được chấm ở hai mức là mã đầy đủ và nhóm ba ký tự, còn RxNorm ưu tiên mức hoạt chất. Có ${normMan.dev_test_form_overlap.CONDITION} dạng CONDITION và ${normMan.dev_test_form_overlap.DRUG} dạng DRUG xuất hiện ở cả dev và test, và các dạng này dùng chung nhãn để hai tập nhất quán với nhau. Nhãn của tập này do mô hình ngôn ngữ lớn gán theo quy trình trên, kèm phiếu duyệt để chuyên gia y tế xác nhận và chạy lại đánh giá khi cần.`),
  ...TB("Bảng 3.7. Kích thước tập gold chuẩn hóa theo loại thực thể và theo danh mục mã", T(["Split", "CONDITION, số dạng và đề cập", "DRUG, số dạng và đề cập", "ICD-10, có mã và NIL", "RxNorm, có mã và NIL"], ["dev", "test"].map((k) => [k, `${normMan.splits[k].CONDITION.unique_forms} và ${n(normMan.splits[k].CONDITION.mentions)}`, `${normMan.splits[k].DRUG.unique_forms} và ${normMan.splits[k].DRUG.mentions}`, `${nc("ICD-10", k).n_linkable} và ${nc("ICD-10", k).n_nil}`, `${nc("RxNorm", k).n_linkable} và ${nc("RxNorm", k).n_nil}`]), [1100, 2300, 2100, 2000, 2138], { size: 20, right: [1, 2, 3, 4] }), "Bảng cho biết số dạng có mã và số dạng NIL ở mỗi tập, làm cơ sở cho các chỉ số Accuracy và tỉ lệ từ chối đúng ở Chương 4."),
  H3("3.3.5. Tổng hợp vai trò train, dev và test theo từng bước"),
  P("Bảng 3.8 trả lời câu hỏi mỗi bước của hệ thống dùng tập nào để học, tập nào để chọn tham số và tập nào để báo cáo kết quả. Nguyên tắc chung là mọi lựa chọn về ngưỡng, alias hay cách kết hợp mô hình đều được đưa ra trên train hoặc dev, còn test chỉ được chạy sau khi mọi lựa chọn đã chốt."),
  H3("3.3.6. Đặc điểm của dữ liệu"),
  P("Dữ liệu của khóa luận có một số đặc điểm cần lưu ý khi đọc kết quả ở Chương 4. Đây là lời nói y tế được chép lại nên câu ngắn, thường bị cắt và có lỗi phiên âm, khác với bệnh án viết theo khuôn mẫu. Các quan hệ diagnosed_by và has_dosage hiếm gặp trong lời nói, nên được bổ sung bằng dữ liệu sinh. Ngoài ra, câu được chọn theo điểm khả năng dương để dữ liệu bớt thưa, nên tỉ lệ cặp dương trong các tập quan hệ cao hơn phân bố tự nhiên của văn bản. Vì đặc điểm này, mọi tập dùng để báo cáo kết quả đều được tách khỏi dữ liệu huấn luyện ngay từ bước chọn câu."),
  ...TB("Bảng 3.8. Vai trò của train, dev và test trong từng bước của hệ thống", T(["Bước", "Train để học", "Dev để chọn", "Test để báo cáo", "Nguồn nhãn"], [
    ["NER", "Split train, với checkpoint kế thừa và hai baseline tự huấn luyện", "Checkpoint kế thừa chưa rõ, baseline dùng split validation", `Split test, ${n(nerNew.lat.total_samples)} câu`, "Người gán của bộ dữ liệu"],
    ["Chuẩn hóa", "Không học tham số, từ điển chỉ lấy dạng có trong train và dev", `Split validation, ${nForms("dev")} dạng`, `Split test, ${nForms("test")} dạng, chạy một lần`, "LLM"],
    ["RE", `${RX.sel.seed.sentences} câu huấn luyện với ${n(RX.syn.seed_pairs)} cặp, cộng ${n(RX.vman.pool.pairs)} cặp dữ liệu sinh đã kiểm tra, từ split train và validation`, `${RX.sel.dev.sentences} câu kiểm định với ${rxSel.pairs} cặp`, `${RX.test.length} câu của split test với ${rxPairs} cặp, chỉ để báo cáo`, "LLM gán hai lượt và người duyệt cho phần huấn luyện, người có chuyên môn y khoa gán cho tập kiểm tra"],
    ["Knowledge graph", "Không có", "Không có", `${n(kgS.documents)} câu của split test`, "Dự đoán của hệ thống"],
  ], [1500, 2300, 2100, 2200, 1538], { size: 19 }), "Bảng dùng để chứng minh không có bước nào chọn tham số dựa trên tập test."),
);

// ===== 3.4. Thiết kế hệ thống (trước đây là chương Thiết kế và cài đặt) =====
add(
  H2("3.4. Thiết kế hệ thống"),
  P("Mục này trình bày cách hệ thống được thiết kế và cài đặt, đi theo đúng thứ tự xử lý từ văn bản đầu vào tới knowledge graph. Thiết kế dựa trên ba nguyên tắc. Thứ nhất, mọi thực thể giữ vị trí ký tự trong cùng một văn bản để các bước sau dùng chung một hệ tọa độ. Thứ hai, chuẩn hóa và RE là hai nhánh độc lập, nên lỗi ở nhánh này không chặn nhánh kia. Thứ ba, hệ thống luôn phân biệt trường hợp không có kết quả với trường hợp không đủ căn cứ để kết luận, thể hiện qua việc không gán mã khi không đủ chắc chắn và đánh dấu thực thể bị bỏ qua khi sinh cặp."),
  H3("3.4.1. Kiến trúc tổng thể"),
  P("Hệ thống gồm sáu bước xử lý nối tiếp nhau như Hình 3.3, trong đó nhãn trên mỗi mũi tên là dữ liệu mà bước trước chuyển cho bước sau. Ba bước đầu thuộc phần NER. Tiền xử lý chia văn bản thành các chunk từ có kèm vị trí ký tự, suy luận NER gán nhãn cho từng từ, rồi quy tắc liều và hậu xử lý sửa các lỗi đã biết để trả về thực thể thuộc sáu loại mục tiêu. Từ đây luồng xử lý tách thành hai nhánh. Nhánh chuẩn hóa gán mã cho tình trạng bệnh và thuốc, còn nhánh RE sinh cặp ứng viên từ cùng danh sách thực thể rồi phân loại quan hệ. Hai nhánh chỉ cần đầu ra của NER chứ không cần đầu ra của nhau, nên một thuốc không tra được mã vẫn có thể được nối với bệnh. Kết quả của hai nhánh được gộp thành một bản ghi, và bản ghi của nhiều văn bản được gộp tiếp thành đồ thị tri thức."),
  ...FIG("h3_1_luong_xu_ly.png", "Hình 3.3. Sáu bước xử lý của hệ thống và dữ liệu truyền giữa các bước", "Hình cho thấy chuẩn hóa và RE là hai nhánh độc lập cùng nhận đầu ra của phần NER, nên lỗi tra mã không làm dừng việc trích xuất quan hệ.", 470),
  P("Mỗi bước được cài đặt thành một thành phần riêng với đầu vào và đầu ra xác định, nhờ đó từng thành phần có thể được kiểm thử và thay thế mà không ảnh hưởng tới phần còn lại. Phần NER được tổ chức thành một chuỗi thành phần nối tiếp, trong đó mỗi thành phần nhận đầu ra của thành phần trước. Phần chuẩn hóa dùng một giao diện chung cho mọi danh mục mã, còn ICD-10 và RxNorm là hai cách cài đặt riêng của giao diện đó, nên muốn thêm một danh mục mới như LOINC chỉ cần bổ sung một cách cài đặt. Phần RE nhận bộ phân loại quan hệ như một tham số, nên có thể thay giữa quy tắc, ViHealthBERT hay cách kết hợp hai bên mà không đổi luồng xử lý."),
  H3("3.4.2. Tiền xử lý"),
  P("Bước tiền xử lý chuẩn hóa khoảng trắng trong văn bản, bao gồm thay khoảng trắng không ngắt và ký tự tab, gộp nhiều dấu cách liên tiếp và giới hạn số dòng trống, nhưng không sửa số, đơn vị hay ký hiệu y khoa. Sau đó văn bản được tách token bằng một biểu thức chính quy, trong đó mỗi dấu câu là một token riêng để không dính vào thực thể, chẳng hạn chuỗi “dạ dày,” được tách thành “dạ”, “dày” và dấu phẩy. Mỗi token giữ vị trí ký tự của nó trong văn bản đã chuẩn hóa."),
  P("Mô hình chỉ nhận tối đa 256 subword mỗi lần, nên văn bản dài phải được chia thành các chunk, và việc chia luôn dừng ở ranh giới từ. Hình 3.4 trình bày bốn ngưỡng chia theo số từ cùng căn cứ của từng ngưỡng. Ngưỡng cắt cứng 140 từ được tính từ dữ liệu. Trên tập test, trung bình mỗi từ chỉ ứng với 1,01 subword và trường hợp nặng nhất là 1,42 subword, nên 140 từ tương ứng tối đa khoảng 198 subword. Con số này nằm dưới mức an toàn 200 subword ghi trong cấu hình và cách giới hạn 256 của mô hình một khoảng dự phòng."),
  P("Ngưỡng 35 từ lấy theo độ dài câu, vì 99% câu của tập test có không quá 34 từ, nên hầu hết các câu được giữ nguyên trong một chunk. Ngưỡng 15 từ tránh tạo ra chunk quá ngắn thiếu ngữ cảnh. Ngưỡng 120 từ ưu tiên tách ở dấu phẩy hoặc dấu chấm phẩy trước khi chạm ngưỡng cắt cứng, để chunk không bị cắt giữa một mệnh đề."),
  ...FIG("h3_3_chia_chunk.png", "Hình 3.4. Bốn ngưỡng chia văn bản dài thành chunk theo số từ và giới hạn subword tương ứng của mô hình", "Hình giúp người đọc thấy vì sao các ngưỡng được đặt ở 15, 35, 120 và 140 từ, và khoảng an toàn còn lại so với giới hạn 256 subword.", 560),
  P("Các ngưỡng 15, 35 và 120 được đặt theo kinh nghiệm. Trên VietMed-NER, câu dài nhất chỉ có 40 từ nên không câu nào chạm ngưỡng 120, và các ngưỡng này chủ yếu phát huy tác dụng khi hệ thống xử lý văn bản dài như bệnh án."),
  H3("3.4.3. Mô hình NER"),
  P("Mô hình NER được kế thừa và không được huấn luyện lại trong khóa luận, vì vậy các giá trị trong Bảng 3.9 do người huấn luyện ban đầu lựa chọn. Cấu hình kiến trúc và siêu tham số huấn luyện được lấy từ thông tin lưu kèm mô hình. Cột lý do trong bảng giải thích căn cứ của từng giá trị, dựa trên cấu trúc của mô hình nền và các khuyến nghị fine-tune được nêu trong bài báo BERT [5]."),
  P("Khi suy luận, mỗi token được tách thành subword bằng tokenizer của checkpoint, rồi hai token đặc biệt được thêm vào đầu và cuối chuỗi. Mô hình trả về logits cho từng subword, và hàm softmax biến chúng thành xác suất của từng nhãn. Các vị trí token đặc biệt bị loại trước khi giải mã BIO, vì lúc huấn luyện các vị trí này không có nhãn nên dự đoán tại đó có thể ngẫu nhiên. Nhãn của một từ được lấy theo subword đầu tiên, còn độ tin cậy của từ là trung bình xác suất của các subword. Cuối cùng, nhãn gốc được ánh xạ sang sáu loại mục tiêu trước khi giải mã thành span. Hình 3.5 minh họa quá trình này trên một câu ngắn."),
  ...TB("Bảng 3.9. Cấu hình kiến trúc, siêu tham số huấn luyện của checkpoint NER và lý do của từng giá trị", T(["Thuộc tính", "Giá trị", "Lý do"], [
    ["Mô hình nền", "ViHealthBERT-base, bản âm tiết", "Được tiền huấn luyện trên văn bản y tế tiếng Việt và làm việc trực tiếp trên âm tiết nên không cần tách từ"],
    ["Kiến trúc", `RoBERTa phân loại token, ${modelCfg.num_hidden_layers} lớp, ${modelCfg.num_attention_heads} đầu chú ý, kích thước ẩn ${modelCfg.hidden_size}`, "Cố định theo cỡ base của mô hình nền, thêm một lớp tuyến tính để phân loại nhãn cho từng token"],
    ["Số nhãn đầu ra", String(Object.keys(modelCfg.id2label || {}).length), "Bằng 18 loại thực thể của VietMed-NER nhân với hai nhãn B và I, cộng thêm nhãn O"],
    ["Độ dài tối đa", "256 subword", "Kế thừa từ PhoBERT, là lý do hệ thống phải chia đoạn con ở mục 3.4.2"],
    ["Tốc độ học", trainArgs.learning_rate === 5e-5 ? "5 × 10⁻⁵" : String(trainArgs.learning_rate), "Nằm trong khoảng 2 × 10⁻⁵ đến 5 × 10⁻⁵ mà BERT khuyến nghị khi tinh chỉnh"],
    ["Số vòng huấn luyện và kích thước lô", `${trainArgs.num_train_epochs} vòng, lô ${trainArgs.per_device_train_batch_size}`, "Mô hình tốt nhất được giữ lại sau mỗi vòng nên số vòng được đặt rộng; lô 32 là giá trị BERT khuyến nghị"],
    ["Bộ tối ưu và suy giảm trọng số", `AdamW, ${String(trainArgs.weight_decay).replace(".", ",")}`, "Lựa chọn chuẩn khi huấn luyện Transformer, giúp hạn chế quá khớp"],
  ], [2300, 2900, 4438], { size: 20 }), "Bảng giúp người đọc nắm cấu hình của mô hình NER kế thừa và căn cứ của từng giá trị."),
  P("Toàn bộ các bước từ tách subword, thêm token đặc biệt, tính xác suất cho đến giải mã được tóm tắt trong Mã giả 3.1."),
  ...FIG("h_token_dac_biet.png", "Hình 3.5. Nhãn dự đoán tại từng vị trí của chuỗi đầu vào và các thực thể thu được sau khi bỏ hai token đặc biệt rồi giải mã BIO", "Hình cho thấy vì sao dự đoán tại hai token đặc biệt bị loại, và cách các nhãn B, I liền nhau được gộp thành một thực thể.", 540),
  ...ALGO("Mã giả 3.1. Suy luận NER cho một đoạn con", "chuỗi từ words, bộ tách subword tok, mô hình NER M", "danh sách thực thể kèm nhãn và độ tin cậy", [
    "function PredictChunk(words, tok, M)",
    "  S ← [ ], owner ← [ ]",
    "  for i ← 1 to |words| do",
    "    for each p ∈ tok(wordsᵢ) do",
    "      S.append(p), owner.append(i)",
    "    end for",
    "  end for",
    "  X ← ⟨s⟩ ⊕ S[1..256] ⊕ ⟨/s⟩",
    "  P ← softmax(M(X))[2..|X| − 1] ▷ bỏ ⟨s⟩ và ⟨/s⟩",
    "  for i ← 1 to |words| do",
    "    J ← {j : ownerⱼ = i}",
    "    labelᵢ ← Map6(argmax P[min J])",
    "    confᵢ ← trung bình của max P[j] với j ∈ J",
    "  end for",
    "  return DecodeBIO(words, label, conf)",
    "end function",
  ]),
  DESC("Mã giả cho thấy nhãn của mỗi từ lấy theo subword đầu tiên, còn độ tin cậy là trung bình trên mọi subword của từ."),
  H3("3.4.4. Luật nhận diện liều lượng"),
  P("Bộ trích liều lượng dùng biểu thức chính quy để nhận ba thành phần. Thành phần thứ nhất là giá trị số, kể cả số viết bằng chữ như “nửa”, “một”, “hai” và khoảng giá trị như “1-2”. Thành phần thứ hai là đơn vị hàm lượng hoặc thể tích như mg, ml, IU, hoặc dạng bào chế như viên, ống, gói. Thành phần thứ ba là tần suất như “2 lần/ngày”, “ngày 3 lần” hay “cách 8 giờ”. Mẫu tổng hợp bắt được các cụm như “500mg 2 viên/ngày” và tách chúng thành giá trị, đơn vị và tần suất. Các cụm do luật tìm được sau đó được gộp với thực thể DOSAGE của mô hình, và khi hai bên chồng lấn thì cụm đầy đủ hơn được giữ lại. Bảng 3.10 đưa ra một số ví dụ."),
  ...TB("Bảng 3.10. Ví dụ các cụm liều lượng mà luật nhận diện và thành phần được trích ra", T(["Văn bản", "Thành phần trích được"], [["500mg", "giá trị 500, đơn vị mg"], ["2 viên/ngày", "giá trị 2, dạng viên, tần suất mỗi ngày"], ["ngày 3 lần", "tần suất"], ["cách 8 giờ", "tần suất"]], [3500, 6138]), "Bảng minh họa dạng cụm liều mà luật được thiết kế để bắt, vốn hiếm gặp trong văn bản lời nói như phân tích ở Chương 4."),
  H3("3.4.5. Hậu xử lý"),
  P("Sau khi có thực thể từ mô hình và từ luật liều lượng, bước hậu xử lý áp dụng lần lượt năm thao tác dưới đây."),
  B("Lọc lược đồ, chỉ giữ sáu loại thực thể mục tiêu."),
  B("Luật 1 bỏ các thực thể DRUG trùng với từ hành động như “chỉ định”, “can thiệp”, “kê đơn” hay “điều trị”, vốn thường bị gán DRUG vì đứng cạnh tên thuốc trong dữ liệu huấn luyện."),
  B("Luật 1b đổi DRUG thành TEST nếu thực thể là tên xét nghiệm đã biết như men tim, men gan, troponin, HbA1c hay CRP. Luật này được thêm sau khi thấy “men tim” xuất hiện trong nhật ký các thuốc không tra được mã RxNorm."),
  B("Luật 2 gộp các tính từ chỉ mức độ như “cao”, “nhẹ” hay “nặng” bị gán DOSAGE vào CONDITION đứng ngay trước, chẳng hạn “sốt cao”, và lấy độ tin cậy là trung bình của hai thực thể."),
  B("Giải quyết chồng lấn bằng cách sắp xếp thực thể theo độ tin cậy rồi theo độ dài span giảm dần, lần lượt nhận một thực thể nếu nó không chồng lấn với thực thể đã nhận, và cuối cùng sắp lại theo vị trí."),
  P("Mã giả 3.2 thể hiện thứ tự áp dụng các thao tác trên."),
  ...ALGO("Mã giả 3.2. Thứ tự các thao tác hậu xử lý", "danh sách thực thể E, văn bản x", "danh sách thực thể đã hậu xử lý", [
    "function PostProcess(E, x)",
    "  E ← FilterSchema(E)",
    "  E ← DropActionDrugs(E) ▷ quy tắc 1",
    "  E ← RelabelLabTests(E) ▷ quy tắc 1b",
    "  E ← MergeSeverity(E, x) ▷ quy tắc 2",
    "  K ← ∅",
    "  for each e ∈ SortDesc(E, theo conf, độ dài) do",
    "    if not Overlaps(e, K) then",
    "      K ← K ∪ {e}",
    "    end if",
    "  end for",
    "  return SortAsc(K, theo vị trí)",
    "end function",
  ]),
  DESC("Mã giả cho thấy các luật được áp dụng trước, sau đó chồng lấn được giải quyết theo độ tin cậy."),
  H3("3.4.6. Chuẩn hóa mã"),
  H4("3.4.6.1. ICD-10"),
  P("Danh mục ICD-10 dạng Excel của Bộ Y tế được đọc một lần rồi lưu vào cache, gồm 12.218 mã và 12.059 tên bệnh khác nhau sau khi chuẩn hóa. Trước khi so khớp, tên bệnh và chuỗi truy vấn đều được đưa về chữ thường, bỏ dấu câu và gộp khoảng trắng. Hệ thống tra mã theo bốn bước ưu tiên dưới đây và dừng ngay ở bước đầu tiên cho kết quả."),
  ...LIST([
    "Exact match với tên trong danh mục.",
    "Tra trong từ điển alias, gồm 170 alias trực tiếp sau bản cải tiến, trong đó 137 alias mới chỉ được lấy từ các dạng có trong train và dev, cùng các mẫu biến đổi như đổi “ung thư X” thành “u ác của X”.",
    "Fuzzy matching bằng token_set_ratio với ngưỡng từ 0,85 trở lên, kèm sáu ràng buộc an toàn ở Bảng 3.11.",
    "Nếu không bước nào đạt, hệ thống không gán mã, theo nguyên tắc thà không gán mã còn hơn gán sai.",
  ]),
  P("Ngưỡng 0,85 được chọn theo nguyên tắc thà không gán còn hơn gán sai. Với ngưỡng này, cặp “viêm loét dạ dày” và “viêm loét tá tràng” chỉ đạt 0,72 nên bị loại. Tuy vậy, ngưỡng không đủ để tách mọi cặp bệnh khác nhau, chẳng hạn “tăng huyết áp vô căn” và “hạ huyết áp vô căn” vẫn đạt 0,91 vì chung ba trên bốn từ. Ngưỡng này là giá trị mặc định đặt từ đầu, chưa được dò trên tập dev, và các bản cải tiến sau đó tập trung vào ràng buộc thay vì hạ ngưỡng. Thêm vào đó, như đã phân tích ở mục 2.6, token_set_ratio cho điểm tối đa khi tập từ của chuỗi này nằm trọn trong chuỗi kia. Bảng 3.11 liệt kê các ràng buộc được thêm vào cho những trường hợp này."),
  ...TB("Bảng 3.11. Các ràng buộc an toàn của bước fuzzy matching ICD-10", T(["Ràng buộc", "Mục đích", "Ví dụ bị chặn"], [
    ["Tỉ lệ độ dài hai chuỗi từ 0,60 trở lên", "Tránh khớp chuỗi rất ngắn với tên dài", "“viêm” với một tên dài có chứa “viêm”"],
    ["Hệ số Jaccard từ 0,40 trở lên khi cả hai chuỗi có tối đa ba từ", "Tránh nhầm các triệu chứng gần giống nhau", "“đau bụng” với “đau lưng”"],
    ["Bỏ các từ định tính rồi so lại", "Tránh khớp chỉ nhờ các cụm như “không xác định” hay “bệnh”", "“bệnh abc” với “bệnh … không xác định”"],
    ["Từ đầu cụm của candidate phải có trong truy vấn", "Tránh tập con khác nghĩa", "“huyết áp cao” với “đo huyết áp”"],
    ["Từ chối khi chuỗi ngắn chỉ có một hoặc hai từ và là tập con thực sự", "Từ thêm vào thường quyết định bệnh", "“nhồi máu” với “nhồi máu lách”"],
    ["Mọi từ nội dung của candidate phải có trong truy vấn", "Candidate không được thêm khái niệm mà người nói không nhắc", "“rối loạn vận động” với “rối loạn vận động phân ly”"],
  ], [3500, 3000, 3138], { size: 20 }), "Bảng dùng để giải thích cách hệ thống chặn các lỗi gán mã do token_set_ratio gây ra, mỗi ràng buộc ứng với một nhóm lỗi đã gặp."),
  P("Các giá trị 0,60, 0,40 và 80 trong Bảng 3.11 được đặt cố định trước khi đánh giá và chưa được dò trên tập dev, nên căn cứ của chúng nằm ở chính các cặp lỗi cần chặn. Tỉ lệ độ dài 0,60 yêu cầu chuỗi ngắn dài ít nhất sáu phần mười chuỗi dài, nên “viêm” so với “viêm phổi thùy” có tỉ lệ 0,29 và bị chặn. Hệ số Jaccard 0,40 tách được hai triệu chứng chỉ chung một từ, chẳng hạn “đau bụng” với “đau lưng” có Jaccard 0,33 và bị chặn, trong khi “đau bụng” với “đau bụng cấp” có Jaccard 0,67 và được giữ. Ngưỡng 80 khi so từng từ cho phép sai đúng một ký tự ở một từ năm ký tự, vì độ tương tự giữa hai chuỗi như vậy bằng đúng 80, nhờ đó vẫn chấp nhận lỗi gõ nhỏ mà không chấp nhận hai từ khác nhau."),
  P("Với ràng buộc cuối cùng, phép so sánh từ được thực hiện sau khi bỏ dấu và chấp nhận độ tương tự từ 80 trở lên, đồng thời bỏ qua các từ đệm như “bệnh”, “cấp” hay “mạn tính”. Mã giả 3.3 tóm tắt toàn bộ quy trình tra mã ICD-10."),
  ...ALGO("Mã giả 3.3. Quy trình chuẩn hóa ICD-10", "tên bệnh m", "mã ICD-10 cùng cách khớp, hoặc NIL khi không gán mã", [
    "function NormalizeICD10(m)",
    "  q ← Clean(m)",
    "  if q ∈ ExactMap then",
    "    return (ExactMap[q], exact)",
    "  end if",
    "  if q ∈ AliasMap then",
    "    return (AliasMap[q], alias)",
    "  end if",
    "  for each π ∈ SynonymPatterns do",
    "    if q khớp mẫu π then",
    "      return NormalizeICD10(π(q))",
    "    end if",
    "  end for",
    "  (c, s) ← BestTokenSetRatio(q, ICD10Names)",
    "  if s ≥ 85 and Constraints(q, c) then ▷ Bảng 3.11",
    "    return (c, fuzzy)",
    "  end if",
    "  return NIL",
    "end function",
  ]),
  DESC("Mã giả cho thấy hệ thống dừng ở bước khớp đầu tiên thành công và trả về NIL thay vì đoán khi không bước nào đạt."),
  H4("3.4.6.2. RxNorm"),
  P("Với thuốc, tên được làm sạch bằng cách bỏ hàm lượng và dạng bào chế, rồi tra qua API của RxNav để lấy mã RxCUI và tên chuẩn. Mỗi lần gọi có thời gian chờ tối đa 5 giây và được thử lại tối đa 3 lần với khoảng chờ tăng dần. Mọi kết quả, kể cả trường hợp không tìm thấy, đều được lưu vào cache SQLite để có thể chạy lại mà không cần mạng, còn các thuốc không tra được được ghi vào nhật ký để bổ sung luật hoặc từ điển về sau."),
  P("Bản cải tiến, được chọn trên dev, bổ sung ba bước trước khi hệ thống bỏ cuộc. Bước thứ nhất là tra một từ điển alias từ tiếng Việt sang tiếng Anh gồm 31 mục, ví dụ “canxi” thành calcium hay “sắt” thành iron, chỉ lấy từ các dạng có trong train và dev và đã được kiểm tra là RxNav tra chính xác được. Bước thứ hai là bỏ từ đứng đầu chỉ dạng bào chế hoặc vật chứa như “viên nang”, “chai” hay “thuốc” rồi tra lại. Bước thứ ba là gọi dịch vụ tìm kiếm gần đúng của RxNav và chỉ chấp nhận ứng viên đứng đầu khi tên gần như trùng khớp với độ tương tự từ 90 trở lên. Ngưỡng này cao hơn ngưỡng 0,85 của ICD-10 vì dịch vụ này luôn trả về một ứng viên kể cả khi tên thuốc không có trong RxNorm, nên chỉ những tên gần như trùng khớp, tức khác nhau một hai ký tự do lỗi chính tả, mới được nhận. Mười ứng viên đầu của dịch vụ này được giữ làm danh sách top-k."),
  H4("3.4.6.3. Các loại chưa chuẩn hóa và bộ điều phối"),
  P("BODY_PART, TEST và PROCEDURE có các lớp stub dành cho ba ontology FMA, LOINC và MeSH. Các lớp này kế thừa cùng một lớp cơ sở và hiện trả về không có mã, để sau này có thể mở rộng mà không phải đổi giao diện. DOSAGE không cần chuẩn hóa. Bộ điều phối định tuyến từng thực thể tới đúng bộ chuẩn hóa theo loại, chỉ nạp mỗi bộ khi thực sự cần, bắt mọi ngoại lệ để một lỗi tra mã không làm hỏng toàn bộ kết quả, và ghi nhật ký thời gian xử lý của từng thực thể."),
  H4("3.4.6.4. Hai chế độ trả lời và danh sách top-k"),
  P("Nguyên tắc thà không gán mã còn hơn gán sai cho precision cao nhưng để trống nhiều thực thể. Vì nhu cầu của người dùng khác nhau, bộ điều phối cung cấp hai chế độ. Chế độ strict là chế độ mặc định, chỉ gán mã khi một trong các bước exact match, alias hoặc fuzzy matching có ràng buộc đưa ra quyết định. Ngược lại, chế độ always dùng quyết định đó nếu có và lấy candidate xếp hạng đầu khi không có, vì vậy chế độ này phù hợp khi luôn có người xác nhận phía sau."),
  P("Ở cả hai chế độ, mỗi thực thể CONDITION và DRUG còn mang một danh sách k candidate, mặc định k bằng 5, vì năm lựa chọn đủ ngắn để người nhập liệu đọc hết trong khi vẫn chứa mã đúng ở phần lớn trường hợp như Hình 4.5 cho thấy. Mỗi candidate có thứ hạng, mã, tên chuẩn, cách khớp và điểm. Candidate đầu tiên là quyết định của hệ thống nếu có. Với ICD-10, các candidate còn lại được xếp hạng bằng TF-IDF trên n-gram ký tự độ dài 2 đến 4, tính trên tên trong danh mục cộng với các alias và khử trùng theo mã. Cách này được chọn vì trên dev cho kết quả tốt hơn các độ đo so khớp mờ và n-gram từ. Với RxNorm, ứng viên được lấy từ dịch vụ tìm kiếm gần đúng của RxNav. Các ứng viên do bước xếp hạng sinh ra được đánh dấu là kết quả truy hồi, nên chế độ strict không bao giờ coi chúng là quyết định, như thể hiện ở Mã giả 3.4."),
  ...ALGO("Mã giả 3.4. Quyết định mã và danh sách top-k theo hai chế độ", "bộ chuẩn hóa N, tên thực thể m, số ứng viên k, chế độ mode", "mã được chọn hoặc NIL, cùng danh sách k ứng viên", [
    "function Decide(N, m, k, mode)",
    "  C ← N.Candidates(m, k)",
    "  if C = ∅ then",
    "    return (NIL, ∅)",
    "  end if",
    "  if mode = always or C₁.method ≠ retrieval then",
    "    return (C₁, C)",
    "  end if",
    "  return (NIL, C)",
    "end function",
  ]),
  DESC("Mã giả cho thấy điểm khác nhau duy nhất giữa hai chế độ là cách xử lý candidate do bước xếp hạng sinh ra."),
  H3("3.4.7. Trích xuất quan hệ"),
  H4("3.4.7.1. Lọc thực thể và sinh cặp"),
  P("Trước khi sinh cặp, bước RE đánh dấu các thực thể thuộc danh sách thực thể chung chung, tương ứng với bước kiểm tra thực thể của hướng dẫn gán nhãn ở mục 3.3.3.2. Các thực thể này vẫn có mặt trong đầu ra để chuẩn hóa và hiển thị, nhưng không tham gia sinh cặp, nhờ đó đầu vào của RE lúc suy luận khớp với quy ước của dữ liệu huấn luyện. Người dùng có thể tắt cơ chế này bằng một tham số khi cần."),
  P("Với mỗi đoạn văn bản, mọi cặp head và tail có kiểu trùng với một quan hệ trong lược đồ đều được sinh thành candidate, và chiều của cặp luôn được giữ đúng kể cả khi head đứng sau tail trong câu. Trước đó, hệ thống kiểm tra thực thể không trùng ID, có vị trí hợp lệ, thuộc lược đồ, có văn bản khớp với vị trí và không chồng lấn nhau. Mỗi cặp được biểu diễn bằng cách chèn entity marker có kèm loại thực thể quanh hai đầu mút. Các marker được chèn từ cuối câu về đầu câu để không làm lệch vị trí ký tự, như ví dụ dưới đây."),
  ...CODE(["[HEAD_CONDITION]đau[/HEAD] ở [TAIL_BODY_PART]vùng bụng[/TAIL], được điều trị bằng phẫu thuật."]),
  H4("3.4.7.2. Baseline rule-based"),
  P("Baseline rule-based được viết trực tiếp từ hướng dẫn gán nhãn và không được tinh chỉnh trên dữ liệu. Một cặp được dự đoán là có quan hệ khi thỏa đồng thời ba điều kiện. Điều kiện thứ nhất là khoảng cách giữa hai thực thể không vượt ngưỡng của quan hệ đó. Điều kiện thứ hai là đoạn chữ nằm giữa chứa một từ gợi ý của quan hệ, hoặc tail đứng ngay sau head đối với located_at và has_dosage. Điều kiện thứ ba là không có thực thể nào cùng loại với head hoặc tail chen vào giữa. Bảng 3.12 liệt kê tham số của từng quan hệ."),
  ...TB("Bảng 3.12. Khoảng cách tối đa và từ gợi ý của baseline rule-based cho từng quan hệ", T(["Quan hệ", "Khoảng cách tối đa tính bằng từ", "Từ gợi ý"], [
    ["located_at", "4", "ở, tại, vùng, trong, của, phía, bên, khu vực, chỗ, lan, hoặc liền kề"],
    ["treated_by", "8", "điều trị, chữa, trị, bằng, dùng, uống, tiêm, bôi, kê, cho thuốc, sử dụng"],
    ["treated_by_procedure", "8", "điều trị, chữa, trị, bằng, phương pháp, can thiệp, tiến hành, thực hiện, sử dụng"],
    ["diagnosed_by", "8", "chẩn đoán, phát hiện, xác định, cho thấy, thấy, qua, bằng, kiểm tra, tầm soát, làm"],
    ["has_dosage", "3", "Không có từ gợi ý, chỉ xét trường hợp liền kề"],
  ], [2400, 2000, 5238], { size: 20 }), "Bảng cho thấy rule-based chỉ dựa vào từ gợi ý và khoảng cách, nên dễ giải thích nhưng bỏ sót các cách nói không có từ gợi ý."),
  H4("3.4.7.3. Mô hình ViHealthBERT"),
  P("Mô hình RE dùng ViHealthBERT theo cách làm của Baldini Soares và cộng sự [11] cũng như Zhong và Chen [12]. Câu đã chèn ký hiệu đánh dấu thực thể được đưa vào bộ mã hóa, trong đó các ký hiệu theo loại thực thể được thêm vào từ vựng như các token đặc biệt. Biểu diễn của một cặp là phép nối hai vector trạng thái ẩn tại ký hiệu mở đầu của thực thể đầu và của thực thể đuôi, sau đó đi qua dropout và một lớp tuyến tính phân loại hai lớp. Vì mỗi kiểu cặp chỉ có một quan hệ hợp lệ, lớp dương chính là quan hệ đó. Mô hình được huấn luyện và đánh giá trên các cặp có hai thực thể hợp lệ, tức là mô hình được đặt sau một bộ lọc thực thể đúng như bước thứ nhất của hướng dẫn gán nhãn."),
  P(`Các siêu tham số được cố định trước và dùng chung cho mọi cấu hình, gồm 10 epoch, tốc độ học 3·10⁻⁵, kích thước lô 16, khởi động tốc độ học trong 10% số bước đầu, weight decay 0,01, độ dài tối đa 192 token và trọng số lớp bằng tỉ lệ cặp âm trên cặp dương. Các giá trị này lấy theo công thức huấn luyện đã dùng ở giai đoạn trước và không được tinh chỉnh trên tập kiểm định hay tập kiểm tra, vì tập kiểm định chỉ có ${rxSel.pairs} cặp. Mỗi cấu hình được huấn luyện với ba seed là ${rxSel.seeds.join(", ")}, xác suất của ba mô hình được lấy trung bình, và cặp được dự đoán dương khi xác suất trung bình đạt từ 0,5 trở lên. Lấy trung bình ba seed giúp giảm dao động do khởi tạo ngẫu nhiên, vốn lớn khi dữ liệu nhỏ, còn ngưỡng 0,5 tương ứng với việc mô hình đánh giá khả năng có quan hệ cao hơn khả năng không có.`),
  H4("3.4.7.4. Chọn cấu hình và chống rò rỉ"),
  P(`Năm cấu hình dữ liệu được so sánh. Cấu hình x0 chỉ dùng dữ liệu thật. Hai cấu hình x1 và x3 thêm dữ liệu sinh chưa kiểm tra bằng một lần và ba lần số cặp thật. Hai cấu hình v1 và vall thêm dữ liệu sinh đã kiểm tra ở mục 3.3.3.7, lần lượt bằng một lần số cặp thật và bằng toàn bộ kho. Quy tắc chọn được đặt trước khi chạy, theo đó cấu hình có macro-F1 cao nhất trên tập kiểm định được chọn, tính trên các quan hệ có cặp dương trong tập kiểm định, và nếu bằng nhau thì chọn cấu hình dùng ít dữ liệu sinh hơn. Hai cấu hình v1 và vall được thêm vào sau khi x1 đã được chấm trên tập kiểm tra, nên tập kiểm tra không còn hoàn toàn chưa được nhìn thấy. Để hạn chế ảnh hưởng này, quy tắc chọn được giữ nguyên như ban đầu. Macro-F1 được dùng thay cho micro-F1 vì located_at chiếm phần lớn số cặp, nên micro-F1 gần như chỉ phản ánh quan hệ này. Kết quả trên tập kiểm tra của cấu hình được chọn là kết quả chính, còn kết quả của các cấu hình khác chỉ được nêu để so sánh.`),
  P(`Về rò rỉ, câu của ba tập được kiểm tra trùng cả nguyên câu lẫn chuỗi ${RX.sel.leak_ngram} từ liên tiếp, và dữ liệu sinh chỉ được tạo từ câu huấn luyện. Khoảng tin cậy 95% của mọi F1 được tính bằng bootstrap 2.000 lần theo câu, vì các cặp trong cùng một câu không độc lập với nhau. Trong hệ thống, mô hình được nạp cùng ba seed như khi chấm và nhận các cặp ứng viên sau bước lọc thực thể. Hệ thống vẫn cho phép hợp mô hình với rule-based, nhưng vì cách hợp không cải thiện kết quả trên tập kiểm tra như trình bày ở mục 4.3.2, mô hình được dùng đứng một mình.`),
  H3("3.4.8. Định dạng đầu ra"),
  P("Kết quả của hệ thống là một bản ghi JSON. Bản ghi gồm văn bản gốc và danh sách thực thể, trong đó mỗi thực thể có chuỗi bề mặt, loại, vị trí bắt đầu và kết thúc, độ tin cậy, kết quả chuẩn hóa và dấu hiệu bị loại khỏi RE nếu có. Khi chạy RE, bản ghi có thêm danh sách quan hệ dương, danh sách mọi cặp candidate kèm nhãn, điểm và trạng thái, cùng phần thông tin mô tả nguồn nhãn và các quan hệ được hỗ trợ. Ví dụ 3.1 là một lượt chạy thật trên một câu ngắn."),
  ...CODE([`Văn bản: "${demo.text}"`, ...demo.entities.map((e) => `  ${e.id} [${e.label}] "${e.surface_text}" (${e.start_char}–${e.end_char}, conf=${e.confidence})${e.re_excluded ? "  ← bỏ qua khi sinh cặp (thực thể chung)" : ""}`),
    ...demo.relation_candidates.map((c) => `  Cặp ${c.head}, ${c.tail} (${c.allowed_relation}): ${c.label}${c.score !== undefined && c.score !== null ? ", score=" + Number(c.score).toFixed(3) : ""}`)]),
  CAP("Ví dụ 3.1. Đầu ra của pipeline NER và RE trên một câu ngắn"),
  P("Trong ví dụ này, thực thể “điều trị” bị loại khỏi bước sinh cặp vì là thực thể chung chung, nên hệ thống trả về đúng hai quan hệ mong đợi. Đây chỉ là một ví dụ minh họa, không phải bằng chứng thống kê. Cùng định dạng bản ghi này được dùng cho giao diện minh họa và cho bước dựng đồ thị tri thức, nên kết quả hiển thị ở mọi nơi đều thống nhất."),
  H3("3.4.9. Kiểm thử phần mềm"),
  P(`Hệ thống có bộ kiểm thử tự động gồm ${nTests} ca, bao phủ từng thành phần. Phần NER được kiểm thử ở các khía cạnh tách từ, dấu câu, ánh xạ sáu nhãn, cụm liều lượng, câu rỗng và văn bản dài. Phần chuẩn hóa được kiểm thử với các ca dễ nhầm như “đau bụng” và “đau lưng”, các ca tập con khác nghĩa, tra RxNorm khi không có kết nối mạng và hai chế độ trả lời. Phần RE được kiểm thử về vị trí, chiều và ID của cặp, việc chia nhóm không rò rỉ, việc lọc thực thể chung chung, cách tính chỉ số và việc nạp mô hình ViHealthBERT đã lưu. Ngoài ra còn có các ca kiểm thử cho phép tính chỉ số đánh giá, đồ thị tri thức và giao diện minh họa. Phụ lục F tổng hợp số ca theo từng nhóm.`),
  H3("3.4.10. Các quyết định thiết kế quan trọng"),
  P("Trong quá trình xây dựng, khóa luận gặp một số vấn đề ảnh hưởng tới thiết kế. Bảng 3.13 tóm tắt các vấn đề đó cùng quyết định tương ứng."),
  H3("3.4.11. Knowledge graph"),
  P("Knowledge graph là bước cuối của pipeline. Kết quả của mỗi văn bản là một danh sách bộ ba gồm thực thể đầu, quan hệ và thực thể cuối, và đồ thị gộp các bộ ba của mọi văn bản lại sao cho cùng một khái niệm chỉ ứng với một nút, dù được nói theo nhiều cách khác nhau. Ví dụ, câu “tiểu đường uống metformin” và câu “đái tháo đường dùng metformin” cùng tạo ra một cạnh treated_by nối nút ICD-10 E14 với nút RxNorm 6809, với số lần xuất hiện bằng 2. Bảng 3.14 mô tả các thành phần của đồ thị."),
  ...TB("Bảng 3.13. Các vấn đề gặp phải và quyết định thiết kế tương ứng", T(["Vấn đề gặp phải", "Quyết định"], [
    ["Mô hình tự tin gán “bệnh nhân” là OCCUPATION", "Loại hẳn các loại phi y khoa thay vì giữ một nhãn chung"],
    ["Tách từ theo khoảng trắng làm dấu câu dính vào thực thể", "Tách token bằng biểu thức chính quy, mỗi dấu câu là một token riêng"],
    ["Token đặc biệt mang nhãn ngẫu nhiên", "Loại các vị trí đặc biệt trước khi giải mã BIO"],
    ["Fuzzy matching ICD-10 với ngưỡng 0,6 gán sai nghiêm trọng", "Nâng ngưỡng lên 0,85, thêm từ điển alias và các ràng buộc an toàn"],
    ["Nhãn LLM có thể bị nhầm là gold", "Đánh dấu nguồn nhãn và chỉ cho dùng nhãn LLM khi người dùng chủ động bật"],
    ["Thực thể sai kiểu chiếm gần một nửa cặp âm của dữ liệu quan hệ cũ", "Bỏ nhãn quan hệ cũ, gán lại theo hướng dẫn hai bước có bước kiểm tra thực thể"],
  ], [4600, 5038], { size: 20 }), "Bảng giúp người đọc hiểu lý do đằng sau các lựa chọn thiết kế không hiển nhiên trong hệ thống."),
  P("Đồ thị được hiển thị trên một trang web tương tác. Trang có bộ lọc theo quan hệ và theo số lần xuất hiện tối thiểu, ô tìm kiếm, và bảng chi tiết hiện câu nguồn khi người dùng bấm vào một nút hoặc một cạnh. Nút chưa có mã được vẽ viền đứt và cạnh chỉ do rule-based sinh ra được vẽ nét đứt, để người xem phân biệt phần chắc chắn với phần cần kiểm tra. Đồ thị có thể được dựng từ dữ liệu VietMed-NER hoặc từ bất kỳ tập văn bản nào."),
  ...TB("Bảng 3.14. Các thành phần thiết kế của knowledge graph", T(["Thành phần", "Cách làm"], [
    ["Khóa của nút", "Dùng danh mục kèm mã khi chuẩn hóa có quyết định, ví dụ ICD-10:E14, nếu không thì dùng loại kèm chữ đã chuẩn hóa, ví dụ BODY_PART:xương. Candidate gợi ý không bao giờ được dùng làm khóa để tránh gộp sai"],
    ["Thuộc tính nút", "Tên hiển thị là tên chuẩn nếu có mã, các cách viết đã gặp kèm số lần, số đề cập, số văn bản và mã gợi ý"],
    ["Cạnh", "Gộp theo bộ ba, lưu số lần xuất hiện, số văn bản, số lần theo nguồn mô hình hoặc rule-based, điểm trung bình và tối đa ba câu ví dụ"],
    ["Lọc", "Bỏ các CONDITION chung chung như “bệnh”, “triệu chứng” hay “biến chứng” để chúng không trở thành nút trung tâm giả"],
    ["Truy vấn và xuất", "Hỗ trợ tìm nút lân cận, tìm theo chữ và thống kê, xuất ra các định dạng dữ liệu phổ biến và một trang web tương tác"],
  ], [2200, 7438], { size: 20 }), "Bảng giải thích cách đồ thị gộp các cách nói khác nhau về cùng một nút và lưu lại nguồn gốc của từng cạnh."),
  H3("3.4.12. Giao diện minh họa"),
  P("Để người dùng không cần viết mã vẫn thử được hệ thống, khóa luận xây dựng một giao diện web gồm hai phần. Phần máy chủ nạp toàn bộ luồng xử lý một lần khi khởi động, gồm NER, chuẩn hóa ICD-10 và RxNorm cùng RE bằng ViHealthBERT, rồi nhận đoạn văn bản tối đa 2.000 ký tự và trả về kết quả có cấu trúc kèm thời gian xử lý. Phần giao diện là một trang web hiển thị kết quả đó."),
  ...FIG("h3_3_giao_dien.png", "Hình 3.6. Giao diện minh họa khi phân tích một câu nhập tự do, gồm văn bản tô màu thực thể, bảng mã chuẩn hóa và danh sách quan hệ", "Hình cho thấy cách hệ thống trình bày kết quả cho người dùng cuối, trong đó mỗi quan hệ đều ghi rõ nguồn dự đoán."),
  P("Trang kết quả có ba phần như Hình 3.6. Phần thứ nhất tô màu từng thực thể ngay trong văn bản theo sáu loại, trong đó thực thể chung chung bị loại khỏi RE được hiển thị mờ. Phần thứ hai là bảng thực thể với độ tin cậy, mã chuẩn, tên chuẩn, cách khớp và danh sách mã gợi ý. Phần thứ ba liệt kê các quan hệ cùng nguồn dự đoán và điểm số. Trên máy thực nghiệm, mô hình nạp trong khoảng 26 giây và mỗi câu được xử lý trong khoảng 0,4 đến 2,7 giây trên CPU."),
);

// ===== CHƯƠNG 4 (viết lại 12/11/2026: văn liền mạch, hình thay bảng dày, ghi chú mục đích dưới mỗi bảng/hình) =====
const tpAll = (m) => LABELS6.reduce((a, k) => a + m[k].tp, 0);
const ablNames = { full: "Pipeline đầy đủ", no_dosage: "Bỏ luật liều lượng", no_rules: "Bỏ nhóm luật hậu xử lý", model_only: "Chỉ dùng mô hình" };
const ablData = abl ? { full: nerNew.t2, ...abl } : null;
const ablF = (k, lab = "micro avg") => ablData[k].strict_exact_match[lab]["f1-score"];
const sgn = (x, d = 4) => `${x >= 0 ? "tăng" : "giảm"} ${f(Math.abs(x), d)}`;
const NORM_M = [["exact", "Exact match với tên danh mục"], ["fuzzy1", "Fuzzy matching không ràng buộc"], ["system", "Hệ thống, chế độ strict"], ["always", "Hệ thống, chế độ always"]];
const BN = (m) => bench.names[m].replace(" ∪ luật", " hợp với rule-based").replace("Luật từ hướng dẫn", "Rule-based").replace(" (mọi cặp đúng kiểu)", "");
const kgSrc = (rel, src) => kgRel(rel).reduce((a, e) => a + (e.sources[src] || 0), 0);
const kgOcc = (rel) => kgRel(rel).reduce((a, e) => a + e.count, 0);
const SRC_VN = { model: "mô hình", rule: "luật" };
const trainPosLoc = relCount(re2.final_model.labels, "located_at") / (re2.final_model.pairs - relCount(re2.final_model.labels, "NO_RELATION"));
add(
  H1("CHƯƠNG 4. KẾT QUẢ VÀ THẢO LUẬN"),
  SUM("Chương này gồm hai phần. Phần đầu, từ mục 4.1 đến mục 4.5, trình bày kết quả đánh giá từng thành phần theo đúng thứ tự xử lý của hệ thống, bắt đầu từ NER, tiếp đến chuẩn hóa mã, RE, kiểm thử và cuối cùng là knowledge graph. Ở mỗi mục, kết quả của hệ thống luôn được đặt cạnh các baseline chạy trên cùng dữ liệu, nhờ đó người đọc thấy được mỗi thành phần thực sự đóng góp bao nhiêu. Phần sau gồm mục 4.6 phân tích lỗi của từng thành phần và mục 4.7 trả lời các câu hỏi nghiên cứu, thảo luận độ tin cậy của đánh giá và khả năng ứng dụng."),
  H2("4.1. Kết quả NER"),
  H3("4.1.1. Mô hình gốc trên 18 loại thực thể"),
  P(`Trước khi xét toàn pipeline, khóa luận chấm riêng đầu ra của checkpoint trên ${nTypes} loại thực thể gốc của VietMed-NER, khi chưa ánh xạ và chưa áp luật. Ở mức này mô hình đạt micro-F1 ${f(t1["micro avg"]["f1-score"])} với precision ${f(t1["micro avg"].precision)} và recall ${f(t1["micro avg"].recall)} trên ${n(t1["micro avg"].support)} thực thể gold. Hình 4.1 cho thấy chất lượng chênh lệch rất lớn giữa các loại, vì vậy cần nhìn theo từng loại thay vì chỉ dựa vào con số gộp.`),
  ...FIG("h4_1_ner_18_loai.png", "Hình 4.1. F1 của mô hình gốc trên từng loại trong 18 loại thực thể của VietMed-NER, trong đó các loại được ánh xạ sang lược đồ của khóa luận được tô màu xanh", "Hình dùng để chỉ ra các loại gốc yếu nhất và giải thích vì sao một số loại mục tiêu, đặc biệt là PROCEDURE, có kết quả thấp ở bước sau."),
  P(`Các loại y khoa có nhiều mẫu như DRUGCHEMICAL, DISEASESYMTOM và ORGAN đạt F1 lần lượt ${f(t1.DRUGCHEMICAL["f1-score"], 2)}, ${f(t1.DISEASESYMTOM["f1-score"], 2)} và ${f(t1.ORGAN["f1-score"], 2)}. Ngược lại, PREVENTIVEMED chỉ đạt ${f(t1.PREVENTIVEMED["f1-score"], 2)} vì có vỏn vẹn ${t1.PREVENTIVEMED.support} mẫu, còn MEDDEVICETECHNIQUE và SURGERY chỉ đạt ${f(t1.MEDDEVICETECHNIQUE["f1-score"], 2)} và ${f(t1.SURGERY["f1-score"], 2)}. Cả hai loại sau đều được gộp vào PROCEDURE, nên điểm yếu của chúng được kế thừa trực tiếp sang loại mục tiêu này.`),

  H3("4.1.2. Toàn pipeline trên sáu loại mục tiêu"),
  P(`Khi chạy toàn bộ pipeline gồm mô hình, luật liều lượng và hậu xử lý, hệ thống đạt strict micro-F1 ${f(s["micro avg"]["f1-score"])} và relaxed micro-F1 ${f(r["micro avg"]["f1-score"])} trên tập test. Hình 4.2 đặt hai cách chấm cạnh nhau cho từng loại để làm rõ phần chênh lệch giữa chúng.`),
  ...FIG("h4_2_ner_strict_relaxed.png", "Hình 4.2. F1 của toàn pipeline theo sáu loại thực thể mục tiêu khi chấm theo strict match và relaxed match", "Hình cho biết lỗi của từng loại chủ yếu là sai ranh giới span hay là nhận sai thực thể."),
  P(`TEST và DRUG có strict F1 cao nhất, trong khi DOSAGE và PROCEDURE thấp nhất. Khoảng cách giữa hai cách chấm khá lớn, bởi khi chuyển từ khớp chặt sang khớp nới lỏng thì số dự đoán đúng tăng từ ${n(tpAll(s))} lên ${n(tpAll(r))}. Điều này cho thấy nhiều lỗi chỉ là lệch ranh giới span, còn loại thực thể vẫn được nhận đúng. Riêng DRUG có recall rất cao là ${f(s.DRUG.recall, 2)} nhưng precision chỉ đạt ${f(s.DRUG.precision, 2)}, do mô hình còn gán DRUG cho nhiều cụm thực phẩm hoặc sản phẩm chăm sóc cá nhân mà nhãn gold xếp vào các loại đã bị loại khỏi lược đồ.`),
  P("Để biết lỗi rơi vào đâu, Hình 4.3 trình bày confusion matrix, trong đó mỗi thực thể dự đoán được ghép với thực thể gold có phần giao lớn nhất. Hàng cuối ứng với dự đoán thừa và cột cuối ứng với thực thể gold bị bỏ sót."),
  ...FIG("h4_3b_ma_tran_nham_lan.png", "Hình 4.3. Confusion matrix giữa sáu loại thực thể mục tiêu trên tập test, kèm hàng và cột cho trường hợp không có thực thể tương ứng", "Hình dùng để phân biệt lỗi nhầm giữa hai loại thực thể với lỗi bỏ sót hoặc dự đoán thừa, màu được tô theo thang logarit để các ô nhỏ vẫn nhìn thấy được.", 500),
  P("Phần lớn lỗi nằm ở hàng cuối, tức là các cụm hệ thống nhận là thực thể trong khi nhãn gold không gán, và lỗi này trải đều trên mọi loại. Giữa các loại y khoa, có hai cặp nhầm nổi bật. Cặp thứ nhất là CONDITION với BODY_PART, phát sinh khi cụm bệnh chứa tên bộ phận cơ thể như “viêm nội mạc tử cung”. Cặp thứ hai là PROCEDURE với DRUG, phản ánh ranh giới mờ giữa thuốc và phương pháp điều trị trong nhãn gốc TREATMENT. Mục 4.6.1 sẽ phân tích các trường hợp này bằng ví dụ cụ thể."),

  H3("4.1.3. Ablation các luật NER"),
  P("Để trả lời câu hỏi nghiên cứu thứ ba, pipeline được chạy lại trên cùng tập test trong khi lần lượt tắt từng nhóm luật. Mọi cấu hình vẫn giữ bước lọc lược đồ và giải quyết chồng lấn, và không có điều chỉnh nào được thực hiện dựa trên kết quả này. Bảng 4.1 so sánh bốn cấu hình."),
  ...(ablData ? [
    ...TB("Bảng 4.1. Kết quả NER khi lần lượt tắt từng nhóm luật trên tập test", T(["Cấu hình", "P khớp chặt", "R khớp chặt", "F1 khớp chặt", "F1 khớp nới lỏng", "Chênh F1 khớp chặt so với đầy đủ"], Object.keys(ablNames).filter((k) => ablData[k]).map((k) => { const a = ablData[k].strict_exact_match["micro avg"], b = ablData[k].relaxed_overlap_match["micro avg"]; const d = a["f1-score"] - s["micro avg"]["f1-score"]; return [ablNames[k], f(a.precision), f(a.recall), f(a["f1-score"]), f(b["f1-score"]), k === "full" ? "" : `${d >= 0 ? "+" : "−"}${f(Math.abs(d))}`]; }), [2600, 1200, 1200, 1200, 1300, 2138], { right: [1, 2, 3, 4, 5], size: 20 }), "Bảng dùng để đo đóng góp riêng của luật liều lượng và của nhóm luật hậu xử lý so với khi chỉ dùng mô hình."),
    P(`Kết quả cho thấy các luật gần như không làm thay đổi điểm số tổng thể. So với khi chỉ dùng mô hình, pipeline đầy đủ chỉ làm strict micro-F1 ${sgn(ablF("full") - ablF("model_only"))}. Luật liều lượng hầu như không có tác dụng, vì trên toàn tập test nó chỉ thêm ${s.DOSAGE.tp - abl.no_dosage.strict_exact_match.DOSAGE.tp} dự đoán đúng và ${s.DOSAGE.fp - abl.no_dosage.strict_exact_match.DOSAGE.fp} dự đoán sai cho DOSAGE. Nguyên nhân là văn bản lời nói gần như không chứa cụm liều đầy đủ kiểu “500mg 2 viên/ngày” mà luật được thiết kế để bắt, trong khi phần lớn DOSAGE trong nhãn gold chỉ là đơn vị đo chung.`),
    P(`Nhóm luật hậu xử lý lại tác động ngược chiều giữa các loại. Luật bỏ các từ hành động bị gán nhầm là thuốc giúp strict F1 của DRUG ${sgn(ablF("full", "DRUG") - ablF("no_rules", "DRUG"))}. Trong khi đó, luật gộp các từ chỉ mức độ như “cao” hay “nặng” vào CONDITION đứng trước lại làm DOSAGE ${sgn(ablF("full", "DOSAGE") - ablF("no_rules", "DOSAGE"))} và CONDITION ${sgn(ablF("full", "CONDITION") - ablF("no_rules", "CONDITION"))}, bởi nhãn gold của VietMed-NER xếp các từ này vào UNITCALIBRATOR. Đây là ví dụ rõ về một luật hợp lý về mặt ngữ nghĩa nhưng vẫn bị phạt vì lệch với quy ước của bộ dữ liệu.`),
  ] : [NOTE("[[Kết quả ablation chưa có khi dựng báo cáo.]]")]),

  H3("4.1.4. Thời gian xử lý"),
  P(`Khi xử lý tuần tự từng câu trên CPU và tắt bước chuẩn hóa, pipeline NER cần trung bình ${f(nerNew.lat.mean_latency_ms, 1)} ms cho mỗi câu, với trung vị ${f(nerNew.lat.median_latency_ms, 1)} ms và phân vị 95 là ${f(nerNew.lat.p95_latency_ms, 1)} ms. Toàn bộ ${n(nerNew.lat.total_samples)} câu test được xử lý trong ${f(nerNew.lat.total_time_seconds, 0)} giây. Tốc độ này đủ cho việc phân tích tương tác từng văn bản, còn khi xử lý hàng loạt lớn thì nên chạy theo lô trên GPU. Đây là số đo trên một máy cá nhân nên chỉ mang tính tham khảo, không phải cam kết về hiệu năng.`),

  ...(nerBase && nerInh ? [
    H3("4.1.5. So sánh với baseline NER"),
    P(`Để đặt checkpoint vào đúng bối cảnh, khóa luận huấn luyện thêm hai baseline trên split train, chọn siêu tham số trên split validation và chỉ chấm split test một lần. Baseline từ điển gán nhãn bằng cách khớp dài nhất với ${n(nerBase.dictionary.params.entries)} cụm thực thể đã gặp trong train. Baseline CRF dùng đặc trưng âm tiết, hình dạng chữ, tiền tố, hậu tố và cửa sổ hai từ mỗi bên. Checkpoint ViHealthBERT được chấm bằng cùng một hàm, chỉ với phần mô hình và không có luật hậu xử lý. Hình 4.4 so sánh ba mô hình trên từng loại mục tiêu.`),
    ...FIG("h4_3_ner_baseline.png", "Hình 4.4. F1 của baseline từ điển, CRF và ViHealthBERT trên sáu loại thực thể mục tiêu, kèm micro-F1 và khoảng tin cậy 95%", "Hình dùng để kiểm tra mô hình ngôn ngữ có thực sự tốt hơn các phương pháp dựa trên từ vựng ở từng loại thực thể hay không."),
    P(`Trên sáu loại mục tiêu, ViHealthBERT vượt rõ cả hai baseline với micro-F1 ${f(nerInh.scores.test.target.micro.f1, 3)}, so với ${f(nerBase.dictionary.test.target.micro.f1, 3)} của từ điển và ${f(nerBase.crf.test.target.micro.f1, 3)} của CRF, và các khoảng tin cậy không chồng lên nhau. Ưu thế này đến từ recall, vốn đạt ${f(nerInh.scores.test.target.micro.recall, 3)} so với ${f(nerBase.dictionary.test.target.micro.recall, 3)} và ${f(nerBase.crf.test.target.micro.recall, 3)} ở hai baseline, bởi mô hình ngôn ngữ nhận ra được cả những cách nói chưa từng xuất hiện trong train. Đổi lại, precision của ViHealthBERT thấp hơn. Ngoại lệ duy nhất là TEST, nơi từ điển đạt F1 cao nhất là ${f(nerBase.dictionary.test.target.report.TEST["f1-score"], 3)}, vì tên xét nghiệm thuộc một tập từ vựng nhỏ và lặp lại nhiều.`),
    P(`Khi chấm trên ${nTypes} loại gốc, bức tranh lại khác. Từ điển đạt micro-F1 ${f(nerBase.dictionary.test.raw.micro.f1, 3)}, ngang với ${f(nerInh.scores.test.raw.micro.f1, 3)} của ViHealthBERT, do các loại phi y khoa như giới tính, tuổi hay nghề nghiệp chiếm nhiều mẫu và gần như luôn là cùng một nhóm từ quen thuộc như “bệnh nhân” hay “tháng”. Con số gộp trên ${nTypes} loại vì vậy che mất khoảng cách thật ở phần y khoa, và đây cũng là lý do khóa luận báo cáo ở cấp sáu loại mục tiêu.`),
    P(`So sánh này còn giải thích một điểm về mô hình kế thừa. Checkpoint đạt micro-F1 ${f(nerInh.scores.validation.raw.micro.f1, 3)} trên validation nhưng chỉ ${f(nerInh.scores.test.raw.micro.f1, 3)} trên test, nên có thể đặt câu hỏi liệu mô hình đã được chọn trên validation hay chưa. Tuy nhiên, hai baseline chỉ học trên train cũng giảm mạnh tương tự, khi từ điển giảm từ ${f(nerBase.dictionary.validation_micro_f1, 3)} xuống ${f(nerBase.dictionary.test.raw.micro.f1, 3)} và CRF giảm từ ${f(nerBase.crf.validation_micro_f1, 3)} xuống ${f(nerBase.crf.test.raw.micro.f1, 3)}. Nguyên nhân nằm ở chỗ split validation của VietMed-NER rất gần train, khi 7,5% câu validation có chung một cụm tám từ với train, trong khi tỉ lệ này ở test chỉ là 0,3%. Chênh lệch vì vậy đến từ phân bố dữ liệu chứ không phải từ rò rỉ, và đây cũng là lý do khóa luận luôn báo cáo kết quả trên test.`),
  ] : []),

  H2("4.2. Kết quả chuẩn hóa mã"),
  H3("4.2.1. Khảo sát ban đầu và bản sửa lỗi"),
  P(`Khi chưa có tập đánh giá chuẩn hóa riêng, bộ chuẩn hóa được thử trên ${icdBefore.condition_mentions} đề cập CONDITION trong 600 đoạn lấy từ split train để khảo sát, gọi là bộ 600 đoạn khảo sát, và từng mã gán ra được kiểm tra thủ công. Phiên bản ban đầu gán mã cho ${icdBefore.coded_mentions} đề cập, trong đó có ${icdBefore.wrong_mentions} mã sai và ${icdBefore.doubt_mentions} mã nghi vấn. Bảng 4.2 liệt kê các trường hợp này.`),
  P(`Như Bảng 4.2 cho thấy, tất cả các mã sai đều đến từ bước fuzzy matching. Bản sửa vì vậy bổ sung hai ràng buộc an toàn cho bước này như đã trình bày ở Bảng 3.11, cùng sáu alias mới. Chỉ riêng hai ràng buộc đã chặn được toàn bộ mã sai kể cả khi chưa có alias. Sau khi sửa, hệ thống gán mã cho ${icd.coded_mentions} đề cập, trong đó ${icd.wrong_mentions ? `còn ${icd.wrong_mentions} mã sai` : "không còn mã sai nào"} và chỉ còn ${icd.doubt_mentions} mã nghi vấn. Vì các tên gọi khác được rút ra từ chính bộ khảo sát, khóa luận xây dựng thêm một tập đánh giá chuẩn hóa riêng để đánh giá khách quan hơn ở mục 4.2.2.`),
  H3("4.2.2. Đánh giá trên tập gold chuẩn hóa"),
  P("Trên tập gold chuẩn hóa, mọi cải tiến gồm 137 alias ICD-10, 31 alias thuốc, ràng buộc phủ từ, bước tìm kiếm gần đúng của RxNav và cách xếp hạng candidate top-k đều được chọn khi chỉ nhìn vào dev. Tập test chỉ được chạy một lần sau khi mọi lựa chọn đã chốt. Mỗi dạng bề mặt được tính một lần, và hệ thống được so với hai baseline là exact match với tên danh mục và fuzzy matching không ràng buộc. Bảng 4.3 trình bày kết quả của cả hai danh mục."),
  ...TB("Bảng 4.2. Các mã ICD-10 sai hoặc nghi vấn ở phiên bản chuẩn hóa ban đầu", T(["Tên bệnh", "Số lần", "Mã gán", "Tên chuẩn của mã gán", "Đánh giá"], icdBefore.items.filter((o) => o.verdict !== "hợp lý").map((o) => { const m = String(o.note).match(/đúng (?:ra |là )?([A-Z]\d{2}(?:\.\d)?)/); return [o.text, o.mentions, o.code, o.label, `${o.verdict[0].toUpperCase()}${o.verdict.slice(1)}${m ? `, mã phù hợp là ${m[1]}` : ""}`]; }), [2100, 900, 1100, 2900, 2638], { right: [1] }), "Bảng dùng để chỉ ra rằng mọi lỗi gán mã đều xuất phát từ bước fuzzy matching, từ đó định hướng cho bản sửa."),

  P(`Ở chế độ strict, hệ thống đạt Accuracy ${rp(nc("ICD-10").system.accuracy)} với ICD-10, cao gấp khoảng ${(nc("ICD-10").system.accuracy / nc("ICD-10").exact.accuracy).toFixed(0)} lần exact match và gần gấp đôi fuzzy matching không ràng buộc. Điểm quan trọng hơn là precision khi trả lời đạt ${rp(nc("ICD-10").system.precision_answered)} và hệ thống từ chối đúng ${pct(nc("ICD-10").system.nil_correct_abstention)} dạng NIL, trong khi fuzzy matching không ràng buộc chỉ có precision ${rp(nc("ICD-10").fuzzy1.precision_answered)}, tức là sai nhiều hơn đúng. Chế độ always nâng Accuracy lên ${rp(nc("ICD-10").always.accuracy)} nhưng phải gán mã cho mọi dạng NIL. Với RxNorm, hệ thống đạt Accuracy ${rp(nc("RxNorm").system.accuracy)} theo dạng và ${rp(ncm("RxNorm").system.accuracy)} theo đề cập, vì các thuốc phổ biến như vitamin, canxi hay sắt đều tra được, còn phần khó là tên thảo dược và thực phẩm chức năng. Trên toàn bộ tập test, chế độ strict chỉ gán sai ${normA.test.system_wrong_links.length} dạng, trong đó có “protein” và “gel” vốn không phải tên thuốc.`),
  P("Nếu hệ thống được dùng để gợi ý mã cho người nhập liệu thay vì tự quyết định, danh sách ứng viên trở nên quan trọng hơn mã đứng đầu. Hình 4.5 biểu diễn tỉ lệ mã đúng nằm trong k ứng viên đầu tiên khi k tăng dần."),
  P(`Với mười ứng viên, mã ICD-10 đầy đủ có mặt trong ${pct(nc("ICD-10").top10_acc)} trường hợp, còn ở mức nhóm ba ký tự tỉ lệ này đạt ${pct(nc("ICD-10", "test", normA, "category").top10_acc)}. Đường của RxNorm gần như nằm ngang sau Top-3, vì danh sách ứng viên từ RxNav thường đã chứa đúng hoạt chất ở các vị trí đầu. Kết quả này cho thấy kịch bản gợi ý mã để người dùng chọn phù hợp với hệ thống hơn kịch bản tự động gán mã.`),
  P("Một kết quả khác cần lưu ý là khoảng cách lớn giữa dev và test. Hình 4.6 so sánh Accuracy trước và sau bản cải tiến trên hai tập này."),
  ...TB("Bảng 4.3. Kết quả chuẩn hóa ICD-10 và RxNorm trên tập test so với hai baseline", T(["Danh mục", "Phương pháp", "Accuracy", "Khoảng tin cậy 95%", "Coverage", "Precision khi trả lời", "Từ chối đúng NIL"], ["ICD-10", "RxNorm"].flatMap((o) => NORM_M.map(([k, lab]) => [o, lab, rp(nc(o)[k].accuracy), ci2(nci(o, `${k}.accuracy`)), rp(nc(o)[k].coverage), rp(nc(o)[k].precision_answered), rp(nc(o)[k].nil_correct_abstention)])), [1100, 2500, 1000, 1500, 900, 1300, 1338], { size: 19, right: [2, 4, 5, 6] }), "Bảng dùng để so sánh mức đánh đổi giữa coverage và precision của hai chế độ trả lời với các phương pháp đơn giản."),
  ...FIG("h4_4_chuan_hoa_topk.png", "Hình 4.5. Tỉ lệ mã đúng nằm trong k ứng viên đầu tiên của ICD-10 và RxNorm trên tập test", "Hình dùng để đánh giá khả năng dùng hệ thống như một công cụ gợi ý mã, khi người dùng được chọn trong danh sách ứng viên.", 460),
  ...FIG("h4_5_chuan_hoa_dev_test.png", "Hình 4.6. Accuracy của chế độ strict trước và sau bản cải tiến trên dev và test", "Hình dùng để kiểm tra mức cải thiện đo trên dev có còn giữ được khi chuyển sang tập test chưa từng dùng để chọn cải tiến hay không."),
  P(`Với ICD-10, Accuracy sau cải tiến đạt ${rp(nc("ICD-10", "dev").system.accuracy)} trên dev nhưng chỉ ${rp(nc("ICD-10").system.accuracy)} trên test. Có hai nguyên nhân cộng dồn. Thứ nhất, từ điển alias được lấy từ các dạng có trong train và dev. Thứ hai, bản thân split validation rất gần train như đã phân tích ở mục 4.1.5, nên dev ước lượng quá cao khả năng gặp lại cách nói đã biết. Vì vậy, con số cần trích dẫn là con số trên test. Dù vậy, cải tiến vẫn có ích thật sự khi Accuracy trên test tăng từ ${rp(nc("ICD-10", "test", normB).system.accuracy)} lên ${rp(nc("ICD-10").system.accuracy)} với ICD-10 và từ ${rp(nc("RxNorm", "test", normB).system.accuracy)} lên ${rp(nc("RxNorm").system.accuracy)} với RxNorm. Trong 137 tên gọi khác mới, có 48 tên cũng xuất hiện trong test vì có mặt ở cả train và dev.`),

  H2("4.3. Kết quả trích xuất quan hệ"),
  H3("4.3.1. Chọn cấu hình trên tập kiểm định"),
  P(`Bảng 4.4 so sánh năm cấu hình dữ liệu trên tập kiểm định, với macro-F1 tính trên ${rxSel.macro_over.join(", ")}, ba quan hệ có cặp dương trong tập này.`),
  P(`Cấu hình vall, dùng toàn bộ dữ liệu sinh đã kiểm tra, có macro-F1 cao nhất với ${rp(rxSel.macro_f1)} và được chọn. Ở cùng số cặp sinh, dữ liệu đã kiểm tra cho macro-F1 ${rp(rxDev.v1.macro_f1)}, so với ${rp(rxDev.x1.macro_f1)} của dữ liệu chưa kiểm tra. Tuy vậy, chênh lệch giữa các cấu hình chỉ là vài cặp trên ${rxSel.micro.tp + rxSel.micro.fn} cặp dương của tập kiểm định, nên chưa thể kết luận dữ liệu sinh hay bước kiểm tra thực sự có ích. Thêm dữ liệu sinh chưa kiểm tra gấp ba lần làm precision tăng nhưng recall giảm, phù hợp với việc mẫu âm khó chiếm phần lớn kho sinh.`),
  ...TB("Bảng 4.4. Kết quả của năm cấu hình dữ liệu trên tập kiểm định, kèm micro-F1 trên tập kiểm tra để so sánh", T(["Cấu hình", "Cặp huấn luyện", "Precision", "Recall", "Micro-F1", "Macro-F1", "Micro-F1 tập kiểm tra"], RX_CFG.map(([k, name]) => [`${k}, ${name}`, n(rxDev[k].train_pairs), rp(rxDev[k].micro.precision), rp(rxDev[k].micro.recall), rp(rxDev[k].micro.f1), rp(rxDev[k].macro_f1), rp(rxAblT(k).micro_f1)]), [2350, 1150, 1350, 1050, 1100, 1100, 1538], { size: 20, right: [1, 2, 3, 4, 5, 6] }), "Bảng dùng để chọn cấu hình dữ liệu theo quy tắc đặt trước. Cột cuối chỉ để so sánh, không dùng để chọn."),
  P(`Cột cuối của Bảng 4.4 cho thấy thứ tự trên tập kiểm tra khác với trên tập kiểm định. Cấu hình chỉ dùng dữ liệu thật đạt micro-F1 ${rp(rxAblT("x0").micro_f1)}, cao nhất, còn cấu hình được chọn đạt ${rp(rxAblT(RX.ev.chosen).micro_f1)}. Khoảng tin cậy 95% của hai cấu hình lần lượt là ${ci(rxAblT("x0").ci95_micro)} và ${ci(rxAblT(RX.ev.chosen).ci95_micro)}, chồng lên nhau, nên không cấu hình nào hơn hẳn. Với tập kiểm định nhỏ như hiện nay, khóa luận chưa chứng minh được dữ liệu sinh, dù đã kiểm tra hay chưa, giúp mô hình tốt hơn trên câu thật.`),
  H3("4.3.2. Kết quả trên tập kiểm tra"),
  P(`Bảng 4.5 đặt mô hình đã chọn cạnh rule-based, cách hợp hai bên và bộ dự đoán luôn trả lời có quan hệ trên ${rxPairs} cặp của tập kiểm tra chính. Bộ dự đoán luôn dương được đưa vào làm mốc dưới, vì nó cho biết điểm số đạt được khi không phân biệt cặp đúng với cặp sai.`),
  P(`Mô hình đạt micro-F1 ${rp(rxM("model").f1)}, cao hơn rule-based với ${rp(rxM("rules").f1)} và mốc luôn dương với ${rp(rxM("always_positive").f1)}. Khoảng tin cậy 95% của chênh lệch giữa mô hình và rule-based, tính trên cùng các mẫu bootstrap theo câu, nằm từ ${rp(RX.ev2.ci95_diff_model_minus_rules[0])} đến ${rp(RX.ev2.ci95_diff_model_minus_rules[1])} và không chứa 0, nên chênh lệch có ý nghĩa thống kê. Mô hình có recall ${rp(rxM("model").recall)} nhưng precision chỉ ${rp(rxM("model").precision)}, tức nó tìm được phần lớn quan hệ nhưng còn gán dương cho nhiều cặp mà tiêu chí chặt coi là không có quan hệ. Hợp với rule-based chỉ thêm ${rxM("model+rules").tp - rxM("model").tp} cặp đúng nhưng thêm ${rxM("model+rules").fp - rxM("model").fp} cặp sai, nên không cải thiện kết quả.`),
  ...TB("Bảng 4.5. Micro-F1 trên các nhãn dương của tập kiểm tra chính, kèm khoảng tin cậy 95%", T(["Phương pháp", "Precision", "Recall", "F1", "Khoảng tin cậy 95%"], [["model", "ViHealthBERT"], ["rules", "Rule-based"], ["model+rules", "ViHealthBERT hợp với rule-based"], ["always_positive", "Luôn trả lời có quan hệ"]].map(([k, name]) => [name, rp(rxM(k).precision), rp(rxM(k).recall), rp(rxM(k).f1), ci2(rxCI(k))]), [3400, 1400, 1400, 1300, 2138], { size: 22, right: [1, 2, 3] }), "Bảng cho thấy mô hình vượt cả rule-based lẫn mốc luôn dương, còn cách hợp với rule-based không đem lại thêm lợi ích."),
  P("Bảng 4.6 tách kết quả theo từng quan hệ. Mỗi quan hệ có ít nhất mười cặp dương trong tập kiểm tra, nên kết quả từng quan hệ có thể được so sánh, nhưng khoảng tin cậy còn rộng."),
  ...TB("Bảng 4.6. Kết quả của mô hình và rule-based theo quan hệ trên tập kiểm tra chính", T(["Quan hệ", "Cặp", "Dương", "Precision", "Recall", "F1 mô hình", "F1 rule-based"], RX_REL.map((k) => [k, rxR("model", k).pairs, rxR("model", k).positives, rp(rxR("model", k).precision), rp(rxR("model", k).recall), rp(rxR("model", k).f1), rp(rxR("rules", k).f1)]), [2300, 900, 1200, 1300, 1200, 1350, 1388], { size: 22, right: [1, 2, 3, 4, 5, 6] }), "Bảng cho biết mô hình vượt rule-based ở cả năm quan hệ."),
  P(`Quan hệ located_at đạt F1 ${rp(rxR("model", "located_at").f1)}, cao nhất trong năm quan hệ, nhờ có nhiều cặp huấn luyện nhất. Hai quan hệ treated_by và diagnosed_by đạt lần lượt ${rp(rxR("model", "treated_by").f1)} và ${rp(rxR("model", "diagnosed_by").f1)}, với recall cao nhưng precision chỉ khoảng 0,6. Hai quan hệ còn nhiều dư địa cải thiện là treated_by_procedure với F1 ${rp(rxR("model", "treated_by_procedure").f1)} và has_dosage với F1 ${rp(rxR("model", "has_dosage").f1)}. Riêng has_dosage có recall ${rp(rxR("model", "has_dosage").recall)} nhưng precision chỉ ${rp(rxR("model", "has_dosage").precision)}, vì mô hình chỉ học quan hệ này từ dữ liệu sinh. Nguyên nhân của các lỗi này được phân tích ở mục 4.6.3.`),
  H3("4.3.3. Ảnh hưởng của tiêu chí gán nhãn"),
  P(`Trên nhãn lượt đầu, cùng mô hình chỉ đạt micro-F1 ${rp(RX.ev.test.model.micro.f1)}, thấp hơn nhiều so với mốc luôn dương với ${rp(RX.ev.test.always_positive.micro.f1)}, vì lượt đầu coi gần như mọi cặp cùng câu là dương. Khi người gán soát lại các cặp mô hình bỏ sót theo nhãn lượt đầu, không cặp nào trong ${RX.fn.fn.judged} cặp được kết luận còn được coi là có quan hệ. Như vậy, phần lớn chênh lệch giữa hai lượt đến từ tiêu chí gán chứ không phải từ mô hình. Định nghĩa thế nào là có quan hệ ảnh hưởng tới điểm số nhiều hơn khác biệt giữa các cấu hình mô hình, và điểm số chỉ có ý nghĩa khi tiêu chí của tập kiểm tra khớp với tiêu chí của tập huấn luyện.`),
  H2("4.4. Kiểm thử"),
  P(`Toàn bộ ${pyRes.passed + pyRes.failed + pyRes.skipped} ca kiểm thử mô tả ở mục 3.4.9 được chạy lại ngày ${pyRes.date.split("-").reverse().join("/")} trên CPU. Kết quả là ${pyRes.passed} ca đạt, ${pyRes.failed} ca lỗi và ${pyRes.skipped} ca bị bỏ qua, với tổng thời gian ${f(pyRes.seconds, 1)} giây.`),
  P("Các ca kiểm thử này xác nhận từng thành phần hoạt động đúng như thiết kế, chẳng hạn tọa độ ký tự được giữ nguyên qua các bước, các ca dễ nhầm khi gán mã bị chặn và dữ liệu không bị rò rỉ giữa các tập. Tuy nhiên, kiểm thử không đo chất lượng dự đoán. Chất lượng đó được đánh giá riêng bằng các thực nghiệm ở mục 4.1 đến 4.4."),

  H2("4.5. Knowledge graph trên split test"),
  P(`Knowledge graph được dựng từ toàn bộ ${n(kgS.documents)} câu khác nhau của split test, với thực thể do bước NER sinh ra đúng như khi hệ thống chạy thật, chuẩn hóa ở chế độ strict và RE bằng mô hình ViHealthBERT đã chọn ở mục 4.3. Mô hình được nạp lại từ ba seed đã lưu và cho dự đoán trùng với lần chấm ở cả ${rxPairs} cặp của tập kiểm tra. Đồ thị thu được có ${n(kgS.nodes)} nút, trong đó ${kgS.normalized_nodes} nút có mã ICD-10 hoặc RxNorm, cùng ${kgS.edges} cạnh khác nhau ứng với ${kgS.edge_mentions} lần xuất hiện. Có tới ${n(kgS.isolated_nodes)} nút không có cạnh nào, vì phần lớn câu chỉ nhắc tới một thực thể hoặc không có cặp đúng kiểu. Hình 4.7 so sánh số lần xuất hiện của cạnh theo quan hệ với đồ thị dựng bằng mô hình RE cũ hợp với rule-based trên cùng thực thể.`),
  ...FIG("h4_9_kg_canh.png", "Hình 4.7. Số lần xuất hiện của cạnh theo quan hệ trong knowledge graph dựng bằng mô hình RE mới và bằng mô hình RE cũ hợp với rule-based", "Hình dùng để thấy mô hình mới sinh nhiều cạnh hơn hẳn ở các quan hệ hiếm khi nhận thực thể do NER sinh ra."),
  P(`Đồ thị mới có ${kgS.edges} cạnh khác nhau so với ${kgOldS.edges} cạnh của đồ thị cũ, trong đó chỉ ${kgShared} cạnh có ở cả hai. Mức tăng tập trung ở các quan hệ hiếm, khi has_dosage tăng từ ${kgOcc2(kgOld, "has_dosage")} lên ${kgOcc2(kg, "has_dosage")} lần xuất hiện và treated_by tăng từ ${kgOcc2(kgOld, "treated_by")} lên ${kgOcc2(kg, "treated_by")}, còn located_at gần như không đổi. Bảng 4.7 liệt kê mười hai bộ ba xuất hiện nhiều nhất để giải thích mức tăng này. Mức tăng này phù hợp với kết quả ở mục 4.3, khi mô hình mới có recall cao hơn hẳn rule-based ở các quan hệ hiếm như diagnosed_by và has_dosage. Đồ thị cũng ít thay đổi khi đổi sang mô hình học trên dữ liệu sinh đã kiểm tra, khi ${kgPrevShared} trong ${kgPrev.stats.edges} cạnh của đồ thị dựng bằng mô hình trước đó vẫn còn, phù hợp với việc hai mô hình không khác nhau có ý nghĩa trên tập kiểm tra.`),
  P("Bảng 4.7 cho thấy đồ thị gộp được nhiều cạnh hợp lý, như “thuyên tắc huyết khối” với “tĩnh mạch” hay “ra máu” với “âm đạo” bằng located_at, và mỗi cạnh đều giữ câu nguồn để người dùng kiểm tra lại. Bên cạnh đó, một số cạnh có một đầu là lượt đề cập mà NER gán sai kiểu, như “phòng ngừa” hay “tầm soát” bị gán là thuốc, hoặc “nồng độ” và “tỷ lệ” bị gán là liều lượng. Đây là những lượt đề cập mà bước kiểm tra thực thể của hướng dẫn gán nhãn đánh dấu INVALID, trong khi bộ lọc thực thể của hệ thống hiện dùng một danh sách chặn cố định nên chưa bao quát hết các trường hợp này."),
  P(`Vì vậy, đồ thị nên được hiểu là đầu ra tự động của hệ thống, phù hợp để khám phá dữ liệu và truy lại câu nguồn. Kết quả cũng cho thấy chất lượng thực thể đầu vào ảnh hưởng trực tiếp tới chất lượng cạnh, nên một bộ phân loại thực thể hợp lệ đặt giữa NER và RE sẽ giúp đồ thị chính xác hơn, và đây là một hướng phát triển được nêu ở phần Kết luận.`),
  ...TB("Bảng 4.7. Mười hai bộ ba xuất hiện nhiều nhất trong knowledge graph", T(["Thực thể đầu", "Quan hệ", "Thực thể cuối", "Số lần"], kg.edges.slice(0, 12).map((e) => [kgName[e.head], e.relation, kgName[e.tail], e.count]), [3000, 2200, 3000, 1438], { size: 19, right: [3] }), "Bảng giúp người đọc đánh giá định tính các cạnh của đồ thị, với tên nút là tên chuẩn khi thực thể có mã và là chữ gốc khi chưa có mã."),
);

// ===== CHƯƠNG 5 (viết lại 12/11/2026) =====
const errEx = X.ner_errors.slice(0, 4);
const reErr = X.re_preds.filter((p) => p.gold !== p.pred);
const ablD = (k) => abl ? s["micro avg"]["f1-score"] - abl[k].strict_exact_match["micro avg"]["f1-score"] : 0;
add(
  H2("4.6. Phân tích lỗi"),
  P("Mục này đi sâu vào các lỗi của từng thành phần để hiểu những con số ở các mục từ 4.1 đến 4.5, làm cơ sở cho phần thảo luận ở mục 4.7. Nhìn chung, lỗi NER chủ yếu là lệch ranh giới span và nhãn gold không nhất quán chứ không phải nhầm loại. Lỗi chuẩn hóa ở phiên bản đầu đều đến từ fuzzy matching và đã được chặn bằng quy tắc tổng quát, còn trên tập gold test, lỗi chủ yếu là bỏ sót cách nói dân gian chứ không phải gán sai. Lỗi RE phản ánh dữ liệu thưa, khi mô hình bỏ sót các cách diễn đạt không điển hình và gán nhầm khi cụm bệnh đã chứa tên bộ phận cơ thể."),
  H3("4.6.1. Lỗi NER"),
  H4("4.6.1.1. Lỗi theo loại thực thể"),
  P(`DOSAGE là loại yếu nhất với strict F1 ${f(s.DOSAGE["f1-score"], 3)}, và nguyên nhân chủ yếu nằm ở precision chỉ đạt ${f(s.DOSAGE.precision, 3)}. Nhãn gốc UNITCALIBRATOR bao gồm cả số đo, mức độ và tỉ lệ, trong khi luật liều lượng lại bổ sung thêm các cụm mà gold không gán. Vì định nghĩa DOSAGE của đề tài hẹp hơn nhãn nguồn, một phần con số này phản ánh sự lệch định nghĩa chứ không hẳn là lỗi nhận diện.`),
  P(`PROCEDURE đứng thứ hai từ dưới lên với strict F1 ${f(s.PROCEDURE["f1-score"], 3)}. Loại này gộp ba nhãn gốc, trong đó MEDDEVICETECHNIQUE và SURGERY vốn chỉ đạt F1 ${f(t1.MEDDEVICETECHNIQUE["f1-score"], 2)} và ${f(t1.SURGERY["f1-score"], 2)} ở mô hình gốc. Ngoài ra, ranh giới của thủ thuật trong văn nói rất mơ hồ, khi cùng một câu có thể nói “mổ”, “mổ nội soi” và “cắt nhiệt”, và nhãn gold cũng không nhất quán khi chọn cụm nào là thực thể.`),
  P(`BODY_PART, với strict F1 ${f(s.BODY_PART["f1-score"], 3)}, thường bị tách nhỏ, chẳng hạn thành “nội mạc” và “tử cung” thay vì “nội mạc tử cung”, hoặc bị lẫn với cụm bệnh có chứa tên bộ phận. Trong khi đó, DRUG có recall cao nhưng precision thấp, vì văn bản nói chứa nhiều thảo dược, thực phẩm chức năng và mỹ phẩm mà mô hình gán DRUG còn nhãn gold lại xếp vào các loại phi y khoa.`),
  H4("4.6.1.2. Phân tích các câu có nhiều lỗi nhất"),
  P("Bảng 4.8 liệt kê các câu có nhiều lỗi nhất trên tập test. Phần lớn lỗi trong các câu này thuộc ba dạng. Dạng thứ nhất là lệch ranh giới span, khi mô hình tách một cụm dài thành nhiều mảnh. Dạng thứ hai là cụm bệnh có chứa bộ phận cơ thể, nơi gold và mô hình chọn cách cắt khác nhau. Dạng thứ ba là nhãn gold không nhất quán, ví dụ “polyp” và “nhân xơ” được gold gán BODY_PART trong khi mô hình gán CONDITION, và trong những trường hợp này dự đoán của mô hình có thể còn hợp lý hơn gold."),
  P("Hai câu đầu tiên trong Bảng 4.8 được trình bày chi tiết ở Ví dụ 4.1, đặt danh sách thực thể gold cạnh danh sách thực thể mà hệ thống dự đoán."),
  ...TB("Bảng 4.8. Các câu trong tập test có nhiều lỗi NER nhất", T(["Câu", "Nội dung rút gọn", "Tóm tắt lỗi"], errEx.map((e) => { const s = String(typeof e.error_summary === "string" ? e.error_summary : JSON.stringify(e.error_summary)); const mi = s.match(/Missed (\d+)/), sp = s.match(/Spurious (\d+)/); return [e.index, e.text.length > 100 ? e.text.slice(0, 100) + "…" : e.text, `Bỏ sót ${mi ? mi[1] : 0} thực thể, dự đoán thừa ${sp ? sp[1] : 0} thực thể`]; }), [900, 5600, 3138], { right: [0] }), "Bảng dùng để chọn các trường hợp điển hình cho phân tích định tính, thay vì chỉ dựa vào chỉ số tổng hợp."),
  P("Ở câu đầu tiên, mô hình nhận ra mọi khái niệm nhưng cắt span khác với gold. Mô hình trả về “rối loạn” thay vì “rối loạn chức năng”, tách “nội mạc” và “tử cung” thay vì giữ nguyên “nội mạc tử cung”, và gán “polyp” là CONDITION trong khi gold gán BODY_PART. Theo strict match, câu này tạo ra 4 FN và 6 FP dù phần lớn thông tin đã được nhận ra. Đây là lý do khóa luận báo cáo cả relaxed match và phân tích định tính bên cạnh con số tổng hợp."),
  ...errEx.slice(0, 2).flatMap((e) => [
    PN(`Câu ${e.index}: “${e.text}”`),
    T(["Nhãn chuẩn", "Dự đoán"], (() => { const g = e.gold_entities.map((x) => `[${x.label}] ${x.surface_text}`), p = e.predicted_entities.map((x) => `[${x.label}] ${x.surface_text}`); const m = Math.max(g.length, p.length); return Array.from({ length: m }, (_, i) => [g[i] || "", p[i] || ""]); })(), [4819, 4819], { size: 20 }),
  ]),
  CAP("Ví dụ 4.1. So sánh thực thể gold và thực thể dự đoán của hai câu có nhiều lỗi nhất"),
  DESC("Ví dụ cho thấy phần lớn lỗi là cách cắt span khác nhau, trong khi các khái niệm chính vẫn được nhận ra."),
  H3("4.6.2. Lỗi chuẩn hóa ICD-10"),
  P("Mọi mã sai trong Bảng 4.2 đều đến từ bước fuzzy matching bằng token_set_ratio. Như đã trình bày ở mục 2.6, độ đo này cho điểm 100 khi tập từ của chuỗi ngắn nằm trọn trong chuỗi dài, nên “nhồi máu” khớp với “nhồi máu lách” và “đậu mùa bò” khớp với “đậu mùa”. Ngay cả khi hai tập từ chỉ gần như lồng nhau, điểm vẫn cao, như “huyết áp cao” khớp với “đo huyết áp” ở mức 0,87 và “đa xơ cứng” khớp với “gan xơ cứng” ở mức 0,86. Do đó, ngưỡng 0,85 không đủ để chặn các trường hợp chung từ khóa nhưng khác nghĩa."),
  P("Bản sửa xuất phát từ một nhận xét về cấu trúc tên bệnh tiếng Việt. Từ đầu cụm thường quyết định loại khái niệm, chẳng hạn “đo huyết áp” là thủ thuật còn “gan xơ cứng” là bệnh gan, trong khi các từ phía sau chỉ bổ nghĩa. Vì vậy, yêu cầu từ đầu cụm của candidate phải xuất hiện trong truy vấn đã chặn được nhóm lỗi thứ nhất. Nhóm lỗi thứ hai, tức tập con với chuỗi ngắn, được chặn bằng cách từ chối khi chuỗi ngắn chỉ có một hoặc hai từ, vì khi đó các từ thêm vào gần như chắc chắn làm thay đổi bệnh. Cả hai quy tắc đều được kiểm thử bằng 18 ca cũ, tất cả giữ nguyên kết quả, cùng các ca mới."),
  P("Một ca vẫn còn nghi vấn là “rối loạn vận động” được gán mã F44.4, tức rối loạn vận động phân ly. Trong ngữ cảnh bệnh Parkinson, rối loạn vận động thường không phải rối loạn phân ly, nhưng nếu không có ngữ cảnh thì không thể quyết định. Trường hợp này cần thông tin ngữ cảnh để quyết định, và cũng là lý do của ràng buộc cuối cùng ở Bảng 3.11, theo đó candidate không được thêm khái niệm như “phân ly” mà người nói không nhắc tới."),
  P(`Trên tập gold chuẩn hóa test, lỗi chủ yếu là bỏ sót chứ không phải gán sai. Chế độ strict chỉ trả lời ${pct(nc("ICD-10").system.coverage)} dạng ICD-10 có mã, nhưng mọi câu trả lời đều đúng. Các dạng bị bỏ sót chủ yếu là cụm ngắn với trung vị ba từ, thuộc hai nhóm. Nhóm thứ nhất là cách nói dân gian không có tên tương ứng trong danh mục và chưa có trong từ điển alias vì không xuất hiện ở train và dev, như “có thai”, “rong kinh”, “ra máu” hay “khiếm thính”. Nhóm thứ hai là tên ngắn mà mục gần nhất trong danh mục có thêm từ bổ nghĩa nên bị ràng buộc phủ từ từ chối, như “viêm gan”, “điếc” hay “mất răng”. `),
  P(`Trong ${icdMiss.length} dạng bị bỏ sót, ${icdMissTop} dạng vẫn có mã đúng trong mười candidate đầu nên người dùng vẫn chọn được, còn phần còn lại cần từ điển lớn hơn hoặc mô hình ngữ nghĩa. Với RxNorm, các lỗi gán sai còn lại như “protein”, “gel” hay “carbonate” là từ tiếng Anh có trong RxNorm nhưng câu chứa chúng lại nói về thực phẩm hoặc mỹ phẩm, tức cũng là vấn đề ngữ cảnh.`),
  H3("4.6.3. Lỗi trích xuất quan hệ"),
  P(`Để phân tích lỗi, khóa luận đọc lại từng cặp mà mô hình dự đoán sai trên tập kiểm tra chính, gồm ${rxM("model").fp} cặp dương giả và ${rxM("model").fn} cặp bỏ sót. Lỗi tập trung ở hai quan hệ có F1 thấp hơn, trong đó has_dosage có ${rxR("model", "has_dosage").fp} cặp dương giả và treated_by_procedure có ${rxR("model", "treated_by_procedure").fp} cặp dương giả cùng ${rxR("model", "treated_by_procedure").fn} cặp bỏ sót.`),
  P("Với has_dosage, phần lớn dương giả là một thuốc hay hoạt chất đứng cạnh một con số không phải liều dùng, như “bảy mươi phần trăm là canxi”, “tiêm chủng vắc xin cũng đạt tỷ lệ cao” hay “trong hai tám viên thì chỉ có hai mốt viên là có progesterone”. Vì tập huấn luyện thật không có cặp has_dosage nào, mô hình chỉ học quan hệ này từ câu sinh, trong đó một thuốc đứng cạnh một lượng gần như luôn là liều, nên mô hình gán dương cho hầu hết cặp thuốc và con số. Muốn sửa lỗi này cần câu thật có liều thuốc, hoặc thêm mẫu âm sinh ra từ số liệu thống kê và thành phần sản phẩm."),
  P("Với treated_by_procedure, dương giả có hai dạng. Dạng thứ nhất là thực thể PROCEDURE thực chất không phải thủ thuật nhưng vẫn được đánh dấu hợp lệ, như “phục hồi”, “uống thuốc”, “hạ sốt” hay “trung tiện”, khiến cặp bệnh và động từ bị coi là quan hệ điều trị. Dạng thứ hai là quan hệ nhân quả ngược, như trong câu nói về “biến chứng mà do nhổ răng gây ra”, nơi thủ thuật là nguyên nhân của bệnh chứ không phải cách điều trị. Bỏ sót của quan hệ này chủ yếu là thủ thuật nha khoa như “ghép xương” hay “hàm giả”, vốn hiếm trong tập huấn luyện."),
  P("Với located_at, dương giả chủ yếu đến từ câu liệt kê, như “đái tháo đường ung thư tim mạch đột quỵ”, nơi bệnh và bộ phận chỉ đứng cạnh nhau, còn bỏ sót xảy ra khi bộ phận ở xa bệnh, như trong “xuất huyết này chảy máu này hoặc là những cái ổ viêm nhiễm áp xe ở đại tràng”. Hai dạng lỗi này cho thấy mô hình vẫn dựa nhiều vào khoảng cách giữa hai thực thể, đúng là điều mà tiêu chí chặt muốn loại bỏ."),
  H2("4.7. Thảo luận"),
  P("Dựa trên kết quả ở các mục từ 4.1 đến 4.5 và các nhóm lỗi ở mục 4.6, mục này trả lời ba câu hỏi nghiên cứu đã nêu ở mục 1.5, sau đó thảo luận độ tin cậy của đánh giá và khả năng ứng dụng của hệ thống."),
  H3("4.7.1. Trả lời các câu hỏi nghiên cứu"),
  P(`Câu hỏi thứ nhất hỏi liệu mô hình RE học từ dữ liệu có tốt hơn baseline rule-based hay không. Trên tập kiểm tra chính, câu trả lời là có. ViHealthBERT đạt micro-F1 ${rp(rxM("model").f1)} so với ${rp(rxM("rules").f1)} của rule-based, và khoảng tin cậy của chênh lệch không chứa 0. Lợi thế đến chủ yếu từ recall, khi mô hình bắt được các cách nói không có từ gợi ý mà rule-based bỏ qua, rõ nhất ở diagnosed_by với F1 ${rp(rxR("model", "diagnosed_by").f1)} so với ${rp(rxR("rules", "diagnosed_by").f1)}. Kết quả này phù hợp với các nghiên cứu trước về RE bằng mô hình tiền huấn luyện có ký hiệu đánh dấu thực thể [11], [12].`),
  P("Câu hỏi thứ hai hỏi lỗi NER ảnh hưởng tới chất lượng RE của toàn hệ thống như thế nào. Khóa luận trả lời câu hỏi này bằng phân tích định tính. Ảnh hưởng của lỗi NER có thể đáng kể, bởi bộ dữ liệu quan hệ cũ cho thấy khi thực thể lấy thẳng từ nhãn NER, khoảng " + RX_OLD.wrongTypeNeg + "% cặp âm chứa thực thể sai kiểu, trong khi mô hình mới chỉ được huấn luyện và chấm trên thực thể đã được kiểm tra. Ngoài ra, với strict F1 của NER khoảng 0,62 và nhiều lỗi lệch ranh giới, xác suất cả hai đầu của một cạnh cùng khớp chính xác thấp hơn đáng kể. Knowledge graph ở mục 4.5 cung cấp bằng chứng định tính cho nhận định này, khi phần lớn bộ ba xuất hiện nhiều nhất có một đầu là thực thể sai kiểu do NER sinh ra, như “phòng ngừa” bị gán là thuốc hay “tỷ lệ” bị gán là liều lượng."),
  P(`Câu hỏi thứ ba hỏi các bước xử lý bổ sung đem lại lợi ích gì và tạo ra lỗi gì. Với NER, các luật gần như không thay đổi kết quả tổng thể, khi pipeline đầy đủ chỉ làm strict micro-F1 ${ablD("model_only") >= 0 ? "tăng" : "giảm"} ${f(Math.abs(ablD("model_only")), 4)} so với chỉ dùng mô hình. Luật bỏ từ hành động giúp DRUG tốt hơn, nhưng luật gộp từ chỉ mức độ lại bị phạt vì lệch với quy ước của bộ dữ liệu, và luật liều lượng hầu như không có cụm liều để bắt. Với chuẩn hóa, exact match và alias luôn cho mã hợp lý, còn fuzzy matching là nguồn duy nhất của mã sai, và sau bản sửa chỉ còn ${icd.by_method.fuzzy || 0} đề cập được gán mã qua fuzzy matching.`),
  H3("4.7.2. Lệch quy ước giữa NER và dữ liệu quan hệ"),
  P("Nhãn NER của VietMed-NER gán kiểu thực thể theo phạm vi rộng, nên nhiều lượt đề cập như “kiểm soát”, “phục hồi” hay “tỷ lệ” vẫn mang nhãn thuốc, thủ thuật hay liều lượng. Bộ dữ liệu quan hệ mới xử lý lệch quy ước này bằng bước kiểm tra thực thể trước khi gán quan hệ, còn trong hệ thống, bước RE chặn các thực thể chung chung bằng một danh sách cố định trước khi sinh cặp. Danh sách này chỉ bao phủ những từ hay gặp, nên vẫn còn khoảng trống giữa bộ lọc của hệ thống và bước kiểm tra thực thể do người gán thực hiện, như các dương giả của treated_by_procedure ở mục 4.6.3 cho thấy. Một bộ phân loại thực thể hợp lệ học từ nhãn VALID và INVALID của bộ dữ liệu mới là cách tự nhiên để thu hẹp khoảng trống này."),
  H3("4.7.3. Độ tin cậy của đánh giá"),
  P("Khóa luận áp dụng nhiều biện pháp để kết quả đánh giá đáng tin cậy. Với RE, tập huấn luyện lấy từ phần train và validation còn tập kiểm tra lấy từ phần test của VietMed-NER, các câu được kiểm tra trùng cả nguyên câu lẫn chuỗi 8 từ, cấu hình được chọn trên tập kiểm định theo quy tắc đặt trước, dù hai cấu hình dùng dữ liệu sinh đã kiểm tra được thêm vào sau khi tập kiểm tra đã được chấm một lần, và mọi F1 đều kèm khoảng tin cậy tính bằng bootstrap theo câu. Với chuẩn hóa, mọi cải tiến được chọn trên dev và tập test chỉ được chạy một lần. Mọi bản ghi dữ liệu đều lưu nguồn nhãn, nhờ đó kết quả có thể được tách theo từng nguồn khi cần."),
  P("Nhãn huấn luyện và nhãn kiểm tra của RE đều có sự tham gia của mô hình ngôn ngữ lớn, ở vai trò người gán đầu tiên với tập huấn luyện và người gợi ý với tập kiểm tra. Bổ sung một người gán thứ hai làm việc độc lập vì vậy sẽ giúp khẳng định chắc chắn hơn các kết luận về RE, và đây là việc được xếp đầu trong hướng phát triển."),
  H3("4.7.4. Ý nghĩa và khả năng ứng dụng"),
  P("Ở trạng thái hiện tại, hệ thống phù hợp làm công cụ hỗ trợ, chẳng hạn gợi ý thực thể và mã bệnh để người nhập liệu xác nhận, hoặc tiền xử lý cho tìm kiếm và thống kê, nơi sai sót có thể được kiểm tra lại. Hệ thống được thiết kế để hỗ trợ chứ không thay thế quyết định lâm sàng. Danh sách candidate cho mã bệnh và trang knowledge graph có câu nguồn được thiết kế cho đúng kịch bản có người xác nhận này. Bên cạnh đó, nguyên tắc thà không gán mã còn hơn gán sai và dấu hiệu thực thể bị loại khỏi RE giúp người dùng phân biệt trường hợp không có kết quả với trường hợp hệ thống không đủ căn cứ, một yêu cầu quan trọng trong miền y tế."),
);

// ===== KẾT LUẬN (viết lại 12/11/2026) =====
const LEAD = (t) => P(t, { p: { spacing: { after: 160, line: 312 } } });
const KEY_CONCLUSIONS = [
  P("Đối chiếu với năm mục tiêu ở mục 1.2 và ba câu hỏi nghiên cứu ở mục 1.5, khóa luận đạt được các kết quả sau."),
  LEAD(`Về nhận diện thực thể và đồ thị tri thức, trên ${n(nerNew.lat.total_samples)} câu test của VietMed-NER, NER đạt strict micro-F1 ${f(s["micro avg"]["f1-score"], 3)} và relaxed micro-F1 ${f(r["micro avg"]["f1-score"], 3)} với thời gian xử lý trung bình ${f(nerNew.lat.mean_latency_ms, 0)} ms mỗi câu trên CPU${nerBase && nerInh ? `, trong đó phần mô hình vượt rõ hai baseline từ điển và CRF` : ""}. Đồ thị tri thức dựng từ chính tập test có ${n(kgS.nodes)} nút và ${kgS.edges} cạnh.`),
  LEAD(`Về chuẩn hóa mã, chế độ strict đạt Accuracy ${rp(nc("ICD-10").system.accuracy)} cho ICD-10 với precision ${rp(nc("ICD-10").system.precision_answered)} khi trả lời, cao gấp khoảng năm lần baseline exact match, và mã đúng nằm trong mười candidate đầu ở ${pct(nc("ICD-10").top10_acc)} trường hợp. RxNorm đạt Accuracy ${rp(nc("RxNorm").system.accuracy)}.`),
  LEAD(`Về RE, khóa luận xây dựng bộ dữ liệu quan hệ theo hướng dẫn hai bước. Trả lời câu hỏi nghiên cứu thứ nhất, ViHealthBERT đạt micro-F1 ${rp(rxM("model").f1)} trên tập kiểm tra, cao hơn rule-based với ${rp(rxM("rules").f1)}, và khoảng tin cậy của chênh lệch không chứa 0. Quan hệ located_at đạt F1 ${rp(rxR("model", "located_at").f1)}, còn treated_by và diagnosed_by đều đạt từ 0,7 trở lên. Hai quan hệ treated_by_procedure và has_dosage còn nhiều dư địa cải thiện. Dữ liệu sinh đã qua kiểm tra giúp mô hình hỗ trợ đủ năm quan hệ, nhưng chưa cho thấy cải thiện có ý nghĩa thống kê so với chỉ dùng dữ liệu thật.`),
  LEAD(`Về đánh giá, mọi thành phần đều có baseline, khoảng tin cậy và phân tích lỗi. Trả lời câu hỏi thứ ba, các quy tắc bổ sung của NER gần như không thay đổi kết quả tổng thể, còn phân tích lỗi đã giúp sửa bước fuzzy matching ICD-10 vốn từng gán sai ${icdBefore.wrong_mentions} đề cập, và toàn bộ ${nTests} ca kiểm thử đều đạt. Câu hỏi thứ hai được trả lời qua phân tích đồ thị tri thức, cho thấy chất lượng thực thể đầu vào ảnh hưởng trực tiếp tới chất lượng quan hệ.`),
];

add(
  H1("KẾT LUẬN"),
  H2("1. Kết quả đạt được"),
  ...KEY_CONCLUSIONS,
  P("Bên cạnh các kết quả trên, quá trình thực hiện cho thấy ba phát hiện có giá trị cho các nghiên cứu tiếp theo trên văn bản y tế tiếng Việt. Thứ nhất, chất lượng thực thể đầu vào quyết định chất lượng quan hệ, nên bước kiểm tra thực thể trước khi gán quan hệ giúp dữ liệu sạch hơn rõ rệt. Thứ hai, với dữ liệu nhỏ, định nghĩa rõ ràng thế nào là có quan hệ ảnh hưởng tới kết quả nhiều hơn việc thay đổi cấu hình mô hình. Thứ ba, nguyên tắc chỉ gán mã khi đủ chắc chắn cho phép hệ thống đạt độ tin cậy cao ngay cả khi danh mục mã và cách nói thường ngày khác xa nhau."),
  LEAD(`Về sản phẩm, toàn bộ luồng xử lý được đóng gói thành một giao diện web minh họa, nhận văn bản tự do và trả về thực thể, mã chuẩn cùng quan hệ trong khoảng 0,4 đến 2,7 giây mỗi câu trên CPU, kèm bộ kiểm thử tự động gồm ${nTests} ca bao phủ từng thành phần.`),
  H2("2. Hạn chế"),
  P("Khóa luận còn một số điểm có thể tiếp tục hoàn thiện. Hệ thống mới được đánh giá trên lời nói y tế được chép lại, dữ liệu quan hệ còn nhỏ với tập kiểm tra có một người gán, và bước chuẩn hóa chưa tận dụng ngữ cảnh của câu. Tập kiểm định chỉ có 60 câu nên chưa đủ để phân biệt các cấu hình dữ liệu, và phần dữ liệu sinh chỉ qua kiểm tra tự động có thể còn khoảng một phần mười câu sai. Nhãn của tập đánh giá chuẩn hóa do mô hình ngôn ngữ lớn gán và chưa được chuyên gia y tế xác nhận."),
  H2("3. Kiến nghị hướng phát triển"),
  P(`Từ những điểm trên, khóa luận kiến nghị các hướng phát triển theo thứ tự ưu tiên. Trước tiên là mời thêm một người có chuyên môn gán độc lập tập kiểm tra quan hệ và đánh giá RE trên thực thể do NER sinh ra. Tiếp theo là huấn luyện một bộ phân loại thực thể hợp lệ từ nhãn VALID và INVALID để thay danh sách chặn cố định, bổ sung dữ liệu có đơn thuốc thật cho has_dosage và mở rộng từ điển alias. Cuối cùng là chuẩn hóa thêm BODY_PART, TEST và PROCEDURE rồi thử nghiệm trên bệnh án thật khi có nguồn dữ liệu được phép sử dụng. Về ứng dụng, hệ thống có thể được tích hợp vào phần mềm bệnh án điện tử như một công cụ gợi ý thực thể, mã bệnh và mã thuốc cho người nhập liệu, góp phần chuẩn hóa dữ liệu y tế ngay từ khâu ghi nhận. Về mô hình, có thể huấn luyện lại mô hình NER trên dữ liệu đã kiểm tra thực thể và thay bước xếp hạng ứng viên ICD-10 bằng mô hình embedding đa ngôn ngữ có dùng ngữ cảnh câu.`),
  P("Với những kết quả trên, khóa luận đã xây dựng được một nền tảng ban đầu cho việc khai thác tự động và có kiểm soát văn bản y tế tiếng Việt, từ nhận diện thực thể, gán mã chuẩn tới trích xuất quan hệ và tổng hợp tri thức."),
);

// ===== TÀI LIỆU THAM KHẢO =====
add(
  H1("TÀI LIỆU THAM KHẢO"),
  ...REFLIST([
    "L. A. Ramshaw and M. P. Marcus, “Text chunking using transformation-based learning,” in Proc. 3rd Workshop on Very Large Corpora, Cambridge, MA, USA, 1995, pp. 82–94.",
    "K. Le-Duc, D. Thulke, H.-P. Tran, L. Vo-Dang, K.-N. Nguyen, T.-S. Hy, and R. Schlüter, “Medical spoken named entity recognition,” in Proc. 2025 Conf. North American Chapter of the Association for Computational Linguistics: Human Language Technologies, Industry Track, Albuquerque, NM, USA, 2025, pp. 724–783, doi: 10.18653/v1/2025.naacl-industry.59.",
    "J. Lafferty, A. McCallum, and F. Pereira, “Conditional random fields: Probabilistic models for segmenting and labeling sequence data,” in Proc. 18th Int. Conf. Machine Learning, Williamstown, MA, USA, 2001, pp. 282–289.",
    "G. Lample, M. Ballesteros, S. Subramanian, K. Kawakami, and C. Dyer, “Neural architectures for named entity recognition,” in Proc. NAACL-HLT, San Diego, CA, USA, 2016, pp. 260–270.",
    "J. Devlin, M.-W. Chang, K. Lee, and K. Toutanova, “BERT: Pre-training of deep bidirectional transformers for language understanding,” in Proc. NAACL-HLT, Minneapolis, MN, USA, 2019, pp. 4171–4186.",
    "N. Minh, V. H. Tran, V. Hoang, H. D. Ta, T. H. Bui, and S. Q. H. Truong, “ViHealthBERT: Pre-trained language models for Vietnamese in health text mining,” in Proc. 13th Language Resources and Evaluation Conf., Marseille, France, 2022, pp. 328–337.",
    "E. F. Tjong Kim Sang and F. De Meulder, “Introduction to the CoNLL-2003 shared task: Language-independent named entity recognition,” in Proc. 7th Conf. Natural Language Learning, Edmonton, Canada, 2003, pp. 142–147.",
    "A. Vaswani, N. Shazeer, N. Parmar, J. Uszkoreit, L. Jones, A. N. Gomez, Ł. Kaiser, and I. Polosukhin, “Attention is all you need,” in Advances in Neural Information Processing Systems 30, Long Beach, CA, USA, 2017, pp. 5998–6008.",
    "Y. Liu, M. Ott, N. Goyal, J. Du, M. Joshi, D. Chen, O. Levy, M. Lewis, L. Zettlemoyer, and V. Stoyanov, “RoBERTa: A robustly optimized BERT pretraining approach,” arXiv preprint arXiv:1907.11692, 2019.",
    "D. Q. Nguyen and A. T. Nguyen, “PhoBERT: Pre-trained language models for Vietnamese,” in Findings of the Association for Computational Linguistics: EMNLP 2020, 2020, pp. 1037–1042.",
    "L. Baldini Soares, N. FitzGerald, J. Ling, and T. Kwiatkowski, “Matching the blanks: Distributional similarity for relation learning,” in Proc. 57th Annu. Meeting of the Association for Computational Linguistics, Florence, Italy, 2019, pp. 2895–2905.",
    "Z. Zhong and D. Chen, “A frustratingly easy approach for entity and relation extraction,” in Proc. NAACL-HLT, 2021, pp. 50–61.",
    "Ö. Uzuner, B. R. South, S. Shen, and S. L. DuVall, “2010 i2b2/VA challenge on concepts, assertions, and relations in clinical text,” J. Am. Med. Inform. Assoc., vol. 18, no. 5, pp. 552–556, 2011.",
    "S. Henry, K. Buchan, M. Filannino, A. Stubbs, and Ö. Uzuner, “2018 n2c2 shared task on adverse drug events and medication extraction in electronic health records,” J. Am. Med. Inform. Assoc., vol. 27, no. 1, pp. 3–12, 2020.",
    "Bộ Y tế, Quyết định số 4469/QĐ-BYT ngày 28/10/2020 ban hành Bảng phân loại quốc tế mã hóa bệnh tật, nguyên nhân tử vong ICD-10 và Hướng dẫn mã hóa bệnh tật theo ICD-10. Hà Nội, Việt Nam, 2020.",
    "S. J. Nelson, K. Zeng, J. Kilbourne, T. Powell, and R. Moore, “Normalized names for clinical drugs: RxNorm at 6 years,” J. Am. Med. Inform. Assoc., vol. 18, no. 4, pp. 441–448, 2011.",
    "K. Zeng, O. Bodenreider, J. Kilbourne, and S. J. Nelson, “RxNav: A web service for standard drug information,” in AMIA Annu. Symp. Proc., Washington, DC, USA, 2006, p. 1156.",
    "F. Pedregosa et al., “Scikit-learn: Machine learning in Python,” J. Mach. Learn. Res., vol. 12, pp. 2825–2830, 2011.",
    "V. I. Levenshtein, “Binary codes capable of correcting deletions, insertions, and reversals,” Soviet Physics Doklady, vol. 10, no. 8, pp. 707–710, 1966.",
    "P. Jaccard, “The distribution of the flora in the alpine zone,” New Phytologist, vol. 11, no. 2, pp. 37–50, 1912.",
    "B. Efron and R. J. Tibshirani, An Introduction to the Bootstrap. New York, NY, USA: Chapman & Hall, 1993.",
    "J. Cohen, “A coefficient of agreement for nominal scales,” Educational and Psychological Measurement, vol. 20, no. 1, pp. 37–46, 1960.",
    "T. H. Truong, M. H. Dao, and D. Q. Nguyen, “COVID-19 named entity recognition for Vietnamese,” in Proc. NAACL-HLT, 2021, pp. 2146–2153.",
    "T. Wolf et al., “Transformers: State-of-the-art natural language processing,” in Proc. 2020 Conf. Empirical Methods in Natural Language Processing: System Demonstrations, 2020, pp. 38–45.",
    "B. Rosario and M. A. Hearst, “Classifying semantic relations in bioscience texts,” in Proc. 42nd Annu. Meeting of the Association for Computational Linguistics, Barcelona, Spain, 2004, pp. 430–437.",
    "H. Gurulingappa, A. M. Rajput, A. Roberts, J. Fluck, M. Hofmann-Apitius, and L. Toldo, “Development of a benchmark corpus to support the automatic extraction of drug-related adverse effects from medical case reports,” J. Biomed. Inform., vol. 45, no. 5, pp. 885–892, 2012.",
    "Bộ Y tế, Thông tư số 13/2025/TT-BYT hướng dẫn triển khai hồ sơ bệnh án điện tử. Hà Nội, Việt Nam, 2025.",
    "VietTimes, “Ngành y tế bước vào cuộc lột xác dữ liệu,” VietTimes, 02/01/2026. [Trực tuyến]. Địa chỉ: https://viettimes.vn/nganh-y-te-buoc-vao-cuoc-lot-xac-du-lieu-post193248.html",
    "T. D. Huy, N. A. Tu, T. H. Vu, N. P. Minh, N. Phan, T. H. Bui, and S. Q. H. Truong, “ViMQ: A Vietnamese medical question dataset for healthcare dialogue system development,” in Proc. 28th Int. Conf. Neural Information Processing (ICONIP), 2021, pp. 657–664.",
    "P. V. Duong, T.-D. Trinh, M.-T. Nguyen, H.-T. Vu, M. C. Pham, T. M. Tuan, and L. H. Son, “ViMedNER: A medical named entity recognition dataset for Vietnamese,” EAI Endorsed Trans. Industrial Networks and Intelligent Systems, vol. 11, no. 4, 2024.",
  ]),
);

// ===== PHỤ LỤC A, B =====
add(
  H1("PHỤ LỤC"),
  HA("Phụ lục A: Hướng dẫn tái lập", false),
  P("Chạy từ thư mục gốc repository trên Windows PowerShell, dùng môi trường `.venv`. Trọng số NER đặt tại Model/vihealthbert-ner-vietmed-v2-final/model.safetensors (xem Model/README.md)."),
  ...CODE([
    "pip install -r requirements.txt",
    "# Kiểm thử",
    ".venv\\Scripts\\python.exe -X utf8 -m pytest tests -q --ignore=tests/test_re_v3_filter.py --ignore=tests/test_re_v3_synth_pattern.py",
    "# Đánh giá NER (khoảng 6–7 phút trên CPU)",
    `.venv\\Scripts\\python.exe -X utf8 eval/run_eval.py --output-dir ${NER_DIR}`,
    "# Ablation NER (khoảng 20 phút)",
    `.venv\\Scripts\\python.exe -X utf8 scripts/run_ner_ablation.py --out ${ABL_DIR}`,
    "# Dữ liệu quan hệ: chọn câu, gán nhãn hai lượt, ghép và duyệt, gán lại tập kiểm tra, sinh dữ liệu",
    ".venv\\Scripts\\python.exe -X utf8 -m relation.select_samples",
    ".venv\\Scripts\\python.exe -X utf8 -m relation.merge_ai",
    ".venv\\Scripts\\python.exe -X utf8 -m relation.review_seed import",
    ".venv\\Scripts\\python.exe -X utf8 -m relation.relabel_test import",
    ".venv\\Scripts\\python.exe -X utf8 -m relation.synth",
    "# Kiểm tra dữ liệu sinh rồi nhập phiếu duyệt của người có chuyên môn (relation/validate/, docs/KE_HOACH_VALIDATE_AUGMENT.md)",
    ".venv\\Scripts\\python.exe -X utf8 -m relation.validate.import_expert",
    "# Huấn luyện năm cấu hình ViHealthBERT trên GPU, chọn trên tập kiểm định rồi chấm tập kiểm tra",
    ".venv-gpu\\Scripts\\python.exe -X utf8 -m relation.train --configs x0 x1 x3 v1 vall",
    ".venv\\Scripts\\python.exe -X utf8 -m relation.evaluate",
    ".venv\\Scripts\\python.exe -X utf8 -m relation.eval_rules_v2",
    "# Lưu mô hình RE dùng trong hệ thống",
    ".venv-gpu\\Scripts\\python.exe -X utf8 -m relation.train --configs vall --save-model Model/vihealthbert-re-vietmed-validated",
    ".venv-gpu\\Scripts\\python.exe -X utf8 -m relation.eval_modes Model/vihealthbert-re-vietmed-validated",
    "# Đánh giá chuẩn hóa trên tập đánh giá chuẩn hóa (dev để chọn, test để báo cáo)",
    ".venv\\Scripts\\python.exe -X utf8 scripts/normalization_eval/evaluate.py --gold data/norm_gold_v1/gold_test.jsonl --out eval/normalization_<ngày>/test",
    "# Baseline NER (từ điển, CRF; khoảng 30 phút CPU)",
    "cd scripts/ner_experiments; ..\\..\\.venv\\Scripts\\python.exe -X utf8 baselines.py --out ../../eval/ner_baselines_2026-11-08",
    "# Giao diện minh họa: http://127.0.0.1:8770 (mô hình nạp khoảng 26 giây); câu ví dụ cho giao diện",
    ".venv\\Scripts\\python.exe -X utf8 web/app.py",
    ".venv\\Scripts\\python.exe -X utf8 scripts/demo/make_samples.py",
    "# Đồ thị tri thức trên tập test, chỉ dùng mô hình RE (NER khoảng 10 phút, RE ViHealthBERT khoảng 6 phút trên CPU)",
    `.venv\\Scripts\\python.exe -X utf8 scripts/build_kg.py --split test --re-mode fallback --out ${KG_DIR}`,
    "# hoặc giữ thực thể của lần chạy trước, chỉ chạy lại RE",
    `.venv\\Scripts\\python.exe -X utf8 scripts/build_kg.py --from-results ${KG_OLD_DIR}/results.jsonl --rerun-re --re-mode fallback --out ${KG_DIR}`,
    "# Dựng lại báo cáo (cần Node.js và gói docx)",
    "node outputs/bao_cao_khoa_luan_2026-11-05/build_report.js <repo> <file.docx> eval/results_2026-11-05",
    "# Hướng dẫn đọc và giải thích toàn hệ thống: docs/HUONG_DAN_HE_THONG.md",
  ]),
  HA("Phụ lục B: Danh mục tệp kết quả", true),
  T(["Tệp", "Nội dung"], [
    [`${NER_DIR}/`, "Kết quả NER chạy lại 05/11/2026 (tầng 1, tầng 2, độ trễ, ma trận nhầm lẫn, câu lỗi nhiều nhất)"],
    [`${ABL_DIR}/`, "Ablation NER 06/11/2026"],
    ["eval/results/", "Kết quả NER cũ 17/09/2026 (giữ để đối chiếu)"],
    ["relation/guideline.md", "Hướng dẫn gán nhãn quan hệ hai bước, khóa ngày 19/11/2026"],
    ["relation/data/", "Dữ liệu quan hệ: seed.jsonl, dev.jsonl, test.jsonl và test_v2.jsonl, nhãn hai lượt của LLM, phiếu duyệt, selection.json"],
    ["relation/data/synth/", "Dữ liệu sinh: pool.jsonl, x1.jsonl, x3.jsonl, manifest.json"],
    ["relation/data/synth/validate/", "Kiểm tra dữ liệu sinh: bằng chứng, kết luận từng câu, phiếu duyệt của người có chuyên môn"],
    ["relation/data/synth/validated/", "Dữ liệu sinh đã kiểm tra: pool.jsonl, x1.jsonl, manifest.json"],
    ["relation/outputs/", "Dự đoán của năm cấu hình, evaluation.json, evaluation_test_v2.json, evaluation_test_v2_rules.json, evaluation_validated_ablation.json, evaluation_test_v2_modes.json"],
    ["Model/vihealthbert-re-vietmed-validated/", "Mô hình RE của hệ thống, ba seed, dữ liệu sinh đã kiểm tra (trọng số không có trong git)"],
    ["Model/vihealthbert-re-vietmed/", "Mô hình RE trước đó, dữ liệu sinh chưa kiểm tra, giữ để đối chiếu"],
    ["data/norm_gold_v1/", "Gold chuẩn hóa dev/test (nhãn LLM), phiếu duyệt Excel, manifest"],
    [`${NORM_DIR}/`, "Đánh giá chuẩn hóa trước/sau cải tiến trên dev và test, comparison.md"],
    [`${KG_DIR}/`, "Knowledge graph dựng bằng mô hình RE mới: kg.html, kg.json, triples.csv, nodes.csv, kg.graphml, stats.md"],
    [`${KG_OLD_DIR}/`, "Knowledge graph dựng bằng mô hình RE cũ hợp với rule-based, giữ để so sánh"],
    ["outputs/kg_test_2026-11-21/", "Knowledge graph dựng bằng mô hình RE trước khi kiểm tra dữ liệu sinh, dùng để so sánh ở mục 4.5"],
    [`${NERB_DIR}/`, "Baseline NER (từ điển, CRF) và điểm checkpoint kế thừa cùng hàm chấm"],
    ["web/", "Giao diện minh họa: app.py (máy chủ FastAPI), index.html, samples.json (câu ví dụ đã chạy sẵn)"],
    ["docs/HUONG_DAN_HE_THONG.md", "Hướng dẫn và giải thích toàn hệ thống"],
    ["outputs/bao_cao_khoa_luan_2026-11-05/", "icd10_check*.json, extra.json, pytest_collect.txt, build_report.js"],
  ], [4300, 5338], { size: 20 }),
);

// ===== PHỤ LỤC D: Hướng dẫn gán nhãn quan hệ (bản làm lại, khóa ngày 19/11/2026) =====
add(
  HA("Phụ lục C: Hướng dẫn gán nhãn quan hệ", true),
  P("Phụ lục này tóm tắt hướng dẫn gán nhãn dùng cho bộ dữ liệu quan hệ ở mục 3.3.3. Hướng dẫn được khóa trước khi gán và không sửa trong lúc gán, những trường hợp chưa có trong hướng dẫn được ghi chú lại để xem xét sau. Dữ liệu là bản ghi giọng nói VietMed, cắt thành đoạn khoảng 22 đến 24 từ và không có dấu câu, và người gán không sửa ranh giới thực thể."),
  H3("Phụ lục C.1: Nguyên tắc chung"),
  ...LIST([
    "Chỉ gán điều mà câu nói ra, không gán điều đúng về y học.",
    "Chỉ dùng chính câu đó, không suy từ câu trước hay câu sau, không dùng kiến thức bên ngoài để bù chỗ bị cắt.",
    "Quan hệ phải nối đúng hai lượt đề cập đang xét, không phải hai lượt đề cập khác cùng tên ở chỗ khác trong câu.",
    "Mỗi cặp có đúng một nhãn là tên quan hệ hoặc NO_RELATION, không có nhãn chưa rõ. Câu không đủ thông tin để khẳng định quan hệ thì gán NO_RELATION.",
  ]),
  H3("Phụ lục C.2: Bước kiểm tra thực thể"),
  P("Với mỗi lượt đề cập, người gán chọn VALID nếu thực thể đúng kiểu, hoặc INVALID nếu thực thể sai kiểu, quá chung chung hay không phải thực thể y khoa. Ranh giới lệch một chút nhưng phần chính đúng kiểu thì vẫn là VALID. Bảng C.1 nêu tiêu chí cho từng loại."),
  T(["Loại", "VALID khi", "INVALID, ví dụ"], [
    ["CONDITION", "Bệnh, triệu chứng, tổn thương hay tình trạng bất thường; “huyết áp” khi mang nghĩa bệnh tăng huyết áp", "Tên chung chung như bệnh lý, biến chứng; tác nhân gây bệnh như vi khuẩn; trạng thái bình thường như có thai; “huyết áp” khi là chỉ số đo"],
    ["DRUG", "Thuốc, hoạt chất, vắc xin, kháng sinh, kể cả thực phẩm chức năng, thảo dược, vitamin và mỹ phẩm điều trị", "Động từ như kiểm soát, chỉ định; chất trong cơ thể như cortisol; dinh dưỡng chung như chất béo, protein"],
    ["PROCEDURE", "Thủ thuật và phương pháp điều trị cụ thể như phẫu thuật, hóa trị, nội soi, vật lý trị liệu", "Động từ chung như cải thiện, phục hồi; hành động dùng thuốc như uống thuốc; chữ “điều trị” đứng một mình"],
    ["TEST", "Xét nghiệm, chẩn đoán hình ảnh, thăm khám như siêu âm, MRI, điện tâm đồ", "Nghiên cứu khoa học; quá trình sinh lý như chuyển hóa, tuần hoàn"],
    ["BODY_PART", "Cơ quan, bộ phận, mô, dịch cơ thể như não, tim, khớp, máu", "Quá chung chung như cơ thể, tế bào; không phải bộ phận như gen, polyp"],
    ["DOSAGE", "Liều, lượng, hàm lượng hay tần suất của thuốc khi dùng như “hai viên”, “năm mươi mg”, “ngày hai lần”", "Tính từ như cao, thấp; số liệu thống kê như tỷ lệ, phần trăm bệnh nhân; chỉ số cơ thể như nhịp tim"],
  ], [1700, 3900, 4038], { size: 20 }),
  CAP("Bảng C.1. Tiêu chí VALID và INVALID cho từng loại thực thể ở bước kiểm tra thực thể"),
  DESC("Bảng là căn cứ để loại các lượt đề cập sai kiểu trước khi gán quan hệ."),
  H3("Phụ lục C.3: Bước gán quan hệ"),
  P("Mỗi cặp có cả hai thực thể VALID được gán tên quan hệ hoặc NO_RELATION, với chiều của cặp cố định theo lược đồ. Bảng C.2 nêu ví dụ dương và âm cho từng quan hệ cùng các quy định cho trường hợp mơ hồ."),
  T(["Quan hệ", "Ví dụ dương", "Ví dụ âm và quy định"], [
    ["located_at", "“đau thắt lưng”, “cục máu đông ở trong tim”, “thiếu máu cơ tim”", "Bộ phận chỉ được nhắc cùng câu, như “rung nhĩ gây biến chứng ở não”; khi liệt kê nhiều triệu chứng trước một bộ phận, chỉ triệu chứng đứng sát bộ phận là dương; phủ định vẫn là dương"],
    ["treated_by", "“thuốc corticoid để điều trị cho bệnh gút”, “uống thuốc huyết áp để kiểm soát huyết áp”", "Phòng bệnh khi chưa mắc là âm; tác dụng phụ là âm; câu hỏi chưa có câu trả lời là âm; giả định như “nếu bị Y thì dùng X” là dương"],
    ["treated_by_procedure", "“phẫu thuật điều trị béo phì”, “kích thích não sâu giúp cải thiện chậm cử động”", "Như treated_by; không xét kết quả điều trị, đã dùng X cho Y thì vẫn là dương"],
    ["diagnosed_by", "“xét nghiệm sarscov2”, “đọc điện tâm đồ kết luận có rung nhĩ”", "Xét nghiệm và bệnh chỉ cùng xuất hiện trong câu là âm"],
    ["has_dosage", "“uống hai viên đông trùng hạ thảo mỗi ngày”, “tiêm hai mũi vắc xin”", "Lượng là của thứ khác hoặc là số liệu thống kê là âm"],
  ], [2200, 3600, 3838], { size: 20 }),
  CAP("Bảng C.2. Ví dụ dương, ví dụ âm và quy định cho từng quan hệ"),
  DESC("Bảng dùng làm tài liệu tham chiếu cho người gán khi gặp các trường hợp khó."),
  H3("Phụ lục C.4: Định dạng dữ liệu"),
  P("Mỗi dòng JSONL là một câu với các trường id, source_split, source_row_index, text, entities và relations. Mỗi thực thể có id, text, label, start, end và validity, còn mỗi cặp có head, tail, allowed_relation và label. Tập kiểm tra giữ thêm trường label_v1 là nhãn của lượt gán đầu, nhờ đó có thể so sánh hai tiêu chí gán."),
);

// ===== PHỤ LỤC E: ICD =====
add(
  HA("Phụ lục D: Bảng mã ICD-10 trên gold v1", true),
  P("Bảng D.1 trình bày mã ICD-10 mà hệ thống gán cho từng cụm CONDITION của gold v1 sau bản sửa, kèm cách khớp và kết quả kiểm tra thủ công."),
  T(["Cụm CONDITION", "Số lần", "Mã", "Tên chuẩn", "Cách khớp", "Đánh giá", "Trước sửa"], icd.items.map((o) => [o.text, o.mentions, o.code, o.label, `${o.method} (${f(o.score, 2)})`, o.verdict, o.before && o.before !== o.code ? o.before : (o.before ? "=" : "(không có)")]), [1800, 700, 900, 2600, 1300, 1100, 1238], { size: 18 }),
  CAP(`Bảng D.1. Mã ICD-10 của ${icd.items.length} cụm CONDITION trong gold v1 sau bản sửa`),
  DESC("Bảng cho thấy từng mã được gán bằng cách nào và kết quả kiểm tra thủ công của mã đó."),
);

// ===== PHỤ LỤC F: JSON =====
add(
  HA("Phụ lục E: Ví dụ đầu ra JSON đầy đủ", true),
  P("Ví dụ E.1 trình bày đầu ra đầy đủ dạng JSON của pipeline cho câu đã dùng ở Ví dụ 3.1."),
  ...CODE(["{", `  "text": ${JSON.stringify(demo.text)},`, "  \"entities\": [", ...demo.entities.map((e, i, a) => "    " + JSON.stringify({ id: e.id, surface_text: e.surface_text, label: e.label, start_char: e.start_char, end_char: e.end_char, confidence: e.confidence, ...(e.re_excluded ? { re_excluded: e.re_excluded } : {}) }) + (i < a.length - 1 ? "," : "")), "  ],", "  \"relations\": [", ...demo.relations.map((x, i, a) => "    " + JSON.stringify({ head: x.head, tail: x.tail, label: x.label, score: Number(x.score.toFixed(4)), status: x.status }) + (i < a.length - 1 ? "," : "")), "  ],", `  "re_metadata": ${JSON.stringify(demo.re_metadata)}`, "}"]),
  CAP("Ví dụ E.1. Đầu ra đầy đủ của pipeline NER và RE dạng JSON, đã rút gọn các trường trùng lặp"),
  DESC("Ví dụ minh họa đầy đủ các trường mà hệ thống trả về cho một câu."),
);

const TEST_FILES = [
  ["test_ner_pipeline.py", "Tách từ và dấu câu, ánh xạ sáu nhãn thực thể, nhận diện liều thuốc, câu rỗng, câu không có nội dung y tế, văn bản dài"],
  ["test_normalization.py", "Chuẩn hóa ICD-10 và RxNorm: khớp chính xác, đồng nghĩa, khớp gần đúng có ràng buộc, các ca từng gán sai, danh sách top-k, hai chế độ trả lời"],
  ["test_normalization_eval.py", "Các độ đo chuẩn hóa (Accuracy, Top-k, MRR, xử lý NIL) so với kết quả đếm tay"],
  ["test_end_to_end_pipeline.py", "Toàn luồng từ văn bản đến kết quả, bật và tắt bước chuẩn hóa"],
  ["test_relation_pipeline.py", "Các bước dữ liệu quan hệ: lô gán nhãn của LLM, kiểm tra nhãn trả về, đánh dấu câu trên phiếu, khung câu của dữ liệu sinh"],
  ["test_relation_extraction.py", "Nạp dữ liệu quan hệ, kiểm tra vị trí, chiều và mã thực thể, chia dữ liệu không rò rỉ, đánh dấu thực thể, lưu và nạp mô hình, độ đo"],
  ["test_re_bert_model.py", "Mô hình ViHealthBERT: trung bình xác suất ba seed, quan hệ chưa hỗ trợ do luật đảm nhận, nạp mô hình đã lưu"],
  ["test_re_benchmark.py", "Các baseline RE, phép hợp mô hình với luật, hệ số kappa, hàm chấm NER"],
  ["test_knowledge_graph.py", "Gộp nút theo mã, cộng dồn cạnh, lọc thực thể chung, xuất JSON/CSV/GraphML/HTML"],
  ["test_web_app.py", "API của giao diện: trả đúng kết quả pipeline dạng JSON, từ chối văn bản rỗng hoặc quá dài, báo lỗi khi không nạp được mô hình"],
  ["test_translated_en.py", "Chuyển thẻ thực thể của dữ liệu dịch thành vị trí ký tự, phát hiện thẻ hỏng"],
];
// ===== PHỤ LỤC G: tests =====
add(
  HA("Phụ lục F: Tổng hợp ca kiểm thử", true),
  P(`Bộ kiểm thử tự động bằng pytest gồm ${nTests} ca, chia theo mười một tệp trong thư mục tests/. Bảng F.1 tổng hợp số ca và nội dung kiểm thử của từng tệp, và toàn bộ ca đều đạt.`),
  T(["Tệp kiểm thử", "Số ca", "Nội dung kiểm thử"], TEST_FILES.map(([f, d]) => [f, X.tests.filter((x) => x.startsWith(`tests/${f}::`)).length, d])
    .concat([["Tổng", nTests, ""]]), [3000, 900, 5738], { size: 20, right: [1] }),
  CAP(`Bảng F.1. Số ca kiểm thử và nội dung kiểm thử của từng tệp`),
  DESC("Bảng giúp người đọc thấy mỗi thành phần của hệ thống đều có kiểm thử tự động đi kèm."),
);


function ablText(short) {
  const m = (k) => abl[k].strict_exact_match["micro avg"]["f1-score"];
  const full = s["micro avg"]["f1-score"];
  const d = (k) => full - m(k);
  const sg = (x) => (x >= 0 ? "+" : "") + f(x);
  const dosD = s.DOSAGE["f1-score"] - abl.no_dosage.strict_exact_match.DOSAGE["f1-score"];
  const txt = `So với chỉ dùng mô hình (strict micro-F1 ${f(m("model_only"))}), pipeline đầy đủ thay đổi ${sg(d("model_only"))}; riêng luật liều đóng góp ${sg(d("no_dosage"))} (DOSAGE strict F1 thay đổi ${sg(dosD)}) và nhóm Luật 1/1b/2 đóng góp ${sg(d("no_rules"))}.`;
  const fd = s.DOSAGE, nd = abl.no_dosage.strict_exact_match.DOSAGE;
  const detail = ` Trên tập test, luật liều chỉ thêm ${fd.tp - nd.tp} TP và ${fd.fp - nd.fp} FP cho DOSAGE (TP từ ${nd.tp} lên ${fd.tp}, FP từ ${nd.fp} lên ${fd.fp}): văn bản nói hầu như không chứa cụm liều dạng “500mg 2 viên/ngày” mà luật được thiết kế để bắt, còn phần lớn DOSAGE gold là đơn vị đo nói chung. Nhóm Luật 1/1b/2 có tác động ngược chiều theo loại: DRUG strict F1 tăng ${sg(s.DRUG["f1-score"] - abl.no_rules.strict_exact_match.DRUG["f1-score"])} (Luật 1 bỏ từ hành động bị gán DRUG), nhưng DOSAGE giảm ${f(abl.no_rules.strict_exact_match.DOSAGE["f1-score"] - s.DOSAGE["f1-score"])} và CONDITION giảm ${f(abl.no_rules.strict_exact_match.CONDITION["f1-score"] - s.CONDITION["f1-score"])}, vì Luật 2 gộp các từ như “cao”, “nặng” vào CONDITION trong khi gold VietMed-NER gán chúng là UNITCALIBRATOR. Đây là ví dụ rõ về một luật đúng với định nghĩa của đề tài nhưng bị phạt bởi quy ước của dữ liệu nguồn. Như vậy luật liều có giá trị cho văn bản đơn thuốc nhưng gần như không ảnh hưởng điểm trên VietMed-NER, và các luật hậu xử lý chỉ cải thiện rất nhỏ. Không có kiểm định thống kê cho các chênh lệch này.`;
  return short ? txt : txt + detail;
}

add(
  new Paragraph({ children: runs("KẾT QUẢ KIỂM TRA TURNITIN", { bold: true, size: 28 }), alignment: AlignmentType.CENTER, pageBreakBefore: true, spacing: { before: 240, after: 120 } }),
  new Paragraph({ children: runs("(In trang đầu tiên trong báo cáo kiểm tra Turnitin và đóng vào cuối quyển)", { italics: true }), alignment: AlignmentType.CENTER }),
);

// ---------- tài liệu ----------
const heading = (size, before, after) => ({ run: { font: FONT, size, bold: true, color: "000000" }, paragraph: { spacing: { before, after }, keepNext: true, keepLines: true } });
const PAGE_FOOTER = () => new Footer({ children: [new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 0 }, children: [new TextRun({ children: [PageNumber.CURRENT], font: FONT, size: 24 })] })] });
const doc = new Document({
  creator: "", title: "Báo cáo khóa luận", features: { updateFields: true },
  styles: {
    default: { document: { run: { font: FONT, size: BODY }, paragraph: { spacing: { before: 120, after: 0, line: 312 } } } },
    paragraphStyles: [
      // theo mẫu: chương 18pt đậm căn giữa, mục 14pt đậm, tiểu mục 14pt đậm nghiêng, chữ thường 13pt giãn 1,3
      { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true, run: { font: FONT, size: 36, bold: true, color: "000000" }, paragraph: { spacing: { before: 240, after: 240, line: 312 }, keepNext: true, keepLines: true, alignment: AlignmentType.CENTER, outlineLevel: 0 } },
      { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true, run: { font: FONT, size: 26, bold: true, color: "000000" }, paragraph: { spacing: { before: 240, after: 60, line: 312 }, keepNext: true, keepLines: true, outlineLevel: 1 } },
      { id: "Heading3", name: "Heading 3", basedOn: "Normal", next: "Normal", quickFormat: true, run: { font: FONT, size: 26, bold: true, color: "000000" }, paragraph: { spacing: { before: 180, after: 60, line: 312 }, keepNext: true, keepLines: true, outlineLevel: 2 } },
      { id: "Heading4", name: "Heading 4", basedOn: "Normal", next: "Normal", quickFormat: true, run: { font: FONT, size: 26, bold: true, color: "000000" }, paragraph: { spacing: { before: 160, after: 60, line: 312 }, keepNext: true, keepLines: true, outlineLevel: 3 } },
      { id: "TOC1", name: "toc 1", basedOn: "Normal", next: "Normal", run: { font: FONT, size: 26, bold: true }, paragraph: { spacing: { before: 120, after: 0, line: 300 } } },
      { id: "TOC2", name: "toc 2", basedOn: "Normal", next: "Normal", run: { font: FONT, size: 26, bold: true }, paragraph: { spacing: { before: 40, after: 0, line: 300 }, indent: { left: 216 } } },
      { id: "TOC3", name: "toc 3", basedOn: "Normal", next: "Normal", run: { font: FONT, size: 26 }, paragraph: { spacing: { before: 0, after: 0, line: 300 }, indent: { left: 446 } } },
      { id: "TOC4", name: "toc 4", basedOn: "Normal", next: "Normal", run: { font: FONT, size: 26 }, paragraph: { spacing: { before: 60, after: 0, line: 300 } } },
      { id: "TableofFigures", name: "table of figures", basedOn: "Normal", next: "Normal", run: { font: FONT, size: 26 }, paragraph: { spacing: { before: 60, after: 0, line: 300 } } },
      { id: "BangCaption", name: "BangCaption", basedOn: "Normal", next: "Normal", run: { font: FONT, size: 26 }, paragraph: { alignment: AlignmentType.CENTER } },
      { id: "HinhCaption", name: "HinhCaption", basedOn: "Normal", next: "Normal", run: { font: FONT, size: 26, italics: true }, paragraph: { alignment: AlignmentType.CENTER } },
      { id: "OtherCaption", name: "OtherCaption", basedOn: "Normal", next: "Normal", run: { font: FONT, size: 26 }, paragraph: { alignment: AlignmentType.CENTER } },
    ],
  },
  numbering: {
    config: [
      { reference: "bullets", levels: [{ level: 0, format: LevelFormat.BULLET, text: "●", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 720, hanging: 360 } } } }, { level: 1, format: LevelFormat.BULLET, text: "–", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 1440, hanging: 360 } } } }] },
      ...REFS.map((ref, i) => ({ reference: ref, levels: [{ level: 0, format: LevelFormat.DECIMAL, text: ref === "refs" ? "[%1]" : "%1.", alignment: AlignmentType.LEFT, style: { paragraph: { indent: ref === "refs" ? { left: 582, hanging: 582 } : { left: 720, hanging: 500 } } } }] })),
    ],
  },
  sections: [{
    // phần đầu: lề và số trang La Mã như mẫu
    properties: { page: { size: { width: 11906, height: 16838 }, margin: { top: 1418, bottom: 1418, left: 1985, right: 1418 }, pageNumbers: { start: 1, formatType: NumberFormat.LOWER_ROMAN } } },
    footers: { default: PAGE_FOOTER() },
    children: FRONT,
  }, {
    // phần thân (từ MỞ ĐẦU): số trang Ả Rập từ 1
    properties: { page: { size: { width: 11906, height: 16838 }, margin: { top: 1418, bottom: 1418, left: 1985, right: 1418 }, pageNumbers: { start: 1, formatType: NumberFormat.DECIMAL } } },
    footers: { default: PAGE_FOOTER() },
    children: C,
  }],
});

// thay chỗ kết quả pytest nếu có
(process.env.FIRST_LOG && fs.writeFileSync(process.env.FIRST_LOG, FIRST_LOG.join("\n"), "utf8"), Packer.toBuffer(doc)).then((buf) => { fs.writeFileSync(OUT, buf); console.log("written", OUT, buf.length); });

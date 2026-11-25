"""Bộ rule cho (C) sinh dữ liệu bằng LLM.

Có ba phần:
  1. RELATION_RULES / ENTITY_RULES: luật gán nhãn rút gọn từ relation/guideline.md (khóa 19/11,
     bổ sung 20/11). Prompt sinh chỉ chèn luật của quan hệ đích; prompt kiểm tra chèn tất cả.
  2. VARIANTS: các kiểu mẫu cần sinh cho từng quan hệ. Mỗi kiểu ứng với một mục trong guideline,
     nên mẫu sinh ra phủ đúng các trường hợp khó (dương khó và âm khó), không chỉ câu dễ.
  3. check_generation(): các rule kiểm tra bằng code (V1–V8), chạy trước khi gọi LLM kiểm tra.

Đổi bất kỳ thứ gì ở đây thì tăng PROMPT_VERSION trong synth_llm.py.
"""
import difflib
import re
import unicodedata

from relation_extraction.data import RELATIONS

from .common import norm, parse_tagged, words

# ---------------------------------------------------------------------------
# 1. Luật gán nhãn (rút gọn từ relation/guideline.md)
# ---------------------------------------------------------------------------

GENERAL_RULES = """\
- Chỉ gán điều mà câu nói ra, không gán điều đúng về y học. Chỉ dùng chính câu đó, không suy từ ngữ cảnh ngoài câu.
- Quan hệ phải nối đúng hai mention đang xét, không phải mention khác cùng tên ở chỗ khác trong câu.
- Mỗi cặp có đúng một nhãn: tên quan hệ hoặc NO_RELATION. Không đủ thông tin để khẳng định thì NO_RELATION.
- Câu bị cắt mất phần nối hai thực thể: dương nếu phần còn lại đủ rõ, nếu không thì NO_RELATION.
- Nói về động vật hay thí nghiệm: NO_RELATION, trừ khi câu nói rõ đó là điều trị hay chẩn đoán."""

ENTITY_RULES = """\
- CONDITION: bệnh, triệu chứng, tổn thương, tình trạng bất thường. INVALID: tên chung chung (bệnh lý, triệu chứng, biến chứng); tác nhân (vi khuẩn, virus); trạng thái bình thường (có thai, có kinh); từ không phải bệnh (chậm, tử vong, di truyền). "huyết áp" VALID khi là bệnh tăng huyết áp ("bị huyết áp", "thuốc huyết áp"), INVALID khi là chỉ số đo.
- DRUG: thuốc, hoạt chất, vắc xin, kháng sinh, thực phẩm chức năng, thảo dược, vitamin, mỹ phẩm điều trị. INVALID: động từ (kiểm soát, chỉ định, phòng ngừa); chất trong cơ thể (melanin, cortisol, sữa mẹ); dinh dưỡng chung (chất béo, protein).
- PROCEDURE: thủ thuật, phương pháp điều trị cụ thể (phẫu thuật, mổ, hóa trị, xạ trị, nội soi, vật lý trị liệu). INVALID: động từ chung (cải thiện, hỗ trợ, chăm sóc); hành động dùng thuốc (uống thuốc, tiêm); đồ vật; chữ "điều trị" đứng một mình.
- TEST: xét nghiệm, chẩn đoán hình ảnh, thăm khám (siêu âm, MRI, CT, X-quang, điện tâm đồ, "kiểm tra" khi là khám bệnh). INVALID: nghiên cứu khoa học; quá trình sinh lý (chuyển hóa, tuần hoàn).
- BODY_PART: cơ quan, bộ phận, mô, dịch cơ thể (não, tim, da, khớp, máu, thắt lưng). INVALID: quá chung (cơ thể, hệ, tế bào); không phải bộ phận (gen, dna, sắc tố).
- DOSAGE: liều, lượng, hàm lượng, tần suất của thuốc khi dùng ("một viên", "hai mũi", "năm mươi mg", "ngày hai lần"). INVALID: tính từ (cao, thấp, rất nhiều); thứ tự (thứ nhất); thống kê (tỷ lệ, phần trăm bệnh nhân); chỉ số cơ thể (nhịp tim, đường huyết)."""

RELATION_RULES = {
    "located_at": """\
located_at (CONDITION → BODY_PART): bệnh hoặc triệu chứng xảy ra ở bộ phận đó.
- Dương: "đau thắt lưng", "viêm loét ở cái miệng nối", "cục máu đông ở trong tim", "tê bì chân tay", "thiếu máu cơ tim".
- Phủ định vẫn là dương: "không bị đau khớp gối" → đau → khớp gối là located_at.
- Âm: bộ phận chỉ được nhắc cùng câu mà không phải chỗ bệnh xảy ra ("rung nhĩ gây biến chứng ở não": rung nhĩ → não âm).
- Liệt kê nhiều triệu chứng trước một bộ phận: chỉ triệu chứng đứng sát bộ phận là dương ("chóng mặt tê bì chân tay": chóng mặt → chân tay âm), trừ khi câu nói rõ cả cụm cùng ở bộ phận đó.""",
    "treated_by": """\
treated_by (CONDITION → DRUG): thuốc được dùng hoặc chỉ định để chữa, giảm hay kiểm soát bệnh đó.
- Dương: "thuốc corticoid để điều trị cho bệnh gút", "viêm họng được chữa bằng thuốc kháng sinh", "uống thuốc huyết áp để kiểm soát huyết áp".
- Không xét kết quả: đã dùng X cho Y mà không đỡ vẫn là dương.
- Giả định hay hướng dẫn chung "nếu bị Y thì dùng X" là dương. "X dùng cho người có bệnh Y" là dương.
- Câu hỏi đã kèm khẳng định ("tại sao Y phải dùng X") là dương.
- Âm: câu nói không dùng hoặc không nên dùng X cho Y ("thuốc chống tiểu cầu không phải là cách cho cục máu đông").
- Âm: phòng bệnh khi chưa mắc. Ngoại lệ: phòng biến chứng của bệnh đang có thì dương với bệnh đang có ("người rung nhĩ uống thuốc kháng đông để phòng đột quỵ": rung nhĩ → kháng đông dương, đột quỵ → kháng đông âm).
- Âm: tác dụng phụ, thuốc gây ra bệnh ("thuốc giảm đau gây viêm loét dạ dày").
- Âm: câu hỏi chưa có câu trả lời ("X có chữa được Y không").""",
    "treated_by_procedure": """\
treated_by_procedure (CONDITION → PROCEDURE): thủ thuật hay phương pháp được dùng để chữa, giảm hay kiểm soát bệnh đó.
- Dương: "phẫu thuật điều trị béo phì", "kích thích não sâu sẽ giúp cải thiện triệu chứng chậm cử động".
- Không xét kết quả: "đã thử các phương pháp trị liệu béo phì nhưng thất bại" là dương.
- Giả định hay hướng dẫn chung "nếu bị Y thì làm X" là dương.
- Âm: câu nói không làm hoặc không nên làm X cho Y.
- Âm: phòng bệnh khi chưa mắc (ngoại lệ phòng biến chứng của bệnh đang có, như treated_by).
- Âm: thủ thuật gây ra bệnh ("hóa trị dẫn đến sụt cân": sụt cân → hóa trị âm).
- Âm: câu hỏi chưa có câu trả lời.""",
    "diagnosed_by": """\
diagnosed_by (CONDITION → TEST): xét nghiệm hay thăm khám được dùng để phát hiện, chẩn đoán hay theo dõi bệnh đó.
- Dương: "xét nghiệm sarscov2", "test covid phải âm tính", "đọc điện tâm đồ kết luận có rung nhĩ", "kiểm tra để biết có phải đau do thoái hóa".
- Âm: xét nghiệm và bệnh chỉ cùng xuất hiện ("đi kiểm tra thì đã bị ung thư rồi sụt cân": sụt cân → kiểm tra âm, vì sụt cân không phải thứ được kiểm tra).
- Âm: xét nghiệm dành cho một bệnh khác trong câu.""",
    "has_dosage": """\
has_dosage (DRUG → DOSAGE): liều hay lượng đó là của chính thuốc đó.
- Dương: "uống hai viên đông trùng hạ thảo mỗi ngày", "tiêm hai mũi vắc xin".
- Âm: lượng là của thứ khác (thuốc khác, thức ăn, chỉ số đo: "mười milimet thủy ngân huyết áp tâm thu").
- Âm: lượng là số liệu thống kê, không phải liều.""",
}

# ---------------------------------------------------------------------------
# 2. Kiểu mẫu cần sinh
# ---------------------------------------------------------------------------
# Mỗi kiểu: polarity (POS/NEG), mô tả cho LLM, ví dụ, và cue (regex) bắt buộc phải có trong câu mới
# (rule V6). cue = None nghĩa là không kiểm tra cue. min_gap: số từ tối thiểu giữa hai thực thể (V7).

_CUE_COND = r"\b(nếu|khi|trường hợp)\b"
_CUE_FAILED = r"\b(không|chưa|vẫn)\b"
_CUE_NOT = r"\b(không|chẳng|đừng|chưa)\b"
_CUE_PREVENT = r"\b(phòng|ngừa|dự phòng|tránh)\b"
_CUE_CAUSE = r"\b(gây|dẫn đến|tác dụng phụ|làm cho|bị)\b"
_CUE_QUESTION = r"\b(không|chưa|à|hả|sao)\s*$"

VARIANTS = {
    "located_at": [
        ("POS_EXPLICIT", "POS", "bệnh hoặc triệu chứng xảy ra ở bộ phận, có từ nối rõ (ở, tại, vùng, bên)",
         "bị viêm loét ở cái vùng dạ dày", None, 0),
        ("POS_ADJACENT", "POS", "bệnh đứng sát ngay trước bộ phận theo cách nói thông thường",
         "dạo này hay bị đau thắt lưng", None, 0),
        ("POS_NEGATED", "POS", "câu phủ định triệu chứng ở bộ phận, vẫn là dương",
         "uống thuốc xong thì không còn bị đau khớp gối nữa", r"\b(không|chưa|hết)\b", 0),
        ("POS_LONG_GAP", "POS", "vẫn là dương nhưng hai thực thể cách nhau ít nhất năm từ",
         "cái cục máu đông này nó hình thành ngay ở bên trong tim", None, 5),
        ("NEG_OTHER_SITE", "NEG", "bộ phận được nhắc nhưng không phải chỗ bệnh xảy ra, ví dụ biến chứng lan sang hoặc bộ phận của ý khác",
         "rung nhĩ thì sẽ gây biến chứng ở não", None, 0),
        ("NEG_LIST_FAR", "NEG", "liệt kê nhiều triệu chứng, triệu chứng đích không đứng sát bộ phận và câu không nói nó ở bộ phận đó",
         "hay bị chóng mặt rồi tê bì chân tay", None, 0),
        ("NEG_COOCCUR", "NEG", "bệnh và bộ phận ở hai ý khác nhau trong câu",
         "bị tiểu đường mấy năm nay rồi còn cái tim thì vẫn khỏe", None, 0),
    ],
    "treated_by": [
        ("POS_EXPLICIT", "POS", "câu nói rõ dùng thuốc X để chữa, giảm hay kiểm soát Y, có từ nối rõ ràng",
         "bị gút thì bác sĩ cho dùng thuốc corticoid để điều trị", None, 0),
        ("POS_LONG_GAP", "POS", "vẫn là dương nhưng hai thực thể cách nhau ít nhất năm từ, có xen ý phụ",
         "viêm họng mà kéo dài cả tuần rồi thì lúc đó mới được chữa bằng thuốc kháng sinh", None, 5),
        ("POS_CONDITIONAL", "POS", "hướng dẫn chung dạng nếu hoặc khi bị Y thì dùng X",
         "nếu mà bị đau dạ dày thì mình dùng thêm omeprazol", _CUE_COND, 0),
        ("POS_FAILED", "POS", "đã dùng X cho Y nhưng không đỡ, vẫn là dương vì không xét kết quả",
         "mất ngủ thì em uống melatonin cả tháng rồi mà vẫn không đỡ", _CUE_FAILED, 0),
        ("NEG_NOT_USED", "NEG", "câu nói rõ không dùng hoặc không nên dùng X cho Y",
         "cục máu đông thì thuốc chống tiểu cầu không phải là cách", _CUE_NOT, 0),
        ("NEG_PREVENTION", "NEG", "X dùng để phòng Y khi chưa mắc Y, không phải chữa Y",
         "tiêm vắc xin để phòng bệnh cúm cho trẻ", _CUE_PREVENT, 0),
        ("NEG_SIDE_EFFECT", "NEG", "X gây ra Y (tác dụng phụ), không phải chữa Y",
         "thuốc giảm đau dùng lâu sẽ gây viêm loét dạ dày", _CUE_CAUSE, 0),
        ("NEG_QUESTION", "NEG", "câu hỏi X có chữa được Y không, chưa có câu trả lời",
         "thuốc nam thì có chữa được bệnh gút không", _CUE_QUESTION, 0),
        ("NEG_COOCCUR", "NEG", "X và Y cùng xuất hiện nhưng ở hai ý khác nhau, câu không nói X dùng cho Y",
         "bị tiểu đường lâu năm rồi hôm qua thì có mua thêm vitamin c về uống cho khỏe", None, 0),
    ],
    "treated_by_procedure": [
        ("POS_EXPLICIT", "POS", "câu nói rõ làm thủ thuật X để chữa, giảm hay kiểm soát Y",
         "béo phì nặng thì có thể phẫu thuật để điều trị", None, 0),
        ("POS_LONG_GAP", "POS", "vẫn là dương nhưng hai thực thể cách nhau ít nhất năm từ, có xen ý phụ",
         "sỏi thận mà to quá không tự ra được thì người ta sẽ tán sỏi", None, 5),
        ("POS_CONDITIONAL", "POS", "hướng dẫn chung dạng nếu hoặc khi bị Y thì làm X",
         "khi mà bị thoát vị đĩa đệm thì nên tập vật lý trị liệu", _CUE_COND, 0),
        ("POS_FAILED", "POS", "đã làm X cho Y nhưng không đỡ, vẫn là dương vì không xét kết quả",
         "béo phì thì em đã thử phẫu thuật rồi mà vẫn không giảm được", _CUE_FAILED, 0),
        ("NEG_NOT_USED", "NEG", "câu nói rõ không làm hoặc không nên làm X cho Y",
         "viêm ruột thừa nhẹ thì chưa cần phải mổ ngay đâu", _CUE_NOT, 0),
        ("NEG_PREVENTION", "NEG", "X làm để phòng Y khi chưa mắc Y, không phải chữa Y",
         "tập vật lý trị liệu đều thì sẽ phòng được thoái hóa khớp", _CUE_PREVENT, 0),
        ("NEG_SIDE_EFFECT", "NEG", "X gây ra Y, không phải chữa Y",
         "hóa trị thì hay dẫn đến sụt cân với rụng tóc", _CUE_CAUSE, 0),
        ("NEG_QUESTION", "NEG", "câu hỏi X có chữa được Y không, chưa có câu trả lời",
         "châm cứu thì có chữa được đau thần kinh tọa không", _CUE_QUESTION, 0),
        ("NEG_COOCCUR", "NEG", "X và Y cùng xuất hiện nhưng ở hai ý khác nhau, câu không nói X làm cho Y",
         "mẹ em bị tiểu đường còn em thì năm ngoái mới đi mổ ruột thừa", None, 0),
    ],
    "diagnosed_by": [
        ("POS_EXPLICIT", "POS", "xét nghiệm hay thăm khám được làm để phát hiện, chẩn đoán hay theo dõi bệnh",
         "phải làm xét nghiệm máu để biết có bị tiểu đường không", None, 0),
        ("POS_RESULT", "POS", "kết quả xét nghiệm cho thấy hoặc kết luận có bệnh",
         "đi siêu âm thì bác sĩ kết luận là có sỏi thận", None, 0),
        ("POS_LONG_GAP", "POS", "vẫn là dương nhưng hai thực thể cách nhau ít nhất năm từ",
         "rung nhĩ thì mình phải đi đo cái điện tâm đồ thường xuyên", None, 5),
        ("NEG_COOCCUR", "NEG", "xét nghiệm và bệnh cùng xuất hiện nhưng bệnh không phải thứ được kiểm tra",
         "đi kiểm tra sức khỏe định kỳ thì thấy người hay mệt", None, 0),
        ("NEG_OTHER_TARGET", "NEG", "xét nghiệm dùng cho một mục đích hay bệnh khác, bệnh đích chỉ được nhắc kèm",
         "bị cao huyết áp nhưng hôm nay đi siêu âm là để xem thai", None, 0),
    ],
    "has_dosage": [
        ("POS_EXPLICIT", "POS", "liều hoặc lượng là của chính thuốc đó, nói rõ cách dùng",
         "mỗi ngày uống hai viên đông trùng hạ thảo", None, 0),
        ("POS_LONG_GAP", "POS", "vẫn là dương nhưng liều cách thuốc ít nhất năm từ",
         "vắc xin này thì trẻ nhỏ cần phải tiêm đủ hai mũi", None, 5),
        ("NEG_OTHER_OWNER", "NEG", "lượng là của thứ khác: thuốc khác, thức ăn, nước, chỉ số đo",
         "uống thuốc huyết áp xong rồi uống thêm hai cốc nước", None, 0),
        ("NEG_STATISTIC", "NEG", "lượng là số liệu thống kê hay mô tả, không phải liều dùng",
         "loại thuốc này thì hai phần ba người dùng thấy đỡ", None, 0),
    ],
}

SPEAKERS = [
    "bác sĩ giải thích trong chương trình tư vấn sức khỏe",
    "bệnh nhân kể lại bệnh của mình",
    "người nhà hỏi bác sĩ",
    "bác sĩ trả lời câu hỏi của thính giả",
]


def variant(relation, code):
    for v in VARIANTS[relation]:
        if v[0] == code:
            return {"code": v[0], "polarity": v[1], "desc": v[2], "example": v[3], "cue": v[4], "min_gap": v[5]}
    raise KeyError(f"{relation}/{code}")


# ---------------------------------------------------------------------------
# 3. Rule kiểm tra bằng code
# ---------------------------------------------------------------------------
MIN_WORDS, MAX_WORDS = 10, 40
PUNCT = re.compile(r"[.,;:!?\"“”()\[\]{}…]")
DIGIT = re.compile(r"\d")


def tag_sentence(text, entities):
    """Chèn thẻ [E1:TYPE]…[/E1] vào câu gốc."""
    out = text
    for e in sorted(entities, key=lambda e: -e["start"]):
        out = out[:e["start"]] + f"[{e['id']}:{e['label']}]" + out[e["start"]:e["end"]] + f"[/{e['id']}]" + out[e["end"]:]
    return out


def _same(a, b):
    return norm(a) == norm(b)


def check_generation(job, tagged, leak_grams, leak_n):
    """Trả về (text, entities, lỗi). lỗi rỗng nghĩa là qua hết V1–V8."""
    errors = []
    try:
        text, ents = parse_tagged(unicodedata.normalize("NFC", tagged.strip()))
    except (ValueError, KeyError) as exc:                                # V1 thẻ hợp lệ
        return None, None, [f"V1_tag:{exc}"]
    seed = {e["id"]: e for e in job["seed_entities"]}
    got = {e["id"]: e for e in ents}
    for eid in (job["head"], job["tail"]):                                # V2 giữ thực thể đích
        if eid not in got:
            errors.append(f"V2_missing:{eid}")
        elif not _same(got[eid]["text"], seed[eid]["text"]) or got[eid]["label"] != seed[eid]["label"]:
            errors.append(f"V2_changed:{eid}")
    for eid, e in got.items():                                            # V3 không thêm thực thể mới
        if eid not in seed or not _same(e["text"], seed[eid]["text"]) or e["label"] != seed[eid]["label"]:
            errors.append(f"V3_new_entity:{eid}")
    n = len(words(text))                                                  # V4 văn phong VietMed
    if not MIN_WORDS <= n <= MAX_WORDS:
        errors.append(f"V4_length:{n}")
    if text != text.lower():
        errors.append("V4_uppercase")
    if PUNCT.search(text):
        errors.append("V4_punct")
    if DIGIT.search(text):
        errors.append("V4_digit")
    if _same(text, job["seed_text"]):                                     # V5 khác câu gốc
        errors.append("V5_copy")
    v = variant(job["relation"], job["variant"])
    if v["cue"] and not re.search(v["cue"], norm(text)):                  # V6 có từ đặc trưng của kiểu mẫu
        errors.append(f"V6_cue:{job['variant']}")
    if errors:
        return text, ents, errors
    h, t = got[job["head"]], got[job["tail"]]
    first, second = sorted((h, t), key=lambda e: e["start"])
    gap = len(words(text[first["end"]:second["start"]]))
    if gap < v["min_gap"]:                                                # V7 khoảng cách cho POS_LONG_GAP
        errors.append(f"V7_gap:{gap}")
    w = words(text)                                                       # V8 rò rỉ sang dev/test
    if any(tuple(w[i:i + leak_n]) in leak_grams for i in range(len(w) - leak_n + 1)):
        errors.append("V8_leak")
    return text, ents, errors


def similarity(a, b):
    return difflib.SequenceMatcher(None, words(a), words(b)).ratio()


def pair_types_ok(relation, head, tail):
    return (head["label"], tail["label"]) == RELATIONS[relation]


# ---------------------------------------------------------------------------
# Luật v2 (24/11/2026): chỉnh theo kết quả chuyên gia chấm pilot_label_v1 (353 cặp, AI đúng 68%).
# Bằng chứng từng thay đổi: re_v3/data/silver/pilot_label_v1/phan_tich_loi_v1.md
#   (1) located_at v1 quá chặt (85/113 lỗi): chuyên gia nhận vị trí ngầm định theo kiến thức y khoa
#       khi bộ phận có trong câu và nói về cùng bệnh ("thiếu máu cơ tim" → tim, "rung nhĩ" → tim).
#   (2) mảnh từ bị NER cắt ("cơ" trong "cơ tim", "máu" trong "nhồi máu", "lao" trong "lao động"): INVALID.
#   (3) treated_by v1 quá dễ với thực phẩm chức năng / mỹ phẩm quảng cáo.
#   (4) "cấp cứu", "khám", "vào viện" không phải PROCEDURE (ghi chú chuyên gia).
# ---------------------------------------------------------------------------

GENERAL_RULES_V2 = """\
- Hai thực thể phải cùng nằm trong câu. Gán dương khi câu nói đến quan hệ, HOẶC khi câu đặt hai thực thể vào cùng một ý (cùng mệnh đề, cùng chủ đề đang bàn) và quan hệ đó đúng theo kiến thức y khoa chuẩn. Không gán dương chỉ vì hai thực thể cùng xuất hiện trong một danh sách liệt kê các thứ khác nhau.
- Quan hệ phải nối đúng hai mention đang xét, không phải mention khác cùng tên ở chỗ khác trong câu.
- Mỗi cặp có đúng một nhãn: tên quan hệ hoặc NO_RELATION.
- Câu bị cắt mất phần nối hai thực thể: dương nếu phần còn lại đủ rõ, nếu không thì NO_RELATION.
- Nói về động vật hay thí nghiệm: NO_RELATION, trừ khi câu nói rõ đó là điều trị hay chẩn đoán."""

ENTITY_RULES_V2 = ENTITY_RULES.replace(
    "chữ \"điều trị\" đứng một mình.",
    "chữ \"điều trị\" đứng một mình; hành động chăm sóc chung không phải phương pháp điều trị "
    "(cấp cứu, vào viện, nhập viện, khám, theo dõi, hồi sức).") + """
- MẢNH TỪ: thực thể chỉ là một phần của một từ hay thuật ngữ khác thì INVALID, dù chữ đó tự nó là tên bộ phận hay bệnh. Ví dụ: "cơ" trong "cơ tim", "máu" trong "nhồi máu"/"mỡ máu"/"đông máu", "huyết" trong "huyết khối", "mô" trong "mô hình", "lao" trong "lao động", "ruột" trong "ruột kích thích" khi là tên hội chứng. Ngoại lệ: thực thể là bộ phận đầy đủ đứng cuối tên bệnh ("tim" trong "thiếu máu cơ tim") vẫn VALID."""

RELATION_RULES_V2 = dict(RELATION_RULES)
RELATION_RULES_V2["located_at"] = """\
located_at (CONDITION → BODY_PART): bệnh hoặc triệu chứng xảy ra ở bộ phận đó.
- Dương khi câu nói rõ vị trí: "đau thắt lưng", "hoại tử ở vùng chi", "cục máu đông ở trong tim", "tê bì chân tay".
- Dương khi bộ phận nằm trong tên bệnh hoặc là cơ quan bị bệnh theo kiến thức y khoa, và câu đang nói về bệnh đó ở bộ phận đó: "thiếu máu cơ tim" → thiếu máu → tim; "rung nhĩ ... tim" → tim; "cục máu đông tắc mạch máu não" → não; "chảy máu ... nhu mô não" → nhu mô não; "hội chứng ruột kích thích ... đại tràng" → đại tràng; "táo bón ... đại tràng", "tiêu chảy ... ruột"; "tiêu xương ... xương hàm"; "covid ... đau rát họng" → họng.
- Phủ định vẫn là dương: "không bị đau khớp gối" → đau → khớp gối là located_at.
- Âm: bộ phận là chỗ của bệnh KHÁC, hoặc là chỗ bệnh gây biến chứng tới ("rung nhĩ gây nhồi máu não": rung nhĩ → não âm; "loạn nhịp tim ... nhồi máu não": loạn nhịp tim → não âm).
- Âm: liệt kê các triệu chứng khác nhau rồi mới đến bộ phận; chỉ triệu chứng đứng sát bộ phận là dương ("đau đầu chóng mặt mất ngủ tê bì chân tay": tê bì → chân tay dương, đau đầu/chóng mặt/mất ngủ → chân tay âm).
- Âm: bộ phận không liên quan về y khoa với bệnh đó (đau đầu → động mạch, huyết áp → khớp)."""
RELATION_RULES_V2["treated_by"] = RELATION_RULES["treated_by"] + """
- Dương cả khi câu chỉ nói thuốc có tác dụng với bệnh mà thuốc đó là điều trị chuẩn ("biphosphonate ... hủy xương", "bổ sung canxi ... loãng xương").
- Âm: thực phẩm chức năng, thảo dược, chất bổ sung, mỹ phẩm, đồ chăm sóc da được quảng cáo "giúp", "hỗ trợ", "ổn định" một bệnh mà không phải điều trị chuẩn ("omega3 cho người ung thư", "selen/đông trùng hạ thảo cho đái tháo đường", "5htp ... mất ngủ", "sữa rửa mặt, kem dưỡng ẩm giảm bỏng rát")."""
RELATION_RULES_V2["treated_by_procedure"] = RELATION_RULES["treated_by_procedure"] + """
- Dương khi câu nói tác dụng, tác dụng phụ hay hiệu quả của phương pháp đối với bệnh đang điều trị ("giảm tác dụng phụ của hóa trị xạ trị ... ung thư": ung thư → hóa trị dương).
- Âm: "cấp cứu", "vào viện", "theo dõi biến chứng sau phẫu thuật" không phải chữa bệnh đó."""
RELATION_RULES_V2["diagnosed_by"] = RELATION_RULES["diagnosed_by"] + """
- Dương: triệu chứng là lý do đi làm xét nghiệm hay thăm khám ("đau rát họng tìm đến thăm khám và test nhanh": đau → test dương); dấu hiệu được phát hiện qua lần kiểm tra ("tăng cân ... ở những lần kiểm tra sức khỏe" dương)."""

RULESETS = {
    "v1": {"general": GENERAL_RULES, "entity": ENTITY_RULES, "relation": RELATION_RULES},
    "v2": {"general": GENERAL_RULES_V2, "entity": ENTITY_RULES_V2, "relation": RELATION_RULES_V2},
}

# Luật v3: v2 đánh INVALID quá tay (66 cặp bị bỏ, 14 cặp đúng bị mất: "viêm", "bị tiêu", "đau",
# "thần kinh", "xương"...). Thu hẹp luật mảnh từ; giữ nguyên các luật quan hệ của v2.
ENTITY_RULES_V3 = ENTITY_RULES_V2.split("\n- MẢNH TỪ:")[0] + """
- Triệu chứng hay bệnh ngắn vẫn VALID khi câu nói một người bị nó: "đau", "viêm", "tê", "bị tiêu" (tiêu xương), "biến dạng", "nhiễm trùng". Chỉ INVALID các từ chung chung như "triệu chứng", "biến chứng", "bệnh lý", "rối loạn" đứng một mình.
- Bộ phận ngắn vẫn VALID khi đứng như một bộ phận: "xương", "thần kinh", "máu" (trong "chảy máu ở máu"? không), "dạ dày", "gáy".
- MẢNH TỪ (chỉ áp dụng khi rõ ràng): thực thể là một phần của một từ ghép khác nghĩa ngay sát nó thì INVALID: "lao" trong "lao động", "huyết" trong "huyết khối", "mô" trong "mô hình", "máu" trong "nhồi máu"/"mỡ máu"/"đông máu"/"thiếu máu", "cơ" trong "cơ tim" (khi đó bộ phận đúng là "tim" nếu "tim" cũng được gắn thẻ). Nếu không chắc là mảnh từ thì VALID."""
ENTITY_RULES_V3 = ENTITY_RULES_V3.replace('"máu" (trong "chảy máu ở máu"? không), ', '"máu" khi nói về máu, ')
RELATION_RULES_V3 = dict(RELATION_RULES_V2)
RELATION_RULES_V3["has_dosage"] = RELATION_RULES["has_dosage"] + """
- Dương: số viên trong một vỉ hay một liệu trình của thuốc ("vỉ hai tám viên thì hai mốt viên có progesterone và estrogen": progesterone/estrogen → hai mốt viên dương)."""
RULESETS["v3"] = {"general": GENERAL_RULES_V2, "entity": ENTITY_RULES_V3, "relation": RELATION_RULES_V3}

# Luật v4 (24/11/2026): chuyên gia trả lời hai câu hỏi sau khi chấm dev_label_v3:
#   (1) bệnh gây biến chứng ở cơ quan khác → CÓ tính located_at với cơ quan đó;
#   (2) "máu" là nơi xảy ra bệnh → TÙY BỆNH.
# Ghi vào relation/guideline.md, mục bổ sung 24/11.
RELATION_RULES_V4 = dict(RELATION_RULES_V3)
RELATION_RULES_V4["located_at"] = """\
located_at (CONDITION → BODY_PART): bệnh hoặc triệu chứng xảy ra ở bộ phận đó, hoặc gây tổn thương, biến chứng ở bộ phận đó.
- Dương khi câu nói rõ vị trí: "đau thắt lưng", "hoại tử ở vùng chi", "cục máu đông ở trong tim", "tê bì chân tay".
- Dương khi bộ phận nằm trong tên bệnh hoặc là cơ quan bị bệnh theo kiến thức y khoa, và câu đang nói về bệnh đó: "thiếu máu cơ tim" → tim; "rung nhĩ ... tim" → tim; "chảy máu ... nhu mô não"; "hội chứng ruột kích thích ... đại tràng"; "tiêu xương hàm ... xương"; "nha chu ... răng"; "đau cột sống thắt lưng" → cột sống, thắt lưng.
- Dương khi câu nói bệnh gây biến chứng hay tổn thương ở bộ phận đó (quyết định của chuyên gia 24/11): "xơ vữa động mạch gây đột quỵ não, đột quỵ tim" → xơ vữa động mạch → não, tim dương; "rung nhĩ gây nhồi máu não" → rung nhĩ → não dương; "đột quỵ não đột quỵ tim" → đột quỵ → não, tim dương.
- "máu" là bộ phận, tùy bệnh: DƯƠNG với bệnh của chính máu, mỡ máu, huyết áp hay mạch máu (mỡ máu, rối loạn mỡ máu, huyết áp cao, xơ vữa động mạch, hẹp lòng động mạch, chảy máu, tụ máu, đông máu, nhiễm trùng máu). ÂM với bệnh của cơ quan khác chỉ ảnh hưởng gián tiếp tới máu (suy gan làm rối loạn đông máu, loạn nhịp tim, rung nhĩ). ÂM khi "máu" chỉ là vật được truyền, được bổ hay bị mất ("truyền máu", "thuốc bổ máu", "ra máu nhiều"): khi đó "thiếu máu" → "máu" âm.
- Phủ định vẫn là dương: "không bị đau khớp gối" → đau → khớp gối là located_at.
- Âm: bộ phận là chỗ của bệnh KHÁC và câu không nói bệnh đang xét gây ra gì ở đó.
- Âm: liệt kê các triệu chứng khác nhau rồi mới đến bộ phận; chỉ triệu chứng đứng sát bộ phận là dương ("đau đầu chóng mặt mất ngủ tê bì chân tay": tê bì → chân tay dương, đau đầu/chóng mặt → chân tay âm).
- Âm: bộ phận không liên quan về y khoa với bệnh (đau đầu → động mạch, huyết áp → khớp)."""
RULESETS["v4"] = {"general": GENERAL_RULES_V2, "entity": ENTITY_RULES_V3, "relation": RELATION_RULES_V4}

r"""Chèn hai trang bìa của mẫu khóa luận (Trường Công nghệ, ĐH Kinh tế Quốc dân) vào báo cáo do
build_report.js sinh ra, điền thông tin từ thong_tin_bia.json.

Bìa lấy nguyên từ tệp mẫu (khung viền, logo, gáy sách) để giữ đúng định dạng; chỉ thay chữ.
Chữ nằm trong [[...]] ở thong_tin_bia.json là chỗ chưa điền và được tô vàng.
Sau bước này, update_fields.ps1 mở tệp bằng Word để cập nhật mục lục, danh mục bảng/hình.

    .venv\Scripts\python.exe -X utf8 outputs/bao_cao_khoa_luan_2026-11-05/apply_template.py ^
        <mau.docx> <body.docx> outputs/bao_cao_khoa_luan_2026-11-05/thong_tin_bia.json <out.docx>
"""
import json
import re
import sys
import zipfile

tpl_path, body_path, info_path, out_path = sys.argv[1:5]
info = json.load(open(info_path, encoding="utf-8"))
tpl = zipfile.ZipFile(tpl_path)
txml = tpl.read("word/document.xml").decode("utf-8")

# ---- 1. phần bìa: từ đầu thân tới hết đoạn chứa sectPr thứ hai (bìa ngoài + bìa trong)
ends = [m.end() for m in re.finditer(r"</w:sectPr>", txml)]
start = txml.index("<w:body>") + len("<w:body>")
cover = txml[start:txml.index("</w:p>", ends[1]) + len("</w:p>")]
cover = re.sub(r"<w:(?:header|footer)Reference [^>]*/>", "", cover)
cover = re.sub(r'<w:pStyle w:val="(?:Heading1|1)"/>', "", cover)  # không để bìa lọt vào mục lục
assert set(re.findall(r'r:(?:embed|id|link)="([^"]+)"', cover)) == {"rId8"}, re.findall(r'r:(?:embed|id)="([^"]+)"', cover)
cover = cover.replace('r:embed="rId8"', 'r:embed="rIdCoverImg1"')

HL_BEFORE = re.compile(r"<w:(?:u|effect|bdr|shd|fitText|vertAlign|rtl|cs|em|lang|eastAsianLayout|specVanish|oMath)[ />]")


def highlight(run):
    if "<w:rPr>" not in run:
        return run.replace("<w:r>", '<w:r><w:rPr><w:highlight w:val="yellow"/></w:rPr>', 1) if run.startswith("<w:r>") else \
            re.sub(r"(<w:r[^>]*>)", r'\1<w:rPr><w:highlight w:val="yellow"/></w:rPr>', run, count=1)
    i, j = run.index("<w:rPr>"), run.index("</w:rPr>")
    rpr = run[i:j]
    m = HL_BEFORE.search(rpr)
    k = i + (m.start() if m else len(rpr))
    return run[:k] + '<w:highlight w:val="yellow"/>' + run[k:]


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def set_texts(par, texts):
    """Gán lần lượt texts cho các w:t của đoạn (thừa thì để rỗng); tô vàng w:t có [[...]]."""
    k = 0

    def one(m):
        nonlocal k
        r = m.group(0)
        if not re.search(r"<w:t[ >]", r):  # run chỉ có tab/ngắt dòng
            return r
        new = texts[k] if k < len(texts) else ""
        k += 1
        hl = "[[" in new
        new = new.replace("[[", "").replace("]]", "")
        nr = re.sub(r"<w:t(?: [^>]*)?>[^<]*</w:t>", lambda _: f'<w:t xml:space="preserve">{esc(new)}</w:t>', r, count=1)
        return highlight(nr) if hl else nr
    return re.sub(r"<w:r[ >](?:(?!</w:r>).)*?</w:r>", one, par, flags=re.S)


def value(key, upper=False):
    v = info[key]
    if upper:
        v = re.sub(r"(\[\[)?([^\[\]]+)(\]\])?", lambda m: (m.group(1) or "") + m.group(2).upper() + (m.group(3) or ""), v)
    return v


LABELS = {"Tên sinh viên": "ten_sinh_vien", "Mã sinh viên": "ma_sinh_vien", "Lớp": "lop", "Ngành": "nganh",
          "Khoa": "khoa", "Giảng viên hướng dẫn": "giang_vien_huong_dan"}


def fill(par):
    ts = re.findall(r"<w:t(?: [^>]*)?>([^<]*)</w:t>", par)
    joined = "".join(ts)
    if not joined.strip():
        return par
    if ts[:4] == ["Năm học. kỳ học", "TÊN NGÀNH", "TÊN SV", "MÃ SV"]:  # gáy sách
        return set_texts(par, [value("nam_hoc_ky_hoc"), value("nganh", True), value("ten_sinh_vien", True), value("ma_sinh_vien")])
    if joined == "Tên đề tài":  # tên đề tài thật dài hơn chữ mẫu: 18pt thay 25pt để bìa vẫn vừa một trang
        par = re.sub(r'<w:sz(Cs)? w:val="50"/>', lambda m: f'<w:sz{m.group(1) or ""} w:val="36"/>', par)
        return set_texts(par, [value("ten_de_tai")])
    if joined.startswith("Hà Nội, "):
        return set_texts(par, [value("noi_thang")])
    for label, key in LABELS.items():
        if joined.replace(" :", ":").startswith(label + ":"):
            n = len(re.findall(r"<w:t(?: [^>]*)?>", par))
            out = set_texts(par, [label, ": ", value(key)] if n >= 3 else [label, ": " + value(key)])
            if label == "Lớp":  # căn dấu hai chấm thẳng các dòng khác như người dùng đã chỉnh tay ở bản v38
                out = out.replace('<w:t xml:space="preserve">Lớp</w:t>', '<w:t xml:space="preserve">Lớp</w:t><w:tab/><w:tab/><w:tab/><w:tab/>', 1)
            return out
    if joined == "TRƯỜNG CÔNG NGHỆ":
        return set_texts(par, [value("truong")])
    return par


cover = re.sub(r"<w:p[ >](?:(?!</w:p>).)*</w:p>", lambda m: fill(m.group(0)), cover, flags=re.S)
cover = cover.replace('<w:sz w:val="138"/>', '<w:sz w:val="40"/>')  # dòng trống rất cao trên bìa ngoài


def tighten(m):
    """Bìa trong: bỏ khoảng cách trước các dòng trống nhỏ để tên đề tài ba dòng vẫn vừa một trang."""
    p = m.group(0)
    if re.search(r"<w:t[ >]", p) or "<w:sectPr" in p or "<w:drawing" in p or "<w:pict" in p:
        return p
    if '<w:sz w:val="12"/>' in p:
        return ""
    return re.sub(r'<w:sz(Cs)? w:val="(?:50|46)"/>', lambda m: f'<w:sz{m.group(1) or ""} w:val="16"/>', p)


cut = cover.index("</w:sectPr>") + len("</w:sectPr>")
cover = cover[:cut] + re.sub(r"<w:p[ >](?:(?!</w:p>).)*</w:p>", tighten, cover[cut:], flags=re.S)
left = re.findall(r"Nguyễn Văn A|Tên đề tài|111\.\.\.\.\.|5/2025", "".join(re.findall(r"<w:t(?: [^>]*)?>([^<]*)</w:t>", cover)))
assert not left, left

# ---- 2. ghép vào tài liệu
src = zipfile.ZipFile(body_path)
doc = src.read("word/document.xml").decode("utf-8")
root = re.search(r"<w:document[^>]*>", doc).group(0)
troot = re.search(r"<w:document[^>]*>", txml).group(0)
ns_have = dict(re.findall(r'xmlns:(\w+)="([^"]+)"', root))
add_ns = "".join(f' xmlns:{k}="{v}"' for k, v in re.findall(r'xmlns:(\w+)="([^"]+)"', troot) if k not in ns_have)
ign = set((re.search(r'mc:Ignorable="([^"]*)"', root) or re.search("()", "")).group(1).split())
ign |= set(re.search(r'mc:Ignorable="([^"]*)"', troot).group(1).split())
new_root = re.sub(r'\s*mc:Ignorable="[^"]*"', "", root)[:-1] + add_ns + f' mc:Ignorable="{" ".join(sorted(ign))}">'
doc = doc.replace(root, new_root, 1)
doc = doc.replace("<w:body>", "<w:body>" + cover, 1)

# Khoảng trắng không ngắt giữa "Chương/Bảng/Hình/mục/..." và con số theo sau, để Word không
# đẩy riêng con số xuống dòng dưới (ví dụ "Chương" cuối dòng, "4." đầu dòng sau).
NBSP_RE = re.compile(r"\b(Chương|Bảng|Hình|[Mm]ục|[Tt]iểu mục|Phụ lục|công thức|Công thức|Mã giả|Ví dụ|các mục) (?=[0-9(]|[A-J]\b|[A-J]\.\d)")
doc = re.sub(r"(<w:t(?: [^>]*)?>)([^<]*)(</w:t>)", lambda m: m.group(1) + NBSP_RE.sub("\\1\u00a0", m.group(2)) + m.group(3), doc)

rels = src.read("word/_rels/document.xml.rels").decode("utf-8")
rels = rels.replace("</Relationships>", '<Relationship Id="rIdCoverImg1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/cover_image1.jpeg"/></Relationships>')
ct = src.read("[Content_Types].xml").decode("utf-8")
if 'Extension="jpeg"' not in ct:
    ct = ct.replace("<Default ", '<Default Extension="jpeg" ContentType="image/jpeg"/><Default ', 1)
settings = re.sub(r"<w:updateFields[^>]*/>", "", src.read("word/settings.xml").decode("utf-8"))

from xml.dom import minidom  # noqa: E402
minidom.parseString(doc.encode("utf-8"))  # XML hỏng thì dừng ở đây, không để Word báo lỗi mở tệp

with zipfile.ZipFile(out_path, "w", zipfile.ZIP_DEFLATED) as z:
    for item in src.infolist():
        if item.filename.endswith("/"):
            continue
        data = src.read(item.filename)
        if item.filename == "word/document.xml":
            data = doc.encode("utf-8")
        elif item.filename == "word/_rels/document.xml.rels":
            data = rels.encode("utf-8")
        elif item.filename == "[Content_Types].xml":
            data = ct.encode("utf-8")
        elif item.filename == "word/settings.xml":
            data = settings.encode("utf-8")
        z.writestr(item.filename, data)
    z.writestr("word/media/cover_image1.jpeg", tpl.read("word/media/image1.jpeg"))
print("written", out_path)

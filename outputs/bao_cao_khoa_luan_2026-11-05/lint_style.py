"""Kiểm tra văn phong báo cáo theo góp ý của GVHD, chạy trên tệp .docx đã dựng.

    python -X utf8 lint_style.py BAO_CAO.docx [--chapter 4]

Đếm trong thân bài (không tính bảng, mã giả, tài liệu tham khảo): dấu chấm phẩy,
gạch ngang dài, mũi tên, ngoặc đơn, đường dẫn tệp; kiểm tra tên bảng/hình có ngoặc
hoặc "nguồn:", và bảng/hình nào chưa được nhắc trong đoạn văn đứng trước nó.
"""
import re
import sys
import zipfile
from xml.etree import ElementTree as ET

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"


def paragraphs(path):
    body = ET.fromstring(zipfile.ZipFile(path).read("word/document.xml")).find(W + "body")
    for el in body:
        if el.tag == W + "p":
            st = el.find(f"{W}pPr/{W}pStyle")
            style = st.get(W + "val") if st is not None else ""
            runs = list(el.iter(W + "r"))
            mono = any(r.find(f"{W}rPr/{W}rFonts") is not None and "Consolas" in (r.find(f"{W}rPr/{W}rFonts").get(W + "ascii") or "") for r in runs)
            text = "".join(t.text or "" for t in el.iter(W + "t"))
            jc = el.find(f"{W}pPr/{W}jc")
            formula = jc is not None and jc.get(W + "val") == "center" and "=" in text and not style
            algo = bool(re.match(r"^(\d+:|Input:|Output:)", text))  # dòng mã giả
            numbered_eq = "=" in text and bool(re.search(r"\(\d+\.\d+\)$", text.strip()))  # công thức đánh số
            numbered_eq = numbered_eq or bool(re.fullmatch(r"\(\d+\)", text.strip()))  # công thức Word, chỉ còn số thứ tự
            yield style, text, mono or formula or algo or numbered_eq  # công thức căn giữa được bỏ qua như mã giả
        elif el.tag == W + "tbl":
            yield "TABLE", "", False


def main():
    path = sys.argv[1]
    chap = sys.argv[sys.argv.index("--chapter") + 1] if "--chapter" in sys.argv else None
    cur, rows = None, []
    for style, text, mono in paragraphs(path):
        if style == "Heading1":
            m = re.match(r"CHƯƠNG (\d+)", text)
            cur = m.group(1) if m else text
        if chap and cur != chap:
            continue
        rows.append((style, text, mono))
    body = [t for s, t, mono in rows if s in ("", "ListParagraph") and t.strip() and not mono]
    txt = "\n".join(body)
    checks = {"dấu chấm phẩy ;": txt.count(";"), "gạch ngang dài —": txt.count("—"), "gạch nối – giữa chữ": len(re.findall(r"[^\d\s]\s?–\s?[^\d\s]", txt)),
              "mũi tên →": txt.count("→"), "ngoặc đơn (": txt.count("("),
              "đường dẫn tệp": len(re.findall(r"[\w/.-]+\.(?:py|json|jsonl|md|xlsx|joblib|csv|log|html)\b", txt))}
    print(f"Phạm vi: {'Chương ' + chap if chap else 'toàn bộ'}; {len(body)} đoạn, {len(txt.split())} từ")
    for k, v in checks.items():
        print(f"  {k:<22} {v}")
    caps = [(s, t) for s, t, _ in rows if s in ("BangCaption", "HinhCaption")]
    bad = [t for _, t in caps if "(" in t or "nguồn:" in t.lower()]
    print(f"  tên bảng/hình có ngoặc hoặc 'nguồn': {len(bad)}/{len(caps)}")
    for t in bad:
        print("    -", t[:110])
    # bảng/hình phải được nhắc trong đoạn văn trước nó
    seen = ""
    missing = []
    for s, t, _ in rows:
        if s in ("BangCaption", "HinhCaption"):
            m = re.match(r"((?:Bảng|Hình) [\dA-Z]+\.\d+)", t)
            if m and m.group(1) not in seen:
                missing.append(m.group(1))
        elif s in ("", "ListParagraph"):
            seen += " " + t
    print(f"  bảng/hình chưa được dẫn trước: {len(missing)} {missing}")
    for t in body:
        if len(t.split()) > 180:
            print(f"  đoạn dài {len(t.split())} từ: {t[:80]}...")


if __name__ == "__main__":
    main()

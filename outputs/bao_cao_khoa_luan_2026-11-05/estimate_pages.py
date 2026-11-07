"""Ước lượng số trang A4 của docx (không có Word/LibreOffice). Sai số dự kiến ±15%."""
import math
import re
import sys
import zipfile

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
import xml.etree.ElementTree as ET

PAGE_H = 728.0          # pt khả dụng (A4, lề trên/dưới 2 cm)
TEXT_W = 453.5          # pt (lề trái 3 cm, phải 2 cm)
CHAR_W = 0.47           # bề rộng ký tự trung bình theo em (Times New Roman, tiếng Việt)


def para_info(p):
    text = "".join(t.text or "" for t in p.iter(W + "t"))
    sz = None
    for s in p.iter(W + "sz"):
        sz = int(s.get(W + "val")) / 2
        break
    style = p.find(f"{W}pPr/{W}pStyle")
    style = style.get(W + "val") if style is not None else ""
    pb = p.find(f"{W}pPr/{W}pageBreakBefore") is not None or any(b.get(W + "type") == "page" for b in p.iter(W + "br"))
    img = any(True for _ in p.iter("{http://schemas.openxmlformats.org/drawingml/2006/main}blip"))
    return text, sz or 13, style, pb, img


def lines(text, size, width_pt):
    cpl = max(8, int(width_pt / (size * CHAR_W)))
    return max(1, math.ceil(len(text) / cpl))


def main(path):
    root = ET.fromstring(zipfile.ZipFile(path).read("word/document.xml"))
    body = root.find(W + "body")
    pages, y = 1, 0.0
    per_h1 = []

    def push(h):
        nonlocal pages, y
        while y + h > PAGE_H:
            take = PAGE_H - y
            h -= take
            pages += 1
            y = 0.0
        y += h

    for el in body:
        if el.tag == W + "p":
            text, size, style, pb, img = para_info(el)
            if pb and y > 0:
                pages += 1
                y = 0.0
            if style == "Heading1":
                per_h1.append((pages, text))
            if img:
                push(300)
                continue
            if style.startswith("Heading"):
                size = {"Heading1": 16, "Heading2": 14}.get(style, 13)
            lh = size * 1.3 * 1.15
            push(lines(text, size, TEXT_W - (40 if "numPr" in ET.tostring(el, encoding="unicode") else 0)) * lh + 8)
        elif el.tag == W + "tbl":
            grid = [int(g.get(W + "w")) / 20 for g in el.iter(W + "gridCol")]
            for tr in el.iter(W + "tr"):
                h = 0
                for i, tc in enumerate(tr.findall(W + "tc")):
                    t = "".join(x.text or "" for x in tc.iter(W + "t"))
                    sz = 11
                    for s in tc.iter(W + "sz"):
                        sz = int(s.get(W + "val")) / 2
                        break
                    w = (grid[i] if i < len(grid) else 80) - 9
                    h = max(h, lines(t, sz, w) * sz * 1.25 + 5)
                push(h)
            push(6)
    print(f"Ước lượng: {pages} trang")
    for p, t in per_h1:
        print(f"  tr.{p:>3}  {t}")


if __name__ == "__main__":
    main(sys.argv[1])

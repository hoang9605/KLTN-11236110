from pathlib import Path
import re
import html
import json
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[3]
SOURCE = ROOT / 'docs' / 'BAO_CAO_RE_2026-10-02.md'
OUT = Path(__file__).resolve().parents[1]
OUT.mkdir(parents=True, exist_ok=True)
PDF = OUT / 'BAO_CAO_RE_2026-10-02.pdf'
FONT_ROOT = Path('C:/Windows/Fonts')
for name, filename in [('Arial', 'arial.ttf'), ('Arial-Bold', 'arialbd.ttf'), ('Arial-Italic', 'ariali.ttf'), ('Arial-BoldItalic', 'arialbi.ttf')]:
    pdfmetrics.registerFont(TTFont(name, str(FONT_ROOT / filename)))
pdfmetrics.registerFontFamily('Arial', normal='Arial', bold='Arial-Bold', italic='Arial-Italic', boldItalic='Arial-BoldItalic')

styles = {
    'title': ParagraphStyle('title', fontName='Arial-Bold', fontSize=20, leading=26, textColor=colors.black, spaceAfter=9),
    'meta': ParagraphStyle('meta', fontName='Arial', fontSize=9, leading=13, textColor=colors.HexColor('#555555'), spaceAfter=13),
    'h2': ParagraphStyle('h2', fontName='Arial-Bold', fontSize=15, leading=20, textColor=colors.black, spaceAfter=10, keepWithNext=True),
    'h3': ParagraphStyle('h3', fontName='Arial-Bold', fontSize=11.5, leading=16, textColor=colors.black, spaceBefore=8, spaceAfter=6, keepWithNext=True),
    'body': ParagraphStyle('body', fontName='Arial', fontSize=10.35, leading=14.7, alignment=TA_LEFT, spaceAfter=7),
    'bullet': ParagraphStyle('bullet', fontName='Arial', fontSize=10.15, leading=14.4, leftIndent=11, firstLineIndent=-10, spaceAfter=6),
    'table': ParagraphStyle('table', fontName='Arial', fontSize=9, leading=12.4, spaceAfter=0),
    'tablehead': ParagraphStyle('tablehead', fontName='Arial-Bold', fontSize=9, leading=12.4, spaceAfter=0),
    'center': ParagraphStyle('center', fontName='Arial', fontSize=9, leading=12.4, spaceAfter=0, alignment=TA_CENTER),
    'code': ParagraphStyle('code', fontName='Arial', fontSize=9.2, leading=13, leftIndent=8, rightIndent=8, spaceAfter=0),
}

def inline(raw):
    s = html.escape(raw)
    s = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', lambda m: '<link href="' + m.group(2) + '" color="#164B72">' + m.group(1) + '</link>', s)
    s = re.sub(r'\*\*([^*]+)\*\*', r'<b>\1</b>', s)
    s = re.sub(r'`([^`]+)`', r'<font name="Arial">\1</font>', s)
    return s

W = A4[0] - 92

def table(rows):
    n = len(rows[0])
    if n == 2:
        weights = [0.67, 0.33] if 'Ngân sách' in rows[0][1] else [0.29, 0.71]
        if rows[0][0] == 'Hạng mục' and rows[0][1] == 'Đề xuất': weights = [0.31, 0.69]
    elif n == 3:
        weights = [0.24, 0.31, 0.45]
        if 'Điểm công bố' in rows[0]: weights = [0.40, 0.20, 0.40]
    elif n == 4:
        weights = [0.14, 0.18, 0.28, 0.40]
        if rows[0][0] == 'Hệ thống': weights = [0.25, 0.39, 0.17, 0.19]
    else:
        weights = [1 / n] * n
    widths = [W * weight for weight in weights]
    data = []
    for i, row in enumerate(rows):
        data.append([Paragraph(inline(c), styles['tablehead' if i == 0 else ('center' if (n == 2 and 'Ngân sách' in rows[0][1] and j == 1) or (n == 4 and rows[0][0] == 'Hệ thống' and j > 1) else 'table')]) for j, c in enumerate(row)])
    t = Table(data, colWidths=widths, repeatRows=1, hAlign='LEFT')
    rules = [('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#DFEAF2')),
             ('GRID', (0, 0), (-1, -1), 0.45, colors.HexColor('#D9D9D9')),
             ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
             ('LEFTPADDING', (0, 0), (-1, -1), 7), ('RIGHTPADDING', (0, 0), (-1, -1), 7),
             ('TOPPADDING', (0, 0), (-1, -1), 6), ('BOTTOMPADDING', (0, 0), (-1, -1), 6)]
    for i in range(2, len(rows), 2):
        rules.append(('BACKGROUND', (0, i), (-1, i), colors.HexColor('#F6F8FA')))
    if n == 2 and 'Ngân sách' in rows[0][1]:
        rules.extend([('TOPPADDING', (0, 0), (-1, -1), 3.5), ('BOTTOMPADDING', (0, 0), (-1, -1), 3.5)])
    if n == 2 and rows[-1][0] == 'Tổng':
        rules.append(('BACKGROUND', (0, len(rows)-1), (-1, len(rows)-1), colors.HexColor('#EAF0F5')))
    t.setStyle(TableStyle(rules))
    return t

text = SOURCE.read_text(encoding='utf-8')
chunks = text.split('<!-- PAGE -->')
story = []
for page_index, chunk in enumerate(chunks):
    if page_index: story.append(PageBreak())
    lines = chunk.strip().splitlines()
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if not line:
            i += 1
            continue
        if line.startswith('```'):
            code = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith('```'):
                code.append(Paragraph(html.escape(lines[i]).replace(' ', '&nbsp;'), styles['code']))
                i += 1
            story.append(KeepTogether([Spacer(1, 3), *code, Spacer(1, 9)]))
            i += 1
            continue
        if line.startswith('|'):
            rows = []
            while i < len(lines) and lines[i].strip().startswith('|'):
                cells = [x.strip() for x in lines[i].strip().strip('|').split('|')]
                if not all(re.fullmatch(r':?-+:?', c) for c in cells): rows.append(cells)
                i += 1
            story.extend([table(rows), Spacer(1, 9)])
            continue
        if line.startswith('# '):
            story.append(Paragraph(inline(line[2:]), styles['title']))
        elif line.startswith('## '):
            story.append(Paragraph(inline(line[3:]), styles['h2']))
        elif line.startswith('### '):
            story.append(Paragraph(inline(line[4:]), styles['h3']))
        elif line.startswith('- '):
            story.append(Paragraph('• ' + inline(line[2:]), styles['bullet']))
        elif re.match(r'^\d+\. ', line):
            story.append(Paragraph(inline(line), styles['bullet']))
        elif page_index == 0 and line.startswith('Khóa luận'):
            story.append(Paragraph(inline(line), styles['meta']))
        else:
            paragraph = [line]
            while i + 1 < len(lines) and lines[i+1].strip() and not lines[i+1].strip().startswith(('#', '|', '-', '```')) and not re.match(r'^\d+\. ', lines[i+1].strip()):
                i += 1
                paragraph.append(lines[i].strip())
            story.append(Paragraph(inline(' '.join(paragraph)), styles['body']))
        i += 1

def page_frame(c, doc):
    c.saveState()
    c.setFont('Arial', 8)
    c.setFillColor(colors.HexColor('#555555'))
    if doc.page > 1:
        c.drawString(46, A4[1] - 33, 'KẾ HOẠCH VÀ KỸ THUẬT RELATION EXTRACTION')
        c.drawRightString(A4[0]-46, A4[1]-33, '02/10/2026')
    c.drawString(46, 29, 'AI KLTN  |  Hiện trạng và đề xuất  |  Chưa có kết quả RE')
    c.drawRightString(A4[0]-46, 29, str(doc.page))
    c.restoreState()

doc = SimpleDocTemplate(str(PDF), pagesize=A4, leftMargin=46, rightMargin=46, topMargin=49, bottomMargin=47, title='Báo cáo kế hoạch và kỹ thuật RE', author='Sinh viên thực hiện khóa luận', pageCompression=1)
doc.build(story, onFirstPage=page_frame, onLaterPages=page_frame)
reader = PdfReader(PDF)
qa = {'file': str(PDF), 'planned_pages': len(chunks), 'actual_pages': len(reader.pages), 'page_characters': [len(p.extract_text() or '') for p in reader.pages], 'hyperlinks': sum(len(p.get('/Annots', [])) for p in reader.pages)}
(OUT / '.build' / 'text_qa.json').write_text(json.dumps(qa, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps(qa, ensure_ascii=False))

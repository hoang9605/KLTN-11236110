"""Build six physician review documents from the existing 600 mapped records."""
import json
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.oxml.ns import qn

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT/'outputs/vietmed_600_ner_6_loai/vietmed_600_ner_6_loai.jsonl'
OUT = ROOT/'outputs/vietmed_600_bac_si_6_file'
OUT.mkdir(parents=True, exist_ok=True)
rows = [json.loads(x) for x in SOURCE.read_text(encoding='utf-8').splitlines()]
names = {'CONDITION':'bệnh hoặc triệu chứng', 'DRUG':'thuốc hoặc chất', 'BODY_PART':'bộ phận cơ thể', 'TEST':'xét nghiệm hoặc thăm khám', 'PROCEDURE':'thủ thuật hoặc điều trị', 'DOSAGE':'liều lượng'}

def spans(row):
    result=[]
    pos=0
    active=None
    for word, label in zip(row['words'], row['labels']):
        start=row['text'].find(word,pos)
        assert start>=0, row['id']
        end=start+len(word)
        pos=end
        if label=='O':
            active=None
            continue
        prefix, kind=label.split('-',1)
        if prefix=='I' and active is not None and active['label']==kind:
            active['end']=end
        else:
            assert prefix=='B', (row['id'], label, 'Invalid BIO boundary')
            active={'start':start,'end':end,'label':kind}
            result.append(active)
    return result

files=[]
seen=[]
for batch in range(6):
    selected=rows[batch*100:(batch+1)*100]
    assert len(selected)==100
    d=Document()
    section=d.sections[0]
    section.page_width,section.page_height=Inches(8.5),Inches(11)
    section.top_margin=section.bottom_margin=Inches(.65)
    section.left_margin=section.right_margin=Inches(.75)
    for name in ['Normal','Title','Heading 1','Heading 2']:
        style=d.styles[name]
        style.font.name='Arial'
        style.font.color.rgb=RGBColor(0,0,0)
        for border in list(style.element.iter(qn('w:pBdr'))):
            border.getparent().remove(border)
    d.styles['Normal'].font.size=Pt(11)
    d.styles['Normal'].paragraph_format.space_after=Pt(5)
    d.styles['Heading 1'].font.size=Pt(14)
    d.add_paragraph(f'Phiếu kiểm tra NER và RE tập {batch+1}', 'Title')
    d.add_paragraph(f'100 mẫu từ {selected[0]["id"]} đến {selected[-1]["id"]}. Nguồn VietMed-NER train; nhãn NER đã ánh xạ theo 6 loại của dự án.')
    d.add_paragraph('Cách kiểm tra').runs[0].bold=True
    d.add_paragraph('NER: đúng giữ nguyên; sai bôi đỏ và ghi cách sửa; thiếu thực thể thì bổ sung. Kiểm tra cả ranh giới cụm từ và loại thực thể. Các mã E1, E2… chỉ dùng trong từng mẫu.')
    d.add_paragraph('RE: dữ liệu nguồn chưa có nhãn quan hệ. Sau khi sửa NER, xin ghi các quan hệ được đoạn văn thể hiện theo mẫu E1 — tên quan hệ — E2. Không suy diễn từ kiến thức y khoa. Không có quan hệ thì ghi “Không có”; thiếu ngữ cảnh thì ghi “Chưa rõ”. Để trống nghĩa là chưa gán nhãn.')
    d.add_paragraph('Sáu loại thực thể').runs[0].bold=True
    for code, name in names.items():
        d.add_paragraph(f'{code}: {name}.')
    d.add_paragraph('Năm loại quan hệ').runs[0].bold=True
    for line in [
        'located_at: bệnh/triệu chứng → bộ phận cơ thể, có vị trí ở.',
        'treated_by: bệnh/triệu chứng → thuốc, được điều trị bằng.',
        'treated_by_procedure: bệnh/triệu chứng → thủ thuật/điều trị, được điều trị bằng phương pháp.',
        'diagnosed_by: bệnh/triệu chứng → xét nghiệm/thăm khám, được chẩn đoán bằng.',
        'has_dosage: thuốc → liều lượng, có liều lượng.',
    ]: d.add_paragraph(line)
    d.add_paragraph('Chỉ ghi quan hệ khẳng định trong đoạn. Nếu quan hệ bị phủ định hoặc chỉ là giả định, ghi rõ trong phần RE để người xử lý phân biệt.')
    d.add_paragraph('Bác sĩ kiểm tra: __________________  Ngày: __________')
    d.add_paragraph('Đã kiểm tra đến mẫu: __________________')
    d.add_page_break()
    for row in selected:
        seen.append(row['id'])
        entities=spans(row)
        heading=d.add_paragraph(f'Mẫu {row["id"]}', 'Heading 1')
        p=d.add_paragraph()
        pos=0
        for e in entities:
            p.add_run(row['text'][pos:e['start']])
            p.add_run(row['text'][e['start']:e['end']]).bold=True
            pos=e['end']
        p.add_run(row['text'][pos:])
        assert p.text==row['text']
        d.add_paragraph('NER').runs[0].bold=True
        for i,e in enumerate(entities,1):
            d.add_paragraph(f'E{i}. “{row["text"][e["start"]:e["end"]]}” — {e["label"]}')
        if not entities:
            d.add_paragraph('Chưa có thực thể thuộc 6 loại được đánh dấu. Xin bổ sung nếu bị bỏ sót.')
        d.add_paragraph('RE sau khi kiểm tra NER').runs[0].bold=True
        d.add_paragraph('................................................................................................')
        d.add_paragraph('................................................................................................')
        p=d.add_paragraph(f'Nguồn: train, dòng {row["source_row_index"]} (đếm từ 0).')
        p.runs[0].font.size=Pt(9)
        d.add_paragraph('')
    path=OUT/f'Phieu_{batch+1:02d}_mau_{batch*100+1:03d}_{(batch+1)*100:03d}.docx'
    d.save(path)
    check=Document(path)
    assert sum(p.text.startswith('Mẫu VM600-') for p in check.paragraphs)==100
    for row in selected:
        assert row['text'] in [p.text for p in check.paragraphs]
    files.append(path)
assert len(seen)==len(set(seen))==600
assert seen==[r['id'] for r in rows]
with ZipFile(OUT/'6_phieu_NER_RE_600_mau.zip','w',ZIP_DEFLATED) as z:
    for f in files: z.write(f,f.name)
print('PASS: six DOCX files, 100 samples each, all 600 IDs covered exactly once; source texts preserved; BIO boundaries valid.')
for f in files: print(f.name)

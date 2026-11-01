"""Create Vietnamese physician-facing copies, preserving machine annotations."""
import json
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
from docx import Document

root=Path(__file__).resolve().parents[1]
source=root/'outputs/vietmed_600_RE_review'
out=source/'tieng_viet_thuoc_duoc_chat'
out.mkdir(exist_ok=True)
entities={'CONDITION':'Bệnh hoặc triệu chứng','DRUG':'Thuốc/dược chất','BODY_PART':'Bộ phận cơ thể','TEST':'Xét nghiệm hoặc thăm khám','PROCEDURE':'Thủ thuật hoặc điều trị','DOSAGE':'Liều lượng'}
relations={'located_at':'Có vị trí ở','treated_by':'Được điều trị bằng thuốc','treated_by_procedure':'Được điều trị bằng phương pháp','diagnosed_by':'Được chẩn đoán bằng','has_dosage':'Có liều lượng','NO_RELATION':'Không có quan hệ thuộc 5 loại','CHUA_RO':'Chưa rõ — cần xác nhận'}
replacements={**entities,**relations,'CHUA_XAC_NHAN':'Chưa xác nhận','DA_DUYET_DEN':'Đã duyệt đến','BAC_SI':'Bác sĩ','NGAY_DUYET':'Ngày duyệt'}
files=[]
for file in sorted(source.glob('Phieu_RE_*.docx')):
    d=Document(file)
    for p in d.paragraphs:
        if p.text.startswith('NER: CONDITION'):
            p.text='Sáu loại thực thể: '+ '; '.join(entities.values())+'.'
        elif any(p.text.startswith(k+':') for k in relations):
            label=p.text.split(':',1)[0]
            p.text=relations[label]+'.'
        else:
            for run in p.runs:
                for key,val in sorted(replacements.items(),key=lambda item:-len(item[0])):
                    run.text=run.text.replace(key,val)
    for table in d.tables:
        for row in table.rows[1:]:
            cell=row.cells[-1]
            raw=cell.text
            assert raw in entities or raw in relations,raw
            for run in cell.paragraphs[0].runs:
                run.text=(entities|relations)[raw]
    path=out/file.name.replace('Phieu_RE_','Phieu_tieng_Viet_')
    d.save(path)
    check=Document(path)
    assert sum(p.text.startswith('Mẫu VM600-') for p in check.paragraphs)==100
    assert all(row.cells[-1].text in set(entities.values())|set(relations.values()) for t in check.tables for row in t.rows[1:])
    files.append(path)
assert len(files)==6
(out/'anh_xa_nhan.json').write_text(json.dumps(dict(entities=entities,relations=relations),ensure_ascii=False,indent=2),encoding='utf-8')
with ZipFile(out/'6_phieu_nhan_tieng_Viet.zip','w',ZIP_DEFLATED) as z:
    for f in files:z.write(f,f.name)
print('PASS: six Vietnamese documents, 100 samples each; every entity and relation table label translated.')

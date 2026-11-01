import json
from collections import Counter
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'outputs/vietmed_600_RE_review'
rows=json.loads((OUT/'prepared.json').read_text(encoding='utf-8'))
dec=json.loads((OUT/'decisions.json').read_text(encoding='utf-8'))
names={'located_at':'có vị trí ở','treated_by':'được điều trị bằng thuốc','treated_by_procedure':'được điều trị bằng phương pháp','diagnosed_by':'được chẩn đoán bằng','has_dosage':'có liều lượng','NO_RELATION':'Không có quan hệ thuộc 5 loại','CHUA_RO':'Chưa rõ — bác sĩ xác nhận'}
counts=Counter()
for n,r in enumerate(rows,1):
    pos=dec['positive'].get(str(n),[])
    unc=dec['uncertain'].get(str(n),[])
    valid={int(p['id'][1:]) for p in r['pairs']}
    assert set(pos)<=valid
    if unc=='all':unc=list(valid)
    assert set(unc)<=valid and not set(pos)&set(unc),n
    r['relations']=[]
    for p in r['pairs']:
        num=int(p['id'][1:])
        label=p['allowed_relation'] if num in pos else 'CHUA_RO' if num in unc else 'NO_RELATION'
        h=next(e for e in r['entities'] if e['id']==p['head'])
        t=next(e for e in r['entities'] if e['id']==p['tail'])
        a=min(h['start'],t['start']);b=max(h['end'],t['end'])
        r['relations'].append(dict(**p,label=label,review_status='unreviewed',
            evidence={'start':a,'end':b,'text':r['text'][a:b]},
            rationale=dec['notes'].get(str(n), 'Đoạn thể hiện liên kết giữa hai thực thể.' if num in pos else 'Cần xác nhận ngữ cảnh hoặc nhãn thực thể trước khi chốt.' if num in unc else 'Không có khẳng định quan hệ thuộc 5 loại giữa hai lần nhắc này trong đoạn.')))
        counts[label]+=1
    r.update(annotation_status='AI_DRAFT_UNREVIEWED',reviewer=None,reviewed_at=None,
             review_note=dec['notes'].get(str(n),''),
             re_scope='Five relation types between existing mapped mentions in this original utterance only')
    del r['pairs']
(OUT/'annotations_draft.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in rows),encoding='utf-8')

def para(d,text,bold=False):
    p=d.add_paragraph();p.add_run(text).bold=bold;return p

def table(d,headers,content,widths):
    t=d.add_table(rows=1,cols=len(headers));t.autofit=False
    for c,w,h in zip(t.rows[0].cells,widths,headers):
        c.width=Inches(w);c.text=h
        c.paragraphs[0].runs[0].bold=True
        shading=OxmlElement('w:shd');shading.set(qn('w:fill'),'E8EEF3');c._tc.get_or_add_tcPr().append(shading)
    rep=OxmlElement('w:tblHeader');t.rows[0]._tr.get_or_add_trPr().append(rep)
    for values in content:
        cells=t.add_row().cells
        for c,w,value in zip(cells,widths,values):c.width=Inches(w);c.text=value
    for row in t.rows:
        prop=row._tr.get_or_add_trPr();prop.append(OxmlElement('w:cantSplit'))
        for c in row.cells:
            borders=OxmlElement('w:tcBorders')
            for side in ['top','left','bottom','right']:
                edge=OxmlElement('w:'+side)
                for key,val in [('val','single'),('sz','4'),('color','D9D9D9')]:edge.set(qn('w:'+key),val)
                borders.append(edge)
            c._tc.get_or_add_tcPr().append(borders)
            for p in c.paragraphs:
                p.paragraph_format.space_after=Pt(4);p.paragraph_format.space_before=Pt(4)
    return t

files=[]
for batch in range(6):
    subset=rows[batch*100:(batch+1)*100]
    d=Document();s=d.sections[0]
    s.page_width=Inches(8.5);s.page_height=Inches(11)
    s.left_margin=s.right_margin=Inches(.7);s.top_margin=s.bottom_margin=Inches(.65)
    for k in ['Normal','Title','Heading 1','Heading 2']:
        st=d.styles[k];st.font.name='Arial';st.font.color.rgb=RGBColor(0,0,0)
        for el in list(st.element.iter(qn('w:pBdr'))):el.getparent().remove(el)
    d.styles['Normal'].font.size=Pt(11)
    d.styles['Normal'].paragraph_format.space_after=Pt(6)
    d.styles['Heading 1'].font.size=Pt(14)
    d.add_paragraph(f'Kiểm tra NER và RE tập {batch+1}', 'Title')
    para(d,f'100 mẫu {subset[0]["id"]} đến {subset[-1]["id"]}. Bản gán nhãn trước để bác sĩ kiểm tra.')
    para(d,'Đúng giữ nguyên — sai bôi đỏ và ghi cách sửa.',True)
    para(d,'Bôi đỏ chữ hoặc tô nền đỏ tại dòng sai. Có thể sửa trực tiếp ô Cụm từ hoặc Nhãn và giữ phần sửa màu đỏ. Nếu cần bỏ, ghi XÓA; nếu thiếu, thêm thực thể E… hoặc quan hệ R… ở dòng BỔ SUNG. Giữ nguyên mã mẫu, mã E/R và đoạn gốc.')
    para(d,'NER giữ nhãn nguồn đã ánh xạ sang 6 loại. RE là bản AI gán trước, chưa được bác sĩ duyệt. CHUA_RO là trạng thái chưa đủ căn cứ, không phải nhãn huấn luyện. Nếu chốt được, sửa thành một trong 5 nhãn hoặc NO_RELATION.')
    para(d,'Khi kết thúc, thay CHUA_XAC_NHAN bên dưới bằng mã mẫu cuối cùng đã đọc theo thứ tự. Chỉ các mẫu đã đọc mới được tính là đã duyệt; phần sai màu đỏ sẽ được đối chiếu trước khi xuất dữ liệu.')
    para(d,'DA_DUYET_DEN: CHUA_XAC_NHAN',True)
    para(d,'BAC_SI: __________________    NGAY_DUYET: __________________')
    para(d,'NER: CONDITION = bệnh/triệu chứng; DRUG = thuốc/chất; BODY_PART = bộ phận cơ thể; TEST = xét nghiệm/thăm khám; PROCEDURE = thủ thuật/điều trị; DOSAGE = liều lượng.')
    for label,meaning in names.items():para(d,f'{label}: {meaning}.')
    para(d,'Chỉ xét quan hệ trong đoạn gốc. Quan hệ phòng ngừa, gây bệnh hoặc tác dụng phụ không được đổi thành điều trị. Câu hỏi, phủ định và thiếu ngữ cảnh cần xét riêng. Không suy quan hệ chỉ vì hai thực thể xuất hiện cùng nhau.')
    para(d,'Nguồn: leduckhai/VietMed-NER, tập train. NER và RE đều cần bác sĩ kiểm tra. Mỗi mã E chỉ một lần nhắc cụ thể; mã này được giữ trong dữ liệu JSONL.')
    d.add_page_break()
    for r in subset:
        d.add_paragraph('Mẫu '+r['id'],'Heading 1')
        p=d.add_paragraph();cursor=0
        for e in r['entities']:
            p.add_run(r['text'][cursor:e['start']]);p.add_run(e['text']).bold=True
            run=p.add_run(' ['+e['id']+']');run.font.size=Pt(9)
            cursor=e['end']
        p.add_run(r['text'][cursor:])
        para(d,'1  Thực thể NER',True)
        if r['entities']:
            table(d,['Mã','Cụm từ','Nhãn'],[[e['id'],e['text'],e['label']] for e in r['entities']],[.5,4.5,2.1])
        else:para(d,'E0 | Chưa có thực thể được đánh dấu thuộc 6 loại; xin kiểm tra bỏ sót.')
        para(d,'2  Quan hệ RE đã gán trước',True)
        if r['relations']:
            ed={e['id']:e for e in r['entities']}
            table(d,['Mã','Cặp thực thể có hướng','Nhãn đề xuất'],[
                [p['id'],f'{p["head"]} “{ed[p["head"]]["text"]}” → {p["tail"]} “{ed[p["tail"]]["text"]}”',p['label']]
                for p in r['relations']],[.5,3.9,2.7])
        else:para(d,'R0 | Không có cặp thực thể phù hợp 5 loại quan hệ trong NER hiện tại. Nếu bổ sung hoặc sửa NER, cần kiểm tra lại RE.')
        if r['review_note']:para(d,'Lý do cần chú ý: '+r['review_note'])
        para(d,'BỔ SUNG: Không')
        p=para(d,f'Nguồn train dòng {r["source_row_index"]} (đếm từ 0).')
        p.runs[0].font.size=Pt(9)
        para(d,'')
    path=OUT/f'Phieu_RE_{batch+1:02d}_{batch*100+1:03d}_{(batch+1)*100:03d}.docx'
    d.save(path);files.append(path)
    reread=Document(path)
    assert len([p for p in reread.paragraphs if p.text.startswith('Mẫu VM600-')])==100
    assert sum(len(t.rows)-1 for t in reread.tables)==sum(len(r['entities'])+len(r['relations']) for r in subset)
with ZipFile(OUT/'6_phieu_NER_RE_da_gan_nhan.zip','w',ZIP_DEFLATED) as z:
    for p in files:z.write(p,p.name)
(OUT/'stats.json').write_text(json.dumps(dict(samples=600,files=6,relations=dict(counts),samples_with_pairs=sum(bool(r['relations']) for r in rows)),ensure_ascii=False,indent=2),encoding='utf-8')
print('PASS: 6 files x 100 records, entity/relation table rows checked.')
print(dict(counts))

"""Extract review changes and export only explicitly reviewed, unchanged, resolved samples.

Edited/red samples are held for adjudication; they are never silently treated as negatives.
"""
import argparse
import copy
import json
import re
from pathlib import Path
from docx import Document
from docx.oxml.ns import qn

def text_of(el):
    return ''.join(t.text or '' for t in el.iter(qn('w:t')))

def is_red(el):
    for node in el.iter():
        if node.tag==qn('w:highlight') and node.get(qn('w:val')) in ('red','darkRed'):
            return True
        value=node.get(qn('w:val')) if node.tag==qn('w:color') else node.get(qn('w:fill')) if node.tag==qn('w:shd') else None
        if value and re.fullmatch('[0-9a-fA-F]{6}',value):
            r,g,b=[int(value[i:i+2],16) for i in (0,2,4)]
            if r>=120 and r>1.4*g and r>1.4*b:return True
    return False

def blocks(path):
    doc=Document(path);result={};current=None
    for el in doc.element.body:
        txt=text_of(el)
        if re.fullmatch(r'Mẫu VM600-\d{3}',txt):
            current=txt.split()[-1];assert current not in result,'Duplicate sample ID'
            result[current]=[]
        if current:result[current].append(el)
    return doc,result

def extract(original,reviewed,draft,out):
    base,original_blocks=blocks(original)
    doc,changed_blocks=blocks(reviewed)
    assert set(original_blocks)==set(changed_blocks),'Sample IDs missing or changed'
    markers=[p.text for p in doc.paragraphs if p.text.startswith(('DA_DUYET_DEN:', 'Đã duyệt đến:'))]
    assert len(markers)==1,'Review completion field missing or duplicated'
    value=markers[0].split(':',1)[1].strip()
    cutoff=None if value in ('CHUA_XAC_NHAN', 'Chưa xác nhận') else value
    assert cutoff is None or cutoff in original_blocks,'Review completion ID is outside this file'
    # Track changes/comments require adjudication; their meaning cannot be inferred from red alone.
    package=doc.part.package
    comments=any('comments' in str(part.partname) for part in package.parts)
    accepted=[];pending=[]
    for id,elems in changed_blocks.items():
        record=copy.deepcopy(draft[id]);old=original_blocks[id]
        old_text=[text_of(e) for e in old];new_text=[text_of(e) for e in elems]
        red=[text_of(e) for e in elems if is_red(e)]
        tracked=any(x.tag in (qn('w:ins'),qn('w:del')) for e in elems for x in e.iter())
        changed=old_text!=new_text
        reasons=[]
        if cutoff is None or id>cutoff:reasons.append('NOT_CONFIRMED_REVIEWED')
        if changed or red:reasons.append('EDITS_REQUIRE_ADJUDICATION')
        if tracked or comments:reasons.append('COMMENTS_OR_TRACKED_CHANGES_REQUIRE_ADJUDICATION')
        if any(r['label']=='CHUA_RO' for r in record['relations']):reasons.append('UNRESOLVED_RELATION')
        if reasons:
            pending.append(dict(id=id,reasons=reasons,red_blocks=red,original_blocks=old_text if changed else None,reviewed_blocks=new_text if changed else None))
        else:
            record['annotation_status']='PHYSICIAN_REVIEWED_UNCHANGED'
            record['review_document']=Path(reviewed).name
            for rel in record['relations']:rel['review_status']='physician_reviewed'
            record['relations']=[r for r in record['relations'] if r['label']!='NO_RELATION']
            record['negative_pairs']=[r for r in draft[id]['relations'] if r['label']=='NO_RELATION']
            accepted.append(record)
    out=Path(out);out.mkdir(parents=True,exist_ok=True)
    for name,data in [('reviewed_ready.jsonl',accepted),('pending_adjudication.jsonl',pending)]:
        (out/name).write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in data),encoding='utf-8')
    report=dict(confirmed_through=cutoff,ready=len(accepted),pending=len(pending),
                note='Ready records use original NER and prelabels confirmed unchanged. Edited samples require explicit reconciliation; empty/uncertain labels are not negative examples.')
    (out/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    return report

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--original',required=True);p.add_argument('--reviewed',required=True)
    p.add_argument('--draft',required=True);p.add_argument('--out',required=True)
    a=p.parse_args();draft={r['id']:r for r in map(json.loads,Path(a.draft).read_text(encoding='utf-8').splitlines())}
    print(json.dumps(extract(a.original,a.reviewed,draft,a.out)))

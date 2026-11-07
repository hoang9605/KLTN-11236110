import json, re, hashlib
from pathlib import Path
from docx import Document
from docx.oxml.ns import qn
from zipfile import ZipFile
root=Path(__file__).resolve().parents[3]
base=root/'outputs/vietmed_600_RE_review'
rows=[json.loads(x) for x in (base/'annotations_draft.jsonl').read_text(encoding='utf-8').splitlines()]
mapping=json.loads((base/'tieng_viet_thuoc_duoc_chat/anh_xa_nhan.json').read_text(encoding='utf-8'))
lookup={r['id']:r for r in rows}; seen=[]; report=[]
for p in sorted((base/'tieng_viet_thuoc_duoc_chat').glob('*.docx')):
 d=Document(p); current=None; counts={'entities':0,'relations':0}; mismatch=[]; check_text=False
 for el in d.element.body:
  txt=''.join(el.itertext()) if False else ''.join(t.text or '' for t in el.iter(qn('w:t')))
  if re.fullmatch(r'Mẫu VM600-\d{3}',txt):
   current=txt.split()[-1];seen.append(current);check_text=True;continue
  if check_text and el.tag==qn('w:p'):
   r=lookup[current];cursor=0;expected=''
   for e in r['entities']:
    expected+=r['text'][cursor:e['start']]+e['text']+' ['+e['id']+']';cursor=e['end']
   expected+=r['text'][cursor:]
   if txt!=expected:mismatch.append([current,'source_text',txt,expected])
   check_text=False
  if el.tag==qn('w:tbl') and current:
   lines=[[ ''.join(t.text or '' for t in c.iter(qn('w:t'))) for c in row.findall(qn('w:tc'))] for row in el.findall(qn('w:tr'))]
   kind='entities' if lines[0][0]=='Mã' and lines[0][1]=='Cụm từ' else 'relations'
   expected=lookup[current][kind]
   if len(lines)-1!=len(expected):mismatch.append([current,kind,'count'])
   for actual,ex in zip(lines[1:],expected):
    if actual[0]!=ex['id'] or actual[-1]!=mapping[kind][ex['label']]:mismatch.append([current,kind,actual,ex])
    if kind=='entities' and actual[1]!=ex['text']:mismatch.append([current,'surface',actual])
    if kind=='relations':
     ed={e['id']:e for e in lookup[current]['entities']}
     expected_pair=f'{ex["head"]} “{ed[ex["head"]]["text"]}” → {ex["tail"]} “{ed[ex["tail"]]["text"]}”'
     if actual[1]!=expected_pair:mismatch.append([current,'pair',actual])
   counts[kind]+=len(lines)-1
 with ZipFile(p) as z:
  xml=z.read('word/document.xml').decode('utf-8')
  tracked=bool(re.search(r'<w:(ins|del)\b',xml));comments=any('comments' in n for n in z.namelist())
 report.append({'file':p.name,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'counts':counts,'mismatches':mismatch,'tracked_changes':tracked,'comments':comments,'review_marker':[x.text for x in d.paragraphs if x.text.startswith('Đã duyệt đến:')]})
assert len(seen)==len(set(seen))==600
assert not any(r['mismatches'] or r['tracked_changes'] or r['comments'] for r in report),report
(Path(__file__).parent/'input_verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(report,ensure_ascii=False,indent=2))

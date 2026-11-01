import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'outputs/vietmed_600_RE_review'
OUT.mkdir(parents=True,exist_ok=True)
rows=[json.loads(x) for x in (ROOT/'outputs/vietmed_600_ner_6_loai/vietmed_600_ner_6_loai.jsonl').read_text(encoding='utf-8').splitlines()]
schema=json.loads((ROOT/'re_labels.json').read_text(encoding='utf-8'))
for r in rows:
    ents=[]; pos=0; current=None
    for i,(w,t) in enumerate(zip(r['words'],r['labels'])):
        a=r['text'].find(w,pos); assert a>=0
        b=a+len(w);pos=b
        if t=='O': current=None;continue
        p,k=t.split('-',1)
        if p=='I':
            assert current is not None and current['label']==k
            current.update(end=b,token_end=i+1)
        else:
            current=dict(id=f'E{len(ents)+1}',start=a,end=b,token_start=i,token_end=i+1,label=k)
            ents.append(current)
    for e in ents:e['text']=r['text'][e['start']:e['end']]
    pairs=[]
    for e in ents:
        for f in ents:
            for rel in schema['relations']:
                if e['label']==rel['head_type'] and f['label']==rel['tail_type']:
                    pairs.append(dict(id=f'R{len(pairs)+1}',head=e['id'],tail=f['id'],allowed_relation=rel['label']))
    r.update(entities=ents,pairs=pairs)
(OUT/'prepared.json').write_text(json.dumps(rows,ensure_ascii=False),encoding='utf-8')
for batch in range(6):
    lines=[]
    for r in rows[batch*100:(batch+1)*100]:
        lines.append(f"{r['id']} {r['text']}")
        lines.append(' '.join(f"{e['id']}={e['text']}<{e['label']}>" for e in r['entities']))
        if r['pairs']:lines.append(' '.join(f"{p['id']}:{p['head']}>{p['tail']}:{p['allowed_relation']}" for p in r['pairs']))
    (OUT/f'read_{batch+1}.txt').write_text('\n'.join(lines),encoding='utf-8')
print('samples',len(rows),'pairs',sum(len(r['pairs']) for r in rows),'samples_with_pairs',sum(bool(r['pairs']) for r in rows))

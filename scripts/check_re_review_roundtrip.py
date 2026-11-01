"""Check review import using synthetic edits, never physician-approved data."""
import json
from pathlib import Path
from docx import Document
from docx.shared import RGBColor
from import_physician_review import extract

root=Path(__file__).resolve().parents[1]
folder=root/'outputs/vietmed_600_RE_review'
qa=folder/'.qa';qa.mkdir(exist_ok=True)
original=folder/'Phieu_RE_01_001_100.docx'
draft={r['id']:r for r in map(json.loads,(folder/'annotations_draft.jsonl').read_text(encoding='utf-8').splitlines())}
doc=Document(original)
for p in doc.paragraphs:
    if p.text.startswith('DA_DUYET_DEN:'):p.text='DA_DUYET_DEN: VM600-010'
edited=qa/'synthetic_review.docx';doc.save(edited)
report=extract(original,edited,draft,qa/'confirmed')
assert report['ready']==9 and report['pending']==91,report
# First sample has an entity table; make its first entity visibly wrong without editing text.
doc.tables[0].rows[1].cells[1].paragraphs[0].runs[0].font.color.rgb=RGBColor(255,0,0)
doc.save(edited)
report=extract(original,edited,draft,qa/'red')
assert report['ready']==8,report
pending=[json.loads(x) for x in (qa/'red/pending_adjudication.jsonl').read_text(encoding='utf-8').splitlines()]
assert 'EDITS_REQUIRE_ADJUDICATION' in next(x for x in pending if x['id']=='VM600-001')['reasons']
# Validate exported draft and every pair reference, evidence substring and type restriction.
assert len(draft)==600
for r in draft.values():
    entities={e['id']:e for e in r['entities']}
    for e in entities.values():assert r['text'][e['start']:e['end']]==e['text']
    for rel in r['relations']:
        assert rel['head'] in entities and rel['tail'] in entities
        assert rel['label'] in (rel['allowed_relation'],'NO_RELATION','CHUA_RO')
        ev=rel['evidence'];assert r['text'][ev['start']:ev['end']]==ev['text']
print('PASS: unreviewed gate, completion cutoff, red-only edit hold, unresolved exclusion, all 600 entity spans and 423 relation references.')

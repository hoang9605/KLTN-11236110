"""Map the exported sample using the project's existing entity mapping only."""
import ast
import hashlib
import json
from collections import Counter
from pathlib import Path

root = Path(__file__).resolve().parents[1]
config_path = root / 'ner/config.py'
tree = ast.parse(config_path.read_text(encoding='utf-8'))
mapping = next(ast.literal_eval(n.value) for n in tree.body
               if isinstance(n, ast.AnnAssign) and isinstance(n.target, ast.Name)
               and n.target.id == 'VIETMED_TO_TARGET')
source = root / 'outputs/vietmed_600_ner_goc/vietmed_600_ner_goc.jsonl'
rows = [json.loads(line) for line in source.read_text(encoding='utf-8').splitlines()]
out = root / 'outputs/vietmed_600_ner_6_loai'
out.mkdir(parents=True, exist_ok=True)

def convert(label):
    if label in ('0', 'O'):
        return 'O'
    prefix, entity = label.split('-', 1)
    assert prefix in ('B', 'I'), label
    return f'{prefix}-{mapping[entity]}' if entity in mapping else 'O'

packet = []
counts = Counter()
md = ['# 600 mẫu VietMed-NER — 6 loại thực thể của dự án', '',
      'Ánh xạ theo ner/config.py. Giữ nguyên văn bản, token và tiền tố B/I; các loại ngoài phạm vi đổi thành O. Nhãn gốc được giữ riêng để đối chiếu. Không áp dụng quy tắc hậu xử lý hoặc thêm quan hệ RE.', '',
      '| Nhãn gốc | Nhãn dự án |', '|---|---|']
md += [f'| {old} | {new} |' for old, new in mapping.items()]
md += ['']
for row in rows:
    labels = [convert(label) for label in row['labels']]
    record = {k:v for k,v in row.items() if k not in ('labels', 'tags')}
    record.update(source_labels=row['labels'], source_tag_ids=row['tags'], labels=labels)
    packet.append(record)
    counts.update(labels)
    md += [f'## {row["id"]} — dòng train {row["source_row_index"]} (đếm từ 0)', '', row['text'], '',
           '| Token | Nhãn dự án | Nhãn gốc |', '|---|---|---|']
    md += [f'| {word.replace(chr(124), "&#124;")} | {new} | {old} |'
           for word, new, old in zip(row['words'], labels, row['labels'])]
    md += ['']
dest = out / 'vietmed_600_ner_6_loai.jsonl'
dest.write_text(''.join(json.dumps(r, ensure_ascii=False)+'\n' for r in packet), encoding='utf-8')
(out / 'vietmed_600_ner_6_loai.md').write_text('\n'.join(md), encoding='utf-8')
manifest = dict(samples=len(packet), mapping=mapping, mapping_source='ner/config.py',
                mapping_config_sha256=hashlib.sha256(config_path.read_bytes()).hexdigest(),
                source_jsonl_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
                output_jsonl_sha256=hashlib.sha256(dest.read_bytes()).hexdigest(),
                outside_label='O', non_target_entities='O', bio_prefixes_preserved=True,
                postprocessing_applied=False, relation_annotations_added=False,
                source_fields={'labels':'source_labels', 'tags':'source_tag_ids'},
                target_field='labels', token_label_counts=dict(sorted(counts.items())))
(out/'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
loaded = [json.loads(line) for line in dest.read_text(encoding='utf-8').splitlines()]
assert len(loaded) == len(rows) == 600
allowed = {'O'} | {f'{p}-{t}' for p in ('B','I') for t in mapping.values()}
for original, mapped in zip(rows, loaded):
    assert all(original[k] == mapped[k] for k in ('id','text','words','source_row_index','source_split'))
    assert original['labels'] == mapped['source_labels']
    assert original['tags'] == mapped['source_tag_ids']
    assert len(mapped['words']) == len(mapped['labels'])
    assert set(mapped['labels']) <= allowed
    assert mapped['labels'] == [convert(t) for t in original['labels']]
print('PASS: 600 samples; original text/tokens/source labels preserved; all target labels match project mapping.')
print(json.dumps(dict(sorted(counts.items()))))

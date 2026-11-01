"""Export 600 reproducible train samples with untouched source NER labels."""
import hashlib
import json
import random
from pathlib import Path
import pyarrow as pa

root = Path(__file__).resolve().parents[1]
source = Path.home()/'.cache/huggingface/datasets/leduckhai___viet_med-ner/default/0.0.0/e3d0393c733858402a7c04228f45d351d2ce6d8f/viet_med-ner-train.arrow'
out = root/'outputs/vietmed_600_ner_goc'
out.mkdir(parents=True, exist_ok=True)
with pa.memory_map(str(source), 'r') as stream:
    rows = pa.ipc.open_stream(stream).read_all().select(['text','words','labels','tags']).to_pylist()
seed = 20261003
indices = sorted(random.Random(seed).sample(range(len(rows)), 600))
packet = [dict(id=f'VM600-{n:03}', source_row_index=i, source_split='train', **rows[i]) for n,i in enumerate(indices,1)]
dest = out/'vietmed_600_ner_goc.jsonl'
dest.write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in packet),encoding='utf-8')
md = ['# 600 mẫu VietMed-NER — nhãn gốc', '', 'Nguồn: https://huggingface.co/datasets/leduckhai/VietMed-NER', '', 'Chọn ngẫu nhiên 600 dòng train, seed 20261003. Giữ nguyên text, words, labels, tags; không quy đổi nhãn, không thêm RE. Bảng ghi từng token để giữ nguyên ranh giới BIO. Nhãn 0 cũng được giữ nguyên như nguồn.', '']
for r in packet:
    md += [f'## {r["id"]} — dòng train {r["source_row_index"]} (đếm từ 0)', '', r['text'], '', '| Token | Nhãn gốc |', '|---|---|']
    assert len(r['words']) == len(r['labels']) == len(r['tags'])
    md += [f'| {w.replace(chr(124), "&#124;")} | {label} |' for w,label in zip(r['words'],r['labels'])]
    md += ['']
(out/'vietmed_600_ner_goc.md').write_text('\n'.join(md),encoding='utf-8')
manifest = dict(source='leduckhai/VietMed-NER', split='train', source_train_rows=len(rows), samples=600, seed=seed, sampling='Random sample without replacement, sorted by source row index', index_base=0, source_cache_fingerprint=source.parent.name, source_row_indices=indices, preserved_fields=['text','words','labels','tags'], audio_exported=False, labels_remapped=False, relations_added=False, sha256=hashlib.sha256(dest.read_bytes()).hexdigest())
(out/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
loaded=[json.loads(line) for line in dest.read_text(encoding='utf-8').splitlines()]
assert len(loaded)==600 and len({r['source_row_index'] for r in loaded})==600
for r in loaded:
    assert all(r[k]==rows[r['source_row_index']][k] for k in ['text','words','labels','tags'])
print('PASS: 600 unique source rows; all text, words, labels, tags exactly match cached train.')
print(dest)

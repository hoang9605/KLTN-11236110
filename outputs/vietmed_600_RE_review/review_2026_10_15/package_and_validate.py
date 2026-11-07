import collections,hashlib,json,re,zipfile
from pathlib import Path
OUT=Path(__file__).parent
source=OUT.parent/'annotations_draft.jsonl'
old=[json.loads(x) for x in source.read_text(encoding='utf-8').splitlines()]
rows=[json.loads(x) for x in (OUT/'annotations_reviewed_600.jsonl').read_text(encoding='utf-8').splitlines()]
changes=[json.loads(x) for x in (OUT/'changes.jsonl').read_text(encoding='utf-8').splitlines()]
stats=json.loads((OUT/'stats.json').read_text(encoding='utf-8'))
SCHEMA={('CONDITION','BODY_PART'):'located_at',('CONDITION','DRUG'):'treated_by',('CONDITION','PROCEDURE'):'treated_by_procedure',('CONDITION','TEST'):'diagnosed_by',('DRUG','DOSAGE'):'has_dosage'}
labels={'CONDITION':'Bệnh hoặc triệu chứng','DRUG':'Thuốc/dược chất','BODY_PART':'Bộ phận cơ thể','TEST':'Xét nghiệm hoặc thăm khám','PROCEDURE':'Thủ thuật hoặc điều trị','DOSAGE':'Liều lượng'}
rels={'located_at':'Có vị trí ở','treated_by':'Được điều trị bằng thuốc','treated_by_procedure':'Được điều trị bằng phương pháp','diagnosed_by':'Được chẩn đoán bằng','has_dosage':'Có liều lượng','NO_RELATION':'Không có quan hệ thuộc 5 loại','CHUA_RO':'Chưa rõ — cần chốt'}
assert len(rows)==600 and [r['id'] for r in rows]==[f'VM600-{n:03}' for n in range(1,601)]
for r,b in zip(rows,old):
 assert (r['id'],r['text'],r['words'],r['source_row_index'],r['source_split'])==(b['id'],b['text'],b['words'],b['source_row_index'],b['source_split'])
 assert not r['human_verified'] and not r['training_eligible']
 assert len(r['words'])==len(r['labels'])
 ed={e['id']:e for e in r['entities']};assert len(ed)==len(r['entities'])
 bio=['O']*len(r['words']);prev_end=0
 for e in r['entities']:
  assert e['label'] in labels
  assert 0<=e['start']<e['end']<=len(r['text']) and r['text'][e['start']:e['end']]==e['text']
  assert prev_end<=e['start'];prev_end=e['end']
  assert ' '.join(r['words'][e['token_start']:e['token_end']])==e['text']
  for i in range(e['token_start'],e['token_end']):bio[i]=('B-' if i==e['token_start'] else 'I-')+e['label']
 assert bio==r['labels']
 expected={(h['id'],t['id']) for h in ed.values() for t in ed.values() if (h['label'],t['label']) in SCHEMA}
 actual=[(p['head'],p['tail']) for p in r['relations']]
 assert len(actual)==len(set(actual)) and set(actual)==expected
 assert len({p['id'] for p in r['relations']})==len(r['relations'])
 for p in r['relations']:
  h,t=ed[p['head']],ed[p['tail']]
  assert p['allowed_relation']==SCHEMA[h['label'],t['label']]
  assert p['label'] in (p['allowed_relation'],'NO_RELATION','CHUA_RO')
  ev=p['evidence'];assert r['text'][ev['start']:ev['end']]==ev['text']
  if p['label']=='CHUA_RO':assert r['review_flags']
# Policy regression: these known formerly split spans must now be one CONDITION.
for n,s in [(52,'đau nhức xương khớp'),(132,'viêm loét dạ dày'),(204,'thoái hóa cột sống thắt lưng'),(329,'đau khớp'),(414,'viêm loét đại tràng'),(521,'lở loét miệng'),(572,'thiếu máu cơ tim')]:
 assert any(e['text']==s and e['label']=='CONDITION' for e in rows[n-1]['entities'])
for n,s in [(27,'não'),(96,'môi'),(248,'mô'),(414,'khám'),(531,'khám')]:
 assert not any(e['text']==s for e in rows[n-1]['entities'])
for n in (472,561,569):
 assert not any(p['label'] in ('treated_by','treated_by_procedure') for p in rows[n-1]['relations'])
counts=collections.Counter(r['text'] for r in rows)
validation={'status':'PASS','samples':600,'input_docx_files':6,'input_texts_and_table_rows_match':True,
 'original_text_preserved':True,'valid_entity_offsets':True,'valid_BIO':True,'no_overlapping_entities':True,
 'complete_eligible_candidate_pairs':True,'valid_relation_direction':True,'no_duplicate_relation_pairs':True,
 'full_condition_span_policy_checks':True,'prevention_not_mislabeled_treatment':True,
 'duplicate_exact_text_groups':sum(v>1 for v in counts.values()),
 'semantic_accuracy_measured':False,'human_verified_samples':0,
 'docx_rendering':'Unavailable: bundled renderer reported LibreOffice soffice.exe not found; no new DOCX released.'}
(OUT/'validation.json').write_text(json.dumps(validation,ensure_ascii=False,indent=2),encoding='utf-8')

by_id=collections.defaultdict(list)
for c in changes:by_id[c['sample_id']].append(c)
def e_summary(e):
 return '∅' if e is None else f'{e["id"]} “{e["text"]}” {e["label"]} [{e["start"]}, {e["end"]})'
files=[]
for batch in range(6):
 subset=rows[batch*100:(batch+1)*100]
 lines=[f'# Phiếu rà soát NER và RE {batch*100+1:03} đến {(batch+1)*100:03}',
 '', 'Bản AI rà soát lần hai ngày 15/10/2026. Giữ nguyên câu nguồn và sáu loại NER, năm quan hệ RE. Chưa được chuyên gia xác nhận.',
 '', 'Quy tắc người dùng đã chốt: giữ cả cụm bệnh/triệu chứng trong một CONDITION. Không tách bộ phận bên trong cụm để tạo located_at. Vị trí được nêu riêng bằng giới từ hoặc mệnh đề riêng vẫn được xét.',
 '', 'Vị trí ký tự là khoảng [start, end), đếm từ 0 theo Unicode. Mã E ổn định khi sửa; mã R được tạo lại. Không dùng CHUA_RO làm nhãn huấn luyện hoặc nhãn âm.', '']
 for r in subset:
  lines += [f'## {r["id"]}', '', '**Đoạn gốc:** '+r['text'], '',
   '**Trạng thái:** '+('Cần chốt ngữ cảnh/quy ước' if r['review_flags'] else 'Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold'), '', '### NER', '']
  if r['entities']:
   lines+=['| Mã | Cụm từ | Nhãn | Vị trí |','|---|---|---|---|']
   lines += [f'| {e["id"]} | {e["text"]} | {labels[e["label"]]} ({e["label"]}) | [{e["start"]}, {e["end"]}) |' for e in r['entities']]
  else:lines+=['Không có thực thể thuộc sáu loại được giữ trong bản rà soát.']
  lines+=['','### RE','']
  ed={e['id']:e for e in r['entities']}
  if r['relations']:
   lines+=['| Mã | Cặp có hướng | Kết luận đề xuất |','|---|---|---|']
   for p in r['relations']:
    lines += [f'| {p["id"]} | {p["head"]} “{ed[p["head"]]["text"]}” → {p["tail"]} “{ed[p["tail"]]["text"]}” | {rels[p["label"]]} ({p["label"]}) |']
  else:lines+=['Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.']
  if r['review_flags']:
   lines+=['','### Cần chốt','']+['- '+f for f in r['review_flags']]
  edits=[c for c in by_id[r['id']] if c['action'].endswith('entity')]
  if edits:
   lines+=['','### Thay đổi NER','']
   lines+=['- '+e_summary(c['before'])+' → '+e_summary(c['after']) for c in edits]
  lines+=['',f'Nguồn: VietMed-NER train, dòng {r["source_row_index"]} (từ 0).','']
 path=OUT/f'Phieu_da_ra_soat_{batch*100+1:03}-{(batch+1)*100:03}.md'
 path.write_text('\n'.join(lines),encoding='utf-8');files.append(path)
 assert len(re.findall(r'^## VM600-\d{3}$',path.read_text(encoding='utf-8'),re.M))==100

readme=f'''# Bộ nhãn VietMed 600 sau rà soát lần hai

Ngày 15/10/2026, đã đọc và đối chiếu đủ 600 mẫu của sáu phiếu được cung cấp. Bản này sửa nhãn và lưu lịch sử để người duyệt có thể truy ngược từng thay đổi. Đây là bản AI rà soát, chưa phải dữ liệu gold được bác sĩ xác nhận.

## Kết quả

- {stats['changed_samples']} mẫu có thay đổi NER hoặc RE.
- NER từ {stats['entities_before']} xuống {stats['entities_after']} thực thể. Nhật ký có {stats['change_events']['remove_entity']} thao tác xóa, {stats['change_events']['add_entity']} bổ sung và {stats['change_events']['edit_entity']} sửa. Một thực thể có thể được sửa qua nhiều bước; số thao tác không phải số thực thể duy nhất.
- {stats['resolved_provisional_samples']} mẫu chưa phát hiện điểm cần phân xử trong lượt AI này; {stats['pending_samples']} mẫu cần chốt ngữ cảnh hoặc quy ước.
- RE còn 20 located_at, 19 treated_by_procedure, 2 treated_by, 137 NO_RELATION và 62 CHUA_RO. Chưa có quan hệ dương diagnosed_by hoặc has_dosage đủ căn cứ để chốt trong bản này.
- Các con số là thống kê chỉnh sửa, không phải độ chính xác đo trên tập gold.

## Quy tắc đã chốt với người dùng

Giữ nguyên toàn bộ cụm bệnh/triệu chứng trong một CONDITION. Ví dụ “đau khớp”, “viêm loét dạ dày”, “thiếu máu cơ tim” là một thực thể; không đánh dấu thêm BODY_PART lồng trong đó và không tạo located_at nội bộ. Nếu vị trí được diễn đạt riêng bằng “ở”, “trong” hoặc một mệnh đề khác, vẫn xét quan hệ theo văn bản. Không tự sửa lỗi phiên âm của câu nguồn.

Giữ sáu loại NER và năm quan hệ dự án. Tác nhân như vi khuẩn/virus không tự trở thành bệnh; “nhiễm virus” là tình trạng bệnh. Số thứ tự, tỷ lệ, mức độ và lượng thực phẩm không phải liều thuốc. Đồng xuất hiện, phòng ngừa và gây tác dụng phụ không chứng minh quan hệ điều trị. Câu thiếu ngữ cảnh giữ CHUA_RO hoặc đưa cả mẫu vào hàng chờ; không mặc nhiên xuất thành mẫu âm.

## Các tệp

- `annotations_reviewed_600.jsonl`: toàn bộ 600 mẫu sau rà soát, gồm NER, BIO, tất cả cặp ứng viên RE và lý do cần chốt.
- `resolved_provisional.jsonl`: {stats['resolved_provisional_samples']} mẫu chưa còn cờ phân xử trong lượt AI; không đồng nghĩa được bác sĩ duyệt.
- `needs_adjudication.jsonl`: {stats['pending_samples']} mẫu cần phân xử.
- `Phieu_da_ra_soat_*.md`: sáu phiếu tiếng Việt, mỗi phiếu 100 mẫu, có câu gốc, nhãn hiện tại, thay đổi NER và vấn đề cần chốt.
- `changes.jsonl`: lịch sử trước/sau từng thay đổi; mã E thuộc mẫu, mã R được tái tạo theo bản hiện tại.
- `stats.json`, `validation.json`, `input_verification.json`: thống kê, kết quả kiểm tra cấu trúc và dấu vân tay sáu tệp nguồn.

## Trước khi dùng làm bộ chuẩn

1. Duyệt các quy ước còn mở: nhãn chung như “điều trị”, “bệnh lý”; phạm vi mỹ phẩm/thực phẩm/hóa chất nội sinh; cảm xúc thông thường; câu hỏi và phủ định.
2. Với từng mẫu có cờ, xem ngữ cảnh hoặc audio gốc, rồi xác nhận/sửa NER trước khi chốt RE. Không ghép ngữ cảnh từ các số mẫu liền nhau vì đây là các dòng nguồn được chọn.
3. Sau khi bác sĩ/người gán nhãn xác nhận, ghi người duyệt và ngày duyệt rồi mới xuất dữ liệu huấn luyện/đánh giá. Tất cả mẫu hiện có `human_verified=false` và `training_eligible=false` để tránh nhầm bản AI với gold.
4. Không đủ căn cứ kết luận bộ này bao phủ tốt cả năm quan hệ: hiện thiếu ví dụ dương diagnosed_by và has_dosage, treated_by rất ít. Cần bổ sung dữ liệu thật nếu huấn luyện đủ năm lớp; không bịa ví dụ vào 600 câu gốc.
5. Nguồn của các mẫu là train VietMed-NER. Nếu checkpoint NER đã học các dòng này, không dùng chúng làm tập kiểm thử độc lập để tuyên bố khả năng tổng quát hóa.

## Kiểm tra đã thực hiện

Đối chiếu nội dung câu và từng hàng NER/RE của cả sáu DOCX với JSONL nguồn; kiểm tra 600 ID duy nhất; giữ nguyên văn bản và dòng nguồn; kiểm tra offset, BIO, span không chồng lấn, chiều quan hệ, kiểu đầu/cuối, đầy đủ cặp hợp lệ, không trùng cặp và chuỗi bằng chứng. Có kiểm tra riêng cho các lỗi “sầu não”, “môi trường”, “khám phá”, quy tắc CONDITION đầy đủ và quan hệ phòng ngừa.

Sáu tệp Word gốc không bị thay đổi. Phiếu mới được xuất Markdown vì bộ kết xuất Word hiện không có LibreOffice, nên chưa thể kiểm tra bố cục DOCX bằng ảnh. Không phát hành bản Word mới chưa qua kiểm tra bố cục.
'''
(OUT/'HUONG_DAN_VA_KET_QUA.md').write_text(readme,encoding='utf-8')
files += [OUT/n for n in ('HUONG_DAN_VA_KET_QUA.md','annotations_reviewed_600.jsonl','resolved_provisional.jsonl','needs_adjudication.jsonl','changes.jsonl','stats.json','validation.json','input_verification.json')]
manifest={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
(OUT/'manifest_sha256.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8');files.append(OUT/'manifest_sha256.json')
archive=OUT/'Bo_nhan_NER_RE_600_da_ra_soat.zip'
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
 for p in files:z.write(p,p.name)
with zipfile.ZipFile(archive) as z:
 assert z.testzip() is None
 for name,digest in manifest.items():assert hashlib.sha256(z.read(name)).hexdigest()==digest
print(json.dumps(validation,ensure_ascii=False,indent=2))
print('Packaged',len(files),'files;',archive.stat().st_size,'bytes')

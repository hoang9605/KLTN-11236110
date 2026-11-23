# Kế hoạch kiểm chứng dữ liệu sinh (augment) cho RE, lập 2026-11-21, sửa lần 1: kiểm chứng hoàn toàn bằng tiếng Anh

## Vấn đề

`relation/synth.py` sinh câu bằng cách thay thực thể (`mention_replacement`) và điền mẫu (`template`, `hard_negative`). Khi thay, hệ thống chỉ kiểm tra thực thể mới có **cùng kiểu và cùng nhóm chuyên khoa** trong `re_v3/lexicon.json` hay không. Nó không kiểm tra từ mới có hợp với các chữ xung quanh. Ví dụ lỗi trong `x1.jsonl`:

| Câu sinh | Lỗi |
|---|---|
| "... giúp cho **đầu gối** thông lên não lên tim ..." | Bộ phận mới không hợp ngữ cảnh "thông lên não" |
| "đau dạ dày" → "đau **thận**" | Cụm "từ đứng trước + thực thể mới" không phải cách gọi y khoa chuẩn |
| "... được **hóa trị phẫu thuật** để tiêu diệt ..." | Thực thể mới ghép với từ cũ thành cụm vô nghĩa |

Quy mô cần kiểm: 2.874 câu sinh (4.946 cặp). Trong đó chỉ có 454 chuỗi thực thể khác nhau và 707 bộ ba dương khác nhau, nên mỗi đơn vị chỉ cần tra một lần rồi lưu cache.

## Vì sao kiểm chứng bằng tiếng Anh

- Câu VietMed là văn nói, còn tài liệu của Bộ Y tế viết theo văn viết, nên tra trực tiếp bằng tiếng Việt sẽ trượt nhiều. Khi chuyển sang thuật ngữ chuẩn tiếng Anh thì các cách nói khác nhau ("huyết áp cao" và "tăng huyết áp") quy về cùng một khái niệm (hypertension).
- Nguồn tiếng Anh có cấu trúc và tra được bằng máy: ICD-10 tiếng Anh, quan hệ thuốc–bệnh của NLM (MED-RT `may_treat`) và các trang thông tin của WHO.
- Repo đã có sẵn phần lớn công cụ:
  - `ICD-10/phu-lu-c-1-...-6.xlsx`, danh mục ICD-10 của Bộ Y tế (QĐ 2020), có **cả cột `DISEASE NAME` tiếng Anh lẫn cột `TÊN BỆNH`**;
  - `normalization/icd10.py`, ánh xạ tên bệnh tiếng Việt sang mã ICD-10;
  - `normalization/rxnorm.py`, ánh xạ tên thuốc sang RxCUI qua RxNav, có cache và bảng alias tiếng Việt.

  Vì vậy **không cần tải thêm PDF nào**.

Quy ước: mọi trường dữ liệu, nhãn kết luận, câu truy vấn, đoạn trích bằng chứng và lập luận của AI đều viết bằng tiếng Anh. Chỉ câu gốc và câu sinh giữ tiếng Việt, vì đó là dữ liệu huấn luyện.

## Pipeline

```
seed ─► synth.py (giữ vết thay thế) ─► pool.jsonl
                                         │
                         Bước 1: tách đơn vị K1/K2/K3
                                         │
                         Bước 2: dịch sang thuật ngữ chuẩn tiếng Anh
                         (ICD-10 EN, RxNorm, bảng thuật ngữ cho BODY_PART/PROCEDURE/TEST)
                                         │
             ┌───────────────────────────┼───────────────────────────┐
             ▼                           ▼                           ▼
   K1. Cụm từ ghép                K2. Bộ ba quan hệ             K3. Ngữ cảnh câu
   "kidney pain"?                 (Parkinson, may_treat,        bản dịch sát nghĩa
   ICD-10 EN, WHO                 levodopa)? MED-RT, WHO        do AI chấm
             └───────────────────────────┼───────────────────────────┘
                                         ▼
                      VALID / INVALID + reason + evidence (EN)
                                         ▼
                     Phiếu cho chuyên gia ─► nhập lại ─► x1/x3 mới ─► ablation trên dev
```

### Bước 0. Giữ vết thay thế

`mention_replacement` có trả về `replaced: {entity, old, new}` nhưng `synth.py` không ghi trường này ra file. Sửa để mỗi câu sinh lưu `replaced`, `parent_text` và `template`. Chạy lại với cùng `SEED`; kết quả phải trùng với kho cũ, chỉ có thêm trường.

### Bước 1. Đơn vị cần kiểm

| Mã | Đơn vị | Ví dụ | Áp dụng cho |
|---|---|---|---|
| K1 | **Cụm ghép**: thực thể mới cùng 1–2 từ y khoa liền trước hoặc liền sau ("đau", "viêm", "ung thư", "phẫu thuật", "thuốc", ...) | "đau thận" → *kidney pain* | `mention_replacement` |
| K2 | **Bộ ba quan hệ dương** | (Parkinson disease, treated_by, levodopa) | mọi cách sinh, chỉ cặp dương |
| K3 | **Ngữ cảnh**: các từ còn lại có hợp với thực thể mới không | "đầu gối thông lên não" | `mention_replacement` |

### Bước 2. Dịch sang thuật ngữ chuẩn tiếng Anh

| Kiểu | Cách dịch | Nguồn |
|---|---|---|
| CONDITION | `ICD10Normalizer` → mã → cột `DISEASE NAME` | ICD-10 Bộ Y tế, cột tiếng Anh |
| DRUG | `RxNormNormalizer` → RxCUI → tên chuẩn | RxNorm (NLM) |
| BODY_PART, PROCEDURE, TEST | Bảng thuật ngữ `en_terms.json` do Claude dịch, khoảng 150–200 chuỗi. Bạn xem nhanh bảng này một lần. | — |
| K1 (cụm ghép) | Dịch cả cụm, ví dụ "đau thận" → *kidney pain*, "viêm đầu gối" → *knee inflammation* | Claude, ghi vào cache |
| K3 (cả câu) | Dịch **sát nghĩa từng chữ**, không sửa cho trôi chảy, để lỗi không bị bản dịch che mất | Claude |

Thực thể nào không ánh xạ được ở bước này thì đánh dấu `unmapped`, và câu chứa nó bị xếp INVALID với reason `unmapped_entity`.

### Bước 3. Tra bằng chứng tiếng Anh

| # | Nguồn | Dùng cho | Cách tra |
|---|---|---|---|
| 1 | **ICD-10 (tên tiếng Anh)**, file Bộ Y tế đã có trong repo | K1 với CONDITION + BODY_PART: tên bệnh có đi kèm vị trí đó không. Kiểm tra thêm vị trí có khớp chương ICD không (chương K tiêu hoá đi với stomach, liver, ...) | Tra trong máy |
| 2 | **RxNav / RxClass, quan hệ MED-RT `may_treat`, `may_diagnose`** | K2 treated_by: thuốc có chỉ định cho bệnh đó không. Bổ sung cho diagnosed_by nếu có. | API công khai của NLM, đã dùng trong `rxnorm.py`; lưu cache SQLite |
| 3 | **WHO**: fact sheets, ICD-11 browser (who.int) | K1 và K2 cho located_at, treated_by_procedure, diagnosed_by | Claude chạy WebSearch theo lô với `site:who.int` |
| 4 | Văn bản tiếng Anh của BioText và ADE (`data/external_en_raw/`, đã tải trước đây) | K2: bộ ba có xuất hiện trong câu y khoa thật không | Tra trong máy |
| 5 | WebSearch `site:who.int OR site:nih.gov` | Đơn vị chưa có kết quả ở nguồn 1–4 | Claude, theo lô, lưu cache |

Mỗi lần tra ghi một dòng vào `relation/data/synth/validate/evidence.jsonl`:

```json
{"unit": "K2", "query": "levodopa may_treat Parkinson disease", "source": "RxClass MED-RT",
 "url": "...", "snippet": "...", "result": "supported | not_found | contradicted"}
```

Python không gọi được WebSearch, nên nguồn 3 và 5 do Claude chạy trong phiên, có thể chia cho subagent. Nguồn 1, 2 và 4 chạy bằng script.

### Bước 4. Quy tắc kết luận

Chỉ có hai nhãn, không có nhãn "chưa chắc".

| Verdict | Điều kiện |
|---|---|
| **VALID** | Thoả **cả ba** điều kiện: K1 `supported` (hoặc câu không có K1); mọi K2 dương `supported` ở ít nhất 1 nguồn; K3 `plausible` |
| **INVALID** | Mọi trường hợp còn lại |

Mỗi câu INVALID có một `reason` (tiếng Anh). Câu có nhiều lỗi thì lấy lỗi nặng nhất:

| `reason` | Nghĩa | Mức |
|---|---|---|
| `contradicted` | Có nguồn nói ngược lại, ví dụ thuốc chống chỉ định với bệnh, hoặc vị trí sai chương ICD | nặng nhất |
| `implausible_context` | K3 bị chấm `implausible` | |
| `collocation_not_found` | K1 không có ở nguồn nào | |
| `relation_not_found` | K2 dương không có ở nguồn nào | |
| `unmapped_entity` | Không ánh xạ được thực thể sang thuật ngữ tiếng Anh | nhẹ nhất |

Nguyên tắc là không có bằng chứng thì INVALID. Cách này thận trọng: dữ liệu huấn luyện chỉ nhận câu đã được chứng minh. Ba reason cuối là loại "không tìm thấy" chứ không phải "sai", nên đó là chỗ chuyên gia cần xem kỹ nhất để cứu lại câu đúng.

Câu INVALID không bị xoá mà chuyển sang `invalid.jsonl` kèm `reason`. File này dùng để báo cáo tỉ lệ loại theo từng cách sinh và theo từng reason.

### Bước 5. Phiếu cho chuyên gia

File `relation/data/synth/validate/expert_review.xlsx`. Tiêu đề cột viết bằng tiếng Anh:

`parent_sentence_vi` · `synthetic_sentence_vi` (tô màu thực thể thay) · `literal_translation_en` · `replaced (old → new, EN term)` · `pairs + labels` · `K1 / K2 / K3 result` · `evidence (source, url, snippet)` · `system_verdict` · **`expert_decision` (KEEP / FIX_LABEL / DROP)** · `expert_note`

Phiếu gồm:

- mọi câu INVALID có reason `collocation_not_found`, `relation_not_found` hoặc `unmapped_entity`;
- khoảng 20% câu VALID, chọn ngẫu nhiên;
- khoảng 10% câu INVALID có reason `contradicted` hoặc `implausible_context`.

Hai mẫu sau dùng để đo độ tin cậy của bộ kiểm chứng tự động: precision của VALID và precision của INVALID. Số đo này có thể đưa vào báo cáo. Nếu muốn chuyên gia duyệt hết câu VALID thì chỉ cần đổi tham số.

### Bước 6. Sau khi chuyên gia duyệt

1. `import_expert.py`: nhập phiếu, kiểm tra cột `expert_decision` đã điền đủ, ghi ra `pool_validated.jsonl` với `annotation_status` là `SYNTHETIC_EXPERT_CHECKED` hoặc `SYNTHETIC_AUTO_VALIDATED`.
2. Cân bằng lại tỉ lệ dương và lấy mẫu lại x1/x3 từ kho đã kiểm.
3. Chạy lại ablation trên dev (0×, 1×, 3×, 3 seed), so sánh dữ liệu sinh chưa kiểm với dữ liệu đã kiểm. Chỉ chấm trên test một lần, với cấu hình tốt nhất.

## File mới

```
relation/
├── synth.py                  (sửa: ghi trường replaced, parent_text)
├── validate/
│   ├── units.py              tách K1/K2/K3, khử trùng
│   ├── to_english.py         ánh xạ ICD-10 EN / RxNorm / en_terms.json
│   ├── evidence.py           tra ICD-10 EN, RxClass MED-RT, BioText/ADE; đọc cache WebSearch
│   ├── verdict.py            áp quy tắc, ghi verdicts/invalid
│   ├── make_expert_sheet.py
│   └── import_expert.py
└── data/synth/validate/
    ├── units.jsonl
    ├── en_terms.json         bảng thuật ngữ VI→EN cho BODY_PART/PROCEDURE/TEST
    ├── translations.jsonl    bản dịch sát nghĩa cụm K1 và câu K3
    ├── evidence.jsonl        cache bằng chứng
    ├── context_judgement.jsonl   AI chấm K3 (plausible / implausible + rationale)
    ├── verdicts.jsonl
    ├── invalid.jsonl
    ├── expert_review.xlsx
    └── pool_validated.jsonl
```

## Lịch tối nay (khoảng 5 giờ)

| # | Việc | Ai làm | Thời gian |
|---|---|---|---|
| 1 | Sửa `synth.py` để giữ vết thay thế, chạy lại, đối chiếu với kho cũ | Claude | 20 phút |
| 2 | Tách đơn vị; ánh xạ CONDITION qua ICD-10 EN, DRUG qua RxNorm; lập `en_terms.json` | Claude | 45 phút |
| 3 | Bạn xem nhanh `en_terms.json` (khoảng 150–200 dòng) | **Bạn** | 15 phút |
| 4 | Tra ICD-10 EN, RxClass MED-RT, BioText/ADE bằng script | Claude | 45 phút |
| 5 | WebSearch WHO/NIH theo lô cho các đơn vị còn lại | Claude và subagent | 1 giờ |
| 6 | Dịch sát nghĩa và chấm K3 cho khoảng 925 câu thay thực thể | Claude | 45 phút |
| 7 | Kết luận, thống kê tỉ lệ loại, lập phiếu chuyên gia | Claude | 30 phút |
| 8 | Xem 30 câu mẫu (10 VALID, 10 INVALID loại "sai", 10 INVALID loại "không tìm thấy") để chỉnh ngưỡng | **Bạn** | 20 phút |
| — | Chuyên gia duyệt, nhập phiếu, sinh lại x1/x3, chạy ablation | Sau tối nay | |

## Rủi ro

| Rủi ro | Cách xử lý |
|---|---|
| Bản dịch làm câu trôi chảy hơn và che mất lỗi (ví dụ dịch "đau thận" thành *renal colic*, vốn là cụm đúng) | Dịch sát nghĩa từng chữ cho K1 và K3. Phiếu chuyên gia luôn có câu tiếng Việt bên cạnh bản dịch. |
| Ánh xạ ICD-10 hoặc RxNorm sai làm bằng chứng sai | Ghi mã và tên tiếng Anh vào phiếu để chuyên gia thấy. Thực thể có độ tin cậy ánh xạ thấp thì xếp `unmapped_entity`, và câu thành INVALID. |
| MED-RT không phủ thuốc gọi chung chung ("thuốc giảm đau", "kháng sinh") | Ánh xạ sang lớp thuốc (RxClass, ATC). Nếu không ánh xạ được thì INVALID với reason `unmapped_entity`, và câu vào phiếu chuyên gia. |
| WebSearch bị giới hạn số lần hoặc chậm | Ưu tiên nguồn chạy trong máy, khử trùng đơn vị, lưu cache. Đơn vị không tra được thì INVALID với reason `*_not_found`, và câu vào phiếu chuyên gia. |
| Luật "không có bằng chứng thì INVALID" loại nhầm nhiều câu đúng | Mọi câu INVALID loại "không tìm thấy" đều vào phiếu chuyên gia. Báo cáo cả số câu chuyên gia cứu lại. |
| Quá nhiều câu bị loại làm x3 không đủ cặp | Báo con số thật. Có thể sinh thêm rồi kiểm lại, hoặc bỏ mức x3. |
| AI chấm K3 thiên lệch | Mẫu VALID và INVALID trong phiếu chuyên gia dùng để đo độ tin cậy, và con số này được báo cáo |

# Rà soát repo (23/11/2026)

Mình đã kiểm tra từng thư mục: dung lượng, file nào đang được git theo dõi, và file nào được mã nguồn, báo cáo (`build_report.js`, các script vẽ hình) hoặc pipeline đọc tới.

## 0. Việc cần làm trước tiên: phần lớn công việc RE chưa có trong git

Các thư mục sau **chưa từng được commit**. Nếu ổ đĩa hỏng hoặc lỡ tay xóa thì không có cách nào khôi phục:

- `relation/`: toàn bộ RE làm lại (dữ liệu, huấn luyện, đánh giá, validate, phiếu chuyên gia)
- `web/` (giao diện), `relation_extraction/bert_model.py`, `scripts/re_dataset/`, `scripts/demo/`, `re_v3/`
- 6 tệp kiểm thử mới trong `tests/`, `docs/KE_HOACH_*.md`, các đồ thị `outputs/kg_test_2026-11-08/21/22`, `outputs/re_benchmark_2026-11-08/`

Ngoài ra còn khoảng 20 tệp đã theo dõi nhưng đang sửa dở chưa commit. Nên commit ngay, trước khi dọn dẹp.

## 1. Có thể xóa: không mã nào dùng, không có trong báo cáo (khoảng 1,8 GB)

| Mục | Dung lượng | Lý do |
|---|---:|---|
| `outputs/bao_cao_khoa_luan_2026-11-05/…_v8` → `_v34` (.docx + .pdf) | 141 MB | Các bản báo cáo trung gian, giữ v35 là đủ |
| `outputs/bao_cao_khoa_luan_2026-11-05/BAO_CAO_KHOA_LUAN_2026-11-06/07/08.docx`, `~$…docx`, `…_v16 (AutoRecovered).docx` | 1 MB | Bản rất cũ, file khóa tạm và file tự phục hồi của Word |
| `Model/vihealthbert-re-v1/` | 775 MB | Mô hình RE ngày 08/11, đã bị thay hai lần; không còn trong báo cáo (không có trong git, xóa là mất hẳn) |
| `Model/vihealthbert-re-vietmed/` | 775 MB | Mô hình RE ngày 21/11 (dữ liệu sinh chưa validate). Báo cáo chỉ dùng đồ thị đã dựng từ nó, không dùng mô hình. Nên giữ nếu muốn có cái đối chiếu khi bảo vệ |
| `outputs/01a0e828-227a-7aa1-9cea-b43d6dc98027/` | 1,9 MB | Phiếu 80 mẫu gửi bác sĩ (giai đoạn thử), tên thư mục là mã ngẫu nhiên |
| `outputs/wireframes/`, `outputs/re_handout_2026-10-02/`, `outputs/re_report_2026-10-02/` | 4,5 MB | Bản phác giao diện và báo cáo RE gửi thầy ngày 02/10, đã lỗi thời |
| `outputs/re_demo_2026-11-21.json`, `outputs/kg_test_*.log`, `outputs/*.log` | < 50 KB | Đã có bản 22/11; log chạy |
| `context.md` | 3 KB | Gần trùng với `PROJECT_CONTEXT.md` |
| `test_run.py`, `run_demo_and_tests.py` | 8 KB | Script chạy thử từ tháng 9 (còn ghi "2.229 mẫu", số cũ), đã được thay bằng `pytest tests` |
| `eval_run.log`, `test_eval_run.log` | — | Đã bị xóa trong thư mục làm việc, chỉ cần commit việc xóa |
| `normalization/logs/*.log`, `logs/*` | 2 MB | Log khi chạy; thư mục `logs/` vốn đã nằm trong `.gitignore` |
| `.pytest_cache/`, các `__pycache__/` | nhỏ | Tự sinh lại, đã nằm trong `.gitignore` |

Các tệp cần bạn tự xem trước khi xóa:

- `KHOA_LUAN_TOT_NGHIEP_NguyenHaiHoang-11236110.docx`, `… (2).docx` (13/11) và `KLTN-NguyenHaiHoang-11236110.docx` (08/11): có thể có phần bạn sửa tay.
- `PROJECT_CONTEXT.md`, `PROJECT_OVERVIEW.md` (tháng 9): lỗi thời, nội dung đã có trong `docs/HUONG_DAN_HE_THONG.md`. Nên xóa hoặc thay bằng một `README.md` ngắn.
- `docs/BAO_CAO_RE_*`, `docs/RE_PLAN_3_WEEKS.md`, `docs/superpowers/`: kế hoạch và báo cáo cũ, chỉ còn giá trị lịch sử.

## 2. Không còn dùng trong báo cáo, nhưng chưa xóa được ngay

Các bộ dữ liệu RE cũ đã bị loại khỏi khóa luận, nhưng `build_report.js` vẫn đọc chúng ở đầu file. Xóa đi thì báo cáo không dựng được nữa.

- `outputs/re_gold_v1_baseline/`, `re_ai_v2/`, `re_ai_baseline/`, `re_baselines/`, `re_benchmark_2026-11-08/`, `vietmed_600_RE_review/`
- `data/golden_test/`, `data/re_test_random_v1/`, `data/re_translated_en_v1/`, `data/re_ai_v2/`
- Các script đã tạo ra chúng: `scripts/golden_test/`, `apply_paper_review.py`, `build_re_review_v2.py`, `prepare_re_review.py`, `check_re_review_roundtrip.py`, `import_physician_review.py`, `re_compare_baselines.py`, `translate_review_labels_vi.py`, `build_six_review_docs.py`, `run_pending_experiments.py`, `demo_e2e.py`, và phần lớn `scripts/re_dataset/` (trừ `bert_re.py`)

Tổng cộng chỉ khoảng 15 MB. Muốn dọn thì phải sửa `build_report.js` bỏ các dòng đọc này rồi dựng lại báo cáo để kiểm tra. **Khuyên để sau khi nộp**, vì làm bây giờ có rủi ro mà lợi ích không đáng kể.

## 3. Trông như thừa nhưng phải giữ

| Mục | Vì sao |
|---|---|
| `re_v3/` | `relation/synth.py` và `relation/validate/import_expert.py` import `re_v3.synth_pattern` và dùng `re_v3/lexicon.json` |
| `scripts/re_dataset/bert_re.py` | `relation/train.py` dùng hàm huấn luyện trong file này |
| `data/external_en_raw/` | `relation/validate/evidence.py` đọc BioText và ADE từ đây |
| `data/re_gold_v1/` | Là "bộ 600 đoạn khảo sát" của phần chuẩn hóa (mục 4.2.1, Phụ lục D) |
| `outputs/kg_test_2026-11-08/`, `kg_test_2026-11-21/` | Mục 4.5 và Hình 4.7 so sánh với hai đồ thị này |
| `outputs/kg_test_2026-11-07/` | Mặc định `--from-results` của `scripts/build_kg.py` vẫn trỏ vào đây |
| `relation/data/synth/validate/rxnav_cache.db` | Cache tra RxNorm, xóa thì phải gọi mạng lại |
| `ICD-10/` | Danh mục ICD-10 Bộ Y tế mà chuẩn hóa đọc vào (bản PDF là văn bản gốc để trích dẫn) |
| `Code/Model/vihealthbert-ner-vietmed-v2-final/`, `vihealthbert-re-vietmed-validated/` | Hai mô hình đang dùng (`Model` là liên kết tới `Code/Model`) |

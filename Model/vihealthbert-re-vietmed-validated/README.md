# ViHealthBERT-RE (dữ liệu sinh đã validate)

Mô hình trích xuất quan hệ mà pipeline, đồ thị tri thức, web và demo đang dùng (`scripts/build_kg.py`, `web/app.py`, `scripts/demo/make_samples.py`). Mô hình chạy đứng một mình (`knowledge_graph.HybridRelationExtractor`, chế độ fallback: bộ luật chỉ dùng cho quan hệ mô hình không hỗ trợ, mà mô hình hỗ trợ cả năm), vì hợp với luật không cải thiện kết quả trên test_v2 (bảng dưới). Thay cho `Model/vihealthbert-re-vietmed` (dữ liệu sinh chưa validate), mô hình cũ vẫn giữ để đối chiếu.

- **Kiến trúc**: `demdecuong/vihealthbert-base-syllable`, thêm 14 token đánh dấu (`[HEAD_<kiểu>]`, `[TAIL_<kiểu>]`, `[/HEAD]`, `[/TAIL]`). Biểu diễn cặp là hai vector tại hai token mở, nối lại, qua dropout và một lớp tuyến tính ra {NO_RELATION, có quan hệ}. Mã: `relation_extraction/bert_model.py`.
- **Quan hệ hỗ trợ**: located_at, treated_by, treated_by_procedure, diagnosed_by, has_dosage.
- **Dữ liệu huấn luyện**: 3.193 cặp = 1.169 cặp của `relation/data/seed.jsonl` (AI gán hai lượt, người chuyên môn duyệt) + 2.024 cặp sinh `relation/data/synth/validated/pool.jsonl`.
  Dữ liệu sinh đã qua bước validate (`relation/validate/`, kế hoạch ở `docs/KE_HOACH_VALIDATE_AUGMENT.md`): kiểm tra cụm từ (VietMed-NER, ICD-10 Bộ Y tế), quan hệ (MED-RT, RxNorm, BioText/ADE, WHO/NIH) và ngữ cảnh câu, rồi chuyên gia duyệt 521 câu (`relation/data/synth/validate/phieu_duyet_chuyen_gia.xlsx`). Số liệu ở `relation/data/synth/validated/manifest.json`.
- **Chọn cấu hình**: macro F1 cao nhất trên tập kiểm định trong x0 / x1 / v1 / vall / x3 (`relation/outputs/evaluation.json`, quy tắc đặt trước). vall đạt 0,853, cao nhất. Tập kiểm định chỉ có 60 câu, 111 cặp, có cặp dương cho 3 / 5 quan hệ.
- **Huấn luyện**: 10 epoch, lr 3e-5, batch 16, warmup 10%, weight decay 0,01, trọng số lớp n_neg/n_pos, độ dài tối đa 192, fp16, ba seed 42/43/44. Xác suất lấy trung bình qua ba seed, ngưỡng 0,5. Siêu tham số đặt trước. Toàn bộ thông số ở `re_config.json`.
- **Kết quả trên tập kiểm tra test_v2** (100 câu, 311 cặp, 106 dương, người chuyên môn gán): xem `relation/outputs/evaluation_test_v2_modes.json` (mô hình nạp lại trên CPU, như pipeline).

  | Cách chạy | Precision | Recall | Micro F1 | KTC 95% | Macro F1 |
  |---|---|---|---|---|---|
  | Mô hình | 0,595 | 0,830 | 0,693 | 0,623–0,755 | 0,632 |
  | Bộ luật | 0,750 | 0,425 | 0,542 | 0,446–0,634 | 0,356 |
  | Mô hình ∪ luật (pipeline) | 0,574 | 0,840 | 0,682 | 0,613–0,747 | 0,618 |
  | Luôn dương (mốc) | 0,341 | 1,000 | 0,508 | 0,441–0,580 | 0,521 |

  Kiểm tra nạp lại: 311 cặp, xác suất lệch tối đa 0,0033 so với lúc huấn luyện, 0 nhãn bị đổi.

  So sánh các cấu hình trên test_v2 (chỉ để báo cáo, không dùng để chọn; `relation/outputs/evaluation_validated_ablation.json`): x0 0,729 · x1 0,702 · v1 0,710 · vall 0,693 · x3 0,709 micro F1. Khoảng tin cậy chồng nhau, không cấu hình nào hơn hẳn.

## Trọng số

Ba file `model_seed42.safetensors`, `model_seed43.safetensors`, `model_seed44.safetensors` (fp16, mỗi file khoảng 270 MB) bị loại khỏi Git bởi `.gitignore`; các file cấu hình và tokenizer được commit. Nếu thiếu trọng số, huấn luyện lại (khoảng 2 giờ trên GTX 1650):

```
.venv-gpu\Scripts\python.exe -X utf8 -m relation.train --configs vall --save-model Model/vihealthbert-re-vietmed-validated
```

Mô hình trước đó vẫn dùng được bằng `--re-model Model/vihealthbert-re-vietmed`.

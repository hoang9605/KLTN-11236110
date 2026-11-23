# ViHealthBERT-RE

Mô hình trích xuất quan hệ mà pipeline, đồ thị tri thức, web và demo đang dùng (`scripts/build_kg.py`, `web/app.py`, `scripts/demo/make_samples.py`). Mô hình luôn chạy kết hợp với bộ luật (`knowledge_graph.HybridRelationExtractor`, chế độ union).

- **Kiến trúc**: `demdecuong/vihealthbert-base-syllable`, thêm 14 token đánh dấu (`[HEAD_<kiểu>]`, `[TAIL_<kiểu>]`, `[/HEAD]`, `[/TAIL]`). Biểu diễn cặp là hai vector tại hai token mở, nối lại, qua dropout và một lớp tuyến tính ra {NO_RELATION, có quan hệ}. Mã: `relation_extraction/bert_model.py`.
- **Quan hệ hỗ trợ**: cả năm quan hệ located_at, treated_by, treated_by_procedure, diagnosed_by, has_dosage.
- **Dữ liệu huấn luyện**: 2.338 cặp, gồm 1.169 cặp của `relation/data/seed.jsonl` (AI gán hai lượt, người chuyên môn duyệt) và 1.169 cặp sinh `relation/data/synth/x1.jsonl` (thay thực thể, mẫu câu dương và mẫu âm khó). Mức dữ liệu sinh này được chọn trên tập kiểm định (`relation/outputs/evaluation.json`).
- **Huấn luyện**: 10 epoch, lr 3e-5, batch 16, warmup 10%, weight decay 0,01, trọng số lớp n_neg/n_pos, độ dài tối đa 192, fp16, ba seed 42/43/44. Xác suất lấy trung bình qua ba seed, ngưỡng 0,5. Siêu tham số đặt trước, không chỉnh trên dev hay test. Toàn bộ thông số ở `re_config.json`.
- **Kết quả trên tập kiểm tra** (100 câu, 311 cặp, người chuyên môn gán; `relation/outputs/evaluation_test_v2_modes.json`):

  | Cách chạy | Precision | Recall | Micro F1 | Khoảng tin cậy 95% |
  |---|---:|---:|---:|---|
  | ViHealthBERT-RE | 0,62 | 0,81 | 0,70 | 0,63–0,77 |
  | Bộ luật | 0,73 | 0,46 | 0,57 | 0,47–0,66 |
  | ViHealthBERT-RE ∪ luật (pipeline) | 0,60 | 0,85 | 0,70 | 0,63–0,77 |
  | Luôn đoán có quan hệ | 0,34 | 1,00 | 0,51 | 0,44–0,58 |

  Mô hình nạp lại trên CPU cho xác suất lệch tối đa 0,004 so với lúc huấn luyện, không đổi nhãn nào.

## Trọng số

Ba file `model_seed42.safetensors`, `model_seed43.safetensors`, `model_seed44.safetensors` (fp16, mỗi file khoảng 270 MB) bị loại khỏi Git bởi `.gitignore`; các file cấu hình và tokenizer được commit. Nếu thiếu trọng số, huấn luyện lại (khoảng 1,6 giờ trên GTX 1650):

```
.venv-gpu\Scripts\python.exe -X utf8 -m relation.train --configs x1 --save-model Model/vihealthbert-re-vietmed
```

Mô hình trước đó vẫn dùng được bằng `--re-model Model/vihealthbert-re-v1`.

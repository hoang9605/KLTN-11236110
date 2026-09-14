# Checkpoint Model: ViHealthBERT NER VietMed v2 Final

Thư mục này chứa cấu hình tokenizer và trọng số mô hình cho bài toán Vietnamese Clinical NER.

## Thông tin mô hình
- **Base model**: `demdecuong/vihealthbert-base-syllable` (PhoBERT-based RoBERTa kiến trúc y tế tiếng Việt).
- **Fine-tuned trên**: `VietMed-NER` (dataset 37 nhãn BIO lâm sàng).
- **Đầu ra ánh xạ**: 6 thực thể mục tiêu (`CONDITION`, `DRUG`, `BODY_PART`, `TEST`, `PROCEDURE`, `DOSAGE`).

## Hướng dẫn tải trọng số mô hình (Weights Download)
Do file trọng số `model.safetensors` có dung lượng **512.86 MB** (vượt giới hạn 100 MB của GitHub standard push), file này được loại trừ khỏi Git repository.

Để chạy pipeline suy luận, hãy thực hiện:
1. Tải checkpoint `model.safetensors` từ kho lưu trữ Google Drive / Hugging Face của nhóm dự án.
2. Đặt file vào đúng đường dẫn sau:
   ```
   Model/vihealthbert-ner-vietmed-v2-final/model.safetensors
   ```
3. Đảm bảo thư mục có đầy đủ các file phụ trợ đã được commit sẵn:
   - `config.json`
   - `tokenizer_config.json`
   - `vocab.txt`
   - `bpe.codes`
   - `added_tokens.json`

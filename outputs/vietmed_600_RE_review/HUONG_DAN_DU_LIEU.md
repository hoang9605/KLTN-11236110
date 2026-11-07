# Phiếu kiểm tra và dữ liệu tương ứng

## Bác sĩ thực hiện

1. Đọc đoạn và kiểm tra bảng NER trước, sau đó kiểm tra bảng RE.
2. Đúng giữ nguyên. Sai bôi đỏ chữ hoặc tô nền đỏ cả dòng; sửa trực tiếp cụm từ/nhãn bằng chữ đỏ hoặc ghi cách sửa ở BỔ SUNG. Không đổi mã mẫu và mã E/R. Nếu bỏ thực thể/quan hệ, ghi XÓA thay vì xóa mất dòng.
3. CHUA_RO: sửa thành nhãn cụ thể nếu xác định được; nếu vẫn thiếu căn cứ thì giữ nguyên, mẫu chưa được đưa vào train RE.
4. Nếu thiếu, ghi ở BỔ SUNG, ví dụ `E4: cụm từ — CONDITION; R3: E4 → E2 — treated_by`. Với cụm từ lặp lại, nêu lần xuất hiện.
5. Khi dừng, thay CHUA_XAC_NHAN ở DA_DUYET_DEN bằng mã mẫu cuối cùng đã đọc liên tục trong file. Điền bác sĩ và ngày duyệt. Không cần đánh dấu từng dòng đúng.

## Cấu trúc và nguồn

- 6 DOCX, mỗi file đúng 100 mẫu, giữ nguyên thứ tự và mã VM600-001 đến VM600-600.
- NER lấy từ 600 dòng train VietMed-NER đã chọn trước, ánh xạ bằng ner/config.py. Không chạy lại mô hình NER, không tự sửa nhãn nguồn.
- annotations_draft.jsonl là bản AI đề xuất, chưa phải gold. Trường source_labels/source_tag_ids giữ nhãn nguồn; labels là BIO đã ánh xạ.
- entities: id, text, label, start/end là vị trí ký tự Python Unicode, end không bao gồm ký tự cuối; token_start/token_end cùng quy ước.
- relations: id, head, tail tham chiếu entities; label, allowed_relation, evidence và rationale. NO_RELATION chỉ nói không có quan hệ thuộc 5 loại trong đoạn giữa cặp này, không phủ nhận mọi liên hệ y học. CHUA_RO là trạng thái tạm, không phải lớp mô hình.
- Mã E/R có phạm vi trong mỗi mẫu. Khóa toàn cục là sample_id + entity_id hoặc sample_id + relation_id.
- Chỉ sinh cặp theo hướng và kiểu thực thể trong re_labels.json. Các mẫu không có cặp có relations rỗng; không tự tạo negative giả. Nếu bác sĩ sửa NER thì phải xét lại cặp RE.
- Đánh nhãn theo văn bản gốc, không xác nhận tính đúng y khoa của phát biểu trong nguồn. Quan hệ phòng ngừa, nguyên nhân, tác dụng phụ không được đổi thành điều trị.
- Chính sách thận trọng: không truyền vị trí hoặc phương pháp sang các lần nhắc khác chỉ vì cùng loại; trường hợp câu hỏi, phủ định, câu bị cắt hoặc NER chưa chắc được giữ CHUA_RO khi không thể kết luận.

## Đọc lại file đã duyệt

Giữ file gốc, lưu bản bác sĩ sửa thành file khác. Nếu dùng Google Docs, tải lại DOCX để giữ chữ/nền đỏ. Chạy scripts/import_physician_review.py với Python có python-docx:

```text
python scripts/import_physician_review.py --original outputs/vietmed_600_RE_review/Phieu_RE_01_001_100.docx --reviewed FILE_BAC_SI_SUA.docx --draft outputs/vietmed_600_RE_review/annotations_draft.jsonl --out outputs/review_import_01
```

- reviewed_ready.jsonl: chỉ các mẫu xác nhận đã đọc, không sửa, không bôi đỏ, không CHUA_RO. Giữ nhãn positive trong relations và cặp âm trong negative_pairs.
- pending_adjudication.jsonl: các đoạn sửa/bôi đỏ, chưa đọc hoặc còn CHUA_RO. Có nội dung gốc và nội dung sửa để đối chiếu. Dòng màu đỏ không tự động biến thành NO_RELATION.
- Sửa NER cần cập nhật span, BIO và toàn bộ cặp RE liên quan. Các chỉnh sửa được giữ chờ đối chiếu thay vì đoán ý của bác sĩ. Sau đối chiếu mới xuất thành mẫu train.
- Công cụ không tự giải quyết comment hoặc Track Changes; có các mục này thì giữ chờ đối chiếu.
- Sau khi chốt, tách train/dev/test theo nhóm hội thoại nếu xác minh được nhóm và kiểm tra trùng nội dung. Đây là mẫu từ train nguồn, không phải tập kiểm tra độc lập cho mô hình NER đã học cùng nguồn.

## Giới hạn bản hiện tại

Đây là 600 mẫu ngẫu nhiên, không cân bằng theo quan hệ. Không có positive chắc chắn cho diagnosed_by và has_dosage trong bản đề xuất hiện tại. Không bổ sung nhãn dương bằng suy đoán để đủ lớp. Cần xem kết quả bác sĩ duyệt trước khi quyết định bổ sung mẫu cho các lớp thiếu.

# RE thử nghiệm với nhãn AI

Người dùng đã chọn dùng nhãn AI ngày 16/10/2026. Nguồn: bản rà soát 600 mẫu ngày 15/10. Không thay đổi dữ liệu nguồn hoặc cờ human_verified/training_eligible.

## Thiết kế thực thi

Module riêng `relation_extraction`, sử dụng schema `re_labels.json`. Chỉ dùng cặp có nhãn rõ ràng đã ghi trong dữ liệu; bỏ CHUA_RO, không tự sinh nhãn âm. Cho phép bản AI bằng lựa chọn tường minh; lưu review_flags và hash nguồn. Các cặp có quyết định rõ trong mẫu còn cờ được dùng cho thí nghiệm và được thống kê riêng.

TF-IDF ký tự trên câu có marker head/tail và Logistic Regression cân bằng lớp là mô hình thử nghiệm nhẹ. Không huấn luyện lại NER. Đây chưa phải mô hình ViHealthBERT RE trong đề xuất nghiên cứu cũ. Chia nhóm theo văn bản chuẩn hóa, giữ tất cả cặp cùng nhóm ở một tập. Nhóm hiếm được đưa vào train để có lớp học; tập giữ lại không bảo đảm đủ nhãn. Không dùng test chọn mô hình/ngưỡng.

Suy luận chỉ xét đúng chiều/kiểu trong schema, chặn lớp không có positive ở train bằng trạng thái unsupported. Có wrapper nhận output NER hiện có và CLI train/predict. Báo cáo P/R/F1 thử nghiệm trên nhãn AI (không phải kết quả gold hoặc metric nghiên cứu đã chốt), support và các lớp thiếu. Nguồn VietMed train không là test độc lập cho NER.

## Các bước và kiểm tra

- [x] Test dữ liệu: yêu cầu opt-in AI, loại CHUA_RO, không sinh âm, sai offset/chiều/ID phải lỗi.
- [x] Test chia nhóm: câu trùng không rò qua split; lặp lại cùng seed ra cùng kết quả.
- [x] Test model: marker giữ đúng chiều kể cả head đứng sau, save/load giữ dự đoán, lớp thiếu trả unsupported.
- [x] Test metric bằng cặp đếm tay, wrapper dùng văn bản/offset mà NER trả về.
- [x] Implement loader, split, model, wrapper, CLI và tài liệu sử dụng.
- [x] Chạy test, huấn luyện thật, lưu checkpoint/split/report/predictions, chạy CLI dự đoán.

Hoàn tất khi các test trọng yếu qua và có checkpoint thực sự học từ dữ liệu AI cùng kết quả tái lập. Không tuyên bố chất lượng đủ năm quan hệ hay đã fine-tune encoder.

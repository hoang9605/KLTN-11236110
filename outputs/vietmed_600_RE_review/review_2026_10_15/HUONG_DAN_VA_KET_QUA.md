# Bộ nhãn VietMed 600 sau rà soát lần hai

Ngày 15/10/2026, đã đọc và đối chiếu đủ 600 mẫu của sáu phiếu được cung cấp. Bản này sửa nhãn và lưu lịch sử để người duyệt có thể truy ngược từng thay đổi. Đây là bản AI rà soát, chưa phải dữ liệu gold được bác sĩ xác nhận.

## Kết quả

- 306 mẫu có thay đổi NER hoặc RE.
- NER từ 1158 xuống 894 thực thể. Nhật ký có 331 thao tác xóa, 67 bổ sung và 143 sửa. Một thực thể có thể được sửa qua nhiều bước; số thao tác không phải số thực thể duy nhất.
- 317 mẫu chưa phát hiện điểm cần phân xử trong lượt AI này; 283 mẫu cần chốt ngữ cảnh hoặc quy ước.
- RE còn 20 located_at, 19 treated_by_procedure, 2 treated_by, 137 NO_RELATION và 62 CHUA_RO. Chưa có quan hệ dương diagnosed_by hoặc has_dosage đủ căn cứ để chốt trong bản này.
- Các con số là thống kê chỉnh sửa, không phải độ chính xác đo trên tập gold.

## Quy tắc đã chốt với người dùng

Giữ nguyên toàn bộ cụm bệnh/triệu chứng trong một CONDITION. Ví dụ “đau khớp”, “viêm loét dạ dày”, “thiếu máu cơ tim” là một thực thể; không đánh dấu thêm BODY_PART lồng trong đó và không tạo located_at nội bộ. Nếu vị trí được diễn đạt riêng bằng “ở”, “trong” hoặc một mệnh đề khác, vẫn xét quan hệ theo văn bản. Không tự sửa lỗi phiên âm của câu nguồn.

Giữ sáu loại NER và năm quan hệ dự án. Tác nhân như vi khuẩn/virus không tự trở thành bệnh; “nhiễm virus” là tình trạng bệnh. Số thứ tự, tỷ lệ, mức độ và lượng thực phẩm không phải liều thuốc. Đồng xuất hiện, phòng ngừa và gây tác dụng phụ không chứng minh quan hệ điều trị. Câu thiếu ngữ cảnh giữ CHUA_RO hoặc đưa cả mẫu vào hàng chờ; không mặc nhiên xuất thành mẫu âm.

## Các tệp

- `annotations_reviewed_600.jsonl`: toàn bộ 600 mẫu sau rà soát, gồm NER, BIO, tất cả cặp ứng viên RE và lý do cần chốt.
- `resolved_provisional.jsonl`: 317 mẫu chưa còn cờ phân xử trong lượt AI; không đồng nghĩa được bác sĩ duyệt.
- `needs_adjudication.jsonl`: 283 mẫu cần phân xử.
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

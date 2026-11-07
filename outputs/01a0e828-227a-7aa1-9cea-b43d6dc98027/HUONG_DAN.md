# Bộ pilot VietMed-NER: 80 mẫu để bác sĩ kiểm duyệt

Nguồn: https://huggingface.co/datasets/leduckhai/VietMed-NER. Chỉ dùng tập train, 4.616 hàng trong bản cache đang có. Ngày chuẩn bị: 29/09/2026.

## Bắt đầu

1. Mở `VietMed_80_mau_bac_si.xlsx`, đọc trang `Huong_dan`.
2. Làm thử VM001–VM010 trước. Chốt cách xử lý ca phủ định, câu hỏi, thông tin thuốc/liều và chẩn đoán.
3. Ở `Thuc_the`, lọc mã mẫu. Chọn Giữ / Sửa / Xóa / Chưa rõ cho từng thực thể. Với Sửa, điền cả cụm đúng và loại đúng. Nếu cụm lặp, ghi lần xuất hiện cần sửa.
4. Ở `Quan_he`, lọc cùng mã mẫu. Chọn Có / Không / Chưa rõ / Cặp không còn hợp lệ. Cột quan hệ cần xét chỉ là câu hỏi, không phải đáp án.
5. Thêm thực thể/quan hệ bỏ sót tại `Bo_sung`. Không sửa văn bản gốc hoặc mã định danh. Nhắc rõ lần xuất hiện khi hai cụm giống nhau.
6. Ở `Van_ban`, ghi người duyệt, ghi chú và trạng thái. Nếu còn mục mơ hồ, chọn Cần xem lại.
7. Lưu file Excel đã điền và gửi lại cho người chuẩn bị dữ liệu. Chưa đổi JSONL thành gold hoặc tự đưa vào huấn luyện.

## Quy tắc cần bác sĩ thống nhất

- Chỉ gán quan hệ được thể hiện trong đoạn. Không bổ sung bằng kiến thức ngoài đoạn.
- Câu bị cụt, phủ định hoặc giả định chưa có quy tắc thống nhất: chọn Chưa rõ, ghi lý do. Không ghép hàng liền kề vì thứ tự file chưa xác minh là thứ tự hội thoại.
- Nhãn NER gốc có thể cần sửa. UNITCALIBRATOR không luôn là liều thuốc; MEDDEVICETECHNIQUE không luôn có vai trò điều trị.
- `has_dosage` đang dùng cho thông tin liều thuốc của schema hiện tại; cần bác sĩ chốt cách xử lý hàm lượng, lượng dùng, tần suất. Không coi số đo xét nghiệm là liều thuốc.
- Blank = chưa kiểm tra. Không = đã xác nhận không có quan hệ được hỏi. Chưa rõ = chưa đủ căn cứ. Cặp không còn hợp lệ = thực thể đã sửa/xóa nên cặp gốc không còn dùng được.
- Một thực thể có thể có nhiều quan hệ. Mỗi lần xuất hiện có một ID riêng. Không tự gộp hai mention cùng tên.
- Nếu bác sĩ thêm/sửa/xóa thực thể, cần cập nhật và rà lại toàn bộ cặp liên quan trước khi đóng bản gold.

## Quy mô và cách lấy mẫu

- 80 đoạn nguyên văn; 247 thực thể theo mapping hiện tại; 180 cặp ứng viên chưa có nhãn.
- 11 mẫu đã trao đổi, 24 mẫu ngẫu nhiên có giới hạn độ dài, 45 mẫu ưu tiên kiểu cặp (9 mẫu bổ sung/kiểu). Seed 20260929.
- 21 đoạn chưa có cặp ứng viên từ nhãn hiện tại; vẫn cần kiểm tra thực thể/quan hệ bỏ sót.
- Số cặp theo loại: {"located_at": 51, "treated_by": 40, "treated_by_procedure": 44, "diagnosed_by": 22, "has_dosage": 23}. Đây không phải số quan hệ dương.
- Bộ này phục vụ pilot và chỉnh guideline, không phải test độc lập hoặc mẫu đại diện phân bố tự nhiên.
- Chưa xác minh conversation ID. Không dùng 80 mẫu này để tạo train/dev/test bằng cách chia ngẫu nhiên các cặp.

## File và đối chiếu sau khi bác sĩ trả

- XLSX: phiếu chính, các ô nhập liệu màu vàng nhạt và có tên cột rõ ràng.
- JSONL: text, words, BIO labels, tag IDs, entities và candidate pairs gốc; nhãn quan hệ để null, không có đáp án tự sinh.
- manifest.json: nguồn, hash file nguồn, seed, hàng đã chọn và thống kê.

Trước khi đưa vào train: đối chiếu mã mẫu/ID, áp dụng sửa thực thể mà giữ bản gốc, căn lại offset bằng text không đổi, xử lý cụm lặp, sinh lại cặp, kiểm tra kiểu/chiều, giải quyết Chưa rõ và chỉ nhận mẫu được kiểm duyệt đầy đủ. Không tự gán âm cho cặp bỏ trống hoặc cặp mới sinh sau chỉnh sửa. Workbook chỉ là phiếu nhập liệu, chưa có chức năng tự chuyển các sửa đổi thành gold.

Mã hàng nguồn bắt đầu từ 0. Văn bản giữ nguyên, không sửa chính tả, thêm ngữ cảnh hoặc tạo câu tổng hợp. Bác sĩ kiểm duyệt bằng chứng văn bản; ghi riêng bất đồng chuyên môn về nội dung. Kiểm tra điều kiện sử dụng nguồn trước khi phát hành lại corpus.

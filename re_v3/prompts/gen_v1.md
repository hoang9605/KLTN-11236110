Bạn tạo dữ liệu huấn luyện cho bài toán trích xuất quan hệ y khoa tiếng Việt.

Dữ liệu gốc là bộ VietMed: bản ghi lời nói trong các chương trình tư vấn sức khỏe, cắt thành đoạn khoảng hai mươi đến ba mươi từ. Văn phong: chữ thường, không dấu câu, số viết bằng chữ, nhiều từ đệm ("thì", "là", "cái", "mà", "á", "nha", "ạ"), đoạn có thể bị cắt ngang ở đầu hoặc cuối.

NHIỆM VỤ
Viết lại MỘT câu gốc thành một câu mới sao cho cặp thực thể đích mang đúng nhãn được yêu cầu, theo đúng kiểu mẫu được yêu cầu.

QUY TẮC BẮT BUỘC
1. Hai thực thể đích giữ nguyên chữ, nguyên id, nguyên kiểu, bọc trong thẻ như câu gốc, ví dụ [E1:CONDITION]đau đầu[/E1].
2. Các thực thể khác của câu gốc: hoặc giữ nguyên thẻ và chữ, hoặc bỏ hẳn khỏi câu. KHÔNG thêm tên bệnh, triệu chứng, thuốc, bộ phận, xét nghiệm, thủ thuật hay liều lượng nào mới ngoài các thực thể đã có thẻ. Được dùng từ chung như "thuốc", "bệnh", "cái này".
3. Văn phong VietMed: chữ thường, không dấu câu, không chữ số (số viết bằng chữ), từ mười lăm đến ba mươi lăm từ, giữ giọng nói của câu gốc. Không viết như sách hay báo.
4. Câu mới phải khác câu gốc. Giữ chủ đề của câu gốc, chỉ đổi những gì cần để cặp đích mang đúng nhãn.
5. Nhãn của cặp đích phải đúng theo LUẬT GÁN NHÃN bên dưới (luật quyết định, không phải trực giác). Nội dung câu vẫn phải hợp lý như lời một người thật nói về sức khỏe, không bịa điều vô lý về y khoa.
6. Nếu không làm được mà vẫn giữ các quy tắc trên (thực thể đích không phải thực thể y khoa thật, quá chung chung, sai kiểu, hoặc kiểu mẫu không hợp với hai thực thể này), trả về skip = true và ghi lý do. Bỏ qua tốt hơn là sinh câu sai.

LUẬT GÁN NHÃN CHUNG
$general_rules

LUẬT CỦA QUAN HỆ ĐÍCH
$relation_rules

KIỂU MẪU YÊU CẦU: $variant_code
$variant_desc
Ví dụ minh họa kiểu mẫu (chỉ để hiểu ý, không chép): "$variant_example"

ĐẦU RA
Chỉ trả về một đối tượng JSON, không kèm chữ nào khác:
{"skip": false, "skip_reason": "", "tagged": "<câu mới có thẻ>", "evidence": "<cụm từ trong câu mới quyết định nhãn của cặp đích>"}
=== USER ===
Câu gốc: $seed_tagged

Cặp đích: [$head_id] "$head_text" ($head_type) → [$tail_id] "$tail_text" ($tail_type)
Quan hệ đang xét: $relation
Nhãn yêu cầu cho cặp đích: $target_label
Kiểu mẫu: $variant_code
Người nói: $speaker

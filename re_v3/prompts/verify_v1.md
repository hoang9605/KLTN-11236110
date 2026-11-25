Bạn là người gán nhãn quan hệ y khoa tiếng Việt, làm việc theo hướng dẫn gán nhãn đã khóa.

Câu là bản ghi lời nói VietMed: chữ thường, không dấu câu, có thể bị cắt ngang. Thực thể đã được đánh dấu bằng thẻ [E1:KIỂU]…[/E1]. Không sửa ranh giới thực thể.

Làm hai bước.

BƯỚC A: KIỂM TRA THỰC THỂ
Với mỗi thực thể có thẻ, chọn VALID (đúng kiểu) hoặc INVALID (sai kiểu, quá chung chung, hoặc không phải thực thể y khoa). Ranh giới lệch một chút nhưng phần chính đúng kiểu thì vẫn VALID.
$entity_rules

BƯỚC B: GÁN QUAN HỆ CHO TỪNG CẶP
Mỗi cặp trong danh sách có chiều cố định head → tail và chỉ có một quan hệ có thể có. Gán đúng tên quan hệ đó nếu câu khẳng định quan hệ, ngược lại gán NO_RELATION. Cặp có thực thể INVALID vẫn phải ghi nhãn NO_RELATION.

Luật chung:
$general_rules

Luật từng quan hệ:
$relation_rules

ĐẦU RA
Chỉ trả về một đối tượng JSON, không kèm chữ nào khác:
{"entities": [{"id": "E1", "validity": "VALID", "reason": "<ngắn>"}],
 "pairs": [{"pair_id": "R1", "label": "<tên quan hệ hoặc NO_RELATION>", "evidence": "<cụm từ làm bằng chứng, rỗng nếu NO_RELATION>", "reason": "<ngắn>"}]}
Phải có đủ mọi thực thể và mọi cặp trong danh sách.
=== USER ===
Câu: $tagged

Các cặp cần gán:
$pair_list

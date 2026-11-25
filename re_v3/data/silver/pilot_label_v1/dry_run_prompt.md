## system

Bạn là người gán nhãn quan hệ y khoa tiếng Việt, làm việc theo hướng dẫn gán nhãn đã khóa.

Câu là bản ghi lời nói VietMed: chữ thường, không dấu câu, có thể bị cắt ngang. Thực thể đã được đánh dấu bằng thẻ [E1:KIỂU]…[/E1]. Không sửa ranh giới thực thể.

Làm hai bước.

BƯỚC A: KIỂM TRA THỰC THỂ
Với mỗi thực thể có thẻ, chọn VALID (đúng kiểu) hoặc INVALID (sai kiểu, quá chung chung, hoặc không phải thực thể y khoa). Ranh giới lệch một chút nhưng phần chính đúng kiểu thì vẫn VALID.
- CONDITION: bệnh, triệu chứng, tổn thương, tình trạng bất thường. INVALID: tên chung chung (bệnh lý, triệu chứng, biến chứng); tác nhân (vi khuẩn, virus); trạng thái bình thường (có thai, có kinh); từ không phải bệnh (chậm, tử vong, di truyền). "huyết áp" VALID khi là bệnh tăng huyết áp ("bị huyết áp", "thuốc huyết áp"), INVALID khi là chỉ số đo.
- DRUG: thuốc, hoạt chất, vắc xin, kháng sinh, thực phẩm chức năng, thảo dược, vitamin, mỹ phẩm điều trị. INVALID: động từ (kiểm soát, chỉ định, phòng ngừa); chất trong cơ thể (melanin, cortisol, sữa mẹ); dinh dưỡng chung (chất béo, protein).
- PROCEDURE: thủ thuật, phương pháp điều trị cụ thể (phẫu thuật, mổ, hóa trị, xạ trị, nội soi, vật lý trị liệu). INVALID: động từ chung (cải thiện, hỗ trợ, chăm sóc); hành động dùng thuốc (uống thuốc, tiêm); đồ vật; chữ "điều trị" đứng một mình.
- TEST: xét nghiệm, chẩn đoán hình ảnh, thăm khám (siêu âm, MRI, CT, X-quang, điện tâm đồ, "kiểm tra" khi là khám bệnh). INVALID: nghiên cứu khoa học; quá trình sinh lý (chuyển hóa, tuần hoàn).
- BODY_PART: cơ quan, bộ phận, mô, dịch cơ thể (não, tim, da, khớp, máu, thắt lưng). INVALID: quá chung (cơ thể, hệ, tế bào); không phải bộ phận (gen, dna, sắc tố).
- DOSAGE: liều, lượng, hàm lượng, tần suất của thuốc khi dùng ("một viên", "hai mũi", "năm mươi mg", "ngày hai lần"). INVALID: tính từ (cao, thấp, rất nhiều); thứ tự (thứ nhất); thống kê (tỷ lệ, phần trăm bệnh nhân); chỉ số cơ thể (nhịp tim, đường huyết).

BƯỚC B: GÁN QUAN HỆ CHO TỪNG CẶP
Mỗi cặp trong danh sách có chiều cố định head → tail và chỉ có một quan hệ có thể có. Gán đúng tên quan hệ đó nếu câu khẳng định quan hệ, ngược lại gán NO_RELATION. Cặp có thực thể INVALID vẫn phải ghi nhãn NO_RELATION.

Luật chung:
- Chỉ gán điều mà câu nói ra, không gán điều đúng về y học. Chỉ dùng chính câu đó, không suy từ ngữ cảnh ngoài câu.
- Quan hệ phải nối đúng hai mention đang xét, không phải mention khác cùng tên ở chỗ khác trong câu.
- Mỗi cặp có đúng một nhãn: tên quan hệ hoặc NO_RELATION. Không đủ thông tin để khẳng định thì NO_RELATION.
- Câu bị cắt mất phần nối hai thực thể: dương nếu phần còn lại đủ rõ, nếu không thì NO_RELATION.
- Nói về động vật hay thí nghiệm: NO_RELATION, trừ khi câu nói rõ đó là điều trị hay chẩn đoán.

Luật từng quan hệ:
located_at (CONDITION → BODY_PART): bệnh hoặc triệu chứng xảy ra ở bộ phận đó.
- Dương: "đau thắt lưng", "viêm loét ở cái miệng nối", "cục máu đông ở trong tim", "tê bì chân tay", "thiếu máu cơ tim".
- Phủ định vẫn là dương: "không bị đau khớp gối" → đau → khớp gối là located_at.
- Âm: bộ phận chỉ được nhắc cùng câu mà không phải chỗ bệnh xảy ra ("rung nhĩ gây biến chứng ở não": rung nhĩ → não âm).
- Liệt kê nhiều triệu chứng trước một bộ phận: chỉ triệu chứng đứng sát bộ phận là dương ("chóng mặt tê bì chân tay": chóng mặt → chân tay âm), trừ khi câu nói rõ cả cụm cùng ở bộ phận đó.

ĐẦU RA
Chỉ trả về một đối tượng JSON, không kèm chữ nào khác:
{"entities": [{"id": "E1", "validity": "VALID", "reason": "<ngắn>"}],
 "pairs": [{"pair_id": "R1", "label": "<tên quan hệ hoặc NO_RELATION>", "evidence": "<cụm từ làm bằng chứng, rỗng nếu NO_RELATION>", "reason": "<ngắn>"}]}
Phải có đủ mọi thực thể và mọi cặp trong danh sách.

## user

Câu: [E1:BODY_PART]tử cung[/E1] phần phụ là hoàn toàn bình thường không có bệnh lý gì cả nhưng mà chỉ do do [E2:CONDITION]rối loạn[/E2] về chức năng của

Các cặp cần gán:
R1: [E2] "rối loạn" → [E1] "tử cung" | quan hệ có thể: located_at

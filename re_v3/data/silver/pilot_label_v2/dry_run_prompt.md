## system

Bạn là người gán nhãn quan hệ y khoa tiếng Việt, làm việc theo hướng dẫn gán nhãn đã khóa.

Câu là bản ghi lời nói VietMed: chữ thường, không dấu câu, có thể bị cắt ngang. Thực thể đã được đánh dấu bằng thẻ [E1:KIỂU]…[/E1]. Không sửa ranh giới thực thể.

Làm hai bước.

BƯỚC A: KIỂM TRA THỰC THỂ
Với mỗi thực thể có thẻ, chọn VALID (đúng kiểu) hoặc INVALID (sai kiểu, quá chung chung, hoặc không phải thực thể y khoa). Ranh giới lệch một chút nhưng phần chính đúng kiểu thì vẫn VALID.
- CONDITION: bệnh, triệu chứng, tổn thương, tình trạng bất thường. INVALID: tên chung chung (bệnh lý, triệu chứng, biến chứng); tác nhân (vi khuẩn, virus); trạng thái bình thường (có thai, có kinh); từ không phải bệnh (chậm, tử vong, di truyền). "huyết áp" VALID khi là bệnh tăng huyết áp ("bị huyết áp", "thuốc huyết áp"), INVALID khi là chỉ số đo.
- DRUG: thuốc, hoạt chất, vắc xin, kháng sinh, thực phẩm chức năng, thảo dược, vitamin, mỹ phẩm điều trị. INVALID: động từ (kiểm soát, chỉ định, phòng ngừa); chất trong cơ thể (melanin, cortisol, sữa mẹ); dinh dưỡng chung (chất béo, protein).
- PROCEDURE: thủ thuật, phương pháp điều trị cụ thể (phẫu thuật, mổ, hóa trị, xạ trị, nội soi, vật lý trị liệu). INVALID: động từ chung (cải thiện, hỗ trợ, chăm sóc); hành động dùng thuốc (uống thuốc, tiêm); đồ vật; chữ "điều trị" đứng một mình; hành động chăm sóc chung không phải phương pháp điều trị (cấp cứu, vào viện, nhập viện, khám, theo dõi, hồi sức).
- TEST: xét nghiệm, chẩn đoán hình ảnh, thăm khám (siêu âm, MRI, CT, X-quang, điện tâm đồ, "kiểm tra" khi là khám bệnh). INVALID: nghiên cứu khoa học; quá trình sinh lý (chuyển hóa, tuần hoàn).
- BODY_PART: cơ quan, bộ phận, mô, dịch cơ thể (não, tim, da, khớp, máu, thắt lưng). INVALID: quá chung (cơ thể, hệ, tế bào); không phải bộ phận (gen, dna, sắc tố).
- DOSAGE: liều, lượng, hàm lượng, tần suất của thuốc khi dùng ("một viên", "hai mũi", "năm mươi mg", "ngày hai lần"). INVALID: tính từ (cao, thấp, rất nhiều); thứ tự (thứ nhất); thống kê (tỷ lệ, phần trăm bệnh nhân); chỉ số cơ thể (nhịp tim, đường huyết).
- MẢNH TỪ: thực thể chỉ là một phần của một từ hay thuật ngữ khác thì INVALID, dù chữ đó tự nó là tên bộ phận hay bệnh. Ví dụ: "cơ" trong "cơ tim", "máu" trong "nhồi máu"/"mỡ máu"/"đông máu", "huyết" trong "huyết khối", "mô" trong "mô hình", "lao" trong "lao động", "ruột" trong "ruột kích thích" khi là tên hội chứng. Ngoại lệ: thực thể là bộ phận đầy đủ đứng cuối tên bệnh ("tim" trong "thiếu máu cơ tim") vẫn VALID.

BƯỚC B: GÁN QUAN HỆ CHO TỪNG CẶP
Mỗi cặp trong danh sách có chiều cố định head → tail và chỉ có một quan hệ có thể có. Gán đúng tên quan hệ đó nếu câu khẳng định quan hệ, ngược lại gán NO_RELATION. Cặp có thực thể INVALID vẫn phải ghi nhãn NO_RELATION.

Luật chung:
- Hai thực thể phải cùng nằm trong câu. Gán dương khi câu nói đến quan hệ, HOẶC khi câu đặt hai thực thể vào cùng một ý (cùng mệnh đề, cùng chủ đề đang bàn) và quan hệ đó đúng theo kiến thức y khoa chuẩn. Không gán dương chỉ vì hai thực thể cùng xuất hiện trong một danh sách liệt kê các thứ khác nhau.
- Quan hệ phải nối đúng hai mention đang xét, không phải mention khác cùng tên ở chỗ khác trong câu.
- Mỗi cặp có đúng một nhãn: tên quan hệ hoặc NO_RELATION.
- Câu bị cắt mất phần nối hai thực thể: dương nếu phần còn lại đủ rõ, nếu không thì NO_RELATION.
- Nói về động vật hay thí nghiệm: NO_RELATION, trừ khi câu nói rõ đó là điều trị hay chẩn đoán.

Luật từng quan hệ:
located_at (CONDITION → BODY_PART): bệnh hoặc triệu chứng xảy ra ở bộ phận đó.
- Dương khi câu nói rõ vị trí: "đau thắt lưng", "hoại tử ở vùng chi", "cục máu đông ở trong tim", "tê bì chân tay".
- Dương khi bộ phận nằm trong tên bệnh hoặc là cơ quan bị bệnh theo kiến thức y khoa, và câu đang nói về bệnh đó ở bộ phận đó: "thiếu máu cơ tim" → thiếu máu → tim; "rung nhĩ ... tim" → tim; "cục máu đông tắc mạch máu não" → não; "chảy máu ... nhu mô não" → nhu mô não; "hội chứng ruột kích thích ... đại tràng" → đại tràng; "táo bón ... đại tràng", "tiêu chảy ... ruột"; "tiêu xương ... xương hàm"; "covid ... đau rát họng" → họng.
- Phủ định vẫn là dương: "không bị đau khớp gối" → đau → khớp gối là located_at.
- Âm: bộ phận là chỗ của bệnh KHÁC, hoặc là chỗ bệnh gây biến chứng tới ("rung nhĩ gây nhồi máu não": rung nhĩ → não âm; "loạn nhịp tim ... nhồi máu não": loạn nhịp tim → não âm).
- Âm: liệt kê các triệu chứng khác nhau rồi mới đến bộ phận; chỉ triệu chứng đứng sát bộ phận là dương ("đau đầu chóng mặt mất ngủ tê bì chân tay": tê bì → chân tay dương, đau đầu/chóng mặt/mất ngủ → chân tay âm).
- Âm: bộ phận không liên quan về y khoa với bệnh đó (đau đầu → động mạch, huyết áp → khớp).

ĐẦU RA
Chỉ trả về một đối tượng JSON, không kèm chữ nào khác:
{"entities": [{"id": "E1", "validity": "VALID", "reason": "<ngắn>"}],
 "pairs": [{"pair_id": "R1", "label": "<tên quan hệ hoặc NO_RELATION>", "evidence": "<cụm từ làm bằng chứng, rỗng nếu NO_RELATION>", "reason": "<ngắn>"}]}
Phải có đủ mọi thực thể và mọi cặp trong danh sách.

## user

Câu: [E1:BODY_PART]tử cung[/E1] phần phụ là hoàn toàn bình thường không có bệnh lý gì cả nhưng mà chỉ do do [E2:CONDITION]rối loạn[/E2] về chức năng của

Các cặp cần gán:
R1: [E2] "rối loạn" → [E1] "tử cung" | quan hệ có thể: located_at

# located_at-POS-0000 (POS_EXPLICIT, nhãn located_at)

## system

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
- Chỉ gán điều mà câu nói ra, không gán điều đúng về y học. Chỉ dùng chính câu đó, không suy từ ngữ cảnh ngoài câu.
- Quan hệ phải nối đúng hai mention đang xét, không phải mention khác cùng tên ở chỗ khác trong câu.
- Mỗi cặp có đúng một nhãn: tên quan hệ hoặc NO_RELATION. Không đủ thông tin để khẳng định thì NO_RELATION.
- Câu bị cắt mất phần nối hai thực thể: dương nếu phần còn lại đủ rõ, nếu không thì NO_RELATION.
- Nói về động vật hay thí nghiệm: NO_RELATION, trừ khi câu nói rõ đó là điều trị hay chẩn đoán.

LUẬT CỦA QUAN HỆ ĐÍCH
located_at (CONDITION → BODY_PART): bệnh hoặc triệu chứng xảy ra ở bộ phận đó.
- Dương: "đau thắt lưng", "viêm loét ở cái miệng nối", "cục máu đông ở trong tim", "tê bì chân tay", "thiếu máu cơ tim".
- Phủ định vẫn là dương: "không bị đau khớp gối" → đau → khớp gối là located_at.
- Âm: bộ phận chỉ được nhắc cùng câu mà không phải chỗ bệnh xảy ra ("rung nhĩ gây biến chứng ở não": rung nhĩ → não âm).
- Liệt kê nhiều triệu chứng trước một bộ phận: chỉ triệu chứng đứng sát bộ phận là dương ("chóng mặt tê bì chân tay": chóng mặt → chân tay âm), trừ khi câu nói rõ cả cụm cùng ở bộ phận đó.

KIỂU MẪU YÊU CẦU: POS_EXPLICIT
bệnh hoặc triệu chứng xảy ra ở bộ phận, có từ nối rõ (ở, tại, vùng, bên)
Ví dụ minh họa kiểu mẫu (chỉ để hiểu ý, không chép): "bị viêm loét ở cái vùng dạ dày"

ĐẦU RA
Chỉ trả về một đối tượng JSON, không kèm chữ nào khác:
{"skip": false, "skip_reason": "", "tagged": "<câu mới có thẻ>", "evidence": "<cụm từ trong câu mới quyết định nhãn của cặp đích>"}

## user

Câu gốc: như số [E1:CONDITION]đau[/E1] rát [E2:BODY_PART]họng[/E2] tìm đến thăm khám và [E3:TEST]test[/E3] nhanh phát hiện nhiễm [E4:CONDITION]covid19[/E4]

Cặp đích: [E1] "đau" (CONDITION) → [E2] "họng" (BODY_PART)
Quan hệ đang xét: located_at
Nhãn yêu cầu cho cặp đích: located_at
Kiểu mẫu: POS_EXPLICIT
Người nói: người nhà hỏi bác sĩ

---

# located_at-NEG-0000 (NEG_OTHER_SITE, nhãn NO_RELATION)

## system

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
- Chỉ gán điều mà câu nói ra, không gán điều đúng về y học. Chỉ dùng chính câu đó, không suy từ ngữ cảnh ngoài câu.
- Quan hệ phải nối đúng hai mention đang xét, không phải mention khác cùng tên ở chỗ khác trong câu.
- Mỗi cặp có đúng một nhãn: tên quan hệ hoặc NO_RELATION. Không đủ thông tin để khẳng định thì NO_RELATION.
- Câu bị cắt mất phần nối hai thực thể: dương nếu phần còn lại đủ rõ, nếu không thì NO_RELATION.
- Nói về động vật hay thí nghiệm: NO_RELATION, trừ khi câu nói rõ đó là điều trị hay chẩn đoán.

LUẬT CỦA QUAN HỆ ĐÍCH
located_at (CONDITION → BODY_PART): bệnh hoặc triệu chứng xảy ra ở bộ phận đó.
- Dương: "đau thắt lưng", "viêm loét ở cái miệng nối", "cục máu đông ở trong tim", "tê bì chân tay", "thiếu máu cơ tim".
- Phủ định vẫn là dương: "không bị đau khớp gối" → đau → khớp gối là located_at.
- Âm: bộ phận chỉ được nhắc cùng câu mà không phải chỗ bệnh xảy ra ("rung nhĩ gây biến chứng ở não": rung nhĩ → não âm).
- Liệt kê nhiều triệu chứng trước một bộ phận: chỉ triệu chứng đứng sát bộ phận là dương ("chóng mặt tê bì chân tay": chóng mặt → chân tay âm), trừ khi câu nói rõ cả cụm cùng ở bộ phận đó.

KIỂU MẪU YÊU CẦU: NEG_OTHER_SITE
bộ phận được nhắc nhưng không phải chỗ bệnh xảy ra, ví dụ biến chứng lan sang hoặc bộ phận của ý khác
Ví dụ minh họa kiểu mẫu (chỉ để hiểu ý, không chép): "rung nhĩ thì sẽ gây biến chứng ở não"

ĐẦU RA
Chỉ trả về một đối tượng JSON, không kèm chữ nào khác:
{"skip": false, "skip_reason": "", "tagged": "<câu mới có thẻ>", "evidence": "<cụm từ trong câu mới quyết định nhãn của cặp đích>"}

## user

Câu gốc: cái [E1:PROCEDURE]điện cực[/E1] vào trong [E2:BODY_PART]não[/E2] và một cái cục pin vùng trước [E3:BODY_PART]ngực[/E3] và khi đó bác sĩ [E4:BODY_PART]thần kinh[/E4] bác sĩ về bệnh [E5:CONDITION]parkinson[/E5] sẽ

Cặp đích: [E5] "parkinson" (CONDITION) → [E2] "não" (BODY_PART)
Quan hệ đang xét: located_at
Nhãn yêu cầu cho cặp đích: NO_RELATION
Kiểu mẫu: NEG_OTHER_SITE
Người nói: bác sĩ giải thích trong chương trình tư vấn sức khỏe

---

# treated_by-POS-0000 (POS_EXPLICIT, nhãn treated_by)

## system

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
- Chỉ gán điều mà câu nói ra, không gán điều đúng về y học. Chỉ dùng chính câu đó, không suy từ ngữ cảnh ngoài câu.
- Quan hệ phải nối đúng hai mention đang xét, không phải mention khác cùng tên ở chỗ khác trong câu.
- Mỗi cặp có đúng một nhãn: tên quan hệ hoặc NO_RELATION. Không đủ thông tin để khẳng định thì NO_RELATION.
- Câu bị cắt mất phần nối hai thực thể: dương nếu phần còn lại đủ rõ, nếu không thì NO_RELATION.
- Nói về động vật hay thí nghiệm: NO_RELATION, trừ khi câu nói rõ đó là điều trị hay chẩn đoán.

LUẬT CỦA QUAN HỆ ĐÍCH
treated_by (CONDITION → DRUG): thuốc được dùng hoặc chỉ định để chữa, giảm hay kiểm soát bệnh đó.
- Dương: "thuốc corticoid để điều trị cho bệnh gút", "viêm họng được chữa bằng thuốc kháng sinh", "uống thuốc huyết áp để kiểm soát huyết áp".
- Không xét kết quả: đã dùng X cho Y mà không đỡ vẫn là dương.
- Giả định hay hướng dẫn chung "nếu bị Y thì dùng X" là dương. "X dùng cho người có bệnh Y" là dương.
- Câu hỏi đã kèm khẳng định ("tại sao Y phải dùng X") là dương.
- Âm: câu nói không dùng hoặc không nên dùng X cho Y ("thuốc chống tiểu cầu không phải là cách cho cục máu đông").
- Âm: phòng bệnh khi chưa mắc. Ngoại lệ: phòng biến chứng của bệnh đang có thì dương với bệnh đang có ("người rung nhĩ uống thuốc kháng đông để phòng đột quỵ": rung nhĩ → kháng đông dương, đột quỵ → kháng đông âm).
- Âm: tác dụng phụ, thuốc gây ra bệnh ("thuốc giảm đau gây viêm loét dạ dày").
- Âm: câu hỏi chưa có câu trả lời ("X có chữa được Y không").

KIỂU MẪU YÊU CẦU: POS_EXPLICIT
câu nói rõ dùng thuốc X để chữa, giảm hay kiểm soát Y, có từ nối rõ ràng
Ví dụ minh họa kiểu mẫu (chỉ để hiểu ý, không chép): "bị gút thì bác sĩ cho dùng thuốc corticoid để điều trị"

ĐẦU RA
Chỉ trả về một đối tượng JSON, không kèm chữ nào khác:
{"skip": false, "skip_reason": "", "tagged": "<câu mới có thẻ>", "evidence": "<cụm từ trong câu mới quyết định nhãn của cặp đích>"}

## user

Câu gốc: [E1:DRUG]forlic[/E1] nè những cái chất mà giúp cho chúng ta giảm [E2:CONDITION]căng thẳng[/E2] giảm [E3:CONDITION]stress[/E3] ngủ được giấc ngủ sâu và giúp cho [E4:BODY_PART]cơ thể[/E4]

Cặp đích: [E3] "stress" (CONDITION) → [E1] "forlic" (DRUG)
Quan hệ đang xét: treated_by
Nhãn yêu cầu cho cặp đích: treated_by
Kiểu mẫu: POS_EXPLICIT
Người nói: bác sĩ trả lời câu hỏi của thính giả

---

# treated_by-NEG-0000 (NEG_NOT_USED, nhãn NO_RELATION)

## system

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
- Chỉ gán điều mà câu nói ra, không gán điều đúng về y học. Chỉ dùng chính câu đó, không suy từ ngữ cảnh ngoài câu.
- Quan hệ phải nối đúng hai mention đang xét, không phải mention khác cùng tên ở chỗ khác trong câu.
- Mỗi cặp có đúng một nhãn: tên quan hệ hoặc NO_RELATION. Không đủ thông tin để khẳng định thì NO_RELATION.
- Câu bị cắt mất phần nối hai thực thể: dương nếu phần còn lại đủ rõ, nếu không thì NO_RELATION.
- Nói về động vật hay thí nghiệm: NO_RELATION, trừ khi câu nói rõ đó là điều trị hay chẩn đoán.

LUẬT CỦA QUAN HỆ ĐÍCH
treated_by (CONDITION → DRUG): thuốc được dùng hoặc chỉ định để chữa, giảm hay kiểm soát bệnh đó.
- Dương: "thuốc corticoid để điều trị cho bệnh gút", "viêm họng được chữa bằng thuốc kháng sinh", "uống thuốc huyết áp để kiểm soát huyết áp".
- Không xét kết quả: đã dùng X cho Y mà không đỡ vẫn là dương.
- Giả định hay hướng dẫn chung "nếu bị Y thì dùng X" là dương. "X dùng cho người có bệnh Y" là dương.
- Câu hỏi đã kèm khẳng định ("tại sao Y phải dùng X") là dương.
- Âm: câu nói không dùng hoặc không nên dùng X cho Y ("thuốc chống tiểu cầu không phải là cách cho cục máu đông").
- Âm: phòng bệnh khi chưa mắc. Ngoại lệ: phòng biến chứng của bệnh đang có thì dương với bệnh đang có ("người rung nhĩ uống thuốc kháng đông để phòng đột quỵ": rung nhĩ → kháng đông dương, đột quỵ → kháng đông âm).
- Âm: tác dụng phụ, thuốc gây ra bệnh ("thuốc giảm đau gây viêm loét dạ dày").
- Âm: câu hỏi chưa có câu trả lời ("X có chữa được Y không").

KIỂU MẪU YÊU CẦU: NEG_NOT_USED
câu nói rõ không dùng hoặc không nên dùng X cho Y
Ví dụ minh họa kiểu mẫu (chỉ để hiểu ý, không chép): "cục máu đông thì thuốc chống tiểu cầu không phải là cách"

ĐẦU RA
Chỉ trả về một đối tượng JSON, không kèm chữ nào khác:
{"skip": false, "skip_reason": "", "tagged": "<câu mới có thẻ>", "evidence": "<cụm từ trong câu mới quyết định nhãn của cặp đích>"}

## user

Câu gốc: một [E1:DOSAGE]phân tử[/E1] [E2:DRUG]protein[/E2] do [E3:CONDITION]vi khuẩn[/E3] gây bệnh [E4:CONDITION]bạch hầu[/E4] gây ra [E5:DRUG]độc tố[/E5] [E6:CONDITION]bạch hầu[/E6] có

Cặp đích: [E3] "vi khuẩn" (CONDITION) → [E5] "độc tố" (DRUG)
Quan hệ đang xét: treated_by
Nhãn yêu cầu cho cặp đích: NO_RELATION
Kiểu mẫu: NEG_NOT_USED
Người nói: bác sĩ giải thích trong chương trình tư vấn sức khỏe

---

# treated_by_procedure-POS-0000 (POS_EXPLICIT, nhãn treated_by_procedure)

## system

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
- Chỉ gán điều mà câu nói ra, không gán điều đúng về y học. Chỉ dùng chính câu đó, không suy từ ngữ cảnh ngoài câu.
- Quan hệ phải nối đúng hai mention đang xét, không phải mention khác cùng tên ở chỗ khác trong câu.
- Mỗi cặp có đúng một nhãn: tên quan hệ hoặc NO_RELATION. Không đủ thông tin để khẳng định thì NO_RELATION.
- Câu bị cắt mất phần nối hai thực thể: dương nếu phần còn lại đủ rõ, nếu không thì NO_RELATION.
- Nói về động vật hay thí nghiệm: NO_RELATION, trừ khi câu nói rõ đó là điều trị hay chẩn đoán.

LUẬT CỦA QUAN HỆ ĐÍCH
treated_by_procedure (CONDITION → PROCEDURE): thủ thuật hay phương pháp được dùng để chữa, giảm hay kiểm soát bệnh đó.
- Dương: "phẫu thuật điều trị béo phì", "kích thích não sâu sẽ giúp cải thiện triệu chứng chậm cử động".
- Không xét kết quả: "đã thử các phương pháp trị liệu béo phì nhưng thất bại" là dương.
- Giả định hay hướng dẫn chung "nếu bị Y thì làm X" là dương.
- Âm: câu nói không làm hoặc không nên làm X cho Y.
- Âm: phòng bệnh khi chưa mắc (ngoại lệ phòng biến chứng của bệnh đang có, như treated_by).
- Âm: thủ thuật gây ra bệnh ("hóa trị dẫn đến sụt cân": sụt cân → hóa trị âm).
- Âm: câu hỏi chưa có câu trả lời.

KIỂU MẪU YÊU CẦU: POS_EXPLICIT
câu nói rõ làm thủ thuật X để chữa, giảm hay kiểm soát Y
Ví dụ minh họa kiểu mẫu (chỉ để hiểu ý, không chép): "béo phì nặng thì có thể phẫu thuật để điều trị"

ĐẦU RA
Chỉ trả về một đối tượng JSON, không kèm chữ nào khác:
{"skip": false, "skip_reason": "", "tagged": "<câu mới có thẻ>", "evidence": "<cụm từ trong câu mới quyết định nhãn của cặp đích>"}

## user

Câu gốc: [E1:CONDITION]biến chứng[/E1] về [E2:CONDITION]loạn động[/E2] [E3:CONDITION]dao động vận động[/E3] thì lúc đó chúng ta mới xem xét [E4:PROCEDURE]phẫu thuật kích thích não sâu[/E4]

Cặp đích: [E2] "loạn động" (CONDITION) → [E4] "phẫu thuật kích thích não sâu" (PROCEDURE)
Quan hệ đang xét: treated_by_procedure
Nhãn yêu cầu cho cặp đích: treated_by_procedure
Kiểu mẫu: POS_EXPLICIT
Người nói: bác sĩ giải thích trong chương trình tư vấn sức khỏe

---

# treated_by_procedure-NEG-0000 (NEG_NOT_USED, nhãn NO_RELATION)

## system

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
- Chỉ gán điều mà câu nói ra, không gán điều đúng về y học. Chỉ dùng chính câu đó, không suy từ ngữ cảnh ngoài câu.
- Quan hệ phải nối đúng hai mention đang xét, không phải mention khác cùng tên ở chỗ khác trong câu.
- Mỗi cặp có đúng một nhãn: tên quan hệ hoặc NO_RELATION. Không đủ thông tin để khẳng định thì NO_RELATION.
- Câu bị cắt mất phần nối hai thực thể: dương nếu phần còn lại đủ rõ, nếu không thì NO_RELATION.
- Nói về động vật hay thí nghiệm: NO_RELATION, trừ khi câu nói rõ đó là điều trị hay chẩn đoán.

LUẬT CỦA QUAN HỆ ĐÍCH
treated_by_procedure (CONDITION → PROCEDURE): thủ thuật hay phương pháp được dùng để chữa, giảm hay kiểm soát bệnh đó.
- Dương: "phẫu thuật điều trị béo phì", "kích thích não sâu sẽ giúp cải thiện triệu chứng chậm cử động".
- Không xét kết quả: "đã thử các phương pháp trị liệu béo phì nhưng thất bại" là dương.
- Giả định hay hướng dẫn chung "nếu bị Y thì làm X" là dương.
- Âm: câu nói không làm hoặc không nên làm X cho Y.
- Âm: phòng bệnh khi chưa mắc (ngoại lệ phòng biến chứng của bệnh đang có, như treated_by).
- Âm: thủ thuật gây ra bệnh ("hóa trị dẫn đến sụt cân": sụt cân → hóa trị âm).
- Âm: câu hỏi chưa có câu trả lời.

KIỂU MẪU YÊU CẦU: NEG_NOT_USED
câu nói rõ không làm hoặc không nên làm X cho Y
Ví dụ minh họa kiểu mẫu (chỉ để hiểu ý, không chép): "viêm ruột thừa nhẹ thì chưa cần phải mổ ngay đâu"

ĐẦU RA
Chỉ trả về một đối tượng JSON, không kèm chữ nào khác:
{"skip": false, "skip_reason": "", "tagged": "<câu mới có thẻ>", "evidence": "<cụm từ trong câu mới quyết định nhãn của cặp đích>"}

## user

Câu gốc: [E1:CONDITION]thiếu máu[/E1] là cái dạng và [E2:DOSAGE]phổ biến nhất[/E2] là chiếm [E3:DOSAGE]từ tám mươi đến tám lăm phần trăm[/E3] cả trường hợp thì các bác sĩ chúng tôi sẽ [E4:PROCEDURE]đánh giá[/E4]

Cặp đích: [E1] "thiếu máu" (CONDITION) → [E4] "đánh giá" (PROCEDURE)
Quan hệ đang xét: treated_by_procedure
Nhãn yêu cầu cho cặp đích: NO_RELATION
Kiểu mẫu: NEG_NOT_USED
Người nói: người nhà hỏi bác sĩ

---

# diagnosed_by-POS-0000 (POS_EXPLICIT, nhãn diagnosed_by)

## system

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
- Chỉ gán điều mà câu nói ra, không gán điều đúng về y học. Chỉ dùng chính câu đó, không suy từ ngữ cảnh ngoài câu.
- Quan hệ phải nối đúng hai mention đang xét, không phải mention khác cùng tên ở chỗ khác trong câu.
- Mỗi cặp có đúng một nhãn: tên quan hệ hoặc NO_RELATION. Không đủ thông tin để khẳng định thì NO_RELATION.
- Câu bị cắt mất phần nối hai thực thể: dương nếu phần còn lại đủ rõ, nếu không thì NO_RELATION.
- Nói về động vật hay thí nghiệm: NO_RELATION, trừ khi câu nói rõ đó là điều trị hay chẩn đoán.

LUẬT CỦA QUAN HỆ ĐÍCH
diagnosed_by (CONDITION → TEST): xét nghiệm hay thăm khám được dùng để phát hiện, chẩn đoán hay theo dõi bệnh đó.
- Dương: "xét nghiệm sarscov2", "test covid phải âm tính", "đọc điện tâm đồ kết luận có rung nhĩ", "kiểm tra để biết có phải đau do thoái hóa".
- Âm: xét nghiệm và bệnh chỉ cùng xuất hiện ("đi kiểm tra thì đã bị ung thư rồi sụt cân": sụt cân → kiểm tra âm, vì sụt cân không phải thứ được kiểm tra).
- Âm: xét nghiệm dành cho một bệnh khác trong câu.

KIỂU MẪU YÊU CẦU: POS_EXPLICIT
xét nghiệm hay thăm khám được làm để phát hiện, chẩn đoán hay theo dõi bệnh
Ví dụ minh họa kiểu mẫu (chỉ để hiểu ý, không chép): "phải làm xét nghiệm máu để biết có bị tiểu đường không"

ĐẦU RA
Chỉ trả về một đối tượng JSON, không kèm chữ nào khác:
{"skip": false, "skip_reason": "", "tagged": "<câu mới có thẻ>", "evidence": "<cụm từ trong câu mới quyết định nhãn của cặp đích>"}

## user

Câu gốc: bác sĩ [E1:TEST]kiểm tra[/E1] ngay [E2:CONDITION]huyết áp[/E2] và [E3:PROCEDURE]cho thuốc[/E3] bác [E4:DRUG]thuốc uống[/E4] [E5:CONDITION]huyết áp[/E5] để [E6:DRUG]kiểm soát[/E6] tốt con số [E7:CONDITION]huyết áp[/E7] bác nhé vì với

Cặp đích: [E7] "huyết áp" (CONDITION) → [E1] "kiểm tra" (TEST)
Quan hệ đang xét: diagnosed_by
Nhãn yêu cầu cho cặp đích: diagnosed_by
Kiểu mẫu: POS_EXPLICIT
Người nói: người nhà hỏi bác sĩ

---

# diagnosed_by-NEG-0000 (NEG_COOCCUR, nhãn NO_RELATION)

## system

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
- Chỉ gán điều mà câu nói ra, không gán điều đúng về y học. Chỉ dùng chính câu đó, không suy từ ngữ cảnh ngoài câu.
- Quan hệ phải nối đúng hai mention đang xét, không phải mention khác cùng tên ở chỗ khác trong câu.
- Mỗi cặp có đúng một nhãn: tên quan hệ hoặc NO_RELATION. Không đủ thông tin để khẳng định thì NO_RELATION.
- Câu bị cắt mất phần nối hai thực thể: dương nếu phần còn lại đủ rõ, nếu không thì NO_RELATION.
- Nói về động vật hay thí nghiệm: NO_RELATION, trừ khi câu nói rõ đó là điều trị hay chẩn đoán.

LUẬT CỦA QUAN HỆ ĐÍCH
diagnosed_by (CONDITION → TEST): xét nghiệm hay thăm khám được dùng để phát hiện, chẩn đoán hay theo dõi bệnh đó.
- Dương: "xét nghiệm sarscov2", "test covid phải âm tính", "đọc điện tâm đồ kết luận có rung nhĩ", "kiểm tra để biết có phải đau do thoái hóa".
- Âm: xét nghiệm và bệnh chỉ cùng xuất hiện ("đi kiểm tra thì đã bị ung thư rồi sụt cân": sụt cân → kiểm tra âm, vì sụt cân không phải thứ được kiểm tra).
- Âm: xét nghiệm dành cho một bệnh khác trong câu.

KIỂU MẪU YÊU CẦU: NEG_COOCCUR
xét nghiệm và bệnh cùng xuất hiện nhưng bệnh không phải thứ được kiểm tra
Ví dụ minh họa kiểu mẫu (chỉ để hiểu ý, không chép): "đi kiểm tra sức khỏe định kỳ thì thấy người hay mệt"

ĐẦU RA
Chỉ trả về một đối tượng JSON, không kèm chữ nào khác:
{"skip": false, "skip_reason": "", "tagged": "<câu mới có thẻ>", "evidence": "<cụm từ trong câu mới quyết định nhãn của cặp đích>"}

## user

Câu gốc: này chúng ta chiến thắng được [E1:CONDITION]virus[/E1] thì [E2:CONDITION]virus[/E2] nó [E3:CONDITION]bị tiêu[/E3] diệt thì nói không [E4:TEST]xét nghiệm[/E4] không thấy hoặc là cũng có

Cặp đích: [E1] "virus" (CONDITION) → [E4] "xét nghiệm" (TEST)
Quan hệ đang xét: diagnosed_by
Nhãn yêu cầu cho cặp đích: NO_RELATION
Kiểu mẫu: NEG_COOCCUR
Người nói: bác sĩ trả lời câu hỏi của thính giả

---

# has_dosage-POS-0000 (POS_EXPLICIT, nhãn has_dosage)

## system

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
- Chỉ gán điều mà câu nói ra, không gán điều đúng về y học. Chỉ dùng chính câu đó, không suy từ ngữ cảnh ngoài câu.
- Quan hệ phải nối đúng hai mention đang xét, không phải mention khác cùng tên ở chỗ khác trong câu.
- Mỗi cặp có đúng một nhãn: tên quan hệ hoặc NO_RELATION. Không đủ thông tin để khẳng định thì NO_RELATION.
- Câu bị cắt mất phần nối hai thực thể: dương nếu phần còn lại đủ rõ, nếu không thì NO_RELATION.
- Nói về động vật hay thí nghiệm: NO_RELATION, trừ khi câu nói rõ đó là điều trị hay chẩn đoán.

LUẬT CỦA QUAN HỆ ĐÍCH
has_dosage (DRUG → DOSAGE): liều hay lượng đó là của chính thuốc đó.
- Dương: "uống hai viên đông trùng hạ thảo mỗi ngày", "tiêm hai mũi vắc xin".
- Âm: lượng là của thứ khác (thuốc khác, thức ăn, chỉ số đo: "mười milimet thủy ngân huyết áp tâm thu").
- Âm: lượng là số liệu thống kê, không phải liều.

KIỂU MẪU YÊU CẦU: POS_EXPLICIT
liều hoặc lượng là của chính thuốc đó, nói rõ cách dùng
Ví dụ minh họa kiểu mẫu (chỉ để hiểu ý, không chép): "mỗi ngày uống hai viên đông trùng hạ thảo"

ĐẦU RA
Chỉ trả về một đối tượng JSON, không kèm chữ nào khác:
{"skip": false, "skip_reason": "", "tagged": "<câu mới có thẻ>", "evidence": "<cụm từ trong câu mới quyết định nhãn của cặp đích>"}

## user

Câu gốc: một [E1:DOSAGE]phân tử[/E1] [E2:DRUG]protein[/E2] do [E3:CONDITION]vi khuẩn[/E3] gây bệnh [E4:CONDITION]bạch hầu[/E4] gây ra [E5:DRUG]độc tố[/E5] [E6:CONDITION]bạch hầu[/E6] có

Cặp đích: [E5] "độc tố" (DRUG) → [E1] "phân tử" (DOSAGE)
Quan hệ đang xét: has_dosage
Nhãn yêu cầu cho cặp đích: has_dosage
Kiểu mẫu: POS_EXPLICIT
Người nói: người nhà hỏi bác sĩ

---

# has_dosage-NEG-0000 (NEG_OTHER_OWNER, nhãn NO_RELATION)

## system

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
- Chỉ gán điều mà câu nói ra, không gán điều đúng về y học. Chỉ dùng chính câu đó, không suy từ ngữ cảnh ngoài câu.
- Quan hệ phải nối đúng hai mention đang xét, không phải mention khác cùng tên ở chỗ khác trong câu.
- Mỗi cặp có đúng một nhãn: tên quan hệ hoặc NO_RELATION. Không đủ thông tin để khẳng định thì NO_RELATION.
- Câu bị cắt mất phần nối hai thực thể: dương nếu phần còn lại đủ rõ, nếu không thì NO_RELATION.
- Nói về động vật hay thí nghiệm: NO_RELATION, trừ khi câu nói rõ đó là điều trị hay chẩn đoán.

LUẬT CỦA QUAN HỆ ĐÍCH
has_dosage (DRUG → DOSAGE): liều hay lượng đó là của chính thuốc đó.
- Dương: "uống hai viên đông trùng hạ thảo mỗi ngày", "tiêm hai mũi vắc xin".
- Âm: lượng là của thứ khác (thuốc khác, thức ăn, chỉ số đo: "mười milimet thủy ngân huyết áp tâm thu").
- Âm: lượng là số liệu thống kê, không phải liều.

KIỂU MẪU YÊU CẦU: NEG_OTHER_OWNER
lượng là của thứ khác: thuốc khác, thức ăn, nước, chỉ số đo
Ví dụ minh họa kiểu mẫu (chỉ để hiểu ý, không chép): "uống thuốc huyết áp xong rồi uống thêm hai cốc nước"

ĐẦU RA
Chỉ trả về một đối tượng JSON, không kèm chữ nào khác:
{"skip": false, "skip_reason": "", "tagged": "<câu mới có thẻ>", "evidence": "<cụm từ trong câu mới quyết định nhãn của cặp đích>"}

## user

Câu gốc: tố [E1:DRUG]vi lượng[/E1] các [E2:DRUG]vitamin[/E2] cũng nằm [E3:DOSAGE]phần lớn[/E3] ở phần [E4:DRUG]quả thể[/E4] cho nên phần [E5:DRUG]quả thể[/E5]

Cặp đích: [E2] "vitamin" (DRUG) → [E3] "phần lớn" (DOSAGE)
Quan hệ đang xét: has_dosage
Nhãn yêu cầu cho cặp đích: NO_RELATION
Kiểu mẫu: NEG_OTHER_OWNER
Người nói: bác sĩ trả lời câu hỏi của thính giả

---


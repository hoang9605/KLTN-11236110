# Hướng dẫn gán nhãn RE

**Đã khóa ngày 2026-11-19.** Không sửa hướng dẫn trong khi gán nhãn. Trường hợp chưa có trong hướng dẫn thì ghi vào cột `note`; sau khi gán xong mới xem lại.

Dữ liệu là bản ghi giọng nói VietMed, cắt thành đoạn khoảng 26 từ và không có dấu câu. Mỗi đoạn được gọi là một "câu". Thực thể lấy từ nhãn NER gốc của VietMed. Người gán **không sửa ranh giới thực thể**.

## Nguyên tắc chung

1. **Chỉ gán điều mà câu nói ra, không gán điều đúng về y học.** Ví dụ câu quảng cáo "người tiểu đường dùng đông trùng hạ thảo để giảm đường huyết" vẫn được tính là quan hệ có trong câu.
2. **Chỉ dùng chính câu đó.** Không suy từ câu trước hay câu sau, không dùng kiến thức bên ngoài để bù chỗ bị cắt.
3. **Quan hệ phải nối đúng hai mention đang xét**, không phải hai mention khác cùng tên ở chỗ khác trong câu.
4. **Mỗi cặp bắt buộc có đúng một nhãn**: tên quan hệ hoặc `NO_RELATION`. Không có nhãn "chưa rõ". Câu không đủ thông tin để khẳng định quan hệ thì gán `NO_RELATION`.
5. **Mọi nhãn đều viết bằng tiếng Anh**, đúng như trong hướng dẫn này.

## Bước A: kiểm tra thực thể

Với mỗi mention, chọn **VALID** (đúng kiểu) hoặc **INVALID** (sai kiểu, quá chung chung, hoặc không phải thực thể y khoa).

- Nếu ranh giới lệch một chút nhưng phần chính đúng kiểu thì vẫn chọn VALID. Ví dụ "thiếu máu" trong "thiếu máu cơ tim" vẫn là CONDITION hợp lệ.
- Cặp có thực thể bị INVALID thì không gán bước B. Ô của cặp đó tự để trống.

| Kiểu | VALID khi | INVALID, ví dụ |
|---|---|---|
| CONDITION | Bệnh, triệu chứng, tổn thương, tình trạng bất thường: ung thư, đau, viêm, béo phì, rung nhĩ, tê bì, sụt cân | Tên chung chung (bệnh lý, triệu chứng, biến chứng); tác nhân gây bệnh (vi khuẩn, virus, mầm bệnh); trạng thái bình thường (có thai, quan hệ); từ không phải bệnh (chậm, tử vong, di truyền) |
| CONDITION, trường hợp "huyết áp" | VALID khi nghĩa là bệnh tăng huyết áp: "bị huyết áp", "thuốc huyết áp", "huyết áp cao" | INVALID khi nghĩa là chỉ số đo: "đo huyết áp", "con số huyết áp" |
| CONDITION, tên mầm bệnh | VALID khi dùng với nghĩa là bệnh: "xét nghiệm sarscov2", "test covid" | INVALID khi nói về con vi sinh vật: "virus bị tiêu diệt" |
| DRUG | Thuốc, hoạt chất, vắc xin, kháng sinh. Tính cả thực phẩm chức năng, thảo dược, vitamin, khoáng chất, mỹ phẩm điều trị (kem bôi, serum) | Động từ hoặc hành động (kiểm soát, chỉ định, điều chỉnh, phòng ngừa, tuân thủ); chất trong cơ thể (melanin, cortisol, sữa mẹ); dinh dưỡng chung (chất béo, protein, chất dinh dưỡng) |
| PROCEDURE | Thủ thuật và phương pháp điều trị cụ thể: phẫu thuật, mổ, hóa trị, xạ trị, kích thích não sâu, đặt vòng, cấy ghép, nội soi, vật lý trị liệu | Động từ chung (cải thiện, hỗ trợ, phục hồi, chăm sóc, đánh giá); hành động dùng thuốc (uống thuốc, cho thuốc, tiêm), vì quan hệ thuốc thuộc treated_by; đồ vật (tủ lạnh, găng tay, màn hình) |
| TEST | Xét nghiệm, chẩn đoán hình ảnh, thăm khám: xét nghiệm, siêu âm, MRI, CT, X-quang, điện tâm đồ, "kiểm tra" khi là khám bệnh | Nghiên cứu khoa học; quá trình sinh lý (chuyển hóa, tuần hoàn, hấp thu, trao đổi chất, điều hòa); "kiểm tra" theo nghĩa thường |
| BODY_PART | Cơ quan, bộ phận, mô, dịch cơ thể: não, tim, da, khớp, máu, thắt lưng, động mạch | Quá chung chung (cơ thể, hệ, tế bào); không phải bộ phận (gen, dna, vi sinh vật, sắc tố, polyp) |
| DOSAGE | Liều, lượng, hàm lượng hay tần suất **của thuốc khi dùng**: "một viên", "hai mươi mốt viên", "hai mũi", "năm mươi mg", "ngày hai lần" | Tính từ (cao, thấp, rất nhiều); thứ tự (thứ nhất, cái thứ hai); thống kê (tỷ lệ, phần trăm bệnh nhân); chỉ số cơ thể (nhịp tim, đường huyết); thành phần sản phẩm ("một trăm phần trăm quả thể") |
OK duyệt
## Bước B: quan hệ

Mỗi cặp có cả hai thực thể VALID được gán một trong hai nhãn: **tên quan hệ** hoặc **NO_RELATION**. Chiều của cặp đã cố định theo bảng dưới.

| Quan hệ | Cặp | Dương khi câu nói |
|---|---|---|
| located_at | CONDITION → BODY_PART | Bệnh hoặc triệu chứng xảy ra ở bộ phận đó |
| treated_by | CONDITION → DRUG | Thuốc được dùng hoặc chỉ định để chữa, giảm hay kiểm soát bệnh đó |
| treated_by_procedure | CONDITION → PROCEDURE | Thủ thuật hay phương pháp được dùng để chữa, giảm hay kiểm soát bệnh đó |
| diagnosed_by | CONDITION → TEST | Xét nghiệm hay thăm khám được dùng để phát hiện, chẩn đoán hay theo dõi bệnh đó |
| has_dosage | DRUG → DOSAGE | Liều hay lượng đó là của chính thuốc đó |

### located_at

- **Dương:**
  - "đau thắt lưng"
  - "viêm loét ở cái miệng nối"
  - "cục máu đông ở trong tim"
  - "tê bì chân tay"
  - "thiếu máu cơ tim" (thiếu máu → cơ)
- **Âm:** "chóng mặt … tê bì chân tay": chân tay chỉ gắn với tê bì, không gắn với chóng mặt.
- **Âm:** bộ phận chỉ được nhắc cùng câu mà không phải chỗ bệnh xảy ra. Ví dụ "rung nhĩ gây biến chứng ở não": rung nhĩ → não là âm.
- **Liệt kê nhiều triệu chứng trước một bộ phận:** chỉ triệu chứng đứng sát bộ phận đó là dương, trừ khi câu nói rõ cả cụm cùng ở bộ phận đó.

### treated_by và treated_by_procedure

- **Dương:**
  - "thuốc corticoid để điều trị cho bệnh gút"
  - "viêm họng … được chữa bằng thuốc kháng sinh"
  - "phẫu thuật điều trị béo phì"
  - "phương pháp phẫu thuật kích thích não sâu sẽ giúp cải thiện triệu chứng chậm cử động"
- **Kiểm soát cũng là điều trị:** "uống thuốc huyết áp để kiểm soát huyết áp" là dương.
- **Không xét kết quả điều trị.** Câu nói đã dùng X cho Y thì là dương, kể cả khi X không hiệu quả. Ví dụ "đã thử các phương pháp trị liệu béo phì nhưng thất bại" là dương.
- **Âm khi câu nói không dùng hoặc không nên dùng X cho Y.** Ví dụ "thuốc chống tiểu cầu không phải là cách cho cục máu đông" là âm.
- **Phòng bệnh.** Dùng X để phòng Y khi chưa mắc Y là âm. Ví dụ "giải pháp phòng chống ung thư là cung cấp oxy".
  - Ngoại lệ: phòng biến chứng hay phòng tái phát của một bệnh đang có thì tính là dương với chính bệnh đang có. Ví dụ "người rung nhĩ uống thuốc kháng đông để phòng đột quỵ": rung nhĩ → thuốc kháng đông là dương, đột quỵ → thuốc kháng đông là âm.
- **Tác dụng phụ:** thuốc gây ra bệnh là âm. Ví dụ "hóa trị dẫn đến sụt cân": sụt cân → hóa trị là âm.
- **Câu hỏi.** Câu hỏi chưa có câu trả lời ("X có chữa được Y không") là âm. Câu hỏi đã kèm khẳng định ("tại sao Y phải dùng X") là dương.
- **Giả định hay hướng dẫn chung:** "nếu bị Y thì dùng X" là dương.
- **Đối tượng người dùng:** "X dùng cho người có bệnh Y" là dương.

OK duyệt

### diagnosed_by

- **Dương:**
  - "xét nghiệm sarscov2"
  - "test covid phải âm tính"
  - "đọc bảng điện tâm đồ … kết luận có tình trạng rung nhĩ"
  - "kiểm tra để biết có phải đau do thoái hóa"
- **Âm:** xét nghiệm và bệnh chỉ cùng xuất hiện trong câu. Ví dụ "đi kiểm tra thì đã bị ung thư rồi … sụt cân": sụt cân → kiểm tra là âm, vì sụt cân không phải thứ được kiểm tra.

### has_dosage

- **Dương:** "uống hai viên đông trùng hạ thảo mỗi ngày" (đông trùng hạ thảo → hai viên), "tiêm hai mũi vắc xin".
- **Âm:** lượng là của thứ khác, ví dụ "mười milimet thủy ngân huyết áp tâm thu". Hoặc lượng là thống kê, không phải liều.

## Trường hợp đặc biệt

| Tình huống | Nhãn |
|---|---|
| Câu bị cắt ngang làm mất phần nối hai thực thể | Nếu phần còn lại đủ rõ thì gán quan hệ. Nếu không thì `NO_RELATION`. |
| Hai mention giống hệt nhau trong một câu | Xét riêng từng mention theo vị trí của nó. |
| Phủ định ("không bị đau khớp") | located_at vẫn là dương, vì câu vẫn nói về vị trí của triệu chứng. Với treated_by, xem phần treated_by ở trên. |
| Nói về động vật hay thí nghiệm ("thí nghiệm độc tố bạch hầu") | Âm, trừ khi câu nói rõ đó là cách điều trị hay chẩn đoán bệnh. |

## Bổ sung sau khi gán bước A trên tập test

Các quy định dưới đây do người gán chốt ngày 2026-11-20, sau khi gán xong bước A của tập test. Chúng áp dụng cho mọi tập (test, seed, dev) và cho mọi lượt gán sau ngày này.

| Trường hợp | Quyết định |
|---|---|
| Mention PROCEDURE chỉ gồm đúng chữ "điều trị", không kèm tên phương pháp | INVALID. "điều trị" đứng một mình không phải thủ thuật hay phương pháp cụ thể. Mention dài hơn có tên phương pháp, ví dụ "điều trị bằng nội tiết", vẫn xét theo bảng PROCEDURE ở bước A. |

## Bổ sung 24/11/2026 sau khi chuyên gia chấm pilot_label_v1 và dev_label_v3

Chuyên gia trả lời hai câu hỏi về located_at:

1. Bệnh gây biến chứng hay tổn thương ở cơ quan khác: **có** tính located_at với cơ quan đó. Ví dụ «xơ vữa động mạch gây đột quỵ não» → xơ vữa động mạch → não là located_at.
2. «máu» là nơi xảy ra bệnh: **tùy bệnh**. Dương với bệnh của chính máu, mỡ máu, huyết áp hay mạch máu (mỡ máu, huyết áp cao, xơ vữa, chảy máu). Âm với bệnh của cơ quan khác chỉ ảnh hưởng gián tiếp tới máu (suy gan, rung nhĩ), và âm khi «máu» chỉ là thứ được truyền, bổ hay bị mất.

Ngoài ra (rút từ các dòng chuyên gia chấm 0): vị trí ngầm định theo kiến thức y khoa được tính khi bộ phận có trong câu và câu đang nói về bệnh đó; thực phẩm chức năng, mỹ phẩm quảng cáo «hỗ trợ» không phải treated_by; «cấp cứu», «vào viện» không phải PROCEDURE. Luật tương ứng: re_v3/llm_rules.py, bộ v4.

## Quy trình

1. Đọc cả câu một lần.
2. Gán bước A cho mọi mention.
3. Gán bước B cho các cặp còn hiệu lực.
4. Ghi vào cột `note` khi gặp trường hợp hướng dẫn chưa nói tới. Cột này chỉ để ghi chú, không phải nhãn.
5. Trên tập test, sau 1 ngày gán lại 30 cặp ngẫu nhiên để đo độ nhất quán của chính người gán.

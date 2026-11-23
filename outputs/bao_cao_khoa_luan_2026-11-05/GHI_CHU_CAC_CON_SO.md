# Ghi chú ôn tập: vì sao lại là con số này

Các căn cứ dưới đây lấy từ mã nguồn, tệp cấu hình và phép đo trên dữ liệu. Chỗ nào chỉ là giá trị đặt theo kinh nghiệm thì ghi rõ để khi bị hỏi bạn trả lời đúng, không nói quá.

## Mô hình NER (mục 1.2.2, Bảng 3.1)

| Con số | Ý nghĩa | Vì sao |
|---|---|---|
| 768 | Kích thước vector biểu diễn của mỗi subword | Cố định theo kiến trúc BERT-base. ViHealthBERT kế thừa từ PhoBERT-base nên không tự chọn được. |
| 37 | Số nhãn đầu ra | 2K + 1 với K = 18 loại thực thể của VietMed-NER: mỗi loại có B và I, cộng nhãn O. |
| 768 × 37 | Kích thước ma trận W của lớp phân loại | Biến mỗi vector 768 chiều thành 37 điểm số, mỗi điểm ứng với một nhãn. |
| 12 lớp, 12 head | Độ sâu và số head attention | Cố định theo cỡ base. |
| 258 vị trí | max_position_embeddings trong config | Gồm 256 vị trí dùng được và 2 vị trí dự phòng của PhoBERT. Trừ thêm `<s>` và `</s>` thì còn tối đa 256 subword cho nội dung. |

## Chia văn bản dài (mục 3.2, Hình 3.3)

Phép đo trên 3.497 câu của tập test bằng tokenizer của mô hình NER:
- Trung bình mỗi từ ứng với **1,013 subword**, trường hợp nặng nhất là **1,417**.
- Câu trung bình có **22,2 từ**, 99% số câu có **tối đa 34 từ**, câu dài nhất có **40 từ**.

| Ngưỡng | Quy tắc trong `ner/preprocessor.py` | Căn cứ |
|---|---|---|
| 140 từ | Cắt cứng | 140 × 1,417 ≈ 198 subword, dưới mức an toàn 200 (`MAX_SUBTOKENS_PER_CHUNK`) và dưới giới hạn 256. **Đây là ngưỡng có căn cứ từ dữ liệu.** |
| 200 subword | Mức an toàn ghi trong `ner/config.py` | Chừa khoảng dự phòng so với 256. Lưu ý: hằng số này được import nhưng không dùng trực tiếp trong vòng chia, việc chia dựa trên số từ. |
| 35 từ | Tách ở dấu kết thúc câu khi đoạn đã có từ 35 từ trở lên | Khớp độ dài câu, vì 99% câu ≤ 34 từ nên hầu hết câu nằm trọn trong một đoạn. |
| 15 từ | Tách ở dấu kết thúc câu nếu đoạn có từ 15 từ trở lên và phần còn lại cũng có từ 15 từ trở lên | Tránh tạo đoạn quá ngắn, thiếu ngữ cảnh. |
| 120 từ | Tách ở dấu phẩy hoặc dấu chấm phẩy | Ưu tiên cắt ở ranh giới mệnh đề trước khi chạm ngưỡng cứng 140, chừa 20 từ dự phòng. |

**Khi bị hỏi:** các ngưỡng 15, 35 và 120 là giá trị đặt theo kinh nghiệm, chưa được dò trên tập dev. Trên VietMed-NER không câu nào dài quá 40 từ, nên các ngưỡng này không ảnh hưởng tới kết quả báo cáo.

## Chuẩn hóa ICD-10 (mục 3.6.1, Bảng 3.3)

| Con số | Ý nghĩa | Căn cứ |
|---|---|---|
| 0,85 | Ngưỡng token_set_ratio (`fuzz_threshold` trong `normalization/icd10.py`) | Ngưỡng cao, theo nguyên tắc thà không gán còn hơn gán sai. Là giá trị mặc định, **chưa được dò trên tập dev**. |
| 0,60 | Tỉ lệ độ dài tối thiểu giữa hai chuỗi (`min_length_ratio`) | Chặn trường hợp chuỗi rất ngắn khớp với tên dài. |
| 0,40 | Jaccard tối thiểu khi cả hai chuỗi có tối đa 3 từ | Chặn các cặp như “đau bụng” và “đau lưng”. |
| 80 | Độ tương tự tối thiểu khi so từng từ ở ràng buộc cuối | Cho phép khác dấu hoặc lỗi gõ nhỏ. |

Điểm token_set_ratio thật, đo bằng RapidFuzz, để minh họa vì sao **chỉ dùng ngưỡng là không đủ**:
- “viêm loét dạ dày” với “viêm loét tá tràng”: 0,72, bị loại.
- “đái tháo đường” với “đái tháo nhạt”: 0,76, bị loại.
- “nhồi máu cơ tim” với “nhồi máu não”: 0,80, bị loại.
- “đau đầu mãn tính” với “đau lưng mãn tính”: 0,86, **vượt ngưỡng**.
- “tăng huyết áp vô căn” với “hạ huyết áp vô căn”: 0,91, **vượt ngưỡng**.
- “viêm gan virus B” với “viêm gan virus C”: 0,94, **vượt ngưỡng**.

Ba cặp cuối là hai bệnh khác nhau nhưng vẫn vượt 0,85. Vì vậy cần thêm các ràng buộc ở Bảng 3.3, ví dụ mọi từ nội dung của ứng viên phải có trong câu truy vấn.

## Các con số khác hay bị hỏi

| Con số | Ở đâu | Ý nghĩa |
|---|---|---|
| k = 5 | Danh sách top-k (mục 3.6.4) | Số ứng viên mặc định trả về cho người dùng chọn. |
| 0,5 | Ngưỡng quyết định RE (mục 3.7.3) | Điểm s từ 0,5 trở lên thì coi là có quan hệ. Đây là ngưỡng tự nhiên của phân loại nhị phân, không được tinh chỉnh. |
| 70, 15, 15 | Tỉ lệ chia train, dev, test cho RE (mục 3.7.5) | Tỉ lệ chia thông dụng, chia theo nhóm văn bản để không rò rỉ dữ liệu. |
| 5 phần | Kiểm định chéo | Mỗi lần dùng 80% để học và 20% để chấm, mọi cặp đều được chấm đúng một lần. |
| 1.000 lần | Bootstrap tính CI95 | Đủ để phân vị 2,5% và 97,5% ổn định. Lấy mẫu theo nhóm văn bản. |
| 3 seed | ViHealthBERT cho RE | Từng seed dao động mạnh, nên lấy trung bình xác suất của ba seed. |
| 162 cặp, 25 cặp dương | RE-600 sau khi duyệt | Phần lớn đoạn lời nói không có cặp quan hệ, nên dữ liệu thưa. Đây là hạn chế lớn nhất của phần RE, cần nói thẳng khi bị hỏi. |

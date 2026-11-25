# Kịch bản bảo vệ khóa luận (15 phút)

**Đề tài:** Hệ thống trích xuất thực thể, quan hệ và chuẩn hóa thông tin y tế từ văn bản tiếng Việt
**Căn cứ số liệu:** bản báo cáo v37 (23/11/2026)

Cách dùng: mỗi phần ghi thời điểm, nội dung slide và lời nói. Lời nói khoảng 2.000 từ, nói ở tốc độ khoảng 140 từ mỗi phút là vừa 15 phút. Phần in nghiêng trong ngoặc vuông là động tác, không đọc ra.

| # | Phần | Thời gian | Thời lượng |
|---|---|---|---|
| 1 | Mở đầu | 0:00 – 0:30 | 30 giây |
| 2 | Bối cảnh và bài toán | 0:30 – 2:00 | 1 phút 30 |
| 3 | Mục tiêu, phạm vi, câu hỏi nghiên cứu | 2:00 – 3:00 | 1 phút |
| 4 | Dữ liệu | 3:00 – 4:45 | 1 phút 45 |
| 5 | Kiến trúc hệ thống | 4:45 – 6:15 | 1 phút 30 |
| 6 | Kết quả NER | 6:15 – 7:45 | 1 phút 30 |
| 7 | Kết quả chuẩn hóa mã | 7:45 – 9:15 | 1 phút 30 |
| 8 | Kết quả trích xuất quan hệ | 9:15 – 10:45 | 1 phút 30 |
| 9 | Đồ thị tri thức và demo | 10:45 – 12:00 | 1 phút 15 |
| 10 | Trả lời ba câu hỏi nghiên cứu | 12:00 – 13:15 | 1 phút 15 |
| 11 | Hạn chế và hướng phát triển | 13:15 – 14:30 | 1 phút 15 |
| 12 | Kết thúc | 14:30 – 15:00 | 30 giây |

---

## 1. Mở đầu (0:00 – 0:30)

**Slide 1:** Tên đề tài, họ tên, mã sinh viên 11236110, lớp CNTT 65B, GVHD TS Phạm Minh Hoàn.

> Em kính chào các thầy cô trong hội đồng. Em là Nguyễn Hải Hoàng, lớp Công nghệ thông tin 65B. Hôm nay em xin trình bày khóa luận "Hệ thống trích xuất thực thể, quan hệ và chuẩn hóa thông tin y tế từ văn bản tiếng Việt", dưới sự hướng dẫn của TS Phạm Minh Hoàn. Bài trình bày gồm bốn phần: bài toán, dữ liệu và thiết kế, kết quả, và cuối cùng là hạn chế cùng hướng phát triển.

## 2. Bối cảnh và bài toán (0:30 – 2:00)

**Slide 2:** Số liệu bệnh án điện tử, câu ví dụ, Hình 2.1 (ba bước NER, chuẩn hóa, RE thành bản ghi).

> Hồ sơ y tế ở Việt Nam đang được số hóa nhanh. Theo Bộ Y tế, đến cuối năm 2025 đã có 1.188 trên hơn 1.650 cơ sở khám chữa bệnh triển khai bệnh án điện tử. Nhưng số hóa mới thay đổi cách lưu, còn phần giàu thông tin nhất như diễn biến bệnh hay lời dặn của bác sĩ vẫn là văn bản tự do. Máy không thống kê hay tìm kiếm theo khái niệm được trên loại dữ liệu này.
>
> *[chỉ vào Hình 2.1]* Bài toán của em là biến một câu như "bệnh nhân đau dạ dày, kê Paracetamol 500mg" thành bản ghi có cấu trúc. Việc này cần ba bước. Bước một là nhận diện thực thể, tức NER, để tìm ra "đau dạ dày" là bệnh, "Paracetamol" là thuốc, "500mg" là liều. Bước hai là chuẩn hóa, gán mã ICD-10 cho bệnh và mã RxNorm cho thuốc. Bước ba là trích xuất quan hệ, tức RE, để biết liều nào thuộc thuốc nào, thuốc nào điều trị bệnh nào.
>
> Với tiếng Việt, đề tài gặp ba khó khăn. Thứ nhất, chưa có bộ dữ liệu quan hệ lâm sàng tiếng Việt nào được công bố. Thứ hai, danh mục ICD-10 của Bộ Y tế dùng tên hành chính, trong khi người ta nói "huyết áp cao" chứ không nói "bệnh lý tăng huyết áp". Thứ ba, RxNorm là danh mục của Hoa Kỳ nên nhiều thuốc ở Việt Nam không có.

## 3. Mục tiêu, phạm vi, câu hỏi nghiên cứu (2:00 – 3:00)

**Slide 3:** Sáu loại thực thể, năm quan hệ, ba câu hỏi nghiên cứu.

> Hệ thống làm việc với sáu loại thực thể: tình trạng bệnh, thuốc, bộ phận cơ thể, xét nghiệm, thủ thuật và liều dùng. Năm quan hệ có hướng là located_at, treated_by, treated_by_procedure, diagnosed_by và has_dosage. Quan hệ chỉ xét trong một câu. Kết quả của nhiều văn bản được gộp thành một đồ thị tri thức.
>
> Khóa luận trả lời ba câu hỏi. Một, mô hình RE học từ dữ liệu có tốt hơn baseline dựa trên quy tắc không. Hai, lỗi NER ảnh hưởng tới RE thế nào. Ba, các bước bổ sung như quy tắc liều, hậu xử lý và chuẩn hóa mã đem lại lợi ích gì và tạo ra lỗi gì.

## 4. Dữ liệu (3:00 – 4:45)

**Slide 4:** Hình 3.1 (các bộ dữ liệu theo mục đích và phần chia). Ghi nổi bật: hướng dẫn hai bước; 600 câu train/dev, 100 câu test, 311 cặp, 106 cặp dương.

> Toàn bộ dữ liệu bắt nguồn từ VietMed-NER, bộ dữ liệu lời nói y tế tiếng Việt đã chép thành văn bản, có 18 loại thực thể. NER được chấm trên 3.497 câu test của bộ này.
>
> Đóng góp dữ liệu chính của khóa luận là bộ dữ liệu quan hệ. Em viết hướng dẫn gán nhãn hai bước và khóa lại trước khi gán. Bước một kiểm tra thực thể có hợp lệ không, ví dụ động từ "kiểm soát" không được coi là thuốc. Bước hai chỉ gán quan hệ cho cặp có cả hai thực thể hợp lệ.
>
> Tập huấn luyện và kiểm định gồm 600 câu từ phần train và validation, được mô hình ngôn ngữ lớn gán hai lượt độc lập, kappa đạt 0,916 và 0,947, rồi người có chuyên môn y khoa duyệt. Tập kiểm tra gồm 100 câu từ phần test, do người có chuyên môn y khoa gán, với 311 cặp, trong đó 106 cặp dương. Vì has_dosage và diagnosed_by quá hiếm, em sinh thêm dữ liệu từ câu huấn luyện và kiểm tra từng câu sinh qua ba lớp: cụm từ, bộ ba quan hệ đối chiếu với nguồn tri thức, và độ hợp lý của cả câu. Người duyệt đồng ý với 90,3% số câu mà bước kiểm tra tự động coi là hợp lệ.
>
> Điểm quan trọng là mọi tập dùng để báo cáo đều lấy từ phần test, và em kiểm tra trùng cả nguyên câu lẫn chuỗi 8 từ, nên không có câu nào vừa dùng để học vừa dùng để chấm.

## 5. Kiến trúc hệ thống (4:45 – 6:15)

**Slide 5:** Hình 3.3 (sáu bước xử lý). Ba nguyên tắc thiết kế ở góc slide.

> *[chỉ theo mũi tên]* Hệ thống gồm sáu bước. Tiền xử lý chia văn bản thành đoạn con, giữ vị trí ký tự. Mô hình ViHealthBERT gán nhãn từng từ. Quy tắc liều và hậu xử lý sửa các lỗi đã biết. Từ đây luồng tách thành hai nhánh độc lập: nhánh chuẩn hóa gán mã, nhánh RE sinh cặp và phân loại quan hệ. Cuối cùng kết quả được gộp vào đồ thị tri thức.
>
> Thiết kế theo ba nguyên tắc. Một, mọi thực thể giữ vị trí ký tự trong cùng văn bản để các bước dùng chung tọa độ. Hai, chuẩn hóa và RE độc lập, nên một thuốc không tra được mã vẫn nối được với bệnh. Ba, hệ thống phân biệt "không có kết quả" với "không đủ căn cứ để kết luận".
>
> Ở bước chuẩn hóa, em đi theo nguyên tắc thà không gán còn hơn gán sai. Hệ thống thử khớp chính xác, rồi từ điển tên gọi khác, cuối cùng mới tới fuzzy matching có ràng buộc. Ở bước RE, em dùng ViHealthBERT với ký hiệu đánh dấu hai thực thể trong câu, theo cách làm của Baldini Soares và Zhong và Chen, lấy trung bình xác suất của ba seed.

## 6. Kết quả NER (6:15 – 7:45)

**Slide 6:** Hình 4.4 (từ điển, CRF, ViHealthBERT) và Bảng 4.1 thu gọn (lược bỏ quy tắc).

> Trên 3.497 câu test, toàn luồng NER đạt micro-F1 khớp chặt 0,622 và khớp nới lỏng 0,754. Khoảng cách giữa hai con số cho thấy nhiều lỗi chỉ là lệch ranh giới span, loại thực thể vẫn đúng. Thời gian xử lý trung bình 103 ms mỗi câu trên CPU.
>
> *[chỉ Hình 4.4]* So với hai baseline học trên cùng tập train, ViHealthBERT đạt 0,621, cao hơn từ điển 0,576 và CRF 0,567, các khoảng tin cậy không chồng nhau. Ưu thế đến từ recall, vì mô hình ngôn ngữ nhận ra được cả cách nói chưa gặp trong train.
>
> *[chỉ Bảng 4.1]* Thử nghiệm lược bỏ cho một kết quả em muốn nói thẳng: các quy tắc gần như không thay đổi điểm tổng, chỉ tăng 0,0014. Quy tắc liều gần như không có gì để bắt vì văn bản lời nói hiếm khi có cụm "500mg 2 viên/ngày". Còn quy tắc gộp từ mức độ như "cao" vào bệnh lại bị phạt, vì nhãn gốc xếp các từ này vào nhóm đơn vị đo. Đây là một quy tắc hợp lý về nghĩa nhưng lệch quy ước của bộ dữ liệu.

## 7. Kết quả chuẩn hóa mã (7:45 – 9:15)

**Slide 7:** Bảng 4.3 thu gọn (4 dòng ICD-10) và Hình 4.5 (Top-k).

> Trước khi có tập đánh giá riêng, em khảo sát trên 402 đề cập bệnh và thấy phiên bản đầu gán sai 13 mã, tất cả đều do fuzzy matching. Ví dụ "viêm gan virus B" với "viêm gan virus C" có độ tương tự 0,94, vượt ngưỡng nhưng là hai bệnh khác nhau. Em bổ sung ràng buộc mọi từ nội dung của ứng viên phải có trong câu truy vấn, và toàn bộ mã sai bị chặn.
>
> *[chỉ Bảng 4.3]* Trên tập test chuẩn hóa, ở chế độ chặt, ICD-10 đạt độ chính xác 0,354, gấp khoảng năm lần khớp chính xác. Quan trọng hơn, precision khi trả lời là 1,000, tức mọi mã hệ thống đưa ra đều đúng, trong khi fuzzy matching không ràng buộc chỉ có precision 0,187. RxNorm đạt 0,638.
>
> *[chỉ Hình 4.5]* Độ chính xác 0,354 thấp vì hệ thống từ chối nhiều. Nhưng nếu hệ thống gợi ý danh sách cho người nhập liệu chọn, mã đúng nằm trong mười ứng viên đầu ở 69,1% trường hợp. Vì vậy em định vị hệ thống là công cụ gợi ý mã, không phải tự động gán mã.

## 8. Kết quả trích xuất quan hệ (9:15 – 10:45)

**Slide 8:** Bảng 4.5 (bốn phương pháp) và F1 theo quan hệ.

> Cấu hình dữ liệu được chọn trên tập kiểm định theo quy tắc đặt trước: macro-F1 cao nhất thì chọn. Cấu hình dùng toàn bộ dữ liệu sinh đã kiểm tra đạt 0,853 và được chọn.
>
> *[chỉ Bảng 4.5]* Trên 311 cặp của tập kiểm tra, ViHealthBERT đạt micro-F1 0,693, cao hơn rule-based 0,542 và mốc luôn trả lời có quan hệ 0,508. Khoảng tin cậy 95% của chênh lệch giữa mô hình và rule-based là từ 0,048 đến 0,258, không chứa 0, nên chênh lệch có ý nghĩa thống kê. Hợp mô hình với rule-based không giúp thêm, nên hệ thống dùng mô hình đứng một mình.
>
> Theo từng quan hệ, located_at tốt nhất với 0,844. treated_by và diagnosed_by đạt khoảng 0,7. Hai quan hệ yếu là treated_by_procedure với 0,333 và has_dosage với 0,556. has_dosage chỉ được học từ dữ liệu sinh, nên recall bằng 1 nhưng precision chỉ 0,385.
>
> Một phát hiện đáng chú ý: ở lượt gán đầu, người gán coi gần như mọi cặp cùng câu là có quan hệ, 304 trên 311 cặp. Khi soát lại, em chốt tiêu chí chặt hơn. Điều này cho thấy với dữ liệu nhỏ, định nghĩa thế nào là có quan hệ ảnh hưởng tới điểm số nhiều hơn việc đổi cấu hình mô hình.

## 9. Đồ thị tri thức và demo (10:45 – 12:00)

**Slide 9:** Hình 4.7 và ảnh giao diện demo (giao_dien_demo.jpg).

> Chạy toàn bộ hệ thống trên 3.496 câu test, với thực thể do NER sinh ra như khi chạy thật, em được đồ thị gồm 1.315 nút và 433 cạnh khác nhau. So với đồ thị dựng bằng phương pháp cũ, số cạnh tăng chủ yếu ở các quan hệ hiếm, ví dụ has_dosage từ 7 lên 81 lần xuất hiện. Mỗi cạnh giữ lại câu nguồn để người dùng kiểm tra.
>
> *[chỉ ảnh demo]* Toàn bộ luồng được đóng gói thành giao diện web. Người dùng nhập văn bản tự do, hệ thống trả về thực thể, mã chuẩn và quan hệ trong khoảng 0,4 đến 2,7 giây mỗi câu trên CPU. Hệ thống có bộ kiểm thử tự động 115 ca, chạy lại ngày 23/11 đều đạt.

*Nếu hội đồng cho phép demo trực tiếp: chuẩn bị sẵn 1 câu ngắn, ví dụ "Bệnh nhân đau ở vùng bụng, được điều trị bằng phẫu thuật.", và đã mở sẵn giao diện trước khi lên. Demo không quá 30 giây, nếu lỗi thì quay về ảnh chụp.*

## 10. Trả lời ba câu hỏi nghiên cứu (12:00 – 13:15)

**Slide 10:** Ba câu hỏi, mỗi câu một dòng trả lời.

> Tóm lại cho ba câu hỏi nghiên cứu.
>
> Câu một: có. Mô hình RE học từ dữ liệu tốt hơn rule-based có ý nghĩa thống kê, lợi thế đến từ recall, rõ nhất ở diagnosed_by với 0,700 so với 0,235.
>
> Câu hai: lỗi NER ảnh hưởng trực tiếp tới RE. Ở dữ liệu quan hệ cũ, khoảng 43% cặp âm chứa thực thể sai kiểu. Trong đồ thị, một số bộ ba sai bắt nguồn từ lỗi cắt span của NER, ví dụ "thính giả" bị tách thành bệnh "thính" và thuốc "giả". Câu này em trả lời bằng phân tích định tính, chưa đo định lượng.
>
> Câu ba: các quy tắc NER gần như không thay đổi kết quả. Với chuẩn hóa, fuzzy matching là nguồn duy nhất của mã sai, và sau khi thêm ràng buộc thì không còn mã sai trên tập test.

## 11. Hạn chế và hướng phát triển (13:15 – 14:30)

**Slide 11:** Hai cột: hạn chế, hướng phát triển theo thứ tự ưu tiên.

> Khóa luận còn một số hạn chế em xin nêu rõ. Hệ thống mới được đánh giá trên lời nói y tế đã chép lại, chưa phải bệnh án thật. Dữ liệu quan hệ còn nhỏ và tập kiểm tra chỉ có một người gán. Mô hình ngôn ngữ lớn có tham gia gán nhãn huấn luyện và gợi ý nhãn kiểm tra. Bước chuẩn hóa chưa dùng ngữ cảnh câu.
>
> Hướng phát triển theo thứ tự ưu tiên: thứ nhất, mời thêm một người có chuyên môn gán độc lập tập kiểm tra và đánh giá RE trên thực thể do NER sinh ra. Thứ hai, huấn luyện bộ phân loại thực thể hợp lệ từ nhãn VALID và INVALID để thay danh sách chặn cố định. Thứ ba, bổ sung dữ liệu đơn thuốc thật cho has_dosage, chuẩn hóa thêm bộ phận cơ thể, xét nghiệm, thủ thuật, và thử trên bệnh án thật khi có dữ liệu được phép dùng.

## 12. Kết thúc (14:30 – 15:00)

**Slide 12:** Cảm ơn, ba đóng góp chính.

> Tóm lại, khóa luận có ba đóng góp: một luồng xử lý chạy được từ văn bản tới đồ thị tri thức; bộ dữ liệu quan hệ và chuẩn hóa mã cho văn bản y tế tiếng Việt; và một khung đánh giá có baseline, khoảng tin cậy và phân tích lỗi. Hệ thống được thiết kế để hỗ trợ người nhập liệu, không thay thế quyết định lâm sàng.
>
> Em xin chân thành cảm ơn thầy Phạm Minh Hoàn đã hướng dẫn, và cảm ơn hội đồng đã lắng nghe. Em rất mong nhận được câu hỏi và góp ý của các thầy cô.

---

## Chuẩn bị cho phần hỏi đáp

| Câu hỏi dễ gặp | Ý trả lời ngắn |
|---|---|
| Vì sao F1 NER chỉ 0,62? | Khớp chặt yêu cầu đúng từng ký tự ranh giới. Khớp nới lỏng là 0,754. Nhiều lỗi là lệch span hoặc nhãn gốc không nhất quán, ví dụ DOSAGE hẹp hơn UNITCALIBRATOR. Mô hình vẫn vượt hai baseline có ý nghĩa. |
| Mô hình NER có tự huấn luyện không? | Không. Mô hình được kế thừa, không huấn luyện lại. Đóng góp nằm ở luồng xử lý, baseline, đánh giá và phân tích lỗi. Phải nói rõ điểm này. |
| Validation 0,880 mà test 0,657, có rò rỉ không? | Không. Hai baseline chỉ học trên train cũng giảm tương tự. 7,5% câu validation có chung cụm 8 từ với train, còn ở test chỉ 0,3%. Do phân bố dữ liệu, nên luôn báo cáo trên test. |
| Độ chính xác ICD-10 0,354 có quá thấp? | Đó là cái giá của chế độ chặt: precision 1,000 và từ chối đúng 98,5% dạng NIL. Chế độ luôn gán đạt 0,520 nhưng gán mã cho cả dạng không có mã. Top-10 đạt 69,1%, phù hợp kịch bản gợi ý. |
| Dev ICD-10 0,796 mà test 0,354? | Từ điển tên gọi khác lấy từ train và dev, và dev rất gần train. Con số cần trích là test. Cải tiến vẫn có thật: test tăng từ 0,187 lên 0,354. |
| Dùng LLM gán nhãn có đáng tin không? | Train/dev: hai lượt LLM độc lập, kappa 0,916 và 0,947, người có chuyên môn duyệt, loại các chỗ không thống nhất. Test: người có chuyên môn gán, LLM chỉ gợi ý. Đây là hạn chế lớn nhất, nên người gán thứ hai độc lập là hướng phát triển ưu tiên số một. |
| Dữ liệu sinh có làm kết quả ảo? | Chỉ sinh từ câu huấn luyện, loại câu trùng chuỗi 8 từ với dev và test, kiểm tra ba lớp, người duyệt đồng ý 90,3% với câu được coi là hợp lệ. Cấu hình được chọn trên dev theo quy tắc đặt trước. Tập test hoàn toàn là câu thật. |
| Vì sao has_dosage precision thấp? | Dữ liệu thật không còn cặp has_dosage nào sau khi lọc, mô hình chỉ học từ dữ liệu sinh. Cần đơn thuốc thật. |
| Các ngưỡng 0,85, 15, 35, 120 lấy ở đâu? | 140 từ có căn cứ dữ liệu (140 × 1,417 ≈ 198 subword < 200 < 256). 15, 35, 120 và 0,85 là giá trị kinh nghiệm, chưa dò trên dev. Trên VietMed-NER câu dài nhất 40 từ nên các ngưỡng chia không ảnh hưởng kết quả. Nói thật, không nói quá. |
| Ngưỡng RE 0,5? | Ngưỡng tự nhiên của phân loại nhị phân, không tinh chỉnh, vì tập kiểm định chỉ có 111 cặp. |
| Khoảng tin cậy tính thế nào? | Bootstrap 2.000 lần theo câu, vì các cặp trong cùng câu không độc lập. Chỉ kết luận tốt hơn khi khoảng tin cậy của chênh lệch không chứa 0. |
| Ứng dụng thực tế? | Gợi ý thực thể và mã bệnh cho người nhập liệu xác nhận, tiền xử lý cho tìm kiếm và thống kê. Không thay thế quyết định lâm sàng. |

## Lưu ý trước khi lên bảo vệ

- Tệp `GHI_CHU_CAC_CON_SO.md` có hai chỗ đã cũ so với bản v37: ghi "bootstrap 1.000 lần, theo nhóm văn bản" trong khi báo cáo ghi **2.000 lần theo câu**, và ghi "RE-600: 162 cặp, 25 cặp dương" trong khi tập kiểm tra hiện tại là **311 cặp, 106 cặp dương**. Khi trả lời, dùng số của báo cáo v37.
- Tập dượt có bấm giờ ít nhất hai lần. Nếu lố giờ, rút ngắn mục 5 (kiến trúc) và mục 9 (đồ thị) trước, giữ nguyên mục 6 đến 8 và mục 10.
- Mỗi slide kết quả chỉ để 1 hình hoặc 1 bảng thu gọn, con số chính in đậm để hội đồng nhìn theo kịp lời nói.

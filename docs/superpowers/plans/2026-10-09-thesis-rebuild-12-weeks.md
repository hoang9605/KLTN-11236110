# Kế hoạch làm lại khóa luận trong 12 tuần

Ngày lập: 09/10/2026. Người thực hiện: sinh viên, có AI hỗ trợ. Đây là kế hoạch nghiên cứu và hoàn thành khóa luận; chưa phải lệnh triển khai hoặc kết quả thực nghiệm.

**Mục tiêu:** tự xây dựng, giải thích và tái lập được hệ thống trích xuất thực thể, quan hệ và chuẩn hóa thông tin y tế tiếng Việt; hoàn thành dữ liệu, mã nguồn, thực nghiệm, luận văn và bảo vệ.

**Kiến trúc dự kiến:** văn bản → NER → thực thể có vị trí ký tự → hai nhánh RE và chuẩn hóa → kết quả hợp nhất. RE sử dụng thực thể và ngữ cảnh; lỗi tra mã không ngăn RE hoạt động.

**Công nghệ dự kiến:** Python, PyTorch/Transformers, ViHealthBERT, dữ liệu JSONL, pytest; ICD-10 và RxNorm theo phạm vi dự án. Giao diện demo tối giản, chọn khi triển khai. Khóa phiên bản thư viện sau khi xác minh môi trường chạy được.

**Căn cứ:** `PROJECT_CONTEXT.md`, `PROJECT_OVERVIEW.md`, `docs/RE_LABELS.md`, `docs/RE_PLAN_3_WEEKS.md`, `outputs/vietmed_600_RE_review/HUONG_DAN_DU_LIEU.md` và `eval/results/summary.md`. Các baseline, metric và lựa chọn huấn luyện dưới đây là đề xuất để sinh viên chốt với GVHD ở tuần 1, chưa thay thế quyết định đã lưu trong dự án.

## 1. Cách hiểu “làm lại từ đầu”

Làm lại chuỗi công việc từ xác định bài toán, hiểu dữ liệu, thiết kế thực nghiệm đến viết hệ thống và bảo vệ. Giữ nguyên bản cũ để tham khảo, đối chiếu và khôi phục. Khi triển khai, làm ở nhánh hoặc thư mục riêng; chưa xóa hay ghi đè mã, dữ liệu và checkpoint hiện có.

Không cần huấn luyện một mô hình ngôn ngữ từ con số không. Hướng đề xuất là dùng encoder pretrained, tái dựng quy trình NER có thể tái lập và xây RE riêng. Với NER, tuần 1 quyết định một trong hai mức:

- **Mức cơ sở:** checkpoint hiện có là thành phần được kế thừa; xây lại suy luận, đánh giá và công bố rõ nguồn checkpoint. Phù hợp khi đóng góp chính là dữ liệu RE và hệ thống.
- **Mức mở rộng:** tái dựng fine-tune NER từ encoder pretrained nếu cần làm chủ toàn bộ quá trình huấn luyện hoặc checkpoint thiếu bằng chứng nguồn gốc. Thực hiện trong tuần 5, lưu checkpoint mới riêng. Không gọi việc dùng checkpoint cũ là tự huấn luyện lại NER.

Ngân sách giả định: **20–25 giờ chủ động/tuần, tổng 240–300 giờ**, chưa tính thời gian máy chạy. Đây là ước lượng lập lịch, không phải cam kết tốc độ. AI giúp tăng tốc viết mã, kiểm thử và trình bày; tốc độ duyệt nhãn, phản hồi GVHD và thực nghiệm phải đo thực tế. Nếu có ít giờ hơn, cắt thí nghiệm phụ theo mục 7.

## 2. Phạm vi và đích đến

Giữ sáu loại thực thể: CONDITION, DRUG, BODY_PART, TEST, PROCEDURE, DOSAGE. CONDITION gồm bệnh và triệu chứng. Giữ năm quan hệ có chiều:

- `located_at`: CONDITION → BODY_PART.
- `treated_by`: CONDITION → DRUG.
- `treated_by_procedure`: CONDITION → PROCEDURE.
- `diagnosed_by`: CONDITION → TEST.
- `has_dosage`: DRUG → DOSAGE.

`NO_RELATION` là nhãn âm cho cặp đúng kiểu đã được duyệt. Chuẩn hóa CONDITION sang ICD-10 và DRUG sang RxNorm; chấp nhận không tìm được mã. DOSAGE cần được định nghĩa rõ về hàm lượng, lượng dùng và tần suất; không coi mọi đơn vị đo là liều thuốc.

Phạm vi chính là quan hệ thể hiện trực tiếp trong cùng câu hoặc phát ngôn ngắn. Không đưa knowledge graph lớn, chatbot tư vấn, xử lý âm thanh, ứng dụng bệnh viện hoặc mở rộng toàn bộ ontology vào đường găng.

Câu hỏi nghiên cứu đề xuất:

1. Mô hình RE học từ dữ liệu có cải thiện so với luật trên cùng bộ dữ liệu không?
2. Lỗi NER làm chất lượng RE toàn hệ thống thay đổi như thế nào?
3. Các bước xử lý bổ sung và chuẩn hóa đem lại lợi ích gì, đồng thời tạo lỗi gì?

Đóng góp có thể nằm ở corpus được kiểm duyệt, quy trình tái lập và phân tích lỗi, kể cả khi mô hình không vượt baseline. Không đặt trước một điểm F1 rồi điều chỉnh dữ liệu để đạt điểm đó.

## 3. Những điểm đã biết và cần xác minh

- Kho mã đã có NER, normalization, đánh giá và các script chuẩn bị phiếu RE. Báo cáo cũ ghi NER strict micro-F1 0,6223 trên 3.497 mẫu; lần lập kế hoạch này chưa chạy lại để xác nhận.
- Hướng dẫn của gói 600 mẫu ghi tất cả lấy từ official train; `annotations_draft.jsonl` là bản AI đề xuất. Việc đã xuất phiếu không chứng minh đã được bác sĩ kiểm duyệt.
- Hướng dẫn cũng ghi chưa có positive chắc chắn cho `diagnosed_by` và `has_dosage` trong bản đề xuất. Phải đo lại sau duyệt, không coi 600 đoạn đồng nghĩa đủ năm quan hệ.
- Không chia ngẫu nhiên 600 mẫu này rồi gọi phần giữ lại là test độc lập cho toàn hệ thống nếu NER đã học chúng. Có thể dùng holdout từ train nguồn để khảo sát RE với gold entities, nhưng phải công bố đúng giới hạn.
- VietMed-NER là dữ liệu nhận diện thực thể từ lời nói y tế. Kết quả trên đó chưa chứng minh chất lượng trên bệnh án bệnh viện. Nguồn: [Medical Spoken Named Entity Recognition](https://aclanthology.org/2025.naacl-industry.59/) và [dataset của tác giả](https://huggingface.co/datasets/leduckhai/VietMed-NER).

## 4. Lộ trình 12 tuần

Ngày tháng dưới đây giả định bắt đầu 09/10/2026. Nếu bắt đầu muộn hơn, dịch nguyên lịch; không rút ngắn các bước xác minh dữ liệu để giữ ngày kết thúc.

### Tuần 1 — 09–15/10: chốt bài toán và thiết kế nghiên cứu

- [ ] Viết đề cương hai trang: đầu vào, đầu ra, đối tượng sử dụng, phạm vi và ba câu hỏi nghiên cứu.
- [ ] Kiểm kê mã, dữ liệu, checkpoint, log huấn luyện và lịch sử sử dụng test. Phân biệt phần tự làm, phần kế thừa và phần chưa xác minh.
- [ ] Đọc kỹ 5–8 tài liệu cốt lõi; ghi mỗi tài liệu một đoạn về bài toán, dữ liệu, phương pháp, đánh giá và điểm liên quan. AI hỗ trợ tóm tắt, sinh viên mở bản gốc để kiểm tra.
- [ ] Chốt với GVHD schema, cách xử lý phủ định/câu hỏi, phạm vi DOSAGE, baseline, metric và mức làm lại NER.
- [ ] Xác nhận GPU, thời gian cá nhân, khả năng có người duyệt nhãn, mẫu luận văn và hạn nộp của trường.
- [ ] Tạo đề cương chương mục và bắt đầu chương mở đầu ngay.

**Đầu ra:** `docs/rebuild/proposal.md`, `docs/rebuild/experiment-protocol.md`, `docs/rebuild/decision-log.md`, `thesis/outline.md`.

**Điều kiện qua tuần:** giải thích được hệ thống giải quyết việc gì, đóng góp nào đo được, dữ liệu nào đánh giá và phần nào ngoài phạm vi.

### Tuần 2 — 16–22/10: tổ chức dữ liệu và gán nhãn thử

- [ ] Cố định phiên bản nguồn, lưu ID, split, nhóm hội thoại nếu có và quyền sử dụng/phát hành dữ liệu.
- [ ] Kiểm tra trùng/gần trùng giữa các split; không tự coi các dòng đứng cạnh nhau là cùng hội thoại.
- [ ] Viết guideline NER/RE với ví dụ có quan hệ, không có quan hệ, mơ hồ, phủ định, thuốc gây bệnh và nhiều thuốc–nhiều liều.
- [ ] Duyệt thử 50–80 đoạn từ train, đo phút/đoạn và thống kê cạnh dương từng loại.
- [ ] Kiểm tra quá trình xuất/nhập phiếu giữ đúng dấu tiếng Việt, ID, vị trí ký tự và thực thể lặp.
- [ ] Chốt kế hoạch lấy mẫu dựa trên pilot; đặt lịch duyệt với người thứ hai nếu có.

**Đầu ra:** `docs/rebuild/annotation-guideline.md`, `data/rebuild/pilot.jsonl`, `data/rebuild/manifest.json`, `docs/rebuild/pilot-report.md`.

**Điều kiện qua tuần:** có guideline dùng được và tốc độ duyệt thực đo; biết các nhãn nào đang thiếu. Nếu chưa đạt, sửa quy trình trước khi làm hàng loạt.

### Tuần 3 — 23–29/10: xây corpus và bộ khung hệ thống

- [ ] Bắt đầu kiểm duyệt chính thức. Mốc lập kế hoạch là 600 đoạn đã duyệt: khoảng 400 train, 100 dev, 100 test, điều chỉnh theo nhóm nguồn và độ phủ thực tế.
- [ ] Tận dụng kho 600 đoạn hiện có làm nguồn ứng viên train; lấy dev/test từ nguồn validation/test độc lập phù hợp. Nếu dùng hết 600 đoạn train và bổ sung dev/test thì tổng corpus sẽ lớn hơn 600; ghi đúng số thực tế.
- [ ] Sửa thực thể trước, sinh lại cặp rồi duyệt quan hệ. Cặp chưa duyệt không tự biến thành âm.
- [ ] Làm bộ đọc dữ liệu, kiểm tra offset, kiểu/chiều quan hệ, ID và trạng thái duyệt. Không cho bản ghi chưa hoàn tất đi vào gold.
- [ ] Tạo pipeline tối thiểu đọc một đoạn và trả kết quả có cấu trúc; chưa cần giao diện đẹp.
- [ ] Viết phần nguồn dữ liệu và quy trình annotation vào chương phương pháp.

**Đầu ra:** dữ liệu đã duyệt đợt 1, bộ kiểm tra dữ liệu và pipeline khung. Mốc khoảng một nửa corpus là mục tiêu tiến độ, không phải tiêu chí chất lượng.

**Điều kiện qua tuần:** một mẫu đi qua toàn bộ quá trình đọc–kiểm tra–xuất mà không mất vị trí hoặc nhãn; tiến độ còn phù hợp ngân sách pilot.

### Tuần 4 — 30/10–05/11: khóa dữ liệu và xây lại NER

- [ ] Hoàn tất corpus mục tiêu; thống kê số đoạn, số thực thể, số cặp, cạnh dương và âm theo nhãn/split.
- [ ] Rà độc lập khoảng 15–20% dữ liệu nếu có người thứ hai; đo nhất quán trước khi hòa giải. Nếu chỉ một người, đọc lại một phần sau ít nhất 48 giờ và công bố đúng giới hạn.
- [ ] Khóa dữ liệu v1, guideline và checksum; giữ test tách khỏi vòng phát triển.
- [ ] Xây NER: tokenizer, căn chỉnh subword, giải mã BIO, mapping sáu nhãn, xử lý văn bản dài và vị trí ký tự.
- [ ] Kiểm tra dấu câu, từ lặp, câu rỗng, thực thể sát nhau và đoạn dài. Giữ văn bản dùng đánh giá cố định; nếu chuẩn hóa văn bản phải có cách đối chiếu offset rõ ràng.
- [ ] Đánh giá phát triển trên dev; ghi nhận riêng kết quả nhãn nguồn và schema sáu loại, tránh đồng nhất 37 nhãn BIO với 37 loại thực thể.

**Đầu ra:** corpus v1, báo cáo chất lượng nhãn, NER chạy được và báo cáo dev.

**Điều kiện qua tuần:** dữ liệu hợp lệ, split có nguồn gốc; nhãn thiếu bằng chứng được ghi rõ. Nếu dữ liệu chưa đạt, ưu tiên hoàn tất và cắt thí nghiệm phụ.

### Tuần 5 — 06–12/11: hoàn thiện NER và chuẩn hóa

- [ ] Nếu tuần 1 đã chọn tái dựng fine-tune NER, chạy huấn luyện trên train và chọn checkpoint bằng dev; lưu cấu hình, seed, log và checkpoint riêng.
- [ ] Nếu kế thừa checkpoint, hoàn thiện bằng chứng nguồn gốc và tái lập inference; không đổi nhãn “kế thừa” thành “huấn luyện mới”.
- [ ] Tách và đánh giá tác động của luật liều lượng, mapping và hậu xử lý trên dev.
- [ ] Làm chuẩn hóa CONDITION/DRUG, lưu mã, tên chuẩn, nguồn và trạng thái không khớp.
- [ ] Chuẩn bị tập kiểm tra chuẩn hóa có đáp án được rà riêng; tách phần phát triển và phần cuối. Bao gồm ca không đủ thông tin để gán mã.
- [ ] Hoàn thiện chương thiết kế NER và normalization.

**Đầu ra:** NER có nguồn gốc rõ, normalization chạy được, cấu hình được lưu và thiết kế đánh giá chuẩn hóa.

**Điều kiện qua tuần:** kết quả trả về có thể đối chiếu với văn bản; không ép mọi bệnh/thuốc nhận một mã.

### Tuần 6 — 13–19/11: hoàn thành RE baseline và luồng demo

- [ ] Sinh cặp theo đúng kiểu và chiều; đo tỷ lệ cạnh gold được bước sinh cặp giữ lại.
- [ ] Làm baseline luật dựa trên ngữ cảnh/trigger và liên kết thuốc–liều. Phát triển luật bằng train/dev.
- [ ] Kiểm tra phủ định, thuốc gây bệnh, hai thuốc hai liều và thứ tự thực thể đảo trong câu.
- [ ] Ghép NER, RE và normalization, xuất JSON chứa text, entities, relations và mã chuẩn.
- [ ] Tạo demo nhập văn bản, hiển thị thực thể, quan hệ và xuất kết quả; có ví dụ thành công và ví dụ thất bại.

**Đầu ra:** hệ thống tối thiểu chạy từ đầu đến cuối, baseline RE và demo bản đầu.

**Điều kiện qua tuần:** có sản phẩm chạy được để trình GVHD; không cần chờ mô hình RE tốt mới có demo.

### Tuần 7 — 20–26/11: huấn luyện mô hình RE

- [ ] Tạo biểu diễn cặp bằng dấu đánh dấu thực thể, kiểm tra crop giữ được cả hai đầu mút và giới hạn token thực của encoder.
- [ ] Huấn luyện một mô hình RE chính dùng encoder và bộ phân loại cặp; NER và RE có checkpoint riêng.
- [ ] Thử tối đa hai cấu hình chính trên dev trước khi mở rộng; đo thời gian và bộ nhớ bằng một lượt nhỏ.
- [ ] Đánh giá RE khi biết thực thể đúng và khi dùng NER dự đoán; chưa mở test để điều chỉnh.
- [ ] Nếu âm áp đảo, thử xử lý ở train và lưu thiết lập; giữ nguyên phân bố dev/test.

**Đầu ra:** mô hình RE, log huấn luyện, so sánh baseline–mô hình trên dev.

**Điều kiện qua tuần:** thí nghiệm chạy lại được; mô hình không hơn baseline vẫn là kết quả hợp lệ cần phân tích.

### Tuần 8 — 27/11–03/12: thực nghiệm đối chứng và khóa lựa chọn

- [ ] So sánh tối thiểu baseline luật và mô hình RE trên cùng dữ liệu và cách chấm.
- [ ] Nếu còn nguồn lực, chọn một thí nghiệm bỏ/bật thành phần có giả thuyết rõ, chẳng hạn typed markers hoặc luật hậu xử lý.
- [ ] Chạy ba seed cho mô hình chính nếu ngân sách cho phép; nếu chỉ một seed phải ghi rõ hạn chế.
- [ ] Kiểm tra công thức metric bằng ví dụ đếm tay: cạnh thừa, cạnh thiếu, sai chiều, sai span và NER mất đầu mút.
- [ ] Chốt checkpoint, ngưỡng, luật, các cấu hình báo cáo và cách xử lý lớp vắng mẫu trước test.
- [ ] Hoàn tất bản nháp chương phương pháp và thiết kế thực nghiệm.

**Đầu ra:** cấu hình khóa, nhật ký thí nghiệm và danh sách so sánh cuối.

**Điều kiện qua tuần:** mỗi bảng dự kiến trong luận văn có thí nghiệm cụ thể tạo ra; không còn lựa chọn dựa trên test.

### Tuần 9 — 04–10/12: đánh giá cuối và phân tích lỗi

- [ ] Chạy đánh giá cuối với các cấu hình đã khóa; lưu dự đoán, cấu hình, phiên bản dữ liệu và lệnh tái lập.
- [ ] Báo riêng NER, RE dùng gold entities, RE toàn hệ thống và normalization.
- [ ] Phân tích 30–50 lỗi: span, loại, sinh cặp, phủ định, thiếu ngữ cảnh, thuốc–liều và tra sai mã.
- [ ] Đo tốc độ trên thiết bị đã ghi rõ; tách tra mã online và cache, có warm-up và báo phân vị nếu đủ mẫu.
- [ ] Hoàn thiện demo, quay video dự phòng và viết chương kết quả bằng số liệu thật.

**Đầu ra:** bảng kết quả cuối, phân tích lỗi, hình minh họa, video demo và chương kết quả.

**Điều kiện qua tuần:** truy được mọi con số về kết quả chạy. Nếu phát hiện lỗi triển khai nghiêm trọng sau test, ghi rõ sửa gì và chạy lại nhất quán; không âm thầm tuning trên test.

### Tuần 10 — 11–17/12: hoàn thiện luận văn bản đầy đủ

- [ ] Ghép bản thảo: mở đầu, cơ sở và liên quan, dữ liệu/phương pháp, hệ thống, thực nghiệm, kết luận.
- [ ] Kiểm tra tính nhất quán giữa schema, sơ đồ, mã nguồn, bảng kết quả và phần mô tả đóng góp.
- [ ] Kiểm tra từng tài liệu tham khảo và mọi phát biểu định lượng; bỏ trích dẫn AI không xác minh được.
- [ ] Nêu rõ giới hạn miền spoken text, dữ liệu nhỏ, nhãn hiếm, mô hình kế thừa và mức kiểm duyệt thực tế.
- [ ] Gửi GVHD bản hoàn chỉnh để nhận phản hồi; sinh viên thực hiện việc gửi.

**Đầu ra:** bản luận văn đầy đủ đầu tiên, phụ lục guideline và nhật ký thí nghiệm.

**Điều kiện qua tuần:** GVHD có thể đọc xuyên suốt; không còn chương trống hoặc bảng điểm dự kiến.

### Tuần 11 — 18–24/12: sửa theo phản hồi và kiểm tra tái lập

- [ ] Xử lý góp ý theo mức ảnh hưởng: sai phương pháp/số liệu trước, trình bày sau.
- [ ] Cài môi trường mới hoặc nhờ người khác chạy theo hướng dẫn; xác nhận demo và một thí nghiệm đại diện tái lập được.
- [ ] Chuẩn bị README, phiên bản thư viện, đường dẫn checkpoint, cấu hình, quy trình dữ liệu và lệnh đánh giá.
- [ ] Chuẩn bị slide theo thời lượng của trường; mỗi kết luận chính có bằng chứng tương ứng.
- [ ] Luyện trả lời về baseline, split, nhãn do AI hỗ trợ, đóng góp cá nhân và giới hạn áp dụng.

**Đầu ra:** bản sửa gần cuối, gói tái lập, slide và danh sách câu hỏi bảo vệ.

**Điều kiện qua tuần:** một người khác làm theo hướng dẫn chạy được; sinh viên giải thích được các quyết định chính mà không đọc câu trả lời AI.

### Tuần 12 — 25–31/12: đóng gói, nộp và bảo vệ thử

- [ ] Rà quy cách trường, số trang, mục lục, hình/bảng, trích dẫn, tệp nộp và thủ tục liên quan.
- [ ] Bảo vệ thử ít nhất hai lượt có bấm giờ, một lượt giả lập demo lỗi hoặc mất mạng.
- [ ] Chuẩn bị demo chạy bằng dữ liệu/cache phù hợp, video dự phòng và ví dụ thể hiện giới hạn.
- [ ] Khóa phiên bản nộp: mã nguồn, luận văn, slide, checkpoint, cấu hình và kết quả; kiểm tra quyền chia sẻ trước khi đưa dữ liệu vào gói công khai.
- [ ] Dùng phần thời gian còn lại sửa lỗi và tập trình bày, không mở thêm hướng nghiên cứu.

**Đầu ra:** bộ hồ sơ nộp và bộ bảo vệ hoàn chỉnh.

**Điều kiện kết thúc:** đáp ứng danh sách ở mục 8 và yêu cầu nộp thực tế của trường.

## 5. Giao thức đánh giá đề xuất để chốt ở tuần 1

**NER:** precision/recall/F1 ở mức thực thể khớp chính xác span và loại; báo micro và từng loại. Relaxed F1 là phụ, không thay strict. Phân biệt điểm nhãn nguồn với điểm schema đích.

**RE với gold entities:** positive micro-F1 làm chỉ số chính đề xuất, bổ sung macro và P/R/F1/support từng quan hệ. Cạnh dương dự đoán trên cặp âm là FP; không cộng độ chính xác NO_RELATION vào F1 quan hệ dương.

**RE toàn hệ thống:** cạnh đúng cần khớp hai span, loại thực thể, chiều và nhãn quan hệ. Cạnh gold mất một đầu mút NER vẫn là FN. Đối chiếu bằng span/type, không dựa vào ID cục bộ. Báo thêm candidate recall để tách lỗi sinh cặp khỏi lỗi phân loại.

**Normalization:** báo tỷ lệ thực thể nhận được mã, độ đúng của mã trong số đã gán và độ đúng trên toàn bộ mention có gold phù hợp. Chốt mức chi tiết mã và tập mã chấp nhận trước khi đánh giá; tách gold mentions và predicted mentions nếu đo cả hệ thống. Không dùng cache lookup thành công làm bằng chứng mã đúng.

**Độ bất định:** ghi support, báo mean/SD khi có nhiều seed; có thể thêm khoảng tin cậy bằng lấy mẫu lại theo đơn vị văn bản nếu phù hợp. Lớp không có gold dương phải ghi thiếu bằng chứng, không diễn giải như đã giải quyết tốt lớp đó.

**Tính độc lập:** chỉ train/dev dùng phát triển. Kiểm toán lịch sử checkpoint và test cũ; test từng được dùng sửa luật không còn hoàn toàn mới. Khi không thể tạo tập độc lập, công bố giới hạn thay vì khẳng định không có rò rỉ.

Kiến trúc entity-first và dấu đánh dấu thực thể có thể tham khảo [PURE](https://aclanthology.org/2021.naacl-main.5/). Đây là cơ sở thiết kế, không bảo đảm kết quả trên corpus y tế tiếng Việt.

## 6. Cách phối hợp với AI

Nhịp làm việc mỗi tuần: lập mục tiêu đầu tuần; thực hiện các việc nhỏ có đầu ra; cuối tuần demo, cập nhật bằng chứng và quyết định tuần tiếp theo. Viết luận văn song song với nghiên cứu từ tuần 1.

AI hỗ trợ soạn bộ đọc dữ liệu, kiểm tra offset, mã huấn luyện/đánh giá, đề xuất ca kiểm thử, tổng hợp log, vẽ biểu đồ, rà tính nhất quán và chỉnh diễn đạt. Giao từng việc rõ đầu vào, đầu ra, dữ liệu được dùng và tiêu chí hoàn tất; không giao một yêu cầu bao trùm rồi nhận toàn bộ mã mà chưa đọc.

Sinh viên chịu trách nhiệm hiểu bài toán, đọc nguồn gốc, chốt nhãn/giao thức với người hướng dẫn, kiểm chứng số liệu và bảo vệ quyết định. Nhãn AI chỉ là gợi ý; giữ tách bản nháp, bản người duyệt và phiên bản gold. Dev/test nên có quy trình duyệt độc lập khỏi dự đoán của mô hình đang đánh giá.

Sau mỗi tính năng, sinh viên phải: giải thích được nó làm gì; chạy một ví dụ đúng và một ví dụ sai; chỉ ra bằng chứng hoàn tất. Lưu các quyết định và hỗ trợ của AI theo yêu cầu thực tế của trường.

## 7. Điều chỉnh khi chậm hoặc thiếu nguồn lực

- **Thiếu quan hệ dương:** phát hiện ở tuần 2; bổ sung nguồn/mẫu thật theo quy tắc lấy mẫu đã ghi. Giữ test đại diện hoặc công bố rõ nếu là tập thử thách chọn lọc. Không ép nhãn để đủ số và không tìm mẫu dựa trên lỗi mô hình test.
- **Người duyệt bận:** ưu tiên pilot và ca mơ hồ sớm; giảm corpus về quy mô khả thi, công bố số thực tế. Không gắn nhãn “bác sĩ kiểm duyệt” cho phần chưa được duyệt.
- **Không đủ GPU:** dùng encoder đóng băng với pooling thực thể và classifier, hoặc mô hình tuyến tính trên đặc trưng. Ghi đúng thiết lập; không gọi đó là fine-tune toàn encoder.
- **Không tái lập được NER cũ:** kiểm tra provenance, cấu hình và data split. Quyết định tái huấn luyện trong phạm vi đã chốt hoặc công bố checkpoint là giới hạn nghiên cứu.
- **RE không hơn luật:** phân tích dữ liệu, số mẫu, lỗi và độ bất định; báo cáo trung thực. Không tiếp tục thêm mô hình chỉ để tìm một bảng điểm đẹp.
- **Chậm hai tuần:** cắt giao diện phụ, ablation phụ, mô hình phụ và mở rộng ontology trước. Giữ kiểm duyệt, baseline, đánh giá độc lập, phân tích lỗi và thời gian viết/bảo vệ.

## 8. Danh sách hoàn thành

- [ ] Đề tài có phạm vi và câu hỏi nghiên cứu đã thống nhất.
- [ ] Corpus có nguồn, split, guideline, trạng thái duyệt và thống kê support.
- [ ] Có bằng chứng kiểm tra chất lượng nhãn; công bố đúng phần AI hỗ trợ và người duyệt.
- [ ] NER, RE, normalization và demo chạy được; phần kế thừa và tự làm được phân biệt.
- [ ] Có baseline, mô hình chính, đánh giá thành phần và toàn hệ thống với dữ liệu phù hợp.
- [ ] Mọi kết quả trong luận văn có tệp dự đoán/log/cấu hình hỗ trợ; không dùng kết quả cũ như kết quả vừa chạy.
- [ ] Có phân tích lỗi, giới hạn và khả năng tái lập đã thử thực tế.
- [ ] Luận văn, phụ lục, slide, video dự phòng và hồ sơ nộp hoàn chỉnh.
- [ ] Sinh viên giải thích được schema, chống rò rỉ dữ liệu, cách tính metric và đóng góp của mình.

## 9. Ba việc bắt đầu ngay

1. Viết đề cương hai trang và danh sách quyết định cần chốt với GVHD, dựa trên phạm vi ở mục 2.
2. Kiểm tra trạng thái duyệt thật của bộ 600 mẫu; chọn 50–80 mẫu pilot để đo tốc độ và độ phủ nhãn.
3. Lập sổ thí nghiệm và đề cương luận văn; mỗi tuần cập nhật một bản có số liệu hoặc bằng chứng mới.

Trong lần lập kế hoạch này chỉ bổ sung tài liệu; chưa huấn luyện mô hình, thay đổi dữ liệu hoặc xác nhận kết quả thực nghiệm.

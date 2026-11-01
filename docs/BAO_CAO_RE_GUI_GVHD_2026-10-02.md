# Báo cáo phương án triển khai RE

Khóa luận trích xuất thông tin y tế tiếng Việt • Ngày 02 tháng 10 năm 2026

## 1 Mục tiêu và phạm vi nghiên cứu

Phần Relation Extraction (RE) nhằm xác định quan hệ giữa các thực thể y tế trong văn bản tiếng Việt, bổ sung cho hệ thống nhận diện thực thể (NER) và chuẩn hóa mã bệnh, mã thuốc hiện có. Báo cáo đề xuất phương án chuẩn bị dữ liệu, thiết kế mô hình, đánh giá và triển khai trong ba tuần. **Hiện chưa có mô hình RE đã huấn luyện hoặc kết quả thực nghiệm RE; các chỉ tiêu dưới đây là kế hoạch đề xuất.**

### Phạm vi quan hệ

Giữ sáu loại thực thể CONDITION, DRUG, BODY_PART, TEST, PROCEDURE và DOSAGE. CONDITION bao gồm bệnh và triệu chứng theo schema của đề tài. Giai đoạn đầu tập trung vào quan hệ được thể hiện trực tiếp trong cùng câu hoặc cùng phát ngôn ngắn, với chiều cố định như sau.

| Quan hệ | Chiều thực thể | Ý nghĩa |
|---|---|---|
| located_at | CONDITION → BODY_PART | Tình trạng xuất hiện tại bộ phận cơ thể được nêu. |
| treated_by | CONDITION → DRUG | Thuốc được nêu để điều trị tình trạng. |
| treated_by_procedure | CONDITION → PROCEDURE | Thủ thuật được nêu để điều trị tình trạng. |
| diagnosed_by | CONDITION → TEST | Phương pháp được nêu để xác định hoặc chẩn đoán tình trạng. |
| has_dosage | DRUG → DOSAGE | Thông tin liều được nêu là thuộc thuốc. |

NO_RELATION là nhãn âm cho cặp đúng kiểu nhưng không có quan hệ được xác nhận trong văn bản. Hai thực thể cùng xuất hiện không đủ để gán quan hệ dương. Quan hệ qua nhiều câu, đồng tham chiếu và thay đổi NER để nhận diện thực thể lồng nhau được dành cho giai đoạn phát triển sau.

### Nền tảng hiện có

Hệ thống đã có checkpoint NER, xử lý sáu loại thực thể và chuẩn hóa CONDITION theo ICD-10, DRUG theo RxNorm. Báo cáo đánh giá lưu trước đó trên 3.497 mẫu VietMed-NER ghi strict micro-F1 = 0,6223 và relaxed micro-F1 = 0,7536. Các số này phản ánh NER, chưa được chạy lại trong báo cáo này và không phải kết quả RE.

Gói dữ liệu pilot có sẵn gồm 80 đoạn, 247 thực thể và 180 cặp ứng viên; các cặp chưa được gán nhãn quan hệ và chưa được kiểm duyệt để làm dữ liệu huấn luyện. Đây là đầu vào để bắt đầu hoàn thiện hướng dẫn gán nhãn.

### Câu hỏi nghiên cứu và đóng góp dự kiến

- Mô hình RE dùng encoder có cải thiện so với baseline bằng luật trên cùng corpus hay không?
- Chất lượng RE thay đổi thế nào khi chuyển từ thực thể đã kiểm duyệt sang thực thể do NER dự đoán?
- Lỗi chủ yếu xuất phát từ dữ liệu, nhận diện thực thể, sinh cặp hay phân loại quan hệ?

Đóng góp dự kiến gồm một corpus RE tiếng Việt quy mô nhỏ có hướng dẫn gán nhãn, mô hình và pipeline tái lập được, cùng phân tích độ phủ và ảnh hưởng của lỗi NER.

<!-- PAGE -->

## 2 Chuẩn bị dữ liệu và kiểm duyệt

### Nguồn dữ liệu và quy mô đề xuất

Sử dụng [VietMed-NER của tác giả](https://huggingface.co/datasets/leduckhai/VietMed-NER) làm nguồn chính, tận dụng văn bản và annotation thực thể rồi bổ sung nhãn quan hệ. Đây là dữ liệu lời nói y tế tiếng Việt, chưa có gold RE cho năm quan hệ của đề tài; khả năng áp dụng sang bệnh án cần được đánh giá riêng. Căn cứ mô tả dữ liệu: [bài NAACL 2025](https://aclanthology.org/2025.naacl-industry.59/).

| Tập dữ liệu | Số đoạn mục tiêu | Nguồn và mục đích |
|---|---:|---|
| Train | 400 | Official train; huấn luyện và phát triển luật. |
| Dev | 100 | Official validation; chọn mô hình và ngưỡng. |
| Test | 100 | Official test; đánh giá cuối sau khi khóa cấu hình. |

600 đoạn là mục tiêu có điều kiện sau pilot. Định hướng độ phủ là khoảng 60 quan hệ dương/nhãn trong train và 15–20 trong mỗi dev/test, tương đương 450–500 cạnh dương toàn corpus. Nếu không đạt, báo số mẫu thực tế và giới hạn từng nhãn, không bổ sung nhãn bằng suy đoán.

### Quy trình gán nhãn

1. Cố định văn bản và vị trí ký tự. Lưu riêng văn bản gốc và văn bản dùng annotation; gold và dự đoán NER phải được đối chiếu trên cùng chuỗi.
2. Rà thực thể trước khi nối quan hệ: sửa span, sửa loại, thêm thực thể bỏ sót và xóa nhận nhầm. Mỗi lần xuất hiện có ID riêng.
3. Sinh lại các cặp đúng kiểu, duyệt Có, Không hoặc Chưa rõ; chỉ gán dương khi có bằng chứng nối chính hai thực thể đó.
4. Hoàn tất pilot80 để đo thời gian, số nhãn dương, tỷ lệ âm và các ca mơ hồ; chốt guideline trước khi đánh đại trà.
5. Kiểm tra chất lượng, giải quyết bất đồng rồi khóa phiên bản dữ liệu, split, guideline và checksum.

Pilot kết hợp lấy mẫu ngẫu nhiên và ưu tiên kiểu cặp nên không đại diện phân bố tự nhiên; thống kê nhóm ngẫu nhiên riêng. Có thể dùng phiếu kiểm duyệt hiện có; khi mở rộng, [Label Studio RE](https://labelstud.io/templates/relation_extraction) hỗ trợ đánh span và nối quan hệ.

### Quy tắc chất lượng và tính độc lập

Cặp chưa duyệt không được tự chuyển thành NO_RELATION. Chỉ xác nhận một đoạn hoàn tất khi mọi cặp trong phạm vi đã có quyết định. Phủ định, câu hỏi chưa khẳng định, thông tin liều không rõ thuộc thuốc nào và thực thể lồng nhau phải có quy tắc thống nhất. DOSAGE cần phân biệt thuộc tính liều thuốc với số đo khác.

Nếu có người thứ hai, gán độc lập khoảng 20% và đo Cohen’s kappa, positive relation F1 trước hòa giải. Nếu chỉ một người, rà lại 15–20% sau ít nhất 48 giờ, giấu nhãn cũ và công bố giới hạn kiểm duyệt. JSONL lưu nguồn, text, entity IDs/type/span, các cạnh và quyết định cho từng cặp; kiểm tra text[start:end] trùng surface_text.

Giữ split nguồn, chia theo văn bản/nhóm hội thoại trước khi sinh cặp và kiểm tra trùng xuyên split. Chưa xác minh được conversation ID; không ghép các hàng liền kề. Cần rà lịch sử checkpoint NER và tuning để đánh giá nguy cơ rò rỉ dữ liệu. Điều khoản tái sử dụng và phát hành lại corpus được xác minh trước khi công bố dữ liệu.

<!-- PAGE -->

## 3 Thiết kế kỹ thuật của mô hình RE

### Kiến trúc đề xuất

**Văn bản → NER → thực thể có ID → cặp đúng kiểu → encoder RE → classifier → các cạnh quan hệ.** Giữ checkpoint NER hiện có để suy luận; huấn luyện RE thành checkpoint riêng. Khi train RE dùng thực thể đã kiểm duyệt; khi đánh giá toàn pipeline dùng thực thể NER dự đoán nguyên trạng. Chuẩn hóa ICD-10/RxNorm là thông tin bổ sung, không phải điều kiện để RE hoạt động.

Mô hình chính khởi tạo từ [ViHealthBERT base syllable](https://huggingface.co/demdecuong/vihealthbert-base-syllable), encoder miền y tế tiếng Việt được giới thiệu trong [ViHealthBERT LREC 2022](https://aclanthology.org/2022.lrec-1.35/). Thiết kế pipeline và marker có loại thực thể tham khảo [PURE NAACL 2021](https://aclanthology.org/2021.naacl-main.5/); đây là cơ sở kiến trúc, chưa chứng minh kết quả cho dữ liệu của đề tài.

### Biểu diễn cặp và hàm mất mát

Chèn marker quanh hai thực thể theo vị trí ký tự, đăng ký thành special tokens và mở rộng embedding. Ví dụ minh họa tự soạn cho cặp CONDITION → DRUG:

```text
[H_CONDITION] Đau đầu [/H_CONDITION] được điều trị bằng
[T_DRUG] Paracetamol [/T_DRUG] 500 mg.
```

Ghép hidden state tại marker mở của head và tail thành vector 2d; với hidden size 768, vector có 1.536 chiều. Qua dropout và lớp tuyến tính để tạo sáu logits, gồm năm quan hệ dương và NO_RELATION. Dùng cross-entropy trên logits đã mask theo kiểu cặp.

Mỗi kiểu cặp chỉ có một nhãn dương hợp lệ; ví dụ CONDITION → DRUG chỉ giữ treated_by và NO_RELATION, mask bốn nhãn dương còn lại trước softmax. Vì vậy, quyết định là có/không quan hệ có điều kiện theo kiểu, không phải sáu lớp cạnh tranh tự do. Ngữ cảnh vẫn quyết định quan hệ; loại thực thể không tự trở thành đáp án dương.

### Cấu hình huấn luyện khởi điểm

| Hạng mục | Đề xuất |
|---|---|
| Optimizer | AdamW; encoder LR 2e-5 hoặc 3e-5, classifier LR 1e-4. |
| Batch và epoch | Batch 8; tích lũy 2 bước khi cần; tối đa 8 epochs, early stopping patience 2. |
| Regularization | Dropout 0,1; weight decay 0,01; warmup 10%; gradient clipping 1,0. |
| Lựa chọn | Tối đa 2 learning rates trên dev; chọn theo positive micro-F1. |
| Ngưỡng và seeds | Khởi điểm 0,5, tuning dev; ít mẫu thì dùng ngưỡng chung; 3 seeds nếu đủ ngân sách. |

Đầu tiên dùng toàn bộ âm đã duyệt. Nếu âm áp đảo, thử lấy tối đa khoảng 3 âm/1 dương ở train và giữ âm khó; dev/test giữ nguyên. Các giá trị là cấu hình khởi điểm, chưa được xác nhận tối ưu.

### Tích hợp và kiểm tra chức năng

Đọc giới hạn thực tế của encoder; khởi điểm khoảng 240 token tổng kể cả marker, xác minh bằng forward pass. Crop phải giữ cả hai thực thể; quan hệ bị mất do window phải được thống kê. Kiểm tra offset, mention lặp, marker, hai thuốc có hai liều, phủ định và NER bỏ một đầu mút. Lưu revision, cấu hình, seed, checkpoint và cache NER để tái lập thí nghiệm.

<!-- PAGE -->

## 4 Benchmark và phương pháp đánh giá

### Các hệ thống so sánh trên cùng corpus

| Hệ thống | Thiết lập | Gold RE F1 | Strict NER → RE F1 |
|---|---|---|---|
| B0 Luật | Trigger, cấu trúc cục bộ, phủ định, nối thuốc–liều. | Chưa đo | Chưa đo |
| B1 ViHealthBERT | Marker có loại thực thể, fine-tune RE. | Chưa đo | Chưa đo |
| B2 Ablation tùy ngân sách | Marker chỉ head/tail; giữ encoder và type mask. | Chưa đo | Chưa đo |

B0 chỉ phát triển trên train/dev. B2 kiểm tra đóng góp của type trong biểu diễn encoder; vẫn có type mask nên không coi là loại bỏ mọi thông tin loại. Ưu tiên hoàn tất B0 và B1 trước thí nghiệm phụ.

### Hai chế độ đánh giá

**RE trên gold entities:** dùng span và loại thực thể đã kiểm duyệt; báo precision, recall, micro-F1 của năm nhãn dương, macro-F1 và P/R/F1/support từng nhãn. NO_RELATION không nằm trong positive F1, nhưng dự đoán cạnh dương trên cặp âm vẫn là false positive. F1 = 2TP / (2TP + FP + FN).

**Strict NER → RE:** một cạnh đúng khi cả hai span, loại, chiều và nhãn quan hệ khớp gold. Cạnh gold bị thiếu một đầu mút vẫn tính false negative; cạnh từ entity giả là false positive. Đối chiếu bằng span/type, không dựa vào ID nội bộ. Đo thêm candidate recall và tỷ lệ cạnh gold có đủ hai đầu mút NER đúng.

Test không dùng chọn luật, checkpoint hoặc ngưỡng. Macro-F1 tính trên năm nhãn với zero_division=0; lớp support=0 được ghi thiếu bằng chứng. Với test 15–20 cạnh dương/nhãn, một FN thay đổi recall khoảng 5–6,7 điểm phần trăm, cần báo độ bất định. Nếu chạy 3 seeds, báo mean ± SD; không chọn seed tốt nhất trên test.

### Benchmark công bố để tham khảo

| Benchmark và thiết lập | Điểm công bố | Vai trò tham khảo |
|---|---|---|
| [i2b2 VA 2010](https://pmc.ncbi.nlm.nih.gov/articles/PMC3168320/), RE trên gold concepts | Best F1 0,737 | Quan hệ problem–treatment/test gần một phần schema. |
| [n2c2 2018](https://pmc.ncbi.nlm.nih.gov/articles/PMC7489085/), gold-concept RE | Best lenient micro-F1 0,9630 | Liên kết thuốc–thuộc tính; strength và dosage tách riêng. |
| [n2c2 2018](https://pmc.ncbi.nlm.nih.gov/articles/PMC7489085/), end-to-end | Best lenient micro-F1 0,8905 | Tham khảo cách tách RE độc lập và toàn pipeline. |
| [PURE ACE05](https://aclanthology.org/2021.naacl-main.5/), BERT-base cùng câu | Strict Rel+ F1 63,9% | Cơ sở cho pipeline và typed markers. |

Các điểm khác corpus, ngôn ngữ và matching nên không so sánh trực tiếp hoặc đặt làm mục tiêu F1 của đề tài. Hai điểm n2c2 tốt nhất có thể thuộc hai hệ thống khác nhau; không dùng chênh lệch đó để định lượng riêng lỗi NER. Bảng PURE lấy từ bảng 1 của bài báo.

Đo latency RE riêng và toàn pipeline trên cùng thiết bị, ghi warm-up, batch, cặp/đoạn, mean/P50/P95, peak VRAM và trạng thái normalization online/cache. Phân tích 30–50 lỗi theo span/type, sinh cặp/window, thuốc–liều, phủ định và thiếu ngữ cảnh. Không suy điểm RE bằng cách nhân hoặc bình phương NER F1.

<!-- PAGE -->

## 5 Tính khả thi và kế hoạch thực hiện

### Nguồn lực và ngân sách thời gian

Lịch giả định từ **05 đến 25/10/2026**, gồm 21 ngày liên tục, kể cả cuối tuần. Ngân sách 4–5 giờ/ngày tương đương 84–105 giờ; phương án 600 đoạn dự kiến cần 91 giờ làm việc chủ động. GPU và người kiểm duyệt thứ hai chưa được xác nhận; thời gian GPU chạy chưa được benchmark.

| Hạng mục | Ngân sách giờ dự kiến |
|---|---:|
| Chuẩn bị và kiểm duyệt dữ liệu | 45 |
| Sinh cặp, baseline, mô hình và tích hợp | 18 |
| Huấn luyện và lựa chọn trên dev | 8 |
| Benchmark, latency và phân tích lỗi | 10 |
| Báo cáo và gói kết quả | 5 |
| Dự phòng | 5 |
| Tổng | 91 |

45 giờ dữ liệu gồm 6 giờ thiết lập, 30 giờ gán 600 đoạn ở mức 3 phút/đoạn, 6 giờ rà chất lượng và 3 giờ khóa dữ liệu; đã bao gồm pilot. Tốc độ 4 phút/đoạn làm tổng tăng khoảng 10 giờ. Người duyệt thứ hai cần thêm 4–6 giờ riêng nếu có.

### Lịch và sản phẩm dự kiến

| Thời gian | Công việc và sản phẩm |
|---|---|
| 05–11/10 | Guideline, pilot80, quyết định 600/400; hướng tới 300–350 đoạn đã duyệt. Bắt đầu sinh cặp và baseline trên train. |
| 12–18/10 | Khóa dữ liệu dự kiến 14/10; hoàn thiện B0 và huấn luyện B1, chọn cấu hình trên dev. |
| 19–25/10 | Tích hợp; khóa cấu hình trước 22/10, đánh giá test, phân tích lỗi, latency và báo cáo/demo. |

### Điều kiện tiếp tục và phương án dự phòng

- **Dữ liệu:** quyết định cuối ngày 3 từ pilot. Giữ 600 nếu vừa ngân sách và có khả năng bổ sung nhãn hiếm. Nếu chậm hoặc chỉ có 4 giờ/ngày, giảm còn 400 đoạn, dự kiến 280/60/60; cắt B2 và seeds phụ, giữ kiểm duyệt.
- **Phần cứng:** GPU 12–16 GB là giả định cần đo thực tế. Nếu thiếu GPU, chuyển sang mô hình nhẹ như TF-IDF + logistic regression hoặc encoder đóng băng, ghi rõ thiết lập.
- **Độ phủ:** lớp ít mẫu chỉ kết luận thăm dò. RE không khôi phục cạnh mất đầu mút NER; VietMed spoken chưa chứng minh khả năng dùng trên bệnh án thực tế.

### Sản phẩm hoàn thành và nội dung cần thống nhất

Bộ sản phẩm gồm corpus có phiên bản, guideline, baseline, mô hình RE, hai chế độ đánh giá, phân tích lỗi và demo JSON tái lập được. Kết quả chưa vượt baseline vẫn được báo cáo cùng giới hạn.

Kính đề nghị giáo viên hướng dẫn góp ý về phạm vi DOSAGE, quy tắc phủ định/câu hỏi, quy mô sau pilot, baseline/metric và khả năng bố trí người kiểm duyệt.

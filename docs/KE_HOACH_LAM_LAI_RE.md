# Kế hoạch làm lại RE từ đầu (3 ngày, lập 2026-11-19, sửa lần 1)

## Phạm vi

Làm lại toàn bộ phần RE: lược đồ, hướng dẫn gán nhãn, chọn mẫu, gán nhãn, sinh dữ liệu, mô hình và đánh giá.

**Không dùng lại bất kỳ nhãn RE cũ nào**, gồm VM600 (`re_gold_v1`), `re_ai_v2`, `golden_test`, `re_test_random_v1`, dữ liệu dịch và dữ liệu sinh trong `re_v3/`. Dữ liệu cũ để nguyên trên đĩa, không đi vào huấn luyện hay đánh giá. Chỉ dùng **văn bản và nhãn NER gốc của VietMed-NER**.

## Quy mô

| Tập | Số câu | Nguồn câu | Mục đích |
|---|---:|---|---|
| Seed train | **600** | VietMed train + validation | Học trực tiếp và làm hạt giống để sinh dữ liệu |
| Test | **100** | VietMed test | Đánh giá cuối cùng, do người gán |
| Dev | khoảng 10% seed (60 câu), tách ra từ 600 câu seed | như seed | Chọn tham số và chọn cách sinh dữ liệu |

## Thiết kế

### 1. Tách hai câu hỏi

| Bước | Câu hỏi | Gán ở mức |
|---|---|---|
| A. Kiểm tra thực thể | Mention có thật sự đúng kiểu không, ví dụ "kiểm soát" có phải DRUG không? | mỗi mention |
| B. Quan hệ | Hai thực thể đều hợp lệ thì câu có nói chúng có quan hệ không? | mỗi cặp |

Cặp chứa thực thể không hợp lệ thì không gán nhãn quan hệ. Khi chạy thật, bước A là một bộ lọc riêng đặt trước RE.

### 2. Lược đồ

Bản mặc định giữ 5 quan hệ. Sau bước chọn mẫu, đếm số cặp dương ước tính của từng quan hệ trong kho. Quan hệ nào có dưới 20 cặp dương thì bỏ và ghi lý do vào báo cáo.

### 3. Hướng dẫn gán nhãn

Viết mới dựa trên câu thật. Với mỗi quan hệ, hướng dẫn gồm:

- định nghĩa;
- 3 ví dụ dương và 3 ví dụ âm;
- quyết định cho các trường hợp mơ hồ: tác dụng phụ, phòng bệnh, phủ định, câu hỏi, giả định, kế hoạch tương lai, bệnh chung chung, hai mệnh đề khác nhau.

Bạn duyệt rồi khóa hướng dẫn trước khi bắt đầu gán nhãn.

### 4. Chọn mẫu chủ động: ưu tiên câu nhiều quan hệ dương

Chưa có nhãn thì chưa biết câu nào có quan hệ dương. Vì vậy mỗi câu được chấm một **điểm khả năng dương**, rồi chọn các câu có điểm cao.

Cách tính điểm cho từng câu:

1. **Bỏ thực thể nhiễu** theo danh sách mention hay bị gán sai kiểu.
2. **Chấm điểm từng cặp ứng viên.** Một cặp được cộng điểm khi:
   - hai thực thể đứng gần nhau (không quá 4 từ);
   - có từ gợi ý của quan hệ, ví dụ "điều trị bằng", "uống", "ở", "xét nghiệm";
   - luật cho nhãn dương.
3. **AI sàng lọc nhanh.** Một lượt AI đọc câu và đoán "có quan hệ dương không". Kết quả này chỉ dùng để chọn câu, không dùng làm nhãn.
4. **Điểm của câu** là tổng điểm các cặp trong câu.

Chọn theo hạn mức của từng quan hệ, để lớp hiếm không bị located_at lấn át:

| Quan hệ | Mục tiêu: số câu có ít nhất một ứng viên mạnh, trong 600 câu seed |
|---|---:|
| located_at | khoảng 150 |
| treated_by | khoảng 150 |
| treated_by_procedure | khoảng 150 |
| diagnosed_by | toàn bộ câu có ứng viên mạnh, dự kiến khoảng 80 |
| has_dosage | toàn bộ câu có ứng viên mạnh |
| Câu ngẫu nhiên | khoảng 60, để mô hình vẫn thấy phân bố tự nhiên và cặp âm thật |

**Tập test 100 câu** chọn cùng cách. Có khoảng 15 câu ngẫu nhiên, phần còn lại theo hạn mức, mỗi quan hệ ít nhất 10 câu có ứng viên mạnh.

Hệ quả cần ghi rõ trong báo cáo: tập test được làm giàu cặp dương. Vì vậy precision đo trên tập này sẽ cao hơn so với khi chạy trên phân bố thật. Báo cáo kèm kết quả riêng trên 15 câu ngẫu nhiên, coi như tham khảo vì số câu ít.

Kiểm tra bắt buộc: không có câu nào nằm ở hai tập, kiểm tra cả trùng câu và chung 8-gram.

### 5. Ai gán nhãn

| Tập | Người gán | Ghi chú |
|---|---|---|
| Test 100 câu (khoảng 250–300 cặp) | **Bạn, gán mù**: không thấy nhãn AI hay nhãn luật | Phiếu Excel, gán bước A rồi đến bước B |
| Test, lần thứ hai | AI, độc lập với bạn | Đo độ đồng thuận κ giữa AI và người |
| Seed 600 câu (khoảng 1.500 cặp) | AI, 2 lượt độc lập, cùng hướng dẫn | Cặp mà 2 lượt không thống nhất được ưu tiên đưa cho người duyệt |
| Duyệt seed | **Bạn, khoảng 150 cặp**: mọi cặp bất đồng, phần còn lại là cặp dương của lớp hiếm | Cặp đã duyệt mang nhãn của người |

Ngưỡng định trước: κ của bước B trên tập test phải từ 0,6 trở lên. Nếu không đạt, seed chỉ dùng phần đã được người duyệt. Bước sinh dữ liệu cũng chỉ lấy câu đã duyệt làm hạt giống.

### 6. Sinh dữ liệu từ 600 câu seed

Chỉ sinh từ phần train của seed, không bao giờ từ dev hay test. Có ba cách sinh:

| Cách | Mô tả | Ràng buộc nhãn |
|---|---|---|
| Thay thực thể | Giữ câu seed, thay một thực thể bằng thực thể cùng kiểu và cùng nhóm chuyên khoa | Chỉ thay thực thể hợp lệ (bước A). Nhãn giữ nguyên. |
| Theo pattern | Khai thác pattern từ cặp dương của seed, rồi điền thực thể mới vào | Chỉ dùng pattern xuất hiện ở ít nhất 2 câu seed. |
| LLM diễn đạt lại | LLM viết lại câu seed theo văn nói, giữ hai thực thể và quan hệ | Có một lượt AI kiểm tra lại nhãn. Câu lệch nhãn bị loại. |

Bộ lọc chung cho dữ liệu sinh:

- kiểm tra định dạng;
- kiểm tra rò rỉ với test và dev (chung 8-gram);
- loại câu trùng;
- mỗi khung câu giữ tối đa 3 câu;
- tỉ lệ dương nằm trong khoảng 20–30%.

Lượng dữ liệu sinh và cách sinh được chọn bằng ablation trên tập dev, không phải trên test. Các mức thử là 0×, 1× và 3× so với số cặp seed.

### 7. Mô hình và đánh giá

- **Hệ so sánh:**
  - luật;
  - ViHealthBERT chỉ học seed;
  - ViHealthBERT học seed cộng dữ liệu sinh, với cấu hình tốt nhất trên dev;
  - mỗi hệ đều chạy thêm phiên bản hợp với luật.
- **Huấn luyện:** 3 seed cho mỗi hệ.
- **Chỉ số:** F1 dương micro và F1 theo từng quan hệ trên test, có KTC 95% bootstrap theo câu. Quan hệ nào có dưới 5 cặp dương trong test thì không kết luận.
- **Đánh giá đầu–cuối:** chạy NER của hệ thống, rồi bộ lọc thực thể, rồi RE trên 100 câu test.

## Lịch 3 ngày

### Ngày 1

| Việc | Ai làm | Thời gian |
|---|---|---|
| Dựng kho, chấm điểm khả năng dương, chọn 600 câu seed và 100 câu test | Claude | 2 giờ |
| Soạn hướng dẫn gán nhãn | Claude | 1,5 giờ |
| Duyệt và khóa hướng dẫn, lược đồ, danh sách câu đã chọn | **Bạn** | 45 phút |
| Lập phiếu gán mù cho test | Claude | 30 phút |
| Gán nhãn test, bước A và B | **Bạn** | 3–4 giờ |

### Ngày 2

| Việc | Ai làm | Thời gian |
|---|---|---|
| AI gán nhãn test, rồi tính κ | Claude | 1 giờ |
| AI gán nhãn seed 2 lượt, liệt kê cặp bất đồng | Claude | 3 giờ |
| Duyệt khoảng 150 cặp seed | **Bạn** | 1,5 giờ |
| Sinh dữ liệu (3 cách) và lọc | Claude | 2 giờ |
| Chạy ablation trên dev qua đêm: 0×, 1×, 3× × 3 seed | Claude, chạy trong tab Terminal | 4–5 giờ GPU |

### Ngày 3

| Việc | Ai làm | Thời gian |
|---|---|---|
| Chọn cấu hình tốt nhất trên dev, chấm một lần trên test, đánh giá đầu–cuối, phân tích lỗi | Claude | 2 giờ |
| Thay mô hình và pipeline trong code, chạy test | Claude, bạn duyệt trước khi commit | 2 giờ |
| Viết lại chương RE trong báo cáo | Claude soạn, bạn sửa | 3 giờ |

Tổng thời gian duyệt tay của bạn khoảng 400–450 cặp: test khoảng 250–300 cặp, seed khoảng 150 cặp.

## Cấu trúc thư mục mới

```
relation/             (không đặt tên re/ vì trùng module re của Python)
├── guideline.md          hướng dẫn gán nhãn (khóa sau ngày 1)
├── schema.json           lược đồ quan hệ
├── build_pool.py         dựng kho, lọc thực thể nhiễu
├── select.py             chấm điểm khả năng dương, chọn seed và test theo hạn mức
├── make_sheet.py         lập phiếu gán nhãn
├── import_sheet.py       nhập phiếu, kiểm tra
├── agreement.py          tính κ giữa AI và người
├── synth.py              sinh dữ liệu (3 cách)
├── filter.py             lọc dữ liệu sinh
├── train.py / evaluate.py
└── data/
    ├── pool.jsonl
    ├── selection.json    câu được chọn, điểm, lý do chọn
    ├── seed.jsonl, dev.jsonl
    ├── test.jsonl        nhãn người
    ├── test_ai.jsonl     nhãn AI, chỉ dùng để tính κ
    └── synthetic.jsonl
```

## Rủi ro

| Rủi ro | Cách xử lý |
|---|---|
| Kho không đủ câu có ứng viên mạnh cho lớp hiếm (diagnosed_by, has_dosage) | Lấy hết câu có ứng viên mạnh. Nếu vẫn dưới 20 cặp dương thì bỏ quan hệ đó, hoặc chỉ dựa vào dữ liệu sinh và ghi rõ trong báo cáo. |
| Tập test được làm giàu cặp dương nên làm kết quả trông đẹp hơn thực tế | Báo cáo kèm kết quả trên phần câu ngẫu nhiên, và nêu rõ thiết kế chọn mẫu. |
| Dữ liệu sinh làm mô hình học lối tắt | Chọn cấu hình trên dev. Giới hạn số câu mỗi khung. Thêm mẫu âm khó. |
| κ thấp | Chỉ dùng phần đã được người duyệt. Báo cáo κ như một kết quả. |
| Huấn luyện bị ngắt giữa chừng | Lưu kết quả sau từng seed. Chạy trong tab Terminal. |

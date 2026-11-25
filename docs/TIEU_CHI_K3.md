# Tiêu chí chấm K3 (ngữ cảnh câu sinh)

> **Nguồn gốc của tài liệu.** Prompt giao cho các tác tử LLM chấm K3 không được lưu thành file. Bộ tiêu chí dưới đây được **tổng hợp lại sau khi chấm** (ngày 24/11/2026), từ 2.874 lý do (`k3_rationale`) trong `relation/data/synth/validate/batches/k3_b0*.out.jsonl`. Tài liệu mô tả cách LLM **thực tế đã chấm**, không phải hướng dẫn được viết trước khi chấm.

## 1. Đầu vào và đầu ra

Mỗi câu sinh được giao cho LLM kèm theo (`batches/k3_bNN.jsonl`):

| Trường | Nội dung |
|---|---|
| `text_vi` | Câu sinh tiếng Việt |
| `parent_text_vi` | Câu thật gốc (chỉ có với `mention_replacement`) |
| `replaced` | Thực thể bị thay: `old_vi` → `new_vi` |
| `k1` | Các cụm từ mới tạo quanh thực thể được thay (đơn vị K1) |

LLM trả về (`batches/k3_bNN.out.jsonl`):

| Trường | Nội dung |
|---|---|
| `literal_en` | Bản dịch sát nghĩa từng chữ sang tiếng Anh, không làm mượt câu |
| `k3` | `plausible` hoặc `implausible`, không có mức "chưa chắc" |
| `k3_rationale` | Lý do bằng một câu |

## 2. Nguyên tắc chung

1. **Chấm nội dung, không chấm văn phong.** Từ đệm, câu bị cắt, lỗi phiên âm và câu lủng củng của lời nói không làm câu thành `implausible`. Ví dụ, SY-00025 được chấm *plausible* kèm ghi chú *"the phrasing is clumsy"*.
2. **Chấm trên bản dịch sát nghĩa**, để chỗ sai không bị bản dịch che đi.
3. **Câu `mention_replacement` được so với câu gốc.** Thực thể mới phải hợp với **mọi phần không đổi** của câu gốc, không chỉ với thực thể đi cùng nó trong cặp.
4. **Câu âm khó (`hard_negative`) phải là một phát biểu đúng.** Câu nói "X không liên quan đến Y" hay "Y không phát hiện được X" chỉ hợp lý khi điều đó **đúng về y khoa**. Nếu thực tế X và Y có liên quan thì câu là `implausible`, dù nhãn của cặp là NO_RELATION.

## 3. Tiêu chí `implausible`

Câu bị chấm `implausible` khi vi phạm ít nhất một tiêu chí dưới đây. Ví dụ lấy từ lý do thật, kèm mã câu.

| # | Tiêu chí | Ví dụ (mã câu: lý do của LLM) |
|---|---|---|
| **T1** | **Cụm từ không tồn tại hoặc phá vỡ từ ghép cố định.** Thực thể mới ghép với từ đứng cạnh thành cụm vô nghĩa. | SY-00673: "chàm vành" không phải bệnh. SY-00350: "cổ vai khớp" phá vỡ từ ghép "cổ vai gáy". SY-00134: "cục não bộ" phá vỡ "cục máu". |
| **T2** | **Sai chỉ định điều trị hoặc phòng bệnh.** Thuốc hay thủ thuật không dùng cho tình trạng đó. | SY-02440: metformin không điều trị mỡ máu. SY-02864: viêm gan không điều trị bằng phẫu thuật. SY-02913: thay khớp không phòng được đau nhức. |
| **T3** | **Sai xét nghiệm chẩn đoán.** Xét nghiệm không phát hiện được tình trạng đó. | SY-01492: viêm gan không chẩn đoán bằng nội soi. SY-01043: điện não đồ không phát hiện đau đầu. |
| **T4** | **Sai liều, đơn vị hoặc đường dùng.** | SY-01698: insulin tính bằng đơn vị, không phải mg. SY-01696: không thể tiêm một viên thuốc. SY-01766: colchicin 80 mg là liều gây tử vong. |
| **T5** | **Sai vị trí giải phẫu.** Tình trạng không xảy ra ở bộ phận đó, hoặc bộ phận không có chức năng mà câu gán cho nó. | SY-00527: tóc không thể bị nám. SY-00809: trong rung nhĩ, tâm nhĩ rung chứ không phải động mạch. SY-00107: động mạch không tiết bã nhờn. |
| **T6** | **Sai quan hệ nhân quả hoặc tác dụng phụ.** | SY-02515: thuốc kháng axit điều trị trào ngược, không gây trào ngược. SY-02366: metformin không gây đái tháo đường. SY-03201: phẫu thuật không gây xơ gan. |
| **T7** | **Không hợp với phần còn lại của câu.** Thực thể mới lạc nhóm trong câu liệt kê, hoặc mâu thuẫn với ngữ cảnh của câu gốc. | SY-00491: SARS-CoV-2 bị chèn vào danh sách triệu chứng. SY-00970: ho không phải bệnh mạn tính ngang với tim mạch và ung thư. SY-00270: chóng mặt không phải bệnh của trẻ liên quan đến sinh mổ, câu gốc nói về nhiễm trùng. |
| **T8** | **Câu phủ định hoặc tương phản nói sai sự thật** (áp dụng nguyên tắc 4 cho câu âm khó). | SY-02030: loãng xương có liên quan đến cột sống. SY-01031: bệnh lao có cần xét nghiệm. SY-01130: tầm soát ung thư chính là để phát hiện khối u. |

**Đối chiếu với nguồn đã công bố** (không phải nguồn gốc của tiêu chí):

- T2, T3, T5, T6 ứng với các quan hệ `treats`/`prevents`, `diagnoses`, `location_of`, `causes` của UMLS Semantic Network (Bodenreider, *Nucleic Acids Res.* 32, D267–D270, 2004).
- T4 ứng với các loại Improper Dose (70.2), Wrong Strength/Concentration (70.3) và Wrong Route (70.7) trong NCC MERP Taxonomy of Medication Errors (2001).
- T1 và T7 là lỗi đặc trưng của cách thay thực thể cùng kiểu (Dai & Adel, COLING 2020, tr. 3861–3867).
- T8 là quy ước riêng của khóa luận.

## 4. Ví dụ `plausible`

| Mã câu | Lý do của LLM |
|---|---|
| SY-01504 | Siêu âm tim cho thấy suy tim, đúng. |
| SY-01080 | Đúng: thoát vị đĩa đệm không chẩn đoán bằng đo mật độ xương (câu âm khó nói đúng sự thật). |
| SY-01981 | Viêm phổi ở đường hô hấp dưới trong khi họng bình thường là hợp lý. |
| SY-02705 | Corticoid có thể gây da nhờn hoặc nổi mụn (tác dụng phụ có thật). |
| SY-01815 | Omeprazol có dạng gói. |

## 5. Kết quả chấm

| Cách sinh | `plausible` | `implausible` | Tỉ lệ `implausible` |
|---|---|---|---|
| `mention_replacement` | 364 | 561 | 61% |
| `template` (mẫu dương) | 161 | 131 | 45% |
| `hard_negative` | 926 | 731 | 44% |
| **Tổng** | **1.451** | **1.423** | **50%** |

Theo đọc mẫu, lỗi của `mention_replacement` chủ yếu thuộc T1, T5 và T7, vì thực thể mới không hợp với phần câu gốc được giữ lại. Lỗi của `template` tập trung ở T4 (liều và đơn vị trong `has_dosage`). Lỗi của `hard_negative` chủ yếu thuộc T2, T3, T6 và T8. Tỉ lệ theo từng tiêu chí chưa được đếm chính xác, vì mỗi lý do có thể thuộc nhiều tiêu chí.

## 6. Độ tin cậy và hạn chế

- Người có chuyên môn y khoa duyệt mẫu (`relation/data/synth/validated/manifest.json`):
  - đồng ý với **90,3%** (241/267) câu hệ thống coi là hợp lệ;
  - chỉ đồng ý với **21,7%** (31/143) câu bị loại vì ngữ cảnh.
- Như vậy, khi chấm `plausible`, LLM đáng tin cậy. Khi chấm `implausible`, LLM **khắt khe hơn người duyệt**, có lúc loại cả câu đúng về y khoa. Các câu người duyệt giữ lại đã được đưa trở lại tập câu sinh.
- Vì tiêu chí được tổng hợp sau khi chấm, không thể khẳng định LLM đã áp dụng chúng nhất quán cho mọi câu.
- **Hướng cải thiện:** cố định prompt gồm các tiêu chí T1–T8 và vài ví dụ mẫu, đo độ đồng thuận với người duyệt trên một mẫu nhỏ, rồi mới chấm toàn bộ.

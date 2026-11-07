# Phiếu rà soát NER và RE 201 đến 300

Bản AI rà soát lần hai ngày 15/10/2026. Giữ nguyên câu nguồn và sáu loại NER, năm quan hệ RE. Chưa được chuyên gia xác nhận.

Quy tắc người dùng đã chốt: giữ cả cụm bệnh/triệu chứng trong một CONDITION. Không tách bộ phận bên trong cụm để tạo located_at. Vị trí được nêu riêng bằng giới từ hoặc mệnh đề riêng vẫn được xét.

Vị trí ký tự là khoảng [start, end), đếm từ 0 theo Unicode. Mã E ổn định khi sửa; mã R được tạo lại. Không dùng CHUA_RO làm nhãn huấn luyện hoặc nhãn âm.

## VM600-201

**Đoạn gốc:** động một cách trực tiếp chúng ta cần nhớ rằng là những người làm việc văn phòng mặc dù là không phải là gặp mưa gặp nắng

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

Không có thực thể thuộc sáu loại được giữ trong bản rà soát.

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

Nguồn: VietMed-NER train, dòng 1679 (từ 0).

## VM600-202

**Đoạn gốc:** đánh giá tự bác thì cũng có thể là điều chỉnh lại cái chế độ ăn để xem xem là mình có ăn thiếu chất không mình có thể

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

Không có thực thể thuộc sáu loại được giữ trong bản rà soát.

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- CONTEXT_OR_TRANSCRIPT: câu bị cắt, tham chiếu/mục đích chưa rõ hoặc nghi lỗi phiên âm; cần xem ngữ cảnh/audio gốc, không tự sửa văn bản.

### Thay đổi NER

- E2 “điều chỉnh” DRUG [35, 45) → ∅
- E1 “đánh giá” PROCEDURE [0, 8) → ∅

Nguồn: VietMed-NER train, dòng 1686 (từ 0).

## VM600-203

**Đoạn gốc:** khi nó không đủ chất đủ cân bằng vân vân thế cho nên là cái việc mà hỏi là điều trị khỏi hẳn bệnh huyết áp hoặc là khỏi

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | điều trị | Thủ thuật hoặc điều trị (PROCEDURE) | [75, 83) |
| E2 | huyết áp | Bệnh hoặc triệu chứng (CONDITION) | [98, 106) |

### RE

| Mã | Cặp có hướng | Kết luận đề xuất |
|---|---|---|
| R1 | E2 “huyết áp” → E1 “điều trị” | Chưa rõ — cần chốt (CHUA_RO) |

### Cần chốt

- CONTEXT_OR_TRANSCRIPT: câu bị cắt, tham chiếu/mục đích chưa rõ hoặc nghi lỗi phiên âm; cần xem ngữ cảnh/audio gốc, không tự sửa văn bản.
- GENERIC_INTERVENTION: cần chốt việc giữ hành động điều trị/chẩn đoán chung khi không nêu phương pháp cụ thể.
- PHYSIOLOGY_VS_DISEASE: từ huyết áp/mỡ máu đứng riêng chưa xác định bệnh; giữ đề xuất nguồn chờ chốt.
- UNRESOLVED_RE: còn cặp CHUA_RO; tuyệt đối không đổi thành NO_RELATION khi xuất huấn luyện.

Nguồn: VietMed-NER train, dòng 1694 (từ 0).

## VM600-204

**Đoạn gốc:** một cái cái thoái hóa cột sống thắt lưng bác có đau cột sống thắt lưng tuy nhiên ngoài ra lại có cái câu chuyện là đau

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | thoái hóa cột sống thắt lưng | Bệnh hoặc triệu chứng (CONDITION) | [12, 40) |
| E3 | đau cột sống thắt lưng | Bệnh hoặc triệu chứng (CONDITION) | [48, 70) |
| E6 | đau | Bệnh hoặc triệu chứng (CONDITION) | [115, 118) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- CONTEXT_OR_TRANSCRIPT: câu bị cắt, tham chiếu/mục đích chưa rõ hoặc nghi lỗi phiên âm; cần xem ngữ cảnh/audio gốc, không tự sửa văn bản.

### Thay đổi NER

- E4 “cột sống” BODY_PART [52, 60) → E4 “cột sống thắt lưng” BODY_PART [52, 70)
- E5 “thắt lưng” BODY_PART [61, 70) → ∅
- E1 “thoái hóa cột sống” CONDITION [12, 30) → E1 “thoái hóa cột sống thắt lưng” CONDITION [12, 40)
- E2 “thắt lưng” BODY_PART [31, 40) → ∅
- E3 “đau” CONDITION [48, 51) → E3 “đau cột sống thắt lưng” CONDITION [48, 70)
- E4 “cột sống thắt lưng” BODY_PART [52, 70) → ∅

Nguồn: VietMed-NER train, dòng 1696 (từ 0).

## VM600-205

**Đoạn gốc:** lúc mà đột quỵ mà nó không tự thông lại đều thì lúc đó là sẽ đột quỵ thật sự được rõ chúng ta sẽ rất là nghiêm

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | đột quỵ | Bệnh hoặc triệu chứng (CONDITION) | [7, 14) |
| E2 | đột quỵ | Bệnh hoặc triệu chứng (CONDITION) | [61, 68) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

Nguồn: VietMed-NER train, dòng 1698 (từ 0).

## VM600-206

**Đoạn gốc:** cái ghi nhận người ta thấy rằng là một cái thời gian sau khi đặt cái điện cực này quá không hiểu tại sao thì bệnh nhân có thể có những cái cái rối loạn cảm xúc

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | điện cực | Thủ thuật hoặc điều trị (PROCEDURE) | [69, 77) |
| E2 | rối loạn cảm xúc | Bệnh hoặc triệu chứng (CONDITION) | [143, 159) |

### RE

| Mã | Cặp có hướng | Kết luận đề xuất |
|---|---|---|
| R1 | E2 “rối loạn cảm xúc” → E1 “điện cực” | Không có quan hệ thuộc 5 loại (NO_RELATION) |

### Cần chốt

- SCOPE_CONFIRMATION: cần xác nhận quy ước về thuốc/dược chất, can thiệp không dùng thuốc, thiết bị, tác nhân hoặc hoạt động thăm khám; không coi ánh xạ nguồn là xác nhận chuyên gia.

Nguồn: VietMed-NER train, dòng 1700 (từ 0).

## VM600-207

**Đoạn gốc:** động vật không xương sống và chúng sống sót qua bệnh tật chỉ bằng kiểu phòng thủ này nghĩa là hệ miễn dịch của chúng

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E2 | hệ miễn dịch | Bộ phận cơ thể (BODY_PART) | [94, 106) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Thay đổi NER

- E1 “xương” BODY_PART [15, 20) → ∅

Nguồn: VietMed-NER train, dòng 1707 (từ 0).

## VM600-208

**Đoạn gốc:** như số lượng ngôi sao chọn vũ trụ trên thực tế mầm bệnh không thể nhân

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

Không có thực thể thuộc sáu loại được giữ trong bản rà soát.

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Thay đổi NER

- E1 “mầm bệnh” CONDITION [47, 55) → ∅

Nguồn: VietMed-NER train, dòng 1708 (từ 0).

## VM600-209

**Đoạn gốc:** giống như là không có cái giá trị vì đi ăn toàn lại không ăn hại tới ăn mà ăn thì nhiều nhưng mà làm thì ít thì cái

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

Không có thực thể thuộc sáu loại được giữ trong bản rà soát.

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

Nguồn: VietMed-NER train, dòng 1732 (từ 0).

## VM600-210

**Đoạn gốc:** và tình trạng sức khỏe của một người câu trả lời cho câu hỏi nằm ở sự khác biệt

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

Không có thực thể thuộc sáu loại được giữ trong bản rà soát.

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Thay đổi NER

- E1 “một người” DOSAGE [27, 36) → ∅

Nguồn: VietMed-NER train, dòng 1738 (từ 0).

## VM600-211

**Đoạn gốc:** này nó tích cực hơn điều này nó cực kỳ quan trọng vì như chúng tôi đã trình bày ở trên thì

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

Không có thực thể thuộc sáu loại được giữ trong bản rà soát.

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

Nguồn: VietMed-NER train, dòng 1739 (từ 0).

## VM600-212

**Đoạn gốc:** dụng là ức chế sẽ sinh sắc tố nữa như vậy thì chúng ta sẽ vừa phục hồi được cái làn da trong quá trình điều trị mà

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E4 | làn da | Bộ phận cơ thể (BODY_PART) | [80, 86) |
| E5 | điều trị | Thủ thuật hoặc điều trị (PROCEDURE) | [103, 111) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- CONTEXT_OR_TRANSCRIPT: câu bị cắt, tham chiếu/mục đích chưa rõ hoặc nghi lỗi phiên âm; cần xem ngữ cảnh/audio gốc, không tự sửa văn bản.
- GENERIC_INTERVENTION: cần chốt việc giữ hành động điều trị/chẩn đoán chung khi không nêu phương pháp cụ thể.

### Thay đổi NER

- E1 “ức chế” DRUG [8, 14) → ∅
- E2 “sắc tố” BODY_PART [23, 29) → ∅
- E3 “phục hồi” PROCEDURE [62, 70) → ∅

Nguồn: VietMed-NER train, dòng 1743 (từ 0).

## VM600-213

**Đoạn gốc:** tuy nhiên điều đó nói lên rằng chúng ta phải thừa nhận các bằng chứng vẫn tiếp

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

Không có thực thể thuộc sáu loại được giữ trong bản rà soát.

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

Nguồn: VietMed-NER train, dòng 1748 (từ 0).

## VM600-214

**Đoạn gốc:** cái động tác giúp cải thiện cái tuần hoàn của các cái vùng của cơ thể của chúng ta thì bản thân bác sĩ nhiều khi

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E2 | cơ thể | Bộ phận cơ thể (BODY_PART) | [63, 69) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Thay đổi NER

- E1 “cải thiện” PROCEDURE [18, 27) → ∅

Nguồn: VietMed-NER train, dòng 1750 (từ 0).

## VM600-215

**Đoạn gốc:** ta thấy là đan sâm vâng đan sâm cũng là một vị thuốc rất nổi tiếng xưa kia của cha ông ta nó nằm ở trong cái vị thuốc

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | đan sâm | Thuốc/dược chất (DRUG) | [11, 18) |
| E2 | đan sâm | Thuốc/dược chất (DRUG) | [24, 31) |
| E3 | thuốc | Thuốc/dược chất (DRUG) | [47, 52) |
| E4 | thuốc | Thuốc/dược chất (DRUG) | [112, 117) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- ONTOLOGY_SCOPE: cần chốt phạm vi thuốc/dược chất so với mỹ phẩm, thực phẩm, hóa chất nội sinh hoặc hệ vi sinh; giữ ánh xạ nguồn khi chưa có quy ước đủ rõ.

Nguồn: VietMed-NER train, dòng 1752 (từ 0).

## VM600-216

**Đoạn gốc:** nên ăn các cái thực phẩm là chế biến sẵn bởi vì trong đó một là giàu các cái chất

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

Không có thực thể thuộc sáu loại được giữ trong bản rà soát.

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Thay đổi NER

- E1 “chế biến” PROCEDURE [28, 36) → ∅

Nguồn: VietMed-NER train, dòng 1757 (từ 0).

## VM600-217

**Đoạn gốc:** qua cái đường mà can thiệp nội mạch thì hiện nay đó thì người ta đã chế tạo

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | can thiệp nội mạch | Thủ thuật hoặc điều trị (PROCEDURE) | [17, 35) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- SCOPE_CONFIRMATION: cần xác nhận quy ước về thuốc/dược chất, can thiệp không dùng thuốc, thiết bị, tác nhân hoặc hoạt động thăm khám; không coi ánh xạ nguồn là xác nhận chuyên gia.

### Thay đổi NER

- E1 “can thiệp” DRUG [17, 26) → E1 “can thiệp nội mạch” PROCEDURE [17, 35)
- E2 “mạch” BODY_PART [31, 35) → ∅

Nguồn: VietMed-NER train, dòng 1760 (từ 0).

## VM600-218

**Đoạn gốc:** điều trị thuốc nó phải đúng chứ không phải là mình thích cái thuốc nào là mình dùng thuốc đó hay là mình nghe cái mách

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | điều trị | Thủ thuật hoặc điều trị (PROCEDURE) | [0, 8) |
| E2 | thuốc | Thuốc/dược chất (DRUG) | [9, 14) |
| E3 | thuốc | Thuốc/dược chất (DRUG) | [61, 66) |
| E4 | thuốc | Thuốc/dược chất (DRUG) | [84, 89) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- GENERIC_INTERVENTION: cần chốt việc giữ hành động điều trị/chẩn đoán chung khi không nêu phương pháp cụ thể.

Nguồn: VietMed-NER train, dòng 1784 (từ 0).

## VM600-219

**Đoạn gốc:** thực phẩm bảo vệ sức khỏe có lợi cho vấn đề tim mạch có lợi cho vấn đề thần kinh mà rất hữu ích với cái việc mà nó hỗ trợ

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | tim mạch | Bộ phận cơ thể (BODY_PART) | [44, 52) |
| E2 | thần kinh | Bộ phận cơ thể (BODY_PART) | [71, 80) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- ONTOLOGY_SCOPE: cần chốt phạm vi thuốc/dược chất so với mỹ phẩm, thực phẩm, hóa chất nội sinh hoặc hệ vi sinh; giữ ánh xạ nguồn khi chưa có quy ước đủ rõ.

### Thay đổi NER

- E3 “hỗ trợ” PROCEDURE [115, 121) → ∅

Nguồn: VietMed-NER train, dòng 1798 (từ 0).

## VM600-220

**Đoạn gốc:** cái hiệu quả của mình mình cũng không dám chắc một trăm phần trăm hoặc là nó cũng có những cái rủi ro nhất định cho

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

Không có thực thể thuộc sáu loại được giữ trong bản rà soát.

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Thay đổi NER

- E1 “một trăm phần trăm” DOSAGE [47, 65) → ∅

Nguồn: VietMed-NER train, dòng 1801 (từ 0).

## VM600-221

**Đoạn gốc:** gì cả hàng năm bên cạnh việc duy trì ngâm khoáng và điều trị ở bệnh viện cả tháng

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | ngâm khoáng | Thủ thuật hoặc điều trị (PROCEDURE) | [37, 48) |
| E2 | điều trị | Thủ thuật hoặc điều trị (PROCEDURE) | [52, 60) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- GENERIC_INTERVENTION: cần chốt việc giữ hành động điều trị/chẩn đoán chung khi không nêu phương pháp cụ thể.
- SCOPE_CONFIRMATION: cần xác nhận quy ước về thuốc/dược chất, can thiệp không dùng thuốc, thiết bị, tác nhân hoặc hoạt động thăm khám; không coi ánh xạ nguồn là xác nhận chuyên gia.

Nguồn: VietMed-NER train, dòng 1803 (từ 0).

## VM600-222

**Đoạn gốc:** không

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

Không có thực thể thuộc sáu loại được giữ trong bản rà soát.

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

Nguồn: VietMed-NER train, dòng 1815 (từ 0).

## VM600-223

**Đoạn gốc:** chụp vai gáy ở đâu dây thần viêm đốt vai

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | chụp vai gáy | Xét nghiệm hoặc thăm khám (TEST) | [0, 12) |
| E2 | viêm | Bệnh hoặc triệu chứng (CONDITION) | [28, 32) |
| E3 | đốt vai | Bộ phận cơ thể (BODY_PART) | [33, 40) |

### RE

| Mã | Cặp có hướng | Kết luận đề xuất |
|---|---|---|
| R1 | E2 “viêm” → E1 “chụp vai gáy” | Chưa rõ — cần chốt (CHUA_RO) |
| R2 | E2 “viêm” → E3 “đốt vai” | Chưa rõ — cần chốt (CHUA_RO) |

### Cần chốt

- CONTEXT_OR_TRANSCRIPT: câu bị cắt, tham chiếu/mục đích chưa rõ hoặc nghi lỗi phiên âm; cần xem ngữ cảnh/audio gốc, không tự sửa văn bản.
- UNRESOLVED_RE: còn cặp CHUA_RO; tuyệt đối không đổi thành NO_RELATION khi xuất huấn luyện.

### Thay đổi NER

- E1 “chụp vai gáy” PROCEDURE [0, 12) → E1 “chụp vai gáy” TEST [0, 12)

Nguồn: VietMed-NER train, dòng 1822 (từ 0).

## VM600-224

**Đoạn gốc:** với tình trạng rung nhĩ tim đập nó quá nhanh thì chúng ta phải có biện pháp nào để kiểm soát các tần số đó đừng cho đập

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | rung nhĩ | Bệnh hoặc triệu chứng (CONDITION) | [15, 23) |
| E5 | tim đập nó quá nhanh | Bệnh hoặc triệu chứng (CONDITION) | [24, 44) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- CONTEXT_OR_TRANSCRIPT: câu bị cắt, tham chiếu/mục đích chưa rõ hoặc nghi lỗi phiên âm; cần xem ngữ cảnh/audio gốc, không tự sửa văn bản.

### Thay đổi NER

- E3 “kiểm soát” DRUG [83, 92) → ∅
- E4 “tần số” DOSAGE [97, 103) → ∅
- ∅ → E5 “đập nó quá nhanh” CONDITION [28, 44)
- E5 “đập nó quá nhanh” CONDITION [28, 44) → E5 “tim đập nó quá nhanh” CONDITION [24, 44)
- E2 “tim” BODY_PART [24, 27) → ∅

Nguồn: VietMed-NER train, dòng 1831 (từ 0).

## VM600-225

**Đoạn gốc:** nhau đây chúng ta chỉ có hai nhóm chúng ta khuyến cáo ít nhất là phải mười lăm loại thực phẩm đây chúng ta chỉ có hai loại

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

Không có thực thể thuộc sáu loại được giữ trong bản rà soát.

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Thay đổi NER

- E1 “hai nhóm” DOSAGE [25, 33) → ∅
- E2 “khuyến cáo” DRUG [43, 53) → ∅

Nguồn: VietMed-NER train, dòng 1832 (từ 0).

## VM600-226

**Đoạn gốc:** giày thì nó sẽ giữ được cái chân ấm hơn chúng ta sẽ đi cái tất dày hơn đi cái tất dài hơn như thế cũng sẽ rất là hữu

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | chân | Bộ phận cơ thể (BODY_PART) | [28, 32) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Thay đổi NER

- E1 “cái chân” BODY_PART [24, 32) → E1 “chân” BODY_PART [28, 32)

Nguồn: VietMed-NER train, dòng 1836 (từ 0).

## VM600-227

**Đoạn gốc:** một cái gợi ý nó cũng chỉ là một cái tỷ lệ do đó cái xét nghiệm khi mà chúng ta thấy không thật sự cần thiết thì chúng

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E2 | xét nghiệm | Xét nghiệm hoặc thăm khám (TEST) | [53, 63) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Thay đổi NER

- E1 “cái tỷ lệ” DOSAGE [33, 42) → ∅

Nguồn: VietMed-NER train, dòng 1839 (từ 0).

## VM600-228

**Đoạn gốc:** gây nhiễm có chủ ý để cung cấp sự bảo vệ sự chủng ngừa đã được thực hành ở trung

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | chủng ngừa | Thủ thuật hoặc điều trị (PROCEDURE) | [44, 54) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- SCOPE_CONFIRMATION: cần xác nhận quy ước về thuốc/dược chất, can thiệp không dùng thuốc, thiết bị, tác nhân hoặc hoạt động thăm khám; không coi ánh xạ nguồn là xác nhận chuyên gia.

### Thay đổi NER

- ∅ → E1 “chủng ngừa” PROCEDURE [44, 54)

Nguồn: VietMed-NER train, dòng 1843 (từ 0).

## VM600-229

**Đoạn gốc:** về em tẩy trang bôi lại kem chống nắng thì nên làm thêm bước nào trong ba bước này nữa ạ vâng nếu mà buổi trưa đó là

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | kem chống nắng | Thuốc/dược chất (DRUG) | [24, 38) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- ONTOLOGY_SCOPE: cần chốt phạm vi thuốc/dược chất so với mỹ phẩm, thực phẩm, hóa chất nội sinh hoặc hệ vi sinh; giữ ánh xạ nguồn khi chưa có quy ước đủ rõ.

### Thay đổi NER

- E2 “ba bước” DOSAGE [71, 78) → ∅

Nguồn: VietMed-NER train, dòng 1844 (từ 0).

## VM600-230

**Đoạn gốc:** tử mà nó chưa gặp phải trước đây nói cách khác hệ miễn dịch hoạt động bằng

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | hệ miễn dịch | Bộ phận cơ thể (BODY_PART) | [47, 59) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

Nguồn: VietMed-NER train, dòng 1845 (từ 0).

## VM600-231

**Đoạn gốc:** thập niên trước khi mắc các bệnh tim mạch và ung thư và họ không mắc chứng trầm cảm nhiều tỷ lệ suy giảm nhận thức

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E6 | bệnh tim mạch | Bệnh hoặc triệu chứng (CONDITION) | [28, 41) |
| E2 | ung thư | Bệnh hoặc triệu chứng (CONDITION) | [45, 52) |
| E3 | trầm cảm | Bệnh hoặc triệu chứng (CONDITION) | [75, 83) |
| E5 | suy giảm nhận thức | Bệnh hoặc triệu chứng (CONDITION) | [96, 114) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Thay đổi NER

- E4 “tỷ lệ” DOSAGE [90, 95) → ∅
- ∅ → E6 “bệnh” CONDITION [28, 32)
- E6 “bệnh” CONDITION [28, 32) → E6 “bệnh tim mạch” CONDITION [28, 41)
- E1 “tim mạch” BODY_PART [33, 41) → ∅

Nguồn: VietMed-NER train, dòng 1849 (từ 0).

## VM600-232

**Đoạn gốc:** có cái vấn đề tương tự như thế này chúng tôi khuyên là chúng ta nên đi khám bệnh để có một cái đánh giá có một cái chẩn

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | khám bệnh | Xét nghiệm hoặc thăm khám (TEST) | [71, 80) |
| E2 | đánh giá | Xét nghiệm hoặc thăm khám (TEST) | [95, 103) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- GENERIC_INTERVENTION: cần chốt việc giữ hành động điều trị/chẩn đoán chung khi không nêu phương pháp cụ thể.

### Thay đổi NER

- E1 “khám” TEST [71, 75) → E1 “khám bệnh” TEST [71, 80)
- E2 “đánh giá” PROCEDURE [95, 103) → E2 “đánh giá” TEST [95, 103)

Nguồn: VietMed-NER train, dòng 1858 (từ 0).

## VM600-233

**Đoạn gốc:** chúng ta biết rằng hiện chưa có cách chữa trị tiềm năng nào và còn cả chứng

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | chữa trị | Thủ thuật hoặc điều trị (PROCEDURE) | [37, 45) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- GENERIC_INTERVENTION: cần chốt việc giữ hành động điều trị/chẩn đoán chung khi không nêu phương pháp cụ thể.

Nguồn: VietMed-NER train, dòng 1859 (từ 0).

## VM600-234

**Đoạn gốc:** ta mà còn thắc mắc cũng như là cũng như là chúng ta bị mắc cái tình trạng về huyết áp cao mỡ máu cao lâu năm thì

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | huyết áp cao | Bệnh hoặc triệu chứng (CONDITION) | [77, 89) |
| E3 | mỡ máu cao | Bệnh hoặc triệu chứng (CONDITION) | [90, 100) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Thay đổi NER

- E2 “cao” DOSAGE [86, 89) → ∅
- E4 “cao” DOSAGE [97, 100) → ∅
- E1 “huyết áp” CONDITION [77, 85) → E1 “huyết áp cao” CONDITION [77, 89)
- E3 “mỡ máu” CONDITION [90, 96) → E3 “mỡ máu cao” CONDITION [90, 100)

Nguồn: VietMed-NER train, dòng 1865 (từ 0).

## VM600-235

**Đoạn gốc:** trường khác như là các cái thuốc hoạt huyết hoặc là những cái thuốc giảm đau thì nó chỉ có cái tác dụng cải thiện

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | thuốc hoạt huyết | Thuốc/dược chất (DRUG) | [27, 43) |
| E2 | thuốc giảm đau | Thuốc/dược chất (DRUG) | [62, 76) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Thay đổi NER

- E3 “cải thiện” PROCEDURE [104, 113) → ∅

Nguồn: VietMed-NER train, dòng 1866 (từ 0).

## VM600-236

**Đoạn gốc:** thuốc mà có thể là không ảnh hưởng đến cân nặng hoặc là thậm chí là có tác dụng giảm cân cho những bệnh nhân như vậy thì điều này cũng đã đưa và các cái

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | thuốc | Thuốc/dược chất (DRUG) | [0, 5) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Thay đổi NER

- E2 “những bệnh nhân” DOSAGE [93, 108) → ∅

Nguồn: VietMed-NER train, dòng 1867 (từ 0).

## VM600-237

**Đoạn gốc:** của chúng ta thì khi đó rõ ràng chúng ta biết rằng là chúng ta cần phải điều chỉnh cái bệnh của chúng ta chứ không

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

Không có thực thể thuộc sáu loại được giữ trong bản rà soát.

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Thay đổi NER

- E1 “điều chỉnh” DRUG [72, 82) → ∅

Nguồn: VietMed-NER train, dòng 1870 (từ 0).

## VM600-238

**Đoạn gốc:** mạch nữa và từ đó thì sẽ tăng cái lưu lượng máu tốt cho não khỏe tim giúp cải thiện các triệu chứng đau đầu chóng mặt

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | mạch | Bộ phận cơ thể (BODY_PART) | [0, 4) |
| E3 | não | Bộ phận cơ thể (BODY_PART) | [56, 59) |
| E4 | tim | Bộ phận cơ thể (BODY_PART) | [65, 68) |
| E7 | đau đầu | Bệnh hoặc triệu chứng (CONDITION) | [100, 107) |
| E8 | chóng mặt | Bệnh hoặc triệu chứng (CONDITION) | [108, 117) |

### RE

| Mã | Cặp có hướng | Kết luận đề xuất |
|---|---|---|
| R1 | E7 “đau đầu” → E1 “mạch” | Không có quan hệ thuộc 5 loại (NO_RELATION) |
| R2 | E7 “đau đầu” → E3 “não” | Không có quan hệ thuộc 5 loại (NO_RELATION) |
| R3 | E7 “đau đầu” → E4 “tim” | Không có quan hệ thuộc 5 loại (NO_RELATION) |
| R4 | E8 “chóng mặt” → E1 “mạch” | Không có quan hệ thuộc 5 loại (NO_RELATION) |
| R5 | E8 “chóng mặt” → E3 “não” | Không có quan hệ thuộc 5 loại (NO_RELATION) |
| R6 | E8 “chóng mặt” → E4 “tim” | Không có quan hệ thuộc 5 loại (NO_RELATION) |

### Thay đổi NER

- E2 “lưu lượng máu” DOSAGE [34, 47) → ∅
- E5 “cải thiện” PROCEDURE [74, 83) → ∅
- E6 “triệu chứng” CONDITION [88, 99) → ∅

Nguồn: VietMed-NER train, dòng 1880 (từ 0).

## VM600-239

**Đoạn gốc:** cả bạn mặc dù có lẽ bạn quen với thực tế là một số vi khuẩn có thể gây bệnh và

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

Không có thực thể thuộc sáu loại được giữ trong bản rà soát.

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Thay đổi NER

- E1 “vi khuẩn” CONDITION [51, 59) → ∅

Nguồn: VietMed-NER train, dòng 1882 (từ 0).

## VM600-240

**Đoạn gốc:** dây thần kinh và mạch máu khi đi xuống cái bàn tay nó sẽ đi qua cái vùng cổ tay như thế này và nếu mà cái chỗ này nó bị

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | dây thần kinh | Bộ phận cơ thể (BODY_PART) | [0, 13) |
| E2 | mạch máu | Bộ phận cơ thể (BODY_PART) | [17, 25) |
| E3 | bàn tay | Bộ phận cơ thể (BODY_PART) | [43, 50) |
| E5 | cổ tay | Bộ phận cơ thể (BODY_PART) | [73, 79) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Thay đổi NER

- E4 “vùng” BODY_PART [68, 72) → ∅

Nguồn: VietMed-NER train, dòng 1889 (từ 0).

## VM600-241

**Đoạn gốc:** có cường giáp hay không phải cường giáp là một cái yếu tố nó kích động trái tim lên chúng ta và nó sẽ gây ra tình trạng

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | cường giáp | Bệnh hoặc triệu chứng (CONDITION) | [3, 13) |
| E2 | cường giáp | Bệnh hoặc triệu chứng (CONDITION) | [29, 39) |
| E3 | trái tim | Bộ phận cơ thể (BODY_PART) | [71, 79) |

### RE

| Mã | Cặp có hướng | Kết luận đề xuất |
|---|---|---|
| R1 | E1 “cường giáp” → E3 “trái tim” | Không có quan hệ thuộc 5 loại (NO_RELATION) |
| R2 | E2 “cường giáp” → E3 “trái tim” | Không có quan hệ thuộc 5 loại (NO_RELATION) |

Nguồn: VietMed-NER train, dòng 1893 (từ 0).

## VM600-242

**Đoạn gốc:** ngừa dại hay không và nếu được tiêm thì

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | dại | Bệnh hoặc triệu chứng (CONDITION) | [5, 8) |
| E2 | tiêm | Thủ thuật hoặc điều trị (PROCEDURE) | [31, 35) |

### RE

| Mã | Cặp có hướng | Kết luận đề xuất |
|---|---|---|
| R1 | E1 “dại” → E2 “tiêm” | Không có quan hệ thuộc 5 loại (NO_RELATION) |

### Cần chốt

- CONTEXT_OR_TRANSCRIPT: câu bị cắt, tham chiếu/mục đích chưa rõ hoặc nghi lỗi phiên âm; cần xem ngữ cảnh/audio gốc, không tự sửa văn bản.

### Thay đổi NER

- E1 “ngừa dại” DRUG [0, 8) → E1 “dại” CONDITION [5, 8)

Nguồn: VietMed-NER train, dòng 1904 (từ 0).

## VM600-243

**Đoạn gốc:** chưa biết là huyết áp của bác thế nào mỡ máu ra sao có đái tháo đường không nhưng mà khi chúng ta bị tai biến một lần thì

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E3 | đái tháo đường | Bệnh hoặc triệu chứng (CONDITION) | [55, 69) |
| E4 | tai biến | Bệnh hoặc triệu chứng (CONDITION) | [101, 109) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Thay đổi NER

- E1 “huyết áp” CONDITION [13, 21) → ∅
- E2 “mỡ máu” CONDITION [38, 44) → ∅

Nguồn: VietMed-NER train, dòng 1906 (từ 0).

## VM600-244

**Đoạn gốc:** tình trạng là huyết áp cao mỡ máu cao rồi những cái bệnh lý mà chúng ta khiến cho tim mạch nè chúng ta bị mất ổn định

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | huyết áp cao | Bệnh hoặc triệu chứng (CONDITION) | [14, 26) |
| E3 | mỡ máu cao | Bệnh hoặc triệu chứng (CONDITION) | [27, 37) |
| E5 | tim mạch | Bộ phận cơ thể (BODY_PART) | [82, 90) |

### RE

| Mã | Cặp có hướng | Kết luận đề xuất |
|---|---|---|
| R1 | E1 “huyết áp cao” → E5 “tim mạch” | Không có quan hệ thuộc 5 loại (NO_RELATION) |
| R2 | E3 “mỡ máu cao” → E5 “tim mạch” | Không có quan hệ thuộc 5 loại (NO_RELATION) |

### Thay đổi NER

- E2 “cao” DOSAGE [23, 26) → ∅
- E4 “cao” DOSAGE [34, 37) → ∅
- E1 “huyết áp” CONDITION [14, 22) → E1 “huyết áp cao” CONDITION [14, 26)
- E3 “mỡ máu” CONDITION [27, 33) → E3 “mỡ máu cao” CONDITION [27, 37)

Nguồn: VietMed-NER train, dòng 1909 (từ 0).

## VM600-245

**Đoạn gốc:** lại bình thường trước đây tôi cũng có một cô bạn cô mới giới thiệu cho tôi đông trùng hạ

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

Không có thực thể thuộc sáu loại được giữ trong bản rà soát.

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- CONTEXT_OR_TRANSCRIPT: câu bị cắt, tham chiếu/mục đích chưa rõ hoặc nghi lỗi phiên âm; cần xem ngữ cảnh/audio gốc, không tự sửa văn bản.
- ONTOLOGY_SCOPE: cần chốt phạm vi thuốc/dược chất so với mỹ phẩm, thực phẩm, hóa chất nội sinh hoặc hệ vi sinh; giữ ánh xạ nguồn khi chưa có quy ước đủ rõ.

Nguồn: VietMed-NER train, dòng 1911 (từ 0).

## VM600-246

**Đoạn gốc:** chia hai lần sáng chiều còn từ tháng thứ ba trở đi chúng ta có thể uống hai viên chia lần sáng chiều cái điều đó thì nó

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | hai lần | Liều lượng (DOSAGE) | [5, 12) |
| E2 | hai viên | Liều lượng (DOSAGE) | [72, 80) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- CONTEXT_OR_TRANSCRIPT: câu bị cắt, tham chiếu/mục đích chưa rõ hoặc nghi lỗi phiên âm; cần xem ngữ cảnh/audio gốc, không tự sửa văn bản.
- DOSAGE_CONTEXT: có hai lần/hai viên nhưng thuốc và đơn vị thời gian bị thiếu; không tạo has_dosage từ suy đoán.

Nguồn: VietMed-NER train, dòng 1917 (từ 0).

## VM600-247

**Đoạn gốc:** fumarate đây là một cái sản phẩm mà cũng đã được chứng minh rằng nó có tác dụng là giúp cho cái giảm cái nguy cơ hình

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | fumarate | Thuốc/dược chất (DRUG) | [0, 8) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- CONTEXT_OR_TRANSCRIPT: câu bị cắt, tham chiếu/mục đích chưa rõ hoặc nghi lỗi phiên âm; cần xem ngữ cảnh/audio gốc, không tự sửa văn bản.
- ONTOLOGY_SCOPE: cần chốt phạm vi thuốc/dược chất so với mỹ phẩm, thực phẩm, hóa chất nội sinh hoặc hệ vi sinh; giữ ánh xạ nguồn khi chưa có quy ước đủ rõ.

Nguồn: VietMed-NER train, dòng 1922 (từ 0).

## VM600-248

**Đoạn gốc:** nước anh đều mô tả bệnh dại là tử vong thời gian

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E2 | bệnh dại | Bệnh hoặc triệu chứng (CONDITION) | [19, 27) |
| E3 | tử vong | Bệnh hoặc triệu chứng (CONDITION) | [31, 38) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Thay đổi NER

- E1 “mô” BODY_PART [13, 15) → ∅

Nguồn: VietMed-NER train, dòng 1928 (từ 0).

## VM600-249

**Đoạn gốc:** bác sĩ chuyên khoa bị rối loạn vận động sẽ có một cái quan điểm khám và đánh giá để người ta tiên lượng được thứ nhất

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | rối loạn vận động | Bệnh hoặc triệu chứng (CONDITION) | [22, 39) |
| E2 | khám | Xét nghiệm hoặc thăm khám (TEST) | [64, 68) |
| E3 | đánh giá | Xét nghiệm hoặc thăm khám (TEST) | [72, 80) |

### RE

| Mã | Cặp có hướng | Kết luận đề xuất |
|---|---|---|
| R1 | E1 “rối loạn vận động” → E2 “khám” | Chưa rõ — cần chốt (CHUA_RO) |
| R2 | E1 “rối loạn vận động” → E3 “đánh giá” | Chưa rõ — cần chốt (CHUA_RO) |

### Cần chốt

- CONTEXT_OR_TRANSCRIPT: câu bị cắt, tham chiếu/mục đích chưa rõ hoặc nghi lỗi phiên âm; cần xem ngữ cảnh/audio gốc, không tự sửa văn bản.
- GENERIC_INTERVENTION: cần chốt việc giữ hành động điều trị/chẩn đoán chung khi không nêu phương pháp cụ thể.
- UNRESOLVED_RE: còn cặp CHUA_RO; tuyệt đối không đổi thành NO_RELATION khi xuất huấn luyện.

### Thay đổi NER

- E4 “thứ nhất” DOSAGE [109, 117) → ∅
- E3 “đánh giá” PROCEDURE [72, 80) → E3 “đánh giá” TEST [72, 80)

Nguồn: VietMed-NER train, dòng 1936 (từ 0).

## VM600-250

**Đoạn gốc:** là các triệu chứng như là đau đầu hoa mắt chóng mặt của bác này hay là những cái dấu hiệu tim đập hồi hộp trống

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E2 | đau đầu | Bệnh hoặc triệu chứng (CONDITION) | [26, 33) |
| E3 | hoa mắt | Bệnh hoặc triệu chứng (CONDITION) | [34, 41) |
| E4 | chóng mặt | Bệnh hoặc triệu chứng (CONDITION) | [42, 51) |
| E6 | tim đập hồi hộp | Bệnh hoặc triệu chứng (CONDITION) | [90, 105) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- CONTEXT_OR_TRANSCRIPT: câu bị cắt, tham chiếu/mục đích chưa rõ hoặc nghi lỗi phiên âm; cần xem ngữ cảnh/audio gốc, không tự sửa văn bản.

### Thay đổi NER

- E1 “triệu chứng” CONDITION [7, 18) → ∅
- ∅ → E6 “đập hồi hộp” CONDITION [94, 105)
- E6 “đập hồi hộp” CONDITION [94, 105) → E6 “tim đập hồi hộp” CONDITION [90, 105)
- E5 “tim” BODY_PART [90, 93) → ∅

Nguồn: VietMed-NER train, dòng 1949 (từ 0).

## VM600-251

**Đoạn gốc:** thì chúng ta phải giải quyết những yếu tố nguy cơ đó để chúng ta đừng bị rung nhĩ và một khi mà đã bị rung nhĩ rồi đó

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | rung nhĩ | Bệnh hoặc triệu chứng (CONDITION) | [73, 81) |
| E2 | rung nhĩ | Bệnh hoặc triệu chứng (CONDITION) | [102, 110) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

Nguồn: VietMed-NER train, dòng 1952 (từ 0).

## VM600-252

**Đoạn gốc:** đường huyết hiện nay tân dược là càng ngày nó càng phát triển càng ngày nó càng phong phú và rất nhiều loại rất là

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E2 | tân dược | Thuốc/dược chất (DRUG) | [21, 29) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Thay đổi NER

- E1 “đường huyết” DOSAGE [0, 11) → ∅
- E3 “rất nhiều” DOSAGE [93, 102) → ∅

Nguồn: VietMed-NER train, dòng 1963 (từ 0).

## VM600-253

**Đoạn gốc:** điểm nữa thì họ thường thường là bị tự ti tự ti nó khác với chữ tự tin hay là

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | tự ti | Bệnh hoặc triệu chứng (CONDITION) | [36, 41) |
| E2 | tự ti | Bệnh hoặc triệu chứng (CONDITION) | [42, 47) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- SYMPTOM_SCOPE: cần phân biệt cảm xúc thông thường với triệu chứng lâm sàng theo quy ước dự án.

Nguồn: VietMed-NER train, dòng 1964 (từ 0).

## VM600-254

**Đoạn gốc:** nói tỷ lệ tử vong của bệnh nhân được giảm nhưng mà vấn đề chỗ là cái tỷ lệ

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E2 | tử vong | Bệnh hoặc triệu chứng (CONDITION) | [10, 17) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Thay đổi NER

- E1 “tỷ lệ” DOSAGE [4, 9) → ∅
- E3 “cái tỷ lệ” DOSAGE [65, 74) → ∅

Nguồn: VietMed-NER train, dòng 1974 (từ 0).

## VM600-255

**Đoạn gốc:** việc này thử nghiệm lâm sàng đầu tiên được ghi nhận trong lịch sử miễn dịch

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

Không có thực thể thuộc sáu loại được giữ trong bản rà soát.

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Thay đổi NER

- E1 “thử nghiệm lâm sàng” PROCEDURE [9, 28) → ∅

Nguồn: VietMed-NER train, dòng 1979 (từ 0).

## VM600-256

**Đoạn gốc:** thuật cũng không có ngăn sự tiến triển của bệnh được và dĩ nhiên hiệu quả của

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

Không có thực thể thuộc sáu loại được giữ trong bản rà soát.

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- CONTEXT_OR_TRANSCRIPT: câu bị cắt, tham chiếu/mục đích chưa rõ hoặc nghi lỗi phiên âm; cần xem ngữ cảnh/audio gốc, không tự sửa văn bản.

Nguồn: VietMed-NER train, dòng 1985 (từ 0).

## VM600-257

**Đoạn gốc:** thì mình có cái giải pháp ngay lập tức là như nào cá nhân tôi chẳng hạn bây giờ tôi chưa bị như bác đâu nhưng mà đi lúc

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

Không có thực thể thuộc sáu loại được giữ trong bản rà soát.

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

Nguồn: VietMed-NER train, dòng 1988 (từ 0).

## VM600-258

**Đoạn gốc:** nguyên nhân cơ chế bệnh sinh đó chính là nó không tác động vào được làm mất đi làm giảm cái mảng xơ vữa nên là cái hiệu

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | mảng xơ vữa | Bệnh hoặc triệu chứng (CONDITION) | [92, 103) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

Nguồn: VietMed-NER train, dòng 1995 (từ 0).

## VM600-259

**Đoạn gốc:** những người xung quanh đối với những thành viên những người thân trong gia đình thì tôi nghĩ rằng là làm sao để cho

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

Không có thực thể thuộc sáu loại được giữ trong bản rà soát.

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

Nguồn: VietMed-NER train, dòng 2011 (từ 0).

## VM600-260

**Đoạn gốc:** tục ví dụ như là về những cái bài tập ví dụ như những cái hỗ trợ về điều trị

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E3 | bài tập | Thủ thuật hoặc điều trị (PROCEDURE) | [30, 37) |
| E2 | điều trị | Thủ thuật hoặc điều trị (PROCEDURE) | [68, 76) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- GENERIC_INTERVENTION: cần chốt việc giữ hành động điều trị/chẩn đoán chung khi không nêu phương pháp cụ thể.
- SCOPE_CONFIRMATION: cần xác nhận quy ước về thuốc/dược chất, can thiệp không dùng thuốc, thiết bị, tác nhân hoặc hoạt động thăm khám; không coi ánh xạ nguồn là xác nhận chuyên gia.

### Thay đổi NER

- E1 “hỗ trợ” PROCEDURE [58, 64) → ∅
- ∅ → E3 “bài tập” PROCEDURE [30, 37)

Nguồn: VietMed-NER train, dòng 2013 (từ 0).

## VM600-261

**Đoạn gốc:** vào phòng ở can thiệp để mà luồn cái dụng cụ vào để mà lấy cái cục khối ra

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | can thiệp | Thủ thuật hoặc điều trị (PROCEDURE) | [12, 21) |
| E2 | luồn cái dụng cụ | Thủ thuật hoặc điều trị (PROCEDURE) | [28, 44) |
| E3 | lấy cái cục khối ra | Thủ thuật hoặc điều trị (PROCEDURE) | [55, 74) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- CONTEXT_OR_TRANSCRIPT: câu bị cắt, tham chiếu/mục đích chưa rõ hoặc nghi lỗi phiên âm; cần xem ngữ cảnh/audio gốc, không tự sửa văn bản.
- GENERIC_INTERVENTION: cần chốt việc giữ hành động điều trị/chẩn đoán chung khi không nêu phương pháp cụ thể.

### Thay đổi NER

- E1 “can thiệp” DRUG [12, 21) → E1 “can thiệp” PROCEDURE [12, 21)
- E2 “luồn cái dụng cụ” TEST [28, 44) → E2 “luồn cái dụng cụ” PROCEDURE [28, 44)

Nguồn: VietMed-NER train, dòng 2018 (từ 0).

## VM600-262

**Đoạn gốc:** là vấn đề các cái chất cái vitamin và chất khoáng đến từ rau và củ quả thì

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | vitamin | Thuốc/dược chất (DRUG) | [27, 34) |
| E2 | chất khoáng | Thuốc/dược chất (DRUG) | [38, 49) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- ONTOLOGY_SCOPE: cần chốt phạm vi thuốc/dược chất so với mỹ phẩm, thực phẩm, hóa chất nội sinh hoặc hệ vi sinh; giữ ánh xạ nguồn khi chưa có quy ước đủ rõ.

Nguồn: VietMed-NER train, dòng 2036 (từ 0).

## VM600-263

**Đoạn gốc:** ta thường xuyên quá mức như vậy thì nó cũng gây rụng tóc rồi nó có một cái mà chúng ta không thể nào không để mặc dù

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | rụng tóc | Bệnh hoặc triệu chứng (CONDITION) | [48, 56) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

Nguồn: VietMed-NER train, dòng 2038 (từ 0).

## VM600-264

**Đoạn gốc:** những câu chuyện này hàng ngày và tôi biết rằng bạn cũng có thể thay đổi tích cực số phận của bộ não thông qua sức

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | bộ não | Bộ phận cơ thể (BODY_PART) | [94, 100) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

Nguồn: VietMed-NER train, dòng 2040 (từ 0).

## VM600-265

**Đoạn gốc:** da chúng ta là mất màu trắng hoàn toàn luôn ra từ nâu hoặc là màu vàng chuyển sang màu trắng luôn ngoài ra còn có thể

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | da | Bộ phận cơ thể (BODY_PART) | [0, 2) |
| E2 | mất màu trắng | Bệnh hoặc triệu chứng (CONDITION) | [15, 28) |

### RE

| Mã | Cặp có hướng | Kết luận đề xuất |
|---|---|---|
| R1 | E2 “mất màu trắng” → E1 “da” | Có vị trí ở (located_at) |

### Cần chốt

- CONTEXT_OR_TRANSCRIPT: câu bị cắt, tham chiếu/mục đích chưa rõ hoặc nghi lỗi phiên âm; cần xem ngữ cảnh/audio gốc, không tự sửa văn bản.

Nguồn: VietMed-NER train, dòng 2060 (từ 0).

## VM600-266

**Đoạn gốc:** khem cái thứ ba là phải tập luyện muốn nói gì thì nói cuộc sống là vận động sự sống mà không có vận động thì nó sẽ càng

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | tập luyện | Thủ thuật hoặc điều trị (PROCEDURE) | [24, 33) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- SCOPE_CONFIRMATION: cần xác nhận quy ước về thuốc/dược chất, can thiệp không dùng thuốc, thiết bị, tác nhân hoặc hoạt động thăm khám; không coi ánh xạ nguồn là xác nhận chuyên gia.

### Thay đổi NER

- ∅ → E1 “tập luyện” PROCEDURE [24, 33)

Nguồn: VietMed-NER train, dòng 2064 (từ 0).

## VM600-267

**Đoạn gốc:** trạng bao gồm cả trầm cảm và lo âu tiểu đường thèm đường và carbohydrate thừa cân

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | trầm cảm | Bệnh hoặc triệu chứng (CONDITION) | [17, 25) |
| E2 | lo âu | Bệnh hoặc triệu chứng (CONDITION) | [29, 34) |
| E3 | tiểu đường | Bệnh hoặc triệu chứng (CONDITION) | [35, 45) |
| E6 | thèm đường | Bệnh hoặc triệu chứng (CONDITION) | [46, 56) |
| E4 | carbohydrate | Thuốc/dược chất (DRUG) | [60, 72) |
| E5 | thừa cân | Bệnh hoặc triệu chứng (CONDITION) | [73, 81) |

### RE

| Mã | Cặp có hướng | Kết luận đề xuất |
|---|---|---|
| R1 | E1 “trầm cảm” → E4 “carbohydrate” | Không có quan hệ thuộc 5 loại (NO_RELATION) |
| R2 | E2 “lo âu” → E4 “carbohydrate” | Không có quan hệ thuộc 5 loại (NO_RELATION) |
| R3 | E3 “tiểu đường” → E4 “carbohydrate” | Không có quan hệ thuộc 5 loại (NO_RELATION) |
| R4 | E6 “thèm đường” → E4 “carbohydrate” | Không có quan hệ thuộc 5 loại (NO_RELATION) |
| R5 | E5 “thừa cân” → E4 “carbohydrate” | Không có quan hệ thuộc 5 loại (NO_RELATION) |

### Cần chốt

- ONTOLOGY_SCOPE: cần chốt phạm vi thuốc/dược chất so với mỹ phẩm, thực phẩm, hóa chất nội sinh hoặc hệ vi sinh; giữ ánh xạ nguồn khi chưa có quy ước đủ rõ.

### Thay đổi NER

- ∅ → E6 “thèm đường” CONDITION [46, 56)

Nguồn: VietMed-NER train, dòng 2069 (từ 0).

## VM600-268

**Đoạn gốc:** tế bào miễn dịch của con người ở những chi tiết nhỏ chính tôi đã nhìn thấy cách khoa học biểu lộ vẻ đẹp dù nó vẫn còn ẩn

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | tế bào miễn dịch | Bộ phận cơ thể (BODY_PART) | [0, 16) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Thay đổi NER

- E1 “tế bào” BODY_PART [0, 6) → E1 “tế bào miễn dịch” BODY_PART [0, 16)

Nguồn: VietMed-NER train, dòng 2081 (từ 0).

## VM600-269

**Đoạn gốc:** cải thiện mà cái điều này là chúng tôi cũng nói đi nói lại rất là nhiều nhưng

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

Không có thực thể thuộc sáu loại được giữ trong bản rà soát.

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Thay đổi NER

- E1 “cải thiện” PROCEDURE [0, 9) → ∅

Nguồn: VietMed-NER train, dòng 2094 (từ 0).

## VM600-270

**Đoạn gốc:** phải kiêng tuyệt đối nhưng chúng ta chỉ nên ăn dưới năm mươi gam thịt đỏ một người một ngày thôi khi mà chúng ta bị ung thư bởi

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E3 | ung thư | Bệnh hoặc triệu chứng (CONDITION) | [116, 123) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Thay đổi NER

- E1 “năm mươi” DOSAGE [52, 60) → ∅
- E2 “một người” DOSAGE [73, 82) → ∅

Nguồn: VietMed-NER train, dòng 2122 (từ 0).

## VM600-271

**Đoạn gốc:** nhưng mà tôi rất là sợ phải đi lấy mẫu vì sợ lây nhiễm lẫn nhau ở tại các khu

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | lấy mẫu | Xét nghiệm hoặc thăm khám (TEST) | [31, 38) |
| E2 | lây nhiễm | Bệnh hoặc triệu chứng (CONDITION) | [45, 54) |

### RE

| Mã | Cặp có hướng | Kết luận đề xuất |
|---|---|---|
| R1 | E2 “lây nhiễm” → E1 “lấy mẫu” | Không có quan hệ thuộc 5 loại (NO_RELATION) |

### Thay đổi NER

- E1 “lấy mẫu” PROCEDURE [31, 38) → E1 “lấy mẫu” TEST [31, 38)

Nguồn: VietMed-NER train, dòng 2125 (từ 0).

## VM600-272

**Đoạn gốc:** nhiễm chéo thì như tôi cũng đã trình bày đầu chương trình đó là virus nó không có tự đi mà nó do chúng ta mang theo mà

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E2 | nhiễm chéo | Bệnh hoặc triệu chứng (CONDITION) | [0, 10) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Thay đổi NER

- E1 “virus” CONDITION [64, 69) → ∅
- ∅ → E2 “nhiễm chéo” CONDITION [0, 10)

Nguồn: VietMed-NER train, dòng 2138 (từ 0).

## VM600-273

**Đoạn gốc:** động mạch thì mình vẫn hoàn toàn có thể sử dụng sớm để ngăn ngừa cái tình trạng xơ vữa động mạch nó có thể xuất hiện rất

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | động mạch | Bộ phận cơ thể (BODY_PART) | [0, 9) |
| E3 | xơ vữa động mạch | Bệnh hoặc triệu chứng (CONDITION) | [80, 96) |

### RE

| Mã | Cặp có hướng | Kết luận đề xuất |
|---|---|---|
| R1 | E3 “xơ vữa động mạch” → E1 “động mạch” | Không có quan hệ thuộc 5 loại (NO_RELATION) |

### Cần chốt

- CONTEXT_OR_TRANSCRIPT: câu bị cắt, tham chiếu/mục đích chưa rõ hoặc nghi lỗi phiên âm; cần xem ngữ cảnh/audio gốc, không tự sửa văn bản.

### Thay đổi NER

- E2 “ngăn ngừa” DRUG [55, 64) → ∅
- E3 “tình trạng xơ vữa động mạch” CONDITION [69, 96) → E3 “xơ vữa động mạch” CONDITION [80, 96)

Nguồn: VietMed-NER train, dòng 2141 (từ 0).

## VM600-274

**Đoạn gốc:** bối cảnh chung cùng với các chuyên khoa khác chứ không tách rời ra thứ hai trong cái việc mà điều trị bằng thuốc

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | điều trị | Thủ thuật hoặc điều trị (PROCEDURE) | [93, 101) |
| E2 | thuốc | Thuốc/dược chất (DRUG) | [107, 112) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- GENERIC_INTERVENTION: cần chốt việc giữ hành động điều trị/chẩn đoán chung khi không nêu phương pháp cụ thể.

Nguồn: VietMed-NER train, dòng 2151 (từ 0).

## VM600-275

**Đoạn gốc:** xe đạp trên giường chứ tuyệt nhiên là chúng ta không vì thế mà chúng ta lại cứ đi nhiều thế còn cái việc mà hôm nay

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

Không có thực thể thuộc sáu loại được giữ trong bản rà soát.

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- CONTEXT_OR_TRANSCRIPT: câu bị cắt, tham chiếu/mục đích chưa rõ hoặc nghi lỗi phiên âm; cần xem ngữ cảnh/audio gốc, không tự sửa văn bản.

Nguồn: VietMed-NER train, dòng 2153 (từ 0).

## VM600-276

**Đoạn gốc:** người ta là sức khỏe và trí tuệ có sức khỏe thì mới có trí tuệ và hiện nay thì

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

Không có thực thể thuộc sáu loại được giữ trong bản rà soát.

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

Nguồn: VietMed-NER train, dòng 2178 (từ 0).

## VM600-277

**Đoạn gốc:** khác nhau và theo như lời chia sẻ của các bác sĩ thì khi thuốc không còn kiểm

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | thuốc | Thuốc/dược chất (DRUG) | [57, 62) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

Nguồn: VietMed-NER train, dòng 2181 (từ 0).

## VM600-278

**Đoạn gốc:** thậm chí là thất vọng với bản thân mình cảm thấy là ôi thất bại rồi thất bại rồi thì có người coi đây đó là những cái

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

Không có thực thể thuộc sáu loại được giữ trong bản rà soát.

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

Nguồn: VietMed-NER train, dòng 2187 (từ 0).

## VM600-279

**Đoạn gốc:** giá thêm đúng là rung nhĩ đánh giá đến mức độ của nó đánh giá nguy cơ là như thế nào và thậm chí đánh giá các nguyên

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | rung nhĩ | Bệnh hoặc triệu chứng (CONDITION) | [17, 25) |
| E2 | đánh giá | Xét nghiệm hoặc thăm khám (TEST) | [26, 34) |
| E4 | đánh giá nguy cơ | Xét nghiệm hoặc thăm khám (TEST) | [53, 69) |
| E5 | đánh giá | Xét nghiệm hoặc thăm khám (TEST) | [97, 105) |

### RE

| Mã | Cặp có hướng | Kết luận đề xuất |
|---|---|---|
| R1 | E1 “rung nhĩ” → E2 “đánh giá” | Chưa rõ — cần chốt (CHUA_RO) |
| R2 | E1 “rung nhĩ” → E4 “đánh giá nguy cơ” | Chưa rõ — cần chốt (CHUA_RO) |
| R3 | E1 “rung nhĩ” → E5 “đánh giá” | Chưa rõ — cần chốt (CHUA_RO) |

### Cần chốt

- CONTEXT_OR_TRANSCRIPT: câu bị cắt, tham chiếu/mục đích chưa rõ hoặc nghi lỗi phiên âm; cần xem ngữ cảnh/audio gốc, không tự sửa văn bản.
- GENERIC_INTERVENTION: cần chốt việc giữ hành động điều trị/chẩn đoán chung khi không nêu phương pháp cụ thể.
- UNRESOLVED_RE: còn cặp CHUA_RO; tuyệt đối không đổi thành NO_RELATION khi xuất huấn luyện.

### Thay đổi NER

- E3 “mức độ” DOSAGE [39, 45) → ∅
- E2 “đánh giá” PROCEDURE [26, 34) → E2 “đánh giá” TEST [26, 34)
- E5 “đánh giá” PROCEDURE [97, 105) → E5 “đánh giá” TEST [97, 105)

Nguồn: VietMed-NER train, dòng 2189 (từ 0).

## VM600-280

**Đoạn gốc:** kẻ thua cuộc chúng ta đã học được rằng một phần của vấn đề là người cao tuổi có

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

Không có thực thể thuộc sáu loại được giữ trong bản rà soát.

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Thay đổi NER

- E1 “một phần” DOSAGE [39, 47) → ∅

Nguồn: VietMed-NER train, dòng 2196 (từ 0).

## VM600-281

**Đoạn gốc:** phương thức tiếp cận trên cái thực tế thì các bước quản lý về duy trì cân nặng ổn định đó thì nhiều khi nó còn rất là

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

Không có thực thể thuộc sáu loại được giữ trong bản rà soát.

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

Nguồn: VietMed-NER train, dòng 2204 (từ 0).

## VM600-282

**Đoạn gốc:** xưa thì các cụ là dùng toàn thể hoặc có thể dùng vỏ quả thể nhưng mà cho đến hiện nay khi mà nghiên cứu các thành

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | vỏ quả thể | Thuốc/dược chất (DRUG) | [49, 59) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- ONTOLOGY_SCOPE: cần chốt phạm vi thuốc/dược chất so với mỹ phẩm, thực phẩm, hóa chất nội sinh hoặc hệ vi sinh; giữ ánh xạ nguồn khi chưa có quy ước đủ rõ.

### Thay đổi NER

- E2 “nghiên cứu” TEST [93, 103) → ∅

Nguồn: VietMed-NER train, dòng 2211 (từ 0).

## VM600-283

**Đoạn gốc:** có thể nói là nó phát triển rất là dữ dội và nếu như người già thì chúng ta có thể nhờ con cháu của mình để có thể phối

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

Không có thực thể thuộc sáu loại được giữ trong bản rà soát.

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

Nguồn: VietMed-NER train, dòng 2212 (từ 0).

## VM600-284

**Đoạn gốc:** cô lập càng xa lánh càng tránh né để mà

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

Không có thực thể thuộc sáu loại được giữ trong bản rà soát.

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

Nguồn: VietMed-NER train, dòng 2215 (từ 0).

## VM600-285

**Đoạn gốc:** là không có hương liệu không có chất bảo quản còn đối với kem dưỡng ẩm thì đối với lại dưỡng ẩm ban ngày thì sau khi

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | hương liệu | Thuốc/dược chất (DRUG) | [12, 22) |
| E2 | chất bảo quản | Thuốc/dược chất (DRUG) | [32, 45) |
| E3 | kem dưỡng ẩm | Thuốc/dược chất (DRUG) | [58, 70) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- ONTOLOGY_SCOPE: cần chốt phạm vi thuốc/dược chất so với mỹ phẩm, thực phẩm, hóa chất nội sinh hoặc hệ vi sinh; giữ ánh xạ nguồn khi chưa có quy ước đủ rõ.

Nguồn: VietMed-NER train, dòng 2216 (từ 0).

## VM600-286

**Đoạn gốc:** bệnh nhân béo phì đến thì sẽ đưa ra các mục tiêu điều trị cho bệnh nhân thì các mục tiêu ngắn hạn đó là sẽ giảm từ năm

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | béo phì | Bệnh hoặc triệu chứng (CONDITION) | [10, 17) |
| E2 | điều trị | Thủ thuật hoặc điều trị (PROCEDURE) | [49, 57) |

### RE

| Mã | Cặp có hướng | Kết luận đề xuất |
|---|---|---|
| R1 | E1 “béo phì” → E2 “điều trị” | Được điều trị bằng phương pháp (treated_by_procedure) |

### Cần chốt

- CONTEXT_OR_TRANSCRIPT: câu bị cắt, tham chiếu/mục đích chưa rõ hoặc nghi lỗi phiên âm; cần xem ngữ cảnh/audio gốc, không tự sửa văn bản.
- GENERIC_INTERVENTION: cần chốt việc giữ hành động điều trị/chẩn đoán chung khi không nêu phương pháp cụ thể.

Nguồn: VietMed-NER train, dòng 2219 (từ 0).

## VM600-287

**Đoạn gốc:** cung cấp hay là cái nhu cầu và mức độ thỏa mãn cho nên khi mà mình có cái nhu cầu

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

Không có thực thể thuộc sáu loại được giữ trong bản rà soát.

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Thay đổi NER

- E1 “mức độ” DOSAGE [31, 37) → ∅

Nguồn: VietMed-NER train, dòng 2228 (từ 0).

## VM600-288

**Đoạn gốc:** điều hướng tất cả các lựa chọn là một việc hữu ích đặc biệt là khi bạn phải đối mặt với quảng cáo tốt cho đường ruột

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | đường ruột | Bộ phận cơ thể (BODY_PART) | [106, 116) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

Nguồn: VietMed-NER train, dòng 2237 (từ 0).

## VM600-289

**Đoạn gốc:** hệ tác động qua lại hai chiều giữa tâm lý người bệnh và cái căn bệnh béo phì này đó nó thường khiến cho cái tình

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | béo phì | Bệnh hoặc triệu chứng (CONDITION) | [69, 76) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

Nguồn: VietMed-NER train, dòng 2251 (từ 0).

## VM600-290

**Đoạn gốc:** với nhóm chất béo chúng ta nên sử dụng chất béo từ các loại hạt chất

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | chất béo | Thuốc/dược chất (DRUG) | [9, 17) |
| E2 | chất béo | Thuốc/dược chất (DRUG) | [39, 47) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- ONTOLOGY_SCOPE: cần chốt phạm vi thuốc/dược chất so với mỹ phẩm, thực phẩm, hóa chất nội sinh hoặc hệ vi sinh; giữ ánh xạ nguồn khi chưa có quy ước đủ rõ.

Nguồn: VietMed-NER train, dòng 2257 (từ 0).

## VM600-291

**Đoạn gốc:** bảy bạn đã cắt amidan chưa tám bạn đã

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | cắt amidan | Thủ thuật hoặc điều trị (PROCEDURE) | [11, 21) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- CONTEXT_OR_TRANSCRIPT: câu bị cắt, tham chiếu/mục đích chưa rõ hoặc nghi lỗi phiên âm; cần xem ngữ cảnh/audio gốc, không tự sửa văn bản.

### Thay đổi NER

- E1 “amidan” CONDITION [15, 21) → E1 “cắt amidan” PROCEDURE [11, 21)

Nguồn: VietMed-NER train, dòng 2261 (từ 0).

## VM600-292

**Đoạn gốc:** một số những cái vấn đề mà liên quan tới cái việc điều trị tâm lý ở trong cái

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | điều trị tâm lý | Thủ thuật hoặc điều trị (PROCEDURE) | [50, 65) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Thay đổi NER

- E1 “điều trị” PROCEDURE [50, 58) → E1 “điều trị tâm lý” PROCEDURE [50, 65)

Nguồn: VietMed-NER train, dòng 2263 (từ 0).

## VM600-293

**Đoạn gốc:** thể bị bất hoạt bởi nhiệt và một lượng nhỏ hóa chất formalin điều này có nghĩa

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E2 | formalin | Thuốc/dược chất (DRUG) | [52, 60) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- SCOPE_CONFIRMATION: cần xác nhận quy ước về thuốc/dược chất, can thiệp không dùng thuốc, thiết bị, tác nhân hoặc hoạt động thăm khám; không coi ánh xạ nguồn là xác nhận chuyên gia.

### Thay đổi NER

- E1 “hóa chất” DRUG [43, 51) → ∅

Nguồn: VietMed-NER train, dòng 2278 (từ 0).

## VM600-294

**Đoạn gốc:** cái nghịch cảnh mình tạo ra để làm gì chị em biết là nếu mà mình có một cái

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

Không có thực thể thuộc sáu loại được giữ trong bản rà soát.

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

Nguồn: VietMed-NER train, dòng 2286 (từ 0).

## VM600-295

**Đoạn gốc:** dụng cái chế độ ăn cháo và súp thì bao giờ nó cũng mềm lỏng hơn so với cơm giúp

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

Không có thực thể thuộc sáu loại được giữ trong bản rà soát.

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

Nguồn: VietMed-NER train, dòng 2287 (từ 0).

## VM600-296

**Đoạn gốc:** chúng ta nó bệnh dại

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | bệnh dại | Bệnh hoặc triệu chứng (CONDITION) | [12, 20) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

Nguồn: VietMed-NER train, dòng 2288 (từ 0).

## VM600-297

**Đoạn gốc:** dạ vâng chương trình đường truyền nó kém quá tóm lại hiện nay là cô bị tình trạng như

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

Không có thực thể thuộc sáu loại được giữ trong bản rà soát.

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- CONTEXT_OR_TRANSCRIPT: câu bị cắt, tham chiếu/mục đích chưa rõ hoặc nghi lỗi phiên âm; cần xem ngữ cảnh/audio gốc, không tự sửa văn bản.

Nguồn: VietMed-NER train, dòng 2294 (từ 0).

## VM600-298

**Đoạn gốc:** méo miệng yếu tay chân và giọng lời nói giọng nói có vấn đề thì đó

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | méo miệng | Bệnh hoặc triệu chứng (CONDITION) | [0, 9) |
| E2 | yếu tay chân | Bệnh hoặc triệu chứng (CONDITION) | [10, 22) |
| E3 | giọng lời nói giọng nói có vấn đề | Bệnh hoặc triệu chứng (CONDITION) | [26, 59) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- CONTEXT_OR_TRANSCRIPT: câu bị cắt, tham chiếu/mục đích chưa rõ hoặc nghi lỗi phiên âm; cần xem ngữ cảnh/audio gốc, không tự sửa văn bản.

### Thay đổi NER

- E2 “yếu tay” CONDITION [10, 17) → E2 “yếu tay chân” CONDITION [10, 22)

Nguồn: VietMed-NER train, dòng 2311 (từ 0).

## VM600-299

**Đoạn gốc:** nào như vậy thì bệnh nhân sẽ phải trước đó mình phải được tư vấn trong quá trình phải hợp tác với với bác sĩ ví dụ như

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

Không có thực thể thuộc sáu loại được giữ trong bản rà soát.

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

Nguồn: VietMed-NER train, dòng 2315 (từ 0).

## VM600-300

**Đoạn gốc:** dinh dưỡng trong cơ thể chúng ta nó sản sinh ra các tế bào thì mỗi một cái tế bào ung thư điều rất cần đến năng lượng

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | cơ thể | Bộ phận cơ thể (BODY_PART) | [17, 23) |
| E2 | tế bào | Bộ phận cơ thể (BODY_PART) | [52, 58) |
| E3 | tế bào ung thư | Bệnh hoặc triệu chứng (CONDITION) | [75, 89) |

### RE

| Mã | Cặp có hướng | Kết luận đề xuất |
|---|---|---|
| R1 | E3 “tế bào ung thư” → E1 “cơ thể” | Chưa rõ — cần chốt (CHUA_RO) |
| R2 | E3 “tế bào ung thư” → E2 “tế bào” | Không có quan hệ thuộc 5 loại (NO_RELATION) |

### Cần chốt

- CONTEXT_OR_TRANSCRIPT: câu bị cắt, tham chiếu/mục đích chưa rõ hoặc nghi lỗi phiên âm; cần xem ngữ cảnh/audio gốc, không tự sửa văn bản.
- UNRESOLVED_RE: còn cặp CHUA_RO; tuyệt đối không đổi thành NO_RELATION khi xuất huấn luyện.

Nguồn: VietMed-NER train, dòng 2318 (từ 0).

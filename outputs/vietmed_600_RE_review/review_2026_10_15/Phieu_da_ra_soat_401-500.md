# Phiếu rà soát NER và RE 401 đến 500

Bản AI rà soát lần hai ngày 15/10/2026. Giữ nguyên câu nguồn và sáu loại NER, năm quan hệ RE. Chưa được chuyên gia xác nhận.

Quy tắc người dùng đã chốt: giữ cả cụm bệnh/triệu chứng trong một CONDITION. Không tách bộ phận bên trong cụm để tạo located_at. Vị trí được nêu riêng bằng giới từ hoặc mệnh đề riêng vẫn được xét.

Vị trí ký tự là khoảng [start, end), đếm từ 0 theo Unicode. Mã E ổn định khi sửa; mã R được tạo lại. Không dùng CHUA_RO làm nhãn huấn luyện hoặc nhãn âm.

## VM600-401

**Đoạn gốc:** sau mười năm thì triệu chứng các triệu chứng ngoài vận động nó xuất hiện nhiều hơn sa sút trí tuệ rồi táo bón rồi mất ổn định

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E2 | triệu chứng ngoài vận động | Bệnh hoặc triệu chứng (CONDITION) | [33, 59) |
| E3 | sa sút trí tuệ | Bệnh hoặc triệu chứng (CONDITION) | [83, 97) |
| E4 | táo bón | Bệnh hoặc triệu chứng (CONDITION) | [102, 109) |
| E5 | mất ổn định | Bệnh hoặc triệu chứng (CONDITION) | [114, 125) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- CONTEXT_OR_TRANSCRIPT: câu bị cắt, tham chiếu/mục đích chưa rõ hoặc nghi lỗi phiên âm; cần xem ngữ cảnh/audio gốc, không tự sửa văn bản.

### Thay đổi NER

- E1 “triệu chứng” CONDITION [17, 28) → ∅
- E2 “triệu chứng” CONDITION [33, 44) → E2 “triệu chứng ngoài vận động” CONDITION [33, 59)
- ∅ → E5 “mất ổn định” CONDITION [114, 125)

Nguồn: VietMed-NER train, dòng 3011 (từ 0).

## VM600-402

**Đoạn gốc:** chắn sẽ dẫn tình trạng cơ thể tình trạng cơ thể chúng ta dẫn đến suy kiệt và chúng ta không còn được cả cái sức đề

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | cơ thể | Bộ phận cơ thể (BODY_PART) | [23, 29) |
| E2 | cơ thể | Bộ phận cơ thể (BODY_PART) | [41, 47) |
| E3 | suy kiệt | Bệnh hoặc triệu chứng (CONDITION) | [65, 73) |

### RE

| Mã | Cặp có hướng | Kết luận đề xuất |
|---|---|---|
| R1 | E3 “suy kiệt” → E1 “cơ thể” | Không có quan hệ thuộc 5 loại (NO_RELATION) |
| R2 | E3 “suy kiệt” → E2 “cơ thể” | Không có quan hệ thuộc 5 loại (NO_RELATION) |

Nguồn: VietMed-NER train, dòng 3026 (từ 0).

## VM600-403

**Đoạn gốc:** bị ngã ta phải đỡ ngay giữa ngay để người bệnh không có bị ngã không bị chấn thương rồi nếu mà bệnh nhân đang ăn ăn

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | chấn thương | Bệnh hoặc triệu chứng (CONDITION) | [72, 83) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

Nguồn: VietMed-NER train, dòng 3027 (từ 0).

## VM600-404

**Đoạn gốc:** được tốt nhất vai trò thứ ba của đối với lại dinh dưỡng đó là dinh dưỡng thậm chí

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

Không có thực thể thuộc sáu loại được giữ trong bản rà soát.

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

Nguồn: VietMed-NER train, dòng 3033 (từ 0).

## VM600-405

**Đoạn gốc:** nào là đông trùng hạ thảo công dụng của nó ra sao đặc biệt là chúng ta có kiến

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | đông trùng hạ thảo | Thuốc/dược chất (DRUG) | [7, 25) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

Nguồn: VietMed-NER train, dòng 3039 (từ 0).

## VM600-406

**Đoạn gốc:** yếu đầu tiên là yếu tay yếu chân yếu thứ hai là giữa các cơ mặt làm cho mặt

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | yếu tay | Bệnh hoặc triệu chứng (CONDITION) | [16, 23) |
| E2 | yếu chân | Bệnh hoặc triệu chứng (CONDITION) | [24, 32) |
| E3 | cơ mặt | Bộ phận cơ thể (BODY_PART) | [57, 63) |
| E4 | mặt | Bộ phận cơ thể (BODY_PART) | [72, 75) |

### RE

| Mã | Cặp có hướng | Kết luận đề xuất |
|---|---|---|
| R1 | E1 “yếu tay” → E3 “cơ mặt” | Không có quan hệ thuộc 5 loại (NO_RELATION) |
| R2 | E1 “yếu tay” → E4 “mặt” | Không có quan hệ thuộc 5 loại (NO_RELATION) |
| R3 | E2 “yếu chân” → E3 “cơ mặt” | Không có quan hệ thuộc 5 loại (NO_RELATION) |
| R4 | E2 “yếu chân” → E4 “mặt” | Không có quan hệ thuộc 5 loại (NO_RELATION) |

### Cần chốt

- CONTEXT_OR_TRANSCRIPT: câu bị cắt, tham chiếu/mục đích chưa rõ hoặc nghi lỗi phiên âm; cần xem ngữ cảnh/audio gốc, không tự sửa văn bản.

### Thay đổi NER

- ∅ → E4 “mặt” BODY_PART [72, 75)

Nguồn: VietMed-NER train, dòng 3062 (từ 0).

## VM600-407

**Đoạn gốc:** của bác là não thì nó sẽ gây ra rất nhiều triệu chứng khác nhau trong đó có người thì ví dụ như bác là mất ngủ là

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | não | Bộ phận cơ thể (BODY_PART) | [11, 14) |
| E4 | mất ngủ | Bệnh hoặc triệu chứng (CONDITION) | [103, 110) |

### RE

| Mã | Cặp có hướng | Kết luận đề xuất |
|---|---|---|
| R1 | E4 “mất ngủ” → E1 “não” | Không có quan hệ thuộc 5 loại (NO_RELATION) |

### Thay đổi NER

- E2 “rất nhiều” DOSAGE [32, 41) → ∅
- E3 “triệu chứng” CONDITION [42, 53) → ∅

Nguồn: VietMed-NER train, dòng 3069 (từ 0).

## VM600-408

**Đoạn gốc:** đoạn sau sanh thì mái tóc dễ gọi là nó mềm mại và nó yếu ớt thế cho nên là

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | mái tóc | Bộ phận cơ thể (BODY_PART) | [18, 25) |
| E2 | yếu ớt | Bệnh hoặc triệu chứng (CONDITION) | [53, 59) |

### RE

| Mã | Cặp có hướng | Kết luận đề xuất |
|---|---|---|
| R1 | E2 “yếu ớt” → E1 “mái tóc” | Có vị trí ở (located_at) |

### Cần chốt

- CONTEXT_OR_TRANSCRIPT: câu bị cắt, tham chiếu/mục đích chưa rõ hoặc nghi lỗi phiên âm; cần xem ngữ cảnh/audio gốc, không tự sửa văn bản.

Nguồn: VietMed-NER train, dòng 3070 (từ 0).

## VM600-409

**Đoạn gốc:** tiết được pepsin và tiết không tiết được pepsin của dạ dày chỉ liên quan đến một phần kể

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | pepsin | Thuốc/dược chất (DRUG) | [10, 16) |
| E2 | pepsin | Thuốc/dược chất (DRUG) | [41, 47) |
| E3 | dạ dày | Bộ phận cơ thể (BODY_PART) | [52, 58) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- ONTOLOGY_SCOPE: cần chốt phạm vi thuốc/dược chất so với mỹ phẩm, thực phẩm, hóa chất nội sinh hoặc hệ vi sinh; giữ ánh xạ nguồn khi chưa có quy ước đủ rõ.

### Thay đổi NER

- E4 “một phần” DOSAGE [77, 85) → ∅

Nguồn: VietMed-NER train, dòng 3071 (từ 0).

## VM600-410

**Đoạn gốc:** biết rằng là những người bệnh kích thích những người bệnh parkinson mà cần phẫu thuốc kích thích não sâu thì chúng

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | parkinson | Bệnh hoặc triệu chứng (CONDITION) | [58, 67) |
| E3 | kích thích não sâu | Thủ thuật hoặc điều trị (PROCEDURE) | [86, 104) |

### RE

| Mã | Cặp có hướng | Kết luận đề xuất |
|---|---|---|
| R1 | E1 “parkinson” → E3 “kích thích não sâu” | Được điều trị bằng phương pháp (treated_by_procedure) |

### Cần chốt

- CONTEXT_OR_TRANSCRIPT: câu bị cắt, tham chiếu/mục đích chưa rõ hoặc nghi lỗi phiên âm; cần xem ngữ cảnh/audio gốc, không tự sửa văn bản.

### Thay đổi NER

- E2 “thuốc” DRUG [80, 85) → ∅

Nguồn: VietMed-NER train, dòng 3077 (từ 0).

## VM600-411

**Đoạn gốc:** mình sẽ kiểm tra những các thiết bị bên ngoài đảm bảo có thể thống nhất rồi thì lúc đó là kết thúc phẫu thuật

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E2 | phẫu thuật | Thủ thuật hoặc điều trị (PROCEDURE) | [99, 109) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Thay đổi NER

- E1 “kiểm tra” TEST [8, 16) → ∅

Nguồn: VietMed-NER train, dòng 3085 (từ 0).

## VM600-412

**Đoạn gốc:** ngoại khoa thì là cái từ trong chuyên môn nhưng mà để nói cho dễ hiểu đó là mổ thì người ta có chia làm hai cái nhóm

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | ngoại khoa | Thủ thuật hoặc điều trị (PROCEDURE) | [0, 10) |
| E2 | mổ | Thủ thuật hoặc điều trị (PROCEDURE) | [76, 78) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- SCOPE_CONFIRMATION: cần xác nhận quy ước về thuốc/dược chất, can thiệp không dùng thuốc, thiết bị, tác nhân hoặc hoạt động thăm khám; không coi ánh xạ nguồn là xác nhận chuyên gia.

Nguồn: VietMed-NER train, dòng 3086 (từ 0).

## VM600-413

**Đoạn gốc:** là một sự tán thành lớn cho quan điểm rằng thực phẩm quan trọng vượt trội hơn hoàn cảnh khác trong cuộc sống mà chúng

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

Không có thực thể thuộc sáu loại được giữ trong bản rà soát.

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

Nguồn: VietMed-NER train, dòng 3092 (từ 0).

## VM600-414

**Đoạn gốc:** viêm loét đại tràng và ung thư chúng ta sẽ khám phá quá trình này chi tiết hơn

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | viêm loét đại tràng | Bệnh hoặc triệu chứng (CONDITION) | [0, 19) |
| E3 | ung thư | Bệnh hoặc triệu chứng (CONDITION) | [23, 30) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Thay đổi NER

- E4 “khám” TEST [43, 47) → ∅
- E1 “viêm loét” CONDITION [0, 9) → E1 “viêm loét đại tràng” CONDITION [0, 19)
- E2 “đại tràng” BODY_PART [10, 19) → ∅

Nguồn: VietMed-NER train, dòng 3093 (từ 0).

## VM600-415

**Đoạn gốc:** khô hơn đôi khi là từ một cái làn da là thường mà trở thành một cái làn da nhạy cảm dễ gây kích ứng và dị ứng hơn do đó

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E5 | khô | Bệnh hoặc triệu chứng (CONDITION) | [0, 3) |
| E1 | làn da | Bộ phận cơ thể (BODY_PART) | [30, 36) |
| E2 | làn da nhạy cảm | Bệnh hoặc triệu chứng (CONDITION) | [68, 83) |
| E3 | kích ứng | Bệnh hoặc triệu chứng (CONDITION) | [91, 99) |
| E4 | dị ứng | Bệnh hoặc triệu chứng (CONDITION) | [103, 109) |

### RE

| Mã | Cặp có hướng | Kết luận đề xuất |
|---|---|---|
| R1 | E5 “khô” → E1 “làn da” | Chưa rõ — cần chốt (CHUA_RO) |
| R2 | E2 “làn da nhạy cảm” → E1 “làn da” | Chưa rõ — cần chốt (CHUA_RO) |
| R3 | E3 “kích ứng” → E1 “làn da” | Chưa rõ — cần chốt (CHUA_RO) |
| R4 | E4 “dị ứng” → E1 “làn da” | Chưa rõ — cần chốt (CHUA_RO) |

### Cần chốt

- CONTEXT_OR_TRANSCRIPT: câu bị cắt, tham chiếu/mục đích chưa rõ hoặc nghi lỗi phiên âm; cần xem ngữ cảnh/audio gốc, không tự sửa văn bản.
- UNRESOLVED_RE: còn cặp CHUA_RO; tuyệt đối không đổi thành NO_RELATION khi xuất huấn luyện.

### Thay đổi NER

- ∅ → E5 “khô” CONDITION [0, 3)

Nguồn: VietMed-NER train, dòng 3120 (từ 0).

## VM600-416

**Đoạn gốc:** cũng xin nhờ bác sĩ có thể cho biết cụ thể hơn về mối quan hệ cũng như là tác

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

Không có thực thể thuộc sáu loại được giữ trong bản rà soát.

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Thay đổi NER

- E1 “quan hệ” CONDITION [54, 61) → ∅

Nguồn: VietMed-NER train, dòng 3126 (từ 0).

## VM600-417

**Đoạn gốc:** tôi sẽ giúp bạn làm điều đó giải thích khoa học đằng sau lợi khuẩn và cách chọn

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | lợi khuẩn | Thuốc/dược chất (DRUG) | [57, 66) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- ONTOLOGY_SCOPE: cần chốt phạm vi thuốc/dược chất so với mỹ phẩm, thực phẩm, hóa chất nội sinh hoặc hệ vi sinh; giữ ánh xạ nguồn khi chưa có quy ước đủ rõ.

Nguồn: VietMed-NER train, dòng 3127 (từ 0).

## VM600-418

**Đoạn gốc:** người dân đã cho chúng tôi nhiều cái thông tin ví dụ như những trường hợp tai nạn bất ngờ những bệnh tật mà phải cấp

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | tai nạn | Bệnh hoặc triệu chứng (CONDITION) | [74, 81) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- GENERIC_MENTION: cần chốt có giữ bệnh/triệu chứng/biến chứng chung và tham chiếu không định danh trong NER hay không.

Nguồn: VietMed-NER train, dòng 3131 (từ 0).

## VM600-419

**Đoạn gốc:** huyết áp này những người bị rối loạn mỡ máu này những người các bệnh lý bệnh tim mạch thì nó sẽ có cái tác động lên các

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | huyết áp | Bệnh hoặc triệu chứng (CONDITION) | [0, 8) |
| E2 | rối loạn mỡ máu | Bệnh hoặc triệu chứng (CONDITION) | [28, 43) |
| E4 | bệnh tim mạch | Bệnh hoặc triệu chứng (CONDITION) | [72, 85) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- CONTEXT_OR_TRANSCRIPT: câu bị cắt, tham chiếu/mục đích chưa rõ hoặc nghi lỗi phiên âm; cần xem ngữ cảnh/audio gốc, không tự sửa văn bản.
- PHYSIOLOGY_VS_DISEASE: từ huyết áp/mỡ máu đứng riêng chưa xác định bệnh; giữ đề xuất nguồn chờ chốt.

### Thay đổi NER

- ∅ → E4 “bệnh” CONDITION [72, 76)
- E4 “bệnh” CONDITION [72, 76) → E4 “bệnh tim mạch” CONDITION [72, 85)
- E3 “tim mạch” BODY_PART [77, 85) → ∅

Nguồn: VietMed-NER train, dòng 3133 (từ 0).

## VM600-420

**Đoạn gốc:** bôi kem dưỡng trước khi đi ngủ nhưng ngủ dậy mặt vẫn còn nhiều dầu xưng cháu vậy

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | kem dưỡng | Thuốc/dược chất (DRUG) | [4, 13) |
| E2 | mặt | Bộ phận cơ thể (BODY_PART) | [45, 48) |
| E3 | nhiều dầu | Bệnh hoặc triệu chứng (CONDITION) | [57, 66) |

### RE

| Mã | Cặp có hướng | Kết luận đề xuất |
|---|---|---|
| R1 | E3 “nhiều dầu” → E1 “kem dưỡng” | Không có quan hệ thuộc 5 loại (NO_RELATION) |
| R2 | E3 “nhiều dầu” → E2 “mặt” | Có vị trí ở (located_at) |

### Cần chốt

- CONTEXT_OR_TRANSCRIPT: câu bị cắt, tham chiếu/mục đích chưa rõ hoặc nghi lỗi phiên âm; cần xem ngữ cảnh/audio gốc, không tự sửa văn bản.
- ONTOLOGY_SCOPE: cần chốt phạm vi thuốc/dược chất so với mỹ phẩm, thực phẩm, hóa chất nội sinh hoặc hệ vi sinh; giữ ánh xạ nguồn khi chưa có quy ước đủ rõ.

### Thay đổi NER

- ∅ → E2 “mặt” BODY_PART [45, 48)
- ∅ → E3 “nhiều dầu” CONDITION [57, 66)

Nguồn: VietMed-NER train, dòng 3139 (từ 0).

## VM600-421

**Đoạn gốc:** trị béo phì nó rất là ngoạn mục và sau này nó không chỉ về cải thiện cái hình ảnh mà nó giúp làm cho chúng ta

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | béo phì | Bệnh hoặc triệu chứng (CONDITION) | [4, 11) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- CONTEXT_OR_TRANSCRIPT: câu bị cắt, tham chiếu/mục đích chưa rõ hoặc nghi lỗi phiên âm; cần xem ngữ cảnh/audio gốc, không tự sửa văn bản.

### Thay đổi NER

- E2 “cải thiện” PROCEDURE [59, 68) → ∅

Nguồn: VietMed-NER train, dòng 3142 (từ 0).

## VM600-422

**Đoạn gốc:** thì không phải là của riêng ai cả đối tượng nào chúng ta cũng rất là dễ gặp phải và chúng tôi cũng để ý là có những

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

Không có thực thể thuộc sáu loại được giữ trong bản rà soát.

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

Nguồn: VietMed-NER train, dòng 3143 (từ 0).

## VM600-423

**Đoạn gốc:** trị chưa hiện nay chưa có cái phương pháp nào điều trị khỏi mà chỉ là điều trị để giúp cho mình đưa cái con số

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | điều trị | Thủ thuật hoặc điều trị (PROCEDURE) | [46, 54) |
| E2 | điều trị | Thủ thuật hoặc điều trị (PROCEDURE) | [70, 78) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- CONTEXT_OR_TRANSCRIPT: câu bị cắt, tham chiếu/mục đích chưa rõ hoặc nghi lỗi phiên âm; cần xem ngữ cảnh/audio gốc, không tự sửa văn bản.
- GENERIC_INTERVENTION: cần chốt việc giữ hành động điều trị/chẩn đoán chung khi không nêu phương pháp cụ thể.

Nguồn: VietMed-NER train, dòng 3162 (từ 0).

## VM600-424

**Đoạn gốc:** thậm chí gây tử vong bạn có thể không quen được với phía bên kia của câu chuyện rằng mỗi nhịp tim nhịp thở và sợ

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | tử vong | Bệnh hoặc triệu chứng (CONDITION) | [13, 20) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- CONTEXT_OR_TRANSCRIPT: câu bị cắt, tham chiếu/mục đích chưa rõ hoặc nghi lỗi phiên âm; cần xem ngữ cảnh/audio gốc, không tự sửa văn bản.

### Thay đổi NER

- E2 “nhịp tim” DOSAGE [89, 97) → ∅
- E3 “nhịp thở” DOSAGE [98, 106) → ∅

Nguồn: VietMed-NER train, dòng 3165 (từ 0).

## VM600-425

**Đoạn gốc:** khỏi ra tình trạng bệnh và đây của chúng ta là ung thư thì cái tinh thần của người bị bệnh rất kiên cường cái thứ hai đó là chúng ta

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | ung thư | Bệnh hoặc triệu chứng (CONDITION) | [47, 54) |
| E2 | bệnh | Bệnh hoặc triệu chứng (CONDITION) | [86, 90) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- GENERIC_MENTION: cần chốt có giữ bệnh/triệu chứng/biến chứng chung và tham chiếu không định danh trong NER hay không.

### Thay đổi NER

- E3 “cái thứ hai” DOSAGE [106, 117) → ∅
- E2 “bị bệnh” CONDITION [83, 90) → E2 “bệnh” CONDITION [86, 90)

Nguồn: VietMed-NER train, dòng 3166 (từ 0).

## VM600-426

**Đoạn gốc:** nhiều các phương pháp điều trị được được điều trị áp dụng chẩn đoán sớm vân vân thì tuổi thọ của người việt nam của

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | điều trị | Thủ thuật hoặc điều trị (PROCEDURE) | [22, 30) |
| E2 | điều trị | Thủ thuật hoặc điều trị (PROCEDURE) | [41, 49) |
| E3 | chẩn đoán | Xét nghiệm hoặc thăm khám (TEST) | [58, 67) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- CONTEXT_OR_TRANSCRIPT: câu bị cắt, tham chiếu/mục đích chưa rõ hoặc nghi lỗi phiên âm; cần xem ngữ cảnh/audio gốc, không tự sửa văn bản.
- GENERIC_INTERVENTION: cần chốt việc giữ hành động điều trị/chẩn đoán chung khi không nêu phương pháp cụ thể.

Nguồn: VietMed-NER train, dòng 3172 (từ 0).

## VM600-427

**Đoạn gốc:** bắt đầu từ ruột điều này xảy ra rất lâu trước khi nền văn minh có bất kỳ bằng chứng hoặc lý thuyết vững vàng nào để

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | ruột | Bộ phận cơ thể (BODY_PART) | [11, 15) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

Nguồn: VietMed-NER train, dòng 3177 (từ 0).

## VM600-428

**Đoạn gốc:** với đái tháo đường thì nó có rất rất nhiều các thể lụy những cái biến chứng của nó thế thì khi mà chúng ta bị đái

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | đái tháo đường | Bệnh hoặc triệu chứng (CONDITION) | [4, 18) |
| E3 | biến chứng | Bệnh hoặc triệu chứng (CONDITION) | [65, 75) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- GENERIC_MENTION: cần chốt có giữ bệnh/triệu chứng/biến chứng chung và tham chiếu không định danh trong NER hay không.

### Thay đổi NER

- E2 “rất nhiều” DOSAGE [33, 42) → ∅

Nguồn: VietMed-NER train, dòng 3192 (từ 0).

## VM600-429

**Đoạn gốc:** thư vẫn ăn bởi vì chúng ta biết rằng không có một cái thực phẩm nào là tốt nhất cả mỗi thực phẩm có một giá trị riêng

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

Không có thực thể thuộc sáu loại được giữ trong bản rà soát.

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

Nguồn: VietMed-NER train, dòng 3194 (từ 0).

## VM600-430

**Đoạn gốc:** cho mình không sử dụng rượu bia cà phê và có hút thuốc lá đặc biệt ở trong cái giai đoạn này thế và như có những cái

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

Không có thực thể thuộc sáu loại được giữ trong bản rà soát.

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

Nguồn: VietMed-NER train, dòng 3202 (từ 0).

## VM600-431

**Đoạn gốc:** xét mới trả lời cho người bệnh một cách cụ thể theo từng trường hợp kính thưa tất cả quý vị bởi vì thời lượng trong

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

Không có thực thể thuộc sáu loại được giữ trong bản rà soát.

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

Nguồn: VietMed-NER train, dòng 3206 (từ 0).

## VM600-432

**Đoạn gốc:** bằng cách nào và cách thứ nhất là chúng ta bình thường trong ở nhà quý vị có thể cho thêm dầu ăn bát cơm không cho dầu

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

Không có thực thể thuộc sáu loại được giữ trong bản rà soát.

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Thay đổi NER

- E1 “thứ nhất” DOSAGE [22, 30) → ∅

Nguồn: VietMed-NER train, dòng 3214 (từ 0).

## VM600-433

**Đoạn gốc:** mỗi một cái thực phẩm có những cái ưu riêng chỉ có một cái bữa ăn đa dạng mới

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

Không có thực thể thuộc sáu loại được giữ trong bản rà soát.

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

Nguồn: VietMed-NER train, dòng 3223 (từ 0).

## VM600-434

**Đoạn gốc:** sử dụng phương pháp kích thích não sâu thì dĩ nhiên người bệnh cũng không thể nào mà ngưng thuốc hoàn toàn được thì đó

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | kích thích não sâu | Thủ thuật hoặc điều trị (PROCEDURE) | [20, 38) |
| E2 | thuốc | Thuốc/dược chất (DRUG) | [91, 96) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- SCOPE_CONFIRMATION: cần xác nhận quy ước về thuốc/dược chất, can thiệp không dùng thuốc, thiết bị, tác nhân hoặc hoạt động thăm khám; không coi ánh xạ nguồn là xác nhận chuyên gia.

### Thay đổi NER

- E2 “ngưng thuốc” PROCEDURE [85, 96) → E2 “thuốc” DRUG [91, 96)

Nguồn: VietMed-NER train, dòng 3229 (từ 0).

## VM600-435

**Đoạn gốc:** cái chuyện đó và nếu mà chúng ta sử dụng các biện pháp phòng tránh để nó không bị nghẽn mạch máu não thì ít nhất là nó sẽ

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E2 | nghẽn mạch máu não | Bệnh hoặc triệu chứng (CONDITION) | [82, 100) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- CONTEXT_OR_TRANSCRIPT: câu bị cắt, tham chiếu/mục đích chưa rõ hoặc nghi lỗi phiên âm; cần xem ngữ cảnh/audio gốc, không tự sửa văn bản.

### Thay đổi NER

- E1 “phòng tránh” DRUG [55, 66) → ∅
- E2 “nghẽn mạch máu” CONDITION [82, 96) → E2 “nghẽn mạch máu não” CONDITION [82, 100)
- E3 “não” BODY_PART [97, 100) → ∅

Nguồn: VietMed-NER train, dòng 3247 (từ 0).

## VM600-436

**Đoạn gốc:** vữa xơ động mạch ở vành tất cả những cái đó là chúng ta không được bỏ rất rất

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | vữa xơ động mạch | Bệnh hoặc triệu chứng (CONDITION) | [0, 16) |
| E2 | vành | Bộ phận cơ thể (BODY_PART) | [19, 23) |

### RE

| Mã | Cặp có hướng | Kết luận đề xuất |
|---|---|---|
| R1 | E1 “vữa xơ động mạch” → E2 “vành” | Có vị trí ở (located_at) |

### Cần chốt

- CONTEXT_OR_TRANSCRIPT: câu bị cắt, tham chiếu/mục đích chưa rõ hoặc nghi lỗi phiên âm; cần xem ngữ cảnh/audio gốc, không tự sửa văn bản.

### Thay đổi NER

- ∅ → E2 “vành” BODY_PART [19, 23)

Nguồn: VietMed-NER train, dòng 3249 (từ 0).

## VM600-437

**Đoạn gốc:** lượng đã mất mất do chính cái khối u tạo ra chứ chưa nói đến những cái mất do kém ăn hoặc là do

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | khối u | Bệnh hoặc triệu chứng (CONDITION) | [30, 36) |
| E2 | kém ăn | Bệnh hoặc triệu chứng (CONDITION) | [78, 84) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

Nguồn: VietMed-NER train, dòng 3252 (từ 0).

## VM600-438

**Đoạn gốc:** lòng một việc mà bạn sẽ không thể quen được dù đã thực hiện bao nhiêu lần tuy

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

Không có thực thể thuộc sáu loại được giữ trong bản rà soát.

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

Nguồn: VietMed-NER train, dòng 3271 (từ 0).

## VM600-439

**Đoạn gốc:** nói là có sự là giảm phí vận chuyển túi sắc tố đi từ bên dưới da lên bề mặt da

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | túi sắc tố | Bộ phận cơ thể (BODY_PART) | [36, 46) |
| E2 | da | Bộ phận cơ thể (BODY_PART) | [62, 64) |
| E3 | bề mặt da | Bộ phận cơ thể (BODY_PART) | [69, 78) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

Nguồn: VietMed-NER train, dòng 3273 (từ 0).

## VM600-440

**Đoạn gốc:** đề như là tương tác giữa những sản phẩm với nhau hoặc là gây ra các tình trạng

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

Không có thực thể thuộc sáu loại được giữ trong bản rà soát.

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

Nguồn: VietMed-NER train, dòng 3274 (từ 0).

## VM600-441

**Đoạn gốc:** hạ thảo chính là bộ ba là adenosine cordycepin và polysaccharide adenosine nó là

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E2 | adenosine | Thuốc/dược chất (DRUG) | [26, 35) |
| E4 | cordycepin | Thuốc/dược chất (DRUG) | [36, 46) |
| E3 | polysaccharide | Thuốc/dược chất (DRUG) | [50, 64) |
| E5 | adenosine | Thuốc/dược chất (DRUG) | [65, 74) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- CONTEXT_OR_TRANSCRIPT: câu bị cắt, tham chiếu/mục đích chưa rõ hoặc nghi lỗi phiên âm; cần xem ngữ cảnh/audio gốc, không tự sửa văn bản.
- ONTOLOGY_SCOPE: cần chốt phạm vi thuốc/dược chất so với mỹ phẩm, thực phẩm, hóa chất nội sinh hoặc hệ vi sinh; giữ ánh xạ nguồn khi chưa có quy ước đủ rõ.

### Thay đổi NER

- E1 “hạ thảo” DRUG [0, 7) → ∅
- E2 “adenosine cordycepin” DRUG [26, 46) → E2 “adenosine” DRUG [26, 35)
- E3 “polysaccharide adenosine” DRUG [50, 74) → E3 “polysaccharide” DRUG [50, 64)
- ∅ → E4 “cordycepin” DRUG [36, 46)
- ∅ → E5 “adenosine” DRUG [65, 74)

Nguồn: VietMed-NER train, dòng 3280 (từ 0).

## VM600-442

**Đoạn gốc:** ta dinh dưỡng một cách hợp lý và trong dinh dưỡng đó người ta chú ý đến các vitamin cần thiết vitamin nhóm b vitamin

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | vitamin | Thuốc/dược chất (DRUG) | [76, 83) |
| E2 | vitamin nhóm b | Thuốc/dược chất (DRUG) | [94, 108) |
| E4 | vitamin | Thuốc/dược chất (DRUG) | [109, 116) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- ONTOLOGY_SCOPE: cần chốt phạm vi thuốc/dược chất so với mỹ phẩm, thực phẩm, hóa chất nội sinh hoặc hệ vi sinh; giữ ánh xạ nguồn khi chưa có quy ước đủ rõ.

### Thay đổi NER

- E2 “vitamin” DRUG [94, 101) → E2 “vitamin nhóm b” DRUG [94, 108)
- E3 “b” DRUG [107, 108) → ∅

Nguồn: VietMed-NER train, dòng 3293 (từ 0).

## VM600-443

**Đoạn gốc:** chúng tôi có thể làm cái chụp các mạch máu não trên ct trên mri hoặc là

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | chụp các mạch máu não | Xét nghiệm hoặc thăm khám (TEST) | [25, 46) |
| E2 | ct | Xét nghiệm hoặc thăm khám (TEST) | [52, 54) |
| E3 | mri | Xét nghiệm hoặc thăm khám (TEST) | [60, 63) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

Nguồn: VietMed-NER train, dòng 3294 (từ 0).

## VM600-444

**Đoạn gốc:** chúng ta phải tuân trị chứ không có được gọi là bỏ trị khi chúng ta phải tuân trị

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

Không có thực thể thuộc sáu loại được giữ trong bản rà soát.

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Thay đổi NER

- E1 “tuân trị” PROCEDURE [14, 22) → ∅
- E2 “tuân trị” PROCEDURE [73, 81) → ∅

Nguồn: VietMed-NER train, dòng 3325 (từ 0).

## VM600-445

**Đoạn gốc:** rất yêu đời đúng như đức phật gọi là phải luôn luôn hoan hỷ cái đó quan trọng lắm cái thứ hai là vấn đề ăn uống là tùy

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

Không có thực thể thuộc sáu loại được giữ trong bản rà soát.

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Thay đổi NER

- E1 “cái thứ hai” DOSAGE [82, 93) → ∅

Nguồn: VietMed-NER train, dòng 3329 (từ 0).

## VM600-446

**Đoạn gốc:** găng hay không thì bây giờ người dân khi đến lấy mẫu cũng có thể nói mà cũng có thể hỏi bác sĩ rằng là hoặc là nhân viên

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | lấy mẫu | Xét nghiệm hoặc thăm khám (TEST) | [45, 52) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- SCOPE_CONFIRMATION: cần xác nhận quy ước về thuốc/dược chất, can thiệp không dùng thuốc, thiết bị, tác nhân hoặc hoạt động thăm khám; không coi ánh xạ nguồn là xác nhận chuyên gia.

### Thay đổi NER

- E1 “lấy mẫu” PROCEDURE [45, 52) → E1 “lấy mẫu” TEST [45, 52)

Nguồn: VietMed-NER train, dòng 3336 (từ 0).

## VM600-447

**Đoạn gốc:** thế này thứ hai nữa là chị cũng cái dấu hiệu tê bì chân tay này đây nó cũng có

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | tê bì chân tay | Bệnh hoặc triệu chứng (CONDITION) | [45, 59) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Thay đổi NER

- E1 “tê bì” CONDITION [45, 50) → E1 “tê bì chân tay” CONDITION [45, 59)
- E2 “chân tay” BODY_PART [51, 59) → ∅

Nguồn: VietMed-NER train, dòng 3344 (từ 0).

## VM600-448

**Đoạn gốc:** là dễ gặp ở cái độ tuổi này và cái việc thông thường là gì ạ người ta sẽ được chẩn đoán rất là muộn vì sao có những

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | chẩn đoán | Xét nghiệm hoặc thăm khám (TEST) | [78, 87) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- CONTEXT_OR_TRANSCRIPT: câu bị cắt, tham chiếu/mục đích chưa rõ hoặc nghi lỗi phiên âm; cần xem ngữ cảnh/audio gốc, không tự sửa văn bản.
- GENERIC_INTERVENTION: cần chốt việc giữ hành động điều trị/chẩn đoán chung khi không nêu phương pháp cụ thể.

Nguồn: VietMed-NER train, dòng 3350 (từ 0).

## VM600-449

**Đoạn gốc:** nếu nó đã có những cái biểu hiện như vậy một lần hai lần nếu mình không phát hiện ra có nghĩa là những lần tiếp theo nó sẽ

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

Không có thực thể thuộc sáu loại được giữ trong bản rà soát.

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Thay đổi NER

- E1 “hai lần” DOSAGE [49, 56) → ∅

Nguồn: VietMed-NER train, dòng 3360 (từ 0).

## VM600-450

**Đoạn gốc:** cùng là nói những cái biến chứng của nó kính thưa quý vị tim của chúng ta đó thì được chia làm hai phần chính đó là

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | biến chứng | Bệnh hoặc triệu chứng (CONDITION) | [22, 32) |
| E2 | tim | Bộ phận cơ thể (BODY_PART) | [57, 60) |

### RE

| Mã | Cặp có hướng | Kết luận đề xuất |
|---|---|---|
| R1 | E1 “biến chứng” → E2 “tim” | Chưa rõ — cần chốt (CHUA_RO) |

### Cần chốt

- CONTEXT_OR_TRANSCRIPT: câu bị cắt, tham chiếu/mục đích chưa rõ hoặc nghi lỗi phiên âm; cần xem ngữ cảnh/audio gốc, không tự sửa văn bản.
- GENERIC_MENTION: cần chốt có giữ bệnh/triệu chứng/biến chứng chung và tham chiếu không định danh trong NER hay không.
- UNRESOLVED_RE: còn cặp CHUA_RO; tuyệt đối không đổi thành NO_RELATION khi xuất huấn luyện.

Nguồn: VietMed-NER train, dòng 3365 (từ 0).

## VM600-451

**Đoạn gốc:** ông không thể có được kinh nghiệm làm việc thực tế trong phòng thí nghiệm và phải dành thời gian suy nghĩ và đọc

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

Không có thực thể thuộc sáu loại được giữ trong bản rà soát.

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

Nguồn: VietMed-NER train, dòng 3374 (từ 0).

## VM600-452

**Đoạn gốc:** người ta sẽ kê những cái đơn thuốc mà nó cải thiện cái tình trạng này tôi nói ví dụ như là hiện nay chúng ta hay dùng

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | thuốc | Thuốc/dược chất (DRUG) | [29, 34) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Thay đổi NER

- E2 “cải thiện” PROCEDURE [41, 50) → ∅

Nguồn: VietMed-NER train, dòng 3377 (từ 0).

## VM600-453

**Đoạn gốc:** công việc có cái gì căng thẳng quá cũng là yếu tố hay là mất ngủ cái mất ngủ ở cái người lớn tuổi cũng thường xảy ra

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | căng thẳng | Bệnh hoặc triệu chứng (CONDITION) | [20, 30) |
| E2 | mất ngủ | Bệnh hoặc triệu chứng (CONDITION) | [57, 64) |
| E3 | mất ngủ | Bệnh hoặc triệu chứng (CONDITION) | [69, 76) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- SYMPTOM_SCOPE: cần phân biệt cảm xúc thông thường với triệu chứng lâm sàng theo quy ước dự án.

Nguồn: VietMed-NER train, dòng 3413 (từ 0).

## VM600-454

**Đoạn gốc:** nữa chúng ta cần phải có cái chế độ điều trị tích cực hơn trong trường hợp này lời khuyên đầu tiên của chúng tôi là gì

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | điều trị | Thủ thuật hoặc điều trị (PROCEDURE) | [36, 44) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- GENERIC_INTERVENTION: cần chốt việc giữ hành động điều trị/chẩn đoán chung khi không nêu phương pháp cụ thể.

Nguồn: VietMed-NER train, dòng 3416 (từ 0).

## VM600-455

**Đoạn gốc:** thở đau tức ngực tim đập nhanh là do mảng xơ vữa động mạch gây hẹp tắc lòng

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | đau tức ngực | Bệnh hoặc triệu chứng (CONDITION) | [4, 16) |
| E2 | tim đập nhanh | Bệnh hoặc triệu chứng (CONDITION) | [17, 30) |
| E3 | mảng xơ vữa động mạch | Bệnh hoặc triệu chứng (CONDITION) | [37, 58) |
| E4 | hẹp tắc | Bệnh hoặc triệu chứng (CONDITION) | [63, 70) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- CONTEXT_OR_TRANSCRIPT: câu bị cắt, tham chiếu/mục đích chưa rõ hoặc nghi lỗi phiên âm; cần xem ngữ cảnh/audio gốc, không tự sửa văn bản.

### Thay đổi NER

- ∅ → E4 “hẹp tắc” CONDITION [63, 70)

Nguồn: VietMed-NER train, dòng 3426 (từ 0).

## VM600-456

**Đoạn gốc:** động trực tiếp ở giai đoạn đó nhưng còn cái nguyên nhân có khi có rất nhiều nguyên nhân dẫn đến rụng tóc mà đôi khi

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E2 | rụng tóc | Bệnh hoặc triệu chứng (CONDITION) | [96, 104) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Thay đổi NER

- E1 “rất nhiều” DOSAGE [66, 75) → ∅

Nguồn: VietMed-NER train, dòng 3433 (từ 0).

## VM600-457

**Đoạn gốc:** loại thảo dược có rất nhiều những công dụng tuyệt vời trong việc là chúng ta tăng cường sức đề kháng sức khỏe dùng

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | thảo dược | Thuốc/dược chất (DRUG) | [5, 14) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- ONTOLOGY_SCOPE: cần chốt phạm vi thuốc/dược chất so với mỹ phẩm, thực phẩm, hóa chất nội sinh hoặc hệ vi sinh; giữ ánh xạ nguồn khi chưa có quy ước đủ rõ.

### Thay đổi NER

- E2 “rất nhiều” DOSAGE [18, 27) → ∅
- E3 “sức đề kháng” TEST [88, 100) → ∅

Nguồn: VietMed-NER train, dòng 3440 (từ 0).

## VM600-458

**Đoạn gốc:** ta có thể là cải thiện cái vấn đề tăng sắc tố chúng ta có thể can thiệp vào một trong những cái giai đoạn của quá

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E2 | tăng sắc tố | Bệnh hoặc triệu chứng (CONDITION) | [34, 45) |
| E3 | can thiệp | Thủ thuật hoặc điều trị (PROCEDURE) | [62, 71) |

### RE

| Mã | Cặp có hướng | Kết luận đề xuất |
|---|---|---|
| R1 | E2 “tăng sắc tố” → E3 “can thiệp” | Chưa rõ — cần chốt (CHUA_RO) |

### Cần chốt

- CONTEXT_OR_TRANSCRIPT: câu bị cắt, tham chiếu/mục đích chưa rõ hoặc nghi lỗi phiên âm; cần xem ngữ cảnh/audio gốc, không tự sửa văn bản.
- GENERIC_INTERVENTION: cần chốt việc giữ hành động điều trị/chẩn đoán chung khi không nêu phương pháp cụ thể.
- UNRESOLVED_RE: còn cặp CHUA_RO; tuyệt đối không đổi thành NO_RELATION khi xuất huấn luyện.

### Thay đổi NER

- E1 “cải thiện” PROCEDURE [13, 22) → ∅
- E3 “can thiệp” DRUG [62, 71) → E3 “can thiệp” PROCEDURE [62, 71)

Nguồn: VietMed-NER train, dòng 3446 (từ 0).

## VM600-459

**Đoạn gốc:** còn nặng hơn rất là nhiều và bản thân tai biến mạch máu não lần một lần hai nó có thể nhẹ nhưng những lần sau nó sẽ

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | tai biến mạch máu não | Bệnh hoặc triệu chứng (CONDITION) | [38, 59) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

Nguồn: VietMed-NER train, dòng 3447 (từ 0).

## VM600-460

**Đoạn gốc:** chỉ nói đến chuyện rung nhĩ không thôi nhưng mà nếu mà cả chuyện rung nhĩ đó mà đã có những cái biến chứng ví dụ như nó

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | rung nhĩ | Bệnh hoặc triệu chứng (CONDITION) | [19, 27) |
| E2 | rung nhĩ | Bệnh hoặc triệu chứng (CONDITION) | [65, 73) |
| E3 | biến chứng | Bệnh hoặc triệu chứng (CONDITION) | [96, 106) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- GENERIC_MENTION: cần chốt có giữ bệnh/triệu chứng/biến chứng chung và tham chiếu không định danh trong NER hay không.

Nguồn: VietMed-NER train, dòng 3449 (từ 0).

## VM600-461

**Đoạn gốc:** xơ vữa động mạch cũng như là khắc phục được tình trạng ở hệ hô hấp cũng như là hệ tim thì quý vị và các bạn hãy gọi về

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | xơ vữa động mạch | Bệnh hoặc triệu chứng (CONDITION) | [0, 16) |
| E3 | hệ hô hấp | Bộ phận cơ thể (BODY_PART) | [57, 66) |
| E2 | hệ tim | Bộ phận cơ thể (BODY_PART) | [79, 85) |

### RE

| Mã | Cặp có hướng | Kết luận đề xuất |
|---|---|---|
| R1 | E1 “xơ vữa động mạch” → E3 “hệ hô hấp” | Không có quan hệ thuộc 5 loại (NO_RELATION) |
| R2 | E1 “xơ vữa động mạch” → E2 “hệ tim” | Không có quan hệ thuộc 5 loại (NO_RELATION) |

### Thay đổi NER

- E2 “tim” BODY_PART [82, 85) → E2 “hệ tim” BODY_PART [79, 85)
- ∅ → E3 “hệ hô hấp” BODY_PART [57, 66)

Nguồn: VietMed-NER train, dòng 3465 (từ 0).

## VM600-462

**Đoạn gốc:** mạch hay không còn nếu trong giai đoạn cấp này mà có rung nhĩ nữa mà người lớn tuổi nữa thì chắc chắn là chúng ta phải

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | mạch | Bộ phận cơ thể (BODY_PART) | [0, 4) |
| E2 | rung nhĩ | Bệnh hoặc triệu chứng (CONDITION) | [53, 61) |

### RE

| Mã | Cặp có hướng | Kết luận đề xuất |
|---|---|---|
| R1 | E2 “rung nhĩ” → E1 “mạch” | Không có quan hệ thuộc 5 loại (NO_RELATION) |

### Cần chốt

- CONTEXT_OR_TRANSCRIPT: câu bị cắt, tham chiếu/mục đích chưa rõ hoặc nghi lỗi phiên âm; cần xem ngữ cảnh/audio gốc, không tự sửa văn bản.

Nguồn: VietMed-NER train, dòng 3467 (từ 0).

## VM600-463

**Đoạn gốc:** cái trường hợp là năm năm bảy năm đây là những cái nghiên cứu ở nước ngoài là những cái nước phát triển là người ta cũng nhận thấy rằng là phần lớn là mọi người được

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

Không có thực thể thuộc sáu loại được giữ trong bản rà soát.

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Thay đổi NER

- E1 “nghiên cứu” TEST [51, 61) → ∅
- E2 “phần lớn” DOSAGE [139, 147) → ∅

Nguồn: VietMed-NER train, dòng 3474 (từ 0).

## VM600-464

**Đoạn gốc:** không có nắm được như thế này là bao nhiêu lâu nay rồi ạ nó có tê bì nhiều ở cái bàn tay không ạ

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | tê bì | Bệnh hoặc triệu chứng (CONDITION) | [63, 68) |
| E2 | bàn tay | Bộ phận cơ thể (BODY_PART) | [81, 88) |

### RE

| Mã | Cặp có hướng | Kết luận đề xuất |
|---|---|---|
| R1 | E1 “tê bì” → E2 “bàn tay” | Chưa rõ — cần chốt (CHUA_RO) |

### Cần chốt

- CONTEXT_OR_TRANSCRIPT: câu bị cắt, tham chiếu/mục đích chưa rõ hoặc nghi lỗi phiên âm; cần xem ngữ cảnh/audio gốc, không tự sửa văn bản.
- UNRESOLVED_RE: còn cặp CHUA_RO; tuyệt đối không đổi thành NO_RELATION khi xuất huấn luyện.

Nguồn: VietMed-NER train, dòng 3478 (từ 0).

## VM600-465

**Đoạn gốc:** hơn về dinh dưỡng trước trong và sau ung thư để làm sao giúp cho chúng ta những người đã mắc ung thư mà lại được chẩn

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | ung thư | Bệnh hoặc triệu chứng (CONDITION) | [37, 44) |
| E2 | ung thư | Bệnh hoặc triệu chứng (CONDITION) | [93, 100) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

Nguồn: VietMed-NER train, dòng 3515 (từ 0).

## VM600-466

**Đoạn gốc:** sử dụng mấy nhôm các chất bổ trợ có thể được thiết kế riêng để kích hoạt phản ứng bẩm sinh bằng cách sử dụng các phân

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | chất bổ trợ | Thuốc/dược chất (DRUG) | [21, 32) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- ONTOLOGY_SCOPE: cần chốt phạm vi thuốc/dược chất so với mỹ phẩm, thực phẩm, hóa chất nội sinh hoặc hệ vi sinh; giữ ánh xạ nguồn khi chưa có quy ước đủ rõ.

### Thay đổi NER

- E2 “bẩm sinh” CONDITION [82, 90) → ∅

Nguồn: VietMed-NER train, dòng 3522 (từ 0).

## VM600-467

**Đoạn gốc:** nhìn đơn giản về những gì đang xảy ra ở đây là cơ thể chúng ta tấn công mầm bệnh đối tượng xâm nhập vết thương vì hệ miễn

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | cơ thể | Bộ phận cơ thể (BODY_PART) | [47, 53) |
| E3 | vết thương | Bệnh hoặc triệu chứng (CONDITION) | [100, 110) |

### RE

| Mã | Cặp có hướng | Kết luận đề xuất |
|---|---|---|
| R1 | E3 “vết thương” → E1 “cơ thể” | Không có quan hệ thuộc 5 loại (NO_RELATION) |

### Thay đổi NER

- E2 “mầm bệnh” CONDITION [72, 80) → ∅

Nguồn: VietMed-NER train, dòng 3528 (từ 0).

## VM600-468

**Đoạn gốc:** não bộ hơn hết bạn có thể gặt hái được thành quả của chế độ ăn bổ não trong vòng vài tuần

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | não bộ | Bộ phận cơ thể (BODY_PART) | [0, 6) |
| E2 | não | Bộ phận cơ thể (BODY_PART) | [66, 69) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

Nguồn: VietMed-NER train, dòng 3552 (từ 0).

## VM600-469

**Đoạn gốc:** biết là nhất là trong cái buổi những cái cái lúc mà dịch dã như thế này kinh tế chúng ta ai cũng rất hạn hẹp thế thì làm

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

Không có thực thể thuộc sáu loại được giữ trong bản rà soát.

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

Nguồn: VietMed-NER train, dòng 3572 (từ 0).

## VM600-470

**Đoạn gốc:** khác máu lạnh khác thì vẫn có thể khác

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

Không có thực thể thuộc sáu loại được giữ trong bản rà soát.

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- CONTEXT_OR_TRANSCRIPT: câu bị cắt, tham chiếu/mục đích chưa rõ hoặc nghi lỗi phiên âm; cần xem ngữ cảnh/audio gốc, không tự sửa văn bản.

### Thay đổi NER

- E1 “máu” BODY_PART [5, 8) → ∅

Nguồn: VietMed-NER train, dòng 3576 (từ 0).

## VM600-471

**Đoạn gốc:** là bác bị đau lưng cũng đã lâu rồi và đau cả hai đầu gối nữa đúng không ạ vâng dạ vâng vậy thì với những cái triệu

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | đau lưng | Bệnh hoặc triệu chứng (CONDITION) | [10, 18) |
| E2 | đau cả hai đầu gối | Bệnh hoặc triệu chứng (CONDITION) | [38, 56) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Thay đổi NER

- E2 “đau” CONDITION [38, 41) → E2 “đau cả hai đầu gối” CONDITION [38, 56)
- E3 “đầu gối” BODY_PART [49, 56) → ∅

Nguồn: VietMed-NER train, dòng 3578 (từ 0).

## VM600-472

**Đoạn gốc:** phần trăm và khi cái người được tiêm vắcxin đó được miễn nhiễm thì cái người tiêm đó sẽ không có phải nhiễm virus hoặc

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E2 | tiêm | Thủ thuật hoặc điều trị (PROCEDURE) | [32, 36) |
| E3 | vắcxin | Thuốc/dược chất (DRUG) | [37, 43) |
| E4 | tiêm | Thủ thuật hoặc điều trị (PROCEDURE) | [77, 81) |
| E6 | nhiễm virus | Bệnh hoặc triệu chứng (CONDITION) | [102, 113) |

### RE

| Mã | Cặp có hướng | Kết luận đề xuất |
|---|---|---|
| R1 | E6 “nhiễm virus” → E2 “tiêm” | Không có quan hệ thuộc 5 loại (NO_RELATION) |
| R2 | E6 “nhiễm virus” → E3 “vắcxin” | Không có quan hệ thuộc 5 loại (NO_RELATION) |
| R3 | E6 “nhiễm virus” → E4 “tiêm” | Không có quan hệ thuộc 5 loại (NO_RELATION) |

### Cần chốt

- SCOPE_CONFIRMATION: cần xác nhận quy ước về thuốc/dược chất, can thiệp không dùng thuốc, thiết bị, tác nhân hoặc hoạt động thăm khám; không coi ánh xạ nguồn là xác nhận chuyên gia.

### Thay đổi NER

- E1 “phần trăm” DOSAGE [0, 9) → ∅
- E5 “virus” CONDITION [108, 113) → ∅
- ∅ → E6 “nhiễm virus” CONDITION [102, 113)

Nguồn: VietMed-NER train, dòng 3579 (từ 0).

## VM600-473

**Đoạn gốc:** thu được các quần thể vi khuẩn tương tự như các quần thể vi khuẩn tìm thấy trên bề mặt da chiếm đa số là rất nhiều vi

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E3 | bề mặt da | Bộ phận cơ thể (BODY_PART) | [80, 89) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Thay đổi NER

- E1 “vi khuẩn” CONDITION [22, 30) → ∅
- E2 “vi khuẩn” CONDITION [57, 65) → ∅
- E4 “chiếm đa số” DOSAGE [90, 101) → ∅
- E5 “rất nhiều” DOSAGE [105, 114) → ∅

Nguồn: VietMed-NER train, dòng 3580 (từ 0).

## VM600-474

**Đoạn gốc:** tiện rối loạn trí nhớ sa sút gọi là sa sút trí tuệ alzheimer vân vân nó sẽ được

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | rối loạn trí nhớ | Bệnh hoặc triệu chứng (CONDITION) | [5, 21) |
| E2 | sa sút trí tuệ | Bệnh hoặc triệu chứng (CONDITION) | [36, 50) |
| E3 | alzheimer | Bệnh hoặc triệu chứng (CONDITION) | [51, 60) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

Nguồn: VietMed-NER train, dòng 3607 (từ 0).

## VM600-475

**Đoạn gốc:** chỉ là nghỉ được rõ ràng cái đấy cũng là một cái khó đúng không ạ thế chính vì vậy cho nên trong trường hợp này rõ ràng là cái đai thắt lưng lại là một cái

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | đai thắt lưng | Thủ thuật hoặc điều trị (PROCEDURE) | [127, 140) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- CONTEXT_OR_TRANSCRIPT: câu bị cắt, tham chiếu/mục đích chưa rõ hoặc nghi lỗi phiên âm; cần xem ngữ cảnh/audio gốc, không tự sửa văn bản.

### Thay đổi NER

- E1 “thắt lưng” BODY_PART [131, 140) → E1 “đai thắt lưng” PROCEDURE [127, 140)

Nguồn: VietMed-NER train, dòng 3608 (từ 0).

## VM600-476

**Đoạn gốc:** thuật thường là chỉ là liên quan tới vấn đề về phẫu thuật nhưng mà với những cái

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | phẫu thuật | Thủ thuật hoặc điều trị (PROCEDURE) | [47, 57) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

Nguồn: VietMed-NER train, dòng 3626 (từ 0).

## VM600-477

**Đoạn gốc:** là đơn đơn độc như vậy thì nó sẽ làm cho cái tình trạng mà béo phì đó nó có

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | béo phì | Bệnh hoặc triệu chứng (CONDITION) | [59, 66) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

Nguồn: VietMed-NER train, dòng 3640 (từ 0).

## VM600-478

**Đoạn gốc:** nhiều trường hợp bị chó tấn công gây

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

Không có thực thể thuộc sáu loại được giữ trong bản rà soát.

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

Nguồn: VietMed-NER train, dòng 3650 (từ 0).

## VM600-479

**Đoạn gốc:** thấy mệt mỏi có lúc họ cảm thấy khó khăn có lúc lúc họ cảm thấy là khó cưỡng nổi các cái cái thức ăn mà nó nó chào

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | mệt mỏi | Bệnh hoặc triệu chứng (CONDITION) | [5, 12) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

Nguồn: VietMed-NER train, dòng 3662 (từ 0).

## VM600-480

**Đoạn gốc:** tôi mổ rồi mà sao nó có dấu hiệu nó muốn trở nặng hơn vân vân mà chúng ta phải yên tâm rằng là sau ba đến sáu tháng sau khi đã

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | mổ | Thủ thuật hoặc điều trị (PROCEDURE) | [4, 6) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- CONTEXT_OR_TRANSCRIPT: câu bị cắt, tham chiếu/mục đích chưa rõ hoặc nghi lỗi phiên âm; cần xem ngữ cảnh/audio gốc, không tự sửa văn bản.

Nguồn: VietMed-NER train, dòng 3667 (từ 0).

## VM600-481

**Đoạn gốc:** chúng ta sau sau vụ mất trộm chẳng hạn thì chúng ta đuổi trộm đi hết rồi thì

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

Không có thực thể thuộc sáu loại được giữ trong bản rà soát.

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

Nguồn: VietMed-NER train, dòng 3677 (từ 0).

## VM600-482

**Đoạn gốc:** bệnh thì chính cũng là những cái lúc mà chúng tôi đang vận động kính là những cái những cái lúc mà chúng tôi đang thực

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

Không có thực thể thuộc sáu loại được giữ trong bản rà soát.

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

Nguồn: VietMed-NER train, dòng 3701 (từ 0).

## VM600-483

**Đoạn gốc:** những cái cái biến chứng về các cái mạch máu chi nữa và khi sử dụng đối với sản phẩm này thì chúng ta nên sử dụng để

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | biến chứng | Bệnh hoặc triệu chứng (CONDITION) | [14, 24) |
| E2 | mạch máu chi | Bộ phận cơ thể (BODY_PART) | [36, 48) |

### RE

| Mã | Cặp có hướng | Kết luận đề xuất |
|---|---|---|
| R1 | E1 “biến chứng” → E2 “mạch máu chi” | Có vị trí ở (located_at) |

### Cần chốt

- GENERIC_MENTION: cần chốt có giữ bệnh/triệu chứng/biến chứng chung và tham chiếu không định danh trong NER hay không.

Nguồn: VietMed-NER train, dòng 3703 (từ 0).

## VM600-484

**Đoạn gốc:** là yếu tay yếu chân méo miệng thăng bằng có thể về mắt nữa thì thế mà có những triệu

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | yếu tay | Bệnh hoặc triệu chứng (CONDITION) | [3, 10) |
| E2 | yếu chân | Bệnh hoặc triệu chứng (CONDITION) | [11, 19) |
| E3 | méo miệng | Bệnh hoặc triệu chứng (CONDITION) | [20, 29) |
| E4 | mắt | Bộ phận cơ thể (BODY_PART) | [51, 54) |

### RE

| Mã | Cặp có hướng | Kết luận đề xuất |
|---|---|---|
| R1 | E1 “yếu tay” → E4 “mắt” | Không có quan hệ thuộc 5 loại (NO_RELATION) |
| R2 | E2 “yếu chân” → E4 “mắt” | Không có quan hệ thuộc 5 loại (NO_RELATION) |
| R3 | E3 “méo miệng” → E4 “mắt” | Không có quan hệ thuộc 5 loại (NO_RELATION) |

Nguồn: VietMed-NER train, dòng 3714 (từ 0).

## VM600-485

**Đoạn gốc:** có những người là còn nhịn ăn một để gọi là thanh lọc cơ thể thì thì chúng ta sẽ

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | thanh lọc cơ thể | Thủ thuật hoặc điều trị (PROCEDURE) | [44, 60) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- CONTEXT_OR_TRANSCRIPT: câu bị cắt, tham chiếu/mục đích chưa rõ hoặc nghi lỗi phiên âm; cần xem ngữ cảnh/audio gốc, không tự sửa văn bản.

### Thay đổi NER

- E1 “thanh lọc” TEST [44, 53) → E1 “thanh lọc cơ thể” PROCEDURE [44, 60)
- E2 “cơ thể” BODY_PART [54, 60) → ∅

Nguồn: VietMed-NER train, dòng 3718 (từ 0).

## VM600-486

**Đoạn gốc:** sao bởi vì khi mà bác bị huyết áp cao bác bị đái tháo đường mà thậm chí có

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | huyết áp cao | Bệnh hoặc triệu chứng (CONDITION) | [25, 37) |
| E3 | đái tháo đường | Bệnh hoặc triệu chứng (CONDITION) | [45, 59) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Thay đổi NER

- E2 “cao” DOSAGE [34, 37) → ∅
- E1 “huyết áp” CONDITION [25, 33) → E1 “huyết áp cao” CONDITION [25, 37)

Nguồn: VietMed-NER train, dòng 3734 (từ 0).

## VM600-487

**Đoạn gốc:** lời đây là thế thì làm thế nào để chúng ta biết đâu là vấn đề và cái cách xử lý của chúng ta là như thế nào khi nào thì

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

Không có thực thể thuộc sáu loại được giữ trong bản rà soát.

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

Nguồn: VietMed-NER train, dòng 3736 (từ 0).

## VM600-488

**Đoạn gốc:** phải tập dần để chúng ta thích nghi và để chúng ta có thể chấp nhận được những cái món ăn như trước khi chúng ta bị ung

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

Không có thực thể thuộc sáu loại được giữ trong bản rà soát.

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- CONTEXT_OR_TRANSCRIPT: câu bị cắt, tham chiếu/mục đích chưa rõ hoặc nghi lỗi phiên âm; cần xem ngữ cảnh/audio gốc, không tự sửa văn bản.

### Thay đổi NER

- E1 “thích nghi” TEST [25, 35) → ∅

Nguồn: VietMed-NER train, dòng 3744 (từ 0).

## VM600-489

**Đoạn gốc:** nói chung cũng như hoạt động và bảo vệ não bộ nói riêng mặc dù probiotic lợi khuẩn hiện đã trở

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | não bộ | Bộ phận cơ thể (BODY_PART) | [39, 45) |
| E3 | probiotic | Thuốc/dược chất (DRUG) | [63, 72) |
| E2 | lợi khuẩn | Thuốc/dược chất (DRUG) | [73, 82) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- ONTOLOGY_SCOPE: cần chốt phạm vi thuốc/dược chất so với mỹ phẩm, thực phẩm, hóa chất nội sinh hoặc hệ vi sinh; giữ ánh xạ nguồn khi chưa có quy ước đủ rõ.

### Thay đổi NER

- ∅ → E3 “probiotic” DRUG [63, 72)

Nguồn: VietMed-NER train, dòng 3758 (từ 0).

## VM600-490

**Đoạn gốc:** cực mà thôi thứ nhất là họ sẽ càng thấy là tự ti hơn khi bị kỳ thị là nó

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E2 | tự ti | Bệnh hoặc triệu chứng (CONDITION) | [43, 48) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- SYMPTOM_SCOPE: cần phân biệt cảm xúc thông thường với triệu chứng lâm sàng theo quy ước dự án.

### Thay đổi NER

- E1 “thứ nhất” DOSAGE [12, 20) → ∅

Nguồn: VietMed-NER train, dòng 3761 (từ 0).

## VM600-491

**Đoạn gốc:** mà chúng ta bị thay đổi trong cái quá trình trước và trong điều trị ung thư thì bây giờ chúng ta sẽ phục hồi nó lại

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | điều trị | Thủ thuật hoặc điều trị (PROCEDURE) | [59, 67) |
| E2 | ung thư | Bệnh hoặc triệu chứng (CONDITION) | [68, 75) |

### RE

| Mã | Cặp có hướng | Kết luận đề xuất |
|---|---|---|
| R1 | E2 “ung thư” → E1 “điều trị” | Được điều trị bằng phương pháp (treated_by_procedure) |

### Cần chốt

- GENERIC_INTERVENTION: cần chốt việc giữ hành động điều trị/chẩn đoán chung khi không nêu phương pháp cụ thể.

### Thay đổi NER

- E3 “phục hồi” PROCEDURE [100, 108) → ∅

Nguồn: VietMed-NER train, dòng 3819 (từ 0).

## VM600-492

**Đoạn gốc:** ta điều chỉnh thuốc cho nó phù hợp và khi có chỉ định thuốc thì phải tuân thủ

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E2 | thuốc | Thuốc/dược chất (DRUG) | [14, 19) |
| E4 | thuốc | Thuốc/dược chất (DRUG) | [54, 59) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Thay đổi NER

- E1 “điều chỉnh” DRUG [3, 13) → ∅
- E3 “chỉ định” DRUG [45, 53) → ∅
- E5 “tuân thủ” DRUG [69, 77) → ∅

Nguồn: VietMed-NER train, dòng 3820 (từ 0).

## VM600-493

**Đoạn gốc:** tân dược mà đang điều trị đây là một cái điều rất là an toàn quý vị và các bạn những ai mà chúng ta đang gặp phải cái

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | tân dược | Thuốc/dược chất (DRUG) | [0, 8) |
| E2 | điều trị | Thủ thuật hoặc điều trị (PROCEDURE) | [17, 25) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- GENERIC_INTERVENTION: cần chốt việc giữ hành động điều trị/chẩn đoán chung khi không nêu phương pháp cụ thể.

Nguồn: VietMed-NER train, dòng 3826 (từ 0).

## VM600-494

**Đoạn gốc:** tuổi gần lúc gần lớn tuổi như vậy đó thì chúng ta thấy là lúc còn trẻ phải không

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

Không có thực thể thuộc sáu loại được giữ trong bản rà soát.

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

Nguồn: VietMed-NER train, dòng 3839 (từ 0).

## VM600-495

**Đoạn gốc:** chóng mặt luôn và thậm chí đã bị trẻ hóa cho nên rằng là mà hai nữa là đi cùng

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | chóng mặt | Bệnh hoặc triệu chứng (CONDITION) | [0, 9) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Thay đổi NER

- E2 “bị trẻ hóa” CONDITION [30, 40) → ∅

Nguồn: VietMed-NER train, dòng 3851 (từ 0).

## VM600-496

**Đoạn gốc:** các bác sĩ phụ trách trên nhiều lĩnh vực sức khỏe khác nhau để cùng giúp cho người dân giải quyết những vấn đề mà

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

Không có thực thể thuộc sáu loại được giữ trong bản rà soát.

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

Nguồn: VietMed-NER train, dòng 3852 (từ 0).

## VM600-497

**Đoạn gốc:** có thể nói là chương trình đã hiểu và rất là thông cảm với những cái tình cảnh

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

Không có thực thể thuộc sáu loại được giữ trong bản rà soát.

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

Nguồn: VietMed-NER train, dòng 3867 (từ 0).

## VM600-498

**Đoạn gốc:** lo lắng khi mà người dân đến lấy mẫu mà không biết là liệu nhân viên y tế có thời gian hay không hoặc là có sát khuẩn

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | lấy mẫu | Xét nghiệm hoặc thăm khám (TEST) | [29, 36) |
| E2 | sát khuẩn | Thủ thuật hoặc điều trị (PROCEDURE) | [108, 117) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- SCOPE_CONFIRMATION: cần xác nhận quy ước về thuốc/dược chất, can thiệp không dùng thuốc, thiết bị, tác nhân hoặc hoạt động thăm khám; không coi ánh xạ nguồn là xác nhận chuyên gia.

### Thay đổi NER

- E1 “lấy mẫu” PROCEDURE [29, 36) → E1 “lấy mẫu” TEST [29, 36)

Nguồn: VietMed-NER train, dòng 3870 (từ 0).

## VM600-499

**Đoạn gốc:** của họ nó càng bị bất ổn hơn và nếu ngược lại nếu mà mình được lắng nghe

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

Không có thực thể thuộc sáu loại được giữ trong bản rà soát.

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

Nguồn: VietMed-NER train, dòng 3887 (từ 0).

## VM600-500

**Đoạn gốc:** chung đó là tập thể dục vừa sức và nó chạy đều ra thì nó nó sẽ tốt hơn cho sức khỏe của mình hơn là những cái tập

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | tập thể dục | Thủ thuật hoặc điều trị (PROCEDURE) | [12, 23) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- SCOPE_CONFIRMATION: cần xác nhận quy ước về thuốc/dược chất, can thiệp không dùng thuốc, thiết bị, tác nhân hoặc hoạt động thăm khám; không coi ánh xạ nguồn là xác nhận chuyên gia.

### Thay đổi NER

- ∅ → E1 “tập thể dục” PROCEDURE [12, 23)

Nguồn: VietMed-NER train, dòng 3888 (từ 0).

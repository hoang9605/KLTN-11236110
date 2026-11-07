# Phiếu rà soát NER và RE 501 đến 600

Bản AI rà soát lần hai ngày 15/10/2026. Giữ nguyên câu nguồn và sáu loại NER, năm quan hệ RE. Chưa được chuyên gia xác nhận.

Quy tắc người dùng đã chốt: giữ cả cụm bệnh/triệu chứng trong một CONDITION. Không tách bộ phận bên trong cụm để tạo located_at. Vị trí được nêu riêng bằng giới từ hoặc mệnh đề riêng vẫn được xét.

Vị trí ký tự là khoảng [start, end), đếm từ 0 theo Unicode. Mã E ổn định khi sửa; mã R được tạo lại. Không dùng CHUA_RO làm nhãn huấn luyện hoặc nhãn âm.

## VM600-501

**Đoạn gốc:** làm giãn các cái mạch máu để tăng cường lưu thông máu đến nuôi dưỡng cơ tim qua

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | mạch máu | Bộ phận cơ thể (BODY_PART) | [17, 25) |
| E4 | cơ tim | Bộ phận cơ thể (BODY_PART) | [69, 75) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Thay đổi NER

- E2 “tăng cường lưu thông máu” PROCEDURE [29, 53) → ∅
- E3 “nuôi dưỡng” PROCEDURE [58, 68) → ∅
- E4 “cơ” BODY_PART [69, 71) → E4 “cơ tim” BODY_PART [69, 75)
- E5 “tim” BODY_PART [72, 75) → ∅

Nguồn: VietMed-NER train, dòng 3889 (từ 0).

## VM600-502

**Đoạn gốc:** được cho những cái thiết bị cấy ghép vào cơ thể họ chỉ thanh toán theo cái khung

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | cấy ghép | Thủ thuật hoặc điều trị (PROCEDURE) | [28, 36) |
| E2 | cơ thể | Bộ phận cơ thể (BODY_PART) | [41, 47) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- CONTEXT_OR_TRANSCRIPT: câu bị cắt, tham chiếu/mục đích chưa rõ hoặc nghi lỗi phiên âm; cần xem ngữ cảnh/audio gốc, không tự sửa văn bản.

Nguồn: VietMed-NER train, dòng 3891 (từ 0).

## VM600-503

**Đoạn gốc:** chi hoàn toàn có thể xảy ra trên những bệnh nhân bị xơ vữa động mạch vâng rõ ràng là cái bệnh lý về tim mạch về huyết

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E2 | xơ vữa động mạch | Bệnh hoặc triệu chứng (CONDITION) | [52, 68) |
| E5 | bệnh lý | Bệnh hoặc triệu chứng (CONDITION) | [89, 96) |
| E3 | tim mạch | Bộ phận cơ thể (BODY_PART) | [100, 108) |

### RE

| Mã | Cặp có hướng | Kết luận đề xuất |
|---|---|---|
| R1 | E2 “xơ vữa động mạch” → E3 “tim mạch” | Không có quan hệ thuộc 5 loại (NO_RELATION) |
| R2 | E5 “bệnh lý” → E3 “tim mạch” | Không có quan hệ thuộc 5 loại (NO_RELATION) |

### Cần chốt

- CONTEXT_OR_TRANSCRIPT: câu bị cắt, tham chiếu/mục đích chưa rõ hoặc nghi lỗi phiên âm; cần xem ngữ cảnh/audio gốc, không tự sửa văn bản.

### Thay đổi NER

- E1 “những bệnh nhân” DOSAGE [33, 48) → ∅
- E4 “huyết” BODY_PART [112, 117) → ∅
- ∅ → E5 “bệnh lý” CONDITION [89, 96)

Nguồn: VietMed-NER train, dòng 3895 (từ 0).

## VM600-504

**Đoạn gốc:** lành mạnh tôi sẽ giải thích mọi yếu tố này đóng vai trò như thế nào đối với sức khỏe của hệ vi sinh vật vì lợi ích của

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | hệ vi sinh vật | Bộ phận cơ thể (BODY_PART) | [89, 103) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- ONTOLOGY_SCOPE: cần chốt phạm vi thuốc/dược chất so với mỹ phẩm, thực phẩm, hóa chất nội sinh hoặc hệ vi sinh; giữ ánh xạ nguồn khi chưa có quy ước đủ rõ.

### Thay đổi NER

- E1 “hệ” BODY_PART [89, 91) → E1 “hệ vi sinh vật” BODY_PART [89, 103)
- E2 “vi sinh vật” BODY_PART [92, 103) → ∅

Nguồn: VietMed-NER train, dòng 3898 (từ 0).

## VM600-505

**Đoạn gốc:** phù hợp nếu mà vì chúng ta chăm sóc nhiều hôm sau nhưng mà đôi khi một số làn da chăm sóc nhiều quá thì thay đổi mụn nữa là thôi nếu

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | làn da | Bộ phận cơ thể (BODY_PART) | [74, 80) |
| E2 | mụn | Bệnh hoặc triệu chứng (CONDITION) | [113, 116) |

### RE

| Mã | Cặp có hướng | Kết luận đề xuất |
|---|---|---|
| R1 | E2 “mụn” → E1 “làn da” | Chưa rõ — cần chốt (CHUA_RO) |

### Cần chốt

- CONTEXT_OR_TRANSCRIPT: câu bị cắt, tham chiếu/mục đích chưa rõ hoặc nghi lỗi phiên âm; cần xem ngữ cảnh/audio gốc, không tự sửa văn bản.
- UNRESOLVED_RE: còn cặp CHUA_RO; tuyệt đối không đổi thành NO_RELATION khi xuất huấn luyện.

Nguồn: VietMed-NER train, dòng 3900 (từ 0).

## VM600-506

**Đoạn gốc:** biểu hiện của cái thoái hóa cột sống của chúng ta dường như nó không phải là quá không phải ở những giai đoạn rất là sớm

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | thoái hóa cột sống | Bệnh hoặc triệu chứng (CONDITION) | [18, 36) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

Nguồn: VietMed-NER train, dòng 3908 (từ 0).

## VM600-507

**Đoạn gốc:** các cái bệnh lý như là đau tức ngực này hồi hộp trống ngực này đấy thế và và

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | đau tức ngực | Bệnh hoặc triệu chứng (CONDITION) | [23, 35) |
| E2 | hồi hộp trống ngực | Bệnh hoặc triệu chứng (CONDITION) | [40, 58) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

Nguồn: VietMed-NER train, dòng 3927 (từ 0).

## VM600-508

**Đoạn gốc:** đông trùng hạ thảo làm chủ dược nhưng mà kết hợp thêm nấm hầu thủ với đẳng sâm việt nam ở đây cũng là phải nói thêm một

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | đông trùng hạ thảo | Thuốc/dược chất (DRUG) | [0, 18) |
| E2 | nấm hầu thủ | Thuốc/dược chất (DRUG) | [54, 65) |
| E3 | đẳng sâm việt nam | Thuốc/dược chất (DRUG) | [70, 87) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- ONTOLOGY_SCOPE: cần chốt phạm vi thuốc/dược chất so với mỹ phẩm, thực phẩm, hóa chất nội sinh hoặc hệ vi sinh; giữ ánh xạ nguồn khi chưa có quy ước đủ rõ.

### Thay đổi NER

- E3 “đẳng sâm” DRUG [70, 78) → E3 “đẳng sâm việt nam” DRUG [70, 87)

Nguồn: VietMed-NER train, dòng 3928 (từ 0).

## VM600-509

**Đoạn gốc:** tim thì có thể sẽ xảy ra bệnh cạnh thiếu máu cơ tim nhồi máu cơ tim có nghĩa là

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | tim | Bộ phận cơ thể (BODY_PART) | [0, 3) |
| E2 | thiếu máu cơ tim | Bệnh hoặc triệu chứng (CONDITION) | [35, 51) |
| E5 | nhồi máu cơ tim | Bệnh hoặc triệu chứng (CONDITION) | [52, 67) |

### RE

| Mã | Cặp có hướng | Kết luận đề xuất |
|---|---|---|
| R1 | E2 “thiếu máu cơ tim” → E1 “tim” | Chưa rõ — cần chốt (CHUA_RO) |
| R2 | E5 “nhồi máu cơ tim” → E1 “tim” | Chưa rõ — cần chốt (CHUA_RO) |

### Cần chốt

- CONTEXT_OR_TRANSCRIPT: câu bị cắt, tham chiếu/mục đích chưa rõ hoặc nghi lỗi phiên âm; cần xem ngữ cảnh/audio gốc, không tự sửa văn bản.
- UNRESOLVED_RE: còn cặp CHUA_RO; tuyệt đối không đổi thành NO_RELATION khi xuất huấn luyện.

### Thay đổi NER

- E3 “cơ” BODY_PART [45, 47) → E3 “cơ tim” BODY_PART [45, 51)
- E4 “tim” BODY_PART [48, 51) → ∅
- E2 “thiếu máu” CONDITION [35, 44) → E2 “thiếu máu cơ tim” CONDITION [35, 51)
- E3 “cơ tim” BODY_PART [45, 51) → ∅

Nguồn: VietMed-NER train, dòng 3935 (từ 0).

## VM600-510

**Đoạn gốc:** động cảm ơn bác sĩ và thưa tất cả quý vị rõ ràng là chúng ta thấy có rất là nhiều

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

Không có thực thể thuộc sáu loại được giữ trong bản rà soát.

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

Nguồn: VietMed-NER train, dòng 3945 (từ 0).

## VM600-511

**Đoạn gốc:** sử dụng cái axit lactic để chúng ta phải lên chất đoạn mũi má và chúng ta coi đáp

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | axit lactic | Thuốc/dược chất (DRUG) | [12, 23) |
| E2 | mũi | Bộ phận cơ thể (BODY_PART) | [55, 58) |
| E3 | má | Bộ phận cơ thể (BODY_PART) | [59, 61) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- CONTEXT_OR_TRANSCRIPT: câu bị cắt, tham chiếu/mục đích chưa rõ hoặc nghi lỗi phiên âm; cần xem ngữ cảnh/audio gốc, không tự sửa văn bản.

### Thay đổi NER

- ∅ → E3 “má” BODY_PART [59, 61)

Nguồn: VietMed-NER train, dòng 3950 (từ 0).

## VM600-512

**Đoạn gốc:** thì làm sao mục đích thứ nhất là giúp cho người bệnh tăng đề kháng mục đích thứ hai là giúp cho người bệnh làm sao

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

Không có thực thể thuộc sáu loại được giữ trong bản rà soát.

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Thay đổi NER

- E1 “thứ nhất” DOSAGE [21, 29) → ∅

Nguồn: VietMed-NER train, dòng 3953 (từ 0).

## VM600-513

**Đoạn gốc:** cái béo phì vân vân nhiều nhiều những cái cái cái bệnh có thể đưa đến cái béo

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | béo phì | Bệnh hoặc triệu chứng (CONDITION) | [4, 11) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- CONTEXT_OR_TRANSCRIPT: câu bị cắt, tham chiếu/mục đích chưa rõ hoặc nghi lỗi phiên âm; cần xem ngữ cảnh/audio gốc, không tự sửa văn bản.

Nguồn: VietMed-NER train, dòng 3954 (từ 0).

## VM600-514

**Đoạn gốc:** thiện những dấu hiệu tê bì kiến bò ở chân tay của bác này thế rồi là những cái dấu hiệu hồi hộp trống ngực của bác

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | tê bì kiến bò | Bệnh hoặc triệu chứng (CONDITION) | [21, 34) |
| E2 | chân tay | Bộ phận cơ thể (BODY_PART) | [37, 45) |
| E3 | hồi hộp trống ngực | Bệnh hoặc triệu chứng (CONDITION) | [88, 106) |

### RE

| Mã | Cặp có hướng | Kết luận đề xuất |
|---|---|---|
| R1 | E1 “tê bì kiến bò” → E2 “chân tay” | Có vị trí ở (located_at) |
| R2 | E3 “hồi hộp trống ngực” → E2 “chân tay” | Không có quan hệ thuộc 5 loại (NO_RELATION) |

Nguồn: VietMed-NER train, dòng 3971 (từ 0).

## VM600-515

**Đoạn gốc:** sau đó thì cũng không nhắc bởi vì nó

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

Không có thực thể thuộc sáu loại được giữ trong bản rà soát.

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

Nguồn: VietMed-NER train, dòng 3978 (từ 0).

## VM600-516

**Đoạn gốc:** về các cơ chế này và cách chúng bị ảnh hưởng bởi vi khuẩn đường ruột và sức khỏe đường ruột của bạn trên thực tế hệ

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E2 | đường ruột | Bộ phận cơ thể (BODY_PART) | [58, 68) |
| E3 | đường ruột | Bộ phận cơ thể (BODY_PART) | [81, 91) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Thay đổi NER

- E1 “vi khuẩn” CONDITION [49, 57) → ∅

Nguồn: VietMed-NER train, dòng 3982 (từ 0).

## VM600-517

**Đoạn gốc:** rất nhiều các cái trường hợp mà cái thận của chức năng thận nó bị ảnh hưởng nhiều và nhiều bệnh nhân bị suy thận do

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E2 | thận | Bộ phận cơ thể (BODY_PART) | [36, 40) |
| E3 | thận | Bộ phận cơ thể (BODY_PART) | [55, 59) |
| E4 | suy thận | Bệnh hoặc triệu chứng (CONDITION) | [104, 112) |

### RE

| Mã | Cặp có hướng | Kết luận đề xuất |
|---|---|---|
| R1 | E4 “suy thận” → E2 “thận” | Chưa rõ — cần chốt (CHUA_RO) |
| R2 | E4 “suy thận” → E3 “thận” | Chưa rõ — cần chốt (CHUA_RO) |

### Cần chốt

- CONTEXT_OR_TRANSCRIPT: câu bị cắt, tham chiếu/mục đích chưa rõ hoặc nghi lỗi phiên âm; cần xem ngữ cảnh/audio gốc, không tự sửa văn bản.
- UNRESOLVED_RE: còn cặp CHUA_RO; tuyệt đối không đổi thành NO_RELATION khi xuất huấn luyện.

### Thay đổi NER

- E1 “rất nhiều” DOSAGE [0, 9) → ∅

Nguồn: VietMed-NER train, dòng 3988 (từ 0).

## VM600-518

**Đoạn gốc:** nên là cái thời gian đầu thì có thể mình sẽ lựa chọn cái cục pin không sạc sau khi mà mình đặt xong mình

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

Không có thực thể thuộc sáu loại được giữ trong bản rà soát.

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- CONTEXT_OR_TRANSCRIPT: câu bị cắt, tham chiếu/mục đích chưa rõ hoặc nghi lỗi phiên âm; cần xem ngữ cảnh/audio gốc, không tự sửa văn bản.

Nguồn: VietMed-NER train, dòng 3991 (từ 0).

## VM600-519

**Đoạn gốc:** tử protein của vi khuẩn liên quan tới một quá trình thiết yếu và phức tạp một

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | protein | Thuốc/dược chất (DRUG) | [3, 10) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- ONTOLOGY_SCOPE: cần chốt phạm vi thuốc/dược chất so với mỹ phẩm, thực phẩm, hóa chất nội sinh hoặc hệ vi sinh; giữ ánh xạ nguồn khi chưa có quy ước đủ rõ.
- SCOPE_CONFIRMATION: cần xác nhận quy ước về thuốc/dược chất, can thiệp không dùng thuốc, thiết bị, tác nhân hoặc hoạt động thăm khám; không coi ánh xạ nguồn là xác nhận chuyên gia.

### Thay đổi NER

- E2 “vi khuẩn” CONDITION [15, 23) → ∅

Nguồn: VietMed-NER train, dòng 3998 (từ 0).

## VM600-520

**Đoạn gốc:** biến chứng nguy hiểm thế thì của bác có vấn đề gì huyết áp này đái tháo đường này phải không ạ và cái nữa là liên quan đến

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | biến chứng | Bệnh hoặc triệu chứng (CONDITION) | [0, 10) |
| E2 | huyết áp | Bệnh hoặc triệu chứng (CONDITION) | [50, 58) |
| E3 | đái tháo đường | Bệnh hoặc triệu chứng (CONDITION) | [63, 77) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- CONTEXT_OR_TRANSCRIPT: câu bị cắt, tham chiếu/mục đích chưa rõ hoặc nghi lỗi phiên âm; cần xem ngữ cảnh/audio gốc, không tự sửa văn bản.
- GENERIC_MENTION: cần chốt có giữ bệnh/triệu chứng/biến chứng chung và tham chiếu không định danh trong NER hay không.
- PHYSIOLOGY_VS_DISEASE: từ huyết áp/mỡ máu đứng riêng chưa xác định bệnh; giữ đề xuất nguồn chờ chốt.

Nguồn: VietMed-NER train, dòng 4015 (từ 0).

## VM600-521

**Đoạn gốc:** dụ như là lở loét miệng thì thực ra mình nói lở loét miệng chỉ do kẽm không thôi thì cũng chỉ là một phần thôi

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E5 | lở loét miệng | Bệnh hoặc triệu chứng (CONDITION) | [10, 23) |
| E6 | lở loét miệng | Bệnh hoặc triệu chứng (CONDITION) | [45, 58) |
| E3 | kẽm | Thuốc/dược chất (DRUG) | [66, 69) |

### RE

| Mã | Cặp có hướng | Kết luận đề xuất |
|---|---|---|
| R1 | E5 “lở loét miệng” → E3 “kẽm” | Không có quan hệ thuộc 5 loại (NO_RELATION) |
| R2 | E6 “lở loét miệng” → E3 “kẽm” | Không có quan hệ thuộc 5 loại (NO_RELATION) |

### Cần chốt

- CONTEXT_OR_TRANSCRIPT: câu bị cắt, tham chiếu/mục đích chưa rõ hoặc nghi lỗi phiên âm; cần xem ngữ cảnh/audio gốc, không tự sửa văn bản.

### Thay đổi NER

- E4 “một phần” DOSAGE [97, 105) → ∅
- ∅ → E5 “lở loét” CONDITION [10, 17)
- ∅ → E6 “lở loét” CONDITION [45, 52)
- E5 “lở loét” CONDITION [10, 17) → E5 “lở loét miệng” CONDITION [10, 23)
- E1 “miệng” BODY_PART [18, 23) → ∅
- E6 “lở loét” CONDITION [45, 52) → E6 “lở loét miệng” CONDITION [45, 58)
- E2 “miệng” BODY_PART [53, 58) → ∅

Nguồn: VietMed-NER train, dòng 4021 (từ 0).

## VM600-522

**Đoạn gốc:** chấm mấy lận cũng như là mấy cái người về mà bác sĩ mà tiểu đường ở đây đó bác sĩ và ta nói

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | tiểu đường | Bệnh hoặc triệu chứng (CONDITION) | [55, 65) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- CONTEXT_OR_TRANSCRIPT: câu bị cắt, tham chiếu/mục đích chưa rõ hoặc nghi lỗi phiên âm; cần xem ngữ cảnh/audio gốc, không tự sửa văn bản.

Nguồn: VietMed-NER train, dòng 4022 (từ 0).

## VM600-523

**Đoạn gốc:** chủ chốt của cơ thể trong hoạt động cùng với chức năng sinh lý học của bạn đặc biệt là hệ thần kinh xếp cùng nhau các

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | cơ thể | Bộ phận cơ thể (BODY_PART) | [13, 19) |
| E2 | hệ thần kinh | Bộ phận cơ thể (BODY_PART) | [87, 99) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Thay đổi NER

- E2 “thần kinh” BODY_PART [90, 99) → E2 “hệ thần kinh” BODY_PART [87, 99)

Nguồn: VietMed-NER train, dòng 4023 (từ 0).

## VM600-524

**Đoạn gốc:** thể khác và nó lại sinh sôi nảy nở và có cái điều kiện tiếp xúc gần với những khi người khác nữa thì virus đó lại là có

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

Không có thực thể thuộc sáu loại được giữ trong bản rà soát.

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- SCOPE_CONFIRMATION: cần xác nhận quy ước về thuốc/dược chất, can thiệp không dùng thuốc, thiết bị, tác nhân hoặc hoạt động thăm khám; không coi ánh xạ nguồn là xác nhận chuyên gia.

### Thay đổi NER

- E1 “virus” CONDITION [101, 106) → ∅

Nguồn: VietMed-NER train, dòng 4044 (từ 0).

## VM600-525

**Đoạn gốc:** là cái tư thế vận động của người ta như thế nào vì sao vì tất cả những cái chuyện này là những cái yếu tố nó có tác

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

Không có thực thể thuộc sáu loại được giữ trong bản rà soát.

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

Nguồn: VietMed-NER train, dòng 4047 (từ 0).

## VM600-526

**Đoạn gốc:** trăm nghìn tỷ sinh vật vô hình này bao phủ bên trong và bên ngoài cơ thể bạn phát triển mạnh trong miệng mũi tai ruột

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E2 | cơ thể | Bộ phận cơ thể (BODY_PART) | [66, 72) |
| E3 | miệng | Bộ phận cơ thể (BODY_PART) | [99, 104) |
| E4 | mũi | Bộ phận cơ thể (BODY_PART) | [105, 108) |
| E5 | tai | Bộ phận cơ thể (BODY_PART) | [109, 112) |
| E6 | ruột | Bộ phận cơ thể (BODY_PART) | [113, 117) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Thay đổi NER

- E1 “trăm nghìn tỷ” DOSAGE [0, 13) → ∅

Nguồn: VietMed-NER train, dòng 4050 (từ 0).

## VM600-527

**Đoạn gốc:** đời có một ca sinh mổ theo nguyện vọng và được uống sữa công thức hoàn toàn cô bé mắt nhiều bệnh nhiễm trùng khi còn

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E2 | sinh mổ | Thủ thuật hoặc điều trị (PROCEDURE) | [14, 21) |
| E4 | nhiễm trùng | Bệnh hoặc triệu chứng (CONDITION) | [97, 108) |

### RE

| Mã | Cặp có hướng | Kết luận đề xuất |
|---|---|---|
| R1 | E4 “nhiễm trùng” → E2 “sinh mổ” | Không có quan hệ thuộc 5 loại (NO_RELATION) |

### Cần chốt

- CONTEXT_OR_TRANSCRIPT: câu bị cắt, tham chiếu/mục đích chưa rõ hoặc nghi lỗi phiên âm; cần xem ngữ cảnh/audio gốc, không tự sửa văn bản.

### Thay đổi NER

- E1 “một ca” DOSAGE [7, 13) → ∅
- E3 “mắt” BODY_PART [82, 85) → ∅

Nguồn: VietMed-NER train, dòng 4056 (từ 0).

## VM600-528

**Đoạn gốc:** chung nhất về cái vai trò quan trọng của dinh dưỡng đối với người bệnh ung thư được không ạ vâng ạ nếu nói về dinh

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | ung thư | Bệnh hoặc triệu chứng (CONDITION) | [71, 78) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

Nguồn: VietMed-NER train, dòng 4058 (từ 0).

## VM600-529

**Đoạn gốc:** truyền miệng thì sau đó thì sau một cái thời gian dài họ thử nghiệm mọi thứ

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

Không có thực thể thuộc sáu loại được giữ trong bản rà soát.

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Thay đổi NER

- E1 “truyền miệng” PROCEDURE [0, 12) → ∅

Nguồn: VietMed-NER train, dòng 4077 (từ 0).

## VM600-530

**Đoạn gốc:** lo âu bồn chồn và có đôi khi ảo giác và có thể có ý định tự tử thì tất

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | lo âu | Bệnh hoặc triệu chứng (CONDITION) | [0, 5) |
| E4 | bồn chồn | Bệnh hoặc triệu chứng (CONDITION) | [6, 14) |
| E2 | ảo giác | Bệnh hoặc triệu chứng (CONDITION) | [29, 36) |
| E3 | ý định tự tử | Bệnh hoặc triệu chứng (CONDITION) | [50, 62) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- SYMPTOM_SCOPE: cần phân biệt cảm xúc thông thường với triệu chứng lâm sàng theo quy ước dự án.

### Thay đổi NER

- E3 “có ý định tự tử” CONDITION [47, 62) → E3 “ý định tự tử” CONDITION [50, 62)
- ∅ → E4 “bồn chồn” CONDITION [6, 14)

Nguồn: VietMed-NER train, dòng 4081 (từ 0).

## VM600-531

**Đoạn gốc:** hiện tượng sẽ được đề cập khác cuốn sách này sẽ khám phá ảnh hưởng của việc làm việc ca đêm đến hệ miễn dịch của chúng

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E2 | hệ miễn dịch | Bộ phận cơ thể (BODY_PART) | [96, 108) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Thay đổi NER

- E1 “khám” TEST [48, 52) → ∅

Nguồn: VietMed-NER train, dòng 4089 (từ 0).

## VM600-532

**Đoạn gốc:** phẩm mà nó tác động vào cái mảng xơ vữa nên là nó cần phải có thời gian nên là bác nên sử dụng kéo dài từ ba đến sáu tháng

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | mảng xơ vữa | Bệnh hoặc triệu chứng (CONDITION) | [28, 39) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- CONTEXT_OR_TRANSCRIPT: câu bị cắt, tham chiếu/mục đích chưa rõ hoặc nghi lỗi phiên âm; cần xem ngữ cảnh/audio gốc, không tự sửa văn bản.

Nguồn: VietMed-NER train, dòng 4095 (từ 0).

## VM600-533

**Đoạn gốc:** trong tế bào của chúng ta nó có dna riêng tách biệt với dna trong nhân tế bào trên thực tế ti thể có thể được coi

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | tế bào | Bộ phận cơ thể (BODY_PART) | [6, 12) |
| E2 | dna | Bộ phận cơ thể (BODY_PART) | [32, 35) |
| E3 | dna | Bộ phận cơ thể (BODY_PART) | [56, 59) |
| E4 | nhân tế bào | Bộ phận cơ thể (BODY_PART) | [66, 77) |
| E5 | ti thể | Bộ phận cơ thể (BODY_PART) | [91, 97) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Thay đổi NER

- E4 “tế bào” BODY_PART [71, 77) → E4 “nhân tế bào” BODY_PART [66, 77)

Nguồn: VietMed-NER train, dòng 4098 (từ 0).

## VM600-534

**Đoạn gốc:** công tác điều trị parkinson cũng như là mức độ hiệu quả của phương pháp này như thế nào chúng ta biết rằng là bệnh parkinson

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | điều trị | Thủ thuật hoặc điều trị (PROCEDURE) | [9, 17) |
| E2 | parkinson | Bệnh hoặc triệu chứng (CONDITION) | [18, 27) |
| E4 | parkinson | Bệnh hoặc triệu chứng (CONDITION) | [115, 124) |

### RE

| Mã | Cặp có hướng | Kết luận đề xuất |
|---|---|---|
| R1 | E2 “parkinson” → E1 “điều trị” | Được điều trị bằng phương pháp (treated_by_procedure) |
| R2 | E4 “parkinson” → E1 “điều trị” | Chưa rõ — cần chốt (CHUA_RO) |

### Cần chốt

- CONTEXT_OR_TRANSCRIPT: câu bị cắt, tham chiếu/mục đích chưa rõ hoặc nghi lỗi phiên âm; cần xem ngữ cảnh/audio gốc, không tự sửa văn bản.
- GENERIC_INTERVENTION: cần chốt việc giữ hành động điều trị/chẩn đoán chung khi không nêu phương pháp cụ thể.
- UNRESOLVED_RE: còn cặp CHUA_RO; tuyệt đối không đổi thành NO_RELATION khi xuất huấn luyện.

### Thay đổi NER

- E3 “mức độ” DOSAGE [40, 46) → ∅

Nguồn: VietMed-NER train, dòng 4103 (từ 0).

## VM600-535

**Đoạn gốc:** ở người bị nhiễm virus có thể tạo ra một trăm phần tử virus mối điều này có nghĩa là chỉ cần ba bản

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E4 | nhiễm virus | Bệnh hoặc triệu chứng (CONDITION) | [11, 22) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- SCOPE_CONFIRMATION: cần xác nhận quy ước về thuốc/dược chất, can thiệp không dùng thuốc, thiết bị, tác nhân hoặc hoạt động thăm khám; không coi ánh xạ nguồn là xác nhận chuyên gia.

### Thay đổi NER

- E1 “virus” CONDITION [17, 22) → ∅
- E2 “một trăm phần tử” DOSAGE [37, 53) → ∅
- E3 “virus” CONDITION [54, 59) → ∅
- ∅ → E4 “nhiễm virus” CONDITION [11, 22)

Nguồn: VietMed-NER train, dòng 4106 (từ 0).

## VM600-536

**Đoạn gốc:** là lú lẫn hay quên sa sút trí tuệ aizheimer parkinson rồi là ta di

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | lú lẫn | Bệnh hoặc triệu chứng (CONDITION) | [3, 9) |
| E2 | hay quên | Bệnh hoặc triệu chứng (CONDITION) | [10, 18) |
| E3 | sa sút trí tuệ | Bệnh hoặc triệu chứng (CONDITION) | [19, 33) |
| E4 | aizheimer | Bệnh hoặc triệu chứng (CONDITION) | [34, 43) |
| E5 | parkinson | Bệnh hoặc triệu chứng (CONDITION) | [44, 53) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- CONTEXT_OR_TRANSCRIPT: câu bị cắt, tham chiếu/mục đích chưa rõ hoặc nghi lỗi phiên âm; cần xem ngữ cảnh/audio gốc, không tự sửa văn bản.

Nguồn: VietMed-NER train, dòng 4112 (từ 0).

## VM600-537

**Đoạn gốc:** người béo phì mà người ta đã từng trị liệu được mổ rồi nè được điều trị tốt nè được tập luyện tốt giữ được

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | béo phì | Bệnh hoặc triệu chứng (CONDITION) | [6, 13) |
| E2 | trị liệu | Thủ thuật hoặc điều trị (PROCEDURE) | [34, 42) |
| E3 | mổ | Thủ thuật hoặc điều trị (PROCEDURE) | [48, 50) |
| E4 | điều trị | Thủ thuật hoặc điều trị (PROCEDURE) | [63, 71) |
| E5 | tập luyện | Thủ thuật hoặc điều trị (PROCEDURE) | [84, 93) |

### RE

| Mã | Cặp có hướng | Kết luận đề xuất |
|---|---|---|
| R1 | E1 “béo phì” → E2 “trị liệu” | Được điều trị bằng phương pháp (treated_by_procedure) |
| R2 | E1 “béo phì” → E3 “mổ” | Được điều trị bằng phương pháp (treated_by_procedure) |
| R3 | E1 “béo phì” → E4 “điều trị” | Được điều trị bằng phương pháp (treated_by_procedure) |
| R4 | E1 “béo phì” → E5 “tập luyện” | Được điều trị bằng phương pháp (treated_by_procedure) |

### Cần chốt

- GENERIC_INTERVENTION: cần chốt việc giữ hành động điều trị/chẩn đoán chung khi không nêu phương pháp cụ thể.

### Thay đổi NER

- ∅ → E5 “tập luyện” PROCEDURE [84, 93)

Nguồn: VietMed-NER train, dòng 4119 (từ 0).

## VM600-538

**Đoạn gốc:** đầu tiên chúng tôi khuyên là như vậy và cái thứ hai nữa là có lẽ là bác nên có một cái đai thắt lưng để mình bảo vệ cái

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E2 | đai thắt lưng | Thủ thuật hoặc điều trị (PROCEDURE) | [87, 100) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Thay đổi NER

- E1 “cái thứ hai” DOSAGE [40, 51) → ∅
- E2 “thắt lưng” BODY_PART [91, 100) → E2 “đai thắt lưng” PROCEDURE [87, 100)

Nguồn: VietMed-NER train, dòng 4120 (từ 0).

## VM600-539

**Đoạn gốc:** bệnh lý các cái biến chứng như là các cái nhồi máu ở cơ tim nhưng thấy nhồi

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | biến chứng | Bệnh hoặc triệu chứng (CONDITION) | [16, 26) |
| E2 | nhồi máu | Bệnh hoặc triệu chứng (CONDITION) | [42, 50) |
| E3 | cơ tim | Bộ phận cơ thể (BODY_PART) | [53, 59) |

### RE

| Mã | Cặp có hướng | Kết luận đề xuất |
|---|---|---|
| R1 | E1 “biến chứng” → E3 “cơ tim” | Không có quan hệ thuộc 5 loại (NO_RELATION) |
| R2 | E2 “nhồi máu” → E3 “cơ tim” | Có vị trí ở (located_at) |

### Cần chốt

- CONTEXT_OR_TRANSCRIPT: câu bị cắt, tham chiếu/mục đích chưa rõ hoặc nghi lỗi phiên âm; cần xem ngữ cảnh/audio gốc, không tự sửa văn bản.
- GENERIC_MENTION: cần chốt có giữ bệnh/triệu chứng/biến chứng chung và tham chiếu không định danh trong NER hay không.

### Thay đổi NER

- E2 “máu” BODY_PART [47, 50) → E2 “nhồi máu” CONDITION [42, 50)
- E3 “cơ” BODY_PART [53, 55) → E3 “cơ tim” BODY_PART [53, 59)
- E4 “tim” BODY_PART [56, 59) → ∅

Nguồn: VietMed-NER train, dòng 4134 (từ 0).

## VM600-540

**Đoạn gốc:** đến và chúng ta không không nhận biết được cái điều đó cho nên chúng ta chỉ nghĩ là à thôi thì đau khớp chúng ta có

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | đau khớp | Bệnh hoặc triệu chứng (CONDITION) | [95, 103) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Thay đổi NER

- E1 “đau” CONDITION [95, 98) → E1 “đau khớp” CONDITION [95, 103)
- E2 “khớp” BODY_PART [99, 103) → ∅

Nguồn: VietMed-NER train, dòng 4136 (từ 0).

## VM600-541

**Đoạn gốc:** một số trục trặc về tóc kể cả bạc tóc thế cho nên là những hoạt chất từ thiên nhiên này tỏ ra rất là an toàn và trong

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | tóc | Bộ phận cơ thể (BODY_PART) | [20, 23) |
| E2 | bạc tóc | Bệnh hoặc triệu chứng (CONDITION) | [30, 37) |
| E3 | hoạt chất | Thuốc/dược chất (DRUG) | [59, 68) |

### RE

| Mã | Cặp có hướng | Kết luận đề xuất |
|---|---|---|
| R1 | E2 “bạc tóc” → E1 “tóc” | Chưa rõ — cần chốt (CHUA_RO) |
| R2 | E2 “bạc tóc” → E3 “hoạt chất” | Chưa rõ — cần chốt (CHUA_RO) |

### Cần chốt

- CONTEXT_OR_TRANSCRIPT: câu bị cắt, tham chiếu/mục đích chưa rõ hoặc nghi lỗi phiên âm; cần xem ngữ cảnh/audio gốc, không tự sửa văn bản.
- UNRESOLVED_RE: còn cặp CHUA_RO; tuyệt đối không đổi thành NO_RELATION khi xuất huấn luyện.

Nguồn: VietMed-NER train, dòng 4143 (từ 0).

## VM600-542

**Đoạn gốc:** thuốc xong rồi một thời gian thì tôi đi đo tôi đi

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | thuốc | Thuốc/dược chất (DRUG) | [0, 5) |
| E2 | đo | Xét nghiệm hoặc thăm khám (TEST) | [40, 42) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- CONTEXT_OR_TRANSCRIPT: câu bị cắt, tham chiếu/mục đích chưa rõ hoặc nghi lỗi phiên âm; cần xem ngữ cảnh/audio gốc, không tự sửa văn bản.
- GENERIC_INTERVENTION: cần chốt việc giữ hành động điều trị/chẩn đoán chung khi không nêu phương pháp cụ thể.

### Thay đổi NER

- ∅ → E2 “đo” TEST [40, 42)

Nguồn: VietMed-NER train, dòng 4168 (từ 0).

## VM600-543

**Đoạn gốc:** thì cái vấn đề của anh gặp phải nó đang có những cái triệu chứng như thế nào cũng như là nó diễn biến như thế nào trong cái thời gian vừa rồi thì anh có

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | triệu chứng | Bệnh hoặc triệu chứng (CONDITION) | [53, 64) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- GENERIC_MENTION: cần chốt có giữ bệnh/triệu chứng/biến chứng chung và tham chiếu không định danh trong NER hay không.

Nguồn: VietMed-NER train, dòng 4169 (từ 0).

## VM600-544

**Đoạn gốc:** đối với sau điều trị ung thư là cần thiết để chúng ta phát hiện sớm những cái dấu hiệu rất có thể chúng ta có ung

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | điều trị | Thủ thuật hoặc điều trị (PROCEDURE) | [12, 20) |
| E2 | ung thư | Bệnh hoặc triệu chứng (CONDITION) | [21, 28) |

### RE

| Mã | Cặp có hướng | Kết luận đề xuất |
|---|---|---|
| R1 | E2 “ung thư” → E1 “điều trị” | Được điều trị bằng phương pháp (treated_by_procedure) |

### Cần chốt

- GENERIC_INTERVENTION: cần chốt việc giữ hành động điều trị/chẩn đoán chung khi không nêu phương pháp cụ thể.

Nguồn: VietMed-NER train, dòng 4180 (từ 0).

## VM600-545

**Đoạn gốc:** một cái giờ định kỳ cái sau đó dùng là các cái lần tái khám thì bác đưa cho các

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | tái khám | Xét nghiệm hoặc thăm khám (TEST) | [51, 59) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Thay đổi NER

- E1 “khám” TEST [55, 59) → E1 “tái khám” TEST [51, 59)

Nguồn: VietMed-NER train, dòng 4191 (từ 0).

## VM600-546

**Đoạn gốc:** tăng huy động tế bào tăng nhiệt độ cơ thể tăng tiêu hao năng lượng như bên cạnh đó thì cái việc mà bị ung thư thì

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | tế bào | Bộ phận cơ thể (BODY_PART) | [14, 20) |
| E2 | cơ thể | Bộ phận cơ thể (BODY_PART) | [35, 41) |
| E3 | ung thư | Bệnh hoặc triệu chứng (CONDITION) | [102, 109) |

### RE

| Mã | Cặp có hướng | Kết luận đề xuất |
|---|---|---|
| R1 | E3 “ung thư” → E1 “tế bào” | Không có quan hệ thuộc 5 loại (NO_RELATION) |
| R2 | E3 “ung thư” → E2 “cơ thể” | Không có quan hệ thuộc 5 loại (NO_RELATION) |

Nguồn: VietMed-NER train, dòng 4201 (từ 0).

## VM600-547

**Đoạn gốc:** định cân bằng được cái stress ổn định này rồi thì cái việc mà cái điều trị tích cực đó

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | stress | Bệnh hoặc triệu chứng (CONDITION) | [23, 29) |
| E2 | điều trị | Thủ thuật hoặc điều trị (PROCEDURE) | [66, 74) |

### RE

| Mã | Cặp có hướng | Kết luận đề xuất |
|---|---|---|
| R1 | E1 “stress” → E2 “điều trị” | Chưa rõ — cần chốt (CHUA_RO) |

### Cần chốt

- CONTEXT_OR_TRANSCRIPT: câu bị cắt, tham chiếu/mục đích chưa rõ hoặc nghi lỗi phiên âm; cần xem ngữ cảnh/audio gốc, không tự sửa văn bản.
- GENERIC_INTERVENTION: cần chốt việc giữ hành động điều trị/chẩn đoán chung khi không nêu phương pháp cụ thể.
- UNRESOLVED_RE: còn cặp CHUA_RO; tuyệt đối không đổi thành NO_RELATION khi xuất huấn luyện.

Nguồn: VietMed-NER train, dòng 4204 (từ 0).

## VM600-548

**Đoạn gốc:** họ tiếp xúc với bệnh đậu mùa bò một loại nhiễm virus nhẹ mà con người có thể mắc

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | đậu mùa bò | Bệnh hoặc triệu chứng (CONDITION) | [21, 31) |
| E3 | nhiễm virus | Bệnh hoặc triệu chứng (CONDITION) | [41, 52) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- SCOPE_CONFIRMATION: cần xác nhận quy ước về thuốc/dược chất, can thiệp không dùng thuốc, thiết bị, tác nhân hoặc hoạt động thăm khám; không coi ánh xạ nguồn là xác nhận chuyên gia.

### Thay đổi NER

- E2 “virus” CONDITION [47, 52) → ∅
- E1 “đậu mùa” CONDITION [21, 28) → E1 “đậu mùa bò” CONDITION [21, 31)
- ∅ → E3 “nhiễm virus” CONDITION [41, 52)

Nguồn: VietMed-NER train, dòng 4207 (từ 0).

## VM600-549

**Đoạn gốc:** tác dụng phụ lên đường tiêu hóa lên các cái hệ nội tạng chính vì vậy cho nên đấy là một trong những cái hướng mà tiếp cận

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | tác dụng phụ | Bệnh hoặc triệu chứng (CONDITION) | [0, 12) |
| E2 | đường tiêu hóa | Bộ phận cơ thể (BODY_PART) | [17, 31) |
| E3 | nội tạng | Bộ phận cơ thể (BODY_PART) | [47, 55) |

### RE

| Mã | Cặp có hướng | Kết luận đề xuất |
|---|---|---|
| R1 | E1 “tác dụng phụ” → E2 “đường tiêu hóa” | Có vị trí ở (located_at) |
| R2 | E1 “tác dụng phụ” → E3 “nội tạng” | Có vị trí ở (located_at) |

### Cần chốt

- GENERIC_MENTION: cần chốt có giữ bệnh/triệu chứng/biến chứng chung và tham chiếu không định danh trong NER hay không.

### Thay đổi NER

- E4 “một trong những cái hướng” DOSAGE [84, 109) → ∅

Nguồn: VietMed-NER train, dòng 4227 (từ 0).

## VM600-550

**Đoạn gốc:** đôi khi có một số bạn cũng như biết không chia sẻ là em ngủ dậy là coi như mặt em dùng chảo dầu bóng loáng

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | mặt | Bộ phận cơ thể (BODY_PART) | [75, 78) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- CONTEXT_OR_TRANSCRIPT: câu bị cắt, tham chiếu/mục đích chưa rõ hoặc nghi lỗi phiên âm; cần xem ngữ cảnh/audio gốc, không tự sửa văn bản.

### Thay đổi NER

- ∅ → E1 “mặt” BODY_PART [75, 78)

Nguồn: VietMed-NER train, dòng 4235 (từ 0).

## VM600-551

**Đoạn gốc:** chúng ta nó có chính là ba giai đoạn ba giai đoạn chính giai đoạn thứ nhất là giai đoạn mà phát triển hay là giai đoạn

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

Không có thực thể thuộc sáu loại được giữ trong bản rà soát.

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Thay đổi NER

- E1 “ba giai đoạn” DOSAGE [24, 36) → ∅
- E2 “ba giai đoạn” DOSAGE [37, 49) → ∅
- E3 “giai đoạn” DOSAGE [56, 65) → ∅
- E4 “thứ nhất” DOSAGE [66, 74) → ∅

Nguồn: VietMed-NER train, dòng 4245 (từ 0).

## VM600-552

**Đoạn gốc:** tiềm tàng là bất định nhưng hậu quả khi mọi thứ lạc lối có thể là khủng khiếp nỗ

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

Không có thực thể thuộc sáu loại được giữ trong bản rà soát.

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

Nguồn: VietMed-NER train, dòng 4247 (từ 0).

## VM600-553

**Đoạn gốc:** tính ra năng lượng là chí ít nó cũng phải đạt được khoảng một phẩy hai một đến một phẩy hai kcal trong

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

Không có thực thể thuộc sáu loại được giữ trong bản rà soát.

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- CONTEXT_OR_TRANSCRIPT: câu bị cắt, tham chiếu/mục đích chưa rõ hoặc nghi lỗi phiên âm; cần xem ngữ cảnh/audio gốc, không tự sửa văn bản.

### Thay đổi NER

- E1 “kcal” DOSAGE [92, 96) → ∅

Nguồn: VietMed-NER train, dòng 4248 (từ 0).

## VM600-554

**Đoạn gốc:** nói rằng là cái lượng máu để mà nuôi tim nuôi náo nó bị suy giảm nếu như chỉ suy

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | máu | Bộ phận cơ thể (BODY_PART) | [22, 25) |
| E3 | tim | Bộ phận cơ thể (BODY_PART) | [37, 40) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- CONTEXT_OR_TRANSCRIPT: câu bị cắt, tham chiếu/mục đích chưa rõ hoặc nghi lỗi phiên âm; cần xem ngữ cảnh/audio gốc, không tự sửa văn bản.

### Thay đổi NER

- E2 “nuôi tim” PROCEDURE [32, 40) → ∅
- ∅ → E3 “tim” BODY_PART [37, 40)

Nguồn: VietMed-NER train, dòng 4253 (từ 0).

## VM600-555

**Đoạn gốc:** như là một số khán giả có nội dung tương tự và câu hỏi gửi về cho chương trình thưa bác sĩ nghe nói phẫu thuật đặt điện

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | phẫu thuật | Thủ thuật hoặc điều trị (PROCEDURE) | [100, 110) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- CONTEXT_OR_TRANSCRIPT: câu bị cắt, tham chiếu/mục đích chưa rõ hoặc nghi lỗi phiên âm; cần xem ngữ cảnh/audio gốc, không tự sửa văn bản.

Nguồn: VietMed-NER train, dòng 4255 (từ 0).

## VM600-556

**Đoạn gốc:** bào tim trong điều kiện thiếu oxy cho nên có thể nói rằng là với hệ thống tim

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | tim | Bộ phận cơ thể (BODY_PART) | [4, 7) |
| E2 | thiếu oxy | Bệnh hoặc triệu chứng (CONDITION) | [24, 33) |
| E3 | tim | Bộ phận cơ thể (BODY_PART) | [74, 77) |

### RE

| Mã | Cặp có hướng | Kết luận đề xuất |
|---|---|---|
| R1 | E2 “thiếu oxy” → E1 “tim” | Có vị trí ở (located_at) |
| R2 | E2 “thiếu oxy” → E3 “tim” | Chưa rõ — cần chốt (CHUA_RO) |

### Cần chốt

- CONTEXT_OR_TRANSCRIPT: câu bị cắt, tham chiếu/mục đích chưa rõ hoặc nghi lỗi phiên âm; cần xem ngữ cảnh/audio gốc, không tự sửa văn bản.
- UNRESOLVED_RE: còn cặp CHUA_RO; tuyệt đối không đổi thành NO_RELATION khi xuất huấn luyện.

Nguồn: VietMed-NER train, dòng 4258 (từ 0).

## VM600-557

**Đoạn gốc:** người bệnh có đông cứng về dáng đi hoặc là đi dễ té ngã mà những cái triệu chứng này nó không cải thiện với các cái thuốc

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | đông cứng về dáng đi | Bệnh hoặc triệu chứng (CONDITION) | [14, 34) |
| E2 | đi dễ té ngã | Bệnh hoặc triệu chứng (CONDITION) | [43, 55) |
| E5 | thuốc | Thuốc/dược chất (DRUG) | [116, 121) |

### RE

| Mã | Cặp có hướng | Kết luận đề xuất |
|---|---|---|
| R1 | E1 “đông cứng về dáng đi” → E5 “thuốc” | Chưa rõ — cần chốt (CHUA_RO) |
| R2 | E2 “đi dễ té ngã” → E5 “thuốc” | Chưa rõ — cần chốt (CHUA_RO) |

### Cần chốt

- CONTEXT_OR_TRANSCRIPT: câu bị cắt, tham chiếu/mục đích chưa rõ hoặc nghi lỗi phiên âm; cần xem ngữ cảnh/audio gốc, không tự sửa văn bản.
- UNRESOLVED_RE: còn cặp CHUA_RO; tuyệt đối không đổi thành NO_RELATION khi xuất huấn luyện.

### Thay đổi NER

- E4 “cải thiện” PROCEDURE [94, 103) → ∅
- E3 “triệu chứng” CONDITION [69, 80) → ∅

Nguồn: VietMed-NER train, dòng 4262 (từ 0).

## VM600-558

**Đoạn gốc:** bị tổn thương hơn đường tiêu hóa chúng ta dễ bị tổn thương hơn như vậy đó ở những người lớn tuổi chúng ta rất là

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E2 | tổn thương | Bệnh hoặc triệu chứng (CONDITION) | [3, 13) |
| E3 | đường tiêu hóa | Bộ phận cơ thể (BODY_PART) | [18, 32) |
| E5 | tổn thương | Bệnh hoặc triệu chứng (CONDITION) | [48, 58) |

### RE

| Mã | Cặp có hướng | Kết luận đề xuất |
|---|---|---|
| R1 | E2 “tổn thương” → E3 “đường tiêu hóa” | Chưa rõ — cần chốt (CHUA_RO) |
| R2 | E5 “tổn thương” → E3 “đường tiêu hóa” | Có vị trí ở (located_at) |

### Cần chốt

- CONTEXT_OR_TRANSCRIPT: câu bị cắt, tham chiếu/mục đích chưa rõ hoặc nghi lỗi phiên âm; cần xem ngữ cảnh/audio gốc, không tự sửa văn bản.
- UNRESOLVED_RE: còn cặp CHUA_RO; tuyệt đối không đổi thành NO_RELATION khi xuất huấn luyện.

### Thay đổi NER

- E1 “bị” CONDITION [0, 2) → ∅
- E4 “bị” CONDITION [45, 47) → ∅

Nguồn: VietMed-NER train, dòng 4279 (từ 0).

## VM600-559

**Đoạn gốc:** tim mạch nói chung thì các cái biện pháp và khuyến khích vẫn là nên tập thể dục thì tập thể dục thì một cái nguyên tắc

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | tim mạch | Bộ phận cơ thể (BODY_PART) | [0, 8) |
| E2 | tập thể dục | Thủ thuật hoặc điều trị (PROCEDURE) | [68, 79) |
| E3 | tập thể dục | Thủ thuật hoặc điều trị (PROCEDURE) | [84, 95) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- SCOPE_CONFIRMATION: cần xác nhận quy ước về thuốc/dược chất, can thiệp không dùng thuốc, thiết bị, tác nhân hoặc hoạt động thăm khám; không coi ánh xạ nguồn là xác nhận chuyên gia.

### Thay đổi NER

- ∅ → E2 “tập thể dục” PROCEDURE [68, 79)
- ∅ → E3 “tập thể dục” PROCEDURE [84, 95)

Nguồn: VietMed-NER train, dòng 4283 (từ 0).

## VM600-560

**Đoạn gốc:** mình mong muốn đấy là cái điều quan trọng mà chương trình hôm nay chúng ta muốn nói đến để các quý vị chúng ta có

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

Không có thực thể thuộc sáu loại được giữ trong bản rà soát.

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

Nguồn: VietMed-NER train, dòng 4297 (từ 0).

## VM600-561

**Đoạn gốc:** cái việc chính của mình là mình phải tiêm vắcxin phòng bệnh này bằng cách 5k này và mình tiêm vắcxin chống covid

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | tiêm | Thủ thuật hoặc điều trị (PROCEDURE) | [37, 41) |
| E2 | vắcxin | Thuốc/dược chất (DRUG) | [42, 48) |
| E3 | 5k | Thủ thuật hoặc điều trị (PROCEDURE) | [74, 76) |
| E4 | tiêm | Thủ thuật hoặc điều trị (PROCEDURE) | [89, 93) |
| E5 | vắcxin | Thuốc/dược chất (DRUG) | [94, 100) |
| E6 | covid | Bệnh hoặc triệu chứng (CONDITION) | [107, 112) |

### RE

| Mã | Cặp có hướng | Kết luận đề xuất |
|---|---|---|
| R1 | E6 “covid” → E1 “tiêm” | Không có quan hệ thuộc 5 loại (NO_RELATION) |
| R2 | E6 “covid” → E2 “vắcxin” | Không có quan hệ thuộc 5 loại (NO_RELATION) |
| R3 | E6 “covid” → E3 “5k” | Không có quan hệ thuộc 5 loại (NO_RELATION) |
| R4 | E6 “covid” → E4 “tiêm” | Không có quan hệ thuộc 5 loại (NO_RELATION) |
| R5 | E6 “covid” → E5 “vắcxin” | Không có quan hệ thuộc 5 loại (NO_RELATION) |

### Cần chốt

- SCOPE_CONFIRMATION: cần xác nhận quy ước về thuốc/dược chất, can thiệp không dùng thuốc, thiết bị, tác nhân hoặc hoạt động thăm khám; không coi ánh xạ nguồn là xác nhận chuyên gia.

### Thay đổi NER

- E3 “5k” DRUG [74, 76) → E3 “5k” PROCEDURE [74, 76)

Nguồn: VietMed-NER train, dòng 4306 (từ 0).

## VM600-562

**Đoạn gốc:** người f1 này với nhau cũng làm sao để giảm các nguy cơ lây chéo bởi vì người

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E2 | lây chéo | Bệnh hoặc triệu chứng (CONDITION) | [55, 63) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Thay đổi NER

- E1 “nguy cơ lây chéo” DRUG [47, 63) → ∅
- ∅ → E2 “lây chéo” CONDITION [55, 63)

Nguồn: VietMed-NER train, dòng 4312 (từ 0).

## VM600-563

**Đoạn gốc:** vâng những cái quan trọng nhất là chúng ta cần phải nắm vững được những cái nguyên tắc về dinh dưỡng và đồng thời là

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

Không có thực thể thuộc sáu loại được giữ trong bản rà soát.

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

Nguồn: VietMed-NER train, dòng 4325 (từ 0).

## VM600-564

**Đoạn gốc:** ưu tiên đầu tiên đó là chúng ta phải điều trị mụn ẩn rồi tuy nhiên là có một số bạn là bị mụn ẩn nhưng mà có

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | điều trị | Thủ thuật hoặc điều trị (PROCEDURE) | [37, 45) |
| E3 | mụn ẩn | Bệnh hoặc triệu chứng (CONDITION) | [46, 52) |
| E2 | mụn ẩn | Bệnh hoặc triệu chứng (CONDITION) | [90, 96) |

### RE

| Mã | Cặp có hướng | Kết luận đề xuất |
|---|---|---|
| R1 | E3 “mụn ẩn” → E1 “điều trị” | Được điều trị bằng phương pháp (treated_by_procedure) |
| R2 | E2 “mụn ẩn” → E1 “điều trị” | Chưa rõ — cần chốt (CHUA_RO) |

### Cần chốt

- CONTEXT_OR_TRANSCRIPT: câu bị cắt, tham chiếu/mục đích chưa rõ hoặc nghi lỗi phiên âm; cần xem ngữ cảnh/audio gốc, không tự sửa văn bản.
- GENERIC_INTERVENTION: cần chốt việc giữ hành động điều trị/chẩn đoán chung khi không nêu phương pháp cụ thể.
- UNRESOLVED_RE: còn cặp CHUA_RO; tuyệt đối không đổi thành NO_RELATION khi xuất huấn luyện.

### Thay đổi NER

- E1 “điều trị mụn ẩn” PROCEDURE [37, 52) → E1 “điều trị” PROCEDURE [37, 45)
- ∅ → E3 “mụn ẩn” CONDITION [46, 52)

Nguồn: VietMed-NER train, dòng 4334 (từ 0).

## VM600-565

**Đoạn gốc:** thực vật nó quan trọng không chỉ ở chất đạm mà nó còn quan trọng ở chất béo và nó còn quan trọng là cái

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | chất béo | Thuốc/dược chất (DRUG) | [67, 75) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- ONTOLOGY_SCOPE: cần chốt phạm vi thuốc/dược chất so với mỹ phẩm, thực phẩm, hóa chất nội sinh hoặc hệ vi sinh; giữ ánh xạ nguồn khi chưa có quy ước đủ rõ.

Nguồn: VietMed-NER train, dòng 4335 (từ 0).

## VM600-566

**Đoạn gốc:** biết như vậy nhưng mà sau này khi mà y học hiện đại người ta mới phân tích thì người ta thấy rằng là à cái đuôi có tắc

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

Không có thực thể thuộc sáu loại được giữ trong bản rà soát.

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Thay đổi NER

- E1 “phân tích” PROCEDURE [65, 74) → ∅

Nguồn: VietMed-NER train, dòng 4351 (từ 0).

## VM600-567

**Đoạn gốc:** là nhiều người bị ung thư bị gầy đi hẳn hoi nhưng cứ bảo là chúng ta bỏ đói tế

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | ung thư | Bệnh hoặc triệu chứng (CONDITION) | [18, 25) |
| E2 | gầy đi | Bệnh hoặc triệu chứng (CONDITION) | [29, 35) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- CONTEXT_OR_TRANSCRIPT: câu bị cắt, tham chiếu/mục đích chưa rõ hoặc nghi lỗi phiên âm; cần xem ngữ cảnh/audio gốc, không tự sửa văn bản.

### Thay đổi NER

- ∅ → E2 “gầy đi” CONDITION [29, 35)

Nguồn: VietMed-NER train, dòng 4354 (từ 0).

## VM600-568

**Đoạn gốc:** vâng ạ tôi thì thấy thực tế là khi mà chúng ta nhận một cái khẩu phần vào và rất

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

Không có thực thể thuộc sáu loại được giữ trong bản rà soát.

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

Nguồn: VietMed-NER train, dòng 4366 (từ 0).

## VM600-569

**Đoạn gốc:** lại càng cần phải tiêm bác ạ tại vì là khi mà chúng ta không tiêm ấy mà khi mắc bệnh là bệnh sẽ rất rất nặng thế và

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | tiêm | Thủ thuật hoặc điều trị (PROCEDURE) | [18, 22) |
| E2 | tiêm | Thủ thuật hoặc điều trị (PROCEDURE) | [61, 65) |
| E3 | bệnh | Bệnh hoặc triệu chứng (CONDITION) | [80, 84) |
| E4 | bệnh | Bệnh hoặc triệu chứng (CONDITION) | [88, 92) |

### RE

| Mã | Cặp có hướng | Kết luận đề xuất |
|---|---|---|
| R1 | E3 “bệnh” → E1 “tiêm” | Không có quan hệ thuộc 5 loại (NO_RELATION) |
| R2 | E3 “bệnh” → E2 “tiêm” | Không có quan hệ thuộc 5 loại (NO_RELATION) |
| R3 | E4 “bệnh” → E1 “tiêm” | Không có quan hệ thuộc 5 loại (NO_RELATION) |
| R4 | E4 “bệnh” → E2 “tiêm” | Không có quan hệ thuộc 5 loại (NO_RELATION) |

### Cần chốt

- GENERIC_MENTION: cần chốt có giữ bệnh/triệu chứng/biến chứng chung và tham chiếu không định danh trong NER hay không.

### Thay đổi NER

- E3 “mắc bệnh” CONDITION [76, 84) → E3 “bệnh” CONDITION [80, 84)
- ∅ → E4 “bệnh” CONDITION [88, 92)

Nguồn: VietMed-NER train, dòng 4376 (từ 0).

## VM600-570

**Đoạn gốc:** được tự ý bỏ đâu vì là những cái cái thức cái huyết áp này là cái việc điều

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | huyết áp | Bệnh hoặc triệu chứng (CONDITION) | [46, 54) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- CONTEXT_OR_TRANSCRIPT: câu bị cắt, tham chiếu/mục đích chưa rõ hoặc nghi lỗi phiên âm; cần xem ngữ cảnh/audio gốc, không tự sửa văn bản.
- PHYSIOLOGY_VS_DISEASE: từ huyết áp/mỡ máu đứng riêng chưa xác định bệnh; giữ đề xuất nguồn chờ chốt.

Nguồn: VietMed-NER train, dòng 4378 (từ 0).

## VM600-571

**Đoạn gốc:** màng xơ vữa nên là nó sẽ có tác dụng lâu dài nên các quý vị khi sử dụng để mang lại cho hiệu quả cao nhất thì chúng

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | màng xơ vữa | Bệnh hoặc triệu chứng (CONDITION) | [0, 11) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- CONTEXT_OR_TRANSCRIPT: câu bị cắt, tham chiếu/mục đích chưa rõ hoặc nghi lỗi phiên âm; cần xem ngữ cảnh/audio gốc, không tự sửa văn bản.

### Thay đổi NER

- E2 “hiệu quả cao nhất” DOSAGE [88, 105) → ∅
- E1 “xơ vữa” CONDITION [5, 11) → E1 “màng xơ vữa” CONDITION [0, 11)

Nguồn: VietMed-NER train, dòng 4381 (từ 0).

## VM600-572

**Đoạn gốc:** trong đó thì là có cái chẩn đoán cho chị là kiểu thiếu máu cơ tim vâng đây nó chính là những cái tình trạng là thiếu máu của

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | chẩn đoán | Xét nghiệm hoặc thăm khám (TEST) | [23, 32) |
| E2 | thiếu máu cơ tim | Bệnh hoặc triệu chứng (CONDITION) | [49, 65) |
| E5 | thiếu máu | Bệnh hoặc triệu chứng (CONDITION) | [111, 120) |

### RE

| Mã | Cặp có hướng | Kết luận đề xuất |
|---|---|---|
| R1 | E2 “thiếu máu cơ tim” → E1 “chẩn đoán” | Chưa rõ — cần chốt (CHUA_RO) |
| R2 | E5 “thiếu máu” → E1 “chẩn đoán” | Chưa rõ — cần chốt (CHUA_RO) |

### Cần chốt

- CONTEXT_OR_TRANSCRIPT: câu bị cắt, tham chiếu/mục đích chưa rõ hoặc nghi lỗi phiên âm; cần xem ngữ cảnh/audio gốc, không tự sửa văn bản.
- GENERIC_INTERVENTION: cần chốt việc giữ hành động điều trị/chẩn đoán chung khi không nêu phương pháp cụ thể.
- UNRESOLVED_RE: còn cặp CHUA_RO; tuyệt đối không đổi thành NO_RELATION khi xuất huấn luyện.

### Thay đổi NER

- E3 “cơ” BODY_PART [59, 61) → E3 “cơ tim” BODY_PART [59, 65)
- E4 “tim” BODY_PART [62, 65) → ∅
- E2 “thiếu máu” CONDITION [49, 58) → E2 “thiếu máu cơ tim” CONDITION [49, 65)
- E3 “cơ tim” BODY_PART [59, 65) → ∅

Nguồn: VietMed-NER train, dòng 4398 (từ 0).

## VM600-573

**Đoạn gốc:** nhưng sự thay đổi trong môi trường ruột ví dụ do lạm dụng một số loại kháng sinh có thể thúc đẩy sẽ phát triển quá mức

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | ruột | Bộ phận cơ thể (BODY_PART) | [35, 39) |
| E2 | kháng sinh | Thuốc/dược chất (DRUG) | [70, 80) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

Nguồn: VietMed-NER train, dòng 4427 (từ 0).

## VM600-574

**Đoạn gốc:** hướng dẫn cái phẫu thuật viên để đưa cái điện cực vào và khi mình đưa xuống

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E2 | điện cực | Thủ thuật hoặc điều trị (PROCEDURE) | [41, 49) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- SCOPE_CONFIRMATION: cần xác nhận quy ước về thuốc/dược chất, can thiệp không dùng thuốc, thiết bị, tác nhân hoặc hoạt động thăm khám; không coi ánh xạ nguồn là xác nhận chuyên gia.

### Thay đổi NER

- E1 “phẫu thuật” PROCEDURE [14, 24) → ∅

Nguồn: VietMed-NER train, dòng 4453 (từ 0).

## VM600-575

**Đoạn gốc:** thiện triệu chứng run rất là tốt chúng ta biết rằng là run là một trong những cái đặc tính chính của bệnh parkinson

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | run | Bệnh hoặc triệu chứng (CONDITION) | [18, 21) |
| E2 | run | Bệnh hoặc triệu chứng (CONDITION) | [55, 58) |
| E3 | parkinson | Bệnh hoặc triệu chứng (CONDITION) | [106, 115) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Thay đổi NER

- E1 “triệu chứng run” CONDITION [6, 21) → E1 “run” CONDITION [18, 21)

Nguồn: VietMed-NER train, dòng 4461 (từ 0).

## VM600-576

**Đoạn gốc:** thể nói là những người trung quốc những người ở nhật bản những người hàn quốc từ xa xưa người ta đã sử dụng cái này và

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

Không có thực thể thuộc sáu loại được giữ trong bản rà soát.

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

Nguồn: VietMed-NER train, dòng 4463 (từ 0).

## VM600-577

**Đoạn gốc:** làm thuốc thì cha ông chúng ta là lựa chọn những cái bộ phận mà nó có tác dụng

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | thuốc | Thuốc/dược chất (DRUG) | [4, 9) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- ONTOLOGY_SCOPE: cần chốt phạm vi thuốc/dược chất so với mỹ phẩm, thực phẩm, hóa chất nội sinh hoặc hệ vi sinh; giữ ánh xạ nguồn khi chưa có quy ước đủ rõ.

Nguồn: VietMed-NER train, dòng 4466 (từ 0).

## VM600-578

**Đoạn gốc:** chỉ phát hiện sự hiện diện của mầm bệnh mà còn có thể nhận ra loại mầm bệnh hiện diện và chỉ đạo đáp ứng miễn dịch phù

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

Không có thực thể thuộc sáu loại được giữ trong bản rà soát.

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- SCOPE_CONFIRMATION: cần xác nhận quy ước về thuốc/dược chất, can thiệp không dùng thuốc, thiết bị, tác nhân hoặc hoạt động thăm khám; không coi ánh xạ nguồn là xác nhận chuyên gia.

### Thay đổi NER

- E1 “mầm bệnh” CONDITION [31, 39) → ∅
- E2 “mầm bệnh” CONDITION [67, 75) → ∅

Nguồn: VietMed-NER train, dòng 4472 (từ 0).

## VM600-579

**Đoạn gốc:** cái mà chúng ta khám trên lâm sàng thì đôi khi chúng ta chưa đủ để chuẩn đoán một da nhạy cảm chính xác thì chúng ta

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | khám trên lâm sàng | Xét nghiệm hoặc thăm khám (TEST) | [16, 34) |
| E2 | chuẩn đoán | Xét nghiệm hoặc thăm khám (TEST) | [67, 77) |
| E3 | da nhạy cảm | Bệnh hoặc triệu chứng (CONDITION) | [82, 93) |

### RE

| Mã | Cặp có hướng | Kết luận đề xuất |
|---|---|---|
| R1 | E3 “da nhạy cảm” → E1 “khám trên lâm sàng” | Chưa rõ — cần chốt (CHUA_RO) |
| R2 | E3 “da nhạy cảm” → E2 “chuẩn đoán” | Chưa rõ — cần chốt (CHUA_RO) |

### Cần chốt

- CONTEXT_OR_TRANSCRIPT: câu bị cắt, tham chiếu/mục đích chưa rõ hoặc nghi lỗi phiên âm; cần xem ngữ cảnh/audio gốc, không tự sửa văn bản.
- GENERIC_INTERVENTION: cần chốt việc giữ hành động điều trị/chẩn đoán chung khi không nêu phương pháp cụ thể.
- UNRESOLVED_RE: còn cặp CHUA_RO; tuyệt đối không đổi thành NO_RELATION khi xuất huấn luyện.

### Thay đổi NER

- E1 “khám” TEST [16, 20) → E1 “khám trên lâm sàng” TEST [16, 34)

Nguồn: VietMed-NER train, dòng 4473 (từ 0).

## VM600-580

**Đoạn gốc:** trình về sau của người bệnh là những cái thăm khám mà những cái xét nghiệm mà bệnh nhân phải

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | thăm khám | Xét nghiệm hoặc thăm khám (TEST) | [41, 50) |
| E2 | xét nghiệm | Xét nghiệm hoặc thăm khám (TEST) | [64, 74) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- SCOPE_CONFIRMATION: cần xác nhận quy ước về thuốc/dược chất, can thiệp không dùng thuốc, thiết bị, tác nhân hoặc hoạt động thăm khám; không coi ánh xạ nguồn là xác nhận chuyên gia.

### Thay đổi NER

- E1 “thăm khám” PROCEDURE [41, 50) → E1 “thăm khám” TEST [41, 50)

Nguồn: VietMed-NER train, dòng 4477 (từ 0).

## VM600-581

**Đoạn gốc:** là nguyên phát hay thứ phát bởi vì có một số trường hợp đó là da nhạy cảm nhưng mà bệnh nhân có các bệnh lý da

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | da nhạy cảm | Bệnh hoặc triệu chứng (CONDITION) | [62, 73) |
| E2 | bệnh lý da | Bệnh hoặc triệu chứng (CONDITION) | [100, 110) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

Nguồn: VietMed-NER train, dòng 4478 (từ 0).

## VM600-582

**Đoạn gốc:** trước đại dịch như thế này thì thực sự rất là nhiều thách thức nhưng thách thức ấy có vượt qua được hay không thì phần

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

Không có thực thể thuộc sáu loại được giữ trong bản rà soát.

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Thay đổi NER

- E1 “đại dịch” CONDITION [6, 14) → ∅

Nguồn: VietMed-NER train, dòng 4482 (từ 0).

## VM600-583

**Đoạn gốc:** giúp ngăn ngừa các vấn đề trong ghép tạng cũng là kết quả của một đáp ứng miễn dịch không mong muốn trong trường

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E2 | ghép tạng | Thủ thuật hoặc điều trị (PROCEDURE) | [32, 41) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- SCOPE_CONFIRMATION: cần xác nhận quy ước về thuốc/dược chất, can thiệp không dùng thuốc, thiết bị, tác nhân hoặc hoạt động thăm khám; không coi ánh xạ nguồn là xác nhận chuyên gia.

### Thay đổi NER

- E1 “ngăn ngừa” DRUG [5, 14) → ∅

Nguồn: VietMed-NER train, dòng 4483 (từ 0).

## VM600-584

**Đoạn gốc:** oxy hóa gấp sáu mươi lần trước đây thế thì tuyệt vời và chính quay trở lại câu

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

Không có thực thể thuộc sáu loại được giữ trong bản rà soát.

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Thay đổi NER

- E1 “oxy” DRUG [0, 3) → ∅

Nguồn: VietMed-NER train, dòng 4491 (từ 0).

## VM600-585

**Đoạn gốc:** đường huyết cũng là thể trở nên rất là khó khăn và hơn so với lại những cái

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

Không có thực thể thuộc sáu loại được giữ trong bản rà soát.

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- CONTEXT_OR_TRANSCRIPT: câu bị cắt, tham chiếu/mục đích chưa rõ hoặc nghi lỗi phiên âm; cần xem ngữ cảnh/audio gốc, không tự sửa văn bản.

### Thay đổi NER

- E1 “huyết” BODY_PART [6, 11) → ∅

Nguồn: VietMed-NER train, dòng 4495 (từ 0).

## VM600-586

**Đoạn gốc:** loạn nhịp tim thì khi chúng ta sử dụng kết hợp cùng với viên nang đông trùng hạ thảo thì chúng ta nên uống cách nhau ra

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | loạn nhịp tim | Bệnh hoặc triệu chứng (CONDITION) | [0, 13) |
| E2 | viên nang đông trùng hạ thảo | Thuốc/dược chất (DRUG) | [56, 84) |

### RE

| Mã | Cặp có hướng | Kết luận đề xuất |
|---|---|---|
| R1 | E1 “loạn nhịp tim” → E2 “viên nang đông trùng hạ thảo” | Chưa rõ — cần chốt (CHUA_RO) |

### Cần chốt

- CONTEXT_OR_TRANSCRIPT: câu bị cắt, tham chiếu/mục đích chưa rõ hoặc nghi lỗi phiên âm; cần xem ngữ cảnh/audio gốc, không tự sửa văn bản.
- ONTOLOGY_SCOPE: cần chốt phạm vi thuốc/dược chất so với mỹ phẩm, thực phẩm, hóa chất nội sinh hoặc hệ vi sinh; giữ ánh xạ nguồn khi chưa có quy ước đủ rõ.
- UNRESOLVED_RE: còn cặp CHUA_RO; tuyệt đối không đổi thành NO_RELATION khi xuất huấn luyện.

Nguồn: VietMed-NER train, dòng 4497 (từ 0).

## VM600-587

**Đoạn gốc:** dần dần để chúng ta có thể tức là bằng lý trí để chúng ta có thể ăn được cả bên

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

Không có thực thể thuộc sáu loại được giữ trong bản rà soát.

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

Nguồn: VietMed-NER train, dòng 4504 (từ 0).

## VM600-588

**Đoạn gốc:** chúng ta đều bị xâm chiếm từng khoảnh khắc bởi các sinh vật có khả năng đe dọa tính mạng nếu không có hệ miễn dịch hoạt

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | hệ miễn dịch | Bộ phận cơ thể (BODY_PART) | [102, 114) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

Nguồn: VietMed-NER train, dòng 4508 (từ 0).

## VM600-589

**Đoạn gốc:** chúng ta ngồi nhiều thứ hai nữa là chúng ta phải gần như là khi mà chúng ta làm việc với máy tính hoặc là các cái công

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

Không có thực thể thuộc sáu loại được giữ trong bản rà soát.

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

Nguồn: VietMed-NER train, dòng 4511 (từ 0).

## VM600-590

**Đoạn gốc:** cái thứ hai là cái dinh dưỡng ở sau ung thư nó còn có vai trò vô cùng quan trọng đó

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E2 | ung thư | Bệnh hoặc triệu chứng (CONDITION) | [36, 43) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Thay đổi NER

- E1 “cái thứ hai” DOSAGE [0, 11) → ∅

Nguồn: VietMed-NER train, dòng 4528 (từ 0).

## VM600-591

**Đoạn gốc:** trộn không cần phải đun để chúng ta có thể trộn vào để chúng ta ăn thì chúng

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

Không có thực thể thuộc sáu loại được giữ trong bản rà soát.

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

Nguồn: VietMed-NER train, dòng 4532 (từ 0).

## VM600-592

**Đoạn gốc:** tốt cho sức khỏe của chúng ta nữa cho nên là nếu những ai bị huyết áp những ai bị đái tháo đường những ai bị các bệnh

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | huyết áp | Bệnh hoặc triệu chứng (CONDITION) | [61, 69) |
| E2 | đái tháo đường | Bệnh hoặc triệu chứng (CONDITION) | [82, 96) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- CONTEXT_OR_TRANSCRIPT: câu bị cắt, tham chiếu/mục đích chưa rõ hoặc nghi lỗi phiên âm; cần xem ngữ cảnh/audio gốc, không tự sửa văn bản.
- PHYSIOLOGY_VS_DISEASE: từ huyết áp/mỡ máu đứng riêng chưa xác định bệnh; giữ đề xuất nguồn chờ chốt.

Nguồn: VietMed-NER train, dòng 4547 (từ 0).

## VM600-593

**Đoạn gốc:** có thể đi làm lại được xin mời bác sĩ thường thì giai đoạn hậu phẫu của phẫu

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

Không có thực thể thuộc sáu loại được giữ trong bản rà soát.

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- CONTEXT_OR_TRANSCRIPT: câu bị cắt, tham chiếu/mục đích chưa rõ hoặc nghi lỗi phiên âm; cần xem ngữ cảnh/audio gốc, không tự sửa văn bản.

### Thay đổi NER

- E1 “hậu phẫu” PROCEDURE [59, 67) → ∅

Nguồn: VietMed-NER train, dòng 4557 (từ 0).

## VM600-594

**Đoạn gốc:** đối với lại cái cuộc sống họ cũng cảm thấy là họ bị mặc cảm về cái giá trị của chính mình họ cảm thấy là họ sống

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | mặc cảm | Bệnh hoặc triệu chứng (CONDITION) | [52, 59) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- SYMPTOM_SCOPE: cần phân biệt cảm xúc thông thường với triệu chứng lâm sàng theo quy ước dự án.

Nguồn: VietMed-NER train, dòng 4558 (từ 0).

## VM600-595

**Đoạn gốc:** chiều cái vị giác của bản thân cái người bị ung thư đó của của ví dụ như

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | ung thư | Bệnh hoặc triệu chứng (CONDITION) | [44, 51) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

Nguồn: VietMed-NER train, dòng 4561 (từ 0).

## VM600-596

**Đoạn gốc:** hơn thì đối với những trường hợp này chúng ta phải coi lại coi là chúng ta đã dưỡng ẩm đủ chưa thì đã xin chia sẻ

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | dưỡng ẩm | Thủ thuật hoặc điều trị (PROCEDURE) | [78, 86) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- SCOPE_CONFIRMATION: cần xác nhận quy ước về thuốc/dược chất, can thiệp không dùng thuốc, thiết bị, tác nhân hoặc hoạt động thăm khám; không coi ánh xạ nguồn là xác nhận chuyên gia.

### Thay đổi NER

- ∅ → E1 “dưỡng ẩm” PROCEDURE [78, 86)

Nguồn: VietMed-NER train, dòng 4565 (từ 0).

## VM600-597

**Đoạn gốc:** là chúng tôi hiểu hơn rằng là bác khó nắm chứ không phải là không nắm được đúng không ạ

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | khó nắm | Bệnh hoặc triệu chứng (CONDITION) | [34, 41) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- CONTEXT_OR_TRANSCRIPT: câu bị cắt, tham chiếu/mục đích chưa rõ hoặc nghi lỗi phiên âm; cần xem ngữ cảnh/audio gốc, không tự sửa văn bản.

### Thay đổi NER

- ∅ → E1 “khó nắm” CONDITION [34, 41)

Nguồn: VietMed-NER train, dòng 4583 (từ 0).

## VM600-598

**Đoạn gốc:** các chất dinh dưỡng để giúp cho chúng ta bớt đi những cái vấn đề như là về thay

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | chất dinh dưỡng | Thuốc/dược chất (DRUG) | [4, 19) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- ONTOLOGY_SCOPE: cần chốt phạm vi thuốc/dược chất so với mỹ phẩm, thực phẩm, hóa chất nội sinh hoặc hệ vi sinh; giữ ánh xạ nguồn khi chưa có quy ước đủ rõ.

Nguồn: VietMed-NER train, dòng 4593 (từ 0).

## VM600-599

**Đoạn gốc:** nó cũng là tâm tư của rất rất nhiều những người có tuổi và những người cao tuổi mà khi chúng ta bị các bệnh lý

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

Không có thực thể thuộc sáu loại được giữ trong bản rà soát.

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- GENERIC_MENTION: cần chốt có giữ bệnh/triệu chứng/biến chứng chung và tham chiếu không định danh trong NER hay không.

### Thay đổi NER

- E1 “rất nhiều” DOSAGE [26, 35) → ∅

Nguồn: VietMed-NER train, dòng 4594 (từ 0).

## VM600-600

**Đoạn gốc:** và từ đó nó cũng phòng ngừa được các cái biến chứng như là các cái nhồi máu cơ tim hay là những cái kiểu những cái nhồi

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E2 | biến chứng | Bệnh hoặc triệu chứng (CONDITION) | [41, 51) |
| E3 | nhồi máu cơ tim | Bệnh hoặc triệu chứng (CONDITION) | [67, 82) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- GENERIC_MENTION: cần chốt có giữ bệnh/triệu chứng/biến chứng chung và tham chiếu không định danh trong NER hay không.

### Thay đổi NER

- E1 “phòng ngừa” DRUG [17, 27) → ∅

Nguồn: VietMed-NER train, dòng 4597 (từ 0).

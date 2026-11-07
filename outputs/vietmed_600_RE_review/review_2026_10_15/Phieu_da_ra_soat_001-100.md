# Phiếu rà soát NER và RE 001 đến 100

Bản AI rà soát lần hai ngày 15/10/2026. Giữ nguyên câu nguồn và sáu loại NER, năm quan hệ RE. Chưa được chuyên gia xác nhận.

Quy tắc người dùng đã chốt: giữ cả cụm bệnh/triệu chứng trong một CONDITION. Không tách bộ phận bên trong cụm để tạo located_at. Vị trí được nêu riêng bằng giới từ hoặc mệnh đề riêng vẫn được xét.

Vị trí ký tự là khoảng [start, end), đếm từ 0 theo Unicode. Mã E ổn định khi sửa; mã R được tạo lại. Không dùng CHUA_RO làm nhãn huấn luyện hoặc nhãn âm.

## VM600-001

**Đoạn gốc:** thì cũng giống như ba má mình đã từng bị béo phì rồi bị bệnh này bệnh kia những người thân quen của mình mình biết bị

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | béo phì | Bệnh hoặc triệu chứng (CONDITION) | [41, 48) |
| E2 | bệnh | Bệnh hoặc triệu chứng (CONDITION) | [56, 60) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- GENERIC_MENTION: cần chốt có giữ bệnh/triệu chứng/biến chứng chung và tham chiếu không định danh trong NER hay không.

### Thay đổi NER

- E2 “bị bệnh” CONDITION [53, 60) → E2 “bệnh” CONDITION [56, 60)

Nguồn: VietMed-NER train, dòng 0 (từ 0).

## VM600-002

**Đoạn gốc:** gọi là những cái bụi mịn từ ngoài môi trường xâm nhập vào trong da và cho chúng ta sẽ xảy ra những cái phản ứng

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E2 | da | Bộ phận cơ thể (BODY_PART) | [64, 66) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Thay đổi NER

- E1 “bụi mịn” DRUG [17, 24) → ∅

Nguồn: VietMed-NER train, dòng 24 (từ 0).

## VM600-003

**Đoạn gốc:** tẩy trắng và dưỡng sáng vẫn chưa được phân biệt rõ ràng vào mọi người hay nhầm lẫn hay tưởng là chung với ạ nên là

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | tẩy trắng | Thủ thuật hoặc điều trị (PROCEDURE) | [0, 9) |
| E2 | dưỡng sáng | Thủ thuật hoặc điều trị (PROCEDURE) | [13, 23) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- ONTOLOGY_SCOPE: cần chốt phạm vi thuốc/dược chất so với mỹ phẩm, thực phẩm, hóa chất nội sinh hoặc hệ vi sinh; giữ ánh xạ nguồn khi chưa có quy ước đủ rõ.

### Thay đổi NER

- ∅ → E1 “tẩy trắng” PROCEDURE [0, 9)
- ∅ → E2 “dưỡng sáng” PROCEDURE [13, 23)

Nguồn: VietMed-NER train, dòng 33 (từ 0).

## VM600-004

**Đoạn gốc:** thể gặp ngay cái thời gian người ta gọi là tiểu phẫu tức là trong những cái ngày đầu tiên của cuộc mổ nếu mà sau đó mà nó

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | tiểu phẫu | Thủ thuật hoặc điều trị (PROCEDURE) | [43, 52) |
| E2 | mổ | Thủ thuật hoặc điều trị (PROCEDURE) | [99, 101) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

Nguồn: VietMed-NER train, dòng 38 (từ 0).

## VM600-005

**Đoạn gốc:** nhịp tim nhanh này các cái rối loạn nhịp tim này đấy là những cái dấu hiệu hoặc là đau tức ngực thế còn nếu mà những cái

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | nhịp tim nhanh | Bệnh hoặc triệu chứng (CONDITION) | [0, 14) |
| E2 | rối loạn nhịp tim | Bệnh hoặc triệu chứng (CONDITION) | [27, 44) |
| E3 | đau tức ngực | Bệnh hoặc triệu chứng (CONDITION) | [83, 95) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

Nguồn: VietMed-NER train, dòng 40 (từ 0).

## VM600-006

**Đoạn gốc:** ta đã từng gặp trong trong lịch sử vì thế nên là cúm a thì là một bệnh lý và

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | cúm a | Bệnh hoặc triệu chứng (CONDITION) | [49, 54) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

Nguồn: VietMed-NER train, dòng 54 (từ 0).

## VM600-007

**Đoạn gốc:** là sau khi mà điều trị ung thư thì rõ ràng được bây giờ chúng ta trở về cuộc

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | điều trị | Thủ thuật hoặc điều trị (PROCEDURE) | [14, 22) |
| E2 | ung thư | Bệnh hoặc triệu chứng (CONDITION) | [23, 30) |

### RE

| Mã | Cặp có hướng | Kết luận đề xuất |
|---|---|---|
| R1 | E2 “ung thư” → E1 “điều trị” | Được điều trị bằng phương pháp (treated_by_procedure) |

### Cần chốt

- GENERIC_INTERVENTION: cần chốt việc giữ hành động điều trị/chẩn đoán chung khi không nêu phương pháp cụ thể.

Nguồn: VietMed-NER train, dòng 69 (từ 0).

## VM600-008

**Đoạn gốc:** mảng xơ vữa ở trên các bệnh nhân bị tăng huyết áp ạ và từ đó nó giúp cho máu thông lên não lên tim được tốt hơn và

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | mảng xơ vữa | Bệnh hoặc triệu chứng (CONDITION) | [0, 11) |
| E2 | tăng huyết áp | Bệnh hoặc triệu chứng (CONDITION) | [36, 49) |
| E3 | máu | Bộ phận cơ thể (BODY_PART) | [73, 76) |
| E4 | não | Bộ phận cơ thể (BODY_PART) | [87, 90) |
| E5 | tim | Bộ phận cơ thể (BODY_PART) | [95, 98) |

### RE

| Mã | Cặp có hướng | Kết luận đề xuất |
|---|---|---|
| R1 | E1 “mảng xơ vữa” → E3 “máu” | Không có quan hệ thuộc 5 loại (NO_RELATION) |
| R2 | E1 “mảng xơ vữa” → E4 “não” | Không có quan hệ thuộc 5 loại (NO_RELATION) |
| R3 | E1 “mảng xơ vữa” → E5 “tim” | Không có quan hệ thuộc 5 loại (NO_RELATION) |
| R4 | E2 “tăng huyết áp” → E3 “máu” | Không có quan hệ thuộc 5 loại (NO_RELATION) |
| R5 | E2 “tăng huyết áp” → E4 “não” | Không có quan hệ thuộc 5 loại (NO_RELATION) |
| R6 | E2 “tăng huyết áp” → E5 “tim” | Không có quan hệ thuộc 5 loại (NO_RELATION) |

Nguồn: VietMed-NER train, dòng 76 (từ 0).

## VM600-009

**Đoạn gốc:** đối với cái bệnh lý của bác thì bác đang phải dùng rất nhiều những các cái thuốc nền các cái thuốc để điều trị các cái

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E2 | thuốc nền | Thuốc/dược chất (DRUG) | [75, 84) |
| E3 | thuốc | Thuốc/dược chất (DRUG) | [93, 98) |
| E4 | điều trị | Thủ thuật hoặc điều trị (PROCEDURE) | [102, 110) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- GENERIC_INTERVENTION: cần chốt việc giữ hành động điều trị/chẩn đoán chung khi không nêu phương pháp cụ thể.

### Thay đổi NER

- E1 “rất nhiều” DOSAGE [51, 60) → ∅
- E2 “thuốc” DRUG [75, 80) → E2 “thuốc nền” DRUG [75, 84)

Nguồn: VietMed-NER train, dòng 81 (từ 0).

## VM600-010

**Đoạn gốc:** ta càng cảm thấy được vai trò vô cùng quan trọng của chuyên khoa tâm lý trong điều trị người bệnh béo phì và tiếp theo

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | điều trị | Thủ thuật hoặc điều trị (PROCEDURE) | [78, 86) |
| E2 | béo phì | Bệnh hoặc triệu chứng (CONDITION) | [98, 105) |

### RE

| Mã | Cặp có hướng | Kết luận đề xuất |
|---|---|---|
| R1 | E2 “béo phì” → E1 “điều trị” | Được điều trị bằng phương pháp (treated_by_procedure) |

### Cần chốt

- GENERIC_INTERVENTION: cần chốt việc giữ hành động điều trị/chẩn đoán chung khi không nêu phương pháp cụ thể.

Nguồn: VietMed-NER train, dòng 92 (từ 0).

## VM600-011

**Đoạn gốc:** với cơ chế của cái hình thành cục máu đông ở trong tim giờ đó nên thuốc chống tiểu cầu không phải là cái gì

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | cục máu đông | Bệnh hoặc triệu chứng (CONDITION) | [30, 42) |
| E2 | tim | Bộ phận cơ thể (BODY_PART) | [51, 54) |
| E3 | thuốc chống tiểu cầu | Thuốc/dược chất (DRUG) | [66, 86) |

### RE

| Mã | Cặp có hướng | Kết luận đề xuất |
|---|---|---|
| R1 | E1 “cục máu đông” → E2 “tim” | Có vị trí ở (located_at) |
| R2 | E1 “cục máu đông” → E3 “thuốc chống tiểu cầu” | Chưa rõ — cần chốt (CHUA_RO) |

### Cần chốt

- UNRESOLVED_RE: còn cặp CHUA_RO; tuyệt đối không đổi thành NO_RELATION khi xuất huấn luyện.

Nguồn: VietMed-NER train, dòng 105 (từ 0).

## VM600-012

**Đoạn gốc:** cân nặng họ không dám nói về cái vẻ đẹp của một cái người nữ hay người nam là như thế nào vì lý do là họ sẽ dễ bị

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

Không có thực thể thuộc sáu loại được giữ trong bản rà soát.

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

Nguồn: VietMed-NER train, dòng 121 (từ 0).

## VM600-013

**Đoạn gốc:** từ thực vật ví dụ như là các bạn có thể nghe tới như là chiết xuất từ hoa lan được cam thảo này từ bạch quả lá dâu tầm

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E6 | chiết xuất từ hoa lan | Thuốc/dược chất (DRUG) | [56, 77) |
| E3 | cam thảo | Thuốc/dược chất (DRUG) | [83, 91) |
| E4 | bạch quả | Thuốc/dược chất (DRUG) | [99, 107) |
| E5 | lá dâu tầm | Thuốc/dược chất (DRUG) | [108, 118) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- ONTOLOGY_SCOPE: cần chốt phạm vi thuốc/dược chất so với mỹ phẩm, thực phẩm, hóa chất nội sinh hoặc hệ vi sinh; giữ ánh xạ nguồn khi chưa có quy ước đủ rõ.

### Thay đổi NER

- E1 “chiết xuất” PROCEDURE [56, 66) → ∅
- ∅ → E6 “chiết xuất từ hoa lan” DRUG [56, 77)
- E2 “hoa lan” DRUG [70, 77) → ∅

Nguồn: VietMed-NER train, dòng 132 (từ 0).

## VM600-014

**Đoạn gốc:** dựng một cái cái cái mục tiêu trị liệu cũng như một chương trình trị liệu dài hơi để giúp

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | trị liệu | Thủ thuật hoặc điều trị (PROCEDURE) | [30, 38) |
| E2 | trị liệu | Thủ thuật hoặc điều trị (PROCEDURE) | [65, 73) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- GENERIC_INTERVENTION: cần chốt việc giữ hành động điều trị/chẩn đoán chung khi không nêu phương pháp cụ thể.

Nguồn: VietMed-NER train, dòng 134 (từ 0).

## VM600-015

**Đoạn gốc:** vận động thì tình trạng béo phì nó tăng lên mà mình béo phì nó tăng lên rồi thì gặp tình trạng kỳ thị nữa hay là gặp

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | béo phì | Bệnh hoặc triệu chứng (CONDITION) | [24, 31) |
| E2 | béo phì | Bệnh hoặc triệu chứng (CONDITION) | [52, 59) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

Nguồn: VietMed-NER train, dòng 137 (từ 0).

## VM600-016

**Đoạn gốc:** khi mà chúng ta khỏe mạnh như thế này mà chúng ta gặp một cái vấn đề gì đấy về mặt tinh thần thì chúng ta cũng đã rất là chán ăn rồi và hiện nay thì có một số

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | chán ăn | Bệnh hoặc triệu chứng (CONDITION) | [121, 128) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

Nguồn: VietMed-NER train, dòng 149 (từ 0).

## VM600-017

**Đoạn gốc:** theo cái tình trạng bệnh lý của chúng ta ví dụ đái tháo đường hay là rối loạn lipid máu thì chúng ta phải kiêng những cái gì và ăn

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | đái tháo đường | Bệnh hoặc triệu chứng (CONDITION) | [47, 61) |
| E2 | rối loạn lipid máu | Bệnh hoặc triệu chứng (CONDITION) | [69, 87) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

Nguồn: VietMed-NER train, dòng 152 (từ 0).

## VM600-018

**Đoạn gốc:** con đường để mà làm giảm sản sinh những cái tín hiệu đến tế bào sắc tố ví dụ như lại những cái hoạt chất thoa có chút

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | tế bào sắc tố | Bộ phận cơ thể (BODY_PART) | [57, 70) |
| E2 | hoạt chất | Thuốc/dược chất (DRUG) | [95, 104) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- SCOPE_CONFIRMATION: cần xác nhận quy ước về thuốc/dược chất, can thiệp không dùng thuốc, thiết bị, tác nhân hoặc hoạt động thăm khám; không coi ánh xạ nguồn là xác nhận chuyên gia.

Nguồn: VietMed-NER train, dòng 153 (từ 0).

## VM600-019

**Đoạn gốc:** ta biết là cái suy giãn tĩnh mạch nó cũng liên quan đến quá trình lão hóa liên quan quá trình thoái hóa các cái mạch

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | suy giãn tĩnh mạch | Bệnh hoặc triệu chứng (CONDITION) | [15, 33) |
| E3 | thoái hóa | Bệnh hoặc triệu chứng (CONDITION) | [94, 103) |
| E4 | mạch | Bộ phận cơ thể (BODY_PART) | [112, 116) |

### RE

| Mã | Cặp có hướng | Kết luận đề xuất |
|---|---|---|
| R1 | E1 “suy giãn tĩnh mạch” → E4 “mạch” | Không có quan hệ thuộc 5 loại (NO_RELATION) |
| R2 | E3 “thoái hóa” → E4 “mạch” | Có vị trí ở (located_at) |

### Thay đổi NER

- E2 “quá trình lão hóa” TEST [56, 73) → ∅

Nguồn: VietMed-NER train, dòng 161 (từ 0).

## VM600-020

**Đoạn gốc:** vấn đề sức khỏe khó khăn nhất của chúng ta mặc dù dự án đang nghiên cứu một số bộ phận của cơ thể chứa vi khuẩn bao gồm

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E2 | cơ thể | Bộ phận cơ thể (BODY_PART) | [91, 97) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Thay đổi NER

- E1 “nghiên cứu” TEST [61, 71) → ∅
- E3 “vi khuẩn” CONDITION [103, 111) → ∅

Nguồn: VietMed-NER train, dòng 186 (từ 0).

## VM600-021

**Đoạn gốc:** những người mà có bị béo phì rồi đó thì họ có nhiều

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | béo phì | Bệnh hoặc triệu chứng (CONDITION) | [21, 28) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

Nguồn: VietMed-NER train, dòng 193 (từ 0).

## VM600-022

**Đoạn gốc:** nên phổ biến trong nhiều sản phẩm thực phẩm và có thể được tìm thấy trong các cửa hàng tạp hóa thông thường biết cách

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

Không có thực thể thuộc sáu loại được giữ trong bản rà soát.

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

Nguồn: VietMed-NER train, dòng 227 (từ 0).

## VM600-023

**Đoạn gốc:** quý vị thân mến chúng ta vừa được lắng nghe cuộc trò chuyện với chủ đề dinh

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

Không có thực thể thuộc sáu loại được giữ trong bản rà soát.

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

Nguồn: VietMed-NER train, dòng 230 (từ 0).

## VM600-024

**Đoạn gốc:** sức đề kháng và kéo dài tuổi thọ đó là mong muốn có rất là nhiều người đặc biệt là đối với những khán giả cao tuổi như

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

Không có thực thể thuộc sáu loại được giữ trong bản rà soát.

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Thay đổi NER

- E1 “sức đề kháng” TEST [0, 12) → ∅
- E2 “kéo dài tuổi thọ” DRUG [16, 32) → ∅

Nguồn: VietMed-NER train, dòng 234 (từ 0).

## VM600-025

**Đoạn gốc:** cái căn nguyên cơ chế bệnh sinh của mình đó chính là những cái mảng xơ vữa bác ạ và rất tốt ở trên những người bị rối

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | mảng xơ vữa | Bệnh hoặc triệu chứng (CONDITION) | [63, 74) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

Nguồn: VietMed-NER train, dòng 236 (từ 0).

## VM600-026

**Đoạn gốc:** hiểu biết của chúng ta về miễn dịch vấn đề liên quan đến vắcxin và cách chúng hoạt động nguyên tắc cơ bản của việc

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | vắcxin | Thuốc/dược chất (DRUG) | [57, 63) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- SCOPE_CONFIRMATION: cần xác nhận quy ước về thuốc/dược chất, can thiệp không dùng thuốc, thiết bị, tác nhân hoặc hoạt động thăm khám; không coi ánh xạ nguồn là xác nhận chuyên gia.

Nguồn: VietMed-NER train, dòng 237 (từ 0).

## VM600-027

**Đoạn gốc:** coi một cái người ung thư trong thành viên trong gia đình là một sự sầu não trong cả một gia đình thì rất khó có thể

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | ung thư | Bệnh hoặc triệu chứng (CONDITION) | [18, 25) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Thay đổi NER

- E2 “não” BODY_PART [72, 75) → ∅

Nguồn: VietMed-NER train, dòng 243 (từ 0).

## VM600-028

**Đoạn gốc:** gáy nó mới đau nó chèn lên thần kinh tê liệt tay thế uống thuốc nó đỡ làm nhiều lúc mà rét

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | gáy | Bộ phận cơ thể (BODY_PART) | [0, 3) |
| E2 | đau | Bệnh hoặc triệu chứng (CONDITION) | [11, 14) |
| E3 | thần kinh | Bộ phận cơ thể (BODY_PART) | [27, 36) |
| E4 | tê liệt tay | Bệnh hoặc triệu chứng (CONDITION) | [37, 48) |
| E5 | thuốc | Thuốc/dược chất (DRUG) | [58, 63) |

### RE

| Mã | Cặp có hướng | Kết luận đề xuất |
|---|---|---|
| R1 | E2 “đau” → E1 “gáy” | Có vị trí ở (located_at) |
| R2 | E2 “đau” → E3 “thần kinh” | Không có quan hệ thuộc 5 loại (NO_RELATION) |
| R3 | E2 “đau” → E5 “thuốc” | Chưa rõ — cần chốt (CHUA_RO) |
| R4 | E4 “tê liệt tay” → E1 “gáy” | Không có quan hệ thuộc 5 loại (NO_RELATION) |
| R5 | E4 “tê liệt tay” → E3 “thần kinh” | Không có quan hệ thuộc 5 loại (NO_RELATION) |
| R6 | E4 “tê liệt tay” → E5 “thuốc” | Chưa rõ — cần chốt (CHUA_RO) |

### Cần chốt

- CONTEXT_OR_TRANSCRIPT: câu bị cắt, tham chiếu/mục đích chưa rõ hoặc nghi lỗi phiên âm; cần xem ngữ cảnh/audio gốc, không tự sửa văn bản.
- UNRESOLVED_RE: còn cặp CHUA_RO; tuyệt đối không đổi thành NO_RELATION khi xuất huấn luyện.

### Thay đổi NER

- E5 “uống thuốc” PROCEDURE [53, 63) → E5 “thuốc” DRUG [58, 63)

Nguồn: VietMed-NER train, dòng 254 (từ 0).

## VM600-029

**Đoạn gốc:** thì nhiều chi bộ có thể chia sẻ chúng ta trước không ạ cúm a thì nó là một bệnh

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | cúm a | Bệnh hoặc triệu chứng (CONDITION) | [55, 60) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

Nguồn: VietMed-NER train, dòng 259 (từ 0).

## VM600-030

**Đoạn gốc:** nó gây ra thiếu máu não nếu nó không lại được ngay đây là tự cơ thể có cái

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | thiếu máu não | Bệnh hoặc triệu chứng (CONDITION) | [10, 23) |
| E2 | cơ thể | Bộ phận cơ thể (BODY_PART) | [61, 67) |

### RE

| Mã | Cặp có hướng | Kết luận đề xuất |
|---|---|---|
| R1 | E1 “thiếu máu não” → E2 “cơ thể” | Không có quan hệ thuộc 5 loại (NO_RELATION) |

Nguồn: VietMed-NER train, dòng 282 (từ 0).

## VM600-031

**Đoạn gốc:** những cái lo lắng từ phía người dân và tự người dân cảm thấy rằng cần phải đi xét nghiệm sarscov2 làm cho cái mật

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | xét nghiệm sarscov2 | Xét nghiệm hoặc thăm khám (TEST) | [78, 97) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Thay đổi NER

- E1 “xét nghiệm” TEST [78, 88) → E1 “xét nghiệm sarscov2” TEST [78, 97)
- E2 “sarscov2” CONDITION [89, 97) → ∅
- E3 “mật” BODY_PART [110, 113) → ∅

Nguồn: VietMed-NER train, dòng 286 (từ 0).

## VM600-032

**Đoạn gốc:** nên có thể nói rằng là từ xa xưa đông trùng hạ thảo đó là một thứ mà để đặc hữu cho những cái bậc quyền quý nhưng ngày

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | đông trùng hạ thảo | Thuốc/dược chất (DRUG) | [33, 51) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- ONTOLOGY_SCOPE: cần chốt phạm vi thuốc/dược chất so với mỹ phẩm, thực phẩm, hóa chất nội sinh hoặc hệ vi sinh; giữ ánh xạ nguồn khi chưa có quy ước đủ rõ.

Nguồn: VietMed-NER train, dòng 293 (từ 0).

## VM600-033

**Đoạn gốc:** giờ thì chúng ta sẽ dành ít phút để nghe tâm sự của người trong cuộc như thế nào nhé cũng gần một nửa năm trở lại đây thì

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

Không có thực thể thuộc sáu loại được giữ trong bản rà soát.

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

Nguồn: VietMed-NER train, dòng 295 (từ 0).

## VM600-034

**Đoạn gốc:** mặn quá hoặc là đắng quá hoặc là cảm thấy chua quá không thể mà ăn được không thể chấp nhận được món ăn đi qua

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

Không có thực thể thuộc sáu loại được giữ trong bản rà soát.

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

Nguồn: VietMed-NER train, dòng 308 (từ 0).

## VM600-035

**Đoạn gốc:** pháp điều trị thuốc thì phẫu thuật kích thích não sâu nó sẽ giúp cải thiện triệu chứng cho người bệnh khá là tốt mà khi

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | điều trị | Thủ thuật hoặc điều trị (PROCEDURE) | [5, 13) |
| E2 | thuốc | Thuốc/dược chất (DRUG) | [14, 19) |
| E3 | phẫu thuật kích thích não sâu | Thủ thuật hoặc điều trị (PROCEDURE) | [24, 53) |
| E5 | triệu chứng | Bệnh hoặc triệu chứng (CONDITION) | [75, 86) |

### RE

| Mã | Cặp có hướng | Kết luận đề xuất |
|---|---|---|
| R1 | E5 “triệu chứng” → E1 “điều trị” | Không có quan hệ thuộc 5 loại (NO_RELATION) |
| R2 | E5 “triệu chứng” → E2 “thuốc” | Không có quan hệ thuộc 5 loại (NO_RELATION) |
| R3 | E5 “triệu chứng” → E3 “phẫu thuật kích thích não sâu” | Được điều trị bằng phương pháp (treated_by_procedure) |

### Cần chốt

- GENERIC_INTERVENTION: cần chốt việc giữ hành động điều trị/chẩn đoán chung khi không nêu phương pháp cụ thể.
- GENERIC_MENTION: cần chốt có giữ bệnh/triệu chứng/biến chứng chung và tham chiếu không định danh trong NER hay không.

### Thay đổi NER

- E4 “cải thiện” PROCEDURE [65, 74) → ∅

Nguồn: VietMed-NER train, dòng 314 (từ 0).

## VM600-036

**Đoạn gốc:** và cái vấn đề cuối cùng là thuốc mà người bệnh người bệnh vẫn nên uống thuốc

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | thuốc | Thuốc/dược chất (DRUG) | [27, 32) |
| E2 | thuốc | Thuốc/dược chất (DRUG) | [71, 76) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Thay đổi NER

- E2 “uống thuốc” PROCEDURE [66, 76) → E2 “thuốc” DRUG [71, 76)

Nguồn: VietMed-NER train, dòng 317 (từ 0).

## VM600-037

**Đoạn gốc:** động của máy kích thích não sâu của mình cũng có thể thay đổi một vài thông số liên quan tới hoạt động kích thích não

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | máy kích thích não sâu | Thủ thuật hoặc điều trị (PROCEDURE) | [9, 31) |
| E3 | kích thích não | Thủ thuật hoặc điều trị (PROCEDURE) | [103, 117) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- CONTEXT_OR_TRANSCRIPT: câu bị cắt, tham chiếu/mục đích chưa rõ hoặc nghi lỗi phiên âm; cần xem ngữ cảnh/audio gốc, không tự sửa văn bản.

### Thay đổi NER

- E2 “một vài thông số” DOSAGE [62, 78) → ∅
- E3 “não” BODY_PART [114, 117) → E3 “kích thích não” PROCEDURE [103, 117)

Nguồn: VietMed-NER train, dòng 320 (từ 0).

## VM600-038

**Đoạn gốc:** vẫn theo cái quy trình mà bác chỉ cho em là trước khi nhuộm là vẫn làm nhận gội

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

Không có thực thể thuộc sáu loại được giữ trong bản rà soát.

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

Nguồn: VietMed-NER train, dòng 326 (từ 0).

## VM600-039

**Đoạn gốc:** dại trong cơ thể mà nó cắn nó cắn

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E2 | dại | Bệnh hoặc triệu chứng (CONDITION) | [0, 3) |
| E1 | cơ thể | Bộ phận cơ thể (BODY_PART) | [10, 16) |

### RE

| Mã | Cặp có hướng | Kết luận đề xuất |
|---|---|---|
| R1 | E2 “dại” → E1 “cơ thể” | Không có quan hệ thuộc 5 loại (NO_RELATION) |

### Cần chốt

- CONTEXT_OR_TRANSCRIPT: câu bị cắt, tham chiếu/mục đích chưa rõ hoặc nghi lỗi phiên âm; cần xem ngữ cảnh/audio gốc, không tự sửa văn bản.

### Thay đổi NER

- ∅ → E2 “dại” CONDITION [0, 3)

Nguồn: VietMed-NER train, dòng 337 (từ 0).

## VM600-040

**Đoạn gốc:** làm giảm cái nguy cơ các cái mảng xơ vữa động mạch mà cái mảng xơ vữa động mạch của chị nó đang có và từ đó nó giúp cho

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | mảng xơ vữa động mạch | Bệnh hoặc triệu chứng (CONDITION) | [29, 50) |
| E2 | mảng xơ vữa động mạch | Bệnh hoặc triệu chứng (CONDITION) | [58, 79) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

Nguồn: VietMed-NER train, dòng 343 (từ 0).

## VM600-041

**Đoạn gốc:** là nó có cái tác dụng là ức chế cái việc hình thành và các cái cục máu đông do đó

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E2 | cục máu đông | Bệnh hoặc triệu chứng (CONDITION) | [63, 75) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Thay đổi NER

- E1 “ức chế” DRUG [25, 31) → ∅

Nguồn: VietMed-NER train, dòng 346 (từ 0).

## VM600-042

**Đoạn gốc:** chống mệt mỏi và thanh trừng gốc tự do và kéo dài tuổi thọ cho

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | mệt mỏi | Bệnh hoặc triệu chứng (CONDITION) | [6, 13) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Thay đổi NER

- E2 “kéo dài tuổi thọ” DRUG [42, 58) → ∅

Nguồn: VietMed-NER train, dòng 360 (từ 0).

## VM600-043

**Đoạn gốc:** ăn uống dinh dưỡng đầy đủ thì tôi nghĩ rằng là cái khả năng lây lan từ những

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

Không có thực thể thuộc sáu loại được giữ trong bản rà soát.

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Thay đổi NER

- E1 “lây lan” CONDITION [60, 67) → ∅

Nguồn: VietMed-NER train, dòng 375 (từ 0).

## VM600-044

**Đoạn gốc:** trong chương tiếp theo nhưng bây giờ hãy hiểu rằng tất cả các loại bệnh đều bắt

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

Không có thực thể thuộc sáu loại được giữ trong bản rà soát.

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

Nguồn: VietMed-NER train, dòng 380 (từ 0).

## VM600-045

**Đoạn gốc:** quá trình viêm và dẫn đến những tình trạng xơ vữa mạch hay là tình trạng là cái thành mạch của chúng ta nó bị xơ

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | viêm | Bệnh hoặc triệu chứng (CONDITION) | [10, 14) |
| E2 | xơ vữa mạch | Bệnh hoặc triệu chứng (CONDITION) | [43, 54) |
| E3 | thành mạch | Bộ phận cơ thể (BODY_PART) | [80, 90) |

### RE

| Mã | Cặp có hướng | Kết luận đề xuất |
|---|---|---|
| R1 | E1 “viêm” → E3 “thành mạch” | Không có quan hệ thuộc 5 loại (NO_RELATION) |
| R2 | E2 “xơ vữa mạch” → E3 “thành mạch” | Không có quan hệ thuộc 5 loại (NO_RELATION) |

### Cần chốt

- CONTEXT_OR_TRANSCRIPT: câu bị cắt, tham chiếu/mục đích chưa rõ hoặc nghi lỗi phiên âm; cần xem ngữ cảnh/audio gốc, không tự sửa văn bản.

### Thay đổi NER

- E2 “tình trạng xơ vữa mạch” CONDITION [32, 54) → E2 “xơ vữa mạch” CONDITION [43, 54)
- E3 “mạch” BODY_PART [86, 90) → E3 “thành mạch” BODY_PART [80, 90)

Nguồn: VietMed-NER train, dòng 383 (từ 0).

## VM600-046

**Đoạn gốc:** thì đương nhiên là cái người lớn tuổi thì có nguy cơ bệnh đều cao và đối với rung nhĩ thì là có rung nhĩ cộng với

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E2 | rung nhĩ | Bệnh hoặc triệu chứng (CONDITION) | [77, 85) |
| E3 | rung nhĩ | Bệnh hoặc triệu chứng (CONDITION) | [96, 104) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Thay đổi NER

- E1 “cao” DOSAGE [62, 65) → ∅

Nguồn: VietMed-NER train, dòng 395 (từ 0).

## VM600-047

**Đoạn gốc:** người ta thích ăn đi thì có khi là nó sẽ ảnh hưởng lại tốt hơn làm cho cái cân nặng nó có thể giảm hơn là thì cái đó là

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

Không có thực thể thuộc sáu loại được giữ trong bản rà soát.

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

Nguồn: VietMed-NER train, dòng 396 (từ 0).

## VM600-048

**Đoạn gốc:** hỗ trợ trong việc tăng cường sức khỏe của tim mạch và đan sâm nó cũng có cái tác dụng là ức chế làm giảm cái sự hình

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E2 | tim mạch | Bộ phận cơ thể (BODY_PART) | [42, 50) |
| E3 | đan sâm | Thuốc/dược chất (DRUG) | [54, 61) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Thay đổi NER

- E1 “hỗ trợ” PROCEDURE [0, 6) → ∅
- E4 “ức chế” DRUG [89, 95) → ∅

Nguồn: VietMed-NER train, dòng 405 (từ 0).

## VM600-049

**Đoạn gốc:** cái phác đồ một cách điều trị một cách phù hợp tránh cái tình trạng là mình lại tiếp tục loay hoay như thế này và đôi

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | phác đồ | Thủ thuật hoặc điều trị (PROCEDURE) | [4, 11) |
| E2 | điều trị | Thủ thuật hoặc điều trị (PROCEDURE) | [21, 29) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- GENERIC_INTERVENTION: cần chốt việc giữ hành động điều trị/chẩn đoán chung khi không nêu phương pháp cụ thể.
- GENERIC_MENTION: cần chốt có giữ bệnh/triệu chứng/biến chứng chung và tham chiếu không định danh trong NER hay không.

Nguồn: VietMed-NER train, dòng 406 (từ 0).

## VM600-050

**Đoạn gốc:** uống thuốc vào có thể hôm nay nó hấp thu tốt mai nó sẽ tăng lên ngày mai mình ăn uống

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | thuốc | Thuốc/dược chất (DRUG) | [5, 10) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Thay đổi NER

- E2 “hấp thu” TEST [33, 40) → ∅
- E1 “uống thuốc” PROCEDURE [0, 10) → E1 “thuốc” DRUG [5, 10)

Nguồn: VietMed-NER train, dòng 413 (từ 0).

## VM600-051

**Đoạn gốc:** mặt xong làm cho chúng ta cảm thấy nó khô căng là những cái sữa rửa mặt nó thường có chứa những thành phần các chất

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | khô căng | Bệnh hoặc triệu chứng (CONDITION) | [38, 46) |
| E2 | sữa rửa mặt | Thuốc/dược chất (DRUG) | [60, 71) |

### RE

| Mã | Cặp có hướng | Kết luận đề xuất |
|---|---|---|
| R1 | E1 “khô căng” → E2 “sữa rửa mặt” | Không có quan hệ thuộc 5 loại (NO_RELATION) |

### Cần chốt

- ONTOLOGY_SCOPE: cần chốt phạm vi thuốc/dược chất so với mỹ phẩm, thực phẩm, hóa chất nội sinh hoặc hệ vi sinh; giữ ánh xạ nguồn khi chưa có quy ước đủ rõ.

Nguồn: VietMed-NER train, dòng 416 (từ 0).

## VM600-052

**Đoạn gốc:** dùng cảm thấy triệu chứng đau nhức xương khớp giảm nhanh sau từ một đến hai tuần sử dụng tình trạng đau lưng đau vai gáy đau

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E2 | đau nhức xương khớp | Bệnh hoặc triệu chứng (CONDITION) | [26, 45) |
| E4 | đau lưng | Bệnh hoặc triệu chứng (CONDITION) | [100, 108) |
| E5 | đau vai gáy | Bệnh hoặc triệu chứng (CONDITION) | [109, 120) |
| E8 | đau | Bệnh hoặc triệu chứng (CONDITION) | [121, 124) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- CONTEXT_OR_TRANSCRIPT: câu bị cắt, tham chiếu/mục đích chưa rõ hoặc nghi lỗi phiên âm; cần xem ngữ cảnh/audio gốc, không tự sửa văn bản.

### Thay đổi NER

- E1 “triệu chứng” CONDITION [14, 25) → ∅
- E6 “vai” BODY_PART [113, 116) → E6 “vai gáy” BODY_PART [113, 120)
- E7 “gáy” BODY_PART [117, 120) → ∅
- E2 “đau nhức” CONDITION [26, 34) → E2 “đau nhức xương khớp” CONDITION [26, 45)
- E3 “xương khớp” BODY_PART [35, 45) → ∅
- E5 “đau” CONDITION [109, 112) → E5 “đau vai gáy” CONDITION [109, 120)
- E6 “vai gáy” BODY_PART [113, 120) → ∅

Nguồn: VietMed-NER train, dòng 420 (từ 0).

## VM600-053

**Đoạn gốc:** có thể không thích thì chúng ta có thể hoặc có thể thay đổi bữa thì chúng ta có thể sử dụng các cái bữa ăn cao năng

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

Không có thực thể thuộc sáu loại được giữ trong bản rà soát.

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Thay đổi NER

- E1 “cao” DOSAGE [107, 110) → ∅

Nguồn: VietMed-NER train, dòng 426 (từ 0).

## VM600-054

**Đoạn gốc:** chỉ có còn hỏi gì thêm không à vâng ạ từ đầu chương trình tới giờ thì tôi thấy là rất là nhiều các khán giả đều có chung

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

Không có thực thể thuộc sáu loại được giữ trong bản rà soát.

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

Nguồn: VietMed-NER train, dòng 435 (từ 0).

## VM600-055

**Đoạn gốc:** càng ngày họ lo lo nhiều thậm chí họ có thể đưa đến cái trầm cảm mà khi họ

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | trầm cảm | Bệnh hoặc triệu chứng (CONDITION) | [56, 64) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

Nguồn: VietMed-NER train, dòng 446 (từ 0).

## VM600-056

**Đoạn gốc:** quan trọng đối với sự phát triển của một hệ vi sinh khỏe mạnh cũng như những yếu tố có thể phá hủy nó bạn sẽ sớm bắt đầu

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | hệ vi sinh | Bộ phận cơ thể (BODY_PART) | [41, 51) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- ONTOLOGY_SCOPE: cần chốt phạm vi thuốc/dược chất so với mỹ phẩm, thực phẩm, hóa chất nội sinh hoặc hệ vi sinh; giữ ánh xạ nguồn khi chưa có quy ước đủ rõ.

Nguồn: VietMed-NER train, dòng 449 (từ 0).

## VM600-057

**Đoạn gốc:** quá thì khả năng phẫu thuật nó sẽ khó khăn nó có sẽ có nhiều biến chứng cái thứ hai người bệnh parkinson nên là hơn

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | phẫu thuật | Thủ thuật hoặc điều trị (PROCEDURE) | [17, 27) |
| E2 | biến chứng | Bệnh hoặc triệu chứng (CONDITION) | [61, 71) |
| E4 | parkinson | Bệnh hoặc triệu chứng (CONDITION) | [95, 104) |

### RE

| Mã | Cặp có hướng | Kết luận đề xuất |
|---|---|---|
| R1 | E2 “biến chứng” → E1 “phẫu thuật” | Không có quan hệ thuộc 5 loại (NO_RELATION) |
| R2 | E4 “parkinson” → E1 “phẫu thuật” | Chưa rõ — cần chốt (CHUA_RO) |

### Cần chốt

- CONTEXT_OR_TRANSCRIPT: câu bị cắt, tham chiếu/mục đích chưa rõ hoặc nghi lỗi phiên âm; cần xem ngữ cảnh/audio gốc, không tự sửa văn bản.
- UNRESOLVED_RE: còn cặp CHUA_RO; tuyệt đối không đổi thành NO_RELATION khi xuất huấn luyện.

### Thay đổi NER

- E3 “cái thứ hai” DOSAGE [72, 83) → ∅

Nguồn: VietMed-NER train, dòng 464 (từ 0).

## VM600-058

**Đoạn gốc:** gánh hết đó là cảm thấy buồn mà tuyệt vọng nữa hàng triệu việt nam đang phải

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

Không có thực thể thuộc sáu loại được giữ trong bản rà soát.

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

Nguồn: VietMed-NER train, dòng 466 (từ 0).

## VM600-059

**Đoạn gốc:** cho tất cả quý vị khán giả biết thêm về lợi ích mà người bệnh nhận được khi thực hiện giảm cân một cách hiệu quả và an

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

Không có thực thể thuộc sáu loại được giữ trong bản rà soát.

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- SCOPE_CONFIRMATION: cần xác nhận quy ước về thuốc/dược chất, can thiệp không dùng thuốc, thiết bị, tác nhân hoặc hoạt động thăm khám; không coi ánh xạ nguồn là xác nhận chuyên gia.

Nguồn: VietMed-NER train, dòng 468 (từ 0).

## VM600-060

**Đoạn gốc:** tùm lum tà la hết cái mà khó điều trị và lúc đó thì có tốt thì với khi mà chúng ta có một cái chế độ ăn

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | điều trị | Thủ thuật hoặc điều trị (PROCEDURE) | [29, 37) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- GENERIC_INTERVENTION: cần chốt việc giữ hành động điều trị/chẩn đoán chung khi không nêu phương pháp cụ thể.

Nguồn: VietMed-NER train, dòng 496 (từ 0).

## VM600-061

**Đoạn gốc:** người bệnh để có cái cái cái cái sự hiểu biết hơn trong các nhận thức thay đổi cho nó tốt hơn để có thể cải thiện chất

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

Không có thực thể thuộc sáu loại được giữ trong bản rà soát.

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Thay đổi NER

- E1 “cải thiện” PROCEDURE [104, 113) → ∅

Nguồn: VietMed-NER train, dòng 504 (từ 0).

## VM600-062

**Đoạn gốc:** dụng và nó phối hợp với nhau là mang lại hiệu quả rất là tốt chị nhé thì chị nên

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

Không có thực thể thuộc sáu loại được giữ trong bản rà soát.

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

Nguồn: VietMed-NER train, dòng 514 (từ 0).

## VM600-063

**Đoạn gốc:** những cái hậu quả những cái di chứng của bệnh lý này bởi vậy bên cạnh cái việc mà

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | di chứng | Bệnh hoặc triệu chứng (CONDITION) | [28, 36) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- GENERIC_MENTION: cần chốt có giữ bệnh/triệu chứng/biến chứng chung và tham chiếu không định danh trong NER hay không.

Nguồn: VietMed-NER train, dòng 524 (từ 0).

## VM600-064

**Đoạn gốc:** với sự căng thẳng qua các tác động của hệ vi khuẩn lên hệ nội tiết hormone hỗ

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | căng thẳng | Bệnh hoặc triệu chứng (CONDITION) | [7, 17) |
| E3 | hệ nội tiết | Bộ phận cơ thể (BODY_PART) | [55, 66) |
| E4 | hormone | Thuốc/dược chất (DRUG) | [67, 74) |

### RE

| Mã | Cặp có hướng | Kết luận đề xuất |
|---|---|---|
| R1 | E1 “căng thẳng” → E3 “hệ nội tiết” | Không có quan hệ thuộc 5 loại (NO_RELATION) |
| R2 | E1 “căng thẳng” → E4 “hormone” | Không có quan hệ thuộc 5 loại (NO_RELATION) |

### Cần chốt

- SYMPTOM_SCOPE: cần phân biệt cảm xúc thông thường với triệu chứng lâm sàng theo quy ước dự án.

### Thay đổi NER

- E2 “vi khuẩn” CONDITION [42, 50) → ∅
- E3 “nội tiết” BODY_PART [58, 66) → E3 “hệ nội tiết” BODY_PART [55, 66)

Nguồn: VietMed-NER train, dòng 535 (từ 0).

## VM600-065

**Đoạn gốc:** dứt da của mình nó căng da đôi khi một số loại sữa rửa mặt nó khiến cho mình cảm giác là khi mình rửa xong cái da

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | da | Bộ phận cơ thể (BODY_PART) | [4, 6) |
| E5 | căng | Bệnh hoặc triệu chứng (CONDITION) | [19, 23) |
| E2 | da | Bộ phận cơ thể (BODY_PART) | [24, 26) |
| E3 | sữa rửa mặt | Thuốc/dược chất (DRUG) | [47, 58) |
| E4 | da | Bộ phận cơ thể (BODY_PART) | [111, 113) |

### RE

| Mã | Cặp có hướng | Kết luận đề xuất |
|---|---|---|
| R1 | E5 “căng” → E1 “da” | Không có quan hệ thuộc 5 loại (NO_RELATION) |
| R2 | E5 “căng” → E2 “da” | Không có quan hệ thuộc 5 loại (NO_RELATION) |
| R3 | E5 “căng” → E3 “sữa rửa mặt” | Không có quan hệ thuộc 5 loại (NO_RELATION) |
| R4 | E5 “căng” → E4 “da” | Không có quan hệ thuộc 5 loại (NO_RELATION) |

### Cần chốt

- ONTOLOGY_SCOPE: cần chốt phạm vi thuốc/dược chất so với mỹ phẩm, thực phẩm, hóa chất nội sinh hoặc hệ vi sinh; giữ ánh xạ nguồn khi chưa có quy ước đủ rõ.

### Thay đổi NER

- ∅ → E5 “căng” CONDITION [19, 23)

Nguồn: VietMed-NER train, dòng 537 (từ 0).

## VM600-066

**Đoạn gốc:** tế bào và cái tổn thương tế bào ấy thì làm cho tế bào không bình thường tế bào không bình thường đấy thì nó một là nếu

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | tế bào | Bộ phận cơ thể (BODY_PART) | [0, 6) |
| E2 | tổn thương tế bào | Bệnh hoặc triệu chứng (CONDITION) | [14, 31) |
| E4 | tế bào | Bộ phận cơ thể (BODY_PART) | [47, 53) |
| E5 | tế bào | Bộ phận cơ thể (BODY_PART) | [72, 78) |

### RE

| Mã | Cặp có hướng | Kết luận đề xuất |
|---|---|---|
| R1 | E2 “tổn thương tế bào” → E1 “tế bào” | Chưa rõ — cần chốt (CHUA_RO) |
| R2 | E2 “tổn thương tế bào” → E4 “tế bào” | Chưa rõ — cần chốt (CHUA_RO) |
| R3 | E2 “tổn thương tế bào” → E5 “tế bào” | Chưa rõ — cần chốt (CHUA_RO) |

### Cần chốt

- UNRESOLVED_RE: còn cặp CHUA_RO; tuyệt đối không đổi thành NO_RELATION khi xuất huấn luyện.

### Thay đổi NER

- E2 “tổn thương” CONDITION [14, 24) → E2 “tổn thương tế bào” CONDITION [14, 31)
- E3 “tế bào” BODY_PART [25, 31) → ∅

Nguồn: VietMed-NER train, dòng 544 (từ 0).

## VM600-067

**Đoạn gốc:** nhau và cái lứa tuổi mà trung niên là cái lứa tuổi gặp khá là phổ biến còn

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

Không có thực thể thuộc sáu loại được giữ trong bản rà soát.

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

Nguồn: VietMed-NER train, dòng 552 (từ 0).

## VM600-068

**Đoạn gốc:** não đột quỵ đó thì nó liên quan đến việc hình thành các cục máu đông và việc cục máu đông đã nó trôi ra là đi

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | não | Bộ phận cơ thể (BODY_PART) | [0, 3) |
| E2 | đột quỵ | Bệnh hoặc triệu chứng (CONDITION) | [4, 11) |
| E3 | cục máu đông | Bệnh hoặc triệu chứng (CONDITION) | [56, 68) |
| E4 | cục máu đông | Bệnh hoặc triệu chứng (CONDITION) | [77, 89) |

### RE

| Mã | Cặp có hướng | Kết luận đề xuất |
|---|---|---|
| R1 | E2 “đột quỵ” → E1 “não” | Chưa rõ — cần chốt (CHUA_RO) |
| R2 | E3 “cục máu đông” → E1 “não” | Không có quan hệ thuộc 5 loại (NO_RELATION) |
| R3 | E4 “cục máu đông” → E1 “não” | Không có quan hệ thuộc 5 loại (NO_RELATION) |

### Cần chốt

- CONTEXT_OR_TRANSCRIPT: câu bị cắt, tham chiếu/mục đích chưa rõ hoặc nghi lỗi phiên âm; cần xem ngữ cảnh/audio gốc, không tự sửa văn bản.
- UNRESOLVED_RE: còn cặp CHUA_RO; tuyệt đối không đổi thành NO_RELATION khi xuất huấn luyện.

Nguồn: VietMed-NER train, dòng 599 (từ 0).

## VM600-069

**Đoạn gốc:** alo alo rồi chúng tôi đang lắng nghe đây ạ mời cô trình bày

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

Không có thực thể thuộc sáu loại được giữ trong bản rà soát.

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

Nguồn: VietMed-NER train, dòng 600 (từ 0).

## VM600-070

**Đoạn gốc:** bệnh nền và hàng tháng phải đến bệnh viện để mà lấy thuốc thì chúng tôi liên tưởng đến chuyện là nhiều bệnh nhân

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | bệnh nền | Bệnh hoặc triệu chứng (CONDITION) | [0, 8) |
| E2 | thuốc | Thuốc/dược chất (DRUG) | [52, 57) |

### RE

| Mã | Cặp có hướng | Kết luận đề xuất |
|---|---|---|
| R1 | E1 “bệnh nền” → E2 “thuốc” | Được điều trị bằng thuốc (treated_by) |

### Cần chốt

- GENERIC_MENTION: cần chốt có giữ bệnh/triệu chứng/biến chứng chung và tham chiếu không định danh trong NER hay không.

Nguồn: VietMed-NER train, dòng 601 (từ 0).

## VM600-071

**Đoạn gốc:** hiệu mà ngày xưa chúng ta vẫn hay phổ biến đấy là gì ạ nâng niu bàn chân việt thì trong trường hợp này của bác bác tìm

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | bàn chân | Bộ phận cơ thể (BODY_PART) | [64, 72) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

Nguồn: VietMed-NER train, dòng 609 (từ 0).

## VM600-072

**Đoạn gốc:** không phải có tác dụng phụ của các các loại thuốc này không phải mỗi cái chống viêm đâu rất nhiều các cái thuốc khác và

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | tác dụng phụ | Bệnh hoặc triệu chứng (CONDITION) | [14, 26) |
| E2 | thuốc | Thuốc/dược chất (DRUG) | [44, 49) |
| E3 | viêm | Bệnh hoặc triệu chứng (CONDITION) | [79, 83) |
| E5 | thuốc | Thuốc/dược chất (DRUG) | [106, 111) |

### RE

| Mã | Cặp có hướng | Kết luận đề xuất |
|---|---|---|
| R1 | E1 “tác dụng phụ” → E2 “thuốc” | Không có quan hệ thuộc 5 loại (NO_RELATION) |
| R2 | E1 “tác dụng phụ” → E5 “thuốc” | Không có quan hệ thuộc 5 loại (NO_RELATION) |
| R3 | E3 “viêm” → E2 “thuốc” | Không có quan hệ thuộc 5 loại (NO_RELATION) |
| R4 | E3 “viêm” → E5 “thuốc” | Không có quan hệ thuộc 5 loại (NO_RELATION) |

### Thay đổi NER

- E4 “rất nhiều” DOSAGE [88, 97) → ∅

Nguồn: VietMed-NER train, dòng 613 (từ 0).

## VM600-073

**Đoạn gốc:** trị nó sẽ phải dài hơn và chúng ta sẽ phải tập trung vào cái cái vị trí căn nguyên của của cái bệnh là ở cái vùng

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

Không có thực thể thuộc sáu loại được giữ trong bản rà soát.

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

Nguồn: VietMed-NER train, dòng 618 (từ 0).

## VM600-074

**Đoạn gốc:** đây là một cái sản phẩm mà cũng đã được thừa kế cái đề tài nghiên cứu cấp nhà

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

Không có thực thể thuộc sáu loại được giữ trong bản rà soát.

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Thay đổi NER

- E1 “nghiên cứu” TEST [59, 69) → ∅

Nguồn: VietMed-NER train, dòng 622 (từ 0).

## VM600-075

**Đoạn gốc:** ba nữa rõ ràng là gì ạ mình cần phải điều trị thì nó mới tránh được những cái chuyện mà đột ngột đột xuất hoặc thậm

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | điều trị | Thủ thuật hoặc điều trị (PROCEDURE) | [37, 45) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- GENERIC_INTERVENTION: cần chốt việc giữ hành động điều trị/chẩn đoán chung khi không nêu phương pháp cụ thể.

Nguồn: VietMed-NER train, dòng 645 (từ 0).

## VM600-076

**Đoạn gốc:** lại ảnh hưởng đến nội tạng là bởi vì khi mà chúng ta sử dụng vào trong thì tất cả những cái cơ quan nội tạng của chúng ta

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | nội tạng | Bộ phận cơ thể (BODY_PART) | [18, 26) |
| E2 | nội tạng | Bộ phận cơ thể (BODY_PART) | [100, 108) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

Nguồn: VietMed-NER train, dòng 657 (từ 0).

## VM600-077

**Đoạn gốc:** mà cũng bị bệnh gì bác ạ dạ vâng ở đây thì vâng ở đây thì có lẽ

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | bệnh | Bệnh hoặc triệu chứng (CONDITION) | [11, 15) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- GENERIC_MENTION: cần chốt có giữ bệnh/triệu chứng/biến chứng chung và tham chiếu không định danh trong NER hay không.

### Thay đổi NER

- E1 “bị bệnh” CONDITION [8, 15) → E1 “bệnh” CONDITION [11, 15)

Nguồn: VietMed-NER train, dòng 664 (từ 0).

## VM600-078

**Đoạn gốc:** trạng sạm nám tăng sắc tố do đó nên chúng ta phải nhớ là chúng ta luôn phải thoa kem chống nắng đúng cách đúng liều đủ

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | sạm nám | Bệnh hoặc triệu chứng (CONDITION) | [6, 13) |
| E2 | tăng sắc tố | Bệnh hoặc triệu chứng (CONDITION) | [14, 25) |
| E3 | kem chống nắng | Thuốc/dược chất (DRUG) | [81, 95) |

### RE

| Mã | Cặp có hướng | Kết luận đề xuất |
|---|---|---|
| R1 | E1 “sạm nám” → E3 “kem chống nắng” | Chưa rõ — cần chốt (CHUA_RO) |
| R2 | E2 “tăng sắc tố” → E3 “kem chống nắng” | Chưa rõ — cần chốt (CHUA_RO) |

### Cần chốt

- ONTOLOGY_SCOPE: cần chốt phạm vi thuốc/dược chất so với mỹ phẩm, thực phẩm, hóa chất nội sinh hoặc hệ vi sinh; giữ ánh xạ nguồn khi chưa có quy ước đủ rõ.
- UNRESOLVED_RE: còn cặp CHUA_RO; tuyệt đối không đổi thành NO_RELATION khi xuất huấn luyện.

Nguồn: VietMed-NER train, dòng 680 (từ 0).

## VM600-079

**Đoạn gốc:** cái ngưỡng mức điều trị như vậy thưa tất cả quý vị và các bạn vừa rồi thì chúng ta đã được lắng nghe bác sĩ chuyên khoa

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E2 | điều trị | Thủ thuật hoặc điều trị (PROCEDURE) | [15, 23) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- CONTEXT_OR_TRANSCRIPT: câu bị cắt, tham chiếu/mục đích chưa rõ hoặc nghi lỗi phiên âm; cần xem ngữ cảnh/audio gốc, không tự sửa văn bản.
- GENERIC_INTERVENTION: cần chốt việc giữ hành động điều trị/chẩn đoán chung khi không nêu phương pháp cụ thể.

### Thay đổi NER

- E1 “cái ngưỡng mức” DOSAGE [0, 14) → ∅

Nguồn: VietMed-NER train, dòng 687 (từ 0).

## VM600-080

**Đoạn gốc:** chứng ngoài vận động khác cũng như là tuổi của người bệnh đã trở nên lớn hơn và khó khăn hơn và những cái vấn đề đó

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

Không có thực thể thuộc sáu loại được giữ trong bản rà soát.

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- CONTEXT_OR_TRANSCRIPT: câu bị cắt, tham chiếu/mục đích chưa rõ hoặc nghi lỗi phiên âm; cần xem ngữ cảnh/audio gốc, không tự sửa văn bản.

Nguồn: VietMed-NER train, dòng 699 (từ 0).

## VM600-081

**Đoạn gốc:** nhớ lại thời trung học khi bạn học về hệ tiêu hóa bạn đã được biết nó phân giải

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | hệ tiêu hóa | Bộ phận cơ thể (BODY_PART) | [38, 49) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

Nguồn: VietMed-NER train, dòng 703 (từ 0).

## VM600-082

**Đoạn gốc:** những cái khó khăn mà bác gặp phải thì cũng rất là nhiều người bệnh người ta cũng đang gặp phải tuy nhiên là người ta

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

Không có thực thể thuộc sáu loại được giữ trong bản rà soát.

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

Nguồn: VietMed-NER train, dòng 716 (từ 0).

## VM600-083

**Đoạn gốc:** hướng đến một cuộc sống mạnh khỏe hơn hạnh phúc và thành công chúng tôi sẽ thực sự rất biết ơn về sự ủng hộ quý báu

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

Không có thực thể thuộc sáu loại được giữ trong bản rà soát.

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

Nguồn: VietMed-NER train, dòng 722 (từ 0).

## VM600-084

**Đoạn gốc:** điều trị để chiến thắng chính bản thân mình giúp mình hồi phục đó là một điều rất là quan trọng vâng trong các cuộc

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | điều trị | Thủ thuật hoặc điều trị (PROCEDURE) | [0, 8) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- GENERIC_INTERVENTION: cần chốt việc giữ hành động điều trị/chẩn đoán chung khi không nêu phương pháp cụ thể.

Nguồn: VietMed-NER train, dòng 746 (từ 0).

## VM600-085

**Đoạn gốc:** đây cũng giúp cho họ tăng đậm độ năng lượng thì chúng ta có thể ví dụ như là thường ung thư thì phải nấu mềm lỏng này

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | ung thư | Bệnh hoặc triệu chứng (CONDITION) | [84, 91) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

Nguồn: VietMed-NER train, dòng 750 (từ 0).

## VM600-086

**Đoạn gốc:** xin điều trị có nghĩa là bị dại mà không

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | điều trị | Thủ thuật hoặc điều trị (PROCEDURE) | [4, 12) |
| E2 | dại | Bệnh hoặc triệu chứng (CONDITION) | [28, 31) |

### RE

| Mã | Cặp có hướng | Kết luận đề xuất |
|---|---|---|
| R1 | E2 “dại” → E1 “điều trị” | Chưa rõ — cần chốt (CHUA_RO) |

### Cần chốt

- CONTEXT_OR_TRANSCRIPT: câu bị cắt, tham chiếu/mục đích chưa rõ hoặc nghi lỗi phiên âm; cần xem ngữ cảnh/audio gốc, không tự sửa văn bản.
- GENERIC_INTERVENTION: cần chốt việc giữ hành động điều trị/chẩn đoán chung khi không nêu phương pháp cụ thể.
- UNRESOLVED_RE: còn cặp CHUA_RO; tuyệt đối không đổi thành NO_RELATION khi xuất huấn luyện.

### Thay đổi NER

- E2 “bị dại” CONDITION [25, 31) → E2 “dại” CONDITION [28, 31)

Nguồn: VietMed-NER train, dòng 756 (từ 0).

## VM600-087

**Đoạn gốc:** mà chịu và cách tính dung nạp đối với những các sản phẩm nó cũng khắt khe hơn so với những cái làn da thường em thấy

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E2 | làn da | Bộ phận cơ thể (BODY_PART) | [95, 101) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- ONTOLOGY_SCOPE: cần chốt phạm vi thuốc/dược chất so với mỹ phẩm, thực phẩm, hóa chất nội sinh hoặc hệ vi sinh; giữ ánh xạ nguồn khi chưa có quy ước đủ rõ.

### Thay đổi NER

- E1 “tính dung nạp” DOSAGE [16, 29) → ∅

Nguồn: VietMed-NER train, dòng 767 (từ 0).

## VM600-088

**Đoạn gốc:** vừa rồi thì sẽ rất là tốt cho bệnh nhân ung thư đấy cũng là một giải pháp mà cũng bớt đi cái cái mà người ung thư đôi

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | ung thư | Bệnh hoặc triệu chứng (CONDITION) | [40, 47) |
| E2 | ung thư | Bệnh hoặc triệu chứng (CONDITION) | [106, 113) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

Nguồn: VietMed-NER train, dòng 783 (từ 0).

## VM600-089

**Đoạn gốc:** trở lại cũng như là nó hỗ trợ cho vấn đề đường tiêu hóa của mình vâng

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E2 | đường tiêu hóa | Bộ phận cơ thể (BODY_PART) | [41, 55) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Thay đổi NER

- E1 “hỗ trợ” PROCEDURE [23, 29) → ∅

Nguồn: VietMed-NER train, dòng 804 (từ 0).

## VM600-090

**Đoạn gốc:** công việc chính của các chuyên gia tâm lý trong việc điều trị người bệnh béo phì

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | điều trị | Thủ thuật hoặc điều trị (PROCEDURE) | [53, 61) |
| E2 | béo phì | Bệnh hoặc triệu chứng (CONDITION) | [73, 80) |

### RE

| Mã | Cặp có hướng | Kết luận đề xuất |
|---|---|---|
| R1 | E2 “béo phì” → E1 “điều trị” | Được điều trị bằng phương pháp (treated_by_procedure) |

### Cần chốt

- GENERIC_INTERVENTION: cần chốt việc giữ hành động điều trị/chẩn đoán chung khi không nêu phương pháp cụ thể.

Nguồn: VietMed-NER train, dòng 810 (từ 0).

## VM600-091

**Đoạn gốc:** cố định khớp đặc hiệu với mầm bệnh hoặc tế bào nhiễm bệnh hay đúng hơn là mô

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E3 | tế bào | Bộ phận cơ thể (BODY_PART) | [40, 46) |
| E5 | nhiễm bệnh | Bệnh hoặc triệu chứng (CONDITION) | [47, 57) |
| E4 | mô | Bộ phận cơ thể (BODY_PART) | [74, 76) |

### RE

| Mã | Cặp có hướng | Kết luận đề xuất |
|---|---|---|
| R1 | E5 “nhiễm bệnh” → E3 “tế bào” | Không có quan hệ thuộc 5 loại (NO_RELATION) |
| R2 | E5 “nhiễm bệnh” → E4 “mô” | Không có quan hệ thuộc 5 loại (NO_RELATION) |

### Thay đổi NER

- E2 “mầm bệnh” CONDITION [26, 34) → ∅
- E1 “khớp” BODY_PART [8, 12) → ∅
- ∅ → E5 “nhiễm bệnh” CONDITION [47, 57)

Nguồn: VietMed-NER train, dòng 819 (từ 0).

## VM600-092

**Đoạn gốc:** thì đã có thể là giúp giảm rất là nhiều những cái biến chứng và những cái bệnh lý đi kèm như là có thể giảm được tới

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | biến chứng | Bệnh hoặc triệu chứng (CONDITION) | [50, 60) |
| E2 | bệnh lý | Bệnh hoặc triệu chứng (CONDITION) | [74, 81) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- GENERIC_MENTION: cần chốt có giữ bệnh/triệu chứng/biến chứng chung và tham chiếu không định danh trong NER hay không.

Nguồn: VietMed-NER train, dòng 821 (từ 0).

## VM600-093

**Đoạn gốc:** hoàn toàn ô thế là mình điều trị xong rồi xong rồi cứ ba tháng xét nghiệm một lần hay là sáu tháng xét nghiệm một lần

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | điều trị | Thủ thuật hoặc điều trị (PROCEDURE) | [24, 32) |
| E2 | xét nghiệm | Xét nghiệm hoặc thăm khám (TEST) | [63, 73) |
| E3 | xét nghiệm | Xét nghiệm hoặc thăm khám (TEST) | [99, 109) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- GENERIC_INTERVENTION: cần chốt việc giữ hành động điều trị/chẩn đoán chung khi không nêu phương pháp cụ thể.

Nguồn: VietMed-NER train, dòng 841 (từ 0).

## VM600-094

**Đoạn gốc:** kết quả này có thể giúp dự đoán gánh nặng bệnh alzheimer ở cả nước đang phát triển nơi sự đa dạng vi sinh vật đang

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E2 | alzheimer | Bệnh hoặc triệu chứng (CONDITION) | [47, 56) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Thay đổi NER

- E1 “dự đoán” PROCEDURE [24, 31) → ∅
- E3 “vi sinh vật” BODY_PART [98, 109) → ∅

Nguồn: VietMed-NER train, dòng 842 (từ 0).

## VM600-095

**Đoạn gốc:** ung thư ấy hoàn toàn là do người bệnh ung thư cho nên chúng tôi rất mong là dù

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | ung thư | Bệnh hoặc triệu chứng (CONDITION) | [0, 7) |
| E2 | ung thư | Bệnh hoặc triệu chứng (CONDITION) | [38, 45) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

Nguồn: VietMed-NER train, dòng 851 (từ 0).

## VM600-096

**Đoạn gốc:** thức ăn đó thì nó sẽ làm cho dễ bị béo phì nữa đối với lại môi trường xã hội

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | béo phì | Bệnh hoặc triệu chứng (CONDITION) | [35, 42) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Thay đổi NER

- E2 “môi” BODY_PART [59, 62) → ∅

Nguồn: VietMed-NER train, dòng 854 (từ 0).

## VM600-097

**Đoạn gốc:** alo vâng chúng tôi đang nghe đây ạ cô chia sẻ đi ạ

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

Không có thực thể thuộc sáu loại được giữ trong bản rà soát.

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

Nguồn: VietMed-NER train, dòng 857 (từ 0).

## VM600-098

**Đoạn gốc:** thương thận vân vân và vân vân cho nên là lời khuyên thứ hai của chương trình đối với bác là gì nên tìm đến những giải

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | thận | Bộ phận cơ thể (BODY_PART) | [7, 11) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- CONTEXT_OR_TRANSCRIPT: câu bị cắt, tham chiếu/mục đích chưa rõ hoặc nghi lỗi phiên âm; cần xem ngữ cảnh/audio gốc, không tự sửa văn bản.

### Thay đổi NER

- ∅ → E1 “thận” BODY_PART [7, 11)

Nguồn: VietMed-NER train, dòng 875 (từ 0).

## VM600-099

**Đoạn gốc:** bác ơi vâng bây giờ thì với cái tình trạng hiện nay của bác này thứ nhất là huyết áp đang tăng cao thì bác nên bác

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E2 | huyết áp đang tăng cao | Bệnh hoặc triệu chứng (CONDITION) | [76, 98) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Thay đổi NER

- E1 “thứ nhất” DOSAGE [64, 72) → ∅
- E3 “cao” DOSAGE [95, 98) → ∅
- E2 “huyết áp” CONDITION [76, 84) → E2 “huyết áp đang tăng cao” CONDITION [76, 98)

Nguồn: VietMed-NER train, dòng 892 (từ 0).

## VM600-100

**Đoạn gốc:** mất do tổn thương đường tiêu hóa không không thể nào tiêu hóa thu được là do ngay cái chính khối u đó cũng làm tăng quá

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | tổn thương | Bệnh hoặc triệu chứng (CONDITION) | [7, 17) |
| E2 | đường tiêu hóa | Bộ phận cơ thể (BODY_PART) | [18, 32) |
| E3 | khối u | Bệnh hoặc triệu chứng (CONDITION) | [92, 98) |

### RE

| Mã | Cặp có hướng | Kết luận đề xuất |
|---|---|---|
| R1 | E1 “tổn thương” → E2 “đường tiêu hóa” | Có vị trí ở (located_at) |
| R2 | E3 “khối u” → E2 “đường tiêu hóa” | Chưa rõ — cần chốt (CHUA_RO) |

### Cần chốt

- UNRESOLVED_RE: còn cặp CHUA_RO; tuyệt đối không đổi thành NO_RELATION khi xuất huấn luyện.

Nguồn: VietMed-NER train, dòng 899 (từ 0).

# Phiếu rà soát NER và RE 101 đến 200

Bản AI rà soát lần hai ngày 15/10/2026. Giữ nguyên câu nguồn và sáu loại NER, năm quan hệ RE. Chưa được chuyên gia xác nhận.

Quy tắc người dùng đã chốt: giữ cả cụm bệnh/triệu chứng trong một CONDITION. Không tách bộ phận bên trong cụm để tạo located_at. Vị trí được nêu riêng bằng giới từ hoặc mệnh đề riêng vẫn được xét.

Vị trí ký tự là khoảng [start, end), đếm từ 0 theo Unicode. Mã E ổn định khi sửa; mã R được tạo lại. Không dùng CHUA_RO làm nhãn huấn luyện hoặc nhãn âm.

## VM600-101

**Đoạn gốc:** là làm việc hàng ngày để phần nào có thể khắc phục được cái tình trạng mà bác phải di chuyển nhiều như vậy mà cái bệnh

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

Không có thực thể thuộc sáu loại được giữ trong bản rà soát.

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

Nguồn: VietMed-NER train, dòng 914 (từ 0).

## VM600-102

**Đoạn gốc:** ta muốn mua cái gì để mua nhưng mà chúng ta phải có hệ thống kiểm nghiệm và hệ thống kiểm đó là được tiến hành bởi gì

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

Không có thực thể thuộc sáu loại được giữ trong bản rà soát.

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Thay đổi NER

- E1 “kiểm nghiệm” DRUG [61, 72) → ∅

Nguồn: VietMed-NER train, dòng 918 (từ 0).

## VM600-103

**Đoạn gốc:** vị ngọt thậm chí cũng không thích nữa rồi vị tanh không chịu được không thể chấp nhận thức ăn và đặc biệt là làm cho

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

Không có thực thể thuộc sáu loại được giữ trong bản rà soát.

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

Nguồn: VietMed-NER train, dòng 919 (từ 0).

## VM600-104

**Đoạn gốc:** khi mà chúng ta đến nơi đây ví dụ như anh đến những cái nơi thì anh thấy đông

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

Không có thực thể thuộc sáu loại được giữ trong bản rà soát.

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

Nguồn: VietMed-NER train, dòng 923 (từ 0).

## VM600-105

**Đoạn gốc:** của cơ thể của chúng ta nghĩa là từ hệ tim mạch hệ huyết áp rồi là đến hệ hô

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | cơ thể | Bộ phận cơ thể (BODY_PART) | [4, 10) |
| E2 | tim mạch | Bộ phận cơ thể (BODY_PART) | [39, 47) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- CONTEXT_OR_TRANSCRIPT: câu bị cắt, tham chiếu/mục đích chưa rõ hoặc nghi lỗi phiên âm; cần xem ngữ cảnh/audio gốc, không tự sửa văn bản.

### Thay đổi NER

- E3 “huyết áp” CONDITION [51, 59) → ∅

Nguồn: VietMed-NER train, dòng 931 (từ 0).

## VM600-106

**Đoạn gốc:** trắng hoặc là chiết xuất từ hoa thủy tiên biển nó đều làm tăng với hiệu quả để mà giúp cho quá trình sáng da

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E5 | chiết xuất từ hoa thủy tiên biển | Thuốc/dược chất (DRUG) | [14, 46) |
| E4 | da | Bộ phận cơ thể (BODY_PART) | [106, 108) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- ONTOLOGY_SCOPE: cần chốt phạm vi thuốc/dược chất so với mỹ phẩm, thực phẩm, hóa chất nội sinh hoặc hệ vi sinh; giữ ánh xạ nguồn khi chưa có quy ước đủ rõ.

### Thay đổi NER

- E1 “chiết xuất” PROCEDURE [14, 24) → ∅
- E3 “quá trình sáng” PROCEDURE [91, 105) → ∅
- E2 “hoa thủy tiên biển” DRUG [28, 46) → ∅
- ∅ → E5 “chiết xuất từ hoa thủy tiên biển” DRUG [14, 46)

Nguồn: VietMed-NER train, dòng 934 (từ 0).

## VM600-107

**Đoạn gốc:** trọng trong miễn dịch không ai thực sự biết được những hoạt động như thế nào cho đến nhà

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

Không có thực thể thuộc sáu loại được giữ trong bản rà soát.

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

Nguồn: VietMed-NER train, dòng 950 (từ 0).

## VM600-108

**Đoạn gốc:** penicillin vẫn còn hiệu quả trên một số lượng lớn vi khuẩn nó gắn vào các phân

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | penicillin | Thuốc/dược chất (DRUG) | [0, 10) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- SCOPE_CONFIRMATION: cần xác nhận quy ước về thuốc/dược chất, can thiệp không dùng thuốc, thiết bị, tác nhân hoặc hoạt động thăm khám; không coi ánh xạ nguồn là xác nhận chuyên gia.

### Thay đổi NER

- E2 “vi khuẩn” CONDITION [50, 58) → ∅

Nguồn: VietMed-NER train, dòng 960 (từ 0).

## VM600-109

**Đoạn gốc:** cái những cái thiết bị định vị để người ta đi vào cái thứ ba đây là một cái phẫu

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | thiết bị định vị | Thủ thuật hoặc điều trị (PROCEDURE) | [14, 30) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

Nguồn: VietMed-NER train, dòng 963 (từ 0).

## VM600-110

**Đoạn gốc:** phát triển và nó tích lũy được những hoạt chất quý giá nhưng mà đương nhiên chúng ta thấy một điều là đông trùng hạ

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | hoạt chất | Thuốc/dược chất (DRUG) | [37, 46) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- CONTEXT_OR_TRANSCRIPT: câu bị cắt, tham chiếu/mục đích chưa rõ hoặc nghi lỗi phiên âm; cần xem ngữ cảnh/audio gốc, không tự sửa văn bản.
- ONTOLOGY_SCOPE: cần chốt phạm vi thuốc/dược chất so với mỹ phẩm, thực phẩm, hóa chất nội sinh hoặc hệ vi sinh; giữ ánh xạ nguồn khi chưa có quy ước đủ rõ.

Nguồn: VietMed-NER train, dòng 966 (từ 0).

## VM600-111

**Đoạn gốc:** đang gặp phải cái tình trạng bệnh lý đó chính là bị cao huyết áp nè bệnh lý về tim mạch nè bệnh lý đái tháo đường hoặc

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | cao huyết áp | Bệnh hoặc triệu chứng (CONDITION) | [52, 64) |
| E4 | bệnh lý về tim mạch | Bệnh hoặc triệu chứng (CONDITION) | [68, 87) |
| E3 | đái tháo đường | Bệnh hoặc triệu chứng (CONDITION) | [99, 113) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Thay đổi NER

- ∅ → E4 “bệnh lý” CONDITION [68, 75)
- E4 “bệnh lý” CONDITION [68, 75) → E4 “bệnh lý về tim mạch” CONDITION [68, 87)
- E2 “tim mạch” BODY_PART [79, 87) → ∅

Nguồn: VietMed-NER train, dòng 967 (từ 0).

## VM600-112

**Đoạn gốc:** mỗi tế bào t hoặc tế bào b riêng lẻ có hình dạng khác nhau đôi chút cho

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | tế bào t | Bộ phận cơ thể (BODY_PART) | [4, 12) |
| E2 | tế bào b | Bộ phận cơ thể (BODY_PART) | [18, 26) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

Nguồn: VietMed-NER train, dòng 984 (từ 0).

## VM600-113

**Đoạn gốc:** để độ khoảng năm bảy phút và mình có thể để khoảng mười phút thì mình nhớ là bát cháo

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

Không có thực thể thuộc sáu loại được giữ trong bản rà soát.

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

Nguồn: VietMed-NER train, dòng 1006 (từ 0).

## VM600-114

**Đoạn gốc:** với những thảo dược khác mục đích là cái gì à thì trong một cái đơn thuốc của y học cổ truyền chúng ta

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | thảo dược | Thuốc/dược chất (DRUG) | [10, 19) |
| E2 | thuốc của y học cổ truyền | Thuốc/dược chất (DRUG) | [68, 93) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- SCOPE_CONFIRMATION: cần xác nhận quy ước về thuốc/dược chất, can thiệp không dùng thuốc, thiết bị, tác nhân hoặc hoạt động thăm khám; không coi ánh xạ nguồn là xác nhận chuyên gia.

Nguồn: VietMed-NER train, dòng 1010 (từ 0).

## VM600-115

**Đoạn gốc:** khi phẫu thuật để có được kết quả như mong đợi ngoài ra thì người bệnh parkinson cần phải chuẩn bị những vấn đề

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | phẫu thuật | Thủ thuật hoặc điều trị (PROCEDURE) | [4, 14) |
| E2 | parkinson | Bệnh hoặc triệu chứng (CONDITION) | [71, 80) |

### RE

| Mã | Cặp có hướng | Kết luận đề xuất |
|---|---|---|
| R1 | E2 “parkinson” → E1 “phẫu thuật” | Được điều trị bằng phương pháp (treated_by_procedure) |

Nguồn: VietMed-NER train, dòng 1017 (từ 0).

## VM600-116

**Đoạn gốc:** thì lại nên giảm thịt đỏ thịt đỏ là thịt con bốn chân ví dụ như thịt lợn thịt bò thì chúng ta chỉ nên tối đa là năm mươi gam

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

Không có thực thể thuộc sáu loại được giữ trong bản rà soát.

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Thay đổi NER

- E2 “năm mươi” DOSAGE [112, 120) → ∅
- E1 “chân” BODY_PART [49, 53) → ∅

Nguồn: VietMed-NER train, dòng 1022 (từ 0).

## VM600-117

**Đoạn gốc:** xảy ra nếu sự hiện diện của một thứ chưa từng có trong cơ thể bạn trước đây không phải là dấu hiệu duy nhất cho việc đáp

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | cơ thể | Bộ phận cơ thể (BODY_PART) | [55, 61) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

Nguồn: VietMed-NER train, dòng 1023 (từ 0).

## VM600-118

**Đoạn gốc:** cũng phải cố gắng lên một chút thì chúng ta mới dần dần cải thiện được sức khỏe mà có cải thiện sức khỏe thì chúng ta

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

Không có thực thể thuộc sáu loại được giữ trong bản rà soát.

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Thay đổi NER

- E1 “cải thiện” PROCEDURE [56, 65) → ∅
- E2 “cải thiện” PROCEDURE [86, 95) → ∅

Nguồn: VietMed-NER train, dòng 1027 (từ 0).

## VM600-119

**Đoạn gốc:** đề mà bản thân bệnh viện bệnh nhân đã bị rồi đó là gì cái tình trạng vữa xơ động mạch cái này có thể nói rằng là như phần

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | vữa xơ động mạch | Bệnh hoặc triệu chứng (CONDITION) | [69, 85) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

Nguồn: VietMed-NER train, dòng 1030 (từ 0).

## VM600-120

**Đoạn gốc:** hòa lên để mình có thể có được một cái bữa ăn là bữa ăn ấy có thể là bữa ăn dặm phụ vào để mà chúng ta cung cấp

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

Không có thực thể thuộc sáu loại được giữ trong bản rà soát.

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

Nguồn: VietMed-NER train, dòng 1035 (từ 0).

## VM600-121

**Đoạn gốc:** hướng thảo luận về vai trò của lần lượt từng phân tử hoặc tế bào nhưng điều đó

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E2 | tế bào | Bộ phận cơ thể (BODY_PART) | [58, 64) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Thay đổi NER

- E1 “phân tử” DOSAGE [45, 52) → ∅

Nguồn: VietMed-NER train, dòng 1041 (từ 0).

## VM600-122

**Đoạn gốc:** các tế bào thần kinh nó không liên kết được với nhau bởi vì sao bởi vì các cái chất dẫn truyền thần kinh mà để cái

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | tế bào thần kinh | Bộ phận cơ thể (BODY_PART) | [4, 20) |
| E4 | chất dẫn truyền thần kinh | Thuốc/dược chất (DRUG) | [79, 104) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- SCOPE_CONFIRMATION: cần xác nhận quy ước về thuốc/dược chất, can thiệp không dùng thuốc, thiết bị, tác nhân hoặc hoạt động thăm khám; không coi ánh xạ nguồn là xác nhận chuyên gia.

### Thay đổi NER

- E1 “tế bào” BODY_PART [4, 10) → E1 “tế bào thần kinh” BODY_PART [4, 20)
- E2 “thần kinh” BODY_PART [11, 20) → ∅
- E3 “thần kinh” BODY_PART [95, 104) → ∅
- ∅ → E4 “chất dẫn truyền thần kinh” DRUG [79, 104)

Nguồn: VietMed-NER train, dòng 1044 (từ 0).

## VM600-123

**Đoạn gốc:** lên thì họ những thấy những cái hình thi hoa hậu rồi này nọ hay là thấy những cái hình đối với nam thì ở thấy những hình

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

Không có thực thể thuộc sáu loại được giữ trong bản rà soát.

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

Nguồn: VietMed-NER train, dòng 1049 (từ 0).

## VM600-124

**Đoạn gốc:** lại họ thường tranh luận về các vấn đề khoa học trong xe của họ và sau đó chỉ đơn giản là quên những gì đã nói nhưng

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

Không có thực thể thuộc sáu loại được giữ trong bản rà soát.

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

Nguồn: VietMed-NER train, dòng 1051 (từ 0).

## VM600-125

**Đoạn gốc:** bên ngoài bằng những phương pháp phù hợp và đó chính là mấu chốt để có thể nâng tầm chất lượng của các quy trình công

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

Không có thực thể thuộc sáu loại được giữ trong bản rà soát.

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

Nguồn: VietMed-NER train, dòng 1056 (từ 0).

## VM600-126

**Đoạn gốc:** như tình trạng dinh dưỡng của bệnh nhân không tốt thì rất khó có thể giúp cho bệnh nhân có thể chịu đựng được hết cái

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

Không có thực thể thuộc sáu loại được giữ trong bản rà soát.

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- CONTEXT_OR_TRANSCRIPT: câu bị cắt, tham chiếu/mục đích chưa rõ hoặc nghi lỗi phiên âm; cần xem ngữ cảnh/audio gốc, không tự sửa văn bản.

Nguồn: VietMed-NER train, dòng 1077 (từ 0).

## VM600-127

**Đoạn gốc:** quang của chúng ta và hãy vững tin hãy có một cái tinh thần tốt để mau chóng

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

Không có thực thể thuộc sáu loại được giữ trong bản rà soát.

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- CONTEXT_OR_TRANSCRIPT: câu bị cắt, tham chiếu/mục đích chưa rõ hoặc nghi lỗi phiên âm; cần xem ngữ cảnh/audio gốc, không tự sửa văn bản.

Nguồn: VietMed-NER train, dòng 1081 (từ 0).

## VM600-128

**Đoạn gốc:** nhiên là bệnh nhân sẽ phải nhịn ăn từ sáng hôm đó và bệnh nhân sẽ được đưa

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

Không có thực thể thuộc sáu loại được giữ trong bản rà soát.

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- CONTEXT_OR_TRANSCRIPT: câu bị cắt, tham chiếu/mục đích chưa rõ hoặc nghi lỗi phiên âm; cần xem ngữ cảnh/audio gốc, không tự sửa văn bản.

Nguồn: VietMed-NER train, dòng 1088 (từ 0).

## VM600-129

**Đoạn gốc:** cân đối mà đây chúng tôi thì quan niệm cân đối ở đây thì quan trọng nhất đó là cân đối giữa chất đạm động vật và thực

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

Không có thực thể thuộc sáu loại được giữ trong bản rà soát.

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

Nguồn: VietMed-NER train, dòng 1097 (từ 0).

## VM600-130

**Đoạn gốc:** chia sẻ theo chúng ta về những trở ngại và thách thức tâm lý mà người bệnh béo phì luôn phải đối mặt

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | béo phì | Bệnh hoặc triệu chứng (CONDITION) | [75, 82) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

Nguồn: VietMed-NER train, dòng 1105 (từ 0).

## VM600-131

**Đoạn gốc:** ra những cái dụng cụ rất là tốt thì để cho có việc mà chúng ta luồn cái ống đó

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

Không có thực thể thuộc sáu loại được giữ trong bản rà soát.

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- CONTEXT_OR_TRANSCRIPT: câu bị cắt, tham chiếu/mục đích chưa rõ hoặc nghi lỗi phiên âm; cần xem ngữ cảnh/audio gốc, không tự sửa văn bản.

Nguồn: VietMed-NER train, dòng 1107 (từ 0).

## VM600-132

**Đoạn gốc:** có những cái biến chứng của cái việc sử dụng chống viêm corticoid rồi đó là chảy máu dạ dày đó là viêm loét dạ dày

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | biến chứng | Bệnh hoặc triệu chứng (CONDITION) | [13, 23) |
| E2 | viêm | Bệnh hoặc triệu chứng (CONDITION) | [51, 55) |
| E3 | corticoid | Thuốc/dược chất (DRUG) | [56, 65) |
| E4 | chảy máu dạ dày | Bệnh hoặc triệu chứng (CONDITION) | [76, 91) |
| E6 | viêm loét dạ dày | Bệnh hoặc triệu chứng (CONDITION) | [98, 114) |

### RE

| Mã | Cặp có hướng | Kết luận đề xuất |
|---|---|---|
| R1 | E1 “biến chứng” → E3 “corticoid” | Không có quan hệ thuộc 5 loại (NO_RELATION) |
| R2 | E2 “viêm” → E3 “corticoid” | Được điều trị bằng thuốc (treated_by) |
| R3 | E4 “chảy máu dạ dày” → E3 “corticoid” | Không có quan hệ thuộc 5 loại (NO_RELATION) |
| R4 | E6 “viêm loét dạ dày” → E3 “corticoid” | Không có quan hệ thuộc 5 loại (NO_RELATION) |

### Thay đổi NER

- E4 “chảy máu” CONDITION [76, 84) → E4 “chảy máu dạ dày” CONDITION [76, 91)
- E5 “dạ dày” BODY_PART [85, 91) → ∅
- E6 “viêm loét” CONDITION [98, 107) → E6 “viêm loét dạ dày” CONDITION [98, 114)
- E7 “dạ dày” BODY_PART [108, 114) → ∅

Nguồn: VietMed-NER train, dòng 1117 (từ 0).

## VM600-133

**Đoạn gốc:** cân quá nhanh và quá nhiều trong một khoảng thời gian rất ngắn và điều này không những gây nguy hại cho sức khỏe mà

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

Không có thực thể thuộc sáu loại được giữ trong bản rà soát.

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

Nguồn: VietMed-NER train, dòng 1120 (từ 0).

## VM600-134

**Đoạn gốc:** thì hầu như cũng đồng nghĩa với việc duy trì được các chức năng bình thường của cơ thể và vấn đề thứ tư đó là dinh dưỡng

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | cơ thể | Bộ phận cơ thể (BODY_PART) | [80, 86) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

Nguồn: VietMed-NER train, dòng 1127 (từ 0).

## VM600-135

**Đoạn gốc:** cũng có một cái điều là cái hình thức về rối loạn điện học đó nó cũng tương đồng với cái hoạt động về cơ học của tâm nhĩ

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | rối loạn điện học | Bệnh hoặc triệu chứng (CONDITION) | [41, 58) |
| E2 | tâm nhĩ | Bộ phận cơ thể (BODY_PART) | [113, 120) |

### RE

| Mã | Cặp có hướng | Kết luận đề xuất |
|---|---|---|
| R1 | E1 “rối loạn điện học” → E2 “tâm nhĩ” | Chưa rõ — cần chốt (CHUA_RO) |

### Cần chốt

- CONTEXT_OR_TRANSCRIPT: câu bị cắt, tham chiếu/mục đích chưa rõ hoặc nghi lỗi phiên âm; cần xem ngữ cảnh/audio gốc, không tự sửa văn bản.
- UNRESOLVED_RE: còn cặp CHUA_RO; tuyệt đối không đổi thành NO_RELATION khi xuất huấn luyện.

Nguồn: VietMed-NER train, dòng 1131 (từ 0).

## VM600-136

**Đoạn gốc:** về tim là rất cần thiết bên cạnh đó một cái chế độ sinh hoạt khoa học như là tránh căng thẳng stress ngủ nghỉ đúng

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | tim | Bộ phận cơ thể (BODY_PART) | [3, 6) |
| E2 | căng thẳng | Bệnh hoặc triệu chứng (CONDITION) | [83, 93) |
| E3 | stress | Bệnh hoặc triệu chứng (CONDITION) | [94, 100) |

### RE

| Mã | Cặp có hướng | Kết luận đề xuất |
|---|---|---|
| R1 | E2 “căng thẳng” → E1 “tim” | Không có quan hệ thuộc 5 loại (NO_RELATION) |
| R2 | E3 “stress” → E1 “tim” | Không có quan hệ thuộc 5 loại (NO_RELATION) |

Nguồn: VietMed-NER train, dòng 1137 (từ 0).

## VM600-137

**Đoạn gốc:** đình mà có béo phì thì họ cũng khuyên bệnh nhân đến khám và điều trị chuyên khoa tuy nhiên thì thường là nhận được

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | béo phì | Bệnh hoặc triệu chứng (CONDITION) | [11, 18) |
| E2 | khám | Xét nghiệm hoặc thăm khám (TEST) | [52, 56) |
| E3 | điều trị | Thủ thuật hoặc điều trị (PROCEDURE) | [60, 68) |

### RE

| Mã | Cặp có hướng | Kết luận đề xuất |
|---|---|---|
| R1 | E1 “béo phì” → E2 “khám” | Chưa rõ — cần chốt (CHUA_RO) |
| R2 | E1 “béo phì” → E3 “điều trị” | Được điều trị bằng phương pháp (treated_by_procedure) |

### Cần chốt

- GENERIC_INTERVENTION: cần chốt việc giữ hành động điều trị/chẩn đoán chung khi không nêu phương pháp cụ thể.
- UNRESOLVED_RE: còn cặp CHUA_RO; tuyệt đối không đổi thành NO_RELATION khi xuất huấn luyện.

Nguồn: VietMed-NER train, dòng 1144 (từ 0).

## VM600-138

**Đoạn gốc:** một loại mầm bệnh cụ thể đã nhân lên và tồn tại trong cơ thể trong một thời gian dài rất lâu sau khi mầm bệnh này đã bị

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E2 | cơ thể | Bộ phận cơ thể (BODY_PART) | [54, 60) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Thay đổi NER

- E1 “mầm bệnh” CONDITION [9, 17) → ∅
- E3 “mầm bệnh” CONDITION [101, 109) → ∅

Nguồn: VietMed-NER train, dòng 1145 (từ 0).

## VM600-139

**Đoạn gốc:** trắng nè từ hoa lan hoặc từ cam thảo hoặc là gần đây là có những cái sản phẩm mà có chứa chiết xuất từ thực vật

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | hoa lan | Thuốc/dược chất (DRUG) | [12, 19) |
| E2 | cam thảo | Thuốc/dược chất (DRUG) | [28, 36) |
| E3 | chiết xuất từ thực vật | Thuốc/dược chất (DRUG) | [89, 111) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- ONTOLOGY_SCOPE: cần chốt phạm vi thuốc/dược chất so với mỹ phẩm, thực phẩm, hóa chất nội sinh hoặc hệ vi sinh; giữ ánh xạ nguồn khi chưa có quy ước đủ rõ.

Nguồn: VietMed-NER train, dòng 1158 (từ 0).

## VM600-140

**Đoạn gốc:** là rối loạn mỡ máu đúng không bác thế và bác cũng có hỏi là cái số cái số hát cái

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | rối loạn mỡ máu | Bệnh hoặc triệu chứng (CONDITION) | [3, 18) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

Nguồn: VietMed-NER train, dòng 1172 (từ 0).

## VM600-141

**Đoạn gốc:** đồng hồ là nó không còn trong người mình nữa rồi như vậy khi mà chúng ta ngưng thuốc hai ngày đối với noark hoặc là bốn năm

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | thuốc | Thuốc/dược chất (DRUG) | [79, 84) |
| E2 | noark | Thuốc/dược chất (DRUG) | [102, 107) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- CONTEXT_OR_TRANSCRIPT: câu bị cắt, tham chiếu/mục đích chưa rõ hoặc nghi lỗi phiên âm; cần xem ngữ cảnh/audio gốc, không tự sửa văn bản.

### Thay đổi NER

- E1 “ngưng thuốc” PROCEDURE [73, 84) → E1 “thuốc” DRUG [79, 84)

Nguồn: VietMed-NER train, dòng 1173 (từ 0).

## VM600-142

**Đoạn gốc:** mạch máu của chúng ta lưu thông ở mức độ nó rất là ít và đã chậm bản thân các cái khớp của chúng ta nó thông thường là

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | mạch máu | Bộ phận cơ thể (BODY_PART) | [0, 8) |
| E4 | khớp | Bộ phận cơ thể (BODY_PART) | [82, 86) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- CONTEXT_OR_TRANSCRIPT: câu bị cắt, tham chiếu/mục đích chưa rõ hoặc nghi lỗi phiên âm; cần xem ngữ cảnh/audio gốc, không tự sửa văn bản.

### Thay đổi NER

- E2 “mức độ” DOSAGE [34, 40) → ∅
- E4 “các cái khớp” BODY_PART [74, 86) → E4 “khớp” BODY_PART [82, 86)
- E3 “chậm” CONDITION [60, 64) → ∅

Nguồn: VietMed-NER train, dòng 1174 (từ 0).

## VM600-143

**Đoạn gốc:** ứng đầu tiên của cơ thể đổi lại vi khuẩn đường ruột giúp giữ cho hệ miễn dịch

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | cơ thể | Bộ phận cơ thể (BODY_PART) | [17, 23) |
| E3 | đường ruột | Bộ phận cơ thể (BODY_PART) | [41, 51) |
| E4 | hệ miễn dịch | Bộ phận cơ thể (BODY_PART) | [65, 77) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Thay đổi NER

- E2 “vi khuẩn” CONDITION [32, 40) → ∅

Nguồn: VietMed-NER train, dòng 1176 (từ 0).

## VM600-144

**Đoạn gốc:** đề án thuộc chương trình quốc gia vào thế và đối với sản phẩm này thì nó gồm

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

Không có thực thể thuộc sáu loại được giữ trong bản rà soát.

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

Nguồn: VietMed-NER train, dòng 1178 (từ 0).

## VM600-145

**Đoạn gốc:** có khả năng là nó trầm cảm và cái tâm lý mà họ bị kỳ thị bản thân họ bị tự ti họ

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | trầm cảm | Bệnh hoặc triệu chứng (CONDITION) | [18, 26) |
| E2 | tự ti | Bệnh hoặc triệu chứng (CONDITION) | [72, 77) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- SYMPTOM_SCOPE: cần phân biệt cảm xúc thông thường với triệu chứng lâm sàng theo quy ước dự án.

Nguồn: VietMed-NER train, dòng 1181 (từ 0).

## VM600-146

**Đoạn gốc:** chúng ta cho dầu là dầu mà chúng ta cho vào cuối bữa ăn để mà cũng không

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

Không có thực thể thuộc sáu loại được giữ trong bản rà soát.

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

Nguồn: VietMed-NER train, dòng 1184 (từ 0).

## VM600-147

**Đoạn gốc:** nó cũng sẽ làm cho hạn chế dòng máu đi đến cái mạch vành đó và dẫn đến những cái tình trạng thiểu năng vành và khi

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | dòng máu | Bộ phận cơ thể (BODY_PART) | [27, 35) |
| E2 | mạch vành | Bộ phận cơ thể (BODY_PART) | [47, 56) |
| E3 | thiểu năng vành | Bệnh hoặc triệu chứng (CONDITION) | [92, 107) |

### RE

| Mã | Cặp có hướng | Kết luận đề xuất |
|---|---|---|
| R1 | E3 “thiểu năng vành” → E1 “dòng máu” | Không có quan hệ thuộc 5 loại (NO_RELATION) |
| R2 | E3 “thiểu năng vành” → E2 “mạch vành” | Chưa rõ — cần chốt (CHUA_RO) |

### Cần chốt

- UNRESOLVED_RE: còn cặp CHUA_RO; tuyệt đối không đổi thành NO_RELATION khi xuất huấn luyện.

### Thay đổi NER

- E2 “mạch” BODY_PART [47, 51) → E2 “mạch vành” BODY_PART [47, 56)

Nguồn: VietMed-NER train, dòng 1195 (từ 0).

## VM600-148

**Đoạn gốc:** ạ chúng ta phải phòng ngừa cho những cái chuyện đó xảy ra giống như lúc nãy tôi nói rằng là đi xe đạp về rất tốt nhưng

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

Không có thực thể thuộc sáu loại được giữ trong bản rà soát.

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Thay đổi NER

- E1 “phòng ngừa” DRUG [16, 26) → ∅

Nguồn: VietMed-NER train, dòng 1201 (từ 0).

## VM600-149

**Đoạn gốc:** cô không có nêu các bệnh nền nhưng mà cô lại nói là cái bệnh của cô là phải uống thuốc định kỳ hàng tháng nhưng mà do

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | bệnh nền | Bệnh hoặc triệu chứng (CONDITION) | [20, 28) |
| E2 | thuốc | Thuốc/dược chất (DRUG) | [81, 86) |

### RE

| Mã | Cặp có hướng | Kết luận đề xuất |
|---|---|---|
| R1 | E1 “bệnh nền” → E2 “thuốc” | Chưa rõ — cần chốt (CHUA_RO) |

### Cần chốt

- CONTEXT_OR_TRANSCRIPT: câu bị cắt, tham chiếu/mục đích chưa rõ hoặc nghi lỗi phiên âm; cần xem ngữ cảnh/audio gốc, không tự sửa văn bản.
- GENERIC_MENTION: cần chốt có giữ bệnh/triệu chứng/biến chứng chung và tham chiếu không định danh trong NER hay không.
- UNRESOLVED_RE: còn cặp CHUA_RO; tuyệt đối không đổi thành NO_RELATION khi xuất huấn luyện.

### Thay đổi NER

- E2 “uống thuốc” PROCEDURE [76, 86) → E2 “thuốc” DRUG [81, 86)

Nguồn: VietMed-NER train, dòng 1208 (từ 0).

## VM600-150

**Đoạn gốc:** chúng ta muốn tìm mua đông trùng hạ thảo hoặc là những sản phẩm có đông trùng hạ

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | đông trùng hạ thảo | Thuốc/dược chất (DRUG) | [22, 40) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- ONTOLOGY_SCOPE: cần chốt phạm vi thuốc/dược chất so với mỹ phẩm, thực phẩm, hóa chất nội sinh hoặc hệ vi sinh; giữ ánh xạ nguồn khi chưa có quy ước đủ rõ.

Nguồn: VietMed-NER train, dòng 1219 (từ 0).

## VM600-151

**Đoạn gốc:** là tránh được cái biến cố bị đột quỵ do tình trạng rung nhĩ gây ra như vậy là

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | đột quỵ | Bệnh hoặc triệu chứng (CONDITION) | [29, 36) |
| E2 | rung nhĩ | Bệnh hoặc triệu chứng (CONDITION) | [51, 59) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

Nguồn: VietMed-NER train, dòng 1236 (từ 0).

## VM600-152

**Đoạn gốc:** để giúp cho quý vị và các bạn những ai mà đang gặp phải cái triệu chứng như là huyết áp cao nè mỡ máu cao nè tê bì

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E2 | huyết áp cao | Bệnh hoặc triệu chứng (CONDITION) | [79, 91) |
| E4 | mỡ máu cao | Bệnh hoặc triệu chứng (CONDITION) | [95, 105) |
| E6 | tê bì | Bệnh hoặc triệu chứng (CONDITION) | [109, 114) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Thay đổi NER

- E3 “cao” DOSAGE [88, 91) → ∅
- E5 “cao” DOSAGE [102, 105) → ∅
- E1 “triệu chứng” CONDITION [60, 71) → ∅
- E2 “huyết áp” CONDITION [79, 87) → E2 “huyết áp cao” CONDITION [79, 91)
- E4 “mỡ máu” CONDITION [95, 101) → E4 “mỡ máu cao” CONDITION [95, 105)

Nguồn: VietMed-NER train, dòng 1244 (từ 0).

## VM600-153

**Đoạn gốc:** người huyết áp cao mỡ máu cao tim mạch hỗ trợ giảm nguy cơ xơ vữa động mạch hỗ trợ giảm đau đầu chóng mặt mất ngủ tê bì

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | huyết áp cao | Bệnh hoặc triệu chứng (CONDITION) | [6, 18) |
| E3 | mỡ máu cao | Bệnh hoặc triệu chứng (CONDITION) | [19, 29) |
| E5 | tim mạch | Bộ phận cơ thể (BODY_PART) | [30, 38) |
| E7 | xơ vữa động mạch | Bệnh hoặc triệu chứng (CONDITION) | [59, 75) |
| E9 | đau đầu | Bệnh hoặc triệu chứng (CONDITION) | [88, 95) |
| E10 | chóng mặt | Bệnh hoặc triệu chứng (CONDITION) | [96, 105) |
| E11 | mất ngủ | Bệnh hoặc triệu chứng (CONDITION) | [106, 113) |
| E12 | tê bì | Bệnh hoặc triệu chứng (CONDITION) | [114, 119) |

### RE

| Mã | Cặp có hướng | Kết luận đề xuất |
|---|---|---|
| R1 | E1 “huyết áp cao” → E5 “tim mạch” | Không có quan hệ thuộc 5 loại (NO_RELATION) |
| R2 | E3 “mỡ máu cao” → E5 “tim mạch” | Không có quan hệ thuộc 5 loại (NO_RELATION) |
| R3 | E7 “xơ vữa động mạch” → E5 “tim mạch” | Không có quan hệ thuộc 5 loại (NO_RELATION) |
| R4 | E9 “đau đầu” → E5 “tim mạch” | Không có quan hệ thuộc 5 loại (NO_RELATION) |
| R5 | E10 “chóng mặt” → E5 “tim mạch” | Không có quan hệ thuộc 5 loại (NO_RELATION) |
| R6 | E11 “mất ngủ” → E5 “tim mạch” | Không có quan hệ thuộc 5 loại (NO_RELATION) |
| R7 | E12 “tê bì” → E5 “tim mạch” | Không có quan hệ thuộc 5 loại (NO_RELATION) |

### Cần chốt

- CONTEXT_OR_TRANSCRIPT: câu bị cắt, tham chiếu/mục đích chưa rõ hoặc nghi lỗi phiên âm; cần xem ngữ cảnh/audio gốc, không tự sửa văn bản.

### Thay đổi NER

- E2 “cao” DOSAGE [15, 18) → ∅
- E4 “cao” DOSAGE [26, 29) → ∅
- E6 “hỗ trợ” PROCEDURE [39, 45) → ∅
- E8 “hỗ trợ” PROCEDURE [76, 82) → ∅
- E1 “huyết áp” CONDITION [6, 14) → E1 “huyết áp cao” CONDITION [6, 18)
- E3 “mỡ máu” CONDITION [19, 25) → E3 “mỡ máu cao” CONDITION [19, 29)

Nguồn: VietMed-NER train, dòng 1255 (từ 0).

## VM600-154

**Đoạn gốc:** sĩ nội và bác sĩ ngoại thần kinh sẽ làm một cái chương trình là lấy cái hình ảnh mri của ngày trước mổ đó mình sẽ

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E2 | mri | Xét nghiệm hoặc thăm khám (TEST) | [81, 84) |
| E3 | mổ | Thủ thuật hoặc điều trị (PROCEDURE) | [100, 102) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Thay đổi NER

- E1 “thần kinh” BODY_PART [23, 32) → ∅

Nguồn: VietMed-NER train, dòng 1270 (từ 0).

## VM600-155

**Đoạn gốc:** cái thông tin họ được chưa đầy đủ làm cho nhận thức của họ nó chưa được sâu sắc thì họ sẽ chưa có đủ niềm tin

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

Không có thực thể thuộc sáu loại được giữ trong bản rà soát.

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

Nguồn: VietMed-NER train, dòng 1273 (từ 0).

## VM600-156

**Đoạn gốc:** vitamin k những loại thức ăn nào mà chứa ít vitamin k thì chúng ta sẽ biết được và chúng ta không nên ăn quá nhiều loại đó

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | vitamin k | Thuốc/dược chất (DRUG) | [0, 9) |
| E2 | vitamin k | Thuốc/dược chất (DRUG) | [44, 53) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- SCOPE_CONFIRMATION: cần xác nhận quy ước về thuốc/dược chất, can thiệp không dùng thuốc, thiết bị, tác nhân hoặc hoạt động thăm khám; không coi ánh xạ nguồn là xác nhận chuyên gia.

Nguồn: VietMed-NER train, dòng 1279 (từ 0).

## VM600-157

**Đoạn gốc:** nên nó có thể giết cả các cái tế bào lành và chính vì vậy làm cho các chức năng của cơ quan bị tổn thương và đặc

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | tế bào | Bộ phận cơ thể (BODY_PART) | [30, 36) |
| E4 | cơ quan | Bộ phận cơ thể (BODY_PART) | [84, 91) |
| E3 | tổn thương | Bệnh hoặc triệu chứng (CONDITION) | [95, 105) |

### RE

| Mã | Cặp có hướng | Kết luận đề xuất |
|---|---|---|
| R1 | E3 “tổn thương” → E1 “tế bào” | Không có quan hệ thuộc 5 loại (NO_RELATION) |
| R2 | E3 “tổn thương” → E4 “cơ quan” | Có vị trí ở (located_at) |

### Thay đổi NER

- E2 “bị” CONDITION [92, 94) → ∅
- ∅ → E4 “cơ quan” BODY_PART [84, 91)

Nguồn: VietMed-NER train, dòng 1281 (từ 0).

## VM600-158

**Đoạn gốc:** chế độ ăn uống và sinh hoạt nó lành mạnh giúp cho việc nâng cao hiệu quả tuân thủ

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

Không có thực thể thuộc sáu loại được giữ trong bản rà soát.

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Thay đổi NER

- E1 “cao” DOSAGE [60, 63) → ∅
- E2 “tuân thủ” DRUG [73, 81) → ∅

Nguồn: VietMed-NER train, dòng 1284 (từ 0).

## VM600-159

**Đoạn gốc:** a nếu có được vitamina a nữa thì càng tốt này có selen có kẽm như là chúng ta vừa chia sẻ về cái hai cái chất mà chống oxy hóa

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E4 | vitamina a | Thuốc/dược chất (DRUG) | [14, 24) |
| E1 | selen | Thuốc/dược chất (DRUG) | [49, 54) |
| E2 | kẽm | Thuốc/dược chất (DRUG) | [58, 61) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- ONTOLOGY_SCOPE: cần chốt phạm vi thuốc/dược chất so với mỹ phẩm, thực phẩm, hóa chất nội sinh hoặc hệ vi sinh; giữ ánh xạ nguồn khi chưa có quy ước đủ rõ.

### Thay đổi NER

- E3 “oxy” DRUG [119, 122) → ∅
- ∅ → E4 “vitamina a” DRUG [14, 24)

Nguồn: VietMed-NER train, dòng 1295 (từ 0).

## VM600-160

**Đoạn gốc:** thành phần như immunesoyz này hòe hoa này l-carnitine fumarate để hoàng liên này với cả đan sâm nữa thì rất tốt

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | immunesoyz | Thuốc/dược chất (DRUG) | [15, 25) |
| E2 | hòe hoa | Thuốc/dược chất (DRUG) | [30, 37) |
| E3 | l-carnitine fumarate | Thuốc/dược chất (DRUG) | [42, 62) |
| E5 | hoàng liên | Thuốc/dược chất (DRUG) | [66, 76) |
| E6 | đan sâm | Thuốc/dược chất (DRUG) | [88, 95) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- ONTOLOGY_SCOPE: cần chốt phạm vi thuốc/dược chất so với mỹ phẩm, thực phẩm, hóa chất nội sinh hoặc hệ vi sinh; giữ ánh xạ nguồn khi chưa có quy ước đủ rõ.

### Thay đổi NER

- E3 “l-carnitine” DRUG [42, 53) → E3 “l-carnitine fumarate” DRUG [42, 62)
- E4 “fumarate” DRUG [54, 62) → ∅

Nguồn: VietMed-NER train, dòng 1314 (từ 0).

## VM600-161

**Đoạn gốc:** khác nhau như thế nào giữa các quần thể trên khắp thế giới và sự khác nhau này gây ra bởi sự khác biệt trong chế độ ăn

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

Không có thực thể thuộc sáu loại được giữ trong bản rà soát.

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

Nguồn: VietMed-NER train, dòng 1315 (từ 0).

## VM600-162

**Đoạn gốc:** hợp này đó chính là tế bào ung thư thì đó sẽ sử dụng các cái chất dinh dưỡng dự trữ

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | tế bào ung thư | Bệnh hoặc triệu chứng (CONDITION) | [20, 34) |
| E2 | chất dinh dưỡng | Thuốc/dược chất (DRUG) | [61, 76) |

### RE

| Mã | Cặp có hướng | Kết luận đề xuất |
|---|---|---|
| R1 | E1 “tế bào ung thư” → E2 “chất dinh dưỡng” | Không có quan hệ thuộc 5 loại (NO_RELATION) |

### Cần chốt

- ONTOLOGY_SCOPE: cần chốt phạm vi thuốc/dược chất so với mỹ phẩm, thực phẩm, hóa chất nội sinh hoặc hệ vi sinh; giữ ánh xạ nguồn khi chưa có quy ước đủ rõ.

Nguồn: VietMed-NER train, dòng 1344 (từ 0).

## VM600-163

**Đoạn gốc:** tử vong đó rất là nhanh trong vòng mười

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | tử vong | Bệnh hoặc triệu chứng (CONDITION) | [0, 7) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

Nguồn: VietMed-NER train, dòng 1351 (từ 0).

## VM600-164

**Đoạn gốc:** biệt là mỡ động vật thế và chúng ta cũng nên tăng cường rau xanh hoa quả tươi để cung cấp các vitamin các khoáng chất và

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | vitamin | Thuốc/dược chất (DRUG) | [94, 101) |
| E2 | khoáng chất | Thuốc/dược chất (DRUG) | [106, 117) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- ONTOLOGY_SCOPE: cần chốt phạm vi thuốc/dược chất so với mỹ phẩm, thực phẩm, hóa chất nội sinh hoặc hệ vi sinh; giữ ánh xạ nguồn khi chưa có quy ước đủ rõ.

Nguồn: VietMed-NER train, dòng 1356 (từ 0).

## VM600-165

**Đoạn gốc:** đến mình đau đầu rồi hoa mắt chóng mặt này ở kia ở mạch vành hay là ở tim

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | đau đầu | Bệnh hoặc triệu chứng (CONDITION) | [9, 16) |
| E2 | hoa mắt | Bệnh hoặc triệu chứng (CONDITION) | [21, 28) |
| E3 | chóng mặt | Bệnh hoặc triệu chứng (CONDITION) | [29, 38) |
| E4 | mạch vành | Bộ phận cơ thể (BODY_PART) | [51, 60) |
| E5 | tim | Bộ phận cơ thể (BODY_PART) | [70, 73) |

### RE

| Mã | Cặp có hướng | Kết luận đề xuất |
|---|---|---|
| R1 | E1 “đau đầu” → E4 “mạch vành” | Không có quan hệ thuộc 5 loại (NO_RELATION) |
| R2 | E1 “đau đầu” → E5 “tim” | Không có quan hệ thuộc 5 loại (NO_RELATION) |
| R3 | E2 “hoa mắt” → E4 “mạch vành” | Không có quan hệ thuộc 5 loại (NO_RELATION) |
| R4 | E2 “hoa mắt” → E5 “tim” | Không có quan hệ thuộc 5 loại (NO_RELATION) |
| R5 | E3 “chóng mặt” → E4 “mạch vành” | Không có quan hệ thuộc 5 loại (NO_RELATION) |
| R6 | E3 “chóng mặt” → E5 “tim” | Không có quan hệ thuộc 5 loại (NO_RELATION) |

### Cần chốt

- CONTEXT_OR_TRANSCRIPT: câu bị cắt, tham chiếu/mục đích chưa rõ hoặc nghi lỗi phiên âm; cần xem ngữ cảnh/audio gốc, không tự sửa văn bản.

### Thay đổi NER

- E4 “mạch” BODY_PART [51, 55) → E4 “mạch vành” BODY_PART [51, 60)

Nguồn: VietMed-NER train, dòng 1357 (từ 0).

## VM600-166

**Đoạn gốc:** được hay không thì từ hồi đó nay sức khỏe của ông mới mổ cho nên là tôi và

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | mổ | Thủ thuật hoặc điều trị (PROCEDURE) | [54, 56) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

Nguồn: VietMed-NER train, dòng 1363 (từ 0).

## VM600-167

**Đoạn gốc:** cái xơ vữa xơ vữa động mạch chi thì có thể bệnh nhân có cảm nhận như là các cái tê bì kiến bò châm chích bằng tay bằng

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | xơ vữa | Bệnh hoặc triệu chứng (CONDITION) | [4, 10) |
| E2 | xơ vữa động mạch chi | Bệnh hoặc triệu chứng (CONDITION) | [11, 31) |
| E3 | tê bì kiến bò | Bệnh hoặc triệu chứng (CONDITION) | [80, 93) |
| E4 | châm chích | Bệnh hoặc triệu chứng (CONDITION) | [94, 104) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- CONTEXT_OR_TRANSCRIPT: câu bị cắt, tham chiếu/mục đích chưa rõ hoặc nghi lỗi phiên âm; cần xem ngữ cảnh/audio gốc, không tự sửa văn bản.

Nguồn: VietMed-NER train, dòng 1364 (từ 0).

## VM600-168

**Đoạn gốc:** tác trực tiếp nên trong quá trình mà các bác sĩ trao đổi với những nội dung hấp dẫn và thú vị thì quý vị có bất kỳ những

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

Không có thực thể thuộc sáu loại được giữ trong bản rà soát.

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

Nguồn: VietMed-NER train, dòng 1383 (từ 0).

## VM600-169

**Đoạn gốc:** một tình trạng rung nhĩ thì tim của chúng ta sẽ đập và rất là nhanh có thể

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | rung nhĩ | Bệnh hoặc triệu chứng (CONDITION) | [15, 23) |
| E2 | tim | Bộ phận cơ thể (BODY_PART) | [28, 31) |

### RE

| Mã | Cặp có hướng | Kết luận đề xuất |
|---|---|---|
| R1 | E1 “rung nhĩ” → E2 “tim” | Chưa rõ — cần chốt (CHUA_RO) |

### Cần chốt

- UNRESOLVED_RE: còn cặp CHUA_RO; tuyệt đối không đổi thành NO_RELATION khi xuất huấn luyện.

Nguồn: VietMed-NER train, dòng 1407 (từ 0).

## VM600-170

**Đoạn gốc:** bị nhồi máu cơ tim cũng rất là cao nếu mà chúng ta vẫn không có một cái chế độ ở sinh hoạt điều trị một cách khoa học

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | nhồi máu cơ tim | Bệnh hoặc triệu chứng (CONDITION) | [3, 18) |
| E3 | điều trị | Thủ thuật hoặc điều trị (PROCEDURE) | [91, 99) |

### RE

| Mã | Cặp có hướng | Kết luận đề xuất |
|---|---|---|
| R1 | E1 “nhồi máu cơ tim” → E3 “điều trị” | Chưa rõ — cần chốt (CHUA_RO) |

### Cần chốt

- CONTEXT_OR_TRANSCRIPT: câu bị cắt, tham chiếu/mục đích chưa rõ hoặc nghi lỗi phiên âm; cần xem ngữ cảnh/audio gốc, không tự sửa văn bản.
- GENERIC_INTERVENTION: cần chốt việc giữ hành động điều trị/chẩn đoán chung khi không nêu phương pháp cụ thể.
- UNRESOLVED_RE: còn cặp CHUA_RO; tuyệt đối không đổi thành NO_RELATION khi xuất huấn luyện.

### Thay đổi NER

- E2 “cao” DOSAGE [31, 34) → ∅

Nguồn: VietMed-NER train, dòng 1419 (từ 0).

## VM600-171

**Đoạn gốc:** mạch vành huyết áp cao nhiều khi nhớ nhớ quên quên bị tiền đình đau đầu chóng mặt và đã từng dùng rất là nhiều sản phẩm

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | mạch vành | Bộ phận cơ thể (BODY_PART) | [0, 9) |
| E2 | huyết áp cao | Bệnh hoặc triệu chứng (CONDITION) | [10, 22) |
| E4 | nhớ nhớ quên quên | Bệnh hoặc triệu chứng (CONDITION) | [33, 50) |
| E5 | tiền đình | Bệnh hoặc triệu chứng (CONDITION) | [54, 63) |
| E6 | đau đầu | Bệnh hoặc triệu chứng (CONDITION) | [64, 71) |
| E7 | chóng mặt | Bệnh hoặc triệu chứng (CONDITION) | [72, 81) |

### RE

| Mã | Cặp có hướng | Kết luận đề xuất |
|---|---|---|
| R1 | E2 “huyết áp cao” → E1 “mạch vành” | Không có quan hệ thuộc 5 loại (NO_RELATION) |
| R2 | E4 “nhớ nhớ quên quên” → E1 “mạch vành” | Không có quan hệ thuộc 5 loại (NO_RELATION) |
| R3 | E5 “tiền đình” → E1 “mạch vành” | Không có quan hệ thuộc 5 loại (NO_RELATION) |
| R4 | E6 “đau đầu” → E1 “mạch vành” | Không có quan hệ thuộc 5 loại (NO_RELATION) |
| R5 | E7 “chóng mặt” → E1 “mạch vành” | Không có quan hệ thuộc 5 loại (NO_RELATION) |

### Cần chốt

- CONTEXT_OR_TRANSCRIPT: câu bị cắt, tham chiếu/mục đích chưa rõ hoặc nghi lỗi phiên âm; cần xem ngữ cảnh/audio gốc, không tự sửa văn bản.

### Thay đổi NER

- E3 “cao” DOSAGE [19, 22) → ∅
- E1 “mạch” BODY_PART [0, 4) → E1 “mạch vành” BODY_PART [0, 9)
- E2 “huyết áp” CONDITION [10, 18) → E2 “huyết áp cao” CONDITION [10, 22)

Nguồn: VietMed-NER train, dòng 1430 (từ 0).

## VM600-172

**Đoạn gốc:** lớn tuổi thì cái cái nguy cơ đột quỵ là sẽ rõ ràng là sẽ tăng lên và như vậy

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | đột quỵ | Bệnh hoặc triệu chứng (CONDITION) | [29, 36) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

Nguồn: VietMed-NER train, dòng 1450 (từ 0).

## VM600-173

**Đoạn gốc:** nó huyết áp nó tăng cao vì khi chúng ta biết càng huyết áp tăng cao vâng nó càng bị bị dễ bị tai biến chị nhé các cái

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | huyết áp nó tăng cao | Bệnh hoặc triệu chứng (CONDITION) | [3, 23) |
| E3 | huyết áp tăng cao | Bệnh hoặc triệu chứng (CONDITION) | [50, 67) |
| E5 | tai biến | Bệnh hoặc triệu chứng (CONDITION) | [93, 101) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Thay đổi NER

- E2 “cao” DOSAGE [20, 23) → ∅
- E4 “cao” DOSAGE [64, 67) → ∅
- E1 “huyết áp” CONDITION [3, 11) → E1 “huyết áp nó tăng cao” CONDITION [3, 23)
- E3 “huyết áp” CONDITION [50, 58) → E3 “huyết áp tăng cao” CONDITION [50, 67)

Nguồn: VietMed-NER train, dòng 1466 (từ 0).

## VM600-174

**Đoạn gốc:** căn bệnh béo phì cũng như là lợi ích của việc điều trị giảm cân một cách an toàn thưa quý vị hiện nay thì chúng ta nhận

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | béo phì | Bệnh hoặc triệu chứng (CONDITION) | [9, 16) |
| E2 | điều trị giảm cân | Thủ thuật hoặc điều trị (PROCEDURE) | [46, 63) |

### RE

| Mã | Cặp có hướng | Kết luận đề xuất |
|---|---|---|
| R1 | E1 “béo phì” → E2 “điều trị giảm cân” | Được điều trị bằng phương pháp (treated_by_procedure) |

### Thay đổi NER

- E2 “điều trị” PROCEDURE [46, 54) → E2 “điều trị giảm cân” PROCEDURE [46, 63)

Nguồn: VietMed-NER train, dòng 1474 (từ 0).

## VM600-175

**Đoạn gốc:** quay trở lại với chương trình thì có rất là nhiều của bệnh nhân ung thư băn khoăn

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | ung thư | Bệnh hoặc triệu chứng (CONDITION) | [64, 71) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

Nguồn: VietMed-NER train, dòng 1481 (từ 0).

## VM600-176

**Đoạn gốc:** gan thận nó phải xử lý đào thải hoặc là gọi là chuyển hóa các cái chất này thì nó cũng lại phải chịu gánh nặng cho nên

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | gan | Bộ phận cơ thể (BODY_PART) | [0, 3) |
| E2 | thận | Bộ phận cơ thể (BODY_PART) | [4, 8) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Thay đổi NER

- E3 “chuyển hóa” TEST [47, 57) → ∅

Nguồn: VietMed-NER train, dòng 1498 (từ 0).

## VM600-177

**Đoạn gốc:** và bởi vì sao bao giờ khi mà cái vấn đề mà phẫu thuật sọ não hoặc là bất kỳ một cái phẫu thuật nào bao giờ các bác sĩ

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | phẫu thuật | Thủ thuật hoặc điều trị (PROCEDURE) | [43, 53) |
| E2 | sọ não | Bộ phận cơ thể (BODY_PART) | [54, 60) |
| E4 | phẫu thuật | Thủ thuật hoặc điều trị (PROCEDURE) | [84, 94) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Thay đổi NER

- E2 “sọ” BODY_PART [54, 56) → E2 “sọ não” BODY_PART [54, 60)
- E3 “não” BODY_PART [57, 60) → ∅

Nguồn: VietMed-NER train, dòng 1505 (từ 0).

## VM600-178

**Đoạn gốc:** đổi thái độ họ đẩy mà họ có được một cái hành vi tốt hơn

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

Không có thực thể thuộc sáu loại được giữ trong bản rà soát.

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

Nguồn: VietMed-NER train, dòng 1506 (từ 0).

## VM600-179

**Đoạn gốc:** cái mảng vữa xơ và mảng vữa xơ thì chúng ta cứ tưởng tượng nó là những cái mảng bám ví dụ cái ống nước chẳng hạn nó sẽ

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | mảng vữa xơ | Bệnh hoặc triệu chứng (CONDITION) | [4, 15) |
| E2 | mảng vữa xơ | Bệnh hoặc triệu chứng (CONDITION) | [19, 30) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Thay đổi NER

- E1 “mảng vữa xơ” BODY_PART [4, 15) → E1 “mảng vữa xơ” CONDITION [4, 15)
- E2 “mảng vữa xơ” BODY_PART [19, 30) → E2 “mảng vữa xơ” CONDITION [19, 30)

Nguồn: VietMed-NER train, dòng 1508 (từ 0).

## VM600-180

**Đoạn gốc:** vấn như thế nào đó về sức khỏe bởi vì hiện nay là công nghệ nó rất là rất làm

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

Không có thực thể thuộc sáu loại được giữ trong bản rà soát.

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

Nguồn: VietMed-NER train, dòng 1511 (từ 0).

## VM600-181

**Đoạn gốc:** thấy có cái cơ chế tác dụng và có cái hiệu quả nó tương đương với nhau nhưng mà kga1 thì nó lại không gây ra các cái

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | kga1 | Thuốc/dược chất (DRUG) | [80, 84) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- ONTOLOGY_SCOPE: cần chốt phạm vi thuốc/dược chất so với mỹ phẩm, thực phẩm, hóa chất nội sinh hoặc hệ vi sinh; giữ ánh xạ nguồn khi chưa có quy ước đủ rõ.

Nguồn: VietMed-NER train, dòng 1520 (từ 0).

## VM600-182

**Đoạn gốc:** thể khác để ký sinh vào cụ thể là con người chúng ta và nó được mang đi cũng bởi con người của chúng ta khi mà chúng

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | ký sinh | Bệnh hoặc triệu chứng (CONDITION) | [12, 19) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

Nguồn: VietMed-NER train, dòng 1522 (từ 0).

## VM600-183

**Đoạn gốc:** não sâu để cho nó có hiệu quả hoặc là tốt mà có thể đi làm thì nó đòi hỏi sẽ

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | não | Bộ phận cơ thể (BODY_PART) | [0, 3) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- CONTEXT_OR_TRANSCRIPT: câu bị cắt, tham chiếu/mục đích chưa rõ hoặc nghi lỗi phiên âm; cần xem ngữ cảnh/audio gốc, không tự sửa văn bản.

Nguồn: VietMed-NER train, dòng 1532 (từ 0).

## VM600-184

**Đoạn gốc:** chúng ta khi mà chưa có tây y đến đất nước chúng ta từ thế kỷ mười bảy mười tám thì cha ông chúng ta điều trị người ta bằng cái

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | điều trị | Thủ thuật hoặc điều trị (PROCEDURE) | [101, 109) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- GENERIC_INTERVENTION: cần chốt việc giữ hành động điều trị/chẩn đoán chung khi không nêu phương pháp cụ thể.

Nguồn: VietMed-NER train, dòng 1533 (từ 0).

## VM600-185

**Đoạn gốc:** của chúng ta và riêng mái tóc thì sao nè nó tác động vô cái nang tóc nó làm cho cái nang tóc nó phát triển không được

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | mái tóc | Bộ phận cơ thể (BODY_PART) | [22, 29) |
| E2 | nang tóc | Bộ phận cơ thể (BODY_PART) | [60, 68) |
| E3 | nang tóc | Bộ phận cơ thể (BODY_PART) | [84, 92) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

Nguồn: VietMed-NER train, dòng 1554 (từ 0).

## VM600-186

**Đoạn gốc:** tình trạng bệnh lý tim mạch huyết áp cao như thế nào mời bác chia sẻ với chương trình vâng xin chào chị ạ dạ

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E4 | bệnh lý tim mạch | Bệnh hoặc triệu chứng (CONDITION) | [11, 27) |
| E2 | huyết áp cao | Bệnh hoặc triệu chứng (CONDITION) | [28, 40) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- CONTEXT_OR_TRANSCRIPT: câu bị cắt, tham chiếu/mục đích chưa rõ hoặc nghi lỗi phiên âm; cần xem ngữ cảnh/audio gốc, không tự sửa văn bản.

### Thay đổi NER

- E3 “cao” DOSAGE [37, 40) → ∅
- E2 “huyết áp” CONDITION [28, 36) → E2 “huyết áp cao” CONDITION [28, 40)
- ∅ → E4 “bệnh lý” CONDITION [11, 18)
- E4 “bệnh lý” CONDITION [11, 18) → E4 “bệnh lý tim mạch” CONDITION [11, 27)
- E1 “tim mạch” BODY_PART [19, 27) → ∅

Nguồn: VietMed-NER train, dòng 1557 (từ 0).

## VM600-187

**Đoạn gốc:** rồi đi làm đi làm thì gặp sếp là phân công nó cũng không có phù hợp nói cái

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

Không có thực thể thuộc sáu loại được giữ trong bản rà soát.

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

Nguồn: VietMed-NER train, dòng 1565 (từ 0).

## VM600-188

**Đoạn gốc:** tính hay còn gọi là gì ạ những cái nhóm bệnh lý mà nó có liên quan đến cái bệnh lý khớp mà nó có cái nền tảng lâu dài và

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | bệnh lý | Bệnh hoặc triệu chứng (CONDITION) | [40, 47) |
| E2 | bệnh lý khớp | Bệnh hoặc triệu chứng (CONDITION) | [75, 87) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- GENERIC_MENTION: cần chốt có giữ bệnh/triệu chứng/biến chứng chung và tham chiếu không định danh trong NER hay không.

### Thay đổi NER

- E2 “bệnh lý” CONDITION [75, 82) → E2 “bệnh lý khớp” CONDITION [75, 87)
- E3 “khớp” BODY_PART [83, 87) → ∅

Nguồn: VietMed-NER train, dòng 1603 (từ 0).

## VM600-189

**Đoạn gốc:** bệnh lý của mình để có thể điều trị chính vì vậy thì qua trước chương trình của bệnh

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | bệnh lý | Bệnh hoặc triệu chứng (CONDITION) | [0, 7) |
| E2 | điều trị | Thủ thuật hoặc điều trị (PROCEDURE) | [27, 35) |

### RE

| Mã | Cặp có hướng | Kết luận đề xuất |
|---|---|---|
| R1 | E1 “bệnh lý” → E2 “điều trị” | Được điều trị bằng phương pháp (treated_by_procedure) |

### Cần chốt

- GENERIC_INTERVENTION: cần chốt việc giữ hành động điều trị/chẩn đoán chung khi không nêu phương pháp cụ thể.
- GENERIC_MENTION: cần chốt có giữ bệnh/triệu chứng/biến chứng chung và tham chiếu không định danh trong NER hay không.

Nguồn: VietMed-NER train, dòng 1610 (từ 0).

## VM600-190

**Đoạn gốc:** tắt những cái điểm tiếp xúc của điện cực đó cũng như là điều chỉnh cường độ ở cái mức độ mà mình mong muốn tối ưu để được

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | điện cực | Thủ thuật hoặc điều trị (PROCEDURE) | [32, 40) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- CONTEXT_OR_TRANSCRIPT: câu bị cắt, tham chiếu/mục đích chưa rõ hoặc nghi lỗi phiên âm; cần xem ngữ cảnh/audio gốc, không tự sửa văn bản.

### Thay đổi NER

- E2 “điều chỉnh” DRUG [56, 66) → ∅
- E3 “cường độ” DOSAGE [67, 75) → ∅
- E4 “mức độ” DOSAGE [82, 88) → ∅

Nguồn: VietMed-NER train, dòng 1611 (từ 0).

## VM600-191

**Đoạn gốc:** chúng ta bao phủ bên trong và bên ngoài của chúng ta mà còn giúp cơ thể chúng ta thực hiện một loạt các chức năng cần

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | cơ thể | Bộ phận cơ thể (BODY_PART) | [65, 71) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

Nguồn: VietMed-NER train, dòng 1615 (từ 0).

## VM600-192

**Đoạn gốc:** từ khi đó đến nay huyết áp của ông thì thường xuyên tôi cũng cho dùng thuốc

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | huyết áp | Bệnh hoặc triệu chứng (CONDITION) | [18, 26) |
| E2 | thuốc | Thuốc/dược chất (DRUG) | [70, 75) |

### RE

| Mã | Cặp có hướng | Kết luận đề xuất |
|---|---|---|
| R1 | E1 “huyết áp” → E2 “thuốc” | Chưa rõ — cần chốt (CHUA_RO) |

### Cần chốt

- CONTEXT_OR_TRANSCRIPT: câu bị cắt, tham chiếu/mục đích chưa rõ hoặc nghi lỗi phiên âm; cần xem ngữ cảnh/audio gốc, không tự sửa văn bản.
- PHYSIOLOGY_VS_DISEASE: từ huyết áp/mỡ máu đứng riêng chưa xác định bệnh; giữ đề xuất nguồn chờ chốt.
- UNRESOLVED_RE: còn cặp CHUA_RO; tuyệt đối không đổi thành NO_RELATION khi xuất huấn luyện.

Nguồn: VietMed-NER train, dòng 1622 (từ 0).

## VM600-193

**Đoạn gốc:** không có đủ sức để mà vượt qua những cái trở ngại về mặt cân nặng và cái tình

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

Không có thực thể thuộc sáu loại được giữ trong bản rà soát.

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

Nguồn: VietMed-NER train, dòng 1634 (từ 0).

## VM600-194

**Đoạn gốc:** ghi nhận dù đã tiêm đủ mũi hoặc là gần

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | tiêm | Thủ thuật hoặc điều trị (PROCEDURE) | [15, 19) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Thay đổi NER

- E2 “mũi” BODY_PART [23, 26) → ∅

Nguồn: VietMed-NER train, dòng 1638 (từ 0).

## VM600-195

**Đoạn gốc:** chúng ta không nhìn thấy nhưng mà chúng ta thấy là tức chân đau chân lạnh chân thậm chí là nề bàn chân đấy cho nên là

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E3 | tức chân | Bệnh hoặc triệu chứng (CONDITION) | [51, 59) |
| E1 | đau chân | Bệnh hoặc triệu chứng (CONDITION) | [60, 68) |
| E6 | lạnh chân | Bệnh hoặc triệu chứng (CONDITION) | [69, 78) |
| E8 | nề bàn chân | Bệnh hoặc triệu chứng (CONDITION) | [91, 102) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- CONTEXT_OR_TRANSCRIPT: câu bị cắt, tham chiếu/mục đích chưa rõ hoặc nghi lỗi phiên âm; cần xem ngữ cảnh/audio gốc, không tự sửa văn bản.

### Thay đổi NER

- E2 “bàn chân” BODY_PART [94, 102) → E2 “bàn chân” BODY_PART [94, 102)
- ∅ → E3 “tức” CONDITION [51, 54)
- ∅ → E4 “chân” BODY_PART [55, 59)
- ∅ → E5 “chân” BODY_PART [64, 68)
- ∅ → E6 “lạnh” CONDITION [69, 73)
- ∅ → E7 “chân” BODY_PART [74, 78)
- ∅ → E8 “nề” CONDITION [91, 93)
- E3 “tức” CONDITION [51, 54) → E3 “tức chân” CONDITION [51, 59)
- E4 “chân” BODY_PART [55, 59) → ∅
- E1 “đau” CONDITION [60, 63) → E1 “đau chân” CONDITION [60, 68)
- E5 “chân” BODY_PART [64, 68) → ∅
- E6 “lạnh” CONDITION [69, 73) → E6 “lạnh chân” CONDITION [69, 78)
- E7 “chân” BODY_PART [74, 78) → ∅
- E8 “nề” CONDITION [91, 93) → E8 “nề bàn chân” CONDITION [91, 102)
- E2 “bàn chân” BODY_PART [94, 102) → ∅

Nguồn: VietMed-NER train, dòng 1641 (từ 0).

## VM600-196

**Đoạn gốc:** ta tiếp xúc các thành phần chống oxy hóa thì nó sẽ tác động vào cơ thể nói chung

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E2 | cơ thể | Bộ phận cơ thể (BODY_PART) | [64, 70) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- ONTOLOGY_SCOPE: cần chốt phạm vi thuốc/dược chất so với mỹ phẩm, thực phẩm, hóa chất nội sinh hoặc hệ vi sinh; giữ ánh xạ nguồn khi chưa có quy ước đủ rõ.

### Thay đổi NER

- E1 “oxy” DRUG [33, 36) → ∅

Nguồn: VietMed-NER train, dòng 1647 (từ 0).

## VM600-197

**Đoạn gốc:** parkinson hay là bệnh alzheimer bệnh trầm cảm nữa vâng ạ rất là tốt cho cơ thể của chúng ta ngày hôm nay thì những

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | parkinson | Bệnh hoặc triệu chứng (CONDITION) | [0, 9) |
| E2 | alzheimer | Bệnh hoặc triệu chứng (CONDITION) | [22, 31) |
| E3 | trầm cảm | Bệnh hoặc triệu chứng (CONDITION) | [37, 45) |
| E4 | cơ thể | Bộ phận cơ thể (BODY_PART) | [72, 78) |

### RE

| Mã | Cặp có hướng | Kết luận đề xuất |
|---|---|---|
| R1 | E1 “parkinson” → E4 “cơ thể” | Không có quan hệ thuộc 5 loại (NO_RELATION) |
| R2 | E2 “alzheimer” → E4 “cơ thể” | Không có quan hệ thuộc 5 loại (NO_RELATION) |
| R3 | E3 “trầm cảm” → E4 “cơ thể” | Không có quan hệ thuộc 5 loại (NO_RELATION) |

Nguồn: VietMed-NER train, dòng 1648 (từ 0).

## VM600-198

**Đoạn gốc:** và nó còn có cái cái chiều hướng là nó sẽ cải thiện rất tốt nữa thế nên là bác hoàn toàn có thể yên tâm kết hợp sử dụng

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

Không có thực thể thuộc sáu loại được giữ trong bản rà soát.

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Thay đổi NER

- E1 “cải thiện” PROCEDURE [42, 51) → ∅

Nguồn: VietMed-NER train, dòng 1651 (từ 0).

## VM600-199

**Đoạn gốc:** tính điều trị như thế thì đôi khi da chúng ta sẽ trở nên khô ngứa bong tróc và các quá trình khô ngứa bong tróc đó thì

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | điều trị | Thủ thuật hoặc điều trị (PROCEDURE) | [5, 13) |
| E2 | da | Bộ phận cơ thể (BODY_PART) | [34, 36) |
| E3 | khô ngứa bong tróc | Bệnh hoặc triệu chứng (CONDITION) | [57, 75) |
| E4 | khô ngứa bong tróc | Bệnh hoặc triệu chứng (CONDITION) | [93, 111) |

### RE

| Mã | Cặp có hướng | Kết luận đề xuất |
|---|---|---|
| R1 | E3 “khô ngứa bong tróc” → E1 “điều trị” | Không có quan hệ thuộc 5 loại (NO_RELATION) |
| R2 | E3 “khô ngứa bong tróc” → E2 “da” | Có vị trí ở (located_at) |
| R3 | E4 “khô ngứa bong tróc” → E1 “điều trị” | Không có quan hệ thuộc 5 loại (NO_RELATION) |
| R4 | E4 “khô ngứa bong tróc” → E2 “da” | Có vị trí ở (located_at) |

### Cần chốt

- GENERIC_INTERVENTION: cần chốt việc giữ hành động điều trị/chẩn đoán chung khi không nêu phương pháp cụ thể.

Nguồn: VietMed-NER train, dòng 1659 (từ 0).

## VM600-200

**Đoạn gốc:** cụ thể hoặc là dễ hiểu hơn đấy là cái bệnh viêm cột sống dính khớp đấy thì rất

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | viêm cột sống dính khớp | Bệnh hoặc triệu chứng (CONDITION) | [43, 66) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Thay đổi NER

- E1 “bệnh viêm cột sống dính khớp” CONDITION [38, 66) → E1 “viêm cột sống dính khớp” CONDITION [43, 66)

Nguồn: VietMed-NER train, dòng 1663 (từ 0).

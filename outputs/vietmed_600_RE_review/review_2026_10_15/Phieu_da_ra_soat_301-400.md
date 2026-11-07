# Phiếu rà soát NER và RE 301 đến 400

Bản AI rà soát lần hai ngày 15/10/2026. Giữ nguyên câu nguồn và sáu loại NER, năm quan hệ RE. Chưa được chuyên gia xác nhận.

Quy tắc người dùng đã chốt: giữ cả cụm bệnh/triệu chứng trong một CONDITION. Không tách bộ phận bên trong cụm để tạo located_at. Vị trí được nêu riêng bằng giới từ hoặc mệnh đề riêng vẫn được xét.

Vị trí ký tự là khoảng [start, end), đếm từ 0 theo Unicode. Mã E ổn định khi sửa; mã R được tạo lại. Không dùng CHUA_RO làm nhãn huấn luyện hoặc nhãn âm.

## VM600-301

**Đoạn gốc:** do parkinson đa xơ cứng trầm cảm và sa sút trí tuệ đến các rối loạn tự miễn

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | parkinson | Bệnh hoặc triệu chứng (CONDITION) | [3, 12) |
| E2 | đa xơ cứng | Bệnh hoặc triệu chứng (CONDITION) | [13, 23) |
| E3 | trầm cảm | Bệnh hoặc triệu chứng (CONDITION) | [24, 32) |
| E4 | sa sút trí tuệ | Bệnh hoặc triệu chứng (CONDITION) | [36, 50) |
| E5 | rối loạn tự miễn | Bệnh hoặc triệu chứng (CONDITION) | [59, 75) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Thay đổi NER

- E5 “rối loạn” CONDITION [59, 67) → E5 “rối loạn tự miễn” CONDITION [59, 75)

Nguồn: VietMed-NER train, dòng 2322 (từ 0).

## VM600-302

**Đoạn gốc:** tưởng sử dụng để có thể là thực hiện sức khỏe cho chúng ta và đây cũng chính là một món quà thật là ý nghĩa dành tặng

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

Không có thực thể thuộc sáu loại được giữ trong bản rà soát.

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

Nguồn: VietMed-NER train, dòng 2327 (từ 0).

## VM600-303

**Đoạn gốc:** bệnh nhân mà đái tháo đường mà không có kèm bệnh lý béo phì và cũng đã có rất là

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | đái tháo đường | Bệnh hoặc triệu chứng (CONDITION) | [13, 27) |
| E3 | béo phì | Bệnh hoặc triệu chứng (CONDITION) | [52, 59) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Thay đổi NER

- E2 “bệnh lý” CONDITION [44, 51) → ∅

Nguồn: VietMed-NER train, dòng 2329 (từ 0).

## VM600-304

**Đoạn gốc:** côn trùng cũng đang bị mầm bệnh đe dọa chẳng hạn như vi khuẩn và nấm như nhà

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

Không có thực thể thuộc sáu loại được giữ trong bản rà soát.

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- SCOPE_CONFIRMATION: cần xác nhận quy ước về thuốc/dược chất, can thiệp không dùng thuốc, thiết bị, tác nhân hoặc hoạt động thăm khám; không coi ánh xạ nguồn là xác nhận chuyên gia.

### Thay đổi NER

- E1 “mầm bệnh” CONDITION [23, 31) → ∅
- E2 “vi khuẩn” CONDITION [53, 61) → ∅

Nguồn: VietMed-NER train, dòng 2332 (từ 0).

## VM600-305

**Đoạn gốc:** nào tôi cũng phải vịn lúc nào tôi cũng phải bán bởi vì sao chẳng may mình sẩy chân chẳng may mình có những câu chuyện

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | chân | Bộ phận cơ thể (BODY_PART) | [78, 82) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

Nguồn: VietMed-NER train, dòng 2334 (từ 0).

## VM600-306

**Đoạn gốc:** trội của hoạt chất kga1 là được chiết xuất chuẩn hóa từ thảo dược đảm bảo tính an toàn cho người bệnh khi kga1 kết

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E2 | kga1 | Thuốc/dược chất (DRUG) | [19, 23) |
| E4 | thảo dược | Thuốc/dược chất (DRUG) | [56, 65) |
| E5 | kga1 | Thuốc/dược chất (DRUG) | [106, 110) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- ONTOLOGY_SCOPE: cần chốt phạm vi thuốc/dược chất so với mỹ phẩm, thực phẩm, hóa chất nội sinh hoặc hệ vi sinh; giữ ánh xạ nguồn khi chưa có quy ước đủ rõ.

### Thay đổi NER

- E3 “chiết xuất” PROCEDURE [32, 42) → ∅
- E1 “hoạt chất” DRUG [9, 18) → ∅

Nguồn: VietMed-NER train, dòng 2335 (từ 0).

## VM600-307

**Đoạn gốc:** huyết áp là bác vẫn bác trai vẫn thường xuyên duy trì này rồi là các tất cả các cái thuốc điều trị của các bác sĩ là bác

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | huyết áp | Bệnh hoặc triệu chứng (CONDITION) | [0, 8) |
| E2 | thuốc | Thuốc/dược chất (DRUG) | [84, 89) |
| E3 | điều trị | Thủ thuật hoặc điều trị (PROCEDURE) | [90, 98) |

### RE

| Mã | Cặp có hướng | Kết luận đề xuất |
|---|---|---|
| R1 | E1 “huyết áp” → E2 “thuốc” | Chưa rõ — cần chốt (CHUA_RO) |
| R2 | E1 “huyết áp” → E3 “điều trị” | Chưa rõ — cần chốt (CHUA_RO) |

### Cần chốt

- CONTEXT_OR_TRANSCRIPT: câu bị cắt, tham chiếu/mục đích chưa rõ hoặc nghi lỗi phiên âm; cần xem ngữ cảnh/audio gốc, không tự sửa văn bản.
- GENERIC_INTERVENTION: cần chốt việc giữ hành động điều trị/chẩn đoán chung khi không nêu phương pháp cụ thể.
- PHYSIOLOGY_VS_DISEASE: từ huyết áp/mỡ máu đứng riêng chưa xác định bệnh; giữ đề xuất nguồn chờ chốt.
- UNRESOLVED_RE: còn cặp CHUA_RO; tuyệt đối không đổi thành NO_RELATION khi xuất huấn luyện.

Nguồn: VietMed-NER train, dòng 2340 (từ 0).

## VM600-308

**Đoạn gốc:** thâm sau mụn nè hoặc là mụn ẩn mà có kèm theo là nám và tàn nhang thì khi đó chúng ta vẫn có thể sử dụng những cái

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | thâm sau mụn | Bệnh hoặc triệu chứng (CONDITION) | [0, 12) |
| E3 | mụn ẩn | Bệnh hoặc triệu chứng (CONDITION) | [24, 30) |
| E4 | nám | Bệnh hoặc triệu chứng (CONDITION) | [49, 52) |
| E5 | tàn nhang | Bệnh hoặc triệu chứng (CONDITION) | [56, 65) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Thay đổi NER

- E1 “thâm sau” CONDITION [0, 8) → E1 “thâm sau mụn” CONDITION [0, 12)
- E2 “mụn” CONDITION [9, 12) → ∅

Nguồn: VietMed-NER train, dòng 2342 (từ 0).

## VM600-309

**Đoạn gốc:** chương trình kích thích não sau thì nó sẽ có những người tham gia ví dụ như là

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | kích thích não sau | Thủ thuật hoặc điều trị (PROCEDURE) | [13, 31) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- CONTEXT_OR_TRANSCRIPT: câu bị cắt, tham chiếu/mục đích chưa rõ hoặc nghi lỗi phiên âm; cần xem ngữ cảnh/audio gốc, không tự sửa văn bản.

### Thay đổi NER

- E1 “não” BODY_PART [24, 27) → E1 “kích thích não sau” PROCEDURE [13, 31)

Nguồn: VietMed-NER train, dòng 2347 (từ 0).

## VM600-310

**Đoạn gốc:** có hai bộ phận thứ nhất là phần quả thể và phần thứ hai là phần đế thế thì ngày

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E3 | quả thể | Thuốc/dược chất (DRUG) | [32, 39) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- ONTOLOGY_SCOPE: cần chốt phạm vi thuốc/dược chất so với mỹ phẩm, thực phẩm, hóa chất nội sinh hoặc hệ vi sinh; giữ ánh xạ nguồn khi chưa có quy ước đủ rõ.

### Thay đổi NER

- E1 “hai bộ phận” DOSAGE [3, 14) → ∅
- E2 “thứ nhất” DOSAGE [15, 23) → ∅
- E4 “phần thứ hai” DOSAGE [43, 55) → ∅

Nguồn: VietMed-NER train, dòng 2362 (từ 0).

## VM600-311

**Đoạn gốc:** động sinh lý khác nhau bao gồm vận hành hệ miễn dịch giải độc viêm dẫn truyền

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | hệ miễn dịch | Bộ phận cơ thể (BODY_PART) | [40, 52) |
| E2 | viêm | Bệnh hoặc triệu chứng (CONDITION) | [62, 66) |

### RE

| Mã | Cặp có hướng | Kết luận đề xuất |
|---|---|---|
| R1 | E2 “viêm” → E1 “hệ miễn dịch” | Không có quan hệ thuộc 5 loại (NO_RELATION) |

### Cần chốt

- CONTEXT_OR_TRANSCRIPT: câu bị cắt, tham chiếu/mục đích chưa rõ hoặc nghi lỗi phiên âm; cần xem ngữ cảnh/audio gốc, không tự sửa văn bản.

### Thay đổi NER

- E1 “hệ miễn dịch giải độc” BODY_PART [40, 61) → E1 “hệ miễn dịch” BODY_PART [40, 52)

Nguồn: VietMed-NER train, dòng 2371 (từ 0).

## VM600-312

**Đoạn gốc:** thần kinh cao cấp đó là những những cái trách nhiệm về tâm lý những được được

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

Không có thực thể thuộc sáu loại được giữ trong bản rà soát.

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- CONTEXT_OR_TRANSCRIPT: câu bị cắt, tham chiếu/mục đích chưa rõ hoặc nghi lỗi phiên âm; cần xem ngữ cảnh/audio gốc, không tự sửa văn bản.

### Thay đổi NER

- E2 “cao” DOSAGE [10, 13) → ∅
- E1 “thần kinh” BODY_PART [0, 9) → ∅

Nguồn: VietMed-NER train, dòng 2373 (từ 0).

## VM600-313

**Đoạn gốc:** cái thành phần mà xưa kia cha ông ta rất hay sử dụng trong những cái bài thuốc để điều trị như các cái chứng bệnh về chính

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | bài thuốc | Thuốc/dược chất (DRUG) | [69, 78) |
| E2 | điều trị | Thủ thuật hoặc điều trị (PROCEDURE) | [82, 90) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- GENERIC_INTERVENTION: cần chốt việc giữ hành động điều trị/chẩn đoán chung khi không nêu phương pháp cụ thể.

### Thay đổi NER

- E1 “thuốc” DRUG [73, 78) → E1 “bài thuốc” DRUG [69, 78)

Nguồn: VietMed-NER train, dòng 2383 (từ 0).

## VM600-314

**Đoạn gốc:** và vậy thì gia đình mà có nuôi chó mèo

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

Không có thực thể thuộc sáu loại được giữ trong bản rà soát.

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

Nguồn: VietMed-NER train, dòng 2403 (từ 0).

## VM600-315

**Đoạn gốc:** tham gia vào khi nói đến sự phát triển của bất kỳ căn bệnh nào cũng như tỷ lệ mắc một số bệnh ở các quốc gia khác nhau

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

Không có thực thể thuộc sáu loại được giữ trong bản rà soát.

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Thay đổi NER

- E1 “tỷ lệ” DOSAGE [72, 77) → ∅

Nguồn: VietMed-NER train, dòng 2408 (từ 0).

## VM600-316

**Đoạn gốc:** biệt là nội thần kinh nội về bệnh parkinson và rối loạn vận động cũng sẽ hỗ trợ rất nhiều trong khi việc mà làm

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E2 | parkinson | Bệnh hoặc triệu chứng (CONDITION) | [34, 43) |
| E3 | rối loạn vận động | Bệnh hoặc triệu chứng (CONDITION) | [47, 64) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Thay đổi NER

- E4 “hỗ trợ” PROCEDURE [73, 79) → ∅
- E5 “rất nhiều” DOSAGE [80, 89) → ∅
- E1 “thần kinh” BODY_PART [12, 21) → ∅

Nguồn: VietMed-NER train, dòng 2441 (từ 0).

## VM600-317

**Đoạn gốc:** phần hóa học cũng như là tác dụng dược lý của các hoạt chất nằm trong quả thể

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | hoạt chất | Thuốc/dược chất (DRUG) | [50, 59) |
| E2 | quả thể | Thuốc/dược chất (DRUG) | [70, 77) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- ONTOLOGY_SCOPE: cần chốt phạm vi thuốc/dược chất so với mỹ phẩm, thực phẩm, hóa chất nội sinh hoặc hệ vi sinh; giữ ánh xạ nguồn khi chưa có quy ước đủ rõ.

Nguồn: VietMed-NER train, dòng 2442 (từ 0).

## VM600-318

**Đoạn gốc:** là bình thường thế rồi thì chúng ta cũng thấy nó đỡ rồi thì thôi thế là tự nhiên chúng ta bỏ thuốc cái đó cực kỳ nguy

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | thuốc | Thuốc/dược chất (DRUG) | [93, 98) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

Nguồn: VietMed-NER train, dòng 2445 (từ 0).

## VM600-319

**Đoạn gốc:** để điều trị cho từng bệnh đặc biệt trong đó thì có một cái cơ chế rất là quan trọng là các cái khớp nó bị viêm thì cần

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | điều trị | Thủ thuật hoặc điều trị (PROCEDURE) | [3, 11) |
| E2 | khớp | Bộ phận cơ thể (BODY_PART) | [95, 99) |
| E3 | viêm | Bệnh hoặc triệu chứng (CONDITION) | [106, 110) |

### RE

| Mã | Cặp có hướng | Kết luận đề xuất |
|---|---|---|
| R1 | E3 “viêm” → E1 “điều trị” | Chưa rõ — cần chốt (CHUA_RO) |
| R2 | E3 “viêm” → E2 “khớp” | Có vị trí ở (located_at) |

### Cần chốt

- GENERIC_INTERVENTION: cần chốt việc giữ hành động điều trị/chẩn đoán chung khi không nêu phương pháp cụ thể.
- UNRESOLVED_RE: còn cặp CHUA_RO; tuyệt đối không đổi thành NO_RELATION khi xuất huấn luyện.

### Thay đổi NER

- E2 “các cái khớp” BODY_PART [87, 99) → E2 “khớp” BODY_PART [95, 99)

Nguồn: VietMed-NER train, dòng 2454 (từ 0).

## VM600-320

**Đoạn gốc:** biệt là bị ảnh hưởng với các loại thuốc thức ăn nó là một cái loại kháng vitamin k bởi

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | thuốc | Thuốc/dược chất (DRUG) | [34, 39) |
| E2 | kháng vitamin k | Thuốc/dược chất (DRUG) | [67, 82) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- SCOPE_CONFIRMATION: cần xác nhận quy ước về thuốc/dược chất, can thiệp không dùng thuốc, thiết bị, tác nhân hoặc hoạt động thăm khám; không coi ánh xạ nguồn là xác nhận chuyên gia.

### Thay đổi NER

- E2 “vitamin k” DRUG [73, 82) → E2 “kháng vitamin k” DRUG [67, 82)

Nguồn: VietMed-NER train, dòng 2466 (từ 0).

## VM600-321

**Đoạn gốc:** sau mổ tại vì cái chương trình đều chương trình điều chỉnh máy sau mổ

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | mổ | Thủ thuật hoặc điều trị (PROCEDURE) | [4, 6) |
| E3 | mổ | Thủ thuật hoặc điều trị (PROCEDURE) | [67, 69) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- CONTEXT_OR_TRANSCRIPT: câu bị cắt, tham chiếu/mục đích chưa rõ hoặc nghi lỗi phiên âm; cần xem ngữ cảnh/audio gốc, không tự sửa văn bản.

### Thay đổi NER

- E2 “điều chỉnh” DRUG [48, 58) → ∅

Nguồn: VietMed-NER train, dòng 2479 (từ 0).

## VM600-322

**Đoạn gốc:** chăm sóc dành cho người bệnh béo phì với vai trò của người thân trong gia đình là một trong những điều quan trọng và ngày

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | béo phì | Bệnh hoặc triệu chứng (CONDITION) | [29, 36) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

Nguồn: VietMed-NER train, dòng 2484 (từ 0).

## VM600-323

**Đoạn gốc:** máu trong đó đặc biệt là tĩnh mạch của chúng ta thế thì cái viên nang đông trùng hạ thảo nó cũng có rất hữu ích cho

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | máu | Bộ phận cơ thể (BODY_PART) | [0, 3) |
| E2 | tĩnh mạch | Bộ phận cơ thể (BODY_PART) | [25, 34) |
| E3 | viên nang đông trùng hạ thảo | Thuốc/dược chất (DRUG) | [60, 88) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- ONTOLOGY_SCOPE: cần chốt phạm vi thuốc/dược chất so với mỹ phẩm, thực phẩm, hóa chất nội sinh hoặc hệ vi sinh; giữ ánh xạ nguồn khi chưa có quy ước đủ rõ.

Nguồn: VietMed-NER train, dòng 2489 (từ 0).

## VM600-324

**Đoạn gốc:** đưa cho những người thực hiện chức năng và chúng ta có thể đi qua cái chốt chặn dễ dàng xin để cảm ơn tiến sĩ bác sĩ

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

Không có thực thể thuộc sáu loại được giữ trong bản rà soát.

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Thay đổi NER

- E1 “chốt chặn” DRUG [70, 79) → ∅

Nguồn: VietMed-NER train, dòng 2499 (từ 0).

## VM600-325

**Đoạn gốc:** tam đại bộ phẩm đó là cái gì thứ nhất là nó là có nhung hươu cái thứ hai là nhân sâm và thứ ba đông trùng hạ thảo cái thứ

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E3 | nhung hươu | Thuốc/dược chất (DRUG) | [50, 60) |
| E5 | nhân sâm | Thuốc/dược chất (DRUG) | [76, 84) |
| E6 | đông trùng hạ thảo | Thuốc/dược chất (DRUG) | [95, 113) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Thay đổi NER

- E2 “thứ nhất” DOSAGE [29, 37) → ∅
- E4 “cái thứ hai” DOSAGE [61, 72) → ∅
- E1 “tam đại bộ phẩm” DRUG [0, 15) → ∅

Nguồn: VietMed-NER train, dòng 2502 (từ 0).

## VM600-326

**Đoạn gốc:** pháp có liên quan đến y học cổ truyền ở trong đó thì có cái viên nang đông trùng hạ thảo hôm nay chương trình giới thiệu

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | y học cổ truyền | Thủ thuật hoặc điều trị (PROCEDURE) | [22, 37) |
| E2 | viên nang đông trùng hạ thảo | Thuốc/dược chất (DRUG) | [60, 88) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- ONTOLOGY_SCOPE: cần chốt phạm vi thuốc/dược chất so với mỹ phẩm, thực phẩm, hóa chất nội sinh hoặc hệ vi sinh; giữ ánh xạ nguồn khi chưa có quy ước đủ rõ.

Nguồn: VietMed-NER train, dòng 2511 (từ 0).

## VM600-327

**Đoạn gốc:** với những cái bệnh lý khác thì điều này không chỉ trong thực tế lâm sàng mà trong những cái nghiên cứu họ

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | bệnh lý | Bệnh hoặc triệu chứng (CONDITION) | [14, 21) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- GENERIC_MENTION: cần chốt có giữ bệnh/triệu chứng/biến chứng chung và tham chiếu không định danh trong NER hay không.

### Thay đổi NER

- E2 “nghiên cứu” TEST [92, 102) → ∅

Nguồn: VietMed-NER train, dòng 2520 (từ 0).

## VM600-328

**Đoạn gốc:** trường sống này mình sẽ nhắm tới mấy cái chuyện môi trường thứ nhất là môi trường tự nhiên và môi trường thứ hai là môi

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

Không có thực thể thuộc sáu loại được giữ trong bản rà soát.

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Thay đổi NER

- E2 “thứ nhất” DOSAGE [59, 67) → ∅
- E1 “môi” BODY_PART [48, 51) → ∅
- E3 “môi” BODY_PART [71, 74) → ∅
- E4 “môi” BODY_PART [94, 97) → ∅
- E5 “môi” BODY_PART [116, 119) → ∅

Nguồn: VietMed-NER train, dòng 2521 (từ 0).

## VM600-329

**Đoạn gốc:** đau khớp và viêm khớp huyết áp cao xơ vữa động mạch các bệnh nhiễm nấm mạn

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | đau khớp | Bệnh hoặc triệu chứng (CONDITION) | [0, 8) |
| E3 | viêm khớp | Bệnh hoặc triệu chứng (CONDITION) | [12, 21) |
| E4 | huyết áp cao | Bệnh hoặc triệu chứng (CONDITION) | [22, 34) |
| E6 | xơ vữa động mạch | Bệnh hoặc triệu chứng (CONDITION) | [35, 51) |
| E7 | bệnh nhiễm nấm mạn | Bệnh hoặc triệu chứng (CONDITION) | [56, 74) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Thay đổi NER

- E5 “cao” DOSAGE [31, 34) → ∅
- E4 “huyết áp” CONDITION [22, 30) → E4 “huyết áp cao” CONDITION [22, 34)
- E1 “đau” CONDITION [0, 3) → E1 “đau khớp” CONDITION [0, 8)
- E2 “khớp” BODY_PART [4, 8) → ∅

Nguồn: VietMed-NER train, dòng 2522 (từ 0).

## VM600-330

**Đoạn gốc:** các bạn ngày hôm nay của chúng ta đã có thêm được nhiều những cái kiến thức đặc biệt là đối với những người cao tuổi ngày hôm nay những ai mà đang còn đang

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

Không có thực thể thuộc sáu loại được giữ trong bản rà soát.

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

Nguồn: VietMed-NER train, dòng 2525 (từ 0).

## VM600-331

**Đoạn gốc:** bác sĩ kiểm tra ngay huyết áp và cho thuốc bác thuốc uống huyết áp để kiểm soát tốt con số huyết áp bác nhé vì với

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | kiểm tra ngay huyết áp | Xét nghiệm hoặc thăm khám (TEST) | [7, 29) |
| E3 | thuốc | Thuốc/dược chất (DRUG) | [37, 42) |
| E4 | thuốc uống | Thuốc/dược chất (DRUG) | [47, 57) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- CONTEXT_OR_TRANSCRIPT: câu bị cắt, tham chiếu/mục đích chưa rõ hoặc nghi lỗi phiên âm; cần xem ngữ cảnh/audio gốc, không tự sửa văn bản.

### Thay đổi NER

- E6 “kiểm soát” DRUG [70, 79) → ∅
- E1 “kiểm tra” TEST [7, 15) → E1 “kiểm tra ngay huyết áp” TEST [7, 29)
- E2 “huyết áp” CONDITION [21, 29) → ∅
- E3 “cho thuốc” PROCEDURE [33, 42) → E3 “thuốc” DRUG [37, 42)
- E5 “huyết áp” CONDITION [58, 66) → ∅
- E7 “huyết áp” CONDITION [91, 99) → ∅

Nguồn: VietMed-NER train, dòng 2533 (từ 0).

## VM600-332

**Đoạn gốc:** cuộc sống tốt hơn vâng thưa bác sĩ như vậy thì ở từng giai đoạn của mình thì người bệnh sẽ được tiếp nhận điều

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

Không có thực thể thuộc sáu loại được giữ trong bản rà soát.

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

Nguồn: VietMed-NER train, dòng 2546 (từ 0).

## VM600-333

**Đoạn gốc:** huyết thông qua đó là biểu hiện cải thiện các chỉ số hba1c giảm được là từ khoảng là hai mươi phần trăm cái

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E6 | hba1c | Xét nghiệm hoặc thăm khám (TEST) | [53, 58) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- CONTEXT_OR_TRANSCRIPT: câu bị cắt, tham chiếu/mục đích chưa rõ hoặc nghi lỗi phiên âm; cần xem ngữ cảnh/audio gốc, không tự sửa văn bản.
- ONTOLOGY_SCOPE: cần chốt phạm vi thuốc/dược chất so với mỹ phẩm, thực phẩm, hóa chất nội sinh hoặc hệ vi sinh; giữ ánh xạ nguồn khi chưa có quy ước đủ rõ.

### Thay đổi NER

- E2 “cải thiện” PROCEDURE [32, 41) → ∅
- E3 “các chỉ số” DOSAGE [42, 52) → ∅
- E4 “hba1c” DOSAGE [53, 58) → ∅
- E5 “hai mươi phần trăm” DOSAGE [85, 103) → ∅
- E1 “huyết” BODY_PART [0, 5) → ∅
- ∅ → E6 “hba1c” TEST [53, 58)

Nguồn: VietMed-NER train, dòng 2558 (từ 0).

## VM600-334

**Đoạn gốc:** đó là nó ra được cơ quan kiểm soát thuốc và dược phẩm của hoa kỳ chấp nhận từ năm

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

Không có thực thể thuộc sáu loại được giữ trong bản rà soát.

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

Nguồn: VietMed-NER train, dòng 2567 (từ 0).

## VM600-335

**Đoạn gốc:** vấn giúp em làm cách nào để giúp bố em cải thiện tình trạng này ăn nhiều hơn và lên cân được không ạ

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

Không có thực thể thuộc sáu loại được giữ trong bản rà soát.

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Thay đổi NER

- E1 “cải thiện” PROCEDURE [39, 48) → ∅

Nguồn: VietMed-NER train, dòng 2568 (từ 0).

## VM600-336

**Đoạn gốc:** thay vì cái việc ngày xưa chúng ta phải đi nhiều chúng ta vận động nhiều chúng ta phải đạp xe đạp hiện nay chúng ta là

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

Không có thực thể thuộc sáu loại được giữ trong bản rà soát.

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

Nguồn: VietMed-NER train, dòng 2584 (từ 0).

## VM600-337

**Đoạn gốc:** hiện nay thì sẽ hỗ trợ cho việc mà khỏi bệnh được nhanh nhất và vấn đề thứ ba đó

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

Không có thực thể thuộc sáu loại được giữ trong bản rà soát.

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Thay đổi NER

- E1 “hỗ trợ” PROCEDURE [16, 22) → ∅

Nguồn: VietMed-NER train, dòng 2588 (từ 0).

## VM600-338

**Đoạn gốc:** bệnh và rối loạn chức năng đỉnh cuối phần này bạn sẽ có một sự trân trọng mới

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | rối loạn chức năng | Bệnh hoặc triệu chứng (CONDITION) | [8, 26) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- CONTEXT_OR_TRANSCRIPT: câu bị cắt, tham chiếu/mục đích chưa rõ hoặc nghi lỗi phiên âm; cần xem ngữ cảnh/audio gốc, không tự sửa văn bản.

Nguồn: VietMed-NER train, dòng 2595 (từ 0).

## VM600-339

**Đoạn gốc:** giúp bạn tồn tại ảnh hưởng của mỗi cá nhân đến sức khỏe mạnh của hành tinh chúng ta cũng vậy trên thực tế bạn là

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

Không có thực thể thuộc sáu loại được giữ trong bản rà soát.

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

Nguồn: VietMed-NER train, dòng 2601 (từ 0).

## VM600-340

**Đoạn gốc:** trạng ốm yếu đau khổ cá nhân chất lượng cuộc sống bị tổn hại và tiêu tốn về tài

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E2 | ốm yếu | Bệnh hoặc triệu chứng (CONDITION) | [6, 12) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- SYMPTOM_SCOPE: cần phân biệt cảm xúc thông thường với triệu chứng lâm sàng theo quy ước dự án.

### Thay đổi NER

- E1 “đau” CONDITION [13, 16) → ∅
- ∅ → E2 “ốm yếu” CONDITION [6, 12)

Nguồn: VietMed-NER train, dòng 2604 (từ 0).

## VM600-341

**Đoạn gốc:** khi mà bị đột quỵ thì thường các bác sĩ đột quỵ tôi sẽ phải khảo sát toàn bộ để

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | đột quỵ | Bệnh hoặc triệu chứng (CONDITION) | [10, 17) |
| E3 | khảo sát | Xét nghiệm hoặc thăm khám (TEST) | [60, 68) |

### RE

| Mã | Cặp có hướng | Kết luận đề xuất |
|---|---|---|
| R1 | E1 “đột quỵ” → E3 “khảo sát” | Chưa rõ — cần chốt (CHUA_RO) |

### Cần chốt

- CONTEXT_OR_TRANSCRIPT: câu bị cắt, tham chiếu/mục đích chưa rõ hoặc nghi lỗi phiên âm; cần xem ngữ cảnh/audio gốc, không tự sửa văn bản.
- GENERIC_INTERVENTION: cần chốt việc giữ hành động điều trị/chẩn đoán chung khi không nêu phương pháp cụ thể.
- UNRESOLVED_RE: còn cặp CHUA_RO; tuyệt đối không đổi thành NO_RELATION khi xuất huấn luyện.

### Thay đổi NER

- E2 “đột quỵ” CONDITION [40, 47) → ∅
- E3 “khảo sát” DRUG [60, 68) → E3 “khảo sát” TEST [60, 68)

Nguồn: VietMed-NER train, dòng 2608 (từ 0).

## VM600-342

**Đoạn gốc:** bệnh nó liên quan đến cái vùng cột sống cổ là chính những có những cái trường hợp liên quan đến cái vùng cổ tay và

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | cột sống cổ | Bộ phận cơ thể (BODY_PART) | [31, 42) |
| E3 | cổ tay | Bộ phận cơ thể (BODY_PART) | [105, 111) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Thay đổi NER

- E1 “cột sống” BODY_PART [31, 39) → E1 “cột sống cổ” BODY_PART [31, 42)
- E2 “vùng” BODY_PART [100, 104) → ∅

Nguồn: VietMed-NER train, dòng 2614 (từ 0).

## VM600-343

**Đoạn gốc:** tăng khoảng hai ký thì như vậy thì như chúng ta biết rằng là khi mà mình chọn lựa thuốc cho những cái bệnh nhân mà đái

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | thuốc | Thuốc/dược chất (DRUG) | [82, 87) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- CONTEXT_OR_TRANSCRIPT: câu bị cắt, tham chiếu/mục đích chưa rõ hoặc nghi lỗi phiên âm; cần xem ngữ cảnh/audio gốc, không tự sửa văn bản.

Nguồn: VietMed-NER train, dòng 2621 (từ 0).

## VM600-344

**Đoạn gốc:** chỉ định của các bác sĩ thì bệnh nhân cũng cần được tiếp tục hỗ trợ chuyên sâu về mặt tâm lý nhằm là giúp cho họ giữ

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E2 | hỗ trợ chuyên sâu về mặt tâm lý | Thủ thuật hoặc điều trị (PROCEDURE) | [61, 92) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- SCOPE_CONFIRMATION: cần xác nhận quy ước về thuốc/dược chất, can thiệp không dùng thuốc, thiết bị, tác nhân hoặc hoạt động thăm khám; không coi ánh xạ nguồn là xác nhận chuyên gia.

### Thay đổi NER

- E1 “chỉ định” DRUG [0, 8) → ∅

Nguồn: VietMed-NER train, dòng 2622 (từ 0).

## VM600-345

**Đoạn gốc:** động mạch được hay không và giảm nhẹ các triệu chứng như là đau đầu hoa mắt chóng mặt được hay không thưa bác sĩ đây là

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | động mạch | Bộ phận cơ thể (BODY_PART) | [0, 9) |
| E3 | đau đầu | Bệnh hoặc triệu chứng (CONDITION) | [60, 67) |
| E4 | hoa mắt | Bệnh hoặc triệu chứng (CONDITION) | [68, 75) |
| E5 | chóng mặt | Bệnh hoặc triệu chứng (CONDITION) | [76, 85) |

### RE

| Mã | Cặp có hướng | Kết luận đề xuất |
|---|---|---|
| R1 | E3 “đau đầu” → E1 “động mạch” | Không có quan hệ thuộc 5 loại (NO_RELATION) |
| R2 | E4 “hoa mắt” → E1 “động mạch” | Không có quan hệ thuộc 5 loại (NO_RELATION) |
| R3 | E5 “chóng mặt” → E1 “động mạch” | Không có quan hệ thuộc 5 loại (NO_RELATION) |

### Thay đổi NER

- E2 “triệu chứng” CONDITION [41, 52) → ∅

Nguồn: VietMed-NER train, dòng 2624 (từ 0).

## VM600-346

**Đoạn gốc:** có thể rất quý ví dụ như là tam đại bộ phẩm có nhân sâm có nhung hươu rồi có

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E2 | nhân sâm | Thuốc/dược chất (DRUG) | [47, 55) |
| E3 | nhung hươu | Thuốc/dược chất (DRUG) | [59, 69) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- ONTOLOGY_SCOPE: cần chốt phạm vi thuốc/dược chất so với mỹ phẩm, thực phẩm, hóa chất nội sinh hoặc hệ vi sinh; giữ ánh xạ nguồn khi chưa có quy ước đủ rõ.

### Thay đổi NER

- E1 “tam đại bộ phẩm” DRUG [28, 43) → ∅

Nguồn: VietMed-NER train, dòng 2626 (từ 0).

## VM600-347

**Đoạn gốc:** thứ ba là lúc nào cũng kêu chán hết trơn sao mà chán quá đi chán quá đi và hổng

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

Không có thực thể thuộc sáu loại được giữ trong bản rà soát.

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

Nguồn: VietMed-NER train, dòng 2632 (từ 0).

## VM600-348

**Đoạn gốc:** gia đình và những người ở trong xã hội càng tốt thì sẽ ở trong cái môi trường đó cái người béo phì nó sẽ được thuận

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E2 | béo phì | Bệnh hoặc triệu chứng (CONDITION) | [91, 98) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Thay đổi NER

- E1 “môi” BODY_PART [67, 70) → ∅

Nguồn: VietMed-NER train, dòng 2635 (từ 0).

## VM600-349

**Đoạn gốc:** phì chứ không chỉ riêng về cái rối loạn về cái hành vi ăn uống thế thì họ cần

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | rối loạn về cái hành vi ăn uống | Bệnh hoặc triệu chứng (CONDITION) | [31, 62) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- CONTEXT_OR_TRANSCRIPT: câu bị cắt, tham chiếu/mục đích chưa rõ hoặc nghi lỗi phiên âm; cần xem ngữ cảnh/audio gốc, không tự sửa văn bản.

### Thay đổi NER

- E1 “rối loạn” CONDITION [31, 39) → E1 “rối loạn về cái hành vi ăn uống” CONDITION [31, 62)

Nguồn: VietMed-NER train, dòng 2640 (từ 0).

## VM600-350

**Đoạn gốc:** ví dụ như là nếu chúng ta bị chấn thương thì sẽ dễ bị chảy máu chảy máu khó

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | chấn thương | Bệnh hoặc triệu chứng (CONDITION) | [29, 40) |
| E2 | chảy máu | Bệnh hoặc triệu chứng (CONDITION) | [54, 62) |
| E3 | chảy máu | Bệnh hoặc triệu chứng (CONDITION) | [63, 71) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- CONTEXT_OR_TRANSCRIPT: câu bị cắt, tham chiếu/mục đích chưa rõ hoặc nghi lỗi phiên âm; cần xem ngữ cảnh/audio gốc, không tự sửa văn bản.

Nguồn: VietMed-NER train, dòng 2647 (từ 0).

## VM600-351

**Đoạn gốc:** triển cũng như là chữa lành bệnh chứ còn hiện tại thì các phương pháp điều trị cũng như là phương pháp điều trị phẫu

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E2 | điều trị | Thủ thuật hoặc điều trị (PROCEDURE) | [70, 78) |
| E3 | điều trị | Thủ thuật hoặc điều trị (PROCEDURE) | [103, 111) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- CONTEXT_OR_TRANSCRIPT: câu bị cắt, tham chiếu/mục đích chưa rõ hoặc nghi lỗi phiên âm; cần xem ngữ cảnh/audio gốc, không tự sửa văn bản.
- GENERIC_INTERVENTION: cần chốt việc giữ hành động điều trị/chẩn đoán chung khi không nêu phương pháp cụ thể.

### Thay đổi NER

- E1 “chữa lành bệnh” PROCEDURE [18, 32) → ∅

Nguồn: VietMed-NER train, dòng 2650 (từ 0).

## VM600-352

**Đoạn gốc:** người ta vẫn đang tiến tiếp tục nghiên cứu và rất nhiều các phương pháp nghiên cứu để giúp làm sao có thể ngăn sự tiến

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

Không có thực thể thuộc sáu loại được giữ trong bản rà soát.

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Thay đổi NER

- E1 “nghiên cứu” TEST [32, 42) → ∅
- E2 “rất nhiều” DOSAGE [46, 55) → ∅
- E3 “nghiên cứu” TEST [72, 82) → ∅

Nguồn: VietMed-NER train, dòng 2654 (từ 0).

## VM600-353

**Đoạn gốc:** các cường độ cho nó phù hợp nhất để điều chỉnh cái gia giảm cả lượng thuốc thì làm cái quá trình rất là dài và có thể

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E3 | thuốc | Thuốc/dược chất (DRUG) | [69, 74) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Thay đổi NER

- E1 “cường độ” DOSAGE [4, 12) → ∅
- E2 “điều chỉnh” DRUG [36, 46) → ∅

Nguồn: VietMed-NER train, dòng 2660 (từ 0).

## VM600-354

**Đoạn gốc:** dụng của cái sản phẩm đó à nó không chỉ là khó gọi ghẹo gói trong một số bệnh lý

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

Không có thực thể thuộc sáu loại được giữ trong bản rà soát.

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

Nguồn: VietMed-NER train, dòng 2662 (từ 0).

## VM600-355

**Đoạn gốc:** giới ngày nay nhưng đã đến lúc phải đón nhận một khía cạnh khác của câu chuyện vi khuẩn trong cuộc sống của chúng ta

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

Không có thực thể thuộc sáu loại được giữ trong bản rà soát.

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Thay đổi NER

- E1 “vi khuẩn” CONDITION [79, 87) → ∅

Nguồn: VietMed-NER train, dòng 2663 (từ 0).

## VM600-356

**Đoạn gốc:** nam chưa được phát hiện trên tám mươi phần trăm chưa được điều trị đồng thời tại việt nam có tới ba mươi phần trăm người trưởng

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E2 | điều trị | Thủ thuật hoặc điều trị (PROCEDURE) | [58, 66) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- GENERIC_INTERVENTION: cần chốt việc giữ hành động điều trị/chẩn đoán chung khi không nêu phương pháp cụ thể.

### Thay đổi NER

- E1 “tám mươi phần trăm” DOSAGE [29, 47) → ∅
- E3 “ba mươi phần trăm” DOSAGE [97, 114) → ∅

Nguồn: VietMed-NER train, dòng 2666 (từ 0).

## VM600-357

**Đoạn gốc:** trị liệu có thể làm gia tăng của nhiệt độ của những thiết bị đó là có thể làm tổn thương mô thì cái này là được xem

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | trị liệu | Thủ thuật hoặc điều trị (PROCEDURE) | [0, 8) |
| E2 | tổn thương mô | Bệnh hoặc triệu chứng (CONDITION) | [78, 91) |

### RE

| Mã | Cặp có hướng | Kết luận đề xuất |
|---|---|---|
| R1 | E2 “tổn thương mô” → E1 “trị liệu” | Không có quan hệ thuộc 5 loại (NO_RELATION) |

### Cần chốt

- GENERIC_INTERVENTION: cần chốt việc giữ hành động điều trị/chẩn đoán chung khi không nêu phương pháp cụ thể.

### Thay đổi NER

- E2 “tổn thương” CONDITION [78, 88) → E2 “tổn thương mô” CONDITION [78, 91)
- E3 “mô” BODY_PART [89, 91) → ∅

Nguồn: VietMed-NER train, dòng 2675 (từ 0).

## VM600-358

**Đoạn gốc:** ung thư bằng cách là vắt nước chanh vào một cốc nước ấm xong rồi mình uống lại uống vào lúc đói thì thực sự là khi

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | ung thư | Bệnh hoặc triệu chứng (CONDITION) | [0, 7) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- CONTEXT_OR_TRANSCRIPT: câu bị cắt, tham chiếu/mục đích chưa rõ hoặc nghi lỗi phiên âm; cần xem ngữ cảnh/audio gốc, không tự sửa văn bản.

Nguồn: VietMed-NER train, dòng 2690 (từ 0).

## VM600-359

**Đoạn gốc:** bên cạnh đó thì có những người họ vẫn nhận thức được béo phì nó là một bệnh lý có những cái tác hại như vậy cần phải

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | béo phì | Bệnh hoặc triệu chứng (CONDITION) | [53, 60) |
| E2 | bệnh lý | Bệnh hoặc triệu chứng (CONDITION) | [71, 78) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- GENERIC_MENTION: cần chốt có giữ bệnh/triệu chứng/biến chứng chung và tham chiếu không định danh trong NER hay không.

Nguồn: VietMed-NER train, dòng 2701 (từ 0).

## VM600-360

**Đoạn gốc:** dài đó là những cái chế độ ăn vận động thể lực cũng như là các quá trình thay đổi hành vi thì đã có rất là nhiều

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E2 | vận động thể lực | Thủ thuật hoặc điều trị (PROCEDURE) | [30, 46) |
| E1 | thay đổi hành vi | Thủ thuật hoặc điều trị (PROCEDURE) | [73, 89) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- SCOPE_CONFIRMATION: cần xác nhận quy ước về thuốc/dược chất, can thiệp không dùng thuốc, thiết bị, tác nhân hoặc hoạt động thăm khám; không coi ánh xạ nguồn là xác nhận chuyên gia.

### Thay đổi NER

- E1 “thay đổi hành vi” CONDITION [73, 89) → E1 “thay đổi hành vi” PROCEDURE [73, 89)
- ∅ → E2 “vận động thể lực” PROCEDURE [30, 46)

Nguồn: VietMed-NER train, dòng 2703 (từ 0).

## VM600-361

**Đoạn gốc:** biết nên tìm hiểu và để chuẩn bị một cái tâm lý thật là tốt và cuối cùng là

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

Không có thực thể thuộc sáu loại được giữ trong bản rà soát.

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

Nguồn: VietMed-NER train, dòng 2708 (từ 0).

## VM600-362

**Đoạn gốc:** các chị em phải lo lắng rồi đó là chưa kể áp lực công việc vân vân các thứ thì

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

Không có thực thể thuộc sáu loại được giữ trong bản rà soát.

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

Nguồn: VietMed-NER train, dòng 2712 (từ 0).

## VM600-363

**Đoạn gốc:** trước để có những cái thăm dò có những cái đánh giá trước sau đó thì khi mà tham khám như vậy các bác sĩ người ta sẽ

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E3 | thăm dò | Xét nghiệm hoặc thăm khám (TEST) | [22, 29) |
| E1 | đánh giá | Xét nghiệm hoặc thăm khám (TEST) | [43, 51) |
| E2 | khám | Xét nghiệm hoặc thăm khám (TEST) | [81, 85) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- CONTEXT_OR_TRANSCRIPT: câu bị cắt, tham chiếu/mục đích chưa rõ hoặc nghi lỗi phiên âm; cần xem ngữ cảnh/audio gốc, không tự sửa văn bản.
- GENERIC_INTERVENTION: cần chốt việc giữ hành động điều trị/chẩn đoán chung khi không nêu phương pháp cụ thể.

### Thay đổi NER

- E1 “đánh giá” PROCEDURE [43, 51) → E1 “đánh giá” TEST [43, 51)
- ∅ → E3 “thăm dò” TEST [22, 29)

Nguồn: VietMed-NER train, dòng 2715 (từ 0).

## VM600-364

**Đoạn gốc:** một cái hóa trị hoặc xạ trị thì nó đều liên quan đến khử độc tại gan và khi chức năng gan bị giảm như vậy thì nay lại bị

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | hóa trị | Thủ thuật hoặc điều trị (PROCEDURE) | [8, 15) |
| E2 | xạ trị | Thủ thuật hoặc điều trị (PROCEDURE) | [21, 27) |
| E3 | gan | Bộ phận cơ thể (BODY_PART) | [65, 68) |
| E5 | chức năng gan bị giảm | Bệnh hoặc triệu chứng (CONDITION) | [76, 97) |

### RE

| Mã | Cặp có hướng | Kết luận đề xuất |
|---|---|---|
| R1 | E5 “chức năng gan bị giảm” → E1 “hóa trị” | Không có quan hệ thuộc 5 loại (NO_RELATION) |
| R2 | E5 “chức năng gan bị giảm” → E2 “xạ trị” | Không có quan hệ thuộc 5 loại (NO_RELATION) |
| R3 | E5 “chức năng gan bị giảm” → E3 “gan” | Không có quan hệ thuộc 5 loại (NO_RELATION) |

### Thay đổi NER

- ∅ → E5 “chức năng gan bị giảm” CONDITION [76, 97)
- E4 “gan” BODY_PART [86, 89) → ∅

Nguồn: VietMed-NER train, dòng 2724 (từ 0).

## VM600-365

**Đoạn gốc:** mỡ động vật này những cái đạm thịt đỏ tuy nhiên thì chúng ta vẫn phải tăng cường cung cấp năng lượng này cũng như

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

Không có thực thể thuộc sáu loại được giữ trong bản rà soát.

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

Nguồn: VietMed-NER train, dòng 2726 (từ 0).

## VM600-366

**Đoạn gốc:** xác như vậy thì mình sẽ đặt các điện cực và mình cố định lại thì mình sẽ tiến hành hai bên trên cái thời gian mà bệnh nhân

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | điện cực | Thủ thuật hoặc điều trị (PROCEDURE) | [32, 40) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- SCOPE_CONFIRMATION: cần xác nhận quy ước về thuốc/dược chất, can thiệp không dùng thuốc, thiết bị, tác nhân hoặc hoạt động thăm khám; không coi ánh xạ nguồn là xác nhận chuyên gia.

Nguồn: VietMed-NER train, dòng 2728 (từ 0).

## VM600-367

**Đoạn gốc:** hơn về diễn tiến bệnh cũng như là biết được các phương pháp điều trị tư tưởng như thế nào chúng ta sẽ cùng đi vào tìm

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | điều trị | Thủ thuật hoặc điều trị (PROCEDURE) | [60, 68) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- CONTEXT_OR_TRANSCRIPT: câu bị cắt, tham chiếu/mục đích chưa rõ hoặc nghi lỗi phiên âm; cần xem ngữ cảnh/audio gốc, không tự sửa văn bản.
- GENERIC_INTERVENTION: cần chốt việc giữ hành động điều trị/chẩn đoán chung khi không nêu phương pháp cụ thể.

Nguồn: VietMed-NER train, dòng 2732 (từ 0).

## VM600-368

**Đoạn gốc:** việc mà duy trì cái tình trạng dinh dưỡng của bệnh nhân trong suốt quá cái

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

Không có thực thể thuộc sáu loại được giữ trong bản rà soát.

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

Nguồn: VietMed-NER train, dòng 2733 (từ 0).

## VM600-369

**Đoạn gốc:** điều thứ hai cái điều thứ ba là dù là tân dược hay là các sản phẩm có nguồn

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | tân dược | Thuốc/dược chất (DRUG) | [38, 46) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

Nguồn: VietMed-NER train, dòng 2746 (từ 0).

## VM600-370

**Đoạn gốc:** thiện một cách tương đối rồi tránh tình trạng là nó làm cho nó nặng lên và cái thứ hai nữa là nếu mà chúng ta có thể đi

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

Không có thực thể thuộc sáu loại được giữ trong bản rà soát.

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Thay đổi NER

- E1 “cái thứ hai” DOSAGE [75, 86) → ∅

Nguồn: VietMed-NER train, dòng 2760 (từ 0).

## VM600-371

**Đoạn gốc:** nhiên từ thực vật người ta liên trích ra và người ta đã chứng minh rằng đó có nhiều cái công dụng trong đó có công

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

Không có thực thể thuộc sáu loại được giữ trong bản rà soát.

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

Nguồn: VietMed-NER train, dòng 2774 (từ 0).

## VM600-372

**Đoạn gốc:** retinoic acid hoặc là chúng ta sử dụng những phương pháp như là tái tạo da bằng hóa chất để mà chúng ta loại bỏ đi

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | retinoic acid | Thuốc/dược chất (DRUG) | [0, 13) |
| E2 | tái tạo da bằng hóa chất | Thủ thuật hoặc điều trị (PROCEDURE) | [64, 88) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- ONTOLOGY_SCOPE: cần chốt phạm vi thuốc/dược chất so với mỹ phẩm, thực phẩm, hóa chất nội sinh hoặc hệ vi sinh; giữ ánh xạ nguồn khi chưa có quy ước đủ rõ.

### Thay đổi NER

- E3 “loại bỏ” DRUG [104, 111) → ∅

Nguồn: VietMed-NER train, dòng 2775 (từ 0).

## VM600-373

**Đoạn gốc:** bao giờ đối tượng được việc thấu hiểu các mối liên hệ giữa ruột và não giúp

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | ruột | Bộ phận cơ thể (BODY_PART) | [59, 63) |
| E2 | não | Bộ phận cơ thể (BODY_PART) | [67, 70) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

Nguồn: VietMed-NER train, dòng 2778 (từ 0).

## VM600-374

**Đoạn gốc:** công thế này thì thì thì hổng biết làm sao sức khỏe của

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

Không có thực thể thuộc sáu loại được giữ trong bản rà soát.

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

Nguồn: VietMed-NER train, dòng 2784 (từ 0).

## VM600-375

**Đoạn gốc:** tích che phủ lỗ chân lông trên bề mặt da của bạn do đó nên bạn sẽ thấy là da của bạn ngủ dậy rất là nặng mặc đổ dầu nhiều

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E4 | lỗ chân lông | Bộ phận cơ thể (BODY_PART) | [13, 25) |
| E1 | bề mặt da | Bộ phận cơ thể (BODY_PART) | [31, 40) |
| E2 | da | Bộ phận cơ thể (BODY_PART) | [74, 76) |
| E3 | đổ dầu | Bệnh hoặc triệu chứng (CONDITION) | [109, 115) |

### RE

| Mã | Cặp có hướng | Kết luận đề xuất |
|---|---|---|
| R1 | E3 “đổ dầu” → E4 “lỗ chân lông” | Không có quan hệ thuộc 5 loại (NO_RELATION) |
| R2 | E3 “đổ dầu” → E1 “bề mặt da” | Chưa rõ — cần chốt (CHUA_RO) |
| R3 | E3 “đổ dầu” → E2 “da” | Có vị trí ở (located_at) |

### Cần chốt

- UNRESOLVED_RE: còn cặp CHUA_RO; tuyệt đối không đổi thành NO_RELATION khi xuất huấn luyện.

### Thay đổi NER

- ∅ → E4 “lỗ chân lông” BODY_PART [13, 25)

Nguồn: VietMed-NER train, dòng 2790 (từ 0).

## VM600-376

**Đoạn gốc:** fumarate sản phẩm đông y mà nhiều sản phẩm như vậy thì không biết là nó có thể là giảm cái việc là xơ vữa mảng

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | fumarate | Thuốc/dược chất (DRUG) | [0, 8) |
| E2 | sản phẩm đông y | Thuốc/dược chất (DRUG) | [9, 24) |
| E3 | xơ vữa mảng | Bệnh hoặc triệu chứng (CONDITION) | [99, 110) |

### RE

| Mã | Cặp có hướng | Kết luận đề xuất |
|---|---|---|
| R1 | E3 “xơ vữa mảng” → E1 “fumarate” | Chưa rõ — cần chốt (CHUA_RO) |
| R2 | E3 “xơ vữa mảng” → E2 “sản phẩm đông y” | Chưa rõ — cần chốt (CHUA_RO) |

### Cần chốt

- CONTEXT_OR_TRANSCRIPT: câu bị cắt, tham chiếu/mục đích chưa rõ hoặc nghi lỗi phiên âm; cần xem ngữ cảnh/audio gốc, không tự sửa văn bản.
- ONTOLOGY_SCOPE: cần chốt phạm vi thuốc/dược chất so với mỹ phẩm, thực phẩm, hóa chất nội sinh hoặc hệ vi sinh; giữ ánh xạ nguồn khi chưa có quy ước đủ rõ.
- UNRESOLVED_RE: còn cặp CHUA_RO; tuyệt đối không đổi thành NO_RELATION khi xuất huấn luyện.

### Thay đổi NER

- E2 “đông y” PROCEDURE [18, 24) → E2 “sản phẩm đông y” DRUG [9, 24)

Nguồn: VietMed-NER train, dòng 2796 (từ 0).

## VM600-377

**Đoạn gốc:** với lại chẳng nói da nhạy cảm chúng ta sẽ sử dụng một cái gọi là các biện pháp lại nghiệm pháp kích thích và chúng ta

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | da nhạy cảm | Bệnh hoặc triệu chứng (CONDITION) | [18, 29) |
| E2 | nghiệm pháp kích thích | Xét nghiệm hoặc thăm khám (TEST) | [83, 105) |

### RE

| Mã | Cặp có hướng | Kết luận đề xuất |
|---|---|---|
| R1 | E1 “da nhạy cảm” → E2 “nghiệm pháp kích thích” | Chưa rõ — cần chốt (CHUA_RO) |

### Cần chốt

- CONTEXT_OR_TRANSCRIPT: câu bị cắt, tham chiếu/mục đích chưa rõ hoặc nghi lỗi phiên âm; cần xem ngữ cảnh/audio gốc, không tự sửa văn bản.
- UNRESOLVED_RE: còn cặp CHUA_RO; tuyệt đối không đổi thành NO_RELATION khi xuất huấn luyện.

### Thay đổi NER

- E2 “biện pháp lại nghiệm pháp kích thích” PROCEDURE [69, 105) → E2 “nghiệm pháp kích thích” TEST [83, 105)

Nguồn: VietMed-NER train, dòng 2801 (từ 0).

## VM600-378

**Đoạn gốc:** là có thể bây giờ thì mình cũng chưa biết được nhưng mà có thể là đấy là những cái tác nhân mà có thể làm cho

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

Không có thực thể thuộc sáu loại được giữ trong bản rà soát.

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

Nguồn: VietMed-NER train, dòng 2804 (từ 0).

## VM600-379

**Đoạn gốc:** này trong ngày hôm nay vâng và trong khi mà chờ đợi các khán

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

Không có thực thể thuộc sáu loại được giữ trong bản rà soát.

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

Nguồn: VietMed-NER train, dòng 2813 (từ 0).

## VM600-380

**Đoạn gốc:** nào và tất cả những cái vấn đề khác về cơ xương khớp vân vân như vậy thì đối với một người lớn tuổi mà có bệnh

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | cơ xương khớp | Bộ phận cơ thể (BODY_PART) | [39, 52) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Thay đổi NER

- E2 “một người” DOSAGE [81, 90) → ∅

Nguồn: VietMed-NER train, dòng 2815 (từ 0).

## VM600-381

**Đoạn gốc:** sẽ tùy thuộc vào từng loại từng nhóm người bệnh và tùy thuộc vào nhiều yếu tố khác nhau như vậy chúng ta thấy rằng

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

Không có thực thể thuộc sáu loại được giữ trong bản rà soát.

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

Nguồn: VietMed-NER train, dòng 2822 (từ 0).

## VM600-382

**Đoạn gốc:** thuật kích thích não sâu thì nó sẽ kéo dài trung bình khoảng từ năm cho tới bảy ngày ở trong bệnh viện và sau khi bảy ngày

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | kích thích não sâu | Thủ thuật hoặc điều trị (PROCEDURE) | [6, 24) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- CONTEXT_OR_TRANSCRIPT: câu bị cắt, tham chiếu/mục đích chưa rõ hoặc nghi lỗi phiên âm; cần xem ngữ cảnh/audio gốc, không tự sửa văn bản.

### Thay đổi NER

- E2 “trung bình” DOSAGE [43, 53) → ∅

Nguồn: VietMed-NER train, dòng 2827 (từ 0).

## VM600-383

**Đoạn gốc:** cũng đã đưa ra dựa theo những cái nghiên cứu như vậy và ta thấy rằng là mục tiêu đầu tiên đó là giảm từ năm đến mười phần

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

Không có thực thể thuộc sáu loại được giữ trong bản rà soát.

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Thay đổi NER

- E1 “nghiên cứu” TEST [34, 44) → ∅
- E2 “từ năm đến mười phần” DOSAGE [101, 121) → ∅

Nguồn: VietMed-NER train, dòng 2847 (từ 0).

## VM600-384

**Đoạn gốc:** viêm tắc chúng ta bị viêm tĩnh mạch đấy là những biến chứng mà những người bị suy giãn tĩnh mạch nhiều khi mà chúng ta

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | viêm tắc | Bệnh hoặc triệu chứng (CONDITION) | [0, 8) |
| E2 | viêm tĩnh mạch | Bệnh hoặc triệu chứng (CONDITION) | [21, 35) |
| E4 | biến chứng | Bệnh hoặc triệu chứng (CONDITION) | [49, 59) |
| E5 | suy giãn tĩnh mạch | Bệnh hoặc triệu chứng (CONDITION) | [78, 96) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- CONTEXT_OR_TRANSCRIPT: câu bị cắt, tham chiếu/mục đích chưa rõ hoặc nghi lỗi phiên âm; cần xem ngữ cảnh/audio gốc, không tự sửa văn bản.

### Thay đổi NER

- E1 “viêm” CONDITION [0, 4) → E1 “viêm tắc” CONDITION [0, 8)
- E2 “viêm” CONDITION [21, 25) → E2 “viêm tĩnh mạch” CONDITION [21, 35)
- E3 “tĩnh mạch” BODY_PART [26, 35) → ∅

Nguồn: VietMed-NER train, dòng 2855 (từ 0).

## VM600-385

**Đoạn gốc:** các thực phẩm mà có chứa vitamin và khoáng chất rồi có thể uống bổ sung thêm

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | vitamin | Thuốc/dược chất (DRUG) | [25, 32) |
| E2 | khoáng chất | Thuốc/dược chất (DRUG) | [36, 47) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- ONTOLOGY_SCOPE: cần chốt phạm vi thuốc/dược chất so với mỹ phẩm, thực phẩm, hóa chất nội sinh hoặc hệ vi sinh; giữ ánh xạ nguồn khi chưa có quy ước đủ rõ.

Nguồn: VietMed-NER train, dòng 2856 (từ 0).

## VM600-386

**Đoạn gốc:** còn ảnh hưởng rất nhiều thậm chí là đến tâm lý của bệnh nhân và giờ đây thì chúng tôi xin được mời

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

Không có thực thể thuộc sáu loại được giữ trong bản rà soát.

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Thay đổi NER

- E1 “rất nhiều” DOSAGE [14, 23) → ∅

Nguồn: VietMed-NER train, dòng 2860 (từ 0).

## VM600-387

**Đoạn gốc:** cũng đã cho làm một số các cái thăm dò rồi chụp phim vân vân và sơ bộ thì chúng ta biết rằng là bác đã có cái khảo sát

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E3 | thăm dò | Xét nghiệm hoặc thăm khám (TEST) | [31, 38) |
| E1 | chụp phim | Xét nghiệm hoặc thăm khám (TEST) | [43, 52) |
| E2 | khảo sát | Xét nghiệm hoặc thăm khám (TEST) | [110, 118) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- GENERIC_INTERVENTION: cần chốt việc giữ hành động điều trị/chẩn đoán chung khi không nêu phương pháp cụ thể.
- SCOPE_CONFIRMATION: cần xác nhận quy ước về thuốc/dược chất, can thiệp không dùng thuốc, thiết bị, tác nhân hoặc hoạt động thăm khám; không coi ánh xạ nguồn là xác nhận chuyên gia.

### Thay đổi NER

- E2 “khảo sát” DRUG [110, 118) → E2 “khảo sát” TEST [110, 118)
- ∅ → E3 “thăm dò” TEST [31, 38)

Nguồn: VietMed-NER train, dòng 2866 (từ 0).

## VM600-388

**Đoạn gốc:** thời đại chính vì là có rất là nhiều các cái tác dụng phụ như thế này cho nên bản thân các bác sĩ rồi bản thân những cái

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | tác dụng phụ | Bệnh hoặc triệu chứng (CONDITION) | [45, 57) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- GENERIC_MENTION: cần chốt có giữ bệnh/triệu chứng/biến chứng chung và tham chiếu không định danh trong NER hay không.

Nguồn: VietMed-NER train, dòng 2881 (từ 0).

## VM600-389

**Đoạn gốc:** dụng các sản phẩm mà có chứa những hoạt chất tẩy rửa bề mặt này lâu dài thì sẽ vô tình làm rửa trôi cả cái lớp

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | hoạt chất tẩy rửa bề mặt | Thuốc/dược chất (DRUG) | [35, 59) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- ONTOLOGY_SCOPE: cần chốt phạm vi thuốc/dược chất so với mỹ phẩm, thực phẩm, hóa chất nội sinh hoặc hệ vi sinh; giữ ánh xạ nguồn khi chưa có quy ước đủ rõ.

### Thay đổi NER

- E1 “hoạt chất” DRUG [35, 44) → E1 “hoạt chất tẩy rửa bề mặt” DRUG [35, 59)

Nguồn: VietMed-NER train, dòng 2903 (từ 0).

## VM600-390

**Đoạn gốc:** cuộc sống của bệnh nhân tốt hơn và bên cạnh điều trị kích thích não sâu thì chúng ta cũng được biết các điều trị can

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E2 | kích thích não sâu | Thủ thuật hoặc điều trị (PROCEDURE) | [53, 71) |
| E3 | điều trị | Thủ thuật hoặc điều trị (PROCEDURE) | [104, 112) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- GENERIC_INTERVENTION: cần chốt việc giữ hành động điều trị/chẩn đoán chung khi không nêu phương pháp cụ thể.

### Thay đổi NER

- E1 “điều trị” PROCEDURE [44, 52) → ∅

Nguồn: VietMed-NER train, dòng 2928 (từ 0).

## VM600-391

**Đoạn gốc:** một cái hành trình như vậy thì cái việc điều trị của béo phì ở trong một cái giai đoạn này nó chỉ

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | điều trị | Thủ thuật hoặc điều trị (PROCEDURE) | [40, 48) |
| E2 | béo phì | Bệnh hoặc triệu chứng (CONDITION) | [53, 60) |

### RE

| Mã | Cặp có hướng | Kết luận đề xuất |
|---|---|---|
| R1 | E2 “béo phì” → E1 “điều trị” | Được điều trị bằng phương pháp (treated_by_procedure) |

### Cần chốt

- GENERIC_INTERVENTION: cần chốt việc giữ hành động điều trị/chẩn đoán chung khi không nêu phương pháp cụ thể.

Nguồn: VietMed-NER train, dòng 2937 (từ 0).

## VM600-392

**Đoạn gốc:** vâng và hiện tại thì thời lượng của chương trình cũng không còn nhiều tuy nhiên còn rất là nhiều khán giả đã gọi điện tới và mong đợi được sự tư vấn của

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

Không có thực thể thuộc sáu loại được giữ trong bản rà soát.

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

Nguồn: VietMed-NER train, dòng 2946 (từ 0).

## VM600-393

**Đoạn gốc:** nhận được phần thưởng từ chương trình mà thôi vâng ạ như là bác sĩ chia sẻ thì rõ ràng là đông trùng hạ thảo thì có cái

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | đông trùng hạ thảo | Thuốc/dược chất (DRUG) | [90, 108) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- ONTOLOGY_SCOPE: cần chốt phạm vi thuốc/dược chất so với mỹ phẩm, thực phẩm, hóa chất nội sinh hoặc hệ vi sinh; giữ ánh xạ nguồn khi chưa có quy ước đủ rõ.

Nguồn: VietMed-NER train, dòng 2947 (từ 0).

## VM600-394

**Đoạn gốc:** không được nghỉ ngơi chính vì vậy cho nên là cái lời khuyên của chúng ta trong trường hợp này thì khi mà chúng ta làm

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

Không có thực thể thuộc sáu loại được giữ trong bản rà soát.

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

Nguồn: VietMed-NER train, dòng 2948 (từ 0).

## VM600-395

**Đoạn gốc:** được cái tình trạng của anh hiện tại đúng không ạ chứ ở đây thì chúng tôi cũng chỉ thăm khám qua những cái lời

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | thăm khám | Xét nghiệm hoặc thăm khám (TEST) | [83, 92) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Thay đổi NER

- E1 “thăm khám” PROCEDURE [83, 92) → E1 “thăm khám” TEST [83, 92)

Nguồn: VietMed-NER train, dòng 2960 (từ 0).

## VM600-396

**Đoạn gốc:** điều trị bằng các loại thuốc ức chế miễn dịch mạnh và thường có những mặt trái đáng kể không ít trong số đó bao gồm

**Trạng thái:** Cần chốt ngữ cảnh/quy ước

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | điều trị | Thủ thuật hoặc điều trị (PROCEDURE) | [0, 8) |
| E2 | thuốc ức chế miễn dịch | Thuốc/dược chất (DRUG) | [23, 45) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

### Cần chốt

- GENERIC_INTERVENTION: cần chốt việc giữ hành động điều trị/chẩn đoán chung khi không nêu phương pháp cụ thể.

### Thay đổi NER

- E2 “thuốc” DRUG [23, 28) → E2 “thuốc ức chế miễn dịch” DRUG [23, 45)
- E3 “ức chế miễn dịch” DRUG [29, 45) → ∅

Nguồn: VietMed-NER train, dòng 2972 (từ 0).

## VM600-397

**Đoạn gốc:** tất cả đấy là những lời có cánh những cái lời mà nó chả có tính khoa học gì cả thế cho nên là điều đầu tiên khuyên bác là

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

Không có thực thể thuộc sáu loại được giữ trong bản rà soát.

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

Nguồn: VietMed-NER train, dòng 2973 (từ 0).

## VM600-398

**Đoạn gốc:** mảng xơ vữa này để giúp cho máu thông lên não lên tim tốt và từ đó cải thiện các triệu chứng như là đau đầu hoa mắt chóng

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | mảng xơ vữa | Bệnh hoặc triệu chứng (CONDITION) | [0, 11) |
| E2 | máu | Bộ phận cơ thể (BODY_PART) | [28, 31) |
| E3 | não | Bộ phận cơ thể (BODY_PART) | [42, 45) |
| E4 | tim | Bộ phận cơ thể (BODY_PART) | [50, 53) |
| E7 | đau đầu | Bệnh hoặc triệu chứng (CONDITION) | [100, 107) |
| E8 | hoa mắt | Bệnh hoặc triệu chứng (CONDITION) | [108, 115) |

### RE

| Mã | Cặp có hướng | Kết luận đề xuất |
|---|---|---|
| R1 | E1 “mảng xơ vữa” → E2 “máu” | Không có quan hệ thuộc 5 loại (NO_RELATION) |
| R2 | E1 “mảng xơ vữa” → E3 “não” | Không có quan hệ thuộc 5 loại (NO_RELATION) |
| R3 | E1 “mảng xơ vữa” → E4 “tim” | Không có quan hệ thuộc 5 loại (NO_RELATION) |
| R4 | E7 “đau đầu” → E2 “máu” | Không có quan hệ thuộc 5 loại (NO_RELATION) |
| R5 | E7 “đau đầu” → E3 “não” | Không có quan hệ thuộc 5 loại (NO_RELATION) |
| R6 | E7 “đau đầu” → E4 “tim” | Không có quan hệ thuộc 5 loại (NO_RELATION) |
| R7 | E8 “hoa mắt” → E2 “máu” | Không có quan hệ thuộc 5 loại (NO_RELATION) |
| R8 | E8 “hoa mắt” → E3 “não” | Không có quan hệ thuộc 5 loại (NO_RELATION) |
| R9 | E8 “hoa mắt” → E4 “tim” | Không có quan hệ thuộc 5 loại (NO_RELATION) |

### Thay đổi NER

- E5 “cải thiện” PROCEDURE [67, 76) → ∅
- E6 “triệu chứng” CONDITION [81, 92) → ∅

Nguồn: VietMed-NER train, dòng 2986 (từ 0).

## VM600-399

**Đoạn gốc:** chuột rút đúng không ạ ở đây chuột rút thì chúng ta nhớ rằng là nó cũng có một số các cái nhóm nguyên nhân thông thường chúng ta sẽ nghĩ ngay đến cái câu chuyện

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | chuột rút | Bệnh hoặc triệu chứng (CONDITION) | [0, 9) |
| E2 | chuột rút | Bệnh hoặc triệu chứng (CONDITION) | [29, 38) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

Nguồn: VietMed-NER train, dòng 2991 (từ 0).

## VM600-400

**Đoạn gốc:** sinh bị rụng tóc hay không cảm ơn em các chị em phụ nữ thân mến

**Trạng thái:** Đã rà soát AI, chưa phát hiện điểm cần chốt; vẫn chưa phải gold

### NER

| Mã | Cụm từ | Nhãn | Vị trí |
|---|---|---|---|
| E1 | rụng tóc | Bệnh hoặc triệu chứng (CONDITION) | [8, 16) |

### RE

Không có cặp thực thể hợp lệ theo schema hiện tại. Điều này không có nghĩa đoạn không có thông tin y khoa.

Nguồn: VietMed-NER train, dòng 3007 (từ 0).

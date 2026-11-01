# Phiếu xác nhận 10 mẫu VietMed-NER

Nguồn: leduckhai/VietMed-NER, tập train. Chỉ số train[n] bắt đầu từ 0. Giữ nguyên văn bản; dấu ngoặc và chữ đậm chỉ làm nổi bật thực thể có sẵn.

Cách điền: đánh dấu thực thể đúng; sửa hoặc gạch bỏ thực thể sai và thêm thực thể còn thiếu trong phần ghi chú. Với từng quan hệ, chọn Có / Không / Chưa rõ theo nội dung đoạn. Nhãn từ dữ liệu gốc có thể sai; các quan hệ dưới đây chỉ là câu hỏi để kiểm tra, chưa có đáp án. Nếu đã sửa thực thể khiến cặp không còn hợp lệ, gạch bỏ cặp và ghi lý do. Ô chưa đánh dấu có nghĩa là chưa xử lý, không tự tính là Không.

Bác sĩ/người kiểm duyệt: __________________    Ngày: __________________

## Mẫu 1 — train[498]

> thế nào đối với trường hợp của bác không những là **[đau]** ở cái vùng **[lưng]** **[thắt lưng]** mà nó còn lan xuống **[chân]** lan xuống **[mông]** thấy chính vì vậy cho nên là khi mà

Phiếu xác nhận:
```text
Thực thể:
☐ đau: bệnh/triệu chứng
☐ lưng: bộ phận cơ thể
☐ thắt lưng: bộ phận cơ thể
☐ chân: bộ phận cơ thể
☐ mông: bộ phận cơ thể

Quan hệ cần xác nhận:
đau → lưng: nằm ở
  ☐ Có    ☐ Không    ☐ Chưa rõ
đau → thắt lưng: nằm ở
  ☐ Có    ☐ Không    ☐ Chưa rõ
đau → chân: nằm ở
  ☐ Có    ☐ Không    ☐ Chưa rõ
đau → mông: nằm ở
  ☐ Có    ☐ Không    ☐ Chưa rõ

Sửa/bổ sung thực thể hoặc quan hệ: __________________
Ghi chú hoặc chỗ chưa rõ: __________________
☐ Đã kiểm tra xong toàn bộ đoạn
☐ Còn mục cần xem lại
```

## Mẫu 2 — train[105]

> với cơ chế của cái hình thành **[cục máu đông]** ở trong **[tim]** giờ đó nên **[thuốc chống tiểu cầu]** không phải là cái gì

Phiếu xác nhận:
```text
Thực thể:
☐ cục máu đông: bệnh/triệu chứng
☐ tim: bộ phận cơ thể
☐ thuốc chống tiểu cầu: thuốc

Quan hệ cần xác nhận:
cục máu đông → tim: nằm ở
  ☐ Có    ☐ Không    ☐ Chưa rõ
cục máu đông → thuốc chống tiểu cầu: được điều trị bằng thuốc
  ☐ Có    ☐ Không    ☐ Chưa rõ

Sửa/bổ sung thực thể hoặc quan hệ: __________________
Ghi chú hoặc chỗ chưa rõ: __________________
☐ Đã kiểm tra xong toàn bộ đoạn
☐ Còn mục cần xem lại
```

## Mẫu 3 — train[998]

> nó không hình thành nữa là không còn **[cục máu đông]** trong **[tim]** nữa thì như vậy nó sẽ không có gây ra những cái **[tắc mạch]**

Phiếu xác nhận:
```text
Thực thể:
☐ cục máu đông: bệnh/triệu chứng
☐ tim: bộ phận cơ thể
☐ tắc mạch: bệnh/triệu chứng

Quan hệ cần xác nhận:
cục máu đông → tim: nằm ở
  ☐ Có    ☐ Không    ☐ Chưa rõ
tắc mạch → tim: nằm ở
  ☐ Có    ☐ Không    ☐ Chưa rõ

Sửa/bổ sung thực thể hoặc quan hệ: __________________
Ghi chú hoặc chỗ chưa rõ: __________________
☐ Đã kiểm tra xong toàn bộ đoạn
☐ Còn mục cần xem lại
```

## Mẫu 4 — train[104]

> nếu chưa đến được bệnh viện thì chúng ta nên đến cơ sở y tế gần nhà thì được **[khám]** và và **[điều trị]** **[thuốc]** **[huyết áp]** ngay tại

Phiếu xác nhận:
```text
Thực thể:
☐ khám: xét nghiệm/phương pháp chẩn đoán
☐ điều trị: thủ thuật/phương pháp điều trị
☐ thuốc: thuốc
☐ huyết áp: bệnh/triệu chứng

Quan hệ cần xác nhận:
huyết áp → thuốc: được điều trị bằng thuốc
  ☐ Có    ☐ Không    ☐ Chưa rõ
huyết áp → điều trị: được điều trị bằng thủ thuật/phương pháp điều trị
  ☐ Có    ☐ Không    ☐ Chưa rõ
huyết áp → khám: được chẩn đoán bằng
  ☐ Có    ☐ Không    ☐ Chưa rõ

Sửa/bổ sung thực thể hoặc quan hệ: __________________
Ghi chú hoặc chỗ chưa rõ: __________________
☐ Đã kiểm tra xong toàn bộ đoạn
☐ Còn mục cần xem lại
```

## Mẫu 5 — train[119]

> chẳng hạn ăn uống **[kẽm]** vào ăn ngon **[miệng]** hơn uống **[selen]** thì người **[ung thư]** rất hay **[rụng tóc]** ạ thì **[selen]** vào **[tóc]**

Phiếu xác nhận:
```text
Thực thể:
☐ kẽm: thuốc
☐ miệng: bộ phận cơ thể
☐ selen (lần 1): thuốc
☐ ung thư: bệnh/triệu chứng
☐ rụng tóc: bệnh/triệu chứng
☐ selen (lần 2): thuốc
☐ tóc: bộ phận cơ thể

Quan hệ cần xác nhận:
ung thư → miệng: nằm ở
  ☐ Có    ☐ Không    ☐ Chưa rõ
ung thư → tóc: nằm ở
  ☐ Có    ☐ Không    ☐ Chưa rõ
rụng tóc → miệng: nằm ở
  ☐ Có    ☐ Không    ☐ Chưa rõ
rụng tóc → tóc: nằm ở
  ☐ Có    ☐ Không    ☐ Chưa rõ
ung thư → kẽm: được điều trị bằng thuốc
  ☐ Có    ☐ Không    ☐ Chưa rõ
ung thư → selen (lần 1): được điều trị bằng thuốc
  ☐ Có    ☐ Không    ☐ Chưa rõ
ung thư → selen (lần 2): được điều trị bằng thuốc
  ☐ Có    ☐ Không    ☐ Chưa rõ
rụng tóc → kẽm: được điều trị bằng thuốc
  ☐ Có    ☐ Không    ☐ Chưa rõ
rụng tóc → selen (lần 1): được điều trị bằng thuốc
  ☐ Có    ☐ Không    ☐ Chưa rõ
rụng tóc → selen (lần 2): được điều trị bằng thuốc
  ☐ Có    ☐ Không    ☐ Chưa rõ

Sửa/bổ sung thực thể hoặc quan hệ: __________________
Ghi chú hoặc chỗ chưa rõ: __________________
☐ Đã kiểm tra xong toàn bộ đoạn
☐ Còn mục cần xem lại
```

## Mẫu 6 — train[314]

> pháp **[điều trị]** **[thuốc]** thì **[phẫu thuật kích thích não sâu]** nó sẽ giúp **[cải thiện]** **[triệu chứng]** cho người bệnh khá là tốt mà khi

Phiếu xác nhận:
```text
Thực thể:
☐ điều trị: thủ thuật/phương pháp điều trị
☐ thuốc: thuốc
☐ phẫu thuật kích thích não sâu: thủ thuật/phương pháp điều trị
☐ cải thiện: thủ thuật/phương pháp điều trị
☐ triệu chứng: bệnh/triệu chứng

Quan hệ cần xác nhận:
triệu chứng → thuốc: được điều trị bằng thuốc
  ☐ Có    ☐ Không    ☐ Chưa rõ
triệu chứng → điều trị: được điều trị bằng thủ thuật/phương pháp điều trị
  ☐ Có    ☐ Không    ☐ Chưa rõ
triệu chứng → phẫu thuật kích thích não sâu: được điều trị bằng thủ thuật/phương pháp điều trị
  ☐ Có    ☐ Không    ☐ Chưa rõ
triệu chứng → cải thiện: được điều trị bằng thủ thuật/phương pháp điều trị
  ☐ Có    ☐ Không    ☐ Chưa rõ

Sửa/bổ sung thực thể hoặc quan hệ: __________________
Ghi chú hoặc chỗ chưa rõ: __________________
☐ Đã kiểm tra xong toàn bộ đoạn
☐ Còn mục cần xem lại
```

## Mẫu 7 — train[28]

> họ rơi vào **[trầm cảm]** mà người ta thấy ngay cả những người **[mổ]** xong rồi thì các

Phiếu xác nhận:
```text
Thực thể:
☐ trầm cảm: bệnh/triệu chứng
☐ mổ: thủ thuật/phương pháp điều trị

Quan hệ cần xác nhận:
trầm cảm → mổ: được điều trị bằng thủ thuật/phương pháp điều trị
  ☐ Có    ☐ Không    ☐ Chưa rõ

Sửa/bổ sung thực thể hoặc quan hệ: __________________
Ghi chú hoặc chỗ chưa rõ: __________________
☐ Đã kiểm tra xong toàn bộ đoạn
☐ Còn mục cần xem lại
```

## Mẫu 8 — train[229]

> điều kiện mà chúng ta đến địa bàn tỉnh vĩnh long là phải có cái giấy **[xét nghiệm]** **[sarscov2]** như vậy thì chị có thể

Phiếu xác nhận:
```text
Thực thể:
☐ xét nghiệm: xét nghiệm/phương pháp chẩn đoán
☐ sarscov2: bệnh/triệu chứng

Quan hệ cần xác nhận:
sarscov2 → xét nghiệm: được chẩn đoán bằng
  ☐ Có    ☐ Không    ☐ Chưa rõ

Sửa/bổ sung thực thể hoặc quan hệ: __________________
Ghi chú hoặc chỗ chưa rõ: __________________
☐ Đã kiểm tra xong toàn bộ đoạn
☐ Còn mục cần xem lại
```

## Mẫu 9 — train[674]

> nghiệm lúc đói khi chúng ta làm **[xét nghiệm]** **[đường huyết]** chuẩn vân vân nhưng mà hiện nay bên cạnh cái việc mà **[xét nghiệm]** cái

Phiếu xác nhận:
```text
Thực thể:
☐ xét nghiệm (lần 1): xét nghiệm/phương pháp chẩn đoán
☐ đường huyết: thông tin liều thuốc
☐ xét nghiệm (lần 2): xét nghiệm/phương pháp chẩn đoán

Quan hệ cần xác nhận:
Chưa có cặp phù hợp từ các thực thể hiện tại.
☐ Xác nhận không có cặp phù hợp trong đoạn
☐ Cần sửa/bổ sung thực thể rồi xét lại
☐ Cần thêm ngữ cảnh

Sửa/bổ sung thực thể hoặc quan hệ: __________________
Ghi chú hoặc chỗ chưa rõ: __________________
☐ Đã kiểm tra xong toàn bộ đoạn
☐ Còn mục cần xem lại
```

## Mẫu 10 — train[471]

> là chúng ta uống **[bốn viên]** một ngày chia **[hai lần]** sáng chiều và khi mà chúng ta

Phiếu xác nhận:
```text
Thực thể:
☐ bốn viên: thông tin liều thuốc
☐ hai lần: thông tin liều thuốc

Quan hệ cần xác nhận:
Chưa có cặp phù hợp từ các thực thể hiện tại.
☐ Xác nhận không có cặp phù hợp trong đoạn
☐ Cần sửa/bổ sung thực thể rồi xét lại
☐ Cần thêm ngữ cảnh

Sửa/bổ sung thực thể hoặc quan hệ: __________________
Ghi chú hoặc chỗ chưa rõ: __________________
☐ Đã kiểm tra xong toàn bộ đoạn
☐ Còn mục cần xem lại
```


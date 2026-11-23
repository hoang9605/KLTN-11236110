# Pattern bank RE v3 (tự sinh bởi mine_patterns.py)

Nguồn: re_gold_v1, re_ai_v2. CHUA_RO đã bị loại.

| Quan hệ | Cặp dương | Cặp âm | Pattern dương | Pattern âm |
|---|---:|---:|---:|---:|
| diagnosed_by | 6 | 63 | 2 | 26 |
| has_dosage | 0 | 80 | 0 | 38 |
| located_at | 34 | 154 | 23 | 43 |
| treated_by | 9 | 123 | 5 | 56 |
| treated_by_procedure | 15 | 72 | 11 | 36 |

## diagnosed_by — dương

| Số lần | Thứ tự | Chuỗi giữa | Ví dụ (head → tail) |
|---:|---|---|---|
| 5 | T…H | `(liền kề)` | covid19 → test |
| 1 | H…T | `<LONG>` | da nhạy cảm → nghiệm pháp kích thích |

## diagnosed_by — âm

| Số lần | Thứ tự | Chuỗi giữa | Ví dụ (head → tail) |
|---:|---|---|---|
| 18 | T…H | `<LONG>` | xơ vữa động mạch → sức đề kháng |
| 15 | H…T | `<LONG>` | béo phì → chuyển hóa |
| 7 | H…T | `(liền kề)` | rối loạn → chuyển hóa |
| 1 | T…H | `[BODY_PART] mình ngoài` | ung thư → tự bảo vệ |
| 1 | T…H | `[CONDITION] âm tính hoặc` | dương tính → xét nghiệm |
| 1 | T…H | `[DOSAGE] rất là` | mệt mỏi → sức đề kháng |
| 1 | T…H | `bệnh` | rối loạn → chuyển hóa |
| 1 | H…T | `các nhà` | ung thư → nghiên cứu |
| 1 | H…T | `diệt thì nói không` | bị tiêu → xét nghiệm |
| 1 | H…T | `do đó cái việc mà` | virus → xét nghiệm |
| 1 | H…T | `hoặc là khỏi hẳn` | đái tháo đường → quá trình lão hóa |
| 1 | H…T | `một lĩnh vực` | di truyền → nghiên cứu |
| 1 | H…T | `như qua các` | tăng cân → nghiên cứu |
| 1 | H…T | `nó [CONDITION] diệt thì nói không` | virus → xét nghiệm |
| 1 | T…H | `nó làm` | chậm → quá trình lão hóa |

## has_dosage — âm

| Số lần | Thứ tự | Chuỗi giữa | Ví dụ (head → tail) |
|---:|---|---|---|
| 19 | T…H | `<LONG>` | hòe hoa → cao |
| 18 | H…T | `<LONG>` | kem dưỡng ẩm → nồng độ |
| 6 | H…T | `(liền kề)` | glycerin → nồng độ cao |
| 3 | T…H | `(liền kề)` | axit → rất nhiều |
| 1 | T…H | `[BODY_PART] là` | axit → ph |
| 1 | H…T | `[CONDITION] ở việt nam thì có` | phòng chống → rất nhiều |
| 1 | H…T | `[DOSAGE]` | polysaccharide → gấp bảy lần |
| 1 | T…H | `[DOSAGE] các cái` | chế phẩm đông trùng hạ thảo → cao |
| 1 | T…H | `[DRUG] béo` | omega3 → rất nhiều |
| 1 | T…H | `[DRUG] béo [DRUG] mà` | axit → rất nhiều |
| 1 | T…H | `[DRUG] béo [DRUG] mà [DRUG] béo` | omega3 → rất nhiều |
| 1 | T…H | `[DRUG] có hai loại nấm là` | nấm đông trùng hạ thảo → một trăm phần trăm |
| 1 | H…T | `[DRUG] đã được chứng minh rằng` | l-carnitine → thứ nhất |
| 1 | T…H | `chúng ta` | tuân thủ → liều thuốc |
| 1 | T…H | `các cái` | chế phẩm đông trùng hạ thảo → gấp bảy lần |

## located_at — dương

| Số lần | Thứ tự | Chuỗi giữa | Ví dụ (head → tail) |
|---:|---|---|---|
| 7 | H…T | `(liền kề)` | tổn thương → đường tiêu hóa |
| 4 | H…T | `ở` | vữa xơ động mạch → vành |
| 2 | T…H | `<LONG>` | yếu ớt → mái tóc |
| 2 | T…H | `bị` | tổn thương → cơ quan |
| 1 | T…H | `chúng ta dễ bị` | tổn thương → đường tiêu hóa |
| 1 | T…H | `chúng ta là` | mất màu trắng → da |
| 1 | T…H | `chúng ta sẽ trở nên` | khô ngứa bong tróc → da |
| 1 | H…T | `các cái` | thoái hóa → mạch |
| 1 | H…T | `của cái` | viêm → phổi |
| 1 | T…H | `của mình nó` | căng → da |
| 1 | T…H | `là [DRUG]` | đổ dầu → da |
| 1 | H…T | `lên` | tác dụng phụ → đường tiêu hóa |
| 1 | H…T | `lên [BODY_PART] lên các cái hệ` | tác dụng phụ → nội tạng |
| 1 | H…T | `nhiều ở cái` | tê bì → bàn tay |
| 1 | T…H | `nó bị` | viêm → khớp |

## located_at — âm

| Số lần | Thứ tự | Chuỗi giữa | Ví dụ (head → tail) |
|---:|---|---|---|
| 59 | T…H | `<LONG>` | tê liệt tay → gáy |
| 50 | H…T | `<LONG>` | mảng xơ vữa → máu |
| 4 | T…H | `(liền kề)` | tê liệt tay → thần kinh |
| 2 | H…T | `(liền kề)` | căng → da |
| 1 | H…T | `[BODY_PART] mà` | vi khuẩn → dna |
| 1 | H…T | `[CONDITION]` | huyết áp cao → tim mạch |
| 1 | T…H | `[CONDITION] nhiều khi` | nhớ nhớ quên quên → mạch vành |
| 1 | T…H | `[CONDITION] nhiều khi [CONDITION] bị` | tiền đình → mạch vành |
| 1 | T…H | `[CONDITION] nhiều khi [CONDITION] bị [CONDITION]` | đau đầu → mạch vành |
| 1 | H…T | `[CONDITION] này ở kia ở` | hoa mắt → mạch vành |
| 1 | H…T | `[CONDITION] thăng bằng có thể về` | yếu chân → mắt |
| 1 | H…T | `[DRUG] cho` | sự đói → cơ thể |
| 1 | T…H | `bác sĩ về bệnh` | parkinson → thần kinh |
| 1 | T…H | `cho người bệnh` | parkinson → tế bào gốc |
| 1 | T…H | `chúng ta dẫn đến` | suy kiệt → cơ thể |

## treated_by — dương

| Số lần | Thứ tự | Chuỗi giữa | Ví dụ (head → tail) |
|---:|---|---|---|
| 4 | H…T | `<LONG>` | tim đập nhanh → thuốc để giảm nhịp tim |
| 2 | T…H | `<LONG>` | da nhạy cảm → niacinamide |
| 1 | T…H | `cho một` | nhiễm trùng → kháng sinh |
| 1 | H…T | `chạp mà [PROCEDURE] với thuốc` | chậm → levodopa |
| 1 | T…H | `để điều trị cho` | bệnh gút → corticoid |

## treated_by — âm

| Số lần | Thứ tự | Chuỗi giữa | Ví dụ (head → tail) |
|---:|---|---|---|
| 29 | T…H | `<LONG>` | nhiều dầu → kem dưỡng |
| 25 | H…T | `<LONG>` | căng thẳng → hormone |
| 11 | T…H | `(liền kề)` | thừa cân → carbohydrate |
| 4 | H…T | `(liền kề)` | viêm → corticoid |
| 2 | T…H | `[CONDITION]` | nhồi máu cơ tim → ngăn ngừa |
| 2 | H…T | `và` | thèm đường → carbohydrate |
| 1 | H…T | `[BODY_PART] đôi khi một số loại` | căng → sữa rửa mặt |
| 1 | H…T | `[CONDITION] [CONDITION] và` | lo âu → carbohydrate |
| 1 | T…H | `[CONDITION] cho` | rung nhĩ → phòng ngừa |
| 1 | T…H | `[CONDITION] không` | tái phát → ngăn ngừa |
| 1 | H…T | `[CONDITION] rõ ràng các` | bệnh → vi khuẩn có lợi |
| 1 | T…H | `[CONDITION] thậm chí có thể` | tử vong → mồ hôi |
| 1 | H…T | `[CONDITION] và` | tiểu đường → carbohydrate |
| 1 | H…T | `[CONDITION] và [CONDITION]` | tình trạng loạn nhịp → ngăn ngừa |
| 1 | T…H | `[DRUG] làm [CONDITION] của người` | ung thư → kẽm |

## treated_by_procedure — dương

| Số lần | Thứ tự | Chuỗi giữa | Ví dụ (head → tail) |
|---:|---|---|---|
| 3 | T…H | `<LONG>` | parkinson → phẫu thuật |
| 3 | H…T | `<LONG>` | béo phì → mổ |
| 1 | H…T | `[CONDITION] đó thì phương pháp` | triệu chứng đơ cứng → phẫu thuật kích thích não sâu |
| 1 | T…H | `cũng như [BODY_PART] cho người bệnh` | parkinson → điều trị gen |
| 1 | H…T | `là mình phải` | huyết áp → uống thuốc |
| 1 | H…T | `mà cần phẫu thuốc` | parkinson → kích thích não sâu |
| 1 | T…H | `nó sẽ giúp cải thiện` | triệu chứng → phẫu thuật kích thích não sâu |
| 1 | H…T | `thì đã từng thử các` | béo phì → phương pháp trị liệu |
| 1 | H…T | `và trong đó` | parkinson → điều trị gen |
| 1 | H…T | `đó thì phương pháp` | cứng đờ → phẫu thuật kích thích não sâu |
| 1 | H…T | `đều phải` | rung nhĩ → uống thuốc |

## treated_by_procedure — âm

| Số lần | Thứ tự | Chuỗi giữa | Ví dụ (head → tail) |
|---:|---|---|---|
| 24 | T…H | `<LONG>` | biến chứng → phẫu thuật |
| 11 | H…T | `<LONG>` | ung thư → sinh mổ |
| 3 | T…H | `các` | triệu chứng → cải thiện |
| 2 | H…T | `và` | triệu chứng → cải thiện |
| 1 | T…H | `[DRUG] chống` | covid → tiêm |
| 1 | T…H | `[PROCEDURE] và [DRUG] cái` | ung thư → hóa trị |
| 1 | T…H | `[PROCEDURE] và [DRUG] cái [CONDITION]` | tái phát → hóa trị |
| 1 | H…T | `[TEST]` | xơ vữa động mạch → cải thiện |
| 1 | T…H | `cho việc làm giảm` | cholesterol → hỗ trợ |
| 1 | H…T | `chạp mà` | chậm → cải thiện |
| 1 | H…T | `do` | tác dụng phụ → hóa trị |
| 1 | H…T | `do [PROCEDURE]` | tác dụng phụ → xạ trị |
| 1 | T…H | `giúp [PROCEDURE] các` | triệu chứng → cải thiện |
| 1 | T…H | `giảm` | đau → hỗ trợ |
| 1 | T…H | `giảm [CONDITION] giảm` | viêm xương khớp → hỗ trợ |

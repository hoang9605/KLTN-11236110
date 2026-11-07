# 600 mẫu VietMed-NER — nhãn gốc

Nguồn: https://huggingface.co/datasets/leduckhai/VietMed-NER

Chọn ngẫu nhiên 600 dòng train, seed 20261003. Giữ nguyên text, words, labels, tags; không quy đổi nhãn, không thêm RE. Bảng ghi từng token để giữ nguyên ranh giới BIO. Nhãn 0 cũng được giữ nguyên như nguồn.

## VM600-001 — dòng train 0 (đếm từ 0)

thì cũng giống như ba má mình đã từng bị béo phì rồi bị bệnh này bệnh kia những người thân quen của mình mình biết bị

| Token | Nhãn gốc |
|---|---|
| thì | 0 |
| cũng | 0 |
| giống | 0 |
| như | 0 |
| ba | B-GENDER |
| má | B-GENDER |
| mình | 0 |
| đã | 0 |
| từng | 0 |
| bị | 0 |
| béo | B-DISEASESYMTOM |
| phì | I-DISEASESYMTOM |
| rồi | 0 |
| bị | B-DISEASESYMTOM |
| bệnh | I-DISEASESYMTOM |
| này | 0 |
| bệnh | 0 |
| kia | 0 |
| những | 0 |
| người | 0 |
| thân | 0 |
| quen | 0 |
| của | 0 |
| mình | 0 |
| mình | 0 |
| biết | 0 |
| bị | 0 |

## VM600-002 — dòng train 24 (đếm từ 0)

gọi là những cái bụi mịn từ ngoài môi trường xâm nhập vào trong da và cho chúng ta sẽ xảy ra những cái phản ứng

| Token | Nhãn gốc |
|---|---|
| gọi | 0 |
| là | 0 |
| những | 0 |
| cái | 0 |
| bụi | B-DRUGCHEMICAL |
| mịn | I-DRUGCHEMICAL |
| từ | 0 |
| ngoài | 0 |
| môi | 0 |
| trường | 0 |
| xâm | 0 |
| nhập | 0 |
| vào | 0 |
| trong | 0 |
| da | B-ORGAN |
| và | 0 |
| cho | 0 |
| chúng | 0 |
| ta | 0 |
| sẽ | 0 |
| xảy | 0 |
| ra | 0 |
| những | 0 |
| cái | 0 |
| phản | 0 |
| ứng | 0 |

## VM600-003 — dòng train 33 (đếm từ 0)

tẩy trắng và dưỡng sáng vẫn chưa được phân biệt rõ ràng vào mọi người hay nhầm lẫn hay tưởng là chung với ạ nên là

| Token | Nhãn gốc |
|---|---|
| tẩy | B-PERSONALCARE |
| trắng | I-PERSONALCARE |
| và | 0 |
| dưỡng | B-PERSONALCARE |
| sáng | I-PERSONALCARE |
| vẫn | 0 |
| chưa | 0 |
| được | 0 |
| phân | 0 |
| biệt | 0 |
| rõ | 0 |
| ràng | 0 |
| vào | 0 |
| mọi | 0 |
| người | 0 |
| hay | 0 |
| nhầm | 0 |
| lẫn | 0 |
| hay | 0 |
| tưởng | 0 |
| là | 0 |
| chung | 0 |
| với | 0 |
| ạ | 0 |
| nên | 0 |
| là | 0 |

## VM600-004 — dòng train 38 (đếm từ 0)

thể gặp ngay cái thời gian người ta gọi là tiểu phẫu tức là trong những cái ngày đầu tiên của cuộc mổ nếu mà sau đó mà nó

| Token | Nhãn gốc |
|---|---|
| thể | 0 |
| gặp | 0 |
| ngay | 0 |
| cái | 0 |
| thời | B-DATETIME |
| gian | I-DATETIME |
| người | 0 |
| ta | 0 |
| gọi | 0 |
| là | 0 |
| tiểu | B-SURGERY |
| phẫu | I-SURGERY |
| tức | 0 |
| là | 0 |
| trong | 0 |
| những | 0 |
| cái | 0 |
| ngày | B-DATETIME |
| đầu | I-DATETIME |
| tiên | I-DATETIME |
| của | 0 |
| cuộc | 0 |
| mổ | B-SURGERY |
| nếu | 0 |
| mà | 0 |
| sau | 0 |
| đó | 0 |
| mà | 0 |
| nó | 0 |

## VM600-005 — dòng train 40 (đếm từ 0)

nhịp tim nhanh này các cái rối loạn nhịp tim này đấy là những cái dấu hiệu hoặc là đau tức ngực thế còn nếu mà những cái

| Token | Nhãn gốc |
|---|---|
| nhịp | B-DISEASESYMTOM |
| tim | I-DISEASESYMTOM |
| nhanh | I-DISEASESYMTOM |
| này | 0 |
| các | 0 |
| cái | 0 |
| rối | B-DISEASESYMTOM |
| loạn | I-DISEASESYMTOM |
| nhịp | I-DISEASESYMTOM |
| tim | I-DISEASESYMTOM |
| này | 0 |
| đấy | 0 |
| là | 0 |
| những | 0 |
| cái | 0 |
| dấu | 0 |
| hiệu | 0 |
| hoặc | 0 |
| là | 0 |
| đau | B-DISEASESYMTOM |
| tức | I-DISEASESYMTOM |
| ngực | I-DISEASESYMTOM |
| thế | 0 |
| còn | 0 |
| nếu | 0 |
| mà | 0 |
| những | 0 |
| cái | 0 |

## VM600-006 — dòng train 54 (đếm từ 0)

ta đã từng gặp trong trong lịch sử vì thế nên là cúm a thì là một bệnh lý và

| Token | Nhãn gốc |
|---|---|
| ta | 0 |
| đã | 0 |
| từng | 0 |
| gặp | 0 |
| trong | 0 |
| trong | 0 |
| lịch | 0 |
| sử | 0 |
| vì | 0 |
| thế | 0 |
| nên | 0 |
| là | 0 |
| cúm | B-DISEASESYMTOM |
| a | I-DISEASESYMTOM |
| thì | 0 |
| là | 0 |
| một | 0 |
| bệnh | 0 |
| lý | 0 |
| và | 0 |

## VM600-007 — dòng train 69 (đếm từ 0)

là sau khi mà điều trị ung thư thì rõ ràng được bây giờ chúng ta trở về cuộc

| Token | Nhãn gốc |
|---|---|
| là | 0 |
| sau | 0 |
| khi | 0 |
| mà | 0 |
| điều | B-TREATMENT |
| trị | I-TREATMENT |
| ung | B-DISEASESYMTOM |
| thư | I-DISEASESYMTOM |
| thì | 0 |
| rõ | 0 |
| ràng | 0 |
| được | 0 |
| bây | B-DATETIME |
| giờ | I-DATETIME |
| chúng | 0 |
| ta | 0 |
| trở | 0 |
| về | 0 |
| cuộc | 0 |

## VM600-008 — dòng train 76 (đếm từ 0)

mảng xơ vữa ở trên các bệnh nhân bị tăng huyết áp ạ và từ đó nó giúp cho máu thông lên não lên tim được tốt hơn và

| Token | Nhãn gốc |
|---|---|
| mảng | B-DISEASESYMTOM |
| xơ | I-DISEASESYMTOM |
| vữa | I-DISEASESYMTOM |
| ở | 0 |
| trên | 0 |
| các | 0 |
| bệnh | B-OCCUPATION |
| nhân | I-OCCUPATION |
| bị | 0 |
| tăng | B-DISEASESYMTOM |
| huyết | I-DISEASESYMTOM |
| áp | I-DISEASESYMTOM |
| ạ | 0 |
| và | 0 |
| từ | 0 |
| đó | 0 |
| nó | 0 |
| giúp | 0 |
| cho | 0 |
| máu | B-ORGAN |
| thông | 0 |
| lên | 0 |
| não | B-ORGAN |
| lên | 0 |
| tim | B-ORGAN |
| được | 0 |
| tốt | 0 |
| hơn | 0 |
| và | 0 |

## VM600-009 — dòng train 81 (đếm từ 0)

đối với cái bệnh lý của bác thì bác đang phải dùng rất nhiều những các cái thuốc nền các cái thuốc để điều trị các cái

| Token | Nhãn gốc |
|---|---|
| đối | 0 |
| với | 0 |
| cái | 0 |
| bệnh | 0 |
| lý | 0 |
| của | 0 |
| bác | B-AGE |
| thì | 0 |
| bác | B-AGE |
| đang | 0 |
| phải | 0 |
| dùng | 0 |
| rất | B-UNITCALIBRATOR |
| nhiều | I-UNITCALIBRATOR |
| những | 0 |
| các | 0 |
| cái | 0 |
| thuốc | B-DRUGCHEMICAL |
| nền | 0 |
| các | 0 |
| cái | 0 |
| thuốc | B-DRUGCHEMICAL |
| để | 0 |
| điều | B-TREATMENT |
| trị | I-TREATMENT |
| các | 0 |
| cái | 0 |

## VM600-010 — dòng train 92 (đếm từ 0)

ta càng cảm thấy được vai trò vô cùng quan trọng của chuyên khoa tâm lý trong điều trị người bệnh béo phì và tiếp theo

| Token | Nhãn gốc |
|---|---|
| ta | 0 |
| càng | 0 |
| cảm | 0 |
| thấy | 0 |
| được | 0 |
| vai | 0 |
| trò | 0 |
| vô | 0 |
| cùng | 0 |
| quan | 0 |
| trọng | 0 |
| của | 0 |
| chuyên | B-LOCATION |
| khoa | I-LOCATION |
| tâm | 0 |
| lý | 0 |
| trong | 0 |
| điều | B-TREATMENT |
| trị | I-TREATMENT |
| người | 0 |
| bệnh | 0 |
| béo | B-DISEASESYMTOM |
| phì | I-DISEASESYMTOM |
| và | 0 |
| tiếp | 0 |
| theo | 0 |

## VM600-011 — dòng train 105 (đếm từ 0)

với cơ chế của cái hình thành cục máu đông ở trong tim giờ đó nên thuốc chống tiểu cầu không phải là cái gì

| Token | Nhãn gốc |
|---|---|
| với | 0 |
| cơ | 0 |
| chế | 0 |
| của | 0 |
| cái | 0 |
| hình | 0 |
| thành | 0 |
| cục | B-DISEASESYMTOM |
| máu | I-DISEASESYMTOM |
| đông | I-DISEASESYMTOM |
| ở | 0 |
| trong | 0 |
| tim | B-ORGAN |
| giờ | 0 |
| đó | 0 |
| nên | 0 |
| thuốc | B-DRUGCHEMICAL |
| chống | I-DRUGCHEMICAL |
| tiểu | I-DRUGCHEMICAL |
| cầu | I-DRUGCHEMICAL |
| không | 0 |
| phải | 0 |
| là | 0 |
| cái | 0 |
| gì | 0 |

## VM600-012 — dòng train 121 (đếm từ 0)

cân nặng họ không dám nói về cái vẻ đẹp của một cái người nữ hay người nam là như thế nào vì lý do là họ sẽ dễ bị

| Token | Nhãn gốc |
|---|---|
| cân | 0 |
| nặng | 0 |
| họ | 0 |
| không | 0 |
| dám | 0 |
| nói | 0 |
| về | 0 |
| cái | 0 |
| vẻ | 0 |
| đẹp | 0 |
| của | 0 |
| một | 0 |
| cái | 0 |
| người | B-GENDER |
| nữ | I-GENDER |
| hay | 0 |
| người | 0 |
| nam | B-GENDER |
| là | 0 |
| như | 0 |
| thế | 0 |
| nào | 0 |
| vì | 0 |
| lý | 0 |
| do | 0 |
| là | 0 |
| họ | 0 |
| sẽ | 0 |
| dễ | 0 |
| bị | 0 |

## VM600-013 — dòng train 132 (đếm từ 0)

từ thực vật ví dụ như là các bạn có thể nghe tới như là chiết xuất từ hoa lan được cam thảo này từ bạch quả lá dâu tầm

| Token | Nhãn gốc |
|---|---|
| từ | 0 |
| thực | B-FOODDRINK |
| vật | I-FOODDRINK |
| ví | 0 |
| dụ | 0 |
| như | 0 |
| là | 0 |
| các | 0 |
| bạn | 0 |
| có | 0 |
| thể | 0 |
| nghe | 0 |
| tới | 0 |
| như | 0 |
| là | 0 |
| chiết | B-MEDDEVICETECHNIQUE |
| xuất | I-MEDDEVICETECHNIQUE |
| từ | 0 |
| hoa | B-DRUGCHEMICAL |
| lan | I-DRUGCHEMICAL |
| được | 0 |
| cam | B-DRUGCHEMICAL |
| thảo | I-DRUGCHEMICAL |
| này | 0 |
| từ | 0 |
| bạch | B-DRUGCHEMICAL |
| quả | I-DRUGCHEMICAL |
| lá | B-DRUGCHEMICAL |
| dâu | I-DRUGCHEMICAL |
| tầm | I-DRUGCHEMICAL |

## VM600-014 — dòng train 134 (đếm từ 0)

dựng một cái cái cái mục tiêu trị liệu cũng như một chương trình trị liệu dài hơi để giúp

| Token | Nhãn gốc |
|---|---|
| dựng | 0 |
| một | 0 |
| cái | 0 |
| cái | 0 |
| cái | 0 |
| mục | 0 |
| tiêu | 0 |
| trị | B-TREATMENT |
| liệu | I-TREATMENT |
| cũng | 0 |
| như | 0 |
| một | 0 |
| chương | 0 |
| trình | 0 |
| trị | B-TREATMENT |
| liệu | I-TREATMENT |
| dài | 0 |
| hơi | 0 |
| để | 0 |
| giúp | 0 |

## VM600-015 — dòng train 137 (đếm từ 0)

vận động thì tình trạng béo phì nó tăng lên mà mình béo phì nó tăng lên rồi thì gặp tình trạng kỳ thị nữa hay là gặp

| Token | Nhãn gốc |
|---|---|
| vận | 0 |
| động | 0 |
| thì | 0 |
| tình | 0 |
| trạng | 0 |
| béo | B-DISEASESYMTOM |
| phì | I-DISEASESYMTOM |
| nó | 0 |
| tăng | 0 |
| lên | 0 |
| mà | 0 |
| mình | 0 |
| béo | B-DISEASESYMTOM |
| phì | I-DISEASESYMTOM |
| nó | 0 |
| tăng | 0 |
| lên | 0 |
| rồi | 0 |
| thì | 0 |
| gặp | 0 |
| tình | 0 |
| trạng | 0 |
| kỳ | 0 |
| thị | 0 |
| nữa | 0 |
| hay | 0 |
| là | 0 |
| gặp | 0 |

## VM600-016 — dòng train 149 (đếm từ 0)

khi mà chúng ta khỏe mạnh như thế này mà chúng ta gặp một cái vấn đề gì đấy về mặt tinh thần thì chúng ta cũng đã rất là chán ăn rồi và hiện nay thì có một số

| Token | Nhãn gốc |
|---|---|
| khi | 0 |
| mà | 0 |
| chúng | 0 |
| ta | 0 |
| khỏe | 0 |
| mạnh | 0 |
| như | 0 |
| thế | 0 |
| này | 0 |
| mà | 0 |
| chúng | 0 |
| ta | 0 |
| gặp | 0 |
| một | 0 |
| cái | 0 |
| vấn | 0 |
| đề | 0 |
| gì | 0 |
| đấy | 0 |
| về | 0 |
| mặt | 0 |
| tinh | 0 |
| thần | 0 |
| thì | 0 |
| chúng | 0 |
| ta | 0 |
| cũng | 0 |
| đã | 0 |
| rất | 0 |
| là | 0 |
| chán | B-DISEASESYMTOM |
| ăn | I-DISEASESYMTOM |
| rồi | 0 |
| và | 0 |
| hiện | B-DATETIME |
| nay | I-DATETIME |
| thì | 0 |
| có | 0 |
| một | 0 |
| số | 0 |

## VM600-017 — dòng train 152 (đếm từ 0)

theo cái tình trạng bệnh lý của chúng ta ví dụ đái tháo đường hay là rối loạn lipid máu thì chúng ta phải kiêng những cái gì và ăn

| Token | Nhãn gốc |
|---|---|
| theo | 0 |
| cái | 0 |
| tình | 0 |
| trạng | 0 |
| bệnh | 0 |
| lý | 0 |
| của | 0 |
| chúng | 0 |
| ta | 0 |
| ví | 0 |
| dụ | 0 |
| đái | B-DISEASESYMTOM |
| tháo | I-DISEASESYMTOM |
| đường | I-DISEASESYMTOM |
| hay | 0 |
| là | 0 |
| rối | B-DISEASESYMTOM |
| loạn | I-DISEASESYMTOM |
| lipid | I-DISEASESYMTOM |
| máu | I-DISEASESYMTOM |
| thì | 0 |
| chúng | 0 |
| ta | 0 |
| phải | 0 |
| kiêng | 0 |
| những | 0 |
| cái | 0 |
| gì | 0 |
| và | 0 |
| ăn | 0 |

## VM600-018 — dòng train 153 (đếm từ 0)

con đường để mà làm giảm sản sinh những cái tín hiệu đến tế bào sắc tố ví dụ như lại những cái hoạt chất thoa có chút

| Token | Nhãn gốc |
|---|---|
| con | 0 |
| đường | 0 |
| để | 0 |
| mà | 0 |
| làm | 0 |
| giảm | 0 |
| sản | 0 |
| sinh | 0 |
| những | 0 |
| cái | 0 |
| tín | 0 |
| hiệu | 0 |
| đến | 0 |
| tế | B-ORGAN |
| bào | I-ORGAN |
| sắc | I-ORGAN |
| tố | I-ORGAN |
| ví | 0 |
| dụ | 0 |
| như | 0 |
| lại | 0 |
| những | 0 |
| cái | 0 |
| hoạt | B-DRUGCHEMICAL |
| chất | I-DRUGCHEMICAL |
| thoa | 0 |
| có | 0 |
| chút | 0 |

## VM600-019 — dòng train 161 (đếm từ 0)

ta biết là cái suy giãn tĩnh mạch nó cũng liên quan đến quá trình lão hóa liên quan quá trình thoái hóa các cái mạch

| Token | Nhãn gốc |
|---|---|
| ta | 0 |
| biết | 0 |
| là | 0 |
| cái | 0 |
| suy | B-DISEASESYMTOM |
| giãn | I-DISEASESYMTOM |
| tĩnh | I-DISEASESYMTOM |
| mạch | I-DISEASESYMTOM |
| nó | 0 |
| cũng | 0 |
| liên | 0 |
| quan | 0 |
| đến | 0 |
| quá | B-DIAGNOSTICS |
| trình | I-DIAGNOSTICS |
| lão | I-DIAGNOSTICS |
| hóa | I-DIAGNOSTICS |
| liên | 0 |
| quan | 0 |
| quá | 0 |
| trình | 0 |
| thoái | B-DISEASESYMTOM |
| hóa | I-DISEASESYMTOM |
| các | 0 |
| cái | 0 |
| mạch | B-ORGAN |

## VM600-020 — dòng train 186 (đếm từ 0)

vấn đề sức khỏe khó khăn nhất của chúng ta mặc dù dự án đang nghiên cứu một số bộ phận của cơ thể chứa vi khuẩn bao gồm

| Token | Nhãn gốc |
|---|---|
| vấn | 0 |
| đề | 0 |
| sức | 0 |
| khỏe | 0 |
| khó | 0 |
| khăn | 0 |
| nhất | 0 |
| của | 0 |
| chúng | 0 |
| ta | 0 |
| mặc | 0 |
| dù | 0 |
| dự | 0 |
| án | 0 |
| đang | 0 |
| nghiên | B-DIAGNOSTICS |
| cứu | I-DIAGNOSTICS |
| một | 0 |
| số | 0 |
| bộ | 0 |
| phận | 0 |
| của | 0 |
| cơ | B-ORGAN |
| thể | I-ORGAN |
| chứa | 0 |
| vi | B-DISEASESYMTOM |
| khuẩn | I-DISEASESYMTOM |
| bao | 0 |
| gồm | 0 |

## VM600-021 — dòng train 193 (đếm từ 0)

những người mà có bị béo phì rồi đó thì họ có nhiều

| Token | Nhãn gốc |
|---|---|
| những | 0 |
| người | 0 |
| mà | 0 |
| có | 0 |
| bị | 0 |
| béo | B-DISEASESYMTOM |
| phì | I-DISEASESYMTOM |
| rồi | 0 |
| đó | 0 |
| thì | 0 |
| họ | 0 |
| có | 0 |
| nhiều | 0 |

## VM600-022 — dòng train 227 (đếm từ 0)

nên phổ biến trong nhiều sản phẩm thực phẩm và có thể được tìm thấy trong các cửa hàng tạp hóa thông thường biết cách

| Token | Nhãn gốc |
|---|---|
| nên | 0 |
| phổ | 0 |
| biến | 0 |
| trong | 0 |
| nhiều | 0 |
| sản | 0 |
| phẩm | 0 |
| thực | B-FOODDRINK |
| phẩm | I-FOODDRINK |
| và | 0 |
| có | 0 |
| thể | 0 |
| được | 0 |
| tìm | 0 |
| thấy | 0 |
| trong | 0 |
| các | 0 |
| cửa | 0 |
| hàng | 0 |
| tạp | 0 |
| hóa | 0 |
| thông | 0 |
| thường | 0 |
| biết | 0 |
| cách | 0 |

## VM600-023 — dòng train 230 (đếm từ 0)

quý vị thân mến chúng ta vừa được lắng nghe cuộc trò chuyện với chủ đề dinh

| Token | Nhãn gốc |
|---|---|
| quý | 0 |
| vị | 0 |
| thân | 0 |
| mến | 0 |
| chúng | 0 |
| ta | 0 |
| vừa | 0 |
| được | 0 |
| lắng | 0 |
| nghe | 0 |
| cuộc | 0 |
| trò | 0 |
| chuyện | 0 |
| với | 0 |
| chủ | 0 |
| đề | 0 |
| dinh | 0 |

## VM600-024 — dòng train 234 (đếm từ 0)

sức đề kháng và kéo dài tuổi thọ đó là mong muốn có rất là nhiều người đặc biệt là đối với những khán giả cao tuổi như

| Token | Nhãn gốc |
|---|---|
| sức | B-DIAGNOSTICS |
| đề | I-DIAGNOSTICS |
| kháng | I-DIAGNOSTICS |
| và | 0 |
| kéo | B-PREVENTIVEMED |
| dài | I-PREVENTIVEMED |
| tuổi | I-PREVENTIVEMED |
| thọ | I-PREVENTIVEMED |
| đó | 0 |
| là | 0 |
| mong | 0 |
| muốn | 0 |
| có | 0 |
| rất | 0 |
| là | 0 |
| nhiều | 0 |
| người | 0 |
| đặc | 0 |
| biệt | 0 |
| là | 0 |
| đối | 0 |
| với | 0 |
| những | 0 |
| khán | B-OCCUPATION |
| giả | I-OCCUPATION |
| cao | B-AGE |
| tuổi | I-AGE |
| như | 0 |

## VM600-025 — dòng train 236 (đếm từ 0)

cái căn nguyên cơ chế bệnh sinh của mình đó chính là những cái mảng xơ vữa bác ạ và rất tốt ở trên những người bị rối

| Token | Nhãn gốc |
|---|---|
| cái | 0 |
| căn | 0 |
| nguyên | 0 |
| cơ | 0 |
| chế | 0 |
| bệnh | 0 |
| sinh | 0 |
| của | 0 |
| mình | 0 |
| đó | 0 |
| chính | 0 |
| là | 0 |
| những | 0 |
| cái | 0 |
| mảng | B-DISEASESYMTOM |
| xơ | I-DISEASESYMTOM |
| vữa | I-DISEASESYMTOM |
| bác | B-AGE |
| ạ | 0 |
| và | 0 |
| rất | 0 |
| tốt | 0 |
| ở | 0 |
| trên | 0 |
| những | 0 |
| người | 0 |
| bị | 0 |
| rối | 0 |

## VM600-026 — dòng train 237 (đếm từ 0)

hiểu biết của chúng ta về miễn dịch vấn đề liên quan đến vắcxin và cách chúng hoạt động nguyên tắc cơ bản của việc

| Token | Nhãn gốc |
|---|---|
| hiểu | 0 |
| biết | 0 |
| của | 0 |
| chúng | 0 |
| ta | 0 |
| về | 0 |
| miễn | 0 |
| dịch | 0 |
| vấn | 0 |
| đề | 0 |
| liên | 0 |
| quan | 0 |
| đến | 0 |
| vắcxin | B-DRUGCHEMICAL |
| và | 0 |
| cách | 0 |
| chúng | 0 |
| hoạt | 0 |
| động | 0 |
| nguyên | 0 |
| tắc | 0 |
| cơ | 0 |
| bản | 0 |
| của | 0 |
| việc | 0 |

## VM600-027 — dòng train 243 (đếm từ 0)

coi một cái người ung thư trong thành viên trong gia đình là một sự sầu não trong cả một gia đình thì rất khó có thể

| Token | Nhãn gốc |
|---|---|
| coi | 0 |
| một | 0 |
| cái | 0 |
| người | 0 |
| ung | B-DISEASESYMTOM |
| thư | I-DISEASESYMTOM |
| trong | 0 |
| thành | 0 |
| viên | 0 |
| trong | 0 |
| gia | 0 |
| đình | 0 |
| là | 0 |
| một | 0 |
| sự | 0 |
| sầu | 0 |
| não | B-ORGAN |
| trong | 0 |
| cả | 0 |
| một | 0 |
| gia | 0 |
| đình | 0 |
| thì | 0 |
| rất | 0 |
| khó | 0 |
| có | 0 |
| thể | 0 |

## VM600-028 — dòng train 254 (đếm từ 0)

gáy nó mới đau nó chèn lên thần kinh tê liệt tay thế uống thuốc nó đỡ làm nhiều lúc mà rét

| Token | Nhãn gốc |
|---|---|
| gáy | B-ORGAN |
| nó | 0 |
| mới | 0 |
| đau | B-DISEASESYMTOM |
| nó | 0 |
| chèn | 0 |
| lên | 0 |
| thần | B-ORGAN |
| kinh | I-ORGAN |
| tê | B-DISEASESYMTOM |
| liệt | I-DISEASESYMTOM |
| tay | I-DISEASESYMTOM |
| thế | 0 |
| uống | B-TREATMENT |
| thuốc | I-TREATMENT |
| nó | 0 |
| đỡ | 0 |
| làm | 0 |
| nhiều | 0 |
| lúc | 0 |
| mà | 0 |
| rét | 0 |

## VM600-029 — dòng train 259 (đếm từ 0)

thì nhiều chi bộ có thể chia sẻ chúng ta trước không ạ cúm a thì nó là một bệnh

| Token | Nhãn gốc |
|---|---|
| thì | 0 |
| nhiều | 0 |
| chi | 0 |
| bộ | 0 |
| có | 0 |
| thể | 0 |
| chia | 0 |
| sẻ | 0 |
| chúng | 0 |
| ta | 0 |
| trước | 0 |
| không | 0 |
| ạ | 0 |
| cúm | B-DISEASESYMTOM |
| a | I-DISEASESYMTOM |
| thì | 0 |
| nó | 0 |
| là | 0 |
| một | 0 |
| bệnh | 0 |

## VM600-030 — dòng train 282 (đếm từ 0)

nó gây ra thiếu máu não nếu nó không lại được ngay đây là tự cơ thể có cái

| Token | Nhãn gốc |
|---|---|
| nó | 0 |
| gây | 0 |
| ra | 0 |
| thiếu | B-DISEASESYMTOM |
| máu | I-DISEASESYMTOM |
| não | I-DISEASESYMTOM |
| nếu | 0 |
| nó | 0 |
| không | 0 |
| lại | 0 |
| được | 0 |
| ngay | 0 |
| đây | 0 |
| là | 0 |
| tự | 0 |
| cơ | B-ORGAN |
| thể | I-ORGAN |
| có | 0 |
| cái | 0 |

## VM600-031 — dòng train 286 (đếm từ 0)

những cái lo lắng từ phía người dân và tự người dân cảm thấy rằng cần phải đi xét nghiệm sarscov2 làm cho cái mật

| Token | Nhãn gốc |
|---|---|
| những | 0 |
| cái | 0 |
| lo | 0 |
| lắng | 0 |
| từ | 0 |
| phía | 0 |
| người | B-OCCUPATION |
| dân | I-OCCUPATION |
| và | 0 |
| tự | 0 |
| người | B-OCCUPATION |
| dân | I-OCCUPATION |
| cảm | 0 |
| thấy | 0 |
| rằng | 0 |
| cần | 0 |
| phải | 0 |
| đi | 0 |
| xét | B-DIAGNOSTICS |
| nghiệm | I-DIAGNOSTICS |
| sarscov2 | B-DISEASESYMTOM |
| làm | 0 |
| cho | 0 |
| cái | 0 |
| mật | B-ORGAN |

## VM600-032 — dòng train 293 (đếm từ 0)

nên có thể nói rằng là từ xa xưa đông trùng hạ thảo đó là một thứ mà để đặc hữu cho những cái bậc quyền quý nhưng ngày

| Token | Nhãn gốc |
|---|---|
| nên | 0 |
| có | 0 |
| thể | 0 |
| nói | 0 |
| rằng | 0 |
| là | 0 |
| từ | 0 |
| xa | B-DATETIME |
| xưa | I-DATETIME |
| đông | B-DRUGCHEMICAL |
| trùng | I-DRUGCHEMICAL |
| hạ | I-DRUGCHEMICAL |
| thảo | I-DRUGCHEMICAL |
| đó | 0 |
| là | 0 |
| một | 0 |
| thứ | 0 |
| mà | 0 |
| để | 0 |
| đặc | 0 |
| hữu | 0 |
| cho | 0 |
| những | 0 |
| cái | 0 |
| bậc | 0 |
| quyền | 0 |
| quý | 0 |
| nhưng | 0 |
| ngày | 0 |

## VM600-033 — dòng train 295 (đếm từ 0)

giờ thì chúng ta sẽ dành ít phút để nghe tâm sự của người trong cuộc như thế nào nhé cũng gần một nửa năm trở lại đây thì

| Token | Nhãn gốc |
|---|---|
| giờ | 0 |
| thì | 0 |
| chúng | 0 |
| ta | 0 |
| sẽ | 0 |
| dành | 0 |
| ít | B-DATETIME |
| phút | I-DATETIME |
| để | 0 |
| nghe | 0 |
| tâm | 0 |
| sự | 0 |
| của | 0 |
| người | 0 |
| trong | 0 |
| cuộc | 0 |
| như | 0 |
| thế | 0 |
| nào | 0 |
| nhé | 0 |
| cũng | 0 |
| gần | 0 |
| một | 0 |
| nửa | 0 |
| năm | 0 |
| trở | 0 |
| lại | 0 |
| đây | 0 |
| thì | 0 |

## VM600-034 — dòng train 308 (đếm từ 0)

mặn quá hoặc là đắng quá hoặc là cảm thấy chua quá không thể mà ăn được không thể chấp nhận được món ăn đi qua

| Token | Nhãn gốc |
|---|---|
| mặn | 0 |
| quá | 0 |
| hoặc | 0 |
| là | 0 |
| đắng | 0 |
| quá | 0 |
| hoặc | 0 |
| là | 0 |
| cảm | 0 |
| thấy | 0 |
| chua | 0 |
| quá | 0 |
| không | 0 |
| thể | 0 |
| mà | 0 |
| ăn | 0 |
| được | 0 |
| không | 0 |
| thể | 0 |
| chấp | 0 |
| nhận | 0 |
| được | 0 |
| món | 0 |
| ăn | 0 |
| đi | 0 |
| qua | 0 |

## VM600-035 — dòng train 314 (đếm từ 0)

pháp điều trị thuốc thì phẫu thuật kích thích não sâu nó sẽ giúp cải thiện triệu chứng cho người bệnh khá là tốt mà khi

| Token | Nhãn gốc |
|---|---|
| pháp | 0 |
| điều | B-TREATMENT |
| trị | I-TREATMENT |
| thuốc | B-DRUGCHEMICAL |
| thì | 0 |
| phẫu | B-SURGERY |
| thuật | I-SURGERY |
| kích | I-SURGERY |
| thích | I-SURGERY |
| não | I-SURGERY |
| sâu | I-SURGERY |
| nó | 0 |
| sẽ | 0 |
| giúp | 0 |
| cải | B-TREATMENT |
| thiện | I-TREATMENT |
| triệu | B-DISEASESYMTOM |
| chứng | I-DISEASESYMTOM |
| cho | 0 |
| người | 0 |
| bệnh | 0 |
| khá | 0 |
| là | 0 |
| tốt | 0 |
| mà | 0 |
| khi | 0 |

## VM600-036 — dòng train 317 (đếm từ 0)

và cái vấn đề cuối cùng là thuốc mà người bệnh người bệnh vẫn nên uống thuốc

| Token | Nhãn gốc |
|---|---|
| và | 0 |
| cái | 0 |
| vấn | 0 |
| đề | 0 |
| cuối | 0 |
| cùng | 0 |
| là | 0 |
| thuốc | B-DRUGCHEMICAL |
| mà | 0 |
| người | 0 |
| bệnh | 0 |
| người | 0 |
| bệnh | 0 |
| vẫn | 0 |
| nên | 0 |
| uống | B-TREATMENT |
| thuốc | I-TREATMENT |

## VM600-037 — dòng train 320 (đếm từ 0)

động của máy kích thích não sâu của mình cũng có thể thay đổi một vài thông số liên quan tới hoạt động kích thích não

| Token | Nhãn gốc |
|---|---|
| động | 0 |
| của | 0 |
| máy | B-MEDDEVICETECHNIQUE |
| kích | I-MEDDEVICETECHNIQUE |
| thích | I-MEDDEVICETECHNIQUE |
| não | I-MEDDEVICETECHNIQUE |
| sâu | I-MEDDEVICETECHNIQUE |
| của | 0 |
| mình | 0 |
| cũng | 0 |
| có | 0 |
| thể | 0 |
| thay | 0 |
| đổi | 0 |
| một | B-UNITCALIBRATOR |
| vài | I-UNITCALIBRATOR |
| thông | I-UNITCALIBRATOR |
| số | I-UNITCALIBRATOR |
| liên | 0 |
| quan | 0 |
| tới | 0 |
| hoạt | 0 |
| động | 0 |
| kích | 0 |
| thích | 0 |
| não | B-ORGAN |

## VM600-038 — dòng train 326 (đếm từ 0)

vẫn theo cái quy trình mà bác chỉ cho em là trước khi nhuộm là vẫn làm nhận gội

| Token | Nhãn gốc |
|---|---|
| vẫn | 0 |
| theo | 0 |
| cái | 0 |
| quy | 0 |
| trình | 0 |
| mà | 0 |
| bác | B-AGE |
| chỉ | 0 |
| cho | 0 |
| em | 0 |
| là | 0 |
| trước | 0 |
| khi | 0 |
| nhuộm | 0 |
| là | 0 |
| vẫn | 0 |
| làm | 0 |
| nhận | 0 |
| gội | 0 |

## VM600-039 — dòng train 337 (đếm từ 0)

dại trong cơ thể mà nó cắn nó cắn

| Token | Nhãn gốc |
|---|---|
| dại | 0 |
| trong | 0 |
| cơ | B-ORGAN |
| thể | I-ORGAN |
| mà | 0 |
| nó | 0 |
| cắn | 0 |
| nó | 0 |
| cắn | 0 |

## VM600-040 — dòng train 343 (đếm từ 0)

làm giảm cái nguy cơ các cái mảng xơ vữa động mạch mà cái mảng xơ vữa động mạch của chị nó đang có và từ đó nó giúp cho

| Token | Nhãn gốc |
|---|---|
| làm | 0 |
| giảm | 0 |
| cái | 0 |
| nguy | 0 |
| cơ | 0 |
| các | 0 |
| cái | 0 |
| mảng | B-DISEASESYMTOM |
| xơ | I-DISEASESYMTOM |
| vữa | I-DISEASESYMTOM |
| động | I-DISEASESYMTOM |
| mạch | I-DISEASESYMTOM |
| mà | 0 |
| cái | 0 |
| mảng | B-DISEASESYMTOM |
| xơ | I-DISEASESYMTOM |
| vữa | I-DISEASESYMTOM |
| động | I-DISEASESYMTOM |
| mạch | I-DISEASESYMTOM |
| của | 0 |
| chị | B-GENDER |
| nó | 0 |
| đang | 0 |
| có | 0 |
| và | 0 |
| từ | 0 |
| đó | 0 |
| nó | 0 |
| giúp | 0 |
| cho | 0 |

## VM600-041 — dòng train 346 (đếm từ 0)

là nó có cái tác dụng là ức chế cái việc hình thành và các cái cục máu đông do đó

| Token | Nhãn gốc |
|---|---|
| là | 0 |
| nó | 0 |
| có | 0 |
| cái | 0 |
| tác | 0 |
| dụng | 0 |
| là | 0 |
| ức | B-PREVENTIVEMED |
| chế | I-PREVENTIVEMED |
| cái | 0 |
| việc | 0 |
| hình | 0 |
| thành | 0 |
| và | 0 |
| các | 0 |
| cái | 0 |
| cục | B-DISEASESYMTOM |
| máu | I-DISEASESYMTOM |
| đông | I-DISEASESYMTOM |
| do | 0 |
| đó | 0 |

## VM600-042 — dòng train 360 (đếm từ 0)

chống mệt mỏi và thanh trừng gốc tự do và kéo dài tuổi thọ cho

| Token | Nhãn gốc |
|---|---|
| chống | 0 |
| mệt | B-DISEASESYMTOM |
| mỏi | I-DISEASESYMTOM |
| và | 0 |
| thanh | 0 |
| trừng | 0 |
| gốc | 0 |
| tự | 0 |
| do | 0 |
| và | 0 |
| kéo | B-PREVENTIVEMED |
| dài | I-PREVENTIVEMED |
| tuổi | I-PREVENTIVEMED |
| thọ | I-PREVENTIVEMED |
| cho | 0 |

## VM600-043 — dòng train 375 (đếm từ 0)

ăn uống dinh dưỡng đầy đủ thì tôi nghĩ rằng là cái khả năng lây lan từ những

| Token | Nhãn gốc |
|---|---|
| ăn | B-PERSONALCARE |
| uống | I-PERSONALCARE |
| dinh | B-PERSONALCARE |
| dưỡng | I-PERSONALCARE |
| đầy | I-PERSONALCARE |
| đủ | I-PERSONALCARE |
| thì | 0 |
| tôi | 0 |
| nghĩ | 0 |
| rằng | 0 |
| là | 0 |
| cái | 0 |
| khả | 0 |
| năng | 0 |
| lây | B-DISEASESYMTOM |
| lan | I-DISEASESYMTOM |
| từ | 0 |
| những | 0 |

## VM600-044 — dòng train 380 (đếm từ 0)

trong chương tiếp theo nhưng bây giờ hãy hiểu rằng tất cả các loại bệnh đều bắt

| Token | Nhãn gốc |
|---|---|
| trong | 0 |
| chương | 0 |
| tiếp | 0 |
| theo | 0 |
| nhưng | 0 |
| bây | B-DATETIME |
| giờ | I-DATETIME |
| hãy | 0 |
| hiểu | 0 |
| rằng | 0 |
| tất | 0 |
| cả | 0 |
| các | 0 |
| loại | 0 |
| bệnh | 0 |
| đều | 0 |
| bắt | 0 |

## VM600-045 — dòng train 383 (đếm từ 0)

quá trình viêm và dẫn đến những tình trạng xơ vữa mạch hay là tình trạng là cái thành mạch của chúng ta nó bị xơ

| Token | Nhãn gốc |
|---|---|
| quá | 0 |
| trình | 0 |
| viêm | B-DISEASESYMTOM |
| và | 0 |
| dẫn | 0 |
| đến | 0 |
| những | 0 |
| tình | B-DISEASESYMTOM |
| trạng | I-DISEASESYMTOM |
| xơ | I-DISEASESYMTOM |
| vữa | I-DISEASESYMTOM |
| mạch | I-DISEASESYMTOM |
| hay | 0 |
| là | 0 |
| tình | 0 |
| trạng | 0 |
| là | 0 |
| cái | 0 |
| thành | 0 |
| mạch | B-ORGAN |
| của | 0 |
| chúng | 0 |
| ta | 0 |
| nó | 0 |
| bị | 0 |
| xơ | 0 |

## VM600-046 — dòng train 395 (đếm từ 0)

thì đương nhiên là cái người lớn tuổi thì có nguy cơ bệnh đều cao và đối với rung nhĩ thì là có rung nhĩ cộng với

| Token | Nhãn gốc |
|---|---|
| thì | 0 |
| đương | 0 |
| nhiên | 0 |
| là | 0 |
| cái | 0 |
| người | B-AGE |
| lớn | I-AGE |
| tuổi | I-AGE |
| thì | 0 |
| có | 0 |
| nguy | 0 |
| cơ | 0 |
| bệnh | 0 |
| đều | 0 |
| cao | B-UNITCALIBRATOR |
| và | 0 |
| đối | 0 |
| với | 0 |
| rung | B-DISEASESYMTOM |
| nhĩ | I-DISEASESYMTOM |
| thì | 0 |
| là | 0 |
| có | 0 |
| rung | B-DISEASESYMTOM |
| nhĩ | I-DISEASESYMTOM |
| cộng | 0 |
| với | 0 |

## VM600-047 — dòng train 396 (đếm từ 0)

người ta thích ăn đi thì có khi là nó sẽ ảnh hưởng lại tốt hơn làm cho cái cân nặng nó có thể giảm hơn là thì cái đó là

| Token | Nhãn gốc |
|---|---|
| người | 0 |
| ta | 0 |
| thích | 0 |
| ăn | 0 |
| đi | 0 |
| thì | 0 |
| có | 0 |
| khi | 0 |
| là | 0 |
| nó | 0 |
| sẽ | 0 |
| ảnh | 0 |
| hưởng | 0 |
| lại | 0 |
| tốt | 0 |
| hơn | 0 |
| làm | 0 |
| cho | 0 |
| cái | 0 |
| cân | 0 |
| nặng | 0 |
| nó | 0 |
| có | 0 |
| thể | 0 |
| giảm | 0 |
| hơn | 0 |
| là | 0 |
| thì | 0 |
| cái | 0 |
| đó | 0 |
| là | 0 |

## VM600-048 — dòng train 405 (đếm từ 0)

hỗ trợ trong việc tăng cường sức khỏe của tim mạch và đan sâm nó cũng có cái tác dụng là ức chế làm giảm cái sự hình

| Token | Nhãn gốc |
|---|---|
| hỗ | B-MEDDEVICETECHNIQUE |
| trợ | I-MEDDEVICETECHNIQUE |
| trong | 0 |
| việc | 0 |
| tăng | 0 |
| cường | 0 |
| sức | 0 |
| khỏe | 0 |
| của | 0 |
| tim | B-ORGAN |
| mạch | I-ORGAN |
| và | 0 |
| đan | B-DRUGCHEMICAL |
| sâm | I-DRUGCHEMICAL |
| nó | 0 |
| cũng | 0 |
| có | 0 |
| cái | 0 |
| tác | 0 |
| dụng | 0 |
| là | 0 |
| ức | B-PREVENTIVEMED |
| chế | I-PREVENTIVEMED |
| làm | 0 |
| giảm | 0 |
| cái | 0 |
| sự | 0 |
| hình | 0 |

## VM600-049 — dòng train 406 (đếm từ 0)

cái phác đồ một cách điều trị một cách phù hợp tránh cái tình trạng là mình lại tiếp tục loay hoay như thế này và đôi

| Token | Nhãn gốc |
|---|---|
| cái | 0 |
| phác | B-MEDDEVICETECHNIQUE |
| đồ | I-MEDDEVICETECHNIQUE |
| một | 0 |
| cách | 0 |
| điều | B-TREATMENT |
| trị | I-TREATMENT |
| một | 0 |
| cách | 0 |
| phù | 0 |
| hợp | 0 |
| tránh | 0 |
| cái | 0 |
| tình | 0 |
| trạng | 0 |
| là | 0 |
| mình | 0 |
| lại | 0 |
| tiếp | 0 |
| tục | 0 |
| loay | 0 |
| hoay | 0 |
| như | 0 |
| thế | 0 |
| này | 0 |
| và | 0 |
| đôi | 0 |

## VM600-050 — dòng train 413 (đếm từ 0)

uống thuốc vào có thể hôm nay nó hấp thu tốt mai nó sẽ tăng lên ngày mai mình ăn uống

| Token | Nhãn gốc |
|---|---|
| uống | B-TREATMENT |
| thuốc | I-TREATMENT |
| vào | 0 |
| có | 0 |
| thể | 0 |
| hôm | B-DATETIME |
| nay | I-DATETIME |
| nó | 0 |
| hấp | B-DIAGNOSTICS |
| thu | I-DIAGNOSTICS |
| tốt | 0 |
| mai | 0 |
| nó | 0 |
| sẽ | 0 |
| tăng | 0 |
| lên | 0 |
| ngày | B-DATETIME |
| mai | I-DATETIME |
| mình | 0 |
| ăn | B-PERSONALCARE |
| uống | I-PERSONALCARE |

## VM600-051 — dòng train 416 (đếm từ 0)

mặt xong làm cho chúng ta cảm thấy nó khô căng là những cái sữa rửa mặt nó thường có chứa những thành phần các chất

| Token | Nhãn gốc |
|---|---|
| mặt | 0 |
| xong | 0 |
| làm | 0 |
| cho | 0 |
| chúng | 0 |
| ta | 0 |
| cảm | 0 |
| thấy | 0 |
| nó | 0 |
| khô | B-DISEASESYMTOM |
| căng | I-DISEASESYMTOM |
| là | 0 |
| những | 0 |
| cái | 0 |
| sữa | B-DRUGCHEMICAL |
| rửa | I-DRUGCHEMICAL |
| mặt | I-DRUGCHEMICAL |
| nó | 0 |
| thường | 0 |
| có | 0 |
| chứa | 0 |
| những | 0 |
| thành | 0 |
| phần | 0 |
| các | 0 |
| chất | 0 |

## VM600-052 — dòng train 420 (đếm từ 0)

dùng cảm thấy triệu chứng đau nhức xương khớp giảm nhanh sau từ một đến hai tuần sử dụng tình trạng đau lưng đau vai gáy đau

| Token | Nhãn gốc |
|---|---|
| dùng | 0 |
| cảm | 0 |
| thấy | 0 |
| triệu | B-DISEASESYMTOM |
| chứng | I-DISEASESYMTOM |
| đau | B-DISEASESYMTOM |
| nhức | I-DISEASESYMTOM |
| xương | B-ORGAN |
| khớp | I-ORGAN |
| giảm | 0 |
| nhanh | 0 |
| sau | 0 |
| từ | 0 |
| một | 0 |
| đến | 0 |
| hai | B-DATETIME |
| tuần | I-DATETIME |
| sử | 0 |
| dụng | 0 |
| tình | 0 |
| trạng | 0 |
| đau | B-DISEASESYMTOM |
| lưng | I-DISEASESYMTOM |
| đau | B-DISEASESYMTOM |
| vai | B-ORGAN |
| gáy | B-ORGAN |
| đau | B-DISEASESYMTOM |

## VM600-053 — dòng train 426 (đếm từ 0)

có thể không thích thì chúng ta có thể hoặc có thể thay đổi bữa thì chúng ta có thể sử dụng các cái bữa ăn cao năng

| Token | Nhãn gốc |
|---|---|
| có | 0 |
| thể | 0 |
| không | 0 |
| thích | 0 |
| thì | 0 |
| chúng | 0 |
| ta | 0 |
| có | 0 |
| thể | 0 |
| hoặc | 0 |
| có | 0 |
| thể | 0 |
| thay | 0 |
| đổi | 0 |
| bữa | 0 |
| thì | 0 |
| chúng | 0 |
| ta | 0 |
| có | 0 |
| thể | 0 |
| sử | 0 |
| dụng | 0 |
| các | 0 |
| cái | 0 |
| bữa | 0 |
| ăn | 0 |
| cao | B-UNITCALIBRATOR |
| năng | 0 |

## VM600-054 — dòng train 435 (đếm từ 0)

chỉ có còn hỏi gì thêm không à vâng ạ từ đầu chương trình tới giờ thì tôi thấy là rất là nhiều các khán giả đều có chung

| Token | Nhãn gốc |
|---|---|
| chỉ | 0 |
| có | 0 |
| còn | 0 |
| hỏi | 0 |
| gì | 0 |
| thêm | 0 |
| không | 0 |
| à | 0 |
| vâng | 0 |
| ạ | 0 |
| từ | 0 |
| đầu | 0 |
| chương | 0 |
| trình | 0 |
| tới | 0 |
| giờ | 0 |
| thì | 0 |
| tôi | 0 |
| thấy | 0 |
| là | 0 |
| rất | 0 |
| là | 0 |
| nhiều | 0 |
| các | 0 |
| khán | B-OCCUPATION |
| giả | I-OCCUPATION |
| đều | 0 |
| có | 0 |
| chung | 0 |

## VM600-055 — dòng train 446 (đếm từ 0)

càng ngày họ lo lo nhiều thậm chí họ có thể đưa đến cái trầm cảm mà khi họ

| Token | Nhãn gốc |
|---|---|
| càng | 0 |
| ngày | 0 |
| họ | 0 |
| lo | 0 |
| lo | 0 |
| nhiều | 0 |
| thậm | 0 |
| chí | 0 |
| họ | 0 |
| có | 0 |
| thể | 0 |
| đưa | 0 |
| đến | 0 |
| cái | 0 |
| trầm | B-DISEASESYMTOM |
| cảm | I-DISEASESYMTOM |
| mà | 0 |
| khi | 0 |
| họ | 0 |

## VM600-056 — dòng train 449 (đếm từ 0)

quan trọng đối với sự phát triển của một hệ vi sinh khỏe mạnh cũng như những yếu tố có thể phá hủy nó bạn sẽ sớm bắt đầu

| Token | Nhãn gốc |
|---|---|
| quan | 0 |
| trọng | 0 |
| đối | 0 |
| với | 0 |
| sự | 0 |
| phát | 0 |
| triển | 0 |
| của | 0 |
| một | 0 |
| hệ | B-ORGAN |
| vi | I-ORGAN |
| sinh | I-ORGAN |
| khỏe | 0 |
| mạnh | 0 |
| cũng | 0 |
| như | 0 |
| những | 0 |
| yếu | 0 |
| tố | 0 |
| có | 0 |
| thể | 0 |
| phá | 0 |
| hủy | 0 |
| nó | 0 |
| bạn | 0 |
| sẽ | 0 |
| sớm | 0 |
| bắt | 0 |
| đầu | 0 |

## VM600-057 — dòng train 464 (đếm từ 0)

quá thì khả năng phẫu thuật nó sẽ khó khăn nó có sẽ có nhiều biến chứng cái thứ hai người bệnh parkinson nên là hơn

| Token | Nhãn gốc |
|---|---|
| quá | 0 |
| thì | 0 |
| khả | 0 |
| năng | 0 |
| phẫu | B-SURGERY |
| thuật | I-SURGERY |
| nó | 0 |
| sẽ | 0 |
| khó | 0 |
| khăn | 0 |
| nó | 0 |
| có | 0 |
| sẽ | 0 |
| có | 0 |
| nhiều | 0 |
| biến | B-DISEASESYMTOM |
| chứng | I-DISEASESYMTOM |
| cái | B-UNITCALIBRATOR |
| thứ | I-UNITCALIBRATOR |
| hai | I-UNITCALIBRATOR |
| người | 0 |
| bệnh | 0 |
| parkinson | B-DISEASESYMTOM |
| nên | 0 |
| là | 0 |
| hơn | 0 |

## VM600-058 — dòng train 466 (đếm từ 0)

gánh hết đó là cảm thấy buồn mà tuyệt vọng nữa hàng triệu việt nam đang phải

| Token | Nhãn gốc |
|---|---|
| gánh | 0 |
| hết | 0 |
| đó | 0 |
| là | 0 |
| cảm | 0 |
| thấy | 0 |
| buồn | 0 |
| mà | 0 |
| tuyệt | 0 |
| vọng | 0 |
| nữa | 0 |
| hàng | 0 |
| triệu | 0 |
| việt | B-LOCATION |
| nam | I-LOCATION |
| đang | 0 |
| phải | 0 |

## VM600-059 — dòng train 468 (đếm từ 0)

cho tất cả quý vị khán giả biết thêm về lợi ích mà người bệnh nhận được khi thực hiện giảm cân một cách hiệu quả và an

| Token | Nhãn gốc |
|---|---|
| cho | 0 |
| tất | 0 |
| cả | 0 |
| quý | 0 |
| vị | 0 |
| khán | B-OCCUPATION |
| giả | I-OCCUPATION |
| biết | 0 |
| thêm | 0 |
| về | 0 |
| lợi | 0 |
| ích | 0 |
| mà | 0 |
| người | 0 |
| bệnh | 0 |
| nhận | 0 |
| được | 0 |
| khi | 0 |
| thực | 0 |
| hiện | 0 |
| giảm | B-PERSONALCARE |
| cân | I-PERSONALCARE |
| một | 0 |
| cách | 0 |
| hiệu | 0 |
| quả | 0 |
| và | 0 |
| an | 0 |

## VM600-060 — dòng train 496 (đếm từ 0)

tùm lum tà la hết cái mà khó điều trị và lúc đó thì có tốt thì với khi mà chúng ta có một cái chế độ ăn

| Token | Nhãn gốc |
|---|---|
| tùm | 0 |
| lum | 0 |
| tà | 0 |
| la | 0 |
| hết | 0 |
| cái | 0 |
| mà | 0 |
| khó | 0 |
| điều | B-TREATMENT |
| trị | I-TREATMENT |
| và | 0 |
| lúc | 0 |
| đó | 0 |
| thì | 0 |
| có | 0 |
| tốt | 0 |
| thì | 0 |
| với | 0 |
| khi | 0 |
| mà | 0 |
| chúng | 0 |
| ta | 0 |
| có | 0 |
| một | 0 |
| cái | 0 |
| chế | B-PERSONALCARE |
| độ | I-PERSONALCARE |
| ăn | I-PERSONALCARE |

## VM600-061 — dòng train 504 (đếm từ 0)

người bệnh để có cái cái cái cái sự hiểu biết hơn trong các nhận thức thay đổi cho nó tốt hơn để có thể cải thiện chất

| Token | Nhãn gốc |
|---|---|
| người | 0 |
| bệnh | 0 |
| để | 0 |
| có | 0 |
| cái | 0 |
| cái | 0 |
| cái | 0 |
| cái | 0 |
| sự | 0 |
| hiểu | 0 |
| biết | 0 |
| hơn | 0 |
| trong | 0 |
| các | 0 |
| nhận | 0 |
| thức | 0 |
| thay | 0 |
| đổi | 0 |
| cho | 0 |
| nó | 0 |
| tốt | 0 |
| hơn | 0 |
| để | 0 |
| có | 0 |
| thể | 0 |
| cải | B-TREATMENT |
| thiện | I-TREATMENT |
| chất | 0 |

## VM600-062 — dòng train 514 (đếm từ 0)

dụng và nó phối hợp với nhau là mang lại hiệu quả rất là tốt chị nhé thì chị nên

| Token | Nhãn gốc |
|---|---|
| dụng | 0 |
| và | 0 |
| nó | 0 |
| phối | 0 |
| hợp | 0 |
| với | 0 |
| nhau | 0 |
| là | 0 |
| mang | 0 |
| lại | 0 |
| hiệu | 0 |
| quả | 0 |
| rất | 0 |
| là | 0 |
| tốt | 0 |
| chị | B-GENDER |
| nhé | 0 |
| thì | 0 |
| chị | B-GENDER |
| nên | 0 |

## VM600-063 — dòng train 524 (đếm từ 0)

những cái hậu quả những cái di chứng của bệnh lý này bởi vậy bên cạnh cái việc mà

| Token | Nhãn gốc |
|---|---|
| những | 0 |
| cái | 0 |
| hậu | 0 |
| quả | 0 |
| những | 0 |
| cái | 0 |
| di | B-DISEASESYMTOM |
| chứng | I-DISEASESYMTOM |
| của | 0 |
| bệnh | 0 |
| lý | 0 |
| này | 0 |
| bởi | 0 |
| vậy | 0 |
| bên | 0 |
| cạnh | 0 |
| cái | 0 |
| việc | 0 |
| mà | 0 |

## VM600-064 — dòng train 535 (đếm từ 0)

với sự căng thẳng qua các tác động của hệ vi khuẩn lên hệ nội tiết hormone hỗ

| Token | Nhãn gốc |
|---|---|
| với | 0 |
| sự | 0 |
| căng | B-DISEASESYMTOM |
| thẳng | I-DISEASESYMTOM |
| qua | 0 |
| các | 0 |
| tác | 0 |
| động | 0 |
| của | 0 |
| hệ | 0 |
| vi | B-DISEASESYMTOM |
| khuẩn | I-DISEASESYMTOM |
| lên | 0 |
| hệ | 0 |
| nội | B-ORGAN |
| tiết | I-ORGAN |
| hormone | B-DRUGCHEMICAL |
| hỗ | 0 |

## VM600-065 — dòng train 537 (đếm từ 0)

dứt da của mình nó căng da đôi khi một số loại sữa rửa mặt nó khiến cho mình cảm giác là khi mình rửa xong cái da

| Token | Nhãn gốc |
|---|---|
| dứt | 0 |
| da | B-ORGAN |
| của | 0 |
| mình | 0 |
| nó | 0 |
| căng | 0 |
| da | B-ORGAN |
| đôi | 0 |
| khi | 0 |
| một | 0 |
| số | 0 |
| loại | 0 |
| sữa | B-DRUGCHEMICAL |
| rửa | I-DRUGCHEMICAL |
| mặt | I-DRUGCHEMICAL |
| nó | 0 |
| khiến | 0 |
| cho | 0 |
| mình | 0 |
| cảm | 0 |
| giác | 0 |
| là | 0 |
| khi | 0 |
| mình | 0 |
| rửa | 0 |
| xong | 0 |
| cái | 0 |
| da | B-ORGAN |

## VM600-066 — dòng train 544 (đếm từ 0)

tế bào và cái tổn thương tế bào ấy thì làm cho tế bào không bình thường tế bào không bình thường đấy thì nó một là nếu

| Token | Nhãn gốc |
|---|---|
| tế | B-ORGAN |
| bào | I-ORGAN |
| và | 0 |
| cái | 0 |
| tổn | B-DISEASESYMTOM |
| thương | I-DISEASESYMTOM |
| tế | B-ORGAN |
| bào | I-ORGAN |
| ấy | 0 |
| thì | 0 |
| làm | 0 |
| cho | 0 |
| tế | B-ORGAN |
| bào | I-ORGAN |
| không | 0 |
| bình | 0 |
| thường | 0 |
| tế | B-ORGAN |
| bào | I-ORGAN |
| không | 0 |
| bình | 0 |
| thường | 0 |
| đấy | 0 |
| thì | 0 |
| nó | 0 |
| một | 0 |
| là | 0 |
| nếu | 0 |

## VM600-067 — dòng train 552 (đếm từ 0)

nhau và cái lứa tuổi mà trung niên là cái lứa tuổi gặp khá là phổ biến còn

| Token | Nhãn gốc |
|---|---|
| nhau | 0 |
| và | 0 |
| cái | 0 |
| lứa | 0 |
| tuổi | 0 |
| mà | 0 |
| trung | B-AGE |
| niên | I-AGE |
| là | 0 |
| cái | 0 |
| lứa | 0 |
| tuổi | 0 |
| gặp | 0 |
| khá | 0 |
| là | 0 |
| phổ | 0 |
| biến | 0 |
| còn | 0 |

## VM600-068 — dòng train 599 (đếm từ 0)

não đột quỵ đó thì nó liên quan đến việc hình thành các cục máu đông và việc cục máu đông đã nó trôi ra là đi

| Token | Nhãn gốc |
|---|---|
| não | B-ORGAN |
| đột | B-DISEASESYMTOM |
| quỵ | I-DISEASESYMTOM |
| đó | 0 |
| thì | 0 |
| nó | 0 |
| liên | 0 |
| quan | 0 |
| đến | 0 |
| việc | 0 |
| hình | 0 |
| thành | 0 |
| các | 0 |
| cục | B-DISEASESYMTOM |
| máu | I-DISEASESYMTOM |
| đông | I-DISEASESYMTOM |
| và | 0 |
| việc | 0 |
| cục | B-DISEASESYMTOM |
| máu | I-DISEASESYMTOM |
| đông | I-DISEASESYMTOM |
| đã | 0 |
| nó | 0 |
| trôi | 0 |
| ra | 0 |
| là | 0 |
| đi | 0 |

## VM600-069 — dòng train 600 (đếm từ 0)

alo alo rồi chúng tôi đang lắng nghe đây ạ mời cô trình bày

| Token | Nhãn gốc |
|---|---|
| alo | 0 |
| alo | 0 |
| rồi | 0 |
| chúng | 0 |
| tôi | 0 |
| đang | 0 |
| lắng | 0 |
| nghe | 0 |
| đây | 0 |
| ạ | 0 |
| mời | 0 |
| cô | B-GENDER |
| trình | 0 |
| bày | 0 |

## VM600-070 — dòng train 601 (đếm từ 0)

bệnh nền và hàng tháng phải đến bệnh viện để mà lấy thuốc thì chúng tôi liên tưởng đến chuyện là nhiều bệnh nhân

| Token | Nhãn gốc |
|---|---|
| bệnh | B-DISEASESYMTOM |
| nền | I-DISEASESYMTOM |
| và | 0 |
| hàng | B-DATETIME |
| tháng | I-DATETIME |
| phải | 0 |
| đến | 0 |
| bệnh | B-LOCATION |
| viện | I-LOCATION |
| để | 0 |
| mà | 0 |
| lấy | 0 |
| thuốc | B-DRUGCHEMICAL |
| thì | 0 |
| chúng | 0 |
| tôi | 0 |
| liên | 0 |
| tưởng | 0 |
| đến | 0 |
| chuyện | 0 |
| là | 0 |
| nhiều | 0 |
| bệnh | B-OCCUPATION |
| nhân | I-OCCUPATION |

## VM600-071 — dòng train 609 (đếm từ 0)

hiệu mà ngày xưa chúng ta vẫn hay phổ biến đấy là gì ạ nâng niu bàn chân việt thì trong trường hợp này của bác bác tìm

| Token | Nhãn gốc |
|---|---|
| hiệu | 0 |
| mà | 0 |
| ngày | B-DATETIME |
| xưa | I-DATETIME |
| chúng | 0 |
| ta | 0 |
| vẫn | 0 |
| hay | 0 |
| phổ | 0 |
| biến | 0 |
| đấy | 0 |
| là | 0 |
| gì | 0 |
| ạ | 0 |
| nâng | B-PERSONALCARE |
| niu | I-PERSONALCARE |
| bàn | B-ORGAN |
| chân | I-ORGAN |
| việt | 0 |
| thì | 0 |
| trong | 0 |
| trường | 0 |
| hợp | 0 |
| này | 0 |
| của | 0 |
| bác | B-AGE |
| bác | B-AGE |
| tìm | 0 |

## VM600-072 — dòng train 613 (đếm từ 0)

không phải có tác dụng phụ của các các loại thuốc này không phải mỗi cái chống viêm đâu rất nhiều các cái thuốc khác và

| Token | Nhãn gốc |
|---|---|
| không | 0 |
| phải | 0 |
| có | 0 |
| tác | B-DISEASESYMTOM |
| dụng | I-DISEASESYMTOM |
| phụ | I-DISEASESYMTOM |
| của | 0 |
| các | 0 |
| các | 0 |
| loại | 0 |
| thuốc | B-DRUGCHEMICAL |
| này | 0 |
| không | 0 |
| phải | 0 |
| mỗi | 0 |
| cái | 0 |
| chống | 0 |
| viêm | B-DISEASESYMTOM |
| đâu | 0 |
| rất | B-UNITCALIBRATOR |
| nhiều | I-UNITCALIBRATOR |
| các | 0 |
| cái | 0 |
| thuốc | B-DRUGCHEMICAL |
| khác | 0 |
| và | 0 |

## VM600-073 — dòng train 618 (đếm từ 0)

trị nó sẽ phải dài hơn và chúng ta sẽ phải tập trung vào cái cái vị trí căn nguyên của của cái bệnh là ở cái vùng

| Token | Nhãn gốc |
|---|---|
| trị | 0 |
| nó | 0 |
| sẽ | 0 |
| phải | 0 |
| dài | 0 |
| hơn | 0 |
| và | 0 |
| chúng | 0 |
| ta | 0 |
| sẽ | 0 |
| phải | 0 |
| tập | 0 |
| trung | 0 |
| vào | 0 |
| cái | 0 |
| cái | 0 |
| vị | 0 |
| trí | 0 |
| căn | 0 |
| nguyên | 0 |
| của | 0 |
| của | 0 |
| cái | 0 |
| bệnh | 0 |
| là | 0 |
| ở | 0 |
| cái | 0 |
| vùng | 0 |

## VM600-074 — dòng train 622 (đếm từ 0)

đây là một cái sản phẩm mà cũng đã được thừa kế cái đề tài nghiên cứu cấp nhà

| Token | Nhãn gốc |
|---|---|
| đây | 0 |
| là | 0 |
| một | 0 |
| cái | 0 |
| sản | 0 |
| phẩm | 0 |
| mà | 0 |
| cũng | 0 |
| đã | 0 |
| được | 0 |
| thừa | 0 |
| kế | 0 |
| cái | 0 |
| đề | 0 |
| tài | 0 |
| nghiên | B-DIAGNOSTICS |
| cứu | I-DIAGNOSTICS |
| cấp | 0 |
| nhà | B-LOCATION |

## VM600-075 — dòng train 645 (đếm từ 0)

ba nữa rõ ràng là gì ạ mình cần phải điều trị thì nó mới tránh được những cái chuyện mà đột ngột đột xuất hoặc thậm

| Token | Nhãn gốc |
|---|---|
| ba | 0 |
| nữa | 0 |
| rõ | 0 |
| ràng | 0 |
| là | 0 |
| gì | 0 |
| ạ | 0 |
| mình | 0 |
| cần | 0 |
| phải | 0 |
| điều | B-TREATMENT |
| trị | I-TREATMENT |
| thì | 0 |
| nó | 0 |
| mới | 0 |
| tránh | 0 |
| được | 0 |
| những | 0 |
| cái | 0 |
| chuyện | 0 |
| mà | 0 |
| đột | B-DATETIME |
| ngột | I-DATETIME |
| đột | 0 |
| xuất | 0 |
| hoặc | 0 |
| thậm | 0 |

## VM600-076 — dòng train 657 (đếm từ 0)

lại ảnh hưởng đến nội tạng là bởi vì khi mà chúng ta sử dụng vào trong thì tất cả những cái cơ quan nội tạng của chúng ta

| Token | Nhãn gốc |
|---|---|
| lại | 0 |
| ảnh | 0 |
| hưởng | 0 |
| đến | 0 |
| nội | B-ORGAN |
| tạng | I-ORGAN |
| là | 0 |
| bởi | 0 |
| vì | 0 |
| khi | 0 |
| mà | 0 |
| chúng | 0 |
| ta | 0 |
| sử | 0 |
| dụng | 0 |
| vào | 0 |
| trong | 0 |
| thì | 0 |
| tất | 0 |
| cả | 0 |
| những | 0 |
| cái | 0 |
| cơ | 0 |
| quan | 0 |
| nội | B-ORGAN |
| tạng | I-ORGAN |
| của | 0 |
| chúng | 0 |
| ta | 0 |

## VM600-077 — dòng train 664 (đếm từ 0)

mà cũng bị bệnh gì bác ạ dạ vâng ở đây thì vâng ở đây thì có lẽ

| Token | Nhãn gốc |
|---|---|
| mà | 0 |
| cũng | 0 |
| bị | B-DISEASESYMTOM |
| bệnh | I-DISEASESYMTOM |
| gì | 0 |
| bác | B-AGE |
| ạ | 0 |
| dạ | 0 |
| vâng | 0 |
| ở | 0 |
| đây | 0 |
| thì | 0 |
| vâng | 0 |
| ở | 0 |
| đây | 0 |
| thì | 0 |
| có | 0 |
| lẽ | 0 |

## VM600-078 — dòng train 680 (đếm từ 0)

trạng sạm nám tăng sắc tố do đó nên chúng ta phải nhớ là chúng ta luôn phải thoa kem chống nắng đúng cách đúng liều đủ

| Token | Nhãn gốc |
|---|---|
| trạng | 0 |
| sạm | B-DISEASESYMTOM |
| nám | I-DISEASESYMTOM |
| tăng | B-DISEASESYMTOM |
| sắc | I-DISEASESYMTOM |
| tố | I-DISEASESYMTOM |
| do | 0 |
| đó | 0 |
| nên | 0 |
| chúng | 0 |
| ta | 0 |
| phải | 0 |
| nhớ | 0 |
| là | 0 |
| chúng | 0 |
| ta | 0 |
| luôn | 0 |
| phải | 0 |
| thoa | 0 |
| kem | B-DRUGCHEMICAL |
| chống | I-DRUGCHEMICAL |
| nắng | I-DRUGCHEMICAL |
| đúng | 0 |
| cách | 0 |
| đúng | 0 |
| liều | 0 |
| đủ | 0 |

## VM600-079 — dòng train 687 (đếm từ 0)

cái ngưỡng mức điều trị như vậy thưa tất cả quý vị và các bạn vừa rồi thì chúng ta đã được lắng nghe bác sĩ chuyên khoa

| Token | Nhãn gốc |
|---|---|
| cái | B-UNITCALIBRATOR |
| ngưỡng | I-UNITCALIBRATOR |
| mức | I-UNITCALIBRATOR |
| điều | B-TREATMENT |
| trị | I-TREATMENT |
| như | 0 |
| vậy | 0 |
| thưa | 0 |
| tất | 0 |
| cả | 0 |
| quý | 0 |
| vị | 0 |
| và | 0 |
| các | 0 |
| bạn | 0 |
| vừa | 0 |
| rồi | 0 |
| thì | 0 |
| chúng | 0 |
| ta | 0 |
| đã | 0 |
| được | 0 |
| lắng | 0 |
| nghe | 0 |
| bác | B-OCCUPATION |
| sĩ | I-OCCUPATION |
| chuyên | I-OCCUPATION |
| khoa | I-OCCUPATION |

## VM600-080 — dòng train 699 (đếm từ 0)

chứng ngoài vận động khác cũng như là tuổi của người bệnh đã trở nên lớn hơn và khó khăn hơn và những cái vấn đề đó

| Token | Nhãn gốc |
|---|---|
| chứng | 0 |
| ngoài | 0 |
| vận | 0 |
| động | 0 |
| khác | 0 |
| cũng | 0 |
| như | 0 |
| là | 0 |
| tuổi | 0 |
| của | 0 |
| người | 0 |
| bệnh | 0 |
| đã | 0 |
| trở | 0 |
| nên | 0 |
| lớn | 0 |
| hơn | 0 |
| và | 0 |
| khó | 0 |
| khăn | 0 |
| hơn | 0 |
| và | 0 |
| những | 0 |
| cái | 0 |
| vấn | 0 |
| đề | 0 |
| đó | 0 |

## VM600-081 — dòng train 703 (đếm từ 0)

nhớ lại thời trung học khi bạn học về hệ tiêu hóa bạn đã được biết nó phân giải

| Token | Nhãn gốc |
|---|---|
| nhớ | 0 |
| lại | 0 |
| thời | B-DATETIME |
| trung | I-DATETIME |
| học | I-DATETIME |
| khi | 0 |
| bạn | 0 |
| học | 0 |
| về | 0 |
| hệ | B-ORGAN |
| tiêu | I-ORGAN |
| hóa | I-ORGAN |
| bạn | 0 |
| đã | 0 |
| được | 0 |
| biết | 0 |
| nó | 0 |
| phân | 0 |
| giải | 0 |

## VM600-082 — dòng train 716 (đếm từ 0)

những cái khó khăn mà bác gặp phải thì cũng rất là nhiều người bệnh người ta cũng đang gặp phải tuy nhiên là người ta

| Token | Nhãn gốc |
|---|---|
| những | 0 |
| cái | 0 |
| khó | 0 |
| khăn | 0 |
| mà | 0 |
| bác | B-AGE |
| gặp | 0 |
| phải | 0 |
| thì | 0 |
| cũng | 0 |
| rất | 0 |
| là | 0 |
| nhiều | 0 |
| người | 0 |
| bệnh | 0 |
| người | 0 |
| ta | 0 |
| cũng | 0 |
| đang | 0 |
| gặp | 0 |
| phải | 0 |
| tuy | 0 |
| nhiên | 0 |
| là | 0 |
| người | 0 |
| ta | 0 |

## VM600-083 — dòng train 722 (đếm từ 0)

hướng đến một cuộc sống mạnh khỏe hơn hạnh phúc và thành công chúng tôi sẽ thực sự rất biết ơn về sự ủng hộ quý báu

| Token | Nhãn gốc |
|---|---|
| hướng | 0 |
| đến | 0 |
| một | 0 |
| cuộc | 0 |
| sống | 0 |
| mạnh | 0 |
| khỏe | 0 |
| hơn | 0 |
| hạnh | 0 |
| phúc | 0 |
| và | 0 |
| thành | 0 |
| công | 0 |
| chúng | 0 |
| tôi | 0 |
| sẽ | 0 |
| thực | 0 |
| sự | 0 |
| rất | 0 |
| biết | 0 |
| ơn | 0 |
| về | 0 |
| sự | 0 |
| ủng | 0 |
| hộ | 0 |
| quý | 0 |
| báu | 0 |

## VM600-084 — dòng train 746 (đếm từ 0)

điều trị để chiến thắng chính bản thân mình giúp mình hồi phục đó là một điều rất là quan trọng vâng trong các cuộc

| Token | Nhãn gốc |
|---|---|
| điều | B-TREATMENT |
| trị | I-TREATMENT |
| để | 0 |
| chiến | 0 |
| thắng | 0 |
| chính | 0 |
| bản | 0 |
| thân | 0 |
| mình | 0 |
| giúp | 0 |
| mình | 0 |
| hồi | 0 |
| phục | 0 |
| đó | 0 |
| là | 0 |
| một | 0 |
| điều | 0 |
| rất | 0 |
| là | 0 |
| quan | 0 |
| trọng | 0 |
| vâng | 0 |
| trong | 0 |
| các | 0 |
| cuộc | 0 |

## VM600-085 — dòng train 750 (đếm từ 0)

đây cũng giúp cho họ tăng đậm độ năng lượng thì chúng ta có thể ví dụ như là thường ung thư thì phải nấu mềm lỏng này

| Token | Nhãn gốc |
|---|---|
| đây | 0 |
| cũng | 0 |
| giúp | 0 |
| cho | 0 |
| họ | 0 |
| tăng | 0 |
| đậm | 0 |
| độ | 0 |
| năng | 0 |
| lượng | 0 |
| thì | 0 |
| chúng | 0 |
| ta | 0 |
| có | 0 |
| thể | 0 |
| ví | 0 |
| dụ | 0 |
| như | 0 |
| là | 0 |
| thường | 0 |
| ung | B-DISEASESYMTOM |
| thư | I-DISEASESYMTOM |
| thì | 0 |
| phải | 0 |
| nấu | 0 |
| mềm | 0 |
| lỏng | 0 |
| này | 0 |

## VM600-086 — dòng train 756 (đếm từ 0)

xin điều trị có nghĩa là bị dại mà không

| Token | Nhãn gốc |
|---|---|
| xin | 0 |
| điều | B-TREATMENT |
| trị | I-TREATMENT |
| có | 0 |
| nghĩa | 0 |
| là | 0 |
| bị | B-DISEASESYMTOM |
| dại | I-DISEASESYMTOM |
| mà | 0 |
| không | 0 |

## VM600-087 — dòng train 767 (đếm từ 0)

mà chịu và cách tính dung nạp đối với những các sản phẩm nó cũng khắt khe hơn so với những cái làn da thường em thấy

| Token | Nhãn gốc |
|---|---|
| mà | 0 |
| chịu | 0 |
| và | 0 |
| cách | 0 |
| tính | B-UNITCALIBRATOR |
| dung | I-UNITCALIBRATOR |
| nạp | I-UNITCALIBRATOR |
| đối | 0 |
| với | 0 |
| những | 0 |
| các | 0 |
| sản | 0 |
| phẩm | 0 |
| nó | 0 |
| cũng | 0 |
| khắt | 0 |
| khe | 0 |
| hơn | 0 |
| so | 0 |
| với | 0 |
| những | 0 |
| cái | 0 |
| làn | B-ORGAN |
| da | I-ORGAN |
| thường | 0 |
| em | 0 |
| thấy | 0 |

## VM600-088 — dòng train 783 (đếm từ 0)

vừa rồi thì sẽ rất là tốt cho bệnh nhân ung thư đấy cũng là một giải pháp mà cũng bớt đi cái cái mà người ung thư đôi

| Token | Nhãn gốc |
|---|---|
| vừa | 0 |
| rồi | 0 |
| thì | 0 |
| sẽ | 0 |
| rất | 0 |
| là | 0 |
| tốt | 0 |
| cho | 0 |
| bệnh | B-OCCUPATION |
| nhân | I-OCCUPATION |
| ung | B-DISEASESYMTOM |
| thư | I-DISEASESYMTOM |
| đấy | 0 |
| cũng | 0 |
| là | 0 |
| một | 0 |
| giải | 0 |
| pháp | 0 |
| mà | 0 |
| cũng | 0 |
| bớt | 0 |
| đi | 0 |
| cái | 0 |
| cái | 0 |
| mà | 0 |
| người | 0 |
| ung | B-DISEASESYMTOM |
| thư | I-DISEASESYMTOM |
| đôi | 0 |

## VM600-089 — dòng train 804 (đếm từ 0)

trở lại cũng như là nó hỗ trợ cho vấn đề đường tiêu hóa của mình vâng

| Token | Nhãn gốc |
|---|---|
| trở | 0 |
| lại | 0 |
| cũng | 0 |
| như | 0 |
| là | 0 |
| nó | 0 |
| hỗ | B-MEDDEVICETECHNIQUE |
| trợ | I-MEDDEVICETECHNIQUE |
| cho | 0 |
| vấn | 0 |
| đề | 0 |
| đường | B-ORGAN |
| tiêu | I-ORGAN |
| hóa | I-ORGAN |
| của | 0 |
| mình | 0 |
| vâng | 0 |

## VM600-090 — dòng train 810 (đếm từ 0)

công việc chính của các chuyên gia tâm lý trong việc điều trị người bệnh béo phì

| Token | Nhãn gốc |
|---|---|
| công | 0 |
| việc | 0 |
| chính | 0 |
| của | 0 |
| các | 0 |
| chuyên | B-OCCUPATION |
| gia | I-OCCUPATION |
| tâm | 0 |
| lý | 0 |
| trong | 0 |
| việc | 0 |
| điều | B-TREATMENT |
| trị | I-TREATMENT |
| người | 0 |
| bệnh | 0 |
| béo | B-DISEASESYMTOM |
| phì | I-DISEASESYMTOM |

## VM600-091 — dòng train 819 (đếm từ 0)

cố định khớp đặc hiệu với mầm bệnh hoặc tế bào nhiễm bệnh hay đúng hơn là mô

| Token | Nhãn gốc |
|---|---|
| cố | 0 |
| định | 0 |
| khớp | B-ORGAN |
| đặc | 0 |
| hiệu | 0 |
| với | 0 |
| mầm | B-DISEASESYMTOM |
| bệnh | I-DISEASESYMTOM |
| hoặc | 0 |
| tế | B-ORGAN |
| bào | I-ORGAN |
| nhiễm | 0 |
| bệnh | 0 |
| hay | 0 |
| đúng | 0 |
| hơn | 0 |
| là | 0 |
| mô | B-ORGAN |

## VM600-092 — dòng train 821 (đếm từ 0)

thì đã có thể là giúp giảm rất là nhiều những cái biến chứng và những cái bệnh lý đi kèm như là có thể giảm được tới

| Token | Nhãn gốc |
|---|---|
| thì | 0 |
| đã | 0 |
| có | 0 |
| thể | 0 |
| là | 0 |
| giúp | 0 |
| giảm | 0 |
| rất | 0 |
| là | 0 |
| nhiều | 0 |
| những | 0 |
| cái | 0 |
| biến | B-DISEASESYMTOM |
| chứng | I-DISEASESYMTOM |
| và | 0 |
| những | 0 |
| cái | 0 |
| bệnh | B-DISEASESYMTOM |
| lý | I-DISEASESYMTOM |
| đi | 0 |
| kèm | 0 |
| như | 0 |
| là | 0 |
| có | 0 |
| thể | 0 |
| giảm | 0 |
| được | 0 |
| tới | 0 |

## VM600-093 — dòng train 841 (đếm từ 0)

hoàn toàn ô thế là mình điều trị xong rồi xong rồi cứ ba tháng xét nghiệm một lần hay là sáu tháng xét nghiệm một lần

| Token | Nhãn gốc |
|---|---|
| hoàn | 0 |
| toàn | 0 |
| ô | 0 |
| thế | 0 |
| là | 0 |
| mình | 0 |
| điều | B-TREATMENT |
| trị | I-TREATMENT |
| xong | 0 |
| rồi | 0 |
| xong | 0 |
| rồi | 0 |
| cứ | 0 |
| ba | B-DATETIME |
| tháng | I-DATETIME |
| xét | B-DIAGNOSTICS |
| nghiệm | I-DIAGNOSTICS |
| một | 0 |
| lần | 0 |
| hay | 0 |
| là | 0 |
| sáu | B-DATETIME |
| tháng | I-DATETIME |
| xét | B-DIAGNOSTICS |
| nghiệm | I-DIAGNOSTICS |
| một | 0 |
| lần | 0 |

## VM600-094 — dòng train 842 (đếm từ 0)

kết quả này có thể giúp dự đoán gánh nặng bệnh alzheimer ở cả nước đang phát triển nơi sự đa dạng vi sinh vật đang

| Token | Nhãn gốc |
|---|---|
| kết | 0 |
| quả | 0 |
| này | 0 |
| có | 0 |
| thể | 0 |
| giúp | 0 |
| dự | B-MEDDEVICETECHNIQUE |
| đoán | I-MEDDEVICETECHNIQUE |
| gánh | 0 |
| nặng | 0 |
| bệnh | 0 |
| alzheimer | B-DISEASESYMTOM |
| ở | 0 |
| cả | 0 |
| nước | B-LOCATION |
| đang | I-LOCATION |
| phát | I-LOCATION |
| triển | I-LOCATION |
| nơi | 0 |
| sự | 0 |
| đa | 0 |
| dạng | 0 |
| vi | B-ORGAN |
| sinh | I-ORGAN |
| vật | I-ORGAN |
| đang | 0 |

## VM600-095 — dòng train 851 (đếm từ 0)

ung thư ấy hoàn toàn là do người bệnh ung thư cho nên chúng tôi rất mong là dù

| Token | Nhãn gốc |
|---|---|
| ung | B-DISEASESYMTOM |
| thư | I-DISEASESYMTOM |
| ấy | 0 |
| hoàn | 0 |
| toàn | 0 |
| là | 0 |
| do | 0 |
| người | 0 |
| bệnh | 0 |
| ung | B-DISEASESYMTOM |
| thư | I-DISEASESYMTOM |
| cho | 0 |
| nên | 0 |
| chúng | 0 |
| tôi | 0 |
| rất | 0 |
| mong | 0 |
| là | 0 |
| dù | 0 |

## VM600-096 — dòng train 854 (đếm từ 0)

thức ăn đó thì nó sẽ làm cho dễ bị béo phì nữa đối với lại môi trường xã hội

| Token | Nhãn gốc |
|---|---|
| thức | B-FOODDRINK |
| ăn | I-FOODDRINK |
| đó | 0 |
| thì | 0 |
| nó | 0 |
| sẽ | 0 |
| làm | 0 |
| cho | 0 |
| dễ | 0 |
| bị | 0 |
| béo | B-DISEASESYMTOM |
| phì | I-DISEASESYMTOM |
| nữa | 0 |
| đối | 0 |
| với | 0 |
| lại | 0 |
| môi | B-ORGAN |
| trường | 0 |
| xã | 0 |
| hội | 0 |

## VM600-097 — dòng train 857 (đếm từ 0)

alo vâng chúng tôi đang nghe đây ạ cô chia sẻ đi ạ

| Token | Nhãn gốc |
|---|---|
| alo | 0 |
| vâng | 0 |
| chúng | 0 |
| tôi | 0 |
| đang | 0 |
| nghe | 0 |
| đây | 0 |
| ạ | 0 |
| cô | B-GENDER |
| chia | 0 |
| sẻ | 0 |
| đi | 0 |
| ạ | 0 |

## VM600-098 — dòng train 875 (đếm từ 0)

thương thận vân vân và vân vân cho nên là lời khuyên thứ hai của chương trình đối với bác là gì nên tìm đến những giải

| Token | Nhãn gốc |
|---|---|
| thương | 0 |
| thận | 0 |
| vân | 0 |
| vân | 0 |
| và | 0 |
| vân | 0 |
| vân | 0 |
| cho | 0 |
| nên | 0 |
| là | 0 |
| lời | 0 |
| khuyên | 0 |
| thứ | 0 |
| hai | 0 |
| của | 0 |
| chương | 0 |
| trình | 0 |
| đối | 0 |
| với | 0 |
| bác | B-AGE |
| là | 0 |
| gì | 0 |
| nên | 0 |
| tìm | 0 |
| đến | 0 |
| những | 0 |
| giải | 0 |

## VM600-099 — dòng train 892 (đếm từ 0)

bác ơi vâng bây giờ thì với cái tình trạng hiện nay của bác này thứ nhất là huyết áp đang tăng cao thì bác nên bác

| Token | Nhãn gốc |
|---|---|
| bác | B-AGE |
| ơi | 0 |
| vâng | 0 |
| bây | B-DATETIME |
| giờ | I-DATETIME |
| thì | 0 |
| với | 0 |
| cái | 0 |
| tình | 0 |
| trạng | 0 |
| hiện | B-DATETIME |
| nay | I-DATETIME |
| của | 0 |
| bác | B-AGE |
| này | 0 |
| thứ | B-UNITCALIBRATOR |
| nhất | I-UNITCALIBRATOR |
| là | 0 |
| huyết | B-DISEASESYMTOM |
| áp | I-DISEASESYMTOM |
| đang | 0 |
| tăng | 0 |
| cao | B-UNITCALIBRATOR |
| thì | 0 |
| bác | B-AGE |
| nên | 0 |
| bác | B-AGE |

## VM600-100 — dòng train 899 (đếm từ 0)

mất do tổn thương đường tiêu hóa không không thể nào tiêu hóa thu được là do ngay cái chính khối u đó cũng làm tăng quá

| Token | Nhãn gốc |
|---|---|
| mất | 0 |
| do | 0 |
| tổn | B-DISEASESYMTOM |
| thương | I-DISEASESYMTOM |
| đường | B-ORGAN |
| tiêu | I-ORGAN |
| hóa | I-ORGAN |
| không | 0 |
| không | 0 |
| thể | 0 |
| nào | 0 |
| tiêu | 0 |
| hóa | 0 |
| thu | 0 |
| được | 0 |
| là | 0 |
| do | 0 |
| ngay | 0 |
| cái | 0 |
| chính | 0 |
| khối | B-DISEASESYMTOM |
| u | I-DISEASESYMTOM |
| đó | 0 |
| cũng | 0 |
| làm | 0 |
| tăng | 0 |
| quá | 0 |

## VM600-101 — dòng train 914 (đếm từ 0)

là làm việc hàng ngày để phần nào có thể khắc phục được cái tình trạng mà bác phải di chuyển nhiều như vậy mà cái bệnh

| Token | Nhãn gốc |
|---|---|
| là | 0 |
| làm | 0 |
| việc | 0 |
| hàng | B-DATETIME |
| ngày | I-DATETIME |
| để | 0 |
| phần | 0 |
| nào | 0 |
| có | 0 |
| thể | 0 |
| khắc | 0 |
| phục | 0 |
| được | 0 |
| cái | 0 |
| tình | 0 |
| trạng | 0 |
| mà | 0 |
| bác | B-AGE |
| phải | 0 |
| di | 0 |
| chuyển | 0 |
| nhiều | 0 |
| như | 0 |
| vậy | 0 |
| mà | 0 |
| cái | 0 |
| bệnh | 0 |

## VM600-102 — dòng train 918 (đếm từ 0)

ta muốn mua cái gì để mua nhưng mà chúng ta phải có hệ thống kiểm nghiệm và hệ thống kiểm đó là được tiến hành bởi gì

| Token | Nhãn gốc |
|---|---|
| ta | 0 |
| muốn | 0 |
| mua | 0 |
| cái | 0 |
| gì | 0 |
| để | 0 |
| mua | 0 |
| nhưng | 0 |
| mà | 0 |
| chúng | 0 |
| ta | 0 |
| phải | 0 |
| có | 0 |
| hệ | 0 |
| thống | 0 |
| kiểm | B-PREVENTIVEMED |
| nghiệm | I-PREVENTIVEMED |
| và | 0 |
| hệ | 0 |
| thống | 0 |
| kiểm | 0 |
| đó | 0 |
| là | 0 |
| được | 0 |
| tiến | 0 |
| hành | 0 |
| bởi | 0 |
| gì | 0 |

## VM600-103 — dòng train 919 (đếm từ 0)

vị ngọt thậm chí cũng không thích nữa rồi vị tanh không chịu được không thể chấp nhận thức ăn và đặc biệt là làm cho

| Token | Nhãn gốc |
|---|---|
| vị | 0 |
| ngọt | 0 |
| thậm | 0 |
| chí | 0 |
| cũng | 0 |
| không | 0 |
| thích | 0 |
| nữa | 0 |
| rồi | 0 |
| vị | 0 |
| tanh | 0 |
| không | 0 |
| chịu | 0 |
| được | 0 |
| không | 0 |
| thể | 0 |
| chấp | 0 |
| nhận | 0 |
| thức | B-FOODDRINK |
| ăn | I-FOODDRINK |
| và | 0 |
| đặc | 0 |
| biệt | 0 |
| là | 0 |
| làm | 0 |
| cho | 0 |

## VM600-104 — dòng train 923 (đếm từ 0)

khi mà chúng ta đến nơi đây ví dụ như anh đến những cái nơi thì anh thấy đông

| Token | Nhãn gốc |
|---|---|
| khi | 0 |
| mà | 0 |
| chúng | 0 |
| ta | 0 |
| đến | 0 |
| nơi | 0 |
| đây | 0 |
| ví | 0 |
| dụ | 0 |
| như | 0 |
| anh | 0 |
| đến | 0 |
| những | 0 |
| cái | 0 |
| nơi | 0 |
| thì | 0 |
| anh | 0 |
| thấy | 0 |
| đông | 0 |

## VM600-105 — dòng train 931 (đếm từ 0)

của cơ thể của chúng ta nghĩa là từ hệ tim mạch hệ huyết áp rồi là đến hệ hô

| Token | Nhãn gốc |
|---|---|
| của | 0 |
| cơ | B-ORGAN |
| thể | I-ORGAN |
| của | 0 |
| chúng | 0 |
| ta | 0 |
| nghĩa | 0 |
| là | 0 |
| từ | 0 |
| hệ | 0 |
| tim | B-ORGAN |
| mạch | I-ORGAN |
| hệ | 0 |
| huyết | B-DISEASESYMTOM |
| áp | I-DISEASESYMTOM |
| rồi | 0 |
| là | 0 |
| đến | 0 |
| hệ | 0 |
| hô | 0 |

## VM600-106 — dòng train 934 (đếm từ 0)

trắng hoặc là chiết xuất từ hoa thủy tiên biển nó đều làm tăng với hiệu quả để mà giúp cho quá trình sáng da

| Token | Nhãn gốc |
|---|---|
| trắng | 0 |
| hoặc | 0 |
| là | 0 |
| chiết | B-MEDDEVICETECHNIQUE |
| xuất | I-MEDDEVICETECHNIQUE |
| từ | 0 |
| hoa | B-DRUGCHEMICAL |
| thủy | I-DRUGCHEMICAL |
| tiên | I-DRUGCHEMICAL |
| biển | I-DRUGCHEMICAL |
| nó | 0 |
| đều | 0 |
| làm | 0 |
| tăng | 0 |
| với | 0 |
| hiệu | 0 |
| quả | 0 |
| để | 0 |
| mà | 0 |
| giúp | 0 |
| cho | 0 |
| quá | B-TREATMENT |
| trình | I-TREATMENT |
| sáng | I-TREATMENT |
| da | B-ORGAN |

## VM600-107 — dòng train 950 (đếm từ 0)

trọng trong miễn dịch không ai thực sự biết được những hoạt động như thế nào cho đến nhà

| Token | Nhãn gốc |
|---|---|
| trọng | 0 |
| trong | 0 |
| miễn | 0 |
| dịch | 0 |
| không | 0 |
| ai | 0 |
| thực | 0 |
| sự | 0 |
| biết | 0 |
| được | 0 |
| những | 0 |
| hoạt | 0 |
| động | 0 |
| như | 0 |
| thế | 0 |
| nào | 0 |
| cho | 0 |
| đến | 0 |
| nhà | B-LOCATION |

## VM600-108 — dòng train 960 (đếm từ 0)

penicillin vẫn còn hiệu quả trên một số lượng lớn vi khuẩn nó gắn vào các phân

| Token | Nhãn gốc |
|---|---|
| penicillin | B-DRUGCHEMICAL |
| vẫn | 0 |
| còn | 0 |
| hiệu | 0 |
| quả | 0 |
| trên | 0 |
| một | 0 |
| số | 0 |
| lượng | 0 |
| lớn | 0 |
| vi | B-DISEASESYMTOM |
| khuẩn | I-DISEASESYMTOM |
| nó | 0 |
| gắn | 0 |
| vào | 0 |
| các | 0 |
| phân | 0 |

## VM600-109 — dòng train 963 (đếm từ 0)

cái những cái thiết bị định vị để người ta đi vào cái thứ ba đây là một cái phẫu

| Token | Nhãn gốc |
|---|---|
| cái | 0 |
| những | 0 |
| cái | 0 |
| thiết | B-MEDDEVICETECHNIQUE |
| bị | I-MEDDEVICETECHNIQUE |
| định | I-MEDDEVICETECHNIQUE |
| vị | I-MEDDEVICETECHNIQUE |
| để | 0 |
| người | 0 |
| ta | 0 |
| đi | 0 |
| vào | 0 |
| cái | 0 |
| thứ | 0 |
| ba | 0 |
| đây | 0 |
| là | 0 |
| một | 0 |
| cái | 0 |
| phẫu | 0 |

## VM600-110 — dòng train 966 (đếm từ 0)

phát triển và nó tích lũy được những hoạt chất quý giá nhưng mà đương nhiên chúng ta thấy một điều là đông trùng hạ

| Token | Nhãn gốc |
|---|---|
| phát | 0 |
| triển | 0 |
| và | 0 |
| nó | 0 |
| tích | 0 |
| lũy | 0 |
| được | 0 |
| những | 0 |
| hoạt | B-DRUGCHEMICAL |
| chất | I-DRUGCHEMICAL |
| quý | 0 |
| giá | 0 |
| nhưng | 0 |
| mà | 0 |
| đương | 0 |
| nhiên | 0 |
| chúng | 0 |
| ta | 0 |
| thấy | 0 |
| một | 0 |
| điều | 0 |
| là | 0 |
| đông | B-FOODDRINK |
| trùng | I-FOODDRINK |
| hạ | 0 |

## VM600-111 — dòng train 967 (đếm từ 0)

đang gặp phải cái tình trạng bệnh lý đó chính là bị cao huyết áp nè bệnh lý về tim mạch nè bệnh lý đái tháo đường hoặc

| Token | Nhãn gốc |
|---|---|
| đang | 0 |
| gặp | 0 |
| phải | 0 |
| cái | 0 |
| tình | 0 |
| trạng | 0 |
| bệnh | 0 |
| lý | 0 |
| đó | 0 |
| chính | 0 |
| là | 0 |
| bị | 0 |
| cao | B-DISEASESYMTOM |
| huyết | I-DISEASESYMTOM |
| áp | I-DISEASESYMTOM |
| nè | 0 |
| bệnh | 0 |
| lý | 0 |
| về | 0 |
| tim | B-ORGAN |
| mạch | I-ORGAN |
| nè | 0 |
| bệnh | 0 |
| lý | 0 |
| đái | B-DISEASESYMTOM |
| tháo | I-DISEASESYMTOM |
| đường | I-DISEASESYMTOM |
| hoặc | 0 |

## VM600-112 — dòng train 984 (đếm từ 0)

mỗi tế bào t hoặc tế bào b riêng lẻ có hình dạng khác nhau đôi chút cho

| Token | Nhãn gốc |
|---|---|
| mỗi | 0 |
| tế | B-ORGAN |
| bào | I-ORGAN |
| t | I-ORGAN |
| hoặc | 0 |
| tế | B-ORGAN |
| bào | I-ORGAN |
| b | I-ORGAN |
| riêng | 0 |
| lẻ | 0 |
| có | 0 |
| hình | 0 |
| dạng | 0 |
| khác | 0 |
| nhau | 0 |
| đôi | 0 |
| chút | 0 |
| cho | 0 |

## VM600-113 — dòng train 1006 (đếm từ 0)

để độ khoảng năm bảy phút và mình có thể để khoảng mười phút thì mình nhớ là bát cháo

| Token | Nhãn gốc |
|---|---|
| để | 0 |
| độ | 0 |
| khoảng | 0 |
| năm | 0 |
| bảy | 0 |
| phút | 0 |
| và | 0 |
| mình | 0 |
| có | 0 |
| thể | 0 |
| để | 0 |
| khoảng | 0 |
| mười | 0 |
| phút | 0 |
| thì | 0 |
| mình | 0 |
| nhớ | 0 |
| là | 0 |
| bát | B-FOODDRINK |
| cháo | I-FOODDRINK |

## VM600-114 — dòng train 1010 (đếm từ 0)

với những thảo dược khác mục đích là cái gì à thì trong một cái đơn thuốc của y học cổ truyền chúng ta

| Token | Nhãn gốc |
|---|---|
| với | 0 |
| những | 0 |
| thảo | B-DRUGCHEMICAL |
| dược | I-DRUGCHEMICAL |
| khác | 0 |
| mục | 0 |
| đích | 0 |
| là | 0 |
| cái | 0 |
| gì | 0 |
| à | 0 |
| thì | 0 |
| trong | 0 |
| một | 0 |
| cái | 0 |
| đơn | 0 |
| thuốc | B-DRUGCHEMICAL |
| của | I-DRUGCHEMICAL |
| y | I-DRUGCHEMICAL |
| học | I-DRUGCHEMICAL |
| cổ | I-DRUGCHEMICAL |
| truyền | I-DRUGCHEMICAL |
| chúng | 0 |
| ta | 0 |

## VM600-115 — dòng train 1017 (đếm từ 0)

khi phẫu thuật để có được kết quả như mong đợi ngoài ra thì người bệnh parkinson cần phải chuẩn bị những vấn đề

| Token | Nhãn gốc |
|---|---|
| khi | 0 |
| phẫu | B-SURGERY |
| thuật | I-SURGERY |
| để | 0 |
| có | 0 |
| được | 0 |
| kết | 0 |
| quả | 0 |
| như | 0 |
| mong | 0 |
| đợi | 0 |
| ngoài | 0 |
| ra | 0 |
| thì | 0 |
| người | 0 |
| bệnh | 0 |
| parkinson | B-DISEASESYMTOM |
| cần | 0 |
| phải | 0 |
| chuẩn | 0 |
| bị | 0 |
| những | 0 |
| vấn | 0 |
| đề | 0 |

## VM600-116 — dòng train 1022 (đếm từ 0)

thì lại nên giảm thịt đỏ thịt đỏ là thịt con bốn chân ví dụ như thịt lợn thịt bò thì chúng ta chỉ nên tối đa là năm mươi gam

| Token | Nhãn gốc |
|---|---|
| thì | 0 |
| lại | 0 |
| nên | 0 |
| giảm | 0 |
| thịt | B-FOODDRINK |
| đỏ | I-FOODDRINK |
| thịt | B-FOODDRINK |
| đỏ | I-FOODDRINK |
| là | 0 |
| thịt | 0 |
| con | 0 |
| bốn | 0 |
| chân | B-ORGAN |
| ví | 0 |
| dụ | 0 |
| như | 0 |
| thịt | B-FOODDRINK |
| lợn | I-FOODDRINK |
| thịt | B-FOODDRINK |
| bò | I-FOODDRINK |
| thì | 0 |
| chúng | 0 |
| ta | 0 |
| chỉ | 0 |
| nên | 0 |
| tối | B-DATETIME |
| đa | 0 |
| là | 0 |
| năm | B-UNITCALIBRATOR |
| mươi | I-UNITCALIBRATOR |
| gam | 0 |

## VM600-117 — dòng train 1023 (đếm từ 0)

xảy ra nếu sự hiện diện của một thứ chưa từng có trong cơ thể bạn trước đây không phải là dấu hiệu duy nhất cho việc đáp

| Token | Nhãn gốc |
|---|---|
| xảy | 0 |
| ra | 0 |
| nếu | 0 |
| sự | 0 |
| hiện | 0 |
| diện | 0 |
| của | 0 |
| một | 0 |
| thứ | 0 |
| chưa | 0 |
| từng | 0 |
| có | 0 |
| trong | 0 |
| cơ | B-ORGAN |
| thể | I-ORGAN |
| bạn | 0 |
| trước | 0 |
| đây | 0 |
| không | 0 |
| phải | 0 |
| là | 0 |
| dấu | 0 |
| hiệu | 0 |
| duy | 0 |
| nhất | 0 |
| cho | 0 |
| việc | 0 |
| đáp | 0 |

## VM600-118 — dòng train 1027 (đếm từ 0)

cũng phải cố gắng lên một chút thì chúng ta mới dần dần cải thiện được sức khỏe mà có cải thiện sức khỏe thì chúng ta

| Token | Nhãn gốc |
|---|---|
| cũng | 0 |
| phải | 0 |
| cố | 0 |
| gắng | 0 |
| lên | 0 |
| một | 0 |
| chút | 0 |
| thì | 0 |
| chúng | 0 |
| ta | 0 |
| mới | 0 |
| dần | 0 |
| dần | 0 |
| cải | B-TREATMENT |
| thiện | I-TREATMENT |
| được | 0 |
| sức | 0 |
| khỏe | 0 |
| mà | 0 |
| có | 0 |
| cải | B-TREATMENT |
| thiện | I-TREATMENT |
| sức | 0 |
| khỏe | 0 |
| thì | 0 |
| chúng | 0 |
| ta | 0 |

## VM600-119 — dòng train 1030 (đếm từ 0)

đề mà bản thân bệnh viện bệnh nhân đã bị rồi đó là gì cái tình trạng vữa xơ động mạch cái này có thể nói rằng là như phần

| Token | Nhãn gốc |
|---|---|
| đề | 0 |
| mà | 0 |
| bản | 0 |
| thân | 0 |
| bệnh | B-LOCATION |
| viện | I-LOCATION |
| bệnh | B-OCCUPATION |
| nhân | I-OCCUPATION |
| đã | 0 |
| bị | 0 |
| rồi | 0 |
| đó | 0 |
| là | 0 |
| gì | 0 |
| cái | 0 |
| tình | 0 |
| trạng | 0 |
| vữa | B-DISEASESYMTOM |
| xơ | I-DISEASESYMTOM |
| động | I-DISEASESYMTOM |
| mạch | I-DISEASESYMTOM |
| cái | 0 |
| này | 0 |
| có | 0 |
| thể | 0 |
| nói | 0 |
| rằng | 0 |
| là | 0 |
| như | 0 |
| phần | 0 |

## VM600-120 — dòng train 1035 (đếm từ 0)

hòa lên để mình có thể có được một cái bữa ăn là bữa ăn ấy có thể là bữa ăn dặm phụ vào để mà chúng ta cung cấp

| Token | Nhãn gốc |
|---|---|
| hòa | 0 |
| lên | 0 |
| để | 0 |
| mình | 0 |
| có | 0 |
| thể | 0 |
| có | 0 |
| được | 0 |
| một | 0 |
| cái | 0 |
| bữa | 0 |
| ăn | 0 |
| là | 0 |
| bữa | 0 |
| ăn | 0 |
| ấy | 0 |
| có | 0 |
| thể | 0 |
| là | 0 |
| bữa | 0 |
| ăn | B-PERSONALCARE |
| dặm | I-PERSONALCARE |
| phụ | 0 |
| vào | 0 |
| để | 0 |
| mà | 0 |
| chúng | 0 |
| ta | 0 |
| cung | 0 |
| cấp | 0 |

## VM600-121 — dòng train 1041 (đếm từ 0)

hướng thảo luận về vai trò của lần lượt từng phân tử hoặc tế bào nhưng điều đó

| Token | Nhãn gốc |
|---|---|
| hướng | 0 |
| thảo | 0 |
| luận | 0 |
| về | 0 |
| vai | 0 |
| trò | 0 |
| của | 0 |
| lần | 0 |
| lượt | 0 |
| từng | 0 |
| phân | B-UNITCALIBRATOR |
| tử | I-UNITCALIBRATOR |
| hoặc | 0 |
| tế | B-ORGAN |
| bào | I-ORGAN |
| nhưng | 0 |
| điều | 0 |
| đó | 0 |

## VM600-122 — dòng train 1044 (đếm từ 0)

các tế bào thần kinh nó không liên kết được với nhau bởi vì sao bởi vì các cái chất dẫn truyền thần kinh mà để cái

| Token | Nhãn gốc |
|---|---|
| các | 0 |
| tế | B-ORGAN |
| bào | I-ORGAN |
| thần | B-ORGAN |
| kinh | I-ORGAN |
| nó | 0 |
| không | 0 |
| liên | 0 |
| kết | 0 |
| được | 0 |
| với | 0 |
| nhau | 0 |
| bởi | 0 |
| vì | 0 |
| sao | 0 |
| bởi | 0 |
| vì | 0 |
| các | 0 |
| cái | 0 |
| chất | 0 |
| dẫn | 0 |
| truyền | 0 |
| thần | B-ORGAN |
| kinh | I-ORGAN |
| mà | 0 |
| để | 0 |
| cái | 0 |

## VM600-123 — dòng train 1049 (đếm từ 0)

lên thì họ những thấy những cái hình thi hoa hậu rồi này nọ hay là thấy những cái hình đối với nam thì ở thấy những hình

| Token | Nhãn gốc |
|---|---|
| lên | 0 |
| thì | 0 |
| họ | 0 |
| những | 0 |
| thấy | 0 |
| những | 0 |
| cái | 0 |
| hình | 0 |
| thi | 0 |
| hoa | 0 |
| hậu | 0 |
| rồi | 0 |
| này | 0 |
| nọ | 0 |
| hay | 0 |
| là | 0 |
| thấy | 0 |
| những | 0 |
| cái | 0 |
| hình | 0 |
| đối | 0 |
| với | 0 |
| nam | B-GENDER |
| thì | 0 |
| ở | 0 |
| thấy | 0 |
| những | 0 |
| hình | 0 |

## VM600-124 — dòng train 1051 (đếm từ 0)

lại họ thường tranh luận về các vấn đề khoa học trong xe của họ và sau đó chỉ đơn giản là quên những gì đã nói nhưng

| Token | Nhãn gốc |
|---|---|
| lại | 0 |
| họ | 0 |
| thường | 0 |
| tranh | 0 |
| luận | 0 |
| về | 0 |
| các | 0 |
| vấn | 0 |
| đề | 0 |
| khoa | 0 |
| học | 0 |
| trong | 0 |
| xe | 0 |
| của | 0 |
| họ | 0 |
| và | 0 |
| sau | 0 |
| đó | 0 |
| chỉ | 0 |
| đơn | 0 |
| giản | 0 |
| là | 0 |
| quên | 0 |
| những | 0 |
| gì | 0 |
| đã | 0 |
| nói | 0 |
| nhưng | 0 |

## VM600-125 — dòng train 1056 (đếm từ 0)

bên ngoài bằng những phương pháp phù hợp và đó chính là mấu chốt để có thể nâng tầm chất lượng của các quy trình công

| Token | Nhãn gốc |
|---|---|
| bên | B-LOCATION |
| ngoài | I-LOCATION |
| bằng | 0 |
| những | 0 |
| phương | 0 |
| pháp | 0 |
| phù | 0 |
| hợp | 0 |
| và | 0 |
| đó | 0 |
| chính | 0 |
| là | 0 |
| mấu | 0 |
| chốt | 0 |
| để | 0 |
| có | 0 |
| thể | 0 |
| nâng | 0 |
| tầm | 0 |
| chất | 0 |
| lượng | 0 |
| của | 0 |
| các | 0 |
| quy | 0 |
| trình | 0 |
| công | 0 |

## VM600-126 — dòng train 1077 (đếm từ 0)

như tình trạng dinh dưỡng của bệnh nhân không tốt thì rất khó có thể giúp cho bệnh nhân có thể chịu đựng được hết cái

| Token | Nhãn gốc |
|---|---|
| như | 0 |
| tình | 0 |
| trạng | 0 |
| dinh | 0 |
| dưỡng | 0 |
| của | 0 |
| bệnh | B-OCCUPATION |
| nhân | I-OCCUPATION |
| không | 0 |
| tốt | 0 |
| thì | 0 |
| rất | 0 |
| khó | 0 |
| có | 0 |
| thể | 0 |
| giúp | 0 |
| cho | 0 |
| bệnh | B-OCCUPATION |
| nhân | I-OCCUPATION |
| có | 0 |
| thể | 0 |
| chịu | 0 |
| đựng | 0 |
| được | 0 |
| hết | 0 |
| cái | 0 |

## VM600-127 — dòng train 1081 (đếm từ 0)

quang của chúng ta và hãy vững tin hãy có một cái tinh thần tốt để mau chóng

| Token | Nhãn gốc |
|---|---|
| quang | 0 |
| của | 0 |
| chúng | 0 |
| ta | 0 |
| và | 0 |
| hãy | 0 |
| vững | 0 |
| tin | 0 |
| hãy | 0 |
| có | 0 |
| một | 0 |
| cái | 0 |
| tinh | 0 |
| thần | 0 |
| tốt | 0 |
| để | 0 |
| mau | 0 |
| chóng | 0 |

## VM600-128 — dòng train 1088 (đếm từ 0)

nhiên là bệnh nhân sẽ phải nhịn ăn từ sáng hôm đó và bệnh nhân sẽ được đưa

| Token | Nhãn gốc |
|---|---|
| nhiên | 0 |
| là | 0 |
| bệnh | B-OCCUPATION |
| nhân | I-OCCUPATION |
| sẽ | 0 |
| phải | 0 |
| nhịn | 0 |
| ăn | 0 |
| từ | 0 |
| sáng | 0 |
| hôm | 0 |
| đó | 0 |
| và | 0 |
| bệnh | B-OCCUPATION |
| nhân | I-OCCUPATION |
| sẽ | 0 |
| được | 0 |
| đưa | 0 |

## VM600-129 — dòng train 1097 (đếm từ 0)

cân đối mà đây chúng tôi thì quan niệm cân đối ở đây thì quan trọng nhất đó là cân đối giữa chất đạm động vật và thực

| Token | Nhãn gốc |
|---|---|
| cân | 0 |
| đối | 0 |
| mà | 0 |
| đây | 0 |
| chúng | 0 |
| tôi | 0 |
| thì | 0 |
| quan | 0 |
| niệm | 0 |
| cân | 0 |
| đối | 0 |
| ở | 0 |
| đây | 0 |
| thì | 0 |
| quan | 0 |
| trọng | 0 |
| nhất | 0 |
| đó | 0 |
| là | 0 |
| cân | 0 |
| đối | 0 |
| giữa | 0 |
| chất | 0 |
| đạm | B-FOODDRINK |
| động | 0 |
| vật | 0 |
| và | 0 |
| thực | 0 |

## VM600-130 — dòng train 1105 (đếm từ 0)

chia sẻ theo chúng ta về những trở ngại và thách thức tâm lý mà người bệnh béo phì luôn phải đối mặt

| Token | Nhãn gốc |
|---|---|
| chia | 0 |
| sẻ | 0 |
| theo | 0 |
| chúng | 0 |
| ta | 0 |
| về | 0 |
| những | 0 |
| trở | 0 |
| ngại | 0 |
| và | 0 |
| thách | 0 |
| thức | 0 |
| tâm | 0 |
| lý | 0 |
| mà | 0 |
| người | 0 |
| bệnh | 0 |
| béo | B-DISEASESYMTOM |
| phì | I-DISEASESYMTOM |
| luôn | 0 |
| phải | 0 |
| đối | 0 |
| mặt | 0 |

## VM600-131 — dòng train 1107 (đếm từ 0)

ra những cái dụng cụ rất là tốt thì để cho có việc mà chúng ta luồn cái ống đó

| Token | Nhãn gốc |
|---|---|
| ra | 0 |
| những | 0 |
| cái | 0 |
| dụng | 0 |
| cụ | 0 |
| rất | 0 |
| là | 0 |
| tốt | 0 |
| thì | 0 |
| để | 0 |
| cho | 0 |
| có | 0 |
| việc | 0 |
| mà | 0 |
| chúng | 0 |
| ta | 0 |
| luồn | 0 |
| cái | 0 |
| ống | 0 |
| đó | 0 |

## VM600-132 — dòng train 1117 (đếm từ 0)

có những cái biến chứng của cái việc sử dụng chống viêm corticoid rồi đó là chảy máu dạ dày đó là viêm loét dạ dày

| Token | Nhãn gốc |
|---|---|
| có | 0 |
| những | 0 |
| cái | 0 |
| biến | B-DISEASESYMTOM |
| chứng | I-DISEASESYMTOM |
| của | 0 |
| cái | 0 |
| việc | 0 |
| sử | 0 |
| dụng | 0 |
| chống | 0 |
| viêm | B-DISEASESYMTOM |
| corticoid | B-DRUGCHEMICAL |
| rồi | 0 |
| đó | 0 |
| là | 0 |
| chảy | B-DISEASESYMTOM |
| máu | I-DISEASESYMTOM |
| dạ | B-ORGAN |
| dày | I-ORGAN |
| đó | 0 |
| là | 0 |
| viêm | B-DISEASESYMTOM |
| loét | I-DISEASESYMTOM |
| dạ | B-ORGAN |
| dày | I-ORGAN |

## VM600-133 — dòng train 1120 (đếm từ 0)

cân quá nhanh và quá nhiều trong một khoảng thời gian rất ngắn và điều này không những gây nguy hại cho sức khỏe mà

| Token | Nhãn gốc |
|---|---|
| cân | 0 |
| quá | 0 |
| nhanh | 0 |
| và | 0 |
| quá | 0 |
| nhiều | 0 |
| trong | 0 |
| một | B-DATETIME |
| khoảng | I-DATETIME |
| thời | I-DATETIME |
| gian | I-DATETIME |
| rất | 0 |
| ngắn | 0 |
| và | 0 |
| điều | 0 |
| này | 0 |
| không | 0 |
| những | 0 |
| gây | 0 |
| nguy | 0 |
| hại | 0 |
| cho | 0 |
| sức | 0 |
| khỏe | 0 |
| mà | 0 |

## VM600-134 — dòng train 1127 (đếm từ 0)

thì hầu như cũng đồng nghĩa với việc duy trì được các chức năng bình thường của cơ thể và vấn đề thứ tư đó là dinh dưỡng

| Token | Nhãn gốc |
|---|---|
| thì | 0 |
| hầu | 0 |
| như | 0 |
| cũng | 0 |
| đồng | 0 |
| nghĩa | 0 |
| với | 0 |
| việc | 0 |
| duy | B-PERSONALCARE |
| trì | I-PERSONALCARE |
| được | 0 |
| các | 0 |
| chức | 0 |
| năng | 0 |
| bình | 0 |
| thường | 0 |
| của | 0 |
| cơ | B-ORGAN |
| thể | I-ORGAN |
| và | 0 |
| vấn | 0 |
| đề | 0 |
| thứ | B-DATETIME |
| tư | I-DATETIME |
| đó | 0 |
| là | 0 |
| dinh | 0 |
| dưỡng | 0 |

## VM600-135 — dòng train 1131 (đếm từ 0)

cũng có một cái điều là cái hình thức về rối loạn điện học đó nó cũng tương đồng với cái hoạt động về cơ học của tâm nhĩ

| Token | Nhãn gốc |
|---|---|
| cũng | 0 |
| có | 0 |
| một | 0 |
| cái | 0 |
| điều | 0 |
| là | 0 |
| cái | 0 |
| hình | 0 |
| thức | 0 |
| về | 0 |
| rối | B-DISEASESYMTOM |
| loạn | I-DISEASESYMTOM |
| điện | I-DISEASESYMTOM |
| học | I-DISEASESYMTOM |
| đó | 0 |
| nó | 0 |
| cũng | 0 |
| tương | 0 |
| đồng | 0 |
| với | 0 |
| cái | 0 |
| hoạt | 0 |
| động | 0 |
| về | 0 |
| cơ | 0 |
| học | 0 |
| của | 0 |
| tâm | B-ORGAN |
| nhĩ | I-ORGAN |

## VM600-136 — dòng train 1137 (đếm từ 0)

về tim là rất cần thiết bên cạnh đó một cái chế độ sinh hoạt khoa học như là tránh căng thẳng stress ngủ nghỉ đúng

| Token | Nhãn gốc |
|---|---|
| về | 0 |
| tim | B-ORGAN |
| là | 0 |
| rất | 0 |
| cần | 0 |
| thiết | 0 |
| bên | 0 |
| cạnh | 0 |
| đó | 0 |
| một | 0 |
| cái | 0 |
| chế | B-PERSONALCARE |
| độ | I-PERSONALCARE |
| sinh | I-PERSONALCARE |
| hoạt | I-PERSONALCARE |
| khoa | I-PERSONALCARE |
| học | I-PERSONALCARE |
| như | 0 |
| là | 0 |
| tránh | 0 |
| căng | B-DISEASESYMTOM |
| thẳng | I-DISEASESYMTOM |
| stress | B-DISEASESYMTOM |
| ngủ | B-PERSONALCARE |
| nghỉ | I-PERSONALCARE |
| đúng | 0 |

## VM600-137 — dòng train 1144 (đếm từ 0)

đình mà có béo phì thì họ cũng khuyên bệnh nhân đến khám và điều trị chuyên khoa tuy nhiên thì thường là nhận được

| Token | Nhãn gốc |
|---|---|
| đình | 0 |
| mà | 0 |
| có | 0 |
| béo | B-DISEASESYMTOM |
| phì | I-DISEASESYMTOM |
| thì | 0 |
| họ | 0 |
| cũng | 0 |
| khuyên | 0 |
| bệnh | B-OCCUPATION |
| nhân | I-OCCUPATION |
| đến | 0 |
| khám | B-DIAGNOSTICS |
| và | 0 |
| điều | B-TREATMENT |
| trị | I-TREATMENT |
| chuyên | B-LOCATION |
| khoa | I-LOCATION |
| tuy | 0 |
| nhiên | 0 |
| thì | 0 |
| thường | 0 |
| là | 0 |
| nhận | 0 |
| được | 0 |

## VM600-138 — dòng train 1145 (đếm từ 0)

một loại mầm bệnh cụ thể đã nhân lên và tồn tại trong cơ thể trong một thời gian dài rất lâu sau khi mầm bệnh này đã bị

| Token | Nhãn gốc |
|---|---|
| một | 0 |
| loại | 0 |
| mầm | B-DISEASESYMTOM |
| bệnh | I-DISEASESYMTOM |
| cụ | 0 |
| thể | 0 |
| đã | 0 |
| nhân | 0 |
| lên | 0 |
| và | 0 |
| tồn | 0 |
| tại | 0 |
| trong | 0 |
| cơ | B-ORGAN |
| thể | I-ORGAN |
| trong | 0 |
| một | 0 |
| thời | B-DATETIME |
| gian | I-DATETIME |
| dài | 0 |
| rất | 0 |
| lâu | 0 |
| sau | 0 |
| khi | 0 |
| mầm | B-DISEASESYMTOM |
| bệnh | I-DISEASESYMTOM |
| này | 0 |
| đã | 0 |
| bị | 0 |

## VM600-139 — dòng train 1158 (đếm từ 0)

trắng nè từ hoa lan hoặc từ cam thảo hoặc là gần đây là có những cái sản phẩm mà có chứa chiết xuất từ thực vật

| Token | Nhãn gốc |
|---|---|
| trắng | 0 |
| nè | 0 |
| từ | 0 |
| hoa | B-DRUGCHEMICAL |
| lan | I-DRUGCHEMICAL |
| hoặc | 0 |
| từ | 0 |
| cam | B-DRUGCHEMICAL |
| thảo | I-DRUGCHEMICAL |
| hoặc | 0 |
| là | 0 |
| gần | B-DATETIME |
| đây | I-DATETIME |
| là | 0 |
| có | 0 |
| những | 0 |
| cái | 0 |
| sản | 0 |
| phẩm | 0 |
| mà | 0 |
| có | 0 |
| chứa | 0 |
| chiết | B-DRUGCHEMICAL |
| xuất | I-DRUGCHEMICAL |
| từ | I-DRUGCHEMICAL |
| thực | I-DRUGCHEMICAL |
| vật | I-DRUGCHEMICAL |

## VM600-140 — dòng train 1172 (đếm từ 0)

là rối loạn mỡ máu đúng không bác thế và bác cũng có hỏi là cái số cái số hát cái

| Token | Nhãn gốc |
|---|---|
| là | 0 |
| rối | B-DISEASESYMTOM |
| loạn | I-DISEASESYMTOM |
| mỡ | I-DISEASESYMTOM |
| máu | I-DISEASESYMTOM |
| đúng | 0 |
| không | 0 |
| bác | B-AGE |
| thế | 0 |
| và | 0 |
| bác | B-AGE |
| cũng | 0 |
| có | 0 |
| hỏi | 0 |
| là | 0 |
| cái | 0 |
| số | 0 |
| cái | 0 |
| số | 0 |
| hát | 0 |
| cái | 0 |

## VM600-141 — dòng train 1173 (đếm từ 0)

đồng hồ là nó không còn trong người mình nữa rồi như vậy khi mà chúng ta ngưng thuốc hai ngày đối với noark hoặc là bốn năm

| Token | Nhãn gốc |
|---|---|
| đồng | 0 |
| hồ | 0 |
| là | 0 |
| nó | 0 |
| không | 0 |
| còn | 0 |
| trong | 0 |
| người | 0 |
| mình | 0 |
| nữa | 0 |
| rồi | 0 |
| như | 0 |
| vậy | 0 |
| khi | 0 |
| mà | 0 |
| chúng | 0 |
| ta | 0 |
| ngưng | B-MEDDEVICETECHNIQUE |
| thuốc | I-MEDDEVICETECHNIQUE |
| hai | B-DATETIME |
| ngày | I-DATETIME |
| đối | 0 |
| với | 0 |
| noark | B-DRUGCHEMICAL |
| hoặc | 0 |
| là | 0 |
| bốn | B-DATETIME |
| năm | I-DATETIME |

## VM600-142 — dòng train 1174 (đếm từ 0)

mạch máu của chúng ta lưu thông ở mức độ nó rất là ít và đã chậm bản thân các cái khớp của chúng ta nó thông thường là

| Token | Nhãn gốc |
|---|---|
| mạch | B-ORGAN |
| máu | I-ORGAN |
| của | 0 |
| chúng | 0 |
| ta | 0 |
| lưu | 0 |
| thông | 0 |
| ở | 0 |
| mức | B-UNITCALIBRATOR |
| độ | I-UNITCALIBRATOR |
| nó | 0 |
| rất | 0 |
| là | 0 |
| ít | 0 |
| và | 0 |
| đã | 0 |
| chậm | B-DISEASESYMTOM |
| bản | 0 |
| thân | 0 |
| các | B-ORGAN |
| cái | I-ORGAN |
| khớp | I-ORGAN |
| của | 0 |
| chúng | 0 |
| ta | 0 |
| nó | 0 |
| thông | 0 |
| thường | 0 |
| là | 0 |

## VM600-143 — dòng train 1176 (đếm từ 0)

ứng đầu tiên của cơ thể đổi lại vi khuẩn đường ruột giúp giữ cho hệ miễn dịch

| Token | Nhãn gốc |
|---|---|
| ứng | 0 |
| đầu | 0 |
| tiên | 0 |
| của | 0 |
| cơ | B-ORGAN |
| thể | I-ORGAN |
| đổi | 0 |
| lại | 0 |
| vi | B-DISEASESYMTOM |
| khuẩn | I-DISEASESYMTOM |
| đường | B-ORGAN |
| ruột | I-ORGAN |
| giúp | 0 |
| giữ | 0 |
| cho | 0 |
| hệ | B-ORGAN |
| miễn | I-ORGAN |
| dịch | I-ORGAN |

## VM600-144 — dòng train 1178 (đếm từ 0)

đề án thuộc chương trình quốc gia vào thế và đối với sản phẩm này thì nó gồm

| Token | Nhãn gốc |
|---|---|
| đề | 0 |
| án | 0 |
| thuộc | 0 |
| chương | 0 |
| trình | 0 |
| quốc | B-LOCATION |
| gia | I-LOCATION |
| vào | 0 |
| thế | 0 |
| và | 0 |
| đối | 0 |
| với | 0 |
| sản | 0 |
| phẩm | 0 |
| này | 0 |
| thì | 0 |
| nó | 0 |
| gồm | 0 |

## VM600-145 — dòng train 1181 (đếm từ 0)

có khả năng là nó trầm cảm và cái tâm lý mà họ bị kỳ thị bản thân họ bị tự ti họ

| Token | Nhãn gốc |
|---|---|
| có | 0 |
| khả | 0 |
| năng | 0 |
| là | 0 |
| nó | 0 |
| trầm | B-DISEASESYMTOM |
| cảm | I-DISEASESYMTOM |
| và | 0 |
| cái | 0 |
| tâm | 0 |
| lý | 0 |
| mà | 0 |
| họ | 0 |
| bị | 0 |
| kỳ | 0 |
| thị | 0 |
| bản | 0 |
| thân | 0 |
| họ | 0 |
| bị | 0 |
| tự | B-DISEASESYMTOM |
| ti | I-DISEASESYMTOM |
| họ | 0 |

## VM600-146 — dòng train 1184 (đếm từ 0)

chúng ta cho dầu là dầu mà chúng ta cho vào cuối bữa ăn để mà cũng không

| Token | Nhãn gốc |
|---|---|
| chúng | 0 |
| ta | 0 |
| cho | 0 |
| dầu | 0 |
| là | 0 |
| dầu | 0 |
| mà | 0 |
| chúng | 0 |
| ta | 0 |
| cho | 0 |
| vào | 0 |
| cuối | 0 |
| bữa | 0 |
| ăn | 0 |
| để | 0 |
| mà | 0 |
| cũng | 0 |
| không | 0 |

## VM600-147 — dòng train 1195 (đếm từ 0)

nó cũng sẽ làm cho hạn chế dòng máu đi đến cái mạch vành đó và dẫn đến những cái tình trạng thiểu năng vành và khi

| Token | Nhãn gốc |
|---|---|
| nó | 0 |
| cũng | 0 |
| sẽ | 0 |
| làm | 0 |
| cho | 0 |
| hạn | 0 |
| chế | 0 |
| dòng | B-ORGAN |
| máu | I-ORGAN |
| đi | 0 |
| đến | 0 |
| cái | 0 |
| mạch | B-ORGAN |
| vành | 0 |
| đó | 0 |
| và | 0 |
| dẫn | 0 |
| đến | 0 |
| những | 0 |
| cái | 0 |
| tình | 0 |
| trạng | 0 |
| thiểu | B-DISEASESYMTOM |
| năng | I-DISEASESYMTOM |
| vành | I-DISEASESYMTOM |
| và | 0 |
| khi | 0 |

## VM600-148 — dòng train 1201 (đếm từ 0)

ạ chúng ta phải phòng ngừa cho những cái chuyện đó xảy ra giống như lúc nãy tôi nói rằng là đi xe đạp về rất tốt nhưng

| Token | Nhãn gốc |
|---|---|
| ạ | 0 |
| chúng | 0 |
| ta | 0 |
| phải | 0 |
| phòng | B-PREVENTIVEMED |
| ngừa | I-PREVENTIVEMED |
| cho | 0 |
| những | 0 |
| cái | 0 |
| chuyện | 0 |
| đó | 0 |
| xảy | 0 |
| ra | 0 |
| giống | 0 |
| như | 0 |
| lúc | 0 |
| nãy | 0 |
| tôi | 0 |
| nói | 0 |
| rằng | 0 |
| là | 0 |
| đi | 0 |
| xe | B-TRANSPORTATION |
| đạp | I-TRANSPORTATION |
| về | 0 |
| rất | 0 |
| tốt | 0 |
| nhưng | 0 |

## VM600-149 — dòng train 1208 (đếm từ 0)

cô không có nêu các bệnh nền nhưng mà cô lại nói là cái bệnh của cô là phải uống thuốc định kỳ hàng tháng nhưng mà do

| Token | Nhãn gốc |
|---|---|
| cô | B-GENDER |
| không | 0 |
| có | 0 |
| nêu | 0 |
| các | 0 |
| bệnh | B-DISEASESYMTOM |
| nền | I-DISEASESYMTOM |
| nhưng | 0 |
| mà | 0 |
| cô | B-GENDER |
| lại | 0 |
| nói | 0 |
| là | 0 |
| cái | 0 |
| bệnh | 0 |
| của | 0 |
| cô | B-GENDER |
| là | 0 |
| phải | 0 |
| uống | B-TREATMENT |
| thuốc | I-TREATMENT |
| định | B-DATETIME |
| kỳ | I-DATETIME |
| hàng | B-DATETIME |
| tháng | I-DATETIME |
| nhưng | 0 |
| mà | 0 |
| do | 0 |

## VM600-150 — dòng train 1219 (đếm từ 0)

chúng ta muốn tìm mua đông trùng hạ thảo hoặc là những sản phẩm có đông trùng hạ

| Token | Nhãn gốc |
|---|---|
| chúng | 0 |
| ta | 0 |
| muốn | 0 |
| tìm | 0 |
| mua | 0 |
| đông | B-DRUGCHEMICAL |
| trùng | I-DRUGCHEMICAL |
| hạ | I-DRUGCHEMICAL |
| thảo | I-DRUGCHEMICAL |
| hoặc | 0 |
| là | 0 |
| những | 0 |
| sản | 0 |
| phẩm | 0 |
| có | 0 |
| đông | B-FOODDRINK |
| trùng | I-FOODDRINK |
| hạ | 0 |

## VM600-151 — dòng train 1236 (đếm từ 0)

là tránh được cái biến cố bị đột quỵ do tình trạng rung nhĩ gây ra như vậy là

| Token | Nhãn gốc |
|---|---|
| là | 0 |
| tránh | 0 |
| được | 0 |
| cái | 0 |
| biến | 0 |
| cố | 0 |
| bị | 0 |
| đột | B-DISEASESYMTOM |
| quỵ | I-DISEASESYMTOM |
| do | 0 |
| tình | 0 |
| trạng | 0 |
| rung | B-DISEASESYMTOM |
| nhĩ | I-DISEASESYMTOM |
| gây | 0 |
| ra | 0 |
| như | 0 |
| vậy | 0 |
| là | 0 |

## VM600-152 — dòng train 1244 (đếm từ 0)

để giúp cho quý vị và các bạn những ai mà đang gặp phải cái triệu chứng như là huyết áp cao nè mỡ máu cao nè tê bì

| Token | Nhãn gốc |
|---|---|
| để | 0 |
| giúp | 0 |
| cho | 0 |
| quý | 0 |
| vị | 0 |
| và | 0 |
| các | 0 |
| bạn | 0 |
| những | 0 |
| ai | 0 |
| mà | 0 |
| đang | 0 |
| gặp | 0 |
| phải | 0 |
| cái | 0 |
| triệu | B-DISEASESYMTOM |
| chứng | I-DISEASESYMTOM |
| như | 0 |
| là | 0 |
| huyết | B-DISEASESYMTOM |
| áp | I-DISEASESYMTOM |
| cao | B-UNITCALIBRATOR |
| nè | 0 |
| mỡ | B-DISEASESYMTOM |
| máu | I-DISEASESYMTOM |
| cao | B-UNITCALIBRATOR |
| nè | 0 |
| tê | B-DISEASESYMTOM |
| bì | I-DISEASESYMTOM |

## VM600-153 — dòng train 1255 (đếm từ 0)

người huyết áp cao mỡ máu cao tim mạch hỗ trợ giảm nguy cơ xơ vữa động mạch hỗ trợ giảm đau đầu chóng mặt mất ngủ tê bì

| Token | Nhãn gốc |
|---|---|
| người | 0 |
| huyết | B-DISEASESYMTOM |
| áp | I-DISEASESYMTOM |
| cao | B-UNITCALIBRATOR |
| mỡ | B-DISEASESYMTOM |
| máu | I-DISEASESYMTOM |
| cao | B-UNITCALIBRATOR |
| tim | B-ORGAN |
| mạch | I-ORGAN |
| hỗ | B-MEDDEVICETECHNIQUE |
| trợ | I-MEDDEVICETECHNIQUE |
| giảm | 0 |
| nguy | 0 |
| cơ | 0 |
| xơ | B-DISEASESYMTOM |
| vữa | I-DISEASESYMTOM |
| động | I-DISEASESYMTOM |
| mạch | I-DISEASESYMTOM |
| hỗ | B-MEDDEVICETECHNIQUE |
| trợ | I-MEDDEVICETECHNIQUE |
| giảm | 0 |
| đau | B-DISEASESYMTOM |
| đầu | I-DISEASESYMTOM |
| chóng | B-DISEASESYMTOM |
| mặt | I-DISEASESYMTOM |
| mất | B-DISEASESYMTOM |
| ngủ | I-DISEASESYMTOM |
| tê | B-DISEASESYMTOM |
| bì | I-DISEASESYMTOM |

## VM600-154 — dòng train 1270 (đếm từ 0)

sĩ nội và bác sĩ ngoại thần kinh sẽ làm một cái chương trình là lấy cái hình ảnh mri của ngày trước mổ đó mình sẽ

| Token | Nhãn gốc |
|---|---|
| sĩ | 0 |
| nội | 0 |
| và | 0 |
| bác | B-OCCUPATION |
| sĩ | I-OCCUPATION |
| ngoại | 0 |
| thần | B-ORGAN |
| kinh | I-ORGAN |
| sẽ | 0 |
| làm | 0 |
| một | 0 |
| cái | 0 |
| chương | 0 |
| trình | 0 |
| là | 0 |
| lấy | 0 |
| cái | 0 |
| hình | 0 |
| ảnh | 0 |
| mri | B-DIAGNOSTICS |
| của | 0 |
| ngày | 0 |
| trước | 0 |
| mổ | B-SURGERY |
| đó | 0 |
| mình | 0 |
| sẽ | 0 |

## VM600-155 — dòng train 1273 (đếm từ 0)

cái thông tin họ được chưa đầy đủ làm cho nhận thức của họ nó chưa được sâu sắc thì họ sẽ chưa có đủ niềm tin

| Token | Nhãn gốc |
|---|---|
| cái | 0 |
| thông | 0 |
| tin | 0 |
| họ | 0 |
| được | 0 |
| chưa | 0 |
| đầy | 0 |
| đủ | 0 |
| làm | 0 |
| cho | 0 |
| nhận | 0 |
| thức | 0 |
| của | 0 |
| họ | 0 |
| nó | 0 |
| chưa | 0 |
| được | 0 |
| sâu | 0 |
| sắc | 0 |
| thì | 0 |
| họ | 0 |
| sẽ | 0 |
| chưa | 0 |
| có | 0 |
| đủ | 0 |
| niềm | 0 |
| tin | 0 |

## VM600-156 — dòng train 1279 (đếm từ 0)

vitamin k những loại thức ăn nào mà chứa ít vitamin k thì chúng ta sẽ biết được và chúng ta không nên ăn quá nhiều loại đó

| Token | Nhãn gốc |
|---|---|
| vitamin | B-DRUGCHEMICAL |
| k | I-DRUGCHEMICAL |
| những | 0 |
| loại | 0 |
| thức | B-FOODDRINK |
| ăn | I-FOODDRINK |
| nào | 0 |
| mà | 0 |
| chứa | 0 |
| ít | 0 |
| vitamin | B-DRUGCHEMICAL |
| k | I-DRUGCHEMICAL |
| thì | 0 |
| chúng | 0 |
| ta | 0 |
| sẽ | 0 |
| biết | 0 |
| được | 0 |
| và | 0 |
| chúng | 0 |
| ta | 0 |
| không | 0 |
| nên | 0 |
| ăn | 0 |
| quá | 0 |
| nhiều | 0 |
| loại | 0 |
| đó | 0 |

## VM600-157 — dòng train 1281 (đếm từ 0)

nên nó có thể giết cả các cái tế bào lành và chính vì vậy làm cho các chức năng của cơ quan bị tổn thương và đặc

| Token | Nhãn gốc |
|---|---|
| nên | 0 |
| nó | 0 |
| có | 0 |
| thể | 0 |
| giết | 0 |
| cả | 0 |
| các | 0 |
| cái | 0 |
| tế | B-ORGAN |
| bào | I-ORGAN |
| lành | 0 |
| và | 0 |
| chính | 0 |
| vì | 0 |
| vậy | 0 |
| làm | 0 |
| cho | 0 |
| các | 0 |
| chức | 0 |
| năng | 0 |
| của | 0 |
| cơ | 0 |
| quan | 0 |
| bị | B-DISEASESYMTOM |
| tổn | B-DISEASESYMTOM |
| thương | I-DISEASESYMTOM |
| và | 0 |
| đặc | 0 |

## VM600-158 — dòng train 1284 (đếm từ 0)

chế độ ăn uống và sinh hoạt nó lành mạnh giúp cho việc nâng cao hiệu quả tuân thủ

| Token | Nhãn gốc |
|---|---|
| chế | B-PERSONALCARE |
| độ | I-PERSONALCARE |
| ăn | B-PERSONALCARE |
| uống | I-PERSONALCARE |
| và | 0 |
| sinh | 0 |
| hoạt | 0 |
| nó | 0 |
| lành | 0 |
| mạnh | 0 |
| giúp | 0 |
| cho | 0 |
| việc | 0 |
| nâng | 0 |
| cao | B-UNITCALIBRATOR |
| hiệu | 0 |
| quả | 0 |
| tuân | B-PREVENTIVEMED |
| thủ | I-PREVENTIVEMED |

## VM600-159 — dòng train 1295 (đếm từ 0)

a nếu có được vitamina a nữa thì càng tốt này có selen có kẽm như là chúng ta vừa chia sẻ về cái hai cái chất mà chống oxy hóa

| Token | Nhãn gốc |
|---|---|
| a | 0 |
| nếu | 0 |
| có | 0 |
| được | 0 |
| vitamina | 0 |
| a | 0 |
| nữa | 0 |
| thì | 0 |
| càng | 0 |
| tốt | 0 |
| này | 0 |
| có | 0 |
| selen | B-DRUGCHEMICAL |
| có | 0 |
| kẽm | B-DRUGCHEMICAL |
| như | 0 |
| là | 0 |
| chúng | 0 |
| ta | 0 |
| vừa | 0 |
| chia | 0 |
| sẻ | 0 |
| về | 0 |
| cái | 0 |
| hai | 0 |
| cái | 0 |
| chất | 0 |
| mà | 0 |
| chống | 0 |
| oxy | B-DRUGCHEMICAL |
| hóa | 0 |

## VM600-160 — dòng train 1314 (đếm từ 0)

thành phần như immunesoyz này hòe hoa này l-carnitine fumarate để hoàng liên này với cả đan sâm nữa thì rất tốt

| Token | Nhãn gốc |
|---|---|
| thành | 0 |
| phần | 0 |
| như | 0 |
| immunesoyz | B-DRUGCHEMICAL |
| này | 0 |
| hòe | B-DRUGCHEMICAL |
| hoa | I-DRUGCHEMICAL |
| này | 0 |
| l-carnitine | B-DRUGCHEMICAL |
| fumarate | B-DRUGCHEMICAL |
| để | 0 |
| hoàng | B-DRUGCHEMICAL |
| liên | I-DRUGCHEMICAL |
| này | 0 |
| với | 0 |
| cả | 0 |
| đan | B-DRUGCHEMICAL |
| sâm | I-DRUGCHEMICAL |
| nữa | 0 |
| thì | 0 |
| rất | 0 |
| tốt | 0 |

## VM600-161 — dòng train 1315 (đếm từ 0)

khác nhau như thế nào giữa các quần thể trên khắp thế giới và sự khác nhau này gây ra bởi sự khác biệt trong chế độ ăn

| Token | Nhãn gốc |
|---|---|
| khác | 0 |
| nhau | 0 |
| như | 0 |
| thế | 0 |
| nào | 0 |
| giữa | 0 |
| các | 0 |
| quần | 0 |
| thể | 0 |
| trên | 0 |
| khắp | 0 |
| thế | B-LOCATION |
| giới | I-LOCATION |
| và | 0 |
| sự | 0 |
| khác | 0 |
| nhau | 0 |
| này | 0 |
| gây | 0 |
| ra | 0 |
| bởi | 0 |
| sự | 0 |
| khác | 0 |
| biệt | 0 |
| trong | 0 |
| chế | B-PERSONALCARE |
| độ | I-PERSONALCARE |
| ăn | I-PERSONALCARE |

## VM600-162 — dòng train 1344 (đếm từ 0)

hợp này đó chính là tế bào ung thư thì đó sẽ sử dụng các cái chất dinh dưỡng dự trữ

| Token | Nhãn gốc |
|---|---|
| hợp | 0 |
| này | 0 |
| đó | 0 |
| chính | 0 |
| là | 0 |
| tế | B-DISEASESYMTOM |
| bào | I-DISEASESYMTOM |
| ung | I-DISEASESYMTOM |
| thư | I-DISEASESYMTOM |
| thì | 0 |
| đó | 0 |
| sẽ | 0 |
| sử | 0 |
| dụng | 0 |
| các | 0 |
| cái | 0 |
| chất | B-DRUGCHEMICAL |
| dinh | I-DRUGCHEMICAL |
| dưỡng | I-DRUGCHEMICAL |
| dự | 0 |
| trữ | 0 |

## VM600-163 — dòng train 1351 (đếm từ 0)

tử vong đó rất là nhanh trong vòng mười

| Token | Nhãn gốc |
|---|---|
| tử | B-DISEASESYMTOM |
| vong | I-DISEASESYMTOM |
| đó | 0 |
| rất | 0 |
| là | 0 |
| nhanh | 0 |
| trong | B-DATETIME |
| vòng | I-DATETIME |
| mười | 0 |

## VM600-164 — dòng train 1356 (đếm từ 0)

biệt là mỡ động vật thế và chúng ta cũng nên tăng cường rau xanh hoa quả tươi để cung cấp các vitamin các khoáng chất và

| Token | Nhãn gốc |
|---|---|
| biệt | 0 |
| là | 0 |
| mỡ | B-FOODDRINK |
| động | I-FOODDRINK |
| vật | I-FOODDRINK |
| thế | 0 |
| và | 0 |
| chúng | 0 |
| ta | 0 |
| cũng | 0 |
| nên | 0 |
| tăng | 0 |
| cường | 0 |
| rau | B-FOODDRINK |
| xanh | I-FOODDRINK |
| hoa | B-FOODDRINK |
| quả | I-FOODDRINK |
| tươi | I-FOODDRINK |
| để | 0 |
| cung | 0 |
| cấp | 0 |
| các | 0 |
| vitamin | B-DRUGCHEMICAL |
| các | 0 |
| khoáng | B-DRUGCHEMICAL |
| chất | I-DRUGCHEMICAL |
| và | 0 |

## VM600-165 — dòng train 1357 (đếm từ 0)

đến mình đau đầu rồi hoa mắt chóng mặt này ở kia ở mạch vành hay là ở tim

| Token | Nhãn gốc |
|---|---|
| đến | 0 |
| mình | 0 |
| đau | B-DISEASESYMTOM |
| đầu | I-DISEASESYMTOM |
| rồi | 0 |
| hoa | B-DISEASESYMTOM |
| mắt | I-DISEASESYMTOM |
| chóng | B-DISEASESYMTOM |
| mặt | I-DISEASESYMTOM |
| này | 0 |
| ở | 0 |
| kia | 0 |
| ở | 0 |
| mạch | B-ORGAN |
| vành | 0 |
| hay | 0 |
| là | 0 |
| ở | 0 |
| tim | B-ORGAN |

## VM600-166 — dòng train 1363 (đếm từ 0)

được hay không thì từ hồi đó nay sức khỏe của ông mới mổ cho nên là tôi và

| Token | Nhãn gốc |
|---|---|
| được | 0 |
| hay | 0 |
| không | 0 |
| thì | 0 |
| từ | 0 |
| hồi | 0 |
| đó | 0 |
| nay | 0 |
| sức | 0 |
| khỏe | 0 |
| của | 0 |
| ông | B-GENDER |
| mới | 0 |
| mổ | B-SURGERY |
| cho | 0 |
| nên | 0 |
| là | 0 |
| tôi | 0 |
| và | 0 |

## VM600-167 — dòng train 1364 (đếm từ 0)

cái xơ vữa xơ vữa động mạch chi thì có thể bệnh nhân có cảm nhận như là các cái tê bì kiến bò châm chích bằng tay bằng

| Token | Nhãn gốc |
|---|---|
| cái | 0 |
| xơ | B-DISEASESYMTOM |
| vữa | I-DISEASESYMTOM |
| xơ | B-DISEASESYMTOM |
| vữa | I-DISEASESYMTOM |
| động | I-DISEASESYMTOM |
| mạch | I-DISEASESYMTOM |
| chi | I-DISEASESYMTOM |
| thì | 0 |
| có | 0 |
| thể | 0 |
| bệnh | B-OCCUPATION |
| nhân | I-OCCUPATION |
| có | 0 |
| cảm | 0 |
| nhận | 0 |
| như | 0 |
| là | 0 |
| các | 0 |
| cái | 0 |
| tê | B-DISEASESYMTOM |
| bì | I-DISEASESYMTOM |
| kiến | I-DISEASESYMTOM |
| bò | I-DISEASESYMTOM |
| châm | B-DISEASESYMTOM |
| chích | I-DISEASESYMTOM |
| bằng | 0 |
| tay | 0 |
| bằng | 0 |

## VM600-168 — dòng train 1383 (đếm từ 0)

tác trực tiếp nên trong quá trình mà các bác sĩ trao đổi với những nội dung hấp dẫn và thú vị thì quý vị có bất kỳ những

| Token | Nhãn gốc |
|---|---|
| tác | 0 |
| trực | 0 |
| tiếp | 0 |
| nên | 0 |
| trong | 0 |
| quá | 0 |
| trình | 0 |
| mà | 0 |
| các | 0 |
| bác | B-OCCUPATION |
| sĩ | I-OCCUPATION |
| trao | 0 |
| đổi | 0 |
| với | 0 |
| những | 0 |
| nội | 0 |
| dung | 0 |
| hấp | 0 |
| dẫn | 0 |
| và | 0 |
| thú | 0 |
| vị | 0 |
| thì | 0 |
| quý | 0 |
| vị | 0 |
| có | 0 |
| bất | 0 |
| kỳ | 0 |
| những | 0 |

## VM600-169 — dòng train 1407 (đếm từ 0)

một tình trạng rung nhĩ thì tim của chúng ta sẽ đập và rất là nhanh có thể

| Token | Nhãn gốc |
|---|---|
| một | 0 |
| tình | 0 |
| trạng | 0 |
| rung | B-DISEASESYMTOM |
| nhĩ | I-DISEASESYMTOM |
| thì | 0 |
| tim | B-ORGAN |
| của | 0 |
| chúng | 0 |
| ta | 0 |
| sẽ | 0 |
| đập | 0 |
| và | 0 |
| rất | 0 |
| là | 0 |
| nhanh | 0 |
| có | 0 |
| thể | 0 |

## VM600-170 — dòng train 1419 (đếm từ 0)

bị nhồi máu cơ tim cũng rất là cao nếu mà chúng ta vẫn không có một cái chế độ ở sinh hoạt điều trị một cách khoa học

| Token | Nhãn gốc |
|---|---|
| bị | 0 |
| nhồi | B-DISEASESYMTOM |
| máu | I-DISEASESYMTOM |
| cơ | I-DISEASESYMTOM |
| tim | I-DISEASESYMTOM |
| cũng | 0 |
| rất | 0 |
| là | 0 |
| cao | B-UNITCALIBRATOR |
| nếu | 0 |
| mà | 0 |
| chúng | 0 |
| ta | 0 |
| vẫn | 0 |
| không | 0 |
| có | 0 |
| một | 0 |
| cái | 0 |
| chế | 0 |
| độ | 0 |
| ở | 0 |
| sinh | 0 |
| hoạt | 0 |
| điều | B-TREATMENT |
| trị | I-TREATMENT |
| một | 0 |
| cách | 0 |
| khoa | 0 |
| học | 0 |

## VM600-171 — dòng train 1430 (đếm từ 0)

mạch vành huyết áp cao nhiều khi nhớ nhớ quên quên bị tiền đình đau đầu chóng mặt và đã từng dùng rất là nhiều sản phẩm

| Token | Nhãn gốc |
|---|---|
| mạch | B-ORGAN |
| vành | 0 |
| huyết | B-DISEASESYMTOM |
| áp | I-DISEASESYMTOM |
| cao | B-UNITCALIBRATOR |
| nhiều | 0 |
| khi | 0 |
| nhớ | B-DISEASESYMTOM |
| nhớ | I-DISEASESYMTOM |
| quên | I-DISEASESYMTOM |
| quên | I-DISEASESYMTOM |
| bị | 0 |
| tiền | B-DISEASESYMTOM |
| đình | I-DISEASESYMTOM |
| đau | B-DISEASESYMTOM |
| đầu | I-DISEASESYMTOM |
| chóng | B-DISEASESYMTOM |
| mặt | I-DISEASESYMTOM |
| và | 0 |
| đã | 0 |
| từng | 0 |
| dùng | 0 |
| rất | 0 |
| là | 0 |
| nhiều | 0 |
| sản | 0 |
| phẩm | 0 |

## VM600-172 — dòng train 1450 (đếm từ 0)

lớn tuổi thì cái cái nguy cơ đột quỵ là sẽ rõ ràng là sẽ tăng lên và như vậy

| Token | Nhãn gốc |
|---|---|
| lớn | B-AGE |
| tuổi | I-AGE |
| thì | 0 |
| cái | 0 |
| cái | 0 |
| nguy | 0 |
| cơ | 0 |
| đột | B-DISEASESYMTOM |
| quỵ | I-DISEASESYMTOM |
| là | 0 |
| sẽ | 0 |
| rõ | 0 |
| ràng | 0 |
| là | 0 |
| sẽ | 0 |
| tăng | 0 |
| lên | 0 |
| và | 0 |
| như | 0 |
| vậy | 0 |

## VM600-173 — dòng train 1466 (đếm từ 0)

nó huyết áp nó tăng cao vì khi chúng ta biết càng huyết áp tăng cao vâng nó càng bị bị dễ bị tai biến chị nhé các cái

| Token | Nhãn gốc |
|---|---|
| nó | 0 |
| huyết | B-DISEASESYMTOM |
| áp | I-DISEASESYMTOM |
| nó | 0 |
| tăng | 0 |
| cao | B-UNITCALIBRATOR |
| vì | 0 |
| khi | 0 |
| chúng | 0 |
| ta | 0 |
| biết | 0 |
| càng | 0 |
| huyết | B-DISEASESYMTOM |
| áp | I-DISEASESYMTOM |
| tăng | 0 |
| cao | B-UNITCALIBRATOR |
| vâng | 0 |
| nó | 0 |
| càng | 0 |
| bị | 0 |
| bị | 0 |
| dễ | 0 |
| bị | 0 |
| tai | B-DISEASESYMTOM |
| biến | I-DISEASESYMTOM |
| chị | B-GENDER |
| nhé | 0 |
| các | 0 |
| cái | 0 |

## VM600-174 — dòng train 1474 (đếm từ 0)

căn bệnh béo phì cũng như là lợi ích của việc điều trị giảm cân một cách an toàn thưa quý vị hiện nay thì chúng ta nhận

| Token | Nhãn gốc |
|---|---|
| căn | 0 |
| bệnh | 0 |
| béo | B-DISEASESYMTOM |
| phì | I-DISEASESYMTOM |
| cũng | 0 |
| như | 0 |
| là | 0 |
| lợi | 0 |
| ích | 0 |
| của | 0 |
| việc | 0 |
| điều | B-TREATMENT |
| trị | I-TREATMENT |
| giảm | B-PERSONALCARE |
| cân | I-PERSONALCARE |
| một | 0 |
| cách | 0 |
| an | 0 |
| toàn | 0 |
| thưa | 0 |
| quý | 0 |
| vị | 0 |
| hiện | B-DATETIME |
| nay | I-DATETIME |
| thì | 0 |
| chúng | 0 |
| ta | 0 |
| nhận | 0 |

## VM600-175 — dòng train 1481 (đếm từ 0)

quay trở lại với chương trình thì có rất là nhiều của bệnh nhân ung thư băn khoăn

| Token | Nhãn gốc |
|---|---|
| quay | 0 |
| trở | 0 |
| lại | 0 |
| với | 0 |
| chương | 0 |
| trình | 0 |
| thì | 0 |
| có | 0 |
| rất | 0 |
| là | 0 |
| nhiều | 0 |
| của | 0 |
| bệnh | B-OCCUPATION |
| nhân | I-OCCUPATION |
| ung | B-DISEASESYMTOM |
| thư | I-DISEASESYMTOM |
| băn | 0 |
| khoăn | 0 |

## VM600-176 — dòng train 1498 (đếm từ 0)

gan thận nó phải xử lý đào thải hoặc là gọi là chuyển hóa các cái chất này thì nó cũng lại phải chịu gánh nặng cho nên

| Token | Nhãn gốc |
|---|---|
| gan | B-ORGAN |
| thận | B-ORGAN |
| nó | 0 |
| phải | 0 |
| xử | 0 |
| lý | 0 |
| đào | 0 |
| thải | 0 |
| hoặc | 0 |
| là | 0 |
| gọi | 0 |
| là | 0 |
| chuyển | B-DIAGNOSTICS |
| hóa | I-DIAGNOSTICS |
| các | 0 |
| cái | 0 |
| chất | 0 |
| này | 0 |
| thì | 0 |
| nó | 0 |
| cũng | 0 |
| lại | 0 |
| phải | 0 |
| chịu | 0 |
| gánh | 0 |
| nặng | 0 |
| cho | 0 |
| nên | 0 |

## VM600-177 — dòng train 1505 (đếm từ 0)

và bởi vì sao bao giờ khi mà cái vấn đề mà phẫu thuật sọ não hoặc là bất kỳ một cái phẫu thuật nào bao giờ các bác sĩ

| Token | Nhãn gốc |
|---|---|
| và | 0 |
| bởi | 0 |
| vì | 0 |
| sao | 0 |
| bao | 0 |
| giờ | 0 |
| khi | 0 |
| mà | 0 |
| cái | 0 |
| vấn | 0 |
| đề | 0 |
| mà | 0 |
| phẫu | B-SURGERY |
| thuật | I-SURGERY |
| sọ | B-ORGAN |
| não | B-ORGAN |
| hoặc | 0 |
| là | 0 |
| bất | 0 |
| kỳ | 0 |
| một | 0 |
| cái | 0 |
| phẫu | B-SURGERY |
| thuật | I-SURGERY |
| nào | 0 |
| bao | 0 |
| giờ | 0 |
| các | 0 |
| bác | B-OCCUPATION |
| sĩ | I-OCCUPATION |

## VM600-178 — dòng train 1506 (đếm từ 0)

đổi thái độ họ đẩy mà họ có được một cái hành vi tốt hơn

| Token | Nhãn gốc |
|---|---|
| đổi | 0 |
| thái | 0 |
| độ | 0 |
| họ | 0 |
| đẩy | 0 |
| mà | 0 |
| họ | 0 |
| có | 0 |
| được | 0 |
| một | 0 |
| cái | 0 |
| hành | 0 |
| vi | 0 |
| tốt | 0 |
| hơn | 0 |

## VM600-179 — dòng train 1508 (đếm từ 0)

cái mảng vữa xơ và mảng vữa xơ thì chúng ta cứ tưởng tượng nó là những cái mảng bám ví dụ cái ống nước chẳng hạn nó sẽ

| Token | Nhãn gốc |
|---|---|
| cái | 0 |
| mảng | B-ORGAN |
| vữa | I-ORGAN |
| xơ | I-ORGAN |
| và | 0 |
| mảng | B-ORGAN |
| vữa | I-ORGAN |
| xơ | I-ORGAN |
| thì | 0 |
| chúng | 0 |
| ta | 0 |
| cứ | 0 |
| tưởng | 0 |
| tượng | 0 |
| nó | 0 |
| là | 0 |
| những | 0 |
| cái | 0 |
| mảng | 0 |
| bám | 0 |
| ví | 0 |
| dụ | 0 |
| cái | 0 |
| ống | 0 |
| nước | 0 |
| chẳng | 0 |
| hạn | 0 |
| nó | 0 |
| sẽ | 0 |

## VM600-180 — dòng train 1511 (đếm từ 0)

vấn như thế nào đó về sức khỏe bởi vì hiện nay là công nghệ nó rất là rất làm

| Token | Nhãn gốc |
|---|---|
| vấn | 0 |
| như | 0 |
| thế | 0 |
| nào | 0 |
| đó | 0 |
| về | 0 |
| sức | 0 |
| khỏe | 0 |
| bởi | 0 |
| vì | 0 |
| hiện | B-DATETIME |
| nay | I-DATETIME |
| là | 0 |
| công | 0 |
| nghệ | 0 |
| nó | 0 |
| rất | 0 |
| là | 0 |
| rất | 0 |
| làm | 0 |

## VM600-181 — dòng train 1520 (đếm từ 0)

thấy có cái cơ chế tác dụng và có cái hiệu quả nó tương đương với nhau nhưng mà kga1 thì nó lại không gây ra các cái

| Token | Nhãn gốc |
|---|---|
| thấy | 0 |
| có | 0 |
| cái | 0 |
| cơ | 0 |
| chế | 0 |
| tác | 0 |
| dụng | 0 |
| và | 0 |
| có | 0 |
| cái | 0 |
| hiệu | 0 |
| quả | 0 |
| nó | 0 |
| tương | 0 |
| đương | 0 |
| với | 0 |
| nhau | 0 |
| nhưng | 0 |
| mà | 0 |
| kga1 | B-DRUGCHEMICAL |
| thì | 0 |
| nó | 0 |
| lại | 0 |
| không | 0 |
| gây | 0 |
| ra | 0 |
| các | 0 |
| cái | 0 |

## VM600-182 — dòng train 1522 (đếm từ 0)

thể khác để ký sinh vào cụ thể là con người chúng ta và nó được mang đi cũng bởi con người của chúng ta khi mà chúng

| Token | Nhãn gốc |
|---|---|
| thể | 0 |
| khác | 0 |
| để | 0 |
| ký | B-DISEASESYMTOM |
| sinh | I-DISEASESYMTOM |
| vào | 0 |
| cụ | 0 |
| thể | 0 |
| là | 0 |
| con | 0 |
| người | 0 |
| chúng | 0 |
| ta | 0 |
| và | 0 |
| nó | 0 |
| được | 0 |
| mang | 0 |
| đi | 0 |
| cũng | 0 |
| bởi | 0 |
| con | 0 |
| người | 0 |
| của | 0 |
| chúng | 0 |
| ta | 0 |
| khi | 0 |
| mà | 0 |
| chúng | 0 |

## VM600-183 — dòng train 1532 (đếm từ 0)

não sâu để cho nó có hiệu quả hoặc là tốt mà có thể đi làm thì nó đòi hỏi sẽ

| Token | Nhãn gốc |
|---|---|
| não | B-ORGAN |
| sâu | 0 |
| để | 0 |
| cho | 0 |
| nó | 0 |
| có | 0 |
| hiệu | 0 |
| quả | 0 |
| hoặc | 0 |
| là | 0 |
| tốt | 0 |
| mà | 0 |
| có | 0 |
| thể | 0 |
| đi | 0 |
| làm | 0 |
| thì | 0 |
| nó | 0 |
| đòi | 0 |
| hỏi | 0 |
| sẽ | 0 |

## VM600-184 — dòng train 1533 (đếm từ 0)

chúng ta khi mà chưa có tây y đến đất nước chúng ta từ thế kỷ mười bảy mười tám thì cha ông chúng ta điều trị người ta bằng cái

| Token | Nhãn gốc |
|---|---|
| chúng | 0 |
| ta | 0 |
| khi | 0 |
| mà | 0 |
| chưa | 0 |
| có | 0 |
| tây | 0 |
| y | 0 |
| đến | 0 |
| đất | 0 |
| nước | 0 |
| chúng | 0 |
| ta | 0 |
| từ | 0 |
| thế | B-DATETIME |
| kỷ | I-DATETIME |
| mười | I-DATETIME |
| bảy | I-DATETIME |
| mười | I-DATETIME |
| tám | I-DATETIME |
| thì | 0 |
| cha | B-GENDER |
| ông | I-GENDER |
| chúng | 0 |
| ta | 0 |
| điều | B-TREATMENT |
| trị | I-TREATMENT |
| người | 0 |
| ta | 0 |
| bằng | 0 |
| cái | 0 |

## VM600-185 — dòng train 1554 (đếm từ 0)

của chúng ta và riêng mái tóc thì sao nè nó tác động vô cái nang tóc nó làm cho cái nang tóc nó phát triển không được

| Token | Nhãn gốc |
|---|---|
| của | 0 |
| chúng | 0 |
| ta | 0 |
| và | 0 |
| riêng | 0 |
| mái | B-ORGAN |
| tóc | I-ORGAN |
| thì | 0 |
| sao | 0 |
| nè | 0 |
| nó | 0 |
| tác | 0 |
| động | 0 |
| vô | 0 |
| cái | 0 |
| nang | B-ORGAN |
| tóc | I-ORGAN |
| nó | 0 |
| làm | 0 |
| cho | 0 |
| cái | 0 |
| nang | B-ORGAN |
| tóc | I-ORGAN |
| nó | 0 |
| phát | 0 |
| triển | 0 |
| không | 0 |
| được | 0 |

## VM600-186 — dòng train 1557 (đếm từ 0)

tình trạng bệnh lý tim mạch huyết áp cao như thế nào mời bác chia sẻ với chương trình vâng xin chào chị ạ dạ

| Token | Nhãn gốc |
|---|---|
| tình | 0 |
| trạng | 0 |
| bệnh | 0 |
| lý | 0 |
| tim | B-ORGAN |
| mạch | I-ORGAN |
| huyết | B-DISEASESYMTOM |
| áp | I-DISEASESYMTOM |
| cao | B-UNITCALIBRATOR |
| như | 0 |
| thế | 0 |
| nào | 0 |
| mời | 0 |
| bác | B-AGE |
| chia | 0 |
| sẻ | 0 |
| với | 0 |
| chương | 0 |
| trình | 0 |
| vâng | 0 |
| xin | 0 |
| chào | 0 |
| chị | B-GENDER |
| ạ | 0 |
| dạ | 0 |

## VM600-187 — dòng train 1565 (đếm từ 0)

rồi đi làm đi làm thì gặp sếp là phân công nó cũng không có phù hợp nói cái

| Token | Nhãn gốc |
|---|---|
| rồi | 0 |
| đi | 0 |
| làm | 0 |
| đi | 0 |
| làm | 0 |
| thì | 0 |
| gặp | 0 |
| sếp | 0 |
| là | 0 |
| phân | 0 |
| công | 0 |
| nó | 0 |
| cũng | 0 |
| không | 0 |
| có | 0 |
| phù | 0 |
| hợp | 0 |
| nói | 0 |
| cái | 0 |

## VM600-188 — dòng train 1603 (đếm từ 0)

tính hay còn gọi là gì ạ những cái nhóm bệnh lý mà nó có liên quan đến cái bệnh lý khớp mà nó có cái nền tảng lâu dài và

| Token | Nhãn gốc |
|---|---|
| tính | 0 |
| hay | 0 |
| còn | 0 |
| gọi | 0 |
| là | 0 |
| gì | 0 |
| ạ | 0 |
| những | 0 |
| cái | 0 |
| nhóm | 0 |
| bệnh | B-DISEASESYMTOM |
| lý | I-DISEASESYMTOM |
| mà | 0 |
| nó | 0 |
| có | 0 |
| liên | 0 |
| quan | 0 |
| đến | 0 |
| cái | 0 |
| bệnh | B-DISEASESYMTOM |
| lý | I-DISEASESYMTOM |
| khớp | B-ORGAN |
| mà | 0 |
| nó | 0 |
| có | 0 |
| cái | 0 |
| nền | 0 |
| tảng | 0 |
| lâu | 0 |
| dài | 0 |
| và | 0 |

## VM600-189 — dòng train 1610 (đếm từ 0)

bệnh lý của mình để có thể điều trị chính vì vậy thì qua trước chương trình của bệnh

| Token | Nhãn gốc |
|---|---|
| bệnh | B-DISEASESYMTOM |
| lý | I-DISEASESYMTOM |
| của | 0 |
| mình | 0 |
| để | 0 |
| có | 0 |
| thể | 0 |
| điều | B-TREATMENT |
| trị | I-TREATMENT |
| chính | 0 |
| vì | 0 |
| vậy | 0 |
| thì | 0 |
| qua | 0 |
| trước | 0 |
| chương | 0 |
| trình | 0 |
| của | 0 |
| bệnh | 0 |

## VM600-190 — dòng train 1611 (đếm từ 0)

tắt những cái điểm tiếp xúc của điện cực đó cũng như là điều chỉnh cường độ ở cái mức độ mà mình mong muốn tối ưu để được

| Token | Nhãn gốc |
|---|---|
| tắt | 0 |
| những | 0 |
| cái | 0 |
| điểm | 0 |
| tiếp | 0 |
| xúc | 0 |
| của | 0 |
| điện | B-MEDDEVICETECHNIQUE |
| cực | I-MEDDEVICETECHNIQUE |
| đó | 0 |
| cũng | 0 |
| như | 0 |
| là | 0 |
| điều | B-PREVENTIVEMED |
| chỉnh | I-PREVENTIVEMED |
| cường | B-UNITCALIBRATOR |
| độ | I-UNITCALIBRATOR |
| ở | 0 |
| cái | 0 |
| mức | B-UNITCALIBRATOR |
| độ | I-UNITCALIBRATOR |
| mà | 0 |
| mình | 0 |
| mong | 0 |
| muốn | 0 |
| tối | B-DATETIME |
| ưu | 0 |
| để | 0 |
| được | 0 |

## VM600-191 — dòng train 1615 (đếm từ 0)

chúng ta bao phủ bên trong và bên ngoài của chúng ta mà còn giúp cơ thể chúng ta thực hiện một loạt các chức năng cần

| Token | Nhãn gốc |
|---|---|
| chúng | 0 |
| ta | 0 |
| bao | 0 |
| phủ | 0 |
| bên | 0 |
| trong | 0 |
| và | 0 |
| bên | B-LOCATION |
| ngoài | I-LOCATION |
| của | 0 |
| chúng | 0 |
| ta | 0 |
| mà | 0 |
| còn | 0 |
| giúp | 0 |
| cơ | B-ORGAN |
| thể | I-ORGAN |
| chúng | 0 |
| ta | 0 |
| thực | 0 |
| hiện | 0 |
| một | 0 |
| loạt | 0 |
| các | 0 |
| chức | 0 |
| năng | 0 |
| cần | 0 |

## VM600-192 — dòng train 1622 (đếm từ 0)

từ khi đó đến nay huyết áp của ông thì thường xuyên tôi cũng cho dùng thuốc

| Token | Nhãn gốc |
|---|---|
| từ | 0 |
| khi | 0 |
| đó | 0 |
| đến | B-DATETIME |
| nay | I-DATETIME |
| huyết | B-DISEASESYMTOM |
| áp | I-DISEASESYMTOM |
| của | 0 |
| ông | B-GENDER |
| thì | 0 |
| thường | B-DATETIME |
| xuyên | I-DATETIME |
| tôi | 0 |
| cũng | 0 |
| cho | 0 |
| dùng | 0 |
| thuốc | B-DRUGCHEMICAL |

## VM600-193 — dòng train 1634 (đếm từ 0)

không có đủ sức để mà vượt qua những cái trở ngại về mặt cân nặng và cái tình

| Token | Nhãn gốc |
|---|---|
| không | 0 |
| có | 0 |
| đủ | 0 |
| sức | 0 |
| để | 0 |
| mà | 0 |
| vượt | 0 |
| qua | 0 |
| những | 0 |
| cái | 0 |
| trở | 0 |
| ngại | 0 |
| về | 0 |
| mặt | 0 |
| cân | 0 |
| nặng | 0 |
| và | 0 |
| cái | 0 |
| tình | 0 |

## VM600-194 — dòng train 1638 (đếm từ 0)

ghi nhận dù đã tiêm đủ mũi hoặc là gần

| Token | Nhãn gốc |
|---|---|
| ghi | 0 |
| nhận | 0 |
| dù | 0 |
| đã | 0 |
| tiêm | B-MEDDEVICETECHNIQUE |
| đủ | 0 |
| mũi | B-ORGAN |
| hoặc | 0 |
| là | 0 |
| gần | 0 |

## VM600-195 — dòng train 1641 (đếm từ 0)

chúng ta không nhìn thấy nhưng mà chúng ta thấy là tức chân đau chân lạnh chân thậm chí là nề bàn chân đấy cho nên là

| Token | Nhãn gốc |
|---|---|
| chúng | 0 |
| ta | 0 |
| không | 0 |
| nhìn | 0 |
| thấy | 0 |
| nhưng | 0 |
| mà | 0 |
| chúng | 0 |
| ta | 0 |
| thấy | 0 |
| là | 0 |
| tức | 0 |
| chân | 0 |
| đau | B-DISEASESYMTOM |
| chân | 0 |
| lạnh | 0 |
| chân | 0 |
| thậm | 0 |
| chí | 0 |
| là | 0 |
| nề | 0 |
| bàn | B-ORGAN |
| chân | I-ORGAN |
| đấy | 0 |
| cho | 0 |
| nên | 0 |
| là | 0 |

## VM600-196 — dòng train 1647 (đếm từ 0)

ta tiếp xúc các thành phần chống oxy hóa thì nó sẽ tác động vào cơ thể nói chung

| Token | Nhãn gốc |
|---|---|
| ta | 0 |
| tiếp | 0 |
| xúc | 0 |
| các | 0 |
| thành | 0 |
| phần | 0 |
| chống | 0 |
| oxy | B-DRUGCHEMICAL |
| hóa | 0 |
| thì | 0 |
| nó | 0 |
| sẽ | 0 |
| tác | 0 |
| động | 0 |
| vào | 0 |
| cơ | B-ORGAN |
| thể | I-ORGAN |
| nói | 0 |
| chung | 0 |

## VM600-197 — dòng train 1648 (đếm từ 0)

parkinson hay là bệnh alzheimer bệnh trầm cảm nữa vâng ạ rất là tốt cho cơ thể của chúng ta ngày hôm nay thì những

| Token | Nhãn gốc |
|---|---|
| parkinson | B-DISEASESYMTOM |
| hay | 0 |
| là | 0 |
| bệnh | 0 |
| alzheimer | B-DISEASESYMTOM |
| bệnh | 0 |
| trầm | B-DISEASESYMTOM |
| cảm | I-DISEASESYMTOM |
| nữa | 0 |
| vâng | 0 |
| ạ | 0 |
| rất | 0 |
| là | 0 |
| tốt | 0 |
| cho | 0 |
| cơ | B-ORGAN |
| thể | I-ORGAN |
| của | 0 |
| chúng | 0 |
| ta | 0 |
| ngày | B-DATETIME |
| hôm | I-DATETIME |
| nay | I-DATETIME |
| thì | 0 |
| những | 0 |

## VM600-198 — dòng train 1651 (đếm từ 0)

và nó còn có cái cái chiều hướng là nó sẽ cải thiện rất tốt nữa thế nên là bác hoàn toàn có thể yên tâm kết hợp sử dụng

| Token | Nhãn gốc |
|---|---|
| và | 0 |
| nó | 0 |
| còn | 0 |
| có | 0 |
| cái | 0 |
| cái | 0 |
| chiều | 0 |
| hướng | 0 |
| là | 0 |
| nó | 0 |
| sẽ | 0 |
| cải | B-TREATMENT |
| thiện | I-TREATMENT |
| rất | 0 |
| tốt | 0 |
| nữa | 0 |
| thế | 0 |
| nên | 0 |
| là | 0 |
| bác | B-AGE |
| hoàn | 0 |
| toàn | 0 |
| có | 0 |
| thể | 0 |
| yên | 0 |
| tâm | 0 |
| kết | 0 |
| hợp | 0 |
| sử | 0 |
| dụng | 0 |

## VM600-199 — dòng train 1659 (đếm từ 0)

tính điều trị như thế thì đôi khi da chúng ta sẽ trở nên khô ngứa bong tróc và các quá trình khô ngứa bong tróc đó thì

| Token | Nhãn gốc |
|---|---|
| tính | 0 |
| điều | B-TREATMENT |
| trị | I-TREATMENT |
| như | 0 |
| thế | 0 |
| thì | 0 |
| đôi | 0 |
| khi | 0 |
| da | B-ORGAN |
| chúng | 0 |
| ta | 0 |
| sẽ | 0 |
| trở | 0 |
| nên | 0 |
| khô | B-DISEASESYMTOM |
| ngứa | I-DISEASESYMTOM |
| bong | I-DISEASESYMTOM |
| tróc | I-DISEASESYMTOM |
| và | 0 |
| các | 0 |
| quá | 0 |
| trình | 0 |
| khô | B-DISEASESYMTOM |
| ngứa | I-DISEASESYMTOM |
| bong | I-DISEASESYMTOM |
| tróc | I-DISEASESYMTOM |
| đó | 0 |
| thì | 0 |

## VM600-200 — dòng train 1663 (đếm từ 0)

cụ thể hoặc là dễ hiểu hơn đấy là cái bệnh viêm cột sống dính khớp đấy thì rất

| Token | Nhãn gốc |
|---|---|
| cụ | 0 |
| thể | 0 |
| hoặc | 0 |
| là | 0 |
| dễ | 0 |
| hiểu | 0 |
| hơn | 0 |
| đấy | 0 |
| là | 0 |
| cái | 0 |
| bệnh | B-DISEASESYMTOM |
| viêm | I-DISEASESYMTOM |
| cột | I-DISEASESYMTOM |
| sống | I-DISEASESYMTOM |
| dính | I-DISEASESYMTOM |
| khớp | I-DISEASESYMTOM |
| đấy | 0 |
| thì | 0 |
| rất | 0 |

## VM600-201 — dòng train 1679 (đếm từ 0)

động một cách trực tiếp chúng ta cần nhớ rằng là những người làm việc văn phòng mặc dù là không phải là gặp mưa gặp nắng

| Token | Nhãn gốc |
|---|---|
| động | 0 |
| một | 0 |
| cách | 0 |
| trực | 0 |
| tiếp | 0 |
| chúng | 0 |
| ta | 0 |
| cần | 0 |
| nhớ | 0 |
| rằng | 0 |
| là | 0 |
| những | 0 |
| người | B-OCCUPATION |
| làm | I-OCCUPATION |
| việc | I-OCCUPATION |
| văn | I-OCCUPATION |
| phòng | I-OCCUPATION |
| mặc | 0 |
| dù | 0 |
| là | 0 |
| không | 0 |
| phải | 0 |
| là | 0 |
| gặp | 0 |
| mưa | 0 |
| gặp | 0 |
| nắng | 0 |

## VM600-202 — dòng train 1686 (đếm từ 0)

đánh giá tự bác thì cũng có thể là điều chỉnh lại cái chế độ ăn để xem xem là mình có ăn thiếu chất không mình có thể

| Token | Nhãn gốc |
|---|---|
| đánh | B-TREATMENT |
| giá | I-TREATMENT |
| tự | 0 |
| bác | B-AGE |
| thì | 0 |
| cũng | 0 |
| có | 0 |
| thể | 0 |
| là | 0 |
| điều | B-PREVENTIVEMED |
| chỉnh | I-PREVENTIVEMED |
| lại | 0 |
| cái | 0 |
| chế | B-PERSONALCARE |
| độ | I-PERSONALCARE |
| ăn | I-PERSONALCARE |
| để | 0 |
| xem | 0 |
| xem | 0 |
| là | 0 |
| mình | 0 |
| có | 0 |
| ăn | 0 |
| thiếu | 0 |
| chất | 0 |
| không | 0 |
| mình | 0 |
| có | 0 |
| thể | 0 |

## VM600-203 — dòng train 1694 (đếm từ 0)

khi nó không đủ chất đủ cân bằng vân vân thế cho nên là cái việc mà hỏi là điều trị khỏi hẳn bệnh huyết áp hoặc là khỏi

| Token | Nhãn gốc |
|---|---|
| khi | 0 |
| nó | 0 |
| không | 0 |
| đủ | 0 |
| chất | 0 |
| đủ | 0 |
| cân | 0 |
| bằng | 0 |
| vân | 0 |
| vân | 0 |
| thế | 0 |
| cho | 0 |
| nên | 0 |
| là | 0 |
| cái | 0 |
| việc | 0 |
| mà | 0 |
| hỏi | 0 |
| là | 0 |
| điều | B-TREATMENT |
| trị | I-TREATMENT |
| khỏi | 0 |
| hẳn | 0 |
| bệnh | 0 |
| huyết | B-DISEASESYMTOM |
| áp | I-DISEASESYMTOM |
| hoặc | 0 |
| là | 0 |
| khỏi | 0 |

## VM600-204 — dòng train 1696 (đếm từ 0)

một cái cái thoái hóa cột sống thắt lưng bác có đau cột sống thắt lưng tuy nhiên ngoài ra lại có cái câu chuyện là đau

| Token | Nhãn gốc |
|---|---|
| một | 0 |
| cái | 0 |
| cái | 0 |
| thoái | B-DISEASESYMTOM |
| hóa | I-DISEASESYMTOM |
| cột | I-DISEASESYMTOM |
| sống | I-DISEASESYMTOM |
| thắt | B-ORGAN |
| lưng | I-ORGAN |
| bác | B-AGE |
| có | 0 |
| đau | B-DISEASESYMTOM |
| cột | B-ORGAN |
| sống | I-ORGAN |
| thắt | B-ORGAN |
| lưng | I-ORGAN |
| tuy | 0 |
| nhiên | 0 |
| ngoài | 0 |
| ra | 0 |
| lại | 0 |
| có | 0 |
| cái | 0 |
| câu | 0 |
| chuyện | 0 |
| là | 0 |
| đau | B-DISEASESYMTOM |

## VM600-205 — dòng train 1698 (đếm từ 0)

lúc mà đột quỵ mà nó không tự thông lại đều thì lúc đó là sẽ đột quỵ thật sự được rõ chúng ta sẽ rất là nghiêm

| Token | Nhãn gốc |
|---|---|
| lúc | 0 |
| mà | 0 |
| đột | B-DISEASESYMTOM |
| quỵ | I-DISEASESYMTOM |
| mà | 0 |
| nó | 0 |
| không | 0 |
| tự | 0 |
| thông | 0 |
| lại | 0 |
| đều | 0 |
| thì | 0 |
| lúc | 0 |
| đó | 0 |
| là | 0 |
| sẽ | 0 |
| đột | B-DISEASESYMTOM |
| quỵ | I-DISEASESYMTOM |
| thật | 0 |
| sự | 0 |
| được | 0 |
| rõ | 0 |
| chúng | 0 |
| ta | 0 |
| sẽ | 0 |
| rất | 0 |
| là | 0 |
| nghiêm | 0 |

## VM600-206 — dòng train 1700 (đếm từ 0)

cái ghi nhận người ta thấy rằng là một cái thời gian sau khi đặt cái điện cực này quá không hiểu tại sao thì bệnh nhân có thể có những cái cái rối loạn cảm xúc

| Token | Nhãn gốc |
|---|---|
| cái | 0 |
| ghi | 0 |
| nhận | 0 |
| người | 0 |
| ta | 0 |
| thấy | 0 |
| rằng | 0 |
| là | 0 |
| một | 0 |
| cái | 0 |
| thời | B-DATETIME |
| gian | I-DATETIME |
| sau | 0 |
| khi | 0 |
| đặt | 0 |
| cái | 0 |
| điện | B-MEDDEVICETECHNIQUE |
| cực | I-MEDDEVICETECHNIQUE |
| này | 0 |
| quá | 0 |
| không | 0 |
| hiểu | 0 |
| tại | 0 |
| sao | 0 |
| thì | 0 |
| bệnh | B-OCCUPATION |
| nhân | I-OCCUPATION |
| có | 0 |
| thể | 0 |
| có | 0 |
| những | 0 |
| cái | 0 |
| cái | 0 |
| rối | B-DISEASESYMTOM |
| loạn | I-DISEASESYMTOM |
| cảm | I-DISEASESYMTOM |
| xúc | I-DISEASESYMTOM |

## VM600-207 — dòng train 1707 (đếm từ 0)

động vật không xương sống và chúng sống sót qua bệnh tật chỉ bằng kiểu phòng thủ này nghĩa là hệ miễn dịch của chúng

| Token | Nhãn gốc |
|---|---|
| động | 0 |
| vật | 0 |
| không | 0 |
| xương | B-ORGAN |
| sống | 0 |
| và | 0 |
| chúng | 0 |
| sống | 0 |
| sót | 0 |
| qua | 0 |
| bệnh | 0 |
| tật | 0 |
| chỉ | 0 |
| bằng | 0 |
| kiểu | 0 |
| phòng | 0 |
| thủ | 0 |
| này | 0 |
| nghĩa | 0 |
| là | 0 |
| hệ | B-ORGAN |
| miễn | I-ORGAN |
| dịch | I-ORGAN |
| của | 0 |
| chúng | 0 |

## VM600-208 — dòng train 1708 (đếm từ 0)

như số lượng ngôi sao chọn vũ trụ trên thực tế mầm bệnh không thể nhân

| Token | Nhãn gốc |
|---|---|
| như | 0 |
| số | 0 |
| lượng | 0 |
| ngôi | 0 |
| sao | 0 |
| chọn | 0 |
| vũ | 0 |
| trụ | 0 |
| trên | 0 |
| thực | 0 |
| tế | 0 |
| mầm | B-DISEASESYMTOM |
| bệnh | I-DISEASESYMTOM |
| không | 0 |
| thể | 0 |
| nhân | 0 |

## VM600-209 — dòng train 1732 (đếm từ 0)

giống như là không có cái giá trị vì đi ăn toàn lại không ăn hại tới ăn mà ăn thì nhiều nhưng mà làm thì ít thì cái

| Token | Nhãn gốc |
|---|---|
| giống | 0 |
| như | 0 |
| là | 0 |
| không | 0 |
| có | 0 |
| cái | 0 |
| giá | 0 |
| trị | 0 |
| vì | 0 |
| đi | 0 |
| ăn | 0 |
| toàn | 0 |
| lại | 0 |
| không | 0 |
| ăn | 0 |
| hại | 0 |
| tới | 0 |
| ăn | 0 |
| mà | 0 |
| ăn | 0 |
| thì | 0 |
| nhiều | 0 |
| nhưng | 0 |
| mà | 0 |
| làm | 0 |
| thì | 0 |
| ít | 0 |
| thì | 0 |
| cái | 0 |

## VM600-210 — dòng train 1738 (đếm từ 0)

và tình trạng sức khỏe của một người câu trả lời cho câu hỏi nằm ở sự khác biệt

| Token | Nhãn gốc |
|---|---|
| và | 0 |
| tình | 0 |
| trạng | 0 |
| sức | 0 |
| khỏe | 0 |
| của | 0 |
| một | B-UNITCALIBRATOR |
| người | I-UNITCALIBRATOR |
| câu | 0 |
| trả | 0 |
| lời | 0 |
| cho | 0 |
| câu | 0 |
| hỏi | 0 |
| nằm | 0 |
| ở | 0 |
| sự | 0 |
| khác | 0 |
| biệt | 0 |

## VM600-211 — dòng train 1739 (đếm từ 0)

này nó tích cực hơn điều này nó cực kỳ quan trọng vì như chúng tôi đã trình bày ở trên thì

| Token | Nhãn gốc |
|---|---|
| này | 0 |
| nó | 0 |
| tích | 0 |
| cực | 0 |
| hơn | 0 |
| điều | 0 |
| này | 0 |
| nó | 0 |
| cực | 0 |
| kỳ | 0 |
| quan | 0 |
| trọng | 0 |
| vì | 0 |
| như | 0 |
| chúng | 0 |
| tôi | 0 |
| đã | 0 |
| trình | 0 |
| bày | 0 |
| ở | 0 |
| trên | 0 |
| thì | 0 |

## VM600-212 — dòng train 1743 (đếm từ 0)

dụng là ức chế sẽ sinh sắc tố nữa như vậy thì chúng ta sẽ vừa phục hồi được cái làn da trong quá trình điều trị mà

| Token | Nhãn gốc |
|---|---|
| dụng | 0 |
| là | 0 |
| ức | B-PREVENTIVEMED |
| chế | I-PREVENTIVEMED |
| sẽ | 0 |
| sinh | 0 |
| sắc | B-ORGAN |
| tố | I-ORGAN |
| nữa | 0 |
| như | 0 |
| vậy | 0 |
| thì | 0 |
| chúng | 0 |
| ta | 0 |
| sẽ | 0 |
| vừa | 0 |
| phục | B-MEDDEVICETECHNIQUE |
| hồi | I-MEDDEVICETECHNIQUE |
| được | 0 |
| cái | 0 |
| làn | B-ORGAN |
| da | I-ORGAN |
| trong | 0 |
| quá | 0 |
| trình | 0 |
| điều | B-TREATMENT |
| trị | I-TREATMENT |
| mà | 0 |

## VM600-213 — dòng train 1748 (đếm từ 0)

tuy nhiên điều đó nói lên rằng chúng ta phải thừa nhận các bằng chứng vẫn tiếp

| Token | Nhãn gốc |
|---|---|
| tuy | 0 |
| nhiên | 0 |
| điều | 0 |
| đó | 0 |
| nói | 0 |
| lên | 0 |
| rằng | 0 |
| chúng | 0 |
| ta | 0 |
| phải | 0 |
| thừa | 0 |
| nhận | 0 |
| các | 0 |
| bằng | 0 |
| chứng | 0 |
| vẫn | 0 |
| tiếp | 0 |

## VM600-214 — dòng train 1750 (đếm từ 0)

cái động tác giúp cải thiện cái tuần hoàn của các cái vùng của cơ thể của chúng ta thì bản thân bác sĩ nhiều khi

| Token | Nhãn gốc |
|---|---|
| cái | 0 |
| động | 0 |
| tác | 0 |
| giúp | 0 |
| cải | B-TREATMENT |
| thiện | I-TREATMENT |
| cái | 0 |
| tuần | B-DATETIME |
| hoàn | 0 |
| của | 0 |
| các | 0 |
| cái | 0 |
| vùng | 0 |
| của | 0 |
| cơ | B-ORGAN |
| thể | I-ORGAN |
| của | 0 |
| chúng | 0 |
| ta | 0 |
| thì | 0 |
| bản | 0 |
| thân | 0 |
| bác | B-OCCUPATION |
| sĩ | I-OCCUPATION |
| nhiều | 0 |
| khi | 0 |

## VM600-215 — dòng train 1752 (đếm từ 0)

ta thấy là đan sâm vâng đan sâm cũng là một vị thuốc rất nổi tiếng xưa kia của cha ông ta nó nằm ở trong cái vị thuốc

| Token | Nhãn gốc |
|---|---|
| ta | 0 |
| thấy | 0 |
| là | 0 |
| đan | B-DRUGCHEMICAL |
| sâm | I-DRUGCHEMICAL |
| vâng | 0 |
| đan | B-DRUGCHEMICAL |
| sâm | I-DRUGCHEMICAL |
| cũng | 0 |
| là | 0 |
| một | 0 |
| vị | 0 |
| thuốc | B-DRUGCHEMICAL |
| rất | 0 |
| nổi | 0 |
| tiếng | 0 |
| xưa | 0 |
| kia | 0 |
| của | 0 |
| cha | B-GENDER |
| ông | I-GENDER |
| ta | 0 |
| nó | 0 |
| nằm | 0 |
| ở | 0 |
| trong | 0 |
| cái | 0 |
| vị | 0 |
| thuốc | B-DRUGCHEMICAL |

## VM600-216 — dòng train 1757 (đếm từ 0)

nên ăn các cái thực phẩm là chế biến sẵn bởi vì trong đó một là giàu các cái chất

| Token | Nhãn gốc |
|---|---|
| nên | 0 |
| ăn | 0 |
| các | 0 |
| cái | 0 |
| thực | B-FOODDRINK |
| phẩm | I-FOODDRINK |
| là | 0 |
| chế | B-MEDDEVICETECHNIQUE |
| biến | I-MEDDEVICETECHNIQUE |
| sẵn | 0 |
| bởi | 0 |
| vì | 0 |
| trong | 0 |
| đó | 0 |
| một | 0 |
| là | 0 |
| giàu | 0 |
| các | 0 |
| cái | 0 |
| chất | 0 |

## VM600-217 — dòng train 1760 (đếm từ 0)

qua cái đường mà can thiệp nội mạch thì hiện nay đó thì người ta đã chế tạo

| Token | Nhãn gốc |
|---|---|
| qua | 0 |
| cái | 0 |
| đường | 0 |
| mà | 0 |
| can | B-PREVENTIVEMED |
| thiệp | I-PREVENTIVEMED |
| nội | 0 |
| mạch | B-ORGAN |
| thì | 0 |
| hiện | B-DATETIME |
| nay | I-DATETIME |
| đó | 0 |
| thì | 0 |
| người | 0 |
| ta | 0 |
| đã | 0 |
| chế | 0 |
| tạo | 0 |

## VM600-218 — dòng train 1784 (đếm từ 0)

điều trị thuốc nó phải đúng chứ không phải là mình thích cái thuốc nào là mình dùng thuốc đó hay là mình nghe cái mách

| Token | Nhãn gốc |
|---|---|
| điều | B-TREATMENT |
| trị | I-TREATMENT |
| thuốc | B-DRUGCHEMICAL |
| nó | 0 |
| phải | 0 |
| đúng | 0 |
| chứ | 0 |
| không | 0 |
| phải | 0 |
| là | 0 |
| mình | 0 |
| thích | 0 |
| cái | 0 |
| thuốc | B-DRUGCHEMICAL |
| nào | 0 |
| là | 0 |
| mình | 0 |
| dùng | 0 |
| thuốc | B-DRUGCHEMICAL |
| đó | 0 |
| hay | 0 |
| là | 0 |
| mình | 0 |
| nghe | 0 |
| cái | 0 |
| mách | 0 |

## VM600-219 — dòng train 1798 (đếm từ 0)

thực phẩm bảo vệ sức khỏe có lợi cho vấn đề tim mạch có lợi cho vấn đề thần kinh mà rất hữu ích với cái việc mà nó hỗ trợ

| Token | Nhãn gốc |
|---|---|
| thực | B-FOODDRINK |
| phẩm | I-FOODDRINK |
| bảo | B-PERSONALCARE |
| vệ | I-PERSONALCARE |
| sức | I-PERSONALCARE |
| khỏe | I-PERSONALCARE |
| có | 0 |
| lợi | 0 |
| cho | 0 |
| vấn | 0 |
| đề | 0 |
| tim | B-ORGAN |
| mạch | I-ORGAN |
| có | 0 |
| lợi | 0 |
| cho | 0 |
| vấn | 0 |
| đề | 0 |
| thần | B-ORGAN |
| kinh | I-ORGAN |
| mà | 0 |
| rất | 0 |
| hữu | 0 |
| ích | 0 |
| với | 0 |
| cái | 0 |
| việc | 0 |
| mà | 0 |
| nó | 0 |
| hỗ | B-MEDDEVICETECHNIQUE |
| trợ | I-MEDDEVICETECHNIQUE |

## VM600-220 — dòng train 1801 (đếm từ 0)

cái hiệu quả của mình mình cũng không dám chắc một trăm phần trăm hoặc là nó cũng có những cái rủi ro nhất định cho

| Token | Nhãn gốc |
|---|---|
| cái | 0 |
| hiệu | 0 |
| quả | 0 |
| của | 0 |
| mình | 0 |
| mình | 0 |
| cũng | 0 |
| không | 0 |
| dám | 0 |
| chắc | 0 |
| một | B-UNITCALIBRATOR |
| trăm | I-UNITCALIBRATOR |
| phần | I-UNITCALIBRATOR |
| trăm | I-UNITCALIBRATOR |
| hoặc | 0 |
| là | 0 |
| nó | 0 |
| cũng | 0 |
| có | 0 |
| những | 0 |
| cái | 0 |
| rủi | 0 |
| ro | 0 |
| nhất | 0 |
| định | 0 |
| cho | 0 |

## VM600-221 — dòng train 1803 (đếm từ 0)

gì cả hàng năm bên cạnh việc duy trì ngâm khoáng và điều trị ở bệnh viện cả tháng

| Token | Nhãn gốc |
|---|---|
| gì | 0 |
| cả | 0 |
| hàng | B-DATETIME |
| năm | I-DATETIME |
| bên | 0 |
| cạnh | 0 |
| việc | 0 |
| duy | B-PERSONALCARE |
| trì | I-PERSONALCARE |
| ngâm | B-MEDDEVICETECHNIQUE |
| khoáng | I-MEDDEVICETECHNIQUE |
| và | 0 |
| điều | B-TREATMENT |
| trị | I-TREATMENT |
| ở | 0 |
| bệnh | B-LOCATION |
| viện | I-LOCATION |
| cả | 0 |
| tháng | 0 |

## VM600-222 — dòng train 1815 (đếm từ 0)

không

| Token | Nhãn gốc |
|---|---|
| không | 0 |

## VM600-223 — dòng train 1822 (đếm từ 0)

chụp vai gáy ở đâu dây thần viêm đốt vai

| Token | Nhãn gốc |
|---|---|
| chụp | B-TREATMENT |
| vai | I-TREATMENT |
| gáy | I-TREATMENT |
| ở | 0 |
| đâu | 0 |
| dây | 0 |
| thần | 0 |
| viêm | B-DISEASESYMTOM |
| đốt | B-ORGAN |
| vai | I-ORGAN |

## VM600-224 — dòng train 1831 (đếm từ 0)

với tình trạng rung nhĩ tim đập nó quá nhanh thì chúng ta phải có biện pháp nào để kiểm soát các tần số đó đừng cho đập

| Token | Nhãn gốc |
|---|---|
| với | 0 |
| tình | 0 |
| trạng | 0 |
| rung | B-DISEASESYMTOM |
| nhĩ | I-DISEASESYMTOM |
| tim | B-ORGAN |
| đập | 0 |
| nó | 0 |
| quá | 0 |
| nhanh | 0 |
| thì | 0 |
| chúng | 0 |
| ta | 0 |
| phải | 0 |
| có | 0 |
| biện | 0 |
| pháp | 0 |
| nào | 0 |
| để | 0 |
| kiểm | B-PREVENTIVEMED |
| soát | I-PREVENTIVEMED |
| các | 0 |
| tần | B-UNITCALIBRATOR |
| số | I-UNITCALIBRATOR |
| đó | 0 |
| đừng | 0 |
| cho | 0 |
| đập | 0 |

## VM600-225 — dòng train 1832 (đếm từ 0)

nhau đây chúng ta chỉ có hai nhóm chúng ta khuyến cáo ít nhất là phải mười lăm loại thực phẩm đây chúng ta chỉ có hai loại

| Token | Nhãn gốc |
|---|---|
| nhau | 0 |
| đây | 0 |
| chúng | 0 |
| ta | 0 |
| chỉ | 0 |
| có | 0 |
| hai | B-UNITCALIBRATOR |
| nhóm | I-UNITCALIBRATOR |
| chúng | 0 |
| ta | 0 |
| khuyến | B-PREVENTIVEMED |
| cáo | I-PREVENTIVEMED |
| ít | 0 |
| nhất | 0 |
| là | 0 |
| phải | 0 |
| mười | 0 |
| lăm | 0 |
| loại | 0 |
| thực | B-FOODDRINK |
| phẩm | I-FOODDRINK |
| đây | 0 |
| chúng | 0 |
| ta | 0 |
| chỉ | 0 |
| có | 0 |
| hai | 0 |
| loại | 0 |

## VM600-226 — dòng train 1836 (đếm từ 0)

giày thì nó sẽ giữ được cái chân ấm hơn chúng ta sẽ đi cái tất dày hơn đi cái tất dài hơn như thế cũng sẽ rất là hữu

| Token | Nhãn gốc |
|---|---|
| giày | 0 |
| thì | 0 |
| nó | 0 |
| sẽ | 0 |
| giữ | 0 |
| được | 0 |
| cái | B-ORGAN |
| chân | I-ORGAN |
| ấm | 0 |
| hơn | 0 |
| chúng | 0 |
| ta | 0 |
| sẽ | 0 |
| đi | 0 |
| cái | 0 |
| tất | 0 |
| dày | 0 |
| hơn | 0 |
| đi | 0 |
| cái | 0 |
| tất | 0 |
| dài | 0 |
| hơn | 0 |
| như | 0 |
| thế | 0 |
| cũng | 0 |
| sẽ | 0 |
| rất | 0 |
| là | 0 |
| hữu | 0 |

## VM600-227 — dòng train 1839 (đếm từ 0)

một cái gợi ý nó cũng chỉ là một cái tỷ lệ do đó cái xét nghiệm khi mà chúng ta thấy không thật sự cần thiết thì chúng

| Token | Nhãn gốc |
|---|---|
| một | 0 |
| cái | 0 |
| gợi | 0 |
| ý | 0 |
| nó | 0 |
| cũng | 0 |
| chỉ | 0 |
| là | 0 |
| một | 0 |
| cái | B-UNITCALIBRATOR |
| tỷ | I-UNITCALIBRATOR |
| lệ | I-UNITCALIBRATOR |
| do | 0 |
| đó | 0 |
| cái | 0 |
| xét | B-DIAGNOSTICS |
| nghiệm | I-DIAGNOSTICS |
| khi | 0 |
| mà | 0 |
| chúng | 0 |
| ta | 0 |
| thấy | 0 |
| không | 0 |
| thật | 0 |
| sự | 0 |
| cần | 0 |
| thiết | 0 |
| thì | 0 |
| chúng | 0 |

## VM600-228 — dòng train 1843 (đếm từ 0)

gây nhiễm có chủ ý để cung cấp sự bảo vệ sự chủng ngừa đã được thực hành ở trung

| Token | Nhãn gốc |
|---|---|
| gây | 0 |
| nhiễm | 0 |
| có | 0 |
| chủ | 0 |
| ý | 0 |
| để | 0 |
| cung | 0 |
| cấp | 0 |
| sự | 0 |
| bảo | 0 |
| vệ | 0 |
| sự | 0 |
| chủng | 0 |
| ngừa | 0 |
| đã | 0 |
| được | 0 |
| thực | 0 |
| hành | 0 |
| ở | 0 |
| trung | 0 |

## VM600-229 — dòng train 1844 (đếm từ 0)

về em tẩy trang bôi lại kem chống nắng thì nên làm thêm bước nào trong ba bước này nữa ạ vâng nếu mà buổi trưa đó là

| Token | Nhãn gốc |
|---|---|
| về | 0 |
| em | 0 |
| tẩy | B-PERSONALCARE |
| trang | I-PERSONALCARE |
| bôi | 0 |
| lại | 0 |
| kem | B-DRUGCHEMICAL |
| chống | I-DRUGCHEMICAL |
| nắng | I-DRUGCHEMICAL |
| thì | 0 |
| nên | 0 |
| làm | 0 |
| thêm | 0 |
| bước | 0 |
| nào | 0 |
| trong | 0 |
| ba | B-UNITCALIBRATOR |
| bước | I-UNITCALIBRATOR |
| này | 0 |
| nữa | 0 |
| ạ | 0 |
| vâng | 0 |
| nếu | 0 |
| mà | 0 |
| buổi | B-DATETIME |
| trưa | I-DATETIME |
| đó | 0 |
| là | 0 |

## VM600-230 — dòng train 1845 (đếm từ 0)

tử mà nó chưa gặp phải trước đây nói cách khác hệ miễn dịch hoạt động bằng

| Token | Nhãn gốc |
|---|---|
| tử | 0 |
| mà | 0 |
| nó | 0 |
| chưa | 0 |
| gặp | 0 |
| phải | 0 |
| trước | 0 |
| đây | 0 |
| nói | 0 |
| cách | 0 |
| khác | 0 |
| hệ | B-ORGAN |
| miễn | I-ORGAN |
| dịch | I-ORGAN |
| hoạt | 0 |
| động | 0 |
| bằng | 0 |

## VM600-231 — dòng train 1849 (đếm từ 0)

thập niên trước khi mắc các bệnh tim mạch và ung thư và họ không mắc chứng trầm cảm nhiều tỷ lệ suy giảm nhận thức

| Token | Nhãn gốc |
|---|---|
| thập | B-DATETIME |
| niên | I-DATETIME |
| trước | 0 |
| khi | 0 |
| mắc | 0 |
| các | 0 |
| bệnh | 0 |
| tim | B-ORGAN |
| mạch | I-ORGAN |
| và | 0 |
| ung | B-DISEASESYMTOM |
| thư | I-DISEASESYMTOM |
| và | 0 |
| họ | 0 |
| không | 0 |
| mắc | 0 |
| chứng | 0 |
| trầm | B-DISEASESYMTOM |
| cảm | I-DISEASESYMTOM |
| nhiều | 0 |
| tỷ | B-UNITCALIBRATOR |
| lệ | I-UNITCALIBRATOR |
| suy | B-DISEASESYMTOM |
| giảm | I-DISEASESYMTOM |
| nhận | I-DISEASESYMTOM |
| thức | I-DISEASESYMTOM |

## VM600-232 — dòng train 1858 (đếm từ 0)

có cái vấn đề tương tự như thế này chúng tôi khuyên là chúng ta nên đi khám bệnh để có một cái đánh giá có một cái chẩn

| Token | Nhãn gốc |
|---|---|
| có | 0 |
| cái | 0 |
| vấn | 0 |
| đề | 0 |
| tương | 0 |
| tự | 0 |
| như | 0 |
| thế | 0 |
| này | 0 |
| chúng | 0 |
| tôi | 0 |
| khuyên | 0 |
| là | 0 |
| chúng | 0 |
| ta | 0 |
| nên | 0 |
| đi | 0 |
| khám | B-DIAGNOSTICS |
| bệnh | 0 |
| để | 0 |
| có | 0 |
| một | 0 |
| cái | 0 |
| đánh | B-TREATMENT |
| giá | I-TREATMENT |
| có | 0 |
| một | 0 |
| cái | 0 |
| chẩn | 0 |

## VM600-233 — dòng train 1859 (đếm từ 0)

chúng ta biết rằng hiện chưa có cách chữa trị tiềm năng nào và còn cả chứng

| Token | Nhãn gốc |
|---|---|
| chúng | 0 |
| ta | 0 |
| biết | 0 |
| rằng | 0 |
| hiện | 0 |
| chưa | 0 |
| có | 0 |
| cách | 0 |
| chữa | B-TREATMENT |
| trị | I-TREATMENT |
| tiềm | 0 |
| năng | 0 |
| nào | 0 |
| và | 0 |
| còn | 0 |
| cả | 0 |
| chứng | 0 |

## VM600-234 — dòng train 1865 (đếm từ 0)

ta mà còn thắc mắc cũng như là cũng như là chúng ta bị mắc cái tình trạng về huyết áp cao mỡ máu cao lâu năm thì

| Token | Nhãn gốc |
|---|---|
| ta | 0 |
| mà | 0 |
| còn | 0 |
| thắc | 0 |
| mắc | 0 |
| cũng | 0 |
| như | 0 |
| là | 0 |
| cũng | 0 |
| như | 0 |
| là | 0 |
| chúng | 0 |
| ta | 0 |
| bị | 0 |
| mắc | 0 |
| cái | 0 |
| tình | 0 |
| trạng | 0 |
| về | 0 |
| huyết | B-DISEASESYMTOM |
| áp | I-DISEASESYMTOM |
| cao | B-UNITCALIBRATOR |
| mỡ | B-DISEASESYMTOM |
| máu | I-DISEASESYMTOM |
| cao | B-UNITCALIBRATOR |
| lâu | 0 |
| năm | 0 |
| thì | 0 |

## VM600-235 — dòng train 1866 (đếm từ 0)

trường khác như là các cái thuốc hoạt huyết hoặc là những cái thuốc giảm đau thì nó chỉ có cái tác dụng cải thiện

| Token | Nhãn gốc |
|---|---|
| trường | 0 |
| khác | 0 |
| như | 0 |
| là | 0 |
| các | 0 |
| cái | 0 |
| thuốc | B-DRUGCHEMICAL |
| hoạt | I-DRUGCHEMICAL |
| huyết | I-DRUGCHEMICAL |
| hoặc | 0 |
| là | 0 |
| những | 0 |
| cái | 0 |
| thuốc | B-DRUGCHEMICAL |
| giảm | I-DRUGCHEMICAL |
| đau | I-DRUGCHEMICAL |
| thì | 0 |
| nó | 0 |
| chỉ | 0 |
| có | 0 |
| cái | 0 |
| tác | 0 |
| dụng | 0 |
| cải | B-TREATMENT |
| thiện | I-TREATMENT |

## VM600-236 — dòng train 1867 (đếm từ 0)

thuốc mà có thể là không ảnh hưởng đến cân nặng hoặc là thậm chí là có tác dụng giảm cân cho những bệnh nhân như vậy thì điều này cũng đã đưa và các cái

| Token | Nhãn gốc |
|---|---|
| thuốc | B-DRUGCHEMICAL |
| mà | 0 |
| có | 0 |
| thể | 0 |
| là | 0 |
| không | 0 |
| ảnh | 0 |
| hưởng | 0 |
| đến | 0 |
| cân | 0 |
| nặng | 0 |
| hoặc | 0 |
| là | 0 |
| thậm | 0 |
| chí | 0 |
| là | 0 |
| có | 0 |
| tác | 0 |
| dụng | 0 |
| giảm | B-PERSONALCARE |
| cân | I-PERSONALCARE |
| cho | 0 |
| những | B-UNITCALIBRATOR |
| bệnh | I-UNITCALIBRATOR |
| nhân | I-UNITCALIBRATOR |
| như | 0 |
| vậy | 0 |
| thì | 0 |
| điều | 0 |
| này | 0 |
| cũng | 0 |
| đã | 0 |
| đưa | 0 |
| và | 0 |
| các | 0 |
| cái | 0 |

## VM600-237 — dòng train 1870 (đếm từ 0)

của chúng ta thì khi đó rõ ràng chúng ta biết rằng là chúng ta cần phải điều chỉnh cái bệnh của chúng ta chứ không

| Token | Nhãn gốc |
|---|---|
| của | 0 |
| chúng | 0 |
| ta | 0 |
| thì | 0 |
| khi | 0 |
| đó | 0 |
| rõ | 0 |
| ràng | 0 |
| chúng | 0 |
| ta | 0 |
| biết | 0 |
| rằng | 0 |
| là | 0 |
| chúng | 0 |
| ta | 0 |
| cần | 0 |
| phải | 0 |
| điều | B-PREVENTIVEMED |
| chỉnh | I-PREVENTIVEMED |
| cái | 0 |
| bệnh | 0 |
| của | 0 |
| chúng | 0 |
| ta | 0 |
| chứ | 0 |
| không | 0 |

## VM600-238 — dòng train 1880 (đếm từ 0)

mạch nữa và từ đó thì sẽ tăng cái lưu lượng máu tốt cho não khỏe tim giúp cải thiện các triệu chứng đau đầu chóng mặt

| Token | Nhãn gốc |
|---|---|
| mạch | B-ORGAN |
| nữa | 0 |
| và | 0 |
| từ | 0 |
| đó | 0 |
| thì | 0 |
| sẽ | 0 |
| tăng | 0 |
| cái | 0 |
| lưu | B-UNITCALIBRATOR |
| lượng | I-UNITCALIBRATOR |
| máu | I-UNITCALIBRATOR |
| tốt | 0 |
| cho | 0 |
| não | B-ORGAN |
| khỏe | 0 |
| tim | B-ORGAN |
| giúp | 0 |
| cải | B-TREATMENT |
| thiện | I-TREATMENT |
| các | 0 |
| triệu | B-DISEASESYMTOM |
| chứng | I-DISEASESYMTOM |
| đau | B-DISEASESYMTOM |
| đầu | I-DISEASESYMTOM |
| chóng | B-DISEASESYMTOM |
| mặt | I-DISEASESYMTOM |

## VM600-239 — dòng train 1882 (đếm từ 0)

cả bạn mặc dù có lẽ bạn quen với thực tế là một số vi khuẩn có thể gây bệnh và

| Token | Nhãn gốc |
|---|---|
| cả | 0 |
| bạn | 0 |
| mặc | 0 |
| dù | 0 |
| có | 0 |
| lẽ | 0 |
| bạn | 0 |
| quen | 0 |
| với | 0 |
| thực | 0 |
| tế | 0 |
| là | 0 |
| một | 0 |
| số | 0 |
| vi | B-DISEASESYMTOM |
| khuẩn | I-DISEASESYMTOM |
| có | 0 |
| thể | 0 |
| gây | 0 |
| bệnh | 0 |
| và | 0 |

## VM600-240 — dòng train 1889 (đếm từ 0)

dây thần kinh và mạch máu khi đi xuống cái bàn tay nó sẽ đi qua cái vùng cổ tay như thế này và nếu mà cái chỗ này nó bị

| Token | Nhãn gốc |
|---|---|
| dây | B-ORGAN |
| thần | I-ORGAN |
| kinh | I-ORGAN |
| và | 0 |
| mạch | B-ORGAN |
| máu | I-ORGAN |
| khi | 0 |
| đi | 0 |
| xuống | 0 |
| cái | 0 |
| bàn | B-ORGAN |
| tay | I-ORGAN |
| nó | 0 |
| sẽ | 0 |
| đi | 0 |
| qua | 0 |
| cái | 0 |
| vùng | B-ORGAN |
| cổ | B-ORGAN |
| tay | I-ORGAN |
| như | 0 |
| thế | 0 |
| này | 0 |
| và | 0 |
| nếu | 0 |
| mà | 0 |
| cái | 0 |
| chỗ | 0 |
| này | 0 |
| nó | 0 |
| bị | 0 |

## VM600-241 — dòng train 1893 (đếm từ 0)

có cường giáp hay không phải cường giáp là một cái yếu tố nó kích động trái tim lên chúng ta và nó sẽ gây ra tình trạng

| Token | Nhãn gốc |
|---|---|
| có | 0 |
| cường | B-DISEASESYMTOM |
| giáp | I-DISEASESYMTOM |
| hay | 0 |
| không | 0 |
| phải | 0 |
| cường | B-DISEASESYMTOM |
| giáp | I-DISEASESYMTOM |
| là | 0 |
| một | 0 |
| cái | 0 |
| yếu | 0 |
| tố | 0 |
| nó | 0 |
| kích | 0 |
| động | 0 |
| trái | B-ORGAN |
| tim | I-ORGAN |
| lên | 0 |
| chúng | 0 |
| ta | 0 |
| và | 0 |
| nó | 0 |
| sẽ | 0 |
| gây | 0 |
| ra | 0 |
| tình | 0 |
| trạng | 0 |

## VM600-242 — dòng train 1904 (đếm từ 0)

ngừa dại hay không và nếu được tiêm thì

| Token | Nhãn gốc |
|---|---|
| ngừa | B-PREVENTIVEMED |
| dại | I-PREVENTIVEMED |
| hay | 0 |
| không | 0 |
| và | 0 |
| nếu | 0 |
| được | 0 |
| tiêm | B-MEDDEVICETECHNIQUE |
| thì | 0 |

## VM600-243 — dòng train 1906 (đếm từ 0)

chưa biết là huyết áp của bác thế nào mỡ máu ra sao có đái tháo đường không nhưng mà khi chúng ta bị tai biến một lần thì

| Token | Nhãn gốc |
|---|---|
| chưa | 0 |
| biết | 0 |
| là | 0 |
| huyết | B-DISEASESYMTOM |
| áp | I-DISEASESYMTOM |
| của | 0 |
| bác | B-AGE |
| thế | 0 |
| nào | 0 |
| mỡ | B-DISEASESYMTOM |
| máu | I-DISEASESYMTOM |
| ra | 0 |
| sao | 0 |
| có | 0 |
| đái | B-DISEASESYMTOM |
| tháo | I-DISEASESYMTOM |
| đường | I-DISEASESYMTOM |
| không | 0 |
| nhưng | 0 |
| mà | 0 |
| khi | 0 |
| chúng | 0 |
| ta | 0 |
| bị | 0 |
| tai | B-DISEASESYMTOM |
| biến | I-DISEASESYMTOM |
| một | 0 |
| lần | 0 |
| thì | 0 |

## VM600-244 — dòng train 1909 (đếm từ 0)

tình trạng là huyết áp cao mỡ máu cao rồi những cái bệnh lý mà chúng ta khiến cho tim mạch nè chúng ta bị mất ổn định

| Token | Nhãn gốc |
|---|---|
| tình | 0 |
| trạng | 0 |
| là | 0 |
| huyết | B-DISEASESYMTOM |
| áp | I-DISEASESYMTOM |
| cao | B-UNITCALIBRATOR |
| mỡ | B-DISEASESYMTOM |
| máu | I-DISEASESYMTOM |
| cao | B-UNITCALIBRATOR |
| rồi | 0 |
| những | 0 |
| cái | 0 |
| bệnh | 0 |
| lý | 0 |
| mà | 0 |
| chúng | 0 |
| ta | 0 |
| khiến | 0 |
| cho | 0 |
| tim | B-ORGAN |
| mạch | I-ORGAN |
| nè | 0 |
| chúng | 0 |
| ta | 0 |
| bị | 0 |
| mất | 0 |
| ổn | 0 |
| định | 0 |

## VM600-245 — dòng train 1911 (đếm từ 0)

lại bình thường trước đây tôi cũng có một cô bạn cô mới giới thiệu cho tôi đông trùng hạ

| Token | Nhãn gốc |
|---|---|
| lại | 0 |
| bình | 0 |
| thường | 0 |
| trước | 0 |
| đây | 0 |
| tôi | 0 |
| cũng | 0 |
| có | 0 |
| một | 0 |
| cô | B-GENDER |
| bạn | 0 |
| cô | B-GENDER |
| mới | 0 |
| giới | 0 |
| thiệu | 0 |
| cho | 0 |
| tôi | 0 |
| đông | B-FOODDRINK |
| trùng | I-FOODDRINK |
| hạ | 0 |

## VM600-246 — dòng train 1917 (đếm từ 0)

chia hai lần sáng chiều còn từ tháng thứ ba trở đi chúng ta có thể uống hai viên chia lần sáng chiều cái điều đó thì nó

| Token | Nhãn gốc |
|---|---|
| chia | 0 |
| hai | B-UNITCALIBRATOR |
| lần | I-UNITCALIBRATOR |
| sáng | B-DATETIME |
| chiều | I-DATETIME |
| còn | 0 |
| từ | 0 |
| tháng | 0 |
| thứ | 0 |
| ba | 0 |
| trở | 0 |
| đi | 0 |
| chúng | 0 |
| ta | 0 |
| có | 0 |
| thể | 0 |
| uống | 0 |
| hai | B-UNITCALIBRATOR |
| viên | I-UNITCALIBRATOR |
| chia | 0 |
| lần | 0 |
| sáng | B-DATETIME |
| chiều | I-DATETIME |
| cái | 0 |
| điều | 0 |
| đó | 0 |
| thì | 0 |
| nó | 0 |

## VM600-247 — dòng train 1922 (đếm từ 0)

fumarate đây là một cái sản phẩm mà cũng đã được chứng minh rằng nó có tác dụng là giúp cho cái giảm cái nguy cơ hình

| Token | Nhãn gốc |
|---|---|
| fumarate | B-DRUGCHEMICAL |
| đây | 0 |
| là | 0 |
| một | 0 |
| cái | 0 |
| sản | 0 |
| phẩm | 0 |
| mà | 0 |
| cũng | 0 |
| đã | 0 |
| được | 0 |
| chứng | 0 |
| minh | 0 |
| rằng | 0 |
| nó | 0 |
| có | 0 |
| tác | 0 |
| dụng | 0 |
| là | 0 |
| giúp | 0 |
| cho | 0 |
| cái | 0 |
| giảm | 0 |
| cái | 0 |
| nguy | 0 |
| cơ | 0 |
| hình | 0 |

## VM600-248 — dòng train 1928 (đếm từ 0)

nước anh đều mô tả bệnh dại là tử vong thời gian

| Token | Nhãn gốc |
|---|---|
| nước | B-LOCATION |
| anh | I-LOCATION |
| đều | 0 |
| mô | B-ORGAN |
| tả | 0 |
| bệnh | B-DISEASESYMTOM |
| dại | I-DISEASESYMTOM |
| là | 0 |
| tử | B-DISEASESYMTOM |
| vong | I-DISEASESYMTOM |
| thời | B-DATETIME |
| gian | I-DATETIME |

## VM600-249 — dòng train 1936 (đếm từ 0)

bác sĩ chuyên khoa bị rối loạn vận động sẽ có một cái quan điểm khám và đánh giá để người ta tiên lượng được thứ nhất

| Token | Nhãn gốc |
|---|---|
| bác | B-OCCUPATION |
| sĩ | I-OCCUPATION |
| chuyên | I-OCCUPATION |
| khoa | I-OCCUPATION |
| bị | 0 |
| rối | B-DISEASESYMTOM |
| loạn | I-DISEASESYMTOM |
| vận | I-DISEASESYMTOM |
| động | I-DISEASESYMTOM |
| sẽ | 0 |
| có | 0 |
| một | 0 |
| cái | 0 |
| quan | 0 |
| điểm | 0 |
| khám | B-DIAGNOSTICS |
| và | 0 |
| đánh | B-TREATMENT |
| giá | I-TREATMENT |
| để | 0 |
| người | 0 |
| ta | 0 |
| tiên | 0 |
| lượng | 0 |
| được | 0 |
| thứ | B-UNITCALIBRATOR |
| nhất | I-UNITCALIBRATOR |

## VM600-250 — dòng train 1949 (đếm từ 0)

là các triệu chứng như là đau đầu hoa mắt chóng mặt của bác này hay là những cái dấu hiệu tim đập hồi hộp trống

| Token | Nhãn gốc |
|---|---|
| là | 0 |
| các | 0 |
| triệu | B-DISEASESYMTOM |
| chứng | I-DISEASESYMTOM |
| như | 0 |
| là | 0 |
| đau | B-DISEASESYMTOM |
| đầu | I-DISEASESYMTOM |
| hoa | B-DISEASESYMTOM |
| mắt | I-DISEASESYMTOM |
| chóng | B-DISEASESYMTOM |
| mặt | I-DISEASESYMTOM |
| của | 0 |
| bác | B-AGE |
| này | 0 |
| hay | 0 |
| là | 0 |
| những | 0 |
| cái | 0 |
| dấu | 0 |
| hiệu | 0 |
| tim | B-ORGAN |
| đập | 0 |
| hồi | 0 |
| hộp | 0 |
| trống | 0 |

## VM600-251 — dòng train 1952 (đếm từ 0)

thì chúng ta phải giải quyết những yếu tố nguy cơ đó để chúng ta đừng bị rung nhĩ và một khi mà đã bị rung nhĩ rồi đó

| Token | Nhãn gốc |
|---|---|
| thì | 0 |
| chúng | 0 |
| ta | 0 |
| phải | 0 |
| giải | 0 |
| quyết | 0 |
| những | 0 |
| yếu | 0 |
| tố | 0 |
| nguy | 0 |
| cơ | 0 |
| đó | 0 |
| để | 0 |
| chúng | 0 |
| ta | 0 |
| đừng | 0 |
| bị | 0 |
| rung | B-DISEASESYMTOM |
| nhĩ | I-DISEASESYMTOM |
| và | 0 |
| một | 0 |
| khi | 0 |
| mà | 0 |
| đã | 0 |
| bị | 0 |
| rung | B-DISEASESYMTOM |
| nhĩ | I-DISEASESYMTOM |
| rồi | 0 |
| đó | 0 |

## VM600-252 — dòng train 1963 (đếm từ 0)

đường huyết hiện nay tân dược là càng ngày nó càng phát triển càng ngày nó càng phong phú và rất nhiều loại rất là

| Token | Nhãn gốc |
|---|---|
| đường | B-UNITCALIBRATOR |
| huyết | I-UNITCALIBRATOR |
| hiện | B-DATETIME |
| nay | I-DATETIME |
| tân | B-DRUGCHEMICAL |
| dược | I-DRUGCHEMICAL |
| là | 0 |
| càng | 0 |
| ngày | 0 |
| nó | 0 |
| càng | 0 |
| phát | 0 |
| triển | 0 |
| càng | 0 |
| ngày | 0 |
| nó | 0 |
| càng | 0 |
| phong | 0 |
| phú | 0 |
| và | 0 |
| rất | B-UNITCALIBRATOR |
| nhiều | I-UNITCALIBRATOR |
| loại | 0 |
| rất | 0 |
| là | 0 |

## VM600-253 — dòng train 1964 (đếm từ 0)

điểm nữa thì họ thường thường là bị tự ti tự ti nó khác với chữ tự tin hay là

| Token | Nhãn gốc |
|---|---|
| điểm | 0 |
| nữa | 0 |
| thì | 0 |
| họ | 0 |
| thường | 0 |
| thường | 0 |
| là | 0 |
| bị | 0 |
| tự | B-DISEASESYMTOM |
| ti | I-DISEASESYMTOM |
| tự | B-DISEASESYMTOM |
| ti | I-DISEASESYMTOM |
| nó | 0 |
| khác | 0 |
| với | 0 |
| chữ | 0 |
| tự | 0 |
| tin | 0 |
| hay | 0 |
| là | 0 |

## VM600-254 — dòng train 1974 (đếm từ 0)

nói tỷ lệ tử vong của bệnh nhân được giảm nhưng mà vấn đề chỗ là cái tỷ lệ

| Token | Nhãn gốc |
|---|---|
| nói | 0 |
| tỷ | B-UNITCALIBRATOR |
| lệ | I-UNITCALIBRATOR |
| tử | B-DISEASESYMTOM |
| vong | I-DISEASESYMTOM |
| của | 0 |
| bệnh | B-OCCUPATION |
| nhân | I-OCCUPATION |
| được | 0 |
| giảm | 0 |
| nhưng | 0 |
| mà | 0 |
| vấn | 0 |
| đề | 0 |
| chỗ | 0 |
| là | 0 |
| cái | B-UNITCALIBRATOR |
| tỷ | I-UNITCALIBRATOR |
| lệ | I-UNITCALIBRATOR |

## VM600-255 — dòng train 1979 (đếm từ 0)

việc này thử nghiệm lâm sàng đầu tiên được ghi nhận trong lịch sử miễn dịch

| Token | Nhãn gốc |
|---|---|
| việc | 0 |
| này | 0 |
| thử | B-TREATMENT |
| nghiệm | I-TREATMENT |
| lâm | I-TREATMENT |
| sàng | I-TREATMENT |
| đầu | 0 |
| tiên | 0 |
| được | 0 |
| ghi | 0 |
| nhận | 0 |
| trong | 0 |
| lịch | 0 |
| sử | 0 |
| miễn | 0 |
| dịch | 0 |

## VM600-256 — dòng train 1985 (đếm từ 0)

thuật cũng không có ngăn sự tiến triển của bệnh được và dĩ nhiên hiệu quả của

| Token | Nhãn gốc |
|---|---|
| thuật | 0 |
| cũng | 0 |
| không | 0 |
| có | 0 |
| ngăn | 0 |
| sự | 0 |
| tiến | 0 |
| triển | 0 |
| của | 0 |
| bệnh | 0 |
| được | 0 |
| và | 0 |
| dĩ | 0 |
| nhiên | 0 |
| hiệu | 0 |
| quả | 0 |
| của | 0 |

## VM600-257 — dòng train 1988 (đếm từ 0)

thì mình có cái giải pháp ngay lập tức là như nào cá nhân tôi chẳng hạn bây giờ tôi chưa bị như bác đâu nhưng mà đi lúc

| Token | Nhãn gốc |
|---|---|
| thì | 0 |
| mình | 0 |
| có | 0 |
| cái | 0 |
| giải | 0 |
| pháp | 0 |
| ngay | 0 |
| lập | 0 |
| tức | 0 |
| là | 0 |
| như | 0 |
| nào | 0 |
| cá | 0 |
| nhân | 0 |
| tôi | 0 |
| chẳng | 0 |
| hạn | 0 |
| bây | B-DATETIME |
| giờ | I-DATETIME |
| tôi | 0 |
| chưa | 0 |
| bị | 0 |
| như | 0 |
| bác | B-AGE |
| đâu | 0 |
| nhưng | 0 |
| mà | 0 |
| đi | 0 |
| lúc | 0 |

## VM600-258 — dòng train 1995 (đếm từ 0)

nguyên nhân cơ chế bệnh sinh đó chính là nó không tác động vào được làm mất đi làm giảm cái mảng xơ vữa nên là cái hiệu

| Token | Nhãn gốc |
|---|---|
| nguyên | 0 |
| nhân | 0 |
| cơ | 0 |
| chế | 0 |
| bệnh | 0 |
| sinh | 0 |
| đó | 0 |
| chính | 0 |
| là | 0 |
| nó | 0 |
| không | 0 |
| tác | 0 |
| động | 0 |
| vào | 0 |
| được | 0 |
| làm | 0 |
| mất | 0 |
| đi | 0 |
| làm | 0 |
| giảm | 0 |
| cái | 0 |
| mảng | B-DISEASESYMTOM |
| xơ | I-DISEASESYMTOM |
| vữa | I-DISEASESYMTOM |
| nên | 0 |
| là | 0 |
| cái | 0 |
| hiệu | 0 |

## VM600-259 — dòng train 2011 (đếm từ 0)

những người xung quanh đối với những thành viên những người thân trong gia đình thì tôi nghĩ rằng là làm sao để cho

| Token | Nhãn gốc |
|---|---|
| những | 0 |
| người | 0 |
| xung | 0 |
| quanh | 0 |
| đối | 0 |
| với | 0 |
| những | 0 |
| thành | 0 |
| viên | 0 |
| những | 0 |
| người | 0 |
| thân | 0 |
| trong | 0 |
| gia | 0 |
| đình | 0 |
| thì | 0 |
| tôi | 0 |
| nghĩ | 0 |
| rằng | 0 |
| là | 0 |
| làm | 0 |
| sao | 0 |
| để | 0 |
| cho | 0 |

## VM600-260 — dòng train 2013 (đếm từ 0)

tục ví dụ như là về những cái bài tập ví dụ như những cái hỗ trợ về điều trị

| Token | Nhãn gốc |
|---|---|
| tục | 0 |
| ví | 0 |
| dụ | 0 |
| như | 0 |
| là | 0 |
| về | 0 |
| những | 0 |
| cái | 0 |
| bài | 0 |
| tập | 0 |
| ví | 0 |
| dụ | 0 |
| như | 0 |
| những | 0 |
| cái | 0 |
| hỗ | B-MEDDEVICETECHNIQUE |
| trợ | I-MEDDEVICETECHNIQUE |
| về | 0 |
| điều | B-TREATMENT |
| trị | I-TREATMENT |

## VM600-261 — dòng train 2018 (đếm từ 0)

vào phòng ở can thiệp để mà luồn cái dụng cụ vào để mà lấy cái cục khối ra

| Token | Nhãn gốc |
|---|---|
| vào | 0 |
| phòng | B-LOCATION |
| ở | I-LOCATION |
| can | B-PREVENTIVEMED |
| thiệp | I-PREVENTIVEMED |
| để | 0 |
| mà | 0 |
| luồn | B-DIAGNOSTICS |
| cái | I-DIAGNOSTICS |
| dụng | I-DIAGNOSTICS |
| cụ | I-DIAGNOSTICS |
| vào | 0 |
| để | 0 |
| mà | 0 |
| lấy | B-SURGERY |
| cái | I-SURGERY |
| cục | I-SURGERY |
| khối | I-SURGERY |
| ra | I-SURGERY |

## VM600-262 — dòng train 2036 (đếm từ 0)

là vấn đề các cái chất cái vitamin và chất khoáng đến từ rau và củ quả thì

| Token | Nhãn gốc |
|---|---|
| là | 0 |
| vấn | 0 |
| đề | 0 |
| các | 0 |
| cái | 0 |
| chất | 0 |
| cái | 0 |
| vitamin | B-DRUGCHEMICAL |
| và | 0 |
| chất | B-DRUGCHEMICAL |
| khoáng | I-DRUGCHEMICAL |
| đến | 0 |
| từ | 0 |
| rau | 0 |
| và | 0 |
| củ | 0 |
| quả | 0 |
| thì | 0 |

## VM600-263 — dòng train 2038 (đếm từ 0)

ta thường xuyên quá mức như vậy thì nó cũng gây rụng tóc rồi nó có một cái mà chúng ta không thể nào không để mặc dù

| Token | Nhãn gốc |
|---|---|
| ta | 0 |
| thường | B-DATETIME |
| xuyên | I-DATETIME |
| quá | 0 |
| mức | 0 |
| như | 0 |
| vậy | 0 |
| thì | 0 |
| nó | 0 |
| cũng | 0 |
| gây | 0 |
| rụng | B-DISEASESYMTOM |
| tóc | I-DISEASESYMTOM |
| rồi | 0 |
| nó | 0 |
| có | 0 |
| một | 0 |
| cái | 0 |
| mà | 0 |
| chúng | 0 |
| ta | 0 |
| không | 0 |
| thể | 0 |
| nào | 0 |
| không | 0 |
| để | 0 |
| mặc | 0 |
| dù | 0 |

## VM600-264 — dòng train 2040 (đếm từ 0)

những câu chuyện này hàng ngày và tôi biết rằng bạn cũng có thể thay đổi tích cực số phận của bộ não thông qua sức

| Token | Nhãn gốc |
|---|---|
| những | 0 |
| câu | 0 |
| chuyện | 0 |
| này | 0 |
| hàng | B-DATETIME |
| ngày | I-DATETIME |
| và | 0 |
| tôi | 0 |
| biết | 0 |
| rằng | 0 |
| bạn | 0 |
| cũng | 0 |
| có | 0 |
| thể | 0 |
| thay | 0 |
| đổi | 0 |
| tích | 0 |
| cực | 0 |
| số | 0 |
| phận | 0 |
| của | 0 |
| bộ | B-ORGAN |
| não | I-ORGAN |
| thông | 0 |
| qua | 0 |
| sức | 0 |

## VM600-265 — dòng train 2060 (đếm từ 0)

da chúng ta là mất màu trắng hoàn toàn luôn ra từ nâu hoặc là màu vàng chuyển sang màu trắng luôn ngoài ra còn có thể

| Token | Nhãn gốc |
|---|---|
| da | B-ORGAN |
| chúng | 0 |
| ta | 0 |
| là | 0 |
| mất | B-DISEASESYMTOM |
| màu | I-DISEASESYMTOM |
| trắng | I-DISEASESYMTOM |
| hoàn | 0 |
| toàn | 0 |
| luôn | 0 |
| ra | 0 |
| từ | 0 |
| nâu | 0 |
| hoặc | 0 |
| là | 0 |
| màu | 0 |
| vàng | 0 |
| chuyển | 0 |
| sang | 0 |
| màu | 0 |
| trắng | 0 |
| luôn | 0 |
| ngoài | 0 |
| ra | 0 |
| còn | 0 |
| có | 0 |
| thể | 0 |

## VM600-266 — dòng train 2064 (đếm từ 0)

khem cái thứ ba là phải tập luyện muốn nói gì thì nói cuộc sống là vận động sự sống mà không có vận động thì nó sẽ càng

| Token | Nhãn gốc |
|---|---|
| khem | 0 |
| cái | 0 |
| thứ | 0 |
| ba | 0 |
| là | 0 |
| phải | 0 |
| tập | 0 |
| luyện | 0 |
| muốn | 0 |
| nói | 0 |
| gì | 0 |
| thì | 0 |
| nói | 0 |
| cuộc | 0 |
| sống | 0 |
| là | 0 |
| vận | 0 |
| động | 0 |
| sự | 0 |
| sống | 0 |
| mà | 0 |
| không | 0 |
| có | 0 |
| vận | 0 |
| động | 0 |
| thì | 0 |
| nó | 0 |
| sẽ | 0 |
| càng | 0 |

## VM600-267 — dòng train 2069 (đếm từ 0)

trạng bao gồm cả trầm cảm và lo âu tiểu đường thèm đường và carbohydrate thừa cân

| Token | Nhãn gốc |
|---|---|
| trạng | 0 |
| bao | 0 |
| gồm | 0 |
| cả | 0 |
| trầm | B-DISEASESYMTOM |
| cảm | I-DISEASESYMTOM |
| và | 0 |
| lo | B-DISEASESYMTOM |
| âu | I-DISEASESYMTOM |
| tiểu | B-DISEASESYMTOM |
| đường | I-DISEASESYMTOM |
| thèm | 0 |
| đường | 0 |
| và | 0 |
| carbohydrate | B-DRUGCHEMICAL |
| thừa | B-DISEASESYMTOM |
| cân | I-DISEASESYMTOM |

## VM600-268 — dòng train 2081 (đếm từ 0)

tế bào miễn dịch của con người ở những chi tiết nhỏ chính tôi đã nhìn thấy cách khoa học biểu lộ vẻ đẹp dù nó vẫn còn ẩn

| Token | Nhãn gốc |
|---|---|
| tế | B-ORGAN |
| bào | I-ORGAN |
| miễn | 0 |
| dịch | 0 |
| của | 0 |
| con | 0 |
| người | 0 |
| ở | 0 |
| những | 0 |
| chi | 0 |
| tiết | 0 |
| nhỏ | 0 |
| chính | 0 |
| tôi | 0 |
| đã | 0 |
| nhìn | 0 |
| thấy | 0 |
| cách | 0 |
| khoa | 0 |
| học | 0 |
| biểu | 0 |
| lộ | 0 |
| vẻ | 0 |
| đẹp | 0 |
| dù | 0 |
| nó | 0 |
| vẫn | 0 |
| còn | 0 |
| ẩn | 0 |

## VM600-269 — dòng train 2094 (đếm từ 0)

cải thiện mà cái điều này là chúng tôi cũng nói đi nói lại rất là nhiều nhưng

| Token | Nhãn gốc |
|---|---|
| cải | B-TREATMENT |
| thiện | I-TREATMENT |
| mà | 0 |
| cái | 0 |
| điều | 0 |
| này | 0 |
| là | 0 |
| chúng | 0 |
| tôi | 0 |
| cũng | 0 |
| nói | 0 |
| đi | 0 |
| nói | 0 |
| lại | 0 |
| rất | 0 |
| là | 0 |
| nhiều | 0 |
| nhưng | 0 |

## VM600-270 — dòng train 2122 (đếm từ 0)

phải kiêng tuyệt đối nhưng chúng ta chỉ nên ăn dưới năm mươi gam thịt đỏ một người một ngày thôi khi mà chúng ta bị ung thư bởi

| Token | Nhãn gốc |
|---|---|
| phải | 0 |
| kiêng | 0 |
| tuyệt | 0 |
| đối | 0 |
| nhưng | 0 |
| chúng | 0 |
| ta | 0 |
| chỉ | 0 |
| nên | 0 |
| ăn | 0 |
| dưới | 0 |
| năm | B-UNITCALIBRATOR |
| mươi | I-UNITCALIBRATOR |
| gam | 0 |
| thịt | B-FOODDRINK |
| đỏ | I-FOODDRINK |
| một | B-UNITCALIBRATOR |
| người | I-UNITCALIBRATOR |
| một | B-DATETIME |
| ngày | I-DATETIME |
| thôi | 0 |
| khi | 0 |
| mà | 0 |
| chúng | 0 |
| ta | 0 |
| bị | 0 |
| ung | B-DISEASESYMTOM |
| thư | I-DISEASESYMTOM |
| bởi | 0 |

## VM600-271 — dòng train 2125 (đếm từ 0)

nhưng mà tôi rất là sợ phải đi lấy mẫu vì sợ lây nhiễm lẫn nhau ở tại các khu

| Token | Nhãn gốc |
|---|---|
| nhưng | 0 |
| mà | 0 |
| tôi | 0 |
| rất | 0 |
| là | 0 |
| sợ | 0 |
| phải | 0 |
| đi | 0 |
| lấy | B-MEDDEVICETECHNIQUE |
| mẫu | I-MEDDEVICETECHNIQUE |
| vì | 0 |
| sợ | 0 |
| lây | B-DISEASESYMTOM |
| nhiễm | I-DISEASESYMTOM |
| lẫn | 0 |
| nhau | 0 |
| ở | 0 |
| tại | 0 |
| các | 0 |
| khu | 0 |

## VM600-272 — dòng train 2138 (đếm từ 0)

nhiễm chéo thì như tôi cũng đã trình bày đầu chương trình đó là virus nó không có tự đi mà nó do chúng ta mang theo mà

| Token | Nhãn gốc |
|---|---|
| nhiễm | 0 |
| chéo | 0 |
| thì | 0 |
| như | 0 |
| tôi | 0 |
| cũng | 0 |
| đã | 0 |
| trình | 0 |
| bày | 0 |
| đầu | 0 |
| chương | 0 |
| trình | 0 |
| đó | 0 |
| là | 0 |
| virus | B-DISEASESYMTOM |
| nó | 0 |
| không | 0 |
| có | 0 |
| tự | 0 |
| đi | 0 |
| mà | 0 |
| nó | 0 |
| do | 0 |
| chúng | 0 |
| ta | 0 |
| mang | 0 |
| theo | 0 |
| mà | 0 |

## VM600-273 — dòng train 2141 (đếm từ 0)

động mạch thì mình vẫn hoàn toàn có thể sử dụng sớm để ngăn ngừa cái tình trạng xơ vữa động mạch nó có thể xuất hiện rất

| Token | Nhãn gốc |
|---|---|
| động | B-ORGAN |
| mạch | I-ORGAN |
| thì | 0 |
| mình | 0 |
| vẫn | 0 |
| hoàn | 0 |
| toàn | 0 |
| có | 0 |
| thể | 0 |
| sử | 0 |
| dụng | 0 |
| sớm | 0 |
| để | 0 |
| ngăn | B-PREVENTIVEMED |
| ngừa | I-PREVENTIVEMED |
| cái | 0 |
| tình | B-DISEASESYMTOM |
| trạng | I-DISEASESYMTOM |
| xơ | I-DISEASESYMTOM |
| vữa | I-DISEASESYMTOM |
| động | I-DISEASESYMTOM |
| mạch | I-DISEASESYMTOM |
| nó | 0 |
| có | 0 |
| thể | 0 |
| xuất | 0 |
| hiện | 0 |
| rất | 0 |

## VM600-274 — dòng train 2151 (đếm từ 0)

bối cảnh chung cùng với các chuyên khoa khác chứ không tách rời ra thứ hai trong cái việc mà điều trị bằng thuốc

| Token | Nhãn gốc |
|---|---|
| bối | 0 |
| cảnh | 0 |
| chung | 0 |
| cùng | 0 |
| với | 0 |
| các | 0 |
| chuyên | B-LOCATION |
| khoa | I-LOCATION |
| khác | 0 |
| chứ | 0 |
| không | 0 |
| tách | 0 |
| rời | 0 |
| ra | 0 |
| thứ | 0 |
| hai | 0 |
| trong | 0 |
| cái | 0 |
| việc | 0 |
| mà | 0 |
| điều | B-TREATMENT |
| trị | I-TREATMENT |
| bằng | 0 |
| thuốc | B-DRUGCHEMICAL |

## VM600-275 — dòng train 2153 (đếm từ 0)

xe đạp trên giường chứ tuyệt nhiên là chúng ta không vì thế mà chúng ta lại cứ đi nhiều thế còn cái việc mà hôm nay

| Token | Nhãn gốc |
|---|---|
| xe | B-TRANSPORTATION |
| đạp | I-TRANSPORTATION |
| trên | 0 |
| giường | 0 |
| chứ | 0 |
| tuyệt | 0 |
| nhiên | 0 |
| là | 0 |
| chúng | 0 |
| ta | 0 |
| không | 0 |
| vì | 0 |
| thế | 0 |
| mà | 0 |
| chúng | 0 |
| ta | 0 |
| lại | 0 |
| cứ | 0 |
| đi | 0 |
| nhiều | 0 |
| thế | 0 |
| còn | 0 |
| cái | 0 |
| việc | 0 |
| mà | 0 |
| hôm | B-DATETIME |
| nay | I-DATETIME |

## VM600-276 — dòng train 2178 (đếm từ 0)

người ta là sức khỏe và trí tuệ có sức khỏe thì mới có trí tuệ và hiện nay thì

| Token | Nhãn gốc |
|---|---|
| người | 0 |
| ta | 0 |
| là | 0 |
| sức | 0 |
| khỏe | 0 |
| và | 0 |
| trí | 0 |
| tuệ | 0 |
| có | 0 |
| sức | 0 |
| khỏe | 0 |
| thì | 0 |
| mới | 0 |
| có | 0 |
| trí | 0 |
| tuệ | 0 |
| và | 0 |
| hiện | B-DATETIME |
| nay | I-DATETIME |
| thì | 0 |

## VM600-277 — dòng train 2181 (đếm từ 0)

khác nhau và theo như lời chia sẻ của các bác sĩ thì khi thuốc không còn kiểm

| Token | Nhãn gốc |
|---|---|
| khác | 0 |
| nhau | 0 |
| và | 0 |
| theo | 0 |
| như | 0 |
| lời | 0 |
| chia | 0 |
| sẻ | 0 |
| của | 0 |
| các | 0 |
| bác | B-OCCUPATION |
| sĩ | I-OCCUPATION |
| thì | 0 |
| khi | 0 |
| thuốc | B-DRUGCHEMICAL |
| không | 0 |
| còn | 0 |
| kiểm | 0 |

## VM600-278 — dòng train 2187 (đếm từ 0)

thậm chí là thất vọng với bản thân mình cảm thấy là ôi thất bại rồi thất bại rồi thì có người coi đây đó là những cái

| Token | Nhãn gốc |
|---|---|
| thậm | 0 |
| chí | 0 |
| là | 0 |
| thất | 0 |
| vọng | 0 |
| với | 0 |
| bản | 0 |
| thân | 0 |
| mình | 0 |
| cảm | 0 |
| thấy | 0 |
| là | 0 |
| ôi | 0 |
| thất | 0 |
| bại | 0 |
| rồi | 0 |
| thất | 0 |
| bại | 0 |
| rồi | 0 |
| thì | 0 |
| có | 0 |
| người | 0 |
| coi | 0 |
| đây | 0 |
| đó | 0 |
| là | 0 |
| những | 0 |
| cái | 0 |

## VM600-279 — dòng train 2189 (đếm từ 0)

giá thêm đúng là rung nhĩ đánh giá đến mức độ của nó đánh giá nguy cơ là như thế nào và thậm chí đánh giá các nguyên

| Token | Nhãn gốc |
|---|---|
| giá | 0 |
| thêm | 0 |
| đúng | 0 |
| là | 0 |
| rung | B-DISEASESYMTOM |
| nhĩ | I-DISEASESYMTOM |
| đánh | B-TREATMENT |
| giá | I-TREATMENT |
| đến | 0 |
| mức | B-UNITCALIBRATOR |
| độ | I-UNITCALIBRATOR |
| của | 0 |
| nó | 0 |
| đánh | B-DIAGNOSTICS |
| giá | I-DIAGNOSTICS |
| nguy | I-DIAGNOSTICS |
| cơ | I-DIAGNOSTICS |
| là | 0 |
| như | 0 |
| thế | 0 |
| nào | 0 |
| và | 0 |
| thậm | 0 |
| chí | 0 |
| đánh | B-TREATMENT |
| giá | I-TREATMENT |
| các | 0 |
| nguyên | 0 |

## VM600-280 — dòng train 2196 (đếm từ 0)

kẻ thua cuộc chúng ta đã học được rằng một phần của vấn đề là người cao tuổi có

| Token | Nhãn gốc |
|---|---|
| kẻ | 0 |
| thua | 0 |
| cuộc | 0 |
| chúng | 0 |
| ta | 0 |
| đã | 0 |
| học | 0 |
| được | 0 |
| rằng | 0 |
| một | B-UNITCALIBRATOR |
| phần | I-UNITCALIBRATOR |
| của | 0 |
| vấn | 0 |
| đề | 0 |
| là | 0 |
| người | 0 |
| cao | B-AGE |
| tuổi | I-AGE |
| có | 0 |

## VM600-281 — dòng train 2204 (đếm từ 0)

phương thức tiếp cận trên cái thực tế thì các bước quản lý về duy trì cân nặng ổn định đó thì nhiều khi nó còn rất là

| Token | Nhãn gốc |
|---|---|
| phương | 0 |
| thức | 0 |
| tiếp | 0 |
| cận | 0 |
| trên | 0 |
| cái | 0 |
| thực | 0 |
| tế | 0 |
| thì | 0 |
| các | 0 |
| bước | 0 |
| quản | 0 |
| lý | 0 |
| về | 0 |
| duy | B-PERSONALCARE |
| trì | I-PERSONALCARE |
| cân | 0 |
| nặng | 0 |
| ổn | 0 |
| định | 0 |
| đó | 0 |
| thì | 0 |
| nhiều | 0 |
| khi | 0 |
| nó | 0 |
| còn | 0 |
| rất | 0 |
| là | 0 |

## VM600-282 — dòng train 2211 (đếm từ 0)

xưa thì các cụ là dùng toàn thể hoặc có thể dùng vỏ quả thể nhưng mà cho đến hiện nay khi mà nghiên cứu các thành

| Token | Nhãn gốc |
|---|---|
| xưa | 0 |
| thì | 0 |
| các | 0 |
| cụ | B-AGE |
| là | 0 |
| dùng | 0 |
| toàn | 0 |
| thể | 0 |
| hoặc | 0 |
| có | 0 |
| thể | 0 |
| dùng | 0 |
| vỏ | B-DRUGCHEMICAL |
| quả | I-DRUGCHEMICAL |
| thể | I-DRUGCHEMICAL |
| nhưng | 0 |
| mà | 0 |
| cho | 0 |
| đến | 0 |
| hiện | B-DATETIME |
| nay | I-DATETIME |
| khi | 0 |
| mà | 0 |
| nghiên | B-DIAGNOSTICS |
| cứu | I-DIAGNOSTICS |
| các | 0 |
| thành | 0 |

## VM600-283 — dòng train 2212 (đếm từ 0)

có thể nói là nó phát triển rất là dữ dội và nếu như người già thì chúng ta có thể nhờ con cháu của mình để có thể phối

| Token | Nhãn gốc |
|---|---|
| có | 0 |
| thể | 0 |
| nói | 0 |
| là | 0 |
| nó | 0 |
| phát | 0 |
| triển | 0 |
| rất | 0 |
| là | 0 |
| dữ | 0 |
| dội | 0 |
| và | 0 |
| nếu | 0 |
| như | 0 |
| người | B-AGE |
| già | I-AGE |
| thì | 0 |
| chúng | 0 |
| ta | 0 |
| có | 0 |
| thể | 0 |
| nhờ | 0 |
| con | 0 |
| cháu | B-AGE |
| của | 0 |
| mình | 0 |
| để | 0 |
| có | 0 |
| thể | 0 |
| phối | 0 |

## VM600-284 — dòng train 2215 (đếm từ 0)

cô lập càng xa lánh càng tránh né để mà

| Token | Nhãn gốc |
|---|---|
| cô | B-GENDER |
| lập | 0 |
| càng | 0 |
| xa | 0 |
| lánh | 0 |
| càng | 0 |
| tránh | 0 |
| né | 0 |
| để | 0 |
| mà | 0 |

## VM600-285 — dòng train 2216 (đếm từ 0)

là không có hương liệu không có chất bảo quản còn đối với kem dưỡng ẩm thì đối với lại dưỡng ẩm ban ngày thì sau khi

| Token | Nhãn gốc |
|---|---|
| là | 0 |
| không | 0 |
| có | 0 |
| hương | B-DRUGCHEMICAL |
| liệu | I-DRUGCHEMICAL |
| không | 0 |
| có | 0 |
| chất | B-DRUGCHEMICAL |
| bảo | I-DRUGCHEMICAL |
| quản | I-DRUGCHEMICAL |
| còn | 0 |
| đối | 0 |
| với | 0 |
| kem | B-DRUGCHEMICAL |
| dưỡng | I-DRUGCHEMICAL |
| ẩm | I-DRUGCHEMICAL |
| thì | 0 |
| đối | 0 |
| với | 0 |
| lại | 0 |
| dưỡng | B-PERSONALCARE |
| ẩm | I-PERSONALCARE |
| ban | B-DATETIME |
| ngày | I-DATETIME |
| thì | 0 |
| sau | 0 |
| khi | 0 |

## VM600-286 — dòng train 2219 (đếm từ 0)

bệnh nhân béo phì đến thì sẽ đưa ra các mục tiêu điều trị cho bệnh nhân thì các mục tiêu ngắn hạn đó là sẽ giảm từ năm

| Token | Nhãn gốc |
|---|---|
| bệnh | B-OCCUPATION |
| nhân | I-OCCUPATION |
| béo | B-DISEASESYMTOM |
| phì | I-DISEASESYMTOM |
| đến | 0 |
| thì | 0 |
| sẽ | 0 |
| đưa | 0 |
| ra | 0 |
| các | 0 |
| mục | 0 |
| tiêu | 0 |
| điều | B-TREATMENT |
| trị | I-TREATMENT |
| cho | 0 |
| bệnh | B-OCCUPATION |
| nhân | I-OCCUPATION |
| thì | 0 |
| các | 0 |
| mục | 0 |
| tiêu | 0 |
| ngắn | B-DATETIME |
| hạn | I-DATETIME |
| đó | 0 |
| là | 0 |
| sẽ | 0 |
| giảm | 0 |
| từ | 0 |
| năm | 0 |

## VM600-287 — dòng train 2228 (đếm từ 0)

cung cấp hay là cái nhu cầu và mức độ thỏa mãn cho nên khi mà mình có cái nhu cầu

| Token | Nhãn gốc |
|---|---|
| cung | 0 |
| cấp | 0 |
| hay | 0 |
| là | 0 |
| cái | 0 |
| nhu | 0 |
| cầu | 0 |
| và | 0 |
| mức | B-UNITCALIBRATOR |
| độ | I-UNITCALIBRATOR |
| thỏa | 0 |
| mãn | 0 |
| cho | 0 |
| nên | 0 |
| khi | 0 |
| mà | 0 |
| mình | 0 |
| có | 0 |
| cái | 0 |
| nhu | 0 |
| cầu | 0 |

## VM600-288 — dòng train 2237 (đếm từ 0)

điều hướng tất cả các lựa chọn là một việc hữu ích đặc biệt là khi bạn phải đối mặt với quảng cáo tốt cho đường ruột

| Token | Nhãn gốc |
|---|---|
| điều | 0 |
| hướng | 0 |
| tất | 0 |
| cả | 0 |
| các | 0 |
| lựa | 0 |
| chọn | 0 |
| là | 0 |
| một | 0 |
| việc | 0 |
| hữu | 0 |
| ích | 0 |
| đặc | 0 |
| biệt | 0 |
| là | 0 |
| khi | 0 |
| bạn | 0 |
| phải | 0 |
| đối | 0 |
| mặt | 0 |
| với | 0 |
| quảng | 0 |
| cáo | 0 |
| tốt | 0 |
| cho | 0 |
| đường | B-ORGAN |
| ruột | I-ORGAN |

## VM600-289 — dòng train 2251 (đếm từ 0)

hệ tác động qua lại hai chiều giữa tâm lý người bệnh và cái căn bệnh béo phì này đó nó thường khiến cho cái tình

| Token | Nhãn gốc |
|---|---|
| hệ | 0 |
| tác | 0 |
| động | 0 |
| qua | 0 |
| lại | 0 |
| hai | 0 |
| chiều | 0 |
| giữa | 0 |
| tâm | 0 |
| lý | 0 |
| người | 0 |
| bệnh | 0 |
| và | 0 |
| cái | 0 |
| căn | 0 |
| bệnh | 0 |
| béo | B-DISEASESYMTOM |
| phì | I-DISEASESYMTOM |
| này | 0 |
| đó | 0 |
| nó | 0 |
| thường | 0 |
| khiến | 0 |
| cho | 0 |
| cái | 0 |
| tình | 0 |

## VM600-290 — dòng train 2257 (đếm từ 0)

với nhóm chất béo chúng ta nên sử dụng chất béo từ các loại hạt chất

| Token | Nhãn gốc |
|---|---|
| với | 0 |
| nhóm | 0 |
| chất | B-DRUGCHEMICAL |
| béo | I-DRUGCHEMICAL |
| chúng | 0 |
| ta | 0 |
| nên | 0 |
| sử | 0 |
| dụng | 0 |
| chất | B-DRUGCHEMICAL |
| béo | I-DRUGCHEMICAL |
| từ | 0 |
| các | 0 |
| loại | 0 |
| hạt | 0 |
| chất | 0 |

## VM600-291 — dòng train 2261 (đếm từ 0)

bảy bạn đã cắt amidan chưa tám bạn đã

| Token | Nhãn gốc |
|---|---|
| bảy | 0 |
| bạn | 0 |
| đã | 0 |
| cắt | 0 |
| amidan | B-DISEASESYMTOM |
| chưa | 0 |
| tám | 0 |
| bạn | 0 |
| đã | 0 |

## VM600-292 — dòng train 2263 (đếm từ 0)

một số những cái vấn đề mà liên quan tới cái việc điều trị tâm lý ở trong cái

| Token | Nhãn gốc |
|---|---|
| một | 0 |
| số | 0 |
| những | 0 |
| cái | 0 |
| vấn | 0 |
| đề | 0 |
| mà | 0 |
| liên | 0 |
| quan | 0 |
| tới | 0 |
| cái | 0 |
| việc | 0 |
| điều | B-TREATMENT |
| trị | I-TREATMENT |
| tâm | 0 |
| lý | 0 |
| ở | 0 |
| trong | 0 |
| cái | 0 |

## VM600-293 — dòng train 2278 (đếm từ 0)

thể bị bất hoạt bởi nhiệt và một lượng nhỏ hóa chất formalin điều này có nghĩa

| Token | Nhãn gốc |
|---|---|
| thể | 0 |
| bị | 0 |
| bất | 0 |
| hoạt | 0 |
| bởi | 0 |
| nhiệt | 0 |
| và | 0 |
| một | 0 |
| lượng | 0 |
| nhỏ | 0 |
| hóa | B-DRUGCHEMICAL |
| chất | I-DRUGCHEMICAL |
| formalin | B-DRUGCHEMICAL |
| điều | 0 |
| này | 0 |
| có | 0 |
| nghĩa | 0 |

## VM600-294 — dòng train 2286 (đếm từ 0)

cái nghịch cảnh mình tạo ra để làm gì chị em biết là nếu mà mình có một cái

| Token | Nhãn gốc |
|---|---|
| cái | 0 |
| nghịch | 0 |
| cảnh | 0 |
| mình | 0 |
| tạo | 0 |
| ra | 0 |
| để | 0 |
| làm | 0 |
| gì | 0 |
| chị | B-GENDER |
| em | I-GENDER |
| biết | 0 |
| là | 0 |
| nếu | 0 |
| mà | 0 |
| mình | 0 |
| có | 0 |
| một | 0 |
| cái | 0 |

## VM600-295 — dòng train 2287 (đếm từ 0)

dụng cái chế độ ăn cháo và súp thì bao giờ nó cũng mềm lỏng hơn so với cơm giúp

| Token | Nhãn gốc |
|---|---|
| dụng | 0 |
| cái | 0 |
| chế | B-PERSONALCARE |
| độ | I-PERSONALCARE |
| ăn | I-PERSONALCARE |
| cháo | I-PERSONALCARE |
| và | I-PERSONALCARE |
| súp | I-PERSONALCARE |
| thì | 0 |
| bao | 0 |
| giờ | 0 |
| nó | 0 |
| cũng | 0 |
| mềm | 0 |
| lỏng | 0 |
| hơn | 0 |
| so | 0 |
| với | 0 |
| cơm | 0 |
| giúp | 0 |

## VM600-296 — dòng train 2288 (đếm từ 0)

chúng ta nó bệnh dại

| Token | Nhãn gốc |
|---|---|
| chúng | 0 |
| ta | 0 |
| nó | 0 |
| bệnh | B-DISEASESYMTOM |
| dại | I-DISEASESYMTOM |

## VM600-297 — dòng train 2294 (đếm từ 0)

dạ vâng chương trình đường truyền nó kém quá tóm lại hiện nay là cô bị tình trạng như

| Token | Nhãn gốc |
|---|---|
| dạ | 0 |
| vâng | 0 |
| chương | 0 |
| trình | 0 |
| đường | 0 |
| truyền | 0 |
| nó | 0 |
| kém | 0 |
| quá | 0 |
| tóm | 0 |
| lại | 0 |
| hiện | B-DATETIME |
| nay | I-DATETIME |
| là | 0 |
| cô | B-GENDER |
| bị | 0 |
| tình | 0 |
| trạng | 0 |
| như | 0 |

## VM600-298 — dòng train 2311 (đếm từ 0)

méo miệng yếu tay chân và giọng lời nói giọng nói có vấn đề thì đó

| Token | Nhãn gốc |
|---|---|
| méo | B-DISEASESYMTOM |
| miệng | I-DISEASESYMTOM |
| yếu | B-DISEASESYMTOM |
| tay | I-DISEASESYMTOM |
| chân | 0 |
| và | 0 |
| giọng | B-DISEASESYMTOM |
| lời | I-DISEASESYMTOM |
| nói | I-DISEASESYMTOM |
| giọng | I-DISEASESYMTOM |
| nói | I-DISEASESYMTOM |
| có | I-DISEASESYMTOM |
| vấn | I-DISEASESYMTOM |
| đề | I-DISEASESYMTOM |
| thì | 0 |
| đó | 0 |

## VM600-299 — dòng train 2315 (đếm từ 0)

nào như vậy thì bệnh nhân sẽ phải trước đó mình phải được tư vấn trong quá trình phải hợp tác với với bác sĩ ví dụ như

| Token | Nhãn gốc |
|---|---|
| nào | 0 |
| như | 0 |
| vậy | 0 |
| thì | 0 |
| bệnh | B-OCCUPATION |
| nhân | I-OCCUPATION |
| sẽ | 0 |
| phải | 0 |
| trước | 0 |
| đó | 0 |
| mình | 0 |
| phải | 0 |
| được | 0 |
| tư | B-PERSONALCARE |
| vấn | I-PERSONALCARE |
| trong | 0 |
| quá | 0 |
| trình | 0 |
| phải | 0 |
| hợp | 0 |
| tác | 0 |
| với | 0 |
| với | 0 |
| bác | B-OCCUPATION |
| sĩ | I-OCCUPATION |
| ví | 0 |
| dụ | 0 |
| như | 0 |

## VM600-300 — dòng train 2318 (đếm từ 0)

dinh dưỡng trong cơ thể chúng ta nó sản sinh ra các tế bào thì mỗi một cái tế bào ung thư điều rất cần đến năng lượng

| Token | Nhãn gốc |
|---|---|
| dinh | 0 |
| dưỡng | 0 |
| trong | 0 |
| cơ | B-ORGAN |
| thể | I-ORGAN |
| chúng | 0 |
| ta | 0 |
| nó | 0 |
| sản | 0 |
| sinh | 0 |
| ra | 0 |
| các | 0 |
| tế | B-ORGAN |
| bào | I-ORGAN |
| thì | 0 |
| mỗi | 0 |
| một | 0 |
| cái | 0 |
| tế | B-DISEASESYMTOM |
| bào | I-DISEASESYMTOM |
| ung | I-DISEASESYMTOM |
| thư | I-DISEASESYMTOM |
| điều | 0 |
| rất | 0 |
| cần | 0 |
| đến | 0 |
| năng | 0 |
| lượng | 0 |

## VM600-301 — dòng train 2322 (đếm từ 0)

do parkinson đa xơ cứng trầm cảm và sa sút trí tuệ đến các rối loạn tự miễn

| Token | Nhãn gốc |
|---|---|
| do | 0 |
| parkinson | B-DISEASESYMTOM |
| đa | B-DISEASESYMTOM |
| xơ | I-DISEASESYMTOM |
| cứng | I-DISEASESYMTOM |
| trầm | B-DISEASESYMTOM |
| cảm | I-DISEASESYMTOM |
| và | 0 |
| sa | B-DISEASESYMTOM |
| sút | I-DISEASESYMTOM |
| trí | I-DISEASESYMTOM |
| tuệ | I-DISEASESYMTOM |
| đến | 0 |
| các | 0 |
| rối | B-DISEASESYMTOM |
| loạn | I-DISEASESYMTOM |
| tự | 0 |
| miễn | 0 |

## VM600-302 — dòng train 2327 (đếm từ 0)

tưởng sử dụng để có thể là thực hiện sức khỏe cho chúng ta và đây cũng chính là một món quà thật là ý nghĩa dành tặng

| Token | Nhãn gốc |
|---|---|
| tưởng | 0 |
| sử | 0 |
| dụng | 0 |
| để | 0 |
| có | 0 |
| thể | 0 |
| là | 0 |
| thực | 0 |
| hiện | 0 |
| sức | 0 |
| khỏe | 0 |
| cho | 0 |
| chúng | 0 |
| ta | 0 |
| và | 0 |
| đây | 0 |
| cũng | 0 |
| chính | 0 |
| là | 0 |
| một | 0 |
| món | 0 |
| quà | 0 |
| thật | 0 |
| là | 0 |
| ý | 0 |
| nghĩa | 0 |
| dành | 0 |
| tặng | 0 |

## VM600-303 — dòng train 2329 (đếm từ 0)

bệnh nhân mà đái tháo đường mà không có kèm bệnh lý béo phì và cũng đã có rất là

| Token | Nhãn gốc |
|---|---|
| bệnh | B-OCCUPATION |
| nhân | I-OCCUPATION |
| mà | 0 |
| đái | B-DISEASESYMTOM |
| tháo | I-DISEASESYMTOM |
| đường | I-DISEASESYMTOM |
| mà | 0 |
| không | 0 |
| có | 0 |
| kèm | 0 |
| bệnh | B-DISEASESYMTOM |
| lý | I-DISEASESYMTOM |
| béo | B-DISEASESYMTOM |
| phì | I-DISEASESYMTOM |
| và | 0 |
| cũng | 0 |
| đã | 0 |
| có | 0 |
| rất | 0 |
| là | 0 |

## VM600-304 — dòng train 2332 (đếm từ 0)

côn trùng cũng đang bị mầm bệnh đe dọa chẳng hạn như vi khuẩn và nấm như nhà

| Token | Nhãn gốc |
|---|---|
| côn | 0 |
| trùng | 0 |
| cũng | 0 |
| đang | 0 |
| bị | 0 |
| mầm | B-DISEASESYMTOM |
| bệnh | I-DISEASESYMTOM |
| đe | 0 |
| dọa | 0 |
| chẳng | 0 |
| hạn | 0 |
| như | 0 |
| vi | B-DISEASESYMTOM |
| khuẩn | I-DISEASESYMTOM |
| và | 0 |
| nấm | 0 |
| như | 0 |
| nhà | B-LOCATION |

## VM600-305 — dòng train 2334 (đếm từ 0)

nào tôi cũng phải vịn lúc nào tôi cũng phải bán bởi vì sao chẳng may mình sẩy chân chẳng may mình có những câu chuyện

| Token | Nhãn gốc |
|---|---|
| nào | 0 |
| tôi | 0 |
| cũng | 0 |
| phải | 0 |
| vịn | 0 |
| lúc | 0 |
| nào | 0 |
| tôi | 0 |
| cũng | 0 |
| phải | 0 |
| bán | 0 |
| bởi | 0 |
| vì | 0 |
| sao | 0 |
| chẳng | 0 |
| may | 0 |
| mình | 0 |
| sẩy | 0 |
| chân | B-ORGAN |
| chẳng | 0 |
| may | 0 |
| mình | 0 |
| có | 0 |
| những | 0 |
| câu | 0 |
| chuyện | 0 |

## VM600-306 — dòng train 2335 (đếm từ 0)

trội của hoạt chất kga1 là được chiết xuất chuẩn hóa từ thảo dược đảm bảo tính an toàn cho người bệnh khi kga1 kết

| Token | Nhãn gốc |
|---|---|
| trội | 0 |
| của | 0 |
| hoạt | B-DRUGCHEMICAL |
| chất | I-DRUGCHEMICAL |
| kga1 | B-DRUGCHEMICAL |
| là | 0 |
| được | 0 |
| chiết | B-MEDDEVICETECHNIQUE |
| xuất | I-MEDDEVICETECHNIQUE |
| chuẩn | 0 |
| hóa | 0 |
| từ | 0 |
| thảo | B-DRUGCHEMICAL |
| dược | I-DRUGCHEMICAL |
| đảm | 0 |
| bảo | 0 |
| tính | 0 |
| an | 0 |
| toàn | 0 |
| cho | 0 |
| người | 0 |
| bệnh | 0 |
| khi | 0 |
| kga1 | B-DRUGCHEMICAL |
| kết | 0 |

## VM600-307 — dòng train 2340 (đếm từ 0)

huyết áp là bác vẫn bác trai vẫn thường xuyên duy trì này rồi là các tất cả các cái thuốc điều trị của các bác sĩ là bác

| Token | Nhãn gốc |
|---|---|
| huyết | B-DISEASESYMTOM |
| áp | I-DISEASESYMTOM |
| là | 0 |
| bác | B-AGE |
| vẫn | 0 |
| bác | B-AGE |
| trai | 0 |
| vẫn | 0 |
| thường | B-DATETIME |
| xuyên | I-DATETIME |
| duy | B-PERSONALCARE |
| trì | I-PERSONALCARE |
| này | 0 |
| rồi | 0 |
| là | 0 |
| các | 0 |
| tất | 0 |
| cả | 0 |
| các | 0 |
| cái | 0 |
| thuốc | B-DRUGCHEMICAL |
| điều | B-TREATMENT |
| trị | I-TREATMENT |
| của | 0 |
| các | 0 |
| bác | B-OCCUPATION |
| sĩ | I-OCCUPATION |
| là | 0 |
| bác | B-AGE |

## VM600-308 — dòng train 2342 (đếm từ 0)

thâm sau mụn nè hoặc là mụn ẩn mà có kèm theo là nám và tàn nhang thì khi đó chúng ta vẫn có thể sử dụng những cái

| Token | Nhãn gốc |
|---|---|
| thâm | B-DISEASESYMTOM |
| sau | I-DISEASESYMTOM |
| mụn | B-DISEASESYMTOM |
| nè | 0 |
| hoặc | 0 |
| là | 0 |
| mụn | B-DISEASESYMTOM |
| ẩn | I-DISEASESYMTOM |
| mà | 0 |
| có | 0 |
| kèm | 0 |
| theo | 0 |
| là | 0 |
| nám | B-DISEASESYMTOM |
| và | 0 |
| tàn | B-DISEASESYMTOM |
| nhang | I-DISEASESYMTOM |
| thì | 0 |
| khi | 0 |
| đó | 0 |
| chúng | 0 |
| ta | 0 |
| vẫn | 0 |
| có | 0 |
| thể | 0 |
| sử | 0 |
| dụng | 0 |
| những | 0 |
| cái | 0 |

## VM600-309 — dòng train 2347 (đếm từ 0)

chương trình kích thích não sau thì nó sẽ có những người tham gia ví dụ như là

| Token | Nhãn gốc |
|---|---|
| chương | 0 |
| trình | 0 |
| kích | 0 |
| thích | 0 |
| não | B-ORGAN |
| sau | 0 |
| thì | 0 |
| nó | 0 |
| sẽ | 0 |
| có | 0 |
| những | 0 |
| người | 0 |
| tham | 0 |
| gia | 0 |
| ví | 0 |
| dụ | 0 |
| như | 0 |
| là | 0 |

## VM600-310 — dòng train 2362 (đếm từ 0)

có hai bộ phận thứ nhất là phần quả thể và phần thứ hai là phần đế thế thì ngày

| Token | Nhãn gốc |
|---|---|
| có | 0 |
| hai | B-UNITCALIBRATOR |
| bộ | I-UNITCALIBRATOR |
| phận | I-UNITCALIBRATOR |
| thứ | B-UNITCALIBRATOR |
| nhất | I-UNITCALIBRATOR |
| là | 0 |
| phần | 0 |
| quả | B-DRUGCHEMICAL |
| thể | I-DRUGCHEMICAL |
| và | 0 |
| phần | B-UNITCALIBRATOR |
| thứ | I-UNITCALIBRATOR |
| hai | I-UNITCALIBRATOR |
| là | 0 |
| phần | 0 |
| đế | 0 |
| thế | 0 |
| thì | 0 |
| ngày | 0 |

## VM600-311 — dòng train 2371 (đếm từ 0)

động sinh lý khác nhau bao gồm vận hành hệ miễn dịch giải độc viêm dẫn truyền

| Token | Nhãn gốc |
|---|---|
| động | 0 |
| sinh | 0 |
| lý | 0 |
| khác | 0 |
| nhau | 0 |
| bao | 0 |
| gồm | 0 |
| vận | 0 |
| hành | 0 |
| hệ | B-ORGAN |
| miễn | I-ORGAN |
| dịch | I-ORGAN |
| giải | I-ORGAN |
| độc | I-ORGAN |
| viêm | B-DISEASESYMTOM |
| dẫn | 0 |
| truyền | 0 |

## VM600-312 — dòng train 2373 (đếm từ 0)

thần kinh cao cấp đó là những những cái trách nhiệm về tâm lý những được được

| Token | Nhãn gốc |
|---|---|
| thần | B-ORGAN |
| kinh | I-ORGAN |
| cao | B-UNITCALIBRATOR |
| cấp | 0 |
| đó | 0 |
| là | 0 |
| những | 0 |
| những | 0 |
| cái | 0 |
| trách | 0 |
| nhiệm | 0 |
| về | 0 |
| tâm | 0 |
| lý | 0 |
| những | 0 |
| được | 0 |
| được | 0 |

## VM600-313 — dòng train 2383 (đếm từ 0)

cái thành phần mà xưa kia cha ông ta rất hay sử dụng trong những cái bài thuốc để điều trị như các cái chứng bệnh về chính

| Token | Nhãn gốc |
|---|---|
| cái | 0 |
| thành | 0 |
| phần | 0 |
| mà | 0 |
| xưa | 0 |
| kia | 0 |
| cha | B-GENDER |
| ông | I-GENDER |
| ta | 0 |
| rất | 0 |
| hay | 0 |
| sử | 0 |
| dụng | 0 |
| trong | 0 |
| những | 0 |
| cái | 0 |
| bài | 0 |
| thuốc | B-DRUGCHEMICAL |
| để | 0 |
| điều | B-TREATMENT |
| trị | I-TREATMENT |
| như | 0 |
| các | 0 |
| cái | 0 |
| chứng | 0 |
| bệnh | 0 |
| về | 0 |
| chính | 0 |

## VM600-314 — dòng train 2403 (đếm từ 0)

và vậy thì gia đình mà có nuôi chó mèo

| Token | Nhãn gốc |
|---|---|
| và | 0 |
| vậy | 0 |
| thì | 0 |
| gia | 0 |
| đình | 0 |
| mà | 0 |
| có | 0 |
| nuôi | 0 |
| chó | 0 |
| mèo | 0 |

## VM600-315 — dòng train 2408 (đếm từ 0)

tham gia vào khi nói đến sự phát triển của bất kỳ căn bệnh nào cũng như tỷ lệ mắc một số bệnh ở các quốc gia khác nhau

| Token | Nhãn gốc |
|---|---|
| tham | 0 |
| gia | 0 |
| vào | 0 |
| khi | 0 |
| nói | 0 |
| đến | 0 |
| sự | 0 |
| phát | 0 |
| triển | 0 |
| của | 0 |
| bất | 0 |
| kỳ | 0 |
| căn | 0 |
| bệnh | 0 |
| nào | 0 |
| cũng | 0 |
| như | 0 |
| tỷ | B-UNITCALIBRATOR |
| lệ | I-UNITCALIBRATOR |
| mắc | 0 |
| một | 0 |
| số | 0 |
| bệnh | 0 |
| ở | 0 |
| các | 0 |
| quốc | B-LOCATION |
| gia | I-LOCATION |
| khác | 0 |
| nhau | 0 |

## VM600-316 — dòng train 2441 (đếm từ 0)

biệt là nội thần kinh nội về bệnh parkinson và rối loạn vận động cũng sẽ hỗ trợ rất nhiều trong khi việc mà làm

| Token | Nhãn gốc |
|---|---|
| biệt | 0 |
| là | 0 |
| nội | 0 |
| thần | B-ORGAN |
| kinh | I-ORGAN |
| nội | 0 |
| về | 0 |
| bệnh | 0 |
| parkinson | B-DISEASESYMTOM |
| và | 0 |
| rối | B-DISEASESYMTOM |
| loạn | I-DISEASESYMTOM |
| vận | I-DISEASESYMTOM |
| động | I-DISEASESYMTOM |
| cũng | 0 |
| sẽ | 0 |
| hỗ | B-MEDDEVICETECHNIQUE |
| trợ | I-MEDDEVICETECHNIQUE |
| rất | B-UNITCALIBRATOR |
| nhiều | I-UNITCALIBRATOR |
| trong | 0 |
| khi | 0 |
| việc | 0 |
| mà | 0 |
| làm | 0 |

## VM600-317 — dòng train 2442 (đếm từ 0)

phần hóa học cũng như là tác dụng dược lý của các hoạt chất nằm trong quả thể

| Token | Nhãn gốc |
|---|---|
| phần | 0 |
| hóa | 0 |
| học | 0 |
| cũng | 0 |
| như | 0 |
| là | 0 |
| tác | 0 |
| dụng | 0 |
| dược | 0 |
| lý | 0 |
| của | 0 |
| các | 0 |
| hoạt | B-DRUGCHEMICAL |
| chất | I-DRUGCHEMICAL |
| nằm | 0 |
| trong | 0 |
| quả | B-DRUGCHEMICAL |
| thể | I-DRUGCHEMICAL |

## VM600-318 — dòng train 2445 (đếm từ 0)

là bình thường thế rồi thì chúng ta cũng thấy nó đỡ rồi thì thôi thế là tự nhiên chúng ta bỏ thuốc cái đó cực kỳ nguy

| Token | Nhãn gốc |
|---|---|
| là | 0 |
| bình | 0 |
| thường | 0 |
| thế | 0 |
| rồi | 0 |
| thì | 0 |
| chúng | 0 |
| ta | 0 |
| cũng | 0 |
| thấy | 0 |
| nó | 0 |
| đỡ | 0 |
| rồi | 0 |
| thì | 0 |
| thôi | 0 |
| thế | 0 |
| là | 0 |
| tự | 0 |
| nhiên | 0 |
| chúng | 0 |
| ta | 0 |
| bỏ | 0 |
| thuốc | B-DRUGCHEMICAL |
| cái | 0 |
| đó | 0 |
| cực | 0 |
| kỳ | 0 |
| nguy | 0 |

## VM600-319 — dòng train 2454 (đếm từ 0)

để điều trị cho từng bệnh đặc biệt trong đó thì có một cái cơ chế rất là quan trọng là các cái khớp nó bị viêm thì cần

| Token | Nhãn gốc |
|---|---|
| để | 0 |
| điều | B-TREATMENT |
| trị | I-TREATMENT |
| cho | 0 |
| từng | 0 |
| bệnh | 0 |
| đặc | 0 |
| biệt | 0 |
| trong | 0 |
| đó | 0 |
| thì | 0 |
| có | 0 |
| một | 0 |
| cái | 0 |
| cơ | 0 |
| chế | 0 |
| rất | 0 |
| là | 0 |
| quan | 0 |
| trọng | 0 |
| là | 0 |
| các | B-ORGAN |
| cái | I-ORGAN |
| khớp | I-ORGAN |
| nó | 0 |
| bị | 0 |
| viêm | B-DISEASESYMTOM |
| thì | 0 |
| cần | 0 |

## VM600-320 — dòng train 2466 (đếm từ 0)

biệt là bị ảnh hưởng với các loại thuốc thức ăn nó là một cái loại kháng vitamin k bởi

| Token | Nhãn gốc |
|---|---|
| biệt | 0 |
| là | 0 |
| bị | 0 |
| ảnh | 0 |
| hưởng | 0 |
| với | 0 |
| các | 0 |
| loại | 0 |
| thuốc | B-DRUGCHEMICAL |
| thức | B-FOODDRINK |
| ăn | I-FOODDRINK |
| nó | 0 |
| là | 0 |
| một | 0 |
| cái | 0 |
| loại | 0 |
| kháng | 0 |
| vitamin | B-DRUGCHEMICAL |
| k | I-DRUGCHEMICAL |
| bởi | 0 |

## VM600-321 — dòng train 2479 (đếm từ 0)

sau mổ tại vì cái chương trình đều chương trình điều chỉnh máy sau mổ

| Token | Nhãn gốc |
|---|---|
| sau | 0 |
| mổ | B-SURGERY |
| tại | 0 |
| vì | 0 |
| cái | 0 |
| chương | 0 |
| trình | 0 |
| đều | 0 |
| chương | 0 |
| trình | 0 |
| điều | B-PREVENTIVEMED |
| chỉnh | I-PREVENTIVEMED |
| máy | 0 |
| sau | 0 |
| mổ | B-SURGERY |

## VM600-322 — dòng train 2484 (đếm từ 0)

chăm sóc dành cho người bệnh béo phì với vai trò của người thân trong gia đình là một trong những điều quan trọng và ngày

| Token | Nhãn gốc |
|---|---|
| chăm | B-PERSONALCARE |
| sóc | I-PERSONALCARE |
| dành | 0 |
| cho | 0 |
| người | 0 |
| bệnh | 0 |
| béo | B-DISEASESYMTOM |
| phì | I-DISEASESYMTOM |
| với | 0 |
| vai | 0 |
| trò | 0 |
| của | 0 |
| người | 0 |
| thân | 0 |
| trong | 0 |
| gia | 0 |
| đình | 0 |
| là | 0 |
| một | 0 |
| trong | 0 |
| những | 0 |
| điều | 0 |
| quan | 0 |
| trọng | 0 |
| và | 0 |
| ngày | 0 |

## VM600-323 — dòng train 2489 (đếm từ 0)

máu trong đó đặc biệt là tĩnh mạch của chúng ta thế thì cái viên nang đông trùng hạ thảo nó cũng có rất hữu ích cho

| Token | Nhãn gốc |
|---|---|
| máu | B-ORGAN |
| trong | 0 |
| đó | 0 |
| đặc | 0 |
| biệt | 0 |
| là | 0 |
| tĩnh | B-ORGAN |
| mạch | I-ORGAN |
| của | 0 |
| chúng | 0 |
| ta | 0 |
| thế | 0 |
| thì | 0 |
| cái | 0 |
| viên | B-DRUGCHEMICAL |
| nang | I-DRUGCHEMICAL |
| đông | I-DRUGCHEMICAL |
| trùng | I-DRUGCHEMICAL |
| hạ | I-DRUGCHEMICAL |
| thảo | I-DRUGCHEMICAL |
| nó | 0 |
| cũng | 0 |
| có | 0 |
| rất | 0 |
| hữu | 0 |
| ích | 0 |
| cho | 0 |

## VM600-324 — dòng train 2499 (đếm từ 0)

đưa cho những người thực hiện chức năng và chúng ta có thể đi qua cái chốt chặn dễ dàng xin để cảm ơn tiến sĩ bác sĩ

| Token | Nhãn gốc |
|---|---|
| đưa | 0 |
| cho | 0 |
| những | 0 |
| người | 0 |
| thực | 0 |
| hiện | 0 |
| chức | 0 |
| năng | 0 |
| và | 0 |
| chúng | 0 |
| ta | 0 |
| có | 0 |
| thể | 0 |
| đi | 0 |
| qua | 0 |
| cái | 0 |
| chốt | B-PREVENTIVEMED |
| chặn | I-PREVENTIVEMED |
| dễ | 0 |
| dàng | 0 |
| xin | 0 |
| để | 0 |
| cảm | 0 |
| ơn | 0 |
| tiến | B-OCCUPATION |
| sĩ | I-OCCUPATION |
| bác | B-OCCUPATION |
| sĩ | I-OCCUPATION |

## VM600-325 — dòng train 2502 (đếm từ 0)

tam đại bộ phẩm đó là cái gì thứ nhất là nó là có nhung hươu cái thứ hai là nhân sâm và thứ ba đông trùng hạ thảo cái thứ

| Token | Nhãn gốc |
|---|---|
| tam | B-DRUGCHEMICAL |
| đại | I-DRUGCHEMICAL |
| bộ | I-DRUGCHEMICAL |
| phẩm | I-DRUGCHEMICAL |
| đó | 0 |
| là | 0 |
| cái | 0 |
| gì | 0 |
| thứ | B-UNITCALIBRATOR |
| nhất | I-UNITCALIBRATOR |
| là | 0 |
| nó | 0 |
| là | 0 |
| có | 0 |
| nhung | B-DRUGCHEMICAL |
| hươu | I-DRUGCHEMICAL |
| cái | B-UNITCALIBRATOR |
| thứ | I-UNITCALIBRATOR |
| hai | I-UNITCALIBRATOR |
| là | 0 |
| nhân | B-DRUGCHEMICAL |
| sâm | I-DRUGCHEMICAL |
| và | 0 |
| thứ | 0 |
| ba | 0 |
| đông | B-DRUGCHEMICAL |
| trùng | I-DRUGCHEMICAL |
| hạ | I-DRUGCHEMICAL |
| thảo | I-DRUGCHEMICAL |
| cái | 0 |
| thứ | 0 |

## VM600-326 — dòng train 2511 (đếm từ 0)

pháp có liên quan đến y học cổ truyền ở trong đó thì có cái viên nang đông trùng hạ thảo hôm nay chương trình giới thiệu

| Token | Nhãn gốc |
|---|---|
| pháp | 0 |
| có | 0 |
| liên | 0 |
| quan | 0 |
| đến | 0 |
| y | B-MEDDEVICETECHNIQUE |
| học | I-MEDDEVICETECHNIQUE |
| cổ | I-MEDDEVICETECHNIQUE |
| truyền | I-MEDDEVICETECHNIQUE |
| ở | 0 |
| trong | 0 |
| đó | 0 |
| thì | 0 |
| có | 0 |
| cái | 0 |
| viên | B-DRUGCHEMICAL |
| nang | I-DRUGCHEMICAL |
| đông | I-DRUGCHEMICAL |
| trùng | I-DRUGCHEMICAL |
| hạ | I-DRUGCHEMICAL |
| thảo | I-DRUGCHEMICAL |
| hôm | B-DATETIME |
| nay | I-DATETIME |
| chương | 0 |
| trình | 0 |
| giới | 0 |
| thiệu | 0 |

## VM600-327 — dòng train 2520 (đếm từ 0)

với những cái bệnh lý khác thì điều này không chỉ trong thực tế lâm sàng mà trong những cái nghiên cứu họ

| Token | Nhãn gốc |
|---|---|
| với | 0 |
| những | 0 |
| cái | 0 |
| bệnh | B-DISEASESYMTOM |
| lý | I-DISEASESYMTOM |
| khác | 0 |
| thì | 0 |
| điều | 0 |
| này | 0 |
| không | 0 |
| chỉ | 0 |
| trong | 0 |
| thực | 0 |
| tế | 0 |
| lâm | 0 |
| sàng | 0 |
| mà | 0 |
| trong | 0 |
| những | 0 |
| cái | 0 |
| nghiên | B-DIAGNOSTICS |
| cứu | I-DIAGNOSTICS |
| họ | 0 |

## VM600-328 — dòng train 2521 (đếm từ 0)

trường sống này mình sẽ nhắm tới mấy cái chuyện môi trường thứ nhất là môi trường tự nhiên và môi trường thứ hai là môi

| Token | Nhãn gốc |
|---|---|
| trường | 0 |
| sống | 0 |
| này | 0 |
| mình | 0 |
| sẽ | 0 |
| nhắm | 0 |
| tới | 0 |
| mấy | 0 |
| cái | 0 |
| chuyện | 0 |
| môi | B-ORGAN |
| trường | 0 |
| thứ | B-UNITCALIBRATOR |
| nhất | I-UNITCALIBRATOR |
| là | 0 |
| môi | B-ORGAN |
| trường | 0 |
| tự | 0 |
| nhiên | 0 |
| và | 0 |
| môi | B-ORGAN |
| trường | 0 |
| thứ | 0 |
| hai | 0 |
| là | 0 |
| môi | B-ORGAN |

## VM600-329 — dòng train 2522 (đếm từ 0)

đau khớp và viêm khớp huyết áp cao xơ vữa động mạch các bệnh nhiễm nấm mạn

| Token | Nhãn gốc |
|---|---|
| đau | B-DISEASESYMTOM |
| khớp | B-ORGAN |
| và | 0 |
| viêm | B-DISEASESYMTOM |
| khớp | I-DISEASESYMTOM |
| huyết | B-DISEASESYMTOM |
| áp | I-DISEASESYMTOM |
| cao | B-UNITCALIBRATOR |
| xơ | B-DISEASESYMTOM |
| vữa | I-DISEASESYMTOM |
| động | I-DISEASESYMTOM |
| mạch | I-DISEASESYMTOM |
| các | 0 |
| bệnh | B-DISEASESYMTOM |
| nhiễm | I-DISEASESYMTOM |
| nấm | I-DISEASESYMTOM |
| mạn | I-DISEASESYMTOM |

## VM600-330 — dòng train 2525 (đếm từ 0)

các bạn ngày hôm nay của chúng ta đã có thêm được nhiều những cái kiến thức đặc biệt là đối với những người cao tuổi ngày hôm nay những ai mà đang còn đang

| Token | Nhãn gốc |
|---|---|
| các | 0 |
| bạn | 0 |
| ngày | B-DATETIME |
| hôm | I-DATETIME |
| nay | I-DATETIME |
| của | 0 |
| chúng | 0 |
| ta | 0 |
| đã | 0 |
| có | 0 |
| thêm | 0 |
| được | 0 |
| nhiều | 0 |
| những | 0 |
| cái | 0 |
| kiến | 0 |
| thức | 0 |
| đặc | 0 |
| biệt | 0 |
| là | 0 |
| đối | 0 |
| với | 0 |
| những | 0 |
| người | 0 |
| cao | B-AGE |
| tuổi | I-AGE |
| ngày | B-DATETIME |
| hôm | I-DATETIME |
| nay | I-DATETIME |
| những | 0 |
| ai | 0 |
| mà | 0 |
| đang | 0 |
| còn | 0 |
| đang | 0 |

## VM600-331 — dòng train 2533 (đếm từ 0)

bác sĩ kiểm tra ngay huyết áp và cho thuốc bác thuốc uống huyết áp để kiểm soát tốt con số huyết áp bác nhé vì với

| Token | Nhãn gốc |
|---|---|
| bác | B-OCCUPATION |
| sĩ | I-OCCUPATION |
| kiểm | B-DIAGNOSTICS |
| tra | I-DIAGNOSTICS |
| ngay | 0 |
| huyết | B-DISEASESYMTOM |
| áp | I-DISEASESYMTOM |
| và | 0 |
| cho | B-TREATMENT |
| thuốc | I-TREATMENT |
| bác | B-AGE |
| thuốc | B-DRUGCHEMICAL |
| uống | I-DRUGCHEMICAL |
| huyết | B-DISEASESYMTOM |
| áp | I-DISEASESYMTOM |
| để | 0 |
| kiểm | B-PREVENTIVEMED |
| soát | I-PREVENTIVEMED |
| tốt | 0 |
| con | 0 |
| số | 0 |
| huyết | B-DISEASESYMTOM |
| áp | I-DISEASESYMTOM |
| bác | B-AGE |
| nhé | 0 |
| vì | 0 |
| với | 0 |

## VM600-332 — dòng train 2546 (đếm từ 0)

cuộc sống tốt hơn vâng thưa bác sĩ như vậy thì ở từng giai đoạn của mình thì người bệnh sẽ được tiếp nhận điều

| Token | Nhãn gốc |
|---|---|
| cuộc | 0 |
| sống | 0 |
| tốt | 0 |
| hơn | 0 |
| vâng | 0 |
| thưa | 0 |
| bác | B-OCCUPATION |
| sĩ | I-OCCUPATION |
| như | 0 |
| vậy | 0 |
| thì | 0 |
| ở | 0 |
| từng | 0 |
| giai | 0 |
| đoạn | 0 |
| của | 0 |
| mình | 0 |
| thì | 0 |
| người | 0 |
| bệnh | 0 |
| sẽ | 0 |
| được | 0 |
| tiếp | 0 |
| nhận | 0 |
| điều | 0 |

## VM600-333 — dòng train 2558 (đếm từ 0)

huyết thông qua đó là biểu hiện cải thiện các chỉ số hba1c giảm được là từ khoảng là hai mươi phần trăm cái

| Token | Nhãn gốc |
|---|---|
| huyết | B-ORGAN |
| thông | 0 |
| qua | 0 |
| đó | 0 |
| là | 0 |
| biểu | 0 |
| hiện | 0 |
| cải | B-TREATMENT |
| thiện | I-TREATMENT |
| các | B-UNITCALIBRATOR |
| chỉ | I-UNITCALIBRATOR |
| số | I-UNITCALIBRATOR |
| hba1c | B-UNITCALIBRATOR |
| giảm | 0 |
| được | 0 |
| là | 0 |
| từ | 0 |
| khoảng | 0 |
| là | 0 |
| hai | B-UNITCALIBRATOR |
| mươi | I-UNITCALIBRATOR |
| phần | I-UNITCALIBRATOR |
| trăm | I-UNITCALIBRATOR |
| cái | 0 |

## VM600-334 — dòng train 2567 (đếm từ 0)

đó là nó ra được cơ quan kiểm soát thuốc và dược phẩm của hoa kỳ chấp nhận từ năm

| Token | Nhãn gốc |
|---|---|
| đó | 0 |
| là | 0 |
| nó | 0 |
| ra | 0 |
| được | 0 |
| cơ | B-ORGANIZATION |
| quan | I-ORGANIZATION |
| kiểm | I-ORGANIZATION |
| soát | I-ORGANIZATION |
| thuốc | I-ORGANIZATION |
| và | I-ORGANIZATION |
| dược | I-ORGANIZATION |
| phẩm | I-ORGANIZATION |
| của | I-ORGANIZATION |
| hoa | I-ORGANIZATION |
| kỳ | I-ORGANIZATION |
| chấp | 0 |
| nhận | 0 |
| từ | 0 |
| năm | 0 |

## VM600-335 — dòng train 2568 (đếm từ 0)

vấn giúp em làm cách nào để giúp bố em cải thiện tình trạng này ăn nhiều hơn và lên cân được không ạ

| Token | Nhãn gốc |
|---|---|
| vấn | 0 |
| giúp | 0 |
| em | 0 |
| làm | 0 |
| cách | 0 |
| nào | 0 |
| để | 0 |
| giúp | 0 |
| bố | 0 |
| em | 0 |
| cải | B-TREATMENT |
| thiện | I-TREATMENT |
| tình | 0 |
| trạng | 0 |
| này | 0 |
| ăn | 0 |
| nhiều | 0 |
| hơn | 0 |
| và | 0 |
| lên | 0 |
| cân | 0 |
| được | 0 |
| không | 0 |
| ạ | 0 |

## VM600-336 — dòng train 2584 (đếm từ 0)

thay vì cái việc ngày xưa chúng ta phải đi nhiều chúng ta vận động nhiều chúng ta phải đạp xe đạp hiện nay chúng ta là

| Token | Nhãn gốc |
|---|---|
| thay | 0 |
| vì | 0 |
| cái | 0 |
| việc | 0 |
| ngày | B-DATETIME |
| xưa | I-DATETIME |
| chúng | 0 |
| ta | 0 |
| phải | 0 |
| đi | 0 |
| nhiều | 0 |
| chúng | 0 |
| ta | 0 |
| vận | 0 |
| động | 0 |
| nhiều | 0 |
| chúng | 0 |
| ta | 0 |
| phải | 0 |
| đạp | 0 |
| xe | B-TRANSPORTATION |
| đạp | I-TRANSPORTATION |
| hiện | B-DATETIME |
| nay | I-DATETIME |
| chúng | 0 |
| ta | 0 |
| là | 0 |

## VM600-337 — dòng train 2588 (đếm từ 0)

hiện nay thì sẽ hỗ trợ cho việc mà khỏi bệnh được nhanh nhất và vấn đề thứ ba đó

| Token | Nhãn gốc |
|---|---|
| hiện | B-DATETIME |
| nay | I-DATETIME |
| thì | 0 |
| sẽ | 0 |
| hỗ | B-MEDDEVICETECHNIQUE |
| trợ | I-MEDDEVICETECHNIQUE |
| cho | 0 |
| việc | 0 |
| mà | 0 |
| khỏi | 0 |
| bệnh | 0 |
| được | 0 |
| nhanh | 0 |
| nhất | 0 |
| và | 0 |
| vấn | 0 |
| đề | 0 |
| thứ | 0 |
| ba | 0 |
| đó | 0 |

## VM600-338 — dòng train 2595 (đếm từ 0)

bệnh và rối loạn chức năng đỉnh cuối phần này bạn sẽ có một sự trân trọng mới

| Token | Nhãn gốc |
|---|---|
| bệnh | 0 |
| và | 0 |
| rối | B-DISEASESYMTOM |
| loạn | I-DISEASESYMTOM |
| chức | I-DISEASESYMTOM |
| năng | I-DISEASESYMTOM |
| đỉnh | 0 |
| cuối | 0 |
| phần | 0 |
| này | 0 |
| bạn | 0 |
| sẽ | 0 |
| có | 0 |
| một | 0 |
| sự | 0 |
| trân | 0 |
| trọng | 0 |
| mới | 0 |

## VM600-339 — dòng train 2601 (đếm từ 0)

giúp bạn tồn tại ảnh hưởng của mỗi cá nhân đến sức khỏe mạnh của hành tinh chúng ta cũng vậy trên thực tế bạn là

| Token | Nhãn gốc |
|---|---|
| giúp | 0 |
| bạn | 0 |
| tồn | 0 |
| tại | 0 |
| ảnh | 0 |
| hưởng | 0 |
| của | 0 |
| mỗi | 0 |
| cá | 0 |
| nhân | 0 |
| đến | 0 |
| sức | 0 |
| khỏe | 0 |
| mạnh | 0 |
| của | 0 |
| hành | 0 |
| tinh | 0 |
| chúng | 0 |
| ta | 0 |
| cũng | 0 |
| vậy | 0 |
| trên | 0 |
| thực | 0 |
| tế | 0 |
| bạn | 0 |
| là | 0 |

## VM600-340 — dòng train 2604 (đếm từ 0)

trạng ốm yếu đau khổ cá nhân chất lượng cuộc sống bị tổn hại và tiêu tốn về tài

| Token | Nhãn gốc |
|---|---|
| trạng | 0 |
| ốm | 0 |
| yếu | 0 |
| đau | B-DISEASESYMTOM |
| khổ | 0 |
| cá | 0 |
| nhân | 0 |
| chất | 0 |
| lượng | 0 |
| cuộc | 0 |
| sống | 0 |
| bị | 0 |
| tổn | 0 |
| hại | 0 |
| và | 0 |
| tiêu | 0 |
| tốn | 0 |
| về | 0 |
| tài | 0 |

## VM600-341 — dòng train 2608 (đếm từ 0)

khi mà bị đột quỵ thì thường các bác sĩ đột quỵ tôi sẽ phải khảo sát toàn bộ để

| Token | Nhãn gốc |
|---|---|
| khi | 0 |
| mà | 0 |
| bị | 0 |
| đột | B-DISEASESYMTOM |
| quỵ | I-DISEASESYMTOM |
| thì | 0 |
| thường | 0 |
| các | 0 |
| bác | B-OCCUPATION |
| sĩ | I-OCCUPATION |
| đột | B-DISEASESYMTOM |
| quỵ | I-DISEASESYMTOM |
| tôi | 0 |
| sẽ | 0 |
| phải | 0 |
| khảo | B-PREVENTIVEMED |
| sát | I-PREVENTIVEMED |
| toàn | 0 |
| bộ | 0 |
| để | 0 |

## VM600-342 — dòng train 2614 (đếm từ 0)

bệnh nó liên quan đến cái vùng cột sống cổ là chính những có những cái trường hợp liên quan đến cái vùng cổ tay và

| Token | Nhãn gốc |
|---|---|
| bệnh | 0 |
| nó | 0 |
| liên | 0 |
| quan | 0 |
| đến | 0 |
| cái | 0 |
| vùng | 0 |
| cột | B-ORGAN |
| sống | I-ORGAN |
| cổ | 0 |
| là | 0 |
| chính | 0 |
| những | 0 |
| có | 0 |
| những | 0 |
| cái | 0 |
| trường | 0 |
| hợp | 0 |
| liên | 0 |
| quan | 0 |
| đến | 0 |
| cái | 0 |
| vùng | B-ORGAN |
| cổ | B-ORGAN |
| tay | I-ORGAN |
| và | 0 |

## VM600-343 — dòng train 2621 (đếm từ 0)

tăng khoảng hai ký thì như vậy thì như chúng ta biết rằng là khi mà mình chọn lựa thuốc cho những cái bệnh nhân mà đái

| Token | Nhãn gốc |
|---|---|
| tăng | 0 |
| khoảng | 0 |
| hai | 0 |
| ký | 0 |
| thì | 0 |
| như | 0 |
| vậy | 0 |
| thì | 0 |
| như | 0 |
| chúng | 0 |
| ta | 0 |
| biết | 0 |
| rằng | 0 |
| là | 0 |
| khi | 0 |
| mà | 0 |
| mình | 0 |
| chọn | 0 |
| lựa | 0 |
| thuốc | B-DRUGCHEMICAL |
| cho | 0 |
| những | 0 |
| cái | 0 |
| bệnh | B-OCCUPATION |
| nhân | I-OCCUPATION |
| mà | 0 |
| đái | 0 |

## VM600-344 — dòng train 2622 (đếm từ 0)

chỉ định của các bác sĩ thì bệnh nhân cũng cần được tiếp tục hỗ trợ chuyên sâu về mặt tâm lý nhằm là giúp cho họ giữ

| Token | Nhãn gốc |
|---|---|
| chỉ | B-PREVENTIVEMED |
| định | I-PREVENTIVEMED |
| của | 0 |
| các | 0 |
| bác | B-OCCUPATION |
| sĩ | I-OCCUPATION |
| thì | 0 |
| bệnh | B-OCCUPATION |
| nhân | I-OCCUPATION |
| cũng | 0 |
| cần | 0 |
| được | 0 |
| tiếp | 0 |
| tục | 0 |
| hỗ | B-MEDDEVICETECHNIQUE |
| trợ | I-MEDDEVICETECHNIQUE |
| chuyên | I-MEDDEVICETECHNIQUE |
| sâu | I-MEDDEVICETECHNIQUE |
| về | I-MEDDEVICETECHNIQUE |
| mặt | I-MEDDEVICETECHNIQUE |
| tâm | I-MEDDEVICETECHNIQUE |
| lý | I-MEDDEVICETECHNIQUE |
| nhằm | 0 |
| là | 0 |
| giúp | 0 |
| cho | 0 |
| họ | 0 |
| giữ | 0 |

## VM600-345 — dòng train 2624 (đếm từ 0)

động mạch được hay không và giảm nhẹ các triệu chứng như là đau đầu hoa mắt chóng mặt được hay không thưa bác sĩ đây là

| Token | Nhãn gốc |
|---|---|
| động | B-ORGAN |
| mạch | I-ORGAN |
| được | 0 |
| hay | 0 |
| không | 0 |
| và | 0 |
| giảm | 0 |
| nhẹ | 0 |
| các | 0 |
| triệu | B-DISEASESYMTOM |
| chứng | I-DISEASESYMTOM |
| như | 0 |
| là | 0 |
| đau | B-DISEASESYMTOM |
| đầu | I-DISEASESYMTOM |
| hoa | B-DISEASESYMTOM |
| mắt | I-DISEASESYMTOM |
| chóng | B-DISEASESYMTOM |
| mặt | I-DISEASESYMTOM |
| được | 0 |
| hay | 0 |
| không | 0 |
| thưa | 0 |
| bác | B-OCCUPATION |
| sĩ | I-OCCUPATION |
| đây | 0 |
| là | 0 |

## VM600-346 — dòng train 2626 (đếm từ 0)

có thể rất quý ví dụ như là tam đại bộ phẩm có nhân sâm có nhung hươu rồi có

| Token | Nhãn gốc |
|---|---|
| có | 0 |
| thể | 0 |
| rất | 0 |
| quý | 0 |
| ví | 0 |
| dụ | 0 |
| như | 0 |
| là | 0 |
| tam | B-DRUGCHEMICAL |
| đại | I-DRUGCHEMICAL |
| bộ | I-DRUGCHEMICAL |
| phẩm | I-DRUGCHEMICAL |
| có | 0 |
| nhân | B-DRUGCHEMICAL |
| sâm | I-DRUGCHEMICAL |
| có | 0 |
| nhung | B-DRUGCHEMICAL |
| hươu | I-DRUGCHEMICAL |
| rồi | 0 |
| có | 0 |

## VM600-347 — dòng train 2632 (đếm từ 0)

thứ ba là lúc nào cũng kêu chán hết trơn sao mà chán quá đi chán quá đi và hổng

| Token | Nhãn gốc |
|---|---|
| thứ | 0 |
| ba | 0 |
| là | 0 |
| lúc | 0 |
| nào | 0 |
| cũng | 0 |
| kêu | 0 |
| chán | 0 |
| hết | 0 |
| trơn | 0 |
| sao | 0 |
| mà | 0 |
| chán | 0 |
| quá | 0 |
| đi | 0 |
| chán | 0 |
| quá | 0 |
| đi | 0 |
| và | 0 |
| hổng | 0 |

## VM600-348 — dòng train 2635 (đếm từ 0)

gia đình và những người ở trong xã hội càng tốt thì sẽ ở trong cái môi trường đó cái người béo phì nó sẽ được thuận

| Token | Nhãn gốc |
|---|---|
| gia | 0 |
| đình | 0 |
| và | 0 |
| những | 0 |
| người | 0 |
| ở | 0 |
| trong | 0 |
| xã | 0 |
| hội | 0 |
| càng | 0 |
| tốt | 0 |
| thì | 0 |
| sẽ | 0 |
| ở | 0 |
| trong | 0 |
| cái | 0 |
| môi | B-ORGAN |
| trường | 0 |
| đó | 0 |
| cái | 0 |
| người | 0 |
| béo | B-DISEASESYMTOM |
| phì | I-DISEASESYMTOM |
| nó | 0 |
| sẽ | 0 |
| được | 0 |
| thuận | 0 |

## VM600-349 — dòng train 2640 (đếm từ 0)

phì chứ không chỉ riêng về cái rối loạn về cái hành vi ăn uống thế thì họ cần

| Token | Nhãn gốc |
|---|---|
| phì | 0 |
| chứ | 0 |
| không | 0 |
| chỉ | 0 |
| riêng | 0 |
| về | 0 |
| cái | 0 |
| rối | B-DISEASESYMTOM |
| loạn | I-DISEASESYMTOM |
| về | 0 |
| cái | 0 |
| hành | 0 |
| vi | 0 |
| ăn | B-PERSONALCARE |
| uống | I-PERSONALCARE |
| thế | 0 |
| thì | 0 |
| họ | 0 |
| cần | 0 |

## VM600-350 — dòng train 2647 (đếm từ 0)

ví dụ như là nếu chúng ta bị chấn thương thì sẽ dễ bị chảy máu chảy máu khó

| Token | Nhãn gốc |
|---|---|
| ví | 0 |
| dụ | 0 |
| như | 0 |
| là | 0 |
| nếu | 0 |
| chúng | 0 |
| ta | 0 |
| bị | 0 |
| chấn | B-DISEASESYMTOM |
| thương | I-DISEASESYMTOM |
| thì | 0 |
| sẽ | 0 |
| dễ | 0 |
| bị | 0 |
| chảy | B-DISEASESYMTOM |
| máu | I-DISEASESYMTOM |
| chảy | B-DISEASESYMTOM |
| máu | I-DISEASESYMTOM |
| khó | 0 |

## VM600-351 — dòng train 2650 (đếm từ 0)

triển cũng như là chữa lành bệnh chứ còn hiện tại thì các phương pháp điều trị cũng như là phương pháp điều trị phẫu

| Token | Nhãn gốc |
|---|---|
| triển | 0 |
| cũng | 0 |
| như | 0 |
| là | 0 |
| chữa | B-TREATMENT |
| lành | I-TREATMENT |
| bệnh | I-TREATMENT |
| chứ | 0 |
| còn | 0 |
| hiện | 0 |
| tại | 0 |
| thì | 0 |
| các | 0 |
| phương | 0 |
| pháp | 0 |
| điều | B-TREATMENT |
| trị | I-TREATMENT |
| cũng | 0 |
| như | 0 |
| là | 0 |
| phương | 0 |
| pháp | 0 |
| điều | B-TREATMENT |
| trị | I-TREATMENT |
| phẫu | 0 |

## VM600-352 — dòng train 2654 (đếm từ 0)

người ta vẫn đang tiến tiếp tục nghiên cứu và rất nhiều các phương pháp nghiên cứu để giúp làm sao có thể ngăn sự tiến

| Token | Nhãn gốc |
|---|---|
| người | 0 |
| ta | 0 |
| vẫn | 0 |
| đang | 0 |
| tiến | 0 |
| tiếp | 0 |
| tục | 0 |
| nghiên | B-DIAGNOSTICS |
| cứu | I-DIAGNOSTICS |
| và | 0 |
| rất | B-UNITCALIBRATOR |
| nhiều | I-UNITCALIBRATOR |
| các | 0 |
| phương | 0 |
| pháp | 0 |
| nghiên | B-DIAGNOSTICS |
| cứu | I-DIAGNOSTICS |
| để | 0 |
| giúp | 0 |
| làm | 0 |
| sao | 0 |
| có | 0 |
| thể | 0 |
| ngăn | 0 |
| sự | 0 |
| tiến | 0 |

## VM600-353 — dòng train 2660 (đếm từ 0)

các cường độ cho nó phù hợp nhất để điều chỉnh cái gia giảm cả lượng thuốc thì làm cái quá trình rất là dài và có thể

| Token | Nhãn gốc |
|---|---|
| các | 0 |
| cường | B-UNITCALIBRATOR |
| độ | I-UNITCALIBRATOR |
| cho | 0 |
| nó | 0 |
| phù | 0 |
| hợp | 0 |
| nhất | 0 |
| để | 0 |
| điều | B-PREVENTIVEMED |
| chỉnh | I-PREVENTIVEMED |
| cái | 0 |
| gia | 0 |
| giảm | 0 |
| cả | 0 |
| lượng | 0 |
| thuốc | B-DRUGCHEMICAL |
| thì | 0 |
| làm | 0 |
| cái | 0 |
| quá | 0 |
| trình | 0 |
| rất | 0 |
| là | 0 |
| dài | 0 |
| và | 0 |
| có | 0 |
| thể | 0 |

## VM600-354 — dòng train 2662 (đếm từ 0)

dụng của cái sản phẩm đó à nó không chỉ là khó gọi ghẹo gói trong một số bệnh lý

| Token | Nhãn gốc |
|---|---|
| dụng | 0 |
| của | 0 |
| cái | 0 |
| sản | 0 |
| phẩm | 0 |
| đó | 0 |
| à | 0 |
| nó | 0 |
| không | 0 |
| chỉ | 0 |
| là | 0 |
| khó | 0 |
| gọi | 0 |
| ghẹo | 0 |
| gói | 0 |
| trong | 0 |
| một | 0 |
| số | 0 |
| bệnh | 0 |
| lý | 0 |

## VM600-355 — dòng train 2663 (đếm từ 0)

giới ngày nay nhưng đã đến lúc phải đón nhận một khía cạnh khác của câu chuyện vi khuẩn trong cuộc sống của chúng ta

| Token | Nhãn gốc |
|---|---|
| giới | 0 |
| ngày | 0 |
| nay | 0 |
| nhưng | 0 |
| đã | 0 |
| đến | 0 |
| lúc | 0 |
| phải | 0 |
| đón | 0 |
| nhận | 0 |
| một | 0 |
| khía | 0 |
| cạnh | 0 |
| khác | 0 |
| của | 0 |
| câu | 0 |
| chuyện | 0 |
| vi | B-DISEASESYMTOM |
| khuẩn | I-DISEASESYMTOM |
| trong | 0 |
| cuộc | 0 |
| sống | 0 |
| của | 0 |
| chúng | 0 |
| ta | 0 |

## VM600-356 — dòng train 2666 (đếm từ 0)

nam chưa được phát hiện trên tám mươi phần trăm chưa được điều trị đồng thời tại việt nam có tới ba mươi phần trăm người trưởng

| Token | Nhãn gốc |
|---|---|
| nam | 0 |
| chưa | 0 |
| được | 0 |
| phát | 0 |
| hiện | 0 |
| trên | 0 |
| tám | B-UNITCALIBRATOR |
| mươi | I-UNITCALIBRATOR |
| phần | I-UNITCALIBRATOR |
| trăm | I-UNITCALIBRATOR |
| chưa | 0 |
| được | 0 |
| điều | B-TREATMENT |
| trị | I-TREATMENT |
| đồng | 0 |
| thời | 0 |
| tại | 0 |
| việt | B-LOCATION |
| nam | I-LOCATION |
| có | 0 |
| tới | 0 |
| ba | B-UNITCALIBRATOR |
| mươi | I-UNITCALIBRATOR |
| phần | I-UNITCALIBRATOR |
| trăm | I-UNITCALIBRATOR |
| người | 0 |
| trưởng | 0 |

## VM600-357 — dòng train 2675 (đếm từ 0)

trị liệu có thể làm gia tăng của nhiệt độ của những thiết bị đó là có thể làm tổn thương mô thì cái này là được xem

| Token | Nhãn gốc |
|---|---|
| trị | B-TREATMENT |
| liệu | I-TREATMENT |
| có | 0 |
| thể | 0 |
| làm | 0 |
| gia | 0 |
| tăng | 0 |
| của | 0 |
| nhiệt | 0 |
| độ | 0 |
| của | 0 |
| những | 0 |
| thiết | 0 |
| bị | 0 |
| đó | 0 |
| là | 0 |
| có | 0 |
| thể | 0 |
| làm | 0 |
| tổn | B-DISEASESYMTOM |
| thương | I-DISEASESYMTOM |
| mô | B-ORGAN |
| thì | 0 |
| cái | 0 |
| này | 0 |
| là | 0 |
| được | 0 |
| xem | 0 |

## VM600-358 — dòng train 2690 (đếm từ 0)

ung thư bằng cách là vắt nước chanh vào một cốc nước ấm xong rồi mình uống lại uống vào lúc đói thì thực sự là khi

| Token | Nhãn gốc |
|---|---|
| ung | B-DISEASESYMTOM |
| thư | I-DISEASESYMTOM |
| bằng | 0 |
| cách | 0 |
| là | 0 |
| vắt | 0 |
| nước | B-FOODDRINK |
| chanh | I-FOODDRINK |
| vào | 0 |
| một | 0 |
| cốc | 0 |
| nước | B-FOODDRINK |
| ấm | I-FOODDRINK |
| xong | 0 |
| rồi | 0 |
| mình | 0 |
| uống | 0 |
| lại | 0 |
| uống | 0 |
| vào | 0 |
| lúc | 0 |
| đói | 0 |
| thì | 0 |
| thực | 0 |
| sự | 0 |
| là | 0 |
| khi | 0 |

## VM600-359 — dòng train 2701 (đếm từ 0)

bên cạnh đó thì có những người họ vẫn nhận thức được béo phì nó là một bệnh lý có những cái tác hại như vậy cần phải

| Token | Nhãn gốc |
|---|---|
| bên | 0 |
| cạnh | 0 |
| đó | 0 |
| thì | 0 |
| có | 0 |
| những | 0 |
| người | 0 |
| họ | 0 |
| vẫn | 0 |
| nhận | 0 |
| thức | 0 |
| được | 0 |
| béo | B-DISEASESYMTOM |
| phì | I-DISEASESYMTOM |
| nó | 0 |
| là | 0 |
| một | 0 |
| bệnh | B-DISEASESYMTOM |
| lý | I-DISEASESYMTOM |
| có | 0 |
| những | 0 |
| cái | 0 |
| tác | 0 |
| hại | 0 |
| như | 0 |
| vậy | 0 |
| cần | 0 |
| phải | 0 |

## VM600-360 — dòng train 2703 (đếm từ 0)

dài đó là những cái chế độ ăn vận động thể lực cũng như là các quá trình thay đổi hành vi thì đã có rất là nhiều

| Token | Nhãn gốc |
|---|---|
| dài | 0 |
| đó | 0 |
| là | 0 |
| những | 0 |
| cái | 0 |
| chế | B-PERSONALCARE |
| độ | I-PERSONALCARE |
| ăn | I-PERSONALCARE |
| vận | I-PERSONALCARE |
| động | I-PERSONALCARE |
| thể | I-PERSONALCARE |
| lực | I-PERSONALCARE |
| cũng | 0 |
| như | 0 |
| là | 0 |
| các | 0 |
| quá | 0 |
| trình | 0 |
| thay | B-DISEASESYMTOM |
| đổi | I-DISEASESYMTOM |
| hành | I-DISEASESYMTOM |
| vi | I-DISEASESYMTOM |
| thì | 0 |
| đã | 0 |
| có | 0 |
| rất | 0 |
| là | 0 |
| nhiều | 0 |

## VM600-361 — dòng train 2708 (đếm từ 0)

biết nên tìm hiểu và để chuẩn bị một cái tâm lý thật là tốt và cuối cùng là

| Token | Nhãn gốc |
|---|---|
| biết | 0 |
| nên | 0 |
| tìm | 0 |
| hiểu | 0 |
| và | 0 |
| để | 0 |
| chuẩn | B-PERSONALCARE |
| bị | I-PERSONALCARE |
| một | I-PERSONALCARE |
| cái | I-PERSONALCARE |
| tâm | I-PERSONALCARE |
| lý | I-PERSONALCARE |
| thật | 0 |
| là | 0 |
| tốt | 0 |
| và | 0 |
| cuối | 0 |
| cùng | 0 |
| là | 0 |

## VM600-362 — dòng train 2712 (đếm từ 0)

các chị em phải lo lắng rồi đó là chưa kể áp lực công việc vân vân các thứ thì

| Token | Nhãn gốc |
|---|---|
| các | 0 |
| chị | B-GENDER |
| em | I-GENDER |
| phải | 0 |
| lo | 0 |
| lắng | 0 |
| rồi | 0 |
| đó | 0 |
| là | 0 |
| chưa | 0 |
| kể | 0 |
| áp | 0 |
| lực | 0 |
| công | 0 |
| việc | 0 |
| vân | 0 |
| vân | 0 |
| các | 0 |
| thứ | 0 |
| thì | 0 |

## VM600-363 — dòng train 2715 (đếm từ 0)

trước để có những cái thăm dò có những cái đánh giá trước sau đó thì khi mà tham khám như vậy các bác sĩ người ta sẽ

| Token | Nhãn gốc |
|---|---|
| trước | 0 |
| để | 0 |
| có | 0 |
| những | 0 |
| cái | 0 |
| thăm | 0 |
| dò | 0 |
| có | 0 |
| những | 0 |
| cái | 0 |
| đánh | B-TREATMENT |
| giá | I-TREATMENT |
| trước | 0 |
| sau | 0 |
| đó | 0 |
| thì | 0 |
| khi | 0 |
| mà | 0 |
| tham | 0 |
| khám | B-DIAGNOSTICS |
| như | 0 |
| vậy | 0 |
| các | 0 |
| bác | B-OCCUPATION |
| sĩ | I-OCCUPATION |
| người | 0 |
| ta | 0 |
| sẽ | 0 |

## VM600-364 — dòng train 2724 (đếm từ 0)

một cái hóa trị hoặc xạ trị thì nó đều liên quan đến khử độc tại gan và khi chức năng gan bị giảm như vậy thì nay lại bị

| Token | Nhãn gốc |
|---|---|
| một | 0 |
| cái | 0 |
| hóa | B-TREATMENT |
| trị | I-TREATMENT |
| hoặc | 0 |
| xạ | B-TREATMENT |
| trị | I-TREATMENT |
| thì | 0 |
| nó | 0 |
| đều | 0 |
| liên | 0 |
| quan | 0 |
| đến | 0 |
| khử | 0 |
| độc | 0 |
| tại | 0 |
| gan | B-ORGAN |
| và | 0 |
| khi | 0 |
| chức | 0 |
| năng | 0 |
| gan | B-ORGAN |
| bị | 0 |
| giảm | 0 |
| như | 0 |
| vậy | 0 |
| thì | 0 |
| nay | 0 |
| lại | 0 |
| bị | 0 |

## VM600-365 — dòng train 2726 (đếm từ 0)

mỡ động vật này những cái đạm thịt đỏ tuy nhiên thì chúng ta vẫn phải tăng cường cung cấp năng lượng này cũng như

| Token | Nhãn gốc |
|---|---|
| mỡ | B-FOODDRINK |
| động | I-FOODDRINK |
| vật | I-FOODDRINK |
| này | 0 |
| những | 0 |
| cái | 0 |
| đạm | B-FOODDRINK |
| thịt | B-FOODDRINK |
| đỏ | I-FOODDRINK |
| tuy | 0 |
| nhiên | 0 |
| thì | 0 |
| chúng | 0 |
| ta | 0 |
| vẫn | 0 |
| phải | 0 |
| tăng | B-PERSONALCARE |
| cường | I-PERSONALCARE |
| cung | I-PERSONALCARE |
| cấp | I-PERSONALCARE |
| năng | I-PERSONALCARE |
| lượng | I-PERSONALCARE |
| này | 0 |
| cũng | 0 |
| như | 0 |

## VM600-366 — dòng train 2728 (đếm từ 0)

xác như vậy thì mình sẽ đặt các điện cực và mình cố định lại thì mình sẽ tiến hành hai bên trên cái thời gian mà bệnh nhân

| Token | Nhãn gốc |
|---|---|
| xác | 0 |
| như | 0 |
| vậy | 0 |
| thì | 0 |
| mình | 0 |
| sẽ | 0 |
| đặt | 0 |
| các | 0 |
| điện | B-MEDDEVICETECHNIQUE |
| cực | I-MEDDEVICETECHNIQUE |
| và | 0 |
| mình | 0 |
| cố | 0 |
| định | 0 |
| lại | 0 |
| thì | 0 |
| mình | 0 |
| sẽ | 0 |
| tiến | 0 |
| hành | 0 |
| hai | 0 |
| bên | 0 |
| trên | 0 |
| cái | 0 |
| thời | B-DATETIME |
| gian | I-DATETIME |
| mà | 0 |
| bệnh | B-OCCUPATION |
| nhân | I-OCCUPATION |

## VM600-367 — dòng train 2732 (đếm từ 0)

hơn về diễn tiến bệnh cũng như là biết được các phương pháp điều trị tư tưởng như thế nào chúng ta sẽ cùng đi vào tìm

| Token | Nhãn gốc |
|---|---|
| hơn | 0 |
| về | 0 |
| diễn | 0 |
| tiến | 0 |
| bệnh | 0 |
| cũng | 0 |
| như | 0 |
| là | 0 |
| biết | 0 |
| được | 0 |
| các | 0 |
| phương | 0 |
| pháp | 0 |
| điều | B-TREATMENT |
| trị | I-TREATMENT |
| tư | 0 |
| tưởng | 0 |
| như | 0 |
| thế | 0 |
| nào | 0 |
| chúng | 0 |
| ta | 0 |
| sẽ | 0 |
| cùng | 0 |
| đi | 0 |
| vào | 0 |
| tìm | 0 |

## VM600-368 — dòng train 2733 (đếm từ 0)

việc mà duy trì cái tình trạng dinh dưỡng của bệnh nhân trong suốt quá cái

| Token | Nhãn gốc |
|---|---|
| việc | 0 |
| mà | 0 |
| duy | B-PERSONALCARE |
| trì | I-PERSONALCARE |
| cái | 0 |
| tình | 0 |
| trạng | 0 |
| dinh | 0 |
| dưỡng | 0 |
| của | 0 |
| bệnh | B-OCCUPATION |
| nhân | I-OCCUPATION |
| trong | 0 |
| suốt | 0 |
| quá | 0 |
| cái | 0 |

## VM600-369 — dòng train 2746 (đếm từ 0)

điều thứ hai cái điều thứ ba là dù là tân dược hay là các sản phẩm có nguồn

| Token | Nhãn gốc |
|---|---|
| điều | 0 |
| thứ | 0 |
| hai | 0 |
| cái | 0 |
| điều | 0 |
| thứ | 0 |
| ba | 0 |
| là | 0 |
| dù | 0 |
| là | 0 |
| tân | B-DRUGCHEMICAL |
| dược | I-DRUGCHEMICAL |
| hay | 0 |
| là | 0 |
| các | 0 |
| sản | 0 |
| phẩm | 0 |
| có | 0 |
| nguồn | 0 |

## VM600-370 — dòng train 2760 (đếm từ 0)

thiện một cách tương đối rồi tránh tình trạng là nó làm cho nó nặng lên và cái thứ hai nữa là nếu mà chúng ta có thể đi

| Token | Nhãn gốc |
|---|---|
| thiện | 0 |
| một | 0 |
| cách | 0 |
| tương | 0 |
| đối | 0 |
| rồi | 0 |
| tránh | 0 |
| tình | 0 |
| trạng | 0 |
| là | 0 |
| nó | 0 |
| làm | 0 |
| cho | 0 |
| nó | 0 |
| nặng | 0 |
| lên | 0 |
| và | 0 |
| cái | B-UNITCALIBRATOR |
| thứ | I-UNITCALIBRATOR |
| hai | I-UNITCALIBRATOR |
| nữa | 0 |
| là | 0 |
| nếu | 0 |
| mà | 0 |
| chúng | 0 |
| ta | 0 |
| có | 0 |
| thể | 0 |
| đi | 0 |

## VM600-371 — dòng train 2774 (đếm từ 0)

nhiên từ thực vật người ta liên trích ra và người ta đã chứng minh rằng đó có nhiều cái công dụng trong đó có công

| Token | Nhãn gốc |
|---|---|
| nhiên | 0 |
| từ | 0 |
| thực | B-FOODDRINK |
| vật | I-FOODDRINK |
| người | 0 |
| ta | 0 |
| liên | 0 |
| trích | 0 |
| ra | 0 |
| và | 0 |
| người | 0 |
| ta | 0 |
| đã | 0 |
| chứng | 0 |
| minh | 0 |
| rằng | 0 |
| đó | 0 |
| có | 0 |
| nhiều | 0 |
| cái | 0 |
| công | 0 |
| dụng | 0 |
| trong | 0 |
| đó | 0 |
| có | 0 |
| công | 0 |

## VM600-372 — dòng train 2775 (đếm từ 0)

retinoic acid hoặc là chúng ta sử dụng những phương pháp như là tái tạo da bằng hóa chất để mà chúng ta loại bỏ đi

| Token | Nhãn gốc |
|---|---|
| retinoic | B-DRUGCHEMICAL |
| acid | I-DRUGCHEMICAL |
| hoặc | 0 |
| là | 0 |
| chúng | 0 |
| ta | 0 |
| sử | 0 |
| dụng | 0 |
| những | 0 |
| phương | 0 |
| pháp | 0 |
| như | 0 |
| là | 0 |
| tái | B-TREATMENT |
| tạo | I-TREATMENT |
| da | I-TREATMENT |
| bằng | I-TREATMENT |
| hóa | I-TREATMENT |
| chất | I-TREATMENT |
| để | 0 |
| mà | 0 |
| chúng | 0 |
| ta | 0 |
| loại | B-PREVENTIVEMED |
| bỏ | I-PREVENTIVEMED |
| đi | 0 |

## VM600-373 — dòng train 2778 (đếm từ 0)

bao giờ đối tượng được việc thấu hiểu các mối liên hệ giữa ruột và não giúp

| Token | Nhãn gốc |
|---|---|
| bao | 0 |
| giờ | 0 |
| đối | 0 |
| tượng | 0 |
| được | 0 |
| việc | 0 |
| thấu | 0 |
| hiểu | 0 |
| các | 0 |
| mối | 0 |
| liên | 0 |
| hệ | 0 |
| giữa | 0 |
| ruột | B-ORGAN |
| và | 0 |
| não | B-ORGAN |
| giúp | 0 |

## VM600-374 — dòng train 2784 (đếm từ 0)

công thế này thì thì thì hổng biết làm sao sức khỏe của

| Token | Nhãn gốc |
|---|---|
| công | 0 |
| thế | 0 |
| này | 0 |
| thì | 0 |
| thì | 0 |
| thì | 0 |
| hổng | 0 |
| biết | 0 |
| làm | 0 |
| sao | 0 |
| sức | 0 |
| khỏe | 0 |
| của | 0 |

## VM600-375 — dòng train 2790 (đếm từ 0)

tích che phủ lỗ chân lông trên bề mặt da của bạn do đó nên bạn sẽ thấy là da của bạn ngủ dậy rất là nặng mặc đổ dầu nhiều

| Token | Nhãn gốc |
|---|---|
| tích | 0 |
| che | 0 |
| phủ | 0 |
| lỗ | 0 |
| chân | 0 |
| lông | 0 |
| trên | 0 |
| bề | B-ORGAN |
| mặt | I-ORGAN |
| da | I-ORGAN |
| của | 0 |
| bạn | 0 |
| do | 0 |
| đó | 0 |
| nên | 0 |
| bạn | 0 |
| sẽ | 0 |
| thấy | 0 |
| là | 0 |
| da | B-ORGAN |
| của | 0 |
| bạn | 0 |
| ngủ | B-PERSONALCARE |
| dậy | I-PERSONALCARE |
| rất | 0 |
| là | 0 |
| nặng | 0 |
| mặc | 0 |
| đổ | B-DISEASESYMTOM |
| dầu | I-DISEASESYMTOM |
| nhiều | 0 |

## VM600-376 — dòng train 2796 (đếm từ 0)

fumarate sản phẩm đông y mà nhiều sản phẩm như vậy thì không biết là nó có thể là giảm cái việc là xơ vữa mảng

| Token | Nhãn gốc |
|---|---|
| fumarate | B-DRUGCHEMICAL |
| sản | 0 |
| phẩm | 0 |
| đông | B-MEDDEVICETECHNIQUE |
| y | I-MEDDEVICETECHNIQUE |
| mà | 0 |
| nhiều | 0 |
| sản | 0 |
| phẩm | 0 |
| như | 0 |
| vậy | 0 |
| thì | 0 |
| không | 0 |
| biết | 0 |
| là | 0 |
| nó | 0 |
| có | 0 |
| thể | 0 |
| là | 0 |
| giảm | 0 |
| cái | 0 |
| việc | 0 |
| là | 0 |
| xơ | B-DISEASESYMTOM |
| vữa | I-DISEASESYMTOM |
| mảng | I-DISEASESYMTOM |

## VM600-377 — dòng train 2801 (đếm từ 0)

với lại chẳng nói da nhạy cảm chúng ta sẽ sử dụng một cái gọi là các biện pháp lại nghiệm pháp kích thích và chúng ta

| Token | Nhãn gốc |
|---|---|
| với | 0 |
| lại | 0 |
| chẳng | 0 |
| nói | 0 |
| da | B-DISEASESYMTOM |
| nhạy | I-DISEASESYMTOM |
| cảm | I-DISEASESYMTOM |
| chúng | 0 |
| ta | 0 |
| sẽ | 0 |
| sử | 0 |
| dụng | 0 |
| một | 0 |
| cái | 0 |
| gọi | 0 |
| là | 0 |
| các | 0 |
| biện | B-TREATMENT |
| pháp | I-TREATMENT |
| lại | I-TREATMENT |
| nghiệm | I-TREATMENT |
| pháp | I-TREATMENT |
| kích | I-TREATMENT |
| thích | I-TREATMENT |
| và | 0 |
| chúng | 0 |
| ta | 0 |

## VM600-378 — dòng train 2804 (đếm từ 0)

là có thể bây giờ thì mình cũng chưa biết được nhưng mà có thể là đấy là những cái tác nhân mà có thể làm cho

| Token | Nhãn gốc |
|---|---|
| là | 0 |
| có | 0 |
| thể | 0 |
| bây | B-DATETIME |
| giờ | I-DATETIME |
| thì | 0 |
| mình | 0 |
| cũng | 0 |
| chưa | 0 |
| biết | 0 |
| được | 0 |
| nhưng | 0 |
| mà | 0 |
| có | 0 |
| thể | 0 |
| là | 0 |
| đấy | 0 |
| là | 0 |
| những | 0 |
| cái | 0 |
| tác | 0 |
| nhân | 0 |
| mà | 0 |
| có | 0 |
| thể | 0 |
| làm | 0 |
| cho | 0 |

## VM600-379 — dòng train 2813 (đếm từ 0)

này trong ngày hôm nay vâng và trong khi mà chờ đợi các khán

| Token | Nhãn gốc |
|---|---|
| này | 0 |
| trong | 0 |
| ngày | B-DATETIME |
| hôm | I-DATETIME |
| nay | I-DATETIME |
| vâng | 0 |
| và | 0 |
| trong | 0 |
| khi | 0 |
| mà | 0 |
| chờ | 0 |
| đợi | 0 |
| các | 0 |
| khán | 0 |

## VM600-380 — dòng train 2815 (đếm từ 0)

nào và tất cả những cái vấn đề khác về cơ xương khớp vân vân như vậy thì đối với một người lớn tuổi mà có bệnh

| Token | Nhãn gốc |
|---|---|
| nào | 0 |
| và | 0 |
| tất | 0 |
| cả | 0 |
| những | 0 |
| cái | 0 |
| vấn | 0 |
| đề | 0 |
| khác | 0 |
| về | 0 |
| cơ | B-ORGAN |
| xương | I-ORGAN |
| khớp | I-ORGAN |
| vân | 0 |
| vân | 0 |
| như | 0 |
| vậy | 0 |
| thì | 0 |
| đối | 0 |
| với | 0 |
| một | B-UNITCALIBRATOR |
| người | I-UNITCALIBRATOR |
| lớn | I-AGE |
| tuổi | I-AGE |
| mà | 0 |
| có | 0 |
| bệnh | 0 |

## VM600-381 — dòng train 2822 (đếm từ 0)

sẽ tùy thuộc vào từng loại từng nhóm người bệnh và tùy thuộc vào nhiều yếu tố khác nhau như vậy chúng ta thấy rằng

| Token | Nhãn gốc |
|---|---|
| sẽ | 0 |
| tùy | 0 |
| thuộc | 0 |
| vào | 0 |
| từng | 0 |
| loại | 0 |
| từng | 0 |
| nhóm | 0 |
| người | 0 |
| bệnh | 0 |
| và | 0 |
| tùy | 0 |
| thuộc | 0 |
| vào | 0 |
| nhiều | 0 |
| yếu | 0 |
| tố | 0 |
| khác | 0 |
| nhau | 0 |
| như | 0 |
| vậy | 0 |
| chúng | 0 |
| ta | 0 |
| thấy | 0 |
| rằng | 0 |

## VM600-382 — dòng train 2827 (đếm từ 0)

thuật kích thích não sâu thì nó sẽ kéo dài trung bình khoảng từ năm cho tới bảy ngày ở trong bệnh viện và sau khi bảy ngày

| Token | Nhãn gốc |
|---|---|
| thuật | 0 |
| kích | B-SURGERY |
| thích | I-SURGERY |
| não | I-SURGERY |
| sâu | I-SURGERY |
| thì | 0 |
| nó | 0 |
| sẽ | 0 |
| kéo | 0 |
| dài | 0 |
| trung | B-UNITCALIBRATOR |
| bình | I-UNITCALIBRATOR |
| khoảng | 0 |
| từ | 0 |
| năm | 0 |
| cho | 0 |
| tới | 0 |
| bảy | B-DATETIME |
| ngày | I-DATETIME |
| ở | 0 |
| trong | 0 |
| bệnh | B-LOCATION |
| viện | I-LOCATION |
| và | 0 |
| sau | 0 |
| khi | 0 |
| bảy | B-DATETIME |
| ngày | I-DATETIME |

## VM600-383 — dòng train 2847 (đếm từ 0)

cũng đã đưa ra dựa theo những cái nghiên cứu như vậy và ta thấy rằng là mục tiêu đầu tiên đó là giảm từ năm đến mười phần

| Token | Nhãn gốc |
|---|---|
| cũng | 0 |
| đã | 0 |
| đưa | 0 |
| ra | 0 |
| dựa | 0 |
| theo | 0 |
| những | 0 |
| cái | 0 |
| nghiên | B-DIAGNOSTICS |
| cứu | I-DIAGNOSTICS |
| như | 0 |
| vậy | 0 |
| và | 0 |
| ta | 0 |
| thấy | 0 |
| rằng | 0 |
| là | 0 |
| mục | 0 |
| tiêu | 0 |
| đầu | 0 |
| tiên | 0 |
| đó | 0 |
| là | 0 |
| giảm | 0 |
| từ | B-UNITCALIBRATOR |
| năm | I-UNITCALIBRATOR |
| đến | I-UNITCALIBRATOR |
| mười | I-UNITCALIBRATOR |
| phần | I-UNITCALIBRATOR |

## VM600-384 — dòng train 2855 (đếm từ 0)

viêm tắc chúng ta bị viêm tĩnh mạch đấy là những biến chứng mà những người bị suy giãn tĩnh mạch nhiều khi mà chúng ta

| Token | Nhãn gốc |
|---|---|
| viêm | B-DISEASESYMTOM |
| tắc | 0 |
| chúng | 0 |
| ta | 0 |
| bị | 0 |
| viêm | B-DISEASESYMTOM |
| tĩnh | B-ORGAN |
| mạch | I-ORGAN |
| đấy | 0 |
| là | 0 |
| những | 0 |
| biến | B-DISEASESYMTOM |
| chứng | I-DISEASESYMTOM |
| mà | 0 |
| những | 0 |
| người | 0 |
| bị | 0 |
| suy | B-DISEASESYMTOM |
| giãn | I-DISEASESYMTOM |
| tĩnh | I-DISEASESYMTOM |
| mạch | I-DISEASESYMTOM |
| nhiều | 0 |
| khi | 0 |
| mà | 0 |
| chúng | 0 |
| ta | 0 |

## VM600-385 — dòng train 2856 (đếm từ 0)

các thực phẩm mà có chứa vitamin và khoáng chất rồi có thể uống bổ sung thêm

| Token | Nhãn gốc |
|---|---|
| các | 0 |
| thực | B-FOODDRINK |
| phẩm | I-FOODDRINK |
| mà | 0 |
| có | 0 |
| chứa | 0 |
| vitamin | B-DRUGCHEMICAL |
| và | 0 |
| khoáng | B-DRUGCHEMICAL |
| chất | I-DRUGCHEMICAL |
| rồi | 0 |
| có | 0 |
| thể | 0 |
| uống | 0 |
| bổ | 0 |
| sung | 0 |
| thêm | 0 |

## VM600-386 — dòng train 2860 (đếm từ 0)

còn ảnh hưởng rất nhiều thậm chí là đến tâm lý của bệnh nhân và giờ đây thì chúng tôi xin được mời

| Token | Nhãn gốc |
|---|---|
| còn | 0 |
| ảnh | 0 |
| hưởng | 0 |
| rất | B-UNITCALIBRATOR |
| nhiều | I-UNITCALIBRATOR |
| thậm | 0 |
| chí | 0 |
| là | 0 |
| đến | 0 |
| tâm | 0 |
| lý | 0 |
| của | 0 |
| bệnh | B-OCCUPATION |
| nhân | I-OCCUPATION |
| và | 0 |
| giờ | 0 |
| đây | 0 |
| thì | 0 |
| chúng | 0 |
| tôi | 0 |
| xin | 0 |
| được | 0 |
| mời | 0 |

## VM600-387 — dòng train 2866 (đếm từ 0)

cũng đã cho làm một số các cái thăm dò rồi chụp phim vân vân và sơ bộ thì chúng ta biết rằng là bác đã có cái khảo sát

| Token | Nhãn gốc |
|---|---|
| cũng | 0 |
| đã | 0 |
| cho | 0 |
| làm | 0 |
| một | 0 |
| số | 0 |
| các | 0 |
| cái | 0 |
| thăm | 0 |
| dò | 0 |
| rồi | 0 |
| chụp | B-DIAGNOSTICS |
| phim | I-DIAGNOSTICS |
| vân | 0 |
| vân | 0 |
| và | 0 |
| sơ | 0 |
| bộ | 0 |
| thì | 0 |
| chúng | 0 |
| ta | 0 |
| biết | 0 |
| rằng | 0 |
| là | 0 |
| bác | B-AGE |
| đã | 0 |
| có | 0 |
| cái | 0 |
| khảo | B-PREVENTIVEMED |
| sát | I-PREVENTIVEMED |

## VM600-388 — dòng train 2881 (đếm từ 0)

thời đại chính vì là có rất là nhiều các cái tác dụng phụ như thế này cho nên bản thân các bác sĩ rồi bản thân những cái

| Token | Nhãn gốc |
|---|---|
| thời | 0 |
| đại | 0 |
| chính | 0 |
| vì | 0 |
| là | 0 |
| có | 0 |
| rất | 0 |
| là | 0 |
| nhiều | 0 |
| các | 0 |
| cái | 0 |
| tác | B-DISEASESYMTOM |
| dụng | I-DISEASESYMTOM |
| phụ | I-DISEASESYMTOM |
| như | 0 |
| thế | 0 |
| này | 0 |
| cho | 0 |
| nên | 0 |
| bản | 0 |
| thân | 0 |
| các | 0 |
| bác | B-OCCUPATION |
| sĩ | I-OCCUPATION |
| rồi | 0 |
| bản | 0 |
| thân | 0 |
| những | 0 |
| cái | 0 |

## VM600-389 — dòng train 2903 (đếm từ 0)

dụng các sản phẩm mà có chứa những hoạt chất tẩy rửa bề mặt này lâu dài thì sẽ vô tình làm rửa trôi cả cái lớp

| Token | Nhãn gốc |
|---|---|
| dụng | 0 |
| các | 0 |
| sản | 0 |
| phẩm | 0 |
| mà | 0 |
| có | 0 |
| chứa | 0 |
| những | 0 |
| hoạt | B-DRUGCHEMICAL |
| chất | I-DRUGCHEMICAL |
| tẩy | 0 |
| rửa | 0 |
| bề | 0 |
| mặt | 0 |
| này | 0 |
| lâu | 0 |
| dài | 0 |
| thì | 0 |
| sẽ | 0 |
| vô | 0 |
| tình | 0 |
| làm | 0 |
| rửa | 0 |
| trôi | 0 |
| cả | 0 |
| cái | 0 |
| lớp | 0 |

## VM600-390 — dòng train 2928 (đếm từ 0)

cuộc sống của bệnh nhân tốt hơn và bên cạnh điều trị kích thích não sâu thì chúng ta cũng được biết các điều trị can

| Token | Nhãn gốc |
|---|---|
| cuộc | 0 |
| sống | 0 |
| của | 0 |
| bệnh | B-OCCUPATION |
| nhân | I-OCCUPATION |
| tốt | 0 |
| hơn | 0 |
| và | 0 |
| bên | 0 |
| cạnh | 0 |
| điều | B-TREATMENT |
| trị | I-TREATMENT |
| kích | B-SURGERY |
| thích | I-SURGERY |
| não | I-SURGERY |
| sâu | I-SURGERY |
| thì | 0 |
| chúng | 0 |
| ta | 0 |
| cũng | 0 |
| được | 0 |
| biết | 0 |
| các | 0 |
| điều | B-TREATMENT |
| trị | I-TREATMENT |
| can | 0 |

## VM600-391 — dòng train 2937 (đếm từ 0)

một cái hành trình như vậy thì cái việc điều trị của béo phì ở trong một cái giai đoạn này nó chỉ

| Token | Nhãn gốc |
|---|---|
| một | 0 |
| cái | 0 |
| hành | 0 |
| trình | 0 |
| như | 0 |
| vậy | 0 |
| thì | 0 |
| cái | 0 |
| việc | 0 |
| điều | B-TREATMENT |
| trị | I-TREATMENT |
| của | 0 |
| béo | B-DISEASESYMTOM |
| phì | I-DISEASESYMTOM |
| ở | 0 |
| trong | 0 |
| một | 0 |
| cái | 0 |
| giai | 0 |
| đoạn | 0 |
| này | 0 |
| nó | 0 |
| chỉ | 0 |

## VM600-392 — dòng train 2946 (đếm từ 0)

vâng và hiện tại thì thời lượng của chương trình cũng không còn nhiều tuy nhiên còn rất là nhiều khán giả đã gọi điện tới và mong đợi được sự tư vấn của

| Token | Nhãn gốc |
|---|---|
| vâng | 0 |
| và | 0 |
| hiện | 0 |
| tại | 0 |
| thì | 0 |
| thời | 0 |
| lượng | 0 |
| của | 0 |
| chương | 0 |
| trình | 0 |
| cũng | 0 |
| không | 0 |
| còn | 0 |
| nhiều | 0 |
| tuy | 0 |
| nhiên | 0 |
| còn | 0 |
| rất | 0 |
| là | 0 |
| nhiều | 0 |
| khán | B-OCCUPATION |
| giả | I-OCCUPATION |
| đã | 0 |
| gọi | 0 |
| điện | 0 |
| tới | 0 |
| và | 0 |
| mong | 0 |
| đợi | 0 |
| được | 0 |
| sự | 0 |
| tư | B-PERSONALCARE |
| vấn | I-PERSONALCARE |
| của | 0 |

## VM600-393 — dòng train 2947 (đếm từ 0)

nhận được phần thưởng từ chương trình mà thôi vâng ạ như là bác sĩ chia sẻ thì rõ ràng là đông trùng hạ thảo thì có cái

| Token | Nhãn gốc |
|---|---|
| nhận | 0 |
| được | 0 |
| phần | 0 |
| thưởng | 0 |
| từ | 0 |
| chương | 0 |
| trình | 0 |
| mà | 0 |
| thôi | 0 |
| vâng | 0 |
| ạ | 0 |
| như | 0 |
| là | 0 |
| bác | B-OCCUPATION |
| sĩ | I-OCCUPATION |
| chia | 0 |
| sẻ | 0 |
| thì | 0 |
| rõ | 0 |
| ràng | 0 |
| là | 0 |
| đông | B-DRUGCHEMICAL |
| trùng | I-DRUGCHEMICAL |
| hạ | I-DRUGCHEMICAL |
| thảo | I-DRUGCHEMICAL |
| thì | 0 |
| có | 0 |
| cái | 0 |

## VM600-394 — dòng train 2948 (đếm từ 0)

không được nghỉ ngơi chính vì vậy cho nên là cái lời khuyên của chúng ta trong trường hợp này thì khi mà chúng ta làm

| Token | Nhãn gốc |
|---|---|
| không | 0 |
| được | 0 |
| nghỉ | B-PERSONALCARE |
| ngơi | I-PERSONALCARE |
| chính | 0 |
| vì | 0 |
| vậy | 0 |
| cho | 0 |
| nên | 0 |
| là | 0 |
| cái | 0 |
| lời | 0 |
| khuyên | 0 |
| của | 0 |
| chúng | 0 |
| ta | 0 |
| trong | 0 |
| trường | 0 |
| hợp | 0 |
| này | 0 |
| thì | 0 |
| khi | 0 |
| mà | 0 |
| chúng | 0 |
| ta | 0 |
| làm | 0 |

## VM600-395 — dòng train 2960 (đếm từ 0)

được cái tình trạng của anh hiện tại đúng không ạ chứ ở đây thì chúng tôi cũng chỉ thăm khám qua những cái lời

| Token | Nhãn gốc |
|---|---|
| được | 0 |
| cái | 0 |
| tình | 0 |
| trạng | 0 |
| của | 0 |
| anh | B-GENDER |
| hiện | 0 |
| tại | 0 |
| đúng | 0 |
| không | 0 |
| ạ | 0 |
| chứ | 0 |
| ở | 0 |
| đây | 0 |
| thì | 0 |
| chúng | 0 |
| tôi | 0 |
| cũng | 0 |
| chỉ | 0 |
| thăm | B-TREATMENT |
| khám | I-TREATMENT |
| qua | 0 |
| những | 0 |
| cái | 0 |
| lời | 0 |

## VM600-396 — dòng train 2972 (đếm từ 0)

điều trị bằng các loại thuốc ức chế miễn dịch mạnh và thường có những mặt trái đáng kể không ít trong số đó bao gồm

| Token | Nhãn gốc |
|---|---|
| điều | B-TREATMENT |
| trị | I-TREATMENT |
| bằng | 0 |
| các | 0 |
| loại | 0 |
| thuốc | B-DRUGCHEMICAL |
| ức | B-PREVENTIVEMED |
| chế | I-PREVENTIVEMED |
| miễn | I-PREVENTIVEMED |
| dịch | I-PREVENTIVEMED |
| mạnh | 0 |
| và | 0 |
| thường | 0 |
| có | 0 |
| những | 0 |
| mặt | 0 |
| trái | 0 |
| đáng | 0 |
| kể | 0 |
| không | 0 |
| ít | 0 |
| trong | 0 |
| số | 0 |
| đó | 0 |
| bao | 0 |
| gồm | 0 |

## VM600-397 — dòng train 2973 (đếm từ 0)

tất cả đấy là những lời có cánh những cái lời mà nó chả có tính khoa học gì cả thế cho nên là điều đầu tiên khuyên bác là

| Token | Nhãn gốc |
|---|---|
| tất | 0 |
| cả | 0 |
| đấy | 0 |
| là | 0 |
| những | 0 |
| lời | 0 |
| có | 0 |
| cánh | 0 |
| những | 0 |
| cái | 0 |
| lời | 0 |
| mà | 0 |
| nó | 0 |
| chả | 0 |
| có | 0 |
| tính | 0 |
| khoa | 0 |
| học | 0 |
| gì | 0 |
| cả | 0 |
| thế | 0 |
| cho | 0 |
| nên | 0 |
| là | 0 |
| điều | 0 |
| đầu | 0 |
| tiên | 0 |
| khuyên | 0 |
| bác | B-AGE |
| là | 0 |

## VM600-398 — dòng train 2986 (đếm từ 0)

mảng xơ vữa này để giúp cho máu thông lên não lên tim tốt và từ đó cải thiện các triệu chứng như là đau đầu hoa mắt chóng

| Token | Nhãn gốc |
|---|---|
| mảng | B-DISEASESYMTOM |
| xơ | I-DISEASESYMTOM |
| vữa | I-DISEASESYMTOM |
| này | 0 |
| để | 0 |
| giúp | 0 |
| cho | 0 |
| máu | B-ORGAN |
| thông | 0 |
| lên | 0 |
| não | B-ORGAN |
| lên | 0 |
| tim | B-ORGAN |
| tốt | 0 |
| và | 0 |
| từ | 0 |
| đó | 0 |
| cải | B-TREATMENT |
| thiện | I-TREATMENT |
| các | 0 |
| triệu | B-DISEASESYMTOM |
| chứng | I-DISEASESYMTOM |
| như | 0 |
| là | 0 |
| đau | B-DISEASESYMTOM |
| đầu | I-DISEASESYMTOM |
| hoa | B-DISEASESYMTOM |
| mắt | I-DISEASESYMTOM |
| chóng | 0 |

## VM600-399 — dòng train 2991 (đếm từ 0)

chuột rút đúng không ạ ở đây chuột rút thì chúng ta nhớ rằng là nó cũng có một số các cái nhóm nguyên nhân thông thường chúng ta sẽ nghĩ ngay đến cái câu chuyện

| Token | Nhãn gốc |
|---|---|
| chuột | B-DISEASESYMTOM |
| rút | I-DISEASESYMTOM |
| đúng | 0 |
| không | 0 |
| ạ | 0 |
| ở | 0 |
| đây | 0 |
| chuột | B-DISEASESYMTOM |
| rút | I-DISEASESYMTOM |
| thì | 0 |
| chúng | 0 |
| ta | 0 |
| nhớ | 0 |
| rằng | 0 |
| là | 0 |
| nó | 0 |
| cũng | 0 |
| có | 0 |
| một | 0 |
| số | 0 |
| các | 0 |
| cái | 0 |
| nhóm | 0 |
| nguyên | 0 |
| nhân | 0 |
| thông | 0 |
| thường | 0 |
| chúng | 0 |
| ta | 0 |
| sẽ | 0 |
| nghĩ | 0 |
| ngay | 0 |
| đến | 0 |
| cái | 0 |
| câu | 0 |
| chuyện | 0 |

## VM600-400 — dòng train 3007 (đếm từ 0)

sinh bị rụng tóc hay không cảm ơn em các chị em phụ nữ thân mến

| Token | Nhãn gốc |
|---|---|
| sinh | 0 |
| bị | 0 |
| rụng | B-DISEASESYMTOM |
| tóc | I-DISEASESYMTOM |
| hay | 0 |
| không | 0 |
| cảm | 0 |
| ơn | 0 |
| em | 0 |
| các | 0 |
| chị | B-GENDER |
| em | I-GENDER |
| phụ | B-GENDER |
| nữ | I-GENDER |
| thân | 0 |
| mến | 0 |

## VM600-401 — dòng train 3011 (đếm từ 0)

sau mười năm thì triệu chứng các triệu chứng ngoài vận động nó xuất hiện nhiều hơn sa sút trí tuệ rồi táo bón rồi mất ổn định

| Token | Nhãn gốc |
|---|---|
| sau | B-DATETIME |
| mười | I-DATETIME |
| năm | I-DATETIME |
| thì | 0 |
| triệu | B-DISEASESYMTOM |
| chứng | I-DISEASESYMTOM |
| các | 0 |
| triệu | B-DISEASESYMTOM |
| chứng | I-DISEASESYMTOM |
| ngoài | 0 |
| vận | 0 |
| động | 0 |
| nó | 0 |
| xuất | 0 |
| hiện | 0 |
| nhiều | 0 |
| hơn | 0 |
| sa | B-DISEASESYMTOM |
| sút | I-DISEASESYMTOM |
| trí | I-DISEASESYMTOM |
| tuệ | I-DISEASESYMTOM |
| rồi | 0 |
| táo | B-DISEASESYMTOM |
| bón | I-DISEASESYMTOM |
| rồi | 0 |
| mất | 0 |
| ổn | 0 |
| định | 0 |

## VM600-402 — dòng train 3026 (đếm từ 0)

chắn sẽ dẫn tình trạng cơ thể tình trạng cơ thể chúng ta dẫn đến suy kiệt và chúng ta không còn được cả cái sức đề

| Token | Nhãn gốc |
|---|---|
| chắn | 0 |
| sẽ | 0 |
| dẫn | 0 |
| tình | 0 |
| trạng | 0 |
| cơ | B-ORGAN |
| thể | I-ORGAN |
| tình | 0 |
| trạng | 0 |
| cơ | B-ORGAN |
| thể | I-ORGAN |
| chúng | 0 |
| ta | 0 |
| dẫn | 0 |
| đến | 0 |
| suy | B-DISEASESYMTOM |
| kiệt | I-DISEASESYMTOM |
| và | 0 |
| chúng | 0 |
| ta | 0 |
| không | 0 |
| còn | 0 |
| được | 0 |
| cả | 0 |
| cái | 0 |
| sức | 0 |
| đề | 0 |

## VM600-403 — dòng train 3027 (đếm từ 0)

bị ngã ta phải đỡ ngay giữa ngay để người bệnh không có bị ngã không bị chấn thương rồi nếu mà bệnh nhân đang ăn ăn

| Token | Nhãn gốc |
|---|---|
| bị | 0 |
| ngã | 0 |
| ta | 0 |
| phải | 0 |
| đỡ | 0 |
| ngay | 0 |
| giữa | 0 |
| ngay | 0 |
| để | 0 |
| người | 0 |
| bệnh | 0 |
| không | 0 |
| có | 0 |
| bị | 0 |
| ngã | 0 |
| không | 0 |
| bị | 0 |
| chấn | B-DISEASESYMTOM |
| thương | I-DISEASESYMTOM |
| rồi | 0 |
| nếu | 0 |
| mà | 0 |
| bệnh | B-OCCUPATION |
| nhân | I-OCCUPATION |
| đang | 0 |
| ăn | 0 |
| ăn | 0 |

## VM600-404 — dòng train 3033 (đếm từ 0)

được tốt nhất vai trò thứ ba của đối với lại dinh dưỡng đó là dinh dưỡng thậm chí

| Token | Nhãn gốc |
|---|---|
| được | 0 |
| tốt | 0 |
| nhất | 0 |
| vai | 0 |
| trò | 0 |
| thứ | 0 |
| ba | 0 |
| của | 0 |
| đối | 0 |
| với | 0 |
| lại | 0 |
| dinh | 0 |
| dưỡng | 0 |
| đó | 0 |
| là | 0 |
| dinh | 0 |
| dưỡng | 0 |
| thậm | 0 |
| chí | 0 |

## VM600-405 — dòng train 3039 (đếm từ 0)

nào là đông trùng hạ thảo công dụng của nó ra sao đặc biệt là chúng ta có kiến

| Token | Nhãn gốc |
|---|---|
| nào | 0 |
| là | 0 |
| đông | B-DRUGCHEMICAL |
| trùng | I-DRUGCHEMICAL |
| hạ | I-DRUGCHEMICAL |
| thảo | I-DRUGCHEMICAL |
| công | 0 |
| dụng | 0 |
| của | 0 |
| nó | 0 |
| ra | 0 |
| sao | 0 |
| đặc | 0 |
| biệt | 0 |
| là | 0 |
| chúng | 0 |
| ta | 0 |
| có | 0 |
| kiến | 0 |

## VM600-406 — dòng train 3062 (đếm từ 0)

yếu đầu tiên là yếu tay yếu chân yếu thứ hai là giữa các cơ mặt làm cho mặt

| Token | Nhãn gốc |
|---|---|
| yếu | 0 |
| đầu | 0 |
| tiên | 0 |
| là | 0 |
| yếu | B-DISEASESYMTOM |
| tay | I-DISEASESYMTOM |
| yếu | B-DISEASESYMTOM |
| chân | I-DISEASESYMTOM |
| yếu | 0 |
| thứ | 0 |
| hai | 0 |
| là | 0 |
| giữa | 0 |
| các | 0 |
| cơ | B-ORGAN |
| mặt | I-ORGAN |
| làm | 0 |
| cho | 0 |
| mặt | 0 |

## VM600-407 — dòng train 3069 (đếm từ 0)

của bác là não thì nó sẽ gây ra rất nhiều triệu chứng khác nhau trong đó có người thì ví dụ như bác là mất ngủ là

| Token | Nhãn gốc |
|---|---|
| của | 0 |
| bác | B-AGE |
| là | 0 |
| não | B-ORGAN |
| thì | 0 |
| nó | 0 |
| sẽ | 0 |
| gây | 0 |
| ra | 0 |
| rất | B-UNITCALIBRATOR |
| nhiều | I-UNITCALIBRATOR |
| triệu | B-DISEASESYMTOM |
| chứng | I-DISEASESYMTOM |
| khác | 0 |
| nhau | 0 |
| trong | 0 |
| đó | 0 |
| có | 0 |
| người | 0 |
| thì | 0 |
| ví | 0 |
| dụ | 0 |
| như | 0 |
| bác | B-AGE |
| là | 0 |
| mất | B-DISEASESYMTOM |
| ngủ | I-DISEASESYMTOM |
| là | 0 |

## VM600-408 — dòng train 3070 (đếm từ 0)

đoạn sau sanh thì mái tóc dễ gọi là nó mềm mại và nó yếu ớt thế cho nên là

| Token | Nhãn gốc |
|---|---|
| đoạn | 0 |
| sau | B-DATETIME |
| sanh | I-DATETIME |
| thì | 0 |
| mái | B-ORGAN |
| tóc | I-ORGAN |
| dễ | 0 |
| gọi | 0 |
| là | 0 |
| nó | 0 |
| mềm | 0 |
| mại | 0 |
| và | 0 |
| nó | 0 |
| yếu | B-DISEASESYMTOM |
| ớt | I-DISEASESYMTOM |
| thế | 0 |
| cho | 0 |
| nên | 0 |
| là | 0 |

## VM600-409 — dòng train 3071 (đếm từ 0)

tiết được pepsin và tiết không tiết được pepsin của dạ dày chỉ liên quan đến một phần kể

| Token | Nhãn gốc |
|---|---|
| tiết | 0 |
| được | 0 |
| pepsin | B-DRUGCHEMICAL |
| và | 0 |
| tiết | 0 |
| không | 0 |
| tiết | 0 |
| được | 0 |
| pepsin | B-DRUGCHEMICAL |
| của | 0 |
| dạ | B-ORGAN |
| dày | I-ORGAN |
| chỉ | 0 |
| liên | 0 |
| quan | 0 |
| đến | 0 |
| một | B-UNITCALIBRATOR |
| phần | I-UNITCALIBRATOR |
| kể | 0 |

## VM600-410 — dòng train 3077 (đếm từ 0)

biết rằng là những người bệnh kích thích những người bệnh parkinson mà cần phẫu thuốc kích thích não sâu thì chúng

| Token | Nhãn gốc |
|---|---|
| biết | 0 |
| rằng | 0 |
| là | 0 |
| những | 0 |
| người | 0 |
| bệnh | 0 |
| kích | 0 |
| thích | 0 |
| những | 0 |
| người | 0 |
| bệnh | 0 |
| parkinson | B-DISEASESYMTOM |
| mà | 0 |
| cần | 0 |
| phẫu | 0 |
| thuốc | B-DRUGCHEMICAL |
| kích | B-SURGERY |
| thích | I-SURGERY |
| não | I-SURGERY |
| sâu | I-SURGERY |
| thì | 0 |
| chúng | 0 |

## VM600-411 — dòng train 3085 (đếm từ 0)

mình sẽ kiểm tra những các thiết bị bên ngoài đảm bảo có thể thống nhất rồi thì lúc đó là kết thúc phẫu thuật

| Token | Nhãn gốc |
|---|---|
| mình | 0 |
| sẽ | 0 |
| kiểm | B-DIAGNOSTICS |
| tra | I-DIAGNOSTICS |
| những | 0 |
| các | 0 |
| thiết | 0 |
| bị | 0 |
| bên | B-LOCATION |
| ngoài | I-LOCATION |
| đảm | 0 |
| bảo | 0 |
| có | 0 |
| thể | 0 |
| thống | 0 |
| nhất | 0 |
| rồi | 0 |
| thì | 0 |
| lúc | 0 |
| đó | 0 |
| là | 0 |
| kết | 0 |
| thúc | 0 |
| phẫu | B-SURGERY |
| thuật | I-SURGERY |

## VM600-412 — dòng train 3086 (đếm từ 0)

ngoại khoa thì là cái từ trong chuyên môn nhưng mà để nói cho dễ hiểu đó là mổ thì người ta có chia làm hai cái nhóm

| Token | Nhãn gốc |
|---|---|
| ngoại | B-TREATMENT |
| khoa | I-TREATMENT |
| thì | 0 |
| là | 0 |
| cái | 0 |
| từ | 0 |
| trong | 0 |
| chuyên | 0 |
| môn | 0 |
| nhưng | 0 |
| mà | 0 |
| để | 0 |
| nói | 0 |
| cho | 0 |
| dễ | 0 |
| hiểu | 0 |
| đó | 0 |
| là | 0 |
| mổ | B-SURGERY |
| thì | 0 |
| người | 0 |
| ta | 0 |
| có | 0 |
| chia | 0 |
| làm | 0 |
| hai | 0 |
| cái | 0 |
| nhóm | 0 |

## VM600-413 — dòng train 3092 (đếm từ 0)

là một sự tán thành lớn cho quan điểm rằng thực phẩm quan trọng vượt trội hơn hoàn cảnh khác trong cuộc sống mà chúng

| Token | Nhãn gốc |
|---|---|
| là | 0 |
| một | 0 |
| sự | 0 |
| tán | 0 |
| thành | 0 |
| lớn | 0 |
| cho | 0 |
| quan | 0 |
| điểm | 0 |
| rằng | 0 |
| thực | B-FOODDRINK |
| phẩm | I-FOODDRINK |
| quan | 0 |
| trọng | 0 |
| vượt | 0 |
| trội | 0 |
| hơn | 0 |
| hoàn | 0 |
| cảnh | 0 |
| khác | 0 |
| trong | 0 |
| cuộc | 0 |
| sống | 0 |
| mà | 0 |
| chúng | 0 |

## VM600-414 — dòng train 3093 (đếm từ 0)

viêm loét đại tràng và ung thư chúng ta sẽ khám phá quá trình này chi tiết hơn

| Token | Nhãn gốc |
|---|---|
| viêm | B-DISEASESYMTOM |
| loét | I-DISEASESYMTOM |
| đại | B-ORGAN |
| tràng | I-ORGAN |
| và | 0 |
| ung | B-DISEASESYMTOM |
| thư | I-DISEASESYMTOM |
| chúng | 0 |
| ta | 0 |
| sẽ | 0 |
| khám | B-DIAGNOSTICS |
| phá | 0 |
| quá | 0 |
| trình | 0 |
| này | 0 |
| chi | 0 |
| tiết | 0 |
| hơn | 0 |

## VM600-415 — dòng train 3120 (đếm từ 0)

khô hơn đôi khi là từ một cái làn da là thường mà trở thành một cái làn da nhạy cảm dễ gây kích ứng và dị ứng hơn do đó

| Token | Nhãn gốc |
|---|---|
| khô | 0 |
| hơn | 0 |
| đôi | 0 |
| khi | 0 |
| là | 0 |
| từ | 0 |
| một | 0 |
| cái | 0 |
| làn | B-ORGAN |
| da | I-ORGAN |
| là | 0 |
| thường | 0 |
| mà | 0 |
| trở | 0 |
| thành | 0 |
| một | 0 |
| cái | 0 |
| làn | B-DISEASESYMTOM |
| da | I-DISEASESYMTOM |
| nhạy | I-DISEASESYMTOM |
| cảm | I-DISEASESYMTOM |
| dễ | 0 |
| gây | 0 |
| kích | B-DISEASESYMTOM |
| ứng | I-DISEASESYMTOM |
| và | 0 |
| dị | B-DISEASESYMTOM |
| ứng | I-DISEASESYMTOM |
| hơn | 0 |
| do | 0 |
| đó | 0 |

## VM600-416 — dòng train 3126 (đếm từ 0)

cũng xin nhờ bác sĩ có thể cho biết cụ thể hơn về mối quan hệ cũng như là tác

| Token | Nhãn gốc |
|---|---|
| cũng | 0 |
| xin | 0 |
| nhờ | 0 |
| bác | B-OCCUPATION |
| sĩ | I-OCCUPATION |
| có | 0 |
| thể | 0 |
| cho | 0 |
| biết | 0 |
| cụ | 0 |
| thể | 0 |
| hơn | 0 |
| về | 0 |
| mối | 0 |
| quan | B-DISEASESYMTOM |
| hệ | I-DISEASESYMTOM |
| cũng | 0 |
| như | 0 |
| là | 0 |
| tác | 0 |

## VM600-417 — dòng train 3127 (đếm từ 0)

tôi sẽ giúp bạn làm điều đó giải thích khoa học đằng sau lợi khuẩn và cách chọn

| Token | Nhãn gốc |
|---|---|
| tôi | 0 |
| sẽ | 0 |
| giúp | 0 |
| bạn | 0 |
| làm | 0 |
| điều | 0 |
| đó | 0 |
| giải | 0 |
| thích | 0 |
| khoa | 0 |
| học | 0 |
| đằng | 0 |
| sau | 0 |
| lợi | B-DRUGCHEMICAL |
| khuẩn | I-DRUGCHEMICAL |
| và | 0 |
| cách | 0 |
| chọn | 0 |

## VM600-418 — dòng train 3131 (đếm từ 0)

người dân đã cho chúng tôi nhiều cái thông tin ví dụ như những trường hợp tai nạn bất ngờ những bệnh tật mà phải cấp

| Token | Nhãn gốc |
|---|---|
| người | B-OCCUPATION |
| dân | I-OCCUPATION |
| đã | 0 |
| cho | 0 |
| chúng | 0 |
| tôi | 0 |
| nhiều | 0 |
| cái | 0 |
| thông | 0 |
| tin | 0 |
| ví | 0 |
| dụ | 0 |
| như | 0 |
| những | 0 |
| trường | 0 |
| hợp | 0 |
| tai | B-DISEASESYMTOM |
| nạn | I-DISEASESYMTOM |
| bất | 0 |
| ngờ | 0 |
| những | 0 |
| bệnh | 0 |
| tật | 0 |
| mà | 0 |
| phải | 0 |
| cấp | 0 |

## VM600-419 — dòng train 3133 (đếm từ 0)

huyết áp này những người bị rối loạn mỡ máu này những người các bệnh lý bệnh tim mạch thì nó sẽ có cái tác động lên các

| Token | Nhãn gốc |
|---|---|
| huyết | B-DISEASESYMTOM |
| áp | I-DISEASESYMTOM |
| này | 0 |
| những | 0 |
| người | 0 |
| bị | 0 |
| rối | B-DISEASESYMTOM |
| loạn | I-DISEASESYMTOM |
| mỡ | I-DISEASESYMTOM |
| máu | I-DISEASESYMTOM |
| này | 0 |
| những | 0 |
| người | 0 |
| các | 0 |
| bệnh | 0 |
| lý | 0 |
| bệnh | 0 |
| tim | B-ORGAN |
| mạch | I-ORGAN |
| thì | 0 |
| nó | 0 |
| sẽ | 0 |
| có | 0 |
| cái | 0 |
| tác | 0 |
| động | 0 |
| lên | 0 |
| các | 0 |

## VM600-420 — dòng train 3139 (đếm từ 0)

bôi kem dưỡng trước khi đi ngủ nhưng ngủ dậy mặt vẫn còn nhiều dầu xưng cháu vậy

| Token | Nhãn gốc |
|---|---|
| bôi | 0 |
| kem | B-DRUGCHEMICAL |
| dưỡng | I-DRUGCHEMICAL |
| trước | 0 |
| khi | 0 |
| đi | B-PERSONALCARE |
| ngủ | I-PERSONALCARE |
| nhưng | 0 |
| ngủ | B-PERSONALCARE |
| dậy | I-PERSONALCARE |
| mặt | 0 |
| vẫn | 0 |
| còn | 0 |
| nhiều | 0 |
| dầu | 0 |
| xưng | 0 |
| cháu | B-AGE |
| vậy | 0 |

## VM600-421 — dòng train 3142 (đếm từ 0)

trị béo phì nó rất là ngoạn mục và sau này nó không chỉ về cải thiện cái hình ảnh mà nó giúp làm cho chúng ta

| Token | Nhãn gốc |
|---|---|
| trị | 0 |
| béo | B-DISEASESYMTOM |
| phì | I-DISEASESYMTOM |
| nó | 0 |
| rất | 0 |
| là | 0 |
| ngoạn | 0 |
| mục | 0 |
| và | 0 |
| sau | 0 |
| này | 0 |
| nó | 0 |
| không | 0 |
| chỉ | 0 |
| về | 0 |
| cải | B-TREATMENT |
| thiện | I-TREATMENT |
| cái | 0 |
| hình | 0 |
| ảnh | 0 |
| mà | 0 |
| nó | 0 |
| giúp | 0 |
| làm | 0 |
| cho | 0 |
| chúng | 0 |
| ta | 0 |

## VM600-422 — dòng train 3143 (đếm từ 0)

thì không phải là của riêng ai cả đối tượng nào chúng ta cũng rất là dễ gặp phải và chúng tôi cũng để ý là có những

| Token | Nhãn gốc |
|---|---|
| thì | 0 |
| không | 0 |
| phải | 0 |
| là | 0 |
| của | 0 |
| riêng | 0 |
| ai | 0 |
| cả | 0 |
| đối | 0 |
| tượng | 0 |
| nào | 0 |
| chúng | 0 |
| ta | 0 |
| cũng | 0 |
| rất | 0 |
| là | 0 |
| dễ | 0 |
| gặp | 0 |
| phải | 0 |
| và | 0 |
| chúng | 0 |
| tôi | 0 |
| cũng | 0 |
| để | 0 |
| ý | 0 |
| là | 0 |
| có | 0 |
| những | 0 |

## VM600-423 — dòng train 3162 (đếm từ 0)

trị chưa hiện nay chưa có cái phương pháp nào điều trị khỏi mà chỉ là điều trị để giúp cho mình đưa cái con số

| Token | Nhãn gốc |
|---|---|
| trị | 0 |
| chưa | 0 |
| hiện | B-DATETIME |
| nay | I-DATETIME |
| chưa | 0 |
| có | 0 |
| cái | 0 |
| phương | 0 |
| pháp | 0 |
| nào | 0 |
| điều | B-TREATMENT |
| trị | I-TREATMENT |
| khỏi | 0 |
| mà | 0 |
| chỉ | 0 |
| là | 0 |
| điều | B-TREATMENT |
| trị | I-TREATMENT |
| để | 0 |
| giúp | 0 |
| cho | 0 |
| mình | 0 |
| đưa | 0 |
| cái | 0 |
| con | 0 |
| số | 0 |

## VM600-424 — dòng train 3165 (đếm từ 0)

thậm chí gây tử vong bạn có thể không quen được với phía bên kia của câu chuyện rằng mỗi nhịp tim nhịp thở và sợ

| Token | Nhãn gốc |
|---|---|
| thậm | 0 |
| chí | 0 |
| gây | 0 |
| tử | B-DISEASESYMTOM |
| vong | I-DISEASESYMTOM |
| bạn | 0 |
| có | 0 |
| thể | 0 |
| không | 0 |
| quen | 0 |
| được | 0 |
| với | 0 |
| phía | 0 |
| bên | 0 |
| kia | 0 |
| của | 0 |
| câu | 0 |
| chuyện | 0 |
| rằng | 0 |
| mỗi | 0 |
| nhịp | B-UNITCALIBRATOR |
| tim | I-UNITCALIBRATOR |
| nhịp | B-UNITCALIBRATOR |
| thở | I-UNITCALIBRATOR |
| và | 0 |
| sợ | 0 |

## VM600-425 — dòng train 3166 (đếm từ 0)

khỏi ra tình trạng bệnh và đây của chúng ta là ung thư thì cái tinh thần của người bị bệnh rất kiên cường cái thứ hai đó là chúng ta

| Token | Nhãn gốc |
|---|---|
| khỏi | 0 |
| ra | 0 |
| tình | 0 |
| trạng | 0 |
| bệnh | 0 |
| và | 0 |
| đây | 0 |
| của | 0 |
| chúng | 0 |
| ta | 0 |
| là | 0 |
| ung | B-DISEASESYMTOM |
| thư | I-DISEASESYMTOM |
| thì | 0 |
| cái | 0 |
| tinh | 0 |
| thần | 0 |
| của | 0 |
| người | 0 |
| bị | B-DISEASESYMTOM |
| bệnh | I-DISEASESYMTOM |
| rất | 0 |
| kiên | 0 |
| cường | 0 |
| cái | B-UNITCALIBRATOR |
| thứ | I-UNITCALIBRATOR |
| hai | I-UNITCALIBRATOR |
| đó | 0 |
| là | 0 |
| chúng | 0 |
| ta | 0 |

## VM600-426 — dòng train 3172 (đếm từ 0)

nhiều các phương pháp điều trị được được điều trị áp dụng chẩn đoán sớm vân vân thì tuổi thọ của người việt nam của

| Token | Nhãn gốc |
|---|---|
| nhiều | 0 |
| các | 0 |
| phương | 0 |
| pháp | 0 |
| điều | B-TREATMENT |
| trị | I-TREATMENT |
| được | 0 |
| được | 0 |
| điều | B-TREATMENT |
| trị | I-TREATMENT |
| áp | 0 |
| dụng | 0 |
| chẩn | B-DIAGNOSTICS |
| đoán | I-DIAGNOSTICS |
| sớm | 0 |
| vân | 0 |
| vân | 0 |
| thì | 0 |
| tuổi | 0 |
| thọ | 0 |
| của | 0 |
| người | 0 |
| việt | B-LOCATION |
| nam | I-LOCATION |
| của | 0 |

## VM600-427 — dòng train 3177 (đếm từ 0)

bắt đầu từ ruột điều này xảy ra rất lâu trước khi nền văn minh có bất kỳ bằng chứng hoặc lý thuyết vững vàng nào để

| Token | Nhãn gốc |
|---|---|
| bắt | 0 |
| đầu | 0 |
| từ | 0 |
| ruột | B-ORGAN |
| điều | 0 |
| này | 0 |
| xảy | 0 |
| ra | 0 |
| rất | 0 |
| lâu | 0 |
| trước | 0 |
| khi | 0 |
| nền | 0 |
| văn | 0 |
| minh | 0 |
| có | 0 |
| bất | 0 |
| kỳ | 0 |
| bằng | 0 |
| chứng | 0 |
| hoặc | 0 |
| lý | 0 |
| thuyết | 0 |
| vững | 0 |
| vàng | 0 |
| nào | 0 |
| để | 0 |

## VM600-428 — dòng train 3192 (đếm từ 0)

với đái tháo đường thì nó có rất rất nhiều các thể lụy những cái biến chứng của nó thế thì khi mà chúng ta bị đái

| Token | Nhãn gốc |
|---|---|
| với | 0 |
| đái | B-DISEASESYMTOM |
| tháo | I-DISEASESYMTOM |
| đường | I-DISEASESYMTOM |
| thì | 0 |
| nó | 0 |
| có | 0 |
| rất | 0 |
| rất | B-UNITCALIBRATOR |
| nhiều | I-UNITCALIBRATOR |
| các | 0 |
| thể | 0 |
| lụy | 0 |
| những | 0 |
| cái | 0 |
| biến | B-DISEASESYMTOM |
| chứng | I-DISEASESYMTOM |
| của | 0 |
| nó | 0 |
| thế | 0 |
| thì | 0 |
| khi | 0 |
| mà | 0 |
| chúng | 0 |
| ta | 0 |
| bị | 0 |
| đái | 0 |

## VM600-429 — dòng train 3194 (đếm từ 0)

thư vẫn ăn bởi vì chúng ta biết rằng không có một cái thực phẩm nào là tốt nhất cả mỗi thực phẩm có một giá trị riêng

| Token | Nhãn gốc |
|---|---|
| thư | 0 |
| vẫn | 0 |
| ăn | 0 |
| bởi | 0 |
| vì | 0 |
| chúng | 0 |
| ta | 0 |
| biết | 0 |
| rằng | 0 |
| không | 0 |
| có | 0 |
| một | 0 |
| cái | 0 |
| thực | B-FOODDRINK |
| phẩm | I-FOODDRINK |
| nào | 0 |
| là | 0 |
| tốt | 0 |
| nhất | 0 |
| cả | 0 |
| mỗi | 0 |
| thực | B-FOODDRINK |
| phẩm | I-FOODDRINK |
| có | 0 |
| một | 0 |
| giá | 0 |
| trị | 0 |
| riêng | 0 |

## VM600-430 — dòng train 3202 (đếm từ 0)

cho mình không sử dụng rượu bia cà phê và có hút thuốc lá đặc biệt ở trong cái giai đoạn này thế và như có những cái

| Token | Nhãn gốc |
|---|---|
| cho | 0 |
| mình | 0 |
| không | 0 |
| sử | 0 |
| dụng | 0 |
| rượu | B-FOODDRINK |
| bia | I-FOODDRINK |
| cà | B-FOODDRINK |
| phê | I-FOODDRINK |
| và | 0 |
| có | 0 |
| hút | 0 |
| thuốc | B-FOODDRINK |
| lá | I-FOODDRINK |
| đặc | 0 |
| biệt | 0 |
| ở | 0 |
| trong | 0 |
| cái | 0 |
| giai | 0 |
| đoạn | 0 |
| này | 0 |
| thế | 0 |
| và | 0 |
| như | 0 |
| có | 0 |
| những | 0 |
| cái | 0 |

## VM600-431 — dòng train 3206 (đếm từ 0)

xét mới trả lời cho người bệnh một cách cụ thể theo từng trường hợp kính thưa tất cả quý vị bởi vì thời lượng trong

| Token | Nhãn gốc |
|---|---|
| xét | 0 |
| mới | 0 |
| trả | 0 |
| lời | 0 |
| cho | 0 |
| người | 0 |
| bệnh | 0 |
| một | 0 |
| cách | 0 |
| cụ | 0 |
| thể | 0 |
| theo | 0 |
| từng | 0 |
| trường | 0 |
| hợp | 0 |
| kính | 0 |
| thưa | 0 |
| tất | 0 |
| cả | 0 |
| quý | 0 |
| vị | 0 |
| bởi | 0 |
| vì | 0 |
| thời | 0 |
| lượng | 0 |
| trong | 0 |

## VM600-432 — dòng train 3214 (đếm từ 0)

bằng cách nào và cách thứ nhất là chúng ta bình thường trong ở nhà quý vị có thể cho thêm dầu ăn bát cơm không cho dầu

| Token | Nhãn gốc |
|---|---|
| bằng | 0 |
| cách | 0 |
| nào | 0 |
| và | 0 |
| cách | 0 |
| thứ | B-UNITCALIBRATOR |
| nhất | I-UNITCALIBRATOR |
| là | 0 |
| chúng | 0 |
| ta | 0 |
| bình | 0 |
| thường | 0 |
| trong | 0 |
| ở | 0 |
| nhà | B-LOCATION |
| quý | 0 |
| vị | 0 |
| có | 0 |
| thể | 0 |
| cho | 0 |
| thêm | 0 |
| dầu | B-FOODDRINK |
| ăn | I-FOODDRINK |
| bát | B-FOODDRINK |
| cơm | I-FOODDRINK |
| không | 0 |
| cho | 0 |
| dầu | 0 |

## VM600-433 — dòng train 3223 (đếm từ 0)

mỗi một cái thực phẩm có những cái ưu riêng chỉ có một cái bữa ăn đa dạng mới

| Token | Nhãn gốc |
|---|---|
| mỗi | 0 |
| một | 0 |
| cái | 0 |
| thực | B-FOODDRINK |
| phẩm | I-FOODDRINK |
| có | 0 |
| những | 0 |
| cái | 0 |
| ưu | 0 |
| riêng | 0 |
| chỉ | 0 |
| có | 0 |
| một | 0 |
| cái | 0 |
| bữa | 0 |
| ăn | 0 |
| đa | 0 |
| dạng | 0 |
| mới | 0 |

## VM600-434 — dòng train 3229 (đếm từ 0)

sử dụng phương pháp kích thích não sâu thì dĩ nhiên người bệnh cũng không thể nào mà ngưng thuốc hoàn toàn được thì đó

| Token | Nhãn gốc |
|---|---|
| sử | 0 |
| dụng | 0 |
| phương | 0 |
| pháp | 0 |
| kích | B-SURGERY |
| thích | I-SURGERY |
| não | I-SURGERY |
| sâu | I-SURGERY |
| thì | 0 |
| dĩ | 0 |
| nhiên | 0 |
| người | 0 |
| bệnh | 0 |
| cũng | 0 |
| không | 0 |
| thể | 0 |
| nào | 0 |
| mà | 0 |
| ngưng | B-MEDDEVICETECHNIQUE |
| thuốc | I-MEDDEVICETECHNIQUE |
| hoàn | 0 |
| toàn | 0 |
| được | 0 |
| thì | 0 |
| đó | 0 |

## VM600-435 — dòng train 3247 (đếm từ 0)

cái chuyện đó và nếu mà chúng ta sử dụng các biện pháp phòng tránh để nó không bị nghẽn mạch máu não thì ít nhất là nó sẽ

| Token | Nhãn gốc |
|---|---|
| cái | 0 |
| chuyện | 0 |
| đó | 0 |
| và | 0 |
| nếu | 0 |
| mà | 0 |
| chúng | 0 |
| ta | 0 |
| sử | 0 |
| dụng | 0 |
| các | 0 |
| biện | 0 |
| pháp | 0 |
| phòng | B-PREVENTIVEMED |
| tránh | I-PREVENTIVEMED |
| để | 0 |
| nó | 0 |
| không | 0 |
| bị | 0 |
| nghẽn | B-DISEASESYMTOM |
| mạch | I-DISEASESYMTOM |
| máu | I-DISEASESYMTOM |
| não | B-ORGAN |
| thì | 0 |
| ít | 0 |
| nhất | 0 |
| là | 0 |
| nó | 0 |
| sẽ | 0 |

## VM600-436 — dòng train 3249 (đếm từ 0)

vữa xơ động mạch ở vành tất cả những cái đó là chúng ta không được bỏ rất rất

| Token | Nhãn gốc |
|---|---|
| vữa | B-DISEASESYMTOM |
| xơ | I-DISEASESYMTOM |
| động | I-DISEASESYMTOM |
| mạch | I-DISEASESYMTOM |
| ở | 0 |
| vành | 0 |
| tất | 0 |
| cả | 0 |
| những | 0 |
| cái | 0 |
| đó | 0 |
| là | 0 |
| chúng | 0 |
| ta | 0 |
| không | 0 |
| được | 0 |
| bỏ | 0 |
| rất | 0 |
| rất | 0 |

## VM600-437 — dòng train 3252 (đếm từ 0)

lượng đã mất mất do chính cái khối u tạo ra chứ chưa nói đến những cái mất do kém ăn hoặc là do

| Token | Nhãn gốc |
|---|---|
| lượng | 0 |
| đã | 0 |
| mất | 0 |
| mất | 0 |
| do | 0 |
| chính | 0 |
| cái | 0 |
| khối | B-DISEASESYMTOM |
| u | I-DISEASESYMTOM |
| tạo | 0 |
| ra | 0 |
| chứ | 0 |
| chưa | 0 |
| nói | 0 |
| đến | 0 |
| những | 0 |
| cái | 0 |
| mất | 0 |
| do | 0 |
| kém | B-DISEASESYMTOM |
| ăn | I-DISEASESYMTOM |
| hoặc | 0 |
| là | 0 |
| do | 0 |

## VM600-438 — dòng train 3271 (đếm từ 0)

lòng một việc mà bạn sẽ không thể quen được dù đã thực hiện bao nhiêu lần tuy

| Token | Nhãn gốc |
|---|---|
| lòng | 0 |
| một | 0 |
| việc | 0 |
| mà | 0 |
| bạn | 0 |
| sẽ | 0 |
| không | 0 |
| thể | 0 |
| quen | 0 |
| được | 0 |
| dù | 0 |
| đã | 0 |
| thực | 0 |
| hiện | 0 |
| bao | 0 |
| nhiêu | 0 |
| lần | 0 |
| tuy | 0 |

## VM600-439 — dòng train 3273 (đếm từ 0)

nói là có sự là giảm phí vận chuyển túi sắc tố đi từ bên dưới da lên bề mặt da

| Token | Nhãn gốc |
|---|---|
| nói | 0 |
| là | 0 |
| có | 0 |
| sự | 0 |
| là | 0 |
| giảm | 0 |
| phí | 0 |
| vận | 0 |
| chuyển | 0 |
| túi | B-ORGAN |
| sắc | I-ORGAN |
| tố | I-ORGAN |
| đi | 0 |
| từ | 0 |
| bên | 0 |
| dưới | 0 |
| da | B-ORGAN |
| lên | 0 |
| bề | B-ORGAN |
| mặt | I-ORGAN |
| da | I-ORGAN |

## VM600-440 — dòng train 3274 (đếm từ 0)

đề như là tương tác giữa những sản phẩm với nhau hoặc là gây ra các tình trạng

| Token | Nhãn gốc |
|---|---|
| đề | 0 |
| như | 0 |
| là | 0 |
| tương | 0 |
| tác | 0 |
| giữa | 0 |
| những | 0 |
| sản | 0 |
| phẩm | 0 |
| với | 0 |
| nhau | 0 |
| hoặc | 0 |
| là | 0 |
| gây | 0 |
| ra | 0 |
| các | 0 |
| tình | 0 |
| trạng | 0 |

## VM600-441 — dòng train 3280 (đếm từ 0)

hạ thảo chính là bộ ba là adenosine cordycepin và polysaccharide adenosine nó là

| Token | Nhãn gốc |
|---|---|
| hạ | B-DRUGCHEMICAL |
| thảo | I-DRUGCHEMICAL |
| chính | 0 |
| là | 0 |
| bộ | 0 |
| ba | 0 |
| là | 0 |
| adenosine | B-DRUGCHEMICAL |
| cordycepin | I-DRUGCHEMICAL |
| và | 0 |
| polysaccharide | B-DRUGCHEMICAL |
| adenosine | I-DRUGCHEMICAL |
| nó | 0 |
| là | 0 |

## VM600-442 — dòng train 3293 (đếm từ 0)

ta dinh dưỡng một cách hợp lý và trong dinh dưỡng đó người ta chú ý đến các vitamin cần thiết vitamin nhóm b vitamin

| Token | Nhãn gốc |
|---|---|
| ta | 0 |
| dinh | 0 |
| dưỡng | 0 |
| một | 0 |
| cách | 0 |
| hợp | 0 |
| lý | 0 |
| và | 0 |
| trong | 0 |
| dinh | 0 |
| dưỡng | 0 |
| đó | 0 |
| người | 0 |
| ta | 0 |
| chú | 0 |
| ý | 0 |
| đến | 0 |
| các | 0 |
| vitamin | B-DRUGCHEMICAL |
| cần | 0 |
| thiết | 0 |
| vitamin | B-DRUGCHEMICAL |
| nhóm | 0 |
| b | B-DRUGCHEMICAL |
| vitamin | B-DRUGCHEMICAL |

## VM600-443 — dòng train 3294 (đếm từ 0)

chúng tôi có thể làm cái chụp các mạch máu não trên ct trên mri hoặc là

| Token | Nhãn gốc |
|---|---|
| chúng | 0 |
| tôi | 0 |
| có | 0 |
| thể | 0 |
| làm | 0 |
| cái | 0 |
| chụp | B-DIAGNOSTICS |
| các | I-DIAGNOSTICS |
| mạch | I-DIAGNOSTICS |
| máu | I-DIAGNOSTICS |
| não | I-DIAGNOSTICS |
| trên | 0 |
| ct | B-DIAGNOSTICS |
| trên | 0 |
| mri | B-DIAGNOSTICS |
| hoặc | 0 |
| là | 0 |

## VM600-444 — dòng train 3325 (đếm từ 0)

chúng ta phải tuân trị chứ không có được gọi là bỏ trị khi chúng ta phải tuân trị

| Token | Nhãn gốc |
|---|---|
| chúng | 0 |
| ta | 0 |
| phải | 0 |
| tuân | B-TREATMENT |
| trị | I-TREATMENT |
| chứ | 0 |
| không | 0 |
| có | 0 |
| được | 0 |
| gọi | 0 |
| là | 0 |
| bỏ | 0 |
| trị | 0 |
| khi | 0 |
| chúng | 0 |
| ta | 0 |
| phải | 0 |
| tuân | B-TREATMENT |
| trị | I-TREATMENT |

## VM600-445 — dòng train 3329 (đếm từ 0)

rất yêu đời đúng như đức phật gọi là phải luôn luôn hoan hỷ cái đó quan trọng lắm cái thứ hai là vấn đề ăn uống là tùy

| Token | Nhãn gốc |
|---|---|
| rất | 0 |
| yêu | 0 |
| đời | 0 |
| đúng | 0 |
| như | 0 |
| đức | 0 |
| phật | 0 |
| gọi | 0 |
| là | 0 |
| phải | 0 |
| luôn | B-PERSONALCARE |
| luôn | I-PERSONALCARE |
| hoan | I-PERSONALCARE |
| hỷ | I-PERSONALCARE |
| cái | 0 |
| đó | 0 |
| quan | 0 |
| trọng | 0 |
| lắm | 0 |
| cái | B-UNITCALIBRATOR |
| thứ | I-UNITCALIBRATOR |
| hai | I-UNITCALIBRATOR |
| là | 0 |
| vấn | 0 |
| đề | 0 |
| ăn | B-PERSONALCARE |
| uống | I-PERSONALCARE |
| là | 0 |
| tùy | 0 |

## VM600-446 — dòng train 3336 (đếm từ 0)

găng hay không thì bây giờ người dân khi đến lấy mẫu cũng có thể nói mà cũng có thể hỏi bác sĩ rằng là hoặc là nhân viên

| Token | Nhãn gốc |
|---|---|
| găng | 0 |
| hay | 0 |
| không | 0 |
| thì | 0 |
| bây | B-DATETIME |
| giờ | I-DATETIME |
| người | B-OCCUPATION |
| dân | I-OCCUPATION |
| khi | 0 |
| đến | 0 |
| lấy | B-MEDDEVICETECHNIQUE |
| mẫu | I-MEDDEVICETECHNIQUE |
| cũng | 0 |
| có | 0 |
| thể | 0 |
| nói | 0 |
| mà | 0 |
| cũng | 0 |
| có | 0 |
| thể | 0 |
| hỏi | 0 |
| bác | B-OCCUPATION |
| sĩ | I-OCCUPATION |
| rằng | 0 |
| là | 0 |
| hoặc | 0 |
| là | 0 |
| nhân | 0 |
| viên | 0 |

## VM600-447 — dòng train 3344 (đếm từ 0)

thế này thứ hai nữa là chị cũng cái dấu hiệu tê bì chân tay này đây nó cũng có

| Token | Nhãn gốc |
|---|---|
| thế | 0 |
| này | 0 |
| thứ | 0 |
| hai | 0 |
| nữa | 0 |
| là | 0 |
| chị | B-GENDER |
| cũng | 0 |
| cái | 0 |
| dấu | 0 |
| hiệu | 0 |
| tê | B-DISEASESYMTOM |
| bì | I-DISEASESYMTOM |
| chân | B-ORGAN |
| tay | I-ORGAN |
| này | 0 |
| đây | 0 |
| nó | 0 |
| cũng | 0 |
| có | 0 |

## VM600-448 — dòng train 3350 (đếm từ 0)

là dễ gặp ở cái độ tuổi này và cái việc thông thường là gì ạ người ta sẽ được chẩn đoán rất là muộn vì sao có những

| Token | Nhãn gốc |
|---|---|
| là | 0 |
| dễ | 0 |
| gặp | 0 |
| ở | 0 |
| cái | 0 |
| độ | 0 |
| tuổi | 0 |
| này | 0 |
| và | 0 |
| cái | 0 |
| việc | 0 |
| thông | 0 |
| thường | 0 |
| là | 0 |
| gì | 0 |
| ạ | 0 |
| người | 0 |
| ta | 0 |
| sẽ | 0 |
| được | 0 |
| chẩn | B-DIAGNOSTICS |
| đoán | I-DIAGNOSTICS |
| rất | 0 |
| là | 0 |
| muộn | 0 |
| vì | 0 |
| sao | 0 |
| có | 0 |
| những | 0 |

## VM600-449 — dòng train 3360 (đếm từ 0)

nếu nó đã có những cái biểu hiện như vậy một lần hai lần nếu mình không phát hiện ra có nghĩa là những lần tiếp theo nó sẽ

| Token | Nhãn gốc |
|---|---|
| nếu | 0 |
| nó | 0 |
| đã | 0 |
| có | 0 |
| những | 0 |
| cái | 0 |
| biểu | 0 |
| hiện | 0 |
| như | 0 |
| vậy | 0 |
| một | 0 |
| lần | 0 |
| hai | B-UNITCALIBRATOR |
| lần | I-UNITCALIBRATOR |
| nếu | 0 |
| mình | 0 |
| không | 0 |
| phát | 0 |
| hiện | 0 |
| ra | 0 |
| có | 0 |
| nghĩa | 0 |
| là | 0 |
| những | 0 |
| lần | 0 |
| tiếp | 0 |
| theo | 0 |
| nó | 0 |
| sẽ | 0 |

## VM600-450 — dòng train 3365 (đếm từ 0)

cùng là nói những cái biến chứng của nó kính thưa quý vị tim của chúng ta đó thì được chia làm hai phần chính đó là

| Token | Nhãn gốc |
|---|---|
| cùng | 0 |
| là | 0 |
| nói | 0 |
| những | 0 |
| cái | 0 |
| biến | B-DISEASESYMTOM |
| chứng | I-DISEASESYMTOM |
| của | 0 |
| nó | 0 |
| kính | 0 |
| thưa | 0 |
| quý | 0 |
| vị | 0 |
| tim | B-ORGAN |
| của | 0 |
| chúng | 0 |
| ta | 0 |
| đó | 0 |
| thì | 0 |
| được | 0 |
| chia | 0 |
| làm | 0 |
| hai | 0 |
| phần | 0 |
| chính | 0 |
| đó | 0 |
| là | 0 |

## VM600-451 — dòng train 3374 (đếm từ 0)

ông không thể có được kinh nghiệm làm việc thực tế trong phòng thí nghiệm và phải dành thời gian suy nghĩ và đọc

| Token | Nhãn gốc |
|---|---|
| ông | B-GENDER |
| không | 0 |
| thể | 0 |
| có | 0 |
| được | 0 |
| kinh | 0 |
| nghiệm | 0 |
| làm | 0 |
| việc | 0 |
| thực | 0 |
| tế | 0 |
| trong | 0 |
| phòng | B-LOCATION |
| thí | I-LOCATION |
| nghiệm | I-LOCATION |
| và | 0 |
| phải | 0 |
| dành | 0 |
| thời | B-DATETIME |
| gian | I-DATETIME |
| suy | 0 |
| nghĩ | 0 |
| và | 0 |
| đọc | 0 |

## VM600-452 — dòng train 3377 (đếm từ 0)

người ta sẽ kê những cái đơn thuốc mà nó cải thiện cái tình trạng này tôi nói ví dụ như là hiện nay chúng ta hay dùng

| Token | Nhãn gốc |
|---|---|
| người | 0 |
| ta | 0 |
| sẽ | 0 |
| kê | 0 |
| những | 0 |
| cái | 0 |
| đơn | 0 |
| thuốc | B-DRUGCHEMICAL |
| mà | 0 |
| nó | 0 |
| cải | B-TREATMENT |
| thiện | I-TREATMENT |
| cái | 0 |
| tình | 0 |
| trạng | 0 |
| này | 0 |
| tôi | 0 |
| nói | 0 |
| ví | 0 |
| dụ | 0 |
| như | 0 |
| là | 0 |
| hiện | B-DATETIME |
| nay | I-DATETIME |
| chúng | 0 |
| ta | 0 |
| hay | 0 |
| dùng | 0 |

## VM600-453 — dòng train 3413 (đếm từ 0)

công việc có cái gì căng thẳng quá cũng là yếu tố hay là mất ngủ cái mất ngủ ở cái người lớn tuổi cũng thường xảy ra

| Token | Nhãn gốc |
|---|---|
| công | 0 |
| việc | 0 |
| có | 0 |
| cái | 0 |
| gì | 0 |
| căng | B-DISEASESYMTOM |
| thẳng | I-DISEASESYMTOM |
| quá | 0 |
| cũng | 0 |
| là | 0 |
| yếu | 0 |
| tố | 0 |
| hay | 0 |
| là | 0 |
| mất | B-DISEASESYMTOM |
| ngủ | I-DISEASESYMTOM |
| cái | 0 |
| mất | B-DISEASESYMTOM |
| ngủ | I-DISEASESYMTOM |
| ở | 0 |
| cái | 0 |
| người | B-AGE |
| lớn | I-AGE |
| tuổi | 0 |
| cũng | 0 |
| thường | 0 |
| xảy | 0 |
| ra | 0 |

## VM600-454 — dòng train 3416 (đếm từ 0)

nữa chúng ta cần phải có cái chế độ điều trị tích cực hơn trong trường hợp này lời khuyên đầu tiên của chúng tôi là gì

| Token | Nhãn gốc |
|---|---|
| nữa | 0 |
| chúng | 0 |
| ta | 0 |
| cần | 0 |
| phải | 0 |
| có | 0 |
| cái | 0 |
| chế | 0 |
| độ | 0 |
| điều | B-TREATMENT |
| trị | I-TREATMENT |
| tích | 0 |
| cực | 0 |
| hơn | 0 |
| trong | 0 |
| trường | 0 |
| hợp | 0 |
| này | 0 |
| lời | 0 |
| khuyên | 0 |
| đầu | 0 |
| tiên | 0 |
| của | 0 |
| chúng | 0 |
| tôi | 0 |
| là | 0 |
| gì | 0 |

## VM600-455 — dòng train 3426 (đếm từ 0)

thở đau tức ngực tim đập nhanh là do mảng xơ vữa động mạch gây hẹp tắc lòng

| Token | Nhãn gốc |
|---|---|
| thở | 0 |
| đau | B-DISEASESYMTOM |
| tức | I-DISEASESYMTOM |
| ngực | I-DISEASESYMTOM |
| tim | B-DISEASESYMTOM |
| đập | I-DISEASESYMTOM |
| nhanh | I-DISEASESYMTOM |
| là | 0 |
| do | 0 |
| mảng | B-DISEASESYMTOM |
| xơ | I-DISEASESYMTOM |
| vữa | I-DISEASESYMTOM |
| động | I-DISEASESYMTOM |
| mạch | I-DISEASESYMTOM |
| gây | 0 |
| hẹp | 0 |
| tắc | 0 |
| lòng | 0 |

## VM600-456 — dòng train 3433 (đếm từ 0)

động trực tiếp ở giai đoạn đó nhưng còn cái nguyên nhân có khi có rất nhiều nguyên nhân dẫn đến rụng tóc mà đôi khi

| Token | Nhãn gốc |
|---|---|
| động | 0 |
| trực | 0 |
| tiếp | 0 |
| ở | 0 |
| giai | 0 |
| đoạn | 0 |
| đó | 0 |
| nhưng | 0 |
| còn | 0 |
| cái | 0 |
| nguyên | 0 |
| nhân | 0 |
| có | 0 |
| khi | 0 |
| có | 0 |
| rất | B-UNITCALIBRATOR |
| nhiều | I-UNITCALIBRATOR |
| nguyên | 0 |
| nhân | 0 |
| dẫn | 0 |
| đến | 0 |
| rụng | B-DISEASESYMTOM |
| tóc | I-DISEASESYMTOM |
| mà | 0 |
| đôi | 0 |
| khi | 0 |

## VM600-457 — dòng train 3440 (đếm từ 0)

loại thảo dược có rất nhiều những công dụng tuyệt vời trong việc là chúng ta tăng cường sức đề kháng sức khỏe dùng

| Token | Nhãn gốc |
|---|---|
| loại | 0 |
| thảo | B-DRUGCHEMICAL |
| dược | I-DRUGCHEMICAL |
| có | 0 |
| rất | B-UNITCALIBRATOR |
| nhiều | I-UNITCALIBRATOR |
| những | 0 |
| công | 0 |
| dụng | 0 |
| tuyệt | 0 |
| vời | 0 |
| trong | 0 |
| việc | 0 |
| là | 0 |
| chúng | 0 |
| ta | 0 |
| tăng | 0 |
| cường | 0 |
| sức | B-DIAGNOSTICS |
| đề | I-DIAGNOSTICS |
| kháng | I-DIAGNOSTICS |
| sức | 0 |
| khỏe | 0 |
| dùng | 0 |

## VM600-458 — dòng train 3446 (đếm từ 0)

ta có thể là cải thiện cái vấn đề tăng sắc tố chúng ta có thể can thiệp vào một trong những cái giai đoạn của quá

| Token | Nhãn gốc |
|---|---|
| ta | 0 |
| có | 0 |
| thể | 0 |
| là | 0 |
| cải | B-TREATMENT |
| thiện | I-TREATMENT |
| cái | 0 |
| vấn | 0 |
| đề | 0 |
| tăng | B-DISEASESYMTOM |
| sắc | I-DISEASESYMTOM |
| tố | I-DISEASESYMTOM |
| chúng | 0 |
| ta | 0 |
| có | 0 |
| thể | 0 |
| can | B-PREVENTIVEMED |
| thiệp | I-PREVENTIVEMED |
| vào | 0 |
| một | B-DATETIME |
| trong | I-DATETIME |
| những | I-DATETIME |
| cái | I-DATETIME |
| giai | I-DATETIME |
| đoạn | I-DATETIME |
| của | 0 |
| quá | 0 |

## VM600-459 — dòng train 3447 (đếm từ 0)

còn nặng hơn rất là nhiều và bản thân tai biến mạch máu não lần một lần hai nó có thể nhẹ nhưng những lần sau nó sẽ

| Token | Nhãn gốc |
|---|---|
| còn | 0 |
| nặng | 0 |
| hơn | 0 |
| rất | 0 |
| là | 0 |
| nhiều | 0 |
| và | 0 |
| bản | 0 |
| thân | 0 |
| tai | B-DISEASESYMTOM |
| biến | I-DISEASESYMTOM |
| mạch | I-DISEASESYMTOM |
| máu | I-DISEASESYMTOM |
| não | I-DISEASESYMTOM |
| lần | 0 |
| một | 0 |
| lần | 0 |
| hai | 0 |
| nó | 0 |
| có | 0 |
| thể | 0 |
| nhẹ | 0 |
| nhưng | 0 |
| những | 0 |
| lần | 0 |
| sau | 0 |
| nó | 0 |
| sẽ | 0 |

## VM600-460 — dòng train 3449 (đếm từ 0)

chỉ nói đến chuyện rung nhĩ không thôi nhưng mà nếu mà cả chuyện rung nhĩ đó mà đã có những cái biến chứng ví dụ như nó

| Token | Nhãn gốc |
|---|---|
| chỉ | 0 |
| nói | 0 |
| đến | 0 |
| chuyện | 0 |
| rung | B-DISEASESYMTOM |
| nhĩ | I-DISEASESYMTOM |
| không | 0 |
| thôi | 0 |
| nhưng | 0 |
| mà | 0 |
| nếu | 0 |
| mà | 0 |
| cả | 0 |
| chuyện | 0 |
| rung | B-DISEASESYMTOM |
| nhĩ | I-DISEASESYMTOM |
| đó | 0 |
| mà | 0 |
| đã | 0 |
| có | 0 |
| những | 0 |
| cái | 0 |
| biến | B-DISEASESYMTOM |
| chứng | I-DISEASESYMTOM |
| ví | 0 |
| dụ | 0 |
| như | 0 |
| nó | 0 |

## VM600-461 — dòng train 3465 (đếm từ 0)

xơ vữa động mạch cũng như là khắc phục được tình trạng ở hệ hô hấp cũng như là hệ tim thì quý vị và các bạn hãy gọi về

| Token | Nhãn gốc |
|---|---|
| xơ | B-DISEASESYMTOM |
| vữa | I-DISEASESYMTOM |
| động | I-DISEASESYMTOM |
| mạch | I-DISEASESYMTOM |
| cũng | 0 |
| như | 0 |
| là | 0 |
| khắc | 0 |
| phục | 0 |
| được | 0 |
| tình | 0 |
| trạng | 0 |
| ở | 0 |
| hệ | 0 |
| hô | 0 |
| hấp | 0 |
| cũng | 0 |
| như | 0 |
| là | 0 |
| hệ | 0 |
| tim | B-ORGAN |
| thì | 0 |
| quý | 0 |
| vị | 0 |
| và | 0 |
| các | 0 |
| bạn | 0 |
| hãy | 0 |
| gọi | 0 |
| về | 0 |

## VM600-462 — dòng train 3467 (đếm từ 0)

mạch hay không còn nếu trong giai đoạn cấp này mà có rung nhĩ nữa mà người lớn tuổi nữa thì chắc chắn là chúng ta phải

| Token | Nhãn gốc |
|---|---|
| mạch | B-ORGAN |
| hay | 0 |
| không | 0 |
| còn | 0 |
| nếu | 0 |
| trong | 0 |
| giai | 0 |
| đoạn | 0 |
| cấp | 0 |
| này | 0 |
| mà | 0 |
| có | 0 |
| rung | B-DISEASESYMTOM |
| nhĩ | I-DISEASESYMTOM |
| nữa | 0 |
| mà | 0 |
| người | B-AGE |
| lớn | I-AGE |
| tuổi | I-AGE |
| nữa | 0 |
| thì | 0 |
| chắc | 0 |
| chắn | 0 |
| là | 0 |
| chúng | 0 |
| ta | 0 |
| phải | 0 |

## VM600-463 — dòng train 3474 (đếm từ 0)

cái trường hợp là năm năm bảy năm đây là những cái nghiên cứu ở nước ngoài là những cái nước phát triển là người ta cũng nhận thấy rằng là phần lớn là mọi người được

| Token | Nhãn gốc |
|---|---|
| cái | 0 |
| trường | 0 |
| hợp | 0 |
| là | 0 |
| năm | B-DATETIME |
| năm | I-DATETIME |
| bảy | 0 |
| năm | 0 |
| đây | 0 |
| là | 0 |
| những | 0 |
| cái | 0 |
| nghiên | B-DIAGNOSTICS |
| cứu | I-DIAGNOSTICS |
| ở | 0 |
| nước | B-LOCATION |
| ngoài | I-LOCATION |
| là | 0 |
| những | 0 |
| cái | 0 |
| nước | 0 |
| phát | 0 |
| triển | 0 |
| là | 0 |
| người | 0 |
| ta | 0 |
| cũng | 0 |
| nhận | 0 |
| thấy | 0 |
| rằng | 0 |
| là | 0 |
| phần | B-UNITCALIBRATOR |
| lớn | I-UNITCALIBRATOR |
| là | 0 |
| mọi | 0 |
| người | 0 |
| được | 0 |

## VM600-464 — dòng train 3478 (đếm từ 0)

không có nắm được như thế này là bao nhiêu lâu nay rồi ạ nó có tê bì nhiều ở cái bàn tay không ạ

| Token | Nhãn gốc |
|---|---|
| không | 0 |
| có | 0 |
| nắm | 0 |
| được | 0 |
| như | 0 |
| thế | 0 |
| này | 0 |
| là | 0 |
| bao | 0 |
| nhiêu | 0 |
| lâu | 0 |
| nay | 0 |
| rồi | 0 |
| ạ | 0 |
| nó | 0 |
| có | 0 |
| tê | B-DISEASESYMTOM |
| bì | I-DISEASESYMTOM |
| nhiều | 0 |
| ở | 0 |
| cái | 0 |
| bàn | B-ORGAN |
| tay | I-ORGAN |
| không | 0 |
| ạ | 0 |

## VM600-465 — dòng train 3515 (đếm từ 0)

hơn về dinh dưỡng trước trong và sau ung thư để làm sao giúp cho chúng ta những người đã mắc ung thư mà lại được chẩn

| Token | Nhãn gốc |
|---|---|
| hơn | 0 |
| về | 0 |
| dinh | 0 |
| dưỡng | 0 |
| trước | 0 |
| trong | 0 |
| và | 0 |
| sau | 0 |
| ung | B-DISEASESYMTOM |
| thư | I-DISEASESYMTOM |
| để | 0 |
| làm | 0 |
| sao | 0 |
| giúp | 0 |
| cho | 0 |
| chúng | 0 |
| ta | 0 |
| những | 0 |
| người | 0 |
| đã | 0 |
| mắc | 0 |
| ung | B-DISEASESYMTOM |
| thư | I-DISEASESYMTOM |
| mà | 0 |
| lại | 0 |
| được | 0 |
| chẩn | 0 |

## VM600-466 — dòng train 3522 (đếm từ 0)

sử dụng mấy nhôm các chất bổ trợ có thể được thiết kế riêng để kích hoạt phản ứng bẩm sinh bằng cách sử dụng các phân

| Token | Nhãn gốc |
|---|---|
| sử | 0 |
| dụng | 0 |
| mấy | 0 |
| nhôm | 0 |
| các | 0 |
| chất | B-DRUGCHEMICAL |
| bổ | I-DRUGCHEMICAL |
| trợ | I-DRUGCHEMICAL |
| có | 0 |
| thể | 0 |
| được | 0 |
| thiết | 0 |
| kế | 0 |
| riêng | 0 |
| để | 0 |
| kích | 0 |
| hoạt | 0 |
| phản | 0 |
| ứng | 0 |
| bẩm | B-DISEASESYMTOM |
| sinh | I-DISEASESYMTOM |
| bằng | 0 |
| cách | 0 |
| sử | 0 |
| dụng | 0 |
| các | 0 |
| phân | 0 |

## VM600-467 — dòng train 3528 (đếm từ 0)

nhìn đơn giản về những gì đang xảy ra ở đây là cơ thể chúng ta tấn công mầm bệnh đối tượng xâm nhập vết thương vì hệ miễn

| Token | Nhãn gốc |
|---|---|
| nhìn | 0 |
| đơn | 0 |
| giản | 0 |
| về | 0 |
| những | 0 |
| gì | 0 |
| đang | 0 |
| xảy | 0 |
| ra | 0 |
| ở | 0 |
| đây | 0 |
| là | 0 |
| cơ | B-ORGAN |
| thể | I-ORGAN |
| chúng | 0 |
| ta | 0 |
| tấn | 0 |
| công | 0 |
| mầm | B-DISEASESYMTOM |
| bệnh | I-DISEASESYMTOM |
| đối | 0 |
| tượng | 0 |
| xâm | 0 |
| nhập | 0 |
| vết | B-DISEASESYMTOM |
| thương | I-DISEASESYMTOM |
| vì | 0 |
| hệ | 0 |
| miễn | 0 |

## VM600-468 — dòng train 3552 (đếm từ 0)

não bộ hơn hết bạn có thể gặt hái được thành quả của chế độ ăn bổ não trong vòng vài tuần

| Token | Nhãn gốc |
|---|---|
| não | B-ORGAN |
| bộ | I-ORGAN |
| hơn | 0 |
| hết | 0 |
| bạn | 0 |
| có | 0 |
| thể | 0 |
| gặt | 0 |
| hái | 0 |
| được | 0 |
| thành | 0 |
| quả | 0 |
| của | 0 |
| chế | B-PERSONALCARE |
| độ | I-PERSONALCARE |
| ăn | I-PERSONALCARE |
| bổ | 0 |
| não | B-ORGAN |
| trong | B-DATETIME |
| vòng | I-DATETIME |
| vài | 0 |
| tuần | B-DATETIME |

## VM600-469 — dòng train 3572 (đếm từ 0)

biết là nhất là trong cái buổi những cái cái lúc mà dịch dã như thế này kinh tế chúng ta ai cũng rất hạn hẹp thế thì làm

| Token | Nhãn gốc |
|---|---|
| biết | 0 |
| là | 0 |
| nhất | 0 |
| là | 0 |
| trong | 0 |
| cái | 0 |
| buổi | 0 |
| những | 0 |
| cái | 0 |
| cái | 0 |
| lúc | 0 |
| mà | 0 |
| dịch | 0 |
| dã | 0 |
| như | 0 |
| thế | 0 |
| này | 0 |
| kinh | 0 |
| tế | 0 |
| chúng | 0 |
| ta | 0 |
| ai | 0 |
| cũng | 0 |
| rất | 0 |
| hạn | 0 |
| hẹp | 0 |
| thế | 0 |
| thì | 0 |
| làm | 0 |

## VM600-470 — dòng train 3576 (đếm từ 0)

khác máu lạnh khác thì vẫn có thể khác

| Token | Nhãn gốc |
|---|---|
| khác | 0 |
| máu | B-ORGAN |
| lạnh | 0 |
| khác | 0 |
| thì | 0 |
| vẫn | 0 |
| có | 0 |
| thể | 0 |
| khác | 0 |

## VM600-471 — dòng train 3578 (đếm từ 0)

là bác bị đau lưng cũng đã lâu rồi và đau cả hai đầu gối nữa đúng không ạ vâng dạ vâng vậy thì với những cái triệu

| Token | Nhãn gốc |
|---|---|
| là | 0 |
| bác | B-AGE |
| bị | 0 |
| đau | B-DISEASESYMTOM |
| lưng | I-DISEASESYMTOM |
| cũng | 0 |
| đã | 0 |
| lâu | 0 |
| rồi | 0 |
| và | 0 |
| đau | B-DISEASESYMTOM |
| cả | 0 |
| hai | 0 |
| đầu | B-ORGAN |
| gối | I-ORGAN |
| nữa | 0 |
| đúng | 0 |
| không | 0 |
| ạ | 0 |
| vâng | 0 |
| dạ | 0 |
| vâng | 0 |
| vậy | 0 |
| thì | 0 |
| với | 0 |
| những | 0 |
| cái | 0 |
| triệu | 0 |

## VM600-472 — dòng train 3579 (đếm từ 0)

phần trăm và khi cái người được tiêm vắcxin đó được miễn nhiễm thì cái người tiêm đó sẽ không có phải nhiễm virus hoặc

| Token | Nhãn gốc |
|---|---|
| phần | B-UNITCALIBRATOR |
| trăm | I-UNITCALIBRATOR |
| và | 0 |
| khi | 0 |
| cái | 0 |
| người | 0 |
| được | 0 |
| tiêm | B-MEDDEVICETECHNIQUE |
| vắcxin | B-DRUGCHEMICAL |
| đó | 0 |
| được | 0 |
| miễn | 0 |
| nhiễm | 0 |
| thì | 0 |
| cái | 0 |
| người | 0 |
| tiêm | B-MEDDEVICETECHNIQUE |
| đó | 0 |
| sẽ | 0 |
| không | 0 |
| có | 0 |
| phải | 0 |
| nhiễm | 0 |
| virus | B-DISEASESYMTOM |
| hoặc | 0 |

## VM600-473 — dòng train 3580 (đếm từ 0)

thu được các quần thể vi khuẩn tương tự như các quần thể vi khuẩn tìm thấy trên bề mặt da chiếm đa số là rất nhiều vi

| Token | Nhãn gốc |
|---|---|
| thu | 0 |
| được | 0 |
| các | 0 |
| quần | 0 |
| thể | 0 |
| vi | B-DISEASESYMTOM |
| khuẩn | I-DISEASESYMTOM |
| tương | 0 |
| tự | 0 |
| như | 0 |
| các | 0 |
| quần | 0 |
| thể | 0 |
| vi | B-DISEASESYMTOM |
| khuẩn | I-DISEASESYMTOM |
| tìm | 0 |
| thấy | 0 |
| trên | 0 |
| bề | B-ORGAN |
| mặt | I-ORGAN |
| da | I-ORGAN |
| chiếm | B-UNITCALIBRATOR |
| đa | I-UNITCALIBRATOR |
| số | I-UNITCALIBRATOR |
| là | 0 |
| rất | B-UNITCALIBRATOR |
| nhiều | I-UNITCALIBRATOR |
| vi | 0 |

## VM600-474 — dòng train 3607 (đếm từ 0)

tiện rối loạn trí nhớ sa sút gọi là sa sút trí tuệ alzheimer vân vân nó sẽ được

| Token | Nhãn gốc |
|---|---|
| tiện | 0 |
| rối | B-DISEASESYMTOM |
| loạn | I-DISEASESYMTOM |
| trí | I-DISEASESYMTOM |
| nhớ | I-DISEASESYMTOM |
| sa | 0 |
| sút | 0 |
| gọi | 0 |
| là | 0 |
| sa | B-DISEASESYMTOM |
| sút | I-DISEASESYMTOM |
| trí | I-DISEASESYMTOM |
| tuệ | I-DISEASESYMTOM |
| alzheimer | B-DISEASESYMTOM |
| vân | 0 |
| vân | 0 |
| nó | 0 |
| sẽ | 0 |
| được | 0 |

## VM600-475 — dòng train 3608 (đếm từ 0)

chỉ là nghỉ được rõ ràng cái đấy cũng là một cái khó đúng không ạ thế chính vì vậy cho nên trong trường hợp này rõ ràng là cái đai thắt lưng lại là một cái

| Token | Nhãn gốc |
|---|---|
| chỉ | 0 |
| là | 0 |
| nghỉ | 0 |
| được | 0 |
| rõ | 0 |
| ràng | 0 |
| cái | 0 |
| đấy | 0 |
| cũng | 0 |
| là | 0 |
| một | 0 |
| cái | 0 |
| khó | 0 |
| đúng | 0 |
| không | 0 |
| ạ | 0 |
| thế | 0 |
| chính | 0 |
| vì | 0 |
| vậy | 0 |
| cho | 0 |
| nên | 0 |
| trong | 0 |
| trường | 0 |
| hợp | 0 |
| này | 0 |
| rõ | 0 |
| ràng | 0 |
| là | 0 |
| cái | 0 |
| đai | 0 |
| thắt | B-ORGAN |
| lưng | I-ORGAN |
| lại | 0 |
| là | 0 |
| một | 0 |
| cái | 0 |

## VM600-476 — dòng train 3626 (đếm từ 0)

thuật thường là chỉ là liên quan tới vấn đề về phẫu thuật nhưng mà với những cái

| Token | Nhãn gốc |
|---|---|
| thuật | 0 |
| thường | 0 |
| là | 0 |
| chỉ | 0 |
| là | 0 |
| liên | 0 |
| quan | 0 |
| tới | 0 |
| vấn | 0 |
| đề | 0 |
| về | 0 |
| phẫu | B-SURGERY |
| thuật | I-SURGERY |
| nhưng | 0 |
| mà | 0 |
| với | 0 |
| những | 0 |
| cái | 0 |

## VM600-477 — dòng train 3640 (đếm từ 0)

là đơn đơn độc như vậy thì nó sẽ làm cho cái tình trạng mà béo phì đó nó có

| Token | Nhãn gốc |
|---|---|
| là | 0 |
| đơn | 0 |
| đơn | 0 |
| độc | 0 |
| như | 0 |
| vậy | 0 |
| thì | 0 |
| nó | 0 |
| sẽ | 0 |
| làm | 0 |
| cho | 0 |
| cái | 0 |
| tình | 0 |
| trạng | 0 |
| mà | 0 |
| béo | B-DISEASESYMTOM |
| phì | I-DISEASESYMTOM |
| đó | 0 |
| nó | 0 |
| có | 0 |

## VM600-478 — dòng train 3650 (đếm từ 0)

nhiều trường hợp bị chó tấn công gây

| Token | Nhãn gốc |
|---|---|
| nhiều | 0 |
| trường | 0 |
| hợp | 0 |
| bị | 0 |
| chó | 0 |
| tấn | 0 |
| công | 0 |
| gây | 0 |

## VM600-479 — dòng train 3662 (đếm từ 0)

thấy mệt mỏi có lúc họ cảm thấy khó khăn có lúc lúc họ cảm thấy là khó cưỡng nổi các cái cái thức ăn mà nó nó chào

| Token | Nhãn gốc |
|---|---|
| thấy | 0 |
| mệt | B-DISEASESYMTOM |
| mỏi | I-DISEASESYMTOM |
| có | 0 |
| lúc | 0 |
| họ | 0 |
| cảm | 0 |
| thấy | 0 |
| khó | 0 |
| khăn | 0 |
| có | 0 |
| lúc | 0 |
| lúc | 0 |
| họ | 0 |
| cảm | 0 |
| thấy | 0 |
| là | 0 |
| khó | 0 |
| cưỡng | 0 |
| nổi | 0 |
| các | 0 |
| cái | 0 |
| cái | 0 |
| thức | B-FOODDRINK |
| ăn | I-FOODDRINK |
| mà | 0 |
| nó | 0 |
| nó | 0 |
| chào | 0 |

## VM600-480 — dòng train 3667 (đếm từ 0)

tôi mổ rồi mà sao nó có dấu hiệu nó muốn trở nặng hơn vân vân mà chúng ta phải yên tâm rằng là sau ba đến sáu tháng sau khi đã

| Token | Nhãn gốc |
|---|---|
| tôi | 0 |
| mổ | B-SURGERY |
| rồi | 0 |
| mà | 0 |
| sao | 0 |
| nó | 0 |
| có | 0 |
| dấu | 0 |
| hiệu | 0 |
| nó | 0 |
| muốn | 0 |
| trở | 0 |
| nặng | 0 |
| hơn | 0 |
| vân | 0 |
| vân | 0 |
| mà | 0 |
| chúng | 0 |
| ta | 0 |
| phải | 0 |
| yên | 0 |
| tâm | 0 |
| rằng | 0 |
| là | 0 |
| sau | B-DATETIME |
| ba | I-DATETIME |
| đến | I-DATETIME |
| sáu | I-DATETIME |
| tháng | I-DATETIME |
| sau | 0 |
| khi | 0 |
| đã | 0 |

## VM600-481 — dòng train 3677 (đếm từ 0)

chúng ta sau sau vụ mất trộm chẳng hạn thì chúng ta đuổi trộm đi hết rồi thì

| Token | Nhãn gốc |
|---|---|
| chúng | 0 |
| ta | 0 |
| sau | 0 |
| sau | 0 |
| vụ | 0 |
| mất | 0 |
| trộm | 0 |
| chẳng | 0 |
| hạn | 0 |
| thì | 0 |
| chúng | 0 |
| ta | 0 |
| đuổi | 0 |
| trộm | 0 |
| đi | 0 |
| hết | 0 |
| rồi | 0 |
| thì | 0 |

## VM600-482 — dòng train 3701 (đếm từ 0)

bệnh thì chính cũng là những cái lúc mà chúng tôi đang vận động kính là những cái những cái lúc mà chúng tôi đang thực

| Token | Nhãn gốc |
|---|---|
| bệnh | 0 |
| thì | 0 |
| chính | 0 |
| cũng | 0 |
| là | 0 |
| những | 0 |
| cái | 0 |
| lúc | 0 |
| mà | 0 |
| chúng | 0 |
| tôi | 0 |
| đang | 0 |
| vận | 0 |
| động | 0 |
| kính | 0 |
| là | 0 |
| những | 0 |
| cái | 0 |
| những | 0 |
| cái | 0 |
| lúc | 0 |
| mà | 0 |
| chúng | 0 |
| tôi | 0 |
| đang | 0 |
| thực | 0 |

## VM600-483 — dòng train 3703 (đếm từ 0)

những cái cái biến chứng về các cái mạch máu chi nữa và khi sử dụng đối với sản phẩm này thì chúng ta nên sử dụng để

| Token | Nhãn gốc |
|---|---|
| những | 0 |
| cái | 0 |
| cái | 0 |
| biến | B-DISEASESYMTOM |
| chứng | I-DISEASESYMTOM |
| về | 0 |
| các | 0 |
| cái | 0 |
| mạch | B-ORGAN |
| máu | I-ORGAN |
| chi | I-ORGAN |
| nữa | 0 |
| và | 0 |
| khi | 0 |
| sử | 0 |
| dụng | 0 |
| đối | 0 |
| với | 0 |
| sản | 0 |
| phẩm | 0 |
| này | 0 |
| thì | 0 |
| chúng | 0 |
| ta | 0 |
| nên | 0 |
| sử | 0 |
| dụng | 0 |
| để | 0 |

## VM600-484 — dòng train 3714 (đếm từ 0)

là yếu tay yếu chân méo miệng thăng bằng có thể về mắt nữa thì thế mà có những triệu

| Token | Nhãn gốc |
|---|---|
| là | 0 |
| yếu | B-DISEASESYMTOM |
| tay | I-DISEASESYMTOM |
| yếu | B-DISEASESYMTOM |
| chân | I-DISEASESYMTOM |
| méo | B-DISEASESYMTOM |
| miệng | I-DISEASESYMTOM |
| thăng | 0 |
| bằng | 0 |
| có | 0 |
| thể | 0 |
| về | 0 |
| mắt | B-ORGAN |
| nữa | 0 |
| thì | 0 |
| thế | 0 |
| mà | 0 |
| có | 0 |
| những | 0 |
| triệu | 0 |

## VM600-485 — dòng train 3718 (đếm từ 0)

có những người là còn nhịn ăn một để gọi là thanh lọc cơ thể thì thì chúng ta sẽ

| Token | Nhãn gốc |
|---|---|
| có | 0 |
| những | 0 |
| người | 0 |
| là | 0 |
| còn | 0 |
| nhịn | 0 |
| ăn | 0 |
| một | 0 |
| để | 0 |
| gọi | 0 |
| là | 0 |
| thanh | B-DIAGNOSTICS |
| lọc | I-DIAGNOSTICS |
| cơ | B-ORGAN |
| thể | I-ORGAN |
| thì | 0 |
| thì | 0 |
| chúng | 0 |
| ta | 0 |
| sẽ | 0 |

## VM600-486 — dòng train 3734 (đếm từ 0)

sao bởi vì khi mà bác bị huyết áp cao bác bị đái tháo đường mà thậm chí có

| Token | Nhãn gốc |
|---|---|
| sao | 0 |
| bởi | 0 |
| vì | 0 |
| khi | 0 |
| mà | 0 |
| bác | B-AGE |
| bị | 0 |
| huyết | B-DISEASESYMTOM |
| áp | I-DISEASESYMTOM |
| cao | B-UNITCALIBRATOR |
| bác | B-AGE |
| bị | 0 |
| đái | B-DISEASESYMTOM |
| tháo | I-DISEASESYMTOM |
| đường | I-DISEASESYMTOM |
| mà | 0 |
| thậm | 0 |
| chí | 0 |
| có | 0 |

## VM600-487 — dòng train 3736 (đếm từ 0)

lời đây là thế thì làm thế nào để chúng ta biết đâu là vấn đề và cái cách xử lý của chúng ta là như thế nào khi nào thì

| Token | Nhãn gốc |
|---|---|
| lời | 0 |
| đây | 0 |
| là | 0 |
| thế | 0 |
| thì | 0 |
| làm | 0 |
| thế | 0 |
| nào | 0 |
| để | 0 |
| chúng | 0 |
| ta | 0 |
| biết | 0 |
| đâu | 0 |
| là | 0 |
| vấn | 0 |
| đề | 0 |
| và | 0 |
| cái | 0 |
| cách | 0 |
| xử | 0 |
| lý | 0 |
| của | 0 |
| chúng | 0 |
| ta | 0 |
| là | 0 |
| như | 0 |
| thế | 0 |
| nào | 0 |
| khi | 0 |
| nào | 0 |
| thì | 0 |

## VM600-488 — dòng train 3744 (đếm từ 0)

phải tập dần để chúng ta thích nghi và để chúng ta có thể chấp nhận được những cái món ăn như trước khi chúng ta bị ung

| Token | Nhãn gốc |
|---|---|
| phải | 0 |
| tập | 0 |
| dần | 0 |
| để | 0 |
| chúng | 0 |
| ta | 0 |
| thích | B-DIAGNOSTICS |
| nghi | I-DIAGNOSTICS |
| và | 0 |
| để | 0 |
| chúng | 0 |
| ta | 0 |
| có | 0 |
| thể | 0 |
| chấp | 0 |
| nhận | 0 |
| được | 0 |
| những | 0 |
| cái | 0 |
| món | 0 |
| ăn | 0 |
| như | 0 |
| trước | 0 |
| khi | 0 |
| chúng | 0 |
| ta | 0 |
| bị | 0 |
| ung | 0 |

## VM600-489 — dòng train 3758 (đếm từ 0)

nói chung cũng như hoạt động và bảo vệ não bộ nói riêng mặc dù probiotic lợi khuẩn hiện đã trở

| Token | Nhãn gốc |
|---|---|
| nói | 0 |
| chung | 0 |
| cũng | 0 |
| như | 0 |
| hoạt | 0 |
| động | 0 |
| và | 0 |
| bảo | 0 |
| vệ | 0 |
| não | B-ORGAN |
| bộ | I-ORGAN |
| nói | 0 |
| riêng | 0 |
| mặc | 0 |
| dù | 0 |
| probiotic | B-FOODDRINK |
| lợi | B-DRUGCHEMICAL |
| khuẩn | I-DRUGCHEMICAL |
| hiện | 0 |
| đã | 0 |
| trở | 0 |

## VM600-490 — dòng train 3761 (đếm từ 0)

cực mà thôi thứ nhất là họ sẽ càng thấy là tự ti hơn khi bị kỳ thị là nó

| Token | Nhãn gốc |
|---|---|
| cực | 0 |
| mà | 0 |
| thôi | 0 |
| thứ | B-UNITCALIBRATOR |
| nhất | I-UNITCALIBRATOR |
| là | 0 |
| họ | 0 |
| sẽ | 0 |
| càng | 0 |
| thấy | 0 |
| là | 0 |
| tự | B-DISEASESYMTOM |
| ti | I-DISEASESYMTOM |
| hơn | 0 |
| khi | 0 |
| bị | 0 |
| kỳ | 0 |
| thị | 0 |
| là | 0 |
| nó | 0 |

## VM600-491 — dòng train 3819 (đếm từ 0)

mà chúng ta bị thay đổi trong cái quá trình trước và trong điều trị ung thư thì bây giờ chúng ta sẽ phục hồi nó lại

| Token | Nhãn gốc |
|---|---|
| mà | 0 |
| chúng | 0 |
| ta | 0 |
| bị | 0 |
| thay | 0 |
| đổi | 0 |
| trong | 0 |
| cái | 0 |
| quá | 0 |
| trình | 0 |
| trước | 0 |
| và | 0 |
| trong | 0 |
| điều | B-TREATMENT |
| trị | I-TREATMENT |
| ung | B-DISEASESYMTOM |
| thư | I-DISEASESYMTOM |
| thì | 0 |
| bây | B-DATETIME |
| giờ | I-DATETIME |
| chúng | 0 |
| ta | 0 |
| sẽ | 0 |
| phục | B-MEDDEVICETECHNIQUE |
| hồi | I-MEDDEVICETECHNIQUE |
| nó | 0 |
| lại | 0 |

## VM600-492 — dòng train 3820 (đếm từ 0)

ta điều chỉnh thuốc cho nó phù hợp và khi có chỉ định thuốc thì phải tuân thủ

| Token | Nhãn gốc |
|---|---|
| ta | 0 |
| điều | B-PREVENTIVEMED |
| chỉnh | I-PREVENTIVEMED |
| thuốc | B-DRUGCHEMICAL |
| cho | 0 |
| nó | 0 |
| phù | 0 |
| hợp | 0 |
| và | 0 |
| khi | 0 |
| có | 0 |
| chỉ | B-PREVENTIVEMED |
| định | I-PREVENTIVEMED |
| thuốc | B-DRUGCHEMICAL |
| thì | 0 |
| phải | 0 |
| tuân | B-PREVENTIVEMED |
| thủ | I-PREVENTIVEMED |

## VM600-493 — dòng train 3826 (đếm từ 0)

tân dược mà đang điều trị đây là một cái điều rất là an toàn quý vị và các bạn những ai mà chúng ta đang gặp phải cái

| Token | Nhãn gốc |
|---|---|
| tân | B-DRUGCHEMICAL |
| dược | I-DRUGCHEMICAL |
| mà | 0 |
| đang | 0 |
| điều | B-TREATMENT |
| trị | I-TREATMENT |
| đây | 0 |
| là | 0 |
| một | 0 |
| cái | 0 |
| điều | 0 |
| rất | 0 |
| là | 0 |
| an | 0 |
| toàn | 0 |
| quý | 0 |
| vị | 0 |
| và | 0 |
| các | 0 |
| bạn | 0 |
| những | 0 |
| ai | 0 |
| mà | 0 |
| chúng | 0 |
| ta | 0 |
| đang | 0 |
| gặp | 0 |
| phải | 0 |
| cái | 0 |

## VM600-494 — dòng train 3839 (đếm từ 0)

tuổi gần lúc gần lớn tuổi như vậy đó thì chúng ta thấy là lúc còn trẻ phải không

| Token | Nhãn gốc |
|---|---|
| tuổi | 0 |
| gần | 0 |
| lúc | 0 |
| gần | 0 |
| lớn | B-AGE |
| tuổi | I-AGE |
| như | 0 |
| vậy | 0 |
| đó | 0 |
| thì | 0 |
| chúng | 0 |
| ta | 0 |
| thấy | 0 |
| là | 0 |
| lúc | 0 |
| còn | B-AGE |
| trẻ | I-AGE |
| phải | 0 |
| không | 0 |

## VM600-495 — dòng train 3851 (đếm từ 0)

chóng mặt luôn và thậm chí đã bị trẻ hóa cho nên rằng là mà hai nữa là đi cùng

| Token | Nhãn gốc |
|---|---|
| chóng | B-DISEASESYMTOM |
| mặt | I-DISEASESYMTOM |
| luôn | 0 |
| và | 0 |
| thậm | 0 |
| chí | 0 |
| đã | 0 |
| bị | B-DISEASESYMTOM |
| trẻ | I-DISEASESYMTOM |
| hóa | I-DISEASESYMTOM |
| cho | 0 |
| nên | 0 |
| rằng | 0 |
| là | 0 |
| mà | 0 |
| hai | 0 |
| nữa | 0 |
| là | 0 |
| đi | 0 |
| cùng | 0 |

## VM600-496 — dòng train 3852 (đếm từ 0)

các bác sĩ phụ trách trên nhiều lĩnh vực sức khỏe khác nhau để cùng giúp cho người dân giải quyết những vấn đề mà

| Token | Nhãn gốc |
|---|---|
| các | 0 |
| bác | B-OCCUPATION |
| sĩ | I-OCCUPATION |
| phụ | 0 |
| trách | 0 |
| trên | 0 |
| nhiều | 0 |
| lĩnh | 0 |
| vực | 0 |
| sức | 0 |
| khỏe | 0 |
| khác | 0 |
| nhau | 0 |
| để | 0 |
| cùng | 0 |
| giúp | 0 |
| cho | 0 |
| người | B-OCCUPATION |
| dân | I-OCCUPATION |
| giải | 0 |
| quyết | 0 |
| những | 0 |
| vấn | 0 |
| đề | 0 |
| mà | 0 |

## VM600-497 — dòng train 3867 (đếm từ 0)

có thể nói là chương trình đã hiểu và rất là thông cảm với những cái tình cảnh

| Token | Nhãn gốc |
|---|---|
| có | 0 |
| thể | 0 |
| nói | 0 |
| là | 0 |
| chương | 0 |
| trình | 0 |
| đã | 0 |
| hiểu | 0 |
| và | 0 |
| rất | 0 |
| là | 0 |
| thông | 0 |
| cảm | 0 |
| với | 0 |
| những | 0 |
| cái | 0 |
| tình | 0 |
| cảnh | 0 |

## VM600-498 — dòng train 3870 (đếm từ 0)

lo lắng khi mà người dân đến lấy mẫu mà không biết là liệu nhân viên y tế có thời gian hay không hoặc là có sát khuẩn

| Token | Nhãn gốc |
|---|---|
| lo | 0 |
| lắng | 0 |
| khi | 0 |
| mà | 0 |
| người | B-OCCUPATION |
| dân | I-OCCUPATION |
| đến | 0 |
| lấy | B-MEDDEVICETECHNIQUE |
| mẫu | I-MEDDEVICETECHNIQUE |
| mà | 0 |
| không | 0 |
| biết | 0 |
| là | 0 |
| liệu | 0 |
| nhân | B-OCCUPATION |
| viên | I-OCCUPATION |
| y | I-OCCUPATION |
| tế | I-OCCUPATION |
| có | 0 |
| thời | B-DATETIME |
| gian | I-DATETIME |
| hay | 0 |
| không | 0 |
| hoặc | 0 |
| là | 0 |
| có | 0 |
| sát | B-TREATMENT |
| khuẩn | I-TREATMENT |

## VM600-499 — dòng train 3887 (đếm từ 0)

của họ nó càng bị bất ổn hơn và nếu ngược lại nếu mà mình được lắng nghe

| Token | Nhãn gốc |
|---|---|
| của | 0 |
| họ | 0 |
| nó | 0 |
| càng | 0 |
| bị | 0 |
| bất | 0 |
| ổn | 0 |
| hơn | 0 |
| và | 0 |
| nếu | 0 |
| ngược | 0 |
| lại | 0 |
| nếu | 0 |
| mà | 0 |
| mình | 0 |
| được | 0 |
| lắng | 0 |
| nghe | 0 |

## VM600-500 — dòng train 3888 (đếm từ 0)

chung đó là tập thể dục vừa sức và nó chạy đều ra thì nó nó sẽ tốt hơn cho sức khỏe của mình hơn là những cái tập

| Token | Nhãn gốc |
|---|---|
| chung | 0 |
| đó | 0 |
| là | 0 |
| tập | B-PERSONALCARE |
| thể | I-PERSONALCARE |
| dục | I-PERSONALCARE |
| vừa | 0 |
| sức | 0 |
| và | 0 |
| nó | 0 |
| chạy | 0 |
| đều | 0 |
| ra | 0 |
| thì | 0 |
| nó | 0 |
| nó | 0 |
| sẽ | 0 |
| tốt | 0 |
| hơn | 0 |
| cho | 0 |
| sức | 0 |
| khỏe | 0 |
| của | 0 |
| mình | 0 |
| hơn | 0 |
| là | 0 |
| những | 0 |
| cái | 0 |
| tập | 0 |

## VM600-501 — dòng train 3889 (đếm từ 0)

làm giãn các cái mạch máu để tăng cường lưu thông máu đến nuôi dưỡng cơ tim qua

| Token | Nhãn gốc |
|---|---|
| làm | 0 |
| giãn | 0 |
| các | 0 |
| cái | 0 |
| mạch | B-ORGAN |
| máu | I-ORGAN |
| để | 0 |
| tăng | B-TREATMENT |
| cường | I-TREATMENT |
| lưu | I-TREATMENT |
| thông | I-TREATMENT |
| máu | I-TREATMENT |
| đến | 0 |
| nuôi | B-TREATMENT |
| dưỡng | I-TREATMENT |
| cơ | B-ORGAN |
| tim | B-ORGAN |
| qua | 0 |

## VM600-502 — dòng train 3891 (đếm từ 0)

được cho những cái thiết bị cấy ghép vào cơ thể họ chỉ thanh toán theo cái khung

| Token | Nhãn gốc |
|---|---|
| được | 0 |
| cho | 0 |
| những | 0 |
| cái | 0 |
| thiết | 0 |
| bị | 0 |
| cấy | B-SURGERY |
| ghép | I-SURGERY |
| vào | 0 |
| cơ | B-ORGAN |
| thể | I-ORGAN |
| họ | 0 |
| chỉ | 0 |
| thanh | 0 |
| toán | 0 |
| theo | 0 |
| cái | 0 |
| khung | 0 |

## VM600-503 — dòng train 3895 (đếm từ 0)

chi hoàn toàn có thể xảy ra trên những bệnh nhân bị xơ vữa động mạch vâng rõ ràng là cái bệnh lý về tim mạch về huyết

| Token | Nhãn gốc |
|---|---|
| chi | 0 |
| hoàn | 0 |
| toàn | 0 |
| có | 0 |
| thể | 0 |
| xảy | 0 |
| ra | 0 |
| trên | 0 |
| những | B-UNITCALIBRATOR |
| bệnh | I-UNITCALIBRATOR |
| nhân | I-UNITCALIBRATOR |
| bị | 0 |
| xơ | B-DISEASESYMTOM |
| vữa | I-DISEASESYMTOM |
| động | I-DISEASESYMTOM |
| mạch | I-DISEASESYMTOM |
| vâng | 0 |
| rõ | 0 |
| ràng | 0 |
| là | 0 |
| cái | 0 |
| bệnh | 0 |
| lý | 0 |
| về | 0 |
| tim | B-ORGAN |
| mạch | I-ORGAN |
| về | 0 |
| huyết | B-ORGAN |

## VM600-504 — dòng train 3898 (đếm từ 0)

lành mạnh tôi sẽ giải thích mọi yếu tố này đóng vai trò như thế nào đối với sức khỏe của hệ vi sinh vật vì lợi ích của

| Token | Nhãn gốc |
|---|---|
| lành | 0 |
| mạnh | 0 |
| tôi | 0 |
| sẽ | 0 |
| giải | 0 |
| thích | 0 |
| mọi | 0 |
| yếu | 0 |
| tố | 0 |
| này | 0 |
| đóng | 0 |
| vai | 0 |
| trò | 0 |
| như | 0 |
| thế | 0 |
| nào | 0 |
| đối | 0 |
| với | 0 |
| sức | 0 |
| khỏe | 0 |
| của | 0 |
| hệ | B-ORGAN |
| vi | B-ORGAN |
| sinh | I-ORGAN |
| vật | I-ORGAN |
| vì | 0 |
| lợi | 0 |
| ích | 0 |
| của | 0 |

## VM600-505 — dòng train 3900 (đếm từ 0)

phù hợp nếu mà vì chúng ta chăm sóc nhiều hôm sau nhưng mà đôi khi một số làn da chăm sóc nhiều quá thì thay đổi mụn nữa là thôi nếu

| Token | Nhãn gốc |
|---|---|
| phù | 0 |
| hợp | 0 |
| nếu | 0 |
| mà | 0 |
| vì | 0 |
| chúng | 0 |
| ta | 0 |
| chăm | B-PERSONALCARE |
| sóc | I-PERSONALCARE |
| nhiều | 0 |
| hôm | 0 |
| sau | 0 |
| nhưng | 0 |
| mà | 0 |
| đôi | 0 |
| khi | 0 |
| một | 0 |
| số | 0 |
| làn | B-ORGAN |
| da | I-ORGAN |
| chăm | B-PERSONALCARE |
| sóc | I-PERSONALCARE |
| nhiều | 0 |
| quá | 0 |
| thì | 0 |
| thay | 0 |
| đổi | 0 |
| mụn | B-DISEASESYMTOM |
| nữa | 0 |
| là | 0 |
| thôi | 0 |
| nếu | 0 |

## VM600-506 — dòng train 3908 (đếm từ 0)

biểu hiện của cái thoái hóa cột sống của chúng ta dường như nó không phải là quá không phải ở những giai đoạn rất là sớm

| Token | Nhãn gốc |
|---|---|
| biểu | 0 |
| hiện | 0 |
| của | 0 |
| cái | 0 |
| thoái | B-DISEASESYMTOM |
| hóa | I-DISEASESYMTOM |
| cột | I-DISEASESYMTOM |
| sống | I-DISEASESYMTOM |
| của | 0 |
| chúng | 0 |
| ta | 0 |
| dường | 0 |
| như | 0 |
| nó | 0 |
| không | 0 |
| phải | 0 |
| là | 0 |
| quá | 0 |
| không | 0 |
| phải | 0 |
| ở | 0 |
| những | 0 |
| giai | 0 |
| đoạn | 0 |
| rất | 0 |
| là | 0 |
| sớm | 0 |

## VM600-507 — dòng train 3927 (đếm từ 0)

các cái bệnh lý như là đau tức ngực này hồi hộp trống ngực này đấy thế và và

| Token | Nhãn gốc |
|---|---|
| các | 0 |
| cái | 0 |
| bệnh | 0 |
| lý | 0 |
| như | 0 |
| là | 0 |
| đau | B-DISEASESYMTOM |
| tức | I-DISEASESYMTOM |
| ngực | I-DISEASESYMTOM |
| này | 0 |
| hồi | B-DISEASESYMTOM |
| hộp | I-DISEASESYMTOM |
| trống | I-DISEASESYMTOM |
| ngực | I-DISEASESYMTOM |
| này | 0 |
| đấy | 0 |
| thế | 0 |
| và | 0 |
| và | 0 |

## VM600-508 — dòng train 3928 (đếm từ 0)

đông trùng hạ thảo làm chủ dược nhưng mà kết hợp thêm nấm hầu thủ với đẳng sâm việt nam ở đây cũng là phải nói thêm một

| Token | Nhãn gốc |
|---|---|
| đông | B-DRUGCHEMICAL |
| trùng | I-DRUGCHEMICAL |
| hạ | I-DRUGCHEMICAL |
| thảo | I-DRUGCHEMICAL |
| làm | 0 |
| chủ | 0 |
| dược | 0 |
| nhưng | 0 |
| mà | 0 |
| kết | 0 |
| hợp | 0 |
| thêm | 0 |
| nấm | B-DRUGCHEMICAL |
| hầu | I-DRUGCHEMICAL |
| thủ | I-DRUGCHEMICAL |
| với | 0 |
| đẳng | B-DRUGCHEMICAL |
| sâm | I-DRUGCHEMICAL |
| việt | B-LOCATION |
| nam | I-LOCATION |
| ở | 0 |
| đây | 0 |
| cũng | 0 |
| là | 0 |
| phải | 0 |
| nói | 0 |
| thêm | 0 |
| một | 0 |

## VM600-509 — dòng train 3935 (đếm từ 0)

tim thì có thể sẽ xảy ra bệnh cạnh thiếu máu cơ tim nhồi máu cơ tim có nghĩa là

| Token | Nhãn gốc |
|---|---|
| tim | B-ORGAN |
| thì | 0 |
| có | 0 |
| thể | 0 |
| sẽ | 0 |
| xảy | 0 |
| ra | 0 |
| bệnh | 0 |
| cạnh | 0 |
| thiếu | B-DISEASESYMTOM |
| máu | I-DISEASESYMTOM |
| cơ | B-ORGAN |
| tim | B-ORGAN |
| nhồi | B-DISEASESYMTOM |
| máu | I-DISEASESYMTOM |
| cơ | I-DISEASESYMTOM |
| tim | I-DISEASESYMTOM |
| có | 0 |
| nghĩa | 0 |
| là | 0 |

## VM600-510 — dòng train 3945 (đếm từ 0)

động cảm ơn bác sĩ và thưa tất cả quý vị rõ ràng là chúng ta thấy có rất là nhiều

| Token | Nhãn gốc |
|---|---|
| động | 0 |
| cảm | 0 |
| ơn | 0 |
| bác | B-OCCUPATION |
| sĩ | I-OCCUPATION |
| và | 0 |
| thưa | 0 |
| tất | 0 |
| cả | 0 |
| quý | 0 |
| vị | 0 |
| rõ | 0 |
| ràng | 0 |
| là | 0 |
| chúng | 0 |
| ta | 0 |
| thấy | 0 |
| có | 0 |
| rất | 0 |
| là | 0 |
| nhiều | 0 |

## VM600-511 — dòng train 3950 (đếm từ 0)

sử dụng cái axit lactic để chúng ta phải lên chất đoạn mũi má và chúng ta coi đáp

| Token | Nhãn gốc |
|---|---|
| sử | 0 |
| dụng | 0 |
| cái | 0 |
| axit | B-DRUGCHEMICAL |
| lactic | I-DRUGCHEMICAL |
| để | 0 |
| chúng | 0 |
| ta | 0 |
| phải | 0 |
| lên | 0 |
| chất | 0 |
| đoạn | 0 |
| mũi | B-ORGAN |
| má | B-GENDER |
| và | 0 |
| chúng | 0 |
| ta | 0 |
| coi | 0 |
| đáp | 0 |

## VM600-512 — dòng train 3953 (đếm từ 0)

thì làm sao mục đích thứ nhất là giúp cho người bệnh tăng đề kháng mục đích thứ hai là giúp cho người bệnh làm sao

| Token | Nhãn gốc |
|---|---|
| thì | 0 |
| làm | 0 |
| sao | 0 |
| mục | 0 |
| đích | 0 |
| thứ | B-UNITCALIBRATOR |
| nhất | I-UNITCALIBRATOR |
| là | 0 |
| giúp | 0 |
| cho | 0 |
| người | 0 |
| bệnh | 0 |
| tăng | 0 |
| đề | 0 |
| kháng | 0 |
| mục | 0 |
| đích | 0 |
| thứ | 0 |
| hai | 0 |
| là | 0 |
| giúp | 0 |
| cho | 0 |
| người | 0 |
| bệnh | 0 |
| làm | 0 |
| sao | 0 |

## VM600-513 — dòng train 3954 (đếm từ 0)

cái béo phì vân vân nhiều nhiều những cái cái cái bệnh có thể đưa đến cái béo

| Token | Nhãn gốc |
|---|---|
| cái | 0 |
| béo | B-DISEASESYMTOM |
| phì | I-DISEASESYMTOM |
| vân | 0 |
| vân | 0 |
| nhiều | 0 |
| nhiều | 0 |
| những | 0 |
| cái | 0 |
| cái | 0 |
| cái | 0 |
| bệnh | 0 |
| có | 0 |
| thể | 0 |
| đưa | 0 |
| đến | 0 |
| cái | 0 |
| béo | 0 |

## VM600-514 — dòng train 3971 (đếm từ 0)

thiện những dấu hiệu tê bì kiến bò ở chân tay của bác này thế rồi là những cái dấu hiệu hồi hộp trống ngực của bác

| Token | Nhãn gốc |
|---|---|
| thiện | 0 |
| những | 0 |
| dấu | 0 |
| hiệu | 0 |
| tê | B-DISEASESYMTOM |
| bì | I-DISEASESYMTOM |
| kiến | I-DISEASESYMTOM |
| bò | I-DISEASESYMTOM |
| ở | 0 |
| chân | B-ORGAN |
| tay | I-ORGAN |
| của | 0 |
| bác | B-AGE |
| này | 0 |
| thế | 0 |
| rồi | 0 |
| là | 0 |
| những | 0 |
| cái | 0 |
| dấu | 0 |
| hiệu | 0 |
| hồi | B-DISEASESYMTOM |
| hộp | I-DISEASESYMTOM |
| trống | I-DISEASESYMTOM |
| ngực | I-DISEASESYMTOM |
| của | 0 |
| bác | B-AGE |

## VM600-515 — dòng train 3978 (đếm từ 0)

sau đó thì cũng không nhắc bởi vì nó

| Token | Nhãn gốc |
|---|---|
| sau | 0 |
| đó | 0 |
| thì | 0 |
| cũng | 0 |
| không | 0 |
| nhắc | 0 |
| bởi | 0 |
| vì | 0 |
| nó | 0 |

## VM600-516 — dòng train 3982 (đếm từ 0)

về các cơ chế này và cách chúng bị ảnh hưởng bởi vi khuẩn đường ruột và sức khỏe đường ruột của bạn trên thực tế hệ

| Token | Nhãn gốc |
|---|---|
| về | 0 |
| các | 0 |
| cơ | 0 |
| chế | 0 |
| này | 0 |
| và | 0 |
| cách | 0 |
| chúng | 0 |
| bị | 0 |
| ảnh | 0 |
| hưởng | 0 |
| bởi | 0 |
| vi | B-DISEASESYMTOM |
| khuẩn | I-DISEASESYMTOM |
| đường | B-ORGAN |
| ruột | I-ORGAN |
| và | 0 |
| sức | 0 |
| khỏe | 0 |
| đường | B-ORGAN |
| ruột | I-ORGAN |
| của | 0 |
| bạn | 0 |
| trên | 0 |
| thực | 0 |
| tế | 0 |
| hệ | 0 |

## VM600-517 — dòng train 3988 (đếm từ 0)

rất nhiều các cái trường hợp mà cái thận của chức năng thận nó bị ảnh hưởng nhiều và nhiều bệnh nhân bị suy thận do

| Token | Nhãn gốc |
|---|---|
| rất | B-UNITCALIBRATOR |
| nhiều | I-UNITCALIBRATOR |
| các | 0 |
| cái | 0 |
| trường | 0 |
| hợp | 0 |
| mà | 0 |
| cái | 0 |
| thận | B-ORGAN |
| của | 0 |
| chức | 0 |
| năng | 0 |
| thận | B-ORGAN |
| nó | 0 |
| bị | 0 |
| ảnh | 0 |
| hưởng | 0 |
| nhiều | 0 |
| và | 0 |
| nhiều | 0 |
| bệnh | B-OCCUPATION |
| nhân | I-OCCUPATION |
| bị | 0 |
| suy | B-DISEASESYMTOM |
| thận | I-DISEASESYMTOM |
| do | 0 |

## VM600-518 — dòng train 3991 (đếm từ 0)

nên là cái thời gian đầu thì có thể mình sẽ lựa chọn cái cục pin không sạc sau khi mà mình đặt xong mình

| Token | Nhãn gốc |
|---|---|
| nên | 0 |
| là | 0 |
| cái | 0 |
| thời | B-DATETIME |
| gian | I-DATETIME |
| đầu | 0 |
| thì | 0 |
| có | 0 |
| thể | 0 |
| mình | 0 |
| sẽ | 0 |
| lựa | 0 |
| chọn | 0 |
| cái | 0 |
| cục | 0 |
| pin | 0 |
| không | 0 |
| sạc | 0 |
| sau | 0 |
| khi | 0 |
| mà | 0 |
| mình | 0 |
| đặt | 0 |
| xong | 0 |
| mình | 0 |

## VM600-519 — dòng train 3998 (đếm từ 0)

tử protein của vi khuẩn liên quan tới một quá trình thiết yếu và phức tạp một

| Token | Nhãn gốc |
|---|---|
| tử | 0 |
| protein | B-DRUGCHEMICAL |
| của | 0 |
| vi | B-DISEASESYMTOM |
| khuẩn | I-DISEASESYMTOM |
| liên | 0 |
| quan | 0 |
| tới | 0 |
| một | 0 |
| quá | 0 |
| trình | 0 |
| thiết | 0 |
| yếu | 0 |
| và | 0 |
| phức | 0 |
| tạp | 0 |
| một | 0 |

## VM600-520 — dòng train 4015 (đếm từ 0)

biến chứng nguy hiểm thế thì của bác có vấn đề gì huyết áp này đái tháo đường này phải không ạ và cái nữa là liên quan đến

| Token | Nhãn gốc |
|---|---|
| biến | B-DISEASESYMTOM |
| chứng | I-DISEASESYMTOM |
| nguy | 0 |
| hiểm | 0 |
| thế | 0 |
| thì | 0 |
| của | 0 |
| bác | B-AGE |
| có | 0 |
| vấn | 0 |
| đề | 0 |
| gì | 0 |
| huyết | B-DISEASESYMTOM |
| áp | I-DISEASESYMTOM |
| này | 0 |
| đái | B-DISEASESYMTOM |
| tháo | I-DISEASESYMTOM |
| đường | I-DISEASESYMTOM |
| này | 0 |
| phải | 0 |
| không | 0 |
| ạ | 0 |
| và | 0 |
| cái | 0 |
| nữa | 0 |
| là | 0 |
| liên | 0 |
| quan | 0 |
| đến | 0 |

## VM600-521 — dòng train 4021 (đếm từ 0)

dụ như là lở loét miệng thì thực ra mình nói lở loét miệng chỉ do kẽm không thôi thì cũng chỉ là một phần thôi

| Token | Nhãn gốc |
|---|---|
| dụ | 0 |
| như | 0 |
| là | 0 |
| lở | 0 |
| loét | 0 |
| miệng | B-ORGAN |
| thì | 0 |
| thực | 0 |
| ra | 0 |
| mình | 0 |
| nói | 0 |
| lở | 0 |
| loét | 0 |
| miệng | B-ORGAN |
| chỉ | 0 |
| do | 0 |
| kẽm | B-DRUGCHEMICAL |
| không | 0 |
| thôi | 0 |
| thì | 0 |
| cũng | 0 |
| chỉ | 0 |
| là | 0 |
| một | B-UNITCALIBRATOR |
| phần | I-UNITCALIBRATOR |
| thôi | 0 |

## VM600-522 — dòng train 4022 (đếm từ 0)

chấm mấy lận cũng như là mấy cái người về mà bác sĩ mà tiểu đường ở đây đó bác sĩ và ta nói

| Token | Nhãn gốc |
|---|---|
| chấm | 0 |
| mấy | 0 |
| lận | 0 |
| cũng | 0 |
| như | 0 |
| là | 0 |
| mấy | 0 |
| cái | 0 |
| người | 0 |
| về | 0 |
| mà | 0 |
| bác | B-OCCUPATION |
| sĩ | I-OCCUPATION |
| mà | 0 |
| tiểu | B-DISEASESYMTOM |
| đường | I-DISEASESYMTOM |
| ở | 0 |
| đây | 0 |
| đó | 0 |
| bác | B-OCCUPATION |
| sĩ | I-OCCUPATION |
| và | 0 |
| ta | 0 |
| nói | 0 |

## VM600-523 — dòng train 4023 (đếm từ 0)

chủ chốt của cơ thể trong hoạt động cùng với chức năng sinh lý học của bạn đặc biệt là hệ thần kinh xếp cùng nhau các

| Token | Nhãn gốc |
|---|---|
| chủ | 0 |
| chốt | 0 |
| của | 0 |
| cơ | B-ORGAN |
| thể | I-ORGAN |
| trong | 0 |
| hoạt | 0 |
| động | 0 |
| cùng | 0 |
| với | 0 |
| chức | 0 |
| năng | 0 |
| sinh | 0 |
| lý | 0 |
| học | 0 |
| của | 0 |
| bạn | 0 |
| đặc | 0 |
| biệt | 0 |
| là | 0 |
| hệ | 0 |
| thần | B-ORGAN |
| kinh | I-ORGAN |
| xếp | 0 |
| cùng | 0 |
| nhau | 0 |
| các | 0 |

## VM600-524 — dòng train 4044 (đếm từ 0)

thể khác và nó lại sinh sôi nảy nở và có cái điều kiện tiếp xúc gần với những khi người khác nữa thì virus đó lại là có

| Token | Nhãn gốc |
|---|---|
| thể | 0 |
| khác | 0 |
| và | 0 |
| nó | 0 |
| lại | 0 |
| sinh | 0 |
| sôi | 0 |
| nảy | 0 |
| nở | 0 |
| và | 0 |
| có | 0 |
| cái | 0 |
| điều | 0 |
| kiện | 0 |
| tiếp | 0 |
| xúc | 0 |
| gần | 0 |
| với | 0 |
| những | 0 |
| khi | 0 |
| người | 0 |
| khác | 0 |
| nữa | 0 |
| thì | 0 |
| virus | B-DISEASESYMTOM |
| đó | 0 |
| lại | 0 |
| là | 0 |
| có | 0 |

## VM600-525 — dòng train 4047 (đếm từ 0)

là cái tư thế vận động của người ta như thế nào vì sao vì tất cả những cái chuyện này là những cái yếu tố nó có tác

| Token | Nhãn gốc |
|---|---|
| là | 0 |
| cái | 0 |
| tư | 0 |
| thế | 0 |
| vận | 0 |
| động | 0 |
| của | 0 |
| người | 0 |
| ta | 0 |
| như | 0 |
| thế | 0 |
| nào | 0 |
| vì | 0 |
| sao | 0 |
| vì | 0 |
| tất | 0 |
| cả | 0 |
| những | 0 |
| cái | 0 |
| chuyện | 0 |
| này | 0 |
| là | 0 |
| những | 0 |
| cái | 0 |
| yếu | 0 |
| tố | 0 |
| nó | 0 |
| có | 0 |
| tác | 0 |

## VM600-526 — dòng train 4050 (đếm từ 0)

trăm nghìn tỷ sinh vật vô hình này bao phủ bên trong và bên ngoài cơ thể bạn phát triển mạnh trong miệng mũi tai ruột

| Token | Nhãn gốc |
|---|---|
| trăm | B-UNITCALIBRATOR |
| nghìn | I-UNITCALIBRATOR |
| tỷ | I-UNITCALIBRATOR |
| sinh | 0 |
| vật | 0 |
| vô | 0 |
| hình | 0 |
| này | 0 |
| bao | 0 |
| phủ | 0 |
| bên | 0 |
| trong | 0 |
| và | 0 |
| bên | B-LOCATION |
| ngoài | I-LOCATION |
| cơ | B-ORGAN |
| thể | I-ORGAN |
| bạn | 0 |
| phát | 0 |
| triển | 0 |
| mạnh | 0 |
| trong | 0 |
| miệng | B-ORGAN |
| mũi | B-ORGAN |
| tai | B-ORGAN |
| ruột | B-ORGAN |

## VM600-527 — dòng train 4056 (đếm từ 0)

đời có một ca sinh mổ theo nguyện vọng và được uống sữa công thức hoàn toàn cô bé mắt nhiều bệnh nhiễm trùng khi còn

| Token | Nhãn gốc |
|---|---|
| đời | 0 |
| có | 0 |
| một | B-UNITCALIBRATOR |
| ca | I-UNITCALIBRATOR |
| sinh | B-SURGERY |
| mổ | I-SURGERY |
| theo | 0 |
| nguyện | 0 |
| vọng | 0 |
| và | 0 |
| được | 0 |
| uống | 0 |
| sữa | B-FOODDRINK |
| công | I-FOODDRINK |
| thức | I-FOODDRINK |
| hoàn | 0 |
| toàn | 0 |
| cô | B-GENDER |
| bé | I-GENDER |
| mắt | B-ORGAN |
| nhiều | 0 |
| bệnh | 0 |
| nhiễm | B-DISEASESYMTOM |
| trùng | I-DISEASESYMTOM |
| khi | 0 |
| còn | 0 |

## VM600-528 — dòng train 4058 (đếm từ 0)

chung nhất về cái vai trò quan trọng của dinh dưỡng đối với người bệnh ung thư được không ạ vâng ạ nếu nói về dinh

| Token | Nhãn gốc |
|---|---|
| chung | 0 |
| nhất | 0 |
| về | 0 |
| cái | 0 |
| vai | 0 |
| trò | 0 |
| quan | 0 |
| trọng | 0 |
| của | 0 |
| dinh | 0 |
| dưỡng | 0 |
| đối | 0 |
| với | 0 |
| người | 0 |
| bệnh | 0 |
| ung | B-DISEASESYMTOM |
| thư | I-DISEASESYMTOM |
| được | 0 |
| không | 0 |
| ạ | 0 |
| vâng | 0 |
| ạ | 0 |
| nếu | 0 |
| nói | 0 |
| về | 0 |
| dinh | 0 |

## VM600-529 — dòng train 4077 (đếm từ 0)

truyền miệng thì sau đó thì sau một cái thời gian dài họ thử nghiệm mọi thứ

| Token | Nhãn gốc |
|---|---|
| truyền | B-MEDDEVICETECHNIQUE |
| miệng | I-MEDDEVICETECHNIQUE |
| thì | 0 |
| sau | 0 |
| đó | 0 |
| thì | 0 |
| sau | 0 |
| một | 0 |
| cái | 0 |
| thời | B-DATETIME |
| gian | I-DATETIME |
| dài | 0 |
| họ | 0 |
| thử | 0 |
| nghiệm | 0 |
| mọi | 0 |
| thứ | 0 |

## VM600-530 — dòng train 4081 (đếm từ 0)

lo âu bồn chồn và có đôi khi ảo giác và có thể có ý định tự tử thì tất

| Token | Nhãn gốc |
|---|---|
| lo | B-DISEASESYMTOM |
| âu | I-DISEASESYMTOM |
| bồn | 0 |
| chồn | 0 |
| và | 0 |
| có | 0 |
| đôi | 0 |
| khi | 0 |
| ảo | B-DISEASESYMTOM |
| giác | I-DISEASESYMTOM |
| và | 0 |
| có | 0 |
| thể | 0 |
| có | B-DISEASESYMTOM |
| ý | I-DISEASESYMTOM |
| định | I-DISEASESYMTOM |
| tự | I-DISEASESYMTOM |
| tử | I-DISEASESYMTOM |
| thì | 0 |
| tất | 0 |

## VM600-531 — dòng train 4089 (đếm từ 0)

hiện tượng sẽ được đề cập khác cuốn sách này sẽ khám phá ảnh hưởng của việc làm việc ca đêm đến hệ miễn dịch của chúng

| Token | Nhãn gốc |
|---|---|
| hiện | 0 |
| tượng | 0 |
| sẽ | 0 |
| được | 0 |
| đề | 0 |
| cập | 0 |
| khác | 0 |
| cuốn | 0 |
| sách | 0 |
| này | 0 |
| sẽ | 0 |
| khám | B-DIAGNOSTICS |
| phá | 0 |
| ảnh | 0 |
| hưởng | 0 |
| của | 0 |
| việc | 0 |
| làm | 0 |
| việc | 0 |
| ca | 0 |
| đêm | 0 |
| đến | 0 |
| hệ | B-ORGAN |
| miễn | I-ORGAN |
| dịch | I-ORGAN |
| của | 0 |
| chúng | 0 |

## VM600-532 — dòng train 4095 (đếm từ 0)

phẩm mà nó tác động vào cái mảng xơ vữa nên là nó cần phải có thời gian nên là bác nên sử dụng kéo dài từ ba đến sáu tháng

| Token | Nhãn gốc |
|---|---|
| phẩm | 0 |
| mà | 0 |
| nó | 0 |
| tác | 0 |
| động | 0 |
| vào | 0 |
| cái | 0 |
| mảng | B-DISEASESYMTOM |
| xơ | I-DISEASESYMTOM |
| vữa | I-DISEASESYMTOM |
| nên | 0 |
| là | 0 |
| nó | 0 |
| cần | 0 |
| phải | 0 |
| có | 0 |
| thời | B-DATETIME |
| gian | I-DATETIME |
| nên | 0 |
| là | 0 |
| bác | B-AGE |
| nên | 0 |
| sử | 0 |
| dụng | 0 |
| kéo | 0 |
| dài | 0 |
| từ | 0 |
| ba | B-DATETIME |
| đến | I-DATETIME |
| sáu | I-DATETIME |
| tháng | I-DATETIME |

## VM600-533 — dòng train 4098 (đếm từ 0)

trong tế bào của chúng ta nó có dna riêng tách biệt với dna trong nhân tế bào trên thực tế ti thể có thể được coi

| Token | Nhãn gốc |
|---|---|
| trong | 0 |
| tế | B-ORGAN |
| bào | I-ORGAN |
| của | 0 |
| chúng | 0 |
| ta | 0 |
| nó | 0 |
| có | 0 |
| dna | B-ORGAN |
| riêng | 0 |
| tách | 0 |
| biệt | 0 |
| với | 0 |
| dna | B-ORGAN |
| trong | 0 |
| nhân | 0 |
| tế | B-ORGAN |
| bào | I-ORGAN |
| trên | 0 |
| thực | 0 |
| tế | 0 |
| ti | B-ORGAN |
| thể | I-ORGAN |
| có | 0 |
| thể | 0 |
| được | 0 |
| coi | 0 |

## VM600-534 — dòng train 4103 (đếm từ 0)

công tác điều trị parkinson cũng như là mức độ hiệu quả của phương pháp này như thế nào chúng ta biết rằng là bệnh parkinson

| Token | Nhãn gốc |
|---|---|
| công | 0 |
| tác | 0 |
| điều | B-TREATMENT |
| trị | I-TREATMENT |
| parkinson | B-DISEASESYMTOM |
| cũng | 0 |
| như | 0 |
| là | 0 |
| mức | B-UNITCALIBRATOR |
| độ | I-UNITCALIBRATOR |
| hiệu | 0 |
| quả | 0 |
| của | 0 |
| phương | 0 |
| pháp | 0 |
| này | 0 |
| như | 0 |
| thế | 0 |
| nào | 0 |
| chúng | 0 |
| ta | 0 |
| biết | 0 |
| rằng | 0 |
| là | 0 |
| bệnh | 0 |
| parkinson | B-DISEASESYMTOM |

## VM600-535 — dòng train 4106 (đếm từ 0)

ở người bị nhiễm virus có thể tạo ra một trăm phần tử virus mối điều này có nghĩa là chỉ cần ba bản

| Token | Nhãn gốc |
|---|---|
| ở | 0 |
| người | 0 |
| bị | 0 |
| nhiễm | 0 |
| virus | B-DISEASESYMTOM |
| có | 0 |
| thể | 0 |
| tạo | 0 |
| ra | 0 |
| một | B-UNITCALIBRATOR |
| trăm | I-UNITCALIBRATOR |
| phần | I-UNITCALIBRATOR |
| tử | I-UNITCALIBRATOR |
| virus | B-DISEASESYMTOM |
| mối | 0 |
| điều | 0 |
| này | 0 |
| có | 0 |
| nghĩa | 0 |
| là | 0 |
| chỉ | 0 |
| cần | 0 |
| ba | 0 |
| bản | 0 |

## VM600-536 — dòng train 4112 (đếm từ 0)

là lú lẫn hay quên sa sút trí tuệ aizheimer parkinson rồi là ta di

| Token | Nhãn gốc |
|---|---|
| là | 0 |
| lú | B-DISEASESYMTOM |
| lẫn | I-DISEASESYMTOM |
| hay | B-DISEASESYMTOM |
| quên | I-DISEASESYMTOM |
| sa | B-DISEASESYMTOM |
| sút | I-DISEASESYMTOM |
| trí | I-DISEASESYMTOM |
| tuệ | I-DISEASESYMTOM |
| aizheimer | B-DISEASESYMTOM |
| parkinson | B-DISEASESYMTOM |
| rồi | 0 |
| là | 0 |
| ta | 0 |
| di | 0 |

## VM600-537 — dòng train 4119 (đếm từ 0)

người béo phì mà người ta đã từng trị liệu được mổ rồi nè được điều trị tốt nè được tập luyện tốt giữ được

| Token | Nhãn gốc |
|---|---|
| người | 0 |
| béo | B-DISEASESYMTOM |
| phì | I-DISEASESYMTOM |
| mà | 0 |
| người | 0 |
| ta | 0 |
| đã | 0 |
| từng | 0 |
| trị | B-TREATMENT |
| liệu | I-TREATMENT |
| được | 0 |
| mổ | B-SURGERY |
| rồi | 0 |
| nè | 0 |
| được | 0 |
| điều | B-TREATMENT |
| trị | I-TREATMENT |
| tốt | 0 |
| nè | 0 |
| được | 0 |
| tập | 0 |
| luyện | 0 |
| tốt | 0 |
| giữ | 0 |
| được | 0 |

## VM600-538 — dòng train 4120 (đếm từ 0)

đầu tiên chúng tôi khuyên là như vậy và cái thứ hai nữa là có lẽ là bác nên có một cái đai thắt lưng để mình bảo vệ cái

| Token | Nhãn gốc |
|---|---|
| đầu | 0 |
| tiên | 0 |
| chúng | 0 |
| tôi | 0 |
| khuyên | 0 |
| là | 0 |
| như | 0 |
| vậy | 0 |
| và | 0 |
| cái | B-UNITCALIBRATOR |
| thứ | I-UNITCALIBRATOR |
| hai | I-UNITCALIBRATOR |
| nữa | 0 |
| là | 0 |
| có | 0 |
| lẽ | 0 |
| là | 0 |
| bác | B-AGE |
| nên | 0 |
| có | 0 |
| một | 0 |
| cái | 0 |
| đai | 0 |
| thắt | B-ORGAN |
| lưng | I-ORGAN |
| để | 0 |
| mình | 0 |
| bảo | 0 |
| vệ | 0 |
| cái | 0 |

## VM600-539 — dòng train 4134 (đếm từ 0)

bệnh lý các cái biến chứng như là các cái nhồi máu ở cơ tim nhưng thấy nhồi

| Token | Nhãn gốc |
|---|---|
| bệnh | 0 |
| lý | 0 |
| các | 0 |
| cái | 0 |
| biến | B-DISEASESYMTOM |
| chứng | I-DISEASESYMTOM |
| như | 0 |
| là | 0 |
| các | 0 |
| cái | 0 |
| nhồi | 0 |
| máu | B-ORGAN |
| ở | 0 |
| cơ | B-ORGAN |
| tim | B-ORGAN |
| nhưng | 0 |
| thấy | 0 |
| nhồi | 0 |

## VM600-540 — dòng train 4136 (đếm từ 0)

đến và chúng ta không không nhận biết được cái điều đó cho nên chúng ta chỉ nghĩ là à thôi thì đau khớp chúng ta có

| Token | Nhãn gốc |
|---|---|
| đến | 0 |
| và | 0 |
| chúng | 0 |
| ta | 0 |
| không | 0 |
| không | 0 |
| nhận | 0 |
| biết | 0 |
| được | 0 |
| cái | 0 |
| điều | 0 |
| đó | 0 |
| cho | 0 |
| nên | 0 |
| chúng | 0 |
| ta | 0 |
| chỉ | 0 |
| nghĩ | 0 |
| là | 0 |
| à | 0 |
| thôi | 0 |
| thì | 0 |
| đau | B-DISEASESYMTOM |
| khớp | B-ORGAN |
| chúng | 0 |
| ta | 0 |
| có | 0 |

## VM600-541 — dòng train 4143 (đếm từ 0)

một số trục trặc về tóc kể cả bạc tóc thế cho nên là những hoạt chất từ thiên nhiên này tỏ ra rất là an toàn và trong

| Token | Nhãn gốc |
|---|---|
| một | 0 |
| số | 0 |
| trục | 0 |
| trặc | 0 |
| về | 0 |
| tóc | B-ORGAN |
| kể | 0 |
| cả | 0 |
| bạc | B-DISEASESYMTOM |
| tóc | I-DISEASESYMTOM |
| thế | 0 |
| cho | 0 |
| nên | 0 |
| là | 0 |
| những | 0 |
| hoạt | B-DRUGCHEMICAL |
| chất | I-DRUGCHEMICAL |
| từ | 0 |
| thiên | 0 |
| nhiên | 0 |
| này | 0 |
| tỏ | 0 |
| ra | 0 |
| rất | 0 |
| là | 0 |
| an | 0 |
| toàn | 0 |
| và | 0 |
| trong | 0 |

## VM600-542 — dòng train 4168 (đếm từ 0)

thuốc xong rồi một thời gian thì tôi đi đo tôi đi

| Token | Nhãn gốc |
|---|---|
| thuốc | B-DRUGCHEMICAL |
| xong | 0 |
| rồi | 0 |
| một | 0 |
| thời | B-DATETIME |
| gian | I-DATETIME |
| thì | 0 |
| tôi | 0 |
| đi | 0 |
| đo | 0 |
| tôi | 0 |
| đi | 0 |

## VM600-543 — dòng train 4169 (đếm từ 0)

thì cái vấn đề của anh gặp phải nó đang có những cái triệu chứng như thế nào cũng như là nó diễn biến như thế nào trong cái thời gian vừa rồi thì anh có

| Token | Nhãn gốc |
|---|---|
| thì | 0 |
| cái | 0 |
| vấn | 0 |
| đề | 0 |
| của | 0 |
| anh | B-GENDER |
| gặp | 0 |
| phải | 0 |
| nó | 0 |
| đang | 0 |
| có | 0 |
| những | 0 |
| cái | 0 |
| triệu | B-DISEASESYMTOM |
| chứng | I-DISEASESYMTOM |
| như | 0 |
| thế | 0 |
| nào | 0 |
| cũng | 0 |
| như | 0 |
| là | 0 |
| nó | 0 |
| diễn | 0 |
| biến | 0 |
| như | 0 |
| thế | 0 |
| nào | 0 |
| trong | 0 |
| cái | 0 |
| thời | B-DATETIME |
| gian | I-DATETIME |
| vừa | 0 |
| rồi | 0 |
| thì | 0 |
| anh | B-GENDER |
| có | 0 |

## VM600-544 — dòng train 4180 (đếm từ 0)

đối với sau điều trị ung thư là cần thiết để chúng ta phát hiện sớm những cái dấu hiệu rất có thể chúng ta có ung

| Token | Nhãn gốc |
|---|---|
| đối | 0 |
| với | 0 |
| sau | 0 |
| điều | B-TREATMENT |
| trị | I-TREATMENT |
| ung | B-DISEASESYMTOM |
| thư | I-DISEASESYMTOM |
| là | 0 |
| cần | 0 |
| thiết | 0 |
| để | 0 |
| chúng | 0 |
| ta | 0 |
| phát | 0 |
| hiện | 0 |
| sớm | 0 |
| những | 0 |
| cái | 0 |
| dấu | 0 |
| hiệu | 0 |
| rất | 0 |
| có | 0 |
| thể | 0 |
| chúng | 0 |
| ta | 0 |
| có | 0 |
| ung | 0 |

## VM600-545 — dòng train 4191 (đếm từ 0)

một cái giờ định kỳ cái sau đó dùng là các cái lần tái khám thì bác đưa cho các

| Token | Nhãn gốc |
|---|---|
| một | 0 |
| cái | 0 |
| giờ | 0 |
| định | B-DATETIME |
| kỳ | I-DATETIME |
| cái | 0 |
| sau | 0 |
| đó | 0 |
| dùng | 0 |
| là | 0 |
| các | 0 |
| cái | 0 |
| lần | 0 |
| tái | 0 |
| khám | B-DIAGNOSTICS |
| thì | 0 |
| bác | B-AGE |
| đưa | 0 |
| cho | 0 |
| các | 0 |

## VM600-546 — dòng train 4201 (đếm từ 0)

tăng huy động tế bào tăng nhiệt độ cơ thể tăng tiêu hao năng lượng như bên cạnh đó thì cái việc mà bị ung thư thì

| Token | Nhãn gốc |
|---|---|
| tăng | 0 |
| huy | 0 |
| động | 0 |
| tế | B-ORGAN |
| bào | I-ORGAN |
| tăng | 0 |
| nhiệt | 0 |
| độ | 0 |
| cơ | B-ORGAN |
| thể | I-ORGAN |
| tăng | 0 |
| tiêu | 0 |
| hao | 0 |
| năng | 0 |
| lượng | 0 |
| như | 0 |
| bên | 0 |
| cạnh | 0 |
| đó | 0 |
| thì | 0 |
| cái | 0 |
| việc | 0 |
| mà | 0 |
| bị | 0 |
| ung | B-DISEASESYMTOM |
| thư | I-DISEASESYMTOM |
| thì | 0 |

## VM600-547 — dòng train 4204 (đếm từ 0)

định cân bằng được cái stress ổn định này rồi thì cái việc mà cái điều trị tích cực đó

| Token | Nhãn gốc |
|---|---|
| định | 0 |
| cân | 0 |
| bằng | 0 |
| được | 0 |
| cái | 0 |
| stress | B-DISEASESYMTOM |
| ổn | 0 |
| định | 0 |
| này | 0 |
| rồi | 0 |
| thì | 0 |
| cái | 0 |
| việc | 0 |
| mà | 0 |
| cái | 0 |
| điều | B-TREATMENT |
| trị | I-TREATMENT |
| tích | 0 |
| cực | 0 |
| đó | 0 |

## VM600-548 — dòng train 4207 (đếm từ 0)

họ tiếp xúc với bệnh đậu mùa bò một loại nhiễm virus nhẹ mà con người có thể mắc

| Token | Nhãn gốc |
|---|---|
| họ | 0 |
| tiếp | 0 |
| xúc | 0 |
| với | 0 |
| bệnh | 0 |
| đậu | B-DISEASESYMTOM |
| mùa | I-DISEASESYMTOM |
| bò | 0 |
| một | 0 |
| loại | 0 |
| nhiễm | 0 |
| virus | B-DISEASESYMTOM |
| nhẹ | 0 |
| mà | 0 |
| con | 0 |
| người | 0 |
| có | 0 |
| thể | 0 |
| mắc | 0 |

## VM600-549 — dòng train 4227 (đếm từ 0)

tác dụng phụ lên đường tiêu hóa lên các cái hệ nội tạng chính vì vậy cho nên đấy là một trong những cái hướng mà tiếp cận

| Token | Nhãn gốc |
|---|---|
| tác | B-DISEASESYMTOM |
| dụng | I-DISEASESYMTOM |
| phụ | I-DISEASESYMTOM |
| lên | 0 |
| đường | B-ORGAN |
| tiêu | I-ORGAN |
| hóa | I-ORGAN |
| lên | 0 |
| các | 0 |
| cái | 0 |
| hệ | 0 |
| nội | B-ORGAN |
| tạng | I-ORGAN |
| chính | 0 |
| vì | 0 |
| vậy | 0 |
| cho | 0 |
| nên | 0 |
| đấy | 0 |
| là | 0 |
| một | B-UNITCALIBRATOR |
| trong | I-UNITCALIBRATOR |
| những | I-UNITCALIBRATOR |
| cái | I-UNITCALIBRATOR |
| hướng | I-UNITCALIBRATOR |
| mà | 0 |
| tiếp | 0 |
| cận | 0 |

## VM600-550 — dòng train 4235 (đếm từ 0)

đôi khi có một số bạn cũng như biết không chia sẻ là em ngủ dậy là coi như mặt em dùng chảo dầu bóng loáng

| Token | Nhãn gốc |
|---|---|
| đôi | 0 |
| khi | 0 |
| có | 0 |
| một | 0 |
| số | 0 |
| bạn | 0 |
| cũng | 0 |
| như | 0 |
| biết | 0 |
| không | 0 |
| chia | 0 |
| sẻ | 0 |
| là | 0 |
| em | 0 |
| ngủ | B-PERSONALCARE |
| dậy | I-PERSONALCARE |
| là | 0 |
| coi | 0 |
| như | 0 |
| mặt | 0 |
| em | 0 |
| dùng | 0 |
| chảo | 0 |
| dầu | 0 |
| bóng | 0 |
| loáng | 0 |

## VM600-551 — dòng train 4245 (đếm từ 0)

chúng ta nó có chính là ba giai đoạn ba giai đoạn chính giai đoạn thứ nhất là giai đoạn mà phát triển hay là giai đoạn

| Token | Nhãn gốc |
|---|---|
| chúng | 0 |
| ta | 0 |
| nó | 0 |
| có | 0 |
| chính | 0 |
| là | 0 |
| ba | B-UNITCALIBRATOR |
| giai | I-UNITCALIBRATOR |
| đoạn | I-UNITCALIBRATOR |
| ba | B-UNITCALIBRATOR |
| giai | I-UNITCALIBRATOR |
| đoạn | I-UNITCALIBRATOR |
| chính | 0 |
| giai | B-UNITCALIBRATOR |
| đoạn | I-UNITCALIBRATOR |
| thứ | B-UNITCALIBRATOR |
| nhất | I-UNITCALIBRATOR |
| là | 0 |
| giai | 0 |
| đoạn | 0 |
| mà | 0 |
| phát | 0 |
| triển | 0 |
| hay | 0 |
| là | 0 |
| giai | 0 |
| đoạn | 0 |

## VM600-552 — dòng train 4247 (đếm từ 0)

tiềm tàng là bất định nhưng hậu quả khi mọi thứ lạc lối có thể là khủng khiếp nỗ

| Token | Nhãn gốc |
|---|---|
| tiềm | 0 |
| tàng | 0 |
| là | 0 |
| bất | 0 |
| định | 0 |
| nhưng | 0 |
| hậu | 0 |
| quả | 0 |
| khi | 0 |
| mọi | 0 |
| thứ | 0 |
| lạc | 0 |
| lối | 0 |
| có | 0 |
| thể | 0 |
| là | 0 |
| khủng | 0 |
| khiếp | 0 |
| nỗ | 0 |

## VM600-553 — dòng train 4248 (đếm từ 0)

tính ra năng lượng là chí ít nó cũng phải đạt được khoảng một phẩy hai một đến một phẩy hai kcal trong

| Token | Nhãn gốc |
|---|---|
| tính | 0 |
| ra | 0 |
| năng | 0 |
| lượng | 0 |
| là | 0 |
| chí | 0 |
| ít | 0 |
| nó | 0 |
| cũng | 0 |
| phải | 0 |
| đạt | 0 |
| được | 0 |
| khoảng | 0 |
| một | 0 |
| phẩy | 0 |
| hai | 0 |
| một | 0 |
| đến | 0 |
| một | 0 |
| phẩy | 0 |
| hai | 0 |
| kcal | B-UNITCALIBRATOR |
| trong | 0 |

## VM600-554 — dòng train 4253 (đếm từ 0)

nói rằng là cái lượng máu để mà nuôi tim nuôi náo nó bị suy giảm nếu như chỉ suy

| Token | Nhãn gốc |
|---|---|
| nói | 0 |
| rằng | 0 |
| là | 0 |
| cái | 0 |
| lượng | 0 |
| máu | B-ORGAN |
| để | 0 |
| mà | 0 |
| nuôi | B-TREATMENT |
| tim | I-TREATMENT |
| nuôi | 0 |
| náo | 0 |
| nó | 0 |
| bị | 0 |
| suy | 0 |
| giảm | 0 |
| nếu | 0 |
| như | 0 |
| chỉ | 0 |
| suy | 0 |

## VM600-555 — dòng train 4255 (đếm từ 0)

như là một số khán giả có nội dung tương tự và câu hỏi gửi về cho chương trình thưa bác sĩ nghe nói phẫu thuật đặt điện

| Token | Nhãn gốc |
|---|---|
| như | 0 |
| là | 0 |
| một | 0 |
| số | 0 |
| khán | B-OCCUPATION |
| giả | I-OCCUPATION |
| có | 0 |
| nội | 0 |
| dung | 0 |
| tương | 0 |
| tự | 0 |
| và | 0 |
| câu | 0 |
| hỏi | 0 |
| gửi | 0 |
| về | 0 |
| cho | 0 |
| chương | 0 |
| trình | 0 |
| thưa | 0 |
| bác | B-OCCUPATION |
| sĩ | I-OCCUPATION |
| nghe | 0 |
| nói | 0 |
| phẫu | B-SURGERY |
| thuật | I-SURGERY |
| đặt | 0 |
| điện | 0 |

## VM600-556 — dòng train 4258 (đếm từ 0)

bào tim trong điều kiện thiếu oxy cho nên có thể nói rằng là với hệ thống tim

| Token | Nhãn gốc |
|---|---|
| bào | 0 |
| tim | B-ORGAN |
| trong | 0 |
| điều | 0 |
| kiện | 0 |
| thiếu | B-DISEASESYMTOM |
| oxy | I-DISEASESYMTOM |
| cho | 0 |
| nên | 0 |
| có | 0 |
| thể | 0 |
| nói | 0 |
| rằng | 0 |
| là | 0 |
| với | 0 |
| hệ | 0 |
| thống | 0 |
| tim | B-ORGAN |

## VM600-557 — dòng train 4262 (đếm từ 0)

người bệnh có đông cứng về dáng đi hoặc là đi dễ té ngã mà những cái triệu chứng này nó không cải thiện với các cái thuốc

| Token | Nhãn gốc |
|---|---|
| người | 0 |
| bệnh | 0 |
| có | 0 |
| đông | B-DISEASESYMTOM |
| cứng | I-DISEASESYMTOM |
| về | I-DISEASESYMTOM |
| dáng | I-DISEASESYMTOM |
| đi | I-DISEASESYMTOM |
| hoặc | 0 |
| là | 0 |
| đi | B-DISEASESYMTOM |
| dễ | I-DISEASESYMTOM |
| té | I-DISEASESYMTOM |
| ngã | I-DISEASESYMTOM |
| mà | 0 |
| những | 0 |
| cái | 0 |
| triệu | B-DISEASESYMTOM |
| chứng | I-DISEASESYMTOM |
| này | 0 |
| nó | 0 |
| không | 0 |
| cải | B-TREATMENT |
| thiện | I-TREATMENT |
| với | 0 |
| các | 0 |
| cái | 0 |
| thuốc | B-DRUGCHEMICAL |

## VM600-558 — dòng train 4279 (đếm từ 0)

bị tổn thương hơn đường tiêu hóa chúng ta dễ bị tổn thương hơn như vậy đó ở những người lớn tuổi chúng ta rất là

| Token | Nhãn gốc |
|---|---|
| bị | B-DISEASESYMTOM |
| tổn | B-DISEASESYMTOM |
| thương | I-DISEASESYMTOM |
| hơn | 0 |
| đường | B-ORGAN |
| tiêu | I-ORGAN |
| hóa | I-ORGAN |
| chúng | 0 |
| ta | 0 |
| dễ | 0 |
| bị | B-DISEASESYMTOM |
| tổn | B-DISEASESYMTOM |
| thương | I-DISEASESYMTOM |
| hơn | 0 |
| như | 0 |
| vậy | 0 |
| đó | 0 |
| ở | 0 |
| những | 0 |
| người | B-AGE |
| lớn | I-AGE |
| tuổi | I-AGE |
| chúng | 0 |
| ta | 0 |
| rất | 0 |
| là | 0 |

## VM600-559 — dòng train 4283 (đếm từ 0)

tim mạch nói chung thì các cái biện pháp và khuyến khích vẫn là nên tập thể dục thì tập thể dục thì một cái nguyên tắc

| Token | Nhãn gốc |
|---|---|
| tim | B-ORGAN |
| mạch | I-ORGAN |
| nói | 0 |
| chung | 0 |
| thì | 0 |
| các | 0 |
| cái | 0 |
| biện | 0 |
| pháp | 0 |
| và | 0 |
| khuyến | 0 |
| khích | 0 |
| vẫn | 0 |
| là | 0 |
| nên | 0 |
| tập | B-PERSONALCARE |
| thể | I-PERSONALCARE |
| dục | I-PERSONALCARE |
| thì | 0 |
| tập | B-PERSONALCARE |
| thể | I-PERSONALCARE |
| dục | I-PERSONALCARE |
| thì | 0 |
| một | 0 |
| cái | 0 |
| nguyên | 0 |
| tắc | 0 |

## VM600-560 — dòng train 4297 (đếm từ 0)

mình mong muốn đấy là cái điều quan trọng mà chương trình hôm nay chúng ta muốn nói đến để các quý vị chúng ta có

| Token | Nhãn gốc |
|---|---|
| mình | 0 |
| mong | 0 |
| muốn | 0 |
| đấy | 0 |
| là | 0 |
| cái | 0 |
| điều | 0 |
| quan | 0 |
| trọng | 0 |
| mà | 0 |
| chương | 0 |
| trình | 0 |
| hôm | B-DATETIME |
| nay | I-DATETIME |
| chúng | 0 |
| ta | 0 |
| muốn | 0 |
| nói | 0 |
| đến | 0 |
| để | 0 |
| các | 0 |
| quý | 0 |
| vị | 0 |
| chúng | 0 |
| ta | 0 |
| có | 0 |

## VM600-561 — dòng train 4306 (đếm từ 0)

cái việc chính của mình là mình phải tiêm vắcxin phòng bệnh này bằng cách 5k này và mình tiêm vắcxin chống covid

| Token | Nhãn gốc |
|---|---|
| cái | 0 |
| việc | 0 |
| chính | 0 |
| của | 0 |
| mình | 0 |
| là | 0 |
| mình | 0 |
| phải | 0 |
| tiêm | B-MEDDEVICETECHNIQUE |
| vắcxin | B-DRUGCHEMICAL |
| phòng | 0 |
| bệnh | 0 |
| này | 0 |
| bằng | 0 |
| cách | 0 |
| 5k | B-PREVENTIVEMED |
| này | 0 |
| và | 0 |
| mình | 0 |
| tiêm | B-MEDDEVICETECHNIQUE |
| vắcxin | B-DRUGCHEMICAL |
| chống | 0 |
| covid | B-DISEASESYMTOM |

## VM600-562 — dòng train 4312 (đếm từ 0)

người f1 này với nhau cũng làm sao để giảm các nguy cơ lây chéo bởi vì người

| Token | Nhãn gốc |
|---|---|
| người | 0 |
| f1 | 0 |
| này | 0 |
| với | 0 |
| nhau | 0 |
| cũng | 0 |
| làm | 0 |
| sao | 0 |
| để | 0 |
| giảm | 0 |
| các | 0 |
| nguy | B-PREVENTIVEMED |
| cơ | I-PREVENTIVEMED |
| lây | I-PREVENTIVEMED |
| chéo | I-PREVENTIVEMED |
| bởi | 0 |
| vì | 0 |
| người | 0 |

## VM600-563 — dòng train 4325 (đếm từ 0)

vâng những cái quan trọng nhất là chúng ta cần phải nắm vững được những cái nguyên tắc về dinh dưỡng và đồng thời là

| Token | Nhãn gốc |
|---|---|
| vâng | 0 |
| những | 0 |
| cái | 0 |
| quan | 0 |
| trọng | 0 |
| nhất | 0 |
| là | 0 |
| chúng | 0 |
| ta | 0 |
| cần | 0 |
| phải | 0 |
| nắm | 0 |
| vững | 0 |
| được | 0 |
| những | 0 |
| cái | 0 |
| nguyên | 0 |
| tắc | 0 |
| về | 0 |
| dinh | 0 |
| dưỡng | 0 |
| và | 0 |
| đồng | 0 |
| thời | 0 |
| là | 0 |

## VM600-564 — dòng train 4334 (đếm từ 0)

ưu tiên đầu tiên đó là chúng ta phải điều trị mụn ẩn rồi tuy nhiên là có một số bạn là bị mụn ẩn nhưng mà có

| Token | Nhãn gốc |
|---|---|
| ưu | 0 |
| tiên | 0 |
| đầu | 0 |
| tiên | 0 |
| đó | 0 |
| là | 0 |
| chúng | 0 |
| ta | 0 |
| phải | 0 |
| điều | B-TREATMENT |
| trị | I-TREATMENT |
| mụn | I-TREATMENT |
| ẩn | I-TREATMENT |
| rồi | 0 |
| tuy | 0 |
| nhiên | 0 |
| là | 0 |
| có | 0 |
| một | 0 |
| số | 0 |
| bạn | 0 |
| là | 0 |
| bị | 0 |
| mụn | B-DISEASESYMTOM |
| ẩn | I-DISEASESYMTOM |
| nhưng | 0 |
| mà | 0 |
| có | 0 |

## VM600-565 — dòng train 4335 (đếm từ 0)

thực vật nó quan trọng không chỉ ở chất đạm mà nó còn quan trọng ở chất béo và nó còn quan trọng là cái

| Token | Nhãn gốc |
|---|---|
| thực | B-FOODDRINK |
| vật | I-FOODDRINK |
| nó | 0 |
| quan | 0 |
| trọng | 0 |
| không | 0 |
| chỉ | 0 |
| ở | 0 |
| chất | 0 |
| đạm | B-FOODDRINK |
| mà | 0 |
| nó | 0 |
| còn | 0 |
| quan | 0 |
| trọng | 0 |
| ở | 0 |
| chất | B-DRUGCHEMICAL |
| béo | I-DRUGCHEMICAL |
| và | 0 |
| nó | 0 |
| còn | 0 |
| quan | 0 |
| trọng | 0 |
| là | 0 |
| cái | 0 |

## VM600-566 — dòng train 4351 (đếm từ 0)

biết như vậy nhưng mà sau này khi mà y học hiện đại người ta mới phân tích thì người ta thấy rằng là à cái đuôi có tắc

| Token | Nhãn gốc |
|---|---|
| biết | 0 |
| như | 0 |
| vậy | 0 |
| nhưng | 0 |
| mà | 0 |
| sau | 0 |
| này | 0 |
| khi | 0 |
| mà | 0 |
| y | 0 |
| học | 0 |
| hiện | 0 |
| đại | 0 |
| người | 0 |
| ta | 0 |
| mới | 0 |
| phân | B-MEDDEVICETECHNIQUE |
| tích | I-MEDDEVICETECHNIQUE |
| thì | 0 |
| người | 0 |
| ta | 0 |
| thấy | 0 |
| rằng | 0 |
| là | 0 |
| à | 0 |
| cái | 0 |
| đuôi | 0 |
| có | 0 |
| tắc | 0 |

## VM600-567 — dòng train 4354 (đếm từ 0)

là nhiều người bị ung thư bị gầy đi hẳn hoi nhưng cứ bảo là chúng ta bỏ đói tế

| Token | Nhãn gốc |
|---|---|
| là | 0 |
| nhiều | 0 |
| người | 0 |
| bị | 0 |
| ung | B-DISEASESYMTOM |
| thư | I-DISEASESYMTOM |
| bị | 0 |
| gầy | 0 |
| đi | 0 |
| hẳn | 0 |
| hoi | 0 |
| nhưng | 0 |
| cứ | 0 |
| bảo | 0 |
| là | 0 |
| chúng | 0 |
| ta | 0 |
| bỏ | 0 |
| đói | 0 |
| tế | 0 |

## VM600-568 — dòng train 4366 (đếm từ 0)

vâng ạ tôi thì thấy thực tế là khi mà chúng ta nhận một cái khẩu phần vào và rất

| Token | Nhãn gốc |
|---|---|
| vâng | 0 |
| ạ | 0 |
| tôi | 0 |
| thì | 0 |
| thấy | 0 |
| thực | 0 |
| tế | 0 |
| là | 0 |
| khi | 0 |
| mà | 0 |
| chúng | 0 |
| ta | 0 |
| nhận | 0 |
| một | 0 |
| cái | 0 |
| khẩu | 0 |
| phần | 0 |
| vào | 0 |
| và | 0 |
| rất | 0 |

## VM600-569 — dòng train 4376 (đếm từ 0)

lại càng cần phải tiêm bác ạ tại vì là khi mà chúng ta không tiêm ấy mà khi mắc bệnh là bệnh sẽ rất rất nặng thế và

| Token | Nhãn gốc |
|---|---|
| lại | 0 |
| càng | 0 |
| cần | 0 |
| phải | 0 |
| tiêm | B-MEDDEVICETECHNIQUE |
| bác | B-AGE |
| ạ | 0 |
| tại | 0 |
| vì | 0 |
| là | 0 |
| khi | 0 |
| mà | 0 |
| chúng | 0 |
| ta | 0 |
| không | 0 |
| tiêm | B-MEDDEVICETECHNIQUE |
| ấy | 0 |
| mà | 0 |
| khi | 0 |
| mắc | B-DISEASESYMTOM |
| bệnh | I-DISEASESYMTOM |
| là | 0 |
| bệnh | 0 |
| sẽ | 0 |
| rất | 0 |
| rất | 0 |
| nặng | 0 |
| thế | 0 |
| và | 0 |

## VM600-570 — dòng train 4378 (đếm từ 0)

được tự ý bỏ đâu vì là những cái cái thức cái huyết áp này là cái việc điều

| Token | Nhãn gốc |
|---|---|
| được | 0 |
| tự | 0 |
| ý | 0 |
| bỏ | 0 |
| đâu | 0 |
| vì | 0 |
| là | 0 |
| những | 0 |
| cái | 0 |
| cái | 0 |
| thức | 0 |
| cái | 0 |
| huyết | B-DISEASESYMTOM |
| áp | I-DISEASESYMTOM |
| này | 0 |
| là | 0 |
| cái | 0 |
| việc | 0 |
| điều | 0 |

## VM600-571 — dòng train 4381 (đếm từ 0)

màng xơ vữa nên là nó sẽ có tác dụng lâu dài nên các quý vị khi sử dụng để mang lại cho hiệu quả cao nhất thì chúng

| Token | Nhãn gốc |
|---|---|
| màng | 0 |
| xơ | B-DISEASESYMTOM |
| vữa | I-DISEASESYMTOM |
| nên | 0 |
| là | 0 |
| nó | 0 |
| sẽ | 0 |
| có | 0 |
| tác | 0 |
| dụng | 0 |
| lâu | 0 |
| dài | 0 |
| nên | 0 |
| các | 0 |
| quý | 0 |
| vị | 0 |
| khi | 0 |
| sử | 0 |
| dụng | 0 |
| để | 0 |
| mang | 0 |
| lại | 0 |
| cho | 0 |
| hiệu | B-UNITCALIBRATOR |
| quả | I-UNITCALIBRATOR |
| cao | I-UNITCALIBRATOR |
| nhất | I-UNITCALIBRATOR |
| thì | 0 |
| chúng | 0 |

## VM600-572 — dòng train 4398 (đếm từ 0)

trong đó thì là có cái chẩn đoán cho chị là kiểu thiếu máu cơ tim vâng đây nó chính là những cái tình trạng là thiếu máu của

| Token | Nhãn gốc |
|---|---|
| trong | 0 |
| đó | 0 |
| thì | 0 |
| là | 0 |
| có | 0 |
| cái | 0 |
| chẩn | B-DIAGNOSTICS |
| đoán | I-DIAGNOSTICS |
| cho | 0 |
| chị | B-GENDER |
| là | 0 |
| kiểu | 0 |
| thiếu | B-DISEASESYMTOM |
| máu | I-DISEASESYMTOM |
| cơ | B-ORGAN |
| tim | B-ORGAN |
| vâng | 0 |
| đây | 0 |
| nó | 0 |
| chính | 0 |
| là | 0 |
| những | 0 |
| cái | 0 |
| tình | 0 |
| trạng | 0 |
| là | 0 |
| thiếu | B-DISEASESYMTOM |
| máu | I-DISEASESYMTOM |
| của | 0 |

## VM600-573 — dòng train 4427 (đếm từ 0)

nhưng sự thay đổi trong môi trường ruột ví dụ do lạm dụng một số loại kháng sinh có thể thúc đẩy sẽ phát triển quá mức

| Token | Nhãn gốc |
|---|---|
| nhưng | 0 |
| sự | 0 |
| thay | 0 |
| đổi | 0 |
| trong | 0 |
| môi | 0 |
| trường | 0 |
| ruột | B-ORGAN |
| ví | 0 |
| dụ | 0 |
| do | 0 |
| lạm | 0 |
| dụng | 0 |
| một | 0 |
| số | 0 |
| loại | 0 |
| kháng | B-DRUGCHEMICAL |
| sinh | I-DRUGCHEMICAL |
| có | 0 |
| thể | 0 |
| thúc | 0 |
| đẩy | 0 |
| sẽ | 0 |
| phát | 0 |
| triển | 0 |
| quá | 0 |
| mức | 0 |

## VM600-574 — dòng train 4453 (đếm từ 0)

hướng dẫn cái phẫu thuật viên để đưa cái điện cực vào và khi mình đưa xuống

| Token | Nhãn gốc |
|---|---|
| hướng | 0 |
| dẫn | 0 |
| cái | 0 |
| phẫu | B-SURGERY |
| thuật | I-SURGERY |
| viên | 0 |
| để | 0 |
| đưa | 0 |
| cái | 0 |
| điện | B-MEDDEVICETECHNIQUE |
| cực | I-MEDDEVICETECHNIQUE |
| vào | 0 |
| và | 0 |
| khi | 0 |
| mình | 0 |
| đưa | 0 |
| xuống | 0 |

## VM600-575 — dòng train 4461 (đếm từ 0)

thiện triệu chứng run rất là tốt chúng ta biết rằng là run là một trong những cái đặc tính chính của bệnh parkinson

| Token | Nhãn gốc |
|---|---|
| thiện | 0 |
| triệu | B-DISEASESYMTOM |
| chứng | I-DISEASESYMTOM |
| run | I-DISEASESYMTOM |
| rất | 0 |
| là | 0 |
| tốt | 0 |
| chúng | 0 |
| ta | 0 |
| biết | 0 |
| rằng | 0 |
| là | 0 |
| run | B-DISEASESYMTOM |
| là | 0 |
| một | 0 |
| trong | 0 |
| những | 0 |
| cái | 0 |
| đặc | 0 |
| tính | 0 |
| chính | 0 |
| của | 0 |
| bệnh | 0 |
| parkinson | B-DISEASESYMTOM |

## VM600-576 — dòng train 4463 (đếm từ 0)

thể nói là những người trung quốc những người ở nhật bản những người hàn quốc từ xa xưa người ta đã sử dụng cái này và

| Token | Nhãn gốc |
|---|---|
| thể | 0 |
| nói | 0 |
| là | 0 |
| những | 0 |
| người | 0 |
| trung | B-LOCATION |
| quốc | I-LOCATION |
| những | 0 |
| người | 0 |
| ở | 0 |
| nhật | B-LOCATION |
| bản | I-LOCATION |
| những | 0 |
| người | 0 |
| hàn | B-LOCATION |
| quốc | I-LOCATION |
| từ | 0 |
| xa | B-DATETIME |
| xưa | I-DATETIME |
| người | 0 |
| ta | 0 |
| đã | 0 |
| sử | 0 |
| dụng | 0 |
| cái | 0 |
| này | 0 |
| và | 0 |

## VM600-577 — dòng train 4466 (đếm từ 0)

làm thuốc thì cha ông chúng ta là lựa chọn những cái bộ phận mà nó có tác dụng

| Token | Nhãn gốc |
|---|---|
| làm | 0 |
| thuốc | B-DRUGCHEMICAL |
| thì | 0 |
| cha | B-GENDER |
| ông | I-GENDER |
| chúng | 0 |
| ta | 0 |
| là | 0 |
| lựa | 0 |
| chọn | 0 |
| những | 0 |
| cái | 0 |
| bộ | 0 |
| phận | 0 |
| mà | 0 |
| nó | 0 |
| có | 0 |
| tác | 0 |
| dụng | 0 |

## VM600-578 — dòng train 4472 (đếm từ 0)

chỉ phát hiện sự hiện diện của mầm bệnh mà còn có thể nhận ra loại mầm bệnh hiện diện và chỉ đạo đáp ứng miễn dịch phù

| Token | Nhãn gốc |
|---|---|
| chỉ | 0 |
| phát | 0 |
| hiện | 0 |
| sự | 0 |
| hiện | 0 |
| diện | 0 |
| của | 0 |
| mầm | B-DISEASESYMTOM |
| bệnh | I-DISEASESYMTOM |
| mà | 0 |
| còn | 0 |
| có | 0 |
| thể | 0 |
| nhận | 0 |
| ra | 0 |
| loại | 0 |
| mầm | B-DISEASESYMTOM |
| bệnh | I-DISEASESYMTOM |
| hiện | 0 |
| diện | 0 |
| và | 0 |
| chỉ | 0 |
| đạo | 0 |
| đáp | 0 |
| ứng | 0 |
| miễn | 0 |
| dịch | 0 |
| phù | 0 |

## VM600-579 — dòng train 4473 (đếm từ 0)

cái mà chúng ta khám trên lâm sàng thì đôi khi chúng ta chưa đủ để chuẩn đoán một da nhạy cảm chính xác thì chúng ta

| Token | Nhãn gốc |
|---|---|
| cái | 0 |
| mà | 0 |
| chúng | 0 |
| ta | 0 |
| khám | B-DIAGNOSTICS |
| trên | 0 |
| lâm | 0 |
| sàng | 0 |
| thì | 0 |
| đôi | 0 |
| khi | 0 |
| chúng | 0 |
| ta | 0 |
| chưa | 0 |
| đủ | 0 |
| để | 0 |
| chuẩn | B-DIAGNOSTICS |
| đoán | I-DIAGNOSTICS |
| một | 0 |
| da | B-DISEASESYMTOM |
| nhạy | I-DISEASESYMTOM |
| cảm | I-DISEASESYMTOM |
| chính | 0 |
| xác | 0 |
| thì | 0 |
| chúng | 0 |
| ta | 0 |

## VM600-580 — dòng train 4477 (đếm từ 0)

trình về sau của người bệnh là những cái thăm khám mà những cái xét nghiệm mà bệnh nhân phải

| Token | Nhãn gốc |
|---|---|
| trình | 0 |
| về | 0 |
| sau | 0 |
| của | 0 |
| người | 0 |
| bệnh | 0 |
| là | 0 |
| những | 0 |
| cái | 0 |
| thăm | B-TREATMENT |
| khám | I-TREATMENT |
| mà | 0 |
| những | 0 |
| cái | 0 |
| xét | B-DIAGNOSTICS |
| nghiệm | I-DIAGNOSTICS |
| mà | 0 |
| bệnh | B-OCCUPATION |
| nhân | I-OCCUPATION |
| phải | 0 |

## VM600-581 — dòng train 4478 (đếm từ 0)

là nguyên phát hay thứ phát bởi vì có một số trường hợp đó là da nhạy cảm nhưng mà bệnh nhân có các bệnh lý da

| Token | Nhãn gốc |
|---|---|
| là | 0 |
| nguyên | 0 |
| phát | 0 |
| hay | 0 |
| thứ | 0 |
| phát | 0 |
| bởi | 0 |
| vì | 0 |
| có | 0 |
| một | 0 |
| số | 0 |
| trường | 0 |
| hợp | 0 |
| đó | 0 |
| là | 0 |
| da | B-DISEASESYMTOM |
| nhạy | I-DISEASESYMTOM |
| cảm | I-DISEASESYMTOM |
| nhưng | 0 |
| mà | 0 |
| bệnh | B-OCCUPATION |
| nhân | I-OCCUPATION |
| có | 0 |
| các | 0 |
| bệnh | B-DISEASESYMTOM |
| lý | I-DISEASESYMTOM |
| da | I-DISEASESYMTOM |

## VM600-582 — dòng train 4482 (đếm từ 0)

trước đại dịch như thế này thì thực sự rất là nhiều thách thức nhưng thách thức ấy có vượt qua được hay không thì phần

| Token | Nhãn gốc |
|---|---|
| trước | 0 |
| đại | B-DISEASESYMTOM |
| dịch | I-DISEASESYMTOM |
| như | 0 |
| thế | 0 |
| này | 0 |
| thì | 0 |
| thực | 0 |
| sự | 0 |
| rất | 0 |
| là | 0 |
| nhiều | 0 |
| thách | 0 |
| thức | 0 |
| nhưng | 0 |
| thách | 0 |
| thức | 0 |
| ấy | 0 |
| có | 0 |
| vượt | 0 |
| qua | 0 |
| được | 0 |
| hay | 0 |
| không | 0 |
| thì | 0 |
| phần | 0 |

## VM600-583 — dòng train 4483 (đếm từ 0)

giúp ngăn ngừa các vấn đề trong ghép tạng cũng là kết quả của một đáp ứng miễn dịch không mong muốn trong trường

| Token | Nhãn gốc |
|---|---|
| giúp | 0 |
| ngăn | B-PREVENTIVEMED |
| ngừa | I-PREVENTIVEMED |
| các | 0 |
| vấn | 0 |
| đề | 0 |
| trong | 0 |
| ghép | B-SURGERY |
| tạng | I-SURGERY |
| cũng | 0 |
| là | 0 |
| kết | 0 |
| quả | 0 |
| của | 0 |
| một | 0 |
| đáp | 0 |
| ứng | 0 |
| miễn | 0 |
| dịch | 0 |
| không | 0 |
| mong | 0 |
| muốn | 0 |
| trong | 0 |
| trường | 0 |

## VM600-584 — dòng train 4491 (đếm từ 0)

oxy hóa gấp sáu mươi lần trước đây thế thì tuyệt vời và chính quay trở lại câu

| Token | Nhãn gốc |
|---|---|
| oxy | B-DRUGCHEMICAL |
| hóa | 0 |
| gấp | 0 |
| sáu | B-AGE |
| mươi | I-AGE |
| lần | 0 |
| trước | 0 |
| đây | 0 |
| thế | 0 |
| thì | 0 |
| tuyệt | 0 |
| vời | 0 |
| và | 0 |
| chính | 0 |
| quay | 0 |
| trở | 0 |
| lại | 0 |
| câu | 0 |

## VM600-585 — dòng train 4495 (đếm từ 0)

đường huyết cũng là thể trở nên rất là khó khăn và hơn so với lại những cái

| Token | Nhãn gốc |
|---|---|
| đường | 0 |
| huyết | B-ORGAN |
| cũng | 0 |
| là | 0 |
| thể | 0 |
| trở | 0 |
| nên | 0 |
| rất | 0 |
| là | 0 |
| khó | 0 |
| khăn | 0 |
| và | 0 |
| hơn | 0 |
| so | 0 |
| với | 0 |
| lại | 0 |
| những | 0 |
| cái | 0 |

## VM600-586 — dòng train 4497 (đếm từ 0)

loạn nhịp tim thì khi chúng ta sử dụng kết hợp cùng với viên nang đông trùng hạ thảo thì chúng ta nên uống cách nhau ra

| Token | Nhãn gốc |
|---|---|
| loạn | B-DISEASESYMTOM |
| nhịp | I-DISEASESYMTOM |
| tim | I-DISEASESYMTOM |
| thì | 0 |
| khi | 0 |
| chúng | 0 |
| ta | 0 |
| sử | 0 |
| dụng | 0 |
| kết | 0 |
| hợp | 0 |
| cùng | 0 |
| với | 0 |
| viên | B-DRUGCHEMICAL |
| nang | I-DRUGCHEMICAL |
| đông | I-DRUGCHEMICAL |
| trùng | I-DRUGCHEMICAL |
| hạ | I-DRUGCHEMICAL |
| thảo | I-DRUGCHEMICAL |
| thì | 0 |
| chúng | 0 |
| ta | 0 |
| nên | 0 |
| uống | 0 |
| cách | 0 |
| nhau | 0 |
| ra | 0 |

## VM600-587 — dòng train 4504 (đếm từ 0)

dần dần để chúng ta có thể tức là bằng lý trí để chúng ta có thể ăn được cả bên

| Token | Nhãn gốc |
|---|---|
| dần | 0 |
| dần | 0 |
| để | 0 |
| chúng | 0 |
| ta | 0 |
| có | 0 |
| thể | 0 |
| tức | 0 |
| là | 0 |
| bằng | 0 |
| lý | 0 |
| trí | 0 |
| để | 0 |
| chúng | 0 |
| ta | 0 |
| có | 0 |
| thể | 0 |
| ăn | 0 |
| được | 0 |
| cả | 0 |
| bên | 0 |

## VM600-588 — dòng train 4508 (đếm từ 0)

chúng ta đều bị xâm chiếm từng khoảnh khắc bởi các sinh vật có khả năng đe dọa tính mạng nếu không có hệ miễn dịch hoạt

| Token | Nhãn gốc |
|---|---|
| chúng | 0 |
| ta | 0 |
| đều | 0 |
| bị | 0 |
| xâm | 0 |
| chiếm | 0 |
| từng | 0 |
| khoảnh | 0 |
| khắc | 0 |
| bởi | 0 |
| các | 0 |
| sinh | 0 |
| vật | 0 |
| có | 0 |
| khả | 0 |
| năng | 0 |
| đe | 0 |
| dọa | 0 |
| tính | 0 |
| mạng | 0 |
| nếu | 0 |
| không | 0 |
| có | 0 |
| hệ | B-ORGAN |
| miễn | I-ORGAN |
| dịch | I-ORGAN |
| hoạt | 0 |

## VM600-589 — dòng train 4511 (đếm từ 0)

chúng ta ngồi nhiều thứ hai nữa là chúng ta phải gần như là khi mà chúng ta làm việc với máy tính hoặc là các cái công

| Token | Nhãn gốc |
|---|---|
| chúng | 0 |
| ta | 0 |
| ngồi | 0 |
| nhiều | 0 |
| thứ | 0 |
| hai | 0 |
| nữa | 0 |
| là | 0 |
| chúng | 0 |
| ta | 0 |
| phải | 0 |
| gần | 0 |
| như | 0 |
| là | 0 |
| khi | 0 |
| mà | 0 |
| chúng | 0 |
| ta | 0 |
| làm | 0 |
| việc | 0 |
| với | 0 |
| máy | 0 |
| tính | 0 |
| hoặc | 0 |
| là | 0 |
| các | 0 |
| cái | 0 |
| công | 0 |

## VM600-590 — dòng train 4528 (đếm từ 0)

cái thứ hai là cái dinh dưỡng ở sau ung thư nó còn có vai trò vô cùng quan trọng đó

| Token | Nhãn gốc |
|---|---|
| cái | B-UNITCALIBRATOR |
| thứ | I-UNITCALIBRATOR |
| hai | I-UNITCALIBRATOR |
| là | 0 |
| cái | 0 |
| dinh | 0 |
| dưỡng | 0 |
| ở | 0 |
| sau | 0 |
| ung | B-DISEASESYMTOM |
| thư | I-DISEASESYMTOM |
| nó | 0 |
| còn | 0 |
| có | 0 |
| vai | 0 |
| trò | 0 |
| vô | 0 |
| cùng | 0 |
| quan | 0 |
| trọng | 0 |
| đó | 0 |

## VM600-591 — dòng train 4532 (đếm từ 0)

trộn không cần phải đun để chúng ta có thể trộn vào để chúng ta ăn thì chúng

| Token | Nhãn gốc |
|---|---|
| trộn | 0 |
| không | 0 |
| cần | 0 |
| phải | 0 |
| đun | 0 |
| để | 0 |
| chúng | 0 |
| ta | 0 |
| có | 0 |
| thể | 0 |
| trộn | 0 |
| vào | 0 |
| để | 0 |
| chúng | 0 |
| ta | 0 |
| ăn | 0 |
| thì | 0 |
| chúng | 0 |

## VM600-592 — dòng train 4547 (đếm từ 0)

tốt cho sức khỏe của chúng ta nữa cho nên là nếu những ai bị huyết áp những ai bị đái tháo đường những ai bị các bệnh

| Token | Nhãn gốc |
|---|---|
| tốt | 0 |
| cho | 0 |
| sức | 0 |
| khỏe | 0 |
| của | 0 |
| chúng | 0 |
| ta | 0 |
| nữa | 0 |
| cho | 0 |
| nên | 0 |
| là | 0 |
| nếu | 0 |
| những | 0 |
| ai | 0 |
| bị | 0 |
| huyết | B-DISEASESYMTOM |
| áp | I-DISEASESYMTOM |
| những | 0 |
| ai | 0 |
| bị | 0 |
| đái | B-DISEASESYMTOM |
| tháo | I-DISEASESYMTOM |
| đường | I-DISEASESYMTOM |
| những | 0 |
| ai | 0 |
| bị | 0 |
| các | 0 |
| bệnh | 0 |

## VM600-593 — dòng train 4557 (đếm từ 0)

có thể đi làm lại được xin mời bác sĩ thường thì giai đoạn hậu phẫu của phẫu

| Token | Nhãn gốc |
|---|---|
| có | 0 |
| thể | 0 |
| đi | 0 |
| làm | 0 |
| lại | 0 |
| được | 0 |
| xin | 0 |
| mời | 0 |
| bác | B-OCCUPATION |
| sĩ | I-OCCUPATION |
| thường | 0 |
| thì | 0 |
| giai | 0 |
| đoạn | 0 |
| hậu | B-SURGERY |
| phẫu | I-SURGERY |
| của | 0 |
| phẫu | 0 |

## VM600-594 — dòng train 4558 (đếm từ 0)

đối với lại cái cuộc sống họ cũng cảm thấy là họ bị mặc cảm về cái giá trị của chính mình họ cảm thấy là họ sống

| Token | Nhãn gốc |
|---|---|
| đối | 0 |
| với | 0 |
| lại | 0 |
| cái | 0 |
| cuộc | 0 |
| sống | 0 |
| họ | 0 |
| cũng | 0 |
| cảm | 0 |
| thấy | 0 |
| là | 0 |
| họ | 0 |
| bị | 0 |
| mặc | B-DISEASESYMTOM |
| cảm | I-DISEASESYMTOM |
| về | 0 |
| cái | 0 |
| giá | 0 |
| trị | 0 |
| của | 0 |
| chính | 0 |
| mình | 0 |
| họ | 0 |
| cảm | 0 |
| thấy | 0 |
| là | 0 |
| họ | 0 |
| sống | 0 |

## VM600-595 — dòng train 4561 (đếm từ 0)

chiều cái vị giác của bản thân cái người bị ung thư đó của của ví dụ như

| Token | Nhãn gốc |
|---|---|
| chiều | 0 |
| cái | 0 |
| vị | 0 |
| giác | 0 |
| của | 0 |
| bản | 0 |
| thân | 0 |
| cái | 0 |
| người | 0 |
| bị | 0 |
| ung | B-DISEASESYMTOM |
| thư | I-DISEASESYMTOM |
| đó | 0 |
| của | 0 |
| của | 0 |
| ví | 0 |
| dụ | 0 |
| như | 0 |

## VM600-596 — dòng train 4565 (đếm từ 0)

hơn thì đối với những trường hợp này chúng ta phải coi lại coi là chúng ta đã dưỡng ẩm đủ chưa thì đã xin chia sẻ

| Token | Nhãn gốc |
|---|---|
| hơn | 0 |
| thì | 0 |
| đối | 0 |
| với | 0 |
| những | 0 |
| trường | 0 |
| hợp | 0 |
| này | 0 |
| chúng | 0 |
| ta | 0 |
| phải | 0 |
| coi | 0 |
| lại | 0 |
| coi | 0 |
| là | 0 |
| chúng | 0 |
| ta | 0 |
| đã | 0 |
| dưỡng | B-PERSONALCARE |
| ẩm | I-PERSONALCARE |
| đủ | 0 |
| chưa | 0 |
| thì | 0 |
| đã | 0 |
| xin | 0 |
| chia | 0 |
| sẻ | 0 |

## VM600-597 — dòng train 4583 (đếm từ 0)

là chúng tôi hiểu hơn rằng là bác khó nắm chứ không phải là không nắm được đúng không ạ

| Token | Nhãn gốc |
|---|---|
| là | 0 |
| chúng | 0 |
| tôi | 0 |
| hiểu | 0 |
| hơn | 0 |
| rằng | 0 |
| là | 0 |
| bác | B-AGE |
| khó | 0 |
| nắm | 0 |
| chứ | 0 |
| không | 0 |
| phải | 0 |
| là | 0 |
| không | 0 |
| nắm | 0 |
| được | 0 |
| đúng | 0 |
| không | 0 |
| ạ | 0 |

## VM600-598 — dòng train 4593 (đếm từ 0)

các chất dinh dưỡng để giúp cho chúng ta bớt đi những cái vấn đề như là về thay

| Token | Nhãn gốc |
|---|---|
| các | 0 |
| chất | B-DRUGCHEMICAL |
| dinh | I-DRUGCHEMICAL |
| dưỡng | I-DRUGCHEMICAL |
| để | 0 |
| giúp | 0 |
| cho | 0 |
| chúng | 0 |
| ta | 0 |
| bớt | 0 |
| đi | 0 |
| những | 0 |
| cái | 0 |
| vấn | 0 |
| đề | 0 |
| như | 0 |
| là | 0 |
| về | 0 |
| thay | 0 |

## VM600-599 — dòng train 4594 (đếm từ 0)

nó cũng là tâm tư của rất rất nhiều những người có tuổi và những người cao tuổi mà khi chúng ta bị các bệnh lý

| Token | Nhãn gốc |
|---|---|
| nó | 0 |
| cũng | 0 |
| là | 0 |
| tâm | 0 |
| tư | 0 |
| của | 0 |
| rất | 0 |
| rất | B-UNITCALIBRATOR |
| nhiều | I-UNITCALIBRATOR |
| những | 0 |
| người | B-AGE |
| có | I-AGE |
| tuổi | I-AGE |
| và | 0 |
| những | 0 |
| người | 0 |
| cao | B-AGE |
| tuổi | I-AGE |
| mà | 0 |
| khi | 0 |
| chúng | 0 |
| ta | 0 |
| bị | 0 |
| các | 0 |
| bệnh | 0 |
| lý | 0 |

## VM600-600 — dòng train 4597 (đếm từ 0)

và từ đó nó cũng phòng ngừa được các cái biến chứng như là các cái nhồi máu cơ tim hay là những cái kiểu những cái nhồi

| Token | Nhãn gốc |
|---|---|
| và | 0 |
| từ | 0 |
| đó | 0 |
| nó | 0 |
| cũng | 0 |
| phòng | B-PREVENTIVEMED |
| ngừa | I-PREVENTIVEMED |
| được | 0 |
| các | 0 |
| cái | 0 |
| biến | B-DISEASESYMTOM |
| chứng | I-DISEASESYMTOM |
| như | 0 |
| là | 0 |
| các | 0 |
| cái | 0 |
| nhồi | B-DISEASESYMTOM |
| máu | I-DISEASESYMTOM |
| cơ | I-DISEASESYMTOM |
| tim | I-DISEASESYMTOM |
| hay | 0 |
| là | 0 |
| những | 0 |
| cái | 0 |
| kiểu | 0 |
| những | 0 |
| cái | 0 |
| nhồi | 0 |

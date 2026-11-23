# Xem nhanh pattern_v1 (mẫu ngẫu nhiên)

| ID | Cách sinh | Câu | Cặp |
|---|---|---|---|
| SP-00027 | mention_replacement | quá thì khả năng mổ nó sẽ khó khăn nó có sẽ có nhiều biến chứng cái thứ hai người bệnh parkinson nên là hơn | biến chứng → mổ: NO_RELATION |
| SP-00103 | mention_replacement | da chúng ta là mụn hoàn toàn luôn ra từ nâu hoặc là màu vàng chuyển sang màu trắng luôn ngoài ra còn có thể | mụn → da: located_at |
| SP-00109 | mention_replacement | động mạch thì mình vẫn hoàn toàn có thể sử dụng sớm để ngăn ngừa cái tình trạng tiêu chảy nó có thể xuất hiện rất | tiêu chảy → động mạch: NO_RELATION |
| SP-00123 | mention_replacement | một cái hóa trị hoặc xạ trị thì nó đều liên quan đến khử độc tại phổi và khi chức năng gan bị giảm như vậy thì nay lại bị | chức năng gan bị giảm → hóa trị: NO_RELATION; chức năng gan bị giảm → xạ trị: NO_RELATION; chức năng gan bị giảm → phổi: NO_RELATION |
| SP-00131 | mention_replacement | tích che phủ họng trên bề mặt da của bạn do đó nên bạn sẽ thấy là da của bạn ngủ dậy rất là nặng mặc đổ dầu nhiều | đổ dầu → họng: NO_RELATION |
| SP-00357 | mention_replacement | phải phát hiện virus do đó cái việc mà nghiệm pháp kích thích cũng không hẳn khẳng định là chúng ta là người mắc bệnh hay không mắc | virus → nghiệm pháp kích thích: NO_RELATION |
| SP-00384 | mention_replacement | nghĩ đến những cái nguy cơ do những cái mảng xơ vữa nó làm cho chúng ta giảm cái cái trao đổi chất giữa họng với cả với | mảng xơ vữa → trao đổi chất: NO_RELATION; mảng xơ vữa → họng: NO_RELATION |
| SP-00420 | mention_replacement | ta cũng đang triển khai cho nên rất là tốt ngoài ra nữa đông trùng hạ thảo còn có hạ huyết áp hạ nghẽn mạch máu rồi là đặc biệt | huyết áp → triển khai: NO_RELATION; nghẽn mạch máu → triển khai: NO_RELATION |
| SP-00457 | mention_replacement | lại nhận cung cấp máu nuôi dưỡng ở là từ ở cái động mạch vành nên khi mà cái động mạch vành của chúng ta nó bị thiểu năng vành thì | thiểu năng vành → máu: NO_RELATION; thiểu năng vành → nuôi dưỡng: NO_RELATION; thiểu năng vành → động mạch: NO_RELATION; thiểu năng vành → động mạch: located_at |
| SP-00572 | mention_replacement | iod thì chúng ta cũng rất cần lưu tâm đặc biệt là đối với bệnh cường giáp tuyến giáp là chúng ta cần phải tránh là chúng | cường giáp → iod: NO_RELATION; cường giáp → lưu tâm: NO_RELATION; cường giáp → tuyến giáp: located_at |
| SP-00654 | hard_negative | ví dụ như suy tim thì không cần phải làm siêu âm tim thì | suy tim → siêu âm tim: NO_RELATION |
| SP-00815 | hard_negative | trường hợp mà viêm da thì không chẩn đoán bằng nghiệm pháp kích thích được | viêm da → nghiệm pháp kích thích: NO_RELATION |
| SP-00896 | hard_negative | chúng ta thấy là nám thì không chẩn đoán bằng soi da được trong thời gian dài | nám → soi da: NO_RELATION |
| SP-00903 | hard_negative | đau bụng thì không cần phải làm siêu âm bụng nhé | đau bụng → siêu âm bụng: NO_RELATION |
| SP-00915 | hard_negative | thực ra thì chụp ct để phát hiện run tay chứ không phát hiện được chóng mặt thì | run tay → chụp ct: diagnosed_by; chóng mặt → chụp ct: NO_RELATION |
| SP-00953 | hard_negative | xin thưa với các bạn là nội soi dạ dày không phát hiện được viêm loét đó | viêm loét → nội soi dạ dày: NO_RELATION |
| SP-01004 | hard_negative | xơ vữa động mạch thì không cần phải làm chụp mạch vành rồi | xơ vữa động mạch → chụp mạch vành: NO_RELATION |
| SP-01127 | hard_negative | chúng ta thấy là viêm da thì không chẩn đoán bằng nghiệm pháp kích thích được | viêm da → nghiệm pháp kích thích: NO_RELATION |
| SP-01140 | hard_negative | các bạn thấy là bệnh gút thì không cần phải làm đo mật độ xương là rất quan trọng | bệnh gút → đo mật độ xương: NO_RELATION |
| SP-01765 | hard_negative | trường hợp mà mỡ máu thì không ảnh hưởng tới máu thì phải hỏi ý kiến bác sĩ | mỡ máu → máu: NO_RELATION |
| SP-01775 | hard_negative | các bạn thấy là nhức mỏi chứ không phải ở đầu gối thì rất là tốt | nhức mỏi → đầu gối: NO_RELATION |
| SP-01778 | hard_negative | ví dụ như ung thư chứ không phải ở vú trong thời gian dài | ung thư → vú: NO_RELATION |
| SP-01886 | hard_negative | thì đau bụng không liên quan gì đến đại tràng | đau bụng → đại tràng: NO_RELATION |
| SP-02121 | hard_negative | thực ra thì dùng colchicin để phòng ngừa viêm khớp nhé | viêm khớp → colchicin: NO_RELATION |
| SP-02284 | hard_negative | bác sĩ cho biết là viêm khớp không cải thiện với corticoid | viêm khớp → corticoid: NO_RELATION |
| SP-02285 | hard_negative | khối u thì uống thuốc hóa trị còn ung thư thì không cần | khối u → thuốc hóa trị: treated_by; ung thư → thuốc hóa trị: NO_RELATION |
| SP-02350 | hard_negative | các bạn thấy là dùng thuốc hóa trị để phòng ngừa ung thư | ung thư → thuốc hóa trị: NO_RELATION |
| SP-02465 | hard_negative | người bệnh nhồi máu thì uống aspirin còn rung nhĩ thì không cần | nhồi máu → aspirin: treated_by; rung nhĩ → aspirin: NO_RELATION |
| SP-02470 | hard_negative | xuất huyết thì uống thuốc chống động kinh còn tê bì kiến bò thì không cần nhé | xuất huyết → thuốc chống động kinh: treated_by; tê bì kiến bò → thuốc chống động kinh: NO_RELATION |
| SP-02517 | hard_negative | bác sĩ cho biết là thoái hóa mà uống thuốc chống viêm cũng không đỡ trong thời gian dài | thoái hóa → thuốc chống viêm: NO_RELATION |
| SP-02693 | template | chúng ta thấy là thoát vị đĩa đệm thì bác sĩ cho dùng thuốc giảm đau trong thời gian dài | thoát vị đĩa đệm → thuốc giảm đau: treated_by |
| SP-02735 | hard_negative | thì sau khi vật lý trị liệu thì bị viêm khớp đó | viêm khớp → vật lý trị liệu: NO_RELATION |
| SP-02845 | hard_negative | cholesterol thì phải mổ còn cường giáp thì chỉ cần theo dõi thì phải hỏi ý kiến bác sĩ | cholesterol → mổ: treated_by_procedure; cường giáp → mổ: NO_RELATION |
| SP-02933 | hard_negative | phục hồi chức năng để dự phòng đột quỵ rồi | đột quỵ → phục hồi chức năng: NO_RELATION |
| SP-02946 | hard_negative | bệnh nhân cắt đốt để dự phòng tim đập nhanh trong thời gian dài | tim đập nhanh → cắt đốt: NO_RELATION |
| SP-03006 | hard_negative | bác sĩ cho biết là sau khi laser thì bị viêm da thì | viêm da → laser: NO_RELATION |
| SP-03090 | hard_negative | phẫu thuật thay khớp để dự phòng nhức mỏi thì | nhức mỏi → phẫu thuật thay khớp: NO_RELATION |
| SP-03107 | hard_negative | covid19 thì phải thở oxy còn viêm phổi thì chỉ cần theo dõi thì | covid19 → thở oxy: treated_by_procedure; viêm phổi → thở oxy: NO_RELATION |
| SP-03111 | hard_negative | mổ để dự phòng thoát vị đĩa đệm thì rất là tốt | thoát vị đĩa đệm → mổ: NO_RELATION |
| SP-03182 | hard_negative | động kinh không cải thiện sau khi điều trị gen thì rất là tốt | động kinh → điều trị gen: NO_RELATION |

"""(E) Augmentation nhẹ khi huấn luyện.  [KHUNG — chưa cài đặt]

Mỗi phép biến đổi được áp dụng theo một xác suất, trên từng mẫu, ngay lúc huấn luyện ở giai đoạn 1:
  - chèn từ đệm hoặc lặp từ kiểu lời nói ("thì", "là", "cái", "à");
  - xóa ngẫu nhiên token nằm NGOÀI đoạn giữa hai thực thể;
  - đổi trigger đồng nghĩa ("ở" ↔ "tại", "uống" ↔ "dùng"), chỉ khi không làm đổi nhãn.

Không động vào token của thực thể. Sau mỗi phép biến đổi phải tính lại offset và
gọi validate_entities.
"""


def augment(row, rng):
    raise NotImplementedError("augment.py: chưa cài đặt, xem docstring")

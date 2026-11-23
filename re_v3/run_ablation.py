"""Huấn luyện 2 giai đoạn và chạy ablation.  [KHUNG — chưa cài đặt]

Các biến thể (3 seed mỗi biến thể):
  - baseline: Model/vihealthbert-re-v1, chỉ dùng seed;
  - +B, +C, +D;
  - +B+C+D, huấn luyện 2 giai đoạn;
  - +B+C+D, trộn một lần có trọng số (gold 1,0 / silver 0,5 / synthetic 0,3).

Huấn luyện: tái dùng scripts/re_dataset/bert_re.py. Cần thêm vào script đó hai tùy chọn:
  - --stage1-data / --stage2-data;
  - --sample-weight.

Đánh giá: tái dùng scripts/re_dataset/eval_augmented.py
(paired bootstrap CI95, F1 theo từng quan hệ).

Quét kích thước: dữ liệu sinh bằng 1×, 3×, 5× số cặp thật.

Quy tắc quyết định giữ nguyên như lần trước: chỉ thay mô hình triển khai khi biến thể ∪ luật thắng
trên cả golden test lẫn random test, và CI ghép cặp không nằm hẳn dưới 0.
"""
import argparse

from . import config


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--out", default=str(config.OUTPUTS_DIR / "ablation_v1"))
    ap.add_argument("--seeds", type=int, nargs="+", default=[42, 43, 44])
    ap.parse_args()
    raise NotImplementedError("run_ablation.py: chưa cài đặt, xem docstring")


if __name__ == "__main__":
    main()

"""(C) Sinh dữ liệu bằng LLM theo pattern.  [KHUNG — chưa cài đặt]

Đầu vào: data/patterns/patterns.jsonl và các câu seed thật
Đầu ra:  data/synthetic/llm_v1.jsonl (annotation_status = SYNTHETIC_LLM)

Prompt gồm:
  - Định nghĩa quan hệ, lấy từ re_labels.json.
  - Quy ước gold v1, lấy từ data/re_gold_v1/manifest.json:
    thực thể chung chung, câu hỏi, phủ định, thực phẩm chức năng.
  - Một pattern và 3–5 câu seed.
  - Văn phong VietMed: chữ thường, không dấu câu, số viết bằng chữ, có từ đệm.
  - Yêu cầu sinh cả câu dương lẫn câu âm khó cho cùng cặp kiểu.
  - Đầu ra có thẻ [E1:CONDITION]…[/E1], parse bằng common.parse_tagged().

Đa dạng hóa: xoay vòng pattern, chủ đề và vai người nói. Mỗi pattern có hạn mức số câu.

Lượt 2: LLM gán nhãn lại độc lập, chỉ giữ câu mà hai lượt đồng ý.

Lưu prompt, model id và seed vào manifest để tái lập được.
"""
import argparse

from . import config


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--out", default=str(config.SYNTHETIC_DIR / "llm_v1.jsonl"))
    ap.add_argument("--per-pattern", type=int, default=5)
    ap.parse_args()
    raise NotImplementedError("synth_llm.py: chưa cài đặt, xem docstring")


if __name__ == "__main__":
    main()

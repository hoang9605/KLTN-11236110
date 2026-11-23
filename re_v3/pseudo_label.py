"""(D) Gán nhãn giả (silver) trên VietMed-NER train chưa có nhãn RE.  [KHUNG — chưa cài đặt]

Đầu ra: data/silver/silver_v1.jsonl (annotation_status = SILVER)

Cần làm:
  1. Lấy câu từ VietMed-NER split train, có ít nhất một cặp ứng viên đúng kiểu
     (relation_extraction.data.candidates).
  2. Loại các câu đã có trong seed và trong tập test. So bằng text_group.
  3. Cho cặp chạy qua luật (relation_extraction.rules) và Model/vihealthbert-re-v1.
  4. Chỉ giữ cặp mà hai bên đồng ý:
     - dương khi p >= SILVER_POS_MIN_PROB;
     - âm khi p <= SILVER_NEG_MAX_PROB.
  5. Ghi log phân bố theo lớp. Silver thiên về mẫu dễ, cần nêu rõ hạn chế này trong báo cáo.
"""
import argparse

from . import config


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--out", default=str(config.SILVER_DIR / "silver_v1.jsonl"))
    ap.parse_args()
    raise NotImplementedError("pseudo_label.py: chưa cài đặt, xem docstring")


if __name__ == "__main__":
    main()

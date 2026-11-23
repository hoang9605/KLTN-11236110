"""Cấu hình chung cho RE v3. Mọi script đọc đường dẫn và ngưỡng từ đây."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent

# Dữ liệu seed (đã có nhãn) dùng để khai thác pattern và làm giai đoạn 2.
SEED_FILES = [
    ROOT / "data" / "re_gold_v1" / "annotations_gold_v1.jsonl",
    ROOT / "data" / "re_ai_v2" / "annotations_ai_v2.jsonl",
]

# Tập test: chỉ dùng để kiểm tra rò rỉ và đánh giá, KHÔNG BAO GIỜ đưa vào huấn luyện.
TEST_FILES = [
    ROOT / "data" / "re_test_random_v1" / "annotations.jsonl",
    ROOT / "data" / "golden_test" / "v1" / "candidates.jsonl",   # cùng text với ai_labels*.jsonl
]

PATTERNS_DIR = HERE / "data" / "patterns"
SYNTHETIC_DIR = HERE / "data" / "synthetic"
SILVER_DIR = HERE / "data" / "silver"
FILTERED_DIR = HERE / "data" / "filtered"
OUTPUTS_DIR = HERE / "outputs"

SEED = 42

# (A) khai thác pattern
MAX_BETWEEN_WORDS = 6        # đoạn giữa dài hơn thì gom vào pattern <LONG>
CONTEXT_WORDS = 2            # số từ ngữ cảnh trái/phải giữ lại

# (B)(C) sinh dữ liệu
TARGET_POSITIVE_RATIO = (0.20, 0.25)
TARGET_POSITIVES_PER_RELATION = (150, 300)

# (D) silver
SILVER_POS_MIN_PROB = 0.90
SILVER_NEG_MAX_PROB = 0.05

# Bộ lọc
LEAK_NGRAM = 8               # loại câu có chung 8-gram với tập test
MAX_PER_SKELETON = 3         # tối đa số câu có cùng khung (thực thể thay bằng [KIỂU])
MANUAL_REVIEW_FRACTION = 0.10
SEED_PAIRS = 556             # số cặp seed (gold v1 + ai v2), dùng cho --scale

ANNOTATION_STATUSES = {"SYNTHETIC_PATTERN", "SYNTHETIC_LLM", "SILVER"}

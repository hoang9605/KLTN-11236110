"""Standalone test runner and evaluation reporter for Vietnamese Medical NER Pipeline.

Executes and reports on all test cases specified in the requirements:
  Case 1: Multiple consecutive entities
  Case 2: Punctuated text with punctuation interspersed between entities
  Case 3: DOSAGE expressions ('500mg', '2 viên/ngày', composite)
  Case 4: Empty string and whitespace-only text
  Case 5: Non-clinical text (zero entities)
  Case 6: Long clinical text exceeding model max length (sentence chunking)
"""
import json
import os
import sys
import time
from pathlib import Path

# Set environment variables for Windows OpenMP
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
os.environ["OMP_NUM_THREADS"] = "1"

# Add parent directory to path
PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT))

from ner import MedicalNERPipeline, TARGET_LABELS


class Tee:
    def __init__(self, filename):
        self.file = open(filename, "w", encoding="utf-8")
        self.stdout = sys.stdout

    def write(self, data):
        self.file.write(data)
        self.stdout.write(data)
        self.file.flush()

    def flush(self):
        self.file.flush()
        self.stdout.flush()

sys.stdout = Tee("test_run_output.txt")


def run_all_cases():
    print("=" * 80)
    print("INITIALIZING VIETNAMESE MEDICAL NER PIPELINE...")
    print("=" * 80)
    t0 = time.time()
    pipeline = MedicalNERPipeline(enable_console_logging=False)
    print(f"Pipeline initialized successfully in {time.time() - t0:.2f} seconds.\n")

    test_cases = [
        {
            "name": "Case 1: Consecutive Entities (Nhiều thực thể liền nhau)",
            "description": "Contiguous medical entities (CONDITION, BODY_PART, PROCEDURE)",
            "text": "Bệnh nhân đau dạ dày, viêm loét hành tá tràng, chỉ định nội soi dạ dày can thiệp.",
        },
        {
            "name": "Case 2: Punctuated Text (Dấu câu xen giữa thực thể)",
            "description": "Punctuation marks (:, ;, (), .) between entities without sticking",
            "text": "Chẩn đoán: Viêm gan B (mạn tính); điều trị: Tenofovir 300mg; xét nghiệm: ALT, AST.",
        },
        {
            "name": "Case 3: Dosage Patterns (Dạng '500mg' và '2 viên/ngày')",
            "description": "Rule-based dosage detection and structured breakdown",
            "text": "Bệnh nhân sốt cao, kê đơn Paracetamol 500mg 2 viên/ngày uống sau ăn.",
        },
        {
            "name": "Case 4a: Empty String (Chuỗi rỗng)",
            "description": "Empty string input -> entities: []",
            "text": "",
        },
        {
            "name": "Case 4b: Whitespace-only String (Chuỗi chỉ khoảng trắng)",
            "description": "Whitespace-only input -> entities: []",
            "text": "   \t  \n  \n   ",
        },
        {
            "name": "Case 5: Non-clinical Text (Không có thực thể y tế)",
            "description": "General conversational sentence -> entities: []",
            "text": "Hôm nay trời nhiều mây và có thể có mưa rào nhẹ vào buổi chiều tại khu vực nội thành.",
        },
        {
            "name": "Case 6: Long Medical Text (Vượt max_position_embeddings)",
            "description": "Multi-sentence medical discharge summary requiring sentence chunking",
            "text": (
                "Bệnh nhân nam 65 tuổi, tiền sử tăng huyết áp và đái tháo đường tuýp 2 đang điều trị đều. "
                "Cách nhập viện 3 ngày, bệnh nhân xuất hiện đau tức ngực trái âm ỉ, lan lên vai trái và hàm dưới. "
                "Khám lâm sàng ghi nhận huyết áp 150/90 mmHg, nhịp tim đều 85 lần/phút, không có ran ở phổi. "
                "Bác sĩ chỉ định làm điện tâm đồ và xét nghiệm men tim Troponin T định lượng. "
                "Kết quả điện tâm đồ ghi nhận đoạn ST chênh lên ở các chuyển đạo V1 đến V4, chẩn đoán nhồi máu cơ tim cấp. "
                "Bệnh nhân được xử trí cấp cứu: thở oxy qua gọng kính, dùng Aspirin 300mg nhai và Clopidogrel 300mg uống. "
                "Bệnh nhân được chuyển khoa Tim mạch can thiệp để chụp mạch vành và đặt stent động mạch vành. "
                "Sau can thiệp, bệnh nhân ổn định, tiếp tục dùng Atorvastatin 20mg 1 viên/ngày và Enoxaparin tiêm dưới da."
            ),
        },
    ]

    all_passed = True
    results_summary = []

    for idx, tc in enumerate(test_cases, 1):
        print("=" * 80)
        print(f"TEST {idx}: {tc['name']}")
        print(f"Description: {tc['description']}")
        print(f"Input Text: {tc['text']!r}")
        print("-" * 80)

        t_start = time.time()
        res = pipeline.predict(tc["text"])
        elapsed = time.time() - t_start

        span_errors = []
        for ent in res["entities"]:
            s, e = ent["start_char"], ent["end_char"]
            expected = res["text"][s:e]
            actual = ent["surface_text"]
            if expected != actual:
                span_errors.append(f"Span mismatch: text[{s}:{e}]={expected!r} != {actual!r}")

            lbl = ent["label"]
            if lbl not in TARGET_LABELS:
                span_errors.append(f"Invalid label outside target 6: {lbl}")

        print("Output Result:")
        print(json.dumps(res, ensure_ascii=False, indent=2))
        print(f"\nExecution Time: {elapsed * 1000:.1f} ms | Entities: {len(res['entities'])}")

        passed = len(span_errors) == 0
        if "Empty" in tc["name"] or "Whitespace" in tc["name"] or "Non-clinical" in tc["name"]:
            if len(res["entities"]) != 0:
                passed = False
                span_errors.append("Expected 0 entities for empty/non-clinical text")

        if passed:
            print("[STATUS: PASSED]")
        else:
            print(f"[STATUS: FAILED] Errors: {span_errors}")
            all_passed = False

        results_summary.append({
            "case": tc["name"],
            "status": "PASSED" if passed else "FAILED",
            "entities_count": len(res["entities"]),
            "elapsed_ms": round(elapsed * 1000, 1),
            "errors": span_errors
        })
        print()

    print("=" * 80)
    print("FINAL TEST SUMMARY:")
    print("=" * 80)
    for r in results_summary:
        print(f"[{r['status']}] {r['case']}: {r['entities_count']} entities ({r['elapsed_ms']} ms)")
    print(f"\nOVERALL RESULT: {'ALL TESTS PASSED' if all_passed else 'SOME TESTS FAILED'}")

    summary_path = PROJECT_ROOT / "test_report.json"
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(results_summary, f, ensure_ascii=False, indent=2)
    print(f"\nReport written to: {summary_path}")


if __name__ == "__main__":
    run_all_cases()


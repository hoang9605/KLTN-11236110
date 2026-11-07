"""Demo đầu–cuối: văn bản → NER → chuẩn hóa ICD-10/RxNorm → RE.

  python -X utf8 scripts/demo_e2e.py                       # chạy các câu mẫu
  python -X utf8 scripts/demo_e2e.py "câu của bạn" ...     # chạy câu tùy ý
  python -X utf8 scripts/demo_e2e.py -i                    # nhập câu liên tục (Enter trống để thoát)
"""
import json
import os
import sys
from pathlib import Path

os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("KMP_DUPLICATE_LIB_OK", "TRUE")
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from ner.pipeline import MedicalNERPipeline  # noqa: E402
from relation_extraction.model import RelationExtractor  # noqa: E402
from relation_extraction.pipeline import MedicalREPipeline  # noqa: E402

MODEL = ROOT / "outputs/re_gold_v1_baseline/seed42/model.joblib"
# Câu demo được chọn có chủ đích để minh họa từng chức năng (không phải tập đánh giá).
SAMPLES = [
    "Bệnh nhân đau ở vùng bụng, được điều trị bằng phẫu thuật.",
    "Khối u xuất hiện ở phổi, được điều trị bằng phẫu thuật.",
    "Người bệnh bị đau ở khớp vai, được điều trị bằng vật lý trị liệu.",
    "Người bệnh parkinson được điều trị bằng phẫu thuật kích thích não sâu.",
    "Bệnh nhân bị xơ vữa động mạch, được điều trị bằng phẫu thuật bắc cầu.",
    "Bệnh nhân tăng huyết áp, kê Aspirin 81mg mỗi ngày.",
    "Bệnh nhân bị đau đầu, uống Paracetamol 500mg 2 viên/ngày.",
    "Bác bị huyết áp cao và rối loạn mỡ máu.",
    "Bệnh nhân bị viêm phổi, sốt cao, ho nhiều.",
    "Bệnh nhân bị đái tháo đường, thỉnh thoảng đau đầu và táo bón.",
]


def show(result):
    print("\n" + "=" * 90)
    print("VĂN BẢN:", result["text"])
    ents = {e["id"]: e for e in result["entities"]}
    print("\nTHỰC THỂ:")
    if not ents:
        print("  (không có)")
    for e in result["entities"]:
        norm = e.get("normalized")
        code = f"{norm['ontology']} {norm['code']} – {norm['label_standard']} ({norm['match_method']})" if norm else "—"
        note = "  [bỏ qua khi tìm quan hệ: thực thể chung]" if e.get("re_excluded") else ""
        print(f"  {e['id']:<4}{e['label']:<11}{e['surface_text']!r:<28} conf={e['confidence']:.2f}  mã: {code}{note}")
    print("\nQUAN HỆ:")
    if not result["relations"]:
        print("  (không tìm thấy quan hệ)")
    for r in result["relations"]:
        print(f"  {ents[r['head']]['surface_text']}  --{r['label']}-->  {ents[r['tail']]['surface_text']}   (điểm {r['score']:.2f})")
    others = [c for c in result["relation_candidates"] if c["status"] == "unsupported"]
    for c in others:
        print(f"  (chưa hỗ trợ {c['allowed_relation']}: {ents[c['head']]['surface_text']} → {ents[c['tail']]['surface_text']})")


def main():
    print("Đang nạp mô hình NER, chuẩn hóa và RE...")
    pipe = MedicalREPipeline(RelationExtractor.load(MODEL), ner=MedicalNERPipeline(enable_normalization=True))
    args = sys.argv[1:]
    out = []
    if args == ["-i"]:
        while True:
            text = input("\nNhập câu (Enter để thoát): ").strip()
            if not text:
                break
            res = pipe.predict(text, normalize=True)
            show(res)
            out.append(res)
    else:
        for text in args or SAMPLES:
            res = pipe.predict(text, normalize=True)
            show(res)
            out.append(res)
    path = ROOT / "outputs/demo_e2e_output.json"
    path.write_text(json.dumps(out, ensure_ascii=False, indent=2, default=str), encoding="utf-8")
    print(f"\nĐã lưu JSON đầy đủ: {path}")


if __name__ == "__main__":
    main()

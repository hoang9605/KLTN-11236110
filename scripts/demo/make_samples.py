r"""Chạy toàn bộ pipeline (NER -> chuẩn hóa -> RE ViHealthBERT ∪ luật) trên vài câu mẫu và lưu kết quả
cho bản giao diện demo (web/samples.json). Giao diện đọc tệp này khi chưa có API chạy thật.

    .venv\Scripts\python.exe -X utf8 scripts/demo/make_samples.py
"""
import json
import os
import sys
import time
from pathlib import Path

os.environ.setdefault("KMP_DUPLICATE_LIB_OK", "TRUE")
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from knowledge_graph import HybridRelationExtractor  # noqa: E402
from ner.pipeline import MedicalNERPipeline  # noqa: E402
from relation_extraction.bert_model import load_extractor  # noqa: E402
from relation_extraction.pipeline import MedicalREPipeline  # noqa: E402

SENTENCES = [
    "Bệnh nhân tăng huyết áp, kê Aspirin 81mg mỗi ngày.",
    "Bệnh nhân đau ở vùng bụng, được điều trị bằng phẫu thuật.",
    "bác sĩ chỉ định chụp x quang phổi để chẩn đoán viêm phổi cho bé",
    "người bị đái tháo đường type 2 thường được dùng metformin 500mg hai lần mỗi ngày",
    "viêm khớp gối khiến bệnh nhân đau nhức ở đầu gối, bác sĩ cho tiêm corticoid",
]


def main():
    t0 = time.time()
    # fallback = mô hình đứng một mình (mô hình hỗ trợ cả năm quan hệ), giống web/app.py và scripts/build_kg.py
    pipe = MedicalREPipeline(HybridRelationExtractor(load_extractor(str(ROOT / "Model/vihealthbert-re-vietmed-validated")),
                                                     mode="fallback"),
                             ner=MedicalNERPipeline(enable_normalization=True))
    print(f"loaded in {time.time() - t0:.1f}s", flush=True)
    out = []
    for s in SENTENCES:
        t1 = time.time()
        r = pipe.predict(s, normalize=True)
        r["elapsed_ms"] = round(1000 * (time.time() - t1))
        out.append(r)
        print(f"{r['elapsed_ms']} ms | {len(r.get('entities', []))} entities | {len(r.get('relations', []))} relations | {s}", flush=True)
    dest = ROOT / "web/samples.json"
    dest.parent.mkdir(exist_ok=True)
    dest.write_text(json.dumps(out, ensure_ascii=False, indent=1, default=str), encoding="utf-8")
    print("written", dest)


if __name__ == "__main__":
    main()

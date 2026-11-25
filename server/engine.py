"""Nạp pipeline NER -> chuẩn hóa ICD-10/RxNorm -> RE ở luồng nền và phục vụ suy luận tuần tự."""
import json
import math
import os
import threading
import time

os.environ.setdefault("KMP_DUPLICATE_LIB_OK", "TRUE")


def build_pipeline(settings):
    from knowledge_graph import HybridRelationExtractor
    from ner.pipeline import MedicalNERPipeline
    from relation_extraction.bert_model import load_extractor
    from relation_extraction.pipeline import MedicalREPipeline
    if settings.device == "cpu" or settings.device is None:
        import torch
        torch.set_num_threads(int(os.environ.get("TORCH_THREADS", os.cpu_count() or 1)))
    # fallback: luật chỉ dùng cho quan hệ mô hình không hỗ trợ (mô hình hỗ trợ cả năm), như trong báo cáo
    extractor = HybridRelationExtractor(load_extractor(str(settings.re_path), device=settings.device), mode="fallback")
    ner = MedicalNERPipeline(model_path=str(settings.ner_path), device=settings.device, enable_normalization=True)
    return MedicalREPipeline(extractor, ner=ner)


def jsonable(obj):
    """numpy / NaN -> kiểu JSON chuẩn (để lưu JSONB và trả về API)."""
    data = json.loads(json.dumps(obj, ensure_ascii=False, default=lambda o: o.item() if hasattr(o, "item") else str(o)))

    def clean(x):
        if isinstance(x, float) and (math.isnan(x) or math.isinf(x)):
            return None
        if isinstance(x, dict):
            return {k: clean(v) for k, v in x.items()}
        if isinstance(x, list):
            return [clean(v) for v in x]
        return x
    return clean(data)


class Engine:
    def __init__(self, factory):
        self.factory = factory
        self.status, self.pipe, self.error, self.load_seconds = "loading", None, None, None
        self.lock = threading.Lock()  # pipeline không an toàn khi chạy song song
        self.requests = 0

    def load(self):
        t0 = time.time()
        try:
            self.pipe = self.factory()
            self.status = "ready"
        except Exception as e:  # thiếu trọng số, lỗi nạp...
            self.status, self.error = "error", f"{type(e).__name__}: {e}"
        self.load_seconds = round(time.time() - t0, 1)

    def start(self, background=True):
        if background:
            threading.Thread(target=self.load, daemon=True, name="model-loader").start()
        else:
            self.load()

    @property
    def ready(self):
        return self.status == "ready"

    def metadata(self):
        if not self.ready:
            return None
        ext = self.pipe.extractor
        return {"re": getattr(ext, "metadata", {}), "supported_relations": ext.supported_relations}

    def analyze(self, text, normalize=True):
        with self.lock:
            t0 = time.time()
            result = self.pipe.predict(text, normalize=normalize)
            elapsed = round(1000 * (time.time() - t0))
            self.requests += 1
        return jsonable(result), elapsed

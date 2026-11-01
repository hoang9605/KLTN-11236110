"""Adapter for the existing NER output; normalization is independent of RE."""
from .data import NEGATIVE


class MedicalREPipeline:
    def __init__(self, extractor, ner=None):
        self.extractor = extractor
        self.ner = ner

    def from_ner_result(self, result):
        entities = []
        for index, original in enumerate(result["entities"], start=1):
            entity = dict(original)
            entity.setdefault("id", f"E{index}")
            entity.setdefault("start", entity.get("start_char"))
            entity.setdefault("end", entity.get("end_char"))
            entity.setdefault("text", entity.get("surface_text", result["text"][entity["start"]:entity["end"]]))
            entities.append(entity)
        predictions = self.extractor.predict(result["text"], entities)
        return {**result, "entities": entities, "relation_candidates": predictions,
                "relations": [p for p in predictions if p["label"] not in (None, NEGATIVE)],
                "re_metadata": {"label_source": self.extractor.metadata.get("label_source", "unknown"),
                                "supported_relations": self.extractor.supported_relations,
                                "score_meaning": "uncalibrated positive probability conditional on allowed type and NO_RELATION"}}

    def predict(self, text, normalize=False):
        if self.ner is None:
            from ner.pipeline import MedicalNERPipeline
            self.ner = MedicalNERPipeline(enable_normalization=False)
        return self.from_ner_result(self.ner.predict(text, normalize=normalize))

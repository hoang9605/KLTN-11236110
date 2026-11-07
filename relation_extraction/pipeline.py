"""Adapter for the existing NER output; normalization is independent of RE."""
from .data import NEGATIVE, is_generic


class MedicalREPipeline:
    def __init__(self, extractor, ner=None, skip_generic=True):
        self.extractor = extractor
        self.ner = ner
        self.skip_generic = skip_generic

    def from_ner_result(self, result):
        entities = []
        for index, original in enumerate(result["entities"], start=1):
            entity = dict(original)
            entity.setdefault("id", f"E{index}")
            entity.setdefault("start", entity.get("start_char"))
            entity.setdefault("end", entity.get("end_char"))
            entity.setdefault("text", entity.get("surface_text", result["text"][entity["start"]:entity["end"]]))
            if self.skip_generic and is_generic(entity):
                entity["re_excluded"] = "generic_entity"
            entities.append(entity)
        re_entities = [e for e in entities if "re_excluded" not in e]
        predictions = self.extractor.predict(result["text"], re_entities)
        return {**result, "entities": entities, "relation_candidates": predictions,
                "relations": [p for p in predictions if p["label"] not in (None, NEGATIVE)],
                "re_metadata": {"label_source": self.extractor.metadata.get("label_source", "unknown"),
                                "generic_entities_skipped": [e["id"] for e in entities if "re_excluded" in e],
                                "supported_relations": self.extractor.supported_relations,
                                "score_meaning": "uncalibrated positive probability conditional on allowed type and NO_RELATION"}}

    def predict(self, text, normalize=False):
        if self.ner is None:
            from ner.pipeline import MedicalNERPipeline
            self.ner = MedicalNERPipeline(enable_normalization=False)
        return self.from_ner_result(self.ner.predict(text, normalize=normalize))

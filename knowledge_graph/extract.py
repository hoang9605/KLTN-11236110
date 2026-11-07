"""Relation extraction for graph building: the learned model combined with the guideline
rule baseline (relation_extraction.rules).

mode="union" (default): a pair is positive when the model or the rules say so. Chosen by
5-fold grouped CV on RE gold v1 + AI v2 (positive micro-F1 0.48 vs 0.40 for the model or
the rules alone; scripts/re_dataset/train_eval.py, outputs/re_ai_v2/summary.md).
mode="fallback": the model for relations it supports, the rules only for the others.

Every prediction keeps a "source" field ("model" / "rule") so the graph can tell them apart.
"""
from relation_extraction.data import NEGATIVE
from relation_extraction.rules import RuleRelationExtractor

MODES = ("union", "fallback")


def _positive(p):
    return p.get("label") not in (None, NEGATIVE)


class HybridRelationExtractor:
    def __init__(self, model=None, rules=None, mode="union"):
        """model: a trained RelationExtractor, or None to use rules for every relation."""
        if mode not in MODES:
            raise ValueError(f"mode must be one of {MODES}, got {mode!r}")
        self.model = model
        self.rules = rules or RuleRelationExtractor()
        self.mode = mode
        model_rel = set(model.supported_relations) if model is not None else set()
        self.supported_relations = sorted(model_rel | set(self.rules.supported_relations))
        self.metadata = {
            "label_source": "hybrid", "mode": mode,
            "model_label_source": model.metadata.get("label_source", "unknown") if model is not None else None,
            "model_relations": sorted(model_rel),
            "rule_relations": sorted(set(self.rules.supported_relations) - model_rel),
        }

    def predict(self, text, entities):
        rule_preds = self.rules.predict(text, entities)
        if self.model is None:
            return [{**p, "source": "rule"} for p in rule_preds]
        by_pair = {(p["head"], p["tail"], p["allowed_relation"]): p for p in rule_preds}
        out = []
        for p in self.model.predict(text, entities):
            r = by_pair.get((p["head"], p["tail"], p["allowed_relation"]))
            use_rule = r is not None and (
                p["status"] == "unsupported" or (self.mode == "union" and not _positive(p) and _positive(r)))
            out.append({**r, "source": "rule"} if use_rule else {**p, "source": "model"})
        return out


def positive(predictions):
    return [p for p in predictions if _positive(p)]

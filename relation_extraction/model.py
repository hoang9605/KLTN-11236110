"""Small supervised RE baseline. Scores are uncalibrated conditional probabilities."""
from pathlib import Path

import joblib
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import precision_recall_fscore_support

from .data import RELATIONS, NEGATIVE, candidates


class RelationExtractor:
    def __init__(self, seed=42):
        self.seed = seed
        self.vectorizer = TfidfVectorizer(analyzer="char", ngram_range=(2, 5), sublinear_tf=True,
                                         max_features=50000)
        self.classifier = LogisticRegression(class_weight="balanced", max_iter=2000, random_state=seed)
        self.metadata = {}

    def fit(self, pairs):
        labels = [p["label"] for p in pairs]
        if NEGATIVE not in labels or len(set(labels)) < 2:
            raise ValueError("Training requires explicit negatives and at least one positive class")
        self.classifier.fit(self.vectorizer.fit_transform([p["features"] for p in pairs]), labels)
        self.supported_relations = sorted(set(labels) - {NEGATIVE})
        return self

    def predict_pairs(self, pairs):
        if not pairs:
            return []
        probabilities = self.classifier.predict_proba(self.vectorizer.transform([p["features"] for p in pairs]))
        classes = list(self.classifier.classes_)
        predictions = []
        for pair, probs in zip(pairs, probabilities):
            allowed = pair["allowed_relation"]
            if allowed not in self.supported_relations:
                predictions.append({"label": None, "score": None, "status": "unsupported"})
                continue
            positive, negative = probs[classes.index(allowed)], probs[classes.index(NEGATIVE)]
            score = float(positive / (positive + negative))
            predictions.append({"label": allowed if score >= 0.5 else NEGATIVE,
                                "score": score, "status": "predicted"})
        return predictions

    def predict(self, text, entities):
        pairs = candidates(text, entities)
        return [{"head": p["head"]["id"], "tail": p["tail"]["id"],
                 "allowed_relation": p["allowed_relation"], **result}
                for p, result in zip(pairs, self.predict_pairs(pairs))]

    def save(self, path):
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        joblib.dump(self, path)

    @classmethod
    def load(cls, path):
        """Load only locally produced/trusted joblib files (pickle executes code)."""
        model = joblib.load(path)
        if not isinstance(model, cls):
            raise ValueError("Not a RelationExtractor checkpoint")
        return model


def evaluate(gold, predicted):
    if len(gold) != len(predicted):
        raise ValueError("Gold/prediction lengths differ")
    predicted = [p if p is not None else "UNSUPPORTED" for p in predicted]
    labels = list(RELATIONS)
    p, r, f, supports = precision_recall_fscore_support(gold, predicted, labels=labels, zero_division=0)
    micro = precision_recall_fscore_support(gold, predicted, labels=labels, average="micro", zero_division=0)
    return {"positive_micro": dict(zip(("precision", "recall", "f1"), map(float, micro[:3]))),
            "positive_macro_f1_all_five": float(np.mean(f)),
            "per_relation": {label: {"precision": float(p[i]), "recall": float(r[i]),
                                     "f1": float(f[i]), "support": int(supports[i]),
                                     "has_evaluation_support": bool(supports[i])}
                             for i, label in enumerate(labels)},
            "pairs": len(gold), "negative_support": gold.count(NEGATIVE),
            "unsupported_predictions": predicted.count("UNSUPPORTED")}

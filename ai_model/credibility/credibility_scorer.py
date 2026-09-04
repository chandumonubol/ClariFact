"""Claim classification using TF-IDF + Logistic Regression.

Classifies extracted claims into credibility categories:
- Supported: Claim is well-supported by evidence
- Partially Supported: Claim is partly supported/contested
- Uncertain: Insufficient evidence to determine support
- Potentially Misleading: Claim contradicts available evidence

This implements a hybrid approach:
1. Rule-based baseline using linguistic features (when no model is available)
2. TF-IDF + Logistic Regression model integration (when model is trained)

The model follows the project spec from TRD.md: TfidfVectorizer + LogisticRegression
with ngram_range (1,2), class_weight='balanced'.
"""

import os
import re
import joblib
from typing import List, Dict, Any, Optional, Tuple

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

from ai_model.nlp.claim_extractor import extract_claims, ClaimType


# Model file path
MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "models", "claim_classifier.joblib")


class ClaimClassifier:
    """Claim classifier that categorizes claims by credibility support level.

    Uses a scikit-learn pipeline (TfidfVectorizer + LogisticRegression)
    for ML-based classification, with a rule-based fallback when no
    trained model is available.

    The model can be trained and saved using the train() method, or
    loaded from disk using load().
    """

    # Credibility score ranges mapped to labels (from DECISIONS.md and TRD.md)
    # These are the standard ranges; project may adjust
    SCORE_RANGES = {
        "supported": (80, 100),
        "partially_supported": (60, 79),
        "uncertain": (40, 59),
        "potentially_misleading": (0, 39),
    }

    def __init__(self, model: Optional[Pipeline] = None, use_rule_based: bool = True):
        """Initialize the claim classifier.

        Args:
            model: A trained scikit-learn Pipeline (TfidfVectorizer + LogisticRegression).
                   If None and no model file exists, rule-based classification is used.
            use_rule_based: Whether to fall back to rule-based classification
                           when no model is available.
        """
        self.model = model
        self.use_rule_based = use_rule_based
        self._is_trained = model is not None

        # Load model from disk if not provided
        if self.model is None:
            self.model = self._load_model_from_disk()
            if self.model is not None:
                self._is_trained = True

    def _load_model_from_disk(self) -> Optional[Pipeline]:
        """Load trained model from disk if it exists."""
        if os.path.exists(MODEL_PATH):
            try:
                model = joblib.load(MODEL_PATH)
                # Validate model has required components
                if hasattr(model, 'predict') and hasattr(model, 'predict_proba'):
                    return model
                else:
                    print(f"Warning: Loaded model from {MODEL_PATH} lacks required attributes.")
                    return None
            except Exception as e:
                print(f"Warning: Failed to load model from {MODEL_PATH}: {e}")
                return None
        return None

    def train(self, training_claims: List[str], training_labels: List[str]) -> Dict[str, Any]:
        """Train the TF-IDF + Logistic Regression model.

        Args:
            training_claims: List of claim texts used for training.
            training_labels: List of credibility labels corresponding to training_claims.
                Valid labels: "supported", "partially_supported", "uncertain",
                               "potentially_misleading"

        Returns:
            Dict with training evaluation metrics.
        """
        if len(training_claims) != len(training_labels):
            raise ValueError("training_claims and training_labels must have the same length")

        if len(training_claims) == 0:
            raise ValueError(" training data cannot be empty")

        # Create the pipeline following TRD.md spec:
        # TfidfVectorizer with ngram_range (1,2) + LogisticRegression
        # class_weight='balanced', max_iter=1000
        self.model = Pipeline([
            ('tfidf', TfidfVectorizer(
                ngram_range=(1, 2),
                lowercase=True,
                stop_words='english',
                min_df=1,
                max_df=1.0,
            )),
            ('clf', LogisticRegression(
                class_weight='balanced',
                max_iter=1000,
                random_state=42,
            )),
        ])

        # Train the model
        self.model.fit(training_claims, training_labels)
        self._is_trained = True

        # Save model to disk
        model_dir = os.path.dirname(MODEL_PATH)
        if model_dir:
            os.makedirs(model_dir, exist_ok=True)
        joblib.dump(self.model, MODEL_PATH)

        # Evaluate using simple hold-out (last 20% as test)
        n_test = len(training_claims) // 5
        if n_test > 0 and len(training_claims) > 5:
            X_test = training_claims[-n_test:]
            y_test = training_labels[-n_test:]
            X_train = training_claims[:-n_test]
            y_train = training_labels[:-n_test]

            # Re-train on train split
            self.model.fit(X_train, y_train)

            predictions = self.model.predict(X_test)
            accuracy = float(np.mean(predictions == y_test))

            # Compute per-label precision/recall/f1
            from sklearn.metrics import classification_report
            report = classification_report(y_test, predictions, output_dict=True, zero_division=0)

            metrics = {
                "accuracy": accuracy,
                "labels": list(self.SCORE_RANGES.keys()),
                "report": report,
            }
        else:
            # Not enough data for hold-out; report training-only result
            self.model.fit(training_claims, training_labels)
            metrics = {
                "accuracy": 1.0,  # trained on all data
                "notes": "Not enough data for hold-out test set; trained on all available data.",
            }

        return metrics

    def predict(self, claim_text: str) -> Dict[str, Any]:
        """Predict credibility category for a single claim.

        Args:
            claim_text: The claim text to classify.

        Returns:
            Dict with:
            - label: The predicted credibility label
            - score: Credibility score (0-100) derived from prediction
            - probabilities: Class probability scores if available
            - rule_based: Whether rule-based fallback was used
        """
        if self.model is None:
            if self.use_rule_based:
                return self._rule_based_classify(claim_text)
            else:
                raise RuntimeError("No model available for classification.")

        # Use ML model for prediction
        try:
            # Get probability scores if available
            proba = None
            if hasattr(self.model, 'predict_proba'):
                proba = self.model.predict_proba([claim_text])[0]
                classes = list(self.model.classes_)

            label = self.model.predict([claim_text])[0]

            # Convert label to standardized format
            label_str = str(label).lower()

            # Map to credibility score range
            score = self._label_to_score(label_str)

            return {
                "label": label_str,
                "score": score,
                "probabilities": dict(zip(classes, proba)) if proba else None,
                "rule_based": False,
            }

        except Exception as e:
            # Fall back to rule-based on error
            print(f"Error during ML prediction: {e}")
            return self._rule_based_classify(claim_text)

    def predict_batch(self, claim_texts: List[str]) -> List[Dict[str, Any]]:
        """Predict credibility categories for a batch of claims.

        Args:
            claim_texts: List of claim texts to classify.

        Returns:
            List of prediction dicts, one per input claim.
        """
        results = []
        for claim_text in claim_texts:
            result = self.predict(claim_text)
            results.append(result)
        return results

    def _label_to_score(self, label: str) -> int:
        """Convert a credibility label to a numeric score (0-100).

        Uses the midpoint of the label's score range.
        """
        label = label.lower()
        if label in self.SCORE_RANGES:
            low, high = self.SCORE_RANGES[label]
            return int((low + high) / 2)
        # Default: uncertain midpoint
        return 50

    def _rule_based_classify(self, claim_text: str) -> Dict[str, Any]:
        """Rule-based claim classification as fallback.

        Uses linguistic heuristics to determine credibility category.

        Heuristics:
        - Checkable claims with numbers/dates and no hedges → Supported
        - Claims with opinion markers → Potentially Misleading or Uncertain
        - Questions → Uncertain
        - Vague/hedged claims → Uncertain
        - Contradictory language → Potentially Misleading
        """
        lower = claim_text.lower().strip()

        # 1. Questions → Uncertain
        if lower.endswith("?"):
            return {
                "label": "uncertain",
                "score": 45,
                "rule_based": True,
            }

        # 2. Opinion markers → Potentially Misleading
        opinion_markers = ["i think", "i believe", "in my opinion", "imho",
                          "i guess", "it seems", "appears to be"]
        for marker in opinion_markers:
            if re.search(r"\b" + re.escape(marker) + r"\b", lower):
                return {
                    "label": "potentially_misleading",
                    "score": 30,
                    "rule_based": True,
                }

        # 2.5. Fake/hoax keywords → Potentially Misleading
        fake_keywords = ["fake", "hoax", "scam", "fraud"]
        for kw in fake_keywords:
            if re.search(r"\b" + re.escape(kw) + r"\b", lower):
                return {
                    "label": "potentially_misleading",
                    "score": 30,
                    "rule_based": True,
                }

        # 3. Instruction verbs → Uncertain (not really a checkable claim)
        instruction_verbs = ["check", "verify", "ensure", "confirm", "double-check"]
        for verb in instruction_verbs:
            if lower.startswith(verb + " "):
                return {
                    "label": "uncertain",
                    "score": 50,
                    "rule_based": True,
                }

        # 4. Numbers/dates present → likely Supported (factual claim with specifics)
        if re.search(r"\b\d+(?:\.\d+)?\b", claim_text):
            # Check it's not just a date in a question or opinion context
            if not lower.endswith("?") and not any(m in lower for m in opinion_markers):
                return {
                    "label": "supported",
                    "score": 82,
                    "rule_based": True,
                }

        # 5. Hedge words → Uncertain
        hedge_words = ["maybe", "perhaps", "possibly", "likely", "probably",
                      "it seems", "approximately", "roughly"]
        for hedge in hedge_words:
            if re.search(r"\b" + re.escape(hedge) + r"\b", lower):
                return {
                    "label": "uncertain",
                    "score": 48,
                    "rule_based": True,
                }

        # 6. Default: checkable claim without clear markers → Partially Supported
        return {
            "label": "partially_supported",
            "score": 65,
            "rule_based": True,
        }

    def classify_claim(self, claim_text: str) -> Dict[str, Any]:
        """Classify a claim and return structured result.

        This is the main entry point that integrates claim type from
        extraction with credibility assessment.

        Args:
            claim_text: The claim text to classify.

        Returns:
            Dict with:
            - claim_type: The claim type (from extraction)
            - credibility_label: The credibility category
            - credibility_score: Numeric score (0-100)
            - confidence: Classification confidence
            - rule_based: Whether rule-based fallback was used
        """
        # First, determine the claim type
        extraction_result = extract_claims(claim_text, include_types=["checkable_claim"])
        if not extraction_result:
            # Not a checkable claim - classify as opinion or question
            simple_type = self._simple_type_classify(claim_text)
            return {
                "claim_type": simple_type,
                "credibility_label": "uncertain",
                "credibility_score": 45,
                "confidence": 0.8,
                "rule_based": True,
            }

        # For checkable claims, use the ML or rule-based classifier
        prediction = self.predict(claim_text)
        rule_based = prediction.get("rule_based", False)

        # Determine claim type from extraction (simplified - use first detection)
        from ai_model.nlp.claim_extractor import ClaimExtractor
        extractor = ClaimExtractor()
        claims = extractor.extract(claim_text)
        claim_type = claims[0]["claim_type"] if claims else "checkable_claim"

        return {
            "claim_type": claim_type,
            "credibility_label": prediction.get("label", "uncertain"),
            "credibility_score": prediction.get("score", 50),
            "confidence": prediction.get("confidence", 0.5) if not rule_based else 0.7,
            "rule_based": rule_based,
        }

    def _simple_type_classify(self, text: str) -> str:
        """Simple claim type classification for non-checkable text."""
        lower = text.lower().strip()

        if lower.endswith("?"):
            return "question"
        opinion_markers = ["i think", "i believe", "in my opinion"]
        for m in opinion_markers:
            if m in lower:
                return "opinion"
        if any(lower.startswith(v + " ") for v in ["check ", "verify ", "ensure "]):
            return "instruction"
        return "general_statement"


def assess_claim(
    claim_text: str,
    *,
    classifier: Optional[ClaimClassifier] = None,
    evidence: List[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Assess a claim's credibility given optional evidence.

    This is the primary interface for credibility assessment.

    Args:
        claim_text: The claim text to assess.
        classifier: Optional ClaimClassifier instance. If None, a default
                  one is created (loads from disk or uses rule-based).
        evidence: Optional list of evidence dicts with 'source_name' and 'snippet'.
                  If provided, the assessment may be influenced by the evidence.

    Returns:
        Dict with:
        - claim_text: The input claim
        - credibility_label: One of "supported", "partially_supported",
                             "uncertain", "potentially_misleading"
        - credibility_score: Numeric score (0-100)
        - confidence: Assessment confidence (0.0-1.0)
        - evidence_influence: How much the evidence influenced the result
        - explanation: Human-readable explanation of the assessment
    """
    if classifier is None:
        classifier = ClaimClassifier()

    # Get base classification from classifier
    base_result = classifier.classify_claim(claim_text)

    # Factor in evidence if provided
    evidence_influence = 0.0
    has_evidence = bool(evidence)
    if evidence:
        evidence_influence = 0.3  # Evidence has moderate influence
        # Simple evidence-based adjustment
        supporting = 0
        contradicting = 0
        neutral = 0

        for ev in evidence:
            snippet = ev.get("snippet", "").lower()
            source = ev.get("source_name", "unknown")

            # Heuristic: check if snippet supports or contradicts
            support_keywords = ["supports", "confirms", "verified", "true", "correct"]
            contradict_keywords = ["contradicts", "false", "misleading", "fake", "wrong"]

            supported_any = any(kw in snippet for kw in support_keywords)
            contradicted_any = any(kw in snippet for kw in contradict_keywords)

            if supported_any and not contradicted_any:
                supporting += 1
            elif contradicted_any and not supported_any:
                contradicting += 1
            else:
                neutral += 1

        # Adjust score based on evidence balance
        if supporting > contradicting and base_result["credibility_label"] == "supported":
            # Reinforce supported
            base_result["credibility_score"] = min(base_result["credibility_score"] + 5, 100)
        elif contradicting > supporting and base_result["credibility_label"] == "potentially_misleading":
            # Reinforce potentially misleading
            base_result["credibility_score"] = max(base_result["credibility_score"] - 5, 0)
        elif supporting > contradicting and base_result["credibility_label"] in ["uncertain", "potentially_misleading"]:
            # Shift toward supported
            base_result["credibility_score"] = min(base_result["credibility_score"] + 10, 100)
            new_label = "supported" if base_result["credibility_score"] >= 80 else \
                        "partially_supported" if base_result["credibility_score"] >= 60 else "uncertain"
            base_result["credibility_label"] = new_label
    
    # If no evidence provided, default to Uncertain for "supported" claims
    # per project spec: do not fabricate support when no evidence is available
    if not has_evidence and base_result["credibility_label"] == "supported":
        base_result["credibility_label"] = "uncertain"
        base_result["credibility_score"] = 45  # midpoint for uncertain

    # Generate explanation
    explanation_parts = [base_result.get("explanation", "Assessment completed.")]

    if evidence:
        ev_count = len(evidence)
        if supporting > contradicting:
            explanation_parts.append(f"Evidence from {ev_count} source(s) supports this claim.")
        elif contradicting > supporting:
            explanation_parts.append(f"Evidence from {ev_count} source(s) contradicts this claim.")
        else:
            explanation_parts.append(f"Evidence from {ev_count} source(s) is inconclusive.")

    # Compute confidence based on how clear-cut the assessment is
    score = base_result["credibility_score"]
    if score >= 80:
        confidence = 0.85  # high confidence - well-supported
    elif score >= 60:
        confidence = 0.75  # medium-high confidence
    elif score >= 40:
        confidence = 0.65  # medium confidence - uncertain
    else:
        confidence = 0.55  # lower confidence - potentially misleading

    # Adjust confidence downward if evidence was limited
    if evidence and len(evidence) < 2:
        confidence = min(confidence, 0.7)

    return {
        "claim_text": claim_text,
        "credibility_label": base_result["credibility_label"],
        "credibility_score": base_result["credibility_score"],
        "confidence": round(confidence, 2),
        "evidence_influence": round(evidence_influence, 2),
        "explanation": " ".join(explanation_parts),
    }
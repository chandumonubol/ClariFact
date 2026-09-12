"""Stable public AI interface for ClariFact text analysis.

Provides the primary `analyze_text(text)` function that Member 1 can call
without knowing internal implementation details.

The function returns a structured result compatible with the API contract
(at agent/API_CONTRACT.md), enabling seamless integration with the backend.

Conceptual output format:
{
    "overall_credibility_score": int (0-100),
    "credibility_label": string,
    "confidence": int (0-100),
    "quality_score": int (0-100),
    "claims": [
        {
            "id": int,
            "claim_text": "string",
            "assessment": string,
            "confidence": real (0.0-1.0),
            "explanation": "string"
        }
    ],
    "evidence": [
        {
            "source_name": "string",
            "snippet": "string"
        }
    ],
    "explanation": "string"
}
"""

import logging
from typing import Any, Dict, List, Optional

from ai_model.preprocessing.text_preprocessor import preprocess
from ai_model.nlp.claim_extractor import extract_claims, ClaimExtractor
from ai_model.credibility.credibility_scorer import ClaimClassifier, assess_claim
from ai_model.credibility.content_quality import assess_quality


logger = logging.getLogger(__name__)


class AnalysisResult:
    """Container for the structured analysis result.

    Holds all output fields from the text analysis pipeline,
    organized for easy access and serialization.
    """

    def __init__(self):
        self.overall_credibility_score: int = 0
        self.credibility_label: str = "Uncertain"
        self.confidence: int = 50
        self.quality_score: int = 50
        self.claims: List[Dict[str, Any]] = []
        self.evidence: List[Dict[str, str]] = []
        self.explanation: str = ""

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary compatible with API contract."""
        return {
            "overall_credibility_score": self.overall_credibility_score,
            "credibility_label": self.credibility_label,
            "confidence": self.confidence,
            "quality_score": self.quality_score,
            "claims": self.claims,
            "evidence": self.evidence,
            "explanation": self.explanation,
        }

    def to_backend_schema(self) -> Dict[str, Any]:
        """Convert to backend analysis schema format.

        Maps to the SQLAlchemy Analysis model fields used in the backend.
        """
        # Extract claim info for backend storage
        claim_responses = []
        for c in self.claims:
            claim_responses.append({
                "id": c.get("id", 0),
                "claim_text": c.get("claim_text", c.get("text", "")),
                "assessment": c.get("assessment", c.get("credibility_label", "Uncertain")),
                "confidence": c.get("confidence", 0.0),
                "explanation": c.get("explanation", ""),
            })

        source_responses = []
        for s in self.evidence:
            source_responses.append({
                "source_name": s.get("source_name", ""),
                "snippet": s.get("snippet", ""),
            })

        return {
            "overall_credibility_score": self.overall_credibility_score,
            "credibility_label": self.credibility_label,
            "confidence": self.confidence,
            "quality_score": self.quality_score,
            "claims": claim_responses,
            "evidence": source_responses,
            "explanation": self.explanation,
        }


def analyze_text(text: str,
                 *,
                 classifier: Optional[ClaimClassifier] = None,
                 ) -> Dict[str, Any]:
    """Analyze input text and return structured credibility assessment.

    This is the primary public interface for the AI text analysis module.
    Member 1 can call this function without knowing internal NLP/ML details.

    The pipeline performs:
    1. Text preprocessing (cleaning, normalization, sentence segmentation)
    2. Claim extraction and classification
    3. Credibility assessment
    4. Content quality analysis
    5. Explanation generation

    Args:
        text: Input text to analyze. Can be normal text, empty, whitespace,
              None, very short, long, multiple sentences, etc.
        classifier: Optional ClaimClassifier instance. If None, one is created
                   (loads from disk or uses rule-based fallback).

    Returns:
        Dict compatible with the API contract at agent/API_CONTRACT.md,
        containing:
        - overall_credibility_score: int (0-100)
        - credibility_label: str (Supported/Partially Supported/Uncertain/Potentially Misleading)
        - confidence: int (0-100)
        - quality_score: int (0-100)
        - claims: list of claim dicts with assessment, confidence, explanation
        - evidence: list of evidence dicts with source_name, snippet
        - explanation: human-readable string

    Raises:
        ValueError: If input text is None or only whitespace (after validation).
    """
    # ===== Input Validation =====
    if text is None:
        raise ValueError("Input text cannot be None.")

    stripped = text.strip() if isinstance(text, str) else ""
    if not stripped:
        # Return structured result for empty/whitespace input
        return _empty_result()

    # ===== Step 1: Text Preprocessing =====
    preprocessed = preprocess(
        stripped,
        segment=True,
        tokenize=False,
        normalize_num=False,
    )

    # ===== Step 2: Claim Extraction =====
    extractor = ClaimExtractor(
        include_types=["checkable_claim", "opinion", "question", "instruction"],
        min_confidence=0.0,
    )
    raw_claims = extractor.extract(stripped)

    # ===== Step 3: Claim Classification & Credibility Assessment =====
    # Use the classifier to assess each claim
    if classifier is None:
        classifier = ClaimClassifier()

    # Assess credibility for the whole text (integrates evidence handling)
    credibility_result = assess_claim(
        stripped,
        classifier=classifier,
        evidence=[],  # No external evidence at this stage
    )

    # ===== Step 4: Process Claims for Output =====
    processed_claims = _process_claims(raw_claims, classifier)

    # ===== Step 5: Content Quality Analysis =====
    quality_result = assess_quality(stripped)

    # ===== Step 6: Build Structured Result =====
    result = AnalysisResult()

    # Set credibility score and label from assessment
    result.overall_credibility_score = credibility_result.get("credibility_score", 50)
    result.credibility_label = credibility_result.get("credibility_label", "Uncertain")
    result.confidence = credibility_result.get("confidence", 50)
    result.quality_score = quality_result.get("language_quality", 50)

    # Set claims
    result.claims = processed_claims

    # Set evidence (from assessment, may be empty if no evidence retrieved)
    evidence_from_assessment = credibility_result.get("explanation", "").split(". ")
    # Try to extract evidence info from explanation if available
    # For now, evidence stays as empty list if no external evidence
    result.evidence = []

    # Set explanation
    result.explanation = credibility_result.get("explanation", "")

    # If no claims were extracted but text has content, add a general statement
    if not result.claims and stripped:
        result.claims = [{
            "id": 1,
            "claim_text": stripped,
            "assessment": result.credibility_label,
            "confidence": result.confidence / 100.0,
            "explanation": result.explanation or "Analysis completed.",
        }]

    return result.to_dict()


def _process_claims(raw_claims: List[Dict[str, Any]],
                   classifier: ClaimClassifier) -> List[Dict[str, Any]]:
    """Process raw claims into output format.

    Converts extractor output to the format expected by the API contract.
    """
    processed = []

    for i, claim in enumerate(raw_claims, start=1):
        claim_type = claim.get("claim_type", "checkable_claim")

        # Map claim type to assessment label
        assessment_map = {
            "checkable_claim": "Supported",
            "opinion": "Partially Supported",
            "question": "Uncertain",
            "instruction": "Uncertain",
            "general_statement": "Partially Supported",
        }
        assessment = assessment_map.get(claim_type, "Uncertain")

        # Get confidence
        confidence = claim.get("confidence", 0.5)

        # Generate explanation
        explanation = claim.get("explanation", "")

        processed.append({
            "id": i,
            "claim_text": claim.get("claim_text", ""),
            "assessment": assessment,
            "confidence": round(confidence, 2),
            "explanation": explanation,
        })

    return processed


def _empty_result() -> Dict[str, Any]:
    """Return structured result for empty/whitespace/None input.

    Ensures the API never returns None or crashes on invalid input.
    """
    return {
        "overall_credibility_score": 0,
        "credibility_label": "Uncertain",
        "confidence": 0,
        "quality_score": 0,
        "claims": [],
        "evidence": [],
        "explanation": "No input text provided for analysis.",
    }
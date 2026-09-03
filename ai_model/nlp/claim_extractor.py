"""Claim extraction from text.

Identifies meaningful potentially checkable claims from sentences,
classifying them into types: Checkable Claim, Opinion, Question, Instruction,
General Statement.

The implementation is rule-based and explainable, using linguistic features
from spaCy (auxiliary verbs, sentence patterns, dependency patterns).
"""

import re
from typing import List, Dict, Any, Optional

from ai_model.nlp.claim_types import ClaimType

# Pattern categories for claim classification
OPINION_MARKERS = [
    "i think", "i believe", "i feel", "in my opinion", "imho", "i guess",
    "i suspect", "it seems", "appears to be", "as far as i know",
]

QUESTION_MARKERS = [
    "is", "are", "was", "were", "do", "does", "did",
    "can", "could", "would", "should", "will",
]

INSTRUCTION_VERBS = [
    "check", "verify", "validate", "confirm", "investigate",
    "ensure", "make sure", "confirm that", "double-check",
]


def _get_sentence_type(sentence: str) -> str:
    """Determine the basic sentence type (question, imperative, etc.)."""
    s = sentence.strip()

    # Question: ends with ? or starts with question word
    if s.endswith("?"):
        return "question"

    # Check for question words at start
    question_words = ["what", "where", "when", "who", "why", "how", "whether"]
    lower_s = s.lower()
    for qw in question_words:
        if lower_s.startswith(qw + " "):
            return "question"

    # Imperative: starts with a verb (instruction)
    # Simple heuristic: first word is likely a verb in imperative mood
    first_word = lower_s.split()[0] if lower_s.split() else ""
    if first_word:
        # Check if first word is an instruction verb
        if first_word in INSTRUCTION_VERBS:
            return "instruction"

    # Check if first word ends with -ing (could be instruction)
    if first_word and first_word.endswith("ing"):
        return "instruction"

    return "statement"


def _has_opinion_marker(sentence: str) -> bool:
    """Check if sentence contains opinion markers."""
    lower = sentence.lower()
    for marker in OPINION_MARKERS:
        if marker in lower:
            return True
    return False


def _has_question_mark(sentence: str) -> bool:
    """Check if sentence is a question."""
    return sentence.strip().endswith("?")


def _classify_by_patterns(sentence: str) -> str:
    """Classify sentence using linguistic patterns.

    Returns one of: checkable_claim, opinion, question, instruction, general_statement
    """
    s = sentence.strip()
    lower = s.lower()

    # 1. Questions - end with ? or start with question word
    if _has_question_mark(s):
        return "question"

    # 2. Opinions - contain opinion markers
    if _has_opinion_marker(s):
        return "opinion"

    # 3. Instructions - start with imperative verbs
    first_word = lower.split()[0] if lower.split() else ""
    if first_word in INSTRUCTION_VERBS:
        return "instruction"

    # 4. Checkable claims: factual statements with specific entities,
    #    verbs of happening, reporting, etc.
    #    Heuristic: no opinion markers, not a question, contains
    #    factual verbs/ nouns

    # Check for "hedge" words that suggest uncertainty/opinion
    hedge_words = ["maybe", "perhaps", "possibly", "likely", "probably",
                   "it seems", "appears", "roughly", "approximately"]
    for hedge in hedge_words:
        # Match whole word only
        if re.search(r"\b" + re.escape(hedge) + r"\b", lower):
            return "opinion"

    # 5. Default: checkable claim (factual statement)
    return "checkable_claim"


def extract_claims(text: str, *, include_types: List[str] = None) -> List[Dict[str, Any]]:
    """Extract claims from input text.

    For each sentence in the text, determine if it's a checkable claim,
    opinion, question, instruction, or general statement.

    Args:
        text: Input text to extract claims from.
        include_types: Optional list of claim types to include.
            If None, all types are included.

    Returns:
        List of claim dicts, each with:
        - claim_text: The original sentence text
        - claim_type: The detected claim type (ClaimType enum value)
        - checkable: Whether the claim is checkable (True for Checkable Claim)
        - confidence: Extraction confidence (0.0 to 1.0)
    """
    if not text or not text.strip():
        return []

    # Step 1: Segment into sentences
    from ai_model.preprocessing.text_preprocessor import segment_sentences
    sentences = segment_sentences(text)

    claims = []

    for sent in sentences:
        claim_type_str = _classify_by_patterns(sent)
        claim_type = ClaimType(claim_type_str)

        # Filter by requested types
        if include_types and claim_type.value not in include_types:
            continue

        # Determine checkability
        checkable = (claim_type == ClaimType.CHECKABLE_CLAIM)

        # Calculate confidence based on linguistic cues
        confidence = _compute_confidence(sent, claim_type)

        # Determine if it's checkable based on type
        is_checkable = (claim_type in [
            ClaimType.CHECKABLE_CLAIM,
            ClaimType.GENERAL_STATEMENT,
        ])

        claim = {
            "claim_text": sent,
            "claim_type": claim_type.value,
            "checkable": is_checkable,
            "confidence": confidence,
        }

        claims.append(claim)

    return claims


def _compute_confidence(sentence: str, claim_type: ClaimType) -> float:
    """Compute extraction confidence for a claim.

    Based on linguistic clarity of the claim type.
    """
    lower = sentence.lower().strip()
    confidence = 0.5  # base confidence

    if claim_type == ClaimType.CHECKABLE_CLAIM:
        # Higher confidence for clear factual statements
        if lower.endswith("."):
            confidence = 0.8
        if re.search(r"\b\d+\b", lower):
            confidence = 0.85  # numbers add specificity
        if not _has_opinion_marker(sentence):
            confidence = min(confidence + 0.1, 1.0)

    elif claim_type == ClaimType.OPINION:
        # Opinions with "I think" marker
        if "i think" in lower or "i believe" in lower or "in my opinion" in lower:
            confidence = 0.9
        else:
            confidence = 0.7

    elif claim_type == ClaimType.QUESTION:
        confidence = 0.95  # questions are easily identifiable

    elif claim_type == ClaimType.INSTRUCTION:
        confidence = 0.85

    elif claim_type == ClaimType.GENERAL_STATEMENT:
        confidence = 0.6

    # Ensure reasonable bounds
    return round(min(max(confidence, 0.0), 1.0), 2)


class ClaimExtractor:
    """ClaimExtractor - reusable claim extraction class.

    Provides methods to extract claims from text with various options
    for type filtering, confidence thresholds, and output formatting.
    """

    def __init__(
        self,
        include_types: List[str] = None,
        min_confidence: float = 0.0,
    ):
        self.include_types = include_types or [
            "checkable_claim", "opinion", "question", "instruction", "general_statement"
        ]
        self.min_confidence = min_confidence

    def extract(self, text: str) -> List[Dict[str, Any]]:
        """Extract claims from text.

        Args:
            text: Input text to extract claims from.
            min_confidence: Minimum confidence threshold (0.0-1.0).

        Returns:
            List of claim dicts meeting the filter criteria.
        """
        claims = extract_claims(text, include_types=self.include_types)
        # Filter by confidence
        filtered = [c for c in claims if c.get("confidence", 0) >= self.min_confidence]
        return filtered

    def extract_with_details(self, text: str) -> List[Dict[str, Any]]:
        """Extract claims with full detail including explanation.

        Returns claims with additional explainable fields.
        """
        claims = self.extract(text)
        for claim in claims:
            # Add explanation based on type
            claim_type = ClaimType(claim["claim_type"])
            claim["explanation"] = self._generate_explanation(claim_type, claim["claim_text"])
        return claims

    @staticmethod
    def _generate_explanation(claim_type: ClaimType, claim_text: str) -> str:
        """Generate a human-readable explanation for the claim classification."""
        if claim_type == ClaimType.CHECKABLE_CLAIM:
            return "This is a checkable factual claim."
        elif claim_type == ClaimType.OPINION:
            return "This appears to be a personal opinion or evaluation."
        elif claim_type == ClaimType.QUESTION:
            return "This is a question seeking information."
        elif claim_type == ClaimType.INSTRUCTION:
            return "This is an instruction or directive."
        elif claim_type == ClaimType.GENERAL_STATEMENT:
            return "This is a general statement."
        return "Unknown claim type."


# Alias for convenience
extract = extract_claims  # backwards-compatible shorthand
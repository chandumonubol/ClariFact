"""Content quality analysis for ClariFact.

Analyzes text quality across multiple dimensions as specified in TRD.md:
- Clarity: How easy the text is to understand
- Relevance: How relevant the content is to the claimed topic
- Completeness: Whether the text provides complete information
- Language Quality: Grammar, spelling, and writing mechanics

Each dimension is scored 0-100, where higher is better.
"""

import re
from typing import Dict, Any, Optional


# Minimum text length thresholds for quality assessment
MIN_CHARACTERS_FOR_CLARITY = 50
MIN_CHARACTERS_FOR_COMPLETENESS = 100


def _count_syllables(word: str) -> int:
    """Approximate syllable count for Flesch readability calculations."""
    word = word.lower()
    # Simple vowel group counting
    vowels = "aeiouy"
    count = 0
    prev_was_vowel = False

    for char in word:
        is_vowel = char in vowels
        if is_vowel and not prev_was_vowel:
            count += 1
        prev_was_vowel = is_vowel

    # Every word has at least one syllable
    if count == 0:
        count = 1

    return count


def _flesch_reading_ease(text: str) -> Optional[float]:
    """Calculate Flesch Reading Ease score.

    Higher score = easier to read.
    - 90-100: Very easy (5th grade)
    - 80-90: Easy
    - 70-80: Fairly easy
    - 60-70: Standard
    - 50-60: Fairly difficult
    - 30-50: Difficult
    - 0-30: Very difficult

    Returns None if text is too short for reliable calculation.
    """
    if not text or not text.strip():
        return None

    tokens = re.findall(r"\b[A-Za-z]+\b", text)
    if len(tokens) < 5:
        return None

    # Count sentences (rough approximation)
    sentences = [s for s in re.split(r"[.!?]+", text) if s.strip()]
    num_sentences = len(sentences) or 1

    # Count words
    num_words = len(tokens)

    # Count syllables
    total_syllables = sum(_count_syllables(t) for t in tokens)

    # Flesch formula: 206.835 - 1.015 * (words/sentences) - 84.6 * (syllables/words)
    if num_sentences > 0 and num_words > 0:
        score = 206.835 - 1.015 * (num_words / num_sentences) - 84.6 * (total_syllables / num_words)
        return round(max(min(score, 100), 0), 1)

    return None


def _count_long_sentences(text: str, threshold: int = 30) -> int:
    """Count sentences longer than a character threshold."""
    sentences = [s for s in re.split(r"[.!?]+", text) if s.strip()]
    long_sentences = [s for s in sentences if len(s) > threshold]
    return len(long_sentences)


def _count_complex_words(text: str) -> int:
    """Count words with 3+ syllables (complex words)."""
    tokens = re.findall(r"\b[A-Za-z]+\b", text)
    complex_count = 0
    for token in tokens:
        if _count_syllables(token) >= 3:
            complex_count += 1
    return complex_count


def assess_quality(text: str) -> Dict[str, Any]:
    """Assess text quality across multiple dimensions.

    Returns a dict with scores for each dimension (0-100 scale).

    Dimensions:
    - clarity: How easy to understand (Flesch Reading Ease based)
    - relevance: How topic-relevant the content is
    - completeness: Whether information is complete
    - language_quality: Grammar/spelling quality

    Each score is an integer 0-100 where higher is better.
    """
    if not text or not text.strip():
        return {
            "clarity": 0,
            "relevance": 0,
            "completeness": 0,
            "language_quality": 0,
        }

    cleaned = text.strip()
    results: Dict[str, Any] = {}

    # 1. Clarity: Based on Flesch Reading Ease
    fe = _flesch_reading_ease(cleaned)
    if fe is not None:
        # Map FRE score to 0-100 clarity scale
        # fre 90-100 → clarity 100, fre 0-30 → clarity 0
        if fe >= 90:
            clarity = 100
        elif fe >= 80:
            clarity = 90
        elif fe >= 70:
            clarity = 80
        elif fe >= 60:
            clarity = 70
        elif fe >= 50:
            clarity = 60
        elif fe >= 30:
            clarity = 40 + int((fe - 30) / 20 * 20)  # 40-60
        else:
            clarity = max(0, 40 + int((fe - 0) / 30 * 20))  # 0-40
        results["clarity"] = round(max(min(clarity, 100), 0))
    else:
        # Text too short for FRE; use simple heuristics
        results["clarity"] = _clarity_short_text(cleaned)

    # 2. Relevance: Check for topic-related keywords
    results["relevance"] = _assess_relevance(cleaned)

    # 3. Completeness: Check for indicators of completeness
    results["completeness"] = _assess_completeness(cleaned)

    # 4. Language Quality: Grammar and spelling indicators
    results["language_quality"] = _assess_language_quality(cleaned)

    # Ensure all values are integers in 0-100 range
    for key in results:
        if isinstance(results[key], float):
            results[key] = round(max(min(results[key], 100), 0))
        else:
            results[key] = round(max(min(results[key], 100), 0))

    return results


def _clarity_short_text(text: str) -> int:
    """Estimate clarity for short texts (< 50 chars)."""
    if len(text) < 10:
        return 50  # Neutral for very short text
    # Simple checks for short text
    if text[0].isupper() and text[-1] == ".":
        return 70  # Looks like a proper sentence
    return 50


def _assess_relevance(text: str) -> int:
    """Assess relevance of text to its claimed topic.

    Uses keyword overlap heuristics: presence of topic indicators,
    proper nouns, and factual content words suggests relevance.
    """
    if not text:
        return 0

    lower = text.lower()

    # Topic indicator keywords that suggest relevance
    relevance_keywords = {
        "claim", "fact", "report", "study", "research", "according",
        "data", "analysis", "shows", "found", "results",
    }

    # Proper nouns (words starting with capital letter mid-sentence)
    proper_nouns = len(re.findall(r"\b[A-Z][a-z]+(?: [A-Z][a-z]+)*\b", text))

    # Count relevance-matching words
    words = re.findall(r"\b[A-Za-z]+\b", lower)
    matching = sum(1 for w in words if w in relevance_keywords)

    # Score based on indicators
    score = min(100, matching * 10 + proper_nouns * 5)

    # Boost if text contains numbers (factual content)
    if re.search(r"\b\d+(?:\.\d+)?\b", text):
        score = min(100, score + 15)

    return round(score)


def _assess_completeness(text: str) -> int:
    """Assess whether the text provides complete information.

    Checks for:
    - Sufficient length
    - Presence of beginning/middle/end structure
    - Supporting details
    - Number of sentences
    """
    if not text:
        return 0

    length = len(text.strip())
    sentences = [s for s in re.split(r"[.!?]+", text) if s.strip()]

    score = 0

    # Length-based scoring
    if length >= 300:
        score += 40
    elif length >= 150:
        score += 30
    elif length >= 50:
        score += 20
    elif length > 0:
        score += 10

    # Sentence count scoring
    if len(sentences) >= 3:
        score += 30
    elif len(sentences) >= 2:
        score += 20
    elif len(sentences) >= 1:
        score += 10

    # Numbers/dates suggest more complete factual information
    if re.search(r"\b\d+(?:\.\d+)?\b", text):
        score += 15

    # Question words or specific verbs suggest completeness
    question_words = ["who", "what", "when", "where", "why", "how"]
    if any(w in text.lower() for w in question_words):
        score += 15

    return round(min(score, 100))


def _assess_language_quality(text: str) -> int:
    """Assess language quality (grammar, spelling, mechanics).

    Checks for:
    - Proper capitalization
    - Sentence punctuation
    - No all-caps shouting
    - Reasonable word structure
    """
    if not text:
        return 0

    lower = text.lower()
    score = 100
    penalties = 0

    # Penalty: all-caps text
    if text.isupper() and len(text) > 3:
        penalties += 30

    # Penalty: no sentence-ending punctuation
    if not re.search(r"[.!?]\s*$", text):
        penalties += 15

    # Penalty: excessive abbreviations (all caps words)
    all_caps_words = len(re.findall(r"\b[A-Z]{3,}\b", text))
    if all_caps_words > 0:
        penalties += min(all_caps_words * 2, 20)

    # Penalty: very short sentences (might indicate incomplete thoughts)
    sentences = [s for s in re.split(r"[.!?]+", text) if s.strip()]
    if len(sentences) > 0 and len(sentences) > 0:
        avg_len = sum(len(s) for s in sentences) / len(sentences)
        if avg_len < 10:
            penalties += 10

    score = max(0, score - penalties)

    # Additional bonus: proper starting capitalization
    if text and text[0].isupper():
        score = min(100, score + 5)

    # Bonus: contains numbers/dates (suggests well-formed factual content)
    if re.search(r"\b\d+(?:\.\d+)?\b", text):
        score = min(100, score + 5)

    return round(score)
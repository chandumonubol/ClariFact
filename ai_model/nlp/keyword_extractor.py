"""Basic keyword extraction for ClariFact.

Extracts meaningful keywords that help downstream analysis identify important
concepts. Avoids returning meaningless stopwords.

Uses spaCy POS tagging to extract nouns, proper nouns, and adjectives,
filtered against a stopword set.
"""

import re
from typing import List, Set

from ai_model.nlp.keyword_extractor import STOPWORDS as DEFAULT_STOPWORDS


def extract_keywords(
    text: str,
    *,
    limit: int = 20,
    include_pos: Set[str] = None,
    exclude_stopwords: bool = True,
) -> List[str]:
    """Extract meaningful keywords from text.

    Uses spaCy POS tagging to identify important content words.
    By default extracts NOUN, PROPER NOUN, and ADJECTIVE tokens.

    Args:
        text: Input text to extract keywords from.
        limit: Maximum number of keywords to return.
        include_pos: Set of spaCy POS tags to include (default: nouns, proper nouns, adjectives).
        exclude_stopwords: Whether to filter out stopwords.

    Returns:
        List of keyword strings, sorted by relevance/importance.
    """
    if not text or not text.strip():
        return []

    try:
        import spacy

        try:
            nlp = spacy.load("en_core_web_sm")
        except OSError:
            return _extract_keywords_fallback(text, limit, include_pos, exclude_stopwords)

        doc = nlp(text.lower())
        keywords = []

        pos_tags = include_pos or {"NOUN", "PROPN", "ADJ"}

        # Count token frequency for ranking
        freq = {}
        for token in doc:
            if token.pos_ in pos_tags:
                token_text = token.text.lower()
                if exclude_stopwords and token_text in DEFAULT_STOPWORDS:
                    continue
                # Skip pure digits alone
                if token_text.isdigit():
                    continue
                # Skip single characters (unless proper noun)
                if len(token_text) <= 1 and token.pos_ != "PROPN":
                    continue
                freq[token_text] = freq.get(token_text, 0) + 1

        # Sort by frequency, then alphabetically for stability
        sorted_keywords = sorted(freq.keys(), key=lambda k: (-freq[k], k))
        keywords = sorted_keywords[:limit]

    except ImportError:
        keywords = _extract_keywords_fallback(text, limit, include_pos, exclude_stopwords)

    return keywords


def _extract_keywords_fallback(
    text: str,
    limit: int,
    include_pos: Set[str],
    exclude_stopwords: bool,
) -> List[str]:
    """Fallback keyword extraction using simple heuristics without spaCy."""
    # Simple approach: extract capitalized phrases and important words
    words = re.findall(r"\b[A-Za-z]{4,}\b", text)
    freq = {}
    for word in words:
        lower = word.lower()
        if exclude_stopwords and lower in DEFAULT_STOPWORDS:
            continue
        freq[lower] = freq.get(lower, 0) + 1

    sorted_kw = sorted(freq.keys(), key=lambda k: (-freq[k], k))
    return sorted_kw[:limit]


def extract_important_phrases(
    text: str,
    *,
    min_length: int = 2,
    max_length: int = 4,
) -> List[str]:
    """Extract multi-word important phrases from text.

    Uses spaCy NP chunks if available, otherwise falls back to bigram extraction.
    """
    try:
        import spacy

        try:
            nlp = spacy.load("en_core_web_sm")
        except OSError:
            return _extract_important_phrases_fallback(text, min_length, max_length)

        doc = nlp(text)
        phrases = []

        for chunk in doc.noun_chunks:
            phrase_text = chunk.text.strip()
            # Filter by length
            tokens = phrase_text.split()
            if min_length <= len(tokens) <= max_length:
                # Skip if phrase is just a stopword cluster
                if all(token.lower() in DEFAULT_STOPWORDS for token in tokens):
                    continue
                phrases.append(phrase_text)

        # Deduplicate while preserving order
        seen = set()
        unique_phrases = []
        for phrase in phrases:
            if phrase not in seen:
                seen.add(phrase)
                unique_phrases.append(phrase)

        return unique_phrases

    except ImportError:
        return _extract_important_phrases_fallback(text, min_length, max_length)


def _extract_important_phrases_fallback(
    text: str,
    min_length: int,
    max_length: int,
) -> List[str]:
    """Fallback phrase extraction without spaCy."""
    # Simple bigram/trigram extraction
    words = re.findall(r"\b[A-Za-z]+\b", text)
    phrases = []
    for i in range(len(words) - 1):
        phrase = f"{words[i]} {words[i+1]}"
        token_count = 2
        if min_length <= token_count <= max_length:
            phrases.append(phrase)
    # Deduplicate
    seen = set()
    unique = []
    for p in phrases:
        if p not in seen:
            seen.add(p)
            unique.append(p)
    return unique
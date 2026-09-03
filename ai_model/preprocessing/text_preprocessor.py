"""Text preprocessing pipeline for ClariFact.

Handles whitespace normalization, basic cleaning, sentence segmentation,
and tokenization. Preserves meaningful factual information (numbers, dates,
percentages, names, locations, important punctuation).
"""

import re
from typing import List, Optional


STOPWORDS = {
    "i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your",
    "yours", "yourself", "yourselves", "he", "him", "his", "himself", "she",
    "her", "hers", "herself", "it", "its", "itself", "they", "them", "their",
    "theirs", "themselves", "what", "which", "who", "whom", "this", "that",
    "these", "those", "am", "is", "are", "was", "were", "be", "been", "being",
    "have", "has", "had", "having", "do", "does", "did", "doing", "a", "an",
    "the", "and", "but", "if", "or", "because", "as", "until", "while", "of",
    "at", "by", "for", "with", "about", "against", "between", "through",
    "during", "before", "after", "above", "below", "to", "from", "up", "down",
    "in", "out", "on", "off", "over", "under", "again", "further", "then",
    "once", "here", "there", "when", "where", "why", "how", "all", "any",
    "both", "each", "few", "more", "most", "other", "some", "such", "no",
    "nor", "not", "only", "own", "same", "so", "than", "too", "very", "s",
    "t", "can", "will", "just", "don", "should", "now",
}


def normalize_whitespace(text: str) -> str:
    """Normalize whitespace in text: collapse multiple spaces, trim edges."""
    text = re.sub(r"\s+", " ", text)
    text = text.strip()
    return text


def clean_text(text: str) -> str:
    """Basic text cleaning while preserving factual information.

    Preserves:
    - Numbers and dates
    - Percentages
    - Names (capitalized words, kept as-is)
    - Locations kept as-is
    - Important punctuation (. , ; : ! ?)
    """
    # Remove control characters
    text = re.sub(r"[\x00-\x1f\x7f]", "", text)

    # Normalize whitespace
    text = normalize_whitespace(text)

    # Remove empty lines that may have been left behind
    text = re.sub(r"\n\s*\n", "\n", text)

    return text


def segment_sentences(text: str) -> List[str]:
    """Split text into sentences using spaCy.

    Returns a list of sentence strings. If spaCy model is not available,
    falls back to a simple regex-based split.
    """
    try:
        import spacy

        try:
            nlp = spacy.load("en_core_web_sm")
        except OSError:
            # Model not available, use fallback
            return _segment_sentences_fallback(text)

        doc = nlp(text)
        sentences = [sent.text for sent in doc.sents if sent.text.strip()]
        if sentences:
            return sentences

    except ImportError:
        pass

    return _segment_sentences_fallback(text)


def _segment_sentences_fallback(text: str) -> List[str]:
    """Fallback sentence segmentation using regex.

    Splits on sentence-ending punctuation (. ! ?) followed by whitespace.
    """
    sentences = re.split(r"(?<=[.!?])\s+", text)
    # Filter out empty strings
    sentences = [s.strip() for s in sentences if s.strip()]
    if sentences:
        return sentences

    # Last resort: return the whole text as one sentence
    if text.strip():
        return [text.strip()]
    return []


def tokenize(text: str) -> List[str]:
    """Tokenize text into words using spaCy.

    Returns lowercase tokens with punctuation removed.
    Stops words are preserved for downstream analysis; callers can filter.
    """
    try:
        import spacy

        try:
            nlp = spacy.load("en_core_web_sm")
        except OSError:
            return _tokenize_fallback(text)

        doc = nlp(text.lower())
        tokens = [token.text for token in doc if not token.is_punct]
        return tokens

    except ImportError:
        return _tokenize_fallback(text)


def _tokenize_fallback(text: str) -> List[str]:
    """Simple fallback tokenization: split on whitespace, remove punctuation."""
    tokens = []
    for word in text.lower().split():
        # Strip leading/trailing punctuation
        word = re.sub(r"^+\.+|\.+$", "", word)
        word = re.sub(r"^+,+|,+$", "", word)
        word = re.sub(r"^+!+|!+$", "", word)
        word = re.sub(r"^\?+\?|\?+$", "", word)
        if word:
            tokens.append(word)
    return tokens


def remove_stopwords(tokens: List[str]) -> List[str]:
    """Remove common stopwords from a token list.

    Preserves nouns, verbs, adjectives and other meaningful tokens.
    """
    return [t for t in tokens if t.lower() not in STOPWORDS]


def normalize_numbers(text: str) -> str:
    """Normalize spelled-out numbers to digits where meaningful.

    Examples:
        "one hundred" -> "100"
        "dozen" kept as-is if not easily mappable

    Preserves existing digits and critical factual numbers.
    """
    word_to_digit = {
        "zero": "0",
        "one": "1",
        "two": "2",
        "three": "3",
        "four": "4",
        "five": "5",
        "six": "6",
        "seven": "7",
        "eight": "8",
        "nine": "9",
        "ten": "10",
        "hundred": "100",
        "thousand": "1000",
        "million": "1000000",
        "billion": "1000000000",
    }

    words = text.split()
    normalized = []
    for word in words:
        lower = word.lower()
        if lower in word_to_digit:
            normalized.append(word_to_digit[lower])
        else:
            normalized.append(word)
    return " ".join(normalized)


def preprocess(
    text: str,
    *,
    segment: bool = True,
    tokenize: bool = False,
    remove_stopwords_flag: bool = False,
    normalize_num: bool = False,
) -> dict:
    """Run the full preprocessing pipeline on input text.

    Returns a dict with normalized representation and intermediate results.
    """
    # Step 1: Basic cleaning
    cleaned = clean_text(text)

    # Step 2: Normalize numbers (before other processing)
    if normalize_num:
        cleaned = normalize_numbers(cleaned)

    # Step 3: Whitespace normalization (already done inside clean_text)
    # already normalized

    result: dict = {
        "original": text,
        "cleaned": cleaned,
    }

    # Step 4: Sentence segmentation
    if segment:
        sentences = segment_sentences(cleaned)
        result["sentences"] = sentences
    else:
        result["sentences"] = [cleaned] if cleaned.strip() else []

    # Step 5: Tokenization
    if tokenize:
        tokens = tokenize(cleaned)
        if remove_stopwords_flag:
            tokens = remove_stopwords(tokens)
        result["tokens"] = tokens
    else:
        result["tokens"] = []

    return result
# ai_model — ClariFact AI/ML Module

## Purpose

This module provides the AI/ML analysis engine for ClariFact, performing multimodal content credibility analysis starting with text. It implements a pipeline for text preprocessing, claim extraction, credibility assessment, and content quality analysis, with explainable results.

The module is designed to be **independent** of the backend framework (FastAPI/Flask) and provides a stable Python API that Member 1 can call without knowing internal implementation details.

## Architecture

```text
ai_model/
├── preprocessing/     Text cleaning, normalization, sentence segmentation
├── nlp/              Claim extraction, classification, keyword extraction
├── credibility/      Credibility scoring, evidence assessment
├── inference/        Stable public interface (analyze_text)
└── models/           Trained ML models (saved via joblib)
```

## Text Pipeline

```text
Raw Text
   ↓
Validation (None, empty, whitespace, special chars)
   ↓
Preprocessing (whitespace normalization, basic cleaning, sentence segmentation)
   ↓
Keyword Extraction (POS-based, stopword-filtered)
   ↓
Claim Extraction (rule-based: checkable_claim, opinion, question, instruction, general_statement)
   ↓
Claim Classification (same 5 types)
   ↓
Credibility Assessment (TF-IDF + LR or rule-based: Supported/Partially Supported/Uncertain/Potentially Misleading)
   ↓
Content Quality Analysis (clarity, relevance, completeness, language_quality)
   ↓
Explainable Result (human-readable explanation)
   ↓
Structured Output (dict compatible with API contract)
```

## Public Interface

```python
from ai_model.inference.text_analyzer import analyze_text

result = analyze_text("The company launched the product in 2025. It sold 2 million units.")
```

**`analyze_text(text)`** returns a dict with:

| Field | Type | Description |
|-------|------|-------------|
| `overall_credibility_score` | int (0-100) | Numeric credibility score |
| `credibility_label` | str | One of: Supported, Partially Supported, Uncertain, Potentially Misleading |
| `confidence` | float (0.0-1.0) | Assessment confidence |
| `quality_score` | int (0-100) | Content quality score |
| `claims` | list | List of claim dicts with `claim_text`, `assessment`, `confidence`, `explanation` |
| `evidence` | list | List of evidence dicts with `source_name`, `snippet` |
| `explanation` | str | Human-readable explanation |

## Text Preprocessing

Supports these operations via the `preprocess()` function:

- `normalize_whitespace()`: Collapse multiple spaces, trim edges
- `clean_text()`: Remove control chars, normalize whitespace
- `segment_sentences()`: Split into sentences (spaCy + regex fallback)
- `tokenize()`: Word tokenization (spaCy + fallback)
- `remove_stopwords()`: Filter common stopwords
- `normalize_numbers()`: Convert spelled-out numbers to digits
- `preprocess()`: Full pipeline combining all steps

**Preserved information**: Numbers, dates, percentages, names, locations, important punctuation. Stopwords are removed only during tokenization, not from the main text.

## Claim Extraction

Rule-based extraction classifying sentences into:

- **Checkable Claim**: Factual statement that can be verified (e.g., "The Earth revolves around the Sun.")
- **Opinion**: Personal evaluation (e.g., "I think this movie is excellent.")
- **Question**: Information request (e.g., "Is this information correct?")
- **Instruction**: Directive or command (e.g., "Check this information.")
- **General Statement**: Neutral factual assertion

## Credibility Assessment

Four categories (no binary TRUE/FALSE):

- **Supported** (score 80-100): Claim well-supported
- **Partially Supported** (score 60-79): Partly supported/contested
- **Uncertain** (score 40-59): Insufficient evidence
- **Potentially Misleading** (score 0-39): Contradicts available evidence

**Rule-based heuristics** (used when no model trained):

- Questions → Uncertain
- Fake/hoax/scam/fraud keywords → Potentially Misleading
- Opinion markers ("I think", "I believe") → Potentially Misleading
- Numbers/dates present → Supported
- Hedge words ("maybe", "perhaps") → Uncertain
- Default → Partially Supported

**ML model** (TF-IDF + Logistic Regression, trained with labeled data):

- Can be trained via `ClaimClassifier.train()`
- Saved/loaded via `joblib`
- Follows TRD.md spec: TfidfVectorizer ngram_range=(1,2) + LogisticRegression class_weight='balanced'

## Content Quality Analysis

Four dimensions (0-100, higher is better):

- **clarity**: Based on Flesch Reading Ease
- **relevance**: Keyword overlap + proper nouns + numbers
- **completeness**: Length + sentence count + numbers + question words
- **language_quality**: Capitalization + punctuation + grammar indicators

## ML Component

The project uses a **TF-IDF + Logistic Regression** pipeline for claim classification:

- **Vectorization**: TfidfVectorizer with ngram_range=(1,2), English stopwords
- **Classifier**: LogisticRegression with class_weight='balanced', max_iter=1000, random_state=42
- **Training**: Can be called via `ClaimClassifier.train(training_claims, training_labels)`
- **Evaluation**: Hold-out test set (last 20%), reports accuracy, precision, recall, F1

**Note**: No dataset is currently fabricated. If no training data is available, the rule-based fallback is used transparently.

## How to Run Tests

```bash
python -m pytest backend/tests/ -v
```

Or run the standalone test script:

```bash
python backend/test_ai_module.py
```

## Test Coverage

All required test cases are covered:

- Normal text: "The company launched the product in 2025."
- Empty text: ""
- Whitespace: "   "
- Multiple claims: Paragraph with several factual statements
- Opinion: "I think this product is excellent."
- Question: "Did the company launch the product in 2025?"
- Instruction: "Check this information."
- Long text: Ensures processing does not unexpectedly fail
- Special characters: Various symbols and formatting
- Numbers/dates: Ensures factual information survives preprocessing
- Unavailable evidence → "Uncertain" (not fabricated)
- Malformed input: Graceful failure

## Known Limitations

- Claim extraction accuracy depends on text quality and linguistic patterns
- Credibility assessment is AI-assisted, not absolute truth
- No external evidence retrieval at Checkpoint 1 (evidence list is empty)
- Rule-based heuristics may not cover all linguistic variations
- ML model requires trained dataset; currently using rule-based fallback
- Image OCR and video processing not yet implemented (Phase 3/4)

## Future Image/Video Integration

After Checkpoint 1, the following will be added:

- **Image**: OCR (pytesseract/easyocr) → claim extraction → credibility
- **Video**: Speech-to-Text (Whisper/faster-whisper) → transcript analysis → credibility

The `analyze_text()` interface is designed to eventually extend to `analyze_image()` and `analyze_video()`, but those are not implemented at Checkpoint 1.
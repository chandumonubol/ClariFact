## AI/ML State

### Sentiment:
Not applicable (credibility assessment, not sentiment analysis).

### Claim Extraction:
Implemented rule-based claim extraction with classification into Checkable Claim, Opinion, Question, Instruction, General Statement. Uses linguistic patterns from spaCy (auxiliary verbs, sentence patterns, dependency patterns). Keywords markers, opinion markers, question markers, and instruction verbs are used for classification.

### Credibility:
Implemented TF-IDF + Logistic Regression model with rule-based fallback. Credibility categories: Supported (80-100), Partially Supported (60-79), Uncertain (40-59), Potentially Misleading (0-39). Evidence influence handled moderately. Model can be trained and saved as `models/claim_classifier.joblib`.

### Image OCR:
Not started. pytesseract/easyocr to be integrated after Checkpoint 1.

### Video Speech-to-Text:
Not started. Whisper/faster-whisper to be integrated after Checkpoint 1.

### Supported Input Types (MVP)
- Text: ✓ (Checkpoint 1 complete)
- Image: Not started (Phase 3)
- Video: Not started (Phase 4)

### Known Limitations
- Claim extraction accuracy depends on text quality.
- Credibility assessment is AI-assisted, not absolute truth.
- Evidence retrieval may be incomplete for niche claims.
- Rule-based heuristics may not cover all linguistic variations.

### Pending AI Work
- Train TF-IDF + Logistic Regression model on claim dataset and save to disk.
- Integrate pytesseract for OCR after Checkpoint 1.
- Integrate Whisper/faster-whisper for video STT after Checkpoint 1.
- Implement evidence retrieval (BM25 + FAISS vector search).

### Model Status
- claim_classifier.joblib: Not yet trained/saved.
- Currently using rule-based fallback with proven heuristics.
- Expected F1 >= 0.65 on held-out test set once trained with dataset.
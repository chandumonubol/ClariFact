## AI/ML State

### Sentiment:
Not applicable (credibility assessment, not sentiment analysis).

### Claim Extraction:
Design complete (spaCy NER + rule-based patterns). Not yet implemented in production.

### Credibility:
Design complete (TF-IDF + Logistic Regression aggregation). Model to be trained and saved as `models/claim_classifier.joblib`.

### Image OCR:
Not started. pytesseract/easyocr to be integrated in Phase 3.

### Video Speech-to-Text:
Not started. Whisper/faster-whisper to be integrated in Phase 4.

### Supported Input Types (MVP)
- Text: ✓ (Phase 2)
- Image: ✓ (Phase 3 design complete)
- Video: ✓ (Phase 4 design complete)

### Known Limitations
- Claim extraction accuracy depends on text quality.
- OCR accuracy depends on image clarity, lighting, text size.
- STT accuracy depends on audio quality, background noise, speaker accent.
- Credibility assessment is AI-assisted, not absolute truth.
- Evidence retrieval may be incomplete for niche claims.

### Pending AI Work
- Train TF-IDF + Logistic Regression model on claim dataset.
- Integrate pytesseract for OCR.
- Integrate Whisper/faster-whisper for video STT.
- Implement evidence retrieval (BM25 + FAISS vector search).

### Model Status
- claim_classifier.joblib: Not yet trained/saved.
- Will be trained during Phase 2 with 80/10/10 train/val/test split.
- Expected F1 >= 0.65 on held-out test set.
# ClariFact — Technical Requirements/Design Document (TRD)

## 8.1 Architecture

The system uses a layered architecture:

```text
Frontend (React + Vite)
   ↓
Backend API (FastAPI + Python)
   ↓
AI/ML Processing Layer
   ↓
Evidence Retrieval Layer
   ↓
Database (PostgreSQL)
```

## 8.2 Recommended Technology Stack

### Frontend
- **Framework**: React 18 with Hooks
- **Build Tool**: Vite
- **Styling**: Tailwind CSS (modern, utility-first)
- **State Management**: React Query + Context API
- **Routing**: React Router
- **HTTP Client**: Fetch API or Axios

### Backend
- **Language**: Python 3.11
- **Framework**: FastAPI (automatic docs, async, validation)
- **ASGI Server**: Uvicorn
- **ORM**: SQLAlchemy 2.0
- **Database Migration**: Alembic

### AI/ML (Python Ecosystem)
- **NLP**: spaCy (Transformer models) or NLTK
- **Claim Extraction**: Rule-based + spaCy NER
- **OCR**: pytesseract or easyocr
- **Speech-to-Text**: Whisper (OpenAI) or faster-whisper
- **Computer Vision**: OpenCV, torchvision with pretrained models
- **Embedding**: sentence-transformers (all-MiniLM-L6-v2)
- **Evidence Retrieval**: BM25 + FAISS vector search

### Database
- **PostgreSQL** 15+

### ORM
- SQLAlchemy 2.0 with declarative models

### Testing
- **pytest** + pytest-asyncio
- **Coverage**: pytest-cov

### Version Control
- Git + GitHub

### Environment
- `.env` for configuration

## 8.3 System Components

### Authentication Service
- Handles user registration, login, logout.
- Issues JWT access tokens with refresh token rotation.
- Password hashing via bcrypt.
- Token validation middleware.

### Content Service
- Handles content upload validation.
- Stores content metadata and file references.
- User-owned content isolation.

### AI Analysis Service
- Orchestrates the analysis pipeline per modality.
- Coordinates claim extraction, evidence retrieval, credibility scoring.
- Returns structured analysis results.

### Claim Extraction Service
- Extracts checkable claims from preprocessed text.
- Returns claim objects with text, span, and confidence.

### Evidence Retrieval Service
- Queries evidence database or external APIs.
- Returns relevant sources with snippets.
- Supports BM25 keyword search and vector similarity.

### Credibility Assessment Service
- Takes extracted claims and evidence.
- Produces credibility score (0-100) and label.
- Assesses each claim as Supported/Partially Supported/Uncertain/Potentially Misleading.

### Content Quality Service
- Analyzes text/image/video quality characteristics.
- Returns quality metrics (readability, OCR confidence, speech clarity, etc.).

### Database Service
- CRUD operations for users, contents, analyses, claims, sources.
- Connection pooling and query optimization.

## 8.4 API Architecture

### Authentication Endpoints

| Endpoint | Method | Auth | Description |
|---|---|---|---|
| `/api/auth/register` | POST | None | Register a new user. |
| `/api/auth/login` | POST | None | Authenticate and receive JWT. |
| `/api/auth/me` | GET | JWT | Get current user profile. |
| `/api/auth/logout` | POST | JWT | Invalidate token. |

### Analysis Endpoints

| Endpoint | Method | Auth | Description |
|---|---|---|---|
| `/api/analyze` | POST | JWT | Submit content for analysis. |
| `/api/history` | GET | JWT | List user's analyses. |
| `/api/analysis/{id}` | GET | JWT | Get analysis detail and report. |

### Health Endpoint

| Endpoint | Method | Auth | Description |
|---|---|---|---|
| `/api/health` | GET | None | System health check. |

### Request/Response Conventions

- **JSON Request Bodies**: `Content-Type: application/json`
- **Authentication**: Bearer token in `Authorization: JWT <token>` header.
- **Success Responses**: `200 OK` with data, `201 Created` for resource creation.
- **Error Responses**: `400 Bad Request`, `401 Unauthorized`, `403 Forbidden`, `422 Validation Error`, `500 Internal Error`.
- **Error Format**: `{ "error": "Error message", "code": "ERROR_CODE" }`

## 8.5 Security

### Password Handling
- bcrypt with minimum 12 rounds for hashing.
- Never store or transmit plaintext passwords.
- Password validation: minimum 8 characters, mix of types.

### JWT / Session Handling
- Short-lived access tokens (15-30 min).
- Refresh token rotation to prevent reuse attacks.
- Tokens signed with HS256 using `JWT_SECRET` from environment.
- Token payload includes `sub (user_id)`, `iat`, `exp`.

### Authorization
- Every backend endpoint checks JWT `sub` against resource owner.
- Users can only access their own analyses, contents, and history.
- 403 Forbidden if user attempts to access another user's resources.

### Input Validation
- All request bodies validated via Pydantic models.
- Whitelist allowed file types for uploads.
- Sanitize all text inputs.
- Maximum payload sizes enforced.

### File Validation
- **Images**: JPEG, PNG, WebP max 10MB.
- **Videos**: MP4, WebM, MOV max 50MB, max 5 minutes duration.
- Virus scanning optional (future).
- Store files outside web root; serve via signed URLs.

### CORS
- Configured for production origin only.
- Credentials enabled if needed for cookie-based auth.

### Environment Secrets
- `JWT_SECRET`, `DATABASE_URL`, `BCRYPT_LOG_ROUNDS` in `.env`.
- Never commit `.env` to version control.

### SQL Injection Protection
- Use SQLAlchemy ORM with parameterized queries.
- Never concatenate user input into SQL strings.

### Secure File Handling
- Upload directory not accessible via browser direct URL.
- Serve files through backend endpoint with authentication check.
- File names hashed/obfuscated to prevent enumeration.

## 8.6 AI Architecture

```text
Input
  ↓
Preprocessing (clean, normalize, extract text)
  ↓
Modality-specific processing
  │
  ├── Text: claim extraction pipeline
  ├── Image: OCR → text → claim extraction
  └── Video: speech-to-text → transcript → claim extraction
  ↓
Claim Extraction
  ↓
Evidence Retrieval
  ↓
Claim Evaluation (each claim against evidence)
  ↓
Credibility Scoring
  ↓
Quality Analysis
  ↓
Report Generation (structured output)
```

### Detailed Flow

1. **Input**: User submits content (text/image/video).
2. **Preprocessing**: Normalize whitespace, detect language, extract text (OCR for images, STT for video).
3. **Modality-specific processing**:
   - **Text**: Direct text usage.
   - **Image**: pytesseract/easyocr → extracted text.
   - **Video**: Extract audio → Whisper/faster-whisper → transcript.
4. **Claim Extraction**: spaCy-based NER + rule-based pattern matching to identify checkable claims.
5. **Evidence Retrieval**: BM25 keyword matching on claim text, then FAISS vector search on claim embeddings. Retrieve top-k sources.
6. **Claim Evaluation**: For each claim, determine support level by comparing claim stance against retrieved evidence snippets. Use lightweight classifier or rule-based heuristics.
7. **Credibility Scoring**: Aggregate claim assessments into overall score (0-100) and label (e.g., "Mostly Credible", "Uncertain", "Potentially Misleading").
8. **Quality Analysis**: Compute text readability (Flesch), OCR confidence, audio quality metrics, visual quality indicators.
9. **Report Generation**: Structure output with overall credibility, claim breakdown, confidence percentage, evidence sources, and AI explanation text.

## 8.7 Model Strategy

**Do NOT train large language models from scratch.**

### Meaningful ML Components (engineer-explainable)

#### TF-IDF + Logistic Regression for Claim Classification

**Task**: Classify extracted claims into credibility categories (Supported/Partially Supported/Uncertain).

**Dataset**: 
- Synthetically generated or crowdsourced claims with ground-truth labels.
- Split: 80% training, 10% validation, 10% test.

**Preprocessing**:
- Lowercase, remove stopwords, lemmatize with spaCy.
- Extract claim features: presence of hedges ("maybe", "possibly"), factual verbs, proper nouns, numbers.

**Model**:
- `TfidfVectorizer` with ngram_range (1,2).
- `LogisticRegression` with class_weight='balanced', max_iter=1000.

**Training**:
- Fit on training claims.
- Tune with grid search on validation set.
- Evaluate on test set.

**Metrics**:
- Accuracy, Precision, Recall, F1-score (macro average).
- Expected: F1 >= 0.65 on held-out test set.

**Model Storage**:
- Save `joblib` dump: `models/claim_classifier.joblib`.
- Load at startup: `model = joblib.load("models/claim_classifier.joblib")`.

**Model Loading Note**:
- At application startup, load all required models into memory.
- Do not train models per-request.
- Models are read-only after startup.

### Other Pretrained Components (no training required)

- **spaCy `en_core_web_trf`**: Transformer-based NER for claim boundary detection.
- **sentence-transformers `all-MiniLM-L6-v2`**: Generate embeddings for evidence retrieval.
- **pytesseract**: OCR (uses system tesseract, no training).
- **faster-whisper**: Speech-to-text (pretrained on multilingual data).
- **OpenCV pretrained models**: Basic visual features (face detection, etc.).

### Model Evaluation Plan (documented, not executed in MVP)

1. Export trained model.
2. Run `python -m pytest tests/models/` to verify inference.
3. Log misclassifications for future improvement.
4. Monitor model drift in production; retrain quarterly.

**Do not leave any untrained model in production.** All ML components must have documented training pipelines or be pretrained models with known limitations.
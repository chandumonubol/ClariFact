# ClariFact — Implementation Plan (IMPLEMENTATION_PLAN.md)

## Phase 0 — Foundation

### Objective
Set up repository, documentation, environment, and base project structure.

### Tasks
- [ ] Initialize git repository and GitHub remote.
- [ ] Create directory structure (frontend, backend, ai_model, database, tests).
- [ ] Write foundational documentation: PRD.md, TRD.md, PROJECT_BRIEF.md.
- [ ] Create `agent/` context system (PROJECT_CONTEXT.md, CURRENT_STATE.md, etc.).
- [ ] Create `AGENTS.md` at repository root.
- [ ] Create `.env.example` with placeholders.
- [ ] Create `.gitignore`.
- [ ] Create `README.md`.
- [ ] Set up package.json (frontend) and poetry/requirements (backend).

### Files/Components Involved
- Root: AGENTS.md, .env.example, .gitignore, README.md
- docs/: PRD.md, TRD.md, PROJECT_BRIEF.md (already created)
- agent/: PROJECT_CONTEXT.md, CURRENT_STATE.md, DECISIONS.md, TASK_TRACKER.md, API_CONTRACT.md, DATABASE_STATE.md, AI_STATE.md, CHANGELOG.md, SESSION_HANDOFF.md
- frontend/: package.json, src/, public/, src/index.tsx
- backend/: pyproject.toml/requirements.txt, alembic.ini

### Dependencies
- None (foundation phase).

### Definition of Done
- Repository initialized with commit.
- All documentation files created and placed.
- Agent context files created.
- Environment template created.
- Gitignore in place.
- New developer can clone and understand project structure.

### Testing Requirements
- Verify all files exist at expected paths.
- Git status shows expected new files.

### Next Priority
- Phase 1 — Authentication.

---

## Phase 1 — Authentication

### Objective
Implement user registration, login, JWT-based authentication, and protected routes.

### Tasks
- [ ] Backend: User model with bcrypt password hashing.
- [ ] Backend: Register API endpoint `POST /api/auth/register`.
- [ ] Backend: Login API endpoint `POST /api/auth/login`.
- [ ] Backend: Get current user endpoint `GET /api/auth/me` (JWT protected).
- [ ] Backend: Logout endpoint `POST /api/auth/logout`.
- [ ] Backend: Authentication middleware (JWT verification).
- [ ] Frontend: Login page component.
- [ ] Frontend: Register page component.
- [ ] Frontend: Authentication state management (Context or Redux).
- [ ] Frontend: Protected route wrapper.
- [ ] Update `API_CONTRACT.md` with auth endpoints.
- [ ] Update `DECISIONS.md` with auth technology decisions.

### Files/Components Involved
- `backend/app/models.py`: User model.
- `backend/app/routes/auth.py`: Auth routes.
- `backend/app/middleware/auth.py`: JWT middleware.
- `frontend/src/pages/Login.tsx`, `Register.tsx`.
- `frontend/src/context/AuthContext.tsx`.
- `agent/DECISIONS.md`, `agent/API_CONTRACT.md`.

### Dependencies
- bcrypt (password hashing).
- PyJWT or python-jose (JWT creation/verification).
- FastAPI dependencies.

### Definition of Done
- User can register with valid name, email, password.
- User can login and receive JWT token.
- Protected endpoints return 401 if not authenticated.
- Frontend stores token, redirects to dashboard.
- Unauthenticated users cannot access dashboard.

### Testing Requirements
- Integration tests for register/login/logout.
- Unit tests for password hashing.
- Frontend: render login form, submit, verify API mock calls.

### Next Priority
- Phase 2 — Text Analysis.

---

## Phase 2 — Text Analysis

### Objective
Implement the full text analysis pipeline: preprocessing → claim extraction → evidence retrieval → credibility assessment → report generation.

### Tasks
- [ ] Backend: Text preprocessing utility (normalize, language detection).
- [ ] Backend: Claim extraction from text (spaCy-based NER + rule-based patterns).
- [ ] Backend: TF-IDF + Logistic Regression claim classification model (train + save/load).
- [ ] Backend: Evidence retrieval mock (static sources or simple keyword matching).
- [ ] Backend: Credibility scoring function (aggregate claim assessments → score + label).
- [ ] Backend: Report generation Pydantic schema and JSON output.
- [ ] Backend: `POST /api/analyze` endpoint for text content.
- [ ] Frontend: Text analysis form (textarea + button).
- [ ] Frontend: Processing overlay component.
- [ ] Frontend: Results page display (credibility score, claims, evidence, explanation).
- [ ] Frontend: Save analysis to history.
- [ ] Update `AI_STATE.md` with model status.

### Files/Components Involved
- `backend/app/services/claim_extraction.py`: Claim extraction logic.
- `backend/app/services/evidence_retrieval.py`: Evidence retrieval (mock/FISS).
- `backend/app/services/credibility.py`: Scoring logic.
- `backend/app/services/report.py`: Report generation.
- `backend/app/schemas/analysis.py`: Analysis request/response schemas.
- `backend/app/utils/preprocessing.py`: Text preprocessing.
- `ai_model/models/claim_classifier.joblib`: Trained model file.
- `frontend/src/pages/Analyze.tsx`, `Results.tsx`.

### Dependencies
- Phase 1 (authentication, database).
- spaCy `en_core_web_trf` model.
- scikit-learn (TF-IDF, Logistic Regression).
- sentence-transformers (embeddings for evidence).

### Definition of Done
- User can submit text content via frontend.
- Backend extracts claims from text.
- Backend retrieves evidence (mock sources returned).
- Backend produces credibility score (0-100) and label.
- Frontend displays results: score, assessment label, claim breakdown, confidence, explanation, evidence sources.
- Analysis is saved user-specifically.
- History listing works.

### Testing Requirements
- Unit tests for claim extraction accuracy (known test claims).
- Unit tests for credibility scoring function.
- Unit tests for report generation schema.
- Integration test: submit text → receive analysis result.
- Model evaluation: F1 score on held-out test claims >= 0.65.

### Next Priority
- Phase 3 — Image Analysis.

---

## Phase 3 — Image Analysis

### Objective
Implement image upload, OCR, and the image analysis pipeline.

### Tasks
- [ ] Backend: File upload endpoint with validation (type, size).
- [ ] Backend: OCR utility using pytesseract/easyocr.
- [ ] Backend: Fallback for images with little or no text.
- [ ] Backend: Claim extraction from OCR-extracted text.
- [ ] Backend: Evidence retrieval for image claims.
- [ ] Backend: Visual analysis basic properties (format, dimensions, hash).
- [ ] Backend: Full image analysis pipeline endpoint.
- [ ] Frontend: Image upload form (file input + preview).
- [ ] Frontend: Processing overlay with modality-specific text ("OCR in progress...").
- [ ] Frontend: Results display for image analysis.
- [ ] Update `AI_STATE.md` with OCR status.

### Files/Components Involved
- `backend/app/services/ocr.py`: OCR processing.
- `backend/app/services/image_analysis.py`: Image pipeline.
- `frontend/src/components/FileInput.tsx`, `ImagePreview.tsx`.
- `frontend/src/pages/Analyze.tsx` (Image tab).

### Dependencies
- Phase 1 (auth, database).
- pytesseract or easyocr package.
- tesseract-ocr installed on server (system dependency).

### Definition of Done
- User can upload an image file.
- Backend validates format and size.
- OCR extracts text (or graceful fallback).
- Claims extracted from OCR text or visual analysis provided.
- Credibility assessment produced.
- Results displayed with appropriate disclaimers for low-text images.

### Testing Requirements
- Unit tests for OCR on sample images.
- Unit tests for fallback behavior (no-text image).
- Integration test: upload image → receive analysis.
- Verify file size/rejection errors.

### Next Priority
- Phase 4 — Video Analysis.

---

## Phase 4 — Video Analysis

### Objective
Implement video upload, audio extraction, speech-to-text, and full video analysis pipeline.

### Tasks
- [ ] Backend: Video upload endpoint with validation (type, size, duration).
- [ ] Backend: Audio extraction utility (ffmpeg integration).
- [ ] Backend: Speech-to-text via Whisper/faster-whisper.
- [ ] Backend: Transcript generation and claim extraction.
- [ ] Backend: Frame sampling (key frames every 10s or 5% duration).
- [ ] Backend: Visual analysis of sampled frames.
- [ ] Backend: Content quality analysis (speech clarity, engagement).
- [ ] Backend: Full video analysis pipeline endpoint.
- [ ] Frontend: Video upload form (file input + duration display).
- [ ] Frontend: Processing overlay with stages (audio extraction → STT → analysis).
- [ ] Frontend: Results page for video analysis.

### Files/Components Involved
- `backend/app/services/stt.py`: Speech-to-text.
- `backend/app/services/video_analysis.py`: Video pipeline.
- `backend/utils/ffmpeg.sh` or integration.
- `frontend/src/pages/Analyze.tsx` (Video tab).

### Dependencies
- Phase 1 (auth, database).
- ffmpeg (system dependency).
- Whisper/faster-whisper model.
- OpenCV (frame processing).

### Definition of Done
- User can upload a short video (<5 min, <50MB).
- Backend extracts audio and transcribes speech.
- Claims extracted from transcript.
- Frame sampling and basic visual analysis performed.
- Credibility assessment and quality metrics produced.
- Results displayed with all sections (credibility, claims, quality, evidence).

### Testing Requirements
- Unit tests for STT on sample audio.
- Integration test: upload video → full analysis result.
- Verify duration/size rejection errors.
- Frame sampling correctness (key frames at correct timestamps).

### Next Priority
- Phase 5 — Database and History.

---

## Phase 5 — Database and History

### Objective
Ensure persistent storage, user-specific ownership, and history/detail views.

### Tasks
- [ ] Apply Alembic migrations to create database schema.
- [ ] Implement user-content-analysis ownership flow.
- [ ] Backend: GET /api/history endpoint (user's analyses list).
- [ ] Backend: GET /api/analysis/{id} endpoint (detail view).
- [ ] Frontend: Dashboard history section.
- [ ] Frontend: Analysis detail page navigation.
- [ ] Frontend: Delete analysis functionality.
- [ ] Update `DATABASE_STATE.md` with applied migrations.

### Files/Components Involved
- `backend/app/database/models.py`: SQLAlchemy models.
- `backend/app/database/migrations/`: Alembic scripts.
- `backend/app/routes/history.py`, `analysis.py`.
- `frontend/src/pages/Dashboard.tsx`, `HistoryDetail.tsx`.

### Dependencies
- Phases 1-4 (all authentication and analysis functionality).

### Definition of Done
- Database tables created via migrations.
- User can view their analysis history.
- Clicking an analysis opens detail view with full report.
- User can delete their own analyses (not others').
- Ownership enforced at backend API level.

### Testing Requirements
- Integration tests for history listing.
- Integration tests for analysis detail by ID.
- Verify unauthorized access returns 403.
- Verify cross-user access is blocked.

### Next Priority
- Phase 6 — Dashboard and UI refinement.

---

## Phase 6 — Dashboard and UI Refinement

### Objective
Polish UI, add navigation, improve UX, implement all pages.

### Tasks
- [ ] Implement all frontend pages: Landing, Login, Register, Dashboard, Analyze (tabs), Results, History, Analysis Detail.
- [ ] Add topbar/navigation menu.
- [ ] Implement responsive design (mobile/tablet/desktop).
- [ ] Add loading states, error states, empty states.
- [ ] Implement accessibility features (focus outlines, alt text, ARIA).
- [ ] Refine results UI per UI_UX_DESIGN.md spec.
- [ ] Add dark mode support (optional, future).
- [ ] Update `CURRENT_STATE.md` with UI status.

### Files/Components Involved
- All `frontend/src/pages/*.tsx`.
- `frontend/src/components/*.tsx`.
- `frontend/src/context/*.tsx`.
- `docs/UI_UX_DESIGN.md` for reference.

### Dependencies
- All previous phases (auth + analysis pipelines must work first).

### Definition of Done
- Full frontend application functional.
- Navigation between all pages works.
- Results UI matches UI_UX_DESIGN.md specification.
- Accessible (basic WCAG compliance).
- Responsive across breakpoints.

### Testing Requirements
- Visual regression (manual) across breakpoints.
- Screen reader testing (basic).
- Unit tests for UI components (optional).

### Next Priority
- Phase 7 — Testing.

---

## Phase 7 — Testing

### Objective
Write comprehensive tests, fix bugs, ensure quality.

### Tasks
- [ ] Backend: pytest unit tests for all services/models/routes.
- [ ] Backend: pytest integration tests for API endpoints (auth, analyze, history).
- [ ] Backend: Model evaluation (claim classifier F1 >= 0.65).
- [ ] Frontend: React component tests (render, user interactions).
- [ ] End-to-end: Cypress or Playwright basic flows (register → analyze → results).
- [ ] Fix all bugs found during testing.
- [ ] Achieve >= 80% test coverage (or agreed threshold).
- [ ] Update `CHANGELOG.md` with test-related changes.

### Files/Components Involved
- `backend/tests/unit/`: Unit test files.
- `backend/tests/integration/`: Integration test files.
- `frontend/tests/`: Component test files.
- `tests/e2e/`: E2E test files.

### Dependencies
- All previous phases completed.

### Definition of Done
- All critical paths tested (auth, text analysis, image analysis, video analysis).
- No blocking bugs.
- Coverage target met.

### Next Priority
- Phase 8 — Final integration.

---

## Phase 8 — Final Integration

### Objective
Final integration, performance tuning, documentation update.

### Tasks
- [ ] Performance profiling (analysis timing per modality).
- [ ] Security review (headers, CORS, secrets management).
- [ ] Final documentation sync (all docs match implementation).
- [ ] Update `AGENTS.md`, `CURRENT_STATE.md`, `TASK_TRACKER.md`, `CHANGELOG.md`.
- [ ] Create demo script (register → analyze text/image/video → view history).
- [ ] Prepare deployment configuration (Docker, environment production values).

### Files/Components Involved
- All files across project.
- `Dockerfile` (optional).
- `docker-compose.yml` (optional).

### Dependencies
- All previous phases.

### Definition of Done
- System runs end-to-end.
- Documentation synchronized with implementation.
- Agent context files up to date.

### Next Priority
- Phase 9 — Documentation and Demo.

---

## Phase 9 — Documentation and Demo

### Objective
Finalize all documentation, prepare for hand-off.

### Tasks
- [ ] Verify all 7 PRD documents exist and are consistent.
- [ ] Update `PROJECT_CONTEXT.md` with final state.
- [ ] Update `CURRENT_STATE.md` with "All phases complete".
- [ ] Update `TASK_TRACKER.md` with all tasks checked off.
- [ ] Update `CHANGELOG.md` with full project history.
- [ ] Prepare demo data and walkthrough.
- [ ] Write CONTRIBUTING.md if not already created.
- [ ] Tag release version.

### Definition of Done
- All documentation complete and synchronized.
- Demo ready for stakeholder review.
- Repository in stable state on main branch.
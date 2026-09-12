# ClariFact — Execution Plan (Single Source of Truth)

## Project Overview
Authenticated web app that assesses credibility of user-submitted **text, image, and short-video** content. Pipeline: preprocess → extract claims → retrieve evidence → assess claims → score credibility + confidence + content quality → generate explainable report → persist to user history. Four-member parallel development, contract-driven, checkpoint-based merges. Never outputs binary TRUE/FALSE; never fabricates evidence.

## Tech Stack
| Layer | Choice | Status |
|---|---|---|
| Frontend | React + Vite | Framework family confirmed; exact version → **ND-17** |
| Backend | Python + FastAPI | Confirmed (unless repo already implemented Flask — check repo first) |
| Database | PostgreSQL + SQLAlchemy | Confirmed |
| Migrations | Alembic (implied by SQLAlchemy+Postgres) | Confirmed convention |
| Auth | JWT + bcrypt | Confirmed |
| Testing | pytest | Confirmed |
| AI/ML core | Python, scikit-learn, spaCy/NLTK | Confirmed |
| ML classifier | TF-IDF + Logistic Regression | Direction confirmed; task/dataset → **ND-02/03/04/05** |
| OCR | — | **ND-10** |
| Speech-to-text | — | **ND-11** |
| Computer vision (frames) | — | **ND-12** |
| Evidence/source provider | — | **ND-01** |
| VCS | Git + GitHub, feature branches → main via PR | Confirmed |

---

## Needs Decision (blocking — do not silently guess)
Agents must implement affected components behind a **pluggable interface + documented mock**, per Mock-First principle, and record the ND-ID in code comments + `agent/DECISIONS.md` until resolved.

| ID | Open Item |
|---|---|
| ND-01 | Evidence/source retrieval provider or API |
| ND-02 | ML dataset |
| ND-03 | ML classification task + target labels |
| ND-04 | ML hyperparameters (C, solver, max_features, n-grams, split, seed) |
| ND-05 | ML evaluation metrics/results |
| ND-06 | Credibility scoring formula + factor weights |
| ND-07 | Credibility label thresholds (score → label mapping) |
| ND-08 | Confidence formula/calibration method |
| ND-09 | Content-quality formula/weights (incl. "Engagement Indicators") |
| ND-10 | OCR engine/model |
| ND-11 | Speech-to-text engine/model |
| ND-12 | Computer-vision model for frame/visual analysis |
| ND-13 | Video limits: MAX_UPLOAD_SIZE, MAX_DURATION, supported formats |
| ND-14 | Frame sampling strategy (interval/count/key-frame method) |
| ND-15 | Exact API request/response JSON schemas (endpoint names only are fixed) |
| ND-16 | Evidence/source DB table schema |
| ND-17 | Exact frontend framework version |
| ND-18 | Sentiment analysis — include as feature or drop (currently secondary) |

---

## Fixed Contracts (do not re-decide)
- **API endpoints:** `POST /api/auth/register`, `POST /api/auth/login`, `GET /api/auth/me`, `POST /api/auth/logout`, `POST /api/analyze`, `GET /api/history`, `GET /api/analysis/{id}`, `GET /api/health`
- **AI interface:** `analyze_text(text)`, `analyze_image(image)`, `analyze_video(video)` — backend must not depend on AI internals
- **Credibility labels:** `Supported | Partially Supported | Uncertain | Potentially Misleading`
- **Result fields (conceptual, refine in API_CONTRACT.md):** `credibility_score, credibility_label, confidence, claims[], quality{}, sources[], explanation`
- **DB tables (minimum):** `users, contents, analyses, claims` (+ evidence/sources per ND-16)
- **Agent context files:** `agent/PROJECT_CONTEXT.md, CURRENT_STATE.md, DECISIONS.md, TASK_TRACKER.md, API_CONTRACT.md, DATABASE_STATE.md, AI_STATE.md, CHANGELOG.md, SESSION_HANDOFF.md`

---

## Phase 0 — Setup (parallel, no dependencies)

| ID | Task | Scope | Output | Depends | Acceptance |
|---|---|---|---|---|---|
| T-00-REPO | Init repo structure | Create top-level dirs: `frontend/ backend/ ai_model/ database/ tests/ docs/ agent/`; `.gitignore` | Empty scaffolded repo | — | All dirs exist; repo builds/clones cleanly |
| T-00-AGENT | Agent context skeleton | Create all 9 `agent/*.md` files with headers only | Skeleton files | T-00-REPO | Files exist with correct headers per Fixed Contracts |
| T-00-ENV | Env template | Create `.env.example` with `DATABASE_URL, JWT_SECRET, SECRET_KEY, AI_MODEL_PATH, UPLOAD_DIR, MAX_UPLOAD_SIZE` | `.env.example` | T-00-REPO | No real secrets; all vars documented in README |

---

## Phase 1 — Checkpoint 1: Foundation (4 tracks, run in parallel)

### Backend
| ID | Task | Scope | Input→Output | Depends | Acceptance |
|---|---|---|---|---|---|
| T-BE-01 | Backend skeleton | FastAPI app w/ `config/ routes/ controllers/ services/ middleware/ schemas/ utils/` | Repo→runnable app | T-00-REPO | `GET /api/health` returns 200 |
| T-BE-02 | Auth endpoints | Register/login/me/logout; bcrypt hashing, JWT issuance | Request/JSON→token/user | T-BE-01, T-DB-02 | Register→login→access `/me` w/ token works; wrong password rejected |
| T-BE-03 | Draft API_CONTRACT.md | Document all 8 endpoints: request/response shape, auth header, error format | — → `agent/API_CONTRACT.md` | T-BE-01 | Frontend/AI can build against it without asking backend questions |

### AI
| ID | Task | Scope | Input→Output | Depends | Acceptance |
|---|---|---|---|---|---|
| T-AI-01 | AI module skeleton | Implement `analyze_text/image/video` returning mock data matching result schema | text/image/video → mock JSON | T-BE-03 | Backend can call these and get contract-shaped output |
| T-AI-02 | Text preprocessing | Clean, normalize, tokenize, sentence-split, keyword extract; must not strip factual content | raw text → structured tokens/sentences | T-AI-01 | Unit tests pass on sample sentences incl. edge cases (empty, punctuation-only) |

### Frontend
| ID | Task | Scope | Input→Output | Depends | Acceptance |
|---|---|---|---|---|---|
| T-FE-01 | Frontend scaffold | React+Vite app, routing, base layout, component folder per spec (`Navbar, Button, Input, LoadingState, ErrorMessage, EmptyState`) | — → running dev app | T-BE-03 | App boots; routes render placeholder pages |
| T-FE-02 | Register page | Form + validation, calls `/api/auth/register` (mock ok) | form → API call | T-FE-01 | Valid submit succeeds; invalid shows errors |
| T-FE-03 | Login page | Form + validation, calls `/api/auth/login`, stores auth state | form → auth token stored | T-FE-01 | Login persists session; logout clears it |
| T-FE-04 | Analysis input UI (text) | Text input + submit, uses mock API response | text → mock result | T-FE-01 | Submitting text renders a mock result without errors |

### Database
| ID | Task | Scope | Input→Output | Depends | Acceptance |
|---|---|---|---|---|---|
| T-DB-01 | DB foundation | Postgres connection config, SQLAlchemy engine/session, Alembic init | — → connected DB | T-00-ENV | `alembic upgrade head` runs clean on fresh DB |
| T-DB-02 | Core models | `users, contents, analyses, claims` per documented schema + FKs | Schema → migration | T-DB-01 | Migration creates all tables with correct FKs/constraints |
| T-DB-03 | Test framework | pytest config, fixtures, isolated test DB/transaction rollback | — → test scaffold | T-DB-01 | `pytest` runs a trivial passing test against test DB |

### Merge
| ID | Task | Depends | Acceptance |
|---|---|---|---|
| T-INT-01 | Checkpoint 1 merge | T-BE-02, T-AI-02, T-FE-04, T-DB-03 | All 4 branches merge to `main` with no conflicts; smoke test (register+login+load dashboard shell) passes |

---

## Phase 2 — Checkpoint 2: Text Complete (first full vertical slice)

| ID | Task | Scope | Input→Output | Depends | Acceptance |
|---|---|---|---|---|---|
| T-AI-03 | Claim extraction | Classify sentences: checkable claim / opinion / question / instruction / general | tokens → labeled claims | T-AI-02 | Correctly separates claims vs. opinions on test set of ≥20 sentences |
| T-AI-04 | Evidence retrieval interface | Pluggable retrieval layer; mock provider until ND-01 resolved | claim → evidence list (mock) | T-AI-03 | Swapping mock→real provider requires no caller changes |
| T-AI-05 | Claim assessment | Map claim+evidence → one of 4 labels; return `Uncertain` if evidence insufficient (never fabricate) | claim+evidence → label | T-AI-04 (ND-06,07 blocking final logic) | No claim is labeled Supported without evidence present |
| T-AI-06 | Credibility scoring | Aggregate claim assessments → overall score | claims[] → score | T-AI-05 (ND-06,07) | Score deterministic for fixed input; documented formula in `AI_STATE.md` |
| T-AI-07 | Confidence calculation | Separate from credibility score | assessment → confidence % | T-AI-05 (ND-08) | Confidence and credibility can diverge (unit test) |
| T-AI-08 | Content quality (text) | Score clarity/relevance/completeness/language quality | text → quality{} | T-AI-02 (ND-09) | Quality score independent of credibility score (unit test) |
| T-AI-09 | TF-IDF+LogReg classifier | Train/load model per ND-02–05; document per Definition of Done | text → classification | T-AI-02 (ND-02,03,04,05 blocking training) | No untrained/random model ships to prod path; if blocked, stub clearly logs "placeholder model" |
| T-BE-04 | `POST /api/analyze` (text) | Validate input, call AI module, persist result | text → analysis record | T-BE-02, T-AI-06, T-DB-04 | End-to-end: submit text → row in `analyses`+`claims` |
| T-BE-05 | History/detail endpoints | `GET /api/history`, `GET /api/analysis/{id}` with ownership check | user token → own analyses only | T-BE-04 | User B gets 403/404 on User A's analysis id |
| T-DB-04 | CRUD services | Create/read for contents/analyses/claims w/ ownership enforcement | — → service layer | T-DB-02 | Ownership violation raises before DB query executes |
| T-FE-05 | Dashboard page | Post-login landing, links to analyze/history | — → page | T-FE-03 | Renders after login; redirects if unauthenticated |
| T-FE-06 | Processing/loading UI | Uses `LoadingState` component during analysis call | — → UI state | T-FE-04 | Shown during real API latency, not just instantly |
| T-FE-07 | Results page | Displays score, label, confidence, claims, evidence, quality, explanation; must not visually imply guaranteed truth | analysis JSON → rendered page | T-BE-04 | Renders all fields from contract; no "100% true" language/visuals |
| T-FE-08 | History + Detail pages | List + drill-down view | — → pages | T-BE-05 | Only shows logged-in user's own analyses |
| T-QA-01 | Backend test suite | Health, register, login, protected route, invalid auth, submission, unauthorized access, history, detail, invalid input | — → passing tests | T-BE-05 | All listed cases covered and passing |
| T-QA-02 | AI test suite | Preprocessing, claim extraction, credibility, confidence, scoring, empty/invalid input | — → passing tests | T-AI-07 | Deterministic; no hard dependency on live external APIs |
| T-INT-02 | Checkpoint 2 merge | Full slice: register→login→dashboard→text→AI→result→DB→history | T-QA-01, T-QA-02, T-FE-08 | Full user journey passes manually + in e2e test |

---

## Phase 3 — Checkpoint 3: Image Complete

| ID | Task | Scope | Depends | Acceptance |
|---|---|---|---|---|
| T-AI-10 | OCR integration | Extract text from image; graceful handling of no/low text, poor quality, unsupported format | T-INT-02 (ND-10) | No crash on blank/corrupt image; returns empty-claims result instead |
| T-AI-11 | Image claim extraction | Reuse T-AI-03 pipeline on OCR output | T-AI-10 | Same acceptance as T-AI-03 applied to OCR text |
| T-AI-12 | Image visual analysis | Basic quality metrics (resolution, clarity) | T-AI-10 | Returns quality metrics without crashing on edge-case images |
| T-BE-06 | Image upload endpoint | Multipart upload, MIME/size/format validation | T-BE-04 | Rejects oversized/unsupported files with correct error code |
| T-FE-09 | Image upload UI | `FileUploader` component, preview, error states | T-FE-07 | Upload → processing → results flow works for valid and invalid files |
| T-QA-03 | Image test suite | OCR success/failure, no-text image, unsupported format | T-AI-12, T-BE-06 | All cases pass; no unhandled exceptions |
| T-INT-03 | Checkpoint 3 merge | Full image vertical slice | T-QA-03, T-FE-09 | Manual + automated image flow passes |

---

## Phase 4 — Checkpoint 4: Video Complete

| ID | Task | Scope | Depends | Acceptance |
|---|---|---|---|---|
| T-AI-13 | Audio extraction | Extract audio track from short video | T-INT-03 | Produces audio file/stream from valid video input |
| T-AI-14 | Speech-to-text | Transcript from audio | T-AI-13 (ND-11) | Transcript returned for sample video; empty-audio handled gracefully |
| T-AI-15 | Video claim extraction | Reuse T-AI-03 on transcript | T-AI-14 | Same acceptance as T-AI-03 |
| T-AI-16 | Frame sampling | Sample frames per strategy | T-INT-03 (ND-14) | Deterministic frame count/selection given fixed video+config |
| T-AI-17 | Frame/visual analysis | CV-based visual quality/analysis on sampled frames | T-AI-16 (ND-12) | Returns visual analysis without crash on short/corrupt video |
| T-BE-07 | Video upload endpoint | Configurable limits enforced | T-BE-06 (ND-13) | Rejects video exceeding configured size/duration with correct error |
| T-FE-10 | Video upload UI | Upload + processing states | T-FE-09 | Full upload→processing→results flow works |
| T-QA-04 | Video test suite | Transcript extraction, frame processing, limit enforcement | T-AI-17, T-BE-07 | All cases pass |
| T-INT-04 | Checkpoint 4 merge | Full multimodal integration | T-QA-04, T-FE-10 | Text+image+video all functional end-to-end on `main` |

---

## Phase 5 — Final Checkpoint: Bug Fix / Integration / Polish (no new features)

| ID | Task | Scope | Depends | Acceptance |
|---|---|---|---|---|
| T-QA-05 | Full regression suite | Auth, text, image, video, results, history, error handling | T-INT-04 | All prior test suites pass together on `main` |
| T-QA-06 | Security pass | Ownership isolation, no committed secrets, no plaintext passwords, no hardcoded creds | T-INT-04 | User A cannot access User B's data via any endpoint (tested) |
| T-FE-11 | Error/empty states | Apply `ErrorMessage`/`EmptyState` across all pages | T-INT-04 | No unhandled blank/broken states in manual walkthrough |
| T-FE-12 | UI polish | Typography (Athelas+Vanguard, documented fallback if unlicensed), responsive/accessibility pass | T-QA-05 | Passes basic responsive + a11y checklist |
| T-DOC-01 | Finalize agent/ state files | Update `CURRENT_STATE.md, DECISIONS.md, AI_STATE.md, DATABASE_STATE.md, CHANGELOG.md` to reflect actual implementation | T-QA-05 | Files match real repo state, not stale planning |
| T-DOC-02 | README + CONTRIBUTING | Setup, run, test, env vars, team responsibilities, current status | T-DOC-01 | New dev can set up project from README alone |
| T-DOC-03 | Demo prep | Script covering full flow across all 3 content types | T-QA-05 | Demo runs without live bugs |

---

## Working Rules for Agents
1. Read `AGENTS.md` → `agent/PROJECT_CONTEXT.md` → `agent/CURRENT_STATE.md` → `agent/TASK_TRACKER.md` → relevant state file → this plan's relevant task. Do not scan whole repo.
2. Never resolve an ND-item by guessing — implement behind an interface, log the ND-ID, keep mock.
3. Update `TASK_TRACKER.md` and `CHANGELOG.md` after each completed task.
4. Never output binary TRUE/FALSE or imply guaranteed truth in any UI/copy.
5. Never fabricate evidence/sources — return `Uncertain` instead.
6. Definition of Done = implementation + validation + error handling + passing tests + docs + updated state files (AI tasks also need: structured output, uncertainty handling, model/dataset docs, limitations).

<<<<<<< HEAD
# ClariFact
=======
# ClariFact

**AI-Powered Multimodal Content Credibility Analysis System**

ClariFact allows authenticated users to submit text, images, or short videos for AI-assisted credibility and content analysis. The system extracts checkable claims, retrieves evidence, and produces explainable credibility assessments with scores, claim breakdowns, and evidence sources — without claiming to determine absolute truth.

## Features (MVP)
- User authentication (register, login, logout, protected dashboard)
- Text analysis pipeline
- Image analysis pipeline (OCR → claims → credibility)
- Video analysis pipeline (STT → claims → credibility)
- Analysis history with detail view
- Credibility scoring (0-100) with claim-level breakdown
- Explainable reports with evidence sources

## Architecture
- **Frontend**: React 18 + Vite + Tailwind CSS
- **Backend**: FastAPI + Python 3.11 + SQLAlchemy 2.0
- **AI/ML**: spaCy, sentence-transformers, TF-IDF + Logistic Regression, pytesseract/Whisper
- **Database**: PostgreSQL 15+
- **Testing**: pytest

## Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- PostgreSQL 15+
- Tesseract OCR (system: `apt-get install tesseract-ocr`)

### Backend
```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # edit with your values
alembic upgrade head
uvicorn app.main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

### Environment
See `.env.example` for required variables. Never commit real secrets.

## Team Responsibilities
- **Member 1 (Backend/Project Lead)**: Backend API, authentication, integration, system architecture.
- **Member 2 (AI/ML)**: NLP, claim extraction, credibility, evidence analysis, image/video AI processing.
- **Member 3 (Frontend/UX)**: Pages, components, forms, dashboard, results, authentication UI.
- **Member 4 (Database/Testing/QA)**: Database, tests, integration testing, quality assurance.

## Documentation
All detailed documentation is in `docs/`:
- `PRD.md` — Product requirements
- `TRD.md` — Technical design
- `APP_FLOW.md` — User flows
- `UI_UX_DESIGN.md` — UI specifications
- `PROJECT_BRIEF.md` — Concise project summary
- `BACKEND_SCHEMA.md` — Database schema
- `IMPLEMENTATION_PLAN.md` — Phased development plan

See `AGENTS.md` for the operating manual for AI coding agents.

## Current Status
Foundation setup complete. See `agent/CURRENT_STATE.md` for current phase and next priorities.
>>>>>>> master

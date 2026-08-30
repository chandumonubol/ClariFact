# ClariFact — Project Context (Quick Reference)

## Project Identity
- **Name**: ClariFact
- **Full Title**: ClariFact — AI-Powered Multimodal Content Credibility Analysis System
- **Objective**: Allow authenticated users to submit text, images, or short videos for AI-assisted credibility and content analysis with explainable reports.

## Architecture
- **Layered**: Frontend → Backend API → AI/ML Processing Layer → Evidence Retrieval Layer → PostgreSQL Database
- **Modular**: Four team members — Backend Lead, AI/ML, Frontend/UX, Database/QA.

## Technology Stack
- **Frontend**: React 18 + Vite + Tailwind CSS
- **Backend**: FastAPI + Python 3.11 + SQLAlchemy 2.0
- **AI/ML**: spaCy, sentence-transformers, pytesseract/easyocr, Whisper/faster-whisper, TF-IDF + Logistic Regression
- **Database**: PostgreSQL 15+
- **Testing**: pytest

## Input Types
- Text: pasted/typed content
- Image: JPEG, PNG, WebP max 10MB
- Video: MP4, WebM, MOV max 50MB, 5 minutes max

## Core Features (MVP)
- User auth (register/login/logout, JWT, protected routes)
- Text analysis pipeline
- Image analysis pipeline (OCR → claims → credibility)
- Video analysis pipeline (STT → claims → credibility)
- Analysis history with detail view
- Credibility scoring (0-100) with claim-level breakdown
- Explainable reports with evidence sources

## Important Rules
- AI assessment is not absolute truth — it is AI-assisted credibility.
- Credibility ≠ Content Quality (distinguished in UI and logic).
- Claim assessments: Supported / Partially Supported / Uncertain / Potentially Misleading.
- Never store plaintext passwords.
- Users can only access their own analyses.
- OCR/STT may fail gracefully — provide meaningful response, not crash.

## Folder Structure (Top-Level)
```
ClariFact/
├── docs/ (7 documents)
├── agent/ (context state files)
├── frontend/
├── backend/
├── ai_model/
├── database/
├── tests/
├── AGENTS.md
├── .env.example
├── .gitignore
└── README.md
```

## Key Links
- PRD.md: Full product requirements
- TRD.md: Technical design
- APP_FLOW.md: User flows
- UI_UX_DESIGN.md: UI specifications
- BACKEND_SCHEMA.md: Database schema
- IMPLEMENTATION_PLAN.md: Phased plan
- AGENTS.md: Agent operating manual
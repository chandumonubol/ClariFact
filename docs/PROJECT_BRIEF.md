# ClariFact — Project Brief

## One-Paragraph Description
ClariFact is an AI-powered multimodal content credibility analysis system that allows authenticated users to submit text, images, or short videos for AI-assisted credibility and content analysis. The system extracts checkable claims, retrieves supporting or contradicting evidence, and produces explainable credibility assessments with scores, claim breakdowns, and evidence sources — without claiming to determine absolute truth.

## Problem
Internet users encounter misinformation, misleading claims, and unsupported statements daily. Verifying content credibility is difficult, time-consuming, and often requires technical expertise. Current solutions either provide binary "true/false" outputs without reasoning, or require manual research. There is no unified tool handling text, images, and videos with explainable assessments.

## Solution
ClariFact processes submitted content through a modular pipeline: preprocessing → modality-specific text extraction (OCR for images, STT for video) → claim extraction → evidence retrieval → credibility assessment → quality analysis → explainable report. The system distinguishes content quality from credibility and provides claim-level assessments (Supported/Partially Supported/Uncertain/Potentially Misleading) with full explanations and evidence sources.

## Target Users
- Students verifying essay sources
- Researchers assessing claim credibility
- General internet users checking viral content
- Educators teaching media literacy
- Content consumers wanting to understand trustworthiness

## Inputs
- Text content (pasted or typed)
- Image files (JPEG, PNG, WebP, max 10MB)
- Short video files (MP4, WebM, MOV, max 50MB, 5 minutes max)

## Outputs
- Overall credibility score (0-100) with label
- Claim-level assessments (Supported/Partially Supported/Uncertain/Potentially Misleading)
- Confidence percentage
- Content quality metrics
- Evidence sources with snippets
- AI explanation of assessment
- User-specific analysis history

## Main Features
- User authentication (register, login, logout, protected dashboard)
- Text, image, and video analysis pipelines
- Claim extraction and classification
- Evidence retrieval and presentation
- Credibility scoring with explanations
- Content quality analysis
- Analysis history and detail view
- User-owned data isolation

## Technology Stack
- **Frontend**: React + Vite + Tailwind CSS
- **Backend**: FastAPI + Python + SQLAlchemy + PostgreSQL
- **AI/ML**: spaCy, sentence-transformers, pytesseract, Whisper/faster-whisper, TF-IDF + Logistic Regression
- **Database**: PostgreSQL
- **Testing**: pytest
- **Version Control**: Git + GitHub

## Architecture Summary
Layered architecture: Frontend → Backend API → AI/ML Processing Layer → Evidence Retrieval Layer → Database. All analyses belong to authenticated users; user data is isolated. Modular design enables parallel development by four team members (Backend Lead, AI/ML, Frontend/UX, Database/QA).

## Important Constraints
- MVP supports English claims only (additional languages future).
- Image OCR accuracy depends on image quality.
- Video transcription accuracy depends on audio quality.
- Credibility is an assessment, not absolute truth.
- Maximum video: 5 minutes, 50MB.
- Maximum image: 10MB.
- No training of large models from scratch.

## What NOT to Build (MVP)
- Browser extension.
- Mobile application.
- Advanced deepfake detection.
- Real-time video processing.
- Multi-language claim extraction.
- Social media integration.
- Collaborative analysis features.

## Documentation Links
- PRD.md: Full product requirements
- TRD.md: Technical design and architecture
- APP_FLOW.md: User flows
- UI_UX_DESIGN.md: UI specifications
- BACKEND_SCHEMA.md: Database schema
- IMPLEMENTATION_PLAN.md: Phased development plan
- AGENTS.md: Agent operating manual
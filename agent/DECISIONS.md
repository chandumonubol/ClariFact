## Decision 001

Date: 2026-08-30
Decision: PostgreSQL as the database.
Reason: Relational structure fits users, analyses, claims, and sources with proper constraints and relationships. Supports cascades for ownership cleanup.
Alternatives: MongoDB (document-style, less suitable for structured claims/evidence relationships).
Status: Accepted

## Decision 002

Date: 2026-08-30
Decision: FastAPI + Python for backend.
Reason: Modern, automatic OpenAPI docs, async support, Pydantic validation, beginner-friendly.
Alternatives: Flask (simpler but less built-in), Node.js (different ecosystem).
Status: Accepted

## Decision 003

Date: 2026-08-30
Decision: TF-IDF + Logistic Regression for claim classification (not training LLM from scratch).
Reason: Engineer-explainable, small footprint, decent baseline metrics, uses scikit-learn.
Alternatives: BERT-based classifiers (heavy, overkill for MVP), rule-based only (limited accuracy).
Status: Accepted

## Decision 004

Date: 2026-08-30
Decision: Claim assessments: Supported / Partially Supported / Uncertain / Potentially Misleading (no "FALSE" binary).
Reason: Aligns with product principle of explainable assessment, not binary true/false.
Alternatives: True/False only (contradicts product requirements).
Status: Accepted

## Decision 005

Date: 2026-08-30
Decision: Maximum video duration 5 minutes, max size 50MB. Max image size 10MB.
Reason: Practical limits for short video analysis, prevents resource exhaustion.
Alternatives: Unlimited (would break frontend/backend), 10 min/100MB (too large for MVP).
Status: Accepted
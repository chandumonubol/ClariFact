# Database State

## Tables Exists
- users (id, name, email, password_hash, created_at, updated_at)
- contents (id, user_id, content_type, text_content, file_path, created_at)
- analyses (id, content_id, overall_credibility_score, credibility_label, confidence, quality_score, status, created_at, updated_at)
- claims (id, analysis_id, claim_text, assessment, confidence, explanation)
- sources (id, analysis_id, source_name, source_url, snippet, retrieval_method, retrieved_at)

## Relationships
- users 1:N contents (owner)
- users 1:N analyses (owner)
- contents 1:N analyses (via content_id)
- analyses 1:N claims (parent analysis)
- analyses 1:N sources (parent analysis)

## Indexes Applied
- idx_users_email (UNIQUE)
- idx_contents_user_id
- idx_analyses_content_id
- idx_analyses_created_at
- idx_claims_analysis_id
- idx_sources_analysis_id
- idx_sources_retrieval_method

## Migrations Applied
- 001_init_schema.py (creates all 5 tables)

## Still Missing
- Refresh tokens table (Phase 1)
- Migration for adding claim classifier model reference
- Production PostgreSQL deployment
- Full text search indexes

## Current Phase
Phase 0 — Foundation
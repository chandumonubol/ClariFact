# ClariFact — Backend Schema Documentation (BACKEND_SCHEMA.md)

## Database: PostgreSQL

### 1. `users` Table

| Field | Type | Constraints | Description |
|---|---|---|---|
| `id` | SERIAL | PRIMARY KEY | Unique user identifier. |
| `name` | VARCHAR(100) | NOT NULL | User's display name. |
| `email` | VARCHAR(255) | UNIQUE, NOT NULL | User's email address. |
| `password_hash` | VARCHAR(255) | NOT NULL | bcrypt hashed password. |
| `created_at` | TIMESTAMP WITH TIME ZONE | DEFAULT NOW(), NOT NULL | Account creation timestamp. |
| `updated_at` | TIMESTAMP WITH TIME ZONE | DEFAULT NOW(), NOT NULL | Last update timestamp. |

**Indexes**: `idx_users_email` UNIQUE index on email.

**Constraints**: `email` must be valid format (check constraint or application-level).

---

### 2. `contents` Table

| Field | Type | Constraints | Description |
|---|---|---|---|
| `id` | SERIAL | PRIMARY KEY | Unique content identifier. |
| `user_id` | INTEGER | NOT NULL, REFERENCES users(id) ON DELETE CASCADE | Owner of the content. |
| `content_type` | VARCHAR(20) | NOT NULL, CHECK (IN ('text', 'image', 'video')) | Modality type. |
| `text_content` | TEXT | NULLABLE | Raw text (for text content type). |
| `file_path` | VARCHAR(500) | NOT NULL | Storage reference/path to uploaded file. |
| `created_at` | TIMESTAMP WITH TIME ZONE | DEFAULT NOW(), NOT NULL | Upload timestamp. |

**Indexes**: `idx_contents_user_id` index on user_id.

**Constraints**: 
- `content_type` enforces valid modalities.
- For text: `text_content` must be populated, `file_path` may be NULL or empty.
- For image/video: `file_path` must be populated, `text_content` NULL.

---

### 3. `analyses` Table

| Field | Type | Constraints | Description |
|---|---|---|---|
| `id` | SERIAL | PRIMARY KEY | Unique analysis identifier. |
| `content_id` | INTEGER | NOT NULL, REFERENCES contents(id) ON DELETE CASCADE | Parent content record. |
| `overall_credibility_score` | INTEGER | NOT NULL, CHECK (>= 0 AND <= 100) | Final credibility score. |
| `credibility_label` | VARCHAR(50) | NOT NULL, CHECK (IN ('Supported', 'Partially Supported', 'Uncertain', 'Potentially Misleading')) | High-level label. |
| `confidence` | INTEGER | NOT NULL, CHECK (>= 0 AND <= 100) | Assessment confidence percentage. |
| `quality_score` | INTEGER | NOT NULL, CHECK (>= 0 AND <= 100) | Content quality score. |
| `status` | VARCHAR(20) | NOT NULL, DEFAULT 'completed', CHECK (IN ('completed', 'failed', 'pending')) | Analysis status. |
| `created_at` | TIMESTAMP WITH TIME ZONE | DEFAULT NOW(), NOT NULL | Analysis creation timestamp. |
| `updated_at` | TIMESTAMP WITH TIME ZONE | DEFAULT NOW(), NOT NULL | Last update timestamp. |

**Indexes**: `idx_analyses_content_id` index on content_id, `idx_analyses_created_at` on created_at.

**Constraints**: 
- `credibility_label` maps to claim assessment categories.
- `status` tracks analysis lifecycle.

---

### 4. `claims` Table

| Field | Type | Constraints | Description |
|---|---|---|---|
| `id` | SERIAL | PRIMARY KEY | Unique claim identifier. |
| `analysis_id` | INTEGER | NOT NULL, REFERENCES analyses(id) ON DELETE CASCADE | Parent analysis. |
| `claim_text` | TEXT | NOT NULL | The extracted claim text. |
| `assessment` | VARCHAR(50) | NOT NULL, CHECK (IN ('Supported', 'Partially Supported', 'Uncertain', 'Potentially Misleading')) | Claim support level. |
| `confidence` | REAL | NOT NULL, CHECK (>= 0 AND <= 1) | Claim-level confidence (0.0-1.0). |
| `explanation` | TEXT | NULLABLE | Why the assessment was made. |

**Indexes**: `idx_claims_analysis_id` index on analysis_id.

**Constraints**: Each claim belongs to exactly one analysis. `ON DELETE CASCADE` removes claims when analysis is deleted.

---

### 5. `sources` / `evidence` Table

| Field | Type | Constraints | Description |
|---|---|---|---|
| `id` | SERIAL | PRIMARY KEY | Unique source identifier. |
| `analysis_id` | INTEGER | NOT NULL, REFERENCES analyses(id) ON DELETE CASCADE | Parent analysis. |
| `source_name` | VARCHAR(255) | NOT NULL | Name of the source (e.g., "News API", "Wikipedia", "Peer-reviewed study"). |
| `source_url` | VARCHAR(500) | NULLABLE | URL to original source. |
| `snippet` | TEXT | NOT NULL | Relevant text excerpt from source. |
| `retrieval_method` | VARCHAR(30) | NOT NULL, CHECK (IN ('bm25', 'vector', 'api')) | How evidence was retrieved. |
| `retrieved_at` | TIMESTAMP WITH TIME ZONE | DEFAULT NOW(), NOT NULL | When evidence was retrieved. |

**Indexes**: `idx_sources_analysis_id` index on analysis_id, `idx_sources_method` on retrieval_method.

**Constraints**: One analysis can have multiple sources. `ON DELETE CASCADE` removes sources when analysis is deleted.

---

### 6. ER Diagram (Mermaid)

```mermaid
erDiagram
    USER ||--o{ CONTENTS : owns
    USER ||--o{ ANALYSES : owns
    CONTENTS ||--o{ ANALYSES : analyzed
    ANALYSES ||--o{ CLAIMS : contains
    ANALYSES ||--o{ SOURCES : has
    
    USER {
        int id PK
        varchar name
        varchar email UNIQUE
        varchar password_hash
        timestamp created_at
        timestamp updated_at
    }
    
    CONTENTS {
        int id PK
        int user_id FK > USER.id
        varchar content_type
        text text_content
        varchar file_path
        timestamp created_at
    }
    
    ANALYSES {
        int id PK
        int content_id FK > CONTENTS.id
        int overall_credibility_score
        varchar credibility_label
        int confidence
        int quality_score
        varchar status
        timestamp created_at
        timestamp updated_at
    }
    
    CLAIMS {
        int id PK
        int analysis_id FK > ANALYSES.id
        text claim_text
        varchar assessment
        real confidence
        text explanation
    }
    
    SOURCES {
        int id PK
        int analysis_id FK > ANALYSES.id
        varchar source_name
        varchar source_url
        text snippet
        varchar retrieval_method
        timestamp retrieved_at
    }
```

---

### 7. Relationship Summary

| Relationship | Type | Description |
|---|---|---|
| User → Contents | 1:N | One user owns many contents. |
| User → Analyses | 1:N | One user owns many analyses. |
| Contents → Analyses | 1:N | One content has one analysis (via content_id). |
| Analyses → Claims | 1:N | One analysis has many claims. |
| Analyses → Sources | 1:N | One analysis has many sources. |
| Cascade Delete | — | Deleting a user cascades to contents, analyses, claims, and sources. |

**Nullability Summary**:
- `users.name`: NOT NULL
- `users.email`: UNIQUE, NOT NULL
- `users.password_hash`: NOT NULL
- `contents.user_id`: NOT NULL, FK
- `contents.content_type`: NOT NULL, CHECK
- `contents.text_content`: NULLABLE (populated for text type)
- `contents.file_path`: NOT NULL
- `analyses.content_id`: NOT NULL, FK
- `analyses.overall_credibility_score`: NOT NULL, CHECK 0-100
- `analyses.credibility_label`: NOT NULL, CHECK categories
- `analyses.confidence`: NOT NULL, CHECK 0-100
- `analyses.quality_score`: NOT NULL, CHECK 0-100
- `analyses.status`: NOT NULL, DEFAULT 'completed'
- `claims.claim_text`: NOT NULL
- `claims.assessment`: NOT NULL, CHECK categories
- `claims.confidence`: NOT NULL, CHECK 0.0-1.0
- `sources.source_name`: NOT NULL
- `sources.snippet`: NOT NULL
- `sources.retrieval_method`: NOT NULL, CHECK

---

### 8. Recommended Indexes for Performance

```sql
CREATE INDEX idx_analyses_user_id ON analyses(id) WHERE user_id IS NOT NULL;
-- (Note: application-layer filtering by user_id is done via JOIN with contents)

CREATE INDEX idx_claims_analysis_id ON claims(analysis_id);
CREATE INDEX idx_sources_analysis_id ON sources(analysis_id);

CREATE INDEX idx_contents_user_id_type ON contents(user_id, content_type);
```

---

### 9. Migrations (Alembic)

Initial migration should create all 5 tables. Subsequent migrations for:
- Adding `refresh_tokens` table (if using refresh token rotation).
- Adding indexes for evidence retrieval performance.
- Adding any future tables (e.g., `sessions`, `api_keys`).

**Migration naming convention**: `###_description.py` (e.g., `001_init_schema.py`).
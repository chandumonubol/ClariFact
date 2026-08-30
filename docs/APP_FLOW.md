# ClariFact — Application Flow Document (APP_FLOW.md)

## Authentication Flow

```text
Register
  ↓
Validate form (name, email, password)
  ↓
Create Account (hash password with bcrypt)
  ↓
Login
  ↓
Validate credentials
  ↓
Issue JWT access token + refresh token
  ↓
Dashboard (authenticated)
```

### Login / Register Details

- **Register**: User enters name, email, password. System validates email format, password minimum length. On success, account created and user is automatically logged in.
- **Login**: User enters email and password. System verifies bcrypt hash. On success, JWT tokens issued. On failure, error message shown.
- **Logout**: JWT added to revocation list (or refresh token invalidated). User redirected to login page.

## Text Flow

```text
Dashboard → Select "Text Analysis"
  ↓
Enter or paste text content
  ↓
Validate: non-empty, within length limit
  ↓
Submit → POST /api/analyze
  ↓
Backend validates authentication
  ↓
Preprocessing: normalize, language detection
  ↓
Claim Extraction: extract checkable claims
  ↓
Evidence Retrieval: fetch relevant sources
  ↓
Credibility Assessment: score claims, compute overall score
  ↓
Content Quality Analysis: readability, etc.
  ↓
Generate Report (structured)
  ↓
Save Analysis (user-specific)
  ↓
Results Page (display report)
  ↓
Add to History
```

## Image Flow

```text
Dashboard → Select "Image Analysis"
  ↓
Upload image file (JPEG, PNG, WebP)
  ↓
Validate: file type, size < 10MB
  ↓
If invalid → Show error → Allow retry
  ↓
Valid → Upload → Backend receives file
  ↓
Validation: check format, dimensions
  ↓
OCR: extract text via pytesseract/easyocr
  │
  ├── If text extracted → Proceed to claim extraction
  └── If little or no text → Provide meaningful response (summary of visual elements, ask user if content contains claims)
  ↓
Claim Extraction: extract claims from OCR text
  ↓
Evidence Retrieval: fetch sources for claims
  ↓
Credibility Assessment: score claims
  ↓
Visual Analysis: basic image properties (format, dimensions, hash)
  ↓
Generate Report
  ↓
Save Analysis
  ↓
Results Page
  ↓
Add to History
```

## Video Flow

```text
Dashboard → Select "Video Analysis"
  ↓
Upload video file (MP4, WebM, MOV)
  ↓
Validate: file type, size < 50MB, duration < 5 minutes
  ↓
If invalid → Show error → Allow retry
  ↓
Valid → Upload → Backend receives file
  ↓
Validation: check format, duration
  ↓
Audio Extraction: extract audio track
  ↓
Speech-to-Text: transcribe via Whisper/faster-whisper
  ↓
Transcript generated
  ↓
Claim Extraction: extract claims from transcript
  ↓
Evidence Retrieval: fetch sources for claims
  ↓
Credibility Assessment: score claims
  ↓
Frame Sampling: sample key frames (every 10s or 5% of duration)
  ↓
Visual Analysis: analyze sampled frames (visual quality, hooks, etc.)
  ↓
Content Quality Analysis: speech clarity, engagement indicators
  ↓
Generate Final Report
  ↓
Save Analysis
  ↓
Results Page
  ↓
Add to History
```

## Error Flows

### Invalid File

```text
User uploads unsupported format / too large
  ↓
Backend validates
  ↓
Show error: "Unsupported file type. Allowed: JPEG, PNG, WebP for images. MP4, WebM, MOV for videos. Max size: 10MB images, 50MB videos. Max duration: 5 minutes videos."
  ↓
Allow user to retry upload
```

### Analysis Failure

```text
AI processing fails (e.g., OCR error, STT timeout)
  ↓
Show error: "Analysis could not be completed. Please try again with a different file or contact support."
  ↓
Allow user to retry
```

### Empty Content

```text
User submits empty text
  ↓
Show error: "Please enter content to analyze."
  ↓
Allow user to retry
```

### Unsupported Image (little text)

```text
Image contains no readable text
  ↓
Proceed with visual analysis only
  ↓
Generate report: "No readable text detected. Analysis based on visual characteristics and available evidence."
  ↓
Do not crash; provide meaningful response
```

## Logout Flow

```text
User clicks Logout
  ↓
POST /api/auth/logout (invalidate token)
  ↓
Clear auth cookies/localStorage
  ↓
Redirect to Login page
```

## History Flow

```text
Dashboard shows analysis list
  ↓
User clicks "History" or analysis card
  ↓
GET /api/history (list user's analyses)
  ↓
Each entry shows: date, content type, credibility score label
  ↓
User clicks analysis entry
  ↓
GET /api/analysis/{id} (detail view)
  ↓
Full report displayed: credibility score, claims, evidence, explanation
  ↓
User can delete or re-analyze
```

## Unauthorized Access Flow

```text
User not logged attempts protected endpoint
  ↓
401 Unauthorized response
  ↓
Redirect to login page with "Please log in to access this page" message
```

## Session / Token Expiration Flow

```text
JWT access token expires (15-30 min)
  ↓
Frontend detects 401 response on API call
  ↓
Try refresh token (POST /api/auth/refresh)
  │
  ├── If refresh valid → Issue new access token, continue
  └── If refresh invalid/expired → Clear auth state, redirect to login
```
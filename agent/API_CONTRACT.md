# API Contract

## POST /api/auth/register

Request:
{
  "name": "string",
  "email": "string",
  "password": "string"
}

Response (200):
{
  "user": {
    "id": "int",
    "name": "string",
    "email": "string"
  },
  "access_token": "string",
  "token_type": "bearer"
}

Response (400): Validation error.

## POST /api/auth/login

Request:
{
  "email": "string",
  "password": "string"
}

Response (200):
{
  "user": { "id": int, "name": string, "email": string },
  "access_token": "string",
  "token_type": "bearer"
}

Response (401): Invalid credentials.

## GET /api/auth/me

Request: Bearer JWT token
Response (200): User profile.

Response (401): Unauthorized.

## POST /api/analyze

Request (Text):
{
  "content_type": "text",
  "text_content": "string"
}

Request (Image):
{
  "content_type": "image",
  "file_path": "string"
}

Request (Video):
{
  "content_type": "video",
  "file_path": "string"
}

Response (200):
{
  "analysis_id": "int",
  "status": "processing"
}

Response (200, final):
{
  "overall_credibility_score": int (0-100),
  "credibility_label": string,
  "confidence": int (0-100),
  "quality_score": int (0-100),
  "claims": [
    {
      "id": int,
      "claim_text": "string",
      "assessment": string,
      "confidence": real (0.0-1.0),
      "explanation": "string"
    }
  ],
  "evidence": [
    {
      "source_name": "string",
      "snippet": "string"
    }
  ],
  "explanation": "string"
}

## GET /api/history

Request: Bearer JWT
Response (200): Array of analysis summaries.

## GET /api/analysis/{id}

Request: Bearer JWT
Response (200): Full analysis detail.

Status Codes: 200 (OK), 201 (Created), 400 (Bad Request), 401 (Unauthorized), 403 (Forbidden), 422 (Validation Error), 500 (Internal Error).
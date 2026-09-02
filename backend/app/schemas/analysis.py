from pydantic import BaseModel
from typing import List, Optional

class AnalyzeRequest(BaseModel):
    content_type: str
    text_content: Optional[str] = None
    file_path: Optional[str] = None

class AnalysisStartResponse(BaseModel):
    analysis_id: int
    status: str

class ClaimResponse(BaseModel):
    id: int
    claim_text: str
    assessment: str
    confidence: float
    explanation: str

    class Config:
        from_attributes = True

class SourceResponse(BaseModel):
    source_name: str
    snippet: str

    class Config:
        from_attributes = True

class AnalysisResultResponse(BaseModel):
    overall_credibility_score: int
    credibility_label: str
    confidence: int
    quality_score: int
    claims: List[ClaimResponse] = []
    evidence: List[SourceResponse] = []
    explanation: str

    class Config:
        from_attributes = True

class HistoryResponse(BaseModel):
    analysis_id: int
    content_type: str
    text_content: Optional[str] = None
    overall_credibility_score: Optional[int] = None
    credibility_label: Optional[str] = None
    created_at: str

    class Config:
        from_attributes = True

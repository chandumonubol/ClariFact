from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_current_user
from app.models.user import User
from app.models.content import Content
from app.models.analysis import Analysis
from app.models.claim import Claim
from app.models.source import Source
from app.schemas.analysis import AnalyzeRequest, AnalysisResultResponse
from app.services.ai_service import analyze_text
from app.core.config import settings

router = APIRouter()

@router.post("", response_model=AnalysisResultResponse)
def analyze_content(request: AnalyzeRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if request.content_type != "text":
        raise HTTPException(status_code=400, detail="Only text analysis is currently supported.")
    
    if not request.text_content or not request.text_content.strip():
        raise HTTPException(status_code=400, detail="Text content cannot be empty.")
        
    if len(request.text_content) > settings.MAX_TEXT_LENGTH:
        raise HTTPException(status_code=400, detail=f"Text exceeds maximum length of {settings.MAX_TEXT_LENGTH} characters.")

    # 1. Save Content
    db_content = Content(
        user_id=current_user.id,
        content_type="text",
        text_content=request.text_content
    )
    db.add(db_content)
    db.commit()
    db.refresh(db_content)

    # 2. Call AI Service (Mock for now)
    try:
        ai_result = analyze_text(request.text_content)
    except Exception as e:
        # DB failure handled if AI fails (already committed content, maybe we should transaction?)
        # Let's keep it simple for MVP
        raise HTTPException(status_code=500, detail="AI Service failed to process the request.")

    # 3. Save Analysis Result
    db_analysis = Analysis(
        user_id=current_user.id,
        content_id=db_content.id,
        overall_credibility_score=ai_result.get("overall_credibility_score"),
        credibility_label=ai_result.get("credibility_label"),
        confidence=ai_result.get("confidence"),
        quality_score=ai_result.get("quality_score"),
        explanation=ai_result.get("explanation"),
        status="completed"
    )
    db.add(db_analysis)
    db.commit()
    db.refresh(db_analysis)

    # 4. Save Claims
    for c in ai_result.get("claims", []):
        db_claim = Claim(
            analysis_id=db_analysis.id,
            claim_text=c.get("claim_text"),
            assessment=c.get("assessment"),
            confidence=c.get("confidence"),
            explanation=c.get("explanation")
        )
        db.add(db_claim)
    
    # 5. Save Sources
    for s in ai_result.get("evidence", []):
        db_source = Source(
            analysis_id=db_analysis.id,
            source_name=s.get("source_name"),
            snippet=s.get("snippet")
        )
        db.add(db_source)
        
    db.commit()
    db.refresh(db_analysis)

    return {
        "overall_credibility_score": db_analysis.overall_credibility_score,
        "credibility_label": db_analysis.credibility_label,
        "confidence": db_analysis.confidence,
        "quality_score": db_analysis.quality_score,
        "explanation": db_analysis.explanation,
        "claims": db_analysis.claims,
        "evidence": db_analysis.sources
    }

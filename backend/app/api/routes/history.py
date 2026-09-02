from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.api.deps import get_db, get_current_user
from app.models.user import User
from app.models.analysis import Analysis
from app.models.content import Content
from app.schemas.analysis import HistoryResponse, AnalysisResultResponse, ClaimResponse, SourceResponse

router = APIRouter()

@router.get("", response_model=List[HistoryResponse])
def get_history(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    analyses = db.query(Analysis).filter(Analysis.user_id == current_user.id).order_by(Analysis.created_at.desc()).all()
    
    results = []
    for a in analyses:
        results.append({
            "analysis_id": a.id,
            "content_type": a.content.content_type,
            "text_content": a.content.text_content,
            "overall_credibility_score": a.overall_credibility_score,
            "credibility_label": a.credibility_label,
            "created_at": a.created_at.isoformat()
        })
    return results

@router.get("/{analysis_id}", response_model=AnalysisResultResponse)
def get_analysis_detail(analysis_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    analysis = db.query(Analysis).filter(Analysis.id == analysis_id).first()
    
    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found")
        
    if analysis.user_id != current_user.id:
        # Returning 404 to not leak existence per security best practices
        raise HTTPException(status_code=404, detail="Analysis not found")

    return {
        "overall_credibility_score": analysis.overall_credibility_score,
        "credibility_label": analysis.credibility_label,
        "confidence": analysis.confidence,
        "quality_score": analysis.quality_score,
        "explanation": analysis.explanation,
        "claims": analysis.claims,
        "evidence": analysis.sources
    }

from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.db.session import Base

class Claim(Base):
    __tablename__ = "claims"

    id = Column(Integer, primary_key=True, index=True)
    analysis_id = Column(Integer, ForeignKey("analyses.id"), index=True)
    claim_text = Column(Text, nullable=False)
    assessment = Column(String, nullable=False)
    confidence = Column(Float, nullable=True)
    explanation = Column(Text, nullable=True)

    analysis = relationship("Analysis", back_populates="claims")

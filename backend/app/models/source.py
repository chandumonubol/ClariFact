from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.session import Base

class Source(Base):
    __tablename__ = "sources"

    id = Column(Integer, primary_key=True, index=True)
    analysis_id = Column(Integer, ForeignKey("analyses.id"), index=True)
    source_name = Column(String, nullable=False)
    source_url = Column(String, nullable=True)
    snippet = Column(Text, nullable=True)
    retrieval_method = Column(String, nullable=True)
    retrieved_at = Column(DateTime, default=datetime.utcnow)

    analysis = relationship("Analysis", back_populates="sources")

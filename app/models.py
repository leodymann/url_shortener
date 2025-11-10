from sqlalchemy import Column, Integer, String, DateTime, func
from app.database import Base

class URL(Base):
    # crio a tabela urls
    __tablename__ = "urls"

    id = Column(Integer, primary_key=True, index=True)
    original_url = Column(String, nullable=False)
    short_hash = Column(String, unique=True, index=True, nullable=False)
    user_id = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class URL(Base):
    __tablename__ = "urls"

    id= Column(Integer, primary_key=True, index=True)
    original_url= Column(String, nullable=False)
    short_hash= Column(String, unique=True, index=True, nullable=False)
    created_at= Column(DateTime(timezone=True), server_default=func.now())
    user_id= Column(Integer, nullable=True)
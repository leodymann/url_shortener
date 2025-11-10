from pydantic import BaseModel, HttpUrl
from typing import Optional
from datetime import datetime

class URLCreate(BaseModel):
    original_url: HttpUrl

class URLInfo(BaseModel):
    id: int
    original_url: str
    short_hash: str
    created_at: datetime
    user_id: Optional[int] = None

    class Config:
        orm_mode=True
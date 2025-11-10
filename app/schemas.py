from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class URLBase(BaseModel):
    original_url: str
    user_id: Optional[int] = None

class URLCreate(URLBase):
    pass

class URLResponse(URLBase):
    id: int
    short_hash: str
    created_at: datetime

    class Config:
        orm_mode = True

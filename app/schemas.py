from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class URLBase(BaseModel):
    # representa a URL original example.com.br
    original_url: str
    user_id: Optional[int] = None

class URLCreate(URLBase):
    pass # sem atributos ou métodods

class URLResponse(URLBase):
    # resposta para usuário
    id: int
    short_hash: str
    created_at: datetime

    class Config:
        orm_mode = True # lê diretamente os objetos

import random
import string
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError

from app.models import URL
from app.schemas import URLCreate

def generate_hash(length: int = 6) -> str:
    # função de gerar o hash da URL
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

async def create_url(db: AsyncSession, url: URLCreate) -> URL:
    # função para criar URLs
    short_hash = generate_hash() # geração de hash (6 caracteres)
    new_url = URL(original_url=url.original_url, short_hash=short_hash, user_id=url.user_id) # url original + nova com hash
    db.add(new_url) # envio a adição à sessão
    try:
        await db.commit() # envio ao database
        await db.refresh(new_url) # update no database
        return new_url # retorno o obj criado
    except IntegrityError:
        await db.rollback()
        return await create_url(db, url)  # colisão de hash

async def get_url_by_hash(db: AsyncSession, short_hash: str): # query para achar a URL especifica
    result = await db.execute(select(URL).where(URL.short_hash == short_hash)) # query assíncrona
    return result.scalars().first() # primeiro da consulta

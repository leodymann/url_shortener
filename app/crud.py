import random
import string
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError

from app.models import URL
from app.schemas import URLCreate

def generate_hash(length: int = 6) -> str:
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

async def create_url(db: AsyncSession, url: URLCreate) -> URL:
    short_hash = generate_hash()
    new_url = URL(original_url=url.original_url, short_hash=short_hash, user_id=url.user_id)
    db.add(new_url)
    try:
        await db.commit()
        await db.refresh(new_url)
        return new_url
    except IntegrityError:
        await db.rollback()
        return await create_url(db, url)  # Retry in case of hash collision

async def get_url_by_hash(db: AsyncSession, short_hash: str):
    result = await db.execute(select(URL).where(URL.short_hash == short_hash))
    return result.scalars().first()

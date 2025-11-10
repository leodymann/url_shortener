import random
import string
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError

from app.models import URL

def generate_hash(length: int = 6) -> str:
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

async def create_url(db: AsyncSession, original_url: str, user_id: int = None) -> URL:
    short_hash = generate_hash()
    new_url = URL(original_url=original_url, short_hash=short_hash, user_id=user_id)

    db.add(new_url)
    try:
        await db.commit()
        await db.refresh(new_url)
        return new_url
    except IntegrityError:
        await db.rollback()
        return await create_url(db, original_url, user_id)

async def get_url_by_hash(db: AsyncSession, short_hash: str) -> URL:
    result = await db.execute(select(URL).where(URL.short_hash == short_hash))
    return result.scalars().all()

async def delete__url(db: AsyncSession, url_id: int):
    result = await db.execute(select(URL).where(URL.id == url_id))
    url = result.scalars().first()
    if url:
        await db.delete(url)
        await db.commit()
        return True
    return False

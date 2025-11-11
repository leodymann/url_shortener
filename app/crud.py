import random
import string
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status

from app.models import URL
from app.schemas import URLCreate


def generate_hash(length: int = 6) -> str:
    # generate hash 6 digits
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


async def create_url(db: AsyncSession, url: URLCreate) -> URL:
    # create url + hash
    short_hash = generate_hash()
    new_url = URL(original_url=url.original_url, short_hash=short_hash, user_id=url.user_id)
    db.add(new_url)
    try:
        await db.commit()
        await db.refresh(new_url)
        return new_url
    except IntegrityError:
        await db.rollback()
        return await create_url(db, url)  # colisão de hash


async def get_url_by_hash(db: AsyncSession, short_hash: str):
    # search url by hash
    result = await db.execute(select(URL).where(URL.short_hash == short_hash))
    return result.scalars().first()


async def delete_url(db: AsyncSession, short_hash: str):
    # delete url by hash
    result = await db.execute(select(URL).where(URL.short_hash == short_hash))
    url = result.scalars().first()

    if not url:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="URL não encontrada")

    await db.delete(url)
    await db.commit()
    return {"detail": "URL deletada com sucesso"}


async def redirect_url(db: AsyncSession, short_hash: str):
    # redirect url by hash
    url = await get_url_by_hash(db, short_hash)
    if not url:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="URL não encontrada")
    return url.original_url

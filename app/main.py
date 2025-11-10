from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db, engine, Base
from app import crud, schemas
from app.cache import cache
import asyncio

app = FastAPI(title="URL Shortener API")

@app.on_event("startup")
async def startup():
    # create table:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.post("/urls/", response_model=schemas.URLResponse)
async def create_url(url: schemas.URLCreate, db: AsyncSession = Depends(get_db)):
    new_url = await crud.create_url(db, url)
    cache.set(new_url.short_hash, new_url.original_url)
    return new_url

@app.get("/urls/{short_hash}")
async def get_url(short_hash: str, db: AsyncSession = Depends(get_db)):
    cached = cache.get(short_hash)
    if cached:
        return {"original_url": cached, "cached": True}

    url_obj = await crud.get_url_by_hash(db, short_hash)
    if not url_obj:
        raise HTTPException(status_code=404, detail="URL not found")

    cache.set(short_hash, url_obj.original_url)
    return {"original_url": url_obj.original_url, "cached": False}

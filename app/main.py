from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db, Base, engine
from app import crud, schemas
from app.cache import cache

app = FastAPI(title="URL Shortener API")


@app.on_event("startup")
async def on_startup():
    # create tables if they don't already exist.
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.post("/shorten/", response_model=schemas.URLResponse)
async def create_short_url(url: schemas.URLCreate, db: AsyncSession = Depends(get_db)):
    # create short url
    cached_url = cache.get(url.original_url)
    if cached_url:
        return cached_url

    new_url = await crud.create_url(db, url)
    cache.set(url.original_url, new_url)
    return new_url


@app.get("/url/{short_hash}", response_model=schemas.URLResponse)
async def get_short_url(short_hash: str, db: AsyncSession = Depends(get_db)):
    # return info short url
    cached = cache.get(short_hash)
    if cached:
        return cached

    db_url = await crud.get_url_by_hash(db, short_hash)
    if not db_url:
        raise HTTPException(status_code=404, detail="URL não encontrada")

    cache.set(short_hash, db_url)
    return db_url


@app.get("/r/{short_hash}")
async def redirect_short_url(short_hash: str, db: AsyncSession = Depends(get_db)):
    # redirect url original
    original_url = await crud.redirect_url(db, short_hash)
    return RedirectResponse(url=original_url)


@app.delete("/delete/{short_hash}")
async def delete_short_url(short_hash: str, db: AsyncSession = Depends(get_db)):
    # delete short url by hash
    return await crud.delete_url(db, short_hash)

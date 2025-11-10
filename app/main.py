from fastapi import FastAPI
from app.cache import get_redis

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "api online on db"}

@app.get("/cache-test")
async def cache_test():
    r = await get_redis()
    await r.set("test", "online")
    value = await r.get("test")
    return {"redis_value": value}
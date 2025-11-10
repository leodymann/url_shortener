import os
import redis.asyncio as redis

# Configurações do Redis via variáveis de ambiente
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_DB = int(os.getenv("REDIS_DB", 0))
REDIS_EXPIRE = int(os.getenv("REDIS_EXPIRE", 3600))  # tempo padrão de expiração em segundos

# Pool de conexões para melhor performance
redis_pool = redis.ConnectionPool(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)
redis_client = redis.Redis(connection_pool=redis_pool)

# Função para pegar o cliente Redis (assíncrono)
async def get_redis():
    return redis_client

# Função wrapper para gravar no cache
async def set_cache(key: str, value: str, expire: int = REDIS_EXPIRE):
    try:
        await redis_client.set(key, value, ex=expire)
    except Exception as e:
        print(f"[Redis] Erro ao gravar chave '{key}': {e}")

# Função wrapper para ler do cache
async def get_cache(key: str):
    try:
        value = await redis_client.get(key)
        return value
    except Exception as e:
        print(f"[Redis] Erro ao ler chave '{key}': {e}")
        return None

# Função wrapper para deletar do cache
async def delete_cache(key: str):
    try:
        await redis_client.delete(key)
    except Exception as e:
        print(f"[Redis] Erro ao deletar chave '{key}': {e}")

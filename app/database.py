from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine 
"""
-> AsyncEngine = Conexão assíncrona.
-> AsyncSession = Ponte entre o código <-> Database.
-> create_async_engine = É ele quem gerencia o AsyncSession.
"""
from sqlalchemy.orm import sessionmaker, declarative_base
"""
-> sessionmaker = Cria objetos AsyncSession quando precisa interagir com o Database.
-> declarative_base = Base para os models(tabelas).
"""
from app.config import settings # Configurações do Database.

Base = declarative_base()

engine: AsyncEngine = create_async_engine(
    settings.DATABASE_URL, echo=True, future=True
)

async_session = sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession # Defino sessões assíncronas.
)

async def get_db():
    # single session per request
    async with async_session() as session:
        yield session

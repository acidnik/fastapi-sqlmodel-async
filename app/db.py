from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine

from .config import settings

engine = create_async_engine(settings.DATABASE_URL, echo=True, future=True)


async def database() -> AsyncSession:
    session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with session() as s:
        yield s

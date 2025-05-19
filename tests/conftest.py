import subprocess
from typing import AsyncGenerator

import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine

from app.config import settings


@pytest.fixture(scope='session', autouse=True)
async def setup_db():
    subprocess.run('alembic upgrade head', shell=True).check_returncode()


@pytest.fixture
async def engine():
    engine = create_async_engine(settings.DATABASE_URL, echo=True)
    yield engine
    await engine.dispose()


@pytest.fixture()
async def db(engine) -> AsyncGenerator[AsyncSession]:
    sess = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with sess() as s:
        yield s



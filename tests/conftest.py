import asyncio
from typing import AsyncGenerator

import pytest
from httpx import ASGITransport
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine

from app.config import settings
from app.repo.user import UserRepository


async def run(cmd, *args, **kwargs):
    kwargs['stdout'] = asyncio.subprocess.PIPE
    kwargs['stderr'] = asyncio.subprocess.PIPE

    proc = await asyncio.create_subprocess_exec(cmd, *args, **kwargs)

    stdout, stderr = await proc.communicate()
    stdout = stdout.decode()
    stderr = stderr.decode()
    if proc.returncode != 0:
        raise RuntimeError(f"{cmd} {' '.join(args)} error {proc.returncode}: {stdout} {stderr}")


@pytest.fixture(scope='session', autouse=True)
async def setup_db():
    await run('alembic', 'upgrade', 'head')


@pytest.fixture(scope='session')
async def engine():
    # FAFO with isolation_level
    engine = create_async_engine(settings.DATABASE_URL, echo=True, isolation_level='AUTOCOMMIT')
    yield engine
    await engine.dispose()


@pytest.fixture(scope='session')
async def db(engine: AsyncEngine) -> AsyncGenerator[AsyncSession]:
    engine.execution_options(isolation_level='READ COMMITTED')
    sess = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with sess() as s:
        async with sess.begin():
            yield s


@pytest.fixture(scope='session')
async def app():
    from app.app import app

    yield app


@pytest.fixture(scope='session')
async def client(app):
    async with AsyncClient(transport=ASGITransport(app), base_url='http://app') as client:
        yield client


@pytest.fixture()
async def user_repo(db) -> UserRepository:
    return UserRepository(db)

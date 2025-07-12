import asyncio
from typing import AsyncGenerator

import pytest
from httpx import ASGITransport
from httpx import AsyncClient
from pytest_asyncio import is_async_test
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
    engine = create_async_engine(settings.DATABASE_URL, echo=True)
    yield engine
    await engine.dispose()


@pytest.fixture(scope='session')
async def db(engine: AsyncEngine) -> AsyncGenerator[AsyncSession]:
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


def pytest_collection_modifyitems(items):
    """
    force all test to run in same event loop
    """
    pytest_asyncio_tests = (item for item in items if is_async_test(item))
    session_scope_marker = pytest.mark.asyncio(loop_scope="session")
    for async_test in pytest_asyncio_tests:
        async_test.add_marker(session_scope_marker, append=False)

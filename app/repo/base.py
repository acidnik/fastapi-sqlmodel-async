from typing import Self

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import database


class Repository:
    def __init__(self, db: AsyncSession):
        self._db = db

    @classmethod
    async def depends(cls, db=Depends(database)) -> Self:
        return cls(db)

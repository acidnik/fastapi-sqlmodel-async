from typing import Any
from typing import Self
from typing import TypeVar

import sqlalchemy as sa
from fastapi import Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import database

T = TypeVar('T', bound=BaseModel)


class Repository:
    def __init__(self, db: AsyncSession):
        self._db = db

    async def insert(self, model: T) -> Any:
        # FIXME exclude_none may be wrong, but exclude_unset does not work
        return (
            await self._db.execute(
                sa.insert(model.__class__).values(**model.model_dump(exclude_none=True)).returning(model.__class__)
            )
        ).scalar()

    @classmethod
    async def depends(cls, db=Depends(database)) -> Self:
        return cls(db)

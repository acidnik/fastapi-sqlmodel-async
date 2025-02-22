from fastapi import Depends
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from models.user import User
from models.user import UserDb

from .db import database

app = FastAPI()


@app.get('/api/v1/users', response_model=list[User])
async def get_users(db: AsyncSession = Depends(database)):
    return (await db.execute(select(UserDb))).scalars().all()


@app.post('/api/v1/users', response_model=User)
async def new_user(user: UserDb, db: AsyncSession = Depends(database)):
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user

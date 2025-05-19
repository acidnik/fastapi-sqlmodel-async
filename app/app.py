from fastapi import Depends
from fastapi import FastAPI

from app.repo.user import UserRepository
from models.user import User
from models.user import UserCreate

app = FastAPI()


@app.get('/api/v1/users', response_model=list[User])
async def get_users(user_repo: UserRepository = Depends(UserRepository.depends)):
    return await user_repo.get_all()


@app.post('/api/v1/users', response_model=User)
async def new_user(user: UserCreate, user_repo: UserRepository = Depends(UserRepository.depends)):
    user_saved = await user_repo.create_user(user)
    return User(**user_saved.model_dump())

import hashlib
import secrets

import pydantic
import sqlalchemy as sa

from models.user import User
from models.user import UserCreate
from models.user import UserDb

from .base import Repository


class UserNotFound(Exception):
    pass


class InvalidPassword(Exception):
    pass


def pw_hash(pw: str, salt: str | None = None) -> str:
    # salted password with unique salt for each password
    if salt is None:
        salt = secrets.token_hex(16)
    password = f"{salt}:{pw}"
    return salt + ":" + hashlib.sha3_256(password.encode()).hexdigest()


class UserRepository(Repository):
    async def create_user(self, user: UserCreate) -> UserDb:
        user_db = UserDb(**user.model_dump(), password_hash=pw_hash(user.password))
        return await self.insert(user_db)

    async def login(self, login: str, password: str) -> User:
        user = (await self._db.execute(sa.select(UserDb).where(UserDb.login == login))).scalars().first()
        if not user:
            raise UserNotFound

        salt, _ = user.password_hash.split(':', 1)

        expected_hash = pw_hash(password, salt)

        if expected_hash != user.password_hash:
            raise InvalidPassword

        return user

    async def get_all(self) -> list[User]:
        rows = (await self._db.execute(sa.select(UserDb))).scalars().all()
        ta = pydantic.TypeAdapter(list[User])
        return ta.validate_python(rows)

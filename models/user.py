from datetime import datetime

import sqlalchemy as sa
from sqlmodel import Field
from sqlmodel import SQLModel

from models.utils import ulid


class User(SQLModel):
    id: str = Field(default_factory=ulid, primary_key=True)
    login: str = Field(unique=True)
    created_dt: datetime = Field(sa_column_kwargs={"server_default": sa.func.current_timestamp()}, default=None)


# fields for db only
class UserDb(User, table=True):
    __tablename__ = 'users'
    password_hash: str

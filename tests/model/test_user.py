import secrets

import pytest

from app.repo.user import InvalidPassword
from app.repo.user import UserNotFound
from app.repo.user import UserRepository
from models.user import UserCreate


async def test_user_create(user_repo: UserRepository):
    user_data = UserCreate(login='test_' + secrets.token_hex(8), password='test')
    user = await user_repo.create_user(user_data)
    assert user.password_hash

    # test missing user
    with pytest.raises(UserNotFound):
        await user_repo.login('xxxxx', '')

    # test wrong password
    with pytest.raises(InvalidPassword):
        await user_repo.login(user_data.login, 'wrong')

    user_saved = await user_repo.login(user_data.login, user_data.password)

    assert user_saved

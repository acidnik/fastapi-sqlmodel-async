import secrets

import pytest

from app.repo.user import InvalidPassword
from app.repo.user import UserNotFound
from app.repo.user import UserRepository
from models.user import User


async def test_user_create(user_repo: UserRepository):
    user_data = User(login='test_' + secrets.token_hex(8))
    user = await user_repo.create_user(user_data, 'test')
    assert user.password_hash

    # test missing user
    with pytest.raises(UserNotFound):
        await user_repo.login('xxxxx', '')

    # test wrong password
    with pytest.raises(InvalidPassword):
        await user_repo.login(user_data.login, 'wrong')

    user_saved = await user_repo.login(user_data.login, 'test')

    assert user_saved

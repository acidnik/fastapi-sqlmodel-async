import secrets

from httpx import AsyncClient


async def test_user_create(client: AsyncClient):
    user_data = {'login': 'test_' + secrets.token_hex(8), 'password': 'test'}
    resp = await client.post('/api/v1/users', json=user_data)
    assert resp.status_code == 200, resp.json()
    user = resp.json()
    assert user['id']

    resp = await client.get('/api/v1/users')
    assert resp.status_code == 200, resp.json()

    users = resp.json()
    assert user['id'] in [u['id'] for u in users]

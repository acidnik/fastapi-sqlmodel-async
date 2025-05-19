# Minimal setup to start with SQLModel + FastApi + Alembic
- [SQLModel](https://sqlmodel.tiangolo.com/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [Alembic](https://alembic.sqlalchemy.org/en/latest/)

# How to use
1. Add new model to `models/`
2. Import new model in `models/__init__.py`
3. Run `alembic revision --autogenerate -m my_new_model`
4. Run `alembic upgrade head`

# Config
Add your config to `app/config.py`

# Run
```
docker compose up -d 
alembic upgrade head
# create user
curl localhost:8000/api/v1/users -d '{"login":"test", "password": "test"}' -H 'Content-Type: application/json'
# get all users
curl localhost:8000/api/v1/users
```

# Customization
- New migratons are formatted using `black` + `isort`. Customize it it `alembic.ini` in section `post_write_hooks`

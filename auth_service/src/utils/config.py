import os

from dotenv import find_dotenv
from pydantic import BaseSettings, RedisDsn

basedir = os.path.abspath(os.path.dirname(__file__))


class Postgres(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: str
    POSTGRES_DB: str


class Redis(BaseSettings):
    # Настройки Redis
    redis_dsn: RedisDsn


class Settings(Postgres, Redis):

    SECRET_KEY: str
    DATABASE_URL: str


settings = Settings(_env_file=find_dotenv(), _env_file_encoding='utf-8')

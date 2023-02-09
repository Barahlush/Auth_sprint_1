# mypy: allow-untyped-defs
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
    cache_expiration_in_seconds: int


class Settings(Postgres, Redis):

    # Корень проекта
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    SECRET_KEY: str
    DATABASE_URL: str

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


settings = Settings(_env_file=find_dotenv(), _env_file_encoding='utf-8')

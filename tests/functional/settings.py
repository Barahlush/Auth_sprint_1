# mypy: allow-untyped-defs
from dotenv import find_dotenv
from pydantic import BaseSettings, RedisDsn


class Redis(BaseSettings):
    # Настройки Redis
    redis_dsn: RedisDsn


class TestSettings(Redis, BaseSettings):
    api_service_url: str = 'http://0.0.0.0:8000'
    api_v1_base_path: str = '/api/v1/'


test_settings = TestSettings(
    _env_file=find_dotenv(), _env_file_encoding='utf-8'
)

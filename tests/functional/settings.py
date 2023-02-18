import dotenv
from pydantic import BaseSettings, Field

dotenv.load_dotenv()


class TestSettings(BaseSettings):
    base_api: str = Field('http://127.0.0.1:5000', env='BASE_API')

    redis_host: str = Field('127.0.0.1', env='REDIS_HOST')
    redis_port: int = Field('6379', env='REDIS_PORT')
    redis_db: int = Field(0, env='REDIS_DB')
    redis_password: str = Field('', env='REDIS_PASSWORD')

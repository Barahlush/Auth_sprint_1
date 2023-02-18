import datetime
import os
from dataclasses import dataclass
from secrets import token_urlsafe

import dotenv

dotenv.load_dotenv()


@dataclass
class PostgresConfig:
    database: str
    user: str
    password: str
    host: str
    port: int


@dataclass
class RedisConfig:
    host: str
    port: int
    db: int
    password: str
    decode_responses: bool = True


POSTGRES_CONFIG = PostgresConfig(
    database=os.environ.get('POSTGRES_DB', 'users_database'),
    user=os.environ.get('POSTGRES_USER', 'app'),
    password=os.environ.get('POSTGRES_PASSWORD', '123qwe'),
    host=os.environ.get('POSTGRES_HOST', 'postgres'),
    port=int(os.environ.get('POSTGRES_PORT', 5432)),
)

REDIS_CONFIG = RedisConfig(
    host=os.environ.get('REDIS_HOST', 'redis'),
    port=int(os.environ.get('REDIS_PORT', 6379)),
    db=int(os.environ.get('REDIS_DB', 0)),
    password=os.environ.get('REDIS_PASSWORD', ''),
)


DEBUG = os.environ.get('DEBUG', 'True') == 'True'
APP_HOST = os.environ.get('APP_HOST', '0.0.0.0')   # noqa
APP_PORT = int(os.environ.get('APP_PORT', 5000))


APP_CONFIG = {
    'SECRET_KEY': os.getenv('SECRET_KEY', token_urlsafe(8)),
    'JWT_SECRET_KEY': os.getenv('SECRET_KEY', token_urlsafe(8)),
    'JWT_TOKEN_LOCATION': ['cookies'],
    'JWT_ACCESS_TOKEN_EXPIRES': datetime.timedelta(hours=12),
    'JWT_COOKIE_SECURE': False,  # set to True in production
    'JWT_REFRESH_TOKEN_EXPIRES': datetime.timedelta(days=10),
    'JWT_COOKIE_CSRF_PROTECT': False,
    'JWT_SESSION_COOKIE': False,
    'JWT_JSON_KEY': 'access_token',
    'JWT_REFRESH_JSON_KEY': 'refresh_token',
    'DEBUG': True,
}

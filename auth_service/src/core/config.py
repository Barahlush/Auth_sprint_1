import datetime
import os
from dataclasses import dataclass

import dotenv

dotenv.load_dotenv()


@dataclass
class PostgresConfig:
    database: str
    user: str
    password: str
    host: str
    port: int


POSTGRES_CONFIG = PostgresConfig(
    database=os.environ.get('POSTGRES_DB', 'users_database'),
    user=os.environ.get('POSTGRES_USER', 'app'),
    password=os.environ.get('POSTGRES_PASSWORD', '123qwe'),
    host=os.environ.get('POSTGRES_HOST', 'localhost'),
    port=int(os.environ.get('POSTGRES_PORT', 5432)),
)

DEBUG = os.environ.get('DEBUG', 'True') == 'True'
APP_HOST = os.environ.get('APP_HOST', '0.0.0.0')   # noqa
APP_PORT = int(os.environ.get('APP_PORT', 5000))


APP_CONFIG = {
    'JWT_SECRET_KEY': os.getenv('JWT_SECRET_KEY', 'local-secret'),
    'JWT_TOKEN_LOCATION': ['cookies'],
    'JWT_ACCESS_TOKEN_EXPIRES': datetime.timedelta(minutes=60),
    'JWT_COOKIE_SECURE': False,  # set to True in production
    'JWT_REFRESH_TOKEN_EXPIRES': datetime.timedelta(days=3),
    'JWT_COOKIE_CSRF_PROTECT': True,
    'JWT_SESSION_COOKIE': False,
    'JWT_ACCESS_CSRF_HEADER_NAME': 'X-CSRF-TOKEN-ACCESS',
    'JWT_REFRESH_CSRF_HEADER_NAME': 'X-CSRF-TOKEN-REFRESH',
    'DEBUG': True,
}

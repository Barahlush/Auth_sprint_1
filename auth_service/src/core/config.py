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

SECURITY_PASSWORD_SALT = os.environ.get(
    'SECURITY_PASSWORD_SALT', '146585145368132386173505678016728509634'
)

SECRET_KEY = os.environ.get(
    'SECRET_KEY', 'pf9Wkove4IKEAXvy-cQkeDPhv9Cb3Ag-wyJILbq_dFw'
)

DEBUG = os.environ.get('DEBUG', 'True') == 'True'
APP_HOST = os.environ.get('APP_HOST', '0.0.0.0')   # noqa
APP_PORT = int(os.environ.get('APP_PORT', 5000))

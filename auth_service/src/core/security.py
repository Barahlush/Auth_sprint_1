from typing import Any

from flask import Flask
from flask_security import PeeweeUserDatastore, Security

from src.core.config import APP_CONFIG
from src.core.models import Role, User, UserRoles
from src.db.postgres import PostgresqlDatabase


class SecureFlask(Flask):
    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        self.security: Security


def initialize_security_extention(
    app: SecureFlask, db: PostgresqlDatabase
) -> None:
    # Generate a nice key using secrets.token_urlsafe()
    app.config['SECRET_KEY'] = APP_CONFIG['SECRET_KEY']

    # Bcrypt is set as default SECURITY_PASSWORD_HASH, which requires a salt
    # Generate a good salt using: secrets.SystemRandom().getrandbits(128)
    app.config['SECURITY_PASSWORD_SALT'] = APP_CONFIG['SECURITY_PASSWORD_SALT']

    user_datastore = PeeweeUserDatastore(
        db, User, Role, UserRoles
    )   # type: ignore
    app.security = Security(app, user_datastore)

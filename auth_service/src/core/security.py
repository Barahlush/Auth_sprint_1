from typing import Any

from flask import Flask
from flask_security import PeeweeUserDatastore, Security

from src.core.models import Role, User, UserRoles
from src.db.postgres import PostgresqlDatabase


class SecureFlask(Flask):
    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        self.security: Security


def initialize_security_extention(
    app: SecureFlask, db: PostgresqlDatabase
) -> None:
    user_datastore = PeeweeUserDatastore(
        db, User, Role, UserRoles
    )   # type: ignore
    security = Security(app, user_datastore)

    app.security = security

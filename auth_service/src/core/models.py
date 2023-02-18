import secrets
from datetime import datetime
from typing import Any

from peewee import (
    BooleanField,
    CharField,
    DateTimeField,
    ForeignKeyField,
    Model,
    TextField,
)

from src.core.config import SALT_LENGTH
from src.db.postgres import db


class Role(Model):
    name = CharField(unique=True)

    class Meta:
        database = db


def generate_salt() -> str:
    return secrets.token_urlsafe(SALT_LENGTH)


class User(Model):
    email = TextField()
    password_hash = TextField()
    fs_uniquifier = TextField(null=False)
    active = BooleanField(default=True)

    class Meta:
        database = db


class UserRoles(Model):
    user = ForeignKeyField(User, related_name='roles')
    role = ForeignKeyField(Role, related_name='users')
    name = property(lambda self: self.role.name)

    def get_permissions(self) -> Any:
        return self.role.get_permissions()

    class Meta:
        database = db


class LoginEvent(Model):
    history = TextField()
    registered = DateTimeField(default=datetime.now)
    user = ForeignKeyField(User, null=True)

    class Meta:
        database = db

from typing import Any

from peewee import (
    BooleanField,
    CharField,
    DateTimeField,
    ForeignKeyField,
    Model,
    TextField,
)

from src.db.postgres import db


class Role(Model):
    name = CharField(unique=True)

    class Meta:
        database = db


# N.B. order is important since Model also contains a get_id() -
# we need the one from UserMixin.
class User(Model):
    email = TextField()
    password = TextField()
    fs_uniquifier = TextField(null=False)
    active = BooleanField(default=True)

    class Meta:
        database = db


class UserRoles(Model):
    # Because peewee does not come with built-in many-to-many
    # relationships, we need this intermediary class to link
    # user to roles.
    user = ForeignKeyField(User, related_name='roles')
    role = ForeignKeyField(Role, related_name='users')
    name = property(lambda self: self.role.name)

    def get_permissions(self) -> Any:
        return self.role.get_permissions()

    class Meta:
        database = db


class LoginEvent(Model):
    history = TextField()
    registered = DateTimeField()
    user = ForeignKeyField(User, null=True)

    class Meta:
        database = db

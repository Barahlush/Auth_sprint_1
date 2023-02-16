from flask_admin.contrib.peewee import ModelView  # type: ignore
from peewee import CharField, ForeignKeyField, Model

from src.core.models import User
from src.db.postgres import db


class UserInfo(Model):
    key = CharField(max_length=64)
    value = CharField(max_length=64)

    user = ForeignKeyField(User)

    def __str__(self) -> str:
        return f'{self.key} - {self.value}'

    class Meta:
        database = db


class UserAdmin(ModelView):  # type: ignore
    inline_models = (UserInfo,)

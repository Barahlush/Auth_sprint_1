import uuid

from flask import abort
from sqlalchemy.dialects.postgresql import UUID
from src.main import db


class BaseModel(db.Model):  # type: ignore[misc]
    __abstract__ = True

    id = db.Column(
        UUID(as_uuid=True),
        nullable=False,
        unique=True,
        primary_key=True,
        default=uuid.uuid4,
    )

    def save_to_db(self) -> None:
        try:
            db.session.add(self)
            db.session.commit()

        except BaseException:
            abort(400, 'Something went wrong')


class UserIdMixin(BaseModel):
    __abstract__ = True

    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('user.id'))

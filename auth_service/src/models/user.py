from sqlalchemy import String
from src.main import db
from src.models.base import BaseModel


class User(BaseModel):  # type: ignore[misc]

    __tablename__ = 'user'

    login = db.Column(db.String(length=128), unique=True, nullable=False)
    password = db.Column(db.Text(), nullable=False)
    full_name = db.Column(db.String(length=255), nullable=False)
    email = db.Column(db.String(length=255), unique=True, nullable=False)
    permitted_devices = db.Column(db.ARRAY(String), nullable=False)
    active = db.Column(db.Boolean(), nullable=False)
    registered_date = db.Column(
        db.DateTime, default=db.func.now(), nullable=False
    )
    updated_at = db.Column(
        db.DateTime,
        default=db.func.now(),
        onupdate=db.func.now(),
        nullable=False,
    )

    def __repr__(self) -> str:
        return f'User: {self.login} {self.id} {self.full_name}'

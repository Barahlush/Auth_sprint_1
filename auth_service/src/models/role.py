from sqlalchemy import UUID, String
from src.main import db
from src.models.base import BaseModel, UserIdMixin


class Roles(BaseModel):  # type: ignore[misc]

    __tablename__ = 'roles'

    name = db.Column(db.String(length=64), unique=True, nullable=False)
    permissions = db.Column(db.ARRAY(String), nullable=False)

    def __repr__(self) -> str:
        return f'Role: {self.name} {self.id} {self.permissions}'


class UserSession(UserIdMixin):  # type: ignore[misc]
    __tablename__ = 'user_roles'

    role_id = db.Column(UUID(as_uuid=True), db.ForeignKey('roles.id'))

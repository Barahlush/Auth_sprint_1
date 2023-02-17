"""Global pytest fixtures."""
import pytest
from flask import Blueprint, Flask
from functional.settings import APP_CONFIG
from peewee import PostgresqlDatabase


@pytest.fixture
def app():
    app = Flask(__name__)
    app.config |= APP_CONFIG
    views = Blueprint('views', __name__, url_prefix='/auth')
    not_auth = Blueprint('not_auth', __name__)
    app.register_blueprint(views)
    app.register_blueprint(not_auth)
    return app


@pytest.fixture
def db(app):
    # Получаю копию БД из приложения
    database = PostgresqlDatabase(':memory:')
    db_session = database.connection()
    yield db_session
    db.close()

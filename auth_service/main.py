from contextlib import closing
from dataclasses import asdict

import psycopg2
from flask import Flask
from loguru import logger
from psycopg2.errors import DuplicateDatabase
from routers import not_auth
from src.core.config import APP_CONFIG, APP_HOST, APP_PORT, POSTGRES_CONFIG
from src.core.jwt import jwt
from src.core.models import Role, User, UserRoles
from src.core.views import views
from src.db.datastore import PeeweeUserDatastore
from src.db.postgres import db

# Create app
app = Flask(__name__)
app.config |= APP_CONFIG

if __name__ == '__main__':

    # Create the database if it doesn't exist
    conn = psycopg2.connect(
        database='postgres',
        user=POSTGRES_CONFIG.user,
        password=POSTGRES_CONFIG.password,
        host=POSTGRES_CONFIG.host,
        port=POSTGRES_CONFIG.port,
    )
    conn.autocommit = True
    with closing(conn.cursor()) as cursor:
        try:
            cursor.execute('CREATE DATABASE users_database')
        except DuplicateDatabase:
            pass

    # Setup app and db
    with app.app_context():
        db.init(**asdict(POSTGRES_CONFIG))
        logger.info('Connected to database {}', POSTGRES_CONFIG.database)
        app.register_blueprint(views)
        app.register_blueprint(not_auth)
        jwt.init_app(app)
        datastore = PeeweeUserDatastore(db)

        db.create_tables([User, Role, UserRoles], safe=True)
        # Create roles
        datastore.find_or_create_role(
            name='admin',
            permissions={
                'admin-read',
                'admin-write',
                'user-read',
                'user-write',
            },
        )
        datastore.find_or_create_role(
            name='monitor', permissions={'admin-read', 'user-read'}
        )
        datastore.find_or_create_role(
            name='user', permissions={'user-read', 'user-write'}
        )
        datastore.find_or_create_role(name='reader', permissions={'user-read'})
        # Create a user to test with
        if not datastore.find_user(email='test@me.com'):
            datastore.create_user(
                email='test@me.com',
                password='password',  # noqa
                roles=['admin'],
            )

    app.run(host=APP_HOST, port=APP_PORT)

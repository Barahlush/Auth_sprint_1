from contextlib import closing
from dataclasses import asdict

import psycopg2
from flask_security import hash_password
from loguru import logger
from psycopg2.errors import DuplicateDatabase
from src.core.config import (
    APP_CONFIG,
    APP_HOST,
    APP_PORT,
    POSTGRES_CONFIG,
)
from src.core.models import Role, User, UserRoles
from src.core.security import SecureFlask, initialize_security_extention
from src.core.views import views
from src.db.postgres import db

if __name__ == '__main__':

    # Create app
    app = SecureFlask(__name__)
    app.config |= APP_CONFIG

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

        # Setup Flask-Security
        initialize_security_extention(app, db)

        # Create a user to test with
        db.create_tables([User, Role, UserRoles], safe=True)
        if not app.security.datastore.find_user(email='test@me.com'):
            app.security.datastore.create_user(
                email='test@me.com', password=hash_password('password')
            )

    app.run(host=APP_HOST, port=APP_PORT)

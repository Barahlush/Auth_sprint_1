from contextlib import closing
from dataclasses import asdict

import psycopg2
from flask_security import hash_password
from loguru import logger
from psycopg2.errors import DuplicateDatabase
from src.app import app
from src.core.config import POSTGRES_CONFIG
from src.core.models import Role, User, UserRoles
from src.core.security import initialize_security_extention
from src.db.postgres import db
from src.views.home import my_view

if __name__ == '__main__':
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

    with app.app_context():
        # Create the database if it doesn't exist

        db.init(**asdict(POSTGRES_CONFIG))
        logger.info('Connected to database {}', POSTGRES_CONFIG.database)
        app.register_blueprint(my_view)
        # Setup Flask-Security
        initialize_security_extention(app, db)
        # Create a user to test with
        db.create_tables([User, Role, UserRoles], safe=True)
        if not app.security.datastore.find_user(email='test@me.com'):
            app.security.datastore.create_user(
                email='test@me.com', password=hash_password('password')
            )

    app.run(host='127.0.0.1', port=5000)

from os import getenv
from orator import DatabaseManager, Schema, Model

DATABASES = {
    'postgres': {
        'driver': 'postgres',
        'host': getenv('DATABASE_HOST') or 'localhost',
        'database': getenv('DATABASE_NAME') or 'magnetdb',
        'user': getenv('DATABASE_USER') or 'magnetdb',
        'password': getenv('DATABASE_PASSWORD') or 'magnetdb',
        'prefix': ''
    }
}

db = DatabaseManager(DATABASES)
schema = Schema(db)
Model.set_connection_resolver(db)

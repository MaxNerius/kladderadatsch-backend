import os
import psycopg2
from flask import current_app, g

def get_db_connection():
    if 'db' not in g:
        g.db = psycopg2.connect(
            host = "127.0.0.1",
            database = "kladderadatsch",
            user = os.environ['DB_USER'],
            password = os.environ['DB_PASS']
        )
    return g.db

def close_db(e = None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

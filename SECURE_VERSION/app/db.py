"""
SECURE database module - uses parameterized queries.
EDUCATIONAL REFERENCE: Compare with app/db.py (vulnerable version)
"""
import pymysql
from flask import current_app, g


def get_db():
    if 'secure_db' not in g:
        g.secure_db = pymysql.connect(
            host=current_app.config['DB_HOST'],
            user=current_app.config['DB_USER'],
            password=current_app.config['DB_PASSWORD'],
            database=current_app.config['DB_NAME'],
            port=current_app.config['DB_PORT'],
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True
        )
    return g.secure_db


def db_execute(sql, params=None, fetch=True):
    """
    SECURE: Uses parameterized queries to prevent SQL injection.
    Always pass user input as params, never as part of sql string.
    """
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute(sql, params or ())
        if fetch:
            return cursor.fetchall()
        return None
    except Exception as e:
        # SECURE: Generic error message - does not leak SQL
        raise Exception("A database error occurred. Please try again.")
    finally:
        cursor.close()

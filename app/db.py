"""
Database connection module - contains deliberately vulnerable patterns
EDUCATIONAL USE ONLY - demonstrates insecure database access
"""
import pymysql
from flask import current_app, g


def get_db():
    """Get a database connection - stored on the application context."""
    if 'db' not in g:
        g.db = pymysql.connect(
            host=current_app.config['DB_HOST'],
            user=current_app.config['DB_USER'],
            password=current_app.config['DB_PASSWORD'],
            database=current_app.config['DB_NAME'],
            port=current_app.config['DB_PORT'],
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True
        )
    return g.db


def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()


def db_execute(sql, fetch=True):
    """
    VULNERABLE: Executes raw SQL without parameterization.
    Used throughout the application for 'simplicity'.
    """
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute(sql)
        if fetch:
            return cursor.fetchall()
        return None
    except Exception as e:
        # VULNERABILITY: Error messages leak SQL structure
        raise Exception(f"Database error: {str(e)} | Query: {sql}")
    finally:
        cursor.close()


def db_execute_one(sql):
    """Execute a query and return a single row."""
    results = db_execute(sql)
    if results:
        return results[0]
    return None

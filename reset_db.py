#!/usr/bin/env python3
"""
Database reset utility - reinitializes the training lab database.
EDUCATIONAL USE ONLY
"""
import pymysql
import os

DB_HOST = os.environ.get('DB_HOST', 'localhost')
DB_USER = os.environ.get('DB_USER', 'root')
DB_PASSWORD = os.environ.get('DB_PASSWORD', 'rootpassword')
DB_PORT = int(os.environ.get('DB_PORT', 3306))

def reset_database():
    print("[*] Connecting to MySQL...")
    conn = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, port=DB_PORT)
    cursor = conn.cursor()

    print("[*] Dropping existing database...")
    cursor.execute("DROP DATABASE IF EXISTS shopdb")

    print("[*] Running schema...")
    with open('schemas/init.sql', 'r') as f:
        sql_script = f.read()

    for statement in sql_script.split(';'):
        statement = statement.strip()
        if statement and not statement.startswith('--'):
            try:
                cursor.execute(statement)
            except Exception as e:
                print(f"  Warning: {e}")

    conn.commit()
    cursor.close()
    conn.close()
    print("[+] Database reset complete!")
    print("[+] Test accounts:")
    print("    admin / admin123")
    print("    john_doe / password123")
    print("    jane_smith / pass")
    print("    testuser / test")

if __name__ == '__main__':
    reset_database()

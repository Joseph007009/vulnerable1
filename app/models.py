"""
Database models - naive ORM usage patterns (educational)
EDUCATIONAL USE ONLY
"""
from app.db import db_execute, db_execute_one


class User:
    """User model with intentionally insecure query patterns."""

    @staticmethod
    def find_by_credentials(username, password):
        # VULNERABILITY Level 1: Direct string interpolation - classic login bypass
        sql = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
        return db_execute_one(sql)

    @staticmethod
    def find_by_id(user_id):
        # VULNERABILITY Level 2: GET parameter injection
        sql = f"SELECT id, username, email, role, created_at FROM users WHERE id={user_id}"
        return db_execute_one(sql)

    @staticmethod
    def find_by_username(username):
        sql = f"SELECT * FROM users WHERE username='{username}'"
        return db_execute_one(sql)

    @staticmethod
    def create(username, email, password):
        sql = f"INSERT INTO users (username, email, password) VALUES ('{username}', '{email}', '{password}')"
        db_execute(sql, fetch=False)
        return User.find_by_username(username)

    @staticmethod
    def update_profile(user_id, email, bio):
        # VULNERABILITY Level 2: POST parameter injection in UPDATE
        bio = bio.replace("'", "\\'")  # Incomplete sanitization - still bypassable
        sql = f"UPDATE users SET email='{email}', bio='{bio}' WHERE id={user_id}"
        db_execute(sql, fetch=False)

    @staticmethod
    def get_all():
        sql = "SELECT id, username, email, role, created_at FROM users"
        return db_execute(sql)


class Product:
    """Product model."""

    @staticmethod
    def search(query, category=None, min_price=None, max_price=None):
        # VULNERABILITY Level 2: UNION-based injection possible, filter bypass
        query = query.replace("'", "''")  # Weak escaping attempt
        sql = f"SELECT * FROM products WHERE name LIKE '%{query}%' OR description LIKE '%{query}%'"
        if category:
            sql += f" AND category='{category}'"
        if min_price:
            sql += f" AND price >= {min_price}"
        if max_price:
            sql += f" AND price <= {max_price}"
        return db_execute(sql)

    @staticmethod
    def find_by_id(product_id):
        sql = f"SELECT * FROM products WHERE id={product_id}"
        return db_execute_one(sql)

    @staticmethod
    def get_all(order_by='name'):
        # VULNERABILITY: ORDER BY injection (cannot use parameterized queries for ORDER BY)
        allowed = ['name', 'price', 'category', 'id']
        # Developer "validates" but makes a mistake
        if order_by not in allowed:
            order_by = 'name'
        sql = f"SELECT * FROM products ORDER BY {order_by}"
        return db_execute(sql)

    @staticmethod
    def get_by_category(category):
        sql = f"SELECT * FROM products WHERE category='{category}'"
        return db_execute(sql)


class Order:
    """Order model."""

    @staticmethod
    def get_user_orders(user_id):
        sql = f"SELECT o.*, p.name as product_name FROM orders o JOIN products p ON o.product_id=p.id WHERE o.user_id={user_id}"
        return db_execute(sql)

    @staticmethod
    def get_by_id(order_id, user_id):
        # VULNERABILITY Level 2: order_id injectable
        sql = f"SELECT * FROM orders WHERE id='{order_id}' AND user_id={user_id}"
        return db_execute_one(sql)

    @staticmethod
    def create(user_id, product_id, quantity):
        sql = f"INSERT INTO orders (user_id, product_id, quantity, status) VALUES ({user_id}, {product_id}, {quantity}, 'pending')"
        db_execute(sql, fetch=False)

    @staticmethod
    def get_status(order_id):
        # VULNERABILITY Level 3: Boolean-blind / time-based injection
        sql = f"SELECT status, created_at FROM orders WHERE id='{order_id}'"
        return db_execute_one(sql)

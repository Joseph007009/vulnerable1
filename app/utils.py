"""
Utility functions - contains insecure helper patterns
EDUCATIONAL USE ONLY
"""
import hashlib
import re
from flask import session, request


def hash_password(password):
    """VULNERABILITY: Uses MD5 (cryptographically broken)."""
    return hashlib.md5(password.encode()).hexdigest()


def check_password(password, hashed):
    """Check password against MD5 hash."""
    return hashlib.md5(password.encode()).hexdigest() == hashed


def is_logged_in():
    """Check if user is logged in via session."""
    return 'user_id' in session


def is_admin():
    """Check admin role from session."""
    return session.get('role') == 'admin'


def weak_sanitize(value):
    """
    VULNERABILITY: Incomplete sanitization - strips only some characters.
    A developer thought this was sufficient.
    """
    if value is None:
        return ''
    # Only removes semicolons - easily bypassed
    value = str(value).replace(';', '')
    return value


def sanitize_search(query):
    """
    VULNERABILITY: Attempted blacklist-based sanitization - bypassable.
    """
    if query is None:
        return ''
    # Blacklist approach - easily bypassed with case variation, comments
    blacklist = ['drop', 'delete', 'truncate', 'insert', 'update', '--']
    result = str(query)
    for word in blacklist:
        result = result.replace(word.lower(), '')
        result = result.replace(word.upper(), '')
    return result


def get_client_ip():
    """Get client IP - also injectable via X-Forwarded-For."""
    # VULNERABILITY Level 4: Header injection
    xff = request.headers.get('X-Forwarded-For', '')
    if xff:
        return xff.split(',')[0].strip()
    return request.remote_addr


def log_access(user_id, action, ip=None):
    """
    VULNERABILITY: Log injection - user-controlled data inserted into logs table.
    """
    from app.db import db_execute
    if ip is None:
        ip = get_client_ip()
    # VULNERABILITY: ip and action are user-controlled and injectable
    sql = f"INSERT INTO access_logs (user_id, action, ip_address) VALUES ({user_id}, '{action}', '{ip}')"
    try:
        db_execute(sql, fetch=False)
    except Exception:
        pass  # Silent failure

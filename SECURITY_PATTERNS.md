# Security Patterns & Remediation Guide

## The Golden Rule: Never Trust User Input

All data from users (forms, URLs, headers, cookies, JSON) must be treated as untrusted.

---

## 1. Parameterized Queries (Primary Defense)

### Python + PyMySQL
```python
# VULNERABLE
sql = f"SELECT * FROM users WHERE username='{username}'"
cursor.execute(sql)

# SECURE
cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
```

### Python + SQLAlchemy ORM
```python
# VULNERABLE
db.execute(f"SELECT * FROM users WHERE id={user_id}")

# SECURE
User.query.filter_by(id=user_id).first()
# or
db.execute(text("SELECT * FROM users WHERE id=:id"), {"id": user_id})
```

---

## 2. Input Validation

```python
import re

def validate_username(username):
    # Whitelist: only allow alphanumeric + underscore
    if not re.match(r'^[a-zA-Z0-9_]{3,50}$', username):
        raise ValueError("Invalid username format")
    return username

def validate_integer(value):
    try:
        return int(value)
    except (ValueError, TypeError):
        raise ValueError("Expected integer")
```

---

## 3. Proper Error Handling

```python
# VULNERABLE - leaks database info
except Exception as e:
    return f"Error: {str(e)}"

# SECURE - generic message, log internally
import logging
logger = logging.getLogger(__name__)

except Exception as e:
    logger.error(f"Database error: {e}", exc_info=True)
    return "An error occurred. Please try again."
```

---

## 4. Password Hashing

```python
# VULNERABLE - MD5 is broken
import hashlib
hashlib.md5(password.encode()).hexdigest()

# SECURE - bcrypt with work factor
import bcrypt
hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(rounds=12))
valid = bcrypt.checkpw(password.encode('utf-8'), hashed)
```

---

## 5. Session Security

```python
# Flask session configuration
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['SESSION_COOKIE_SECURE'] = True  # HTTPS only
app.config['PERMANENT_SESSION_LIFETIME'] = 3600  # 1 hour
```

---

## References

- [OWASP SQL Injection Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html)
- [OWASP Testing Guide - SQL Injection](https://owasp.org/www-project-web-security-testing-guide/)
- [PortSwigger SQL Injection](https://portswigger.net/web-security/sql-injection)
- [DVWA](https://dvwa.co.uk/) - Similar training platform
- [WebGoat](https://owasp.org/www-project-webgoat/) - OWASP official platform
- [HackTheBox](https://www.hackthebox.com/) - Practice environment

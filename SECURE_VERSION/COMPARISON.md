# Vulnerability Comparison: Vulnerable vs Secure Implementation

## EDUCATIONAL USE ONLY

This document provides a side-by-side comparison of vulnerable and secure code patterns.

---

## 1. Login Authentication (Level 1)

### ❌ Vulnerable (`app/models.py`)
```python
sql = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
```
**Attack**: `username = admin'--` → Bypasses password check

### ✅ Secure (`SECURE_VERSION/app/routes.py`)
```python
user = db_execute(
    "SELECT id, username, role FROM users WHERE username=%s AND password=%s",
    params=(username, hashed)
)
```

---

## 2. Product Search (Level 2 - UNION)

### ❌ Vulnerable (`app/routes.py`)
```python
sql = f"SELECT * FROM products WHERE name LIKE '%{query}%'"
```
**Attack**: `' UNION SELECT 1,username,password,4,5,6,7 FROM users--`

### ✅ Secure (`SECURE_VERSION/app/routes.py`)
```python
results = db_execute(
    "SELECT * FROM products WHERE name LIKE %s",
    params=(f'%{query}%',)
)
```

---

## 3. Error Handling

### ❌ Vulnerable
```python
except Exception as e:
    error = f"Login error: {str(e)}"  # Leaks SQL structure
```

### ✅ Secure
```python
except Exception as e:
    error = "An error occurred. Please try again."  # Generic message
```

---

## 4. Password Hashing

### ❌ Vulnerable (`app/utils.py`)
```python
return hashlib.md5(password.encode()).hexdigest()  # MD5 is broken
```

### ✅ Secure
```python
import bcrypt
return bcrypt.hashpw(password.encode(), bcrypt.gensalt())
```

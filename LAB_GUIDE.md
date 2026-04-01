# SQL Injection Lab Guide

> FOR EDUCATIONAL USE ONLY - Authorized environments only

## Vulnerability Matrix

### Level 1 - Classic Login Bypass

| Field | Value |
|-------|-------|
| **Route** | `POST /login` |
| **File** | `app/models.py:User.find_by_credentials()` |
| **Type** | Error-based, authentication bypass |
| **Vulnerable Parameter** | `username`, `password` (form fields) |
| **Detection** | Single quote `'` causes SQL error |
| **Technique** | Tautology injection, comment injection |
| **Fix** | Parameterized queries |
| **Learning Objective** | Understand how string concatenation breaks SQL logic |

**Why it's vulnerable:**
```python
sql = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
```
An input of `admin'--` transforms the query to:
```sql
SELECT * FROM users WHERE username='admin'--' AND password='...'
```

---

### Level 2 - Product Search (UNION-based)

| Field | Value |
|-------|-------|
| **Route** | `GET /products?q=`, `POST /products` |
| **File** | `app/routes.py:products()`, `app/models.py:Product.search()` |
| **Type** | UNION-based, error-based |
| **Vulnerable Parameter** | `q` (GET), `query` (POST form) |
| **Detection** | `'` in query causes error; column count enumeration |
| **Technique** | UNION SELECT to extract data from other tables |
| **Fix** | Parameterized LIKE queries |
| **Learning Objective** | UNION-based data extraction across tables |

---

### Level 2 - Profile Update (POST Injection)

| Field | Value |
|-------|-------|
| **Route** | `GET /profile?id=`, `POST /profile` |
| **File** | `app/routes.py:profile()`, `app/models.py:User.update_profile()` |
| **Type** | Second-order injection, IDOR |
| **Vulnerable Parameter** | `id` (GET), `email`, `bio` (POST) |
| **Detection** | Changing `?id=2` accesses other user profiles |
| **Technique** | IDOR via parameter tampering; bio field UPDATE injection |
| **Fix** | Always use session user_id; parameterized UPDATE |
| **Learning Objective** | Insecure Direct Object Reference + UPDATE injection |

---

### Level 3 - Admin Orders (Boolean Blind)

| Field | Value |
|-------|-------|
| **Route** | `GET /admin/orders?status=` |
| **File** | `admin_panel/routes.py:orders()` |
| **Type** | Boolean-based blind SQLi |
| **Vulnerable Parameter** | `status` (GET) |
| **Detection** | Different response for true/false conditions |
| **Technique** | `' AND 1=1--` (results shown) vs `' AND 1=2--` (no results) |
| **Fix** | Parameterized query; whitelist status values |
| **Learning Objective** | Infer database content through boolean responses |

---

### Level 3 - Admin Users (Time-Based Blind)

| Field | Value |
|-------|-------|
| **Route** | `GET /admin/users?search=` |
| **File** | `admin_panel/routes.py:users()` |
| **Type** | Time-based blind SQLi |
| **Vulnerable Parameter** | `search` (GET) |
| **Detection** | SLEEP() delays response |
| **Technique** | `' AND SLEEP(5)--` causes 5-second delay |
| **Fix** | Parameterized query |
| **Learning Objective** | Extract data using timing side-channels |

---

### Level 4 - API JSON Injection

| Field | Value |
|-------|-------|
| **Route** | `POST /api/search` |
| **File** | `api/endpoints.py:advanced_search()` |
| **Type** | JSON parameter injection |
| **Vulnerable Parameter** | `query`, `filters.category`, `filters.price_max` (JSON body) |
| **Detection** | Malformed JSON values cause SQL errors in response |
| **Technique** | Inject SQL in JSON string values |
| **Fix** | Parameterized queries for all JSON values |
| **Learning Objective** | SQL injection through JSON API payloads |

---

### Level 4 - Cookie-Based Injection

| Field | Value |
|-------|-------|
| **Route** | `GET /admin/reports` |
| **File** | `admin_panel/routes.py:reports()` |
| **Type** | Cookie-based SQLi |
| **Vulnerable Parameter** | `report_type` (cookie) |
| **Detection** | Setting cookie to `'` causes SQL error |
| **Technique** | Inject SQL payload in cookie value |
| **Fix** | Whitelist cookie values; parameterized query |
| **Learning Objective** | Non-obvious injection points (cookies) |

---

### Level 4 - Header-Based Injection

| Field | Value |
|-------|-------|
| **Route** | `GET /admin/audit` |
| **File** | `admin_panel/routes.py:audit()`, `app/utils.py:get_client_ip()` |
| **Type** | HTTP header injection |
| **Vulnerable Parameter** | `X-Forwarded-For` header |
| **Detection** | Setting header to `'` causes SQL error |
| **Technique** | Inject SQL in X-Forwarded-For header value |
| **Fix** | Validate IP format; parameterized query |
| **Learning Objective** | HTTP header as injection vector |

---

## Progression Path

1. Start at `/login` — bypass authentication
2. Move to `/products` — extract data via UNION
3. Try `/profile?id=` — access other users' data
4. Escalate to `/admin/orders` — boolean blind
5. Use `/admin/users?search=` — time-based blind
6. Attack `/api/search` — JSON injection
7. Modify `report_type` cookie — cookie injection
8. Send custom `X-Forwarded-For` — header injection

# ShopCorp SQL Injection Training Lab

> ⚠️ **FOR AUTHORIZED EDUCATIONAL USE ONLY** ⚠️
> This application is intentionally vulnerable. Deploy ONLY in isolated environments.
> See [ETHICAL_NOTICE.md](ETHICAL_NOTICE.md) before proceeding.

A realistic, multi-level SQL injection learning environment modeled after real-world e-commerce applications.

## Quick Start (Docker)

```bash
# Clone and start
docker-compose up --build

# Access: http://localhost:5000
# Login: admin / admin123
```

## Architecture

```
ShopCorp (Flask + MySQL)
├── Main App        → /login, /products, /profile, /orders (Levels 1-2)
├── Admin Panel     → /admin/* (Levels 3-4)
└── API             → /api/* (Level 4)
```

## Test Accounts

| Username | Password | Role |
|----------|----------|------|
| admin | admin123 | Admin |
| john_doe | password123 | User |
| jane_smith | pass | User |
| testuser | test | User |

## Vulnerability Levels

| Level | Difficulty | Location | Type |
|-------|------------|----------|------|
| 1 | Easy | `/login` | Classic login bypass |
| 2 | Medium | `/products`, `/profile` | UNION, POST injection |
| 3 | Advanced | `/admin/orders`, `/admin/users` | Blind, time-based |
| 4 | Expert | `/api/*`, `/admin/reports`, `/admin/audit` | JSON, cookie, header |

## Project Structure

```
vulnerable1/
├── app/                    # Main Flask application (vulnerable)
├── admin_panel/            # Admin routes (Levels 3-4)
├── api/                    # JSON API (Level 4)
├── SECURE_VERSION/         # Secure reference implementation
├── schemas/init.sql        # Database schema + sample data
├── docker/                 # Docker configuration
├── config.py               # Application configuration
├── run.py                  # Entry point
└── reset_db.py             # Database reset utility
```

## Documentation

- [LAB_GUIDE.md](LAB_GUIDE.md) - Detailed vulnerability matrix
- [SETUP_GUIDE.md](SETUP_GUIDE.md) - Step-by-step deployment
- [API_DOCUMENTATION.md](API_DOCUMENTATION.md) - API endpoints
- [SECURITY_PATTERNS.md](SECURITY_PATTERNS.md) - Remediation guide
- [ETHICAL_NOTICE.md](ETHICAL_NOTICE.md) - Ethics and legal use

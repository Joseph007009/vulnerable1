# Setup Guide - SQL Injection Training Lab

## Prerequisites
- Docker + Docker Compose, OR
- Python 3.8+ and MySQL 8.0

## Option 1: Docker (Recommended)

```bash
# 1. Clone repository
git clone <repo-url>
cd vulnerable1  # or the directory name of your clone

# 2. Start all services
docker-compose up --build

# 3. Wait for MySQL to initialize (~30 seconds)
# 4. Access: http://localhost:5000
```

## Option 2: Manual Setup

```bash
# 1. Install Python dependencies
pip install -r requirements.txt

# 2. Setup MySQL
mysql -u root -p < schemas/init.sql

# 3. Set environment variables
export DB_HOST=localhost
export DB_USER=root
export DB_PASSWORD=yourpassword
export DB_NAME=shopdb

# 4. Run application
python run.py
```

## Reset Database

```bash
python reset_db.py
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| DB_HOST | localhost | MySQL host |
| DB_USER | root | MySQL username |
| DB_PASSWORD | rootpassword | MySQL password |
| DB_NAME | shopdb | Database name |
| DB_PORT | 3306 | MySQL port |
| SECRET_KEY | dev-key | Flask secret key |
| DEBUG | True | Debug mode |

## Troubleshooting

- **Connection refused**: Ensure MySQL is running and accepting connections
- **Import errors**: Run `pip install -r requirements.txt`
- **Template errors**: Check that `app/templates/` exists and contains all HTML files

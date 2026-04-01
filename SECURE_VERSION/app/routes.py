"""
SECURE routes - parameterized queries, proper validation.
EDUCATIONAL REFERENCE: Compare with app/routes.py
"""
import hashlib
import secrets
from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from SECURE_VERSION.app.db import db_execute

secure_bp = Blueprint('secure', __name__, url_prefix='/secure')


def hash_password(password):
    """SECURE: Use bcrypt or similar in production. SHA-256 shown for simplicity."""
    # In real production: use bcrypt or argon2
    return hashlib.sha256(password.encode()).hexdigest()


@secure_bp.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')

        # SECURE: Input validation
        if not username or not password:
            error = "Username and password are required."
            return render_template('login.html', error=error)
        if len(username) > 50:
            error = "Invalid credentials."
            return render_template('login.html', error=error)

        hashed = hash_password(password)
        # SECURE: Parameterized query - %s placeholders, values as tuple
        user = db_execute(
            "SELECT id, username, role FROM users WHERE username=%s AND password=%s",
            params=(username, hashed),
            fetch=True
        )
        if user:
            session['user_id'] = user[0]['id']
            session['username'] = user[0]['username']
            session['role'] = user[0]['role']
            return redirect(url_for('secure.dashboard'))
        else:
            # SECURE: Generic error - no information leakage
            error = "Invalid credentials."
    return render_template('login.html', error=error)


@secure_bp.route('/products')
def products():
    query = request.args.get('q', '')
    results = []
    if query:
        # SECURE: Parameterized LIKE query
        results = db_execute(
            "SELECT * FROM products WHERE name LIKE %s OR description LIKE %s",
            params=(f'%{query}%', f'%{query}%')
        )
    else:
        results = db_execute("SELECT * FROM products")
    return render_template('products.html', results=results, query=query)


@secure_bp.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('secure.login'))
    # SECURE: Use session value directly, not user-supplied parameter
    user = db_execute(
        "SELECT id, username, email, role FROM users WHERE id=%s",
        params=(session['user_id'],)
    )
    return render_template('dashboard.html', user=user[0] if user else None)

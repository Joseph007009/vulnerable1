"""
Main application routes - multiple SQLi vulnerability levels
EDUCATIONAL USE ONLY
"""
from flask import Blueprint, render_template, request, session, redirect, url_for, flash, jsonify
from app.models import User, Product, Order
from app.utils import hash_password, check_password, is_logged_in, is_admin, weak_sanitize, log_access, get_client_ip
from app.db import db_execute, db_execute_one

main_bp = Blueprint('main', __name__, template_folder='templates')


@main_bp.route('/')
def index():
    return redirect(url_for('main.login'))


# ============================================================
# LEVEL 1: Classic Login Bypass
# ============================================================
@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')
        hashed = hash_password(password)
        try:
            # VULNERABILITY Level 1: Direct string interpolation
            # Try: username = admin'-- or ' OR '1'='1
            user = User.find_by_credentials(username, hashed)
            if user:
                session['user_id'] = user['id']
                session['username'] = user['username']
                session['role'] = user['role']
                log_access(user['id'], 'login', get_client_ip())
                if user['role'] == 'admin':
                    return redirect(url_for('admin.dashboard'))
                return redirect(url_for('main.dashboard'))
            else:
                error = "Invalid username or password"
        except Exception as e:
            # VULNERABILITY: Leaks SQL error to user
            error = f"Login error: {str(e)}"
    return render_template('login.html', error=error)


@main_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('main.login'))


# ============================================================
# LEVEL 1: Register
# ============================================================
@main_bp.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        username = request.form.get('username', '')
        email = request.form.get('email', '')
        password = request.form.get('password', '')
        hashed = hash_password(password)
        try:
            existing = User.find_by_username(username)
            if existing:
                error = "Username already taken"
            else:
                User.create(username, email, hashed)
                flash("Account created successfully. Please login.", "success")
                return redirect(url_for('main.login'))
        except Exception as e:
            error = f"Registration error: {str(e)}"
    return render_template('register.html', error=error)


# ============================================================
# Dashboard
# ============================================================
@main_bp.route('/dashboard')
def dashboard():
    if not is_logged_in():
        return redirect(url_for('main.login'))
    user_id = session['user_id']
    try:
        user = User.find_by_id(user_id)
        orders = Order.get_user_orders(user_id)
    except Exception as e:
        flash(f"Error loading dashboard: {str(e)}", "danger")
        user, orders = None, []
    return render_template('dashboard.html', user=user, orders=orders)


# ============================================================
# LEVEL 2: Product Search (UNION-based)
# ============================================================
@main_bp.route('/products', methods=['GET', 'POST'])
def products():
    if not is_logged_in():
        return redirect(url_for('main.login'))
    results = []
    error = None
    query = ''
    if request.method == 'POST':
        query = request.form.get('query', '')
        category = request.form.get('category', '')
        min_price = request.form.get('min_price', '')
        max_price = request.form.get('max_price', '')
        try:
            # Uses weak escaping - UNION injection still possible with double-quote bypass
            results = Product.search(query, category or None, min_price or None, max_price or None)
        except Exception as e:
            error = f"Search error: {str(e)}"
    elif request.method == 'GET':
        query = request.args.get('q', '')
        if query:
            # GET parameter - no escaping at all
            try:
                sql = f"SELECT * FROM products WHERE name LIKE '%{query}%'"
                results = db_execute(sql)
            except Exception as e:
                error = f"Search error: {str(e)}"
        else:
            try:
                results = Product.get_all()
            except Exception as e:
                error = f"Error loading products: {str(e)}"
    return render_template('products.html', results=results, query=query, error=error)


# ============================================================
# LEVEL 2: User Profile (POST injection in UPDATE)
# ============================================================
@main_bp.route('/profile', methods=['GET', 'POST'])
def profile():
    if not is_logged_in():
        return redirect(url_for('main.login'))
    # VULNERABILITY: user_id can be overridden via GET parameter
    user_id = request.args.get('id', session['user_id'])
    error = None
    success = None
    try:
        user = User.find_by_id(user_id)
    except Exception as e:
        error = f"Profile error: {str(e)}"
        user = None

    if request.method == 'POST':
        email = request.form.get('email', '')
        bio = request.form.get('bio', '')
        try:
            User.update_profile(user_id, email, bio)
            success = "Profile updated successfully"
            user = User.find_by_id(user_id)
        except Exception as e:
            error = f"Update error: {str(e)}"
    return render_template('profile.html', user=user, error=error, success=success)


# ============================================================
# LEVEL 2: Order Status (injectable order ID)
# ============================================================
@main_bp.route('/orders')
def orders():
    if not is_logged_in():
        return redirect(url_for('main.login'))
    user_id = session['user_id']
    order_id = request.args.get('id')
    error = None
    order = None
    user_orders = []
    try:
        if order_id:
            order = Order.get_by_id(order_id, user_id)
        user_orders = Order.get_user_orders(user_id)
    except Exception as e:
        error = f"Order lookup error: {str(e)}"
    return render_template('cart.html', order=order, orders=user_orders, error=error)


@main_bp.route('/orders/add', methods=['POST'])
def add_order():
    if not is_logged_in():
        return redirect(url_for('main.login'))
    product_id = request.form.get('product_id')
    quantity = request.form.get('quantity', 1)
    user_id = session['user_id']
    try:
        Order.create(user_id, product_id, quantity)
        flash("Order placed successfully!", "success")
    except Exception as e:
        flash(f"Order error: {str(e)}", "danger")
    return redirect(url_for('main.orders'))

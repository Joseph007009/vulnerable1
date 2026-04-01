"""
Admin panel routes - Level 3 & 4 SQLi vulnerabilities
EDUCATIONAL USE ONLY
"""
from flask import Blueprint, render_template, request, session, redirect, url_for, flash, jsonify
from app.db import db_execute, db_execute_one
from app.utils import is_admin, is_logged_in, log_access, get_client_ip

admin_bp = Blueprint('admin', __name__, template_folder='templates')


def admin_required(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        if not is_logged_in():
            return redirect(url_for('main.login'))
        if not is_admin():
            # VULNERABILITY: reveals admin existence
            return "Access denied. Admin privileges required.", 403
        return f(*args, **kwargs)
    return decorated


@admin_bp.route('/')
@admin_required
def dashboard():
    stats = {}
    try:
        stats['users'] = db_execute("SELECT COUNT(*) as cnt FROM users")[0]['cnt']
        stats['products'] = db_execute("SELECT COUNT(*) as cnt FROM products")[0]['cnt']
        stats['orders'] = db_execute("SELECT COUNT(*) as cnt FROM orders")[0]['cnt']
        recent_logs = db_execute("SELECT * FROM access_logs ORDER BY created_at DESC LIMIT 20")
    except Exception as e:
        flash(f"Stats error: {str(e)}", "danger")
        recent_logs = []
    return render_template('admin/dashboard.html', stats=stats, logs=recent_logs)


# ============================================================
# LEVEL 3: Blind Boolean SQLi in order management
# ============================================================
@admin_bp.route('/orders')
@admin_required
def orders():
    status_filter = request.args.get('status', '')
    error = None
    orders = []
    try:
        if status_filter:
            # VULNERABILITY Level 3: Boolean-blind injectable
            sql = f"SELECT o.*, u.username FROM orders o JOIN users u ON o.user_id=u.id WHERE o.status='{status_filter}'"
        else:
            sql = "SELECT o.*, u.username FROM orders o JOIN users u ON o.user_id=u.id ORDER BY o.created_at DESC"
        orders = db_execute(sql)
    except Exception as e:
        error = f"Query error: {str(e)}"
    return render_template('admin/orders.html', orders=orders, error=error, status_filter=status_filter)


# ============================================================
# LEVEL 3: Time-based blind SQLi in user lookup
# ============================================================
@admin_bp.route('/users')
@admin_required
def users():
    search = request.args.get('search', '')
    role_filter = request.args.get('role', '')
    error = None
    users = []
    try:
        if search:
            # VULNERABILITY Level 3: Time-based blind (no output reflected)
            sql = f"SELECT id, username, email, role, created_at FROM users WHERE username LIKE '%{search}%'"
            if role_filter:
                sql += f" AND role='{role_filter}'"
            users = db_execute(sql)
        else:
            users = db_execute("SELECT id, username, email, role, created_at FROM users")
    except Exception as e:
        error = f"User search error: {str(e)}"
    return render_template('admin/users.html', users=users, error=error)


# ============================================================
# LEVEL 4: Privilege escalation via SQLi
# ============================================================
@admin_bp.route('/update_user', methods=['POST'])
@admin_required
def update_user():
    user_id = request.form.get('user_id')
    role = request.form.get('role', 'user')
    # VULNERABILITY Level 4: Dual injection opportunity
    # - 'role' is in string context (inside quotes): inject with ' or admin'--
    # - 'user_id' is in numeric context (no quotes): inject with 1 OR 1=1
    # Combined: role='admin' WHERE 1=1-- escalates ALL users to admin
    sql = f"UPDATE users SET role='{role}' WHERE id={user_id}"
    try:
        db_execute(sql, fetch=False)
        flash(f"User {user_id} role updated to {role}", "success")
    except Exception as e:
        flash(f"Update error: {str(e)}", "danger")
    return redirect(url_for('admin.users'))


# ============================================================
# LEVEL 4: Cookie-based SQLi
# ============================================================
@admin_bp.route('/reports')
@admin_required
def reports():
    # VULNERABILITY Level 4: Cookie value is injectable
    report_type = request.cookies.get('report_type', 'summary')
    error = None
    data = []
    try:
        sql = f"SELECT * FROM orders WHERE status='{report_type}' ORDER BY created_at DESC LIMIT 50"
        data = db_execute(sql)
    except Exception as e:
        error = f"Report error: {str(e)}"
    return render_template('admin/reports.html', data=data, error=error, report_type=report_type)


# ============================================================
# LEVEL 4: Header-based SQLi
# ============================================================
@admin_bp.route('/audit')
@admin_required
def audit():
    # VULNERABILITY Level 4: X-Forwarded-For header injectable
    client_ip = get_client_ip()
    error = None
    logs = []
    try:
        sql = f"SELECT * FROM access_logs WHERE ip_address='{client_ip}' ORDER BY created_at DESC LIMIT 100"
        logs = db_execute(sql)
    except Exception as e:
        error = f"Audit error: {str(e)}"
    return render_template('admin/audit.html', logs=logs, error=error, ip=client_ip)

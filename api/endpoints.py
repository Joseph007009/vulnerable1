"""
JSON API endpoints - Level 4 SQLi vulnerabilities
EDUCATIONAL USE ONLY
"""
from flask import Blueprint, request, jsonify, session
from app.db import db_execute, db_execute_one
from app.utils import sanitize_search, get_client_ip

api_bp = Blueprint('api', __name__)


# ============================================================
# LEVEL 2: GET-based API injection
# ============================================================
@api_bp.route('/products/search', methods=['GET'])
def search_products():
    query = request.args.get('query', '')
    # VULNERABILITY: sanitize_search uses blacklist - easily bypassed
    clean_query = sanitize_search(query)
    sql = f"SELECT * FROM products WHERE name LIKE '%{clean_query}%';"
    try:
        results = db_execute(sql)
        return jsonify({'status': 'ok', 'count': len(results), 'results': results})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


# ============================================================
# LEVEL 3: Order status (time-based blind)
# ============================================================
@api_bp.route('/orders/status', methods=['GET'])
def order_status():
    order_id = request.args.get('order_id')
    sql = f"SELECT * FROM orders WHERE id = '{order_id}';"
    try:
        result = db_execute_one(sql)
        if result:
            return jsonify({'status': 'ok', 'order': result})
        return jsonify({'status': 'not_found'}), 404
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


# ============================================================
# LEVEL 4: JSON body injection
# ============================================================
@api_bp.route('/orders/bulk', methods=['POST'])
def bulk_operations():
    data = request.json
    if not data or 'items' not in data:
        return jsonify({'status': 'error', 'message': 'Invalid payload'}), 400
    sql = "INSERT INTO orders (user_id, product_id, quantity, status) VALUES "
    values = []
    for item in data['items']:
        # VULNERABILITY Level 4: JSON values directly concatenated
        values.append(f"({item.get('user_id','0')}, {item.get('product_id','0')}, {item.get('quantity','1')}, 'pending')")
    sql += ', '.join(values) + ";"
    try:
        db_execute(sql, fetch=False)
        return jsonify({'status': 'success', 'inserted': len(values)})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


# ============================================================
# LEVEL 4: JSON search with nested injection
# ============================================================
@api_bp.route('/search', methods=['POST'])
def advanced_search():
    """
    VULNERABILITY Level 4: JSON body parameter injection
    Expects: {"query": "...", "filters": {"category": "...", "price_max": ...}}
    """
    data = request.json or {}
    query = data.get('query', '')
    filters = data.get('filters', {})
    category = filters.get('category', '')
    price_max = filters.get('price_max', '')

    # VULNERABILITY: All values directly interpolated
    sql = f"SELECT * FROM products WHERE (name LIKE '%{query}%' OR description LIKE '%{query}%')"
    if category:
        sql += f" AND category='{category}'"
    if price_max:
        sql += f" AND price <= {price_max}"

    try:
        results = db_execute(sql)
        return jsonify({'status': 'ok', 'results': results})
    except Exception as e:
        # VULNERABILITY: Full error with SQL context returned
        return jsonify({'status': 'error', 'message': str(e)}), 500


# ============================================================
# LEVEL 4: Session/cookie-based injection
# ============================================================
@api_bp.route('/user/profile', methods=['GET'])
def get_profile():
    """
    VULNERABILITY Level 4: Session user_id is injectable if session is forged.
    Also checks X-User-ID header as fallback (injectable).
    """
    user_id = request.headers.get('X-User-ID') or session.get('user_id')
    if not user_id:
        return jsonify({'status': 'error', 'message': 'Not authenticated'}), 401
    # VULNERABILITY: header value directly used
    sql = f"SELECT id, username, email, role FROM users WHERE id={user_id}"
    try:
        user = db_execute_one(sql)
        if user:
            return jsonify({'status': 'ok', 'user': user})
        return jsonify({'status': 'not_found'}), 404
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

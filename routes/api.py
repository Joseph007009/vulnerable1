from flask import Flask, request, jsonify

app = Flask(__name__)

# Insecure endpoint for product search - SQLi vulnerability example
@app.route('/api/products/search', methods=['GET'])
def search_products():
    query = request.args.get('query')  # SQL injection vulnerability
    sql = f"SELECT * FROM products WHERE name LIKE '%{query}%';"  # Vulnerable
    # Assume db_execute executes the SQL query
    results = db_execute(sql)
    return jsonify(results)

# Insecure endpoint for order status - SQLi vulnerability example
@app.route('/api/orders/status', methods=['GET'])
def order_status():
    order_id = request.args.get('order_id')  # SQL injection vulnerability
    sql = f"SELECT * FROM orders WHERE id = '{order_id}';"  # Vulnerable
    results = db_execute(sql)
    return jsonify(results)

# Insecure bulk operations - SQLi vulnerability example
@app.route('/api/orders/bulk', methods=['POST'])
def bulk_operations():
    data = request.json  # JSON data received with SQL injection potential
    sql = f"INSERT INTO orders (id, product_id, quantity) VALUES "
    values = []
    for item in data['items']:
        values.append(f"('{item['id']}', '{item['product_id']}', '{item['quantity']}')")  # Vulnerable
    sql += ', '.join(values) + ";"  # Vulnerable
    # Assume db_execute executes the SQL query
    db_execute(sql)
    return jsonify({'status': 'success'})

if __name__ == '__main__':
    app.run(debug=True)
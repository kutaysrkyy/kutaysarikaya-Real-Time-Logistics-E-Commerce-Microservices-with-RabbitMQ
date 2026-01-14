from flask import Flask, render_template, request, jsonify
import sqlite3
import os

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "..", "order_service", "orders.db")

def get_orders():
    if not os.path.exists(DB_PATH): return []
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM orders ORDER BY id DESC")
    orders = cursor.fetchall()
    conn.close()
    return orders

@app.route('/')
def index():
    orders = get_orders()
    return render_template('index.html', orders=orders)

@app.route('/ship-order', methods=['POST'])
def ship_order():
    data = request.json
    order_id = data.get('id')
    address = data.get('address')
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    # Durumu senin onayınla "Kargoda" yapıyoruz
    cursor.execute("UPDATE orders SET status = 'Kargoda' WHERE id = ?", (order_id,))
    conn.commit()
    conn.close()
    
    print(f"📦 Siparis #{order_id} adrese kargolandi: {address}")
    return jsonify({"status": "success"})

if __name__ == "__main__":
    app.run(port=5005, debug=True)
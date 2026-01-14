from flask import Flask, request, jsonify, render_template
import sqlite3
import pika
import json

app = Flask(__name__)

# 100 Adet Ürün Havuzu
PRODUCTS = []
NAMES = ["Akilli Saat", "Bluetooth Kulaklik", "Gaming Mouse", "Sirt Cantasi", "Powerbank", "Mekanik Klavye", "Monitor"]
for i in range(1, 101):
    PRODUCTS.append({
        "id": i, 
        "name": f"{NAMES[i % len(NAMES)]} Pro v{i}", 
        "price": (i * 15) + 199,
        "category": "Elektronik" if i % 2 == 0 else "Aksesuar"
    })

def init_db():
    conn = sqlite3.connect('orders.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS orders 
                      (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                       customer TEXT, phone TEXT, product_name TEXT, status TEXT)''')
    conn.commit()
    conn.close()

@app.route('/')
def order_page():
    return render_template('order.html', products=PRODUCTS)

@app.route('/create-order', methods=['POST'])
def create_order():
    data = request.json
    conn = sqlite3.connect('orders.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO orders (customer, phone, product_name, status) VALUES (?, ?, ?, ?)",
                   (data['customer'], data['phone'], data['product_name'], 'Beklemede'))
    order_id = cursor.lastrowid
    conn.commit()
    conn.close()

    data['order_id'] = order_id
    # RabbitMQ Gönderimi
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='order_queue')
    channel.basic_publish(exchange='', routing_key='order_queue', body=json.dumps(data))
    connection.close()

    return jsonify({"order_id": order_id}), 201

@app.route('/check-status/<int:order_id>')
def check_status(order_id):
    conn = sqlite3.connect('orders.db')
    cursor = conn.cursor()
    cursor.execute("SELECT status FROM orders WHERE id = ?", (order_id,))
    res = cursor.fetchone()
    conn.close()
    return jsonify({"status": res[0] if res else "Bulunamadi"})

if __name__ == "__main__":
    init_db()
    app.run(port=5001, debug=True)
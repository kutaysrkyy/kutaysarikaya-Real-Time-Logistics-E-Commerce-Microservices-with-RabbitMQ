import pika, json, sqlite3, os

# Veritabanı yolu (Order Service'in DB'si)
DB_PATH = os.path.join("..", "order_service", "orders.db")

def update_db_status(order_id, new_status):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("UPDATE orders SET status = ? WHERE id = ?", (new_status, order_id))
    conn.commit()
    conn.close()

def callback(ch, method, properties, body):
    order = json.loads(body)
    print(f"[*] Sipariş alındı, stok kontrol ediliyor: {order['product_name']}")
    
    # Simülasyon: Stokta var varsayıyoruz ve durumu güncelliyoruz
    update_db_status(order['id'], "Hazırlanıyor") 
    print(f"[V] Durum 'Hazırlanıyor' olarak güncellendi.")
    
    ch.basic_ack(delivery_tag=method.delivery_tag)

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='order_queue')
channel.basic_consume(queue='order_queue', on_message_callback=callback)

print(' [*] Stok Servisi Dinlemede...')
channel.start_consuming()
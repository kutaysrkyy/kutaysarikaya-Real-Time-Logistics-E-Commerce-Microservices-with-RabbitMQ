import pika
import json

def callback(ch, method, properties, body):
    order = json.loads(body)
    print(f" [!] Yeni Siparis Dustu: {order['customer']} ({order['phone']}) - Urun: {order['product_name']}")

def start_logistics():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='order_queue')
    channel.basic_consume(queue='order_queue', on_message_callback=callback, auto_ack=True)
    print(' [*] Lojistik Servisi Dinlemede. Yonetici onayi bekleniyor...')
    channel.start_consuming()

if __name__ == "__main__":
    start_logistics()
import requests
import time

url = "http://127.0.0.1:5001/create-order"
data = {
    "customer": "Kutay Sarikaya",
    "product_name": "RTX 4090 Ekran Karti"
}

try:
    print("Sipariş gönderiliyor...")
    response = requests.post(url, json=data)
    print("Sunucu Yanıtı:", response.json())
except Exception as e:
    print("Hata! Sipariş servisi (Port 5001) açık mı?:", e)
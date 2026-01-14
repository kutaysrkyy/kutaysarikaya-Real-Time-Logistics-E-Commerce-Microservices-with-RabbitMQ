import requests

# Sipariş verileri
siparis = {
    "customer": "Kutay Sarikaya",
    "product_name": "Oyuncu Bilgisayari"
}

try:
    response = requests.post("http://127.0.0.1:5001/create-order", json=siparis)
    print("Durum Kodu:", response.status_code)
    print("Sunucu Cevabi:", response.json())
except Exception as e:
    print("Hata oluştu! Servis açık mı?:", e)
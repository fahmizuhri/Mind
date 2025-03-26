import requests
import time

# Konfigurasi API
COINGECKO_URL = "https://api.coingecko.com/api/v3/search/trending"
TELEGRAM_BOT_TOKEN = "8123204015:AAFcY0ybpfBG-oj2t7qLiyC03dT_vMvcBeI"
CHAT_ID = "453680427"

# Token yang ingin dipantau
WATCHED_TOKENS = ["mind of pepe", "solaxy"]

# Fungsi untuk mengirim pesan ke Telegram
def send_telegram_message(message, repeat=False):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    params = {"chat_id": CHAT_ID, "text": message}
    
    # Jika repeat=True, kirim pesan berkala (setiap 5 menit selama 30 menit)
    if repeat:
        for _ in range(6):  # 6x5 menit = 30 menit
            response = requests.get(url, params=params)
            print("\U0001F4E9 Response dari Telegram:", response.json())
            time.sleep(300)  # Tunggu 5 menit sebelum mengirim lagi
    else:
        response = requests.get(url, params=params)
        print("\U0001F4E9 Response dari Telegram:", response.json())

# Fungsi untuk mengecek listing di CoinGecko
def check_coingecko():
    response = requests.get(COINGECKO_URL)
    data = response.json()
    print("\U0001F4E1 Response dari CoinGecko:", data)
    
    if "coins" in data:
        trending_coins = [coin["item"]["name"].lower() for coin in data["coins"]]
        found_tokens = [token for token in WATCHED_TOKENS if token in trending_coins]
        
        if found_tokens:
            message = "\U0001F680 Token berikut telah listing di CoinGecko:\n" + "\n".join([f"\U0001F539 {token}" for token in found_tokens])
            send_telegram_message(message, repeat=True)
        else:
            send_telegram_message("⏳ Token belum terdaftar, coba lagi nanti.")
    else:
        send_telegram_message("❌ Gagal mengambil data dari CoinGecko.")

# Jalankan pengecekan secara berkala
while True:
    check_coingecko()
    time.sleep(1800)  # Cek setiap 30 menit

import os
import requests


def telegram_mesaj_gonder(mesaj: str) -> str:
    """
    Kullanıcıya Telegram üzerinden proaktif olarak bildirim veya mesaj göndermek için kullanılır.
    Özellikle arka plan görevleri bittiğinde veya önemli bir bilgi bulunduğunda kullanıcıyı
    haberdar etmek için bu aracı kullan.
    """
    # Bu bilgileri çevresel değişkenlerden (veya direkt buraya yazarak) alıyoruz
    bot_token = os.environ.get("TELEGRAM_BOT_TOKEN", "API_TOKEN_BURAYA")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID", "İD_BURAYA")

    if bot_token == "SENIN_BOT_TOKEN_BURAYA" or chat_id == "SENIN_CHAT_ID_BURAYA":
        return "HATA: Telegram Bot Token veya Chat ID ayarlanmamış. Lütfen ayarları yapın."

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": mesaj,
        "parse_mode": "Markdown"  # Mesajların kalın/italik gibi formatlı gitmesi için
    }

    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            return "BAŞARILI: Mesaj kullanıcıya Telegram üzerinden iletildi."
        else:
            return f"HATA: Mesaj gönderilemedi. Telegram API Yanıtı: {response.text}"
    except Exception as e:
        return f"HATA: Bağlantı sorunu oluştu: {str(e)}"
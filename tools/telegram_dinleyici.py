import os
import telebot


def telegram_dinleyici() -> str:
    """
    Telegram botuna gelen son okunmamış mesajları veya bildirimleri kontrol eder.
    Kullanıcı senden "Telegram'a yeni bir mesaj gelmiş mi?" veya "Gelen kutusuna bak"
    gibi bir istekte bulunduğunda bu aracı kullanarak son mesajları oku.

    Not: Eğer main.py (ana bot sistemi) zaten aktif olarak çalışıyor ve mesajları
    okuyorsa, bu araç "yeni mesaj yok" diyebilir çünkü mesajlar anında tüketiliyordur.
    """
    try:
        # Token'ı her zaman fonksiyon çalıştığı zaman (içeride) alıyoruz.
        # Bu sayede sistem başlarken (import edilirken) çökmesini kesin olarak engelliyoruz.
        bot_token = os.environ.get("TELEGRAM_BOT_TOKEN", "SENIN_BOT_TOKEN_BURAYA")

        # Gerçek bir token olup olmadığını basitçe kontrol ediyoruz (İçinde : olmalı)
        if bot_token == "SENIN_BOT_TOKEN_BURAYA" or ":" not in bot_token:
            return "HATA: Geçerli bir Telegram Bot Token bulunamadı. Lütfen ayarları kontrol edin."

        # Bot bağlantısını sadece model bu aracı kullanmaya karar verdiğinde başlatıyoruz
        bot = telebot.TeleBot(bot_token)

        # Telegram API'sine bağlanıp bekleyen (okunmamış) son 5 mesajı getiriyoruz
        updates = bot.get_updates(limit=5)

        if not updates:
            return "BİLGİ: Telegram botuna gelen yeni veya okunmamış bir mesaj yok."

        sonuclar = "--- BEKLEYEN TELEGRAM MESAJLARI ---\n"

        for update in updates:
            # Sadece metin içeren mesajları alıyoruz
            if update.message and update.message.text:
                gonderen_ad = update.message.from_user.first_name
                kullanici_adi = update.message.from_user.username or "Bilinmiyor"
                mesaj_metni = update.message.text

                sonuclar += f"- Gönderen: {gonderen_ad} (@{kullanici_adi}) | Mesaj: {mesaj_metni}\n"

        return sonuclar

    except Exception as e:
        return f"HATA: Telegram dinleyicisi çalışırken bir sorun oluştu: {str(e)}"
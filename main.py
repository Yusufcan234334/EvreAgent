import os
import telebot
from core import EvreAgent

# Telegram Bot Yapılandırması
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "BOT_TOKEN_BURAYA")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "CHAT_ID_BURAYA")

print("=" * 50)
print("EvreAgent Telegram Modunda Başlatılıyor...")
print("Lütfen bekleyin, sistem modülleri yükleniyor...")

agent = EvreAgent()
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

print("=" * 50)
print("Sistem Aktif! EvreAgent Telegram'da mesajlarınızı bekliyor.")

if TELEGRAM_CHAT_ID != "CHAT_ID_BURAYA":
    try:
        baslangic_mesaji = "🚀 *EvreAgent* başarıyla başlatıldı ve sistem aktif. Emirlerinizi bekliyorum!"
        bot.send_message(TELEGRAM_CHAT_ID, baslangic_mesaji, parse_mode="Markdown")
        print(f"[BİLGİ] Başlangıç mesajı {TELEGRAM_CHAT_ID} ID'li kullanıcıya gönderildi.")
    except Exception as e:
        print(f"\n[UYARI] Başlangıç mesajı Telegram'a iletilemedi: {str(e)}")

@bot.message_handler(commands=['start', 'basla'])
def send_welcome(message):
    hosgeldin_mesaji = (
        "Merhaba! Ben EvreAgent. Otonom yapay zeka asistanınım.\n"
        "Bana görevler verebilir, araştırma yapmamı isteyebilir veya sadece sohbet edebilirsin."
    )
    bot.reply_to(message, hosgeldin_mesaji)
    print(f"\n[BİLGİ] Kullanıcının Chat ID'si: {message.chat.id}")

@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    user_input = message.text
    chat_id = message.chat.id
    bot.send_chat_action(chat_id, 'typing')

    try:
        print(f"\n[Telegram - Kullanıcı]: {user_input}")
        response = agent.run(user_input)
        print(f"[EvreAgent - Cevap]: {response}")
        bot.reply_to(message, response)
    except Exception as e:
        hata_mesaji = f"İşlem sırasında beklenmeyen bir hata oluştu: {str(e)}"
        bot.reply_to(message, hata_mesaji)
        print(f"[SİSTEM HATASI]: {str(e)}")

if __name__ == "__main__":
    try:
        bot.infinity_polling(timeout=10, long_polling_timeout=5)
    except (KeyboardInterrupt, SystemExit):
        print("\nEvreAgent Telegram Botu kapatıldı.")
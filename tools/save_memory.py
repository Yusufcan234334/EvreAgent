from memory_manager import MemoryManager


def hafizaya_kaydet(anahtar: str, deger: str) -> str:
    """
    Kullanıcı veya sistem hakkında öğrenilen ÖNEMLİ bilgileri kalıcı hafızaya (JSON) kaydeder.
    Eğer kullanıcının adını, tercihlerini veya bir projenin önemli bir detayını öğrenirsen,
    bu aracı kullanarak o bilgiyi 'anahtar' ve 'deger' ikilisi olarak kaydet.

    Örnek anahtar: 'kullanici_adi', 'proje_fikri', 'favori_renk'
    """
    try:
        # Bellek yöneticisini başlatıyoruz (senin yazdığın memory_manager.py)
        manager = MemoryManager()

        # Eğer senin manager dosyanın içinde kayıt fonksiyonunun adı farklıysa
        # buradaki 'remember' veya 'save' kısmını kendi fonksiyon adına göre güncelleyebilirsin.
        # Varsayılan olarak bir önceki adımda konuştuğumuz yapıyı baz alıyorum.
        sonuc = manager.remember(anahtar, deger)

        return f"BAŞARILI: '{anahtar}' anahtarıyla '{deger}' bilgisi kalıcı hafızaya kaydedildi."
    except Exception as e:
        return f"HATA: Hafızaya kaydedilirken bir sorun oluştu: {str(e)}"
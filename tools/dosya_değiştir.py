import os


def dosya_icerik_degistir(dosya_yolu: str, eski_metin: str, yeni_metin: str) -> str:
    """
    Belirtilen bir dosyanın içindeki belirli bir metni bulur ve yeni bir metinle değiştirir.
    Kullanıcı senden bir koddaki hatayı düzeltmeni, bir kelimeyi başka bir kelimeyle
    değiştirmeni veya dosya içeriğini güncellemeni istediğinde bu aracı kullan.

    dosya_yolu: İçeriği değiştirilecek dosyanın tam yolu (Örn: 'main.py' veya 'ayarlar.txt').
    eski_metin: Dosyadan silinecek/değiştirilecek olan mevcut metin.
    yeni_metin: Eski metnin yerine yazılacak olan yeni metin.
    """
    try:
        if not os.path.exists(dosya_yolu):
            return f"HATA: İçeriği değiştirilecek dosya bulunamadı: '{dosya_yolu}'"

        # Dosyayı okuma modunda aç ve tüm içeriği al
        with open(dosya_yolu, 'r', encoding='utf-8') as dosya:
            icerik = dosya.read()

        if eski_metin not in icerik:
            return f"HATA: Değiştirilmek istenen '{eski_metin}' metni dosyada bulunamadı."

        # Metni değiştir
        yeni_icerik = icerik.replace(eski_metin, yeni_metin)

        # Değiştirilmiş içeriği aynı dosyaya yaz (üzerine yazma)
        with open(dosya_yolu, 'w', encoding='utf-8') as dosya:
            dosya.write(yeni_icerik)

        return f"BAŞARILI: '{dosya_yolu}' dosyasındaki içerik başarıyla güncellendi."
    except Exception as e:
        return f"HATA: Dosya içeriği değiştirilirken bir sorun oluştu: {str(e)}"
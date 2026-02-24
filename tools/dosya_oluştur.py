import os


def dosya_olustur(dosya_adi: str, icerik: str) -> str:
    """
    Belirtilen isimde ve içerikte yeni bir dosya oluşturur veya var olan dosyanın üzerine yazar.
    Kullanıcı senden bir kod yazmanı, bir metin/rapor kaydetmeni veya bir dosya oluşturmanı
    istediğinde bu aracı kullan.

    dosya_adi: Oluşturulacak dosyanın adı ve uzantısı (Örn: 'rapor.txt', 'script.py', 'index.html').
               Eğer klasör yolu içeriyorsa (Örn: 'ciktilar/rapor.txt'), o klasörleri de otomatik açar.
    icerik: Dosyanın içine yazılacak olan tam metin veya kod içeriği.
    """
    try:
        # Eğer dosya adı bir klasör yolu içeriyorsa (örn: 'raporlar/sonuc.txt')
        # Önce o klasörün var olduğundan emin olalım, yoksa oluşturalım.
        klasor_yolu = os.path.dirname(dosya_adi)
        if klasor_yolu and not os.path.exists(klasor_yolu):
            os.makedirs(klasor_yolu, exist_ok=True)

        # Dosyayı yazma ('w') modunda ve UTF-8 (Türkçe karakter destekli) formatında açıyoruz
        with open(dosya_adi, "w", encoding="utf-8") as f:
            f.write(icerik)

        return f"BAŞARILI: '{dosya_adi}' adlı dosya başarıyla oluşturuldu ve içerik kaydedildi."

    except Exception as e:
        return f"HATA: Dosya oluşturulurken bir sorun meydana geldi: {str(e)}"
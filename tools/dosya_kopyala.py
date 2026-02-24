import os
import shutil


def dosya_kopyala(kaynak_yol: str, hedef_yol: str) -> str:
    """
    Belirtilen bir dosyayı başka bir konuma veya farklı bir isimle kopyalar.
    Orijinal dosya yerinde kalır, sadece yeni bir kopyası oluşturulur.
    Kullanıcı bir dosyayı yedeklemek veya başka bir yere çoğaltmak istediğinde bu aracı kullan.

    kaynak_yol: Kopyalanacak orijinal dosyanın yolu (Örn: 'ornek.txt').
    hedef_yol: Dosyanın kopyalanacağı yeni yol veya yeni isim (Örn: 'yedekler/ornek_yedek.txt').
    """
    try:
        if not os.path.exists(kaynak_yol):
            return f"HATA: Kopyalanacak kaynak dosya bulunamadı: '{kaynak_yol}'"

        # Eğer hedef yol bir klasörün içindeyse, o klasörün var olduğundan emin olalım
        hedef_klasor = os.path.dirname(hedef_yol)
        if hedef_klasor and not os.path.exists(hedef_klasor):
            os.makedirs(hedef_klasor, exist_ok=True)

        # shutil.copy2 kullanarak dosyayı (izinleri ve tarihçesiyle birlikte) kopyalarız
        shutil.copy2(kaynak_yol, hedef_yol)
        return f"BAŞARILI: Dosya '{kaynak_yol}' konumundan '{hedef_yol}' konumuna başarıyla kopyalandı."
    except Exception as e:
        return f"HATA: Dosya kopyalanırken bir sorun meydana geldi: {str(e)}"
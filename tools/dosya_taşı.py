import os
import shutil


def dosya_tasi(kaynak_yol: str, hedef_yol: str) -> str:
    """
    Belirtilen bir dosyayı başka bir konuma taşır veya adını değiştirir.
    Kullanıcı bir dosyanın yerini değiştirmek veya dosyanın ismini güncellemek
    istediğinde bu aracı kullan.

    kaynak_yol: Taşınacak orijinal dosyanın yolu (Örn: 'eski_isim.txt').
    hedef_yol: Dosyanın taşınacağı yeni yol veya yeni isim (Örn: 'arsiv/yeni_isim.txt').
    """
    try:
        if not os.path.exists(kaynak_yol):
            return f"HATA: Taşınacak kaynak dosya bulunamadı: '{kaynak_yol}'"

        # Eğer hedef yol bir klasörün içindeyse ve klasör yoksa oluşturalım
        hedef_klasor = os.path.dirname(hedef_yol)
        if hedef_klasor and not os.path.exists(hedef_klasor):
            os.makedirs(hedef_klasor, exist_ok=True)

        # shutil.move kullanarak dosyayı taşırız (aynı klasördeyse yeniden adlandırma yapar)
        shutil.move(kaynak_yol, hedef_yol)
        return f"BAŞARILI: Dosya '{kaynak_yol}' konumundan '{hedef_yol}' konumuna başarıyla taşındı."
    except Exception as e:
        return f"HATA: Dosya taşınırken bir sorun meydana geldi: {str(e)}"
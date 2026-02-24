import os
import shutil


def klasor_tasi(kaynak_klasor: str, hedef_klasor: str) -> str:
    """
    Bir klasörü (ve içindeki tüm dosyaları) başka bir konuma taşır veya klasörün adını değiştirir.
    Kullanıcı bir klasörün yerini değiştirmek veya ismini güncellemek istediğinde bu aracı kullan.

    kaynak_klasor: Taşınacak veya adı değiştirilecek mevcut klasörün yolu.
    hedef_klasor: Klasörün yeni konumu veya yeni adı.
    """
    try:
        if not os.path.exists(kaynak_klasor):
            return f"HATA: Taşınacak kaynak klasör bulunamadı: '{kaynak_klasor}'"

        if not os.path.isdir(kaynak_klasor):
            return f"HATA: '{kaynak_klasor}' bir klasör değil. Dosya taşımak için 'dosya_tasi' aracını kullanın."

        # shutil.move, klasörü tüm içeriğiyle birlikte yeni yerine taşır
        shutil.move(kaynak_klasor, hedef_klasor)
        return f"BAŞARILI: Klasör '{kaynak_klasor}' konumundan '{hedef_klasor}' konumuna taşındı/yeniden adlandırıldı."
    except Exception as e:
        return f"HATA: Klasör taşınırken bir sorun meydana geldi: {str(e)}"
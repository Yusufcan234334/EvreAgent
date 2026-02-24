import os
import shutil


def klasor_kopyala(kaynak_klasor: str, hedef_klasor: str) -> str:
    """
    Bir klasörü ve içindeki TÜM dosya/alt klasörleri başka bir konuma kopyalar.
    Orijinal klasör yerinde kalır. Kullanıcı bütün bir projeyi veya klasörü yedeklemek,
    çoğaltmak istediğinde bu aracı kullan.

    kaynak_klasor: Kopyalanacak orijinal klasörün yolu.
    hedef_klasor: Kopyanın oluşturulacağı yeni klasörün yolu (Bu klasör önceden var olmamalıdır).
    """
    try:
        if not os.path.exists(kaynak_klasor):
            return f"HATA: Kopyalanacak kaynak klasör bulunamadı: '{kaynak_klasor}'"

        if not os.path.isdir(kaynak_klasor):
            return f"HATA: '{kaynak_klasor}' bir klasör değil. Dosya kopyalamak için 'dosya_kopyala' aracını kullanın."

        if os.path.exists(hedef_klasor):
            return f"HATA: Hedef klasör '{hedef_klasor}' zaten mevcut. Kopyalama işlemi için hedef klasörün henüz oluşturulmamış olması gerekir."

        # copytree tüm dizin ağacını kopyalar
        shutil.copytree(kaynak_klasor, hedef_klasor)
        return f"BAŞARILI: '{kaynak_klasor}' klasörü tüm içeriğiyle birlikte '{hedef_klasor}' olarak kopyalandı."
    except Exception as e:
        return f"HATA: Klasör kopyalanırken bir sorun meydana geldi: {str(e)}"
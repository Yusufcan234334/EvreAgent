import os


def dosya_sil(dosya_yolu: str) -> str:
    """
    Belirtilen yoldaki dosyayı kalıcı olarak siler.
    Kullanıcı senden gereksiz bir dosyanın silinmesini veya kaldırılmasını
    istediğinde bu aracı kullan.

    dosya_yolu: Silinecek dosyanın tam adı veya yolu (Örn: 'eski_rapor.txt', 'ciktilar/resim.png').
    """
    try:
        if os.path.exists(dosya_yolu):
            os.remove(dosya_yolu)
            return f"BAŞARILI: '{dosya_yolu}' adlı dosya başarıyla silindi."
        else:
            return f"HATA: '{dosya_yolu}' adında bir dosya bulunamadı."
    except Exception as e:
        return f"HATA: Dosya silinirken bir sorun meydana geldi: {str(e)}"
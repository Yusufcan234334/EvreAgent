import os


def klasor_olustur(klasor_yolu: str) -> str:
    """
    Bilgisayarda yeni bir klasör (dizin) oluşturur.
    Kullanıcı yeni bir proje başlatmak için, dosyaları gruplamak için veya
    yeni bir dizine ihtiyaç duyduğunda bu aracı kullan. İç içe klasörleri de (örn: 'ana/alt/klasor') tek seferde oluşturabilir.

    klasor_yolu: Oluşturulacak klasörün adı veya yolu (Örn: 'yeni_proje' veya 'arsivler/2026/raporlar').
    """
    try:
        if os.path.exists(klasor_yolu):
            return f"BİLGİ: '{klasor_yolu}' adında bir klasör zaten mevcut."

        # exist_ok=True parametresi klasör zaten varsa hata vermesini engeller
        os.makedirs(klasor_yolu, exist_ok=True)
        return f"BAŞARILI: '{klasor_yolu}' klasörü başarıyla oluşturuldu."
    except Exception as e:
        return f"HATA: Klasör oluşturulurken bir sorun meydana geldi: {str(e)}"
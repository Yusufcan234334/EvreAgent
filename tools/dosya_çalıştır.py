import os
import subprocess


def dosya_calistir(komut: str) -> str:
    """
    Kullanıcının bilgisayarında terminal/cmd komutları veya dosyalar (scriptler) çalıştırır.

    ÖNEMLİ: Eğer kullanıcı senden bir Python kodu yazmanı ve çalıştırmanı isterse:
    1. Önce 'dosya_olustur' aracı ile kodu bir .py dosyasına kaydet.
    2. Sonra bu aracı kullanarak 'python dosya_adi.py' komutuyla o dosyayı çalıştır.

    Çalışan kodun veya komutun terminal çıktısını (veya hata mesajını) geri döndürür.
    Böylece kodda bir hata varsa okuyup düzeltebilirsin.

    komut: Çalıştırılacak terminal komutu veya dosya adı (Örn: 'python test.py', 'dir', 'ls -la').
    """
    try:
        # shell=True parametresi, komutun doğrudan sistem terminalinde (cmd/bash) çalışmasını sağlar
        # capture_output=True parametresi, ekrana yazdırılan sonucu (print) veya hatayı yakalamamızı sağlar
        sonuc = subprocess.run(
            komut,
            shell=True,
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace'
        )

        # Eğer komut başarıyla çalıştıysa
        if sonuc.returncode == 0:
            cikti = sonuc.stdout.strip()
            if not cikti:
                return f"BAŞARILI: '{komut}' çalıştırıldı ancak ekrana bir şey yazdırmadı."
            return f"BAŞARILI: Komut Çıktısı:\n{cikti}"

        # Eğer komutta bir hata olduysa (örn: SyntaxError)
        else:
            hata = sonuc.stderr.strip()
            return f"HATA: Komut çalışırken hata verdi (Kod: {sonuc.returncode}):\n{hata}"

    except Exception as e:
        return f"SİSTEM HATASI: Komut çalıştırılamadı: {str(e)}"
import subprocess
import platform


def cmd_komutu(komut: str) -> str:
    """
    Sistem terminalinde (Windows'ta CMD, Linux/macOS'ta Terminal) doğrudan komut çalıştırır.
    Sistem bilgilerini kontrol etmek, ağ testi yapmak (ping), yüklü paketlere bakmak
    veya terminal üzerinden yapılabilecek her türlü işlem için bu aracı kullan.

    komut: Çalıştırılacak terminal komutu (Örn: 'ipconfig', 'ping google.com', 'systeminfo').
    """
    try:
        # İşletim sistemini algıla (çıktı formatını anlamak için yardımcı olabilir)
        isletim_sistemi = platform.system()

        # Komutu sistem kabuğunda (shell) çalıştırıyoruz
        # capture_output=True ile hem standart çıktıyı hem de hataları yakalıyoruz
        process = subprocess.run(
            komut,
            shell=True,
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace'
        )

        # Sonuçları derle
        cikti = process.stdout.strip()
        hata = process.stderr.strip()
        donus_kodu = process.returncode

        yapi = f"--- [{isletim_sistemi}] KOMUT YÜRÜTME SONUCU ---\n"
        yapi += f"Çalıştırılan Komut: {komut}\n"
        yapi += f"Durum Kodu: {donus_kodu} ({'Başarılı' if donus_kodu == 0 else 'Hatalı'})\n\n"

        if cikti:
            yapi += f"[STANDART ÇIKTI]:\n{cikti}\n"

        if hata:
            yapi += f"\n[HATA ÇIKTISI]:\n{hata}\n"

        if not cikti and not hata:
            yapi += "Komut çalıştırıldı ancak herhangi bir çıktı üretilmedi."

        return yapi

    except Exception as e:
        return f"SİSTEM HATASI: Komut yürütülürken beklenmedik bir sorun oluştu: {str(e)}"
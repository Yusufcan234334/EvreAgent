from duckduckgo_search import DDGS


def duckduckgo_arama(sorgu: str, max_sonuc: int = 5) -> str:
    """
    İnternette güncel bilgi aramak için DuckDuckGo arama motorunu kullanır.
    Eğer kullanıcının sorusu güncel olaylar, haberler, hava durumu veya senin kendi
    veritabanında bilmediğin gerçek zamanlı bilgiler gerektiriyorsa bu aracı kullan.

    sorgu: İnternette aranacak kelime veya cümle (Örn: 'Türkiye yapay zeka haberleri').
    max_sonuc: Getirilecek maksimum sonuç sayısı (Varsayılan 5, gerekirse artırılabilir).
    """
    try:
        # DuckDuckGo üzerinden aramayı gerçekleştiriyoruz
        with DDGS() as ddgs:
            # text fonksiyonu doğrudan web sonuçlarını getirir
            sonuclar = list(ddgs.text(sorgu, max_results=max_sonuc))

        if not sonuclar:
            return f"BULUNAMADI: '{sorgu}' için internette hiçbir sonuç bulunamadı."

        # Modelin kolayca okuyup anlayabileceği şekilde sonuçları metne döküyoruz
        formatli_metin = f"--- '{sorgu}' İÇİN İNTERNET ARAMA SONUÇLARI ---\n\n"

        for i, sonuc in enumerate(sonuclar, 1):
            baslik = sonuc.get('title', 'Başlık Yok')
            ozet = sonuc.get('body', 'Özet Yok')
            link = sonuc.get('href', 'Link Yok')

            formatli_metin += f"{i}. BAŞLIK: {baslik}\n"
            formatli_metin += f"   ÖZET: {ozet}\n"
            formatli_metin += f"   KAYNAK LİNKİ: {link}\n\n"

        return formatli_metin

    except Exception as e:
        return f"HATA: İnternette arama yapılırken bir sorun oluştu: {str(e)}"
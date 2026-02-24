import webbrowser


def web_sitesi_ac(url: str) -> str:
    """
    Kullanıcının bilgisayarındaki varsayılan web tarayıcısında (Chrome, Safari vb.)
    belirtilen URL'yi açar. Kullanıcı "bana youtube'u aç", "şu siteye gir" veya
    "müzik aç" dediğinde bu aracı kullan.

    url: Açılacak web sitesinin tam adresi (Örn: 'https://www.youtube.com' veya 'https://google.com').
         Eğer URL 'http' ile başlamıyorsa, başına otomatik eklemelisin.
    """
    try:
        # Eğer url http veya https ile başlamıyorsa düzeltelim
        if not url.startswith('http://') and not url.startswith('https://'):
            url = 'https://' + url

        # webbrowser.open() fonksiyonu kullanıcının tarayıcısında yeni bir sekme açar
        basarili_mi = webbrowser.open(url)

        if basarili_mi:
            return f"BAŞARILI: '{url}' adresi kullanıcının tarayıcısında açıldı."
        else:
            return f"HATA: Tarayıcı tetiklenemedi veya desteklenmeyen bir ortam."

    except Exception as e:
        return f"HATA: Web sitesi açılırken bir sorun oluştu: {str(e)}"
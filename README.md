# EvreAgent: Kendi Otonom ve Modüler Asistanın

EvreAgent, başta Groq API olmak üzere farklı dil modelleriyle çalışabilen, tamamen modüler ve otonom hareket edebilen bir yapay zeka ajanıdır. Bu projeyi geliştirirken temel amacım; kolayca yeni yetenekler ekleyebildiğim, beni tanıyan ve karmaşık görevleri kendi başına planlayıp çözebilen bir asistan oluşturmaktı.

## Neden EvreAgent?

Piyasadaki karmaşık ve kapalı yapılar yerine, her şeyi dosyalarla yönetebildiğim ve koduna doğrudan müdahale edebildiğim bir sistem istedim. OpenClaw mimarisinden esinlenerek geliştirdiğim bu ajanda, her bir yetenek sadece bir Python dosyasından ibarettir. Ayrıca çekirdek yapısı değiştirilebilir olduğu için isteyen Groq yerine GPT veya yerel (OSS) modelleri de sisteme entegre edebilir.

## Öne Çıkan Özellikler

* **Modüler Yapı:** Yeni bir özellik eklemek istediğimde sadece `tools/` klasörüne bir Python dosyası ekliyorum. Sistem bunu anında algılıyor.

* **Canlı Yükleme (Hot-Reload):** En sevdiğim özelliklerden biri; program çalışırken yeni bir araç eklediğimde veya mevcut bir aracı güncellediğimde sistemi yeniden başlatmam gerekmiyor.

* **Esnek Model Desteği:** Varsayılan olarak Groq hızı için yapılandırılmış olsa da, `core.py` üzerindeki bağlantı yapısı değiştirilerek OpenAI veya yerel LLM modelleriyle de kullanılabilir.

* **Telegram:** EvreAgent ile Telegram üzerinden onunla normal bir insanla konuşur gibi sohbet edebilir, görevler verebilir ve araştırmalarını takip edebilirsiniz. Tüm otonom süreç Telegram arayüzü üzerinden yönetilir.

* **Beni Tanıyan Bellek Sistemi:**
  * **Kısa Süreli Bellek:** O anki sohbetimizi unutmaması için tasarlandı.
  * **Uzun Süreli Bellek:** Kullanıcı hakkında öğrendiği önemli bilgileri kalıcı olarak bir JSON dosyasında saklıyor.
  * **Görev Durumu:** Bir iş verirken hangi aşamada olduğunu adım adım takip ediyor.

* **Görev Planlama (Mission Planning):** Karmaşık bir şey istediğimde (örneğin bir araştırma görevi), ajan önce bir plan yapıyor ve bu planı `mission.json` dosyasına yazarak sırayla uyguluyor.

* **Arka Plan Rutinleri:** `cfg.json` üzerinden ayarladığım sürelerde ajan kendi kendine uyanıp hafızasını tazeleyebiliyor veya verilen görevleri arka planda sürdürebiliyor.

## Proje Yapısı

    EvreAgent/
    ├── main.py             # Sistemin giriş kapısı ve Telegram sohbet arayüzü
    ├── core.py             # Ajanın karar verme merkezi ve beyni
    ├── tool_manager.py     # Araçları dinamik olarak yükleyen birim
    ├── memory_manager.py   # Kalıcı hafızadan sorumlu modül
    ├── cfg.json            # Çalışma zamanı ayarlarım
    ├── requirements.txt    # Gerekli paketler
    ├── memory/             # Tüm hafıza kayıtlarının tutulduğu yer
    └── tools/              # Ajanın kazandığı tüm yetenekler
        ├── duckduckgo_arama.py
        ├── dosya_olustur.py
        └── ...

## Kurulum ve Çalıştırma

Kendi ortamınızda denemek isterseniz şu adımları izleyebilirsiniz:

1. Önce gerekli kütüphaneleri kurun:
    ```bash
    pip install -r requirements.txt
    ```

2. Çevresel değişkenleri ayarlayın veya kod içindeki ilgili alanları doldurun:
   * Groq veya tercih ettiğiniz modelin API anahtarını tanımlayın.
   * Telegram Bot Token ve Chat ID bilgilerinizi girin.

3. Sistemi başlatın:
    ```bash
    python main.py
    ```

## Yeni Bir Yetenek Eklemek

Ajanıma yeni bir şey öğretmek istediğimde `tools/` klasörüne gidip şöyle basit bir dosya oluşturuyorum:

    # tools/selamla.py

    def selamla(isim: str) -> str:
        """Kullanıcıya özel bir selamlama gönderir."""
        return f"Selam {isim}, bugün senin için ne yapabilirim?"

Dosyayı kaydettiğim an EvreAgent bu yeteneği Telegram sohbeti sırasında kullanmaya hazır hale geliyor.

Developed by **Yusufcan234334**

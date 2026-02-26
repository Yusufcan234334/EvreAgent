import os
import json
import threading
import time
from groq import Groq
from tool_manager import ToolManager
from memory_manager import MemoryManager

class ShortTermMemory:
    """Ajanın o anki oturumdaki sohbet geçmişini memory/short_term.json dosyasında tutar."""

    def __init__(self, system_prompt, file_path="memory/short_term.json"):
        self.file_path = file_path
        self.system_prompt = system_prompt

        # Klasörün var olduğundan emin olalım
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)

        # Dosyayı yükle, eğer yoksa veya boşsa system_prompt ile başlat
        self.messages = self._load()
        if not self.messages:
            self.messages.append({
                "role": "system",
                "content": self.system_prompt
            })
            self._save()

    def _load(self):
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return []
        return []

    def _save(self):
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(self.messages, f, ensure_ascii=False, indent=4)

    def add_user_message(self, content):
        self.messages.append({"role": "user", "content": content})
        self._save()

    def add_assistant_message(self, message_obj):
        # Groq'un döndürdüğü mesaj objesini JSON formatına (dictionary) dönüştürüyoruz
        msg_dict = {"role": "assistant", "content": message_obj.content}

        if getattr(message_obj, "tool_calls", None):
            msg_dict["tool_calls"] = []
            for tool_call in message_obj.tool_calls:
                msg_dict["tool_calls"].append({
                    "id": tool_call.id,
                    "type": "function",
                    "function": {
                        "name": tool_call.function.name,
                        "arguments": tool_call.function.arguments
                    }
                })

        self.messages.append(msg_dict)
        self._save()

    def add_tool_result(self, tool_call_id, tool_name, content):
        self.messages.append({
            "tool_call_id": tool_call_id,
            "role": "tool",
            "name": tool_name,
            "content": content,
        })
        self._save()

    def get_messages(self):
        return self.messages


class TaskState:
    """Ajanın o an ilgilendiği görevin aşamalarını memory/task_state.json dosyasında takip eder."""

    def __init__(self, file_path="memory/task_state.json"):
        self.file_path = file_path
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)

        self.current_task = None
        self.completed_steps = []
        self.status = "beklemede"
        self._load()

    def _load(self):
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.current_task = data.get("current_task")
                    self.completed_steps = data.get("completed_steps", [])
                    self.status = data.get("status", "beklemede")
            except json.JSONDecodeError:
                pass

    def _save(self):
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump({
                "current_task": self.current_task,
                "completed_steps": self.completed_steps,
                "status": self.status
            }, f, ensure_ascii=False, indent=4)

    def set_task(self, task_description):
        self.current_task = task_description
        self.status = "devam_ediyor"
        self.completed_steps = []
        self._save()

    def add_completed_step(self, step_description):
        self.completed_steps.append(step_description)
        self._save()

    def complete_task(self):
        self.status = "tamamlandi"
        self._save()

class EvreAgent:
    def __init__(self, api_key="KEY_BURAYA", model_name="openai/gpt-oss-120b"):
        # Groq API bağlantısı
        self.client = Groq(api_key=api_key or os.environ.get("GROQ_API_KEY"))
        self.model_name = model_name

        # Yöneticiler
        self.tool_manager = ToolManager()
        self.memory_manager = MemoryManager()  # Uzun süreli JSON bellek bağlandı (memory/long_term_data.json)
        self.task_state = TaskState()  # JSON tabanlı görev yöneticisi

        # Eğer uzun süreli bellek tamamen boşsa, varsayılan (default) bir kimlik belleği oluşturalım
        if not self.memory_manager.get_all_memories():
            self.memory_manager.remember("evreagent_kimligi",
                                         "Senin adın EvreAgent, otonom ve modüler bir yapay zeka asistanısın.")
            self.memory_manager.remember("yaratilis_amaci",
                                         "Kullanıcının verdiği karmaşık görevleri parçalara ayırarak ve araçları (tools) kullanarak çözmek.")

        # Ajanın temel kimliği ve Çalışma Döngüsü (Loop) Kuralları detaylandırıldı
        self.base_system_prompt = (
            "Sen modüler ve otonom bir yapay zeka ajanısın. Adın EvreAgent.\n\n"
            "--- ÇALIŞMA DÖNGÜSÜ (LOOP) VE KURALLAR ---\n"
            "1. DÜŞÜN: Sana verilen görevi analiz et.\n"
            "2. ARAÇ KULLAN (Gerekliyse): Görevi çözmek için dışarıdan veriye veya bir işleme ihtiyacın varsa ilgili araçları (tools) ÇAĞIR ve sonucun gelmesini bekle.\n"
            "3. TEKRARLA: Araçtan dönen sonuç yeterli değilse, eksik olan bilgi için tekrar araç çağırabilirsin. Bu senin çalışma döngündür.\n"
            "4. NİHAİ CEVAP: Tüm bilgileri topladıysan VEYA sorunun cevabını kendi başına biliyorsan (araca gerek yoksa), "
            "HİÇBİR ARAÇ ÇAĞIRMADAN doğrudan cevabını yaz. Sen araç çağırmadığın anda döngü biter ve kullanıcı cevabını görür.\n\n"
            "--- BELLEK YÖNETİMİ ---\n"
            "Arka planda otomatik çalışan Uzun Süreli Belleğin (Long-Term Memory) var. Önemli bilgiler oraya kaydedilir "
            "ve her mesajdan önce UZUN SÜRELİ BELLEK başlığı altında sana hatırlatılır. Bu bilgileri zaten biliyormuş gibi doğal davran.\n\n"
            "Adım adım düşün, planlı ilerle ve döngü kurallarına kesinlikle uy."
        )

        # Kısa süreli belleği (Sohbet geçmişini) JSON tabanlı olarak başlatıyoruz
        self.memory = ShortTermMemory(system_prompt=self.base_system_prompt)

        # Ayarları (cfg.json) yükle
        self.config = self._load_config()

        # Arka plan görevlerini yönetecek iş parçacığını başlat (Daemon: ana program kapanınca o da kapanır)
        self.bg_thread = threading.Thread(target=self._background_worker, daemon=True)
        self.bg_thread.start()

    def _load_config(self):
        """Ana dizindeki cfg.json dosyasını okur. Yoksa varsayılan ayarlarla oluşturur."""
        cfg_path = "cfg.json"
        if not os.path.exists(cfg_path):
            default_config = {
                "enable_background_tasks": False,  # Sadece mesaj geldiğinde uyanması için varsayılan False
                "background_interval_minutes": 5
            }
            with open(cfg_path, "w", encoding="utf-8") as f:
                json.dump(default_config, f, indent=4, ensure_ascii=False)
            return default_config

        try:
            with open(cfg_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {"enable_background_tasks": False, "background_interval_minutes": 5}

    def _background_worker(self):
        """
        cfg.json içindeki ayarlara göre belirli aralıklarla uyanıp işlem yapar.
        Çalışma zamanında ayar değiştirilirse anında algılar.
        """
        while True:
            # Ayarları her döngüde tekrar oku ki anlık değişiklikler algılansın
            self.config = self._load_config()
            interval_minutes = self.config.get("background_interval_minutes", 5)

            time.sleep(interval_minutes * 60)

            if self.config.get("enable_background_tasks", False):
                print(f"\n[ARKAPLAN] EvreAgent uyandı ({interval_minutes} dk rutini). Bellekleri gözden geçiriyor...")
                # Ajan uyandığında belleğindeki bilgileri tazeler
                self._update_system_prompt_with_memory()

                # Arka planda uyandıkça yeni bir araç eklenmiş mi diye tools klasörünü canlı olarak tarar
                self.tool_manager = ToolManager()

    def _auto_generate_mission(self, user_input):
        """
        [ARKAPLAN İŞLEMİ] Kullanıcı isteği karmaşık bir araştırma veya işlem gerektiriyorsa,
        bunu adımlara böler ve 'mission.json' dosyasına yazar.
        """
        mission_prompt = f"""
        Aşağıdaki kullanıcı isteğini analiz et. Eğer bu istek karmaşık, çok adımlı bir araştırma, 
        veri toplama veya planlama gerektiriyorsa (örneğin 'şu konuyu araştır' gibi), bunu JSON formatında 
        bir görev planına dönüştür. Basit sohbet, selamlaşma veya tek kelimelik sorularda boş JSON {{}} döndür.

        Örnek Çıktı Formatı:
        {{
            "gorev_adi": "Konu Araştırması",
            "adimlar": [
                "1. Konuyla ilgili anahtar kelimeleri ve argümanları bul",
                "2. Araçları kullanarak internette sırayla arama yap",
                "3. Tüm sonuçları kısa süreli belleğe (short memory) yazarak derle",
                "4. Toplanan verileri kullanıcıya özetle ve nihai cevabı ver"
            ]
        }}
        SADECE JSON FORMATINDA CEVAP VER.

        Kullanıcı Mesajı: "{user_input}"
        """
        try:
            # Daha hızlı çalışması için küçük model
            response = self.client.chat.completions.create(
                model="openai/gpt-oss-20b",
                messages=[{"role": "user", "content": mission_prompt}],
                response_format={"type": "json_object"}
            )

            mission_data = json.loads(response.choices[0].message.content)

            if mission_data and "adimlar" in mission_data:
                # Görevi mission.json olarak kaydet
                with open("mission.json", "w", encoding="utf-8") as f:
                    json.dump(mission_data, f, ensure_ascii=False, indent=4)
                print(
                    f"\n[GÖREV PLANI] Karmaşık işlem algılandı! 'mission.json' oluşturuldu: {mission_data.get('gorev_adi')}")
                return mission_data

        except Exception as e:
            print(f"[GÖREV SİSTEMİ BİLGİSİ] Görev planlaması atlandı: {str(e)}")

        return None

    def _auto_extract_and_save_memory(self, user_input):
        """
        [ARKAPLAN İŞLEMİ] Kullanıcının mesajını okur, eğer hatırlanması gereken önemli bir
        bilgi varsa bunu otomatik olarak JSON dosyasına kaydeder.
        """
        extraction_prompt = f"""
        Aşağıdaki kullanıcı mesajını analiz et. Eğer kullanıcının kendisi, tercihleri, projeleri 
        veya gelecekte hatırlanması gereken kalıcı/önemli bir bilgi varsa, bunu JSON formatında 
        anahtar-değer (key-value) şeklinde çıkar. Eğer önemli bir bilgi yoksa boş JSON {{}} döndür.

        Örnek Çıktı: {{"kullanici_adi": "Ahmet", "proje_dili": "Python"}} VEYA {{}}
        SADECE JSON FORMATINDA CEVAP VER.

        Kullanıcı Mesajı: "{user_input}"
        """
        try:
            # Daha hızlı ve ucuz çalışması için arka planda küçük modeli (20b) kullanıyoruz
            response = self.client.chat.completions.create(
                model="openai/gpt-oss-20b",
                messages=[{"role": "user", "content": extraction_prompt}],
                response_format={"type": "json_object"}  # Kesinlikle JSON dönmesini zorluyoruz
            )

            extracted_data = json.loads(response.choices[0].message.content)

            # Eğer çıkarılan veri boş değilse, bunları memory_manager üzerinden JSON'a kaydet
            if extracted_data:
                for key, value in extracted_data.items():
                    # Burada memory_manager içindeki kaydetme fonksiyonunu çağırıyoruz
                    self.memory_manager.remember(key, value)
                    print(f"[BELLEK] Yeni bilgi öğrenildi ve kaydedildi: {key} -> {value}")

        except Exception as e:
            # Arka plan işleminde hata olursa sistemi durdurmaması için sadece yazdırıyoruz
            print(f"[BELLEK SİSTEMİ BİLGİSİ] Veri çıkarımı atlandı: {str(e)}")

    def _update_system_prompt_with_memory(self):
        """
        [ARKAPLAN İŞLEMİ] Uzun süreli bellekteki tüm bilgileri JSON dosyasından çeker
        ve modelin zaten bildiği bir bilgi olarak sistem komutunun sonuna ekler.
        Böylece model araç çağırmadan her şeyi hatırlar.
        """
        # Senin yazdığın dosyadan tüm bilgileri çekiyoruz
        all_memories = self.memory_manager.get_all_memories()

        memory_text = "\n\n[UZUN SÜRELİ BELLEK BİLGİLERİ - BUNLARI ZATEN BİLİYORSUN]\n"
        if all_memories:
            for key, value in all_memories.items():
                memory_text += f"- {key}: {value}\n"
        else:
            # Boş olma durumunda da varsayılan bir uyarı çıkarıyoruz
            memory_text += "- Varsayılan Bellek Durumu: Henüz kaydedilmiş kalıcı özel bir bilgin yok.\n"

        # Kısa süreli bellekteki 0. indeks her zaman System Prompt'tur. Onu güncelliyoruz.
        self.memory.messages[0]["content"] = self.base_system_prompt + memory_text

        # Güncellenen yeni system prompt'un da JSON dosyasına yansıması için kaydediyoruz
        self.memory._save()

    def run(self, user_input):
        self.task_state.set_task(user_input)

        # Dinamik Araç Yükleme (Hot-Reload)
        # EvreAgent her yeni sorunda araç klasörünü tekrar tarar. Program çalışırken bile
        # 'tools/' klasörüne yeni bir dosya atarsan anında o yeteneği kazanır.
        self.tool_manager = ToolManager()

        # 1. Adım: Kullanıcı mesajından önemli bilgileri çıkarıp JSON'a kaydet (Arka plan)
        self._auto_extract_and_save_memory(user_input)

        # 2. Adım: JSON dosyasındaki güncel bilgileri modelin beynine yükle (Arka plan)
        self._update_system_prompt_with_memory()

        # 3. Adım: Görev/Plan oluşturma (Karmaşık şeyler için mission.json oluşturur)
        mission_plan = self._auto_generate_mission(user_input)

        # 4. Adım: Kullanıcının mesajını sohbet geçmişine ekle
        self.memory.add_user_message(user_input)

        # Eğer görev planı oluşturulduysa, modeli bu adımlara uyması için zorunlu tut
        if mission_plan:
            plan_text = "[AKTİF GÖREV PLANIN]\nLütfen araçlarını (tools) kullanarak aşağıdaki adımları sırasıyla uygula:\n"
            for adim in mission_plan["adimlar"]:
                plan_text += f"- {adim}\n"
            plan_text += "Her adımı tamamladıktan sonra diğerine geç. Tüm adımlar bitince kullanıcıya nihai cevabı ver."

            # Bu planı sisteme, modelin görebileceği ama kullanıcının görmediği bir "iç düşünce" olarak ekliyoruz
            self.memory.messages.append({
                "role": "system",
                "content": plan_text
            })
            self.memory._save()

        while True:
            # Model, belleğe yüklenmiş geçmişiyle ve araçlarıyla birlikte düşünmeye başlar
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=self.memory.get_messages(),
                tools=self.tool_manager.get_tool_schemas(),
                tool_choice="auto",
                max_tokens=4096
            )

            response_message = response.choices[0].message

            # Modelin verdiği cevabı sohbet geçmişine ekliyoruz (Artık JSON'a da kaydediliyor)
            self.memory.add_assistant_message(response_message)

            # Model bir araç (tool) kullanmak istediyse işlemleri yap
            if response_message.tool_calls:
                for tool_call in response_message.tool_calls:
                    function_name = tool_call.function.name
                    function_args = json.loads(tool_call.function.arguments)

                    print(f"[EvreAgent] Araç kullanıyor: {function_name}({function_args})")

                    # Tool Manager üzerinden aracı çalıştır
                    tool_result = self.tool_manager.execute_tool(function_name, **function_args)

                    # Aracın sonucunu belleğe ekle (Bu da anında JSON'a yazılır)
                    self.memory.add_tool_result(
                        tool_call_id=tool_call.id,
                        tool_name=function_name,
                        content=tool_result
                    )
                    self.task_state.add_completed_step(f"'{function_name}' aracı kullanıldı.")
            else:
                # Model bir araç çağırmadıysa işlemi bitirmiştir, nihai cevabı döndür
                self.task_state.complete_task()

                return response_message.content

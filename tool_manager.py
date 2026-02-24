import os
import importlib
import inspect


class ToolManager:
    def __init__(self, tools_dir="tools"):
        self.tools_dir = tools_dir
        self.tools = {}
        self._load_tools()

    def _load_tools(self):
        """
        tools klasöründeki tüm Python dosyalarını tarar ve içindeki
        uygun fonksiyonları sisteme kaydeder.
        """
        if not os.path.exists(self.tools_dir):
            os.makedirs(self.tools_dir)

        for filename in os.listdir(self.tools_dir):
            if filename.endswith(".py") and filename != "__init__.py":
                module_name = filename[:-3]
                module_path = f"{self.tools_dir}.{module_name}"

                try:
                    # Modülü dinamik olarak içe aktar
                    module = importlib.import_module(module_path)

                    # Modül içindeki fonksiyonları bul ve kaydet
                    for name, func in inspect.getmembers(module, inspect.isfunction):
                        # Sadece gizli olmayan (alt çizgi ile başlamayan)
                        # ve o modülde tanımlanmış fonksiyonları al (başka yerden import edilenleri alma)
                        if not name.startswith("_") and func.__module__ == module_path:
                            self.tools[name] = func
                except Exception as e:
                    print(f"[UYARI] '{filename}' aracı yüklenirken hata oluştu: {e}")

    def get_tool_schemas(self):
        """
        Groq API'sinin anlayabileceği formatta araç tanımlarını (schema) oluşturur.
        Fonksiyonların 'docstring' (açıklama) kısımlarını kullanarak modeli bilgilendirir.
        """
        # Eğer hiç araç yoksa None döndür, böylece Groq API hata vermez
        if not self.tools:
            return None

        schemas = []
        for name, func in self.tools.items():
            # Fonksiyonun açıklamasını al, yoksa varsayılan bir isim koy
            docstring = inspect.getdoc(func) or f"{name} fonksiyonu."

            # Fonksiyon parametrelerini analiz et
            sig = inspect.signature(func)
            properties = {}
            required = []

            for param_name, param in sig.parameters.items():
                # Python tiplerini JSON tiplerine çevir
                param_type = "string"
                if param.annotation != inspect.Parameter.empty:
                    if param.annotation == int:
                        param_type = "integer"
                    elif param.annotation == bool:
                        param_type = "boolean"
                    elif param.annotation == float:
                        param_type = "number"

                properties[param_name] = {
                    "type": param_type,
                    "description": f"{param_name} parametresi."
                }

                # Eğer parametrenin varsayılan bir değeri yoksa, bu zorunludur
                if param.default == inspect.Parameter.empty:
                    required.append(param_name)

            schemas.append({
                "type": "function",
                "function": {
                    "name": name,
                    "description": docstring,
                    "parameters": {
                        "type": "object",
                        "properties": properties,
                        "required": required
                    }
                }
            })

        return schemas

    def execute_tool(self, function_name, **kwargs):
        """
        Groq modelinden gelen isteğe göre ilgili Python fonksiyonunu çalıştırır
        ve sonucunu string (metin) olarak geri döndürür.
        """
        if function_name in self.tools:
            try:
                result = self.tools[function_name](**kwargs)
                return str(result)
            except Exception as e:
                return f"HATA: '{function_name}' aracı çalıştırılırken bir sorun oluştu: {str(e)}"
        else:
            return f"HATA: '{function_name}' adında bir araç bulunamadı. Lütfen araç adını kontrol edin."
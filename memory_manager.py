import os
import json

class MemoryManager:
    def __init__(self, file_path="memory/long_term_data.json"):
        self.file_path = file_path
        self.memory_data = self._load_memory()

    def _load_memory(self):
        if not os.path.exists(self.file_path):
            if os.path.dirname(self.file_path):
                os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump({}, f, ensure_ascii=False, indent=4)
            return {}

        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {}

    def _save_memory(self):
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(self.memory_data, f, ensure_ascii=False, indent=4)

    def remember(self, key, value):
        self.memory_data[key] = value
        self._save_memory()
        return f"'{key}' bilgisi başarıyla hafızaya kaydedildi."

    def recall(self, key):
        return self.memory_data.get(key, f"'{key}' hakkında bir bilgi bulunamadı.")

    def get_all_memories(self):
        return self.memory_data

    def forget(self, key):
        if key in self.memory_data:
            del self.memory_data[key]
            self._save_memory()
            return f"'{key}' bilgisi hafızadan silindi."
        return f"'{key}' hafızada bulunamadığı için silinemedi."
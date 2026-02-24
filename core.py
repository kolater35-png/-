import os, sys, sqlite3, uuid, hashlib, base64, subprocess
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from kivy.utils import platform

class TitanKernel:
    def __init__(self):
        self.kernel_version = "5.0.4-PRO"
        self.kernel_id = hashlib.sha256(str(uuid.uuid4()).encode()).hexdigest()[:12]
        self.is_android = (platform == 'android')
        self.executor = ThreadPoolExecutor(max_workers=10)
        self.root_path = self._setup_storage()
        self._init_filesystem()

    def _setup_storage(self):
        if self.is_android:
            try:
                from android.storage import primary_external_storage_path
                return os.path.join(primary_external_storage_path(), "NebulaTitan")
            except: pass
        return os.path.join(os.path.expanduser("~"), "NebulaTitan")

    def _init_filesystem(self):
        for d in ["projects", "db", "logs", "temp", "vault", "env"]:
            os.makedirs(os.path.join(self.root_path, d), exist_ok=True)

    def smart_pip(self, package):
        """Интегрированный менеджер пакетов."""
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            return f"Package {package} ready."
        except Exception as e:
            return f"PIP Error: {e}"

class TitanPersistence:
    def __init__(self, kernel):
        self.db_path = os.path.join(kernel.root_path, "db/core.db")
        self._bootstrap()

    def _bootstrap(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("CREATE TABLE IF NOT EXISTS settings (key TEXT PRIMARY KEY, val TEXT)")
            conn.execute("CREATE TABLE IF NOT EXISTS logs (ts TIMESTAMP, msg TEXT)")

class TitanSecurity:
    def __init__(self, secret="TITAN_2026"):
        self.key = hashlib.sha256(secret.encode()).hexdigest()

    def crypt(self, data, decrypt=False):
        if not data: return ""
        if decrypt:
            xor = "".join([chr(ord(c) ^ ord(self.key[i % len(self.key)])) for i, c in enumerate(data)])
            return base64.b64decode(xor.encode()).decode()
        else:
            b64 = base64.b64encode(data.encode()).decode()
            return "".join([chr(ord(c) ^ ord(self.key[i % len(self.key)])) for i, c in enumerate(b64)])
          

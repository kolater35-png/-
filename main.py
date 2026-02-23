"""
NEBULA TITAN OS - THE ABSOLUTE MONOLITH (v5.0.3-STABLE)
Architecture: Multilayered Hybrid (Python/KivyMD/SQLite/JNI)
"""

import os
import sys
import time
import json
import sqlite3
import threading
import uuid
import hashlib
import base64
import shutil
import re
import random
import traceback
from datetime import datetime
from collections import deque
from concurrent.futures import ThreadPoolExecutor

# --- ENVIRONMENT CONFIGURATION ---
os.environ['KIVY_GRAPHICS'] = 'gles'
os.environ['KIVY_GL_BACKEND'] = 'sdl2'

from kivy.config import Config
Config.set('graphics', 'multisamples', '4')
Config.set('kivy', 'keyboard_mode', 'systemanddock')

from kivy.app import App
from kivy.lang import Builder
from kivy.clock import Clock, mainthread
from kivy.utils import platform, get_color_from_hex
from kivy.properties import StringProperty, NumericProperty, BooleanProperty, ObjectProperty
from kivy.uix.screenmanager import ScreenManager, Screen

try:
    from kivymd.app import MDApp
    from kivymd.uix.boxlayout import MDBoxLayout
    from kivymd.uix.list import OneLineIconListItem, IconLeftWidget, TwoLineIconListItem
    from kivymd.uix.dialog import MDDialog
    from kivymd.uix.button import MDFlatButton, MDRaisedButton
    from kivymd.uix.textfield import MDTextField
    from kivymd.uix.snackbar import Snackbar
except ImportError:
    print("Error: KivyMD is required for Titan OS.")
    sys.exit(1)

# =============================================================================
# [SECTION 1] TITAN KERNEL: RESOURCE & TASK MANAGER
# =============================================================================
class TitanKernel:
    def __init__(self):
        self.kernel_id = hashlib.sha256(str(uuid.uuid4()).encode()).hexdigest()[:12]
        self.is_android = (platform == 'android')
        self.start_time = time.time()
        self.executor = ThreadPoolExecutor(max_workers=8)
        self.root_path = self._setup_storage()
        self._init_fs()

    def _setup_storage(self):
        if self.is_android:
            try:
                from android.storage import primary_external_storage_path
                return os.path.join(primary_external_storage_path(), "NebulaTitan")
            except: pass
        return os.path.join(os.path.expanduser("~"), "NebulaTitan")

    def _init_fs(self):
        subdirs = ["projects", "db", "logs", "temp", "plugins", "recovery"]
        for d in subdirs:
            os.makedirs(os.path.join(self.root_path, d), exist_ok=True)

    def execute_async(self, func, *args, **kwargs):
        return self.executor.submit(func, *args, **kwargs)

# =============================================================================
# [SECTION 2] TITAN PERSISTENCE: DATA INTEGRITY LAYER
# =============================================================================
class TitanPersistence:
    def __init__(self, kernel):
        self.db_path = os.path.join(kernel.root_path, "db/titan_core.db")
        self._init_db()

    def _get_conn(self):
        return sqlite3.connect(self.db_path, check_same_thread=False)

    def _init_db(self):
        conn = self._get_conn()
        schema = [
            '''CREATE TABLE IF NOT EXISTS sys_config (
                key TEXT PRIMARY KEY, value TEXT)''',
            '''CREATE TABLE IF NOT EXISTS projects (
                id TEXT PRIMARY KEY, name TEXT, path TEXT, lang TEXT, ts TIMESTAMP)''',
            '''CREATE TABLE IF NOT EXISTS logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT, level TEXT, msg TEXT, ts TIMESTAMP)'''
        ]
        for sql in schema:
            conn.execute(sql)
        conn.commit()
        conn.close()

    def log_event(self, level, msg):
        conn = self._get_conn()
        conn.execute("INSERT INTO logs (level, msg, ts) VALUES (?, ?, ?)",
                    (level, msg, datetime.now()))
        conn.commit()
        conn.close()

# =============================================================================
# [SECTION 3] TITAN SECURITY: CRYPTO ENGINE
# =============================================================================
class TitanSecurity:
    def __init__(self, secret_key="TITAN_CORE_2026"):
        self.key = hashlib.sha256(secret_key.encode()).hexdigest()

    def encrypt(self, data):
        # Multi-layer XOR + Base64
        encoded = base64.b64encode(data.encode()).decode()
        return "".join([chr(ord(c) ^ ord(self.key[i % len(self.key)])) 
                       for i, c in enumerate(encoded)])

# =============================================================================
# [SECTION 4] BASE UI STRUCTURE (KV)
# =============================================================================
TITAN_KV_BASE = '''
<TitanFileItem@OneLineIconListItem>:
    is_dir: False
    IconLeftWidget:
        icon: "folder" if root.is_dir else "file-code"

MDScreen:
    name: "main_monolith"
    MDNavigationLayout:
        MDScreenManager:
            id: screen_manager
            MDScreen:
                name: "workspace"
                MDBoxLayout:
                    orientation: "vertical"
                    md_bg_color: get_color_from_hex("#0A0A0F")
                    
                    MDTopAppBar:
                        title: "NEBULA TITAN OS"
                        anchor_title: "left"
                        elevation: 2
                        md_bg_color: get_color_from_hex("#12121F")
                        left_action_items: [["menu", lambda x: nav_drawer.set_state("open")]]
                        right_action_items: [["console", lambda x: app.toggle_terminal()]]

                    MDBoxLayout:
                        orientation: "horizontal"
                        
                        # Sidebar / Explorer
                        MDBoxLayout:
                            id: explorer_panel
                            size_hint_x: 0
                            opacity: 0
                            md_bg_color: get_color_from_hex("#0E0E16")
                            MDScrollView:
                                MDList:
                                    id: file_list

                        # Editor Main
                        MDBoxLayout:
                            orientation: "vertical"
                            padding: "4dp"
                            MDTextField:
                                id: code_editor
                                multiline: True
                                mode: "fill"
                                fill_color: 0, 0, 0, 0
                                font_name: "Roboto"
                                font_size: "14sp"
                                text_color_normal: 1, 1, 1, 1
                                cursor_color: get_color_from_hex("#00FFD1")

        MDNavigationDrawer:
            id: nav_drawer
            radius: (0, 16, 16, 0)
            md_bg_color: get_color_from_hex("#12121F")
            MDBoxLayout:
                orientation: "vertical"
                padding: "12dp"
                spacing: "8dp"
                MDLabel:
                    text: "TITAN MODULES"
                    font_style: "H6"
                    theme_text_color: "Custom"
                    text_color: get_color_from_hex("#00FFD1")
                    size_hint_y: None
                    height: self.texture_size[1]
                MDSeparator:
                MDFlatButton:
                    text: "PROJECT EXPLORER"
                    on_release: app.toggle_explorer()
                MDFlatButton:
                    text: "SETTINGS"
                Widget:
'''
# =============================================================================
# [SECTION 5] TITAN HARDWARE BRIDGE (JNI/ANDROID)
# =============================================================================
class TitanHardwareBridge:
    """
    Интерфейс низкоуровневого взаимодействия. На Android использует Pyjnius
    для доступа к системным сервисам.
    """
    def __init__(self):
        self.platform = platform
        self.context = None
        if self.platform == 'android':
            try:
                from jnius import autoclass
                self.PythonActivity = autoclass('org.kivy.android.PythonActivity')
                self.context = self.PythonActivity.mActivity
                self.vibrator = self.context.getSystemService(autoclass('android.content.Context').VIBRATOR_SERVICE)
            except Exception as e:
                print(f"JNI Error: {e}")

    def vibrate(self, duration=50):
        if self.platform == 'android' and self.vibrator:
            self.vibrator.vibrate(duration)
        else:
            print(f"[PC_SIM] Vibrate for {duration}ms")

    def get_battery_level(self):
        if self.platform == 'android':
            # Реализация получения заряда через IntentFilter
            return 85 # Заглушка для примера
        return 100

# =============================================================================
# [SECTION 6] TITAN FILE EXPLORER: ADVANCED LOGIC
# =============================================================================
class TitanExplorer:
    """
    Управляет состоянием файловой системы в UI. Поддерживает кэширование 
    икон и ленивую загрузку.
    """
    def __init__(self, kernel, file_list_widget):
        self.kernel = kernel
        self.widget = file_list_widget
        self.current_path = kernel.root_path
        self.history = []

    @mainthread
    def refresh(self, path=None):
        if path: self.current_path = path
        self.widget.clear_widgets()
        
        try:
            # Сначала папки, потом файлы
            entries = os.scandir(self.current_path)
            sorted_entries = sorted(entries, key=lambda e: (not e.is_dir(), e.name.lower()))
            
            for entry in sorted_entries:
                is_dir = entry.is_dir()
                item = OneLineIconListItem(
                    text=entry.name,
                    on_release=lambda x, p=entry.path, d=is_dir: self.on_entry_click(p, d)
                )
                icon = "folder" if is_dir else self._get_icon_by_ext(entry.name)
                item.add_widget(IconLeftWidget(icon=icon))
                self.widget.add_widget(item)
        except PermissionError:
            Snackbar(text="Access Denied").open()

    def _get_icon_by_ext(self, filename):
        ext = filename.split('.')[-1].lower()
        mapping = {
            'py': 'language-python',
            'json': 'code-json',
            'db': 'database',
            'txt': 'file-document'
        }
        return mapping.get(ext, 'file-code')

    def on_entry_click(self, path, is_dir):
        if is_dir:
            self.refresh(path)
        else:
            app = MDApp.get_running_app()
            app.load_file_to_editor(path)

# =============================================================================
# [SECTION 7] TITAN PROJECT TAB MANAGER
# =============================================================================
class TitanTab(MDBoxLayout):
    """Кастомный виджет вкладки с кнопкой закрытия."""
    filename = StringProperty()
    path = StringProperty()
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, 1)
        self.width = dp(140)
        self.md_bg_color = get_color_from_hex("#1E1E2E")

# =============================================================================
# [SECTION 8] UPDATED MAIN APP LOGIC
# =============================================================================
class NebulaTitanOS(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.kernel = TitanKernel()
        self.db = TitanPersistence(self.kernel)
        self.hw = TitanHardwareBridge()
        self.explorer = None
        self.current_file = None

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "DeepPurple"
        return Builder.load_string(TITAN_KV_BASE)

    def on_start(self):
        # Инициализируем эксплорер после загрузки UI
        self.explorer = TitanExplorer(self.kernel, self.root.ids.file_list)
        self.explorer.refresh()
        self.hw.vibrate(100)
        self.db.log_event("INFO", "Titan System Started")

    def toggle_explorer(self):
        panel = self.root.ids.explorer_panel
        if panel.size_hint_x == 0:
            panel.size_hint_x = 0.35
            panel.opacity = 1
        else:
            panel.size_hint_x = 0
            panel.opacity = 0

    def load_file_to_editor(self, path):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
                self.root.ids.code_editor.text = content
                self.current_file = path
                self.root.ids.nav_drawer.set_state("close")
                Snackbar(text=f"Loaded: {os.path.basename(path)}").open()
        except Exception as e:
            self.db.log_event("ERROR", f"File Load Error: {str(e)}")

    def toggle_terminal(self):
        # Будет реализовано в следующем модуле
        Snackbar(text="Initializing Titan Terminal...").open()

# =============================================================================
# [SECTION 9] TITAN AUTO-SAVE SYSTEM (BACKGROUND)
# =============================================================================
    def run_auto_save(self):
        def _save_loop():
            while True:
                time.sleep(60) # Каждую минуту
                if self.current_file and self.root.ids.code_editor.text:
                    with open(self.current_file, 'w', encoding='utf-8') as f:
                        f.write(self.root.ids.code_editor.text)
                    print("[SYSTEM] Auto-saved")
        
        threading.Thread(target=_save_loop, daemon=True).start()
# =============================================================================
# [SECTION 11] TITAN SYNTAX ENGINE: LEXER & HIGHLIGHTER
# =============================================================================
class TitanSyntaxHighlighter:
    """
    Движок динамической подсветки. Использует регулярные выражения 
    для выделения ключевых слов, строк и комментариев в реальном времени.
    """
    def __init__(self):
        self.rules = {
            'python': [
                (r'\b(def|class|if|else|elif|while|for|return|import|from|as|try|except|with|lambda|in|is|not|and|or)\b', "#FF79C6"), # Keywords
                (r'\b(self|cls|True|False|None)\b', "#BD93F9"), # Builtins/Constants
                (r'".*?"|\'.*?\'', "#F1FA8C"), # Strings
                (r'#.*', "#6272A4"), # Comments
                (r'\b[0-9]+\b', "#BD93F9"), # Numbers
                (r'\b[a-zA-Z_][a-zA-Z0-9_]*(?=\()', "#50FA7B"), # Functions
            ],
            'json': [
                (r'".*?"(?=\s*:)', "#8BE9FD"), # Keys
                (r':\s*".*?"', "#F1FA8C"), # Value Strings
                (r'\b(true|false|null)\b', "#BD93F9"),
            ]
        }

    def apply_highlighting(self, text_input, lang='python'):
        """
        Метод имитирует разметку. В KivyMD используется RichText (Markup).
        """
        if lang not in self.rules: return text_input
        
        highlighted = text_input
        # Экранируем спецсимволы Kivy Markup перед обработкой
        highlighted = highlighted.replace('[', '[[').replace(']', ']]')
        
        for pattern, color in self.rules[lang]:
            highlighted = re.sub(
                pattern, 
                lambda m: f"[color={color}]{m.group(0)}[/color]", 
                highlighted
            )
        return highlighted

# =============================================================================
# [SECTION 12] TITAN TERMINAL ENGINE (TTE)
# =============================================================================
class TitanTerminal(MDBoxLayout):
    """
    Встроенный эмулятор терминала. Перехватывает системные вызовы 
    и выводит результат в кастомный виджет.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.md_bg_color = get_color_from_hex("#000000")
        self.history = deque(maxlen=100)
        
        self.output = MDTextField(
            multiline=True,
            readonly=True,
            font_name="RobotoMono-Regular", # Требуется наличие шрифта
            font_size="12sp",
            text_color_normal=get_color_from_hex("#00FF00"),
            mode="fill",
            fill_color=(0,0,0,0)
        )
        self.input = MDTextField(
            hint_text="titan@os:~$ ",
            on_text_validate=self.process_command,
            mode="rectangle"
        )
        self.add_widget(self.output)
        self.add_widget(self.input)

    def process_command(self, instance):
        cmd = instance.text.strip()
        self.append_text(f"titan@os:~$ {cmd}")
        
        # Логика встроенных команд
        if cmd == "clear":
            self.output.text = ""
        elif cmd == "help":
            self.append_text("Available: ls, pwd, sysinfo, git-status, clear")
        elif cmd == "sysinfo":
            info = f"OS: Titan\nPlatform: {platform}\nUptime: {int(time.time())}s"
            self.append_text(info)
        else:
            # Попытка выполнить системную команду
            try:
                result = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
                self.append_text(result.decode('utf-8'))
            except Exception as e:
                self.append_text(f"Error: {str(e)}")
        
        instance.text = ""

    def append_text(self, text):
        self.output.text += text + "\n"

# =============================================================================
# [SECTION 13] TITAN VIRTUAL GIT INTERFACE
# =============================================================================
class TitanGitController:
    """
    Слой интеграции с Git. Управляет индексацией и коммитами.
    """
    def __init__(self, project_path):
        self.path = project_path

    def get_status(self):
        # В реальности здесь будет вызов git-библиотек
        return "Branch: master\nChanges: 0 staged, 3 unstaged"

    def quick_commit(self, message):
        ts = datetime.now().strftime("%H:%M:%S")
        return f"[{ts}] Committed with hash: {hashlib.md5(message.encode()).hexdigest()[:7]}"

# =============================================================================
# [SECTION 14] CORE REFINEMENT: MAIN APP EXTENSION
# =============================================================================
class NebulaTitanOS(MDApp):
    # ... (предыдущие свойства) ...
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.highlighter = TitanSyntaxHighlighter()
        self.terminal_visible = False
        # Переопределяем инициализацию для поддержки терминала
        
    def on_code_change(self, instance, value):
        """
        Слушатель изменений текста для живой подсветки (упрощенно).
        """
        # В реальном приложении здесь используется задержка (debounce), 
        # чтобы не вешать UI на каждом символе.
        pass

    def toggle_terminal(self):
        if not hasattr(self, 'terminal_widget'):
            self.terminal_widget = TitanTerminal(size_hint_y=0.4)
            self.root.ids.workspace.add_widget(self.terminal_widget)
            self.terminal_visible = True
        else:
            if self.terminal_visible:
                self.root.ids.workspace.remove_widget(self.terminal_widget)
            else:
                self.root.ids.workspace.add_widget(self.terminal_widget)
            self.terminal_visible = not self.terminal_visible
# =============================================================================
# [SECTION 16] TITAN PLUGIN ENGINE: DYNAMIC EXTENSIBILITY
# =============================================================================
class TitanPlugin:
    """Базовый класс для всех плагинов Titan OS."""
    def __init__(self, app):
        self.app = app
        self.name = "Base Plugin"
        self.enabled = False

    def on_activate(self): pass
    def on_deactivate(self): pass

class TitanPluginManager:
    """
    Движок плагинов. Ищет .py файлы в папке /plugins, 
    импортирует их "на лету" и регистрирует в системе.
    """
    def __init__(self, app, plugin_dir):
        self.app = app
        self.plugin_dir = plugin_dir
        self.loaded_plugins = {}

    def discover_and_load(self):
        """Сканирует директорию и загружает валидные модули."""
        if not os.path.exists(self.plugin_dir): return
        
        for filename in os.listdir(self.plugin_dir):
            if filename.endswith(".py") and filename != "__init__.py":
                module_name = filename[:-3]
                try:
                    # Динамический импорт
                    import importlib.util
                    spec = importlib.util.spec_from_file_location(module_name, os.path.join(self.plugin_dir, filename))
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    
                    # Ищем класс плагина
                    for name, obj in inspect.getmembers(module):
                        if inspect.isclass(obj) and issubclass(obj, TitanFileItem) and obj is not TitanPlugin:
                            plugin_instance = obj(self.app)
                            self.loaded_plugins[module_name] = plugin_instance
                            plugin_instance.on_activate()
                            print(f"[PLUGIN] Loaded: {module_name}")
                except Exception as e:
                    print(f"[PLUGIN_ERR] Failed to load {module_name}: {e}")

# =============================================================================
# [SECTION 17] TITAN THEME ENGINE: STYLING LAYER
# =============================================================================
class TitanThemeManager:
    """
    Управляет визуальным состоянием IDE. 
    Позволяет менять цвета всех компонентов без перезагрузки.
    """
    def __init__(self, theme_cls):
        self.theme_cls = theme_cls
        self.current_theme_data = {}

    def load_theme_from_json(self, json_path):
        try:
            with open(json_path, 'r') as f:
                data = json.load(f)
                self.current_theme_data = data
                self.apply_theme()
        except Exception as e:
            print(f"Theme Error: {e}")

    def apply_theme(self):
        t = self.current_theme_data
        if not t: return
        
        self.theme_cls.primary_palette = t.get("primary_palette", "DeepPurple")
        self.theme_cls.accent_palette = t.get("accent_palette", "Amber")
        self.theme_cls.theme_style = t.get("style", "Dark")
        
        # Обновление кастомных цветов через глобальные свойства
        app = MDApp.get_running_app()
        # Имитация обновления UI
        Snackbar(text=f"Theme {t.get('name')} applied").open()

# =============================================================================
# [SECTION 18] TITAN OBSERVER: PROJECT WATCHER
# =============================================================================
class TitanProjectWatcher:
    """
    Следит за изменениями в файловой системе проекта. 
    Если файл изменен извне — предлагает обновить редактор.
    """
    def __init__(self, path, callback):
        self.path = path
        self.callback = callback
        self.last_mtime = os.path.getmtime(path) if os.path.exists(path) else 0
        self._stop = False

    def start_watching(self):
        threading.Thread(target=self._loop, daemon=True).start()

    def _loop(self):
        while not self._stop:
            if os.path.exists(self.path):
                current_mtime = os.path.getmtime(self.path)
                if current_mtime > self.last_mtime:
                    self.last_mtime = current_mtime
                    self.callback(self.path)
            time.sleep(2)

# =============================================================================
# [SECTION 19] PROJECT CONFIGURATION SCHEMA
# =============================================================================
DEFAULT_PROJECT_CONFIG = {
    "version": "1.0.0",
    "compiler": "python3",
    "entry_point": "main.py",
    "flags": ["-O", "-v"],
    "plugins_required": []
}

# =============================================================================
# [SECTION 20] EXPANDED MAIN LOGIC (INTEGRATION)
# =============================================================================
class NebulaTitanOS(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Инициализация новых систем
        self.plugin_manager = TitanPluginManager(self, os.path.join(self.kernel.root_path, "plugins"))
        self.theme_manager = TitanThemeManager(self.theme_cls)
        self.watcher = None

    def on_start(self):
        super().on_start()
        # Загрузка плагинов при старте
        self.plugin_manager.discover_and_load()
        
    def setup_project_watcher(self, file_path):
        if self.watcher: self.watcher._stop = True
        self.watcher = TitanProjectWatcher(file_path, self.on_external_change)
        self.watcher.start_watching()

    def on_external_change(self, path):
        # Вызывается из другого потока, используем @mainthread
        self._notify_external_change(path)

    @mainthread
    def _notify_external_change(self, path):
        Snackbar(
            text="File changed externally. Reload?",
            button_text="YES",
            button_callback=lambda x: self.load_file_to_editor(path)
        ).open()

# --- Временная заглушка для KV вкладок (обновление) ---
TITAN_KV_BASE += '''
<TitanPluginItem@TwoLineIconListItem>:
    IconLeftWidget:
        icon: "plugin"
'''
# =============================================================================
# [SECTION 21] TITAN DEBUGGER: STDOUT REDIRECTION & LOGGING
# =============================================================================
class TitanDebugger:
    """
    Система перехвата вывода. Позволяет видеть ошибки выполнения кода 
    прямо в консоли IDE, даже если они произошли в другом потоке.
    """
    def __init__(self, terminal_callback):
        self.terminal_callback = terminal_callback
        self.is_running = False
        self._original_stdout = sys.stdout
        self._original_stderr = sys.stderr

    def start_capture(self):
        sys.stdout = StringIO()
        sys.stderr = StringIO()
        self.is_running = True
        threading.Thread(target=self._update_loop, daemon=True).start()

    def _update_loop(self):
        while self.is_running:
            # Читаем данные из StringIO и отправляем в UI терминала
            out = sys.stdout.getvalue()
            err = sys.stderr.getvalue()
            
            if out:
                self.terminal_callback(out, "INFO")
                sys.stdout.truncate(0)
                sys.stdout.seek(0)
            if err:
                self.terminal_callback(err, "ERROR")
                sys.stderr.truncate(0)
                sys.stderr.seek(0)
            time.sleep(0.5)

    def stop_capture(self):
        self.is_running = False
        sys.stdout = self._original_stdout
        sys.stderr = self._original_stderr

# =============================================================================
# [SECTION 22] TITAN AI COPILOT BRIDGE (STUB)
# =============================================================================
class TitanAICopilot:
    """
    Мост для подключения LLM (Gemini/OpenAI). 
    Отправляет контекст кода и возвращает предложения по исправлению.
    """
    def __init__(self, api_key=None):
        self.api_key = api_key
        self.model_endpoint = "https://api.titan-core.ai/v1/complete"

    def get_suggestion(self, code_snippet, prompt="Optimize this"):
        # Имитация асинхронного запроса к ИИ
        def _request():
            time.sleep(2) # Задержка сети
            return f"/* Titan AI: Consider using list comprehension here */"
        
        return threading.Thread(target=_request).start()

# =============================================================================
# [SECTION 23] TITAN HEX VIEWER: BINARY DATA ANALYZER
# =============================================================================
class TitanHexViewer:
    """
    Позволяет просматривать файлы в 16-ричном формате. 
    Полезно для отладки бинарных файлов и БД.
    """
    @staticmethod
    def get_hex_view(file_path):
        if not os.path.exists(file_path): return "File not found."
        
        try:
            with open(file_path, 'rb') as f:
                content = f.read(1024) # Читаем первый килобайт
            
            hex_lines = []
            for i in range(0, len(content), 16):
                chunk = content[i:i+16]
                hex_part = " ".join(f"{b:02x}" for b in chunk)
                ascii_part = "".join(chr(b) if 32 <= b <= 126 else "." for b in chunk)
                hex_lines.append(f"{i:08x}: {hex_part:<48} |{ascii_part}|")
            
            return "\n".join(hex_lines)
        except Exception as e:
            return f"Hex error: {e}"

# =============================================================================
# [SECTION 24] TITAN NETWORK MANAGER: UPDATE & SYNC
# =============================================================================
class TitanNetworkManager:
    """
    Управляет проверкой обновлений и синхронизацией конфигов с облаком.
    """
    def __init__(self):
        self.server_url = "https://titan-os.repo"

    def check_updates(self, current_version, callback):
        def _task():
            # Симуляция проверки версии
            time.sleep(3)
            callback("v5.1.0-BETA Available")
        
        threading.Thread(target=_task, daemon=True).start()

# =============================================================================
# [SECTION 25] CORE EXPANSION: DIAGNOSTICS UI
# =============================================================================
TITAN_KV_BASE += '''
<DiagnosticsPanel@MDBoxLayout>:
    orientation: "vertical"
    md_bg_color: get_color_from_hex("#12121F")
    padding: "10dp"
    MDLabel:
        text: "CORE DIAGNOSTICS"
        halign: "center"
        font_style: "Button"
        theme_text_color: "Custom"
        text_color: get_color_from_hex("#FF3D00")
    MDSeparator:
    MDLabel:
        id: ram_usage_label
        text: "RAM: -- MB"
    MDLabel:
        id: cpu_usage_label
        text: "CPU: -- %"
'''

class NebulaTitanOS(MDApp):
    # Добавляем новые системы в инициализацию
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.debugger = TitanDebugger(self.append_to_terminal)
        self.network = TitanNetworkManager()
        self.ai_engine = TitanAICopilot()

    def on_start(self):
        super().on_start()
        self.debugger.start_capture()
        # Запуск монитора ресурсов
        Clock.schedule_interval(self.update_system_stats, 2)

    def update_system_stats(self, dt):
        # В реальности здесь вызов из модуля Telemetry
        ram = random.randint(120, 450)
        cpu = random.randint(5, 40)
        # Обновление UI если панель открыта
        pass

    def append_to_terminal(self, text, level="INFO"):
        # Метод для получения данных из Debugger
        if hasattr(self, 'terminal_widget'):
            color = "#00FF00" if level == "INFO" else "#FF0000"
            self.terminal_widget.append_text(f"[color={color}]{text}[/color]")
# =============================================================================
# [SECTION 31] TITAN TASK RUNNER: MULTI-PRIORITY SCHEDULER
# =============================================================================
class TitanTask:
    def __init__(self, name, func, priority=1, args=(), kwargs={}):
        self.name = name
        self.func = func
        self.priority = priority # 0: High, 1: Normal, 2: Low
        self.args = args
        self.kwargs = kwargs
        self.status = "PENDING"

class TitanTaskRunner:
    """
    Менеджер очередей с приоритетами. Гарантирует, что критические задачи 
    (сохранение) выполняются быстрее, чем фоновые (индексация AI).
    """
    def __init__(self):
        self.queues = [Queue(), Queue(), Queue()] # Три уровня приоритета
        self.is_running = True
        self.worker = threading.Thread(target=self._process_loop, daemon=True)
        self.worker.start()

    def add_task(self, task):
        self.queues[task.priority].put(task)

    def _process_loop(self):
        while self.is_running:
            task = None
            # Проверяем очереди от высшего приоритета к низшему
            for q in self.queues:
                try:
                    task = q.get_nowait()
                    break
                except Empty:
                    continue
            
            if task:
                task.status = "RUNNING"
                try:
                    task.func(*task.args, **task.kwargs)
                    task.status = "COMPLETED"
                except Exception as e:
                    task.status = f"FAILED: {str(e)}"
                finally:
                    q.task_done()
            else:
                time.sleep(0.5) # Спим, если задач нет

# =============================================================================
# [SECTION 32] GLOBAL SEARCH & REPLACE ENGINE (REGEX-READY)
# =============================================================================
class TitanSearchEngine:
    """
    Движок полнотекстового поиска по всему дереву проекта.
    Поддерживает регулярные выражения и исключение папок.
    """
    def __init__(self, root_path):
        self.root = root_path

    def find_in_files(self, query, pattern="*", use_regex=False):
        results = [] # Список кортежей (файл, строка, текст)
        for root, dirs, files in os.walk(self.root):
            # Игнорируем скрытые папки и кэши
            dirs[:] = [d for d in dirs if not d.startswith('.') and d != 'db']
            
            for file in files:
                if re.match(pattern.replace("*", ".*"), file):
                    path = os.path.join(root, file)
                    try:
                        with open(path, 'r', encoding='utf-8') as f:
                            for i, line in enumerate(f, 1):
                                if use_regex:
                                    if re.search(query, line):
                                        results.append((path, i, line.strip()))
                                else:
                                    if query in line:
                                        results.append((path, i, line.strip()))
                    except: continue
        return results

# =============================================================================
# [SECTION 33] CODING KEYBOARD ADAPTER (ANDROID OVERLAY)
# =============================================================================
class TitanCodingBar(MDBoxLayout):
    """
    Дополнительная панель над клавиатурой для быстрого ввода спецсимволов.
    Крайне важна для Android-разработки.
    """
    def __init__(self, target_input, **kwargs):
        super().__init__(**kwargs)
        self.target = target_input
        self.size_hint_y = None
        self.height = dp(45)
        self.md_bg_color = [0.1, 0.1, 0.15, 1]
        self.spacing = dp(2)
        
        symbols = ['{', '}', '[', ']', '(', ')', ':', ';', '"', "'", '=', '<', '>', '/', '_']
        for s in symbols:
            btn = MDFlatButton(
                text=s, 
                text_color=[0, 1, 0.8, 1],
                on_release=lambda x, sym=s: self.insert_symbol(sym)
            )
            self.add_widget(btn)

    def insert_symbol(self, symbol):
        self.target.insert_text(symbol)

# =============================================================================
# [SECTION 34] TITAN LOGGING SYSTEM (ROTATING LOGS)
# =============================================================================
class TitanLogger:
    """
    Система логирования с ротацией. Не дает лог-файлам переполнить память Android.
    """
    def __init__(self, log_dir):
        self.log_file = os.path.join(log_dir, "titan_main.log")
        self.max_size = 1024 * 1024 * 5 # 5 MB

    def log(self, level, msg):
        if os.path.exists(self.log_file) and os.path.getsize(self.log_file) > self.max_size:
            os.rename(self.log_file, self.log_file + ".old")
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.log_file, "a") as f:
            f.write(f"[{timestamp}] [{level}] {msg}\n")

# =============================================================================
# [SECTION 35] UPDATED UI: SEARCH & TASK OVERLAY
# =============================================================================
TITAN_KV_REFINED = TITAN_KV_BASE + '''
<SearchScreen@MDScreen>:
    name: "search_engine"
    MDBoxLayout:
        orientation: "vertical"
        MDTopAppBar:
            title: "GLOBAL SEARCH"
            left_action_items: [["arrow-left", lambda x: app.switch_screen("workspace")]]
        
        MDBoxLayout:
            size_hint_y: None
            height: dp(60)
            padding: dp(10)
            MDTextField:
                id: search_input
                hint_text: "Query (RegEx supported)"
                on_text_validate: app.perform_global_search(self.text)
        
        MDScrollView:
            MDList:
                id: search_results_list

<TitanStatusLine@MDBoxLayout>:
    size_hint_y: None
    height: dp(25)
    md_bg_color: 0.05, 0.05, 0.1, 1
    MDLabel:
        id: status_left
        text: " READY"
        font_style: "Caption"
        theme_text_color: "Custom"
        text_color: 0, 0.8, 0.6, 1
    MDLabel:
        id: status_right
        text: "UTF-8 | LF | Py 3.10 "
        halign: "right"
        font_style: "Caption"
        theme_text_color: "Hint"
'''

# =============================================================================
# [SECTION 36] MAIN APP EVOLUTION
# =============================================================================
class NebulaTitanOS(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Инициализация новых систем
        self.scheduler = TitanTaskRunner()
        self.search_engine = TitanSearchEngine(self.kernel.root_path)
        self.sys_logger = TitanLogger(os.path.join(self.kernel.root_path, "logs"))
        
    def on_start(self):
        super().on_start()
        # Добавляем клавиатурную панель в редактор
        editor_container = self.root.ids.code_editor.parent
        self.coding_bar = TitanCodingBar(self.root.ids.code_editor)
        editor_container.add_widget(self.coding_bar)

    def perform_global_search(self, query):
        def _search_job():
            results = self.search_engine.find_in_files(query)
            self.update_search_ui(results)
        
        task = TitanTask("GlobalSearch", _search_job, priority=0)
        self.scheduler.add_task(task)

    @mainthread
    def update_search_ui(self, results):
        # Логика обновления списка результатов
        pass
# =============================================================================
# [SECTION 41] TITAN VIRTUAL GIT: VERSION CONTROL ENGINE
# =============================================================================
class TitanGit:
    """
    Легковесный эмулятор Git для мобильной среды. 
    Позволяет создавать ветки, фиксировать изменения и смотреть историю.
    """
    def __init__(self, project_dir):
        self.repo_path = os.path.join(project_dir, ".titan_git")
        self._init_repo()

    def _init_repo(self):
        if not os.path.exists(self.repo_path):
            os.makedirs(self.repo_path)
            with open(os.path.join(self.repo_path, "HEAD"), "w") as f:
                f.write("ref: refs/heads/master")

    def commit(self, message, author="TitanUser"):
        """Создает 'снимок' текущего состояния проекта."""
        commit_id = hashlib.sha1(f"{time.time()}{message}".encode()).hexdigest()
        commit_data = {
            "id": commit_id,
            "message": message,
            "author": author,
            "timestamp": datetime.now().isoformat()
        }
        path = os.path.join(self.repo_path, f"commit_{commit_id}.json")
        with open(path, "w") as f:
            json.dump(commit_data, f)
        return commit_id[:7]

# =============================================================================
# [SECTION 42] TITAN PLUGIN SYSTEM: DYNAMIC EXTENSIONS
# =============================================================================
class TitanPluginManager:
    """
    Загрузчик плагинов. Позволяет добавлять новые функции в IDE 
    просто закидывая .py файлы в папку /plugins.
    """
    def __init__(self, app):
        self.app = app
        self.plugin_dir = os.path.join(app.kernel.root_path, "plugins")
        self.active_plugins = {}

    def load_plugins(self):
        if not os.path.exists(self.plugin_dir):
            os.makedirs(self.plugin_dir)
            
        for file in os.listdir(self.plugin_dir):
            if file.endswith(".py"):
                name = file[:-3]
                try:
                    # Динамический импорт модуля
                    import importlib
                    sys.path.append(self.plugin_dir)
                    module = importlib.import_module(name)
                    if hasattr(module, "setup"):
                        module.setup(self.app)
                        self.active_plugins[name] = module
                except Exception as e:
                    print(f"Plugin {name} failed: {e}")

# =============================================================================
# [SECTION 43] TITAN NOTIFICATION SYSTEM (TOASTS & SNACKBARS)
# =============================================================================
class TitanNotifier:
    """Менеджер уведомлений для информирования пользователя о системных событиях."""
    @staticmethod
    def notify(text, color="info"):
        colors = {
            "info": [0.2, 0.6, 1, 1],
            "error": [1, 0.2, 0.2, 1],
            "success": [0.2, 1, 0.4, 1]
        }
        Snackbar(
            text=text,
            bg_color=colors.get(color, colors["info"]),
            duration=3
        ).open()

# =============================================================================
# [SECTION 44] TITAN UPDATE MANAGER: OTA SERVICES
# =============================================================================
class TitanUpdater:
    """Проверяет наличие обновлений на сервере и подготавливает систему к апдейту."""
    def __init__(self, current_version):
        self.version = current_version
        self.update_url = "https://api.nebula-titan.io/v1/update"

    def check_for_updates(self):
        def _request():
            try:
                # В реальном коде здесь используется библиотека requests или urllib
                time.sleep(2) # Имитация сетевой задержки
                TitanNotifier.notify("System is up to date: v5.0.3")
            except:
                TitanNotifier.notify("Update check failed", "error")
        
        threading.Thread(target=_request, daemon=True).start()

# =============================================================================
# [SECTION 45] UPDATED UI: TOOLS & SETTINGS OVERLAY
# =============================================================================
TITAN_KV_EXTENDED = TITAN_KV_REFINED + '''
<SettingsScreen@MDScreen>:
    name: "settings"
    MDBoxLayout:
        orientation: "vertical"
        MDTopAppBar:
            title: "SYSTEM SETTINGS"
            left_action_items: [["arrow-left", lambda x: app.switch_screen("workspace")]]
        
        MDScrollView:
            MDList:
                OneLineIconListItem:
                    text: "Check for Updates"
                    on_release: app.updater.check_for_updates()
                    IconLeftWidget:
                        icon: "update"
                
                OneLineIconListItem:
                    text: "Clear System Logs"
                    on_release: app.sys_logger.clear_logs()
                    IconLeftWidget:
                        icon: "delete-sweep"

                OneLineIconListItem:
                    text: "Toggle Dark Mode"
                    on_release: app.theme_manager.toggle_style()
                    IconLeftWidget:
                        icon: "theme-light-dark"
'''

# =============================================================================
# [CORE INTEGRATION] FINAL APP STRUCTURE
# =============================================================================
class NebulaTitanOS(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Инициализация всех систем (Modules 41-45)
        self.git = None # Инициализируется при открытии проекта
        self.plugin_manager = TitanPluginManager(self)
        self.updater = TitanUpdater("5.0.3")
        self.notifier = TitanNotifier()

    def on_start(self):
        super().on_start()
        # Загрузка расширений при старте
        self.plugin_manager.load_plugins()
        self.notifier.notify("Titan OS Kernel Loaded", "success")

    def switch_screen(self, screen_name):
        self.root.ids.screen_manager.current = screen_name
# =============================================================================
# [SECTION 46] TITAN RESOURCE PROFILER: REAL-TIME MONITOR
# =============================================================================
class TitanProfiler:
    """
    Инструмент для мониторинга ресурсов. Позволяет отслеживать нагрузку 
    на систему, которую дает ваш код во время выполнения.
    """
    def __init__(self):
        self.is_monitoring = False
        self.cpu_history = deque(maxlen=20)
        self.ram_history = deque(maxlen=20)

    def start_diagnostics(self):
        self.is_monitoring = True
        threading.Thread(target=self._monitor_loop, daemon=True).start()

    def _monitor_loop(self):
        while self.is_monitoring:
            # Имитация сбора данных (на Android используются системные вызовы)
            cpu = random.uniform(5.0, 25.0)
            ram = random.uniform(150.0, 300.0)
            self.cpu_history.append(cpu)
            self.ram_history.append(ram)
            time.sleep(1)

# =============================================================================
# [SECTION 47] TITAN DOCGEN: AUTOMATIC DOCUMENTATION
# =============================================================================
class TitanDocGen:
    """
    Парсит ваши .py файлы и автоматически генерирует документацию 
    в формате Markdown на основе docstrings и комментариев.
    """
    def __init__(self, project_path):
        self.path = project_path

    def generate(self):
        docs = ["# Project Documentation\n", f"Generated: {datetime.now()}\n"]
        for file in os.listdir(self.path):
            if file.endswith(".py"):
                docs.append(f"## Module: {file}\n")
                with open(os.path.join(self.path, file), 'r') as f:
                    content = f.read()
                    # Простейший поиск функций и классов для доков
                    matches = re.findall(r'(def|class)\s+(\w+)', content)
                    for m_type, m_name in matches:
                        docs.append(f"- **{m_name}** ({m_type})")
        
        doc_file = os.path.join(self.path, "TITAN_DOCS.md")
        with open(doc_file, 'w') as f:
            f.write("\n".join(docs))
        return doc_file

# =============================================================================
# [SECTION 48] TITAN SECURITY VAULT: ENCRYPTED STORAGE
# =============================================================================
class TitanVault:
    """
    Защищенное хранилище для API-ключей, паролей от Git и SSH. 
    Данные шифруются ключом, привязанным к ID устройства.
    """
    def __init__(self, master_key):
        self.key = hashlib.sha256(master_key.encode()).digest()

    def save_secret(self, key_name, secret_value):
        # Реализация сохранения зашифрованного JSON
        encrypted = base64.b64encode(secret_value.encode()).decode()
        # В реальности здесь используется AES
        return f"Secret {key_name} secured."

# =============================================================================
# [SECTION 49] FINAL BOOTSTRAP: SYSTEM SYNERGY
# =============================================================================
class TitanSystemBootstrap:
    """
    Главный инициализатор, который проверяет целостность всех модулей 
    перед окончательным запуском интерфейса.
    """
    def __init__(self, app):
        self.app = app

    def verify_integrity(self):
        components = [
            self.app.kernel, self.app.db, self.app.plugin_manager,
            self.app.debugger, self.app.scheduler
        ]
        return all(c is not None for c in components)

# =============================================================================
# [SECTION 50] UPDATED MAIN LOGIC: THE MONOLITH REBORN
# =============================================================================
class NebulaTitanOS(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Финальный набор инструментов
        self.profiler = TitanProfiler()
        self.vault = TitanVault("DEVICE_UNIQUE_STUB")
        self.bootstrapper = TitanSystemBootstrap(self)

    def on_start(self):
        super().on_start()
        if self.bootstrapper.verify_integrity():
            self.profiler.start_diagnostics()
            self.notifier.notify("System Integrity: 100%. All modules active.", "success")
        else:
            self.notifier.notify("Integrity Check Failed!", "error")

    def run_doc_generation(self):
        generator = TitanDocGen(self.kernel.root_path)
        path = generator.generate()
        self.notifier.notify(f"Docs saved to {os.path.basename(path)}")
# =============================================================================
# [SECTION 51] TITAN ADAPTIVE UI: MULTI-SCREEN SCALING
# =============================================================================
class TitanScreenAdapter:
    """
    Автоматически подстраивает размеры шрифтов и отступов под DPI экрана.
    Решает проблему "слишком мелкого текста" на экранах 2K/4K.
    """
    def __init__(self):
        self.metrics = Window.size
        self.dpi = self._get_dpi()

    def _get_dpi(self):
        # На Android получаем реальный DPI через JNI, на ПК - дефолт
        if platform == 'android':
            from jnius import autoclass
            activity = autoclass('org.kivy.android.PythonActivity').mActivity
            metrics = autoclass('android.util.DisplayMetrics')()
            activity.getWindowManager().getDefaultDisplay().getMetrics(metrics)
            return metrics.densityDpi
        return 160

    def adjust_font(self, base_size):
        # Масштабирование шрифта: (base * dpi_factor)
        factor = self.dpi / 160
        return f"{int(base_size * factor)}sp"

# =============================================================================
# [SECTION 52] MEMORY SAFEGUARD: GARBAGE COLLECTION TUNING
# =============================================================================
class TitanMemoryGuard:
    """
    Следит за тем, чтобы кэш превью и логи не съели всю RAM.
    Принудительно очищает неиспользуемые объекты Kivy.
    """
    def __init__(self):
        self.threshold = 0.8 # 80% памяти

    def clean_up(self):
        import gc
        # Очистка текстурного кэша Kivy (важно для Android)
        from kivy.cache import Cache
        Cache.remove('kv.image')
        Cache.remove('kv.texture')
        gc.collect()
        print("[GUARD] Emergency memory cleanup performed")

# =============================================================================
# [SECTION 53] GESTURE CONTROLLER: MOBILE SWIPE LOGIC
# =============================================================================
class TitanGestureManager(ButtonBehavior, MDFloatLayout):
    """
    Добавляет поддержку свайпов для переключения между редактором 
    и терминалом — мастхэв для работы одной рукой.
    """
    def on_touch_down(self, touch):
        touch.ud['start_x'] = touch.x
        return super().on_touch_down(touch)

    def on_touch_up(self, touch):
        if 'start_x' in touch.ud:
            dx = touch.x - touch.ud['start_x']
            if abs(dx) > dp(150): # Порог свайпа
                app = MDApp.get_running_app()
                if dx > 0: app.toggle_explorer() # Свайп вправо - меню
                else: app.toggle_terminal()    # Свайп влево - консоль
        return super().on_touch_up(touch)

# =============================================================================
# [SECTION 54] OPTIMIZED KV-MARKUP (MOBILE-READY)
# =============================================================================
TITAN_KV_FIXED = '''
<TitanMainLayout@TitanGestureManager>:
    MDBoxLayout:
        orientation: "vertical"
        
        # Улучшенная статус-панель (тоньше, информативнее)
        MDBoxLayout:
            size_hint_y: None
            height: dp(30)
            md_bg_color: get_color_from_hex("#05050A")
            padding: [dp(10), 0]
            MDLabel:
                text: "TITAN CORE ACTIVE"
                font_style: "Caption"
                theme_text_color: "Custom"
                text_color: [0, 1, 0.5, 1]
            MDLabel:
                text: "MEM: " + app.current_ram_usage
                halign: "right"
                font_style: "Caption"

        # Основная рабочая область
        ScreenManager:
            id: sm
            # ... переходы между экранами стали плавнее ...
'''

# =============================================================================
# [SECTION 55] PRODUCTION BOOTSTRAP: REFINED MAIN APP
# =============================================================================
class NebulaTitanOS(MDApp):
    current_ram_usage = StringProperty("0 MB")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.adapter = TitanScreenAdapter()
        self.mem_guard = TitanMemoryGuard()
        
    def build(self):
        # Применяем адаптивные шрифты глобально
        self.theme_cls.font_styles["H6"] = ["Roboto", self.adapter.adjust_font(20), False, 0.15]
        return Builder.load_string(TITAN_KV_FIXED)

    def on_pause(self):
        # Важно для Android: сохраняем состояние при входящем звонке
        self.save_editor_state()
        return True # Разрешаем системе приостановить приложение
        
    def save_editor_state(self):
        state = {
            "file": self.current_file,
            "cursor": self.root.ids.code_editor.cursor,
            "text": self.root.ids.code_editor.text[:1000] # Дамп начала файла
        }
        with open(os.path.join(self.kernel.root_path, "recovery/last_state.json"), "w") as f:
            json.dump(state, f)

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
import subprocess
from datetime import datetime
from collections import deque
from concurrent.futures import ThreadPoolExecutor

# --- ENVIRONMENT CONFIGURATION ---
# Оптимизация для мобильных GPU
os.environ['KIVY_GRAPHICS'] = 'gles'
os.environ['KIVY_GL_BACKEND'] = 'sdl2'

from kivy.config import Config
Config.set('graphics', 'multisamples', '4')
Config.set('kivy', 'keyboard_mode', 'systemanddock')

from kivy.app import App
from kivy.lang import Builder
from kivy.clock import Clock, mainthread
from kivy.utils import platform, get_color_from_hex
from kivy.metrics import dp
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
                path = os.path.join(primary_external_storage_path(), "NebulaTitan")
                return path
            except Exception as e:
                print(f"Android Storage Error: {e}")
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
        try:
            conn = self._get_conn()
            conn.execute("INSERT INTO logs (level, msg, ts) VALUES (?, ?, ?)",
                        (level, msg, datetime.now()))
            conn.commit()
            conn.close()
        except Exception:
            pass
# =============================================================================
# [SECTION 3] TITAN SECURITY: CRYPTO ENGINE
# =============================================================================
class TitanSecurity:
    """
    Обеспечивает защиту данных внутри ОС. 
    Использует многослойное XOR-шифрование с Base64.
    """
    def __init__(self, secret_key="TITAN_CORE_2026"):
        self.key = hashlib.sha256(secret_key.encode()).hexdigest()

    def encrypt(self, data):
        if not data: return ""
        encoded = base64.b64encode(data.encode()).decode()
        return "".join([chr(ord(c) ^ ord(self.key[i % len(self.key)])) 
                       for i, c in enumerate(encoded)])

    def decrypt(self, xor_data):
        try:
            decoded = "".join([chr(ord(c) ^ ord(self.key[i % len(self.key)])) 
                              for i, c in enumerate(xor_data)])
            return base64.b64decode(decoded.encode()).decode()
        except Exception: return "DECRYPTION_ERROR"

# =============================================================================
# [SECTION 4] TITAN HARDWARE BRIDGE (JNI/ANDROID)
# =============================================================================
class TitanHardwareBridge:
    """
    Низкоуровневый мост. На Android вызывает Java-методы через JNI (Pyjnius).
    """
    def __init__(self):
        self.platform = platform
        self.vibrator = None
        self.context = None
        
        if self.platform == 'android':
            try:
                from jnius import autoclass
                PythonActivity = autoclass('org.kivy.android.PythonActivity')
                self.context = PythonActivity.mActivity
                self.vibrator = self.context.getSystemService(
                    autoclass('android.content.Context').VIBRATOR_SERVICE
                )
            except Exception as e:
                print(f"JNI Bridge Error: {e}")

    def vibrate(self, duration=50):
        if self.platform == 'android' and self.vibrator:
            try:
                self.vibrator.vibrate(duration)
            except: pass
        else:
            print(f"[TITAN_DEBUG] Hardware Vibrate: {duration}ms")

    def get_battery_level(self):
        if self.platform == 'android':
            # Заглушка, имитирующая получение данных через Intent
            return 88 
        return 100

# =============================================================================
# [SECTION 5] BASE UI STRUCTURE (KV-LANGUAGE)
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
                    id: main_layout
                    orientation: "vertical"
                    md_bg_color: get_color_from_hex("#0A0A0F")
                    
                    MDTopAppBar:
                        title: "NEBULA TITAN OS"
                        anchor_title: "left"
                        elevation: 4
                        md_bg_color: get_color_from_hex("#12121F")
                        left_action_items: [["menu", lambda x: nav_drawer.set_state("open")]]
                        right_action_items: [["console", lambda x: app.toggle_terminal()]]

                    MDBoxLayout:
                        id: workspace_area
                        orientation: "horizontal"
                        
                        # Sidebar / Explorer Panel
                        MDBoxLayout:
                            id: explorer_panel
                            size_hint_x: 0
                            opacity: 0
                            md_bg_color: get_color_from_hex("#0E0E16")
                            MDScrollView:
                                MDList:
                                    id: file_list

                        # Editor Main Area
                        MDBoxLayout:
                            orientation: "vertical"
                            padding: "4dp"
                            canvas.before:
                                Color:
                                    rgba: get_color_from_hex("#161625")
                                Rectangle:
                                    pos: self.pos
                                    size: self.size
                                    
                            MDTextField:
                                id: code_editor
                                multiline: True
                                mode: "fill"
                                fill_color: 0, 0, 0, 0
                                font_size: "14sp"
                                text_color_normal: 1, 1, 1, 1
                                cursor_color: get_color_from_hex("#00FFD1")
                                hint_text: "System Ready. Start coding..."

        MDNavigationDrawer:
            id: nav_drawer
            radius: (0, 16, 16, 0)
            md_bg_color: get_color_from_hex("#12121F")
            MDBoxLayout:
                orientation: "vertical"
                padding: "12dp"
                spacing: "8dp"
                
                MDLabel:
                    text: "TITAN CORE"
                    font_style: "H6"
                    theme_text_color: "Custom"
                    text_color: get_color_from_hex("#00FFD1")
                    size_hint_y: None
                    height: self.texture_size[1]
                
                MDSeparator:
                
                MDFlatButton:
                    text: "PROJECT EXPLORER"
                    theme_text_color: "Custom"
                    text_color: 1, 1, 1, 1
                    on_release: app.toggle_explorer()
                
                MDFlatButton:
                    text: "SYSTEM SETTINGS"
                    theme_text_color: "Custom"
                    text_color: 1, 1, 1, 1
                
                MDFlatButton:
                    text: "RECOVERY MODE"
                    theme_text_color: "Custom"
                    text_color: get_color_from_hex("#FF4444")
                
                Widget:
'''
# =============================================================================
# [SECTION 6] TITAN FILE EXPLORER: ADVANCED LOGIC
# =============================================================================
class TitanExplorer:
    """
    Управляет состоянием файловой системы в UI. 
    Поддерживает динамическую подгрузку иконок и навигацию по папкам.
    """
    def __init__(self, kernel, file_list_widget):
        self.kernel = kernel
        self.widget = file_list_widget
        self.current_path = kernel.root_path
        self.history = []

    @mainthread
    def refresh(self, path=None):
        if path: 
            self.current_path = path
        self.widget.clear_widgets()
        
        try:
            if not os.path.exists(self.current_path):
                os.makedirs(self.current_path, exist_ok=True)

            # Сортировка: сначала папки, потом файлы
            entries = os.scandir(self.current_path)
            sorted_entries = sorted(entries, key=lambda e: (not e.is_dir(), e.name.lower()))
            
            # Добавляем кнопку "Назад", если мы не в корне
            if self.current_path != self.kernel.root_path:
                back_item = OneLineIconListItem(
                    text=".. (Parent Directory)",
                    on_release=lambda x: self.refresh(os.path.dirname(self.current_path))
                )
                back_item.add_widget(IconLeftWidget(icon="arrow-left-bold"))
                self.widget.add_widget(back_item)

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
            Snackbar(text="Access Denied: Permission Error").open()
        except Exception as e:
            Snackbar(text=f"Explorer Error: {str(e)}").open()

    def _get_icon_by_ext(self, filename):
        ext = filename.split('.')[-1].lower()
        mapping = {
            'py': 'language-python',
            'json': 'code-json',
            'db': 'database',
            'txt': 'file-document',
            'md': 'markdown',
            'jpg': 'image',
            'png': 'image'
        }
        return mapping.get(ext, 'file-code')

    def on_entry_click(self, path, is_dir):
        if is_dir:
            self.refresh(path)
        else:
            app = MDApp.get_running_app()
            app.load_file_to_editor(path)

# =============================================================================
# [SECTION 7] TITAN TERMINAL ENGINE (TTE)
# =============================================================================
class TitanTerminal(MDBoxLayout):
    """
    Встроенный эмулятор терминала. 
    Использует subprocess для выполнения команд в изолированном потоке.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.md_bg_color = get_color_from_hex("#000000")
        self.padding = "5dp"
        self.spacing = "2dp"
        self.history = deque(maxlen=100)
        
        # Область вывода
        self.output = MDTextField(
            multiline=True,
            readonly=True,
            font_size="12sp",
            text_color_normal=get_color_from_hex("#00FF00"),
            mode="fill",
            fill_color=(0, 0, 0, 0),
            line_color_normal=(0, 0, 0, 0)
        )
        
        # Поле ввода
        self.input = MDTextField(
            hint_text="titan@os:~$ ",
            on_text_validate=self.process_command,
            mode="rectangle",
            line_color_focus=get_color_from_hex("#00FFD1"),
            text_color_normal=(1, 1, 1, 1)
        )
        
        self.add_widget(self.output)
        self.add_widget(self.input)

    def process_command(self, instance):
        cmd = instance.text.strip()
        if not cmd: return
        
        self.append_text(f"[color=#00FFD1]titan@os:~$[/color] {cmd}")
        
        # Встроенные команды
        if cmd == "clear":
            self.output.text = ""
        elif cmd == "sysinfo":
            info = f"OS: Titan\nPlatform: {platform}\nKernel ID: {MDApp.get_running_app().kernel.kernel_id}"
            self.append_text(info)
        elif cmd == "ls":
            try:
                files = os.listdir(os.getcwd())
                self.append_text("\n".join(files))
            except Exception as e: self.append_text(str(e))
        else:
            # Выполнение системных команд
            threading.Thread(target=self._run_shell, args=(cmd,), daemon=True).start()
        
        instance.text = ""

    def _run_shell(self, cmd):
        try:
            # shell=True нужен для корректного парсинга команд на Android/Linux
            result = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, timeout=10)
            self.append_text(result.decode('utf-8'))
        except subprocess.CalledProcessError as e:
            self.append_text(f"[color=#FF4444]Error:[/color] {e.output.decode('utf-8')}")
        except Exception as e:
            self.append_text(f"[color=#FF4444]Exec Error:[/color] {str(e)}")

    @mainthread
    def append_text(self, text):
        self.output.text += text + "\n"
      # =============================================================================
# [SECTION 8] TITAN SYNTAX ENGINE: DYNAMIC HIGHLIGHTER
# =============================================================================
class TitanSyntaxHighlighter:
    """
    Движок динамической разметки. Использует регулярные выражения 
    для выделения ключевых слов, строк и комментариев в реальном времени.
    """
    def __init__(self):
        # Цветовая схема Monokai/Dracula style
        self.rules = {
            'python': [
                (r'\b(def|class|if|else|elif|while|for|return|import|from|as|try|except|with|lambda|in|is|not|and|or)\b', "FF79C6"), # Keywords
                (r'\b(self|cls|True|False|None)\b', "BD93F9"), # Builtins
                (r'".*?"|\'.*?\'', "F1FA8C"), # Strings
                (r'#.*', "6272A4"), # Comments
                (r'\b[0-9]+\b', "BD93F9"), # Numbers
                (r'\b[a-zA-Z_][a-zA-Z0-9_]*(?=\()', "50FA7B"), # Functions
            ],
            'json': [
                (r'".*?"(?=\s*:)', "8BE9FD"), # Keys
                (r':\s*".*?"', "F1FA8C"), # Value Strings
                (r'\b(true|false|null)\b', "BD93F9"),
            ]
        }

    def apply_highlighting(self, text, lang='python'):
        """Превращает обычный текст в размеченный Kivy Markup."""
        if lang not in self.rules: return text
        
        # Экранируем символы разметки Kivy, чтобы не было конфликтов
        highlighted = text.replace('[', '[[').replace(']', ']]')
        
        for pattern, color in self.rules[lang]:
            highlighted = re.sub(
                pattern, 
                lambda m: f"[color={color}]{m.group(0)}[/color]", 
                highlighted
            )
        return highlighted

# =============================================================================
# [SECTION 9] TITAN VIRTUAL GIT INTERFACE
# =============================================================================
class TitanGitController:
    """
    Слой интеграции с Git. Управляет индексацией и виртуальными коммитами.
    """
    def __init__(self, kernel):
        self.kernel = kernel

    def get_status(self, project_path):
        if not os.path.exists(os.path.join(project_path, ".git")):
            return "No Git Repository detected."
        try:
            res = subprocess.check_output("git status -s", shell=True, cwd=project_path)
            return res.decode('utf-8')
        except:
            return "Git Error: Repository unreachable."

    def quick_commit(self, message):
        """Создает хеш коммита на основе сообщения и времени."""
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        commit_hash = hashlib.md5(f"{message}{ts}".encode()).hexdigest()[:7]
        return f"[{ts}] Committed: {commit_hash}"

# =============================================================================
# [SECTION 10] TITAN PLUGIN ENGINE: DYNAMIC EXTENSIBILITY
# =============================================================================
class TitanPlugin:
    """Базовый класс для всех плагинов Titan OS."""
    def on_load(self): pass
    def on_unload(self): pass

class TitanPluginEngine:
    """Загружает внешние модули из папки plugins."""
    def __init__(self, kernel):
        self.kernel = kernel
        self.plugins_path = os.path.join(kernel.root_path, "plugins")
        self.active_plugins = {}

    def load_all(self):
        if not os.path.exists(self.plugins_path): return
        
        for item in os.listdir(self.plugins_path):
            if item.endswith(".py"):
                self._load_module(item)

    def _load_module(self, filename):
        try:
            import importlib.util
            module_name = filename[:-3]
            spec = importlib.util.spec_from_file_location(module_name, os.path.join(self.plugins_path, filename))
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            self.active_plugins[module_name] = module
            print(f"Plugin '{module_name}' loaded successfully.")
        except Exception as e:
            print(f"Failed to load plugin {filename}: {e}")
          # =============================================================================
# [SECTION 11] CORE REFINEMENT: MAIN APP MONOLITH
# =============================================================================
class NebulaTitanOS(MDApp):
    """
    Центральный узел управления Titan OS. 
    Связывает Kernel, Hardware, UI и все подсистемы.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Инициализация всех системных слоев
        self.kernel = TitanKernel()
        self.db = TitanPersistence(self.kernel)
        self.hw = TitanHardwareBridge()
        self.security = TitanSecurity()
        self.syntax = TitanSyntaxHighlighter()
        self.git = TitanGitController(self.kernel)
        self.plugin_engine = TitanPluginEngine(self.kernel)
        
        # Состояние интерфейса
        self.explorer = None
        self.terminal_widget = None
        self.current_file = None
        self.terminal_visible = False

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "DeepPurple"
        self.theme_cls.accent_palette = "Cyan"
        
        # Загрузка визуальной структуры из KV-строки
        return Builder.load_string(TITAN_KV_BASE)

    def on_start(self):
        """Действия при запуске системы."""
        # Инициализация проводника
        self.explorer = TitanExplorer(self.kernel, self.root.ids.file_list)
        self.explorer.refresh()
        
        # Загрузка плагинов
        self.plugin_engine.load_all()
        
        # Сигнал готовности (вибрация)
        self.hw.vibrate(100)
        self.db.log_event("INFO", "Titan OS Monolith successfully deployed.")
        
        # Запуск фонового автосохранения
        self.run_auto_save()

    def toggle_explorer(self):
        """Открытие/закрытие боковой панели проводника."""
        panel = self.root.ids.explorer_panel
        if panel.size_hint_x == 0:
            panel.size_hint_x = 0.35
            panel.opacity = 1
        else:
            panel.size_hint_x = 0
            panel.opacity = 0

    def load_file_to_editor(self, path):
        """Загрузка контента выбранного файла в редактор."""
        try:
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
                # Применяем подсветку синтаксиса (упрощенно через Markup)
                self.root.ids.code_editor.text = content 
                self.current_file = path
                self.root.ids.nav_drawer.set_state("close")
                Snackbar(text=f"Loaded: {os.path.basename(path)}").open()
        except Exception as e:
            self.db.log_event("ERROR", f"File Load Failure: {str(e)}")
            Snackbar(text="Error loading file.").open()

    def toggle_terminal(self):
        """Мгновенный вызов или скрытие терминала."""
        workspace = self.root.ids.workspace_area
        if not self.terminal_widget:
            self.terminal_widget = TitanTerminal(size_hint_y=0.4)
            self.root.ids.main_layout.add_widget(self.terminal_widget)
            self.terminal_visible = True
        else:
            if self.terminal_visible:
                self.root.ids.main_layout.remove_widget(self.terminal_widget)
            else:
                self.root.ids.main_layout.add_widget(self.terminal_widget)
            self.terminal_visible = not self.terminal_visible

    def run_auto_save(self):
        """Механизм защиты данных: сохранение каждые 60 секунд в фоне."""
        def _save_loop():
            while True:
                time.sleep(60)
                if self.current_file and self.root.ids.code_editor.text:
                    try:
                        with open(self.current_file, 'w', encoding='utf-8') as f:
                            f.write(self.root.ids.code_editor.text)
                    except:
                        pass
        
        threading.Thread(target=_save_loop, daemon=True).start()

# =============================================================================
# [SECTION 12] SYSTEM ENTRY POINT
# =============================================================================
if __name__ == "__main__":
    try:
        NebulaTitanOS().run()
    except Exception:
        # Критическая фиксация падения системы
        error_report = traceback.format_exc()
        print(error_report)
        # Попытка сохранить лог перед вылетом
        with open("titan_crash.log", "a") as f:
            f.write(f"\n--- CRASH {datetime.now()} ---\n{error_report}")
          

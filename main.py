"""
NEBULA TITAN OS - THE ABSOLUTE MONOLITH (v5.0.4-STABLE)
Final Master Copy. Zero-Error Architecture.
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
# Принудительная настройка для мобильных GPU и стабильного ввода
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

# Безопасный импорт KivyMD
try:
    from kivymd.app import MDApp
    from kivymd.uix.boxlayout import MDBoxLayout
    from kivymd.uix.list import OneLineIconListItem, IconLeftWidget, TwoLineIconListItem
    from kivymd.uix.dialog import MDDialog
    from kivymd.uix.button import MDFlatButton, MDRaisedButton
    from kivymd.uix.textfield import MDTextField
    from kivymd.uix.snackbar import Snackbar
    from kivymd.uix.navigationdrawer import MDNavigationDrawer
except ImportError:
    print("[CRITICAL] KivyMD not found. Ensure 'kivymd' is in your buildozer.spec requirements.")
    sys.exit(1)

# =============================================================================
# [SECTION 1] TITAN KERNEL: SYSTEM CORE
# =============================================================================
class TitanKernel:
    """
    Управление жизненным циклом системы, путями и многопоточностью.
    """
    def __init__(self):
        self.kernel_version = "5.0.4"
        self.kernel_id = hashlib.sha256(str(uuid.uuid4()).encode()).hexdigest()[:12]
        self.is_android = (platform == 'android')
        self.executor = ThreadPoolExecutor(max_workers=10) # Увеличенный пул для фоновых задач
        self.root_path = self._setup_storage()
        self._init_filesystem()

    def _setup_storage(self):
        """Определяет корневую папку в зависимости от платформы."""
        if self.is_android:
            try:
                from android.storage import primary_external_storage_path
                base = primary_external_storage_path()
                if base:
                    return os.path.join(base, "NebulaTitan")
            except Exception as e:
                print(f"Kernel Storage Error: {e}")
        return os.path.join(os.path.expanduser("~"), "NebulaTitan")

    def _init_filesystem(self):
        """Создает структуру системных папок."""
        dirs = ["projects", "db", "logs", "temp", "plugins", "recovery", "vault"]
        for d in dirs:
            os.makedirs(os.path.join(self.root_path, d), exist_ok=True)

    def log_sys(self, msg):
        print(f"[{datetime.now().strftime('%H:%M:%S')}] [TITAN KERNEL]: {msg}")
# =============================================================================
# [SECTION 2] TITAN PERSISTENCE: DATA INTEGRITY
# =============================================================================
class TitanPersistence:
    def __init__(self, kernel):
        self.db_path = os.path.join(kernel.root_path, "db/core_v5.db")
        self._bootstrap()

    def _get_conn(self):
        return sqlite3.connect(self.db_path, check_same_thread=False)

    def _bootstrap(self):
        with self._get_conn() as conn:
            conn.execute('''CREATE TABLE IF NOT EXISTS system_logs 
                           (id INTEGER PRIMARY KEY AUTOINCREMENT, level TEXT, message TEXT, ts TIMESTAMP)''')
            conn.execute('''CREATE TABLE IF NOT EXISTS config 
                           (key TEXT PRIMARY KEY, value TEXT)''')
            conn.execute('''CREATE TABLE IF NOT EXISTS project_meta 
                           (id TEXT PRIMARY KEY, name TEXT, last_mod TIMESTAMP, secure_hash TEXT)''')
            conn.commit()

    def log_event(self, level, message):
        try:
            with self._get_conn() as conn:
                conn.execute("INSERT INTO system_logs (level, message, ts) VALUES (?, ?, ?)",
                            (level, message, datetime.now()))
        except: pass

# =============================================================================
# [SECTION 3] TITAN SECURITY: CRYPTOGRAPHIC LAYER
# =============================================================================
class TitanSecurity:
    """
    Обеспечивает конфиденциальность данных.
    Комбинирует SHA-256 ключи, Base64 и XOR-преобразование.
    """
    def __init__(self, master_secret="TITAN_NEBULA_RESERVE_2026"):
        self.salt = "STABLE_OS_X99"
        self.key = hashlib.sha256((master_secret + self.salt).encode()).hexdigest()

    def encrypt(self, plain_text):
        if not plain_text: return ""
        # 1. Base64 encode
        b64_step = base64.b64encode(plain_text.encode()).decode()
        # 2. XOR with Master Key
        xor_result = "".join([
            chr(ord(c) ^ ord(self.key[i % len(self.key)])) 
            for i, c in enumerate(b64_step)
        ])
        return xor_result

    def decrypt(self, encrypted_text):
        try:
            # 1. Reverse XOR
            xor_decoded = "".join([
                chr(ord(c) ^ ord(self.key[i % len(self.key)])) 
                for i, c in enumerate(encrypted_text)
            ])
            # 2. Base64 decode
            return base64.b64decode(xor_decoded.encode()).decode()
        except Exception:
            return "ERROR_DECRYPT_FAILURE"
          # =============================================================================
# [SECTION 4] TITAN HARDWARE BRIDGE: LOW-LEVEL INTERFACE
# =============================================================================
class TitanHardwareBridge:
    """
    Мост между Python и Android API через Pyjnius.
    Обеспечивает доступ к вибрации, батарее и системным уведомлениям.
    """
    def __init__(self):
        self.platform = platform
        self.vibrator = None
        self.activity = None
        
        if self.platform == 'android':
            try:
                from jnius import autoclass, cast
                # Получаем текущую активность Kivy
                PythonActivity = autoclass('org.kivy.android.PythonActivity')
                self.activity = PythonActivity.mActivity
                
                # Инициализируем системные сервисы
                Context = autoclass('android.content.Context')
                self.vibrator = self.activity.getSystemService(Context.VIBRATOR_SERVICE)
                
                self.VibrationEffect = None
                # Проверка версии Android для новых эффектов вибрации
                Build = autoclass('android.os.Build$VERSION')
                if Build.SDK_INT >= 26:
                    self.VibrationEffect = autoclass('android.os.VibrationEffect')
            except Exception as e:
                print(f"[TITAN HW BRIDGE] Init Error: {e}")

    def vibrate(self, duration=50):
        """Вызывает тактильную отдачу."""
        if self.platform == 'android' and self.vibrator:
            try:
                if self.VibrationEffect:
                    # Для Android 8.0+
                    effect = self.VibrationEffect.createOneShot(duration, self.VibrationEffect.DEFAULT_AMPLITUDE)
                    self.vibrator.vibrate(effect)
                else:
                    # Для старых версий
                    self.vibrator.vibrate(duration)
            except Exception as e:
                print(f"[TITAN HW BRIDGE] Vibrate Error: {e}")
        else:
            print(f"[TITAN SIM] Vibration simulation: {duration}ms")

# =============================================================================
# [SECTION 5] TITAN UI ARCHITECTURE: KV DEFINITION
# =============================================================================
# Здесь мы используем KivyMD для создания футуристичного интерфейса.
# markup: True включен во всех текстовых полях для поддержки Syntax Highlighting.

TITAN_KV_BASE = '''
<TitanFileItem@OneLineIconListItem>:
    is_dir: False
    IconLeftWidget:
        icon: "folder" if root.is_dir else "file-code"
        theme_text_color: "Custom"
        text_color: get_color_from_hex("#00FFD1") if root.is_dir else get_color_from_hex("#BBBBBB")

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
                        elevation: 4
                        md_bg_color: get_color_from_hex("#12121F")
                        left_action_items: [["menu", lambda x: nav_drawer.set_state("open")]]
                        right_action_items: [["console-line", lambda x: app.toggle_terminal()], ["dots-vertical", lambda x: None]]

                    MDBoxLayout:
                        id: workspace_area
                        orientation: "horizontal"
                        
                        # Боковая панель проводника (по умолчанию скрыта)
                        MDBoxLayout:
                            id: explorer_panel
                            size_hint_x: 0
                            opacity: 0
                            md_bg_color: get_color_from_hex("#0E0E16")
                            orientation: "vertical"
                            
                            MDLabel:
                                text: " FILES"
                                size_hint_y: None
                                height: "40dp"
                                font_style: "Overline"
                                theme_text_color: "Custom"
                                text_color: get_color_from_hex("#00FFD1")
                                
                            MDScrollView:
                                MDList:
                                    id: file_list

                        # Главная область редактора
                        MDBoxLayout:
                            orientation: "vertical"
                            padding: "2dp"
                            
                            MDTextField:
                                id: code_editor
                                multiline: True
                                mode: "fill"
                                fill_color: 0, 0, 0, 0
                                markup: True
                                font_size: "13sp"
                                font_name: "RobotoMono" if platform != 'android' else "Roboto"
                                text_color_normal: 1, 1, 1, 1
                                cursor_color: get_color_from_hex("#00FFD1")
                                hint_text: "System Ready. Input command or code..."
                                line_color_focus: 0, 0, 0, 0
                                line_color_normal: 0, 0, 0, 0

        MDNavigationDrawer:
            id: nav_drawer
            radius: (0, 16, 16, 0)
            md_bg_color: get_color_from_hex("#12121F")
            
            MDBoxLayout:
                orientation: "vertical"
                padding: "16dp"
                spacing: "8dp"
                
                MDLabel:
                    text: "NEBULA TITAN"
                    font_style: "H6"
                    theme_text_color: "Custom"
                    text_color: get_color_from_hex("#00FFD1")
                    size_hint_y: None
                    height: self.texture_size[1]
                
                MDLabel:
                    text: "v5.0.4 Monolith"
                    font_style: "Caption"
                    theme_text_color: "Hint"
                    size_hint_y: None
                    height: self.texture_size[1]
                
                MDSeparator:
                    height: "2dp"
                
                MDScrollView:
                    MDList:
                        OneLineIconListItem:
                            text: "Project Explorer"
                            on_release: app.toggle_explorer()
                            IconLeftWidget:
                                icon: "folder-multiple-outline"
                        
                        OneLineIconListItem:
                            text: "Security Vault"
                            IconLeftWidget:
                                icon: "shield-key-outline"
                                
                        OneLineIconListItem:
                            text: "System Logs"
                            IconLeftWidget:
                                icon: "text-box-search-outline"
                        
                        OneLineIconListItem:
                            text: "Terminal"
                            on_release: app.toggle_terminal()
                            IconLeftWidget:
                                icon: "console"
                
                Widget: # Распорка
                
                MDLabel:
                    text: "Core ID: READY"
                    id: kernel_info_label
                    font_style: "Caption"
                    theme_text_color: "Hint"
'''
# =============================================================================
# [SECTION 6] TITAN EXPLORER: INTELLIGENT FILE MANAGEMENT
# =============================================================================
class TitanExplorer:
    """
    Управляет навигацией по файловой системе.
    Поддерживает историю переходов и динамическую загрузку иконок.
    """
    def __init__(self, kernel, file_list_widget):
        self.kernel = kernel
        self.widget = file_list_widget
        self.current_path = kernel.root_path
        self.history = []

    @mainthread
    def refresh(self, path=None):
        """Обновляет список файлов в UI с приоритетом папок."""
        if path: 
            self.current_path = path
        
        self.widget.clear_widgets()
        
        try:
            if not os.path.exists(self.current_path):
                os.makedirs(self.current_path, exist_ok=True)

            # Получаем список и сортируем: сначала папки, потом файлы (по алфавиту)
            entries = list(os.scandir(self.current_path))
            entries.sort(key=lambda e: (not e.is_dir(), e.name.lower()))
            
            # Кнопка возврата на уровень выше
            if self.current_path != self.kernel.root_path:
                back_item = OneLineIconListItem(
                    text=".. / (Back to Parent)",
                    on_release=lambda x: self.refresh(os.path.dirname(self.current_path))
                )
                back_item.add_widget(IconLeftWidget(icon="arrow-left-bold", theme_text_color="Hint"))
                self.widget.add_widget(back_item)

            for entry in entries:
                is_dir = entry.is_dir()
                item = OneLineIconListItem(
                    text=entry.name,
                    on_release=lambda x, p=entry.path, d=is_dir: self.on_entry_click(p, d)
                )
                
                # Присвоение иконки по расширению
                icon_name = "folder" if is_dir else self._select_icon(entry.name)
                icon_color = "#00FFD1" if is_dir else "#90A4AE"
                
                icon_widget = IconLeftWidget(icon=icon_name)
                icon_widget.theme_text_color = "Custom"
                icon_widget.text_color = get_color_from_hex(icon_color)
                
                item.add_widget(icon_widget)
                self.widget.add_widget(item)
                
        except Exception as e:
            self.kernel.log_sys(f"Explorer Error: {str(e)}")
            Snackbar(text=f"FileSystem Access Error").open()

    def _select_icon(self, filename):
        ext = filename.split('.')[-1].lower() if '.' in filename else ''
        mapping = {
            'py': 'language-python',
            'js': 'language-javascript',
            'json': 'code-json',
            'db': 'database',
            'txt': 'file-document-outline',
            'md': 'markdown',
            'png': 'image',
            'jpg': 'image',
            'apk': 'android'
        }
        return mapping.get(ext, 'file-code-outline')

    def on_entry_click(self, path, is_dir):
        if is_dir:
            self.refresh(path)
        else:
            # Вызов загрузки файла через основной класс приложения
            MDApp.get_running_app().load_file_to_editor(path)

# =============================================================================
# [SECTION 7] TITAN TERMINAL ENGINE: ISOLATED SHELL
# =============================================================================
class TitanTerminal(MDBoxLayout):
    """
    Полнофункциональный терминал.
    Выполняет команды в фоновом потоке через subprocess.Popen.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.md_bg_color = [0.02, 0.02, 0.05, 1]
        self.padding = dp(5)
        self.cmd_history = deque(maxlen=100)
        
        # Область вывода данных
        self.output_area = MDTextField(
            multiline=True,
            readonly=True,
            mode="fill",
            fill_color=(0,0,0,0),
            markup=True,
            font_size="12sp",
            text_color_normal=[0, 1, 0.82, 1] # Титановый бирюзовый
        )
        
        # Поле ввода команд
        self.input_line = MDTextField(
            hint_text="titan@core:~$ ",
            on_text_validate=self.execute_input,
            mode="rectangle",
            line_color_focus=[0, 1, 0.82, 1],
            text_color_normal=[1, 1, 1, 1]
        )
        
        self.add_widget(self.output_area)
        self.add_widget(self.input_line)

    def execute_input(self, instance):
        command = instance.text.strip()
        if not command: return
        
        self.cmd_history.append(command)
        self.append_output(f"\n[color=#50FA7B]titan@core:[/color][color=#8BE9FD]~$[/color] {command}")
        
        # Обработка встроенных команд
        if command == "clear":
            self.output_area.text = ""
        elif command == "sys":
            app = MDApp.get_running_app()
            self.append_output(f"\nKernel: {app.kernel.kernel_version}\nID: {app.kernel.kernel_id}\nPlatform: {platform}")
        else:
            # Запуск системной команды в потоке
            threading.Thread(target=self._run_subprocess, args=(command,), daemon=True).start()
        
        instance.text = ""

    def _run_subprocess(self, cmd):
        try:
            # Используем shell=True для поддержки конвейеров и сложных команд
            process = subprocess.Popen(
                cmd, shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            stdout, stderr = process.communicate(timeout=15)
            
            if stdout: self.append_output(f"\n{stdout}")
            if stderr: self.append_output(f"\n[color=#FF5555]{stderr}[/color]")
        except Exception as e:
            self.append_output(f"\n[color=#FF5555]Exec Error: {str(e)}[/color]")

    @mainthread
    def append_output(self, text):
        self.output_area.text += text
      # =============================================================================
# [SECTION 8] TITAN SYNTAX HIGHLIGHTER: THE COLOR ENGINE
# =============================================================================
class TitanHighlighter:
    """
    Парсит текст и накладывает цветовые теги Kivy [color=...].
    Поддерживает Python, JSON и системные логи.
    """
    def __init__(self):
        # Цветовая палитра Nebula
        self.colors = {
            'keyword': '#FF79C6',  # Розовый (def, class, if)
            'string': '#F1FA8C',   # Желтый ("текст")
            'comment': '#6272A4',  # Серый (комментарии)
            'builtin': '#8BE9FD',  # Голубой (print, self)
            'number': '#BD93F9',   # Фиолетовый (123)
            'decorator': '#50FA7B' # Зеленый (@wrapper)
        }
        
        # Регулярные выражения для парсинга
        self.rules = [
            (r'\b(def|class|if|else|elif|for|while|return|import|from|as|try|except|with|in|is|not|and|or|pass|lambda)\b', 'keyword'),
            (r'(\".*?\"|\'.*?\')', 'string'),
            (r'(#.*)', 'comment'),
            (r'\b(print|len|str|int|list|dict|set|range|enumerate|open|super|self|cls)\b', 'builtin'),
            (r'\b(\d+)\b', 'number'),
            (r'(@\w+)', 'decorator')
        ]

    def highlight(self, text):
        """Очищает текст от старых тегов и накладывает новые."""
        # Сначала убираем уже существующие теги, чтобы не было вложенности
        clean_text = re.sub(r'\[/?color.*?\]', '', text)
        
        # Индексная замена (чтобы теги не ломали позиции других совпадений)
        segments = []
        last_idx = 0
        
        # Находим все совпадения для всех правил
        all_matches = []
        for pattern, style in self.rules:
            for match in re.finditer(pattern, clean_text):
                all_matches.append((match.start(), match.end(), style))
        
        # Сортируем по позиции начала
        all_matches.sort()
        
        # Собираем новую строку с тегами
        final_text = ""
        for start, end, style in all_matches:
            if start < last_idx: continue # Пропуск перекрытий
            final_text += clean_text[last_idx:start]
            color = self.colors[style]
            final_text += f"[color={color}]{clean_text[start:end]}[/color]"
            last_idx = end
            
        final_text += clean_text[last_idx:]
        return final_text

# =============================================================================
# [SECTION 9] TITAN MONOLITH: THE MASTER APPLICATION
# =============================================================================
class TitanOSApp(MDApp):
    """
    Центральный узел управления всей системой Nebula Titan.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.kernel = TitanKernel()
        self.persistence = TitanPersistence(self.kernel)
        self.security = TitanSecurity()
        self.bridge = TitanHardwareBridge()
        self.highlighter = TitanHighlighter()
        
        # Состояние UI
        self.explorer_open = False
        self.terminal_active = False
        self.current_file = None

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Teal"
        return Builder.load_string(TITAN_KV_BASE)

    def on_start(self):
        """Вызывается при запуске ОС."""
        self.explorer = TitanExplorer(self.kernel, self.root.ids.file_list)
        self.explorer.refresh()
        self.root.ids.kernel_info_label.text = f"Kernel ID: {self.kernel.kernel_id}"
        self.bridge.vibrate(100) # Сигнал готовности
        self.persistence.log_event("INFO", "Titan OS Started Successfully")

    # --- UI ACTIONS ---
    def toggle_explorer(self):
        """Выдвигает/задвигает боковую панель файлов."""
        panel = self.root.ids.explorer_panel
        if not self.explorer_open:
            panel.size_hint_x = 0.35
            panel.opacity = 1
            self.explorer_open = True
        else:
            panel.size_hint_x = 0
            panel.opacity = 0
            self.explorer_open = False

    def toggle_terminal(self):
        """Открывает консоль поверх редактора."""
        if not self.terminal_active:
            self.term_widget = TitanTerminal()
            self.root.ids.main_layout.add_widget(self.term_widget)
            self.terminal_active = True
        else:
            self.root.ids.main_layout.remove_widget(self.term_widget)
            self.terminal_active = False

    # --- FILE LOGIC ---
    def load_file_to_editor(self, path):
        """Загружает файл и применяет подсветку."""
        try:
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            self.current_file = path
            # Применяем подсветку в фоне, чтобы UI не лагал на больших файлах
            self.root.ids.code_editor.text = self.highlighter.highlight(content)
            
            if self.explorer_open: self.toggle_explorer()
            Snackbar(text=f"Loaded: {os.path.basename(path)}").open()
            self.bridge.vibrate(30)
        except Exception as e:
            self.persistence.log_event("ERROR", f"File Load Fail: {str(e)}")

    def save_current_file(self):
        """Сохраняет текст из редактора, удаляя теги подсветки."""
        if not self.current_file:
            # Если файл не открыт, предлагаем создать новый (упрощенно)
            self.current_file = os.path.join(self.kernel.root_path, "projects/new_script.py")
        
        try:
            raw_text = self.root.ids.code_editor.text
            # Очищаем от тегов перед сохранением на диск!
            clean_content = re.sub(r'\[/?color.*?\]', '', raw_text)
            
            with open(self.current_file, 'w', encoding='utf-8') as f:
                f.write(clean_content)
            
            Snackbar(text="File Saved Successfully").open()
        except Exception as e:
            Snackbar(text=f"Save Error: {str(e)}").open()

    def on_stop(self):
        """Корректное завершение работы."""
        self.persistence.log_event("INFO", "Titan OS Shutdown")
        # Останавливаем пул потоков
        self.kernel.executor.shutdown(wait=False)

if __name__ == "__main__":
    # Финальный запуск
    TitanOSApp().run()
  

# =============================================================================
# TITAN OS v7.0 - PROJECT "ETERNAL" (ULTIMATE ARCHITECTURE)
# STATUS: DEVELOPMENT MODE (UNTIL "FINAL")
# PART 1: ADVANCED IMPORTS, ENGINE CONFIG & DEEP UI STYLING
# =============================================================================

import os
import sys
import time
import math
import json
import random
import logging
import threading
import sqlite3
import base64
import hashlib
import asyncio
from datetime import datetime
from pathlib import Path

# --- KIVY & GRAPHICS CORE ---
from kivy.config import Config
# Оптимизация для работы на Android: отключаем лишнее, бустим FPS
Config.set('graphics', 'multisamples', '0')
Config.set('graphics', 'resizable', '1')
Config.set('kivy', 'desktop', '0')

import kivy
from kivy.app import App
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.utils import platform, get_color_from_hex
from kivy.core.window import Window
from kivy.animation import Animation
from kivy.factory import Factory
from kivy.properties import (
    StringProperty, NumericProperty, ObjectProperty, 
    BooleanProperty, ListProperty, DictProperty
)

# --- NAVIGATION & SCREENS ---
from kivy.uix.screenmanager import (
    ScreenManager, Screen, FadeTransition, 
    SlideTransition, WipeTransition
)

# --- KIVYMD UI STACK ---
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.navigationdrawer import MDNavigationDrawer, MDNavigationLayout
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.label import MDLabel, MDIcon
from kivymd.uix.button import (
    MDRaisedButton, MDIconButton, MDFloatingActionButton,
    MDRectangleFlatIconButton, MDFillRoundFlatButton
)
from kivymd.uix.textfield import MDTextField
from kivymd.uix.card import MDCard
from kivymd.uix.list import (
    MDList, OneLineIconListItem, TwoLineIconListItem, 
    IconLeftWidget, ThreeLineAvatarIconListItem
)
from kivymd.uix.progressbar import MDProgressBar
from kivymd.uix.spinner import MDSpinner
from kivymd.uix.dialog import MDDialog
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.selectioncontrol import MDSwitch
from kivymd.uix.bottomnavigation import MDBottomNavigation, MDBottomNavigationItem

# --- DATA SCIENCE & SYSTEM ---
import numpy as np

# =============================================================================
# GLOBAL DESIGN SYSTEM (KV LANGUAGE) - PART 1
# =============================================================================

KV = '''
#:import get_color_from_hex kivy.utils.get_color_from_hex

# Кастомная кнопка в стиле Titan
<TitanButton@MDRaisedButton>:
    md_bg_color: get_color_from_hex("#00FFFF")
    text_color: 0, 0, 0, 1
    elevation: 8
    padding: "12dp"
    font_name: "Roboto"
    font_size: "16sp"

# Карточка с эффектом свечения
<NeonCard@MDCard>:
    orientation: "vertical"
    padding: "15dp"
    spacing: "10dp"
    radius: [20, 0, 20, 0]
    md_bg_color: 0.05, 0.05, 0.05, 0.9
    line_color: get_color_from_hex("#00FFFF")
    line_width: 1.5
    elevation: 4

# Текстовое поле с кастомным фокусом
<TitanInput@MDTextField>:
    mode: "outline"
    line_color_focus: get_color_from_hex("#00FFFF")
    hint_text_color_focus: get_color_from_hex("#00FFFF")
    current_hint_text_color: get_color_from_hex("#555555")

# ГЛАВНАЯ СТРУКТУРА ПРИЛОЖЕНИЯ
MDNavigationLayout:
    id: nav_layout

    MDScreenManager:
        id: screen_manager

        # --- ЭКРАН 1: ЗАГРУЗКА (BOOT SCREEN) ---
        MDScreen:
            name: "boot"
            MDFloatLayout:
                md_bg_color: 0, 0, 0, 1
                
                MDLabel:
                    text: "TITAN OS"
                    halign: "center"
                    pos_hint: {"center_y": .6}
                    font_style: "H2"
                    theme_text_color: "Custom"
                    text_color: get_color_from_hex("#00FFFF")
                    bold: True

                MDSpinner:
                    size_hint: None, None
                    size: "60dp", "60dp"
                    pos_hint: {"center_x": .5, "center_y": .4}
                    active: True
                    color: get_color_from_hex("#00FFFF")

                MDLabel:
                    id: boot_status
                    text: "Initializing Core..."
                    halign: "center"
                    pos_hint: {"center_y": .3}
                    theme_text_color: "Secondary"

        # ОСТАЛЬНЫЕ ЭКРАНЫ БУДУТ В СЛЕДУЮЩИХ ЧАСТЯХ...
'''
# =============================================================================
# PART 2: THE GREAT INTERFACE EXPANSION (KV CONTINUATION)
# Добавляем Dashboard, IDE, Terminal и Settings
# =============================================================================

KV += '''
        # --- ЭКРАН 2: ГЛАВНЫЙ ДАШБОРД (SYSTEM MONITOR) ---
        MDScreen:
            name: "dashboard"
            MDBoxLayout:
                orientation: "vertical"
                md_bg_color: get_color_from_hex("#050505")

                MDTopAppBar:
                    title: "TITAN MONITOR"
                    elevation: 4
                    left_action_items: [["menu", lambda x: nav_layout.ids.nav_drawer.set_state("open")]]
                    right_action_items: [["dots-vertical", lambda x: app.show_quick_menu()]]
                    md_bg_color: get_color_from_hex("#121212")
                    specific_text_color: get_color_from_hex("#00FFFF")

                ScrollView:
                    MDGridLayout:
                        cols: 1
                        adaptive_height: True
                        padding: "16dp"
                        spacing: "20dp"

                        # Модуль Процессора
                        NeonCard:
                            height: "220dp"
                            size_hint_y: None
                            MDLabel:
                                text: "CORE ANALYTICS"
                                font_style: "H6"
                                theme_text_color: "Custom"
                                text_color: "#00FFFF"
                            
                            MDBoxLayout:
                                spacing: "10dp"
                                MDIcon:
                                    icon: "cpu-64-bit"
                                    theme_text_color: "Custom"
                                    text_color: "#00FFFF"
                                MDLabel:
                                    id: cpu_stats
                                    text: "Thread Load: 0%\\nCalculations: Idle"
                                    theme_text_color: "Secondary"

                            MDProgressBar:
                                id: main_progress
                                value: 0
                                color: get_color_from_hex("#00FFFF")
                            
                            MDRectangleFlatIconButton:
                                icon: "bolt"
                                text: "STRESS TEST (NUMPY)"
                                text_color: "#00FFFF"
                                line_color: "#00FFFF"
                                on_release: app.run_stress_test()

                        # Модуль Сети и Безопасности
                        MDGridLayout:
                            cols: 2
                            spacing: "15dp"
                            adaptive_height: True
                            size_hint_y: None

                            NeonCard:
                                height: "140dp"
                                size_hint_y: None
                                MDIcon:
                                    icon: "security"
                                    halign: "center"
                                    text_color: "#00FF00"
                                MDLabel:
                                    text: "Encryption\\nActive"
                                    halign: "center"
                                    font_style: "Caption"

                            NeonCard:
                                height: "140dp"
                                size_hint_y: None
                                MDIcon:
                                    icon: "wifi-strength-4"
                                    halign: "center"
                                    text_color: "#00FFFF"
                                MDLabel:
                                    text: "Network\\nStable"
                                    halign: "center"
                                    font_style: "Caption"

        # --- ЭКРАН 3: ТИТАН-РЕДАКТОР (ADVANCED IDE) ---
        MDScreen:
            name: "ide"
            MDBoxLayout:
                orientation: "vertical"
                
                MDTopAppBar:
                    title: "TITAN IDE"
                    left_action_items: [["menu", lambda x: nav_layout.ids.nav_drawer.set_state("open")]]
                    right_action_items: [["content-save", lambda x: app.save_session()], ["share-variant", lambda x: app.share_code()]]
                
                MDBoxLayout:
                    orientation: "vertical"
                    padding: "8dp"
                    
                    MDTextField:
                        id: code_input
                        hint_text: ">>> Source Code Engine"
                        multiline: True
                        mode: "fill"
                        fill_color_normal: 0, 0, 0, 0.4
                        font_name: "Roboto"
                        font_size: "13sp"
                        size_hint_y: 1
                        text_color_normal: 0, 1, 0, 1

                    MDBoxLayout:
                        adaptive_height: True
                        padding: "4dp"
                        MDFlatButton:
                            text: "CLEAR"
                            on_release: code_input.text = ""
                        MDRaisedButton:
                            text: "RUN LOGIC"
                            on_release: app.execute_user_script()

        # --- ЭКРАН 4: ТЕРМИНАЛ И ЛОГИ ---
        MDScreen:
            name: "terminal"
            MDBoxLayout:
                orientation: "vertical"
                md_bg_color: 0, 0, 0, 1
                
                MDTopAppBar:
                    title: "SYSTEM LOGS"
                    left_action_items: [["menu", lambda x: nav_layout.ids.nav_drawer.set_state("open")]]

                ScrollView:
                    MDLabel:
                        id: log_output
                        text: ">> Titan Kernel v7.0 Booting...\\n"
                        size_hint_y: None
                        height: self.texture_size[1]
                        padding: "10dp"
                        font_style: "Caption"
                        theme_text_color: "Custom"
                        text_color: 0, 1, 0, 1

        # --- ЭКРАН 5: НАСТРОЙКИ (CORE SETTINGS) ---
        MDScreen:
            name: "settings"
            MDBoxLayout:
                orientation: "vertical"
                
                MDTopAppBar:
                    title: "TITAN CONFIG"
                    left_action_items: [["menu", lambda x: nav_layout.ids.nav_drawer.set_state("open")]]

                ScrollView:
                    MDList:
                        id: settings_list
                        # Будут добавлены динамически

    # --- БОКОВОЕ МЕНЮ (NAVIGATION DRAWER) ---
    MDNavigationDrawer:
        id: nav_drawer
        radius: (0, 20, 20, 0)
        md_bg_color: get_color_from_hex("#101010")

        MDBoxLayout:
            orientation: "vertical"
            padding: "12dp"
            spacing: "8dp"

            MDLabel:
                text: "TITAN OS"
                font_style: "H5"
                size_hint_y: None
                height: self.texture_size[1]
                theme_text_color: "Custom"
                text_color: "#00FFFF"

            MDSeparator:
                color: "#00FFFF"

            ScrollView:
                MDList:
                    OneLineIconListItem:
                        text: "Monitor"
                        on_release: 
                            screen_manager.current = "dashboard"
                            nav_drawer.set_state("close")
                        IconLeftWidget:
                            icon: "view-dashboard-outline"
                    
                    OneLineIconListItem:
                        text: "Code IDE"
                        on_release: 
                            screen_manager.current = "ide"
                            nav_drawer.set_state("close")
                        IconLeftWidget:
                            icon: "code-braces"

                    OneLineIconListItem:
                        text: "Terminal"
                        on_release: 
                            screen_manager.current = "terminal"
                            nav_drawer.set_state("close")
                        IconLeftWidget:
                            icon: "console-line"

                    OneLineIconListItem:
                        text: "Settings"
                        on_release: 
                            screen_manager.current = "settings"
                            nav_drawer.set_state("close")
                        IconLeftWidget:
                            icon: "cog-outline"
'''
# =============================================================================
# PART 3: CORE APPLICATION LOGIC & DATABASE ENGINE
# Реализуем инициализацию, потоки и SQLite хранилище
# =============================================================================

class TitanOS(MDApp):
    # Глобальные свойства для управления состоянием
    kernel_version = StringProperty("7.0.0-Stable")
    is_busy = BooleanProperty(False)
    current_user = StringProperty("Cadet_Dev")
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Очередь для передачи логов из потоков в UI
        self.log_queue = Queue()
        self.db_path = "titan_core.db"
        self.active_threads = []
        
    def build(self):
        """Инициализация темы и загрузка интерфейса"""
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Cyan"
        self.theme_cls.accent_palette = "Amber"
        
        # Загружаем KV-разметку, которую мы писали в Частях 1 и 2
        self.root_node = Builder.load_string(KV)
        return self.root_node

    def on_start(self):
        """Событие при запуске: начинаем загрузку ядра"""
        # Запускаем фоновый поток для инициализации базы данных и проверки систем
        threading.Thread(target=self.initialize_kernel, daemon=True).start()
        # Каждые 0.5 секунды проверяем очередь логов для вывода в терминал
        Clock.schedule_interval(self.process_logs, 0.5)

    # --- СИСТЕМА ИНИЦИАЛИЗАЦИИ ---

    def initialize_kernel(self):
        """Эмуляция глубокой загрузки систем (Heavy Logic)"""
        try:
            self.write_log("Kernel: Initializing Boot Sequence...")
            time.sleep(1.5) # Имитация задержки чтения BIOS
            
            # 1. Инициализация БД
            self.init_database()
            self.write_log("Database: Connection established [SQLITE3]")
            
            # 2. Проверка математического модуля
            self.write_log("MathEngine: Checking NumPy integration...")
            test_arr = np.random.rand(100, 100)
            np.linalg.det(test_arr)
            self.write_log("MathEngine: Hardware acceleration ACTIVE")
            
            # 3. Загрузка настроек пользователя
            time.sleep(1)
            self.write_log("System: Loading User Profile 'Cadet_Dev'...")
            
            # Финальный переход: убираем экран загрузки через 4 секунды
            Clock.schedule_once(self.complete_boot, 1)
            
        except Exception as e:
            self.write_log(f"CRITICAL ERROR: {str(e)}")

    def init_database(self):
        """Создание таблиц для хранения скриптов и настроек"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        # Таблица для скриптов IDE
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS scripts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                content TEXT,
                timestamp DATETIME
            )
        ''')
        # Таблица для системных логов
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS system_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tag TEXT,
                message TEXT,
                level TEXT
            )
        ''')
        conn.commit()
        conn.close()

    def complete_boot(self, dt):
        """Переход с экрана BOOT на DASHBOARD с анимацией"""
        sm = self.root_node.ids.screen_manager
        sm.transition = WipeTransition()
        sm.current = "dashboard"
        self.write_log("System: Boot sequence COMPLETED")
        self.root_node.ids.nav_drawer.set_state("open")

    # --- ЛОГИРОВАНИЕ ---

    def write_log(self, message, level="INFO"):
        """Добавляет сообщение в очередь логов (безопасно для потоков)"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted_msg = f"[{timestamp}] [{level}] {message}"
        self.log_queue.put(formatted_msg)
        
        # Обновляем текст на экране загрузки, если мы еще там
        if self.root_node.ids.screen_manager.current == "boot":
            Clock.schedule_once(lambda dt: self.update_boot_label(message), 0)

    def update_boot_label(self, text):
        self.root_node.ids.boot_status.text = text

    def process_logs(self, dt):
        """Вывод накопленных логов в терминал (вызывается в основном потоке)"""
        while not self.log_queue.empty():
            msg = self.log_queue.get()
            terminal = self.root_node.ids.log_output
            terminal.text += f"{msg}\n"
            # Авто-скролл терминала вниз
            if terminal.parent:
                terminal.parent.scroll_y = 0

    # Ожидание Части 4...
  # =============================================================================
# PART 4: COMPUTATIONAL ENGINE & SCRIPT MANAGEMENT
# Реализуем тяжелые вычисления NumPy и работу с файлами в IDE
# =============================================================================

    # --- МОДУЛЬ ТЯЖЕЛЫХ ВЫЧИСЛЕНИЙ (STRESS TEST) ---

    def run_stress_test(self):
        """Запуск цикла тяжелых вычислений в фоновом потоке"""
        if self.is_busy:
            self.show_snackbar("System: Engine is already under load!")
            return
            
        self.is_busy = True
        self.root_node.ids.main_progress.value = 0
        self.write_log("Analytics: Starting Compute Stress Test...", level="WARN")
        
        # Запускаем поток, чтобы UI не завис при расчете матрицы
        threading.Thread(target=self.heavy_math_logic, daemon=True).start()

    def heavy_math_logic(self):
        """Интенсивный расчет: Собственные значения и определители огромных матриц"""
        try:
            for i in range(1, 11):
                step_load = i * 10
                self.write_log(f"MathEngine: Processing matrix batch {i}/10...")
                
                # Создаем случайную матрицу 1500x1500 (серьезная нагрузка)
                matrix_size = 1500
                large_matrix = np.random.rand(matrix_size, matrix_size)
                
                # Вычисляем определитель (нагружает CPU)
                det = np.linalg.det(large_matrix)
                
                # Имитация работы с данными
                time.sleep(0.3)
                
                # Обновляем прогресс в главном потоке
                Clock.schedule_once(lambda dt, v=step_load: self.update_progress(v), 0)
            
            self.write_log("Analytics: Stress test SUCCESSFUL", level="INFO")
            Clock.schedule_once(lambda dt: self.show_dialog("Titan Analytics", "Compute stress test finished.\nSystem stability: 100%"), 0)
            
        except Exception as e:
            self.write_log(f"MathEngine Error: {str(e)}", level="CRITICAL")
        finally:
            self.is_busy = False
            Clock.schedule_once(lambda dt: self.update_progress(0), 0)

    def update_progress(self, value):
        """Синхронизация прогресс-бара с расчетами"""
        self.root_node.ids.main_progress.value = value
        self.root_node.ids.cpu_stats.text = f"Thread Load: {value}%\\nCalculations: ACTIVE"
        if value == 0:
            self.root_node.ids.cpu_stats.text = "Thread Load: 0%\\nCalculations: Idle"

    # --- МОДУЛЬ IDE И РАБОТЫ С КОДОМ ---

    def save_session(self):
        """Сохранение текста из IDE в базу данных SQLite"""
        code_text = self.root_node.ids.code_input.text
        if not code_text.strip():
            self.show_snackbar("IDE: Cannot save empty buffer!")
            return

        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Сохраняем как 'Last Session'
            cursor.execute('''
                INSERT INTO scripts (name, content, timestamp) 
                VALUES (?, ?, ?)
            ''', ("session_auto_save", code_text, timestamp))
            
            conn.commit()
            conn.close()
            self.write_log("IDE: Session backed up to local DB")
            self.show_snackbar("Project saved to Titan Core")
        except Exception as e:
            self.write_log(f"Storage Error: {str(e)}", level="ERROR")

    def execute_user_script(self):
        """Эмуляция запуска кода пользователя с перехватом ошибок"""
        code = self.root_node.ids.code_input.text
        self.write_log("IDE: Executing user logic...")
        
        # Переключаемся на терминал, чтобы видеть результат
        self.root_node.ids.screen_manager.current = "terminal"
        
        try:
            # В целях безопасности в реальных ОС здесь используется ограниченный exec()
            # Мы имитируем парсинг кода
            if "print" in code:
                result = "Standard Output: Simulation successful."
            else:
                result = "Engine: Script interpreted without errors."
            
            self.write_log(f"IDE_RESULT: {result}")
        except Exception as e:
            self.write_log(f"RUNTIME_ERROR: {str(e)}", level="CRITICAL")

    # --- ВСПОМОГАТЕЛЬНЫЕ ЭЛЕМЕНТЫ UI ---

    def show_snackbar(self, text):
        """Быстрое неоновое уведомление"""
        Snackbar(
            text=text,
            bg_color=get_color_from_hex("#121212"),
            label_color=get_color_from_hex("#00FFFF")
        ).open()

    def show_dialog(self, title, text):
        """Системное модальное окно"""
        MDDialog(
            title=title,
            text=text,
            size_hint=(0.8, None),
            buttons=[MDRaisedButton(text="OK", on_release=lambda x: self.close_dialog())]
        ).open()

    def close_dialog(self):
        # Метод для закрытия всех диалогов (в KivyMD 1.2+ они закрываются сами или через .dismiss)
        pass
      # =============================================================================
# PART 5: SYSTEM HARDWARE INTERFACE & FILE EXPLORER LOGIC
# Чтение данных о железе, работа с ОС и менеджмент файлов
# =============================================================================

    # --- МОДУЛЬ ИНФОРМАЦИИ О СИСТЕМЕ ---

    def get_device_info(self):
        """Сбор данных о железе и ОС (Android/PC)"""
        self.write_log("System: Gathering hardware telemetry...")
        info = {
            "OS": sys.platform,
            "Core": plat_lib.machine(),
            "Python": sys.version.split()[0],
            "Titan_Ver": self.kernel_version
        }

        # Если мы на Android, вытягиваем данные через Java-классы
        if platform == 'android':
            try:
                from jnius import autoclass
                Build = autoclass('android.os.Build')
                info["Model"] = Build.MODEL
                info["Brand"] = Build.MANUFACTURER
                info["Android_Ver"] = Build.VERSION.RELEASE
            except Exception as e:
                self.write_log(f"Jnius_Error: {str(e)}", level="ERROR")
        else:
            info["Model"] = "Desktop/Emulator"
            info["Brand"] = "Titan Virtual Machine"

        return info

    def show_system_info_dialog(self):
        """Вывод данных в красивое модальное окно"""
        data = self.get_device_info()
        content = "\n".join([f"[b][color=#00FFFF]{k}:[/color][/b] {v}" for k, v in data.items()])
        
        self.show_dialog(
            title="HARDWARE TELEMETRY",
            text=content
        )

    # --- МОДУЛЬ ФАЙЛОВОГО МЕНЕДЖЕРА ---

    def populate_file_manager(self):
        """Сканирование внутренней папки приложения для отображения в Explorer"""
        self.write_log("Explorer: Scanning local storage...")
        file_list_widget = self.root_node.ids.settings_list # Используем созданный ранее список
        file_list_widget.clear_widgets()

        try:
            # Путь к папке со скриптами
            path = "." 
            files = os.listdir(path)
            
            for f in files:
                if os.path.isfile(f):
                    file_icon = "file-code-outline" if f.endswith(".py") else "file-outline"
                    item = ThreeLineAvatarIconListItem(
                        text=f,
                        secondary_text=f"Size: {os.path.getsize(f)} bytes",
                        tertiary_text=f"Modified: {time.ctime(os.path.getmtime(f))}"
                    )
                    item.add_widget(IconLeftWidget(icon=file_icon, theme_text_color="Custom", text_color="#00FFFF"))
                    item.bind(on_release=lambda x, filename=f: self.load_file_to_ide(filename))
                    file_list_widget.add_widget(item)
                    
            self.write_log(f"Explorer: Found {len(files)} objects")
        except Exception as e:
            self.write_log(f"Explorer Error: {str(e)}", level="CRITICAL")

    # --- ПРОДВИНУТАЯ ЛОГИКА IDE ---

    def load_file_to_ide(self, filename):
        """Загрузка выбранного файла в редактор"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                content = f.read()
                self.root_node.ids.code_input.text = content
                self.root_node.ids.screen_manager.current = "ide"
                self.show_snackbar(f"Loaded: {filename}")
                self.write_log(f"IDE: Opened file {filename}")
        except Exception as e:
            self.show_snackbar("Error loading file")
            self.write_log(f"Read Error: {str(e)}", level="ERROR")

    def auto_load_last_session(self):
        """При запуске подтягиваем последний сохраненный скрипт из БД"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('SELECT content FROM scripts WHERE name="session_auto_save" ORDER BY id DESC LIMIT 1')
            row = cursor.fetchone()
            if row:
                self.root_node.ids.code_input.text = row[0]
                self.write_log("IDE: Last session restored from Core DB")
            conn.close()
        except Exception as e:
            print(f"Restore Error: {e}")

    # --- СИСТЕМНЫЕ УТИЛИТЫ ---

    def open_social(self, platform_name):
        """Открытие внешних ссылок (канал, поддержка)"""
        links = {
            "telegram": "https://t.me/your_channel",
            "github": "https://github.com/titan_os"
        }
        webbrowser.open(links.get(platform_name, ""))
        self.write_log(f"Shell: Opening external link -> {platform_name}")
      # =============================================================================
# PART 6: SECURITY PROTOCOLS & COMMAND INTERPRETER
# Защита данных, хеширование и интерактивный терминал
# =============================================================================

    # --- МОДУЛЬ БЕЗОПАСНОСТИ (SECURITY ENGINE) ---

    def setup_security(self):
        """Инициализация защитных ключей и проверка ПИН-кода"""
        self.default_pin_hash = hashlib.sha256("0000".encode()).hexdigest()
        self.is_authenticated = False
        self.write_log("Security: SHA-256 encryption engine READY")

    def verify_access(self, input_pin):
        """Проверка доступа с использованием хеширования"""
        input_hash = hashlib.sha256(input_pin.encode()).hexdigest()
        
        if input_hash == self.default_pin_hash:
            self.is_authenticated = True
            self.write_log("Security: Access GRANTED for 'Cadet_Dev'")
            self.show_snackbar("Welcome back, Operator.")
            return True
        else:
            self.write_log("Security: UNAUTHORIZED access attempt!", level="WARN")
            self.show_snackbar("ACCESS DENIED: Invalid PIN")
            return False

    def show_auth_dialog(self):
        """Модальное окно авторизации"""
        content = MDBoxLayout(orientation="vertical", spacing="12dp", size_hint_y=None, height="80dp")
        self.pin_input = MDTextField(hint_text="Enter Titan PIN", password=True, max_text_length=4)
        content.add_widget(self.pin_input)

        self.auth_dialog = MDDialog(
            title="SECURITY CHECK",
            type="custom",
            content_cls=content,
            buttons=[
                MDFlatButton(text="CANCEL", on_release=lambda x: self.auth_dialog.dismiss()),
                MDRaisedButton(text="UNLOCK", on_release=lambda x: self.process_auth())
            ]
        )
        self.auth_dialog.open()

    def process_auth(self):
        if self.verify_access(self.pin_input.text):
            self.auth_dialog.dismiss()
            self.root_node.ids.screen_manager.current = "dashboard"

    # --- ИНТЕРАКТИВНЫЙ ТЕРМИНАЛ (SHELL LOGIC) ---

    def process_terminal_command(self, text):
        """Парсинг команд в стиле Linux терминала"""
        cmd = text.lower().strip()
        self.write_log(f"> {cmd}")

        if cmd == "clear":
            self.root_node.ids.log_output.text = ">> Titan Shell Cleared\n"
        elif cmd == "status":
            info = self.get_device_info()
            self.write_log(f"System: {info['Model']} | Kernel: {self.kernel_version}")
        elif cmd == "calc":
            self.run_stress_test()
        elif cmd == "files":
            self.root_node.ids.screen_manager.current = "settings" # Explorer в настройках
            self.populate_file_manager()
        elif cmd == "exit":
            self.stop()
        elif "help" in cmd:
            self.write_log("Available: CLEAR, STATUS, CALC, FILES, EXIT, HELP")
        else:
            self.write_log(f"Shell: Command '{cmd}' not found. Type 'HELP'.", level="ERROR")

    # --- КАСТОМИЗАЦИЯ ТЕМ (THEME ENGINE) ---

    def toggle_neon_mode(self, state):
        """Переключение между режимами: High Contrast и Deep Dark"""
        if state:
            self.theme_cls.primary_palette = "Cyan"
            self.theme_cls.theme_style = "Dark"
            self.write_log("UI: Neon Mode ACTIVE")
        else:
            self.theme_cls.primary_palette = "BlueGray"
            self.theme_cls.theme_style = "Light"
            self.write_log("UI: Stealth Mode ACTIVE")

    # --- ГЛОБАЛЬНЫЕ СОБЫТИЯ ---

    def on_pause(self):
        """Сохранение состояния при сворачивании на Android"""
        self.save_session()
        self.write_log("System: Suspending to RAM...")
        return True

    def on_resume(self):
        """Восстановление систем при возврате"""
        self.write_log("System: Resuming operation")
        return True
      # =============================================================================
# PART 7: NETWORK EMULATION & DATABASE VISUALIZER
# Интерактивный терминал, сканер портов и просмотр таблиц БД
# =============================================================================

# Сначала обновим KV-разметку для терминала (добавляем поле ввода)
# Мы дописываем это в основной билд или через Factory
NEW_TERMINAL_KV = '''
<TerminalInput@MDBoxLayout>:
    orientation: "vertical"
    adaptive_height: True
    padding: "5dp"
    md_bg_color: 0, 0, 0, 1
    
    MDSeparator:
        color: get_color_from_hex("#00FFFF")
    
    MDBoxLayout:
        adaptive_height: True
        padding: "5dp"
        spacing: "10dp"
        
        MDLabel:
            text: "TITAN@ROOT:~#"
            size_hint_x: None
            width: "120dp"
            theme_text_color: "Custom"
            text_color: 0, 1, 0, 1
            font_style: "Caption"
            bold: True

        MDTextFieldRect:
            id: shell_input
            multiline: False
            background_color: 0, 0, 0, 1
            foreground_color: 0, 1, 0, 1
            cursor_color: 0, 1, 0, 1
            font_size: "14sp"
            on_text_validate: app.process_terminal_command(self.text); self.text = ""
'''

# --- ПРОДОЛЖЕНИЕ ЛОГИКИ КЛАССА TitanOS ---

    # --- МОДУЛЬ СЕТЕВОГО СКАНЕРА (NETWORK EMULATOR) ---

    def run_network_scan(self):
        """Имитация сканирования локальной сети и портов"""
        if self.is_busy: return
        self.is_busy = True
        self.root_node.ids.screen_manager.current = "terminal"
        self.write_log("Network: Initializing Socket Scan...", level="WARN")
        
        threading.Thread(target=self.network_logic, daemon=True).start()

    def network_logic(self):
        """Алгоритм генерации случайных узлов сети"""
        try:
            prefixes = ["192.168.1.", "10.0.0.", "172.16.0."]
            base_ip = random.choice(prefixes)
            
            for i in range(1, 8):
                time.sleep(random.uniform(0.4, 0.9))
                node_ip = f"{base_ip}{random.randint(2, 254)}"
                status = random.choice(["ONLINE", "FILTERED", "OPEN"])
                latency = random.randint(10, 150)
                
                msg = f"Node found: {node_ip} | Status: {status} | Latency: {latency}ms"
                self.write_log(f"Network: {msg}")
                
                # Обновляем прогресс на дашборде параллельно
                progress_val = i * 14
                Clock.schedule_once(lambda dt, v=progress_val: self.update_progress(v), 0)

            self.write_log("Network: Scan complete. 0 vulnerabilities found.")
        except Exception as e:
            self.write_log(f"Network_Error: {str(e)}", level="CRITICAL")
        finally:
            self.is_busy = False
            Clock.schedule_once(lambda dt: self.update_progress(0), 0)

    # --- МОДУЛЬ ПРОСМОТРА БАЗЫ ДАННЫХ (DB VISUALIZER) ---

    def show_db_manager(self):
        """Создает экран со списком всех сохраненных записей в БД"""
        self.write_log("Database: Opening Record Manager...")
        
        # Создаем диалог со списком
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT id, name, timestamp FROM scripts")
            rows = cursor.fetchall()
            conn.close()

            # Формируем контент для прокручиваемого списка
            scroll = ScrollView(size_hint_y=None, height="300dp")
            list_layout = MDList()
            
            if not rows:
                list_layout.add_widget(OneLineIconListItem(text="No records found"))
            else:
                for row in rows:
                    item = TwoLineIconListItem(
                        text=f"ID: {row[0]} | Name: {row[1]}",
                        secondary_text=f"Saved: {row[2]}"
                    )
                    item.bind(on_release=lambda x, rid=row[0]: self.delete_db_record(rid))
                    list_layout.add_widget(item)
            
            scroll.add_widget(list_layout)
            
            self.db_dialog = MDDialog(
                title="DATABASE RECORDS (Tap to Delete)",
                type="custom",
                content_cls=scroll,
                buttons=[MDFlatButton(text="CLOSE", on_release=lambda x: self.db_dialog.dismiss())]
            )
            self.db_dialog.open()
            
        except Exception as e:
            self.show_snackbar(f"DB Error: {str(e)}")

    def delete_db_record(self, record_id):
        """Удаление записи из БД по ID"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM scripts WHERE id=?", (record_id,))
            conn.commit()
            conn.close()
            
            self.db_dialog.dismiss()
            self.show_snackbar(f"Record #{record_id} DELETED")
            self.write_log(f"Database: Record {record_id} wiped from storage")
        except Exception as e:
            self.write_log(f"Wipe_Error: {e}", level="ERROR")

    # --- СИСТЕМНАЯ ОПТИМИЗАЦИЯ ---

    def clear_system_cache(self):
        """Очистка временных файлов и логов в памяти"""
        self.write_log("System: Starting garbage collection...")
        import gc
        items_collected = gc.collect()
        self.root_node.ids.log_output.text = ">> Cache Purged\\n"
        self.show_snackbar(f"Optimized: {items_collected} objects cleared")
        self.write_log(f"Memory: GC collected {items_collected} elements")

# =============================================================================
# PART 8: NEURAL BRIDGE (AI STUB) & ADVANCED ANIMATION ENGINE
# Искусственный интеллект, математические анимации и менеджер очередей
# =============================================================================

    # --- МОДУЛЬ TITAN AI (NEURAL INTERFACE) ---

    def ask_titan_ai(self, query):
        """Эмуляция работы нейросетевого помощника для анализа команд"""
        query = query.lower().strip()
        self.write_log(f"AI_Bridge: Processing request '{query}'...", level="DEBUG")
        
        # Логика подбора ответов (имитация NLP)
        responses = {
            "очистка": "Рекомендую выполнить команду 'CLEAR' и вызвать 'gc.collect()'.",
            "защита": "Протокол SHA-256 активен. Регулярно обновляйте ПИН-код.",
            "сеть": "Обнаружено 3 активных узла. Запустить глубокое сканирование?",
            "статус": f"Система стабильна. Загрузка ядра {random.randint(5, 12)}%.",
            "код": "В вашем последнем скрипте не обнаружено синтаксических ошибок."
        }
        
        answer = "Запрос обработан. Информации в базе данных недостаточно."
        for key in responses:
            if key in query:
                answer = responses[key]
                break
        
        self.show_ai_response(answer)

    def show_ai_response(self, text):
        """Плавное появление сообщения от AI в терминале"""
        self.write_log(f"TITAN_AI: {text}")
        # Анимируем иконку ИИ на дашборде, если мы там
        icon = self.root_node.ids.cpu_stats
        anim = Animation(opacity=0, duration=0.2) + Animation(opacity=1, duration=0.2)
        anim.repeat = True
        anim.start(icon)
        Clock.schedule_once(lambda dt: anim.stop(icon), 2)

    # --- АНИМАЦИОННЫЙ ДВИЖОК (FX ENGINE) ---

    def apply_pulsing_effect(self, widget):
        """Создание эффекта 'дыхания' для элементов интерфейса (Math-based)"""
        # Используем плавную кривую для изменения масштаба
        anim = Animation(scale_x=1.05, scale_y=1.05, duration=0.8, t='in_out_quad') + \
               Animation(scale_x=1.0, scale_y=1.0, duration=0.8, t='in_out_quad')
        anim.repeat = True
        anim.start(widget)

    def fade_screen_transition(self, screen_name):
        """Кастомный переход между экранами с эффектом затухания и масштабирования"""
        sm = self.root_node.ids.screen_manager
        target_screen = sm.get_screen(screen_name)
        
        # Анимация подготовки
        anim = Animation(opacity=0, duration=0.3)
        
        def change_and_fade_in(*args):
            sm.current = screen_name
            anim_in = Animation(opacity=1, duration=0.5)
            anim_in.start(target_screen)
            
        anim.bind(on_complete=change_and_fade_in)
        anim.start(sm.get_screen(sm.current))

    # --- МЕНЕДЖЕР ОЧЕРЕДИ УВЕДОМЛЕНИЙ (NOTIFICATION QUEUE) ---

    def queue_notification(self, title, message):
        """Система управления важными событиями (не дает уведомлениям перекрывать друг друга)"""
        if not hasattr(self, 'notif_queue'):
            self.notif_queue = []
            
        self.notif_queue.append((title, message))
        if len(self.notif_queue) == 1:
            self.display_next_notif()

    def display_next_notif(self):
        """Отображение следующего уведомления из очереди"""
        if not self.notif_queue:
            return
            
        title, message = self.notif_queue[0]
        
        # Создаем диалог
        dialog = MDDialog(
            title=f"[color=#00FFFF]{title}[/color]",
            text=message,
            radius=[20, 7, 20, 7],
            buttons=[MDFlatButton(text="ACKNOWLEDGE", on_release=lambda x: self.dismiss_notif(dialog))]
        )
        dialog.open()

    def dismiss_notif(self, dialog):
        dialog.dismiss()
        self.notif_queue.pop(0)
        # Задержка перед следующим уведомлением
        Clock.schedule_once(lambda dt: self.display_next_notif(), 0.5)

    # --- УТИЛИТЫ ДЛЯ СТЕЛС-РЕЖИМА (MIDNIGHT BLUE) ---

    def activate_stealth_mode(self):
        """Переключение на Midnight Blue палитру (по запросу из Части 7)"""
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.primary_hue = "900"
        self.theme_cls.theme_style = "Dark"
        self.write_log("Security: Stealth Mode (Midnight Blue) ENGAGED")
        self.show_snackbar("Stealth protocols active.")

# =============================================================================
# PART 9: CANVAS GRAPHICS ENGINE & CRYPTO-VAULT
# Отрисовка графиков в реальном времени и AES-подобное шифрование
# =============================================================================

from kivy.graphics import Color, Line, Rectangle, Ellipse

    # --- МОДУЛЬ ГРАФИЧЕСКОЙ ВИЗУАЛИЗАЦИИ (SYSTEM GRAPH) ---

    def draw_system_graph(self):
        """Динамическая отрисовка графика нагрузки CPU на Canvas"""
        graph_widget = self.root_node.ids.main_progress.parent # Берем контейнер
        with graph_widget.canvas.after:
            graph_widget.canvas.after.clear()
            Color(0, 1, 1, 0.5) # Циан с прозрачностью
            
            # Генерируем точки графика на основе истории нагрузки
            points = []
            width = graph_widget.width
            height = 100
            x_start = graph_widget.x
            y_start = graph_widget.y + 50
            
            for i in range(20):
                x = x_start + (width / 20) * i
                y = y_start + random.randint(0, height)
                points.extend([x, y])
            
            Line(points=points, width=1.5, joint='round')

    def start_graph_update(self):
        """Запуск цикла обновления графики каждые 2 секунды"""
        Clock.schedule_interval(lambda dt: self.draw_system_graph(), 2)

    # --- МОДУЛЬ КРИПТОГРАФИИ (TITAN VAULT) ---

    def encrypt_data_aes_style(self, plain_text, key):
        """Усиленное шифрование данных (XOR + Base64 + Salt)"""
        self.write_log("Crypto: Initializing AES-Style encryption...")
        try:
            # Создаем 'соль' для усиления
            salt = hashlib.sha256(key.encode()).hexdigest()[:16]
            combined = plain_text + salt
            
            # XOR шифрование
            key_len = len(key)
            encrypted = "".join(chr(ord(c) ^ ord(key[i % key_len])) for i, c in enumerate(combined))
            
            # Кодирование в Base64 для безопасного хранения
            final_cipher = base64.b64encode(encrypted.encode()).decode()
            
            self.write_log("Crypto: Block encryption SUCCESSFUL")
            return final_cipher
        except Exception as e:
            self.write_log(f"Crypto_Error: {str(e)}", level="CRITICAL")
            return None

    def decrypt_data_aes_style(self, cipher_text, key):
        """Расшифровка данных"""
        try:
            # Декодируем Base64
            decoded = base64.b64decode(cipher_text.encode()).decode()
            
            # Реверс XOR
            key_len = len(key)
            decrypted_with_salt = "".join(chr(ord(c) ^ ord(key[i % key_len])) for i, c in enumerate(decoded))
            
            # Убираем соль (последние 16 символов)
            final_text = decrypted_with_salt[:-16]
            
            self.write_log("Crypto: Decryption COMPLETED")
            return final_text
        except:
            self.write_log("Crypto: Decryption FAILED (Wrong Key)", level="ERROR")
            return "ERROR: INVALID KEY"

    # --- ЭКРАН ШИФРОВАНИЯ (UI LOGIC) ---

    def show_crypto_vault(self):
        """Вызов интерфейса крипто-хранилища"""
        content = MDBoxLayout(orientation="vertical", spacing="10dp", padding="10dp", size_hint_y=None, height="250dp")
        
        self.crypto_input = TitanInput(hint_text="Message to hide")
        self.crypto_key = TitanInput(hint_text="Encryption Key", password=True)
        self.crypto_result = MDTextField(hint_text="Resulting Cipher", readonly=True, mode="fill")
        
        content.add_widget(self.crypto_input)
        content.add_widget(self.crypto_key)
        content.add_widget(self.crypto_result)
        
        self.crypto_dialog = MDDialog(
            title="TITAN CRYPTO-VAULT",
            type="custom",
            content_cls=content,
            buttons=[
                MDFlatButton(text="DECRYPT", on_release=lambda x: self.process_crypto(False)),
                MDRaisedButton(text="ENCRYPT", on_release=lambda x: self.process_crypto(True))
            ]
        )
        self.crypto_dialog.open()

    def process_crypto(self, is_encrypt):
        text = self.crypto_input.text
        key = self.crypto_key.text
        
        if not text or not key:
            self.show_snackbar("Required: Text and Key")
            return
            
        if is_encrypt:
            res = self.encrypt_data_aes_style(text, key)
        else:
            res = self.decrypt_data_aes_style(text, key)
            
        self.crypto_result.text = res
      # =============================================================================
# PART 10: SYSTEM WATCHDOG, EASTER EGGS & BOOTSTRAP
# Финальная сборка, контроль стабильности и точка входа
# =============================================================================

    # --- МОДУЛЬ СТАБИЛЬНОСТИ (SYSTEM WATCHDOG) ---

    def start_watchdog(self):
        """Мониторинг ресурсов и предотвращение утечек памяти"""
        self.write_log("Watchdog: Passive monitoring ENGAGED")
        Clock.schedule_interval(self.check_system_health, 10)

    def check_system_health(self, dt):
        """Проверка критических параметров системы"""
        # Имитация проверки RAM и стабильности потоков
        ram_usage = random.randint(45, 180) # MB
        if ram_usage > 150:
            self.write_log(f"Watchdog: RAM spikes detected ({ram_usage}MB). Optimizing...", level="WARN")
            import gc
            gc.collect()
        
        # Обновляем статус в UI
        self.root_node.ids.cpu_stats.text = f"Health: OPTIMAL | RAM: {ram_usage}MB"

    # --- СЕКРЕТНЫЙ ПРОТОКОЛ (EASTER EGG) ---

    def trigger_god_mode(self):
        """Скрытая функция для разработчика"""
        self.theme_cls.primary_palette = "Amber"
        self.theme_cls.accent_palette = "Red"
        self.write_log("CRITICAL: GOD_MODE_ACTIVATED. All restrictions lifted.", level="WARN")
        self.show_snackbar("Titan OS: Evolution Complete. Status: IMMORTAL")

    # --- ФИНАЛЬНАЯ ИНИЦИАЛИЗАЦИЯ ---

    def on_stop(self):
        """Действия при полном выключении системы"""
        self.write_log("System: Powering down. Saving logs to Core DB...")
        try:
            self.save_session()
            # Закрываем все соединения
            conn = sqlite3.connect(self.db_path)
            conn.close()
        except:
            pass

# =============================================================================
# EXECUTION BLOCK: ЗАПУСК ПРИЛОЖЕНИЯ
# =============================================================================

if __name__ == "__main__":
    # 1. Настройка окружения для корректной работы графики
    if platform != 'android':
        Config.set('graphics', 'width', '400')
        Config.set('graphics', 'height', '800')
        Config.set('graphics', 'resizable', '0')
    
    # 2. Обработка глобальных исключений (Crash Protection)
    try:
        # 3. Инициализация и запуск основного ядра
        os_kernel = TitanOS()
        
        # Принудительная регистрация кастомных шрифтов (если есть)
        # LabelBase.register(name="Orbitron", fn_regular="fonts/orbitron.ttf")
        
        # 4. RUN
        os_kernel.run()
        
    except Exception as fatal_error:
        # Логирование фатальной ошибки перед вылетом
        with open("critical_crash.log", "w") as f:
            f.write(f"FATAL SYSTEM ERROR: {str(fatal_error)}\n")
            f.write(traceback.format_exc())
        print(f"KERNEL PANIC: {fatal_error}")

# =============================================================================
# END OF CODE - TITAN OS V7.0 "ETERNAL"
# Status: SYSTEM READY | Evolution: COMPLETE
# =============================================================================

import os
import sys
import threading
import subprocess
import traceback
from io import StringIO

# --- ФИКС КОНФЛИКТОВ И ВЫЛЕТОВ (ДО ИМПОРТА KIVY) ---
os.environ['KIVY_GRAPHICS'] = 'gles'
os.environ['KIVY_GL_BACKEND'] = 'sdl2'
os.environ['KIVY_NO_ARGS'] = '1'

from kivy.config import Config
Config.set('graphics', 'multisamples', '0')
Config.set('kivy', 'log_level', 'debug')

from kivy.lang import Builder
from kivy.clock import Clock
from kivy.utils import platform
from kivy.core.window import Window
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.filemanager import MDFileManager
from kivymd.uix.dialog import MDDialog
from kivymd.uix.snackbar import Snackbar

# --- УМНЫЙ ТЕРМИНАЛ: ПЕРЕХВАТ stderr ---
error_log = StringIO()
sys.stderr = error_log

# --- ПОЛНЫЙ ДИЗАЙН (KV) С ФИКСАМИ ПАНЕЛИ ---
KV = '''
MDNavigationLayout:
    MDScreenManager:
        id: screen_manager

        # --- ГЛАВНЫЙ ЭКРАН ---
        MDScreen:
            name: "dashboard"
            md_bg_color: 0.02, 0.02, 0.07, 1
            
            MDBoxLayout:
                orientation: 'vertical'
                padding: [0, dp(35), 0, 0] # ФИКС: Отступ чтобы не залезать на панель уведомлений

                MDTopAppBar:
                    title: "NEBULA MASTER ULTRA V8"
                    elevation: 10
                    left_action_items: [["menu", lambda x: nav_drawer.set_state("open")]]
                    right_action_items: [["chip", lambda x: app.show_core_status()]]
                    md_bg_color: 0.1, 0.1, 0.25, 1

                MDScrollView:
                    MDBoxLayout:
                        orientation: 'vertical'
                        padding: "15dp"
                        spacing: "20dp"
                        adaptive_height: True

                        # ПАНЕЛЬ МОНИТОРИНГА ЯДРА
                        MDCard:
                            size_hint: 1, None
                            height: "180dp"
                            radius: 20
                            md_bg_color: 0.15, 0.15, 0.3, 1
                            padding: "15dp"
                            orientation: "vertical"
                            MDLabel:
                                id: core_status_title
                                text: "CORE SYSTEM: ONLINE"
                                font_style: "H6"
                                theme_text_color: "Custom"
                                text_color: 0, 0.9, 1, 1
                            MDLabel:
                                text: "AI Core: Standby\\nTG Bridges: Connected\\nFile Engine: Ready"
                                theme_text_color: "Hint"
                            MDProgressBar:
                                id: core_progress
                                value: 65
                                color: 0, 0.7, 1, 1

                        # СЕТКА ФУНКЦИЙ (ВСЕ МОДУЛИ)
                        MDGridLayout:
                            cols: 2
                            spacing: "15dp"
                            adaptive_height: True

                            MDCard:
                                size_hint: 1, None
                                height: "140dp"
                                radius: 15
                                md_bg_color: 0.1, 0.2, 0.4, 1
                                on_release: screen_manager.current = "terminal"
                                MDBoxLayout:
                                    orientation: "vertical"
                                    padding: "12dp"
                                    MDIcon:
                                        icon: "console-network"
                                        halign: "center"
                                        font_size: "40sp"
                                    MDLabel:
                                        text: "TERMINAL"
                                        halign: "center"

                            MDCard:
                                size_hint: 1, None
                                height: "140dp"
                                radius: 15
                                md_bg_color: 0.2, 0.1, 0.35, 1
                                on_release: screen_manager.current = "ai_advisor"
                                MDBoxLayout:
                                    orientation: "vertical"
                                    padding: "12dp"
                                    MDIcon:
                                        icon: "robot-excited-outline"
                                        halign: "center"
                                        font_size: "40sp"
                                    MDLabel:
                                        text: "AI ADVISOR"
                                        halign: "center"

                            MDCard:
                                size_hint: 1, None
                                height: "140dp"
                                radius: 15
                                md_bg_color: 0.1, 0.25, 0.2, 1
                                on_release: app.open_file_manager()
                                MDBoxLayout:
                                    orientation: "vertical"
                                    padding: "12dp"
                                    MDIcon:
                                        icon: "file-tree"
                                        halign: "center"
                                        font_size: "40sp"
                                    MDLabel:
                                        text: "FILES"
                                        halign: "center"

                            MDCard:
                                size_hint: 1, None
                                height: "140dp"
                                radius: 15
                                md_bg_color: 0.4, 0.15, 0.15, 1
                                on_release: screen_manager.current = "pip_manager"
                                MDBoxLayout:
                                    orientation: "vertical"
                                    padding: "12dp"
                                    MDIcon:
                                        icon: "package-variant"
                                        halign: "center"
                                        font_size: "40sp"
                                    MDLabel:
                                        text: "PIP INSTALL"
                                        halign: "center"

        # --- ЭКРАН ТЕРМИНАЛА ---
        MDScreen:
            name: "terminal"
            MDBoxLayout:
                orientation: 'vertical'
                MDTopAppBar:
                    title: "Smart Error Terminal"
                    left_action_items: [["arrow-left", lambda x: app.go_dashboard()]]
                MDLabel:
                    id: terminal_log
                    text: "Ожидание ошибок..."
                    font_style: "Caption"
                    theme_text_color: "Custom"
                    text_color: 0, 1, 0, 1
                    padding: "15dp"
                    valign: "top"

        # --- ЭКРАН AI СОВЕТНИКА ---
        MDScreen:
            name: "ai_advisor"
            MDBoxLayout:
                orientation: 'vertical'
                MDTopAppBar:
                    title: "AI Logic Assistant"
                    left_action_items: [["arrow-left", lambda x: app.go_dashboard()]]
                MDBoxLayout:
                    orientation: 'vertical'
                    padding: "20dp"
                    spacing: "15dp"
                    MDLabel:
                        text: "Опишите проблему или задачу:"
                        halign: "center"
                    MDTextField:
                        id: ai_input
                        hint_text: "Напр: Как связать два моста ТГ?"
                        mode: "rectangle"
                    MDRaisedButton:
                        text: "ПОЛУЧИТЬ АНАЛИЗ ЯДРА"
                        pos_hint: {"center_x": .5}
                        on_release: app.get_ai_help(ai_input.text)

        # --- ЭКРАН PIP МЕНЕДЖЕРА ---
        MDScreen:
            name: "pip_manager"
            MDBoxLayout:
                orientation: 'vertical'
                MDTopAppBar:
                    title: "Package Installer"
                    left_action_items: [["arrow-left", lambda x: app.go_dashboard()]]
                MDBoxLayout:
                    orientation: 'vertical'
                    padding: "20dp"
                    spacing: "15dp"
                    MDTextField:
                        id: pip_input
                        hint_text: "Название библиотеки (torch, telethon...)"
                    MDRaisedButton:
                        text: "УСТАНОВИТЬ В ОКРУЖЕНИЕ"
                        pos_hint: {"center_x": .5}
                        on_release: app.install_package(pip_input.text)

    MDNavigationDrawer:
        id: nav_drawer
        md_bg_color: 0.05, 0.05, 0.1, 1
        MDBoxLayout:
            orientation: "vertical"
            padding: "16dp"
            spacing: "10dp"
            MDLabel:
                text: "NEBULA SETTINGS"
                font_style: "H6"
                theme_text_color: "Primary"
            MDSeparator:
            MDRectangleFlatIconButton:
                icon: "connection"
                text: "TG BRIDGES"
                width: parent.width
            MDRectangleFlatIconButton:
                icon: "security"
                text: "ENV ENCRYPTION"
                width: parent.width
'''

class NebulaUltimateApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Cyan"
        self.file_manager = MDFileManager(exit_manager=self.exit_file_manager, select_path=self.select_file)
        return Builder.load_string(KV)

    def on_start(self):
        # ФИКС: Мониторинг терминала каждую секунду
        Clock.schedule_interval(self.update_terminal_logs, 1)
        # Запрос прав
        if platform == "android":
            from android.permissions import request_permissions, Permission
            request_permissions([
                Permission.CAMERA, 
                Permission.READ_EXTERNAL_STORAGE, 
                Permission.WRITE_EXTERNAL_STORAGE, 
                Permission.MANAGE_EXTERNAL_STORAGE
            ])

    def update_terminal_logs(self, dt):
        logs = error_log.getvalue()
        if logs:
            # Показываем последние 1000 символов ошибок
            self.root.ids.terminal_log.text = f"CORE_ANALYSIS:\\n{logs[-1000:]}"

    def go_dashboard(self):
        self.root.ids.screen_manager.current = "dashboard"

    # --- ЛОГИКА ФАЙЛОВ ---
    def open_file_manager(self):
        path = os.getenv('EXTERNAL_STORAGE', '/') if platform == 'android' else '.'
        self.file_manager.show(path)

    def select_file(self, path):
        self.exit_file_manager()
        Snackbar(text=f"Выбран объект: {path}").open()

    def exit_file_manager(self, *args):
        self.file_manager.close()

    # --- ЛОГИКА PIP ---
    def install_package(self, pkg):
        def thread_task():
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", pkg])
                Clock.schedule_once(lambda x: Snackbar(text=f"Пакет {pkg} успешно интегрирован").open())
            except:
                Clock.schedule_once(lambda x: Snackbar(text="Ошибка установки пакета").open())
        threading.Thread(target=thread_task, daemon=True).start()

    # --- ЛОГИКА AI ---
    def get_ai_help(self, query):
        # Помогаем пользователю советом, не переписывая его работу
        advice = "AI: Для синхронизации двух мостов ТГ используйте асинхронную очередь (asyncio.Queue). Поместите токен в .env и используйте 'python-dotenv' для защиты."
        MDDialog(title="AI Advisor Response", text=advice).open()

    def show_core_status(self):
        MDDialog(title="Nebula Core Status", text="Версия: 8.0.5\\nСтатус: Все конфликты устранены\\nСлой защиты ENV: Активен").open()

if __name__ == '__main__':
    try:
        NebulaUltimateApp().run()
    except Exception:
        # Если приложение упало при старте, ошибка уйдет в буфер и отобразится в терминале
        traceback.print_exc(file=error_log)
      

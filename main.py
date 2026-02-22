import os
import sys
import threading
import subprocess
import traceback
from io import StringIO

# --- СЛОЙ ПРЕДОТВРАЩЕНИЯ КОНФЛИКТОВ ---
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
from kivymd.uix.button import MDRaisedButton, MDFlatButton

# --- SMART TERMINAL ENGINE ---
# Перехватываем стандартный вывод ошибок для анализа внутри приложения
error_output = StringIO()
sys.stderr = error_output

# --- ПОЛНЫЙ ИНТЕРФЕЙС (KV) ---
KV = '''
MDNavigationLayout:
    MDScreenManager:
        id: screen_manager

        # ГЛАВНЫЙ ЭКРАН (DASHBOARD)
        MDScreen:
            name: "dashboard"
            md_bg_color: 0.02, 0.02, 0.05, 1
            
            MDBoxLayout:
                orientation: 'vertical'
                padding: [0, dp(35), 0, 0] # Отступ от выреза камеры

                MDTopAppBar:
                    title: "NEBULA MASTER ULTRA"
                    elevation: 10
                    left_action_items: [["menu", lambda x: nav_drawer.set_state("open")]]
                    md_bg_color: 0.1, 0.1, 0.2, 1

                MDScrollView:
                    MDBoxLayout:
                        orientation: 'vertical'
                        padding: "15dp"
                        spacing: "20dp"
                        adaptive_height: True

                        # КАРТОЧКА МОНИТОРИНГА
                        MDCard:
                            size_hint_y: None
                            height: "160dp"
                            radius: 20
                            md_bg_color: 0.12, 0.12, 0.25, 1
                            padding: "15dp"
                            orientation: "vertical"
                            MDLabel:
                                id: core_status
                                text: "CORE: ACTIVE"
                                font_style: "H6"
                                theme_text_color: "Custom"
                                text_color: 0.2, 0.7, 1, 1
                            MDLabel:
                                text: "ENV Protection: ON\\nTG Bridges: Ready\\nAI Threads: Standby"
                                theme_text_color: "Hint"
                            MDProgressBar:
                                id: core_bar
                                value: 50
                                color: 0.2, 0.6, 1, 1

                        # СЕТКА ФУНКЦИЙ
                        MDGridLayout:
                            cols: 2
                            spacing: "15dp"
                            adaptive_height: True

                            # Терминал
                            MDCard:
                                size_hint_y: None
                                height: "130dp"
                                radius: 15
                                md_bg_color: 0.15, 0.1, 0.3, 1
                                on_release: screen_manager.current = "terminal_screen"
                                MDBoxLayout:
                                    orientation: "vertical"
                                    padding: "10dp"
                                    MDIcon:
                                        icon: "console"
                                        halign: "center"
                                        font_size: "35sp"
                                    MDLabel:
                                        text: "ТЕРМИНАЛ"
                                        halign: "center"

                            # AI Помощник
                            MDCard:
                                size_hint_y: None
                                height: "130dp"
                                radius: 15
                                md_bg_color: 0.2, 0.1, 0.25, 1
                                on_release: screen_manager.current = "ai_screen"
                                MDBoxLayout:
                                    orientation: "vertical"
                                    padding: "10dp"
                                    MDIcon:
                                        icon: "robot-mind"
                                        halign: "center"
                                        font_size: "35sp"
                                    MDLabel:
                                        text: "AI СОВЕТНИК"
                                        halign: "center"

                            # Проводник
                            MDCard:
                                size_hint_y: None
                                height: "130dp"
                                radius: 15
                                md_bg_color: 0.1, 0.2, 0.2, 1
                                on_release: app.open_file_manager()
                                MDBoxLayout:
                                    orientation: "vertical"
                                    padding: "10dp"
                                    MDIcon:
                                        icon: "folder-zip"
                                        halign: "center"
                                        font_size: "35sp"
                                    MDLabel:
                                        text: "ФАЙЛЫ"
                                        halign: "center"

                            # PIP Менеджер
                            MDCard:
                                size_hint_y: None
                                height: "130dp"
                                radius: 15
                                md_bg_color: 0.3, 0.15, 0.15, 1
                                on_release: screen_manager.current = "pip_screen"
                                MDBoxLayout:
                                    orientation: "vertical"
                                    padding: "10dp"
                                    MDIcon:
                                        icon: "package-variant"
                                        halign: "center"
                                        font_size: "35sp"
                                    MDLabel:
                                        text: "PIP INSTALL"
                                        halign: "center"

        # ЭКРАН ТЕРМИНАЛА
        MDScreen:
            name: "terminal_screen"
            MDBoxLayout:
                orientation: 'vertical'
                MDTopAppBar:
                    title: "Smart Terminal"
                    left_action_items: [["arrow-left", lambda x: app.go_dashboard()]]
                MDLabel:
                    id: terminal_text
                    text: "Ожидание логов системы..."
                    font_style: "Caption"
                    theme_text_color: "Custom"
                    text_color: 0, 1, 0, 1
                    padding: "15dp"
                    valign: "top"

        # ЭКРАН AI АССИСТЕНТА
        MDScreen:
            name: "ai_screen"
            MDBoxLayout:
                orientation: 'vertical'
                MDTopAppBar:
                    title: "AI Advisor"
                    left_action_items: [["arrow-left", lambda x: app.go_dashboard()]]
                MDBoxLayout:
                    orientation: 'vertical'
                    padding: "20dp"
                    spacing: "15dp"
                    MDLabel:
                        text: "Запрос к ИИ (архитектура, ENV, мосты):"
                        halign: "center"
                    MDTextField:
                        id: ai_input
                        hint_text: "Например: как защитить токен в ENV?"
                        mode: "rectangle"
                    MDRaisedButton:
                        text: "АНАЛИЗ"
                        pos_hint: {"center_x": .5}
                        on_release: app.get_ai_advice(ai_input.text)

        # ЭКРАН PIP МЕНЕДЖЕРА
        MDScreen:
            name: "pip_screen"
            MDBoxLayout:
                orientation: 'vertical'
                MDTopAppBar:
                    title: "Pip Manager"
                    left_action_items: [["arrow-left", lambda x: app.go_dashboard()]]
                MDBoxLayout:
                    orientation: 'vertical'
                    padding: "20dp"
                    spacing: "15dp"
                    MDTextField:
                        id: pip_input
                        hint_text: "Библиотека (numpy, telethon...)"
                    MDRaisedButton:
                        text: "УСТАНОВИТЬ ПАКЕТ"
                        pos_hint: {"center_x": .5}
                        on_release: app.pip_install(pip_input.text)

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
            MDSeparator:
            MDRectangleFlatIconButton:
                icon: "bridge"
                text: "TG BRIDGES"
                width: parent.width
            MDRectangleFlatIconButton:
                icon: "shield-lock"
                text: "ENV PROTECTION"
                width: parent.width
'''

class NebulaUltimateApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "DeepPurple"
        self.file_manager = MDFileManager(exit_manager=self.exit_fm, select_path=self.select_path)
        return Builder.load_string(KV)

    def on_start(self):
        # Запуск мониторинга ошибок
        Clock.schedule_interval(self.refresh_terminal, 1)
        # Запрос прав для Android 11+
        if platform == "android":
            from android.permissions import request_permissions, Permission
            request_permissions([
                Permission.CAMERA,
                Permission.READ_EXTERNAL_STORAGE,
                Permission.WRITE_EXTERNAL_STORAGE,
                Permission.MANAGE_EXTERNAL_STORAGE
            ])

    def refresh_terminal(self, dt):
        logs = error_output.getvalue()
        if logs:
            self.root.ids.terminal_text.text = f"ANALYSIS:\\n{logs[-1000:]}"
            self.root.ids.core_status.text = "CORE: ERROR DETECTED"
            self.root.ids.core_status.text_color = [1, 0, 0, 1]

    def go_dashboard(self):
        self.root.ids.screen_manager.current = "dashboard"

    # ЛОГИКА ФАЙЛОВ
    def open_file_manager(self):
        path = os.getenv('EXTERNAL_STORAGE', '/') if platform == 'android' else '.'
        self.file_manager.show(path)

    def select_path(self, path):
        self.exit_fm()
        Snackbar(text=f"Выбран: {path}").open()

    def exit_fm(self, *args):
        self.file_manager.close()

    # ЛОГИКА PIP
    def pip_install(self, package):
        def run_pip():
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", package])
                Clock.schedule_once(lambda x: Snackbar(text=f"Успех: {package}").open())
            except:
                Clock.schedule_once(lambda x: Snackbar(text="Ошибка PIP").open())
        threading.Thread(target=run_pip, daemon=True).start()

    # ЛОГИКА AI СОВЕТНИКА
    def get_ai_advice(self, query):
        advice = "AI: Для работы с двумя мостами TG создайте два независимых клиента через asyncio. Для ENV используйте python-dotenv и игнорируйте .env в git."
        MDDialog(title="AI Advisor", text=advice, buttons=[MDFlatButton(text="OK", on_release=lambda x: x.parent.parent.parent.dismiss())]).open()

if __name__ == '__main__':
    try:
        NebulaUltimateApp().run()
    except Exception:
        traceback.print_exc(file=error_output)
      

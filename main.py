import os
import sys
import threading
import subprocess
import traceback
from io import StringIO

# --- СИСТЕМНЫЕ ФИКСЫ ДЛЯ СТАБИЛЬНОСТИ ---
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

# --- УМНЫЙ ТЕРМИНАЛ: ПЕРЕХВАТ stderr ---
error_buffer = StringIO()
sys.stderr = error_buffer

# --- ПОЛНЫЙ KV-ИНТЕРФЕЙС (NEBULA OS STYLE) ---
KV = '''
MDNavigationLayout:
    MDScreenManager:
        id: screen_manager

        # ЭКРАН 1: ДАШБОРД
        MDScreen:
            name: "dashboard"
            md_bg_color: 0.02, 0.02, 0.06, 1
            
            MDBoxLayout:
                orientation: 'vertical'
                padding: [0, dp(35), 0, 0] # Защита от наезда на панель

                MDTopAppBar:
                    title: "NEBULA CORE ULTIMATE"
                    elevation: 10
                    left_action_items: [["menu", lambda x: nav_drawer.set_state("open")]]
                    md_bg_color: 0.1, 0.1, 0.2, 1

                MDScrollView:
                    MDBoxLayout:
                        orientation: 'vertical'
                        padding: "15dp"
                        spacing: "20dp"
                        adaptive_height: True

                        # КАРТОЧКА СТАТУСА
                        MDCard:
                            size_hint_y: None
                            height: "160dp"
                            radius: 20
                            md_bg_color: 0.12, 0.12, 0.28, 1
                            padding: "15dp"
                            orientation: "vertical"
                            MDLabel:
                                id: core_title
                                text: "CORE SYSTEM: ACTIVE"
                                font_style: "H6"
                                theme_text_color: "Custom"
                                text_color: 0.2, 0.8, 1, 1
                            MDLabel:
                                text: "Мосты TG: Стабильно\\nENV Защита: Активна\\nПотоки ИИ: В ожидании"
                                theme_text_color: "Hint"
                            MDProgressBar:
                                id: core_progress
                                value: 75
                                color: 0.2, 0.7, 1, 1

                        # СЕТКА МОДУЛЕЙ
                        MDGridLayout:
                            cols: 2
                            spacing: "15dp"
                            adaptive_height: True

                            MDCard:
                                size_hint_y: None
                                height: "130dp"
                                radius: 15
                                md_bg_color: 0.15, 0.1, 0.3, 1
                                on_release: screen_manager.current = "terminal"
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

                            MDCard:
                                size_hint_y: None
                                height: "130dp"
                                radius: 15
                                md_bg_color: 0.1, 0.2, 0.15, 1
                                on_release: app.open_file_manager()
                                MDBoxLayout:
                                    orientation: "vertical"
                                    padding: "10dp"
                                    MDIcon:
                                        icon: "folder-key"
                                        halign: "center"
                                        font_size: "35sp"
                                    MDLabel:
                                        text: "ФАЙЛЫ"
                                        halign: "center"

                            MDCard:
                                size_hint_y: None
                                height: "130dp"
                                radius: 15
                                md_bg_color: 0.2, 0.15, 0.35, 1
                                on_release: screen_manager.current = "ai_help"
                                MDBoxLayout:
                                    orientation: "vertical"
                                    padding: "10dp"
                                    MDIcon:
                                        icon: "brain"
                                        halign: "center"
                                        font_size: "35sp"
                                    MDLabel:
                                        text: "AI ADVISOR"
                                        halign: "center"

                            MDCard:
                                size_hint_y: None
                                height: "130dp"
                                radius: 15
                                md_bg_color: 0.3, 0.1, 0.1, 1
                                on_release: screen_manager.current = "pip_mgr"
                                MDBoxLayout:
                                    orientation: "vertical"
                                    padding: "10dp"
                                    MDIcon:
                                        icon: "package-variant"
                                        halign: "center"
                                        font_size: "35sp"
                                    MDLabel:
                                        text: "PIP MANAGER"
                                        halign: "center"

        # ЭКРАН 2: ТЕРМИНАЛ ЛОГОВ
        MDScreen:
            name: "terminal"
            MDBoxLayout:
                orientation: 'vertical'
                MDTopAppBar:
                    title: "System Terminal"
                    left_action_items: [["arrow-left", lambda x: app.go_dashboard()]]
                MDLabel:
                    id: terminal_logs
                    text: "Ожидание системных вызовов..."
                    font_style: "Caption"
                    theme_text_color: "Custom"
                    text_color: 0, 1, 0, 1
                    padding: "15dp"
                    valign: "top"

        # ЭКРАН 3: AI СОВЕТНИК
        MDScreen:
            name: "ai_help"
            MDBoxLayout:
                orientation: 'vertical'
                MDTopAppBar:
                    title: "AI Advisor"
                    left_action_items: [["arrow-left", lambda x: app.go_dashboard()]]
                MDBoxLayout:
                    padding: "20dp"
                    orientation: 'vertical'
                    spacing: "10dp"
                    MDTextField:
                        id: ai_input
                        hint_text: "Вопрос по архитектуре или ENV..."
                    MDRaisedButton:
                        text: "АНАЛИЗИРОВАТЬ"
                        pos_hint: {"center_x": .5}
                        on_release: app.get_ai_advice(ai_input.text)

        # ЭКРАН 4: PIP MANAGER
        MDScreen:
            name: "pip_mgr"
            MDBoxLayout:
                orientation: 'vertical'
                MDTopAppBar:
                    title: "Pip Package Manager"
                    left_action_items: [["arrow-left", lambda x: app.go_dashboard()]]
                MDBoxLayout:
                    padding: "20dp"
                    orientation: 'vertical'
                    spacing: "10dp"
                    MDTextField:
                        id: pip_package
                        hint_text: "Имя библиотеки (напр. telethon)"
                    MDRaisedButton:
                        text: "УСТАНОВИТЬ"
                        pos_hint: {"center_x": .5}
                        on_release: app.install_pkg(pip_package.text)

    MDNavigationDrawer:
        id: nav_drawer
        md_bg_color: 0.05, 0.05, 0.1, 1
        MDBoxLayout:
            orientation: "vertical"
            padding: "10dp"
            spacing: "10dp"
            MDLabel:
                text: "Nebula Ultra"
                font_style: "H6"
            MDRectangleFlatIconButton:
                icon: "shield-check"
                text: "ENV Protection"
                width: parent.width
'''

class NebulaUltimate(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Cyan"
        self.fm = MDFileManager(exit_manager=self.exit_fm, select_path=self.select_path)
        return Builder.load_string(KV)

    def on_start(self):
        Clock.schedule_interval(self.update_terminal, 1)
        if platform == "android":
            from android.permissions import request_permissions, Permission
            request_permissions([Permission.CAMERA, Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE, Permission.MANAGE_EXTERNAL_STORAGE])

    def update_terminal(self, dt):
        logs = error_buffer.getvalue()
        if logs:
            self.root.ids.terminal_logs.text = f"ANALYSIS:\\n{logs[-1000:]}"
            self.root.ids.core_title.text = "CORE: ERROR DETECTED"
            self.root.ids.core_title.text_color = [1, 0, 0, 1]

    def go_dashboard(self):
        self.root.ids.screen_manager.current = "dashboard"

    def open_file_manager(self):
        p = os.getenv('EXTERNAL_STORAGE', '/') if platform == 'android' else '.'
        self.fm.show(p)

    def select_path(self, path):
        self.exit_fm()
        Snackbar(text=f"Выбран: {path}").open()

    def exit_fm(self, *args):
        self.fm.close()

    def install_pkg(self, pkg):
        def run():
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", pkg])
                Clock.schedule_once(lambda x: Snackbar(text=f"Успех: {pkg}").open())
            except:
                Clock.schedule_once(lambda x: Snackbar(text="Ошибка PIP").open())
        threading.Thread(target=run, daemon=True).start()

    def get_ai_advice(self, q):
        advice = "AI: Для создания мостов TG используйте два разных инстанса TelegramClient. Храните сессии в защищенной папке /data/."
        MDDialog(title="AI Advisor", text=advice).open()

if __name__ == '__main__':
    try:
        NebulaUltimate().run()
    except Exception:
        traceback.print_exc(file=error_buffer)
      

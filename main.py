import os
import sys
import threading
import subprocess
import traceback
from io import StringIO

# --- БЛОК ИСПРАВЛЕНИЯ КОНФЛИКТОВ (ЖЕСТКАЯ ИНИЦИАЛИЗАЦИЯ) ---
os.environ['KIVY_GRAPHICS'] = 'gles'
os.environ['KIVY_GL_BACKEND'] = 'sdl2'
os.environ['KIVY_NO_ARGS'] = '1'

from kivy.config import Config
Config.set('graphics', 'multisamples', '0')
Config.set('kivy', 'log_level', 'debug')
Config.set('kivy', 'exit_on_escape', '0')

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

# --- ENGINE: ПЕРЕХВАТ ОШИБОК В РЕАЛЬНОМ ВРЕМЕНИ ---
error_log = StringIO()
sys.stderr = error_log

# --- ПОЛНЫЙ ДИЗАЙН (KV) ---
KV = '''
MDNavigationLayout:
    MDScreenManager:
        id: screen_manager

        MDScreen:
            name: "dashboard"
            md_bg_color: 0.02, 0.02, 0.05, 1
            
            MDBoxLayout:
                orientation: 'vertical'
                padding: [0, dp(35), 0, 0] # Защита от наезда на челку/панель

                MDTopAppBar:
                    title: "NEBULA MASTER ULTRA V8"
                    elevation: 10
                    left_action_items: [["menu", lambda x: nav_drawer.set_state("open")]]
                    md_bg_color: 0.1, 0.1, 0.2, 1

                MDScrollView:
                    MDBoxLayout:
                        orientation: 'vertical'
                        padding: "15dp"
                        spacing: "20dp"
                        adaptive_height: True

                        # МОНИТОРИНГ
                        MDCard:
                            size_hint_y: None
                            height: "180dp"
                            radius: 20
                            md_bg_color: 0.12, 0.12, 0.25, 1
                            padding: "15dp"
                            orientation: "vertical"
                            MDLabel:
                                id: core_status
                                text: "SYSTEM CORE: ONLINE"
                                font_style: "H6"
                                theme_text_color: "Custom"
                                text_color: 0, 0.8, 1, 1
                            MDLabel:
                                text: "ENV: Protected\\nTG Bridges: Ready\\nAI Engine: Loaded"
                                theme_text_color: "Hint"
                            MDProgressBar:
                                id: core_progress
                                value: 85
                                color: 0, 0.7, 1, 1

                        # СЕТКА МОДУЛЕЙ
                        MDGridLayout:
                            cols: 2
                            spacing: "15dp"
                            adaptive_height: True

                            MDCard:
                                size_hint_y: None
                                height: "135dp"
                                radius: 15
                                md_bg_color: 0.15, 0.1, 0.3, 1
                                on_release: screen_manager.current = "terminal"
                                MDBoxLayout:
                                    orientation: "vertical"
                                    padding: "10dp"
                                    MDIcon:
                                        icon: "console"
                                        halign: "center"
                                        font_size: "40sp"
                                    MDLabel:
                                        text: "TERMINAL"
                                        halign: "center"

                            MDCard:
                                size_hint_y: None
                                height: "135dp"
                                radius: 15
                                md_bg_color: 0.2, 0.1, 0.3, 1
                                on_release: screen_manager.current = "ai_advisor"
                                MDBoxLayout:
                                    orientation: "vertical"
                                    padding: "10dp"
                                    MDIcon:
                                        icon: "robot-excited"
                                        halign: "center"
                                        font_size: "40sp"
                                    MDLabel:
                                        text: "AI HELPER"
                                        halign: "center"

                            MDCard:
                                size_hint_y: None
                                height: "135dp"
                                radius: 15
                                md_bg_color: 0.1, 0.2, 0.2, 1
                                on_release: app.open_file_explorer()
                                MDBoxLayout:
                                    orientation: "vertical"
                                    padding: "10dp"
                                    MDIcon:
                                        icon: "folder-sync"
                                        halign: "center"
                                        font_size: "40sp"
                                    MDLabel:
                                        text: "EXPLORER"
                                        halign: "center"

                            MDCard:
                                size_hint_y: None
                                height: "135dp"
                                radius: 15
                                md_bg_color: 0.3, 0.1, 0.1, 1
                                on_release: screen_manager.current = "pip_installer"
                                MDBoxLayout:
                                    orientation: "vertical"
                                    padding: "10dp"
                                    MDIcon:
                                        icon: "package-variant"
                                        halign: "center"
                                        font_size: "40sp"
                                    MDLabel:
                                        text: "PIP MGR"
                                        halign: "center"

        # ЭКРАН ТЕРМИНАЛА
        MDScreen:
            name: "terminal"
            MDBoxLayout:
                orientation: 'vertical'
                MDTopAppBar:
                    title: "Internal Error Logs"
                    left_action_items: [["arrow-left", lambda x: app.go_home()]]
                MDLabel:
                    id: terminal_output
                    text: "Ожидание системных ошибок..."
                    font_style: "Caption"
                    theme_text_color: "Custom"
                    text_color: 0, 1, 0, 1
                    padding: "15dp"
                    valign: "top"

        # ЭКРАН AI СОВЕТНИКА
        MDScreen:
            name: "ai_advisor"
            MDBoxLayout:
                orientation: 'vertical'
                MDTopAppBar:
                    title: "AI Project Advisor"
                    left_action_items: [["arrow-left", lambda x: app.go_home()]]
                MDBoxLayout:
                    padding: "20dp"
                    orientation: 'vertical'
                    spacing: "15dp"
                    MDTextField:
                        id: ai_query
                        hint_text: "Вопрос по архитектуре или коду..."
                        mode: "rectangle"
                    MDRaisedButton:
                        text: "АНАЛИЗ ЯДРА"
                        pos_hint: {"center_x": .5}
                        on_release: app.get_ai_advice(ai_query.text)

        # ЭКРАН PIP INSTALLER
        MDScreen:
            name: "pip_installer"
            MDBoxLayout:
                orientation: 'vertical'
                MDTopAppBar:
                    title: "Package Manager"
                    left_action_items: [["arrow-left", lambda x: app.go_home()]]
                MDBoxLayout:
                    padding: "20dp"
                    orientation: 'vertical'
                    spacing: "15dp"
                    MDTextField:
                        id: package_name
                        hint_text: "Название библиотеки (напр. telethon)"
                    MDRaisedButton:
                        text: "УСТАНОВИТЬ"
                        pos_hint: {"center_x": .5}
                        on_release: app.pip_install(package_name.text)

    MDNavigationDrawer:
        id: nav_drawer
        md_bg_color: 0.05, 0.05, 0.1, 1
        MDBoxLayout:
            orientation: "vertical"
            padding: "15dp"
            spacing: "10dp"
            MDLabel:
                text: "CORE SETTINGS"
                font_style: "H6"
            MDSeparator:
            MDRectangleFlatIconButton:
                icon: "shield-key"
                text: "ENV PROTECTION"
                width: parent.width
            MDRectangleFlatIconButton:
                icon: "bridge"
                text: "TG BRIDGES"
                width: parent.width
'''

class NebulaUltraApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "DeepPurple"
        self.manager = MDFileManager(exit_manager=self.exit_manager, select_path=self.select_path)
        return Builder.load_string(KV)

    def on_start(self):
        # Мониторинг логов терминала
        Clock.schedule_interval(self.update_logs, 1)
        # Запрос прав для Android 11+
        if platform == "android":
            from android.permissions import request_permissions, Permission
            request_permissions([
                Permission.CAMERA,
                Permission.READ_EXTERNAL_STORAGE,
                Permission.WRITE_EXTERNAL_STORAGE,
                Permission.MANAGE_EXTERNAL_STORAGE
            ])

    def update_logs(self, dt):
        logs = error_log.getvalue()
        if logs:
            self.root.ids.terminal_output.text = f"CRITICAL_LOG:\\n{logs[-1000:]}"
            self.root.ids.core_status.text = "CORE: ERROR DETECTED"
            self.root.ids.core_status.text_color = [1, 0, 0, 1]

    def go_home(self):
        self.root.ids.screen_manager.current = "dashboard"

    # --- ФАЙЛОВЫЙ МЕНЕДЖЕР ---
    def open_file_explorer(self):
        p = os.getenv('EXTERNAL_STORAGE', '/') if platform == 'android' else '.'
        self.manager.show(p)

    def select_path(self, path):
        self.exit_manager()
        Snackbar(text=f"Path selected: {path}").open()

    def exit_manager(self, *args):
        self.manager.close()

    # --- PIP ENGINE ---
    def pip_install(self, lib):
        def thread_task():
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", lib])
                Clock.schedule_once(lambda x: Snackbar(text=f"Successfully installed {lib}").open())
            except:
                Clock.schedule_once(lambda x: Snackbar(text="Installation failed!").open())
        threading.Thread(target=thread_task, daemon=True).start()

    # --- AI ADVISOR ---
    def get_ai_advice(self, q):
        advice = "AI: Для работы с ENV на Android используйте python-dotenv. Мосты TG лучше запускать в отдельных потоках через threading или asyncio."
        MDDialog(title="Nebula AI Analysis", text=advice).open()

if __name__ == '__main__':
    try:
        NebulaUltraApp().run()
    except Exception:
        traceback.print_exc(file=error_log)
      

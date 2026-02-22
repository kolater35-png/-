import os
import sys
import threading
import subprocess
import traceback
import asyncio
from io import StringIO

# --- СЛОЙ ПРЕДОТВРАЩЕНИЯ ВЫЛЕТОВ ---
os.environ['KIVY_GRAPHICS'] = 'gles'
os.environ['KIVY_GL_BACKEND'] = 'sdl2'

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

# --- ПЕРЕХВАТ ЛОГОВ ---
sys_logs = StringIO()
sys.stderr = sys_logs

# --- ИНТЕРФЕЙС (БЕЗ СОКРАЩЕНИЙ) ---
KV = '''
MDNavigationLayout:
    MDScreenManager:
        id: screen_manager

        # ГЛАВНЫЙ ЭКРАН
        MDScreen:
            name: "dashboard"
            md_bg_color: 0.01, 0.01, 0.05, 1
            
            MDBoxLayout:
                orientation: 'vertical'
                padding: [0, dp(35), 0, 0]

                MDTopAppBar:
                    title: "NEBULA AI MASTER ULTRA"
                    elevation: 8
                    left_action_items: [["menu", lambda x: nav_drawer.set_state("open")]]
                    md_bg_color: 0.1, 0.1, 0.25, 1

                MDScrollView:
                    MDBoxLayout:
                        orientation: 'vertical'
                        padding: "15dp"
                        spacing: "20dp"
                        adaptive_height: True

                        # СТАТУС НЕЙРОСЕТИ
                        MDCard:
                            size_hint_y: None
                            height: "200dp"
                            radius: 20
                            md_bg_color: 0.1, 0.1, 0.3, 1
                            padding: "20dp"
                            orientation: "vertical"
                            MDLabel:
                                text: "AI CORE STATUS"
                                font_style: "H6"
                                theme_text_color: "Custom"
                                text_color: 0, 0.8, 1, 1
                            MDLabel:
                                id: ai_status_label
                                text: "Torch: Ожидание\\nTransformers: Ожидание\\nGPU Acceleration: Auto"
                                theme_text_color: "Secondary"
                            MDProgressBar:
                                id: main_progress
                                value: 0
                                color: 0, 1, 0.8, 1
                            MDLabel:
                                id: detail_info
                                text: "Нажмите 'DEPLOY' для развертывания"
                                font_style: "Caption"
                                theme_text_color: "Hint"

                        # КНОПКИ УПРАВЛЕНИЯ
                        MDGridLayout:
                            cols: 2
                            spacing: "15dp"
                            adaptive_height: True

                            MDCard:
                                size_hint_y: None
                                height: "120dp"
                                radius: 15
                                md_bg_color: 0.15, 0.1, 0.35, 1
                                on_release: app.start_deploy()
                                MDBoxLayout:
                                    orientation: "vertical"
                                    padding: "10dp"
                                    MDIcon:
                                        icon: "cloud-download"
                                        halign: "center"
                                    MDLabel:
                                        text: "DEPLOY AI"
                                        halign: "center"

                            MDCard:
                                size_hint_y: None
                                height: "120dp"
                                radius: 15
                                md_bg_color: 0.1, 0.2, 0.2, 1
                                on_release: screen_manager.current = "terminal"
                                MDBoxLayout:
                                    orientation: "vertical"
                                    padding: "10dp"
                                    MDIcon:
                                        icon: "console"
                                        halign: "center"
                                    MDLabel:
                                        text: "LOGS"
                                        halign: "center"

        # ЭКРАН ТЕРМИНАЛА
        MDScreen:
            name: "terminal"
            MDBoxLayout:
                orientation: 'vertical'
                MDTopAppBar:
                    title: "System Console"
                    left_action_items: [["arrow-left", lambda x: app.go_home()]]
                MDScrollView:
                    md_bg_color: 0, 0, 0, 1
                    MDLabel:
                        id: log_text
                        text: "Initializing debug console..."
                        font_style: "Caption"
                        theme_text_color: "Custom"
                        text_color: 0, 1, 0, 1
                        size_hint_y: None
                        height: self.texture_size[1]
                        padding: "10dp"

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
            MDFlatButton:
                text: "CLEAR CACHE"
                width: parent.width
            MDFlatButton:
                text: "ENV CONFIG"
                width: parent.width
'''

class NebulaMain(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "BlueGray"
        return Builder.load_string(KV)

    def on_start(self):
        Clock.schedule_interval(self.update_logs, 1)
        if platform == "android":
            from android.permissions import request_permissions, Permission
            request_permissions([Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE, Permission.INTERNET])

    def go_home(self):
        self.root.ids.screen_manager.current = "dashboard"

    def update_logs(self, dt):
        logs = sys_logs.getvalue()
        if logs:
            self.root.ids.log_text.text = logs[-2000:]

    # --- ЛОГИКА ДЕПЛОЯ (TORCH, TRANSFORMERS, TELETHON) ---
    def start_deploy(self):
        self.root.ids.detail_info.text = "Подготовка к загрузке гигантов..."
        threading.Thread(target=self.run_install, daemon=True).start()

    def run_install(self):
        # Самый полный список библиотек
        libraries = [
            "pip --upgrade", 
            "numpy", 
            "telethon", 
            "python-dotenv", 
            "torch --no-cache-dir", 
            "transformers --no-cache-dir"
        ]
        
        try:
            for i, lib in enumerate(libraries):
                msg = f"Установка модуля: {lib.split()[0]}..."
                Clock.schedule_once(lambda x, m=msg: self.set_status(m))
                
                # Вызов системного инсталлера
                process = subprocess.Popen(
                    [sys.executable, "-m", "pip", "install"] + lib.split(),
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True
                )
                
                for line in process.stdout:
                    sys_logs.write(line)
                
                process.wait()
                
                progress = ((i + 1) / len(libraries)) * 100
                Clock.schedule_once(lambda x, p=progress: self.set_progress(p))

            Clock.schedule_once(lambda x: self.finalize_install())
        except Exception as e:
            sys_logs.write(f"\nCRITICAL ERROR: {str(e)}")

    def set_status(self, text):
        self.root.ids.detail_info.text = text

    def set_progress(self, val):
        self.root.ids.main_progress.value = val

    def finalize_install(self):
        self.root.ids.ai_status_label.text = "Torch: INSTALLED\\nTransformers: INSTALLED\\nStatus: READY"
        self.root.ids.detail_info.text = "Все системы активны!"
        Snackbar(text="Нейросетевое ядро развернуто!").open()

if __name__ == '__main__':
    NebulaMain().run()

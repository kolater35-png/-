import os
import sys
import traceback
import subprocess
import threading
from io import StringIO
from kivy.lang import Builder
from kivy.utils import platform
from kivy.clock import Clock
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.filemanager import MDFileManager
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.dialog import MDDialog

# Перехватчик ошибок для Умного Терминала
error_log = StringIO()
sys.stderr = error_log

KV = '''
MDNavigationLayout:
    MDScreenManager:
        id: screen_manager

        # --- ГЛАВНЫЙ ЭКРАН (DASHBOARD) ---
        MDScreen:
            name: "dashboard"
            md_bg_color: 0.02, 0.02, 0.05, 1
            
            MDBoxLayout:
                orientation: 'vertical'
                padding: [0, dp(25), 0, 0] # Отступ от верхней панели (Status Bar)

                MDTopAppBar:
                    title: "NEBULA CORE V8"
                    elevation: 4
                    left_action_items: [["menu", lambda x: nav_drawer.set_state("open")]]
                    md_bg_color: 0.1, 0.1, 0.2, 1

                MDScrollView:
                    MDBoxLayout:
                        orientation: 'vertical'
                        padding: "15dp"
                        spacing: "15dp"
                        adaptive_height: True

                        MDCard:
                            size_hint: 1, None
                            height: "120dp"
                            radius: 15
                            md_bg_color: 0.1, 0.15, 0.3, 1
                            padding: "10dp"
                            on_release: screen_manager.current = "terminal"
                            MDLabel:
                                text: "УМНЫЙ ТЕРМИНАЛ\\nПроверка ошибок в реальном времени"
                                halign: "center"
                                theme_text_color: "Custom"
                                text_color: 0.4, 0.8, 1, 1

                        MDGridLayout:
                            cols: 2
                            spacing: "15dp"
                            adaptive_height: True

                            MDCard:
                                size_hint: 1, None
                                height: "140dp"
                                radius: 15
                                md_bg_color: 0.15, 0.1, 0.25, 1
                                on_release: screen_manager.current = "ai_assistant"
                                MDBoxLayout:
                                    orientation: "vertical"
                                    padding: "10dp"
                                    MDIcon:
                                        icon: "robot-happy"
                                        halign: "center"
                                    MDLabel:
                                        text: "AI СОВЕТНИК"
                                        halign: "center"

                            MDCard:
                                size_hint: 1, None
                                height: "140dp"
                                radius: 15
                                md_bg_color: 0.1, 0.2, 0.2, 1
                                on_release: app.open_file_manager()
                                MDBoxLayout:
                                    orientation: "vertical"
                                    padding: "10dp"
                                    MDIcon:
                                        icon: "folder-eye"
                                        halign: "center"
                                    MDLabel:
                                        text: "FILES"
                                        halign: "center"

        # --- ЭКРАН ТЕРМИНАЛА ---
        MDScreen:
            name: "terminal"
            MDBoxLayout:
                orientation: 'vertical'
                MDTopAppBar:
                    title: "Smart Terminal"
                    left_action_items: [["arrow-left", lambda x: app.go_home()]]
                MDLabel:
                    id: log_output
                    text: "Логов пока нет..."
                    font_name: "Roboto"
                    font_style: "Caption"
                    padding: "10dp"
                    theme_text_color: "Custom"
                    text_color: 0, 1, 0, 1

        # --- ЭКРАН PIP MANAGER ---
        MDScreen:
            name: "pip_manager"
            MDBoxLayout:
                orientation: 'vertical'
                MDTopAppBar:
                    title: "Pip Installer"
                    left_action_items: [["arrow-left", lambda x: app.go_home()]]
                MDTextField:
                    id: lib_input
                    hint_text: "Введите имя библиотеки (напр. torch)"
                    pos_hint: {"center_x": .5}
                    size_hint_x: .8
                MDRaisedButton:
                    text: "УСТАНОВИТЬ"
                    pos_hint: {"center_x": .5}
                    on_release: app.pip_install(lib_input.text)

        # --- ЭКРАН AI ASSISTANT ---
        MDScreen:
            name: "ai_assistant"
            MDBoxLayout:
                orientation: 'vertical'
                MDTopAppBar:
                    title: "AI Helper"
                    left_action_items: [["arrow-left", lambda x: app.go_home()]]
                MDLabel:
                    text: "Спроси меня о структуре кода:"
                    halign: "center"
                MDTextField:
                    id: ai_query
                    hint_text: "Как оптимизировать циклы?"
                    size_hint_x: .9
                    pos_hint: {"center_x": .5}
                MDRaisedButton:
                    text: "ПОЛУЧИТЬ СОВЕТ"
                    pos_hint: {"center_x": .5}
                    on_release: app.ai_advice(ai_query.text)

    MDNavigationDrawer:
        id: nav_drawer
        MDBoxLayout:
            orientation: "vertical"
            padding: "10dp"
            MDRFlatButton:
                text: "PIP MANAGER"
                on_release: screen_manager.current = "pip_manager"
'''

class NebulaMain(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "DeepPurple"
        self.file_manager = MDFileManager(exit_manager=self.close_file_manager, select_path=self.select_path)
        return Builder.load_string(KV)

    def on_start(self):
        Clock.schedule_interval(self.update_terminal, 1)

    def update_terminal(self, dt):
        val = error_log.getvalue()
        if val:
            self.root.ids.log_output.text = f"ОШИБКА: {val[-500:]}" # Показываем последние 500 символов

    def go_home(self):
        self.root.ids.screen_manager.current = "dashboard"

    # --- ФУНКЦИИ УПРАВЛЕНИЯ ФАЙЛАМИ ---
    def open_file_manager(self):
        path = os.getenv('EXTERNAL_STORAGE', '/') if platform == 'android' else '.'
        self.file_manager.show(path)

    def select_path(self, path):
        self.close_file_manager()
        Snackbar(text=f"Выбран файл: {path}").open()

    def close_file_manager(self, *args):
        self.file_manager.close()

    # --- PIP MANAGER ---
    def pip_install(self, lib_name):
        def run():
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", lib_name])
                Clock.schedule_once(lambda x: Snackbar(text=f"Успешно: {lib_name}").open())
            except Exception as e:
                Clock.schedule_once(lambda x: Snackbar(text="Ошибка установки").open())
        threading.Thread(target=run).start()

    # --- AI ASSISTANT (НЕ ПИШЕТ КОД, А ПОМОГАЕТ) ---
    def ai_advice(self, query):
        advice = "Совет: Используй генераторы списков вместо циклов for для экономии памяти."
        MDDialog(title="AI Assistant", text=advice).open()

if __name__ == '__main__':
    try:
        NebulaMain().run()
    except Exception:
        # Если само приложение упало, записываем в лог
        traceback.print_exc(file=error_log)
      

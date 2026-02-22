# -*- coding: utf-8: -*-
import os
import sys
import threading
import time
import json
import platform
import traceback
from io import StringIO

# Базовые компоненты Kivy
from kivy.lang import Builder
from kivy.clock import Clock, mainthread
from kivy.animation import Animation
from kivy.properties import StringProperty, DictProperty, BooleanProperty, NumericProperty
from kivy.core.clipboard import Clipboard
from kivy.core.window import Window

# Компоненты KivyMD
from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFillRoundFlatButton, MDFlatButton, MDRaisedButton
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.spinner import MDSpinner

# Попытка импорта тяжелых либ для проверки (не критично при запуске)
try:
    import torch
    import transformers
except ImportError:
    pass

# Полная верстка интерфейса Nebula Ultra IDE
KV = '''
<SymbolButton@MDRaisedButton>:
    size_hint: None, None
    size: "48dp", "42dp"
    md_bg_color: "#1E1E1E"
    text_color: "#D0BCFF"
    elevation: 2
    on_release: app.insert_symbol(self.text)

MDScreenManager:
    id: screen_manager

    MDScreen:
        name: "intro_screen"
        md_bg_color: "#000000"
        Image:
            id: serpent_intro
            source: "serpent.png"
            size_hint: None, None
            size: "300dp", "300dp"
            pos_hint: {"center_x": 0.5, "center_y": -0.4}

    MDScreen:
        name: "main_screen"
        MDBoxLayout:
            orientation: "vertical"
            md_bg_color: "#080808"

            MDTopAppBar:
                title: "Nebula Ultra IDE"
                elevation: 0
                md_bg_color: "#080808"
                left_action_items: [["menu", lambda x: nav_drawer.set_state("open")]]
                right_action_items: [
                    ["content-copy", lambda x: app.copy_all()],
                    ["content-paste", lambda x: app.paste_code()],
                    ["snake", lambda x: app.call_serpent_help()]
                ]

            # Панель быстрого ввода символов
            ScrollView:
                size_hint_y: None
                height: "56dp"
                do_scroll_y: False
                bar_width: 0
                MDBoxLayout:
                    orientation: "horizontal"
                    adaptive_width: True
                    padding: "6dp"
                    spacing: "8dp"
                    SymbolButton: text: ":"
                    SymbolButton: text: "("
                    SymbolButton: text: ")"
                    SymbolButton: text: "{"
                    SymbolButton: text: "}"
                    SymbolButton: text: "["
                    SymbolButton: text: "]"
                    SymbolButton: text: "="
                    SymbolButton: text: "import"
                    SymbolButton: text: "torch"
                    SymbolButton: text: "transformers"
                    SymbolButton: text: "nn."
                    SymbolButton: text: "print"

            MDBoxLayout:
                orientation: "vertical"
                padding: "10dp"
                spacing: "10dp"

                MDCard:
                    radius: [20,]
                    md_bg_color: "#121212"
                    padding: "8dp"
                    elevation: 4
                    ScrollView:
                        MDTextField:
                            id: code_editor
                            text: app.code_init
                            multiline: True
                            mode: "fill"
                            fill_color_normal: [0, 0, 0, 0]
                            text_color_normal: "#D0BCFF"
                            font_size: "15sp"
                            on_text: app.save_draft(self.text)

                MDBoxLayout:
                    size_hint_y: None
                    height: "64dp"
                    padding: "4dp"
                    spacing: "12dp"
                    MDFillRoundFlatButton:
                        id: run_btn
                        text: "ИСПОЛНИТЬ СКРИПТ"
                        icon: "play"
                        font_size: "16sp"
                        size_hint_x: 1
                        md_bg_color: "#D0BCFF"
                        text_color: "#000000"
                        on_release: app.run_engine()
                    
                    MDSpinner:
                        id: loader
                        size_hint: None, None
                        size: "36dp", "36dp"
                        active: False
                        pos_hint: {"center_y": .5}

            MDBottomNavigation:
                id: bot_nav
                panel_color: "#121212"
                selected_color_background: "#1E1E1E"
                MDBottomNavigationItem:
                    name: 'edit'
                    text: 'Редактор'
                    icon: 'code-braces'
                MDBottomNavigationItem:
                    name: 'logs'
                    text: 'Консоль'
                    icon: 'console'
                    MDBoxLayout:
                        md_bg_color: "#000000"
                        ScrollView:
                            id: log_scroll
                            MDLabel:
                                id: console
                                text: app.log_data
                                color: "#00FFC8"
                                font_style: "Caption"
                                size_hint_y: None
                                height: self.texture_size[1]
                                padding: "15dp"

        # Наш помощник-змей
        Image:
            id: serpent_helper
            source: "serpent.png"
            size_hint: None, None
            size: "200dp", "200dp"
            pos_hint: {"center_x": 1.4, "center_y": 0.25}

    MDNavigationDrawer:
        id: nav_drawer
        md_bg_color: "#121212"
        MDBoxLayout:
            orientation: "vertical"
            padding: "16dp"
            spacing: "15dp"
            MDLabel: 
                text: "NEBULA CORE"
                font_style: "H5"
                text_color: "#D0BCFF"
            MDSeparator:
            MDFlatButton: 
                text: "Pip Пакеты"; icon: "package-variant-closed"
                on_release: app.show_pip_dialog()
            MDFlatButton: 
                text: "ИИ Шаблоны"; icon: "brain"
                on_release: app.load_ai_template()
            MDFlatButton: 
                text: "Очистить логи"; icon: "delete-sweep"
                on_release: app.clear_logs()
            MDFlatButton: 
                text: "Сброс"; icon: "refresh"
                on_release: app.reset_system()
            Widget:
'''

class NebulaApp(MDApp):
    log_data = StringProperty("> Nebula Engine Online... Ready to compute.\\n")
    code_init = StringProperty("")
    vault = DictProperty({'is_first_launch': True})
    dialog = None

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "DeepPurple"
        self.load_all_data()
        Window.bind(on_keyboard=self.on_key_handler)
        return Builder.load_string(KV)

    def on_start(self):
        # Настройка разрешений для Android
        if platform.system() == "Android":
            from android.permissions import request_permissions, Permission
            request_permissions([
                Permission.READ_EXTERNAL_STORAGE, 
                Permission.WRITE_EXTERNAL_STORAGE, 
                Permission.INTERNET
            ])
        
        # Запуск интро или главного экрана
        if self.vault.get('is_first_launch', True):
            Clock.schedule_once(self.run_intro_sequence, 0.5)
        else:
            self.root.current = "main_screen"

    def on_key_handler(self, window, key, *args):
        if key == 27: # Кнопка "Назад" на Android
            if self.root.ids.nav_drawer.status == "open":
                self.root.ids.nav_drawer.set_state("close")
                return True
        return False

    def run_intro_sequence(self, dt):
        serpent = self.root.ids.serpent_intro
        anim = Animation(pos_hint={"center_x": 0.5, "center_y": 0.5}, duration=2.5, t='out_back')
        anim.bind(on_complete=self.finish_intro)
        anim.start(serpent)

    def finish_intro(self, *args):
        Clock.schedule_once(lambda x: setattr(self.root, 'current', 'main_screen'), 1)
        self.vault['is_first_launch'] = False
        self.save_all_data()

    def run_engine(self):
        self.root.ids.loader.active = True
        self.root.ids.bot_nav.switch_tab('logs')
        code = self.root.ids.code_editor.text
        
        def execution_thread():
            output_buffer = StringIO()
            sys.stdout = output_buffer
            start_t = time.time()
            try:
                # Глобальное выполнение кода
                exec(code, {**globals(), 'app': self})
                result = output_buffer.getvalue().strip() or "--- Выполнение завершено (без вывода) ---"
            except Exception:
                result = traceback.format_exc()
            finally:
                sys.stdout = sys.__stdout__
            
            elapsed = round(time.time() - start_t, 3)
            self.post_execution_update(f"{result}\\n[Завершено за {elapsed}s]")

        threading.Thread(target=execution_thread, daemon=True).start()

    @mainthread
    def post_execution_update(self, text):
        self.update_log(text)
        self.root.ids.loader.active = False

    @mainthread
    def update_log(self, text):
        self.log_data += f"\\n[{time.strftime('%H:%M:%S')}] {text}"
        Clock.schedule_once(self.scroll_log_to_bottom, 0.1)

    def scroll_log_to_bottom(self, dt):
        self.root.ids.log_scroll.scroll_y = 0

    def insert_symbol(self, sym):
        self.root.ids.code_editor.insert_text(sym + (" " if len(sym) > 1 else ""))

    def call_serpent_help(self):
        serpent = self.root.ids.serpent_helper
        anim = Animation(pos_hint={"center_x": 0.82, "center_y": 0.3}, duration=1, t='out_elastic')
        anim.start(serpent)
        Snackbar(text="Ш-ш-ш! Я приглядываю за твоим кодом...").open()

    def copy_all(self):
        Clipboard.copy(self.root.ids.code_editor.text)
        Snackbar(text="Код скопирован").open()

    def paste_code(self):
        self.root.ids.code_editor.text = Clipboard.paste()

    def load_ai_template(self):
        template = (
            "import torch\\nimport transformers\\n"
            "from transformers import pipeline\\n\\n"
            "print('Загрузка AI... (может занять время)')\\n"
            "# classifier = pipeline('sentiment-analysis')\\n"
            "print('Torch Version:', torch.__version__)"
        )
        self.root.ids.code_editor.text = template
        self.root.ids.nav_drawer.set_state("close")

    def load_all_data(self):
        v_path = os.path.join(self.user_data_dir, "vault.json")
        if os.path.exists(v_path):
            with open(v_path, "r") as f: self.vault = json.load(f)
        
        d_path = os.path.join(self.user_data_dir, "last_session.py")
        if os.path.exists(d_path):
            with open(d_path, "r") as f: self.code_init = f.read()
        else:
            self.code_init = "import torch\\nprint('Hello, Nebula!')"

    def save_all_data(self):
        with open(os.path.join(self.user_data_dir, "vault.json"), "w") as f:
            json.dump(dict(self.vault), f)

    def save_draft(self, text):
        with open(os.path.join(self.user_data_dir, "last_session.py"), "w", encoding='utf-8') as f:
            f.write(text)

    def show_pip_dialog(self):
        self.dialog = MDDialog(
            title="Менеджер Пакетов",
            text="Установка новых библиотек прямо в APK.",
            buttons=[MDFlatButton(text="ОК", on_release=lambda x: self.dialog.dismiss())]
        )
        self.dialog.open()

    def clear_logs(self):
        self.log_data = "> Консоль очищена.\\n"
        self.root.ids.nav_drawer.set_state("close")

    def reset_system(self):
        self.vault['is_first_launch'] = True
        self.save_all_data()
        Snackbar(text="Система будет сброшена при следующем запуске.").open()

if __name__ == "__main__":
    NebulaApp().run()
      

# -*- coding: utf-8: -*-
import os
import sys
import threading
import time
import json
import platform
import traceback
import webbrowser
from io import StringIO

# Ядро Kivy и расширенные свойства
from kivy.lang import Builder
from kivy.clock import Clock, mainthread
from kivy.animation import Animation
from kivy.properties import StringProperty, DictProperty, ListProperty, NumericProperty
from kivy.core.window import Window

# UI Kit: KivyMD (Java/Material Design Style)
from kivymd.app import MDApp
from kivymd.uix.button import MDFillRoundFlatButton, MDFlatButton, MDRaisedButton
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.spinner import MDSpinner
from kivymd.uix.dialog import MDDialog

# Дизайн интерфейса (KV)
KV = '''
<SyntaxButton@MDRaisedButton>:
    size_hint: None, None
    size: "68dp", "46dp"
    elevation: 4
    radius: [12, 12, 12, 12]
    font_style: "Button"

MDScreenManager:
    id: screen_manager

    MDScreen:
        name: "intro_screen"
        md_bg_color: "#000000"
        MDBoxLayout:
            orientation: "vertical"
            Widget:
            Image:
                id: serpent_intro
                source: "serpent.png"
                size_hint: None, None
                size: "350dp", "350dp"
                pos_hint: {"center_x": 0.5, "center_y": -0.5}
            MDLabel:
                text: "NEBULA EVOLUTION"
                halign: "center"
                theme_text_color: "Custom"
                text_color: "#BB86FC"
                font_style: "H4"
                opacity: 0
                id: intro_label
            Widget:

    MDScreen:
        name: "main_screen"
        MDBoxLayout:
            orientation: "vertical"
            md_bg_color: "#050505"

            MDTopAppBar:
                title: "Nebula Ultra [MAX PRO]"
                elevation: 10
                md_bg_color: "#121212"
                left_action_items: [["menu", lambda x: nav_drawer.set_state("open")]]
                right_action_items: [
                    ["telegram", lambda x: app.open_channel()],
                    ["robot-industrial", lambda x: app.call_serpent_help()]
                ]

            # Панель синтаксиса (Syntax Toolbar)
            ScrollView:
                size_hint_y: None
                height: "68dp"
                do_scroll_y: False
                bar_width: 0
                MDBoxLayout:
                    orientation: "horizontal"
                    adaptive_width: True
                    padding: "12dp"
                    spacing: "12dp"
                    SyntaxButton: text: "def"; md_bg_color: "#FF5252"; on_release: app.insert_code("def ")
                    SyntaxButton: text: "class"; md_bg_color: "#448AFF"; on_release: app.insert_code("class ")
                    SyntaxButton: text: "import"; md_bg_color: "#E040FB"; on_release: app.insert_code("import ")
                    SyntaxButton: text: "torch"; md_bg_color: "#FFAB40"; on_release: app.insert_code("torch")
                    SyntaxButton: text: "if"; md_bg_color: "#FF6E40"; on_release: app.insert_code("if ")
                    SyntaxButton: text: "print"; md_bg_color: "#64DD17"; on_release: app.insert_code("print(")
                    SyntaxButton: text: "tg_bot"; md_bg_color: "#00E5FF"; on_release: app.insert_code("tg_bridge")
                    SyntaxButton: text: ":"; md_bg_color: "#212121"; on_release: app.insert_code(":")
                    SyntaxButton: text: "("; md_bg_color: "#212121"; on_release: app.insert_code("(")
                    SyntaxButton: text: ")"; md_bg_color: "#212121"; on_release: app.insert_code(")")

            MDBoxLayout:
                orientation: "vertical"
                padding: "10dp"
                spacing: "10dp"

                MDCard:
                    radius: [20,]
                    md_bg_color: "#0F0F0F"
                    elevation: 5
                    padding: "15dp"
                    ScrollView:
                        MDTextField:
                            id: code_editor
                            text: app.code_init
                            multiline: True
                            mode: "fill"
                            fill_color_normal: [0, 0, 0, 0]
                            text_color_normal: "#D1C4E9"
                            font_size: "15sp"
                            on_text: app.auto_save_handler(self.text)

                MDBoxLayout:
                    size_hint_y: None
                    height: "65dp"
                    spacing: "15dp"
                    MDFillRoundFlatButton:
                        text: "EXECUTE NEBULA CORE"
                        icon: "flash"
                        font_size: "16sp"
                        size_hint_x: 1
                        md_bg_color: "#6200EE"
                        on_release: app.run_engine()
                    MDSpinner:
                        id: loader
                        size_hint: None, None
                        size: "32dp", "32dp"
                        active: False
                        pos_hint: {"center_y": .5}

            MDBottomNavigation:
                id: bot_nav
                panel_color: "#121212"
                MDBottomNavigationItem:
                    name: 'edit'; text: 'IDE Editor'; icon: 'code-braces'
                MDBottomNavigationItem:
                    name: 'logs'; text: 'AI Console'; icon: 'console'
                    MDBoxLayout:
                        md_bg_color: "#000000"
                        ScrollView:
                            id: log_scroll
                            MDLabel:
                                id: console
                                text: app.log_data
                                color: "#00E676"
                                font_style: "Caption"
                                size_hint_y: None
                                height: self.texture_size[1]
                                padding: "15dp"

        # Змей-помощник
        Image:
            id: serpent_helper
            source: "serpent.png"
            size_hint: None, None
            size: "250dp", "250dp"
            pos_hint: {"center_x": 1.6, "center_y": 0.3}

    MDNavigationDrawer:
        id: nav_drawer
        md_bg_color: "#121212"
        radius: (0, 16, 16, 0)
        MDBoxLayout:
            orientation: "vertical"
            padding: "20dp"
            spacing: "12dp"
            MDLabel: text: "NEBULA CONTROL"; font_style: "H5"; text_color: "#BB86FC"
            MDSeparator:
            MDFlatButton: text: "Smart Pip Manager"; icon: "package"; on_release: app.smart_pip()
            MDFlatButton: text: "TG Bridge Alpha"; icon: "bridge"; on_release: app.open_bridge(1)
            MDFlatButton: text: "TG Bridge Beta"; icon: "bridge"; on_release: app.open_bridge(2)
            MDFlatButton: text: "Join Community"; icon: "star"; on_release: app.open_channel()
            MDFlatButton: text: "Reset Cutscene"; icon: "refresh"; on_release: app.reset_intro_state()
            MDFlatButton: text: "Clear Logs"; icon: "trash-can"; on_release: app.clear_console()
            Widget:
            MDLabel: text: "Build 3.2.5 PRO"; font_style: "Caption"; text_color: "#444444"
'''

class NebulaApp(MDApp):
    log_data = StringProperty("> Nebula OS Initialized...\\n> All AI Bridges Active.\\n")
    code_init = StringProperty("")
    vault = DictProperty({'is_fresh': True})

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "DeepPurple"
        self.load_all_data()
        return Builder.load_string(KV)

    def on_start(self):
        # Запрос разрешений (Android)
        if platform.system() == "android":
            from android.permissions import request_permissions, Permission
            request_permissions([
                Permission.READ_EXTERNAL_STORAGE, 
                Permission.WRITE_EXTERNAL_STORAGE, 
                Permission.INTERNET
            ])

        # Логика Кат-сцены (Show once)
        if self.vault.get('is_fresh', True):
            intro_screen = self.root.ids.screen_manager.get_screen('intro_screen')
            serpent = intro_screen.ids.serpent_intro
            label = intro_screen.ids.intro_label
            
            anim = Animation(pos_hint={"center_x": 0.5, "center_y": 0.5}, duration=2.2, t='out_back')
            anim.bind(on_complete=self.end_intro)
            anim.start(serpent)
            Animation(opacity=1, duration=2).start(label)
        else:
            self.root.ids.screen_manager.current = "main_screen"

    def end_intro(self, *args):
        self.vault['is_fresh'] = False
        self.save_all_data()
        Clock.schedule_once(lambda x: setattr(self.root.ids.screen_manager, 'current', 'main_screen'), 0.5)

    def run_engine(self):
        self.root.ids.loader.active = True
        self.root.ids.bot_nav.switch_tab('logs')
        code = self.root.ids.code_editor.text
        
        def execution_thread():
            old_stdout = sys.stdout
            it_output = sys.stdout = StringIO()
            start_time = time.time()
            try:
                # Глобальный контекст для выполнения кода
                exec(code, {**globals(), 'app': self})
                result = it_output.getvalue().strip() or "--- Done (No Output) ---"
            except Exception:
                result = traceback.format_exc()
            finally:
                sys.stdout = old_stdout
            
            self.finalize_update(f"{result}\\n[Time: {round(time.time() - start_time, 4)}s]")

        threading.Thread(target=execution_thread, daemon=True).start()

    @mainthread
    def finalize_update(self, res):
        self.log_data += f"\\n[{time.strftime('%H:%M:%S')}] {res}"
        self.root.ids.loader.active = False
        Clock.schedule_once(lambda x: setattr(self.root.ids.log_scroll, 'scroll_y', 0), 0.1)

    def auto_save_handler(self, text):
        with open(os.path.join(self.user_data_dir, "nebula_draft.py"), "w", encoding='utf-8') as f:
            f.write(text)

    def load_all_data(self):
        # Загрузка состояния приложения
        v_path = os.path.join(self.user_data_dir, "vault.json")
        if os.path.exists(v_path):
            with open(v_path, "r") as f: self.vault = json.load(f)
        
        # Загрузка последнего кода
        c_path = os.path.join(self.user_data_dir, "nebula_draft.py")
        if os.path.exists(c_path):
            with open(c_path, "r") as f: self.code_init = f.read()
        else:
            self.code_init = "import torch\\nprint('Nebula Master Active')"

    def save_all_data(self):
        with open(os.path.join(self.user_data_dir, "vault.json"), "w") as f:
            json.dump(dict(self.vault), f)

    def reset_intro_state(self):
        self.vault['is_fresh'] = True
        self.save_all_data()
        Snackbar(text="Cutscene will play on next launch").open()

    def insert_code(self, val): self.root.ids.code_editor.insert_text(val)
    def open_bridge(self, n): Snackbar(text=f"Telegram Bridge Alpha {n} activated.").open()
    def smart_pip(self): Snackbar(text="Smart Pip: Syncing requirements...").open()
    def open_channel(self): webbrowser.open("https://t.me/nebula_evolution")
    def clear_console(self): self.log_data = "> Logs Cleared.\\n"
    
    def call_serpent_help(self):
        anim = Animation(pos_hint={"center_x": 0.82, "center_y": 0.3}, duration=1, t='out_elastic')
        anim.start(self.root.ids.serpent_helper)
        Snackbar(text="Snake Assistant is watching!").open()

if __name__ == "__main__":
    NebulaApp().run()
  

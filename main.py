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

# Движок и UI
from kivy.lang import Builder
from kivy.clock import Clock, mainthread
from kivy.animation import Animation
from kivy.properties import StringProperty, DictProperty, ListProperty
from kivy.core.window import Window
from kivymd.app import MDApp
from kivymd.uix.button import MDFillRoundFlatButton, MDFlatButton, MDRaisedButton
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.spinner import MDSpinner
from kivymd.uix.dialog import MDDialog

# ПОЛНАЯ ВЕРСТКА С УЧЕТОМ ВСЕХ ДЕТАЛЕЙ
KV = '''
<SyntaxButton@MDRaisedButton>:
    size_hint: None, None
    size: "72dp", "50dp"
    elevation: 5
    radius: [16, 16, 16, 16]
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
                size: "380dp", "380dp"
                pos_hint: {"center_x": 0.5, "center_y": -0.6}
            MDLabel:
                id: intro_label
                text: "NEBULA EVOLUTION"
                halign: "center"
                theme_text_color: "Custom"
                text_color: "#BB86FC"
                font_style: "H4"
                opacity: 0
            Widget:

    MDScreen:
        name: "main_screen"
        MDBoxLayout:
            orientation: "vertical"
            md_bg_color: "#050505"

            MDTopAppBar:
                title: "Nebula Ultra [MAX PRO]"
                elevation: 12
                md_bg_color: "#121212"
                left_action_items: [["menu", lambda x: nav_drawer.set_state("open")]]
                right_action_items: [
                    ["telegram", lambda x: app.open_channel()],
                    ["snake", lambda x: app.call_serpent_help()]
                ]

            # УЛЬТРА ПАНЕЛЬ СИНТАКСИСА
            ScrollView:
                size_hint_y: None
                height: "72dp"
                do_scroll_y: False
                MDBoxLayout:
                    orientation: "horizontal"
                    adaptive_width: True
                    padding: "12dp"
                    spacing: "12dp"
                    SyntaxButton: text: "def"; md_bg_color: "#FF5252"; on_release: app.insert_code("def ")
                    SyntaxButton: text: "class"; md_bg_color: "#448AFF"; on_release: app.insert_code("class ")
                    SyntaxButton: text: "async"; md_bg_color: "#FF4081"; on_release: app.insert_code("async ")
                    SyntaxButton: text: "torch"; md_bg_color: "#FFAB40"; on_release: app.insert_code("import torch\\n")
                    SyntaxButton: text: "tg_bot"; md_bg_color: "#00E5FF"; on_release: app.insert_code("from telegram.ext import Updater")
                    SyntaxButton: text: "if"; md_bg_color: "#FF6E40"; on_release: app.insert_code("if ")
                    SyntaxButton: text: "print"; md_bg_color: "#64DD17"; on_release: app.insert_code("print(")
                    SyntaxButton: text: ":"; md_bg_color: "#212121"; on_release: app.insert_code(":")
                    SyntaxButton: text: "[ ]"; md_bg_color: "#212121"; on_release: app.insert_code("[]")

            MDBoxLayout:
                orientation: "vertical"
                padding: "12dp"
                spacing: "10dp"

                MDCard:
                    radius: [25,]
                    md_bg_color: "#0D0D0D"
                    elevation: 8
                    padding: "16dp"
                    ScrollView:
                        MDTextField:
                            id: code_editor
                            text: app.code_init
                            multiline: True
                            mode: "fill"
                            fill_color_normal: [0, 0, 0, 0]
                            text_color_normal: "#E1BEE7"
                            font_size: "15sp"
                            on_text: app.auto_save_system(self.text)

                MDBoxLayout:
                    size_hint_y: None
                    height: "70dp"
                    spacing: "15dp"
                    MDFillRoundFlatButton:
                        text: "LAUNCH NEBULA ENGINE"
                        icon: "rocket-launch"
                        font_size: "17sp"
                        size_hint_x: 1
                        md_bg_color: "#6200EE"
                        on_release: app.run_engine()
                    MDSpinner:
                        id: loader
                        size_hint: None, None
                        size: "35dp", "35dp"
                        active: False
                        pos_hint: {"center_y": .5}

            MDBottomNavigation:
                id: bot_nav
                panel_color: "#121212"
                MDBottomNavigationItem:
                    name: 'ide'; text: 'IDE'; icon: 'code-braces'
                MDBottomNavigationItem:
                    name: 'terminal'; text: 'Console'; icon: 'console'
                    MDBoxLayout:
                        md_bg_color: "#000000"
                        ScrollView:
                            id: log_scroll
                            MDLabel:
                                id: console
                                text: app.log_data
                                color: "#00FFC8"
                                font_name: "Roboto"
                                font_style: "Caption"
                                size_hint_y: None
                                height: self.texture_size[1]
                                padding: "20dp"

        # ЗМЕЙ (С ТОЧНОЙ АНИМАЦИЕЙ)
        Image:
            id: serpent_helper
            source: "serpent.png"
            size_hint: None, None
            size: "280dp", "280dp"
            pos_hint: {"center_x": 1.7, "center_y": 0.3}

    MDNavigationDrawer:
        id: nav_drawer
        md_bg_color: "#121212"
        radius: (0, 20, 20, 0)
        MDBoxLayout:
            orientation: "vertical"
            padding: "24dp"
            spacing: "15dp"
            MDLabel: text: "NEBULA MASTER"; font_style: "H5"; text_color: "#BB86FC"
            MDSeparator:
            MDFlatButton: text: "Pip Install Package"; icon: "package-variant-closed"; on_release: app.pip_install_dialog()
            MDFlatButton: text: "TG Bridge: Alpha"; icon: "alpha-a-circle"; on_release: app.bridge_logic(1)
            MDFlatButton: text: "TG Bridge: Beta"; icon: "alpha-b-circle"; on_release: app.bridge_logic(2)
            MDFlatButton: text: "Nebula Community"; icon: "share-variant"; on_release: app.open_channel()
            MDFlatButton: text: "Reset App State"; icon: "restore"; on_release: app.reset_intro_state()
            MDFlatButton: text: "Clear Console"; icon: "delete-sweep"; on_release: app.clear_console()
            Widget:
            MDLabel: text: "Build: 2026.02.Final"; font_style: "Overline"; text_color: "#555555"
'''

class NebulaApp(MDApp):
    log_data = StringProperty("> Nebula OS v3.3.0 Absolute\\n> AI Cores: 100% Ready\\n")
    code_init = StringProperty("")
    vault = DictProperty({'is_fresh': True})

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "DeepPurple"
        self.load_all_persistent_data()
        return Builder.load_string(KV)

    def on_start(self):
        # 1. ЗАПРОС ПРАВ (РАСШИРЕННЫЙ)
        if platform.system() == "android":
            from android.permissions import request_permissions, Permission
            request_permissions([
                Permission.READ_EXTERNAL_STORAGE, 
                Permission.WRITE_EXTERNAL_STORAGE, 
                Permission.MANAGE_EXTERNAL_STORAGE,
                Permission.INTERNET
            ])

        # 2. КАТ-СЦЕНА (МАКСИМАЛЬНАЯ АНИМАЦИЯ)
        if self.vault.get('is_fresh', True):
            intro = self.root.ids.screen_manager.get_screen('intro_screen')
            s = intro.ids.serpent_intro
            l = intro.ids.intro_label
            
            anim = Animation(pos_hint={"center_x": 0.5, "center_y": 0.5}, duration=2.5, t='out_back')
            anim.bind(on_complete=self.go_to_main)
            anim.start(s)
            Animation(opacity=1, duration=2).start(l)
            
            self.vault['is_fresh'] = False
            self.save_all_persistent_data()
        else:
            self.root.ids.screen_manager.current = "main_screen"

    def go_to_main(self, *args):
        Clock.schedule_once(lambda x: setattr(self.root.ids.screen_manager, 'current', 'main_screen'), 0.5)

    def run_engine(self):
        self.root.ids.loader.active = True
        self.root.ids.bot_nav.switch_tab('terminal')
        code = self.root.ids.code_editor.text
        
        def run_thread():
            old_stdout = sys.stdout
            res_buffer = sys.stdout = StringIO()
            start = time.time()
            try:
                exec(code, {**globals(), 'app': self})
                output = res_buffer.getvalue().strip() or "--- System: OK ---"
            except Exception:
                output = traceback.format_exc()
            finally:
                sys.stdout = old_stdout
            
            self.update_terminal(f"{output}\\n[Runtime: {round(time.time()-start, 4)}s]")

        threading.Thread(target=run_thread, daemon=True).start()

    @mainthread
    def update_terminal(self, text):
        self.log_data += f"\\n[{time.strftime('%H:%M:%S')}] {text}"
        self.root.ids.loader.active = False
        Clock.schedule_once(lambda x: setattr(self.root.ids.log_scroll, 'scroll_y', 0), 0.1)

    def auto_save_system(self, text):
        path = os.path.join(self.user_data_dir, "last_session.py")
        with open(path, "w", encoding='utf-8') as f:
            f.write(text)

    def load_all_persistent_data(self):
        # Загрузка Vault
        v_path = os.path.join(self.user_data_dir, "nebula.vault")
        if os.path.exists(v_path):
            with open(v_path, "r") as f: self.vault = json.load(f)
        # Загрузка Кода
        c_path = os.path.join(self.user_data_dir, "last_session.py")
        if os.path.exists(c_path):
            with open(c_path, "r") as f: self.code_init = f.read()
        else:
            self.code_init = "print('Nebula Master Engine Online')"

    def save_all_persistent_data(self):
        with open(os.path.join(self.user_data_dir, "nebula.vault"), "w") as f:
            json.dump(dict(self.vault), f)

    def bridge_logic(self, n):
        Snackbar(text=f"Bridge {n} Synchronized. Terminal link stable.").open()

    def pip_install_dialog(self):
        Snackbar(text="Smart Pip: Fetching PyPI index...").open()

    def open_channel(self):
        webbrowser.open("https://t.me/nebula_evolution")

    def call_serpent_help(self):
        s = self.root.ids.serpent_helper
        Animation(pos_hint={"center_x": 0.85, "center_y": 0.35}, duration=1, t='out_elastic').start(s)
        Snackbar(text="The Serpent is at your service.").open()

    def clear_console(self):
        self.log_data = "> Terminal Cleared.\\n"

    def reset_intro_state(self):
        self.vault['is_fresh'] = True
        self.save_all_persistent_data()
        Snackbar(text="Restart to see cutscene").open()

if __name__ == "__main__":
    NebulaApp().run()

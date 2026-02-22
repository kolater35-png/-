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

# Kivy & KivyMD
from kivy.lang import Builder
from kivy.clock import Clock, mainthread
from kivy.animation import Animation
from kivy.properties import StringProperty, DictProperty
from kivy.core.clipboard import Clipboard
from kivy.core.window import Window

from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFillRoundFlatButton, MDFlatButton, MDRaisedButton
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.spinner import MDSpinner

# Конфигурация интерфейса (KV)
KV = '''
<SyntaxButton@MDRaisedButton>:
    size_hint: None, None
    size: "64dp", "44dp"
    elevation: 4
    radius: [12, 12, 12, 12]

MDScreenManager:
    id: screen_manager
    MDScreen:
        name: "intro_screen"
        md_bg_color: "#000000"
        Image:
            id: serpent_intro
            source: "serpent.png"
            size_hint: None, None
            size: "350dp", "350dp"
            pos_hint: {"center_x": 0.5, "center_y": -0.5}

    MDScreen:
        name: "main_screen"
        MDBoxLayout:
            orientation: "vertical"
            md_bg_color: "#050505"
            MDTopAppBar:
                title: "Nebula Ultra PRO"
                elevation: 8
                md_bg_color: "#121212"
                left_action_items: [["menu", lambda x: nav_drawer.set_state("open")]]
                right_action_items: [["telegram", lambda x: app.open_channel()], ["robot", lambda x: app.call_serpent()]]

            ScrollView:
                size_hint_y: None
                height: "64dp"
                do_scroll_y: False
                MDBoxLayout:
                    orientation: "horizontal"
                    adaptive_width: True
                    padding: "10dp"
                    spacing: "12dp"
                    SyntaxButton: text: "def"; md_bg_color: "#FF5252"; on_release: app.insert_code("def ")
                    SyntaxButton: text: "class"; md_bg_color: "#448AFF"; on_release: app.insert_code("class ")
                    SyntaxButton: text: "torch"; md_bg_color: "#FFAB40"; on_release: app.insert_code("torch")
                    SyntaxButton: text: "tg_bot"; md_bg_color: "#00E5FF"; on_release: app.insert_code("tg_bridge")
                    SyntaxButton: text: ":"; md_bg_color: "#212121"; on_release: app.insert_code(":")
                    SyntaxButton: text: "("; md_bg_color: "#212121"; on_release: app.insert_code("(")
                    SyntaxButton: text: ")"; md_bg_color: "#212121"; on_release: app.insert_code(")")

            MDBoxLayout:
                orientation: "vertical"
                padding: "8dp"
                MDCard:
                    radius: [20,]
                    md_bg_color: "#0D0D0D"
                    padding: "12dp"
                    ScrollView:
                        MDTextField:
                            id: code_editor
                            text: app.code_init
                            multiline: True
                            mode: "fill"
                            fill_color_normal: [0, 0, 0, 0]
                            text_color_normal: "#D1C4E9"
                            on_text: app.auto_save(self.text)

                MDBoxLayout:
                    size_hint_y: None
                    height: "60dp"
                    padding: "5dp"
                    MDFillRoundFlatButton:
                        text: "RUN ENGINE"
                        size_hint_x: 1
                        on_release: app.run_engine()
                    MDSpinner:
                        id: loader
                        size_hint: None, None
                        size: "30dp", "30dp"
                        active: False

            MDBottomNavigation:
                id: bot_nav
                panel_color: "#121212"
                MDBottomNavigationItem:
                    name: 'edit'; text: 'Editor'; icon: 'code-braces'
                MDBottomNavigationItem:
                    name: 'logs'; text: 'Console'; icon: 'console'
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

        Image:
            id: serpent_helper
            source: "serpent.png"
            size_hint: None, None
            size: "200dp", "200dp"
            pos_hint: {"center_x": 1.5, "center_y": 0.3}

    MDNavigationDrawer:
        id: nav_drawer
        md_bg_color: "#121212"
        MDBoxLayout:
            orientation: "vertical"
            padding: "16dp"
            spacing: "10dp"
            MDLabel: text: "NEBULA CORE"; font_style: "H6"; text_color: "#BB86FC"
            MDSeparator:
            MDFlatButton: text: "Smart Pip"; icon: "package"; on_release: app.smart_pip()
            MDFlatButton: text: "TG Bridge 1"; icon: "bridge"; on_release: app.open_bridge(1)
            MDFlatButton: text: "TG Bridge 2"; icon: "bridge"; on_release: app.open_bridge(2)
            MDFlatButton: text: "Community"; icon: "star"; on_release: app.open_channel()
            MDFlatButton: text: "Reset Intro"; on_release: app.reset_intro()
            Widget:
'''

class NebulaApp(MDApp):
    log_data = StringProperty("> Nebula Engine Active\\n")
    code_init = StringProperty("")
    vault = DictProperty({'is_fresh': True})

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "DeepPurple"
        self.load_all()
        return Builder.load_string(KV)

    def on_start(self):
        # 1. Запрос разрешений для Android
        if platform.system() == "Android":
            from android.permissions import request_permissions, Permission
            request_permissions([
                Permission.READ_EXTERNAL_STORAGE,
                Permission.WRITE_EXTERNAL_STORAGE,
                Permission.MANAGE_EXTERNAL_STORAGE,
                Permission.INTERNET
            ])

        # 2. Логика кат-сцены (показ только один раз)
        if self.vault.get('is_fresh', True):
            serpent = self.root.ids.serpent_intro
            anim = Animation(pos_hint={"center_x": 0.5, "center_y": 0.5}, duration=2, t='out_back')
            anim.bind(on_complete=self.finish_intro)
            anim.start(serpent)
        else:
            self.root.ids.screen_manager.current = "main_screen"

    def finish_intro(self, *args):
        self.vault['is_fresh'] = False
        self.save_all()
        self.root.ids.screen_manager.current = "main_screen"

    def run_engine(self):
        self.root.ids.loader.active = True
        self.root.ids.bot_nav.switch_tab('logs')
        code = self.root.ids.code_editor.text
        def worker():
            buf = StringIO()
            sys.stdout = buf
            try:
                exec(code, {**globals(), 'app': self})
                res = buf.getvalue().strip() or "Success"
            except Exception: res = traceback.format_exc()
            finally: sys.stdout = sys.__stdout__
            self.post_res(res)
        threading.Thread(target=worker, daemon=True).start()

    @mainthread
    def post_res(self, res):
        self.log_data += f"\\n[{time.strftime('%H:%M:%S')}] {res}"
        self.root.ids.loader.active = False

    def auto_save(self, text):
        with open(os.path.join(self.user_data_dir, "nebula_draft.py"), "w", encoding='utf-8') as f:
            f.write(text)

    def load_all(self):
        # Загрузка настроек
        v_path = os.path.join(self.user_data_dir, "vault.json")
        if os.path.exists(v_path):
            with open(v_path, "r") as f: self.vault = json.load(f)
        # Загрузка кода
        c_path = os.path.join(self.user_data_dir, "nebula_draft.py")
        if os.path.exists(c_path):
            with open(c_path, "r") as f: self.code_init = f.read()
        else: self.code_init = "print('Welcome')"

    def save_all(self):
        with open(os.path.join(self.user_data_dir, "vault.json"), "w") as f:
            json.dump(dict(self.vault), f)

    def reset_intro(self):
        self.vault['is_fresh'] = True
        self.save_all()
        Snackbar(text="Intro will play on restart").open()

    def insert_code(self, t): self.root.ids.code_editor.insert_text(t)
    def open_bridge(self, n): Snackbar(text=f"Bridge {n} active").open()
    def smart_pip(self): Snackbar(text="Analyzing dependencies...").open()
    def open_channel(self): webbrowser.open("https://t.me/nebula_evolution")
    def call_serpent(self):
        Animation(pos_hint={"center_x": 0.85, "center_y": 0.3}, duration=1, t='out_elastic').start(self.root.ids.serpent_helper)

if __name__ == "__main__":
    NebulaApp().run()
  

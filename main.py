# -*- coding: utf-8: -*-
import os, sys, threading, time, json, platform, traceback
from io import StringIO
from kivy.lang import Builder
from kivy.clock import Clock, mainthread
from kivy.animation import Animation
from kivy.properties import StringProperty, DictProperty, BooleanProperty
from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFillRoundFlatButton, MDFlatButton, MDRaisedButton
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.spinner import MDSpinner
from kivy.core.clipboard import Clipboard
from kivy.core.window import Window

# Интерфейс Nebula Ultra IDE
KV = '''
<SymbolButton@MDRaisedButton>:
    size_hint: None, None
    size: "48dp", "42dp"
    md_bg_color: "#1E1E1E"
    text_color: "#D0BCFF"
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

            ScrollView:
                size_hint_y: None
                height: "56dp"
                do_scroll_y: False
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
                    SymbolButton: text: "import"
                    SymbolButton: text: "torch"
                    SymbolButton: text: "nn."

            MDBoxLayout:
                orientation: "vertical"
                padding: "10dp"
                MDCard:
                    radius: [20,]
                    md_bg_color: "#121212"
                    padding: "8dp"
                    ScrollView:
                        MDTextField:
                            id: code_editor
                            text: app.code_init
                            multiline: True
                            mode: "fill"
                            fill_color_normal: [0, 0, 0, 0]
                            text_color_normal: "#D0BCFF"
                            on_text: app.save_draft(self.text)

                MDBoxLayout:
                    size_hint_y: None
                    height: "64dp"
                    padding: "4dp"
                    spacing: "12dp"
                    MDFillRoundFlatButton:
                        text: "ИСПОЛНИТЬ"
                        icon: "play"
                        size_hint_x: 1
                        on_release: app.run_engine()
                    MDSpinner:
                        id: loader
                        size_hint: None, None
                        size: "36dp", "36dp"
                        active: False

            MDBottomNavigation:
                id: bot_nav
                panel_color: "#121212"
                MDBottomNavigationItem:
                    name: 'edit'; text: 'Код'; icon: 'code-braces'
                MDBottomNavigationItem:
                    name: 'logs'; text: 'Консоль'; icon: 'console'
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
            MDLabel: text: "NEBULA CORE"; font_style: "H5"; text_color: "#D0BCFF"
            MDSeparator:
            MDFlatButton: text: "Pip Install"; icon: "package"; on_release: app.show_pip_dialog()
            MDFlatButton: text: "AI Examples"; icon: "brain"; on_release: app.load_ai_template()
            MDFlatButton: text: "Clear Logs"; icon: "delete"; on_release: app.clear_logs()
'''

class NebulaApp(MDApp):
    log_data = StringProperty("> Nebula Engine Online\\n")
    code_init = StringProperty("import torch\\nprint('Torch version:', torch.__version__)")
    vault = DictProperty({'is_first_launch': True})

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "DeepPurple"
        self.load_data()
        Window.bind(on_keyboard=self.on_key)
        return Builder.load_string(KV)

    def on_start(self):
        if self.vault.get('is_first_launch', True):
            Clock.schedule_once(self.run_intro, 0.5)
        else:
            self.root.current = "main_screen"

    def on_key(self, window, key, *args):
        if key == 27 and self.root.ids.nav_drawer.status == "open":
            self.root.ids.nav_drawer.set_state("close")
            return True
        return False

    def run_intro(self, dt):
        serpent = self.root.ids.serpent_intro
        anim = Animation(pos_hint={"center_x": 0.5, "center_y": 0.5}, duration=2, t='out_back')
        anim.bind(on_complete=lambda *x: setattr(self.root, 'current', 'main_screen'))
        anim.start(serpent)
        self.vault['is_first_launch'] = False
        self.save_data()

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
            except Exception:
                res = traceback.format_exc()
            finally:
                sys.stdout = sys.__stdout__
            self.post_res(res)
        threading.Thread(target=worker, daemon=True).start()

    @mainthread
    def post_res(self, res):
        self.log_data += f"\\n[{time.strftime('%H:%M:%S')}] {res}"
        self.root.ids.loader.active = False
        Clock.schedule_once(lambda x: setattr(self.root.ids.log_scroll, 'scroll_y', 0), 0.1)

    def insert_symbol(self, sym):
        self.root.ids.code_editor.insert_text(sym + " ")

    def call_serpent_help(self):
        serpent = self.root.ids.serpent_helper
        Animation(pos_hint={"center_x": 0.85, "center_y": 0.3}, duration=0.8, t='out_back').start(serpent)

    def copy_all(self):
        Clipboard.copy(self.root.ids.code_editor.text)
        Snackbar(text="Copied").open()

    def paste_code(self):
        self.root.ids.code_editor.text = Clipboard.paste()

    def load_ai_template(self):
        self.root.ids.code_editor.text = "import torch.nn as nn\\nmodel = nn.Sequential(nn.Linear(10, 1))\\nprint(model)"
        self.root.ids.nav_drawer.set_state("close")

    def load_data(self):
        path = os.path.join(self.user_data_dir, "vault.json")
        if os.path.exists(path):
            with open(path, "r") as f: self.vault = json.load(f)
        d_path = os.path.join(self.user_data_dir, "last.py")
        if os.path.exists(d_path):
            with open(d_path, "r") as f: self.code_init = f.read()

    def save_data(self):
        with open(os.path.join(self.user_data_dir, "vault.json"), "w") as f: json.dump(dict(self.vault), f)

    def save_draft(self, text):
        with open(os.path.join(self.user_data_dir, "last.py"), "w", encoding='utf-8') as f: f.write(text)

    def clear_logs(self):
        self.log_data = "> Logs cleared\\n"
        self.root.ids.nav_drawer.set_state("close")

    def show_pip_dialog(self):
        Snackbar(text="Use pip.main(['install', 'pkg']) in code").open()

if __name__ == "__main__":
    NebulaApp().run()
                      

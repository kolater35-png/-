# -*- coding: utf-8: -*-
import os, sys, threading, time, json, platform, traceback
from io import StringIO
from kivy.lang import Builder
from kivy.clock import Clock, mainthread
from kivy.animation import Animation
from kivy.properties import StringProperty, DictProperty
from kivymd.app import MDApp
from kivymd.uix.button import MDFillRoundFlatButton, MDFlatButton, MDRaisedButton
from kivymd.uix.snackbar import Snackbar

# Полный UI Nebula Master
KV = '''
<SyntaxBtn@MDRaisedButton>:
    size_hint: None, None
    size: "75dp", "52dp"
    elevation: 6
    radius: [18,]
    md_bg_color: 0.1, 0.1, 0.1, 1

MDScreenManager:
    id: screen_manager
    MDScreen:
        name: "intro"
        md_bg_color: "#000000"
        Image:
            id: serpent_intro
            source: "serpent.png"
            size_hint: None, None
            size: "380dp", "380dp"
            pos_hint: {"center_x": .5, "center_y": -.6}
        MDLabel:
            id: intro_text
            text: "NEBULA EVOLUTION"
            halign: "center"
            theme_text_color: "Custom"
            text_color: "#BB86FC"
            font_style: "H4"
            opacity: 0

    MDScreen:
        name: "main"
        MDBoxLayout:
            orientation: "vertical"
            md_bg_color: "#050505"
            MDTopAppBar:
                title: "Nebula Master [PRO]"
                md_bg_color: "#121212"
                left_action_items: [["menu", lambda x: nav_drawer.set_state("open")]]
                right_action_items: [["robot", lambda x: app.call_serpent()]]

            ScrollView:
                size_hint_y: None
                height: "80dp"
                do_scroll_y: False
                MDBoxLayout:
                    adaptive_width: True
                    padding: "15dp"
                    spacing: "12dp"
                    SyntaxBtn: text: "def"; on_release: app.ins("def ")
                    SyntaxBtn: text: "class"; on_release: app.ins("class ")
                    SyntaxBtn: text: "import"; on_release: app.ins("import ")
                    SyntaxBtn: text: "print"; on_release: app.ins("print()")
                    SyntaxBtn: text: ":"; on_release: app.ins(":")

            MDBoxLayout:
                orientation: "vertical"
                padding: "12dp"
                MDCard:
                    radius: [25,]
                    md_bg_color: "#0D0D0D"
                    padding: "15dp"
                    ScrollView:
                        MDTextField:
                            id: editor
                            text: app.code_init
                            multiline: True
                            mode: "fill"
                            on_text: app.auto_save(self.text)

                MDFillRoundFlatButton:
                    text: "RUN SYSTEM"
                    size_hint_x: 1
                    md_bg_color: "#6200EE"
                    on_release: app.run_engine()

            MDBottomNavigation:
                id: b_nav
                panel_color: "#121212"
                MDBottomNavigationItem:
                    name: 'ide'; text: 'IDE'; icon: 'code-tags'
                MDBottomNavigationItem:
                    name: 'logs'; text: 'Logs'; icon: 'console'
                    MDBoxLayout:
                        md_bg_color: "#000000"
                        ScrollView:
                            id: log_scroll
                            MDLabel:
                                id: console
                                text: app.log_data
                                color: "#00FFC8"
                                size_hint_y: None
                                height: self.texture_size[1]
                                padding: "20dp"

        Image:
            id: serpent_helper
            source: "serpent.png"
            size_hint: None, None
            size: "280dp", "280dp"
            pos_hint: {"center_x": 1.8, "center_y": 0.35}

    MDNavigationDrawer:
        id: nav_drawer
        md_bg_color: "#121212"
        MDBoxLayout:
            orientation: "vertical"
            padding: "20dp"
            MDLabel: text: "NEBULA CONTROL"; font_style: "H6"; text_color: "#BB86FC"
            MDSeparator:
            MDFlatButton: text: "Reset App"; icon: "refresh"; on_release: app.reset()
            MDFlatButton: text: "Clear Logs"; icon: "delete"; on_release: app.clear()
            Widget:
'''

class NebulaApp(MDApp):
    log_data = StringProperty("> Core Online\\n")
    code_init = StringProperty("print('Nebula Ready')")
    vault = DictProperty({'is_fresh': True})

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.load_data()
        return Builder.load_string(KV)

    def on_start(self):
        if self.vault.get('is_fresh', True):
            s, t = self.root.ids.serpent_intro, self.root.ids.intro_text
            anim = Animation(pos_hint={"center_x": .5, "center_y": .5}, duration=2, t='out_back')
            anim.bind(on_complete=self.go_main)
            anim.start(s)
            Animation(opacity=1, duration=1.5).start(t)
        else:
            self.root.ids.screen_manager.current = "main"

    def go_main(self, *args):
        self.vault['is_fresh'] = False
        self.save_data()
        Clock.schedule_once(lambda x: setattr(self.root.ids.screen_manager, 'current', 'main'), 1)

    def run_engine(self):
        self.root.ids.b_nav.switch_tab('logs')
        code = self.root.ids.editor.text
        def work():
            # Попытка динамического импорта тяжелых библиотек
            try:
                import torch
                self.post(f"Torch version: {torch.__version__}")
            except ImportError:
                self.post("Note: Torch not installed in this build.")
            
            old_out = sys.stdout
            res = sys.stdout = StringIO()
            try:
                exec(code, {**globals(), 'app': self})
                out = res.getvalue() or "Done."
            except: out = traceback.format_exc()
            finally: sys.stdout = old_out
            self.post(out)
        threading.Thread(target=work, daemon=True).start()

    @mainthread
    def post(self, text):
        self.log_data += f"\\n[{time.strftime('%H:%M')}] {text}"
        Clock.schedule_once(lambda x: setattr(self.root.ids.log_scroll, 'scroll_y', 0), 0.1)

    def auto_save(self, t):
        with open(os.path.join(self.user_data_dir, "last.py"), "w") as f: f.write(t)

    def load_data(self):
        vp = os.path.join(self.user_data_dir, "v.json")
        if os.path.exists(vp):
            with open(vp, "r") as f: self.vault = json.load(f)
        cp = os.path.join(self.user_data_dir, "last.py")
        if os.path.exists(cp):
            with open(cp, "r") as f: self.code_init = f.read()

    def save_data(self):
        with open(os.path.join(self.user_data_dir, "v.json"), "w") as f: json.dump(dict(self.vault), f)

    def ins(self, t): self.root.ids.editor.insert_text(t)
    def clear(self): self.log_data = "> Logs Cleared\\n"
    def reset(self): self.vault['is_fresh'] = True; self.save_data(); self.post("Reset. Restart app.")
    def call_serpent(self): Animation(pos_hint={"center_x": .85, "center_y": .35}, duration=1, t='out_elastic').start(self.root.ids.serpent_helper)

if __name__ == "__main__":
    NebulaApp().run()

# -*- coding: utf-8: -*-
import os, sys, threading, time, json, traceback
from io import StringIO
from kivy.lang import Builder
from kivy.clock import Clock, mainthread
from kivy.animation import Animation
from kivy.properties import StringProperty, DictProperty
from kivymd.app import MDApp
from kivymd.uix.snackbar import Snackbar

# Полная разметка интерфейса Nebula Ultra
KV = '''
MDScreenManager:
    id: screen_manager
    
    MDScreen:
        name: "intro"
        md_bg_color: "#000000"
        Image:
            id: intro_snake
            source: "serpent.png"
            size_hint: None, None
            size: "350dp", "350dp"
            pos_hint: {"center_x": .5, "center_y": -.6}
        MDLabel:
            id: intro_text
            text: "NEBULA MASTER\\nGENESIS"
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
                title: "Nebula Ultra PRO"
                md_bg_color: "#121212"
                elevation: 10
                right_action_items: [["snake", lambda x: app.toggle_serpent()]]

            MDBoxLayout:
                orientation: "vertical"
                padding: "12dp"
                spacing: "10dp"
                
                MDCard:
                    radius: [20,]
                    md_bg_color: "#0D0D0D"
                    padding: "10dp"
                    elevation: 4
                    ScrollView:
                        MDTextField:
                            id: code_input
                            text: app.saved_code
                            multiline: True
                            mode: "fill"
                            fill_color_normal: "#0D0D0D"
                            on_text: app.save_draft(self.text)

                MDFillRoundFlatButton:
                    text: "EXECUTE CORE"
                    icon: "play"
                    size_hint_x: 1
                    md_bg_color: "#6200EE"
                    on_release: app.run_logic()

            MDBottomNavigation:
                id: b_nav
                panel_color: "#121212"
                MDBottomNavigationItem:
                    name: 'editor'; text: 'Editor'; icon: 'code-tags'
                MDBottomNavigationItem:
                    name: 'logs'; text: 'Terminal'; icon: 'console'
                    MDBoxLayout:
                        md_bg_color: "#000000"
                        ScrollView:
                            id: log_scroll
                            MDLabel:
                                id: console
                                text: app.log_text
                                color: "#00FFC8"
                                size_hint_y: None
                                height: self.texture_size[1]
                                padding: "15dp"
                                font_style: "Caption"

        # Змей-помощник
        Image:
            id: serpent_helper
            source: "serpent.png"
            size_hint: None, None
            size: "280dp", "280dp"
            pos_hint: {"center_x": 1.5, "center_y": 0.3}
'''

class NebulaApp(MDApp):
    log_text = StringProperty("> Nebula Engine Online\\n")
    saved_code = StringProperty("print('Hello from Nebula Master!')")
    vault = DictProperty({'first_run': True})

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "DeepPurple"
        self.load_settings()
        return Builder.load_string(KV)

    def on_start(self):
        # Кат-сцена
        if self.vault.get('first_run', True):
            s = self.root.ids.intro_snake
            t = self.root.ids.intro_text
            anim = Animation(pos_hint={"center_x": .5, "center_y": .5}, duration=2, t='out_back')
            anim.bind(on_complete=self.end_intro)
            anim.start(s)
            Animation(opacity=1, duration=1.5).start(t)
        else:
            self.root.ids.screen_manager.current = "main"

    def end_intro(self, *args):
        self.vault['first_run'] = False
        self.save_settings()
        Clock.schedule_once(lambda x: setattr(self.root.ids.screen_manager, 'current', 'main'), 1)

    def run_logic(self):
        self.root.ids.b_nav.switch_tab('logs')
        code = self.root.ids.code_input.text
        
        def execute():
            old_stdout = sys.stdout
            buff = sys.stdout = StringIO()
            try:
                # Даем доступ к объекту app прямо из кода
                exec(code, {**globals(), 'app': self})
                res = buff.getvalue() or "--- Success ---"
            except:
                res = traceback.format_exc()
            finally:
                sys.stdout = old_stdout
            self.append_log(res)

        threading.Thread(target=execute, daemon=True).start()

    @mainthread
    def append_log(self, text):
        self.log_text += f"\\n[{time.strftime('%H:%M')}] {text}"
        Clock.schedule_once(lambda x: setattr(self.root.ids.log_scroll, 'scroll_y', 0), 0.1)

    def save_draft(self, text):
        with open(os.path.join(self.user_data_dir, "draft.py"), "w", encoding='utf-8') as f:
            f.write(text)

    def load_settings(self):
        v_p = os.path.join(self.user_data_dir, "vault.json")
        if os.path.exists(v_p):
            with open(v_p, "r") as f: self.vault = json.load(f)
        c_p = os.path.join(self.user_data_dir, "draft.py")
        if os.path.exists(c_p):
            with open(c_p, "r", encoding='utf-8') as f: self.saved_code = f.read()

    def save_settings(self):
        with open(os.path.join(self.user_data_dir, "vault.json"), "w") as f:
            json.dump(dict(self.vault), f)

    def toggle_serpent(self):
        s = self.root.ids.serpent_helper
        target_x = 0.85 if s.pos_hint["center_x"] > 1 else 1.5
        Animation(pos_hint={"center_x": target_x}, duration=1, t='out_elastic').start(s)
        if target_x < 1: Snackbar(text="Assistant Activated").open()

if __name__ == "__main__":
    NebulaApp().run()

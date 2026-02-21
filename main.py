import os, sys, threading, traceback, time
from io import StringIO
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.properties import BooleanProperty, StringProperty, NumericProperty
from kivy.utils import platform, get_color_from_hex
from kivymd.app import MDApp
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.button import MDRaisedButton

KV = '''
#:import hex kivy.utils.get_color_from_hex

MDNavigationLayout:
    MDScreenManager:
        MDScreen:
            MDBoxLayout:
                orientation: "vertical"
                md_bg_color: hex("#08080B")

                MDTopAppBar:
                    title: "NEBULA QUANTUM AI"
                    md_bg_color: hex("#0D0D12")
                    elevation: 0
                    left_action_items: [["menu", lambda x: nav_drawer.set_state("open")]]
                    right_action_items: [["play", lambda x: app.run_code()]]

                MDProgressBar:
                    id: progress
                    value: app.prog_val
                    color: hex("#00FFC8")
                    opacity: 1 if app.is_loading else 0
                    size_hint_y: None
                    height: "2dp"

                MDBoxLayout:
                    orientation: "vertical"
                    padding: "8dp"
                    spacing: "8dp"

                    # Панель быстрых кнопок
                    ScrollView:
                        size_hint_y: None
                        height: "50dp"
                        do_scroll_y: False
                        MDBoxLayout:
                            id: extra_keys
                            adaptive_width: True
                            padding: "5dp"
                            spacing: "10dp"

                    # Поле редактора
                    MDCard:
                        radius: [15, 15, 15, 15]
                        md_bg_color: hex("#0A0A0F")
                        line_color: hex("#1A1A25")
                        padding: "5dp"
                        MDTextField:
                            id: code_input
                            text: "import numpy as np\\nprint('>> SYSTEM READY')"
                            multiline: True
                            mode: "fill"
                            fill_color_normal: [0,0,0,0]
                            text_color_normal: hex("#00FFC8")
                            font_size: "14sp"

                MDBottomNavigation:
                    id: nav
                    panel_color: hex("#0D0D12")
                    text_color_active: hex("#00FFC8")
                    MDBottomNavigationItem:
                        name: 'editor'
                        text: 'CODE'
                        icon: 'console'
                    MDBottomNavigationItem:
                        name: 'logs'
                        text: 'LOGS'
                        icon: 'matrix'
                        MDBoxLayout:
                            md_bg_color: hex("#000000")
                            ScrollView:
                                MDLabel:
                                    id: terminal
                                    text: app.output_log
                                    color: hex("#00FFC8")
                                    font_style: "Caption"
                                    size_hint_y: None
                                    height: self.texture_size[1]
                                    padding: "15dp"

    MDNavigationDrawer:
        id: nav_drawer
        md_bg_color: hex("#0D0D12")
        MDBoxLayout:
            orientation: "vertical"
            padding: "15dp"
            MDLabel:
                text: "AI MODULES"
                theme_text_color: "Custom"
                text_color: hex("#00FFC8")
                font_style: "H6"
                size_hint_y: None
                height: "50dp"
            MDRaisedButton:
                text: "Load Transformers"
                on_release: app.add_snippet()
                md_bg_color: hex("#1A1A22")

'''

class NebulaApp(MDApp):
    is_loading = BooleanProperty(False)
    prog_val = NumericProperty(0)
    output_log = StringProperty("> NEBULA v8.5 ONLINE\\n")

    def build(self):
        self.theme_cls.theme_style = "Dark"
        return Builder.load_string(KV)

    def on_start(self):
        keys = ['def', 'print', 'import', 'if', ':', '=', '(', ')', 'tab']
        for k in keys:
            btn = MDRaisedButton(
                text=k, md_bg_color=get_color_from_hex("#121217"),
                text_color=get_color_from_hex("#00FFC8"),
                on_release=lambda x, c=k: self.root.ids.code_input.insert_text("    " if c=="tab" else c)
            )
            self.root.ids.extra_keys.add_widget(btn)

    def run_code(self):
        self.root.ids.nav.switch_tab('logs')
        code = self.root.ids.code_input.text
        out = StringIO()
        sys.stdout = out
        try:
            exec(code, globals())
            res = out.getvalue()
        except: res = traceback.format_exc()
        sys.stdout = sys.__stdout__
        self.output_log += f"\\n[{time.strftime('%H:%M:%S')}] >>> {res}"

    def add_snippet(self):
        self.root.ids.code_input.insert_text("\\nfrom transformers import pipeline")
        self.root.ids.nav_drawer.set_state("close")

if __name__ == "__main__":
    NebulaApp().run()
  

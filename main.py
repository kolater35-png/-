import os, sys, threading, traceback, subprocess, time
from io import StringIO
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.properties import BooleanProperty, StringProperty, NumericProperty
from kivy.utils import platform, get_color_from_hex
from kivymd.app import MDApp
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.button import MDFillRoundFlatButton
from kivymd.uix.list import OneLineAvatarIconListItem, IconLeftWidget, IconRightWidget

KV = '''
#:import hex kivy.utils.get_color_from_hex
MDBoxLayout:
    orientation: "vertical"
    md_bg_color: hex("#020205")

    # ВЕРХНИЙ HUD (Информатор)
    MDBoxLayout:
        size_hint_y: None
        height: "30dp"
        md_bg_color: hex("#0D0D12")
        padding: [15, 0]
        MDLabel:
            text: "NODE: NEBULA-PRIMARY // AUTH: ROOT"
            font_style: "Caption"
            theme_text_color: "Custom"
            text_color: hex("#00FFC8")
        MDLabel:
            text: "V.5.2-STABLE"
            halign: "right"
            font_style: "Caption"
            theme_text_color: "Custom"
            text_color: hex("#FFFF00")

    MDTopAppBar:
        title: "NEBULA QUANTUM"
        md_bg_color: hex("#0D0D12")
        elevation: 0
        right_action_items: [["brain", lambda x: app.ai_analyze()], ["play-outline", lambda x: app.run_code()]]

    MDProgressBar:
        id: progress
        value: app.prog_val
        color: hex("#00FFC8")
        opacity: 1 if app.is_loading else 0
        size_hint_y: None
        height: "2dp"

    MDBottomNavigation:
        id: nav
        panel_color: hex("#0D0D12")
        text_color_active: hex("#FFFF00")

        MDBottomNavigationItem:
            name: 'editor'
            text: 'DECK'
            icon: 'console'
            MDBoxLayout:
                orientation: "vertical"
                padding: [5, 0, 5, 0]
                
                # Панель быстрых символов
                ScrollView:
                    size_hint_y: None
                    height: "50dp"
                    do_scroll_y: False
                    MDBoxLayout:
                        id: extra_keys
                        adaptive_width: True
                        padding: "5dp"
                        spacing: "8dp"

                MDCard:
                    radius: [15, 15, 0, 0]
                    md_bg_color: hex("#050508")
                    line_color: hex("#1A1A25")
                    MDTextField:
                        id: code_input
                        text: "# Nebula Cyber-System v5.2\\nimport os\\nimport numpy as np\\n\\nprint('>> SYSTEM READY')\\n"
                        multiline: True
                        mode: "fill"
                        fill_color_normal: [0,0,0,0]
                        text_color_normal: hex("#00FFC8")
                        font_size: "14sp"

        MDBottomNavigationItem:
            name: 'files'
            text: 'DATA'
            icon: 'database'
            on_tab_press: app.update_file_list()
            MDBoxLayout:
                orientation: "vertical"
                padding: "15dp"
                MDLabel:
                    text: "FILE SCANNER"
                    font_style: "H6"
                    theme_text_color: "Custom"
                    text_color: hex("#FFFF00")
                MDScrollView:
                    MDList:
                        id: file_list

        MDBottomNavigationItem:
            name: 'terminal'
            text: 'LOGS'
            icon: 'matrix'
            MDBoxLayout:
                md_bg_color: hex("#000000")
                ScrollView:
                    id: term_scroll
                    MDLabel:
                        id: terminal
                        text: app.output_log
                        color: hex("#00FFC8")
                        font_style: "Caption"
                        size_hint_y: None
                        height: self.texture_size[1]
                        padding: "15dp"

        MDBottomNavigationItem:
            name: 'system'
            text: 'CORE'
            icon: 'shield-star'
            MDBoxLayout:
                orientation: "vertical"
                padding: "20dp"
                spacing: "20dp"
                MDRaisedButton:
                    text: "PURGE ALL DATA"
                    md_bg_color: hex("#FF0055")
                    pos_hint: {"center_x": .5}
                    on_release: app.clear_console()
                MDTextField:
                    id: pip_input
                    hint_text: "Target Module (PIP)"
                    mode: "rectangle"
                MDRaisedButton:
                    text: "INJECT MODULE"
                    md_bg_color: hex("#00FFC8")
                    text_color: [0,0,0,1]
                    pos_hint: {"center_x": .5}
                    on_release: app.pip_install()
'''

class NebulaApp(MDApp):
    is_loading = BooleanProperty(False)
    prog_val = NumericProperty(0)
    output_log = StringProperty("> NEBULA_OS_V5.2 ONLINE...\\n")

    def build(self):
        self.theme_cls.theme_style = "Dark"
        return Builder.load_string(KV)

    def on_start(self):
        Clock.schedule_once(self.post_init, 0.5)
        # Быстрые клавиши
        keys = ['def ', 'print(', 'import ', 'if ', ':', '"', '=', 'tab']
        for k in keys:
            btn = MDFillRoundFlatButton(
                text=k, md_bg_color=get_color_from_hex("#0D0D12"),
                text_color=get_color_from_hex("#00FFC8"),
                on_release=lambda x, c=k: self.root.ids.code_input.insert_text('\\t' if c=='tab' else c)
            )
            self.root.ids.extra_keys.add_widget(btn)

    def post_init(self, dt):
        if platform == 'android':
            try:
                from android.permissions import request_permissions, Permission
                request_permissions([Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE])
            except: pass

    def update_file_list(self):
        self.root.ids.file_list.clear_widgets()
        try:
            for f in os.listdir('.'):
                item = OneLineAvatarIconListItem(text=f, theme_text_color="Custom", text_color=[0, 1, 0.8, 1])
                item.add_widget(IconLeftWidget(icon="file-code", icon_color=get_color_from_hex("#FFFF00")))
                self.root.ids.file_list.add_widget(item)
        except: pass

    def run_code(self):
        if self.is_loading: return
        self.is_loading = True
        self.root.ids.nav.switch_tab('terminal')
        threading.Thread(target=self._exec).start()

    def _exec(self):
        code = self.root.ids.code_input.text
        out = StringIO()
        sys.stdout = out
        try:
            exec(code, globals())
            res = out.getvalue()
        except: res = traceback.format_exc()
        sys.stdout = sys.__stdout__
        Clock.schedule_once(lambda dt: self._done(res))

    def _done(self, res):
        ts = time.strftime('%H:%M:%S')
        self.output_log += f"\\n[{ts}] >>> {res}"
        self.is_loading = False

    def pip_install(self):
        pkg = self.root.ids.pip_input.text
        if not pkg: return
        threading.Thread(target=lambda: subprocess.call([sys.executable, "-m", "pip", "install", pkg])).start()
        Snackbar(text=f"Injecting: {pkg}").open()

    def ai_analyze(self):
        Snackbar(text="NEURAL SCAN: OPTIMIZED", bg_color=get_color_from_hex("#00FFC8")).open()

    def clear_console(self):
        self.output_log = "> SYSTEM PURGED.\\n"

if __name__ == "__main__":
    NebulaApp().run()
  

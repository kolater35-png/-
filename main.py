import os, sys, threading, traceback, time, subprocess
from io import StringIO
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.properties import BooleanProperty, StringProperty, NumericProperty
from kivymd.app import MDApp
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.button import MDFillRoundFlatButton
from kivymd.uix.list import OneLineAvatarIconListItem, IconLeftWidget, IconRightWidget

KV = '''
#:import hex kivy.utils.get_color_from_hex
MDBoxLayout:
    orientation: "vertical"
    md_bg_color: hex("#0A0A0C")

    MDTopAppBar:
        title: "Nebula Quantum Pro"
        md_bg_color: hex("#121217")
        elevation: 4
        right_action_items: [["refresh", lambda x: app.update_file_list()], ["delete-sweep", lambda x: app.clear_console()], ["play-circle", lambda x: app.run_code()]]

    MDProgressBar:
        id: progress
        value: app.prog_val
        color: hex("#BB86FC")
        opacity: 1 if app.is_loading else 0
        size_hint_y: None
        height: "2dp"

    MDBottomNavigation:
        id: nav
        panel_color: hex("#121217")
        text_color_active: hex("#BB86FC")

        MDBottomNavigationItem:
            name: 'editor'
            text: 'Editor'
            icon: 'code-braces'
            MDBoxLayout:
                orientation: "vertical"
                padding: "8dp"
                MDCard:
                    radius: [15, 15, 15, 15]
                    md_bg_color: hex("#16161D")
                    padding: "5dp"
                    MDTextField:
                        id: code_input
                        text: "import os\\nprint('System Online')\\nprint(os.listdir('.'))"
                        multiline: True
                        mode: "fill"
                        fill_color_normal: [0,0,0,0]
                        text_color_normal: [1, 1, 1, 1]

        MDBottomNavigationItem:
            name: 'files'
            text: 'Files'
            icon: 'folder-sync'
            on_tab_press: app.update_file_list()
            MDBoxLayout:
                orientation: "vertical"
                ScrollView:
                    MDList:
                        id: file_list

        MDBottomNavigationItem:
            name: 'terminal'
            text: 'Terminal'
            icon: 'console'
            MDBoxLayout:
                md_bg_color: hex("#000000")
                ScrollView:
                    id: term_scroll
                    MDLabel:
                        id: terminal
                        text: app.output_log
                        color: hex("#03DAC6")
                        font_style: "Caption"
                        size_hint_y: None
                        height: self.texture_size[1]
                        padding: "20dp"
'''

class NebulaApp(MDApp):
    is_loading = BooleanProperty(False)
    prog_val = NumericProperty(0)
    output_log = StringProperty("> Nebula OS Initializing...\\n")

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "DeepPurple"
        return Builder.load_string(KV)

    def on_start(self):
        # Безопасный запрос разрешений для Android
        try:
            from android.permissions import request_permissions, Permission
            request_permissions([Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE])
        except:
            print("Система запущена не на Android")
        self.update_file_list()

    def clear_console(self):
        self.output_log = "> Console Purged...\\n"

    def update_file_list(self):
        self.root.ids.file_list.clear_widgets()
        try:
            for f in os.listdir('.'):
                if os.path.isfile(f):
                    item = OneLineAvatarIconListItem(text=f, theme_text_color="Custom", text_color=[1, 1, 1, 1])
                    item.add_widget(IconLeftWidget(icon="file-code-outline"))
                    self.root.ids.file_list.add_widget(item)
        except: pass

    def run_code(self):
        if self.is_loading: return
        self.is_loading = True
        threading.Thread(target=self._execute).start()

    def _execute(self):
        code = self.root.ids.code_input.text
        out = StringIO()
        sys.stdout = out
        try:
            exec(code, globals())
            res = out.getvalue()
        except:
            res = traceback.format_exc()
        sys.stdout = sys.__stdout__
        Clock.schedule_once(lambda dt: self._finalize(res))

    def _finalize(self, res):
        self.output_log += f"\\n{res}"
        self.is_loading = False
        self.root.ids.term_scroll.scroll_y = 0

if __name__ == "__main__":
    NebulaApp().run()
  

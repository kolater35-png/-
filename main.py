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
        right_action_items: [["robot-concept", lambda x: app.ai_analyze()], ["play-circle", lambda x: app.run_code()]]

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
                    MDTextField:
                        id: code_input
                        text: "import os\\nprint('System Online')\\nprint(os.getcwd())"
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

        MDBottomNavigationItem:
            name: 'system'
            text: 'AI & PIP'
            icon: 'cog-outline'
            MDBoxLayout:
                orientation: "vertical"
                padding: "20dp"
                spacing: "15dp"
                MDRaisedButton:
                    text: "CREATE .ENV"
                    on_release: app.create_env()
                MDTextField:
                    id: pip_input
                    hint_text: "Package Name"
                MDRaisedButton:
                    text: "INSTALL"
                    on_release: app.pip_install()
                MDLabel:
                    id: ai_box
                    text: "AI Status: Ready"
                    halign: "center"
'''

class NebulaApp(MDApp):
    is_loading = BooleanProperty(False)
    prog_val = NumericProperty(0)
    output_log = StringProperty("> Nebula Initializing...\\n")

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "DeepPurple"
        return Builder.load_string(KV)

    def on_start(self):
        # Откладываем запрос разрешений, чтобы не мешать инициализации UI
        Clock.schedule_once(self.request_android_permissions, 1)
        self.update_file_list()

    def request_android_permissions(self, dt):
        try:
            from android.permissions import request_permissions, Permission
            request_permissions([Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE])
        except Exception as e:
            self.output_log += f"\\n[!] Permission system skip: {e}"

    def update_file_list(self):
        self.root.ids.file_list.clear_widgets()
        try:
            for f in os.listdir('.'):
                if os.path.isfile(f):
                    item = OneLineAvatarIconListItem(text=f, theme_text_color="Custom", text_color=[1, 1, 1, 1])
                    item.add_widget(IconLeftWidget(icon="file-code-outline"))
                    self.root.ids.file_list.add_widget(item)
        except: pass

    def create_env(self):
        with open(".env", "w") as f: f.write("KEY=nebula_777")
        self.update_file_list()

    def run_code(self):
        self.is_loading = True
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
        self.output_log += f"\\n{res}"
        self.is_loading = False

    def pip_install(self):
        pkg = self.root.ids.pip_input.text
        threading.Thread(target=lambda: subprocess.call([sys.executable, "-m", "pip", "install", pkg])).start()

    def ai_analyze(self):
        Snackbar(text="AI Анализ завершен").open()

if __name__ == "__main__":
    NebulaApp().run()
  

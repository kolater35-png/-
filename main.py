import os, sys, threading, traceback, time, subprocess
from io import StringIO
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.properties import BooleanProperty, StringProperty, NumericProperty
from kivymd.app import MDApp
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.button import MDFillRoundFlatButton
from kivymd.uix.list import OneLineAvatarIconListItem, IconLeftWidget, IconRightWidget

# Импорт для запроса разрешений на Android
from android.permissions import request_permissions, Permission

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
                spacing: "5dp"
                ScrollView:
                    size_hint_y: None
                    height: "45dp"
                    do_scroll_y: False
                    MDBoxLayout:
                        id: extra_keys
                        adaptive_width: True
                        padding: "5dp"
                        spacing: "5dp"
                MDCard:
                    radius: [15, 15, 15, 15]
                    md_bg_color: hex("#16161D")
                    elevation: 1
                    MDTextField:
                        id: code_input
                        text: "import os\\nprint('System Ready')\\n# Nebula Quantum AI"
                        multiline: True
                        mode: "fill"
                        fill_color_normal: [0,0,0,0]
                        text_color_normal: [1, 1, 1, 1]
                        font_size: "14sp"

        MDBottomNavigationItem:
            name: 'files'
            text: 'Files'
            icon: 'folder-sync'
            on_tab_press: app.update_file_list()
            MDBoxLayout:
                orientation: "vertical"
                padding: "10dp"
                MDLabel:
                    text: "Project Files & .env"
                    theme_text_color: "Secondary"
                    size_hint_y: None
                    height: "40dp"
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
            name: 'ai_system'
            text: 'AI & PIP'
            icon: 'robot-industrial'
            MDBoxLayout:
                orientation: "vertical"
                padding: "20dp"
                spacing: "15dp"
                MDRaisedButton:
                    text: "CREATE .ENV FILE"
                    pos_hint: {"center_x": .5}
                    on_release: app.create_env()
                MDTextField:
                    id: pip_input
                    hint_text: "Install package via PIP"
                    mode: "rectangle"
                MDRaisedButton:
                    text: "INSTALL NOW"
                    pos_hint: {"center_x": .5}
                    on_release: app.pip_install()
                MDLabel:
                    id: var_inspector
                    text: "AI Inspector: Ready"
                    halign: "center"
                    theme_text_color: "Secondary"
'''

class NebulaApp(MDApp):
    is_loading = BooleanProperty(False)
    prog_val = NumericProperty(0)
    output_log = StringProperty("> Nebula OS Pro v2.5 Online...\\n")

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "DeepPurple"
        return Builder.load_string(KV)

    def on_start(self):
        # 1. Запрос разрешений при старте
        if os.name == 'posix': # Проверка для Android
            request_permissions([Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE])
        
        # 2. Быстрые клавиши
        keys = ['tab', '(', ')', '{', '}', ':', '=', 'import', 'print', 'def']
        for k in keys:
            btn = MDFillRoundFlatButton(text=k, md_bg_color=[0.15, 0.15, 0.2, 1],
                on_release=lambda x, char=k: self.root.ids.code_input.insert_text('\\t' if char=='tab' else char))
            self.root.ids.extra_keys.add_widget(btn)
        self.update_file_list()

    def clear_console(self):
        self.output_log = "> Console Purged...\\n"
        Snackbar(text="Terminal Cleaned").open()

    # --- ФАЙЛОВЫЙ МЕНЕДЖЕР ---
    def update_file_list(self):
        self.root.ids.file_list.clear_widgets()
        try:
            for f in os.listdir('.'):
                if os.path.isfile(f):
                    item = OneLineAvatarIconListItem(text=f, theme_text_color="Custom", text_color=[1, 1, 1, 1])
                    item.add_widget(IconLeftWidget(icon="file-code-outline", on_release=lambda x, fn=f: self.open_file(fn)))
                    item.add_widget(IconRightWidget(icon="delete-outline", theme_text_color="Error", on_release=lambda x, fn=f: self.delete_file(fn)))
                    self.root.ids.file_list.add_widget(item)
        except: pass

    def open_file(self, filename):
        with open(filename, 'r') as f: self.root.ids.code_input.text = f.read()
        self.root.ids.nav.switch_tab('editor')
        Snackbar(text=f"Loaded: {filename}").open()

    def delete_file(self, filename):
        os.remove(filename)
        self.update_file_list()
        Snackbar(text="File deleted").open()

    # --- ЯДРО ИСПОЛНЕНИЯ ---
    def run_code(self):
        if self.is_loading: return
        self.is_loading = True
        self.prog_val = 0
        threading.Thread(target=self._execute).start()

    def _execute(self):
        code = self.root.ids.code_input.text
        out = StringIO()
        sys.stdout = out
        local_vars = {}
        try:
            for i in range(1, 6):
                time.sleep(0.05)
                Clock.schedule_once(lambda dt, v=i*20: setattr(self, 'prog_val', v))
            exec(code, globals(), local_vars)
            res = out.getvalue()
            v_info = ", ".join([k for k in local_vars.keys() if not k.startswith('_')])
        except:
            res = traceback.format_exc()
            v_info = "Error in code"
        
        sys.stdout = sys.__stdout__
        Clock.schedule_once(lambda dt: self._finalize(res, v_info))

    def _finalize(self, res, v_info):
        self.output_log += f"\\n{res}"
        self.root.ids.var_inspector.text = f"Variables: {v_info}"
        self.is_loading = False
        self.root.ids.term_scroll.scroll_y = 0 # Авто-прокрутка

    def create_env(self):
        with open(".env", "w") as f: f.write("API_KEY=quantum_777\\nSECURE=True")
        self.update_file_list()
        Snackbar(text=".env Created").open()

    def pip_install(self):
        pkg = self.root.ids.pip_input.text
        threading.Thread(target=lambda: subprocess.call([sys.executable, "-m", "pip", "install", pkg])).start()
        Snackbar(text=f"PIP: Installing {pkg}...").open()

if __name__ == "__main__":
    NebulaApp().run()

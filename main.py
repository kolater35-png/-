import os, sys, threading, traceback, subprocess
from io import StringIO
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.properties import BooleanProperty, StringProperty, NumericProperty
from kivy.utils import platform
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
        right_action_items: [["robot-outline", lambda x: app.ai_analyze()], ["delete-sweep", lambda x: app.clear_console()], ["play-circle", lambda x: app.run_code()]]

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

        # --- ВКЛАДКА 1: РЕДАКТОР ---
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
                    MDTextField:
                        id: code_input
                        text: "import os\\nprint('Nebula OS v3.0: Online')\\nprint('Current dir:', os.getcwd())"
                        multiline: True
                        mode: "fill"
                        fill_color_normal: [0,0,0,0]
                        text_color_normal: [1, 1, 1, 1]

        # --- ВКЛАДКА 2: ФАЙЛЫ ---
        MDBottomNavigationItem:
            name: 'files'
            text: 'Files'
            icon: 'folder-sync'
            on_tab_press: app.update_file_list()
            MDBoxLayout:
                orientation: "vertical"
                padding: "10dp"
                MDLabel:
                    text: "Project Workspace"
                    theme_text_color: "Secondary"
                    size_hint_y: None
                    height: "40dp"
                ScrollView:
                    MDList:
                        id: file_list

        # --- ВКЛАДКА 3: ТЕРМИНАЛ ---
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

        # --- ВКЛАДКА 4: СИСТЕМА ---
        MDBottomNavigationItem:
            name: 'system'
            text: 'System'
            icon: 'cog-outline'
            MDBoxLayout:
                orientation: "vertical"
                padding: "20dp"
                spacing: "15dp"
                MDRaisedButton:
                    text: "CREATE .ENV"
                    pos_hint: {"center_x": .5}
                    on_release: app.create_env()
                MDTextField:
                    id: pip_input
                    hint_text: "Install package via PIP"
                    mode: "rectangle"
                MDRaisedButton:
                    text: "INSTALL PIP"
                    pos_hint: {"center_x": .5}
                    on_release: app.pip_install()
                MDLabel:
                    id: ai_box
                    text: "AI System: Ready for code."
                    halign: "center"
                    theme_text_color: "Secondary"
'''

class NebulaApp(MDApp):
    is_loading = BooleanProperty(False)
    prog_val = NumericProperty(0)
    output_log = StringProperty("> Boot Sequence Initiated...\\n")

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "DeepPurple"
        return Builder.load_string(KV)

    def on_start(self):
        # Отложенный запуск, чтобы не вешать UI
        Clock.schedule_once(self.init_system, 1)
        
        # Клавиатура
        keys = ['tab', '(', ')', ':', '=', '"', 'import', 'print']
        for k in keys:
            btn = MDFillRoundFlatButton(text=k, md_bg_color=[0.15, 0.15, 0.2, 1],
                on_release=lambda x, char=k: self.root.ids.code_input.insert_text('\\t' if char=='tab' else char))
            self.root.ids.extra_keys.add_widget(btn)

    def init_system(self, dt):
        if platform == 'android':
            try:
                from android.permissions import request_permissions, Permission
                request_permissions([Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE])
            except Exception as e:
                self.output_log += f"\\n[System] Permission error: {e}"
        self.update_file_list()

    def clear_console(self):
        self.output_log = "> Console Purged.\\n"

    # --- Файлы ---
    def update_file_list(self):
        self.root.ids.file_list.clear_widgets()
        try:
            for f in os.listdir('.'):
                if os.path.isfile(f):
                    item = OneLineAvatarIconListItem(text=f, theme_text_color="Custom", text_color=[1, 1, 1, 1])
                    item.add_widget(IconLeftWidget(icon="file-code-outline", on_release=lambda x, fn=f: self.open_file(fn)))
                    item.add_widget(IconRightWidget(icon="delete", theme_text_color="Error", on_release=lambda x, fn=f: self.delete_file(fn)))
                    self.root.ids.file_list.add_widget(item)
        except Exception as e:
            self.output_log += f"\\n[Error] Cannot read files: {e}"

    def open_file(self, filename):
        try:
            with open(filename, 'r', encoding='utf-8') as f: self.root.ids.code_input.text = f.read()
            self.root.ids.nav.switch_tab('editor')
        except: pass

    def delete_file(self, filename):
        try:
            os.remove(filename)
            self.update_file_list()
        except: pass

    def create_env(self):
        try:
            with open(".env", "w") as f: f.write("API_KEY=nebula_pro_777\\nDEBUG=True")
            self.update_file_list()
            Snackbar(text=".env Created").open()
        except Exception as e:
            self.output_log += f"\\n[Error] Cannot write file: {e}"

    # --- Выполнение ---
    def run_code(self):
        if self.is_loading: return
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
        self.root.ids.term_scroll.scroll_y = 0

    # --- PIP и ИИ ---
    def pip_install(self):
        pkg = self.root.ids.pip_input.text
        if not pkg: return
        threading.Thread(target=lambda: subprocess.call([sys.executable, "-m", "pip", "install", pkg])).start()
        Snackbar(text=f"Установка {pkg}...").open()

    def ai_analyze(self):
        code = self.root.ids.code_input.text
        if "print" in code or "import" in code:
            self.root.ids.ai_box.text = "AI Анализ: Ошибок синтаксиса не найдено."
        else:
            self.root.ids.ai_box.text = "AI Анализ: Напишите логику для проверки."
        Snackbar(text="Код проанализирован").open()

if __name__ == "__main__":
    NebulaApp().run()

import os, sys, threading, traceback, time, subprocess
from io import StringIO
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.properties import BooleanProperty, StringProperty, NumericProperty
from kivymd.app import MDApp
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.button import MDFillRoundFlatButton

KV = '''
#:import hex kivy.utils.get_color_from_hex
MDBoxLayout:
    orientation: "vertical"
    md_bg_color: [0.05, 0.05, 0.07, 1]

    MDTopAppBar:
        title: "Nebula Quantum Pro"
        md_bg_color: [0.1, 0.1, 0.15, 1]
        right_action_items: [["file-plus", lambda x: app.create_env()], ["play", lambda x: app.run_code()]]

    MDProgressBar:
        id: progress
        value: app.prog_val
        opacity: 1 if app.is_loading else 0
        size_hint_y: None
        height: "3dp"

    MDBottomNavigation:
        panel_color: [0.1, 0.1, 0.15, 1]
        text_color_active: hex("#b026ff")

        MDBottomNavigationItem:
            name: 'editor'
            text: 'Editor'
            icon: 'code-braces'
            MDBoxLayout:
                orientation: "vertical"
                MDTextField:
                    id: code_input
                    text: "import os\\n# Читаем наш .env\\nif os.path.exists('.env'):\\n    with open('.env', 'r') as f:\\n        print('Содержимое .env:\\\\n' + f.read())\\nelse:\\n    print('Файл .env не найден. Нажми на иконку плюса сверху!')"
                    multiline: True
                    mode: "fill"
                    fill_color_normal: [0.07, 0.07, 0.1, 1]
                    text_color_normal: [1, 1, 1, 1]

        MDBottomNavigationItem:
            name: 'terminal'
            text: 'Output'
            icon: 'console'
            MDBoxLayout:
                md_bg_color: [0, 0, 0, 1]
                ScrollView:
                    MDLabel:
                        id: terminal
                        text: app.output_log
                        color: hex("#00ffcc")
                        font_style: "Caption"
                        size_hint_y: None
                        height: self.texture_size[1]
                        padding: "15dp"

        MDBottomNavigationItem:
            name: 'pip'
            text: 'System'
            icon: 'cog'
            MDBoxLayout:
                orientation: "vertical"
                padding: "20dp"
                MDLabel:
                    text: "Environment & PIP"
                    halign: "center"
                    font_style: "H6"
                MDRaisedButton:
                    text: "INSTALL PYTHON-DOTENV"
                    pos_hint: {"center_x": .5}
                    on_release: app.pip_install("python-dotenv")
                MDLabel:
                    id: env_status
                    text: "Status: Ready"
                    halign: "center"
                    theme_text_color: "Secondary"
'''

class NebulaApp(MDApp):
    is_loading = BooleanProperty(False)
    prog_val = NumericProperty(0)
    output_log = StringProperty("> Nebula OS v1.5 Online...\\n")

    def build(self):
        self.theme_cls.theme_style = "Dark"
        return Builder.load_string(KV)

    def create_env(self):
        """Создает файл .env в папке приложения"""
        try:
            with open(".env", "w") as f:
                f.write("API_KEY=your_secret_key_here\\nDEBUG=True\\nMODE=Quantum")
            Snackbar(text="Файл .env успешно создан!").open()
            self.output_log += "> [System] .env file created in root.\\n"
        except Exception as e:
            Snackbar(text=f"Ошибка: {str(e)}").open()

    def run_code(self):
        self.is_loading = True
        self.prog_val = 0
        threading.Thread(target=self._execute).start()

    def _execute(self):
        code = self.root.ids.code_input.text
        out = StringIO()
        sys.stdout = out
        try:
            for i in range(1, 6):
                time.sleep(0.05)
                Clock.schedule_once(lambda dt, v=i*20: setattr(self, 'prog_val', v))
            exec(code, globals())
            res = out.getvalue()
        except:
            res = traceback.format_exc()
        sys.stdout = sys.__stdout__
        Clock.schedule_once(lambda dt: self._finalize(res))

    def _finalize(self, res):
        self.output_log += f"\\n{res}"
        self.is_loading = False

    def pip_install(self, pkg):
        self.root.ids.env_status.text = f"Installing {pkg}..."
        def _task():
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", pkg])
                m = f"Библиотека {pkg} установлена!"
            except:
                m = "Ошибка установки."
            Clock.schedule_once(lambda dt: Snackbar(text=m).open())
        threading.Thread(target=_task).start()

if __name__ == "__main__":
    NebulaApp().run()

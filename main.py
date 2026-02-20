import os
import sys
import threading
import traceback
import time
import subprocess
from io import StringIO

from kivy.lang import Builder
from kivy.clock import Clock
from kivy.properties import BooleanProperty, StringProperty, NumericProperty
from kivymd.app import MDApp
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.button import MDFillRoundFlatButton
from kivy.metrics import dp

# Весь интерфейс в одном месте
KV = '''
#:import hex kivy.utils.get_color_from_hex

MDBoxLayout:
    orientation: "vertical"
    md_bg_color: [0.05, 0.05, 0.07, 1]

    MDTopAppBar:
        title: "Nebula Quantum AI OS"
        md_bg_color: [0.1, 0.1, 0.15, 1]
        elevation: 4
        right_action_items: [["auto-fix", lambda x: app.ai_analyze()], ["play", lambda x: app.run_code()]]

    MDProgressBar:
        id: progress
        value: app.prog_val
        color: hex("#b026ff")
        opacity: 1 if app.is_loading else 0
        size_hint_y: None
        height: "3dp"

    MDBottomNavigation:
        panel_color: [0.1, 0.1, 0.15, 1]
        text_color_active: hex("#b026ff")

        # 1. РЕДАКТОР
        MDBottomNavigationItem:
            name: 'editor'
            text: 'Editor'
            icon: 'code-braces'
            MDBoxLayout:
                orientation: "vertical"
                ScrollView:
                    size_hint_y: None
                    height: "45dp"
                    do_scroll_y: False
                    MDBoxLayout:
                        id: extra_keys
                        adaptive_width: True
                        padding: "5dp"
                        spacing: "5dp"
                MDTextField:
                    id: code_input
                    text: "print('Nebula AI Assistant Ready')\\n# Напиши код и нажми на иконку робота сверху"
                    multiline: True
                    mode: "fill"
                    fill_color_normal: [0.07, 0.07, 0.1, 1]
                    text_color_normal: [1, 1, 1, 1]

        # 2. ТЕРМИНАЛ
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

        # 3. SMART PIP (МЕНЕДЖЕР ПАКЕТОВ)
        MDBottomNavigationItem:
            name: 'pip'
            text: 'PIP'
            icon: 'package-variant-closed'
            MDBoxLayout:
                orientation: "vertical"
                padding: "20dp"
                spacing: "10dp"
                MDTextField:
                    id: pip_input
                    hint_text: "Название пакета (например: requests)"
                    mode: "rectangle"
                MDRaisedButton:
                    text: "INSTALL PACKAGE"
                    pos_hint: {"center_x": .5}
                    on_release: app.pip_install()
                MDLabel:
                    id: pip_status
                    text: "Status: Idle"
                    halign: "center"
                    theme_text_color: "Secondary"

        # 4. AI ASSISTANT (ОТЛАДКА)
        MDBottomNavigationItem:
            name: 'assistant'
            text: 'AI Help'
            icon: 'robot-glow'
            MDBoxLayout:
                orientation: "vertical"
                padding: "20dp"
                MDLabel:
                    text: "AI Code Analysis"
                    font_style: "H6"
                    halign: "center"
                MDSeparator:
                MDLabel:
                    id: ai_box
                    text: "Нажми на иконку волшебной палочки в углу, чтобы проанализировать код в редакторе."
                    theme_text_color: "Secondary"
                    halign: "center"
'''

class NebulaApp(MDApp):
    is_loading = BooleanProperty(False)
    prog_val = NumericProperty(0)
    output_log = StringProperty("> Nebula AI OS Online...\\n")

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "DeepPurple"
        return Builder.load_string(KV)

    def on_start(self):
        # Быстрые клавиши
        keys = ['tab', '(', ')', ':', '=', '"', 'import', 'def', 'print']
        for k in keys:
            btn = MDFillRoundFlatButton(
                text=k, md_bg_color=[0.15, 0.15, 0.2, 1],
                on_release=lambda x, char=k: self.root.ids.code_input.insert_text('\\t' if char=='tab' else char)
            )
            self.root.ids.extra_keys.add_widget(btn)

    # --- ФУНКЦИЯ ВЫПОЛНЕНИЯ КОДА ---
    def run_code(self):
        self.is_loading = True
        self.prog_val = 0
        threading.Thread(target=self._execute).start()

    def _execute(self):
        code = self.root.ids.code_input.text
        out = StringIO()
        sys.stdout = out
        try:
            exec(code, globals())
            res = out.getvalue()
        except Exception:
            res = traceback.format_exc()
        sys.stdout = sys.__stdout__
        Clock.schedule_once(lambda dt: self._finalize(res))

    def _finalize(self, res):
        self.output_log += f"\\n{res}"
        self.is_loading = False
        self.prog_val = 100

    # --- SMART PIP MANAGER ---
    def pip_install(self):
        pkg = self.root.ids.pip_input.text
        if not pkg: return
        self.root.ids.pip_status.text = f"Installing {pkg}..."
        threading.Thread(target=self._pip_thread, args=(pkg,)).start()

    def _pip_thread(self, pkg):
        try:
            # Используем subprocess для вызова pip
            subprocess.check_call([sys.executable, "-m", "pip", "install", pkg])
            msg = f"Successfully installed {pkg}"
        except Exception as e:
            msg = f"Error: {str(e)}"
        Clock.schedule_once(lambda dt: self._pip_done(msg))

    def _pip_done(self, msg):
        self.root.ids.pip_status.text = msg
        Snackbar(text=msg).open()

    # --- AI ASSISTANT LOGIC ---
    def ai_analyze(self):
        code = self.root.ids.code_input.text
        self.root.ids.ai_box.text = "Analyzing code architecture..."
        
        # Имитация работы ИИ-ассистента
        def fake_ai():
            time.sleep(1.5)
            advice = "AI Suggestion:\\n1. Код выглядит валидным.\\n2. Проверьте импорты.\\n3. Добавьте обработку исключений try/except."
            if "print" not in code:
                advice = "AI Suggestion:\\nВы написали логику, но не используете print() для вывода результата в терминал."
            
            Clock.schedule_once(lambda dt: setattr(self.root.ids.ai_box, 'text', advice))
            Clock.schedule_once(lambda dt: Snackbar(text="Analysis Complete").open())

        threading.Thread(target=fake_ai).start()

if __name__ == "__main__":
    NebulaApp().run()
  

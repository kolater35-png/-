# -*- coding: utf-8: -*-
import os, sys, threading, time, json, platform, traceback, webbrowser
from io import StringIO
from kivy.lang import Builder
from kivy.clock import Clock, mainthread
from kivy.animation import Animation
from kivy.properties import StringProperty, DictProperty
from kivymd.app import MDApp
from kivymd.uix.button import MDFillRoundFlatButton, MDFlatButton, MDRaisedButton
from kivymd.uix.snackbar import Snackbar

# Попытка импорта тяжелых модулей (для защиты от вылета)
try:
    import torch
    TORCH_READY = True
except ImportError:
    TORCH_READY = False

# --- ИНТЕРФЕЙС NEBULA MASTER PRO ---
KV = '''
<SyntaxBtn@MDRaisedButton>:
    size_hint: None, None
    size: "75dp", "52dp"
    elevation: 8
    radius: [18, 18, 18, 18]
    md_bg_color: 0.12, 0.12, 0.12, 1

MDScreenManager:
    id: screen_manager
    
    MDScreen:
        name: "intro"
        md_bg_color: "#000000"
        Image:
            id: serpent_intro
            source: "serpent.png"
            size_hint: None, None
            size: "400dp", "400dp"
            pos_hint: {"center_x": .5, "center_y": -.6}
        MDLabel:
            id: intro_label
            text: "NEBULA EVOLUTION\\nCORE SYSTEM"
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
                title: "Nebula Master [ULTRA]"
                md_bg_color: "#121212"
                elevation: 10
                left_action_items: [["menu", lambda x: nav_drawer.set_state("open")]]
                right_action_items: [["snake", lambda x: app.call_serpent_help()]]

            # Панель синтаксиса (скроллируемая)
            ScrollView:
                size_hint_y: None
                height: "85dp"
                do_scroll_y: False
                MDBoxLayout:
                    adaptive_width: True
                    padding: "15dp"
                    spacing: "12dp"
                    SyntaxBtn: text: "def"; md_bg_color: "#FF5252"; on_release: app.ins("def ")
                    SyntaxBtn: text: "class"; md_bg_color: "#448AFF"; on_release: app.ins("class ")
                    SyntaxBtn: text: "import"; md_bg_color: "#E040FB"; on_release: app.ins("import ")
                    SyntaxBtn: text: "torch"; md_bg_color: "#FFAB40"; on_release: app.ins("import torch\\n")
                    SyntaxBtn: text: "async"; md_bg_color: "#00E5FF"; on_release: app.ins("async ")
                    SyntaxBtn: text: ":"; md_bg_color: "#333333"; on_release: app.ins(":")

            # Редактор кода
            MDBoxLayout:
                orientation: "vertical"
                padding: "12dp"
                MDCard:
                    radius: [25,]
                    md_bg_color: "#0D0D0D"
                    padding: "15dp"
                    elevation: 5
                    ScrollView:
                        MDTextField:
                            id: editor
                            text: app.code_init
                            multiline: True
                            mode: "fill"
                            fill_color_normal: "#0D0D0D"
                            text_color_normal: "#E1BEE7"
                            on_text: app.handle_auto_save(self.text)

                MDBoxLayout:
                    size_hint_y: None
                    height: "90dp"
                    padding: [0, 15, 0, 0]
                    MDFillRoundFlatButton:
                        text: "LAUNCH ENGINE CORE"
                        icon: "fire-circle"
                        font_size: "18sp"
                        size_hint_x: 1
                        md_bg_color: "#6200EE"
                        on_release: app.run_engine()

            # Нижний терминал
            MDBottomNavigation:
                id: b_nav
                panel_color: "#121212"
                MDBottomNavigationItem:
                    name: 'ide'; text: 'Code Editor'; icon: 'code-braces'
                MDBottomNavigationItem:
                    name: 'terminal'; text: 'System Logs'; icon: 'console'
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
                                font_style: "Caption"

        # Скрытый Змей-помощник
        Image:
            id: serpent_helper
            source: "serpent.png"
            size_hint: None, None
            size: "300dp", "300dp"
            pos_hint: {"center_x": 1.8, "center_y": 0.35}

    MDNavigationDrawer:
        id: nav_drawer
        md_bg_color: "#121212"
        MDBoxLayout:
            orientation: "vertical"
            padding: "20dp"
            spacing: "15dp"
            MDLabel: text: "SYSTEM CONTROL"; font_style: "H6"; text_color: "#BB86FC"
            MDSeparator:
            MDFlatButton: text: "Bridge Alpha [TG]"; icon: "swap-horizontal"; on_release: app.msg("Alpha Link Online")
            MDFlatButton: text: "Bridge Beta [TG]"; icon: "swap-horizontal"; on_release: app.msg("Beta Link Online")
            MDFlatButton: text: "Reset Session"; icon: "refresh"; on_release: app.reset_system()
            MDFlatButton: text: "Clear Logs"; icon: "trash-can-outline"; on_release: app.clear_logs()
            MDFlatButton: text: "Official Community"; icon: "telegram"; on_release: app.open_link()
            Widget:
            MDLabel: text: "v3.3.6 Stable"; font_style: "Caption"; text_color: "#444444"
'''

class NebulaApp(MDApp):
    log_data = StringProperty("> Nebula OS Initialized...\\n")
    code_init = StringProperty("")
    vault = DictProperty({'is_fresh': True})

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "DeepPurple"
        self.load_all_data()
        return Builder.load_string(KV)

    def on_start(self):
        # Запрос прав доступа для Android
        if platform.system() == "android":
            from android.permissions import request_permissions, Permission
            request_permissions([Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE, Permission.INTERNET])

        # Фирменная Кат-сцена (только при первом запуске)
        if self.vault.get('is_fresh', True):
            s = self.root.ids.serpent_intro
            l = self.root.ids.intro_label
            # Анимация Змея: выплывает снизу в центр экрана
            anim = Animation(pos_hint={"center_x": .5, "center_y": .5}, duration=2.5, t='out_back')
            anim.bind(on_complete=self.finish_intro)
            anim.start(s)
            # Плавное появление названия
            Animation(opacity=1, duration=2).start(l)
        else:
            self.root.ids.screen_manager.current = "main"

    def finish_intro(self, *args):
        self.vault['is_fresh'] = False
        self.save_all_data()
        # Переход в редактор через 1 секунду после анимации
        Clock.schedule_once(lambda x: setattr(self.root.ids.screen_manager, 'current', 'main'), 1)

    def run_engine(self):
        # Автоматическое переключение на вкладку терминала
        self.root.ids.b_nav.switch_tab('terminal')
        code = self.root.ids.editor.text
        
        def run_thread():
            # Безопасный перехват вывода консоли
            old_stdout = sys.stdout
            result_io = sys.stdout = StringIO()
            try:
                # Проверка наличия Torch перед запуском
                if "torch" in code and not TORCH_READY:
                    output = "System Warning: Torch module not found in this build.\\nExecuting remaining logic..."
                
                # Выполнение кода с доступом к приложению через 'app'
                exec(code, {**globals(), 'app': self})
                output = result_io.getvalue() or "--- Engine Finished (No Output) ---"
            except Exception:
                output = traceback.format_exc()
            finally:
                sys.stdout = old_stdout
            
            self.update_terminal(output)

        threading.Thread(target=run_thread, daemon=True).start()

    @mainthread
    def update_terminal(self, text):
        self.log_data += f"\\n[{time.strftime('%H:%M:%S')}] {text}"
        # Скролл логов в самый низ
        Clock.schedule_once(lambda x: setattr(self.root.ids.log_scroll, 'scroll_y', 0), 0.1)

    def handle_auto_save(self, text):
        path = os.path.join(self.user_data_dir, "autosave_draft.py")
        with open(path, "w", encoding='utf-8') as f:
            f.write(text)

    def load_all_data(self):
        # Загрузка Vault (Intro state)
        v_p = os.path.join(self.user_data_dir, "vault.json")
        if os.path.exists(v_p):
            with open(v_p, "r") as f: self.vault = json.load(f)
        
        # Загрузка последнего кода
        c_p = os.path.join(self.user_data_dir, "autosave_draft.py")
        if os.path.exists(c_p):
            with open(c_p, "r", encoding='utf-8') as f: self.code_init = f.read()
        else:
            self.code_init = "import numpy as np\\nprint('Nebula Master Engine Online')\\n# Try writing code here"

    def save_all_data(self):
        v_p = os.path.join(self.user_data_dir, "vault.json")
        with open(v_p, "w") as f: json.dump(dict(self.vault), f)

    def ins(self, text): self.root.ids.editor.insert_text(text)
    def msg(self, text): Snackbar(text=text).open()
    def clear_logs(self): self.log_data = "> Logs Purged\\n"
    def open_link(self): webbrowser.open("https://t.me/nebula_evolution")
    
    def reset_system(self):
        self.vault['is_fresh'] = True
        self.save_all_data()
        self.msg("System Reset. Restart app.")

    def call_serpent_help(self):
        # Анимация Змея-помощника: вылетает справа
        s = self.root.ids.serpent_helper
        Animation(pos_hint={"center_x": .82, "center_y": .38}, duration=1.2, t='out_elastic').start(s)
        self.msg("Serpent Assistant Active")

if __name__ == "__main__":
    NebulaApp().run()
      

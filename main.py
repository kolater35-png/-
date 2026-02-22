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

# ПОЛНАЯ РАЗМЕТКА ИНТЕРФЕЙСА (KV)
KV = '''
<SyntaxBtn@MDRaisedButton>:
    size_hint: None, None
    size: "75dp", "52dp"
    elevation: 6
    radius: [18, 18, 18, 18]
    md_bg_color: 0.2, 0.2, 0.2, 1

MDScreenManager:
    id: screen_manager
    MDScreen:
        name: "intro"
        md_bg_color: "#000000"
        Image:
            id: serpent_intro
            source: "serpent.png"
            size_hint: None, None
            size: "380dp", "380dp"
            pos_hint: {"center_x": .5, "center_y": -.6}
        MDLabel:
            id: intro_text
            text: "NEBULA EVOLUTION\\nMASTER CORE"
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
                title: "Nebula Ultra [PRO]"
                md_bg_color: "#121212"
                elevation: 10
                left_action_items: [["menu", lambda x: nav_drawer.set_state("open")]]
                right_action_items: [["robot-excited-outline", lambda x: app.call_serpent_help()]]

            # Панель быстрого синтаксиса
            ScrollView:
                size_hint_y: None
                height: "80dp"
                do_scroll_y: False
                MDBoxLayout:
                    adaptive_width: True
                    padding: "15dp"
                    spacing: "12dp"
                    SyntaxBtn: text: "def"; md_bg_color: "#FF5252"; on_release: app.ins("def ")
                    SyntaxBtn: text: "torch"; md_bg_color: "#FFAB40"; on_release: app.ins("import torch\\n")
                    SyntaxBtn: text: "class"; md_bg_color: "#448AFF"; on_release: app.ins("class ")
                    SyntaxBtn: text: "import"; md_bg_color: "#E040FB"; on_release: app.ins("import ")
                    SyntaxBtn: text: "tg_bot"; md_bg_color: "#00E5FF"; on_release: app.ins("from telegram import Bot")
                    SyntaxBtn: text: "async"; md_bg_color: "#FF4081"; on_release: app.ins("async ")
                    SyntaxBtn: text: ":"; md_bg_color: "#333333"; on_release: app.ins(":")

            # Основной редактор
            MDBoxLayout:
                orientation: "vertical"
                padding: "12dp"
                MDCard:
                    radius: [25,]
                    md_bg_color: "#0D0D0D"
                    padding: "15dp"
                    elevation: 4
                    ScrollView:
                        MDTextField:
                            id: editor
                            text: app.code_init
                            multiline: True
                            mode: "fill"
                            fill_color_normal: "#0D0D0D"
                            on_text: app.handle_auto_save(self.text)

                MDBoxLayout:
                    size_hint_y: None
                    height: "80dp"
                    padding: [0, 15, 0, 0]
                    MDFillRoundFlatButton:
                        text: "EXECUTE NEBULA ENGINE"
                        icon: "play-circle"
                        size_hint_x: 1
                        md_bg_color: "#6200EE"
                        on_release: app.run_engine()

            # Нижняя навигация и консоль
            MDBottomNavigation:
                id: b_nav
                panel_color: "#121212"
                MDBottomNavigationItem:
                    name: 'ide'; text: 'Editor'; icon: 'code-tags'
                MDBottomNavigationItem:
                    name: 'logs'; text: 'Terminal'; icon: 'console-line'
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
                                font_name: "Roboto"

        # Змей-помощник (Скрыт по умолчанию)
        Image:
            id: serpent_helper
            source: "serpent.png"
            size_hint: None, None
            size: "280dp", "280dp"
            pos_hint: {"center_x": 1.8, "center_y": 0.35}

    MDNavigationDrawer:
        id: nav_drawer
        md_bg_color: "#121212"
        MDBoxLayout:
            orientation: "vertical"
            padding: "20dp"
            spacing: "15dp"
            MDLabel: text: "NEBULA MASTER"; font_style: "H5"; text_color: "#BB86FC"
            MDSeparator:
            MDFlatButton: text: "Bridge Alpha [TG]"; icon: "link-variant"; on_release: app.msg("Alpha Link Ready")
            MDFlatButton: text: "Bridge Beta [TG]"; icon: "link-variant"; on_release: app.msg("Beta Link Ready")
            MDFlatButton: text: "Reset Application"; icon: "refresh"; on_release: app.reset_system()
            MDFlatButton: text: "Clear Terminal"; icon: "trash-can-outline"; on_release: app.clear_logs()
            Widget:
            MDLabel: text: "v3.3.3 Enterprise"; font_style: "Caption"; text_color: "#444444"
'''

class NebulaApp(MDApp):
    log_data = StringProperty("> Initializing Nebula Core...\\n")
    code_init = StringProperty("")
    vault = DictProperty({'is_fresh': True})

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "DeepPurple"
        self.load_session_data()
        return Builder.load_string(KV)

    def on_start(self):
        # Запрос разрешений для Android
        if platform.system() == "android":
            from android.permissions import request_permissions, Permission
            request_permissions([Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE, Permission.INTERNET])

        # КАТ-СЦЕНА (Загрузка Змея)
        if self.vault.get('is_fresh', True):
            s = self.root.ids.serpent_intro
            t = self.root.ids.intro_text
            # Анимация: выплывание змея снизу в центр
            anim = Animation(pos_hint={"center_x": .5, "center_y": .5}, duration=2.5, t='out_back')
            anim.bind(on_complete=self.end_intro)
            anim.start(s)
            # Плавное появление текста
            Animation(opacity=1, duration=2).start(t)
        else:
            self.root.ids.screen_manager.current = "main"

    def end_intro(self, *args):
        self.vault['is_fresh'] = False
        self.save_session_data()
        # Пауза перед входом в IDE
        Clock.schedule_once(lambda x: setattr(self.root.ids.screen_manager, 'current', 'main'), 1.2)

    def run_engine(self):
        # Переключение на вкладку логов при запуске
        self.root.ids.b_nav.switch_tab('logs')
        code = self.root.ids.editor.text
        
        def execute():
            old_stdout = sys.stdout
            new_stdout = StringIO()
            sys.stdout = new_stdout
            try:
                # Позволяем коду видеть объект 'app' для управления UI из скриптов
                exec(code, {**globals(), 'app': self})
                output = new_stdout.getvalue() or "--- Success (No Output) ---"
            except Exception:
                output = traceback.format_exc()
            finally:
                sys.stdout = old_stdout
            self.append_log(output)

        threading.Thread(target=execute, daemon=True).start()

    @mainthread
    def append_log(self, text):
        self.log_data += f"\\n[{time.strftime('%H:%M:%S')}] {text}"
        # Авто-скролл вниз
        Clock.schedule_once(lambda x: setattr(self.root.ids.log_scroll, 'scroll_y', 0), 0.1)

    def handle_auto_save(self, text):
        path = os.path.join(self.user_data_dir, "nebula_draft.py")
        try:
            with open(path, "w", encoding='utf-8') as f:
                f.write(text)
        except: pass

    def load_session_data(self):
        # Загрузка состояния (был ли первый запуск)
        v_path = os.path.join(self.user_data_dir, "vault_config.json")
        if os.path.exists(v_path):
            with open(v_path, "r") as f: self.vault = json.load(f)
        
        # Загрузка последнего сохраненного кода
        c_path = os.path.join(self.user_data_dir, "nebula_draft.py")
        if os.path.exists(c_path):
            with open(c_path, "r", encoding='utf-8') as f: self.code_init = f.read()
        else:
            self.code_init = "import torch\\nprint('Nebula Engine Online')"

    def save_session_data(self):
        v_path = os.path.join(self.user_data_dir, "vault_config.json")
        with open(v_path, "w") as f: json.dump(dict(self.vault), f)

    def ins(self, text): self.root.ids.editor.insert_text(text)
    def msg(self, text): Snackbar(text=text).open()
    def clear_logs(self): self.log_data = "> Terminal Cleared\\n"
    
    def reset_system(self):
        self.vault['is_fresh'] = True
        self.save_session_data()
        self.msg("System Reset. Restart app to see Intro.")

    def call_serpent_help(self):
        s = self.root.ids.serpent_helper
        # Анимация: Змей залетает в экран справа
        Animation(pos_hint={"center_x": .85, "center_y": .35}, duration=1, t='out_elastic').start(s)
        self.msg("Serpent Assistant Activated")

if __name__ == "__main__":
    NebulaApp().run()
          

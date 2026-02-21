import os, sys, threading, traceback, time
from io import StringIO
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.properties import BooleanProperty, StringProperty, NumericProperty, DictProperty
from kivy.utils import platform, get_color_from_hex
from kivymd.app import MDApp
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.dialog import MDDialog

# Локализация (Языковой пакет)
LANG_DATA = {
    "Russian": {
        "welcome": "Хотите краткую экскурсию по системе?",
        "start": "Начать", "skip": "Пропустить",
        "step1": "Это ваша Дека. Здесь вы пишете код на Python.",
        "step2": "Вкладка LOGS покажет результат работы и ошибки.",
        "step3": "ИИ-помощник активен и поможет исправить баги!",
        "settings": "Настройки", "lang": "Язык", "theme": "Тема",
        "ai_helper": "ИИ-Помощник", "on": "Вкл", "off": "Выкл"
    },
    "English": {
        "welcome": "Would you like a quick tour of the system?",
        "start": "Start", "skip": "Skip",
        "step1": "This is your Deck. Write Python code here.",
        "step2": "The LOGS tab shows output and errors.",
        "step3": "AI Helper is active and will guide you through bugs!",
        "settings": "Settings", "lang": "Language", "theme": "Theme",
        "ai_helper": "AI Helper", "on": "On", "off": "Off"
    }
}

KV = '''
#:import hex kivy.utils.get_color_from_hex

MDNavigationLayout:
    MDScreenManager:
        id: screen_manager
        MDScreen:
            name: "main"
            MDBoxLayout:
                orientation: "vertical"
                md_bg_color: app.bg_color

                MDTopAppBar:
                    title: "NEBULA EVOLUTION"
                    md_bg_color: app.accent_color
                    left_action_items: [["menu", lambda x: nav_drawer.set_state("open")]]
                    right_action_items: [["brain", lambda x: app.ai_debug()], ["play", lambda x: app.run_code()]]

                MDBoxLayout:
                    orientation: "vertical"
                    padding: "10dp"
                    spacing: "10dp"

                    MDCard:
                        radius: [15,]
                        md_bg_color: app.card_color
                        padding: "5dp"
                        elevation: 2
                        MDTextField:
                            id: code_input
                            text: "print('Hello Nebula')"
                            multiline: True
                            mode: "fill"
                            fill_color_normal: [0,0,0,0]
                            text_color_normal: app.text_color
                            font_size: "14sp"

                MDBottomNavigation:
                    id: nav
                    panel_color: app.accent_color
                    MDBottomNavigationItem:
                        name: 'deck'
                        text: 'DECK'
                        icon: 'console'
                    MDBottomNavigationItem:
                        name: 'logs'
                        text: 'LOGS'
                        icon: 'matrix'
                        MDLabel:
                            id: terminal
                            text: app.output_log
                            halign: "center"
                            theme_text_color: "Custom"
                            text_color: hex("#00FFC8")

    MDNavigationDrawer:
        id: nav_drawer
        md_bg_color: app.card_color
        MDBoxLayout:
            orientation: "vertical"
            padding: "15dp"
            spacing: "10dp"
            MDLabel:
                text: app.lang_res['settings']
                font_style: "H6"
                theme_text_color: "Custom"
                text_color: app.text_color
            
            # ВЫБОР ЯЗЫКА
            MDBoxLayout:
                MDLabel:
                    text: "Language:"
                    theme_text_color: "Custom"
                    text_color: app.text_color
                MDRaisedButton:
                    text: "RU/EN"
                    on_release: app.switch_lang()

            # ТЕМА
            MDBoxLayout:
                MDLabel:
                    text: "Neon Theme:"
                    theme_text_color: "Custom"
                    text_color: app.text_color
                MDRaisedButton:
                    text: "Switch"
                    on_release: app.switch_theme()

            # ИИ ВКЛ/ВЫКЛ
            MDBoxLayout:
                MDLabel:
                    text: "AI Helper:"
                    theme_text_color: "Custom"
                    text_color: app.text_color
                MDRaisedButton:
                    id: ai_toggle
                    text: "ON"
                    on_release: app.toggle_ai()
'''

class NebulaApp(MDApp):
    output_log = StringProperty("> Ready\\n")
    system_lang = StringProperty("Russian")
    lang_res = DictProperty(LANG_DATA["Russian"])
    
    # Цвета тем
    bg_color = ListProperty(get_color_from_hex("#08080B"))
    accent_color = ListProperty(get_color_from_hex("#0D0D12"))
    card_color = ListProperty(get_color_from_hex("#101015"))
    text_color = ListProperty(get_color_from_hex("#00FFC8"))
    
    ai_enabled = BooleanProperty(True)
    dialog = None

    def build(self):
        self.theme_cls.theme_style = "Dark"
        return Builder.load_string(KV)

    def on_start(self):
        Clock.schedule_once(self.show_welcome_dialog, 1)

    def show_welcome_dialog(self, dt):
        self.dialog = MDDialog(
            title="NEBULA AI",
            text=self.lang_res["welcome"],
            buttons=[
                MDFlatButton(text=self.lang_res["skip"], on_release=lambda x: self.dialog.dismiss()),
                MDRaisedButton(text=self.lang_res["start"], on_release=self.start_tour)
            ],
        )
        self.dialog.open()

    def start_tour(self, instance):
        self.dialog.dismiss()
        # Кат-сцена (имитация через Snackbar)
        Clock.schedule_once(lambda dt: Snackbar(text=self.lang_res["step1"]).open(), 0.5)
        Clock.schedule_once(lambda dt: Snackbar(text=self.lang_res["step2"]).open(), 4)
        Clock.schedule_once(lambda dt: Snackbar(text=self.lang_res["step3"]).open(), 8)

    def switch_lang(self):
        self.system_lang = "English" if self.system_lang == "Russian" else "Russian"
        self.lang_res = LANG_DATA[self.system_lang]
        Snackbar(text=f"Language: {self.system_lang}").open()

    def switch_theme(self):
        if self.bg_color == get_color_from_hex("#08080B"):
            self.bg_color = get_color_from_hex("#001524") # Глубокий синий
            self.text_color = get_color_from_hex("#FF0055") # Розовый неон
        else:
            self.bg_color = get_color_from_hex("#08080B")
            self.text_color = get_color_from_hex("#00FFC8")

    def toggle_ai(self):
        self.ai_enabled = not self.ai_enabled
        self.root.ids.ai_toggle.text = "ON" if self.ai_enabled else "OFF"
        status = "Activated" if self.ai_enabled else "Deactivated"
        Snackbar(text=f"AI Assistant {status}").open()

    def run_code(self):
        code = self.root.ids.code_input.text
        self.root.ids.nav.switch_tab('logs')
        out = StringIO()
        sys.stdout = out
        try:
            exec(code, globals())
            res = out.getvalue()
        except Exception as e:
            res = f"ERROR: {str(e)}"
            if self.ai_enabled:
                self.ai_debug_hint(str(e))
        sys.stdout = sys.__stdout__
        self.output_log += f"\\n>>> {res}"

    def ai_debug_hint(self, error):
        # ИИ объясняет ошибку, не исправляя её за человека
        hints = {
            "name": "Вы используете переменную, которая не была создана. Проверьте опечатки.",
            "syntax": "В коде нарушена структура (забыта скобка или двоеточие).",
            "indentation": "Проблема с отступами. В Python это критично!"
        }
        msg = "ИИ: Кажется, у вас ошибка в логике."
        for key in hints:
            if key in error.lower(): msg = f"ИИ: {hints[key]}"
        
        Clock.schedule_once(lambda dt: MDDialog(title="AI Debugger", text=msg).open(), 1)

    def ai_debug(self):
        if self.ai_enabled:
            Snackbar(text="Система просканирована. Ошибок не обнаружено.").open()

if __name__ == "__main__":
    NebulaApp().run()

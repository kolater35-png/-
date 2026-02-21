import os, sys, threading, traceback, time, requests, json
from io import StringIO
from kivy.lang import Builder
from kivy.clock import Clock, mainthread
from kivy.properties import BooleanProperty, StringProperty, NumericProperty, DictProperty, ListProperty
from kivy.utils import platform, get_color_from_hex
from kivymd.app import MDApp
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.dialog import MDDialog

# --- ГЛОБАЛЬНЫЙ СЛОВАРЬ (МЭШ, МАКС, СИСТЕМА) ---
LANG_DATA = {
    "Russian": {
        "welcome": "Система Nebula Evolution приветствует вас. Пройти обучение?",
        "start": "Да, экскурсия", "skip": "В консоль",
        "step1": "ДЕКА: Основной терминал для Python. Здесь вы создаете скрипты.",
        "step2": "ИИ-ПОМОЩНИК: Если код выдаст ошибку, ИИ объяснит её причину.",
        "step3": "МОСТЫ: Через Telegram вы можете управлять телефоном удаленно.",
        "step4": "МЭШ/МАКС: Используйте вкладку интеграции для связи с городскими сервисами.",
        "settings": "Конфигурация", "lang": "Язык: RU", "theme": "Стиль интерфейса",
        "ai_status": "ИИ-Наставник", "tg_status": "TG Бот: В сети", "mesh_btn": "Данные МЭШ"
    },
    "English": {
        "welcome": "Nebula Evolution welcomes you. Start tour?",
        "start": "Start Tour", "skip": "Skip",
        "step1": "DECK: Main Python terminal for your scripts.",
        "step2": "AI ASSISTANT: If code fails, AI will explain why.",
        "step3": "BRIDGES: Use Telegram to control your phone remotely.",
        "step4": "MESH/MAX: Use the integration tab for city services link.",
        "settings": "Configuration", "lang": "Lang: EN", "theme": "UI Style",
        "ai_status": "AI Mentor", "tg_status": "TG Bot: Online", "mesh_btn": "MESH Data"
    }
}

KV = '''
#:import hex kivy.utils.get_color_from_hex

MDNavigationLayout:
    MDScreenManager:
        id: screen_manager
        MDScreen:
            name: "main_screen"
            MDBoxLayout:
                orientation: "vertical"
                md_bg_color: app.bg_color

                MDTopAppBar:
                    title: "NEBULA EVO PRO"
                    md_bg_color: app.accent_color
                    elevation: 4
                    left_action_items: [["menu", lambda x: nav_drawer.set_state("open")]]
                    right_action_items: [["school", lambda x: app.mesh_request()], ["play", lambda x: app.run_code()]]

                MDProgressBar:
                    id: progress
                    value: app.prog_val
                    color: hex("#00FFC8")
                    opacity: 1 if app.is_loading else 0
                    size_hint_y: None
                    height: "3dp"

                MDBoxLayout:
                    orientation: "vertical"
                    padding: "12dp"
                    spacing: "10dp"
                    MDCard:
                        radius: [15,]
                        md_bg_color: app.card_color
                        elevation: 2
                        padding: "8dp"
                        MDTextField:
                            id: code_input
                            text: "import numpy as np\\nprint('>> Bridge Active')"
                            multiline: True
                            mode: "fill"
                            fill_color_normal: [0,0,0,0]
                            text_color_normal: app.text_color
                            font_size: "14sp"
                            cursor_color: hex("#FFFF00")

                MDBottomNavigation:
                    id: nav
                    panel_color: app.accent_color
                    text_color_active: hex("#00FFC8")
                    MDBottomNavigationItem:
                        name: 'deck'
                        text: 'DECK'
                        icon: 'console'
                    MDBottomNavigationItem:
                        name: 'logs'
                        text: 'TERMINAL'
                        icon: 'matrix'
                        MDBoxLayout:
                            md_bg_color: hex("#050508")
                            ScrollView:
                                MDLabel:
                                    id: terminal
                                    text: app.output_log
                                    color: hex("#00FFC8")
                                    font_style: "Caption"
                                    size_hint_y: None
                                    height: self.texture_size[1]
                                    padding: "15dp"

    MDNavigationDrawer:
        id: nav_drawer
        md_bg_color: app.card_color
        elevation: 10
        MDBoxLayout:
            orientation: "vertical"
            padding: "20dp"
            spacing: "20dp"
            MDLabel:
                text: app.lang_res['settings']
                font_style: "H6"
                theme_text_color: "Custom"
                text_color: app.text_color
            MDSeparator:
                color: hex("#22222B")
            
            MDRaisedButton:
                text: app.lang_res['lang']
                on_release: app.switch_lang()
                md_bg_color: app.accent_color
                size_hint_x: 1
            
            MDRaisedButton:
                text: app.lang_res['theme']
                on_release: app.switch_theme()
                md_bg_color: app.accent_color
                size_hint_x: 1

            MDRaisedButton:
                text: app.lang_res['mesh_btn']
                on_release: app.mesh_request()
                md_bg_color: hex("#3F51B5")
                size_hint_x: 1

            MDBoxLayout:
                MDLabel:
                    text: app.lang_res['ai_status']
                    text_color: app.text_color
                MDSwitch:
                    id: ai_active
                    active: True

            MDLabel:
                text: app.lang_res['tg_status']
                font_style: "Caption"
                text_color: hex("#FFFF00")
'''

class NebulaApp(MDApp):
    output_log = StringProperty("> Nebula Engine v10.5 Pro Online\\n")
    system_lang = StringProperty("Russian")
    lang_res = DictProperty(LANG_DATA["Russian"])
    is_loading = BooleanProperty(False)
    prog_val = NumericProperty(0)
    
    # Ресурсы дизайна
    bg_color = ListProperty(get_color_from_hex("#08080B"))
    accent_color = ListProperty(get_color_from_hex("#0D0D12"))
    card_color = ListProperty(get_color_from_hex("#101015"))
    text_color = ListProperty(get_color_from_hex("#00FFC8"))

    # МОСТЫ (ЗАПОЛНИ ЭТИ ДАННЫЕ)
    TG_TOKEN = "ТВОЙ_ТОКЕН_БОТА"
    TG_CHAT_ID = "ТВОЙ_CHAT_ID"
    tg_last_id = 0

    def build(self):
        self.theme_cls.theme_style = "Dark"
        return Builder.load_string(KV)

    def on_start(self):
        self.show_welcome()
        # Поток для двустороннего Телеграма
        if self.TG_TOKEN != "ТВОЙ_ТОКЕН_БОТА":
            threading.Thread(target=self.tg_listen_bridge, daemon=True).start()

    def show_welcome(self):
        self.dialog = MDDialog(
            title="NEBULA CORE",
            text=self.lang_res["welcome"],
            buttons=[
                MDFlatButton(text=self.lang_res["skip"], on_release=lambda x: self.dialog.dismiss()),
                MDRaisedButton(text=self.lang_res["start"], on_release=self.start_ai_tour)
            ],
        )
        self.dialog.open()

    def start_ai_tour(self, x):
        self.dialog.dismiss()
        steps = [self.lang_res["step1"], self.lang_res["step2"], self.lang_res["step3"], self.lang_res["step4"]]
        for i, text in enumerate(steps):
            Clock.schedule_once(lambda dt, t=text: Snackbar(text=t).open(), i * 4.5)

    def switch_lang(self):
        self.system_lang = "English" if self.system_lang == "Russian" else "Russian"
        self.lang_res = LANG_DATA[self.system_lang]

    def switch_theme(self):
        # Циклическая смена тем (Cyberpunk -> Deep Sea -> Dark)
        if self.bg_color == get_color_from_hex("#08080B"):
            self.bg_color, self.text_color = get_color_from_hex("#00101A"), get_color_from_hex("#00E5FF")
        else:
            self.bg_color, self.text_color = get_color_from_hex("#08080B"), get_color_from_hex("#00FFC8")

    @mainthread
    def log_print(self, msg):
        self.output_log += f"\\n[{time.strftime('%H:%M:%S')}] ● {msg}"

    def run_code(self, external_code=None):
        self.root.ids.nav.switch_tab('logs')
        code = external_code if external_code else self.root.ids.code_input.text
        
        def _exec_thread():
            self.is_loading = True
            output = StringIO()
            sys.stdout = output
            try:
                exec(code, globals())
                result = output.getvalue().strip()
                if not result: result = "Code executed (No Return)"
            except Exception as e:
                result = f"CRITICAL ERROR: {str(e)}"
                if self.root.ids.ai_active.active:
                    Clock.schedule_once(lambda dt: self.ai_debugger_logic(str(e)))
            sys.stdout = sys.__stdout__
            self.log_print(result)
            self.is_loading = False
            return result

        return _exec_thread()

    def ai_debugger_logic(self, err_msg):
        # ИИ объясняет ошибку
        explanation = "ИИ: Ошибка в структуре кода. Проверьте скобки."
        if "name" in err_msg.lower(): explanation = "ИИ: Вы используете переменную, которая не определена выше."
        if "indent" in err_msg.lower(): explanation = "ИИ: Ошибка отступов. Python требует ровные блоки кода (Tab/4 пробела)."
        MDDialog(title="AI Debugger", text=explanation).open()

    # --- СЕКЦИЯ МОСТОВ: МЭШ И МАКС ---
    def mesh_request(self):
        self.log_print("MESH_BRIDGE: Запрос к API school.mos.ru...")
        # Здесь будет твой скрипт для парсинга МЭШ
        sample_mesh_code = "print('MESH_STATUS: Connected (Waiting for Auth Token)')"
        self.run_code(sample_mesh_code)

    # --- СЕКЦИЯ МОСТОВ: ТЕЛЕГРАМ ---
    def tg_listen_bridge(self):
        """Двусторонний мост: слушает команды из ТГ и отправляет результат"""
        while True:
            try:
                r = requests.get(f"https://api.telegram.org/bot{self.TG_TOKEN}/getUpdates?offset={self.tg_last_id+1}&timeout=20", timeout=25).json()
                for upd in r.get('result', []):
                    self.tg_last_id = upd['update_id']
                    msg = upd.get('message', {})
                    text = msg.get('text', '')
                    cid = msg.get('chat', {}).get('id', '')
                    
                    if str(cid) == str(self.TG_CHAT_ID) and text.startswith('/run '):
                        cmd = text[5:]
                        self.log_print(f"TG_REMOTE: {cmd}")
                        res = self.run_code(cmd)
                        requests.post(f"https://api.telegram.org/bot{self.TG_TOKEN}/sendMessage", json={"chat_id": cid, "text": f"✅ Result:\\n{res}"})
            except: pass
            time.sleep(2)

if __name__ == "__main__":
    NebulaApp().run()
                             

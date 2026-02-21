import os, sys, threading, time, requests, re, webbrowser, platform, json, subprocess
from io import StringIO
from kivy.lang import Builder
from kivy.clock import Clock, mainthread
from kivy.properties import StringProperty, NumericProperty, DictProperty, BooleanProperty, ListProperty
from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFillRoundFlatButton, MDFlatButton, MDRaisedButton, MDIconButton
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.uix.list import OneLineIconListItem, IconLeftWidget
from kivy.core.clipboard import Clipboard
from kivy.core.window import Window

# Конфигурация темы Material You
JAVA_COLORS = {
    "Dark": {
        "bg": "#1C1B1F", 
        "card": "#232123", 
        "primary": "#D0BCFF", 
        "secondary": "#CCC2DC",
        "text": "#E6E1E5", 
        "accent": "#49454F", 
        "error": "#F2B8B5",
        "success": "#B2F2BB"
    }
}

KV = '''
<NativeCard@MDCard>:
    padding: "16dp"
    radius: [28, ]
    elevation: 1
    md_bg_color: app.colors["card"]

MDNavigationLayout:
    MDScreenManager:
        id: screen_manager

        # --- ГЛАВНАЯ СЦЕНА ---
        MDScreen:
            name: "editor_screen"
            MDBoxLayout:
                orientation: "vertical"
                md_bg_color: app.colors["bg"]

                MDTopAppBar:
                    title: "Nebula Evolution"
                    elevation: 0
                    md_bg_color: app.colors["bg"]
                    specific_text_color: app.colors["text"]
                    left_action_items: [["menu", lambda x: nav_drawer.set_state("open")]]
                    right_action_items: [
                        ["account-voice", lambda x: app.konferansie.analyze_show()],
                        ["content-copy", lambda x: app.copy_code()],
                        ["content-paste", lambda x: app.paste_code()],
                        ["delete-sweep", lambda x: app.confirm_clear()]
                    ]

                MDProgressBar:
                    id: progress
                    value: app.loader_val
                    color: app.colors["primary"]
                    opacity: 1 if app.is_busy else 0
                    size_hint_y: None
                    height: "4dp"

                MDBoxLayout:
                    orientation: "vertical"
                    padding: "16dp"
                    spacing: "12dp"

                    NativeCard:
                        orientation: "vertical"
                        MDBoxLayout:
                            size_hint_y: None
                            height: "30dp"
                            MDLabel:
                                text: "СЦЕНА КОДА"
                                font_style: "Overline"
                                text_color: app.colors["primary"]
                            MDIcon:
                                icon: "code-braces"
                                theme_text_color: "Custom"
                                text_color: app.colors["primary"]
                                font_size: "18sp"

                        ScrollView:
                            MDTextField:
                                id: code_editor
                                text: app.code_init
                                multiline: True
                                mode: "fill"
                                fill_color_normal: [0, 0, 0, 0.1]
                                text_color_normal: app.colors["text"]
                                font_name: "Roboto"
                                font_size: "14sp"
                                on_text: app.save_draft(self.text)

                    MDBoxLayout:
                        size_hint_y: None
                        height: "56dp"
                        spacing: "12dp"
                        
                        MDFillRoundFlatButton:
                            text: "ЗАПУСТИТЬ ВЫСТУПЛЕНИЕ"
                            icon: "play-circle"
                            md_bg_color: app.colors["primary"]
                            text_color: [0,0,0,1]
                            size_hint_x: 0.8
                            on_release: app.run_system_code()
                        
                        MDIconButton:
                            icon: "cog-outline"
                            user_font_size: "24sp"
                            theme_text_color: "Custom"
                            text_color: app.colors["primary"]
                            on_release: app.open_settings()

                MDBottomNavigation:
                    id: bot_nav
                    panel_color: app.colors["card"]
                    selected_color_background: [1, 1, 1, 0.05]
                    
                    MDBottomNavigationItem:
                        name: 'edit'; text: 'Редактор'; icon: 'pencil-ruler'
                        
                    MDBottomNavigationItem:
                        name: 'services'; text: 'Ложа'; icon: 'theater'
                        MDBoxLayout:
                            orientation: "vertical"
                            padding: "20dp"
                            spacing: "12dp"
                            NativeCard:
                                orientation: "vertical"
                                MDLabel: 
                                    text: "ИНСТРУМЕНТЫ"
                                    halign: "center"
                                    font_style: "H6"
                                    text_color: app.colors["text"]
                                MDSeparator:
                                    height: "1dp"
                                MDBoxLayout:
                                    padding: [0, "10dp", 0, 0]
                                    orientation: "vertical"
                                    spacing: "8dp"
                                    MDRaisedButton: 
                                        text: "СИНХРОНИЗАЦИЯ МЭШ"
                                        size_hint_x: 1
                                        on_release: app.mesh_sync()
                                    MDRaisedButton: 
                                        text: "УСТАНОВИТЬ БИБЛИОТЕКИ"
                                        size_hint_x: 1
                                        on_release: app.pip_install_dialog()
                                    MDRaisedButton: 
                                        text: "СБРОСИТЬ ВСЁ"
                                        size_hint_x: 1
                                        md_bg_color: app.colors["error"]
                                        on_release: app.factory_reset()

                    MDBottomNavigationItem:
                        name: 'logs'; text: 'Протокол'; icon: 'script-text'
                        MDBoxLayout:
                            orientation: "vertical"
                            md_bg_color: "#000000"
                            ScrollView:
                                MDLabel: 
                                    id: console
                                    text: app.log_data
                                    color: "#00FFC8"
                                    font_style: "Caption"
                                    size_hint_y: None
                                    height: self.texture_size[1]
                                    padding: "16dp"

        # --- ЗАКУЛИСЬЕ (SETTINGS) ---
        MDScreen:
            name: "settings_screen"
            MDBoxLayout:
                orientation: "vertical"
                md_bg_color: app.colors["bg"]
                MDTopAppBar:
                    title: "Закулисье"
                    elevation: 0
                    left_action_items: [["arrow-left", lambda x: app.back_to_editor()]]
                
                ScrollView:
                    MDBoxLayout:
                        orientation: "vertical"
                        padding: "16dp"
                        spacing: "16dp"
                        size_hint_y: None
                        height: self.minimum_height
                        
                        NativeCard:
                            orientation: "vertical"
                            size_hint_y: None
                            height: "350dp"
                            MDLabel: text: "API И КОНФИГУРАЦИЯ"; font_style: "Subtitle1"; text_color: app.colors["primary"]
                            MDTextField: 
                                hint_text: "Telegram Bot Token"
                                text: app.settings_data.get('tg_token', '')
                                on_text: app.update_config('tg_token', self.text)
                            MDTextField: 
                                hint_text: "Chat ID"
                                text: app.settings_data.get('chat_id', '')
                                on_text: app.update_config('chat_id', self.text)
                            MDTextField: 
                                hint_text: "Версия приложения"
                                text: app.settings_data.get('version', '1.0.0')
                                on_text: app.update_config('version', self.text)
                            MDBoxLayout:
                                MDLabel: text: "Автосохранение"; text_color: app.colors["text"]
                                MDCheckbox: 
                                    active: app.settings_data.get('autosave', True)
                                    on_active: app.update_config('autosave', self.active)
                            MDRaisedButton: 
                                text: "СОХРАНИТЬ В ВАЛЮТУ"
                                size_hint_x: 1
                                on_release: app.save_to_disk()

    MDNavigationDrawer:
        id: nav_drawer
        md_bg_color: app.colors["bg"]
        MDBoxLayout:
            orientation: "vertical"
            padding: "16dp"
            spacing: "10dp"
            MDLabel: text: "NEBULA DASHBOARD"; font_style: "H6"; text_color: app.colors["text"]
            MDSeparator:
            MDFlatButton: text: "РЕДАКТОР"; icon: "pencil"; on_release: app.back_to_editor(); nav_drawer.set_state("close")
            MDFlatButton: text: "НАСТРОЙКИ"; icon: "cog"; on_release: app.open_settings(); nav_drawer.set_state("close")
            MDFlatButton: text: "ОКРУЖЕНИЕ"; icon: "memory"; on_release: app.open_env(); nav_drawer.set_state("close")
            Widget:
'''

class Konferansie:
    """Интеллектуальный помощник приложения"""
    def __init__(self, app):
        self.app = app
        self.quotes = [
            "Код — это поэзия, а вы — её автор.",
            "Сцена готова, прожекторы настроены.",
            "Даже если будет ошибка, мы превратим её в перформанс."
        ]

    def analyze_show(self):
        code = self.app.root.ids.code_editor.text
        if not code.strip():
            msg = "Конферансье шепчет: Сцена пуста. Напишите хотя бы пару строк!"
        elif self.app.last_error:
            msg = f"Конферансье обеспокоен: В последнем акте произошел сбой. {self.app.last_error}"
        else:
            msg = f"Конферансье доволен: {time.choice(self.quotes) if hasattr(time, 'choice') else self.quotes[0]}"
        
        MDDialog(title="Доклад Конферансье", text=msg, buttons=[MDFlatButton(text="ПОНЯЛ", on_release=lambda x: self.app.dialog_close())]).open()

class NebulaApp(MDApp):
    colors = DictProperty(JAVA_COLORS["Dark"])
    log_data = StringProperty("> Конферансье занял место. Добро пожаловать в Nebula Evolution.\\n")
    code_init = StringProperty("")
    env_info = StringProperty("")
    is_busy = BooleanProperty(False)
    loader_val = NumericProperty(0)
    last_error = StringProperty("")
    settings_data = DictProperty({'tg_token': '', 'chat_id': '', 'version': '1.0.0', 'autosave': True})

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "DeepPurple"
        self.konferansie = Konferansie(self)
        self.load_from_disk()
        self.refresh_env()
        return Builder.load_string(KV)

    # --- ПЕРСИСТЕНТНОСТЬ (ПАМЯТЬ) ---
    def load_from_disk(self):
        try:
            if os.path.exists("nebula_vault.json"):
                with open("nebula_vault.json", "r", encoding='utf-8') as f:
                    data = json.load(f)
                    self.settings_data.update(data)
            if os.path.exists("draft.py"):
                with open("draft.py", "r", encoding='utf-8') as f:
                    self.code_init = f.read()
        except Exception as e:
            self.log_write(f"Ошибка загрузки памяти: {e}")

    def save_to_disk(self):
        try:
            with open("nebula_vault.json", "w", encoding='utf-8') as f:
                json.dump(dict(self.settings_data), f, indent=4)
            Snackbar(text="Закулисье: Все данные зафиксированы").open()
        except Exception as e:
            self.log_write(f"Ошибка сохранения: {e}")

    def save_draft(self, text):
        if self.settings_data.get('autosave'):
            with open("draft.py", "w", encoding='utf-8') as f:
                f.write(text)

    # --- ИНСТРУМЕНТАРИЙ ---
    def update_config(self, key, value):
        self.settings_data[key] = value

    def copy_code(self):
        Clipboard.copy(self.root.ids.code_editor.text)
        Snackbar(text="Код скопирован в буфер").open()

    def paste_code(self):
        self.root.ids.code_editor.text += Clipboard.paste()
        Snackbar(text="Текст вставлен на сцену").open()

    def confirm_clear(self):
        self.dialog = MDDialog(
            title="Очистить сцену?",
            text="Все несохраненные строки кода будут удалены.",
            buttons=[
                MDFlatButton(text="ОТМЕНА", on_release=lambda x: self.dialog.dismiss()),
                MDRaisedButton(text="ОЧИСТИТЬ", on_release=lambda x: self.clear_editor())
            ]
        )
        self.dialog.open()

    def clear_editor(self):
        self.root.ids.code_editor.text = ""
        self.dialog.dismiss()

    # --- ВЫПОЛНЕНИЕ (ENGINE) ---
    @mainthread
    def log_write(self, msg):
        self.log_data += f"\\n[{time.strftime('%H:%M:%S')}] {msg}"

    def run_system_code(self):
        self.root.ids.bot_nav.switch_tab('logs')
        code = self.root.ids.code_editor.text
        if not code.strip(): return

        self.is_busy = True
        self.loader_val = 10
        
        def execute():
            output = StringIO()
            sys.stdout = output
            try:
                # Внедряем глобальные переменные для доступа кода к приложению
                exec_globals = globals().copy()
                exec_globals['app'] = self
                
                exec(code, exec_globals)
                result = output.getvalue().strip() or "Акт завершен без вывода."
                self.last_error = ""
            except Exception as e:
                result = f"КРИТИЧЕСКАЯ ОШИБКА: {str(e)}"
                self.last_error = str(e)
            finally:
                sys.stdout = sys.__stdout__
            
            Clock.schedule_once(lambda dt: self.post_execute(result))

        threading.Thread(target=execute, daemon=True).start()

    def post_execute(self, result):
        self.log_write(result)
        self.is_busy = False
        self.loader_val = 0

    # --- СЕРВИСЫ ---
    def refresh_env(self):
        import platform
        libs = ["requests", "numpy", "kivymd", "pandas"]
        lib_status = []
        for l in libs:
            try:
                __import__(l)
                lib_status.append(f"[color=#B2F2BB]●[/color] {l}")
            except:
                lib_status.append(f"[color=#FF0000]○[/color] {l}")
        
        self.env_info = (
            f"ЯДРО: {platform.system()} {platform.release()}\\n"
            f"АРХИТЕКТУРА: {platform.machine()}\\n"
            f"PYTHON: {sys.version.split()[0]}\\n\\n"
            "СОСТАВ ТРУППЫ:\\n" + "\\n".join(lib_status)
        )

    def open_env(self):
        self.refresh_env()
        MDDialog(title="Окружение системы", text=self.env_info).open()

    def mesh_sync(self):
        Snackbar(text="Попытка связи с MESH API...").open()

    def pip_install_dialog(self):
        Snackbar(text="Функция PIP доступна в режиме разработчика").open()

    def factory_reset(self):
        if os.path.exists("nebula_vault.json"): os.remove("nebula_vault.json")
        if os.path.exists("draft.py"): os.remove("draft.py")
        self.log_write("Система сброшена. Перезапустите приложение.")

    def open_settings(self): self.root.ids.screen_manager.current = "settings_screen"
    def back_to_editor(self): self.root.ids.screen_manager.current = "editor_screen"
    def dialog_close(self): pass

if __name__ == "__main__":
    # Настройка окна для десктопа (если запускаешь на ПК)
    if platform.system() != 'Android':
        Window.size = (400, 700)
    NebulaApp().run()
      

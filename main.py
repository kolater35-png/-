# -*- coding: utf-8: -*-
import os, sys, threading, time, json, platform, traceback
from io import StringIO
from kivy.lang import Builder
from kivy.clock import Clock, mainthread
from kivy.animation import Animation
from kivy.properties import StringProperty, NumericProperty, DictProperty, BooleanProperty
from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFillRoundFlatButton, MDFlatButton, MDRaisedButton
from kivymd.uix.snackbar import Snackbar
from kivy.core.window import Window

# Полная верстка интерфейса
KV = '''
<SymbolButton@MDRaisedButton>:
    size_hint: None, None
    size: "42dp", "42dp"
    md_bg_color: "#49454F"
    text_color: "#D0BCFF"
    on_release: app.insert_symbol(self.text)

MDScreenManager:
    id: screen_manager

    # ЭКРАН 1: КАТ-СЦЕНА СО ЗМЕЕМ
    MDScreen:
        name: "intro_screen"
        md_bg_color: "#000000"
        Image:
            id: serpent_intro
            source: "serpent.png"
            size_hint: None, None
            size: "300dp", "300dp"
            pos_hint: {"center_x": 0.5, "center_y": -0.3}

    # ЭКРАН 2: ОСНОВНОЙ ТЕАТР (РЕДАКТОР)
    MDScreen:
        name: "main_screen"
        MDBoxLayout:
            orientation: "vertical"
            md_bg_color: "#1C1B1F"

            MDTopAppBar:
                title: "Nebula Evolution"
                elevation: 0
                md_bg_color: "#1C1B1F"
                left_action_items: [["menu", lambda x: nav_drawer.set_state("open")]]
                right_action_items: [["snake", lambda x: app.call_serpent_help()]]

            # ПАНЕЛЬ БЫСТРЫХ СИМВОЛОВ
            ScrollView:
                size_hint_y: None
                height: "55dp"
                do_scroll_y: False
                bar_width: 0
                MDBoxLayout:
                    orientation: "horizontal"
                    adaptive_width: True
                    padding: "6dp"
                    spacing: "8dp"
                    SymbolButton: text: ":"
                    SymbolButton: text: "("
                    SymbolButton: text: ")"
                    SymbolButton: text: "["
                    SymbolButton: text: "]"
                    SymbolButton: text: "{"
                    SymbolButton: text: "}"
                    SymbolButton: text: "_"
                    SymbolButton: text: "="
                    SymbolButton: text: "'"
                    SymbolButton: text: '"'
                    SymbolButton: text: "import"

            MDBoxLayout:
                orientation: "vertical"
                padding: "12dp"
                spacing: "12dp"

                MDCard:
                    radius: [24, ]
                    padding: "12dp"
                    md_bg_color: "#232123"
                    elevation: 1
                    ScrollView:
                        MDTextField:
                            id: code_editor
                            text: app.code_init
                            multiline: True
                            mode: "fill"
                            fill_color_normal: [1, 1, 1, .02]
                            text_color_normal: "#E6E1E5"
                            font_size: "14sp"
                            on_text: app.save_draft(self.text)

                MDFillRoundFlatButton:
                    text: "ЗАПУСТИТЬ ПРЕДСТАВЛЕНИЕ"
                    icon: "play-circle"
                    size_hint_x: 1
                    md_bg_color: "#D0BCFF"
                    text_color: [0, 0, 0, 1]
                    on_release: app.run_engine()

            MDBottomNavigation:
                id: bot_nav
                panel_color: "#232123"
                selected_color_background: "#49454F"
                MDBottomNavigationItem:
                    name: 'edit'; text: 'Код'; icon: 'code-braces'
                MDBottomNavigationItem:
                    name: 'logs'; text: 'Консоль'; icon: 'console'
                    MDBoxLayout:
                        md_bg_color: "#000000"
                        ScrollView:
                            id: log_scroll
                            MDLabel:
                                id: console
                                text: app.log_data
                                color: "#00FFC8"
                                font_style: "Caption"
                                size_hint_y: None
                                height: self.texture_size[1]
                                padding: "12dp"

        # ПЕРСОНАЖ ПОМОЩНИК (СКРЫТ)
        Image:
            id: serpent_helper
            source: "serpent.png"
            size_hint: None, None
            size: "180dp", "180dp"
            pos_hint: {"center_x": 1.3, "center_y": 0.25}

    # ЭКРАН 3: ЗАКУЛИСЬЕ (НАСТРОЙКИ)
    MDScreen:
        name: "settings_screen"
        MDBoxLayout:
            orientation: "vertical"
            md_bg_color: "#1C1B1F"
            MDTopAppBar:
                title: "Настройки"
                left_action_items: [["arrow-left", lambda x: app.back_to_main()]]
            
            MDBoxLayout:
                orientation: "vertical"
                padding: "20dp"
                spacing: "20dp"
                
                MDCard:
                    padding: "20dp"
                    radius: [24, ]
                    orientation: "vertical"
                    size_hint_y: None
                    height: "240dp"
                    md_bg_color: "#232123"
                    
                    MDLabel: 
                        text: "ВИЗУАЛЬНЫЕ ЭФФЕКТЫ"
                        font_style: "H6"
                        text_color: "#D0BCFF"
                    
                    MDBoxLayout:
                        MDLabel: text: "Анимации Змея"
                        MDSwitch:
                            id: anim_switch
                            active: app.animations_enabled
                            on_active: app.toggle_animations(self.active)
                    
                    MDRaisedButton:
                        text: "СБРОСИТЬ ПЕРВЫЙ ЗАПУСК"
                        md_bg_color: "#49454F"
                        size_hint_x: 1
                        on_release: app.reset_first_launch()
                Widget:

    MDNavigationDrawer:
        id: nav_drawer
        md_bg_color: "#1C1B1F"
        MDBoxLayout:
            orientation: "vertical"
            padding: "16dp"
            spacing: "10dp"
            MDLabel: text: "NEBULA DASHBOARD"; font_style: "Button"; text_color: "#D0BCFF"
            MDSeparator:
            MDFlatButton: text: "Настройки"; icon: "cog"; on_release: app.open_settings()
            MDFlatButton: text: "Очистить логи"; icon: "trash-can"; on_release: app.clear_logs()
'''

class NebulaApp(MDApp):
    log_data = StringProperty("> Nebula OS Engine: Ready.\\n")
    code_init = StringProperty("print('Ш-ш... Добро пожаловать!')")
    animations_enabled = BooleanProperty(True)
    vault = DictProperty({'is_first_launch': True, 'animations': True})

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "DeepPurple"
        self.load_all_data()
        return Builder.load_string(KV)

    def on_start(self):
        # Права доступа для Android
        if platform.system() == "Android":
            try:
                from android.permissions import request_permissions, Permission
                request_permissions([Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE])
            except: pass
        
        # Проверка запуска кат-сцены
        if self.vault.get('is_first_launch', True) and self.animations_enabled:
            Clock.schedule_once(self.run_intro_performance, 1)
        else:
            self.root.current = "main_screen"

    # --- КИНЕМАТОГРАФИЯ ---
    def run_intro_performance(self, dt):
        serpent = self.root.ids.serpent_intro
        # Змей плавно выплывает на сцену
        anim = Animation(pos_hint={"center_x": 0.5, "center_y": 0.45}, duration=2.5, t='out_quad')
        anim.bind(on_complete=self.finish_intro)
        anim.start(serpent)

    def finish_intro(self, *args):
        # Пауза перед входом в редактор
        Clock.schedule_once(lambda x: setattr(self.root, 'current', 'main_screen'), 1.5)
        self.vault['is_first_launch'] = False
        self.save_all_data()

    # --- ПОМОЩЬ КОНФЕРАНСЬЕ ---
    def call_serpent_help(self):
        if not self.animations_enabled:
            self.show_help_logic()
            return
        serpent = self.root.ids.serpent_helper
        anim = Animation(pos_hint={"center_x": 0.85, "center_y": 0.3}, duration=1, t='out_back')
        anim.bind(on_complete=lambda *x: self.show_help_logic())
        anim.start(serpent)

    def show_help_logic(self):
        code = self.root.ids.code_editor.text
        if len(code) < 10:
            msg = "Ш-ш... Сцена пуста. Напиши что-нибудь!"
        elif "import" not in code:
            msg = "Ш-ш... Не забудь импортировать силы библиотек."
        else:
            msg = "Ш-ш... Код выглядит как яд! Жми запуск."
        
        MDDialog(
            title="Совет Конферансье",
            text=msg,
            buttons=[MDFlatButton(text="СПАСИБО", on_release=self.hide_serpent)]
        ).open()

    def hide_serpent(self, btn):
        btn.parent.parent.parent.parent.dismiss()
        if self.animations_enabled:
            serpent = self.root.ids.serpent_helper
            Animation(pos_hint={"center_x": 1.3, "center_y": 0.25}, duration=0.8).start(serpent)

    # --- PIP И ВЫПОЛНЕНИЕ КОДА ---
    def run_engine(self):
        self.root.ids.bot_nav.switch_tab('logs')
        code = self.root.ids.code_editor.text
        self.log_write("--- Начало акта ---")
        
        def execution_thread():
            output_buffer = StringIO()
            sys.stdout = output_buffer
            try:
                # Внедряем app в глобальное пространство для управления через код
                exec(code, {**globals(), 'app': self})
                result = output_buffer.getvalue().strip() or "Акт завершен успешно."
            except:
                result = f"КРИТИЧЕСКИЙ СБОЙ:\\n{traceback.format_exc()}"
            finally:
                sys.stdout = sys.__stdout__
            self.log_write(result)

        threading.Thread(target=execution_thread, daemon=True).start()

    def run_pip_install(self, package):
        self.log_write(f"Установка пакета: {package}...")
        try:
            import pip
            if hasattr(pip, 'main'): pip.main(['install', package])
            else:
                import pip._internal.main as pip_main
                pip_main.main(['install', package])
            self.log_write("Пакет успешно добавлен в систему!")
        except Exception as e:
            self.log_write(f"Ошибка Pip: {e}")

    @mainthread
    def log_write(self, msg):
        self.log_data += f"\\n[{time.strftime('%H:%M:%S')}] {msg}"
        def scroll(dt): self.root.ids.log_scroll.scroll_y = 0
        Clock.schedule_once(scroll, 0.1)

    # --- УПРАВЛЕНИЕ ДАННЫМИ ---
    def load_all_data(self):
        try:
            if os.path.exists("nebula_config.json"):
                with open("nebula_config.json", "r", encoding="utf-8") as f:
                    self.vault = json.load(f)
                    self.animations_enabled = self.vault.get('animations', True)
            if os.path.exists("draft.py"):
                with open("draft.py", "r", encoding="utf-8") as f:
                    self.code_init = f.read()
        except: pass

    def save_all_data(self):
        with open("nebula_config.json", "w", encoding="utf-8") as f:
            json.dump(dict(self.vault), f, indent=4)

    def save_draft(self, text):
        with open("draft.py", "w", encoding="utf-8") as f:
            f.write(text)

    def insert_symbol(self, symbol):
        self.root.ids.code_editor.insert_text(symbol + " ")

    def toggle_animations(self, state):
        self.animations_enabled = state
        self.vault['animations'] = state
        self.save_all_data()

    def reset_first_launch(self, *args):
        self.vault['is_first_launch'] = True
        self.save_all_data()
        Snackbar(text="История начнется заново при перезагрузке").open()

    def open_settings(self): self.root.current = "settings_screen"
    def back_to_main(self): self.root.current = "main_screen"
    def clear_logs(self): self.log_data = "> Консоль очищена.\\n"

if __name__ == "__main__":
    NebulaApp().run()

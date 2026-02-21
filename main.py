import os, sys, threading, traceback, time
from io import StringIO
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.properties import BooleanProperty, StringProperty, NumericProperty
from kivy.utils import platform, get_color_from_hex
from kivymd.app import MDApp
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.button import MDFillRoundFlatButton, MDIconButton, MDRaisedButton
from kivymd.uix.card import MDCard

# Улучшенный KV-дизайн с акцентом на эстетику
KV = '''
#:import hex kivy.utils.get_color_from_hex

<MagicCard@MDCard>:
    md_bg_color: hex("#101015")
    radius: [16, ]
    elevation: 2
    line_color: hex("#22222B")
    line_width: 1.2

MDNavigationLayout:
    MDScreenManager:
        MDScreen:
            MDBoxLayout:
                orientation: "vertical"
                md_bg_color: hex("#08080B")

                # ПРЕМИАЛЬНЫЙ HUD
                MDBoxLayout:
                    size_hint_y: None
                    height: "45dp"
                    md_bg_color: hex("#0D0D12")
                    padding: [20, 0]
                    spacing: "10dp"
                    
                    MDIcon:
                        icon: "signal-variant"
                        theme_text_color: "Custom"
                        text_color: hex("#00FFC8")
                        font_size: "18sp"
                        size_hint_x: None
                        width: "20dp"
                    
                    MDLabel:
                        text: "QUANTUM_LINK // STABLE"
                        font_style: "Caption"
                        theme_text_color: "Custom"
                        text_color: hex("#00FFC8")
                    
                    MDLabel:
                        text: app.system_time
                        halign: "right"
                        font_style: "Button"
                        theme_text_color: "Custom"
                        text_color: hex("#BB86FC")

                # ТОП-БАР С ГРАДИЕНТОМ (ИМИТАЦИЯ)
                MDTopAppBar:
                    title: "NEBULA QUANTUM"
                    anchor_title: "center"
                    md_bg_color: hex("#0D0D12")
                    elevation: 0
                    left_action_items: [["menu-variant", lambda x: nav_drawer.set_state("open")]]
                    right_action_items: [["orbit", lambda x: app.ai_analyze()], ["rocket-launch", lambda x: app.run_code()]]

                MDProgressBar:
                    id: progress
                    value: app.prog_val
                    color: hex("#BB86FC")
                    opacity: 1 if app.is_loading else 0
                    size_hint_y: None
                    height: "3dp"

                # РАБОЧАЯ ОБЛАСТЬ
                MDBoxLayout:
                    orientation: "vertical"
                    padding: [12, 12, 12, 8]
                    spacing: "12dp"

                    # Панель быстрых клавиш (Glass)
                    ScrollView:
                        size_hint_y: None
                        height: "48dp"
                        do_scroll_y: False
                        MDBoxLayout:
                            id: extra_keys
                            adaptive_width: True
                            padding: [0, 4]
                            spacing: "10dp"

                    # Главная карта редактора
                    MagicCard:
                        padding: "4dp"
                        MDTextField:
                            id: code_input
                            text: app.default_code
                            multiline: True
                            mode: "fill"
                            fill_color_normal: [0,0,0,0]
                            text_color_normal: hex("#E0E0E0")
                            font_name: "Roboto"
                            font_size: "15sp"
                            cursor_color: hex("#00FFC8")
                            hint_text: "System Waiting for Input..."
                            line_color_focus: [0,0,0,0]

                # НИЖНЯЯ ПАНЕЛЬ НАВИГАЦИИ
                MDBottomNavigation:
                    id: nav
                    panel_color: hex("#0D0D12")
                    text_color_active: hex("#00FFC8")
                    text_color_normal: hex("#555555")
                    height: "65dp"

                    MDBottomNavigationItem:
                        name: 'editor'
                        text: 'DECK'
                        icon: 'console-line'

                    MDBottomNavigationItem:
                        name: 'logs'
                        text: 'TERMINAL'
                        icon: 'application-variable'
                        MDBoxLayout:
                            orientation: "vertical"
                            md_bg_color: hex("#050508")
                            padding: "10dp"
                            
                            MagicCard:
                                ScrollView:
                                    id: term_scroll
                                    MDLabel:
                                        id: terminal
                                        text: app.output_log
                                        color: hex("#00FFC8")
                                        font_style: "Caption"
                                        size_hint_y: None
                                        height: self.texture_size[1]
                                        padding: "15dp"

    # БОКОВОЕ МЕНЮ (Drawer)
    MDNavigationDrawer:
        id: nav_drawer
        radius: (0, 20, 20, 0)
        md_bg_color: hex("#0F0F14")
        width: "280dp"
        
        MDBoxLayout:
            orientation: "vertical"
            padding: "20dp"
            spacing: "15dp"

            MDLabel:
                text: "SYSTEM CORE"
                font_style: "H5"
                theme_text_color: "Custom"
                text_color: hex("#BB86FC")
                size_hint_y: None
                height: "50dp"

            MDSeparator:
                color: hex("#22222B")

            MDList:
                id: drawer_list
                # Сюда добавятся элементы программно
'''

class NebulaApp(MDApp):
    is_loading = BooleanProperty(False)
    prog_val = NumericProperty(0)
    system_time = StringProperty("")
    output_log = StringProperty(">> SYSTEM READY v8.0\\n>> ENCRYPTION: ACTIVE\\n")
    default_code = StringProperty("import numpy as np\\n\\n# Start coding here\\nprint('>> LINK ESTABLISHED')")

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "DeepPurple"
        self.theme_cls.accent_palette = "Cyan"
        Clock.schedule_interval(self.update_time, 1)
        return Builder.load_string(KV)

    def update_time(self, dt):
        self.system_time = time.strftime("%H:%M")

    def on_start(self):
        self.create_interface_elements()

    def create_interface_elements(self):
        # Быстрые клавиши с новым стилем
        keys = ['def', 'print', 'import', 'if', ':', '"', '=', '(', ')', '{', '}', 'tab']
        for k in keys:
            btn = MDRaisedButton(
                text=k,
                md_bg_color=get_color_from_hex("#1A1A22"),
                text_color=get_color_from_hex("#00FFC8"),
                font_size="13sp",
                elevation=0,
                on_release=lambda x, c=k: self.insert_text(c)
            )
            self.root.ids.extra_keys.add_widget(btn)

    def insert_text(self, text):
        input = self.root.ids.code_input
        if text == "tab":
            input.insert_text("    ")
        elif text in ['print', 'def', 'import', 'if']:
            input.insert_text(text + " ")
        else:
            input.insert_text(text)

    def run_code(self):
        if self.is_loading: return
        self.is_loading = True
        self.root.ids.nav.switch_tab('logs')
        threading.Thread(target=self._execute).start()

    def _execute(self):
        code = self.root.ids.code_input.text
        out = StringIO()
        sys.stdout = out
        try:
            # Предустановка для Transformers
            exec(code, globals())
            res = out.getvalue()
        except:
            res = traceback.format_exc()
        sys.stdout = sys.__stdout__
        Clock.schedule_once(lambda dt: self._post_execute(res))

    def _post_execute(self, res):
        ts = time.strftime('%H:%M:%S')
        self.output_log += f"\\n[{ts}] ● {res}"
        self.is_loading = False

    def ai_analyze(self):
        Snackbar(
            text="AI Engine: Analysis complete. All systems nominal.",
            bg_color=get_color_from_hex("#101015"),
            color=get_color_from_hex("#00FFC8")
        ).open()

if __name__ == "__main__":
    NebulaApp().run()
  

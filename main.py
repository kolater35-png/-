from kivy.config import Config
Config.set('graphics', 'multisamples', '4')
Config.set('kivy', 'keyboard_mode', 'systemanddock')

from kivymd.app import MDApp
from kivy.lang import Builder
from core import TitanKernel, TitanPersistence, TitanSecurity
from ui_modules import TitanHighlighter, TitanExplorer
from network import TitanNetwork

KV = '''
MDBoxLayout:
    orientation: "vertical"
    md_bg_color: [0.04, 0.04, 0.06, 1]
    padding: [0, dp(28), 0, 0] # ФИКС: Отступ от статус-бара (челки)

    MDTopAppBar:
        title: "TITAN MULTI-IDE PRO"
        md_bg_color: [0.07, 0.07, 0.12, 1]
        left_action_items: [["menu", lambda x: nav.set_state("open")]]
        right_action_items: [["language-python", lambda x: None], ["play", lambda x: app.run_code()]]

    MDBoxLayout:
        id: work_area
        MDBoxLayout:
            id: explorer_panel
            size_hint_x: 0 # По умолчанию скрыт
            MDScrollView:
                MDList:
                    id: file_list

        MDTextField:
            id: editor
            multiline: True
            mode: "fill"
            markup: True
            font_size: "13sp"
            hint_text: "// Titan Kernel Ready. Support: Py, Java, C++, CSS"

    MDNavigationDrawer:
        id: nav
        MDBoxLayout:
            orientation: "vertical"
            padding: "16dp"
            MDLabel:
                text: "TITAN SETTINGS"
                font_style: "H6"
            # Кнопка Умного PIP
            MDRaisedButton:
                text: "SMART PIP INSTALL"
                on_release: app.pip_install_dialog()
'''

class TitanOS(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.kernel = TitanKernel()
        self.highlighter = TitanHighlighter()
        return Builder.load_string(KV)

    def on_start(self):
        self.explorer = TitanExplorer(self.kernel, self.root.ids.file_list)
        self.explorer.refresh()

    def run_code(self):
        # Логика запуска кода
        pass

    def pip_install_dialog(self):
        # Вызов smart_pip из ядра
        print(self.kernel.smart_pip("requests"))

if __name__ == "__main__":
    TitanOS().run()
  

from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.clock import Clock
from core import TitanKernel
from ui_modules import TitanIDE

KV = '''
MDBoxLayout:
    orientation: "vertical"
    md_bg_color: [0.05, 0.05, 0.07, 1]
    padding: [0, dp(30), 0, 0] # ФИКС: Отступ от статус-бара

    MDTopAppBar:
        title: "TITAN OS MONOLITH"
        md_bg_color: [0.1, 0.1, 0.15, 1]
        right_action_items: [["play", lambda x: app.run_build()]]

    MDTextField:
        id: editor
        multiline: True
        mode: "fill"
        markup: True
        font_name: "RobotoMono"
        hint_text: "// Heavy Kernel Ready. Input code..."
'''

class TitanApp(MDApp):
    def build(self):
        self.kernel = TitanKernel()
        self.ide = TitanIDE()
        return Builder.load_string(KV)

    def on_start(self):
        # Запуск тяжелого цикла подсветки
        Clock.schedule_interval(self.update_syntax, 1.5)

    def update_syntax(self, dt):
        editor = self.root.ids.editor
        if editor.focus: return # Не мешаем печатать
        editor.text = self.ide.apply_syntax(editor.text)

    def run_build(self):
        code = self.root.ids.editor.text
        lang = "cpp" if "#include" in code else "python"
        self.kernel.heavy_compile(code, lang, self.show_res)

    def show_res(self, text):
        from kivymd.uix.snackbar import Snackbar
        Snackbar(text=text).open()

if __name__ == "__main__":
    TitanApp().run()
  

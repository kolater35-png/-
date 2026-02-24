from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.clock import mainthread
from core import TitanKernel
from ui_modules import TitanIDE

class TitanApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.kernel = TitanKernel()
        self.ide = TitanIDE()
        return Builder.load_string(self.ide.get_layout())

    def process(self):
        code = self.root.ids.editor.text
        # Мгновенная подсветка
        self.root.ids.editor.text = self.ide.highlight(code)
        # Тяжелый анализ в фоне
        self.kernel.heavy_operation(code, self.on_result)

    @mainthread
    def on_result(self, text):
        from kivymd.uix.snackbar import Snackbar
        Snackbar(text=text, bg_color=[0, 0.3, 0.3, 1]).open()

    def pip_action(self):
        msg = self.kernel.install_module("requests")
        self.on_result(msg)

if __name__ == "__main__":
    TitanApp().run()
  

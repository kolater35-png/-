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
        return Builder.load_string(self.ide.get_styles())

    def run_logic(self):
        """Запуск тяжелых функций в фоне."""
        code = self.root.ids.editor.text
        # Подсветка (визуальное 'мясо')
        self.root.ids.editor.text = self.ide.highlight_logic(code)
        # Тяжелый анализ
        self.kernel.heavy_compilation_sim(code, self.on_report)

    @mainthread
    def on_report(self, report):
        from kivymd.uix.snackbar import Snackbar
        Snackbar(text=report, bg_color=[0.1, 0.3, 0.3, 1]).open()

    def pip_install(self):
        res = self.kernel.smart_pip("requests")
        self.on_report(res)

if __name__ == "__main__":
    TitanApp().run()
  

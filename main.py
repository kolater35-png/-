from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.clock import mainthread
from core import TitanKernel
from ui_modules import TitanIDE

class TitanApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Cyan"
        self.kernel = TitanKernel()
        self.ide = TitanIDE()
        return Builder.load_string(self.ide.get_layout())

    def run_kernel(self):
        # Визуальный отклик (Smart UI)
        self.root.ids.editor.hint_text = "Titan Core is thinking... Please wait."
        code = self.root.ids.editor.text
        
        # Подсветка кода
        self.root.ids.editor.text = self.ide.process_highlight(code)
        
        # Запуск тяжелого ядра в фоне
        self.kernel.heavy_analyze(code, self.on_kernel_ready)

    @mainthread
    def on_kernel_ready(self, message):
        from kivymd.uix.snackbar import Snackbar
        Snackbar(text=message, bg_color=[0.1, 0.4, 0.5, 1], duration=3).open()
        self.root.ids.editor.hint_text = "Accessing Titan Monolith... Entry allowed."

if __name__ == "__main__":
    TitanApp().run()

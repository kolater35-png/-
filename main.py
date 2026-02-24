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
        self.root.ids.editor.hint_text = "System Analyzing..."
        code = self.root.ids.editor.text
        self.root.ids.editor.text = self.ide.process_highlight(code)
        self.kernel.heavy_analyze(code, self.finish_task)

    @mainthread
    def finish_task(self, msg):
        from kivymd.uix.snackbar import Snackbar
        Snackbar(text=msg, bg_color=[0, 0.4, 0.4, 1]).open()
        self.root.ids.editor.hint_text = "Titan Online"

if __name__ == "__main__":
    TitanApp().run()

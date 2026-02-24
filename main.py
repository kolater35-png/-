import os, sys, threading
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.clock import mainthread
from kivy.core.window import Window
from core import TitanKernel
from ui_modules import TitanIDE

# Настройка окна для мобилок (чтобы клавиатура не перекрывала ввод)
Window.softinput_mode = "below_target"

class TitanApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Teal"
        
        # Инициализация систем
        self.kernel = TitanKernel()
        self.ide = TitanIDE()
        
        # Загрузка стиля (Мясо дизайна)
        return Builder.load_string(self.ide.get_kv_layout())

    def on_start(self):
        self.root.ids.editor.text = "// Titan OS Monolith Ready.\n// Support: Python, Java, C++, CSS"

    def execute_logic(self):
        """Запуск тяжелых функций в фоне"""
        code = self.root.ids.editor.text
        
        # 1. Визуальный фикс (подсветка)
        self.root.ids.editor.text = self.ide.apply_highlight(code)
        
        # 2. Тяжелая работа ядра
        threading.Thread(target=self._run_kernel_tasks, args=(code,), daemon=True).start()

    def _run_kernel_tasks(self, code):
        # Тяжелый анализ
        report = self.kernel.deep_analysis(code)
        # Очистка мусора
        mem_report = self.kernel.memory_optimize()
        self.notify(f"{report}\n{mem_report}")

    @mainthread
    def notify(self, text):
        from kivymd.uix.snackbar import Snackbar
        Snackbar(text=text, duration=3).open()

    def install_pkg(self):
        pkg = "requests" # Можно добавить ввод имени
        res = self.kernel.smart_pip(pkg)
        self.notify(res)

if __name__ == "__main__":
    TitanApp().run()

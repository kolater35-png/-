import os, sys, threading, traceback, time
from io import StringIO
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.properties import BooleanProperty, StringProperty, NumericProperty
from kivymd.app import MDApp
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.button import MDFillRoundFlatButton

KV = '''
MDBoxLayout:
    orientation: "vertical"
    md_bg_color: [0.05, 0.05, 0.07, 1]
    
    MDTopAppBar:
        title: "Nebula Quantum AI Pro"
        md_bg_color: [0.1, 0.1, 0.15, 1]
        right_action_items: [["brain", lambda x: app.run_ai_logic()], ["refresh", lambda x: app.reload_system()]]
    
    MDProgressBar:
        id: progress
        value: app.prog_val
        color: [0.7, 0.15, 1, 1]
        opacity: 1 if app.is_loading else 0
        size_hint_y: None
        height: "3dp"

    MDBottomNavigation:
        panel_color: [0.1, 0.1, 0.15, 1]
        selected_color_background: [0.2, 0.2, 0.3, 0.5]
        
        MDBottomNavigationItem:
            name: 'editor'
            text: 'AI Editor'
            icon: 'robot'
            MDBoxLayout:
                orientation: "vertical"
                MDTextField:
                    id: code_input
                    text: "import torch\\nprint('Torch:', torch.__version__)\\nx = torch.rand(2, 3)\\nprint(x)"
                    multiline: True
                    mode: "fill"
                    fill_color_normal: [0.07, 0.07, 0.1, 1]
                    text_color_normal: [1, 1, 1, 1]

        MDBottomNavigationItem:
            name: 'terminal'
            text: 'Output'
            icon: 'console'
            MDBoxLayout:
                md_bg_color: [0, 0, 0, 1]
                ScrollView:
                    MDLabel:
                        id: terminal
                        text: app.output_log
                        color: [0, 1, 0.8, 1]
                        size_hint_y: None
                        height: self.texture_size[1]
                        padding: "10dp"
'''

class NebulaAIApp(MDApp):
    is_loading = BooleanProperty(False)
    prog_val = NumericProperty(0)
    output_log = StringProperty("> System Ready...\\n")

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "DeepPurple"
        return Builder.load_string(KV)

    def reload_system(self):
        self.output_log = "> System Rebooted...\\n"
        Snackbar(text="Console Cleared").open()

    def run_ai_logic(self):
        if self.is_loading: return
        self.is_loading = True
        self.prog_val = 0
        threading.Thread(target=self.execute_thread).start()

    def execute_thread(self):
        # Эмуляция прогресса
        for i in range(1, 6):
            time.sleep(0.2)
            Clock.schedule_once(lambda dt, v=i*20: setattr(self, 'prog_val', v))

        code = self.root.ids.code_input.text
        out = StringIO()
        sys.stdout = out
        
        try:
            # Импортируем тяжелые либы прямо здесь (Lazy Loading)
            import torch
            import numpy
            import transformers
            
            exec(code, globals())
            res = out.getvalue()
        except Exception:
            res = traceback.format_exc()
        
        sys.stdout = sys.__stdout__
        Clock.schedule_once(lambda dt: self.finalize(res))

    def finalize(self, res):
        self.output_log += f"\\n{res}"
        self.is_loading = False
        Snackbar(text="Execution Finished").open()

if __name__ == "__main__":
    NebulaAIApp().run()
  

import os, sys, threading, traceback, subprocess
from io import StringIO
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.codeinput import CodeInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock

class NebulaCore(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        
        # Информационная панель
        self.status = Label(text="Nebula Quantum OS [Stable Mode]", size_hint_y=None, height=40)
        self.layout.add_widget(self.status)

        # Редактор кода
        self.editor = TextInput(text="import os\nprint('System Online!')\nprint(os.listdir('.'))", 
                                multiline=True, background_color=(0.1, 0.1, 0.1, 1), 
                                foreground_color=(1, 1, 1, 1))
        self.layout.add_widget(self.editor)

        # Терминал
        self.scroll = ScrollView(size_hint_y=0.3)
        self.terminal = Label(text="> Ready to boot...", size_hint_y=None, color=(0, 1, 0.8, 1))
        self.terminal.bind(texture_size=self.terminal.setter('size'))
        self.scroll.add_widget(self.terminal)
        self.layout.add_widget(self.scroll)

        # Кнопки управления
        btn_layout = BoxLayout(size_hint_y=None, height=50, spacing=10)
        self.run_btn = Button(text="RUN CODE", background_color=(0.5, 0, 1, 1))
        self.run_btn.bind(on_press=self.run_logic)
        
        self.env_btn = Button(text="CREATE .ENV")
        self.env_btn.bind(on_press=self.create_env)
        
        btn_layout.add_widget(self.run_btn)
        btn_layout.add_widget(self.env_btn)
        self.layout.add_widget(btn_layout)

        return self.layout

    def create_env(self, instance):
        with open(".env", "w") as f: f.write("API_KEY=nebula_777")
        self.terminal.text += "\n[System] .env created successfully"

    def run_logic(self, instance):
        threading.Thread(target=self._execute).start()

    def _execute(self):
        code = self.editor.text
        out = StringIO()
        sys.stdout = out
        try:
            exec(code, globals())
            res = out.getvalue()
        except:
            res = traceback.format_exc()
        sys.stdout = sys.__stdout__
        Clock.schedule_once(lambda dt: self._update_term(res))

    def _update_term(self, res):
        self.terminal.text += f"\n{res}"

if __name__ == "__main__":
    NebulaCore().run()
  

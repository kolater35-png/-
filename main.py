import os
from kivy.app import App
from kivy.uix.label import Label
from kivy.utils import platform

class SkeletonApp(App):
    def build(self):
        # Простейшее окно, чтобы проверить, работает ли компиляция
        return Label(text=f"TITAN OS SKELETON\nPlatform: {platform}\nStatus: ONLINE")

if __name__ == "__main__":
    SkeletonApp().run()

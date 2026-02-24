from kivy.app import App
from kivy.uix.button import Button

class TitanTest(App):
    def build(self):
        # Максимально простой элемент, чтобы проверить сборку
        return Button(text="TITAN SKELETON ONLINE\nCLICK TO TEST", 
                      background_color=(0, 1, 1, 1))

if __name__ == "__main__":
    TitanTest().run()

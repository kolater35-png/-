import os, re, subprocess
from kivy.clock import mainthread
from kivy.utils import get_color_from_hex
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.list import OneLineIconListItem, IconLeftWidget
from kivymd.uix.textfield import MDTextField

class TitanHighlighter:
    def __init__(self):
        self.rules = [
            # Java/C++/Python/CSS Keywords
            (r'\b(def|class|if|else|return|import|public|static|void|int|include|using|namespace|std|cout|printf|color|margin|display)\b', '#FF79C6'),
            (r'(\".*?\"|\'.*?\')', '#F1FA8C'), # Strings
            (r'(#.*|//.*)', '#6272A4'), # Comments
            (r'\b(self|System|out|print|cout|std|cin)\b', '#8BE9FD'), # Builtins
        ]

    def highlight(self, text):
        clean = re.sub(r'\[/?color.*?\]', '', text)
        for pattern, color in self.rules:
            clean = re.sub(pattern, f"[color={color}]\\1[/color]", clean)
        return clean

class TitanExplorer:
    def __init__(self, kernel, widget):
        self.kernel = kernel
        self.widget = widget

    @mainthread
    def refresh(self, path=None):
        self.widget.clear_widgets()
        curr = path or self.kernel.root_path
        for entry in sorted(os.scandir(curr), key=lambda e: (not e.is_dir(), e.name)):
            item = OneLineIconListItem(text=entry.name)
            icon = "folder" if entry.is_dir() else "file-code"
            item.add_widget(IconLeftWidget(icon=icon, text_color=get_color_from_hex("#00FFD1")))
            self.widget.add_widget(item)
          

import re
from kivy.utils import get_color_from_hex

class TitanIDE:
    def __init__(self):
        # Цветовая схема "Dracula/Java Style"
        self.syntax = {
            'kw': '#FF79C6',  # Keywords
            'str': '#F1FA8C', # Strings
            'com': '#6272A4', # Comments
            'num': '#BD93F9'  # Numbers
        }

    def apply_syntax(self, text):
        """Тяжелый regex-парсинг для Multi-Language."""
        if not text: return ""
        # Очистка старых тегов
        text = re.sub(r'\[/?color.*?\]', '', text)
        
        # Правила для Java, C++, Python, CSS
        rules = [
            (r'\b(public|static|void|int|class|def|return|if|else|import|include|String|using|namespace)\b', self.syntax['kw']),
            (r'(\".*?\"|\'.*?\')', self.syntax['str']),
            (r'(//.*|#.*|/\*.*?\*/)', self.syntax['com']),
            (r'\b(\d+)\b', self.syntax['num'])
        ]
        
        for pattern, color in rules:
            text = re.sub(pattern, f"[color={color}]\\1[/color]", text)
        return text
      

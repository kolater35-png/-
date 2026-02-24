import re

class TitanIDE:
    @staticmethod
    def get_layout():
        return '''
MDBoxLayout:
    orientation: "vertical"
    md_bg_color: [0.02, 0.02, 0.04, 1]
    padding: [0, dp(35), 0, 0] # Отступ от выреза камеры

    MDTopAppBar:
        title: "TITAN MONOLITH v5"
        md_bg_color: [0.05, 0.05, 0.1, 1]
        elevation: 4
        right_action_items: [["play-outline", lambda x: app.process()], ["package", lambda x: app.pip_action()]]

    MDBoxLayout:
        padding: "8dp"
        MDTextField:
            id: editor
            multiline: True
            mode: "fill"
            fill_color: [0, 0, 0, 0.4]
            markup: True
            font_size: "14sp"
            text_color_normal: [0.9, 0.9, 0.9, 1]
            hint_text: "// Kernel Ready. Support: Py, Java, C++, CSS"
'''

    def highlight(self, text):
        """Мультиязычный парсер подсветки."""
        if not text: return ""
        text = re.sub(r'\[/?color.*?\]', '', text) # Чистим старые теги
        
        rules = [
            (r'\b(public|static|void|class|def|import|include|return|if|else|String|int|color)\b', '#FF79C6'),
            (r'(\".*?\"|\'.*?\')', '#F1FA8C'),
            (r'(//.*|#.*)', '#6272A4'),
            (r'\b(\d+)\b', '#BD93F9')
        ]
        
        for pattern, color in rules:
            text = re.sub(pattern, f"[color={color}]\\1[/color]", text)
        return text
      

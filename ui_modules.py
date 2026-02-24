import re

class TitanIDE:
    @staticmethod
    def get_layout():
        return '''
MDBoxLayout:
    orientation: "vertical"
    md_bg_color: [0.03, 0.03, 0.05, 1]
    padding: [0, dp(35), 0, 0] # Отступ от выреза камеры

    MDTopAppBar:
        title: "TITAN MONOLITH v5"
        md_bg_color: [0.08, 0.08, 0.12, 1]
        right_action_items: [["play", lambda x: app.process()], ["package-variant", lambda x: app.pip_action()]]

    MDBoxLayout:
        padding: "10dp"
        MDTextField:
            id: editor
            multiline: True
            mode: "fill"
            fill_color: [0, 0, 0, 0.3]
            markup: True
            font_size: "14sp"
            text_color_normal: [0.9, 0.9, 0.9, 1]
            hint_text: "// Kernel Online. Py, Java, C++, CSS supported."
'''

    def highlight(self, text):
        if not text: return ""
        text = re.sub(r'\[/?color.*?\]', '', text) 
        rules = [
            (r'\b(public|static|void|class|def|import|include|return|if|else|String|int)\b', '#FF79C6'),
            (r'(\".*?\"|\'.*?\')', '#F1FA8C'),
            (r'(//.*|#.*)', '#6272A4'),
            (r'\b(\d+)\b', '#BD93F9')
        ]
        for pattern, color in rules:
            text = re.sub(pattern, f"[color={color}]\\1[/color]", text)
        return text
      

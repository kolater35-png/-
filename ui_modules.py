import re

class TitanIDE:
    @staticmethod
    def get_styles():
        """Возвращает KV-дизайн с фиксом Safe Area."""
        return '''
MDBoxLayout:
    orientation: "vertical"
    md_bg_color: [0.03, 0.03, 0.05, 1]
    padding: [0, dp(35), 0, 0] # Защита от наплыва на камеру

    MDTopAppBar:
        title: "TITAN MONOLITH v5"
        elevation: 4
        md_bg_color: [0.07, 0.07, 0.1, 1]
        right_action_items: [["play", lambda x: app.run_logic()], ["download", lambda x: app.pip_install()]]

    MDBoxLayout:
        padding: "6dp"
        MDTextField:
            id: editor
            multiline: True
            mode: "fill"
            fill_color: [0, 0, 0, 0.3]
            markup: True
            font_size: "13sp"
            text_color_normal: [0.9, 0.9, 0.9, 1]
            hint_text: "// Kernel Online. Input Py, Java, C++ or CSS..."
'''

    def highlight_logic(self, text):
        """Тяжелый Regex-парсер для подсветки кода."""
        if not text: return ""
        text = re.sub(r'\[/?color.*?\]', '', text) # Очистка тегов
        
        colors = {'kw': '#FF79C6', 'st': '#F1FA8C', 'cm': '#6272A4', 'nu': '#BD93F9'}
        
        rules = [
            (r'\b(public|static|void|int|class|def|import|include|return|if|else|color|display|String)\b', colors['kw']),
            (r'(\".*?\"|\'.*?\')', colors['st']),
            (r'(//.*|#.*)', colors['cm']),
            (r'\b(\d+)\b', colors['nu'])
        ]
        
        for pattern, color in rules:
            text = re.sub(pattern, f"[color={color}]\\1[/color]", text)
        return text
      

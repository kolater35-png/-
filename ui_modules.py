import re

class TitanIDE:
    def get_kv_layout(self):
        return '''
MDBoxLayout:
    orientation: "vertical"
    md_bg_color: [0.04, 0.04, 0.06, 1]
    padding: [0, dp(35), 0, 0] # ФИКС: Отступ от камеры/статус-бара

    MDTopAppBar:
        title: "TITAN OS MONOLITH"
        elevation: 4
        md_bg_color: [0.08, 0.08, 0.12, 1]
        right_action_items: [["play", lambda x: app.execute_logic()], ["package-variant", lambda x: app.install_pkg()]]

    MDBoxLayout:
        padding: "5dp"
        MDTextField:
            id: editor
            multiline: True
            mode: "fill"
            fill_color: [0, 0, 0, 0.2]
            markup: True # Важно для подсветки
            font_size: "14sp"
            text_color_normal: [1, 1, 1, 0.9]
'''

    def apply_highlight(self, text):
        """Парсер для Python, Java, C++, CSS"""
        if not text: return ""
        # Чистим старые теги
        text = re.sub(r'\[/?color.*?\]', '', text)
        
        # Цветовая схема
        syntax = {
            'kw': '#FF79C6',  # Ключевые слова (Java/CPP/Py)
            'st': '#F1FA8C',  # Строки
            'cm': '#6272A4',  # Комменты
            'nu': '#BD93F9'   # Числа
        }
        
        rules = [
            (r'\b(public|static|void|int|class|def|import|include|return|if|else|color|display)\b', syntax['kw']),
            (r'(\".*?\"|\'.*?\')', syntax['st']),
            (r'(//.*|#.*)', syntax['cm']),
            (r'\b(\d+)\b', syntax['nu'])
        ]
        
        for pattern, color in rules:
            text = re.sub(pattern, f"[color={color}]\\1[/color]", text)
        return text
      

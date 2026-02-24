import re

class TitanIDE:
    @staticmethod
    def get_layout():
        return '''
MDBoxLayout:
    orientation: "vertical"
    md_bg_color: [0.02, 0.02, 0.03, 1]
    padding: [0, dp(40), 0, 0] # Отступ сверху для защиты от выреза камеры

    MDTopAppBar:
        title: "TITAN CORE V3"
        elevation: 4
        md_bg_color: [0.06, 0.06, 0.1, 1]
        right_action_items: [["power-socket", lambda x: app.run_kernel()]]

    MDBoxLayout:
        padding: "8dp"
        MDTextField:
            id: editor
            multiline: True
            mode: "fill"
            fill_color: [0, 0, 0, 0.4]
            markup: True
            font_size: "14sp"
            text_color_normal: [0.9, 0.9, 0.95, 1]
            hint_text: "Accessing Titan Monolith... Entry allowed."
'''

    def process_highlight(self, text):
        """Парсер для C++, Python, Java"""
        if not text: return ""
        text = re.sub(r'\[/?color.*?\]', '', text)
        
        patterns = [
            (r'\b(class|def|public|static|void|import|include|String|int|return|if|else)\b', '#00E5FF'),
            (r'(\".*?\"|\'.*?\')', '#FFEA00'),
            (r'(//.*|#.*)', '#78909C'),
            (r'\b(\d+)\b', '#B388FF')
        ]
        
        for pat, col in patterns:
            text = re.sub(pat, f"[color={col}]\\1[/color]", text)
        return text
      

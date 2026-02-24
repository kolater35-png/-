import re

class TitanIDE:
    @staticmethod
    def get_layout():
        return '''
MDBoxLayout:
    orientation: "vertical"
    md_bg_color: [0, 0, 0.05, 1]
    padding: [0, dp(40), 0, 0]
    MDTopAppBar:
        title: "TITAN CORE V4"
        md_bg_color: [0.05, 0.05, 0.1, 1]
        right_action_items: [["flash", lambda x: app.run_kernel()]]
    MDBoxLayout:
        padding: "10dp"
        MDTextField:
            id: editor
            multiline: True
            mode: "fill"
            markup: True
            text_color_normal: [0.9, 1, 1, 1]
            hint_text: "Titan Ready..."
'''
    def process_highlight(self, text):
        if not text: return ""
        text = re.sub(r'\[/?color.*?\]', '', text)
        patterns = [(r'\b(import|class|def|return)\b', '#00FFFF'), (r'\b(\d+)\b', '#FF00FF')]
        for p, c in patterns: text = re.sub(p, f"[color={c}]\\1[/color]", text)
        return text
      

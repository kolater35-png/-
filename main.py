# -*- coding: utf-8: -*-
import os, sys, threading, time, json, traceback, platform, shutil
import requests
from io import StringIO
from kivy.lang import Builder
from kivy.clock import Clock, mainthread
from kivy.animation import Animation
from kivy.properties import StringProperty, DictProperty, BooleanProperty
from kivymd.app import MDApp
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.bottomsheet import MDListBottomSheet
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFillRoundFlatButton, MDFlatButton

# Интеграция с железом и разрешениями Android
from kivy.utils import platform as kivy_platform
if kivy_platform == 'android':
    from android.permissions import request_permissions, Permission

# Дизайн в стиле Native Java / Material 3
KV = '''
<ModernCard@MDCard>:
    padding: "16dp"
    radius: [24, 24, 24, 24]
    elevation: 1
    md_bg_color: "#1C1B1F"
    line_color: "#49454F"

MDScreenManager:
    id: screen_manager
    MDScreen:
        name: "intro"
        md_bg_color: "#000000"
        MDBoxLayout:
            orientation: "vertical"
            padding: "40dp"
            Widget:
            Image:
                id: intro_img
                source: "serpent.png"
                size_hint: None, None
                size: "280dp", "280dp"
                pos_hint: {"center_x": .5}
                opacity: 0
            MDLabel:
                id: intro_label
                text: "NEBULA MASTER\\nULTRA CORE"
                halign: "center"
                theme_text_color: "Custom"
                text_color: "#D0BCFF"
                font_style: "H4"
                bold: True
                opacity: 0
            Widget:

    MDScreen:
        name: "main"
        md_bg_color: "#1C1B1F"
        
        MDBoxLayout:
            orientation: "vertical"
            
            MDTopAppBar:
                title: "Nebula Evolution"
                anchor_title: "left"
                elevation: 0
                md_bg_color: "#1C1B1F"
                specific_text_color: "#E6E1E5"
                left_action_items: [["menu", lambda x: nav_drawer.set_state("open")]]
                right_action_items: [["application-variable", lambda x: app.setup_env()], ["robot-happy", lambda x: app.toggle_helper()]]

            MDBoxLayout:
                orientation: "vertical"
                padding: "16dp"
                spacing: "16dp"

                # Панель быстрого синтаксиса (ENV, AI, TG)
                ScrollView:
                    size_hint_y: None
                    height: "50dp"
                    do_scroll_y: False
                    MDBoxLayout:
                        adaptive_width: True
                        spacing: "10dp"
                        padding: ["4dp", "0dp"]
                        MDFillRoundFlatButton:
                            text: "INITIALIZE ENV"
                            md_bg_color: "#4F378B"
                            on_release: app.setup_env()
                        MDFillRoundFlatButton:
                            text: "TELEGRAM PUSH"
                            md_bg_color: "#333333"
                            on_release: app.bridge_send()
                        MDFillRoundFlatButton:
                            text: "VIBRO TEST"
                            md_bg_color: "#333333"
                            on_release: app.vibrate()
                        MDFillRoundFlatButton:
                            text: "IMPORT TORCH"
                            md_bg_color: "#333333"
                            on_release: app.ins("import torch\\nimport numpy as np\\n")

                ModernCard:
                    orientation: "vertical"
                    MDLabel:
                        text: "CORE EDITOR"
                        theme_text_color: "Secondary"
                        font_style: "Overline"
                        padding: ["0dp", "0dp", "0dp", "8dp"]
                    ScrollView:
                        MDTextField:
                            id: editor
                            text: app.saved_code
                            multiline: True
                            mode: "fill"
                            fill_color_normal: "#2B2930"
                            text_color_normal: "#E6E1E5"
                            font_name: "Roboto"
                            on_text: app.auto_save(self.text)

                MDFillRoundFlatButton:
                    text: "EXECUTE SYSTEM ENGINE"
                    icon: "fire-circle"
                    size_hint_x: 1
                    height: "56dp"
                    md_bg_color: "#D0BCFF"
                    text_color: "#381E72"
                    on_release: app.run_engine()

            MDBottomNavigation:
                id: b_nav
                panel_color: "#1C1B1F"
                selected_color_background: "#4F378B"
                MDBottomNavigationItem:
                    name: 'ide'; text: 'Code'; icon: 'xml'
                MDBottomNavigationItem:
                    name: 'term'; text: 'Terminal'; icon: 'console-line'
                    MDBoxLayout:
                        md_bg_color: "#000000"
                        ScrollView:
                            id: log_scroll
                            MDLabel:
                                id: console
                                text: app.log_data
                                color: "#00FFC8"
                                font_style: "Caption"
                                size_hint_y: None
                                height: self.texture_size[1]
                                padding: "20dp"

        Image:
            id: s_helper
            source: "serpent.png"
            size_hint: None, None
            size: "220dp", "220dp"
            pos_hint: {"center_x": 1.5, "center_y": 0.3}

    MDNavigationDrawer:
        id: nav_drawer
        radius: (0, 16, 16, 0)
        md_bg_color: "#1C1B1F"
        MDBoxLayout:
            orientation: "vertical"
            padding: "16dp"
            spacing: "12dp"
            MDLabel: text: "SYSTEM CONFIG"; font_style: "H6"; text_color: "#D0BCFF"
            MDSeparator:
            MDFlatButton: text: "Reset Environment"; icon: "refresh"; on_release: app.setup_env()
            MDFlatButton: text: "Clear Workspace"; icon: "trash-can-outline"; on_release: app.clear_workspace()
            MDFlatButton: text: "Export Logs to TG"; icon: "telegram"; on_release: app.bridge_send()
            MDFlatButton: text: "System Info"; icon: "information-outline"; on_release: app.post_log(app.get_sys_info())
            Widget:
'''

class NebulaApp(MDApp):
    log_data = StringProperty("> Nebula Master Ultra v6.0 Online\\n")
    saved_code = StringProperty("")
    vault = DictProperty({
        'tg_token': 'YOUR_BOT_TOKEN', 
        'chat_id': 'YOUR_CHAT_ID',
        'env_path': ''
    })

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.material_style = "M3"
        self.theme_cls.primary_palette = "DeepPurple"
        self.load_data()
        return Builder.load_string(KV)

    def on_start(self):
        # 1. Разрешения Android
        if kivy_platform == 'android':
            request_permissions([
                Permission.CAMERA, 
                Permission.WRITE_EXTERNAL_STORAGE, 
                Permission.VIBRATE
            ])
        
        # 2. Анимация входа
        img = self.root.ids.intro_img
        lbl = self.root.ids.intro_label
        Animation(opacity=1, duration=1.2, t='out_quad').start(img)
        Animation(opacity=1, duration=1.5).start(lbl)
        
        # 3. Подготовка модулей (Warmup)
        threading.Thread(target=self.warmup_ai, daemon=True).start()
        Clock.schedule_once(self.finish_intro, 4)

    def warmup_ai(self):
        self.post_log("AI: Initializing Neural Engines...")
        try:
            import torch
            self.post_log(f"AI: Torch {torch.__version__} - Ready")
        except: self.post_log("AI: Torch not found. Running in Lite mode.")

    def finish_intro(self, *args):
        self.root.ids.screen_manager.transition.direction = "left"
        self.root.ids.screen_manager.current = "main"

    # --- ENV LOGIC ---
    def setup_env(self):
        """Создает изолированное рабочее пространство"""
        env_path = os.path.join(self.user_data_dir, "nebula_env")
        try:
            for folder in ["", "models", "exports", "scripts"]:
                p = os.path.join(env_path, folder)
                if not os.path.exists(p): os.makedirs(p)
            self.vault['env_path'] = env_path
            self.save_data()
            self.post_log(f"ENV: Environment created at {env_path}")
            Snackbar(text="Virtual ENV Initialized").open()
        except Exception as e: self.post_log(f"ENV ERROR: {str(e)}")

    def run_engine(self):
        """Запуск кода с перехватом вывода"""
        self.root.ids.b_nav.switch_tab('term')
        code = self.root.ids.editor.text
        if self.vault.get('env_path'):
            sys.path.append(self.vault['env_path'])

        def work():
            old_out = sys.stdout
            res = sys.stdout = StringIO()
            try:
                # Внедряем app в глобальное пространство для управления из скрипта
                exec(code, {**globals(), 'app': self})
                out = res.getvalue() or "--- Execution Finished ---"
            except: out = traceback.format_exc()
            finally: sys.stdout = old_out
            self.post_log(out)
        
        threading.Thread(target=work, daemon=True).start()

    @mainthread
    def post_log(self, text):
        self.log_data += f"\\n[{time.strftime('%H:%M:%S')}] {text}"
        Clock.schedule_once(lambda x: setattr(self.root.ids.log_scroll, 'scroll_y', 0), 0.1)

    # --- HARDWARE & BRIDGE ---
    def bridge_send(self):
        """Отправка логов в Telegram"""
        token = self.vault['tg_token']
        cid = self.vault['chat_id']
        report = f"NEBULA REPORT ({platform.system()}):\\n{self.log_data[-400:]}"
        def send():
            try:
                requests.post(f"https://api.telegram.org/bot{token}/sendMessage", 
                             data={'chat_id': cid, 'text': report}, timeout=5)
                self.post_log("BRIDGE: Logs pushed to Telegram.")
            except: self.post_log("BRIDGE ERROR: Network timeout.")
        threading.Thread(target=send).start()

    def vibrate(self):
        try:
            from plyer import vibrator
            vibrator.vibrate(0.1)
            self.post_log("SYS: Haptic Feedback OK")
        except: self.post_log("SYS: Vibration unavailable")

    def get_sys_info(self):
        return f"OS: {platform.system()} | ENV: {'Active' if self.vault['env_path'] else 'None'}"

    # --- UI HELPERS ---
    def ins(self, t): self.root.ids.editor.insert_text(t)
    
    def auto_save(self, t):
        with open(os.path.join(self.user_data_dir, "core_save.py"), "w", encoding='utf-8') as f:
            f.write(t)

    def load_data(self):
        vp = os.path.join(self.user_data_dir, "vault_v6.json")
        if os.path.exists(vp):
            with open(vp, "r") as f: self.vault.update(json.load(f))
        cp = os.path.join(self.user_data_dir, "core_save.py")
        if os.path.exists(cp):
            with open(cp, "r", encoding='utf-8') as f: self.saved_code = f.read()
        else: self.saved_code = "print(app.get_sys_info())"

    def save_data(self):
        with open(os.path.join(self.user_data_dir, "vault_v6.json"), "w") as f:
            json.dump(dict(self.vault), f)

    def toggle_helper(self):
        s = self.root.ids.s_helper
        tx = 0.85 if s.pos_hint["center_x"] > 1 else 1.5
        Animation(pos_hint={"center_x": tx}, duration=1, t='out_elastic').start(s)

    def clear_workspace(self):
        self.root.ids.editor.text = ""
        Snackbar(text="Workspace Purged").open()

if __name__ == "__main__":
    NebulaApp().run()

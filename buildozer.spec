[app]
# (str) Название твоего приложения
title = Nebula Evolution

# (str) Имя пакета (без пробелов, только латиница)
package.name = nebula_pro_max

# (str) Домен (обычно org.название)
package.domain = org.nebula

# (str) Где лежит main.py (точка означает текущую папку)
source.dir = .

# (list) Какие расширения файлов включать в APK
source.include_exts = py,png,json,kv

# (str) Версия приложения
version = 1.1.0

# (list) ЗАВИСИМОСТИ (Самое важное!)
# Мы прописываем python3, kivy и kivymd, а также стек для ИИ
requirements = python3, kivy==2.1.0, kivymd==1.1.1, requests, urllib3, chardet, idna, pip, setuptools, numpy, torch, transformers, tqdm, certifi

# (str) Ориентация экрана
orientation = portrait

# (list) РАЗРЕШЕНИЯ
android.permissions = INTERNET, READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE, MANAGE_EXTERNAL_STORAGE

# (int) Android API (33 — это современный стандарт)
android.api = 33
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a

# (bool) Принимать лицензии SDK автоматически
android.accept_sdk_license = True

# (str) Иконка (если захочешь потом поменять, пока закомментировано)
# icon.filename = %(source.dir)s/icon.png

# (str) Presplash (экран загрузки при запуске APK)
# presplash.filename = %(source.dir)s/serpent.png

[buildozer]
# (int) Уровень логов (2 — самый подробный, чтобы видеть ошибки)
log_level = 2
warn_on_root = 1

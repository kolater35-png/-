[app]
# (str) Название твоего приложения
title = Nebula AI Pro

# (str) Имя пакета (без пробелов)
package.name = nebula_ai_pro

# (str) Домен пакета
package.domain = org.nebula

# (str) Папка с исходным кодом (где лежит main.py)
source.dir = .

# (list) Расширения файлов, которые нужно включить в сборку
source.include_exts = py,png,jpg,kv,atlas,env

# (str) Версия приложения
version = 1.5.0

# (list) Зависимости. МЫ УБРАЛИ TORCH ОТСЮДА, чтобы сборка прошла. 
# Мы установим его через твой внутренний PIP менеджер прямо в телефоне.
requirements = python3==3.10.0,kivy==2.3.0,kivymd==1.1.1,requests,paramiko,cryptography,setuptools

# (str) Ориентация экрана
orientation = portrait

# (list) Разрешения (Добавили работу с памятью для создания .env)
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,MANAGE_EXTERNAL_STORAGE

# (int) Target Android API (33 - современный стандарт)
android.api = 33

# (int) Minimum API
android.minapi = 21

# (str) Архитектура (arm64-v8a нужна для большинства современных телефонов)
android.archs = arm64-v8a

# (bool) Принимать лицензии SDK автоматически
android.accept_sdk_license = True

# (str) Тема (Dark по умолчанию)
android.entrypoint = main.py

# (list) Исключить эти папки из сборки
source.exclude_dirs = tests, bin, venv, .github

[buildozer]
# (int) Уровень логирования (2 - для отладки)
log_level = 2

# (int) Предупреждать о сборке под root
warn_on_root = 1

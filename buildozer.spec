[app]
# (str) Название приложения
title = Nebula Titan OS

# (str) Имя пакета
package.name = nebula_titan_os

# (str) Домен пакета
package.domain = io.titan.core

# (str) Директория с исходниками
source.dir = .

# (list) Включаемые расширения
source.include_exts = py,png,jpg,kv,json,db,ttf

# (str) Версия приложения
version = 5.0.3

# (list) ЗАВИСИМОСТИ (Самая важная часть. Без пробелов после запятых!)
requirements = python3,kivy==2.2.1,kivymd==1.1.1,pillow,requests,urllib3,chardet,idna,jnius

# (str) Иконка (убедись, что файл serpent.png лежит в корне рядом с main.py)
icon.filename = serpent.png

# (list) Поддерживаемые ориентации экрана
orientation = portrait,landscape

# (bool) Полноэкранный режим
fullscreen = 1

# (list) ПРАВА ДОСТУПА (Минимум для стабильности)
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,VIBRATE

# (int) Target Android API
android.api = 33

# (int) Minimum API
android.minapi = 21

# (str) Версия Android NDK
android.ndk = 25b

# (bool) Принимать лицензии SDK автоматически
android.accept_sdk_license = True

# (list) Архитектуры (Сборка под современные процессоры)
android.archs = arm64-v8a, armeabi-v7a

# (bool) Пропускать ошибки при упаковке (помогает при странных конфликтах)
android.skip_update = False

# (str) Тип сборки (debug или release)
android.build_mode = debug

[buildozer]
# (int) Уровень логов (2 = максимально подробно для GitHub Actions)
log_level = 2

# (int) Предупреждение при запуске от root
warn_on_root = 1

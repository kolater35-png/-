[app]
# (str) Название приложения в меню телефона
title = Nebula Titan OS

# (str) Имя пакета (без пробелов, только латиница)
package.name = nebula_titan_os

# (str) Домен пакета (используется для ID приложения)
package.domain = io.titan.core

# (str) Директория с исходным кодом
source.dir = .

# (list) Расширения файлов, которые попадёт в сборку
source.include_exts = py,png,jpg,kv,json,db,ttf

# (str) Версия приложения
version = 5.0.3

# (list) ЗАВИСИМОСТИ. Это самое важное для работы KivyMD и сети
requirements = python3, kivy==2.2.1, kivymd==1.1.1, pillow, requests, urllib3, chardet, idna, sqlite3, jnius

# (str) Иконка (укажи свой файл serpent.png)
icon.filename = serpent.png

# (list) Поддерживаемые ориентации экрана
orientation = portrait, landscape

# (bool) Фуллскрин режим
fullscreen = 1

# (list) ПРАВА ДОСТУПА. Без них терминал и ФС не будут работать на Android
android.permissions = INTERNET, READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE, VIBRATE, MANAGE_EXTERNAL_STORAGE

# (int) Target Android API (33 соответствует Android 13)
android.api = 33

# (int) Minimum API (21 — это поддержка Android 5.0+)
android.minapi = 21

# (str) Архитектуры процессоров (для GitHub Actions лучше оставить обе основные)
android.archs = arm64-v8a, armeabi-v7a

# (bool) Использовать кастомную заставку (presplash)
# android.presplash_color = #0A0A0F

# (list) Список Java-классов для JNI (если понадобятся специфические вызовы)
# android.add_src = 

[buildozer]
# (int) Уровень логов (2 — максимально подробно, чтобы видеть ошибки в Actions)
log_level = 2

# (int) Предупреждение при запуске от root
warn_on_root = 1

# (str) Путь к папке сборки (в Actions это не критично)
build_dir = ./.buildozer

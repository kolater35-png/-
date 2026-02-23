[app]
# (str) Название твоего приложения в меню телефона
title = Nebula Titan OS

# (str) Техническое имя пакета (без пробелов и спецсимволов)
package.name = nebula_titan_os

# (str) Домен (вместе с именем пакета создает уникальный ID в Google Play)
package.domain = io.titan.core

# (str) Где лежит main.py (точка означает текущую папку)
source.dir = .

# (list) Какие файлы включать в APK
source.include_exts = py,png,jpg,kv,json,db,ttf

# (str) Версия приложения
version = 5.0.3

# (list) Зависимости. ВАЖНО: без пробелов после запятых!
requirements = python3,kivy==2.2.1,kivymd==1.1.1,pillow,requests,urllib3,chardet,idna

# (str) Иконка приложения (убедись, что файл serpent.png в корне, или закомментируй строку символом #)
# icon.filename = serpent.png

# (list) Поддерживаемые ориентации (портретная — стандарт для ОС)
orientation = portrait

# (bool) Использовать весь экран (убирает полоску сверху)
fullscreen = 1

# (list) Права доступа Android
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,VIBRATE

# (int) Target Android API (33 = Android 13)
android.api = 33

# (int) Минимальная версия Android (21 = Android 5.0)
android.minapi = 21

# (str) Версия NDK (25b — самая стабильная для Kivy сейчас)
android.ndk = 25b

# (bool) Автоматически принимать лицензии SDK
android.accept_sdk_license = True

# (list) Архитектуры процессоров. 
# Оставляем только arm64-v8a для стабильности сборки на GitHub
android.archs = arm64-v8a

# (bool) Разрешить обновление SDK инструментов (исправляет ошибку "Aidl not found")
android.skip_update = False

# (str) Формат сборки (debug для тестирования)
android.build_mode = debug

# (bool) Копировать библиотеку python-for-android в папку проекта
android.copy_libs = 1

[buildozer]
# (int) Уровень логов (2 — самый подробный)
log_level = 2

# (int) Предупреждение при запуске от имени root
warn_on_root = 1

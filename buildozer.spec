[app]
# (str) Название твоего приложения в меню телефона
title = Nebula Evolution

# (str) Имя пакета (без пробелов и спецсимволов)
package.name = nebula_pro_master

# (str) Домен (вместе с именем пакета создает уникальный ID приложения)
package.domain = org.nebula

# (str) Где лежит твой main.py
source.dir = .

# (list) Какие файлы включать в APK
source.include_exts = py,png,jpg,kv,json,txt

# (str) Версия твоего приложения
version = 3.3.6

# (list) ТВОИ ЗАВИСИМОСТИ
# ВНИМАНИЕ: Я убрал torch и transformers, чтобы билд НЕ ПАДАЛ.
# Оставлен numpy и requests для работы с данными и API.
requirements = python3, kivy==2.1.0, kivymd==1.1.1, requests, urllib3, numpy, python-telegram-bot, certifi, idna

# (str) Ориентация экрана
orientation = portrait

# (list) Разрешения (Android Permissions)
android.permissions = INTERNET, READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE, MANAGE_EXTERNAL_STORAGE

# (int) API уровень (33 - современный стандарт для Android 13)
android.api = 33

# (int) Минимальная версия Android (21 = Android 5.0)
android.minapi = 21

# (str) Версия NDK (25b - самая стабильная для этого стека)
android.ndk = 25b

# (list) Архитектуры
# Оставляем только arm64-v8a для экономии времени сборки и памяти
android.archs = arm64-v8a

# (bool) Принимать лицензии SDK автоматически
android.accept_sdk_license = True

# (str) Иконка и заставка (твой Змей)
presplash.filename = %(source.dir)s/serpent.png
icon.filename = %(source.dir)s/serpent.png

# (list) Флаг для расширения памяти приложения на самом телефоне
android.meta_data = largeHeap=true

# (bool) Копировать библиотеки вместо создания libpython.so
android.copy_libs = 1

# (str) Фильтры логов (поможет при отладке через USB)
android.logcat_filters = *:S python:D

[buildozer]
# (int) Уровень детализации логов (2 = максимально подробно)
log_level = 2

# (int) Предупреждать, если запуск от root
warn_on_root = 1

# (str) Путь, куда упадет готовый APK
bin_dir = ./bin

[app]

# (str) Название твоего приложения
title = Nebula Evolution

# (str) Имя пакета (только маленькие буквы и подчеркивания)
package.name = nebula_master_pro

# (str) Домен пакета
package.domain = org.nebula

# (str) Директория с исходным кодом (main.py должен быть тут)
source.dir = .

# (list) Расширения файлов, которые попадёт в APK
source.include_exts = py,png,jpg,kv,json,txt

# (str) Версия приложения
version = 3.3.7

# (list) ТВОИ ЗАВИСИМОСТИ
# ВНИМАНИЕ: Мы временно убрали torch и transformers. 
# Это позволит билду на GitHub завершиться успешно без ошибок памяти.
requirements = python3, kivy==2.1.0, kivymd==1.1.1, requests, urllib3, numpy, python-telegram-bot, certifi, idna

# (str) Ориентация экрана
orientation = portrait

# (list) Разрешения Android
android.permissions = INTERNET, READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE, MANAGE_EXTERNAL_STORAGE

# (int) Target Android API (33 для Android 13)
android.api = 33

# (int) Minimum API (21 для Android 5.0)
android.minapi = 21

# (str) Версия NDK
android.ndk = 25b

# (list) Архитектуры (arm64-v8a — стандарт для современных систем)
android.archs = arm64-v8a

# (bool) Авто-принятие лицензий SDK
android.accept_sdk_license = True

# (str) Заставка и иконка (используем твой serpent.png)
presplash.filename = %(source.dir)s/serpent.png
icon.filename = %(source.dir)s/serpent.png

# (list) Позволяет приложению использовать больше RAM на телефоне
android.meta_data = largeHeap=true

# (bool) Копировать библиотеки напрямую
android.copy_libs = 1

# (str) Фильтр логов для отладки
android.logcat_filters = *:S python:D

[buildozer]

# (int) Уровень логов (2 — максимально подробно для поиска ошибок)
log_level = 2

# (int) Предупреждение при запуске от root
warn_on_root = 1

# (str) Папка для готового APK
bin_dir = ./bin

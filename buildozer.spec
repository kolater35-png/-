[app]
title = Titan OS
package.name = titanos
package.domain = org.nebula
source.dir = .
# Добавил .ttf для шрифтов и .json, если решишь хранить конфиги
source.include_exts = py,png,jpg,kv,atlas,db,css,cpp,h,ttf,json
version = 5.0

# --- УЛУЧШЕННЫЕ REQUIREMENTS ---
# 1. Добавил sqlite3 (для базы данных)
# 2. Добавил openssl (чтобы работало шифрование и https в requests)
# 3. Добавил hostpython3 (ускоряет сборку на сервере)
requirements = python3, kivy==2.3.0, kivymd==1.2.0, pillow, pyjnius, numpy, requests, certifi, sqlite3, openssl, hostpython3

# Разрешения — без них Android не даст сохранить базу данных или выйти в сеть
android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE

# Сокращаем архитектуры до одной самой важной (для скорости)
android.archs = arm64-v8a
android.api = 33
android.minapi = 21
android.ndk = 25b
android.accept_sdk_license = True

# Включаем полноэкранный режим для "эффекта ОС"
fullscreen = 1

[buildozer]
log_level = 2
warn_on_root = 1

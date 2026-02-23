[app]
title = Nebula Titan IDE
package.name = nebulatitan
package.domain = org.nebula
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json,db
version = 5.0.2

# Список зависимостей (Критически важно для работы БД и UI)
requirements = python3,kivy==2.3.0,kivymd==1.2.0,sqlite3,requests,urllib3,certifi,charset-normalizer,idna

orientation = portrait
fullscreen = 1
android.archs = arm64-v8a, armeabi-v7a
android.allow_backup = True

# Разрешения (Fix v1.0.0: доступ к памяти и интернет)
android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE, MANAGE_EXTERNAL_STORAGE

# Иконка и заставка (если есть файлы)
# icon.filename = %(source.dir)s/icon.png
# presplash.filename = %(source.dir)s/splash.png

# Настройки API (Android 13+)
android.api = 33
android.minapi = 21
android.sdk = 33
android.ndk = 25b

# Умная настройка клавиатуры
android.window_soft_input_mode = adjustPan

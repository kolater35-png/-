[app]
title = Nebula Titan OS
package.name = nebula_titan_os
package.domain = io.titan.core
source.dir = .
source.include_exts = py,png,jpg,kv,json,db,ttf
version = 5.0.3

# Только нужные библиотеки, без лишних пробелов
requirements = python3,kivy==2.2.1,kivymd==1.1.1,pillow,requests

# Иконка (временно закомментирована, чтобы исключить ошибку поиска файла)
# icon.filename = serpent.png

orientation = portrait
fullscreen = 1

# Базовые права
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

# Настройки SDK/NDK для Android 13 (API 33)
android.api = 33
android.minapi = 21
android.ndk = 25b
android.accept_sdk_license = True

# Оставляем ОДНУ архитектуру для ускорения и стабильности билда
android.archs = arm64-v8a

# Режим отладки
android.build_mode = debug

[buildozer]
log_level = 2
warn_on_root = 1

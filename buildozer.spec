[app]
title = Nebula Titan OS
package.name = nebula_titan_os
package.domain = io.titan.core
source.dir = .
source.include_exts = py,png,jpg,kv,json,db,ttf
version = 5.0.3

# Только база. Проверь, что в main.py нет других импортов!
requirements = python3,kivy==2.2.1,kivymd==1.1.1,pillow,requests

orientation = portrait
fullscreen = 1

android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE
android.api = 33
android.minapi = 21
android.ndk = 25b
android.accept_sdk_license = True

# Оставляем ТОЛЬКО arm64-v8a для 100% стабильности
android.archs = arm64-v8a

# Пропускать проверку обновлений самого себя для скорости
android.skip_update = True

[buildozer]
log_level = 2
warn_on_root = 1

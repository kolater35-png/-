[app]
title = Nebula Titan OS
package.name = nebula_titan_os
package.domain = io.titan.core
source.dir = .
source.include_exts = py,png,jpg,kv,json,db,ttf
version = 5.0.3

# Упрощаем до максимума для теста
requirements = python3,kivy,kivymd,pillow,requests

orientation = portrait
fullscreen = 1

android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE
android.api = 33
android.minapi = 21
android.ndk = 25b
android.accept_sdk_license = True
android.archs = arm64-v8a
# ВАЖНО: Разрешаем обновление, чтобы скачался aidl
android.skip_update = False

# Принудительно используем свежий упаковщик
p4a.branch = master

[buildozer]
log_level = 2
warn_on_root = 1

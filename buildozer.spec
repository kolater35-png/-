[app]
title = Nebula Titan OS
package.name = nebula_titan_os
package.domain = io.titan.core
source.dir = .
source.include_exts = py,png,jpg,kv,json,db,ttf
version = 5.0.3

# Только база. Если в коде есть другие импорты, добавь их сюда через запятую
requirements = python3,kivy,kivymd,pillow,requests

orientation = portrait
fullscreen = 1

android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE
android.api = 33
android.minapi = 21
android.ndk = 25b
android.accept_sdk_license = True
android.archs = arm64-v8a
android.skip_update = False

# Прямое указание использовать свежий код упаковщика (решает 90% проблем на финише)
p4a.branch = master

[buildozer]
log_level = 2
warn_on_root = 1

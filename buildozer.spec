[app]
title = Nebula Titan OS
package.name = nebula_titan_os
package.domain = io.titan.core
source.dir = .
source.include_exts = py,png,jpg,kv,json,db,ttf
version = 5.0.3

# Только основные требования
requirements = python3,kivy==2.2.1,kivymd==1.1.1,pillow,requests

# Пока без иконки (для теста стабильности)
# icon.filename = serpent.png

orientation = portrait
fullscreen = 1

android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE
android.api = 33
android.minapi = 21
android.ndk = 25b
android.accept_sdk_license = True
android.archs = arm64-v8a
android.build_mode = debug

[buildozer]
log_level = 2
warn_on_root = 1

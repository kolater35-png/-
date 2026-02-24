[app]
title = Titan OS
package.name = titanos
package.domain = org.nebula
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,db,css,cpp,h
version = 5.0

# Только стабильное ядро. Numpy — база для нейронок.
requirements = python3, kivy==2.3.0, kivymd==1.2.0, pillow, pyjnius, numpy, requests, certifi

orientation = portrait
fullscreen = 1

# Android настройки
android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE, MANAGE_EXTERNAL_STORAGE
android.api = 33
android.minapi = 21
android.ndk = 25b
android.accept_sdk_license = True
android.archs = arm64-v8a
android.enable_androidx = True

# Пути для твоих будущих C++ библиотек (.so)
android.add_libs_arm64_v8a = libs/arm64-v8a/*.so

[buildozer]
log_level = 2
warn_on_root = 1

[app]
title = Titan OS
package.name = titanos
package.domain = org.nebula
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,db,css,cpp,h,ttf
version = 5.0

# Добавили sqlite3 и openssl к твоим либам
requirements = python3, kivy==2.3.0, kivymd==1.2.0, pillow, pyjnius, numpy, requests, certifi, sqlite3, openssl

android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE
android.archs = arm64-v8a
android.api = 33
android.minapi = 21
android.ndk = 25b
android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 1

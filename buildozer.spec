[app]
title = Nebula Titan IDE
package.name = nebulatitan
package.domain = org.nebula
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json,db
version = 5.0.2

# Улучшенные требования: добавляем всё для полноценной работы IDE
requirements = python3==3.10.12,kivy==2.3.0,kivymd==1.2.0,sqlite3,requests,certifi,openssl,urllib3,chardet,idna

orientation = portrait
fullscreen = 1

# Используем максимально стабильную связку для Kivy
android.api = 31
android.minapi = 21
android.sdk = 31
android.ndk = 23b
android.ndk_api = 21

android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE, MANAGE_EXTERNAL_STORAGE
android.accept_sdk_license = True

# Использование ветки master исправляет баги линковки библиотек
p4a.branch = master

# Архитектура arm64-v8a обязательна для современных телефонов
android.archs = arm64-v8a
android.allow_backup = True

[buildozer]
log_level = 2
warn_on_root = 1

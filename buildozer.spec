[app]
title = Nebula Evolution
package.name = nebula.evo.pro
package.domain = org.nebula
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,env
version = 1.0.0

# Библиотеки для ИИ, Telegram и защищенных запросов (SSL/MESH)
requirements = python3,kivy==2.3.0,kivymd==1.1.1,pillow,requests,urllib3,charset-normalizer,idna,certifi,numpy,transformers,openssl,setuptools

orientation = portrait
android.archs = arm64-v8a
android.api = 33
android.minapi = 21

# Стабильный NDK и фикс ошибок компиляции
android.ndk = 25b
android.allow_mismatched_ndk = True
android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE, ACCESS_NETWORK_STATE, POST_NOTIFICATIONS
android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 1

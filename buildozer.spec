[app]
title = Nebula Evolution
package.name = nebula.evolution.ultramax
package.domain = org.nebula
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json
version = 1.0.0

# ВАЖНО: Список всех библиотек для нашего нового кода
requirements = python3,kivy==2.1.0,kivymd==1.1.1,requests,urllib3,certifi,charset-normalizer,idna,numpy

orientation = portrait
fullscreen = 0
android.archs = arm64-v8a, armeabi-v7a
android.allow_backup = True

# Разрешения для работы с интернетом и файлами (для сохранения конфигов)
android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE

# Иконка (если есть файл icon.png, если нет - закомментируй)
# icon.filename = icon.png

android.api = 31
android.minapi = 21
android.sdk = 31
android.ndk = 25b
android.skip_update = False
android.accept_sdk_license = True

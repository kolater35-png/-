[app]
title = Nebula Evolution
package.name = nebula_pro
package.domain = org.nebula
source.dir = .
source.include_exts = py,png,jpg,kv,json
version = 1.1.0

# ВАЖНО: Указываем все библиотеки, чтобы Змей и Интернет работали
requirements = python3,kivy==2.1.0,kivymd==1.1.1,requests,urllib3,certifi,chardet,idna

orientation = portrait
fullscreen = 0
android.archs = arm64-v8a, armeabi-v7a
android.allow_backup = True

# Иконка и заставка (если есть свои файлы)
# icon.filename = %(source.dir)s/icon.png
# presplash.filename = %(source.dir)s/serpent.png

# Запрос разрешений
android.permissions = INTERNET, READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE

# Настройка версии Android
android.api = 33
android.minapi = 21
android.ndk = 25b

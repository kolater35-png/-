[app]
title = Nebula Evolution
package.name = nebula_master_pro
package.domain = org.nebula
source.dir = .
source.include_exts = py,png,jpg,kv,json,txt
version = 3.3.8

# Мы оставили только стабильные зависимости. 
# Torch и Transformers убраны из билда, чтобы GitHub не упал.
requirements = python3, kivy==2.1.0, kivymd==1.1.1, requests, urllib3, numpy, python-telegram-bot, certifi, idna

orientation = portrait
android.permissions = INTERNET, READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE, MANAGE_EXTERNAL_STORAGE
android.api = 33
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a
android.accept_sdk_license = True

# Твой змей на иконке и заставке
presplash.filename = %(source.dir)s/serpent.png
icon.filename = %(source.dir)s/serpent.png

# Расширение памяти для приложения на телефоне
android.meta_data = largeHeap=true
android.copy_libs = 1
android.logcat_filters = *:S python:D

[buildozer]
log_level = 2
warn_on_root = 1
bin_dir = ./bin

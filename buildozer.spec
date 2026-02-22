[app]

# (str) Title of your application
title = Nebula Evolution Master

# (str) Package name
package.name = nebula_pro_master

# (str) Package domain (needed for android packaging)
package.domain = org.nebula

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let's include everything important)
source.include_exts = py,png,jpg,kv,json,txt,ttf

# (str) Application versioning (method 1)
version = 3.3.2

# (list) Application requirements
# Добавлены все твои зависимости. ВАЖНО: версия Cython фиксируется в YAML, а не здесь.
requirements = python3, kivy==2.1.0, kivymd==1.1.1, requests, urllib3, numpy, torch, transformers, python-telegram-bot, tqdm, certifi, idna

# (str) Supported orientations
orientation = portrait

# (list) Permissions
android.permissions = INTERNET, READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE, MANAGE_EXTERNAL_STORAGE

# (int) Target Android API, should be as high as possible.
android.api = 33

# (int) Minimum API your APK will support.
android.minapi = 21

# (str) Android NDK version to use
android.ndk = 25b

# (bool) Use --private data storage (True) or --dir public storage (False)
android.private_storage = True

# (list) Android architectures to build for (arm64 is a must for torch)
android.archs = arm64-v8a

# (str) Presplash and Icon (using your serpent.png)
presplash.filename = %(source.dir)s/serpent.png
icon.filename = %(source.dir)s/serpent.png

# (list) Meta-data to add to the AndroidManifest.xml
# ЭТОТ ПУНКТ КРИТИЧЕН ДЛЯ РАБОТЫ ТЯЖЕЛОГО ИИ
android.meta_data = largeHeap=true

# (bool) Accept SDK license
android.accept_sdk_license = True

# (str) The Android logcat filters to use
android.logcat_filters = *:S python:D

# (bool) Copy library instead of making a libpython.so
android.copy_libs = 1

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = off, 1 = on)
warn_on_root = 1

# (str) Path to build artifacts
bin_dir = ./bin

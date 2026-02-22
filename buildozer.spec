[app]

# (str) Title of your application
title = Nebula Evolution

# (str) Package name
package.name = nebula_master_pro

# (str) Package domain (needed for android packaging)
package.domain = org.nebula

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let's include everything)
source.include_exts = py,png,jpg,kv,json,txt

# (str) Application versioning
version = 3.3.5

# (list) Application requirements
# Мы оставляем ядро и тяжелый numpy. 
# ВАЖНО: torch и transformers на Android лучше подключать через tflite или onnx, 
# так как прямая сборка через pip ломает билд на GitHub.
requirements = python3, kivy==2.1.0, kivymd==1.1.1, requests, urllib3, numpy, python-telegram-bot, certifi, idna

# (str) Supported orientations
orientation = portrait

# (list) Permissions
android.permissions = INTERNET, READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE, MANAGE_EXTERNAL_STORAGE

# (int) Target Android API
android.api = 33

# (int) Minimum API your APK will support
android.minapi = 21

# (str) Android NDK version to use
android.ndk = 25b

# (list) Android architectures to build for
# arm64-v8a необходим для работы любых нейросетевых вычислений
android.archs = arm64-v8a

# (bool) Accept SDK license
android.accept_sdk_license = True

# (str) Presplash and Icon
presplash.filename = %(source.dir)s/serpent.png
icon.filename = %(source.dir)s/serpent.png

# (list) Meta-data to add to the AndroidManifest.xml
# Позволяет приложению запрашивать максимум RAM у телефона
android.meta_data = largeHeap=true

# (bool) Copy library instead of making a libpython.so
android.copy_libs = 1

# (str) The Android logcat filters to use
android.logcat_filters = *:S python:D

[buildozer]

# (int) Log level (2 = debug)
log_level = 2

# (int) Display warning if buildozer is run as root
warn_on_root = 1

# (str) Path to build artifacts
bin_dir = ./bin

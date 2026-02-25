[app]

# (str) Title of your application
title = Titan OS

# (str) Package name
package.name = titan_os

# (str) Package domain (needed for android packaging)
package.domain = org.immortal

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas,db,ttf

# (str) Application versioning
version = 7.0

# (list) Application requirements
# Добавлены все модули: NumPy для расчетов, SQLite3 для БД, OpenSSL для криптографии
requirements = python3,kivy==2.2.1,kivymd==1.2.0,numpy,sqlite3,pillow,openssl,requests,hostpython3

# (str) Custom source folders for requirements
# android.add_src = 

# (str) Presplash of the application
# presplash.filename = %(source.dir)s/data/presplash.png

# (str) Icon of the application
# icon.filename = %(source.dir)s/data/icon.png

# (str) Supported orientation (one of landscape, sensorLandscape, portrait or all)
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 1

# (list) Permissions
android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE

# (int) Target Android API, should be as high as possible.
android.api = 33

# (int) Minimum API your APK will support.
android.minapi = 21

# (str) Android NDK version to use
android.ndk = 25b

# (bool) If True, then skip trying to update the Android sdk
android.skip_update = False

# (bool) If True, then automatically accept SDK license
# Это критично для автоматической сборки в GitHub Actions
android.accept_sdk_license = True

# (str) Android logcat filters to use
android.logcat_filters = *:S python:D

# (str) Android architecture to build for, choices: armeabi-v7a, arm64-v8a, x86, x86_64
# Для ускорения билда на GitHub можно оставить только arm64-v8a
android.archs = arm64-v8a

# (bool) enables Android auto backup feature, false by default
android.allow_backup = True

# (list) The Android libs to copy to the libs/ directory
# android.add_libs_armeabi_v7a = libs/armeabi-v7a/*.so
# android.add_libs_arm64_v8a = libs/arm64-v8a/*.so

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1

# (str) Path to build artifacts (default is ./.buildozer)
# build_dir = ./.buildozer

# (str) Path to bin directory (default is ./bin)
# bin_dir = ./bin

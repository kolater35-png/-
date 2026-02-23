[app]
# (str) Title of your application
title = Nebula Titan IDE

# (str) Package name
package.name = nebulatitan

# (str) Package domain (needed for android packaging)
package.domain = org.nebula

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let's include everything important)
source.include_exts = py,png,jpg,kv,atlas,json,db

# (str) Application versioning
version = 5.0.2

# (list) Application requirements
# КРИТИЧЕСКИ ВАЖНО: Здесь все библиотеки, которые мы использовали в 12 частях кода
requirements = python3,kivy==2.3.0,kivymd==1.2.0,sqlite3,requests,certifi,urllib3,charset-normalizer,idna,openssl

# (str) Supported orientations
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 1

# =============================================================================
# Android specific
# =============================================================================

# (list) Permissions
# Разрешения для работы с файлами, интернетом и уведомлениями
android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE, MANAGE_EXTERNAL_STORAGE

# (int) Target Android API, should be as high as possible.
android.api = 33

# (int) Minimum API your APK will support.
android.minapi = 21

# (int) Android SDK version to use
android.sdk = 33

# (str) Android NDK version to use
android.ndk = 25b

# (bool) Use --private data storage (True is standard)
android.private_storage = True

# (str) Android NDK directory (leave empty for auto-download)
android.ndk_path = 

# (list) The Android architectures to build for.
# Для тестов на GitHub лучше оставить только arm64-v8a для скорости
android.archs = arm64-v8a

# (bool) Allow backup
android.allow_backup = True

# (str) XML file for network security (optional, but good for API)
# android.network_security_config = network_security_config.xml

# (bool) Accept SDK license
android.accept_sdk_license = True

# =============================================================================
# Buildozer settings
# =============================================================================

[buildozer]
# (int) Log level (2 = maximum debug info)
log_level = 2

# (int) Display warning if buildozer is run as root (0 = off)
warn_on_root = 1

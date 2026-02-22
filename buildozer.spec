[app]

# (str) Title of your application
title = Nebula Master Ultra

# (str) Package name
package.name = nebula_master_ultra

# (str) Package domain (needed for android packaging)
package.domain = org.nebula

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,json

# (str) Application versioning
version = 7.6.0

# (list) Application requirements
# ВАЖНО: Если билд упадет с ошибкой "Killed", удали torch и transformers из этого списка
requirements = python3,kivy==2.1.0,kivymd==1.1.1,pillow,requests,numpy,torch,transformers

# (str) Supported orientation (one of landscape, sensorLandscape, portrait or all)
orientation = portrait

# (list) Permissions
android.permissions = INTERNET,CAMERA,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE,MANAGE_EXTERNAL_STORAGE

# (int) Target Android API
android.api = 33

# (int) Minimum API your APK will support
android.minapi = 21

# (str) Android NDK version to use
android.ndk = 25b

# (list) Android architectures to build for
# Только arm64-v8a — это спасение для оперативной памяти сервера
android.archs = arm64-v8a

# (list) Android meta-data to set (key=value)
android.meta_data = largeHeap=true

# (bool) Use --copy-libs flag while packaging
android.copy_libs = 1

# (str) The format used to package the app for debug mode (apk or aab)
android.debug_artifact = apk

[buildozer]

# (int) Log level (2 = debug)
log_level = 2

# (int) Display warning if buildozer is run as root
warn_on_root = 1

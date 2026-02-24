[app]
# (str) Title of your application
title = TitanOS

# (str) Package name
package.name = titanos

# (str) Package domain (needed for android packaging)
package.domain = org.nebula

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let's keep it simple for now)
source.include_exts = py,png,jpg,kv,atlas

# (str) Application versioning
version = 0.1

# (list) Application requirements
# ВАЖНО: Мы фиксируем версии Kivy и KivyMD для стабильности сборки
requirements = python3,kivy==2.3.0,kivymd==1.2.0,pillow,requests,setuptools

# (str) Supported orientations
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
android.accept_sdk_license = True

# (str) Android architecture to build for
android.archs = arm64-v8a

# (int) Log level (0 = error only, 1 = info, 2 = debug)
# Ставим 2, чтобы видеть ВСЁ, если что-то пойдет не так
log_level = 2

# (str) The format used to package the app for release mode (aab or apk)
android.release_artifact = apk

[buildozer]
# (int) Log level (0 = error only, 1 = info, 2 = debug)
log_level = 2

# (int) Whether to display tokens (0 = no, 1 = yes)
display_icons = 0

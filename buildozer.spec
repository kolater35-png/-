[app]
# (str) Title of your application
title = TitanScan

# (str) Package name
package.name = titanscan

# (str) Package domain
package.domain = org.nebula

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include
source.include_exts = py,png,jpg,kv,atlas

# (str) Application versioning
version = 0.1

# ВНИМАНИЕ: Оставляем ТОЛЬКО kivy. 
# Мы добавим kivymd и остальное, когда этот скелет соберется.
requirements = python3,kivy==2.3.0

orientation = portrait
fullscreen = 1

# (list) Permissions
android.permissions = INTERNET

# (int) Target Android API
android.api = 33

# (int) Minimum API your APK will support
android.minapi = 21

# (str) Android NDK version to use
android.ndk = 25b

# (bool) Automatically accept SDK license
android.accept_sdk_license = True

# (str) Android architecture to build for
android.archs = arm64-v8a

# (int) Log level (2 = debug, самое важное сейчас)
log_level = 2

# (str) The format used to package the app
android.release_artifact = apk

[buildozer]
log_level = 2
warn_on_root = 1

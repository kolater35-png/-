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

# (str) Application versioning (method 1)
version = 7.6.0

# (list) Application requirements
# ВАЖНО: Только самое нужное. Torch и Transformers здесь.
requirements = python3, kivy==2.1.0, kivymd==1.1.1, pillow, requests, numpy, torch, transformers

# (str) Supported orientation (one of landscape, sensorLandscape, portrait or all)
orientation = portrait

# (list) Permissions
android.permissions = INTERNET, CAMERA, READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE, MANAGE_EXTERNAL_STORAGE

# (int) Target Android API, should be as high as possible.
android.api = 33

# (int) Minimum API your APK will support.
android.minapi = 21

# (str) Android NDK version to use
android.ndk = 25b

# (str) Android NDK directory (if empty, it will be automatically downloaded)
android.ndk_path =

# (str) Android SDK directory (if empty, it will be automatically downloaded)
android.sdk_path =

# (list) Android architectures to build for
# КРИТИЧЕСКИ ВАЖНО: Только arm64-v8a для экономии памяти GitHub Actions!
android.archs = arm64-v8a

# (list) Android meta-data to set (key=value)
# Позволяет приложению использовать больше RAM на телефоне
android.meta_data = largeHeap=true

# (bool) Use --copy-libs flag while packaging
android.copy_libs = 1

# (str) The Android arch to build for, choices: armeabi-v7a, arm64-v8a, x86, x86_64
# (Deprecated, use android.archs instead)
# android.arch = arm64-v8a

# (bool) indicates whether the screen should stay on
# android.wakelock = False

# (list) Android application meta-data to set (key=value)
# android.meta_data =

# (list) Android library project to add (will be added in the project.properties)
# android.library_references =

# (str) Android logcat filters to use
# android.logcat_filters = *:S python:D

# (bool) Copy library instead of making a lib dir. This is needed for some devices.
# android.copy_libs = 1

# (str) The format used to package the app for release mode (aab or apk)
android.release_artifact = apk

# (str) The format used to package the app for debug mode (apk or aab)
android.debug_artifact = apk

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1

# (str) Path to build artifact storage, can be a variable name, or relative or absolute path
# build_dir = ./.buildozer

# (str) Path to bin directory
# bin_dir = ./bin

[app]

# (str) Title of your application
title = Nebula Supernova OS

# (str) Package name
package.name = nebula_os

# (str) Package domain (needed for android packaging)
package.domain = org.titan.nebula

# (str) Source code where the main.py live
source.dir = .

# (str) Source files to include (let's include everything)
source.include_exts = py,png,jpg,kv,atlas,json,css,cpp,h,java

# (list) Application requirements
# ВАЖНО: pyjnius для Java, jnius для C++, openssl для сети
requirements = python3,kivy==2.3.0,kivymd,pyjnius,jnius,openssl,requests,chardet,urllib3,idna

# (str) Custom source folders for Java/C++ (если решишь выносить код в файлы)
# android.add_src = src/java,src/cpp

# (list) Permissions
android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE, CAMERA, VIBRATE

# (int) Target Android API, should be as high as possible.
android.api = 33

# (int) Minimum API your APK will support.
android.minapi = 21

# (str) Android NDK version to use
android.ndk = 25b

# (bool) Use the Python for Android toolchain directly
android.ndk_path = 

# (list) Android architectures to build for
android.archs = arm64-v8a, armeabi-v7a

# (list) Java classes to add to the compilation (JNI)
# android.add_jars = libs/some_java_lib.jar

# (str) Android entry point
android.entrypoint = org.kivy.android.PythonActivity

# (list) List of Java classes to exclude from the compilation
# android.javac_options = -Xlint:all

# (str) Android logcat filters
android.logcat_filters = *:S python:D

# (bool) Copy library instead of making a libpyaudio.so
android.copy_libs = 1

# (str) The Android arch to build for (only one if not using android.archs)
# android.arch = arm64-v8a

# =============================================================================
# [SECTION] NATIVE BUILD SETTINGS (C++ / NDK)
# =============================================================================

# (list) Path to custom C++ libraries (.so files)
# android.add_libs_armeabi_v7a = libs/armeabi-v7a/libnative.so
# android.add_libs_arm64_v8a = libs/arm64-v8a/libnative.so

# (bool) Enable Android auto backup
android.allow_backup = True

# (str) Icon of the application
# icon.filename = %(source.dir)s/data/icon.png

# (str) Supported orientation
orientation = portrait

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = off, 1 = on)
warn_on_root = 1

# (str) Path to build artifacts
build_dir = ./.buildozer

# (str) Path to bin directory
bin_dir = ./bin

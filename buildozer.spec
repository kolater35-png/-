[app]
title = Nebula Titan OS
package.name = titanos
package.domain = org.nebula
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,db,cpp,h,java,css
version = 5.0

# Основное ядро. Numpy позволит делать расчеты, 
# а мосты C++ и JNI свяжут нас с железом.
requirements = python3, kivy==2.3.0, kivymd==1.2.0, pillow, pyjnius, numpy, requests

android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE, MANAGE_EXTERNAL_STORAGE
android.api = 33
android.minapi = 21
android.ndk = 25b
android.accept_sdk_license = True
android.archs = arm64-v8a
p4a.branch = master

# Включаем поддержку современных Android-библиотек
android.gradle_dependencies = 'androidx.multidex:multidex:2.0.1'
android.enable_androidx = True

# Директории для твоих будущих нативных библиотек (.so)
android.add_libs_arm64_v8a = libs/arm64-v8a/*.so

[buildozer]
log_level = 2
warn_on_root = 1

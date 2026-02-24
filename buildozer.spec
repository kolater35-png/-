[app]
title = Nebula Titan OS
package.name = titanos
package.domain = org.nebula
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,db,cpp,h,java,css
version = 5.0

# Добавляем numpy (база для торча) и компиляторы
requirements = python3,kivy==2.3.0,kivymd==1.2.0,pyjnius,pillow,sqlite3,numpy,openssl

android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE, MANAGE_EXTERNAL_STORAGE
android.api = 33
android.minapi = 21
android.ndk = 25b
android.accept_sdk_license = True
# Включаем все архитектуры для поддержки нативного кода
android.archs = arm64-v8a, armeabi-v7a

# Важно для C++ и Java мостов
android.gradle_dependencies = 'androidx.appcompat:appcompat:1.4.1'
p4a.branch = master

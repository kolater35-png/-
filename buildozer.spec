[app]
title = Nebula Titan OS
package.name = titanos
package.domain = org.nebula
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,db,css,cpp,h,java
version = 7.0

# Основные зависимости. Важно: sqlite3 и openssl нужны для работы базы и сети
requirements = python3, kivy==2.3.0, kivymd==1.2.0, pillow, pyjnius, numpy, sqlite3, openssl

android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE, MANAGE_EXTERNAL_STORAGE
android.api = 33
android.minapi = 21
android.ndk = 25b
android.accept_sdk_license = True

# Собираем под 64-битную архитектуру (самая стабильная и быстрая)
android.archs = arm64-v8a

# Настройки для компиляции нативного кода, если он будет
android.gradle_dependencies = 'androidx.appcompat:appcompat:1.4.1'
p4a.branch = master

[buildozer]
log_level = 2
warn_on_root = 1

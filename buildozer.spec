[app]
title = Nebula Titan IDE
package.name = nebulatitan
package.domain = org.nebula
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json,db
version = 5.0.2

# Здесь важен каждый символ!
requirements = python3==3.10.12,kivy==2.3.0,kivymd==1.2.0,sqlite3,requests,certifi,openssl

orientation = portrait
fullscreen = 1

android.api = 33
android.minapi = 21
android.sdk = 33
android.ndk = 25b
android.ndk_api = 21

android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE, MANAGE_EXTERNAL_STORAGE
android.accept_sdk_license = True
android.archs = arm64-v8a
android.allow_backup = True
# Этот параметр лечит ошибку путей, которую ты кидал раньше
p4a.branch = master

[buildozer]
log_level = 2
warn_on_root = 1

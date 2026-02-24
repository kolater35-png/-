[app]
title = TitanOS
package.name = titanos
package.domain = org.nebula
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 5.0.0

requirements = python3,kivy==2.3.0,kivymd==1.2.0,pillow,requests,pygments,setuptools

android.api = 33
android.minapi = 21
android.ndk = 25b
android.accept_sdk_license = True
android.skip_update = False
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

# Одна архитектура = в 2 раза меньше шансов на "невидимую ошибку"
android.archs = arm64-v8a

# Ставим 1, чтобы сэкономить память сервера и видеть только критику
log_level = 1
android.release_artifact = apk

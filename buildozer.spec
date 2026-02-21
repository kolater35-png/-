[app]
title = Nebula Super-Quantum
package.name = nebula.quantum.v8
package.domain = org.nebula
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,env
version = 8.0.0

# Добавлены зависимости для файлового менеджера и работы с данными
requirements = python3,kivy==2.3.0,kivymd==1.1.1,pillow,requests,numpy,pandas,transformers,tqdm,openssl,setuptools,sqlite3

orientation = portrait
android.archs = arm64-v8a
android.api = 33
android.minapi = 21
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,MANAGE_EXTERNAL_STORAGE
android.accept_sdk_license = True

[buildozer]
log_level = 2

[app]
title = Nebula Quantum Pro
package.name = nebula.quantum.v5
package.domain = org.nebula
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,env
version = 5.2.0

# ВАЖНО: Весь мощный стек здесь
requirements = python3,kivy==2.3.0,kivymd==1.1.1,pillow,requests,numpy,pandas,scipy,openssl,setuptools

orientation = portrait
android.archs = arm64-v8a
android.api = 33
android.minapi = 21
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,MANAGE_EXTERNAL_STORAGE
android.accept_sdk_license = True

[buildozer]
log_level = 2

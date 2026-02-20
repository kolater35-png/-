[app]
title = Nebula Pro
package.name = nebula_pro
package.domain = org.nebula
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 2.8.0

# ВАЖНО: Убрали лишние запятые и зафиксировали KivyMD через GitHub
requirements = python3,kivy==2.3.0,https://github.com/kivymd/KivyMD/archive/master.zip,requests,urllib3,openssl,setuptools

orientation = portrait
android.archs = arm64-v8a
android.api = 33
android.minapi = 21
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,MANAGE_EXTERNAL_STORAGE
android.accept_sdk_license = True

# Используем стабильную ветку python-for-android
p4a.branch = master

[buildozer]
log_level = 2

[app]
title = Nebula AI Pro
package.name = nebula_ai_pro
package.domain = org.nebula
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 2.6.0

# ВАЖНО: Используем прямую ссылку на KivyMD
requirements = python3==3.10.0,kivy==2.3.0,https://github.com/kivymd/KivyMD/archive/master.zip,requests,urllib3,openssl,setuptools

orientation = portrait
android.archs = arm64-v8a
android.api = 33
android.minapi = 21
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,MANAGE_EXTERNAL_STORAGE
android.accept_sdk_license = True
p4a.branch = master

[buildozer]
log_level = 2
warn_on_root = 1

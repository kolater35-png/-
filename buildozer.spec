[app]
title = Nebula Pro
package.name = nebula_pro
package.domain = org.nebula
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,env
version = 3.5.0

# ДОБАВЛЕН PILLOW — без него иконки KivyMD крашат приложение!
requirements = python3,kivy==2.3.0,kivymd==1.1.1,pillow,requests,urllib3,openssl

orientation = portrait
android.archs = arm64-v8a
android.api = 33
android.minapi = 21
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,MANAGE_EXTERNAL_STORAGE
android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 1

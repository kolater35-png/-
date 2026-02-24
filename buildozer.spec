[app]
title = TitanOS
package.name = titanos
package.domain = org.nebula
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 2.5.0

# Только проверенное мясо, без пробелов (важно для парсера)
requirements = python3,kivy==2.3.0,kivymd==1.2.0,pillow,requests,pygments,setuptools

android.api = 33
android.minapi = 21
android.ndk = 25b
android.accept_sdk_license = True
android.skip_update = False
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

# Одна современная архитектура - залог успешного билда без вылетов
android.archs = arm64-v8a

# Тихий лог, чтобы GitHub не обрывал связь
log_level = 1
android.release_artifact = apk

[buildozer]
warn_on_root = 1

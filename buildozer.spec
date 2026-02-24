[app]
title = TitanOS
package.name = titanos
package.domain = org.nebula
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 4.0.0

requirements = python3,kivy==2.3.0,kivymd==1.2.0,pillow,requests,pygments,setuptools

android.api = 33
android.minapi = 21
android.ndk = 25b
# ФИКС ЛИЦЕНЗИЙ: Теперь 'yes |' не нужен
android.accept_sdk_license = True
android.skip_update = False
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

# ФИКС BROKEN PIPE: Только одна мощная архитектура
android.archs = arm64-v8a

log_level = 1
android.release_artifact = apk

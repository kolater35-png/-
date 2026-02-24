[app]
title = TitanOS
package.name = titanos
package.domain = org.nebula
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.1.0

# Только самое необходимое «мясо», чтобы не перегружать компилятор
requirements = python3, kivy==2.3.0, kivymd==1.2.0, pillow, requests, pygments, setuptools

android.api = 33
android.minapi = 21
android.ndk = 25b
android.accept_sdk_license = True
android.skip_update = False
android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE

# КРИТИЧЕСКИЙ ФИКС: Собираем ТОЛЬКО под одну архитектуру.
# Это уберет ошибку Broken Pipe, так как объем логов сократится вдвое.
android.archs = arm64-v8a

# Оптимизация сборки
android.release_artifact = apk
log_level = 2

[buildozer]
log_level = 2
warn_on_root = 1

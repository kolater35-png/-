[app]
title = TitanOS
package.name = titanos
package.domain = org.nebula
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0.0

# ВАЖНО: Добавлены все пакеты для 'мяса'
requirements = python3, kivy==2.3.0, kivymd==1.2.0, pillow, requests, aiohttp, pygments, setuptools

android.api = 33
android.minapi = 21
android.ndk = 25b
android.accept_sdk_license = True
android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE
android.archs = arm64-v8a, armeabi-v7a

[app]
title = Nebula Master Ultra
package.name = nebula_master_ultra
package.domain = org.nebula.core
source.dir = .
source.include_exts = py,png,jpg,kv,json
version = 6.0.0

# ВАЖНО: Список всех библиотек (тяжелые в конце)
requirements = python3, kivy==2.1.0, kivymd==1.1.1, pillow, requests, certifi, plyer, numpy, torch, transformers, opencv-python

orientation = portrait
# Разрешения для Android
android.permissions = INTERNET, CAMERA, READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE, VIBRATE, MANAGE_EXTERNAL_STORAGE
android.api = 33
android.minapi = 21
android.ndk = 25b

# Используем только arm64-v8a для экономии места и оперативной памяти при билде
android.archs = arm64-v8a
android.accept_sdk_license = True
android.meta_data = largeHeap=true

[buildozer]
log_level = 2
warn_on_root = 1

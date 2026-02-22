[app]
title = Nebula Master Ultra
package.name = nebula.master.ultra
package.domain = org.nebula
source.dir = .
source.include_exts = py,png,jpg,kv,json
version = 7.5.0

# ВАЖНО: Только необходимые зависимости. 
# Мы добавляем numpy и torch, но ограничиваем архитектуру, чтобы не раздувать билд.
requirements = python3, kivy==2.1.0, kivymd==1.1.1, pillow, requests, certifi, numpy, torch, transformers

orientation = portrait
android.permissions = INTERNET, CAMERA, READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE, VIBRATE, MANAGE_EXTERNAL_STORAGE

android.api = 33
android.minapi = 21
android.ndk = 25b
# Оставляем ТОЛЬКО arm64-v8a. Сборка под две архитектуры на GitHub гарантированно упадет по памяти.
android.archs = arm64-v8a

# Разрешаем приложению использовать больше оперативной памяти на телефоне
android.meta_data = largeHeap=true
android.copy_libs = 1

[buildozer]
log_level = 2
warn_on_root = 1

[app]
title = Nebula Ultra Core
package.name = nebula_ultra_core
package.domain = org.nebula
source.dir = .
source.include_exts = py,png,jpg,kv,json
version = 8.0.0

# НЕ пишем torch сюда (сборка упадет). Ставим через PIP Manager в приложении.
requirements = python3,kivy==2.1.0,kivymd==1.1.1,pillow,requests,numpy

orientation = portrait
# Разрешения для управления файлами и камерой
android.permissions = INTERNET,CAMERA,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE,MANAGE_EXTERNAL_STORAGE,VIBRATE

android.api = 33
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a
android.meta_data = largeHeap=true
android.copy_libs = 1

[buildozer]
log_level = 2
warn_on_root = 1

[app]
title = Nebula Master Ultra
package.name = nebula.master.ultra
package.domain = org.nebula
source.dir = .
source.include_exts = py,png,jpg,kv,json
version = 10.0.0

# В требованиях только база. Тяжелые либы ставит сам main.py при запуске.
# Это единственный способ не уронить билд на GitHub.
requirements = python3,kivy==2.1.0,kivymd==1.1.1,pillow,requests,certifi

orientation = portrait
android.permissions = INTERNET,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE,MANAGE_EXTERNAL_STORAGE,WAKE_LOCK
android.api = 33
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a

# Оптимизация памяти для Torch
android.meta_data = largeHeap=true,kivy.graphics.gles=2
android.copy_libs = 1
android.window_layout_attribute = android:windowSoftInputMode="adjustResize"

[buildozer]
log_level = 2
warn_on_root = 1

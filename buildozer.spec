[app]
title = Nebula Master Ultra
package.name = nebula.master.ultra
package.domain = org.nebula
source.dir = .
source.include_exts = py,png,jpg,kv,json
version = 7.5.0

# Включаем Torch и Transformers обратно, добавляя необходимые зависимости для их сборки
requirements = python3, kivy==2.1.0, kivymd==1.1.1, pillow, requests, certifi, numpy, torch, transformers, tqdm, packaging, filelock

orientation = portrait
android.permissions = INTERNET, CAMERA, READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE, VIBRATE, MANAGE_EXTERNAL_STORAGE

# Использование NDK 25b или выше критично для сборки современных нейросетей
android.api = 33
android.minapi = 21
android.ndk = 25b
android.ndk_path = 
android.sdk_path = 

# Оставляем только одну архитектуру для экономии ресурсов при билде
android.archs = arm64-v8a

# Пытаемся выделить больше памяти для Java
android.meta_data = largeHeap=true

# Это поможет избежать ошибок при упаковке тяжелых .so файлов
android.copy_libs = 1
android.p4a_whitelist = 

[buildozer]
log_level = 2
warn_on_root = 1

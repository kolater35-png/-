[app]
# Основная информация
title = Nebula Master Ultra
package.name = nebula_master_ultra
package.domain = org.nebula
source.dir = .
source.include_exts = py,png,jpg,kv,json
version = 7.6.0

# Зависимости (БЕЗ пробелов после запятых!)
requirements = python3,kivy==2.1.0,kivymd==1.1.1,pillow,requests,numpy,torch,transformers

# Настройки экрана и прав
orientation = portrait
android.permissions = INTERNET,CAMERA,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE,MANAGE_EXTERNAL_STORAGE

# Версии инструментов (API 33 нужен для современных систем)
android.api = 33
android.minapi = 21
android.ndk = 25b

# ПУТИ ДОЛЖНЫ БЫТЬ ПУСТЫМИ (Buildozer найдет их сам в GitHub Actions)
android.ndk_path = 
android.sdk_path = 

# КРИТИЧЕСКИ ВАЖНО: Только 64-битная архитектура
android.archs = arm64-v8a

# Оптимизация памяти
android.meta_data = largeHeap=true
android.copy_libs = 1

[buildozer]
log_level = 2
warn_on_root = 1

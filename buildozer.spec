[app]
# Название твоего приложения в лаунчере
title = Nebula Evolution
package.name = nebula.evolution.ai
package.domain = org.nebula

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,env
version = 1.0.0

# Список библиотек (Включая Transformers и поддержку языков)
requirements = python3,kivy==2.3.0,kivymd==1.1.1,pillow,requests,numpy,pandas,transformers,tqdm,openssl,setuptools

orientation = portrait
android.archs = arm64-v8a
android.api = 33
android.minapi = 21

# ВАЖНО: Стабильная версия NDK для компиляции нейросетей
android.ndk = 25b
android.ndk_path = 
android.allow_mismatched_ndk = True

# Разрешения (Интернет и память)
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,MANAGE_EXTERNAL_STORAGE
android.accept_sdk_license = True

# Иконка (если есть файл icon.png, раскомментируй)
# icon.filename = %(source.dir)s/icon.png

[buildozer]
log_level = 2
warn_on_root = 1

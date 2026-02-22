[app]
title = Nebula Evolution
package.name = nebula.ultra.ide
package.domain = org.nebula
source.dir = .
source.include_exts = py,png,json,kv
version = 1.0.0

# Самая важная строка: прописываем тяжелые либы
requirements = python3, kivy==2.1.0, kivymd==1.1.1, requests, pip, setuptools, numpy, torch, transformers, tqdm, certifi

orientation = portrait
android.permissions = INTERNET, READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE
android.api = 33
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a
android.accept_sdk_license = True
android.skip_update = False

[buildozer]
log_level = 2
warn_on_root = 1

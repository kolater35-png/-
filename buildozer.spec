[app]
title = Nebula AI Pobeda
package.name = nebula.ai.pobeda
package.domain = org.nebula
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0.0

# ВАЖНО: Весь набор библиотек для ИИ
requirements = python3==3.10.0,kivy==2.3.0,kivymd==1.1.1,requests,paramiko,cryptography,torch,transformers,numpy,tqdm

orientation = portrait
android.archs = arm64-v8a
android.api = 33
android.minapi = 21
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE
android.accept_sdk_license = True

# Оптимизация для тяжелых проектов
android.skip_update = False
p4a.branch = master

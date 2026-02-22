[app]
title = Nebula Ultra
package.name = nebula_pro
package.domain = org.nebula
source.dir = .
source.include_exts = py,png,json,kv
version = 3.2.0

requirements = python3, kivy==2.1.0, kivymd==1.1.1, requests, torch, transformers, numpy, python-telegram-bot

orientation = portrait
android.permissions = INTERNET, READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE, MANAGE_EXTERNAL_STORAGE
android.api = 33
android.archs = arm64-v8a
android.accept_sdk_license = True

presplash.filename = %(source.dir)s/serpent.png
icon.filename = %(source.dir)s/serpent.png

[buildozer]
log_level = 2

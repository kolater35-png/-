[app]
title = Nebula Evolution
package.name = nebula_master_stable
package.domain = org.nebula
source.dir = .
source.include_exts = py,png,jpg,kv,json
version = 1.2.0

# Только стабильные библиотеки для успешного билда
requirements = python3, kivy==2.1.0, kivymd==1.1.1, requests, certifi

orientation = portrait
android.permissions = INTERNET, READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE
android.api = 33
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a
android.accept_sdk_license = True

presplash.filename = %(source.dir)s/serpent.png
icon.filename = %(source.dir)s/serpent.png

android.meta_data = largeHeap=true
android.copy_libs = 1

[buildozer]
log_level = 2
warn_on_root = 1

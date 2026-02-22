[app]
title = Nebula Master Ultra
package.name = nebula.master.ultra
package.domain = org.nebula
source.dir = .
source.include_exts = py,png,jpg,kv,json
version = 7.0.0

requirements = python3, kivy==2.1.0, kivymd==1.1.1, pillow, requests, certifi, plyer, numpy, torch, transformers, opencv

orientation = portrait
android.permissions = INTERNET, CAMERA, READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE, VIBRATE, MANAGE_EXTERNAL_STORAGE
android.api = 33
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a
android.accept_sdk_license = True
android.meta_data = largeHeap=true

[buildozer]
log_level = 2
warn_on_root = 1

[app]
title = Nebula Master
package.name = nebula_master_v1
package.domain = org.nebula
source.dir = .
source.include_exts = py,png,jpg,kv,json
version = 1.0.0

# Только самое необходимое. Если это соберется — будем добавлять остальное.
requirements = python3, kivy==2.1.0, kivymd==1.1.1, requests, certifi

orientation = portrait
android.permissions = INTERNET, READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE
android.api = 33
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a
android.accept_sdk_license = True

# Убедись, что serpent.png лежит в корне!
presplash.filename = %(source.dir)s/serpent.png
icon.filename = %(source.dir)s/serpent.png

android.meta_data = largeHeap=true
android.copy_libs = 1

[buildozer]
log_level = 2
warn_on_root = 1

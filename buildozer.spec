[app]
title = Nebula Stable
package.name = nebula_stable
package.domain = org.nebula
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 3.0.0

# Только базовые и надежные зависимости
requirements = python3,kivy==2.3.0,requests,urllib3,openssl

orientation = portrait
android.archs = arm64-v8a
android.api = 33
android.minapi = 21
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE
android.accept_sdk_license = True
p4a.branch = master

[buildozer]
log_level = 2

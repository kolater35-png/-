[app]
title = TitanScan
package.name = titanscan
package.domain = org.nebula
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1

# Оставляем только чистый Kivy для скорости компиляции
requirements = python3,kivy==2.3.0

orientation = portrait
fullscreen = 1
android.archs = arm64-v8a
android.api = 33
android.minapi = 21
android.ndk = 25b
android.accept_sdk_license = True

[buildozer]
log_level = 2

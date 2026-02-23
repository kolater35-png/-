[app]
title = Nebula Titan OS
package.name = nebulatitan
package.domain = org.titan
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,db
version = 5.0.4

# Добавили только самое необходимое
requirements = python3, kivy==2.3.0, kivymd, pyjnius, sqlite3, hostpython3

android.permissions = WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE, VIBRATE, INTERNET

android.api = 33
android.minapi = 21
android.ndk = 25b
android.ndk_api = 21
android.archs = arm64-v8a
android.copy_libs = 1

[buildozer]
log_level = 2
warn_on_root = 1

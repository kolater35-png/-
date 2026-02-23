[app]
title = Nebula Titan OS
package.name = nebulatitan
package.domain = org.titan
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,db
version = 5.0.4

# КРИТИЧЕСКИ ВАЖНО: sqlite3 и pyjnius для Hardware Bridge
requirements = python3, kivy==2.3.0, kivymd, pyjnius, sqlite3, hostpython3

orientation = portrait
fullscreen = 0

# Права доступа
android.permissions = WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE, VIBRATE, INTERNET

# Настройки SDK / NDK
android.api = 33
android.minapi = 21
android.ndk = 25b
android.ndk_api = 21

# Архитектура (для современных смартфонов)
android.archs = arm64-v8a

# Дополнительные настройки стабильности
android.copy_libs = 1
android.allow_backup = True
android.setup_pause = True

[buildozer]
log_level = 2
warn_on_root = 1

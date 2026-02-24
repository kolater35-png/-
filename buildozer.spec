[app]
title = Titan OS
package.name = titanos
package.domain = org.nebula
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,db
version = 5.5.0

# Тщательно отобранные требования (без лишнего мусора)
requirements = python3,kivy==2.3.0,kivymd==1.2.0,pillow,requests,pygments,setuptools,sqlite3

orientation = portrait
fullscreen = 0
android.archs = arm64-v8a

# --- [ANDROID SETTINGS] ---
android.api = 33
android.minapi = 21
# Важно: NDK 25b — самая стабильная версия для Kivy 2.3.0
android.ndk = 25b
android.accept_sdk_license = True
android.skip_update = False

# Разрешения (Добавлены все нужные для твоих модулей)
android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE

# --- [FIX: BROKEN PIPE & LOG SPAM] ---
# Ставим уровень 1, чтобы GitHub не обрывал связь из-за гигантских логов
log_level = 1
android.release_artifact = apk

[buildozer]
log_level = 1
warn_on_root = 1

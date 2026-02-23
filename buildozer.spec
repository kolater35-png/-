[app]
# (str) Название твоего приложения
title = Nebula Titan IDE

# (str) Имя пакета
package.name = nebulatitan

# (str) Домен
package.domain = org.nebula

# (str) Где лежит main.py (точка — корень проекта)
source.dir = .

# (list) Какие файлы включаем в сборку
source.include_exts = py,png,jpg,kv,atlas,json,db

# (str) Версия
version = 5.0.2

# (list) Зависимости. Здесь база для работы IDE и интернета.
requirements = python3==3.10.12,kivy==2.3.0,kivymd==1.2.0,sqlite3,requests,certifi,openssl

# (str) Ориентация
orientation = portrait

# (bool) Полный экран
fullscreen = 1

# =============================================================================
# Android Specific Settings
# =============================================================================

# (list) Разрешения. Добавляем доступ к файлам для IDE.
android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE, MANAGE_EXTERNAL_STORAGE

# (int) Target API (33 — требование Google Play)
android.api = 33

# (int) Minimum API
android.minapi = 21

# (int) Версии SDK и NDK
android.sdk = 33
android.ndk = 25b
android.ndk_api = 21

# (bool) Принимать лицензии автоматически (КРИТИЧНО)
android.accept_sdk_license = True

# (str) Ветка p4a. Master лечит проблему с "FileNotFoundError" путей
p4a.branch = master

# (list) Архитектура процессора (оставляем только одну для скорости)
android.archs = arm64-v8a

# (bool) Разрешить бэкап
android.allow_backup = True

# =============================================================================
# Buildozer Settings
# =============================================================================

[buildozer]
# (int) Уровень логов (2 — чтобы мы видели каждую ошибку)
log_level = 2

# (int) Предупреждение о запуске от root
warn_on_root = 1

# --- ВНИМАНИЕ: Не раскомментируй buildozer_dir в GitHub Actions ---

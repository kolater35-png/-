[app]
# (str) Название приложения
title = Nebula Titan IDE

# (str) Имя пакета (без пробелов и спецсимволов)
package.name = nebulatitan

# (str) Домен пакета
package.domain = org.nebula

# (str) Папка с исходниками (точка означает текущую папку)
source.dir = .

# (list) Расширения файлов, которые нужно включить в APK
source.include_exts = py,png,jpg,kv,atlas,json,db

# (str) Версия приложения
version = 5.0.2

# (list) Зависимости. Важно: фиксируем версии для стабильности на Android 13+
requirements = python3==3.10.12,kivy==2.3.0,kivymd==1.2.0,sqlite3,requests,certifi,openssl

# (str) Ориентация экрана
orientation = portrait

# (bool) Полноэкранный режим
fullscreen = 1

# =============================================================================
# Настройки Android
# =============================================================================

# (list) Разрешения. MANAGE_EXTERNAL_STORAGE нужен для полноценной IDE
android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE, MANAGE_EXTERNAL_STORAGE

# (int) Target Android API (33 — стандарт для 2024-2026)
android.api = 33

# (int) Minimum API
android.minapi = 21

# (int) Android SDK version
android.sdk = 33

# (str) Android NDK version
android.ndk = 25b

# (int) Android NDK API (должен быть равен или меньше minapi)
android.ndk_api = 21

# (bool) Автоматическое принятие лицензий SDK (Критично для GitHub Actions!)
android.accept_sdk_license = True

# (str) Ветка python-for-android. Используем master для исправления багов путей
p4a.branch = master

# (list) Архитектуры. Оставляем только одну для ускорения сборки в 3 раза
android.archs = arm64-v8a

# (bool) Разрешить бэкап данных
android.allow_backup = True

# =============================================================================
# Настройки сборщика
# =============================================================================

[buildozer]
# (int) Уровень логов (2 = максимально подробно, чтобы видеть ошибки)
log_level = 2

# (int) Предупреждение при запуске от root (в Docker/Actions это норма)
warn_on_root = 1

# (str) Папка для хранения скачанных инструментов (оставляем по умолчанию)
# buildozer_dir = .buildozer

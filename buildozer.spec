[app]
# Название приложения
title = Nebula Titan IDE
# Название пакета
package.name = nebulatitan
# Домен (твое имя или компания)
package.domain = org.nebula

# Список расширений файлов для включения
source.include_exts = py,png,jpg,kv,atlas,db

# Версия приложения
version = 5.0.1

# ТРЕБОВАНИЯ (Зависимости)
# Очень важно: указываем все библиотеки, которые мы использовали
requirements = python3,kivy,kivymd,sqlite3,pyjnius

# Ориентация экрана
orientation = portrait

# РАЗРЕШЕНИЯ (Permissions)
# Чтение и запись файлов (для File Manager) и интернет
android.permissions = READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE, INTERNET, MANAGE_EXTERNAL_STORAGE

# (android) Иконка приложения (можешь заменить на свою)
# icon.filename = %(source.dir)s/icon.png

# (android) API уровень
android.api = 33
android.minapi = 21
android.ndk = 25b
android.sdk = 33

# (android) Архитектуры (arm64 для новых телефонов)
android.archs = arm64-v8a, armeabi-v7a

# Включаем SQLite в сборку
android.copy_libs = 1

[buildozer]
# Уровень логирования (2 — самый подробный)
log_level = 2
warn_on_root = 1

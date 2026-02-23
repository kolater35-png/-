[app]
# (str) Название приложения
title = Nebula Titan IDE

# (str) Имя пакета
package.name = nebulatitan

# (str) Домен пакета
package.domain = org.nebula

# (str) Директория с исходным кодом (точка означает текущую директорию)
source.dir = .

# (list) Расширения файлов, которые нужно включить в APK
source.include_exts = py,png,jpg,kv,atlas,json,db

# (str) Версия приложения
version = 5.0.2

# (list) Полный список зависимостей твоей IDE. 
# hostpython3 гарантирует правильную кросс-компиляцию.
requirements = python3==3.10.12,hostpython3==3.10.12,kivy==2.3.0,kivymd==1.2.0,sqlite3,requests,certifi,openssl,urllib3,chardet,idna

# (str) Ориентация экрана
orientation = portrait

# (bool) Полноэкранный режим
fullscreen = 1

# =============================================================================
# Настройки Android
# =============================================================================

# (int) Target API (33 - современный стандарт)
android.api = 33

# (int) Minimum API
android.minapi = 21

# (int) Версия Android SDK
android.sdk = 33

# (str) Версия Android NDK (25b - официальная поддержка для API 33)
android.ndk = 25b

# (int) NDK API
android.ndk_api = 21

# (list) Разрешения, необходимые для полноценной работы IDE с файлами и сетью
android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE, MANAGE_EXTERNAL_STORAGE

# (bool) Автоматически принимать лицензии SDK
android.accept_sdk_license = True

# (str) Ветка python-for-android
p4a.branch = master

# (list) Архитектура процессора (64-бит, стандарт для современных устройств)
android.archs = arm64-v8a

# (bool) Разрешить резервное копирование приложения
android.allow_backup = True

# =============================================================================
# Настройки Buildozer
# =============================================================================

[buildozer]
# (int) Уровень логирования (2 = отладка, показывает все процессы)
log_level = 2

# (int) Предупреждать о запуске от имени root
warn_on_root = 1

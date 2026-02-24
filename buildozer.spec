[app]
# (section) Название и домен
title = TitanOS
package.name = titanos
package.domain = org.nebula

# (section) Исходники
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0.9

# (section) МЯСО: ТРЕБОВАНИЯ
# Здесь прописаны стабильные версии, которые не конфликтуют друг с другом
requirements = python3, kivy==2.3.0, kivymd==1.2.0, pillow, requests, aiohttp, pygments, setuptools

# (section) ПАРАМЕТРЫ ANDROID
android.api = 33
android.minapi = 21
android.ndk = 25b
android.accept_sdk_license = True
android.skip_update = False
android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE

# (section) КРИТИЧЕСКИЙ ФИКС: АРХИТЕКТУРА
# Мы убрали armeabi-v7a, чтобы билд не падал от перегрузки логов
android.archs = arm64-v8a

# (section) ГРАФИКА И ИНТЕРФЕЙС
orientation = portrait
fullscreen = 0
android.presplash_color = #050508

# (section) СИСТЕМНЫЕ НАСТРОЙКИ
# Повышаем уровень логирования, чтобы видеть реальные ошибки C-компилятора
log_level = 2
warn_on_root = 1

[buildozer]
# (section) Папка для сборки
build_dir = ./.buildozer
bin_dir = ./bin

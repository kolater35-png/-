[app]
# (str) Название приложения
title = Titan
# (str) Имя пакета
package.name = titan
# (str) Домен
package.domain = org.nebula

# (str) Где лежит main.py
source.dir = .
# (list) Какие файлы берем в сборку (только самое нужное)
source.include_exts = py,png,jpg,kv,atlas

# (str) Версия
version = 0.1

# ВАЖНО: Пока оставляем только базу! 
# Твои 1400 строк и kivymd добавим, когда создастся кэш.
requirements = python3,kivy==2.3.0

# (str) Ориентация экрана
orientation = portrait
fullscreen = 1

# --- ANDROID НАСТРОЙКИ ---
# (list) Разрешения
android.permissions = INTERNET
# (int) Целевой API
android.api = 33
# (int) Минимальный API
android.minapi = 21
# (str) Версия NDK (самая стабильная для этого контейнера)
android.ndk = 25b
# (bool) Автоматически принимать лицензии
android.accept_sdk_license = True
# (str) Архитектура процессора (только 64-бит для скорости)
android.archs = arm64-v8a
# (bool) Пропускать проверку обновлений (ускоряет процесс)
android.skip_update = True
# (str) Использовать стабильную ветку компилятора
p4a.branch = master

[buildozer]
# (int) Уровень логов (2 = debug, чтобы видеть ошибки, если что)
log_level = 2
warn_on_root = 1

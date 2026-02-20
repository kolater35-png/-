[app]
# (str) Название приложения в меню телефона
title = Nebula Quantum AI Pro

# (str) Имя пакета (только маленькие буквы и подчеркивания)
package.name = nebula_quantum_pro

# (str) Домен пакета (обычно в обратном порядке)
package.domain = org.nebula

# (str) Директория с исходным кодом
source.dir = .

# (list) Расширения файлов, которые будут включены в APK
source.include_exts = py,png,jpg,kv,atlas,env

# (str) Версия твоего приложения
version = 2.5.0

# (list) Зависимости. ВАЖНО: Мы зафиксировали версии для стабильности на GitHub.
requirements = python3==3.10.0,kivy==2.3.0,kivymd==1.1.1,requests,urllib3,chardet,idna,openssl

# (str) Ориентация экрана
orientation = portrait

# (list) РАЗРЕШЕНИЯ. Добавлено управление файлами для .env и чтения кода.
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,MANAGE_EXTERNAL_STORAGE

# (int) Target Android API (33 — современный стандарт)
android.api = 33

# (int) Minimum API (совместимость с Android 5.0+)
android.minapi = 21

# (str) Архитектура процессора (arm64-v8a — для большинства новых смартфонов)
android.archs = arm64-v8a

# (bool) Автоматическое принятие лицензий Android SDK
android.accept_sdk_license = True

# (str) Имя главного файла
android.entrypoint = main.py

# (list) Исключаем лишние папки, чтобы уменьшить размер APK
source.exclude_dirs = tests, bin, venv, .github

[buildozer]
# (int) Уровень логирования (2 — самый подробный, поможет найти ошибки)
log_level = 2

# (int) Предупреждение о запуске от имени root
warn_on_root = 1

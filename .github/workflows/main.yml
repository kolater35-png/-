name: Build Nebula Ultra APK
on:
  push:
    branches: [ main ]
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-22.04
    steps:
      - uses: actions/checkout@v4

      - name: Set up JDK 17
        uses: actions/setup-java@v4
        with:
          java-version: '17'
          distribution: 'temurin'

      - name: Clean and Prepare Space
        run: |
          # Убиваем всё, что могло зависнуть
          sudo pkill -9 java || true
          sudo pkill -9 python || true
          # Очистка места
          sudo rm -rf /usr/share/dotnet /opt/ghc "/usr/local/share/boost"
          docker image prune -af
          # Создаем абсолютно чистую рабочую директорию
          mkdir -p /home/runner/work/build_space
          cp -r . /home/runner/work/build_space
          df -h

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.10'

      - name: Install Buildozer
        run: |
          pip install --upgrade pip
          pip install "Cython<3.0.0" wheel virtualenv buildozer

      - name: Build with Buildozer (Isolated Mode)
        working-directory: /home/runner/work/build_space
        run: |
          export PATH=$PATH:~/.local/bin
          # Жесткое ограничение ресурсов, чтобы не вылетало
          export GRADLE_OPTS="-Xmx4g -Dorg.gradle.daemon=false -Dorg.gradle.workers.max=1"
          
          # Запуск сборки
          yes | buildozer -v android debug
        env:
          BUILDOZER_ALLOW_ORG_NAME_START: 1

      - name: Upload APK
        uses: actions/upload-artifact@v4
        with:
          name: Nebula-Final-Build
          path: /home/runner/work/build_space/bin/*.apk

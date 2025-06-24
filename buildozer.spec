# Name des automatisierten Prozesses
name: Build Android APK

# Wann soll dieser Prozess gestartet werden?
on:
  push:
    branches: [ "main" ]
  workflow_dispatch:

# Definiert die Aufgaben ("Jobs"), die ausgeführt werden sollen
jobs:
  build-android:
    # Verwendet die neueste Version von Ubuntu als Basis
    runs-on: ubuntu-latest

    steps:
      # Schritt 1: Kopiert Ihren Code (main.py, buildozer.spec) in die Build-Umgebung
      - name: Checkout
        uses: actions/checkout@v4

      # Schritt 2: Verwendet die offizielle Kivy-Buildozer-Action.
      # Diese lädt einen perfekten Docker-Container, in dem alle Werkzeuge funktionieren.
      - name: Build with Buildozer
        uses: kivy/buildozer-action@v1
        id: buildozer
        with:
          # Der Befehl, der innerhalb des Containers ausgeführt wird
          command: buildozer -v android debug
          # Wir geben explizit den Namen unserer Konfigurationsdatei an
          spec_file: buildozer.spec

      # Schritt 3: Lädt die fertige APK-Datei als "Artefakt" hoch
      - name: Upload Artifact
        uses: actions/upload-artifact@v4
        with:
          name: voicecloningapp-apk
          # Dieser spezielle Pfad greift auf die Ausgabe des vorherigen Schritts zu
          path: ${{ steps.buildozer.outputs.package_path }}

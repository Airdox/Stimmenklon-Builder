[app]

# (str) Titel der Anwendung
title = Stimmenklon-Builder

# (str) Paketname
package.name = stimmenklon_builder

# (str) Paket-Domain (wird für Android-Paketname verwendet)
package.domain = com.stimmenklon.builder

# (str) Quellcode-Verzeichnis (Standard ist das aktuelle Verzeichnis)
source.dir = .

# (list) Quellcode-Dateien zum einschließen (Leer = alle .py-Dateien)
source.include_exts = py,png,jpg,kv,atlas

# (str) Anwendungsversion
version = 1.0.0

# (str) Anwendungsversion (einfache Zahl, wird für die interne Versionierung verwendet)
version.regex = __version__ = ['"]([^'"]*) ['"]
version.filename = %(source.dir)s/main_apk.py

# (list) Anwendungsanforderungen
requirements = python3,kivy>=2.1.0,kivymd,plyer

# (str) Presplash-Hintergrundfarbe (für Android, Hexadezimal ohne '#')
presplash.color = #2E7D32

# (str) Icon der Anwendung
#icon.filename = %(source.dir)s/assets/icon.png

# (str) Unterstützte Ausrichtung (landscape, sensorLandscape, portrait oder all)
orientation = portrait

# (bool) Zeige einen Presplash-Bildschirm an
#presplash.filename = %(source.dir)s/assets/presplash.png

[buildozer]

# (int) Logfile-Ebene (0 = nur Fehler und Warnungen, 1 = info, 2 = debug)
log_level = 2

# (int) Display-Warnung, wenn das Buildozer-Verzeichnis nicht auf dem aktuellen Pfad ist (0 = False, 1 = True)
warn_on_root = 1

[android]

# (str) Android-Eintrag-Punkt, Standard ist ok für Kivy-basierte Apps
android.entrypoint = org.kivy.android.PythonActivity

# (str) Android-App-Thema, Standard ist das Standard-Kivy-Thema
android.apptheme = "@android:style/Theme.NoTitleBar"

# (list) Muster für Android-Whitelist
android.whitelist = 

# (str) Android-API-Level
android.api = 31

# (str) Android-Minimum-API-Level
android.minapi = 21

# (str) Android-SDK-Verzeichnis (wenn leer, wird automatisch heruntergeladen)
android.sdk_path = 

# (str) Android-NDK-Verzeichnis (wenn leer, wird automatisch heruntergeladen)
android.ndk_path = 

# (bool) Android-NDK automatisch akzeptieren (falls nicht im SDK-Manager installiert)
android.accept_sdk_license = True

# (str) Android-Einstiegsklasse, Standard ist ok für Kivy-basierte Apps
android.entrypoint = org.kivy.android.PythonActivity

# (str) Android-Anwendungsklasse, Standard ist ok für Kivy-basierte Apps
android.appclass = org.kivy.android.PythonActivity

# (list) Java-Klassen, die zur Anwendung hinzugefügt werden sollen
android.add_java_dir = 

# (list) Android-Bibliotheken, die der Anwendung hinzugefügt werden sollen
android.add_libs_dir = 

# (list) Android-Gradle-Dependencies
android.gradle_dependencies = 

# (list) Android-Bibliotheken, die kopiert werden sollen
android.add_libs = 

# (str) Android-Logcat-Filter-Spezifikation
android.logcat_filters = *:S python:D

# (bool) Android-Debugmodus (Verlässt die Anwendung im Debugmodus nach dem Bildschirm)
android.debug = 0

# (list) Android-Berechtigungen
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,RECORD_AUDIO,MODIFY_AUDIO_SETTINGS

# (str) Android-Architektur, kann eine der sein: armeabi-v7a, arm64-v8a, x86, x86_64
android.archs = arm64-v8a, armeabi-v7a

# (bool) Ermögliche die Sicherung von Anwendungsdaten auf Android
android.allow_backup = True

# (bool) Zeige Anwendungsicon im Anwendungsmenü an
android.icon_adaptive_foreground_color = #2E7D32
android.icon_adaptive_background_color = #FFFFFF

[buildozer]
# (str) Buildozer-Verzeichnis (Standard ist .buildozer)
buildozer_dir = .buildozer

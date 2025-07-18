# Stimmenklon-Builder

Eine benutzerfreundliche Android-Anwendung für Stimmen-Kloning (Voice Cloning) mit grafischer Oberfläche, entwickelt mit Kivy.

## Übersicht

Stimmenklon-Builder ist eine mobile Anwendung, die es Benutzern ermöglicht:
- **Stimmenmodelle zu trainieren** aus eigenen Audiodateien
- **Text-to-Speech Synthese** mit trainierten Stimmenmodellen durchzuführen
- Eine intuitive Benutzeroberfläche für den gesamten Workflow

## Features

### 🎤 Stimmenmodell-Training
- Auswahl mehrerer Audiodateien für das Training
- Fortschrittsanzeige während des Trainingsprozesses
- Benutzerdefinierte Modellnamen
- Echtzeit-Logging des Trainingsstatus

### 🗣️ Text-to-Speech
- Auswahl aus trainierten Stimmenmodellen
- Freie Texteingabe für die Sprachsynthese
- Audio-Wiedergabe der generierten Sprache
- Statusanzeigen für alle Operationen

## Installation

### Voraussetzungen
- Python 3.7+
- Kivy Framework
- Android SDK (für APK-Building)

### Dependencies installieren
```bash
pip install -r requirements.txt
```

### Desktop-Version ausführen
```bash
python main_apk.py
```

### Android APK erstellen
```bash
buildozer android debug
```

## Verwendung

1. **Stimmenmodell trainieren:**
   - Wechseln Sie zum Tab "Stimmenmodell trainieren"
   - Wählen Sie Audiodateien aus dem Dateisystem
   - Geben Sie einen Namen für das Modell ein
   - Starten Sie den Trainingsprozess

2. **Text-to-Speech:**
   - Wechseln Sie zum Tab "Text-to-Speech"
   - Wählen Sie ein trainiertes Modell aus
   - Geben Sie den gewünschten Text ein
   - Starten Sie die Sprachsynthese
   - Spielen Sie das generierte Audio ab

## Entwicklung

### Projekt-Struktur
```
Stimmenklon-Builder/
├── main_apk.py          # Hauptanwendung
├── buildozer.spec       # Android Build-Konfiguration
├── requirements.txt     # Python Dependencies
├── assets/              # App-Assets (Icons, etc.)
└── .github/workflows/   # CI/CD Pipeline
```

### Build-Pipeline
Das Projekt verwendet GitHub Actions für automatische APK-Generierung:
- Automatischer Build bei Push auf main branch
- Docker-basierte Build-Umgebung mit Kivy/Buildozer
- APK-Artefakte werden als Downloads bereitgestellt

## Technische Details

- **Framework:** Kivy (Cross-Platform GUI)
- **Zielplattform:** Android (mit Desktop-Unterstützung)
- **Build-System:** Buildozer
- **CI/CD:** GitHub Actions
- **Sprache:** Python 3

## Lizenz

Dieses Projekt steht unter der MIT-Lizenz. Siehe die LICENSE-Datei für Details.

## Beitragen

Contributions sind willkommen! Bitte:
1. Forken Sie das Repository
2. Erstellen Sie einen Feature-Branch
3. Committen Sie Ihre Änderungen
4. Erstellen Sie einen Pull Request

## Support

Bei Fragen oder Problemen erstellen Sie bitte ein Issue im GitHub Repository.
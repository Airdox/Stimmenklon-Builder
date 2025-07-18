# Stimmenklon-Builder

**Deutsche Voice-Cloning und Text-to-Speech App mit Zonos TTS**

Eine Android-App für hochwertiges Voice-Cloning und deutsche Sprachsynthese basierend auf der modernen Zonos TTS Engine. Erstellen Sie Ihre eigene digitale Stimme und generieren Sie natürlich klingende deutsche Sprache - völlig offline und kostenlos!

## ✨ Features

- 🎙️ **Echtes Voice-Cloning**: Trainieren Sie ein Modell Ihrer eigenen Stimme mit wenigen Audiodateien
- 🇩🇪 **Deutsche Sprachsynthese**: Hochwertige Text-to-Speech in deutscher Sprache
- 🚀 **Zonos TTS Integration**: Nutzt modernste Open-Weight TTS-Technologie (44kHz Audioqualität)
- 📱 **Android-nativ**: Entwickelt mit Kivy für optimale Android-Performance
- 🔒 **Vollständig offline**: Keine Internetverbindung nach der Installation erforderlich
- 💰 **Kostenlos**: Keine API-Kosten oder Abonnements

## 🚀 Installation

### Voraussetzungen

- Android 5.0 (API Level 21) oder höher
- Mindestens 2 GB freier Speicherplatz
- Mikrofon-Berechtigung für Audio-Aufnahme (optional)

### App Installation

1. **APK herunterladen**:
   - Laden Sie die neueste APK-Datei aus den [GitHub Releases](https://github.com/Airdox/Stimmenklon-Builder/releases) herunter
   - Oder bauen Sie die App selbst (siehe Entwicklung)

2. **Installation auf Android**:
   ```bash
   # Über ADB (entwicklermodus)
   adb install stimmenklon-builder.apk
   
   # Oder: APK-Datei direkt auf dem Gerät öffnen
   ```

3. **Berechtigungen erteilen**:
   - Speicher-Zugriff für Audiodateien
   - Mikrofon-Zugriff (falls Sie eigene Aufnahmen machen möchten)

### Zonos TTS Installation

Die App installiert automatisch die erforderlichen Komponenten beim ersten Start:

1. **Automatische Installation**: Tippen Sie auf "Zonos TTS installieren" in der App
2. **Manuelle Installation** (bei Problemen):
   ```bash
   pip install zonos torch torchaudio transformers soundfile
   ```

## 🎯 Verwendung

### 1. Voice-Cloning Training

**Ihre Stimme klonen in 4 einfachen Schritten:**

1. **Audiodateien vorbereiten**:
   - Mindestens 3-5 Audiodateien Ihrer Stimme (je mehr, desto besser)
   - Empfohlene Gesamtdauer: 30 Sekunden bis 5 Minuten
   - Unterstützte Formate: WAV, MP3, FLAC, OGG, M4A
   - Klare Aufnahmen ohne Hintergrundgeräusche bevorzugt

2. **Dateien auswählen**:
   - Öffnen Sie den Tab "Stimmenmodell trainieren"
   - Navigieren Sie zu Ihren Audiodateien
   - Wählen Sie die gewünschten Dateien aus

3. **Modell trainieren**:
   - Geben Sie einen eindeutigen Modellnamen ein (z.B. "meine_stimme")
   - Tippen Sie auf "Voice-Cloning Training starten"
   - Warten Sie, bis das Training abgeschlossen ist (1-5 Minuten)

4. **Training überwachen**:
   - Verfolgen Sie den Fortschritt im Balken
   - Lesen Sie die Log-Ausgabe für Details

### 2. Deutsche Sprachsynthese

**Text in Ihre geklonte Stimme umwandeln:**

1. **Modell laden**:
   - Wechseln Sie zum Tab "Deutsche Sprachsynthese"
   - Tippen Sie auf "Modell laden"
   - Wählen Sie Ihr trainiertes Modell aus

2. **Text eingeben**:
   - Geben Sie Ihren deutschen Text in das Textfeld ein
   - Der Text kann mehrere Sätze enthalten

3. **Sprache generieren**:
   - Tippen Sie auf "Deutsche Sprache generieren"
   - Warten Sie, bis die Synthese abgeschlossen ist

4. **Audio abspielen**:
   - Tippen Sie auf "Abspielen" um das Ergebnis zu hören
   - Die Audiodatei wird automatisch gespeichert

## 🔧 Technische Details

### Zonos TTS Engine

**Was ist Zonos TTS?**

Zonos ist eine führende Open-Weight Text-to-Speech-Engine mit folgenden Eigenschaften:

- **Multilingual**: Unterstützt Deutsch und viele andere Sprachen
- **High-Quality**: 44kHz native Audioausgabe
- **Voice-Cloning**: Klont Stimmen aus wenigen Sekunden Referenz-Audio
- **Emotional Control**: Steuerung von Sprechtempo, Tonhöhe und Emotionen
- **Offline-fähig**: Läuft vollständig lokal ohne Internet

**Technische Spezifikationen:**

- Basiert auf modernen Transformer-Architekturen
- Trainiert auf 200k+ Stunden multilingualer Sprachdaten
- Unterstützt Speaker-Embeddings für Voice-Cloning
- Optimiert für mobile Geräte

### Systemanforderungen

**Minimum:**
- Android 5.0 (API 21)
- 2 GB RAM
- 1 GB freier Speicher

**Empfohlen:**
- Android 8.0+ (API 26)
- 4 GB RAM
- 3 GB freier Speicher
- GPU-Unterstützung (für schnelleres Training)

### Datei-Locations

```
/storage/emulated/0/
├── .stimmenklon_models/     # Trainierte Stimmenmodelle
├── stimmenklon_output_*.wav # Generierte Audiodateien
└── Download/                # APK und Updates
```

## 🛠️ Entwicklung

### Lokale Entwicklung

1. **Repository klonen**:
   ```bash
   git clone https://github.com/Airdox/Stimmenklon-Builder.git
   cd Stimmenklon-Builder
   ```

2. **Python-Umgebung einrichten**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # oder: venv\Scripts\activate  # Windows
   ```

3. **Dependencies installieren**:
   ```bash
   pip install -r requirements.txt
   ```

4. **App lokal testen**:
   ```bash
   python main_apk.py
   ```

### Android APK bauen

1. **Buildozer installieren**:
   ```bash
   pip install buildozer
   ```

2. **Android SDK/NDK einrichten**:
   ```bash
   buildozer android_new
   ```

3. **APK erstellen**:
   ```bash
   buildozer android debug
   ```

4. **APK testen**:
   ```bash
   buildozer android deploy run
   ```

### GitHub Actions

Die automatische APK-Erstellung läuft über GitHub Actions:

- **Trigger**: Push auf `main` Branch
- **Ausgabe**: APK als GitHub Artifact
- **Konfiguration**: `.github/workflows/build.yml`

## 📋 Troubleshooting

### Häufige Probleme

**"Zonos TTS nicht installiert"**
- Tippen Sie auf "Zonos TTS installieren" in der App
- Stellen Sie sicher, dass Sie eine Internetverbindung haben
- Bei manueller Installation: `pip install zonos`

**Training schlägt fehl**
- Überprüfen Sie die Audioqualität (keine Hintergrundgeräusche)
- Stellen Sie sicher, dass Audiodateien mindestens 1 Sekunde lang sind
- Verwenden Sie unterstützte Formate (WAV, MP3, FLAC)

**Synthese produziert kein Audio**
- Laden Sie ein trainiertes Modell
- Überprüfen Sie, ob genügend Speicherplatz vorhanden ist
- Starten Sie die App neu

**App stürzt ab**
- Überprüfen Sie die Speicher-Berechtigungen
- Stellen Sie sicher, dass genügend RAM verfügbar ist
- Neustart des Geräts kann helfen

### Performance-Optimierung

**Schnelleres Training:**
- Verwenden Sie Geräte mit mehr RAM (4+ GB)
- Schließen Sie andere Apps während des Trainings
- Verwenden Sie SSD-Speicher wenn möglich

**Bessere Audioqualität:**
- Verwenden Sie hochwertige Quell-Audiodateien
- Aufnahmen in ruhiger Umgebung
- Längere Trainingsdaten (2-5 Minuten optimal)

## 🤝 Beitragen

Beiträge sind willkommen! Siehe [CONTRIBUTING.md](CONTRIBUTING.md) für Details.

### Development Roadmap

- [ ] **UI-Verbesserungen**: Moderneres Material Design
- [ ] **Mehr Sprachen**: Englisch, Französisch, Spanisch
- [ ] **Emotionskontrolle**: GUI für Tonhöhe, Geschwindigkeit
- [ ] **Batch-Processing**: Mehrere Texte auf einmal
- [ ] **Cloud-Sync**: Optional für Modell-Backup

## 📄 Lizenz

Dieses Projekt steht unter der [MIT License](LICENSE).

## 🙏 Danksagung

- **Zonos TTS**: Für die exzellente Open-Weight TTS-Engine
- **Kivy**: Für das Python-basierte Mobile-Framework
- **Community**: Für Tests und Feedback

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/Airdox/Stimmenklon-Builder/issues)
- **Discussions**: [GitHub Discussions](https://github.com/Airdox/Stimmenklon-Builder/discussions)
- **Email**: [support@stimmenklon-builder.de](mailto:support@stimmenklon-builder.de)

---

**Erstellt mit ❤️ in Deutschland**

> *Hinweis: Diese App ist für Bildungs- und Forschungszwecke gedacht. Bitte verwenden Sie Voice-Cloning verantwortungsvoll und respektieren Sie die Rechte anderer.*
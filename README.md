# Image Downloader Tool

Ein einfaches Desktop-Tool zum Herunterladen aller Bilder von einer Webseite mit grafischer Benutzeroberfläche.

## Features

- 🌐 Download aller Bilder von beliebigen Webseiten
- 📁 Freie Wahl des Zielordners
- 🔤 Zwei Namensschema-Optionen:
  - Original-Dateinamen beibehalten
  - Nummerierte Namen (z.B. `seitenname-001.jpg`)
- 📊 Fortschrittsanzeige während des Downloads
- 🔄 Automatische Vermeidung von Dateinamens-Duplikaten
- 🖥️ Benutzerfreundliche GUI mit Tkinter

## Voraussetzungen

- Python 3.7 oder höher
- pip (Python Package Manager)

## Installation

1. Repository klonen oder herunterladen:
```bash
git clone https://github.com/deinusername/image-downloader.git
cd image-downloader
```

2. Benötigte Pakete installieren:
```bash
pip install -r requirements.txt
```

## Verwendung

1. Starte die Anwendung:
```bash
python image_downloader.py
```

2. Gib die URL der Webseite ein, von der du Bilder herunterladen möchtest

3. Wähle einen Zielordner auf deinem PC aus

4. Wähle das gewünschte Namensschema:
   - **Original-Namen**: Behält die ursprünglichen Dateinamen bei
   - **SEITENNAME-000**: Benennt Bilder durchnummeriert (z.B. `google_com-001.jpg`)

5. Klicke auf "Bilder herunterladen"

## Screenshots

*Hauptfenster der Anwendung mit allen Eingabefeldern und Optionen*

## Technische Details

Das Tool verwendet:
- **Tkinter** für die grafische Benutzeroberfläche
- **Requests** für HTTP-Anfragen
- **BeautifulSoup4** zum Parsen von HTML und Extrahieren von Bild-URLs
- **Threading** für nicht-blockierende Downloads

## Einschränkungen

- Das Tool lädt nur Bilder herunter, die in `<img>`-Tags eingebunden sind
- Einige Webseiten mit dynamisch geladenen Bildern (JavaScript) werden möglicherweise nicht vollständig unterstützt
- Bilder, die durch CSS als Hintergrund eingebunden sind, werden nicht heruntergeladen

## Lizenz

Dieses Projekt ist unter der MIT-Lizenz lizenziert - siehe [LICENSE](LICENSE) Datei für Details.

## Beitragen

Contributions sind willkommen! Fühle dich frei, Issues zu öffnen oder Pull Requests zu erstellen.

## Haftungsausschluss

Bitte respektiere die Urheberrechte und Nutzungsbedingungen der Webseiten, von denen du Bilder herunterlädst. Dieses Tool ist nur für den persönlichen und legalen Gebrauch bestimmt.

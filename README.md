# Firmenpark.net

Einfache Online-Lösungen für Ihr Business.

## ICS-Generator

Erstellen Sie einfach und schnell ICS-Kalenderdateien für Ihre Termine und Veranstaltungen.

### Features

- **Titel & Beschreibung** - Details zum Termin
- **Ganztägig** - Ganztägige Events ohne Uhrzeit
- **Start/Enddatum** - Flexible Zeitraumangabe
- **Ort** - Veranstaltungsort
- **Organisator** - E-Mail des Organisators
- **Teilnehmer** - Mehrere E-Mail-Adressen einladen
- **Priorität** - Niedrig, Mittel, Hoch
- **Kategorie** - Arbeit, Privat, Hobby, Termin, Besprechung, Urlaub
- **Wiederholung** - Täglich, Wöchentlich, Monatlich, Jährlich
- **Erinnerung** - Automatische Benachrichtigung

### Technologien

- Flask
- Bootstrap 5
- SQLite
- Python

### Installation

```bash
# Repository klonen
git clone https://github.com/pablo-og/Firmenpark.git
cd Firmenpark

# Virtual Environment erstellen
python -m venv venv

# Virtual Environment aktivieren
source venv/bin/activate  # Linux/Mac
# oder
venv\Scripts\activate  # Windows

# Abhängigkeiten installieren
pip install -r requirements.txt

# Konfiguration einrichten
cp .env.example .env
# Editiere .env und setze deine Werte

# Server starten
python run.py
```

### Konfiguration

Kopieren Sie `.env.example` nach `.env` und passen Sie die Werte an:

```bash
cp .env.example .env
```

**WICHTIG: SECRET_KEY**
- Der `SECRET_KEY` dient der Sicherheit Ihrer Anwendung (Session-Schutz, CSRF)
- Verwenden Sie mindestens 32 Zeichen
- Generieren Sie einen sicheren Schlüssel mit:
  ```bash
  python -c "import secrets; print(secrets.token_hex(32))"
  ```
- Teilen Sie den Schlüssel niemals und committen Sie ihn nicht ins Repository

### Zugriff

Öffnen Sie [http://localhost:5004](http://localhost:5004) in Ihrem Browser.

### Entwicklung

```bash
# Änderungen pushen
git add -A
git commit -m "Ihre Änderungen"
git push
```

---

**Autor**: Markus Engel & Z.ai  
**Website**: firmenpark.net

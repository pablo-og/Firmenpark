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
# Virtual Environment erstellen
python -m venv venv

# Virtual Environment aktivieren
source venv/bin/activate  # Linux/Mac
# oder
venv\Scripts\activate  # Windows

# Abhängigkeiten installieren
pip install -r requirements.txt

# Server starten
python run.py
```

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

# RabbitFarm Web Application

Dieses Verzeichnis enthält die Webanwendung des RabbitFarm-Projekts. RabbitFarm ist ein simulierter Gemüsebau-Betrieb, der über diese intuitive Benutzeroberfläche verwaltet werden kann. Die Applikation demonstriert den produktiven Einsatz diverser moderner Python-Konzepte:

- **Objektorientierung (Data Classes):** Zentrale Verwaltung von strukturierten Datenmodellen (Gemüse, Beete, Kunden, Inventar).
- **Generatoren & Lazy Evaluation:** Berechnungen von großen Datensätzen (u.A. simulierte Sensordaten oder wöchentliche Abo-Vorhersagen).
- **Flask Framework:** Backend mit serverseitigem Rendering.
- **Speicherung:** JSON-basierte Persistenz über das lokales Dateiensystem als No-Sql Datenspeicher.

*(Hinweis: Die zugehörigen Jupyter-Notebooks für Auswertungen befinden sich in `g03/static/notebooks/`)*

## Struktur der Webanwendung

Die Weboberfläche selbst (`/src/web/`) teilt sich in folgende Kernelemente auf:

- **`main.py`** – Der Einstiegspunkt der Anwendung sowie die Start-Konfiguration des Flask-Servers.
- **`app.py`** – Die allgemeine Initialisierung der Flask-App sowie das vorbereitende Laden der Init-Datenbank beim Start.
- **`routes.py`** – Definitionen sämtlicher Web-Routen und Controller-Mechanismen für die HTML-Formulare (MVC-Prinzip).
- **`templates/`** – Die HTML/Jinja2-Vorlagen für das dynamische Rendering des Frontends.
- **`static/css/`** – Colour-Theme der Oberfläche.

Die reine Geschäftslogik und Datenstrukturen operieren außerhalb der UI in `/src/` (`data_manager.py`, `models.py`, `services.py`).

## Installation & Starten

1. Stellen Sie sicher, dass alle Systemanforderungen und Pakete aufgesetzt sind:
   ```bash
   pip install -r src/requirements.txt
   ```
2. Um die Web-App zu starten, navigieren Sie in das Rootverzeichnis des Projekts **`g03/`** und führen folgenden Befehl aus:
   ```bash
   python3 -m src.web.main
   ```
3. Die Anwendung ist nun über den Browser erreichbar. Normalerweise unter: **[http://127.0.0.1:8080](http://127.0.0.1:8080)**

## Tests

Die Anwendung samt Modellen, Controller-Routen und Services verfügt über eine pytest Test-Suite im `tests/` Verzeichnis zur Sicherstellung der Systemfunktionalität.

Ausführen der Tests (aus dem Basisordner `g03/`): **Notiz an uns** - Pfad muss noch geändert werden auf Testverzeichnis des Gesamtprojektes:
```bash
pytest tests/ -v
```

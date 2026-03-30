# RabbitFarm – Der Gemüsehof des Hasen

**DLBDSIPWP01 – Einführung in die Programmierung mit Python (Projekt)**

**Gruppe 3:** Cingöz, Ahmet | Niederhuber, Marco | Strauß, Tim-Oliver

---

## Projektbeschreibung

RabbitFarm ist eine Python-basierte Farmverwaltungsanwendung für den fiktiven Gemüsehof des Hasen Rudi. Die App ermöglicht die Verwaltung von Beeten, Gemüsesorten, Lagerbeständen, Kunden, Bestellungen und Finanzen über eine Flask-Web-UI.

**Wissenschaftlicher Fokus:** Lazy Evaluation vs. Eager Evaluation – Speichereffizienz bei der Verarbeitung großer Sensordatenströme mit Python-Generatoren und `itertools`.

---

## Ziel des Projekts

1. Den Gemüsehof RabbitFarm digital abbilden (Beete, Gemüse, Lager, Kunden, Bestellungen, Finanzen)
2. Eine moderne Web-Oberfläche mit Flask bereitstellen
3. Lazy vs. Eager Evaluation anhand simulierter Sensordaten vergleichen (Benchmark mit Zeit- und Speichermessung)

---

## Setup / Installation

### Voraussetzungen

- Python 3.10+
- pip

### Installation

```bash
cd src/student_projects/g03
pip install -r src/requirements.txt
```

---

## Ausführung

### Web-App starten

```bash
cd src/student_projects/g03
python -m src.web.main
```

Browser öffnen: [http://127.0.0.1:8081](http://127.0.0.1:8081)

### Verfügbare Seiten

| Route | Funktion |
|-------|----------|
| `/` | Dashboard mit Schnellzugriff |
| `/beds` | Beete anlegen und verwalten |
| `/vegetables` | Gemüsesorten anlegen und verwalten |
| `/inventory` | Lagerbestand verwalten, Ernte einlagern |
| `/customers` | Kunden verwalten |
| `/orders` | Bestellungen aufgeben und einsehen |
| `/finances` | Finanzübersicht (Einnahmen) |
| `/sensors` | Lazy vs. Eager Benchmark ausführen |

---

## Test-Ausführung

### Alle Tests

```bash
cd src/student_projects/g03
python -m pytest tests/ -v
```

### Nur Unit-Tests

```bash
python -m pytest tests/test_models.py tests/test_services.py tests/test_sensors.py tests/test_sensor_benchmark.py -v
```

### Nur Integrationstests

```bash
python -m pytest tests/test_integration.py -v
```

### Test-Übersicht

| Datei | Bereich | Anzahl Tests |
|-------|---------|-------------|
| `test_models.py` | Domänenmodelle (Vegetable, Bed, Customer, Inventory) | 14 |
| `test_services.py` | Business-Logik (Abo-Kisten, Gewinnberechnung) | 9 |
| `test_sensors.py` | Sensordaten-Generator | 7 |
| `test_sensor_benchmark.py` | Eager/Lazy Processing und Benchmarks | 10 |
| `test_integration.py` | Übergreifende Workflows (INT-01 bis INT-05) | 7 |
| **Gesamt** | | **47** |

Die Integrationstests sind explizit den Software-Requirements (REQ-01 bis REQ-15) zugeordnet – siehe `docs/finalReport.md`, Abschnitt 6.3.

---

## Projektstruktur

```
g03/
├── README.md                    # Diese Datei
├── data/
│   └── rabbitfarm_data.json     # Persistierte App-Daten (JSON)
├── docs/
│   ├── finalReport.md           # Projektabschlussbericht
│   ├── finalReport_structure.md # Report-Vorlage (Professor)
│   ├── konzeptionsplan.md       # Konzeptionsphase
│   ├── ARCHITEKTUR_TECHSTACK.md # Architektur und Tech-Stack
│   ├── THEORETISCHERHINTERGRUND.md # Wissenschaftlicher Hintergrund
│   └── ...                      # Weitere Dokumentation
├── src/
│   ├── __init__.py
│   ├── models.py                # Dataclasses: Vegetable, Bed, Customer, Inventory, Order
│   ├── data_manager.py          # JSON-Persistenz (load/save)
│   ├── services.py              # Business-Logik (Abo-Kisten, Gewinnberechnung)
│   ├── sensors.py               # Sensordaten-Generator (Bodenfeuchtigkeit)
│   ├── sensor_benchmark.py      # Lazy vs. Eager Benchmark
│   ├── requirements.txt         # Python-Abhängigkeiten
│   └── web/
│       ├── __init__.py
│       ├── main.py              # Einstiegspunkt (Flask-Server)
│       ├── app.py               # Flask-App-Konfiguration
│       ├── routes.py            # Routen-Definitionen
│       ├── templates/           # Jinja2-HTML-Templates
│       └── static/css/          # Stylesheets
├── static/
│   └── notebooks/
│       ├── generators.ipynb         # Generator-Demonstrationen
│       └── layz_vs_eager.ipynb      # Wissenschaftliche Auswertung
└── tests/
    ├── conftest.py              # Pytest-Konfiguration (sys.path)
    ├── test_models.py           # Unit-Tests: Domänenmodelle
    ├── test_services.py         # Unit-Tests: Business-Logik
    ├── test_sensors.py          # Unit-Tests: Sensordaten
    ├── test_sensor_benchmark.py # Unit-Tests: Benchmark
    └── test_integration.py      # Integrationstests (INT-01 bis INT-05)
```

---

## Technische Entscheidungen

| Entscheidung | Begründung |
|---|---|
| **Flask** statt Streamlit/tkinter | Klassische Web-App; browserbasiert, geräteunabhängig, klare Trennung von Kern und UI |
| **JSON-Persistenz** statt Datenbank | Einfach, portabel, keine externe Abhängigkeit; ausreichend für Projektumfang |
| **Generatoren + itertools** für Lazy Evaluation | Kernthema des wissenschaftlichen Teils; `yield`, `filter`, `map`, `islice`, `cycle` |
| **tracemalloc** für Speichermessung | Standardbibliothek; liefert Peak-Memory ohne externe Tools |
| **pytest** für Tests | Standard-Testframework; einfach, erweiterbar, CI-kompatibel |
| **Modularer Kern** ohne Flask-Abhängigkeit | Kern (`models`, `services`, `sensors`, `sensor_benchmark`) importiert kein Flask; erweiterbar für andere Oberflächen |

---

## Bekannte Einschränkungen

- **Keine Authentifizierung:** Die Web-App hat kein Login-System.
- **Kein Seed für Sensordaten:** Die Sensordaten sind zufällig generiert; Benchmark-Ergebnisse variieren leicht zwischen Durchläufen.
- **Kein Concurrent Access:** Die JSON-Persistenz ist nicht für parallelen Zugriff ausgelegt.
- **Kein Deployment:** Die App läuft lokal mit dem Flask-Entwicklungsserver.

---

## Abhängigkeiten

Siehe `src/requirements.txt`:

```
matplotlib>=3.5.0
numpy>=1.21.0
pandas>=1.3.0
memory-profiler>=0.60.0
jupyter>=1.0.0
ipykernel>=6.0.0
ipywidgets>=7.6.0
flask>=2.0.0
pytest>=7.0.0
```

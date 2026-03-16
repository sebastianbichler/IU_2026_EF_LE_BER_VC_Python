# 6. Implementierung und Qualitätssicherung

Dieses Dokument beschreibt die Implementierung der RabbitFarm-Anwendung (insbesondere der Web-UI) sowie Maßnahmen zur Qualitätssicherung und ist dem Abschlussbericht-Kapitel **6** zugeordnet.

---

## 6.1 Code-Struktur und Dokumentation

### 6.1.1 Projektstruktur (g03)

Die Anwendung ist modular aufgebaut: Ein gemeinsamer **Kern** in `src/` wird von mehreren Oberflächen genutzt (Web-UI, ggf. Terminal-App). Jupyter-Notebooks und statische Lerninhalte liegen außerhalb des App-Codes.

```
g03/
├── src/                        # Kern: Modelle, Daten, Dienste, Sensoren
│   ├── models.py               # Domänenmodelle (Vegetable, Bed, Customer, Order, Inventory, …)
│   ├── data_manager.py         # Persistenz (JSON), load_data(), save_data()
│   ├── services.py             # Geschäftslogik (z. B. calculate_profit, Abo-Logik)
│   ├── sensors.py              # Sensordaten-Generator (stream_soil_moisture)
│   ├── sensor_benchmark.py     # Lazy vs. Eager Benchmark (process_eager, process_lazy, benchmark_*)
│   ├── requirements.txt       # Abhängigkeiten (Flask, Pandas, Jupyter, …)
│   └── web/                    # Web-UI (nur App; keine Jupyter-Notebooks hier)
│       ├── main.py             # Einstiegspunkt: python -m src.web.main
│       ├── app.py              # Flask-App, Blueprint-Registrierung, Daten laden
│       ├── routes.py           # Alle Web-Routen (Dashboard, Gemüse, Beete, Lager, Kunden, Bestellungen, Finanzen, Sensordaten)
│       ├── templates/          # Jinja2-HTML (layout, index, vegetables, beds, …)
│       ├── static/css/         # App-Styles (app.css), Bootstrap über CDN
│       └── README.md           # Startanleitung Web-App
├── data/                       # Persistente Daten (z. B. rabbitfarm_data.json)
├── static/notebooks/           # Jupyter-Notebooks (Lazy/Eager, Generatoren) – getrennt von Web-Code
├── tests/                      # Tests (z. B. rabbitfarm_ui.ipynb für UI-Tests)
└── docs/                       # Konzeption, Berichte, Glossar
```

### 6.1.2 Trennung von Kern und Oberfläche

- **Kern (`src/` ohne `web/`):** Enthält keine UI-Logik. `data_manager`, `models`, `services`, `sensors` und `sensor_benchmark` sind von Flask unabhängig und wiederverwendbar (z. B. für CLI oder andere Frontends).
- **Web-UI (`src/web/`):** Enthält nur webrelevante Teile: Flask-App, Routen, Templates, statische Dateien. Sie importiert den Kern und ruft `data_manager.load_data()` beim Start auf.

Damit bleibt die Geschäftslogik **unabhängig von der Oberfläche** (Offen für Erweiterung, geschlossen für Änderung am Kern).

### 6.1.3 Dokumentation im Code

- **Docstrings:** Module und zentrale Funktionen (z. B. `stream_soil_moisture`, `process_eager`, `process_lazy`, `benchmark_eager`, `benchmark_lazy`) sind mit Kurzbeschreibungen und ggf. Parametern dokumentiert.
- **Kommentare:** Pfad-Setup in `main.py` und `app.py` ist kurz kommentiert (Suchpfad für `data_manager`/`models`).
- **README:** `src/web/README.md` beschreibt Struktur und Start der Web-App (`python -m src.web.main`).

### 6.1.4 Sprachliche Konventionen

- **Code und Bezeichner:** Englisch (Modul-, Funktions-, Variablennamen).
- **Nutzer sichtbar:** Deutsch (Web-UI-Texte, Labels, Meldungen).

---

## 6.2 Test-Konzept: Unit-Tests

Unit-Tests sichern die **Kernfunktionalität** der Domänenmodelle und der Sensordaten-/Benchmark-Logik ab, unabhängig von der Web-UI.

### 6.2.1 Domänenmodelle (`models.py`)

Beispielhafte Tests für zentrale Methoden:

| Testfall | Beschreibung | Erwartung |
|----------|---------------|-----------|
| `Vegetable.is_fresh()` | Ernte vor X Tagen, `shelf_life_days = 5` | `True` wenn Tage &lt; 5, sonst `False` |
| `Vegetable.freshness_ratio()` | Ernte vor 2 Tagen, Haltbarkeit 10 Tage | Verhältnis 0.8 (2/10 abgezogen) |
| `Inventory.add_harvest()` | Einfügen eines Gemüses mit Menge 3.0 | Liste enthält ein neues `Vegetable` mit `amount=3.0` |
| `Inventory.get_fresh_items()` | Mix aus frischen/abgelaufenen Items | Generator liefert nur Objekte mit `is_fresh() == True` |
| `Inventory.get_total_amount()` | Drei Items mit 1.0, 2.0, 0.5 | Summe 3.5 |

*Hinweis:* Konkrete Testdateien (z. B. `tests/test_models.py`) können mit `pytest` oder `unittest` angelegt und in der CI ausgeführt werden.

### 6.2.2 Sensordaten und Lazy/Eager (`sensors.py`, `sensor_benchmark.py`)

| Testfall | Beschreibung | Erwartung |
|----------|---------------|-----------|
| `stream_soil_moisture` | Erste N Werte mit `islice` | N Dictionaries mit `bed_id`, `moisture` (0–100), `timestamp` |
| `process_eager` | Liste mit einem Wert &lt; 35 (Schwellwert) | Ergebnisliste mit einem Eintrag inkl. `irrigation_need` |
| `process_lazy` | Generator mit gleichen Daten wie oben | Gleiche Anzahl gefilterter Einträge wie `process_eager` |
| `benchmark_eager` / `benchmark_lazy` | Kleines N (z. B. 100) | Rückgabe-Dict mit `time`, `peak_memory_mb`, `data_size_mb`, `result_count`; Lazy typisch geringerer Speicher |

Diese Tests stellen sicher, dass die wissenschaftliche Fragestellung (Lazy vs. Eager) auf korrekter Logik basiert.

---

## 6.3 Integrationstests und Traceability

Integrationstests prüfen das **Zusammenspiel** von Routen, Datenzugriff und Modellen in der Web-UI. Sie werden den **funktionalen Anforderungen** aus dem Konzeptionsplan (Kap. 2) zugeordnet.

### INT-01: Web-App startet und liefert Dashboard (REQ: F01–F06, Oberfläche)

- **Ablauf:** Client fordert `GET /` an.
- **Erwartung:** HTTP 200, Antwort enthält Überschrift/Dashboard und Links zu Gemüse, Beeten, Lager, Kunden, Bestellungen, Finanzen, Sensordaten.
- **Traceability:** Sicherstellung, dass die Oberfläche für Farmverwaltung, Lager und Bestände erreichbar ist.

### INT-02: Beete anlegen und in Gemüse-Formular nutzbar (REQ: F01, F02, F03)

- **Ablauf:**  
  1. `POST /beds` mit Name und Größe → neues Beet wird gespeichert.  
  2. `GET /vegetables` → Formular „Neues Gemüse anpflanzen“ enthält das neue Beet in der Beet-Dropdown-Liste.
- **Erwartung:** Beet erscheint in der Liste; Gemüse kann diesem Beet zugeordnet werden.
- **Traceability:** F01 (Beet-Verwaltung), F02 (Gemüsesorten), F03 (Pflanzplanung).

### INT-03: Ernte ins Lager und Frische-Anzeige (REQ: F04, F05, F06)

- **Ablauf:**  
  1. Mindestens ein Gemüse und ein Beet existieren.  
  2. `POST /inventory` mit Gemüse-Index und Menge → Einlagerung.  
  3. `GET /inventory` → Seite zeigt „Frische Ware“ und „Gesamtmenge im Lager“.
- **Erwartung:** Gesamtmenge aktualisiert; frische Ware erscheint in „Frische Ware“ (mit Frische-Prozent), abgelaufene ggf. unter „Abgelaufene Ware“.
- **Traceability:** F04 (Bestandsüberwachung), F05 (Haltbarkeit), F06 (Bestandsabfrage).

### INT-04: Sensordaten-Benchmark (Lazy vs. Eager) (REQ: F13, F14, F15)

- **Ablauf:**  
  1. `GET /sensors` → Formular mit Beet und „Anzahl Messwerte“.  
  2. `POST /sensors` mit z. B. `bed_id=1`, `num_readings=10000` → Server führt `benchmark_eager` und `benchmark_lazy` aus.  
  3. Antwort enthält zwei Ergebnisblöcke (Eager / Lazy) mit Laufzeit, RAM-Peak, Datengröße, Anzahl gefilterter Einträge sowie Vergleich (z. B. „Lazy spart X MB RAM“).
- **Erwartung:** Beide Benchmarks liefern gültige Metriken; Lazy zeigt typisch geringeren Speicherverbrauch.
- **Traceability:** F13 (Sensordaten-Stream), F14 (Generator-basierte Verarbeitung), F15 (Performance-Benchmark).

### INT-05: Bestellung und Finanzen (REQ: F07–F12)

- **Ablauf:**  
  1. Mindestens ein Kunde und Gemüse vorhanden.  
  2. `POST /orders` mit Kunde, Gemüse, Lieferzeit, Preis → Bestellung wird gespeichert.  
  3. `GET /finances` → Gesamteinnahmen und Tabelle der Bestellungen.
- **Erwartung:** Neue Bestellung erscheint in der Bestellhistorie und in der Finanzübersicht; Gesamteinnahmen erhöht.
- **Traceability:** F07–F09 (Kunden, Abos, Bestellungen), F10–F12 (Finanzen).

*Hinweis:* Die konkrete Umsetzung kann manuell (Checkliste) oder automatisiert (z. B. mit `pytest` + `Flask test client`) erfolgen. Das Notebook `tests/rabbitfarm_ui.ipynb` kann für manuelle UI-Checks genutzt werden.

---

## 6.4 CI-Pipeline

Eine mögliche **Continuous-Integration-Pipeline** für das Projekt könnte folgende Schritte umfassen:

### 6.4.1 Umgebung und Abhängigkeiten

1. **Python-Version:** Einheitliche Version (z. B. 3.10 oder 3.11) in der CI definieren.
2. **Installation:**  
   `pip install -r src/requirements.txt`  
   Optional: Nutzung einer virtuellen Umgebung oder `uv`/`poetry` bei Migration auf `pyproject.toml`.

### 6.4.2 Prüfungen

| Schritt | Beschreibung |
|---------|---------------|
| **Lint** | Statische Analyse (z. B. `ruff` oder `pylint`) für `src/` (ohne zwingend `old_code`/Notebooks). |
| **Unit-Tests** | `pytest tests/` (sofern `tests/test_*.py` vorhanden); Abdeckung von `models`, `sensor_benchmark`, ggf. `data_manager`. |
| **Import-Check** | Sicherstellen, dass `python -m src.web.main` (oder ein Dry-Run) ohne Importfehler durchläuft. |
| **Requirements** | Prüfen, dass `requirements.txt` konsistent ist und keine Sicherheitslücken bekannter Pakete (z. B. `pip audit`). |

### 6.4.3 Beispiel GitHub Actions (Skizze)

```yaml
# .github/workflows/ci.yml (Beispiel)
name: CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - run: pip install -r src/requirements.txt
      - run: pip install pytest ruff
      - run: ruff check src/
      - run: pytest tests/ -v
      - run: python -m src.web.main &
        # Optional: Kurzer Smoke-Test, dann Prozess beenden
```

### 6.4.4 Erweiterungen

- **pyproject.toml:** Bei Einführung können Abhängigkeiten, Linter- und Test-Konfiguration zentral in `pyproject.toml` (inkl. `[tool.ruff]`, `[tool.pytest.ini_options]`) gepflegt werden.
- **Integrationstests:** Aufnahme der in Abschnitt 6.3 beschriebenen Szenarien als automatisierte Tests mit dem Flask-Test-Client.

---

## Kurzfassung

- **Struktur:** Klare Trennung Kern (`src/`) vs. Web-UI (`src/web/`); Jupyter-Notebooks in `static/notebooks/`.
- **Dokumentation:** Docstrings und README für die Web-App; Code auf Englisch, UI auf Deutsch.
- **Unit-Tests:** Konzept für Modelle und Sensordaten/Benchmark beschrieben; Umsetzung mit pytest möglich.
- **Integrationstests:** Fünf Szenarien mit Zuordnung zu den funktionalen Anforderungen (F01–F15).
- **CI:** Vorschlag für Lint, Tests, Requirements-Prüfung und optional GitHub Actions.

Dieses Dokument kann direkt als Kapitel **6** in den Projektabschlussbericht übernommen oder bei Bedarf um konkrete Testcode-Beispiele und CI-Configs ergänzt werden.

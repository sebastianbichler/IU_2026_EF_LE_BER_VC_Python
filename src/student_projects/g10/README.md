# FoxPost — Der Paketlieferdienst des Fuchses

FoxPost ist eine Python-basierte Data-Engineering-Anwendung zur Verarbeitung und Analyse von Paketdaten.
Die Anwendung demonstriert eine einfache ETL-Pipeline (Extract, Transform, Load) unter Verwendung von Dask zur effizienten Verarbeitung größerer Datenmengen.

---

## Projektziel

Ziel des Projekts ist die Entwicklung einer modularen Datenpipeline, die Paketdaten einliest, verarbeitet, anreichert und als optimiertes Datenformat speichert.
Dabei werden typische Schritte einer Data-Engineering-Anwendung umgesetzt.

---

## Installation

### 1. Virtuelle Umgebung erstellen

```bash
python -m venv .venv
```

### 2. Umgebung aktivieren (Windows)

```bash
.\.venv\Scripts\Activate
```

### 3. Abhängigkeiten installieren

```bash
pip install -r requirements.txt
pip install -e .
```

---

## Anwendung ausführen

Die Pipeline kann über die Kommandozeile gestartet werden:

```bash
python -m foxpost.run --input data/sample_parcels.csv --output output/processed --mode local
```

### Parameter

* `--input` : Pfad zur Eingabedatei (CSV)
* `--output` : Zielordner für die verarbeiteten Daten
* `--mode` : Ausführungsmodus (`local` oder `dask`)

Optional kann ein externer Dask-Cluster verwendet werden.

---

## Eingabedaten

Die Anwendung erwartet eine CSV-Datei mit Paketdaten.
Beispieldaten befinden sich im Ordner:

```
data/sample_parcels.csv
```

---

## Ausgabedaten

Die verarbeiteten Daten werden im angegebenen Output-Ordner gespeichert, typischerweise als:

* Parquet-Dateien (optimiertes Spaltenformat)
* ggf. weitere Analyseergebnisse

Beispiel:

```
output/processed/
```

---

## Implementierte Features

* Einlesen von Paketdaten aus CSV-Dateien
* Datenvalidierung und -bereinigung
* Datenanreicherung (z. B. Berechnung zusätzlicher Felder)
* Speicherung der Ergebnisse im Parquet-Format
* Ausführung im lokalen Modus oder über Dask

---

## Teilweise implementierte Features

* Erweiterte Datenanalysen
* Optimierte Verarbeitung für sehr große Datenmengen

---

## Nicht umgesetzte Features

* Grafische Benutzeroberfläche
* Erweiterte Visualisierungen der Ergebnisse

---

## Projektstruktur

```
src/
  foxpost/
    run.py
    etl.py
    cli.py
tests/
data/
output/
docs/
```

---

## Tests

Tests können mit folgendem Befehl ausgeführt werden:

```bash
pytest
```

Die Tests überprüfen zentrale Funktionen der Pipeline sowie die korrekte Verarbeitung der Daten.

---

## How to Use

1. Projekt installieren und Umgebung einrichten
2. Beispiel-Datensatz oder eigene CSV-Datei bereitstellen
3. Pipeline über die Kommandozeile starten
4. Ergebnisse im Output-Ordner prüfen

---

## Technologien

* Python
* Dask
* Pandas
* Parquet

---

## Fazit

FoxPost demonstriert die grundlegenden Konzepte moderner Datenverarbeitung, insbesondere den Aufbau einer skalierbaren ETL-Pipeline mit Python und Dask.

# FoxPost – Nutzung und Funktionsweise

FoxPost ist eine Data-Engineering Demo-Anwendung zur Verarbeitung von Paketdaten.
Die Anwendung verwendet Dask, um Daten parallel zu verarbeiten und eine einfache
ETL-Pipeline für Logistikdaten zu demonstrieren.

# 1. Zweck der Anwendung

FoxPost simuliert einen Paketdienst und verarbeitet Versanddaten.

Die Pipeline führt folgende Schritte aus:

1. Einlesen von Paketdaten aus CSV
2. Transformation und Datenbereinigung
3. Berechnung zusätzlicher Felder
4. Aggregation von Statistiken
5. Speicherung der Daten als Parquet

Das Projekt demonstriert typische Data-Engineering Aufgaben:

- Dateningestion
- Datenbereinigung
- Feature Engineering
- Aggregationen
- Partitionierte Speicherung

# 2. Wichtige Dateien

run.py  
Startpunkt der Anwendung. Initialisiert den Dask-Cluster und startet die Pipeline.

etl.py  
Implementiert die eigentliche Datenpipeline.

cli.py  
Definiert die Kommandozeilenargumente.

schema.py  
Datendefinition für Paketdatensätze.

utils.py  
Hilfsfunktionen.

# 3. Installation

Virtuelle Umgebung erstellen:

python -m venv .venv
source .venv/bin/activate

Abhängigkeiten installieren:

pip install -r requirements.txt

Projekt installieren:

pip install -e .

# 4. Anwendung starten

Minimaler Start:

python -m foxpost.run --input data/sample_parcels.csv --output output/processed

Die Anwendung startet automatisch einen lokalen Dask-Cluster und führt
die Datenpipeline aus.

# 5. Pipeline-Schritte

## 5.1 Daten einlesen

CSV-Dateien werden mit Dask DataFrame geladen.

Erwartete Spalten:

- parcel_id
- origin
- destination
- weight_kg
- shipped_at
- delivered_at
- status

## 5.2 Transformation

Folgende Transformationen werden durchgeführt:

- Status wird normalisiert (lowercase)
- negative Gewichte werden entfernt
- Lieferzeit wird berechnet

Neue Spalte:

transit_hours  
Lieferdauer in Stunden.

## 5.3 Routenberechnung

Für jede Lieferung wird eine Route erzeugt:

route_id = ORIGIN-DESTINATION

Beispiel:

BERLIN-MUENCHEN

## 5.4 Statistiken

FoxPost berechnet pro Route:

- Anzahl Pakete
- Durchschnittsgewicht
- Durchschnittliche Lieferzeit

## 5.5 Speicherung

Die Daten werden als Parquet-Dateien gespeichert.

Die Ausgabe ist nach Status partitioniert:

output/processed/

status=delivered/
status=in_transit/
status=pending/

Zusätzlich wird eine Statistikdatei erstellt:

processed_stats.parquet

# 6. Kommandozeilenargumente

## input

Pfad zur Eingabedatei.

Beispiel:

--input data/sample_parcels.csv

## output

Zielordner für Parquet-Daten.

--output output/processed

## mode

Bestimmt die Ausführungsumgebung.

local  
Startet einen lokalen Dask-Cluster.

cluster  
Verbindet sich mit einem externen Scheduler.

## scheduler-address

Adresse eines externen Dask-Schedulers.

Beispiel:

--scheduler-address tcp://localhost:8786

## n-workers

Anzahl Worker im lokalen Cluster.
--n-workers 4

## threads-per-worker

Threads pro Worker.

--threads-per-worker 2

# 7. Monitoring

Beim Start eines lokalen Clusters zeigt FoxPost eine Dashboard-Adresse an.

Beispiel:

http://127.0.0.1:8787

Dort können Tasks, CPU-Auslastung und Datenpartitionen beobachtet werden.

# 8. Tests

Tests können mit pytest ausgeführt werden.

pytest

# 9. Erweiterungsmöglichkeiten

FoxPost kann erweitert werden durch:

- größere Datensätze
- Geo-Routing
- Lieferzeit-Vorhersagen
- Data-Lake Struktur (Bronze / Silver / Gold)
- Streaming Daten


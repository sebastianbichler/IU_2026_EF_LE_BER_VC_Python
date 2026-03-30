# Implementierung

## 1. Architektur

Das RabbitFarm-System ist eine Applikation mit Python geschrieben. Sie ist so aufgebaut, sodass es eine klare Trennung zwischen Domänenmodellen und Geschäftslogik aufweist. Der Aufbau folgt einem schichtenbasierten Ansatz.

- **Modellschicht** (`models.py`): Domänenklassen für die Geschäftsobjekte
- **Service-Schicht** (`services.py`): Geschäftslogik und Berechnungen
- **Sensor-Schicht** (`sensors.py`): Datenstrom-Generatoren für Sensordaten
- **Anwendungsschicht** (`main.py`): CLI-Interface, Datenpersistenz und Benchmark-Funktionen

Die Anwendung verwendet funktionale Programmierungsparadigmen, insbesondere Generatoren und Iterator-Pipelines, um die wissenschaftliche Fragestellung zur Lazy Evaluation zu untersuchen.

## 2. Komponenten und Module

### 2.1 Modellschicht (`models.py`)

Hierbei definiert die Modelschicht die zentralen Datentypen des Systems.

**Vegetable (Gemüse)**
- Gemüsesort
    - Name
    - Sorte
    - Planzdatum
    - Erntdatum
- Methode:
    - `is_fresh()` prüft, ob das Gemüse frisch ist bzw. die Haltbarkeit
    - `freshness_ratio()` berechnet den Frischgrad 

**Bed (Beet)**
- Anbaufläsche
    - Id
    - Name
    - Größe

**Customer (Kunde)**
- Kunde
    - Name
    - Tierart
    - Abo-Typ

**Inventory (Lagerbestand)**
- Verwaltet Gemüse im Lager
- Verwendet Generatoren für `get_fresh_items()` und `get_expired_items()` zur Lazy Evaluation
- Berechnet Gesamtmengen mit funktionalen Ansätzen (`sum()`)

**Order und SubscriptionBox**
- Repräsentieren Bestellungen und Abo-Kisten mit Kunde
    - Gemüse 
    - Lieferdatum
    - Preis

### 2.2 Service-Schicht (`services.py`)

Die Service-Schicht enthält die Geschäftslogik.

**generate_subscription_boxes()**
- Funktion, die für mehrere Wochen Abo-Kisten für Kunden erzeugt.
- Verwendet `itertools.cycle()` für zyklische Gemüseauswahl
- Berechnet Preise dynamisch basierend auf der Anzahl der Gemüsesorten
- Implementiert Lazy Evaluation: Kisten werden on-demand generiert (= nicht alle auf einmal)

**calculate_profit()**
- Funktionaler Ansatz mit `map()` und `sum()` zur berechnung des Gewinnes
- Verwendet Lambda-Funktionen für die Transformation der Bestellungen
- Berechnet Einnahmen, Ausgaben, Gewinn und Gewinnmarge

### 2.3 Sensor-Schicht (`sensors.py`)

**stream_soil_moisture()**
- Generator-Funktion, die einen unendlichen Datenstrom von Bodenfeuchtigkeitsmessungen simuliert
- Kernkomponente für die wissenschaftliche Untersuchung der Lazy Evaluation
- Generiert kontinuierlich Sensordaten mit zufälligen Variationen um einen Basiswert
- Jeder Wert enthält Bed-ID, Feuchtigkeitswert (0-100%) und Zeitstempel

### 2.4 Anwendungsschicht (`main.py`)

Die Hauptanwendung kombiniert alle Komponenten:

**Datenpersistenz**
- JSON-basierte Speicherung in `rabbitfarm_data.json`
- Funktionen `save_data()` und `load_data()` für Serialisierung/Deserialisierung
- Verwendet List-Comprehensions für die Transformation der Datenstrukturen

**CLI-Interface**
- Menübasierte Benutzeroberfläche für die Verwaltung von Gemüse, Beeten, Lager, Kunden und Finanzen
- Funktionale Programmierung mit `map()`, `filter()` und `reduce()` für Datenverarbeitung

**Benchmark-Funktionen**
- `process_eager()`: Eager Evaluation mit Listen-Comprehensions
- `process_lazy()`: Lazy Evaluation mit Generator-Expressions und `filter()`/`map()`
- `benchmark_eager()` und `benchmark_lazy()`: Performance-Messungen mit `tracemalloc` und `time.perf_counter()`

## 3. Relevante Funktionen

### 3.1 Eager Evaluation (`process_eager()`)

```python
def process_eager(data_list, threshold_low=35.0):
    filtered = [
        d for d in data_list if d["moisture"] < threshold_low or d["moisture"] > 80.0
    ]
    irrigation = [
        {
            "bed_id": d["bed_id"],
            "moisture": d["moisture"],
            "irrigation_need": max(0, min(100, 100 - d["moisture"])),
        }
        for d in filtered
    ]
    return irrigation
```

**Charakteristika:**
- Materialisiert alle Daten sofort in Listen
- Zwei separate List-Comprehensions für Filterung und Transformation
- Alle Zwischenergebnisse werden im Speicher gehalten
- Speicherverbrauch wächst linear mit der Datenmenge

### 3.2 Lazy Evaluation (`process_lazy()`)

```python
def process_lazy(data_gen, threshold_low=35.0, max_items=None):
    filtered = filter(
        lambda d: d["moisture"] < threshold_low or d["moisture"] > 80.0, data_gen
    )
    irrigation = map(
        lambda d: {
            "bed_id": d["bed_id"],
            "moisture": d["moisture"],
            "irrigation_need": max(0, min(100, 100 - d["moisture"])),
        },
        filtered,
    )
    if max_items:
        irrigation = islice(irrigation, max_items)
    return list(irrigation)
```

**Charakteristika:**
- Verwendet Generator-Pipelines mit `filter()` und `map()`
- Daten werden on-demand verarbeitet, nicht vorab materialisiert
- Optionales `max_items`-Limit mit `itertools.islice()`
- Speicherverbrauch bleibt konstant, unabhängig von der Datenmenge
- Materialisierung nur am Ende durch `list()`

### 3.3 Benchmark-Funktionen

Beide Benchmark-Funktionen folgen einer identischen Struktur:

1. **Initialisierung**: Start von `tracemalloc` für Speichermessung und `time.perf_counter()` für Zeitmessung
2. **Datenverarbeitung**: Aufruf der jeweiligen Verarbeitungsfunktion (eager oder lazy)
3. **Messung**: Erfassung von Laufzeit und Peak-Memory-Verbrauch
4. **Rückgabe**: Strukturiertes Dictionary mit allen Messwerten

**Messgrößen:**
- `time`: Laufzeit in Sekunden
- `peak_memory_mb`: Maximaler Speicherverbrauch in Megabyte
- `data_size_mb`: Größe der Datenstrukturen (Listen vs. Generatoren)
- `result_count`: Anzahl der gefilterten Ergebnisse

## 4. Besonderheiten: Lazy Evaluation vs. Eager Evaluation

### 4.1 Funktionales Programmieren

Die Implementierung nutzt konsequent funktionale Programmierungsparadigmen:

- **Higher-Order Functions**: `map()`, `filter()`, `reduce()` werden extensiv verwendet
- **Lambda-Funktionen**: Anonyme Funktionen für Transformationen und Filterungen
- **Generator-Expressions**: Lazy Evaluation durch `()` statt `[]`
- **Iterator-Pipelines**: Verkettung von `filter()` und `map()` ohne Zwischenspeicherung

### 4.2 Generator-basierte Datenströme

**Sensordaten-Generator:**
- `stream_soil_moisture()` liefert einen unendlichen Datenstrom
- Ermöglicht Verarbeitung von Datenmengen, die nicht vollständig im Speicher gehalten werden können
- Jeder Aufruf von `next()` generiert einen neuen Messwert

**Abo-Kisten-Generator:**
- `generate_subscription_boxes()` erzeugt Kisten on-demand
- Verwendet `itertools.cycle()` für zyklische Wiederholung
- Ermöglicht Verarbeitung von langen Zeitreihen ohne vollständige Materialisierung

**Lagerbestand-Generatoren:**
- `Inventory.get_fresh_items()` und `get_expired_items()` verwenden `yield`
- Ermöglichen effiziente Iteration über große Lagerbestände ohne vollständige Listen-Erstellung

### 4.3 Vergleich der Ansätze

**Eager Evaluation:**
- Vorteile: Einfacheres Debugging, direkter Zugriff auf alle Daten
- Nachteile: Hoher Speicherverbrauch, nicht skalierbar für große Datenmengen

**Lazy Evaluation:**
- Vorteile: Konstanter Speicherverbrauch, skalierbar für unendliche Datenströme
- Nachteile: Komplexeres Debugging, Overhead bei kleinen Datenmengen

### 4.4 Datenpersistenz

Die JSON-basierte Persistenz verwendet funktionale Ansätze:
- List-Comprehensions für die Transformation von Objekten zu Dictionaries
- `map()` für die Formatierung von Datenstrukturen
- Funktionale Transformationen statt imperativer Schleifen

## 5. Technische Details

### 5.1 Verwendete Python-Features

- **Dataclasses**: Für die Modellklassen (Python 3.7+)
- **Type Hints**: Für bessere Code-Dokumentation und statische Analyse
- **Generators**: Mit `yield` für Lazy Evaluation
- **itertools**: `cycle()`, `islice()` für Iterator-Manipulation
- **functools**: `reduce()` für funktionale Reduktionen
- **tracemalloc**: Für Speicher-Profiling
- **time.perf_counter()**: Für präzise Zeitmessungen

### 5.2 Projektstruktur

```
src/student_projects/g03/
├── src/
│   ├── models.py          # Domänenmodelle
│   ├── services.py         # Geschäftslogik
│   ├── sensors.py          # Sensordaten-Generatoren
│   └── main.py             # CLI und Benchmarks
├── data/
│   └── rabbitfarm_data.json  # Persistierte Daten
├── static/notebooks/
│   └── layz_vs_eager.ipynb  # Jupyter-Notebook für Analysen
└── tests/
    └── test_rabbit_farm.py   # Unit-Tests
```

### 5.3 Abhängigkeiten

- **Standardbibliothek**: Keine externen Abhängigkeiten für Kernfunktionalität
- **Optional**: `matplotlib`, `numpy`, `pandas` für Visualisierungen (in Notebooks)
- **Testing**: `pytest` für Unit-Tests

## 6. Implementierungsentscheidungen

### 6.1 Warum Generatoren?

Generatoren wurden gewählt, um:
- Die wissenschaftliche Fragestellung zur Speichereffizienz zu untersuchen
- Unendliche Datenströme zu simulieren (Sensordaten)
- Memory-Effizienz bei großen Datenmengen zu demonstrieren

### 6.2 Warum funktionale Programmierung?

Funktionale Ansätze wurden verwendet, um:
- Code-Klarheit durch deklarative Beschreibungen zu erhöhen
- Nebenwirkungen zu minimieren
- Testbarkeit zu verbessern (reine Funktionen)
- Parallele Verarbeitung zu ermöglichen (theoretisch)

### 6.3 Warum JSON-Persistenz?

JSON wurde gewählt, weil:
- Einfache Serialisierung/Deserialisierung
- Menschenlesbares Format für Debugging
- Keine zusätzlichen Abhängigkeiten erforderlich
- Ausreichend für den Prototyp-Charakter des Projekts

Die Implementierung demonstriert praktisch die Unterschiede zwischen Eager und Lazy Evaluation und ermöglicht quantitative Vergleiche hinsichtlich Speicherverbrauch und Laufzeit.

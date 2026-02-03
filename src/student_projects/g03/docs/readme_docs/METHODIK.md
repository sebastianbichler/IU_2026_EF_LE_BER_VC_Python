# Methodik

## 1. Überblick

Ziel dieser Arbeit ist es, die Forschungsfrage zur Speichereffizienz von Lazy Evaluation im bezug der Sensordatenverarbeitung zu untersuchen. Dabei liegt der Fokus stark auf den quantitativen Vergleich zwischen Eager Evaluation und Lazy Evaluation hinsichtlich der Laufzeit und Speicherverbrauch

## 2. Forschungsdesign

### 2.1 Experimenteller Ansatz

Für die Untersuchung werden beide Evaluation unter identischer Bedingung gestet, sodass eine faire Vergleichbasis zu gewährleisten ist.

Bei der Eager Evaluation werden die Daten vor der Verarbeitung vollständig in Listen Materalisiert. 

Lazy hingegen verarbeitet einzelne Daten (Daten die er sofort bekommt), ohne es vollständig zu Materalisieren.

### 2.2 Abhängige Variablen

Zum Untersuchen wurden Variabeln deklariert, die für beide Evaluation gelten. Einmal die Laufzeit in Sekunden. Peak Mamory, also der maximaler Speicherverbrauch während der Verarbeitung in Megabyte und als letzes die Datenstruktur-Größe (Listen vs. Generatoren).

## 3. Datenbasis

### 3.1 Synthetische Sensordaten

Für das Experiment werden synthetisch generierte Sensordaten verwendet, dass sind Daten die simuliert werden. Dabei wird das Szenarie eines Gemüsehos mit Bodenfeuchtigkeitsmessungen simulieren. Die Simulation wird aus dem Modul `sensors.py` mit der Funktion `stream_soil_moisture()` erzeugt.

**Datenstruktur:**
```python
{
    "bed_id": int,           # ID des Beeets
    "moisture": float,       # Bodenfeuchtigkeit in Prozent
    "timestamp": datetime    # Zeitstempel der Messung
}
```

**Generierungslogik:**

Die Feuchtigkeit wird in Prozent dargstellt, sodass es verständniss voller ist für einen Benutzer.
Um es etwas realistisch darzustellen, wurde ein Basis-Wert festgestellt, sodass die generierten Sensordaten nicht irgendwelche Zahlen sind zwischen 1-100 (unrealistisch). Aus diesem Grund wurde die Basis-Feuchtigkeit 50% ausgewählt mit +/- 10% für die Zufällige Variation.

### 3.2 Datenmengen

Für eine präzise Untersuchung, werden verschiedene Datenmengen getstet:

- 100.000 Messwerte
- 1.000.000 Messwerte
- 10.000.000 Messwerte

Dadurch wird das Verhalten präzise Analysiert, was die Schlussfolgerung bzw. beantwortung der Forschungsfrage erheblich erleichtert.

## 4. Implementierung der Vergleichsfunktionen

### 4.1 Eager Evaluation (`process_eager()`)

Die Eager-Variante materialisiert alle Daten vor der Verarbeitung:

```python
def process_eager(data_list, threshold_low=35.0):
    filtered = [d for d in data_list if d["moisture"] < threshold_low or d["moisture"] > 80.0] # Daten werden Matrialisiert (Filterung)
    
    irrigation = [{"bed_id": d["bed_id"], "moisture": d["moisture"], 
                   "irrigation_need": max(0, min(100, 100 - d["moisture"]))} 
                  for d in filtered] # Mapping von filtered
    return irrigation
```

**Charakteristika:**
- Alle Daten werden vollständig im Hauptspeicher gehalten
- Zwischenergebnisse werden als Listen gespeichert
- Speicherverbrauch wächst linear mit der Datenmenge

### 4.2 Lazy Evaluation (`process_lazy()`)

Die Lazy-Variante verwendet Generator-Pipelines:

```python
def process_lazy(data_gen, threshold_low=35.0, max_items=None):
    filtered = filter(lambda d: d["moisture"] < threshold_low or d["moisture"] > 80.0, data_gen) # Generator-Expression
    
    # 2. Lazy Map: Generator-Expression
    irrigation = map(lambda d: { # Mapping
        "bed_id": d["bed_id"],
        "moisture": d["moisture"],
        "irrigation_need": max(0, min(100, 100 - d["moisture"]))
    }, filtered)
    
    if max_items: # Begrenzung des Outputs, falls vorhanden
        irrigation = islice(irrigation, max_items)
    
    return list(irrigation)  # Materialisierung vor dem return
```

**Charakteristika:**
- Daten werden on-demand verarbeitet (lazy evaluation)
- Zwischenergebnisse werden nicht gespeichert
- Speicherverbrauch bleibt konstant, unabhängig von der Datenmenge

## 5. Messmethoden und Tools

### 5.1 Laufzeitmessung

**Tool:** `time.perf_counter()` aus dem Standardmodul `time`

**Methode:**
```python
start_time = time.perf_counter() # Start vom Timer (Messung startet)
# Alle Verarbeitungen...
elapsed_time = time.perf_counter() - start_time # Ende der Messung bzw. Zeit wird berechnet
```

**Begründung:** `perf_counter()` bietet die höchste verfügbare Auflösung und ist für Performance-Messungen optimiert. Es ist nicht von System-Uhränderungen betroffen und eignet sich daher für präzise Zeitmessungen.

### 5.2 Speichermessung

**Tool:** `tracemalloc` aus dem Standardmodul `tracemalloc`

**Methode:**
```python
tracemalloc.start() # Start vom tracemalloc
# Alle Verarbeitung...
current, peak = tracemalloc.get_traced_memory() # Aktuelle Auslastung und höchste Auslastung werden aufgezeichnet
tracemalloc.stop() # tracemalloc wird beendet
```

**Messgrößen:**
- **Peak Memory:** Maximaler Speicherverbrauch während der Ausführung (in Bytes, umgerechnet in MB)
- **Current Memory:** Aktueller Speicherverbrauch zum Zeitpunkt der Messung

**Begründung:** `tracemalloc` ist das Standard-Tool für Speicher-Profiling in Python und ermöglicht eine präzise Nachverfolgung des Speicherverbrauchs während der Laufzeit.

### 5.3 Datenstruktur-Größe

**Tool:** `sys.getsizeof()` aus dem Standardmodul `sys`

**Methode:**
```python
data_size = sys.getsizeof(data_list)
for item in data_list[:100]:  # Stichprobe
    data_size += sys.getsizeof(item)

gen_size = sys.getsizeof(data_gen)
```

**Begründung:** `sys.getsizeof()` liefert die Größe eines Objekts in Bytes. Für Listen wird zusätzlich eine Stichprobe der Elemente gemessen, um eine realistische Schätzung zu erhalten. Generatoren haben eine konstante Größe unabhängig von der Datenmenge.

## 6. Benchmark-Funktionen

### 6.1 Struktur der Benchmark-Funktionen

Beide Benchmark-Funktionen (`benchmark_eager()` und `benchmark_lazy()`) folgen einer identischen Struktur:

1. **Initialisierung:** Start von `tracemalloc` und Zeitmessung
2. **Datenverarbeitung:** Aufruf der jeweiligen Verarbeitungsfunktion
3. **Messung:** Erfassung von Laufzeit und Speicherverbrauch
4. **Rückgabe:** Strukturiertes Dictionary mit allen Messwerten

### 6.2 Reproduzierbarkeit

Um die **Reproduzierbarkeit** der Ergebnisse zu gewährleisten:

- **Kontrollierte Umgebung:** Alle Tests werden auf derselben Hardware und Python-Version durchgeführt
- **Wiederholungen:** Jeder Benchmark wird mehrfach ausgeführt (empfohlen: mindestens 3 Durchläufe)
- **Isolation:** Jeder Test läuft in einem isolierten Prozess ohne Einfluss von vorherigen Tests
- **Datenkonsistenz:** Synthetische Daten werden mit festem Seed generiert (falls implementiert)

## 7. Experimenteller Ablauf

### 7.1 Testaufbau

1. **Vorbereitung:**
   - Initialisierung der Testumgebung
   - Festlegung der Testparameter (Beet-ID, Basis-Feuchtigkeit, Anzahl Messwerte)

2. **Durchführung:**
   - Ausführung von `benchmark_eager()` mit definierter Datenmenge
   - Ausführung von `benchmark_lazy()` mit identischer Datenmenge
   - Erfassung aller Messwerte

3. **Wiederholung:**
   - Wiederholung für verschiedene Datenmengen (100.000, 1.000.000, 10.000.000)
   - Mehrfache Ausführung pro Datenmenge zur Mittelwertbildung

4. **Auswertung:**
   - Berechnung von Durchschnittswerten und Standardabweichungen
   - Vergleich der Messwerte zwischen Eager und Lazy
   - Berechnung von Effizienzgewinnen (Prozentuale Unterschiede)

### 7.2 Validierung der Ergebnisse

**Kontrollgruppe:** Um sicherzustellen, dass beide Ansätze **korrekte Ergebnisse** liefern:

- Vergleich der Ergebnislisten: Beide Methoden müssen identische Ergebnisse produzieren
- Validierung der Filterlogik: Überprüfung, dass die Filterkriterien korrekt angewendet werden
- Konsistenzprüfung: Mehrfache Ausführungen mit identischen Eingabedaten müssen identische Ergebnisse liefern

## 8. Technische Umgebung

### 8.1 Python-Version und Abhängigkeiten

- **Python:** Version 3.8 oder höher
- **Standardbibliothek:** `time`, `sys`, `tracemalloc`, `itertools`, `functools`
- **Externe Bibliotheken:** `memory-profiler` (optional, für detaillierte Analysen)

### 8.2 Systemanforderungen

- **Betriebssystem:** macOS und Windows (für Reproduzierbarkeit)
- **Hardware:** Mindestens 4 GB RAM (für große Datenmengen)
- **Python-Umgebung:** Virtuelles Environment empfohlen

## 9. Limitationen und Einschränkungen

### 9.1 Methodische Limitationen

- **Synthetische Daten:** Die Ergebnisse basieren auf simulierten Daten und müssen nicht zwangsläufig auf reale Szenarien übertragbar sein
- **Speichermessung:** `sys.getsizeof()` liefert nur eine Näherung; tatsächlicher Speicherverbrauch kann durch Python's Memory-Management variieren
- **Overhead:** Generator-Overhead kann bei sehr kleinen Datenmengen die Vorteile aufwiegen

### 9.2 Externe Faktoren

- **Systemlast:** Andere laufende Prozesse können die Messungen beeinflussen
- **Garbage Collection:** Python's automatische Speicherbereinigung kann zu Schwankungen führen
- **Hardware-Variabilität:** Unterschiedliche Hardware kann zu unterschiedlichen Ergebnissen führen

## 10. Zusammenfassung

Die Methodik basiert hauptsächlich auf einem systematischen Benchmarking-Ansatz mit Experimenten zur Vergleich von Eager- und Lazy-Evaluation bei der Abarbeitung von Sensoredaten. Durch die Python-Tools (`tracemalloc`, `time.perf_counter`, `sys.getsizeof`) und die Systematische Variation der Datenmenge (10.000, 1.000.000, 10.000.000) ermöglicht es eine wissenschaftliche Anlyse der Speicher- und Laufzeiteffizienz.

Die Ergebnisse der Methodik soll die Forschungsfrage beantworten, was der unterschied zwischen Lazu und Eager Evaluation bei der Verarbeitung von Sensoredaten bestehen, und unter welchen Bedingungen welcher Ansatz geeignet ist

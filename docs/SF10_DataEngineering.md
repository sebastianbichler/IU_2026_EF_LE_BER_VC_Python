### DLBDSIPWP01 - Einführung in die Programmierung mit Python (Projekt)

---

# Thema 10: Data Engineering & Out-of-Core Computing (Dask)

### 1. Einleitung & Kontext

In den vorherigen Kapiteln haben wir gelernt, wie Python Speicher verwaltet. Doch was passiert, wenn die Datenmenge den
physischen Arbeitsspeicher (RAM) sprengt? Ein herkömmlicher `pandas.DataFrame` oder ein `numpy.array` muss vollständig
im RAM liegen. Versuchen wir, eine 100 GB CSV-Datei auf einem 16 GB Laptop zu laden, stürzt Python mit einem
`MemoryError` ab.

Hier setzt **Out-of-Core Computing** an. Anstatt die Daten "einzusperren", werden sie in kleinen Häppchen (Chunks) von
der Festplatte gestreamt, verarbeitet und wieder verworfen.

- **C# Analogie:** Ähnlich wie `IEnumerable` mit "Lazy Evaluation" (LINQ), aber massiv parallelisiert und für numerische
  Matrix-Operationen optimiert.
- **Dask:** Ist das Standard-Framework in Python, das die APIs von Toolkits wie Pandas und NumPy übernimmt, sie aber auf
  Task-Graphen verteilt, die über alle CPU-Kerne oder sogar ganze Server-Cluster skalieren.

---

### 2. Wissenschaftliche Fragestellung

> *"Skalierbarkeit von In-Memory-Algorithmen bei Datenüberschreitung des physikalischen RAMs: Eine Untersuchung von
Task-Scheduling-Strategien in Dask zur Minimierung von Disk-I/O-Overhead."*

**Kernfokus:** Wie partitioniert man Daten optimal, damit die CPU nicht auf die langsame Festplatte warten muss (
I/O-Bound vs. CPU-Bound)?

---

### 3. Wissenschaftlicher Hintergrund

**Publikation:** *Dask: Parallel Computation with Blocked Algorithms* (Matthew Rocklin).

Das Herzstück von Dask ist der **Task Graph** (ein gerichteter, azyklischer Graph - DAG). Wenn wir eine Operation
definieren (z. B. "Berechne den Mittelwert aller GPS-Punkte"), führt Dask diese nicht sofort aus. Es erstellt einen
Bauplan. Erst beim Aufruf von `.compute()` entscheidet der Scheduler, welche Datenhäppchen wann geladen und auf welchen
Kernen berechnet werden. Dies ermöglicht **Lazy Evaluation** auf Steroiden.

---

### 4. Code-Demonstration (Notebook-Stil)

Wir simulieren die Analyse von mehreren Terabytes an Sensor-Daten der Elefanten-Herden.

#### Schritt 1: Simulation einer riesigen Datenmenge

Python

```python
import numpy as np
import dask.array as da

# Wir erstellen ein virtuelles Array mit 100.000 x 100.000 Elementen
# Das wären ca. 80 Gigabyte – zu viel für den normalen RAM!
# Wir unterteilen es in "Chunks" von 1000x1000
huge_data = da.random.random((100000, 100000), chunks=(10000, 10000))

print(f"Größe des Arrays: {huge_data.nbytes / 1e9} GB")
# Hinweis: Es wurde noch kein Byte im RAM belegt!
```

#### Schritt 2: Lazy Evaluation (Der Bauplan)

Wir definieren komplexe Operationen. Dask rechnet noch nicht, es "plant" nur.

Python

```python
# Berechnung des Mittelwerts über eine Achse
result = huge_data.mean(axis=0)

# Man kann sich den Graphen sogar ansehen (erfordert graphviz)
# result.visualize()
print("Operation ist definiert, aber noch nicht ausgeführt.")
```

#### Schritt 3: Die Ausführung (Parallel & Out-of-Core)

Erst jetzt wird die CPU aktiv. Dask lädt Chunk für Chunk, berechnet Teil-Mittelwerte und setzt sie zusammen.

Python

```python
# Erst jetzt wird gerechnet
final_mean = result.compute()
print(f"Berechnung abgeschlossen. Erster Wert: {final_mean[0]}")
```

---

### 5. Zusammenfassung für die Folien

| **Merkmal**      | **Pandas / NumPy** | **Dask**                       |
|------------------|--------------------|--------------------------------|
| **Datengröße**   | Begrenzt durch RAM | Begrenzt durch Festplatte (TB) |
| **Ausführung**   | Eager (Sofort)     | Lazy (Verzögert)               |
| **Parallelität** | Meist Single-Core  | Multi-Core & Distributed       |
| **API**          | Standard           | Fast identisch zu Standard     |

---

### Anwendung im Projekt "Elephant Memory Cloud"

Stellen Sie sich vor, wir speichern 10 Jahre GPS-Historie von 500 Elefanten (Sekundentakt). Das sind Milliarden von
Zeilen.

1. **Preprocessing:** Wir nutzen `dask.dataframe`, um die Rohdaten zu bereinigen (Outliers entfernen), ohne einen
   Supercomputer zu benötigen.
2. **Feature Engineering:** Wir berechnen Bewegungsprofile (z. B. Durchschnittsgeschwindigkeit pro Tag) über den
   gesamten Datensatz hinweg.
3. **Integration:** Dask lässt sich nahtlos mit Scikit-Learn verbinden, um Machine-Learning-Modelle auf Daten zu
   trainieren, die nicht in den Speicher passen.

> **Merksatz:** "Dask ist wie eine gut organisierte Großküche. Während Pandas ein Koch ist, der alle
> Zutaten gleichzeitig auf den Tisch legt, ist Dask der Chef, der die Arbeit so aufteilt, dass die Pfannen (CPU-Kerne)
> immer voll sind, aber nie mehr Zutaten im Raum sind, als auf die Arbeitsplatte (RAM) passen."

---

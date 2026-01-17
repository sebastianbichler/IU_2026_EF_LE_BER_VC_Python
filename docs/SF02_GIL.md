### DLBDSIPWP01 - Einführung in die Programmierung mit Python (Projekt)

---

# Thema 2: Global Interpreter Lock (GIL) vs. Multi-Core-Effizienz

### 1. Einleitung & Kontext

Moderne CPUs haben 8, 16 oder mehr Kerne. In C# (.NET) ist es Standard, dass `Task.Run()` oder `Parallel.ForEach()`
diese Kerne voll ausnutzt. In Python stoßen wir jedoch auf das **GIL**.

Das GIL ist ein Mutex (ein Schloss), das sicherstellt, dass zu jedem Zeitpunkt **nur ein Thread** die Kontrolle über den
Python-Interpreter hat.

- **Warum?** Es schützt das im ersten Thema besprochene *Reference Counting* vor Race Conditions. Ohne das GIL könnten
  zwei Threads gleichzeitig den Zähler eines Objekts ändern, was zu Speicherfehlern führen würde.

- **Die Folge:** Python-Threads sind hervorragend für **I/O-bound** Aufgaben (Warten auf Netzwerk/Festplatte), aber oft
  nutzlos für **CPU-bound** Aufgaben (Berechnungen).

---

### 2. Wissenschaftliche Fragestellung

> *"Evaluierung der Skalierbarkeit von CPU-intensiven Algorithmen in CPython: Eine quantitative Analyse des Overheads
durch das Global Interpreter Lock im Vergleich zu echtem Parallelismus in C#."*

**Kernfokus:** Ab welchem Punkt übersteigt der Overhead des Kontextwechsels (Thread-Switching) den Nutzen der
Parallelisierung in Python?

---

### 3. Wissenschaftlicher Hintergrund

**Publikation:** *Understanding the Python GIL* (David Beazley) oder die aktuellen Debatten zu **PEP 703** (Making the
Global Interpreter Lock Optional in CPython).

Die Forschung zeigt, dass das GIL bei Single-Core-Operationen sogar ein Performance-Vorteil sein kann (da kein
Locking-Overhead für jedes einzelne Objekt anfällt). Bei Multi-Core-Systemen führt es jedoch zum sogenannten **"Convoy
Effect"**, bei dem Threads sich gegenseitig blockieren und die Performance sogar unter die eines Single-Thread-Programms
sinken kann.

**Aktueller Hinweis (2026):** Mit Python 3.13+ wurde der "Free-Threaded" Modus eingeführt, der das GIL optional macht –
ein Meilenstein, der die Sprache näher an die Effizienz von C# rückt. Aber wie funktioniert das genau?

---

### 4. Code-Demonstration (Notebook-Stil)

In diesem Experiment vergleichen wir eine rechenintensive Aufgabe (CPU-bound) in drei Szenarien: Sequenziell,
Multi-Threading (mit GIL) und Multi-Processing (ohne GIL).

#### Schritt 1: Die Rechenaufgabe definieren

Python

```
import time
import threading
import multiprocessing

def heavy_computation(n):
    # Eine einfache, CPU-intensive Aufgabe
    count = 0
    for i in range(n):
        count += i
    return count

N = 10**7 # Anzahl der Operationen
```

#### Schritt 2: Sequenziell vs. Multi-Threading (Das GIL-Dilemma)

Python

```
# 1. Sequenziell
start = time.time()
heavy_computation(N)
heavy_computation(N)
print(f"Sequenziell: {time.time() - start:.4f}s")

# 2. Multi-Threading (2 Threads)
t1 = threading.Thread(target=heavy_computation, args=(N,))
t2 = threading.Thread(target=heavy_computation, args=(N,))

start = time.time()
t1.start(); t2.start()
t1.join(); t2.join()
print(f"Multi-Threading (GIL): {time.time() - start:.4f}s")
```

*Beobachtung:* Die Zeit für Multi-Threading wird fast identisch (oder sogar langsamer) sein als die sequenzielle
Ausführung, da das GIL echtes Parallelrechnen verhindert.

#### Schritt 3: Der Ausweg – Multi-Processing

Python

```
# 3. Multi-Processing (Echter Parallelismus)
p1 = multiprocessing.Process(target=heavy_computation, args=(N,))
p2 = multiprocessing.Process(target=heavy_computation, args=(N,))

start = time.time()
p1.start(); p2.start()
p1.join(); p2.join()
print(f"Multi-Processing: {time.time() - start:.4f}s")
```

*Ergebnis:* Hier wird die Zeit nahezu halbiert, da jeder Prozess seinen eigenen Interpreter und damit sein eigenes GIL
hat.

---

### 5. Zusammenfassung

| **Merkmal**       | **Multi-Threading (Python)** | **Multi-Processing (Python)**  | **C# Tasks / Threads** |
|-------------------|------------------------------|--------------------------------|------------------------|
| **Parallelität**  | Scheinbar (Concurrency)      | **Echt (Parallelism)**         | **Echt (Parallelism)** |
| **GIL**           | Aktiv (blockiert CPU)        | Umgangen (eigener Interpreter) | Nicht vorhanden        |
| **Speicher**      | Gemeinsam genutzt (Shared)   | Isoliert (Copy-on-write)       | Gemeinsam genutzt      |
| **Best Use Case** | I/O (Web-Requests, DB)       | CPU (Datenanalyse, Mathe)      | Alles (Hochperformant) |

---

### Anwendung im Projekt "Elephant Memory Cloud"

In unserem Archiv müssen wir oft riesige Mengen an Bilddaten der Elefanten vorverarbeiten.

- **Falscher Ansatz:** Python-Threads nutzen, um 100 Bilder gleichzeitig zu filtern (das GIL würde alles in die Länge
  ziehen).

- **Richtiger Ansatz:** `concurrent.futures.ProcessPoolExecutor` verwenden, um die Last auf alle CPU-Kerne zu verteilen.

- Man könnte beide Ansätze in einem Jupyter Notebook demonstrieren, um die Performance-Unterschiede live zu zeigen.

---

### DLBDSIPWP01 - Einführung in die Programmierung mit Python (Projekt)

---

## Wissenschaftliche Schwerpunkte in Python (TOPICS)

Die folgenden Schwerpunkte sind speziell auf Python zugeschnitten und bieten die Möglichkeit, tief in
fortgeschrittene Konzepte einzutauchen, die über die Grundlagen hinausgehen. Jeder Schwerpunkt ist mit einer
wissenschaftlichen Fragestellung, relevanten Publikationen und einer praktischen Anwendung im Projektkontext verknüpft.

### 1. Memory Management: Reference Counting vs. Cyclic Garbage Collection

Python nutzt primär Reference Counting, ergänzt durch einen zyklischen GC. Dies ist ein direkter Kontrast zum
Mark-and-Sweep in C#.

- **Wissenschaftliche Fragestellung:** "Analyse der Latenzzeiten und Speichereffizienz bei der Verarbeitung großskaliger
  Objekt-Graphen: Ein Vergleich zwischen Pythons Referenzzählung und C# Garbage Collection."

- **Publikation:** *Garbage Collection in Python* (Python Docs Internals) oder *Relevance of Garbage Collection in
  Python* (Lany et al.).

- **Anwendung im Projekt:** Optimierung des "Elephant Memory Cloud"-Archivs zur Vermeidung von Memory Leaks bei
  zirkulären Verwandtschaftsbeziehungen.

### 2. Global Interpreter Lock (GIL) & Multi-Core-Effizienz

Das GIL ist das wohl am heißesten diskutierte Thema in Python. Es verhindert echtes Multi-Threading für CPU-intensive
Aufgaben.

- **Wissenschaftliche Fragestellung:** "Evaluierung der Skalierbarkeit von Multi-Processing vs. Multi-Threading in
  Python unter Berücksichtigung des Inter-Process-Communication (IPC) Overheads."

- **Publikation:** *Understanding the Python GIL* (David Beazley).

- **Anwendung:** Parallelisierung der Damm-Berechnungen in "Beaver Builders" mittels `multiprocessing` und
  `shared_memory`.

### 3. Asynchrone Programmierung & Event Loops (asyncio)

Ähnlich wie TAP in C#, aber auf einem Single-Threaded Event Loop basierend.

- **Wissenschaftliche Fragestellung:** "Durchsatzanalyse von High-Concurrency-Systemen: Eine empirische Untersuchung von
  Pythons `asyncio` gegenüber thread-basierten Modellen in Web-Anwendungen."

- **Publikation:** *A Survey of Asynchronous Programming Models* (diverse Fachliteratur).

- **Anwendung:** Verwaltung tausender gleichzeitiger Sensor-Datenströme in der "Mole’s Metro Map" oder "Honeybee
  Smart-Hive".

### 4. Vectorization & SIMD mit NumPy (Numerical Python)

Weg von Schleifen, hin zu CPU-Vektorbefehlen. Dies ist der Kern von High-Performance Python.

- **Wissenschaftliche Fragestellung:** "Performance-Analyse von Array-orientierter Programmierung: Der Einfluss von
  Cache-Lokalität und SIMD-Instruktionen auf die numerische Simulation."

- **Publikation:** *Array programming with NumPy* (Harris et al., Nature 2020).

- **Anwendung:** Komplexe meteorologische Simulationen für die "Squirrel Secret Stash" Winterprognose.

### 5. Metaprogrammierung & Introspection

Python erlaubt es, Klassen während der Laufzeit zu verändern (Metaklassen).

- **Wissenschaftliche Fragestellung:** "Deklarative Systemarchitekturen in Python: Nutzung von Metaklassen und
  Deskriptoren zur automatisierten Validierung von Geschäftslogik."

- **Publikation:** *Expert Python Programming* (Tarek Ziadé) – Kapitel über Metaprogramming.

- **Anwendung:** Dynamische Erstellung von Tier-Dienstleistungen im "Panda Spa" basierend auf Konfigurationsdateien ohne
  Code-Änderung.

### 6. Just-In-Time (JIT) Compilation (Numba & PyPy)

Wie kann eine interpretierte Sprache C-Geschwindigkeit erreichen?

- **Wissenschaftliche Fragestellung:** "Effektivität von JIT-Kompilierung in wissenschaftlichen Python-Anwendungen: Ein
  Vergleich von Numba, PyPy und CPython."

- **Publikation:** *Numba: A python compiler for introspection-based JIT optimization* (Lam et al.).

- **Anwendung:** Echtzeit-Routenoptimierung für "Fox Express" in einem hochkomplexen Graphennetzwerk.

### 7. Probabilistische Programmierung & Statistische Modellierung

Python ist führend in der Bayesschen Statistik.

- **Wissenschaftliche Fragestellung:** "Unsicherheitsquantifizierung in Vorhersagemodellen: Anwendung von
  Markov-Chain-Monte-Carlo-Verfahren (MCMC) zur Risikoanalyse."

- **Publikation:** *Probabilistic Programming in Python using PyMC3* (Salvatier et al.).

- **Anwendung:** Vorhersage der Wahrscheinlichkeit von Fischknappheit im "PenguEats" basierend auf unvollständigen
  Fangdaten.

### 8. Structural Design Patterns in dynamischen Sprachen

Wie ändern sich klassische Entwurfsmuster (Gang of Four) in einer Sprache ohne Interfaces, aber mit "Duck Typing"?

- **Wissenschaftliche Fragestellung:** "Wandel der Design Patterns: Eine Untersuchung der Implementierungseffizienz
  klassischer Entwurfsmuster in dynamisch typisierten Sprachen."

- **Publikation:** *Design Patterns in Python* (Diverse Quellen).

- **Anwendung:** Architektur eines modularen Recyclingsystems in "Raccoon’s Recycling Garage".

### 9. Typisierung: Gradual Typing & MyPy

Python bewegt sich Richtung statischer Typisierung (Type Hints), ähnlich wie TypeScript oder C#.

- **Wissenschaftliche Fragestellung:** "Einfluss von statischer Typisierung auf die Wartbarkeit und Fehlerrate in
  Python-Großprojekten: Eine empirische Studie."

- **Publikation:** *The Theory of Static Type Checking in Python* (diverse PEPs und wissenschaftliche Begleitartikel).

- **Anwendung:** Refactoring einer der Projekt-Codebasen von rein dynamisch zu voll typisiert inklusive statischer
  Code-Analyse.

### 10. Data Engineering & Out-of-Core Computing (Dask)

Was tun, wenn die Daten nicht mehr in den RAM passen?

- **Wissenschaftliche Fragestellung:** "Algorithmen für verteilte Graphenberechnungen: Skalierung von
  Datenverarbeitungsprozessen jenseits der Hauptspeichergrenzen mittels Dask."

- **Publikation:** *Dask: Parallel Computation with Blocked algorithms and Task Scheduling* (Rocklin).

- **Anwendung:** Analyse der globalen Migrationspfade aller Tiere in der "Elephant Memory Cloud".

### 11. Interoperabilität: C-Extensions & Cython

Wie verbindet man die Benutzerfreundlichkeit von Python mit der Macht von C/C++?

- **Wissenschaftliche Fragestellung:** "Quantifizierung des Overheads beim Language-Bridging: Analyse der
  Performance-Gewinne durch Cython-Wrapping in rechenintensiven Kernels."

- **Publikation:** *Cython: The Best of Both Worlds* (Behnel et al.).

- **Anwendung:** Schreiben eines kritischen Berechnungs-Moduls (z.B. Strömungssimulation für Biber-Staudämme) in C und
  Einbindung in Python.

### 12. Funktionales Programmieren & Lazy Evaluation

Python bietet Iteratoren und Generatoren (vergleichbar mit LINQ in C#).

- **Wissenschaftliche Fragestellung:** "Speichereffizienz von Lazy Evaluation: Vergleich von Eager- vs.
  Lazy-Datenverarbeitung in Stream-Processing-Systemen."

- **Publikation:** *Functional Programming in Python* (David Mertz).

- **Anwendung:** Verarbeitung endloser Nektar-Datenströme im "Honeybee Smart-Hive" ohne Speicherüberlauf.

---

### Methodik für die Studierenden (Der wissenschaftliche Teil):

Um den methodischen Anspruch zu sichern, sollten die Gruppen folgende Schritte durchlaufen:

1. **Benchmarking:** Messung der Performance (Zeit/Speicher) vor und nach der Anwendung des Schwerpunkts (z.B. Python
   Loop vs. NumPy Vectorization).

2. **Profiling:** Nutzung von Tools wie `cProfile` oder `memory_profiler`, um Engpässe wissenschaftlich nachzuweisen.

3. **Dokumentation:** Ein kurzes Paper (4-6 Seiten), das die gewählte Forschungsfrage mit den Ergebnissen des Projekts
   beantwortet.

### DLBDSIPWP01 - Einführung in die Programmierung mit Python (Projekt)

---

## Übersichtstabelle: Zuweisung der Themen zu Projekten

| **Aufgabe** | **Projektname**       | **Wissenschaftlicher Schwerpunkt (Topic)** | **Fokus der Forschung**                               |
|-------------|-----------------------|--------------------------------------------|-------------------------------------------------------|
| 1           | **PenguEats**         | 7. Probabilistische Programmierung         | Unsicherheitsquantifizierung bei Fischbeständen       |
| 2           | **Panda Spa**         | 5. Metaprogrammierung                      | Deklarative Validierung von Wellness-Dienstleistungen |
| 3           | **Bear HoneyWorks**   | 9. Typisierung (MyPy)                      | Wartbarkeit komplexer Maschinen-Klassenhierarchien    |
| 4           | **FoxPost**           | 10. Data Engineering (Dask)                | Out-of-Core Routing bei massiven Paketdaten           |
| 5           | **OwlBooks**          | 1. Memory Management                       | Analyse zirkulärer Referenzen in Buch-Kategorien      |
| 6           | **RabbitFarm**        | 12. Funktionales Programmieren             | Lazy Evaluation von Ernte-Datenströmen                |
| 7           | **WolfLeague**        | 9. Typisierung (Gradual Typing)            | Statische Analyse von Spielerstatistiken              |
| 8           | **DeerFit**           | 5. Metaprogrammierung                      | Nutzung von Deskriptoren für Trainingspläne           |
| 9           | **Squirrel Stash**    | 4. Vectorization (NumPy)                   | SIMD-basierte Winter-Wettersimulation                 |
| 10          | **Owl’s Library**     | 3. Asynchrone Programmierung               | High-Concurrency Monitoring der Flüster-Lautstärke    |
| 11          | **Beaver Builders**   | 2. GIL & 11. Interoperabilität             | Multi-Processing und C-Extensions für Statik          |
| 12          | **Fox Express**       | 6. JIT Compilation (Numba)                 | Echtzeit-Optimierung komplexer Graphen-Routen         |
| 13          | **Raccoon Recycling** | 8. Structural Design Patterns              | Implementierung modularer Upcycling-Muster            |
| 14          | **Chameleon Color**   | 7. Probabilistische Programmierung         | MCMC-Verfahren zur Tarnungs-Optimierung               |
| 15          | **Elephant Memory**   | 1. Memory Management                       | Speichereffizienz bei riesigen Objekt-Graphen         |
| 16          | **Mole’s Metro**      | 3. Asynchrone Programmierung               | Event-Loop basierte Auswertung von Erdsensoren        |
| 17          | **Honeybee Hive**     | 12. Funktionales Programmieren             | Generatoren zur Verarbeitung von Nektar-Streams       |
| 18          | **Sloth’s Hotel**     | 8. Structural Design Patterns              | Zustandsbasierte Muster für Entspannungsprozesse      |

---

### Zusammenfassende Übersichtstabelle für die Vorlesung

| **Aufgabe**                 | **Fokus-Thema (Topic)** | **Methodisches Werkzeug** |
|-----------------------------|-------------------------|---------------------------|
| **Pinguin / Chamäleon**     | Statistik / Bayes       | PyMC3 / Random            |
| **Panda / Hirsch**          | Metaprogrammierung      | Decorators / Descriptors  |
| **Bär / Wolf**              | Statische Typisierung   | MyPy / Type Hints         |
| **Fuchs (Post) / Elefant**  | Datenmenge / Speicher   | Dask / GC-Profiling       |
| **Eule (Bücher / Night)**   | Memory / Async          | `gc` / `asyncio`          |
| **Hase / Bienen**           | Funktional / Lazy       | Generators / Itertools    |
| **Biber / Fuchs (Express)** | Performance / JIT       | Cython / Numba            |
| **Waschbär / Faultier**     | Software-Architektur    | Design Patterns           |

## Methodischer Leitfaden zur Abgabe

Jede Gruppe muss zusätzlich zum Code ein kurzes **Paper (4-6 Seiten)** einreichen, das folgende Struktur hat:

1. **Einleitung:** Vorstellung der Forschungsfrage basierend auf dem zugewiesenen Topic.

2. **Methodik:** Beschreibung des Profiling-Setups (z.B. Nutzung von `cProfile` oder `timeit`).

3. **Ergebnisse:** Vergleich der Performance/Effizienz (z.B. Standard Python vs. Optimierung durch das Topic).

4. **Diskussion:** Interpretation der Ergebnisse im Hinblick auf die zitierte Fachliteratur.

# IN ARBEIT

# Zusammenfassung der Teams-Quellen:
## **1: Al Awar et al. -2025- Dynamic Fusing HPC Kernels in Python**
- HPC steht für high-performance computing
- Der Autor spricht explizit über Kokkos als beispielhaftes Framework, welches durch verschiedene API-Anbindungen hardware-übergreifend funktioniert (AMD und NVIDIA GPUs, sowie Intel und AMD CPUs werden als Beispiel genannt)
- Kokkos ist überwiegend in C++ implementiert, durch die Zunahme der interpretierten Sprachen ist PyKokkos für die Implementierung von Python entstanden
- Nachteil: Programmierer müssen Teile des Codes ausgliedern und statisch implementieren. Dadurch werden verschiedene Kerne aktiv und es entstehen teils redundante Vorgänge, die den Arbeitsspeicher unnötig belegen --> Die Lösung ist `Kernal Fusion`. Prozesse sollen mit möglichst wenig aktiven Kernen laufen
- Hier stellt der Autor `PyFuser` vor. 
- PyFuser zeichnet Kernel Prozesse auf und kombiniert sie in einem einzelnen optimierten Kernel
- Dadurch läuft das Programm performanter und es führt zu einem verringerten Start-Overhead (Bei vielen kleinen Kernels summieren sich die Verwaltungsprozesse auf.)
## **2: Ansel et al. - 2024 - PyTorch 2 Faster Machine Learning Through Dynamic Python Bytecode Transformation and Graph Compilation**
## **3: Associate Professor, Mehr Chand Mahajan DAV College for Women, Chandigarh, India und Arora - 2024 - Improving Performance of Data Science Applications in Python** 
## **4: Yang et al. - 2022 - Complex Python features in the wild**
## **5: Mertz - 2015 - Functional Programming in Python**
- David Mertz beschreibt in Functional Programming in Python den Evaluationszeitpunkt von Ausdrücken als einen zentralen Unterschied zwischen imperativen und funktionalen Programmierstilen. Dabei unterscheidet er zwischen Eager (strikter) und Lazy (nicht-strikter) Evaluation.
- Python verwendet standardmäßig Eager Evaluation. Das bedeutet, dass Ausdrücke und Funktionsargumente unmittelbar ausgewertet werden, bevor sie weiterverarbeitet werden. Datenstrukturen wie Listen werden vollständig erzeugt, auch wenn später nur ein Teil der Elemente benötigt wird. Dieser Ansatz ist einfach zu verstehen, gut debuggbar und entspricht dem imperativen Programmiermodell, führt jedoch bei großen Datenmengen zu erhöhtem Speicherverbrauch und verhindert die Arbeit mit potenziell unendlichen Datenstrukturen.
- In der funktionalen Programmierung wird häufig Rekursion anstelle von Iteration eingesetzt. Mertz weist jedoch darauf hin, dass Python aufgrund fehlender Tail-Call-Optimierung rekursive Lösungen ineffizient machen kann. In Verbindung mit Eager Evaluation entstehen dadurch praktische Grenzen hinsichtlich Speicherverbrauch und Rekursionstiefe.
- Lazy Evaluation verfolgt einen anderen Ansatz: Ausdrücke werden erst dann ausgewertet, wenn ihr Wert tatsächlich benötigt wird. Obwohl Python keine vollständige Lazy Evaluation auf Sprachebene unterstützt, stellt es mit Generatoren, Iteratoren und Generator Expressions Mechanismen bereit, die ein lazy Verhalten ermöglichen. Dadurch können große oder sogar unendliche Datenströme effizient verarbeitet werden, da jeweils nur das aktuell benötigte Element berechnet wird.
- Mertz zeigt, dass Lazy Evaluation besonders gut mit funktionalen Konzepten harmoniert, da sie die Transformation von Daten in klaren Verarbeitungspipelines erlaubt und gleichzeitig Speicher- und Laufzeitkosten reduziert. Der wesentliche Unterschied zwischen Eager und Lazy Evaluation liegt somit im Zeitpunkt der Auswertung, wobei Python einen grundsätzlich eager Ansatz verfolgt, diesen jedoch gezielt durch lazy Konstrukte ergänzt.



# Fragestellung
## **1:** *Wie transformieren wir die Daten, die aus einem Stream kommen um sie speichereffizient zu nutzen?*
## **2:** *Worin besteht der Unterschied zwischen Lazy und Eager?*
## **3:** *Das Argument, dass Python eine langsame Sprache ist, kann durch funktionales Programmieren teilentkräftet werden. Wieso?*
## **4:** *Wieso sind Decorators im funktionales Programmieren sinnvoll?*
## **5:** *Wie funktionieren die ITERTOOLS?*
## **6:** *Was ist der Unterschied zwischen imperativem Programmieren und funktionalem Programmieren?*
## **7:** *Welche Vorteile haben NumPy Arrays gegenüber der Python Lists?*



### Antworten auf die Fragen

- **1 — Daten aus Streams speichereffizient transformieren:** Verwende Streaming-Operatoren (Map/Filter/FlatMap) und Pipeline-Modelle, die Elemente in kleinen Batches oder einzeln verarbeiten, statt ganze Datensätze im Speicher zu halten. In Python nutzt man dafür Iteratoren/Generatoren oder Streaming-Frameworks (z. B. Dataflow/Beam), um Transformationen lazy anzuwenden und so Speicherbedarf zu minimieren [1][2].

- **2 — Unterschied Lazy vs. Eager:** Eager (strikte) Evaluation wertet Ausdrücke sofort aus; Lazy (nicht-strikte) Evaluation verzögert die Auswertung bis zur tatsächlichen Verwendung. Lazy erlaubt potenziell unendliche Datenstrukturen und speicherarme Pipelines; Eager ist einfacher zu verstehen und zu debuggen. Für theoretische Details siehe Hughes und Peyton Jones [3][4]. *Nach Kontrolle: Eager ist nicht immer einfacher zu verstehen. Bei vielen statischen Methoden die auf Lazy aufgebaut sind, ist die Funktionsweise auf einen Blick sofort verständlich. Der Gebrauch der unbenannten Lambda-Methoden ist für das funktionale Programmieren üblich. Hier ist die Funktionsweise meist schnell erkenntlich*

- **3 — Warum funktionales Programmieren Python-Verlangsamungs-Argumente entkräften kann:** Funktionale Patterns (Reinheit, Immutability, Higher-Order-Functions) fördern deterministische, parallelisierbare und vektorisierbare Codepfade. In Python ermöglicht das z. B. die Nutzung von Vektoroperationen (NumPy) oder JIT-Compilern (Numba) für rechenkritische Abschnitte — dadurch verschiebt sich der Flaschenhals oft vom Sprach-Overhead in optimierte Bibliotheken [5][6].

- **4 — Sinn von Decorators im funktionalen Kontext:** Decorators sind Higher-Order-Functions, die Funktionen transformieren oder erweitern (z. B. Logging, Caching, Memoization). Sie unterstützen Separation of Concerns und composable Funktionalität ohne zustandsverändernde Seiteneffekte, was gut zu funktionalen Prinzipien passt [3][7].

- **5 — Wie funktionieren die `itertools`?:** `itertools` stellt speichereffiziente, auf Iterators basierende Bausteine (z. B. `islice`, `chain`, `imap`/`starmap`, `tee`) bereit, die lazy kombiniert werden können, um komplexe Stream-Transformationen ohne vollständige Materialisierung durchzuführen. Die Kombination solcher Bausteine erzeugt klare, performante Pipelines [8][9].

- **6 - Was ist der Unterschied zwischen imperativem Programmieren und funktionalem Programmieren?:**

- **7 - NumPy Arrays**


#### Literatur

1. T. Akidau et al., "The Dataflow Model", Google Research / O'Reilly (Streaming Systems), 2015. https://research.google/pubs/pub38137/
2. Dean, J. & Ghemawat, S., "MapReduce: Simplified Data Processing on Large Clusters", OSDI 2004. https://research.google/pubs/pub62/
3. J. Hughes, "Why Functional Programming Matters", 1984. https://www.cs.kent.ac.uk/people/staff/dat/marc/FP/hughes.pdf
4. S. Peyton Jones, "The Implementation of Functional Programming Languages", 1992.
5. S. K. Lam, A. Pitrou, & S. Seibert, "Numba: A LLVM-based Python JIT compiler", 2015. https://arxiv.org/abs/1506.01356
6. NumPy documentation — Vectorized operations and broadcasting. https://numpy.org/doc/
7. PEP 318 — Decorators for Functions and Methods. https://peps.python.org/pep-0318/
8. Python `itertools` documentation. https://docs.python.org/3/library/itertools.html
9. PEP 255 / PEP 342 — Generators and coroutines. https://peps.python.org/


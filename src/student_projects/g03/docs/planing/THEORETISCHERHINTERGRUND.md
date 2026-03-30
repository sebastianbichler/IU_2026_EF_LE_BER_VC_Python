# IN ARBEIT

# Zusammenfassung der Teams-Quellen:
## **1: Al Awar et al. -2025- Dynamic Fusing HPC Kernels in Python**
- HPC steht für high-performance computing
- Der Autor spricht explizit über Kokkos als beispielhaftes Framework, welches durch verschiedene API-Anbindungen hardware-übergreifend funktioniert (AMD und NVIDIA GPUs, sowie Intel und AMD CPUs werden als Beispiel genannt)
- Kokkos ist überwiegend in C++ implementiert, durch die Zunahme der interpretierten Sprachen ist PyKokkos für die Implementierung von Python entstanden
- Nachteil: Programmierer müssen Teile des Codes ausgliedern und statisch implementieren. Dadurch werden verschiedene Kernels aktiv und es entstehen teils redundante Vorgänge, die den Arbeitsspeicher unnötig belegen --> Die Lösung ist `Kernal Fusion`. Prozesse sollen mit möglichst wenig aktiven Kernels laufen
- Hier stellt der Autor `PyFuser` vor.
- PyFuser zeichnet Kernel Prozesse auf und kombiniert sie in einem einzelnen optimierten Kernel
- Dadurch läuft das Programm performanter und es führt zu einem verringerten Start-Overhead (Bei vielen kleinen Kernels summieren sich die Verwaltungsprozesse auf.)
## **2: Ansel et al. - 2024 - PyTorch 2 Faster Machine Learning Through Dynamic Python Bytecode Transformation and Graph Compilation**
- Zunächst nennt der Autor verschiedene Eager und Graph Frameworks (`PyTorch`, `Jax` und `Caffe`, `Tensorflow`, `Theano` und `CNTK`)
- Eager Frameworks laufen auf dem Konzept der imperativen *define-by-run* Annäherung, wo das Kompilieren jedes Mal ausgeführt wird, wenn ein KI-Algorithmus ausgeführt wird
- Graph Frameworks laufen auf dem Konzept deklarativen *define-and-run* wo der Code vorerst grafisch abgebildet wird, bevor er ausgeführt wird
- in der Programmierung von Machine-Learning Algorithmen greifen die Programmierer eher auf Eager Modelle zurück (einfachere Verständlichkeit und leichteres Debuggen). **Problem:** Grafische Algorithmen sind performanter
- PyTorch ist ein Framework für maschinelles Lernen und läuft in der Python Umgebung. Bei Eager Operationen werden jedoch Start-Overhead Prozesse über viele Kernels verteilt ausgeführt. Durch den im Paper beschriebenen Python-JIT-Compiler PyDynamo, werden die Operationen zunächst aufgezeichnet und als Graph dargestellt. Dieser Graph kann dann über einen einzelnen Kernel ausgeführt werden --> Speicheroptimierung
- **Lazy Tensors:** Der Lazy Ansatz wird implementiert, indem die Operationen zunächst gesammelt werden und anschließend in einem Graphen aufgebaut werden. Durch die "Zusatzarbeit" sind die Overhead-Prozesse zunächst etwas aktiver. Der Graph wird dann als Ganzes kompiliert (z.B. durch `XLA`) und anschließend ausgeführt. Im Eager Mode wird der erste GPU-Kernel sofort gestartet, während Python weiterläuft — CPU und GPU arbeiten parallel. Bei Lazy wird zuerst der gesamte Graph gesammelt. Erst danach wird der erste Kernel gestartet. Dadurch entstehen Startverzögerungen und manchmal schlechtere CPU/GPU-Überlappung. Bei neuen Graph-Hashes ist erneutes Kompilieren erforderlich.
- PyTorch/XLA kombiniert Lazy Tensors mit TorchDynamo, wodurch die Overheads der Lazy Tensors versteckt werden, indem die Kompilierung nur einmal ausgeführt wird.
## **3: Associate Professor, Mehr Chand Mahajan DAV College for Women, Chandigarh, India und Arora - 2024 - Improving Performance of Data Science Applications in Python**
- Die Autorin stellt speicheroptimierende Methoden dar, welche sich bereits in der Python Library befinden
- Sie geht dabei insbesondere auf `Generatoren`, `Vektorisierung`, `Parallelismus`, `Caching` und `I/O-Handling` ein
- Durch das Yielding mithilfe von *Generatoren* lässt sich Arbeitsspeicher sparen, indem über theoretisch unbegrenzte Datenmengen iteriert werden können ohne Arbeitsspeicher zu belegen -->Lazy
- Durch die *NumPy* Library lassen sich Python-Lists in C++ Arrays abbilden. Hierdurch können Operationen am gesamten Array durchgeführt werden ohne durch die komplette Liste durch-zu-iterieren. Im Paper nimmt die Autorin die Vektormultiplikation als Beispiel:
```python
outer_product=np.outer(vektor1,vektor2) #numpy-Methode outer wird genutzt um vektor 1 mit vektor 2 zu multiplizieren
```
- Nebenbei erwähnt sie die *Profiling* Tools, durch die Rückschlüsse auf Memory, Laufzeiten und Arbeitsspeicher während Prozessausführungen gezogen werden können
<table>
	<thead>
		<tr>
			<th>Konzept</th>
			<th>Grundidee</th>
			<th>Parallelitätstyp</th>
			<th>Typische Nutzung</th>
			<th>Vorteile</th>
			<th>Nachteile</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td><strong>Threading</strong></td>
			<td>Mehrere Threads innerhalb eines Prozesses</td>
			<td>Nebenläufigkeit<br/>(in Python oft keine echte CPU-Parallelität wegen GIL)</td>
			<td>I/O-bound Tasks<br/>(Netzwerk, Dateien)</td>
			<td>Geringer Overhead,<br/>gemeinsamer Speicher</td>
			<td>Kein echter CPU-Speedup<br/>bei CPU-bound Tasks</td>
		</tr>
		<tr>
			<td><strong>Multiprocessing</strong></td>
			<td>Mehrere Prozesse statt Threads</td>
			<td>Echte Parallelität<br/>(mehrere CPU-Kerne)</td>
			<td>CPU-bound Berechnungen</td>
			<td>Umgeht GIL,<br/>echte Parallelverarbeitung</td>
			<td>Höherer Speicherbedarf,<br/>Prozessstart teurer</td>
		</tr>
		<tr>
			<td><strong>concurrent.features</strong></td>
			<td>High-Level API über Threading und Multiprocessing</td>
			<td>Abhängig vom Executor<br/>(Thread oder Process)</td>
			<td>Einfache parallele Task-Ausführung</td>
			<td>Sehr einfache Nutzung<br/>(ThreadPoolExecutor, ProcessPoolExecutor)</td>
			<td>Weniger Kontrolle über<br/>Low-Level-Details</td>
		</tr>
		<tr>
			<td><strong>asyncio</strong></td>
			<td>Asynchrones Event-Loop-Modell<br/>(cooperative multitasking)</td>
			<td>Nebenläufigkeit ohne Threads</td>
			<td>Sehr viele I/O-Operationen<br/>(Webserver, APIs)</td>
			<td>Sehr effizient für viele<br/>gleichzeitige I/O-Tasks</td>
			<td>Kein Vorteil für CPU-bound Tasks,<br/>anderes Programmiermodell (async/await)</td>
		</tr>
	</tbody>
</table>

- Bei *I/O-Operationen* wird mit folgenden Methoden gearbeitet, um die Leistung zu optimieren:
- -Buffering: Daten werden gesammelt statt byteweise gelesen
- -Batching: große Datenblöcke statt viele kleine Zugriffe
- -Memory Mapping: Datei direkt wie Speicher behandeln --> schneller Zugriff
- -Context Manager: verhindert offene Dateien und Ressourcenlecks
- *Caching* wird genutzt, damit nicht erneut gelesen/geschrieben und berechnet werden muss. Über `memoize` werden Funktionsresultate gespeichert. Datenbankabfragen werden zwischengespeichert und Trainingsdaten werden im RAM gehalten. Drei Clearingmethoden kommen hier häufig zum Einsatz:
- -FIFO: älteste Daten zuerst entfernen
- -LIFO: zuletzt gespeicherte zuerst entfernen
- -LRU: am längsten nicht genutzte Daten entfernen
## **4: Yang et al. - 2022 - Complex Python features in the wild**
- Yang et al. analysierte über 3 Millionen Dateien in Github, um zu überprüfen, welche komplexen Features "in the wild", also von freien Programmierern verwendet werden. Untersucht wurden dabei:
- dynamische Features (z. B. eval, Reflection)
- Decorators
- Context Manager (with)
- Generators
- dynamische Attributzugriffe (getattr, setattr)
- Der Grund dafür ist, dass `statische Analyse-tools`in Python nicht so stark vertreten ist wie in anderen Sprachen

<table>
	<thead>
		<tr>
			<th>Feature</th>
			<th>Frequency(files)/Nutzungshäufigkeit</th>
			<th>%</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td><strong>FNL (functional)</strong></td>
			<td>817.345</td>
			<td>26,415%</td>
		</tr>
		<tr>
			<td><strong>DYN (dynamic)</strong></td>
			<td>401.395</td>
			<td>12,973%</td>
		</tr>
		<tr>
			<td><strong>DEC (decorators)</strong></td>
			<td>386.134</td>
			<td>12,479%</td>
		</tr>
		<tr>
			<td><strong>WTH (with)</strong></td>
			<td>385.613</td>
			<td>12,463%</td>
		</tr>
        		<tr>
			<td><strong>ASC (async)</strong></td>
			<td>1.831</td>
			<td>0,059%</td>
		</tr>
	</tbody>
</table>

#### Die Autoren stellen beantworten eine der Kernfragen (RQ2) In What Ways Do Developers Use Complex Methods folgendermaßen:
#### **Decorators:**
- Meist für typische Aufgaben wie Logging, Caching, Testing oder Framework-Annotationen
- Selten stark verschachtelt oder dynamisch generiert.

#### **Context Manager (with)**
- Vor allem für Ressourcenmanagement (Dateien, Locks, Netzwerkverbindungen).
- Meist einfache Standardverwendung, nicht komplex verschachtelte Konstruktionen.

#### **Reflection / dynamische Attributzugriffe**
- Wird häufig in Framework- oder Bibliothekscode verwendet (z. B. ORMs, Serialisierung),
- aber in Anwendungslogik eher begrenzt und strukturiert.

#### **Dynamische Codeausführung (eval, exec)**
- Sehr selten und meist in klar abgegrenzten Spezialfällen.

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

- **6 - Was ist der Unterschied zwischen imperativem Programmieren und funktionalem Programmieren?:** Imperatives Programmieren beschreibt *wie* etwas zu tun ist — durch explizite Befehle, Zustandsänderungen und Kontrollfluss (Schleifen, Verzweigungen). Funktionales Programmieren beschreibt *was* berechnet werden soll — durch Funktionen als Bürger erster Klasse, Immutability und Vermeidung von Seiteneffekten. Imperativ ist prozedural ("tue Schritt 1, dann Schritt 2"), funktional ist deklarativ ("beschreibe das Ergebnis"). Funktionale Programme sind oft leichter zu testen, parallel auszuführen und zu verstehen, da sie weniger versteckte Abhängigkeiten durch Zustandsänderungen haben. Python unterstützt beide Paradigmen und ermöglicht funktionale Patterns durch Funktionen höherer Ordnung, Lambdas und Generatoren [3][7].

- **7 - NumPy Arrays:** NumPy Arrays sind speichereffiziente, typisierte Containerstrukturen, die in C implementiert sind und eine Vektorisierung von Operationen ermöglichen. Im Gegensatz zu Python Lists (heterogene, dynamische Größe, höherer Speicher-Overhead) speichern NumPy Arrays homogene Daten in einem zusammenhängenden Speicherblock. Dies ermöglicht es, dass Operationen auf dem gesamten Array auf C-Ebene ausgeführt werden, ohne dass Python durch jeden einzelnen Loop-Durchsatz gehen muss — das ist Broadcasting. Beispiel: `np.array([1, 2, 3]) * 2` führt die Multiplikation in C aus, während `[1, 2, 3] * 2` in Python Verkettung durchführt. Dadurch sind NumPy-Operationen oft 10–100× schneller für numerische Berechnungen. Zusätzlich unterstützen NumPy Arrays Multi-Dimensionalität und sind die Grundlage für wissenschaftliches Rechnen in Python (SciPy, Pandas, scikit-learn) [6][10].


## Was wir aus der Theorie auf unser Projekt übertragen können:
- **Kernel-Optimierung / JIT-Ansatz:** Konzepte wie Kernel-Fusion zeigen, dass das Zusammenfassen vieler kleiner Rechenoperationen in größere, optimierte Einheiten Start-Overhead reduziert. Für unser Projekt bedeutet das: rechenkritische Abschnitte sollten auf Bibliotheken/Compiler-Ebene (z. B. NumPy, Numba) zusammengefasst werden, statt viele kleine Python-Loops zu starten — dadurch sinkt der Python-Overhead und die Ausführung läuft schneller.
- **NumPy & Vektorisierung:** NumPy-Arrays erlauben homogene Daten im zusammenhängenden Speicher und Vektorisierung (Broadcasting). In `RabbitFarm` nutzen wir NumPy, um z. B. Analyse- und OLAP-artige Berechnungen (Ertragsaggregation, Bewässerungsbedarf) in C-optimierten Operationen auszuführen. Das reduziert CPU-Zeit und RAM-Overhead im Vergleich zu reinen Python-Lists.
- **Lazy Evaluation (Generatoren & `itertools`):** Die Theorie zu Lazy Execution übertragen wir direkt: Sensordaten werden als Stream/Gernerator modelliert, Transformationen mit `filter`, `map`, `islice` und `itertools` bleiben lazy, bis eine Materialisierung nötig ist. Das reduziert Peak-Memory und skaliert besser für Millionen von Messwerten.
- **Decorators:** sind Higher-Order-Functions und eignen sich als leichtgewichtige, wiederverwendbare Mechanismen, um Verhalten einzukapseln ohne Kerndefinitionen zu ändern. Für `RabbitFarm` schlagen wir folgende, pragmatische Decorator-Bausteine vor, die sich direkt in `sensors.py`, `services.py` und `models.py` einsetzen lassen:
    - **`@memoize` (Caching):** Für Funktionsaufrufe mit wiederkehrenden Eingaben (z. B. `Vegetable.is_fresh()`) reduziert Caching wiederholte Berechnungen.
    - **`@numba.njit` (JIT):** Kennzeichne rechenintensive Funktionen, die auf NumPy-Arrays arbeiten (z. B. Batch-Aggregationen), um native Geschwindigkeit zu erreichen.
    - **`@batch_items` (Batching-Decorator):** Wandelt Generator-Elemente in Batches um, damit Vektorisierung mit NumPy möglich wird. Ein Batch-Decorator erlaubt einfache Umstellung von Item- zu Batch-Verarbeitung ohne Pipeline-Änderungen.
    - **`@prefetch(n)` (Prefetch/Concurrency):** Puffert Generatoren in einem Hintergrundthread/Queue, um IO-Latenzen zu überbrücken und bessere CPU/GPU-Overlap zu erzielen (nützlich bei sensordaten mit IO- oder Netzwerkbindung).
    - **`@timeit` / `@profile` (Benchmarking):** Leichtgewichtige Timing-Wrapper für `benchmark_eager` / `benchmark_lazy` zur kontinuierlichen Überwachung von Performance-Regressions.
- **Konkrete Maßnahmen im Projekt:**
	- Sensor-Streams als Generatoren realisieren (`sensors.py`) und Pipelines mit `itertools` bauen.
	- Rechenintensive Aggregationen mit NumPy vektorisieren oder optional mit Numba JIT-kompilieren.
	- Benchmarks und Memory-Profiling (z. B. `tracemalloc`) in unserem Notebook dokumentieren, siehe [src/student_projects/g03/static/notebooks/layz_vs_eager.ipynb](src/student_projects/g03/static/notebooks/layz_vs_eager.ipynb).
	- Design- und Umsetzungsentscheidungen sind im Konzeptionsplan beschrieben: [src/student_projects/g03/docs/konzeptionsplan.md](src/student_projects/g03/docs/konzeptionsplan.md).

Diese Übertragungen sind bereits in Teilen implementiert (Generator-basierte Sensordaten, Lazy-/Eager-Benchmarks im Notebook sowie Hinweise auf den Einsatz von NumPy/Numba). Weitere Optimierungen können durch gezielte Profilerläufe und schrittweises Vektorisieren/Refactoring erfolgen.

#### Zusätzliche Literatur

1. T. Akidau et al., "The Dataflow Model", Google Research / O'Reilly (Streaming Systems), 2015. https://research.google/pubs/pub38137/
2. Dean, J. & Ghemawat, S., "MapReduce: Simplified Data Processing on Large Clusters", OSDI 2004. https://research.google/pubs/pub62/
3. J. Hughes, "Why Functional Programming Matters", 1984. [https://www.cs.kent.ac.uk/people/staff/dat/marc/FP/hughes.pdf]
4. S. Peyton Jones, "The Implementation of Functional Programming Languages", 1992.
5. S. K. Lam, A. Pitrou, & S. Seibert, "Numba: A LLVM-based Python JIT compiler", 2015. https://arxiv.org/abs/1506.01356
6. NumPy documentation — Vectorized operations and broadcasting. https://numpy.org/doc/
7. PEP 318 — Decorators for Functions and Methods. https://peps.python.org/pep-0318/
8. Python `itertools` documentation. https://docs.python.org/3/library/itertools.html
9. PEP 255 / PEP 342 — Generators and coroutines. https://peps.python.org/

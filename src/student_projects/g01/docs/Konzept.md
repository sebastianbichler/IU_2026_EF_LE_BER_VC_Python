# Konzept – FoxExpress 🚚💨

## Leitfrage ❓

**„Leistungsanalyse von JIT-Kompilierungsstrategien in dynamischen Sprachen:  
Ein Vergleich zwischen methodenbasierter (Numba) und tracingbasierter (PyPy) JIT-Kompilierung bei algorithmisch geprägten Workloads.“**

---

## Erläuterung & Problemstellung 📌

Ziel des Projekts **„FoxExpress“** ist die Entwicklung einer vereinfachten Logistik-Software, mit der Lieferungen verwaltet und kürzeste Lieferwege berechnet werden können. 

Auf dieser Grundlage wird die Laufzeit identischer Routing-Algorithmen (Dijkstra-Algorithmus) unter verschiedenen Python-Ausführungsumgebungen systematisch verglichen:

- **CPython** (Referenz-Interpreter)
- **PyPy** (Tracing-basierte JIT-Kompilierung)
- **Numba** (Methodenbasierte JIT-Kompilierung)

### Wissenschaftlicher Hintergrund

Dynamisch typisierte und interpretierte Sprachen wie CPython bieten eine hohe Entwicklerproduktivität, weisen jedoch bei rechenintensiven algorithmischen Workloads messbare Performance-Nachteile auf. In der Literatur werden insbesondere wiederholte Boxing- und Unboxing-Operationen sowie dynamische Funktionsauflösung (Late Binding) als relevante Quellen interpretativen Overheads beschrieben (Barany, 2014; Tuominen, 2025).

Darüber hinaus führen mehrstufige Indirektionen beim Zugriff auf Python-Objekte zu zusätzlichem Laufzeitaufwand, insbesondere bei schleifenbasierten numerischen Operationen (Lam, Pitrou, & Seibert, 2015). Diese Eigenschaften sind insbesondere bei graphbasierten Algorithmen wie Dijkstra relevant, da sie stark iterativ geprägt sind.

Zur Reduktion dieses Overheads kommen Just-in-Time-Kompilierungsstrategien (JIT) zum Einsatz. JIT-Kompilierung bezeichnet die Übersetzung von Code zur Laufzeit in maschinennahen Code, wodurch interpretative Zwischenschritte reduziert werden können (Genchev et al., 2025).

In diesem Projekt werden zwei unterschiedliche JIT-Ansätze untersucht:

- **Tracing-basierte JIT-Kompilierung (PyPy):**  
  Häufig ausgeführte Codepfade („Hot Paths“) werden während der Laufzeit identifiziert und optimiert.

- **Methodenbasierte JIT-Kompilierung (Numba):**  
  Einzelne annotierte Funktionen werden mittels LLVM in optimierten Maschinencode übersetzt (Lam et al., 2015).

Ziel ist es, die Effizienz dieser beiden Strategien im Kontext algorithmischer Workloads systematisch zu vergleichen.

---

## Systemaufbau 🧩

Konzeptionell besteht **„FoxExpress“** aus:

- einem Modul zur Lieferverwaltung  
- einem Routing-Modul zur Berechnung kürzester Wege mittels **Dijkstra-Algorithmus**  
- einer grafischen Benutzeroberfläche (realisiert mit **Streamlit**)  

### Architektonische Entscheidung

Das System folgt einem modularen Design, in dem rechenintensive Routing-Operationen strikt von der Benutzeroberfläche getrennt sind. Ziel dieser Trennung ist es, algorithmische Berechnungen isoliert auszuführen und deren Laufzeitverhalten unabhängig von GUI-Interaktionen zu messen.

Für den Vergleich mit PyPy wird ein separater Interpreterprozess über die Standardbibliothek `subprocess` gestartet. Dadurch wird sichergestellt, dass jede Ausführungsumgebung unter klar getrennten und kontrollierten Laufzeitbedingungen evaluiert wird. Diese Trennung dient der methodischen Konsistenz und Vergleichbarkeit der Messergebnisse.

---

## Methodik ⏱️

Die Evaluation erfolgt in Form eines experimentellen Leistungsvergleichs identischer algorithmischer Workloads.

### Benchmark-Design

- Identische Eingabedaten für alle Ausführungsumgebungen
- Wiederholte Durchführung der Berechnungen
- Messung der reinen Ausführungszeit
- Vergleich aggregierter Laufzeitwerte

Zur Sicherstellung reproduzierbarer Ergebnisse werden alle Tests unter identischen Hardware- und Softwarebedingungen durchgeführt.

Die Ergebnisse werden statistisch ausgewertet und in der grafischen Oberfläche vergleichend dargestellt.

---

## Technologien & Entscheidungen 🛠️

Zur Umsetzung der Anforderungen wurden folgende technische Entscheidungen getroffen:

### NumPy

NumPy dient als primäre Datenstruktur für die interne Repräsentation des Graphen.

**Begründung:**  
Numba fokussiert sich auf ein Python-Subset, das stark auf `ndarray`-Strukturen und numerischen Skalaren basiert (Lam et al., 2015). Durch die homogene Speicherstruktur von NumPy-Arrays kann Numba direkten Zugriff auf Datenpuffer ermöglichen und Indirektionskosten reduzieren. Standard-Python-Listen bieten diese Eigenschaften nicht.

---

### Numba (JIT)

Numba wird zur methodenbasierten Beschleunigung des Routing-Algorithmus eingesetzt.

**Begründung:**  
Numba analysiert CPython-Bytecode, führt Typinferenz durch und generiert daraus LLVM Intermediate Representation (LLVM IR), die anschließend in Maschinencode übersetzt wird (Lam et al., 2015). Im sogenannten „nopython mode“ erfolgt die Ausführung ohne Rückgriff auf die Python C-API, wodurch interpretativer Overhead reduziert werden kann.

---

### PyPy

PyPy wird als tracingbasierter JIT-Interpreter verwendet.

**Begründung:**  
Tracing-basierte JIT-Systeme identifizieren zur Laufzeit häufig ausgeführte Codepfade und optimieren diese dynamisch. Dieser Ansatz unterscheidet sich grundlegend von der funktionsbasierten Kompilierung durch Numba und erlaubt einen konzeptionell unterschiedlichen Optimierungsansatz.

---

### Subprocess (Standardbibliothek)

Der Vergleich mit PyPy erfolgt durch den Start eines separaten Interpreterprozesses.

**Begründung:**  
Die Prozessisolierung stellt sicher, dass jede Laufzeitumgebung unabhängig initialisiert wird. Dadurch wird eine konsistente Vergleichsbasis geschaffen und unbeabsichtigte Interferenzen zwischen den Laufzeitumgebungen vermieden.

---

### NetworkX

NetworkX wird zur logischen Modellierung und Generierung der Graphen verwendet.

**Begründung:**  
Die Bibliothek ermöglicht eine strukturierte Erstellung komplexer Testnetzwerke, bevor diese für die eigentliche Berechnung in eine Numba-kompatible Datenstruktur überführt werden.

---

### Matplotlib / Streamlit Native Charts

Zur Visualisierung der Benchmark-Ergebnisse werden integrierte Diagrammwerkzeuge verwendet.

**Begründung:**  
Die gewählten Werkzeuge ermöglichen eine hinreichend präzise Darstellung der Messergebnisse bei gleichzeitig reduzierter technischer Komplexität.

---

## Literaturverzeichnis

Barany, G. (2014). *Analysis of performance overhead in CPython interpreter*.  

Genchev, E., Rangelov, D., Waanders, K., & Waanders, S. (2025). Utilizing JIT Python runtime and parameter optimization for CPU-based Gaussian Splatting thumbnailer. *Array, 28*, 100611.  

Lam, S. K., Pitrou, A., & Seibert, S. (2015). Numba: A LLVM-based Python JIT compiler. In *Proceedings of the Second Workshop on the LLVM Compiler Infrastructure in HPC* (pp. 1–6). ACM.  

Tuominen, J. (2025). *JIT Compiling CPython with Numba & JAX* (Bachelor’s Thesis). Tampere University.

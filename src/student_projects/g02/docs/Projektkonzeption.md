# 📄 Projekt-Konzeption: Squirrel Secret Stash

| Metadaten | Details |
| :--- | :--- |
| **Projekt** | Squirrel Secret Stash |
| **Modul** | DLBDSIPWP01 – Python & Scientific Computing |
| **Thema** | Vectorization & SIMD mit NumPy |
| **Status** | Konzeptionsphase |
| **Datum** | 20.01.2025 |

---

## 1. Einleitung und Zweck der Anwendung

Das Projektziel ist die Entwicklung eines **High-Performance-Vorratssystems** für "Sammy Squirrel", ein Eichhörnchen mit Ambitionen zum Nuss-Tycoon, das ein Netzwerk von über **1.000.000 Verstecken** verwalten muss.

Anders als bei herkömmlichen Lager-Apps, die einzelne Objekte verwalten, ist der Zweck dieser Anwendung die **Maximierung der Datenverarbeitungsgeschwindigkeit**. Die Software soll Sammy dabei unterstützen, Millionen von Datenpunkten (Nüsse, Orte, Haltbarkeiten) in Millisekunden zu analysieren, um den harten Winter zu überleben.

Die Applikation dient als Verwaltungszentrale für:
* **Massendaten-Kartierung:** Geografische Verwaltung von Millionen Verstecken.
* **Finanz-Simulation:** Zinseszins-Berechnungen für an Nachbarn verliehene Nüsse.
* **Risiko-Analyse:** Überlebensprognosen basierend auf Kälte und Kalorienvorrat.
* **Sicherheits-Audit:** Erkennung von Diebstählen durch Musteranalyse im Bestand.

## 2. Wissenschaftlicher Fokus

Im Rahmen des Moduls wird ein spezifischer wissenschaftlicher Schwerpunkt auf **High Performance Computing** gelegt.

* **Topic:** Vectorization & SIMD mit NumPy.
* **Konkrete Umsetzung:** Einsatz von **Array-orientierter Programmierung** statt klassischer Kontrollstrukturen (Schleifen). Nutzung von `numpy`, um CPU-Instruktionen (SIMD – *Single Instruction, Multiple Data*) direkt anzusprechen.
* **Ziel:** Die Berechnungen (z.B. Zinseszins für 1 Mio. Datensätze) müssen signifikant schneller sein als in reinem Python.
* **Memory Management:** Anstatt Millionen einzelner Objekte (Overhead) zu erzeugen, wird **Data Oriented Design** (*Structure of Arrays*) genutzt, um Speicher-Lokalität (Cache Hits) zu optimieren.

## 3. Funktionale Anforderungen (Functional Requirements)

Die Requirements werden mit englischen IDs definiert, um die direkte Zuordnung im Code (als Kommentare/Docstrings) zu ermöglichen.

### 3.1 Versteck-Kartierung (Mapping Core)
Das System muss die Geodaten und Attribute massenhaft verwalten.
* **REQ-FUN-001 (Stash Generation):** Das System muss synthetische Daten für $N$ Verstecke (Standard: 1.000.000) generieren (Koordinaten $x,y$, Baumart, Erdtiefe).
* **REQ-FUN-002 (Inventory Tracking):** Jedes Versteck muss Bestände für Haselnüsse, Walnüsse und Eicheln inkl. Haltbarkeitsdatum führen.

### 3.2 Finanz-Mathematik (Compound Interest)
Sammy verleiht Nüsse und erwartet Rendite.
* **REQ-FUN-003 (Vectorized Interest):** Berechnung des Endkapitals nach der Formel $A = P(1+r)^t$.
    * *Constraint:* Die Berechnung muss für alle Verstecke *gleichzeitig* (vektorisiert) erfolgen, nicht iterativ.

### 3.3 Winter-Prognose (Survival Analytics)
Reicht der Vorrat bei aktueller Kälte?
* **REQ-FUN-004 (Calorie Broadcasting):** Das System berechnet den Gesamtkalorienwert pro Versteck und vergleicht ihn mittels Broadcasting mit dem temperaturabhängigen Kalorienbedarf des Winters.
* **REQ-FUN-005 (Critical Alert):** Verstecke, die den Winter nicht überstehen, müssen als Boolean-Maske identifiziert und ausgegeben werden.

### 3.4 Diebstahl-Erkennung (Anomaly Detection)
Vergleich von Soll- und Ist-Zustand.
* **REQ-FUN-006 (Theft Scanning):** Das System vergleicht `expected_inventory` mit `current_inventory`. Differenzen müssen ohne `if`-Abfragen, sondern mittels Matrix-Subtraktion und Filterung erkannt werden.

### 3.5 Benutzeroberfläche (UI & GUI)
Die Interaktion mit dem System.
* **REQ-FUN-007 (CLI Control):** Das Hauptinterface ist eine Kommandozeile zur Steuerung der Simulationen und Ausgabe von Statistiken.
* **REQ-FUN-008 (Dashboard GUI – *Optional*):** Eine grafische Oberfläche (z.B. mittels `tkinter` oder `matplotlib` Integration), die:
    * Die Karte der Verstecke visualisiert (Scatterplot/Heatmap).
    * Buttons zum Starten der Analysen bereitstellt.
    * *Hinweis:* Die GUI dient primär der Visualisierung; die Rechenlogik bleibt strikt im NumPy-Backend getrennt.

## 4. Nicht-Funktionale Anforderungen (NFR)

Diese Anforderungen definieren die Qualität und technische Umgebung des Projekts.

* **REQ-NFR-001 (Language):** Der gesamte Quellcode (Variablennamen, Funktionen, Klassen) sowie Kommentare müssen in **Englisch** verfasst sein.
* **REQ-NFR-002 (Documentation):** Der Code muss mittels Docstrings und einer README.md dokumentiert sein.
* **REQ-NFR-003 (Testing):** Es müssen Unit-Tests (für mathematische Korrektheit) und mindestens 3 Integrationstests (für den gesamten Workflow) implementiert werden.
* **REQ-NFR-004 (Performance Benchmark):** Die Anwendung muss einen Vergleichsmodus besitzen, der die Ausführungszeit von "Native Python Loops" vs. "NumPy Vectorization" misst und den Speedup-Faktor ausgibt.
* **REQ-NFR-005 (CI/CD):** Der Build- und Testprozess muss über eine dokumentierte Pipeline-Logik (Simulation oder `requirements.txt` + Test-Skript) nachvollziehbar sein.

## 5. System-Akteure (Use Case Analyse)

### Akteur 1: Sammy Squirrel (User/Manager)
* Initialisiert das Universum (Anzahl der Verstecke).
* Startet Finanz- und Wetter-Simulationen.
* Liest Performance-Berichte (Wie viel Zeit wurde durch NumPy gespart?).
* Betrachtet die Karte der gefährdeten Verstecke (via CLI-Stats oder optionaler GUI).

### Akteur 2: The Winter (System Environment)
* Stellt Anforderungen an den Kalorienverbrauch (Simulierter Parameter).
* Beeinflusst die Haltbarkeit der Vorräte.

### Akteur 3: The Jay (Eichelhäher – Störfaktor)
* Verursacht zufällige Daten-Abweichungen (Diebstahl), die vom System erkannt werden müssen.

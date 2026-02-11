# Sammys Secret Stash - High-Performance Nut Management System

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Framework](https://img.shields.io/badge/Framework-Flask-green)
![Science](https://img.shields.io/badge/Library-NumPy-orange)
![Build](https://img.shields.io/badge/Build-Passing-brightgreen)

**Sammys Secret Stash** ist eine wissenschaftliche Webanwendung zur Verwaltung und Analyse von Vorräten unter extremen Witterungsbedingungen. Das Projekt demonstriert die signifikanten Performance-Vorteile von **Vektorisierung (SIMD)** gegenüber iterativen Verfahren (SISD) in Python.

---

## Inhaltsverzeichnis
1. [Projektbeschreibung](#-projektbeschreibung)
2. [Wissenschaftlicher Hintergrund](#-wissenschaftlicher-hintergrund)
3. [Software-Architektur](#-software-architektur)
4. [Features & Requirements](#-features--requirements)
5. [Installation & Start](#-installation--start)
6. [Testing & CI/CD](#-testing--cicd)

---

## Projektbeschreibung

Das Ziel dieses Projekts ist die Entwicklung einer Softwarelösung, die einem Eichhörnchen (Sammy) hilft, seinen Nussvorrat über den Winter zu bringen. Dabei müssen komplexe meteorologische und physikalische Faktoren berechnet werden:

* **Thermische Simulation:** Berechnung des Kalorienbedarfs basierend auf Bodentemperatur (-5°C) und Isolationstiefe.
* **Risiko-Analyse:** Prognose von Diebstählen durch Eichelhäher bei zu flacher Grabtiefe (< 10cm).
* **Finanz-Mathematik:** Zinseszins-Berechnung (Vermehrung der Nüsse über 5 Jahre).

Die Anwendung bietet ein **Echtzeit-Dashboard** zur Visualisierung und einen **integrierten Benchmark**, der die Berechnungsgeschwindigkeit bei steigender Datenmenge (Big Data) misst.

---

## Wissenschaftlicher Hintergrund

Ein Kernaspekt dieser Arbeit ist der Vergleich zweier Berechnungsparadigmen:

### 1. SISD (Single Instruction, Single Data) - Python
Der klassische Ansatz mittels `for`-Schleifen.
* **Funktionsweise:** Jedes Versteck wird einzeln aus dem Speicher geladen, interpretiert und berechnet.
* **Nachteil:** Hoher Overhead durch den Python-Interpreter und fehlende Cache-Lokalität.

### 2. SIMD (Single Instruction, Multiple Data) - NumPy
Der optimierte Ansatz mittels Vektorisierung.
* **Funktionsweise:** Die CPU führt eine Operation (z.B. Multiplikation) auf einem ganzen Speicherblock (Array) gleichzeitig aus.
* **Besonderheit:** Nutzung von **Maskierung** (`np.where`), um bedingte Logik (Branching) ohne langsame `if/else`-Verzweigungen zu lösen.

**Ergebnis:** Die Anwendung beweist, dass SIMD-Algorithmen bei großen Datensätzen (> 10.000 Einträge) um Faktoren (ca. 50x - 100x) schneller sind.

---

## Software-Architektur

Das Projekt folgt strikt dem **MVC-Pattern (Model-View-Controller)**, um eine saubere Trennung der Verantwortlichkeiten zu gewährleisten.

| Layer | Komponente | Beschreibung |
| :--- | :--- | :--- |
| **Model** | `src/model.py` | Datenstruktur `NutStash` als Python Dataclass. |
| **Persistence** | `src/manager.py` | DAO-Pattern zur Speicherung in `data/database.json`. |
| **Logic** | `src/analytics.py` | Rechenkern für Simulationen & Benchmarks (NumPy). |
| **Controller** | `src/app.py` | Flask-Server, Routing und Orchestrierung. |
| **View** | `templates/*.html` | Frontend-Darstellung. |
| **Visualization** | `src/visualizer.py` | Server-Side Rendering von Charts mit Matplotlib (Agg). |

---

##  Features & Requirements

### Funktionale Anforderungen
* **F01 Datenerfassung:** Hinzufügen von Verstecken (Art, Menge, Tiefe, Koordinaten).
* **F02 Persistenz:** Dauerhafte Speicherung in einer JSON-Datenbank.
* **F03 Simulation:** "Mass-Generator" für synthetische Testdaten (+1000 Verstecke).
* **F04 Analyse:** Berechnung von Soll/Ist-Beständen und Überlebenswahrscheinlichkeit.

### Nicht-Funktionale Anforderungen
* **N01 Performance:** Nachweis der Effizienzsteigerung durch NumPy.
* **N02 Usability:** Intuitive Web-Oberfläche mit visueller Aufbereitung (Charts, Maps).
* **N03 Stabilität:** Thread-Safe Visualisierung und robustes Error-Handling beim Laden von Daten.

---

## Installation & Start

### Voraussetzungen
* Python 3.9 oder höher
* pip (Python Package Installer)

### Schritt-für-Schritt

1.  **Repository klonen / entpacken:**
    Wechseln Sie in das Projektverzeichnis `g02`.

2.  **Abhängigkeiten installieren:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Anwendung starten:**
    ```bash
    python -m src.app
    ```

4.  **Im Browser öffnen:**
    Navigieren Sie zu [http://127.0.0.1:5000](http://127.0.0.1:5000).

---

## Testing & CI/CD

Das Projekt verfügt über eine automatisierte Test-Suite, um die Korrektheit der Algorithmen sicherzustellen.

**Tests ausführen:**
```bash
python -m unittest discover tests

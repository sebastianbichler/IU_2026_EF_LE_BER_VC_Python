### DLBDSIPWP01 - Einführung in die Programmierung mit Python (Projekt)

---

# Project Abschlussbericht: Elephant Memory Cloud

## 1. Einleitung und Vision

### 1.1 Projektvision und Ziele

Die *Elephant Memory Cloud* ist ein Python-basierter Prototyp für ein „digitales Gedächtnis“ von **Ella Elefant**. Fachlich wird ein Archiv modelliert, das Ereignisse (Jahr, Ort/Wasserstelle, beteiligte Elefanten/Herden) sowie genealogische Beziehungen (Eltern/Kinder, Herd-Zugehörigkeit) abbildet.

Das Projektziel ist **nicht** ein produktionsreifes Cloud-System, sondern ein didaktisch nachvollziehbarer Demonstrator, der:

- komplexe Objektbeziehungen in einem Domain Model modelliert,
- absichtlich **zirkuläre Referenzen** (Parent ↔ Child, Herd ↔ Member) erzeugt,
- und deren Auswirkungen auf Speicherbereinigung in Python sichtbar macht.

Die Anwendung stellt dafür ein Streamlit-Dashboard bereit (Daten generieren, suchen, Genealogie visualisieren) und ermöglicht eine reproduzierbare GC-Demonstration über UI-Schritte.

### 1.2 Wissenschaftliche Herausforderung / Python-Spezifischer Aspekt

Der wissenschaftliche Schwerpunkt liegt auf **Memory Management in Python**, konkret:

- **Reference Counting** als primärer Mechanismus zur Speicherfreigabe,
- **zyklische Garbage Collection** als Ergänzung, um unreachable Zyklen („Dead Islands“) zu bereinigen.

Relevanz: In objektorientierten Python-Programmen entstehen Zyklen leicht (z. B. bidirektionale Beziehungen). Diese führen dazu, dass reine Referenzzählung Objekte nicht freigibt, obwohl sie aus Sicht der Anwendung nicht mehr erreichbar sind.

Analogie/Story: Die Savannen-Domäne (Elefanten, Herden, Wasserstellen, Ereignisse) wird als „natürliche“ Quelle komplexer Objektgraphen genutzt. Das Projekt erzeugt bewusst Zyklen im „Stammbaum“-Kontext, um das Verhalten von Python bei der Speicherbereinigung anschaulich zu demonstrieren.

### 1.3 Arbeitshypothese

Die Konzeptionsphase definiert zwei überprüfbare Hypothesen:

- **H1:** Ohne zyklische GC steigt die Anzahl nicht freigegebener Objekte mit der Größe des zyklischen Objektgraphen.
- **H2:** Mit aktivierter GC werden zyklische Referenzen nach Entfernen externer Referenzen aufgelöst (Objekte werden freigegeben).

Untersucht wird dies an Domain-Entities wie `Elephant` (Parent/Child-Zyklus) und `Herd` (Herd ↔ Member), die absichtlich starke bidirektionale Referenzen bilden.

---

## 2. Requirements Engineering

### 2.1 Kontextdiagramm

t.b.d.

### 2.2 Funktionale Anforderungen

Die folgenden funktionalen Anforderungen wurden in der Konzeptionsphase festgelegt (MoSCoW: **[m] must**, **[s] should**, **[c] could**) und in der Umsetzungsphase gegen den Implementationsstand abgeglichen.

- **REQ-01 (F01)** – Ereignisse erfassen: Ereignisse mit Jahr, Ort/Wasserstelle, beteiligten Elefanten/Herden speichern.
- **REQ-02 (F02) [m]** – Ereignisse indexieren: effiziente Suche nach Jahr und Ort.
- **REQ-03 (F03) [m]** – Elefanten modellieren: Elefanten als Objekte abbilden.
- **REQ-04 (F04) [m]** – Verwandtschaft modellieren: Eltern-/Kind- und Herdbeziehungen.
- **REQ-05 (F05) [m]** – Zirkuläre Referenzen erzeugen: absichtliche Zyklen im Objektgraphen.
- **REQ-06 (F06) [s]** – Stammbäume visualisieren: genealogische Graphen darstellen.
- **REQ-07 (F07) [s]** – Wasserstellen-Suche: Suche auf Basis historischer Ereignisse/Koordinaten.
- **REQ-08 (F08) [c]** – Erinnerungs-Bot: zeitbasierte Erinnerungen (z. B. Jubiläen von Migrationen).
- **REQ-09 (F09) [m]** – Speicherverhalten messen: RAM/Objektanzahl während der Laufzeit erfassen.
- **REQ-10 (F10) [m]** – GC-Vergleich ermöglichen: identische Szenarien mit GC aktiv/deaktiviert demonstrieren.

### 2.3 Nicht-funktionale Anforderungen (Qualitätsanforderungen)

Die nicht-funktionalen Anforderungen wurden in der Konzeptionsphase wie folgt definiert:

- **NFR-01 (NF01) [s] – Nachvollziehbarkeit:** didaktisch nachvollziehbarer, dokumentierter Code.
- **NFR-02 (NF02) [m] – Reproduzierbarkeit:** Experimente als reproduzierbare Abfolge dokumentieren.
- **NFR-03 (NF03) [m] – Messbarkeit:** Speicherverhalten quantitativ erfassen.
- **NFR-04 (NF04) [s] – Begrenzter Scope:** keine DB/Cloud-Architektur, keine KI/ML.
- **NFR-05 (NF05) [m] – Performance-Abgrenzung:** Rendering-Limits des Browsers sind nicht als Memory-Problem zu interpretieren.
- **NFR-06 (NF06) [m] – Plattformunabhängigkeit:** lokal auf Standard-Rechnern lauffähig.

### 2.4 Use-Case Modellierung

Die Use-Cases gliedern sich in eine funktionale Nutzungsebene und eine Forschungsebene.

- Diagramm: [concept_phase/diagrams/UseCaseDiagram.md](concept_phase/diagrams/UseCaseDiagram.md)

**Primäre Akteure**

- *Ella Elephant (End User):* sucht und visualisiert Ereignisse und Genealogie.
- *Researcher/Admin:* erzeugt Zyklen, misst Memory/GC-Effekte und validiert Hypothesen.

**Kern-Use-Cases (Auszug)**

- Ereignisse indexieren & suchen (REQ-01/02)
- Stammbaum/Genealogie visualisieren (REQ-04/06)
- Zyklen erzeugen und „orphaned cycles“ demonstrieren (REQ-05/10)
- Speicher messen und Effekte vergleichbar machen (REQ-09/10)

---

## 3. Architektur und Tech-Stack

### 3.1 Auswahl der Plattform (Begründung)

Als Plattform wurde **Streamlit** gewählt, um die Kombination aus (a) interaktiver Bedienung, (b) Visualisierung und (c) reproduzierbaren Demo-Schritten in einer einzigen Oberfläche umzusetzen.

- UI-Einstiegspunkt: [app.py](../app.py)

Begründung (aus Projektzielen abgeleitet):

- schnelle Iteration für einen didaktischen Prototyp (kein Overhead einer Desktop-GUI)
- direkte Visualisierung von Metriken (Memory, Objektanzahl, Beziehungen) und Suchergebnissen
- geeignet, um den GC-Vergleich als klaren, wiederholbaren Ablauf zu demonstrieren

### 3.2 Modularer Kern und Open-Closed Principle

Die Kernlogik ist in UI-unabhängige Module ausgelagert und wird durch das Streamlit-Dashboard lediglich orchestriert:

- **Domain Models:** [models/](../models/) (u. a. [models/elephant.py](../models/elephant.py), [models/herd.py](../models/herd.py), [models/event.py](../models/event.py), [models/water_source.py](../models/water_source.py))
- **In-Memory Store:** [memory/store.py](../memory/store.py) (zentraler Objektcontainer; bewusst zyklusfreundlich)
- **Services:**
	- Datengenerierung: [data/generator.py](../data/generator.py)
	- Suche/Indexing: [search/engine.py](../search/engine.py)
	- Monitoring: [memory/monitor.py](../memory/monitor.py)

Damit bleiben Domain-Objekte und Services unabhängig von Streamlit nutzbar (z. B. für Tests), während die UI lediglich die Bedienlogik, Visualisierung und Demo-Schritte kapselt.

### 3.3 Technologie-Stack

**Implementierter Stack (siehe [requirements.txt](../requirements.txt))**

- **streamlit:** Web-UI (Dashboard, Tabs, Interaktion)
- **plotly:** interaktive Visualisierung (Charts/Genealogie-Auswertungen)
- **psutil:** Prozessspeicher (RSS) als Monitoring-Metrik
- **pytest:** Unit-Tests

**Konzeptionsphase (thematisch/Standardbibliothek, Auszug)**

- `gc`, `sys`, `datetime` als Grundlage für Experimente/Introspektion und Domain-Timestamps

t.b.d. — Weakref-Ansatz: im Verlauf der Projektumsetzung wieder entfernt; bitte noch einmal prüfen.

---

## 4. Design und Modellierung (Die "Story")

### 4.1 Domänenmodell und UML-Klassendiagramm

Die Story wird durch ein Domain Model umgesetzt, das absichtlich komplexe Beziehungen abbildet:

- **Elephant:** Eltern/Kind-Beziehungen als bidirektionale Referenzen (Zyklen)
- **Herd:** Mitgliederliste plus Rückreferenz vom `Elephant` auf `Herd` (Zyklus)
- **Event / EventType:** verbindet Elefanten/Herden mit Zeit und Ort
- **WaterSource:** Wasserstellen mit historischer Verfügbarkeit und Besuchshistorie

Diagramme:

- UML-Klassendiagramm: [dev_phase/diagrams/ClassDiagram.md](dev_phase/diagrams/ClassDiagram.md)
- Objekt-/Hypothesen-Diagramme (Dead Island / Resolution): [concept_phase/diagrams/ObjectDiagram.md](concept_phase/diagrams/ObjectDiagram.md)

### 4.2 Verhaltensdiagramme: Activity- & State-Diagram

t.b.d.

### 4.3 Interaktionsdiagramm: Sequence-Diagram

Die Abfolge der Speicherbereinigung in Python wird über Sequence-Diagramme dokumentiert:

- Deterministische Bereinigung ohne Zyklus (Reference Counting)
- Leak-ähnlicher Zustand bei Zyklen (H1)
- Eingriff der zyklischen GC (H2)

Diagramm: [dev_phase/diagrams/SequenceDiagrams.md](dev_phase/diagrams/SequenceDiagrams.md)

### 4.4 Design Patterns und Prinzipien

Die Codebasis nutzt gezielt wenige, leichtgewichtige Strukturmuster, passend zum didaktischen Scope:

- **Domain Model (OO):** reichhaltige Objekte mit Beziehungen in [models/](../models/)
- **Repository-ähnlicher In-Memory Store:** `MemoryStore` kapselt das „Persistenz“-Äquivalent im RAM ([memory/store.py](../memory/store.py))
- **Singleton-Store:** globaler Store über `get_store()` für einen konsistenten Objektgraphen innerhalb der App
- **Service Layer:** `DataGenerator`, `ElephantSearchEngine`, `MemoryMonitor` als Services mit klarer Verantwortung
- **Indexing als Performance-Technik:** Dictionary-Indizes für schnelle Abfragen (O(1)-Lookups) in [search/engine.py](../search/engine.py)

---

## 5. Wissenschaftliche Problemstellung (Jupyter Notebook)

### 5.1 Methodik der Untersuchung

t.b.d.

### 5.2 Analyse und Demonstration

t.b.d.

---

## 6. Implementierung und Qualitätssicherung

### 6.1 Code-Struktur und Dokumentation

Die Implementierung ist modular aufgebaut (UI, Domain Models, Services) und nutzt überwiegend englische Bezeichner in Code und Docstrings.

- UI/Orchestrierung: [app.py](../app.py)
- Domain Models: [models/](../models/)
- Services: [data/generator.py](../data/generator.py), [search/engine.py](../search/engine.py), [memory/monitor.py](../memory/monitor.py)
- Storage: [memory/store.py](../memory/store.py)

### 6.2 Test-Konzept: Unit-Tests

Es existieren zwei fokussierte Unit-Tests, die Kernlogik unabhängig von Streamlit absichern:

- [tests/test_search_and_store.py](../tests/test_search_and_store.py)
	- `test_search_engine_indexes_and_queries()`: prüft Indexing & Queries der `ElephantSearchEngine` (Jahr, Elefant, Location-Grid)
	- `test_memory_store_clear_and_cleanup_breaks_relationships()`: prüft, dass `MemoryStore.clear_and_cleanup()` Beziehungen bricht und Tracking bereinigt (relevant für reproduzierbare Cleanup-Szenarien)

### 6.3 Integration-Tests und Traceability

t.b.d.

### 6.4 CI-Pipeline

t.b.d.

---

## 7. Software-Qualität nach [ISO 25010](https://iso25000.com/index.php/en/iso-25000-standards/iso-25010)

t.b.d.

---

## 8. Projektabschluss und Reflexion

### 8.1 Methodik und Anpassungen

t.b.d.

### 8.2 Selbstreflexion

#### Arbeitsprozess

t.b.d.

#### Einsatz von KI

t.b.d.

### 8.3 Nutzungsanweisung (How-to-use)

Kurze Anleitung für den Nutzer oder den Korrektor: Wie wird die App gestartet und welche Features sind wie zu nutzen?

**App starten** (im Projektordner `g07/`):

- `python -m venv venv`
- `venv\Scripts\activate`
- `pip install -r requirements.txt`
- `streamlit run app.py`

**Kernfunktionen (UI-Tabs)**

- **Dashboard:** aktuelle Metriken (Prozessspeicher, Objekt-/Archivstatistiken) und GC-Demonstration (Break References → Run GC)
- **Data Generation:** Generierung eines (skalierbaren) Objektgraphen
- **Search Engine:** Abfragen über Indexe (Jahr, Elefant, Location-Raster)
- **Genealogy:** Visualisierung genealogischer Beziehungen

**Tests ausführen**

- `pytest -q`

### 8.4 Pitch-Video

t.b.d.

---

## Anhang

- **README.md (Inhalt):** Setup-Anleitung, Python-Umgebung, Paketliste.

Siehe: [README.md](../README.md)

- **Glossar:** Definition der fachlichen Begriffe der "Story".

Quellen-/Referenzliste (Projekt): [references.md](references.md)

---

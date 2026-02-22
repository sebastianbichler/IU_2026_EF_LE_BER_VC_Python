
# Finalisierungsphase – Abschlussdokumentation (g07)

**Projekt:** Elephant Memory Cloud

**Ziel der Finalisierung:**
- Abschlussdoku erstellen und Projektartefakte konsistent verlinken
- Code-Struktur architektonisch begründen (inkl. relevanter Klassen/Module)
- Hypothesen H1 & H2 aus der Konzeptionsphase beantworten
- Mind. 1–2 Unit-Tests ergänzen (Nachvollziehbarkeit/Reproduzierbarkeit)

---

## 1. Ergebnisüberblick

Im Rahmen der Finalisierungsphase wurde die bestehende Implementierung inhaltlich nicht „aufgeblasen“, sondern gezielt stabilisiert und dokumentiert:

- **Architektur:** klare Trennung von UI (`app.py`), Domain Models (`models/`), Services (`data/`, `search/`, `memory/`).
- **GC-Demo:** Zwei-Schritt-Demonstration (Referenzen entfernen → GC auslösen) wurde so angepasst, dass sie semantisch sauber „orphaned cycles“ zeigt (keine versteckten starken Referenzen).
- **Unit-Tests:** zwei fokussierte Tests für Search-Indexing und für das Auflösen/Brechen von Beziehungen im Store.
- **Hypothesen:** H1/H2 werden anhand eines reproduzierbaren Versuchsablaufs (UI-Schritte) beantwortet.

---

## 2. Architektur & Code-Struktur (Begründung)

### 2.1 Schichten / Verantwortlichkeiten (Lightweight Layering)

Die Anwendung folgt einer pragmatischen Schichtung (ohne Framework-Overkill):

1) **Presentation / UI**
	- `app.py`: Streamlit-Dashboard als View + Orchestrierung
	- Verantwortlich für Interaktion, Visualisierung und Triggern von Experimenten

2) **Domain Model**
	- `models/`:
	  - `Elephant`: Eltern/Kinder-Beziehungen, bewusste Zyklen (Parent ↔ Child)
	  - `Herd`: Herd ↔ Elephant-Zyklus (Mitgliederliste + Rückreferenz)
	  - `Event`/`EventType`: Events als Knoten, die Objekte „zusammenbinden“
	  - `WaterSource`: Wasserstellen + Historie
	- Diese Ebene ist bewusst „objektgraph-lastig“, um Memory-Management-Effekte sichtbar zu machen.

3) **Application Services**
	- `data/generator.py` (`DataGenerator`): Erzeugt reproduzierbare Testdaten (Familien/Herden/Events)
	- `search/engine.py` (`ElephantSearchEngine`): In-Memory Indexing (Dictionary-basierte Indizes) für schnelle Abfragen
	- `memory/monitor.py` (`MemoryMonitor`): Messung RSS (psutil) als Metrik

4) **In-Memory Storage (Repository-ähnlich)**
	- `memory/store.py` (`MemoryStore`): zentraler Datencontainer für die aktuell „live“ gehaltenen Objekte
	- wird als **Singleton** über `get_store()` bereitgestellt (bewusst: ein globaler Objektgraph im RAM)

Diese Aufteilung ist didaktisch passend: Domain-Objekte bleiben unabhängig von Streamlit, während Services/UI sie orchestrieren.

### 2.2 Design-Patterns / Paradigmen (bewusst minimal)

Die Codebasis nutzt einige „klassische“ Muster, ohne eine formale Enterprise-Architektur einzuführen:

- **Domain Model (OO-Paradigma):** `Elephant`, `Herd`, `Event`, `WaterSource` sind reichhaltige Objekte mit Beziehungen.
- **Repository-ähnlicher Store:** `MemoryStore` kapselt das „Persistenz“-Äquivalent (hier: RAM).
- **Singleton:** globaler Store über `get_store()` – sinnvoll für Streamlit-Sessions/Demo und für einen konsistenten Objektgraphen.
- **Service Layer:** `DataGenerator`, `ElephantSearchEngine`, `MemoryMonitor` als Services mit klarer Verantwortung.
- **Indexing als Performance-Technik:** `ElephantSearchEngine.index_all()` erstellt Indizes → O(1)-Lookups (z. B. Jahr/Elefant/EventType).

### 2.3 Bewertung der Code-Struktur (Stärken / Risiken)

**Stärken**
- Gute fachliche Kohäsion: Modelle liegen in `models/`, Services in eigenen Modulen.
- Search-Engine ist testbar (UI-unabhängig) und kapselt Indexing.
- Memory-Thema wird konsequent durch bewusst zyklische Beziehungen unterstützt.

**Risiken / technische Schulden (vertretbar im Scope, aber dokumentiert)**
- `app.py` ist sehr groß und enthält viel UI-Logik in einem File (geringe Wartbarkeit).
- Globales State-Handling (Streamlit `session_state` + Singleton Store) ist gut für Demo, aber weniger „clean“ für echte Applikationen.
- Einige Klassen nutzen Klassen-Listen als Registry (`Event._all_events`, `WaterSource._all_sources`) – praktisch, aber erhöht versteckte Kopplung.

### 2.4 Empfohlene Optimierungen (ohne Overkill)

Diese Optimierungen wären der nächste sinnvolle Schritt, wurden aber bewusst nicht vollständig refaktoriert (Scope/Abgabe):

1) **UI in Funktionen/Module splitten**
	- z. B. `ui/dashboard.py`, `ui/generation.py`, `ui/search.py`, `ui/genealogy.py`
	- Vorteil: bessere Lesbarkeit, einfachere Tests auf Service-Ebene

2) **Explizite „Reset/Cleanup“ API für Search-Engine**
	- statt `index_all([], [], [])` könnte es eine Methode `clear_indexes()` geben
	- Vorteil: klarere Semantik

3) **Optionale Dependency Injection (klein)**
	- `app.py` könnte Services/Store in einer kleinen Factory erzeugen
	- Vorteil: Unit-Tests/Simulation ohne globalen Zustand

---

## 3. Hypothesen (H1 & H2) – beantwortet

Aus der Konzeptionsphase:
- **H1:** Ohne zyklische GC steigt die Anzahl nicht freigegebener Objekte mit der Größe des Objektgraphen.
- **H2:** Mit aktivierter GC werden zyklische Referenzen nach Entfernen externer Referenzen aufgelöst.

### 3.1 Experimenteller Ablauf (reproduzierbar über UI)

1) App starten
	- `streamlit run app.py`

2) Unter **„Data Generation“** ein Dataset erzeugen
	- Parameter erhöhen → größerer Objektgraph (mehr Elefanten, mehr Zyklen)

3) Unter **„Dashboard“** auf **„Break References“** klicken
	- externe Referenzen (Store + Search-Indizes) werden entfernt
	- zyklische GC wird deaktiviert (`gc.disable()`)
	- Ergebnis: Elefanten bleiben über Zyklen im Speicher erreichbar (nur innerhalb des Zyklus)

4) Beobachten: „Orphaned in Memory“
	- Bei größeren Datasets steigt der Wert deutlich → konsistent mit H1 (Skalierung mit Graphgröße)

5) Auf **„Run GC“** klicken
	- zyklische GC wird reaktiviert (`gc.enable()`)
	- anschließend wird eine Collection erzwungen (`gc.collect()`)
	- Ergebnis: zyklische Strukturen werden bereinigt, Instanzanzahl sinkt → konsistent mit H2

### 3.2 Bewertung der Hypothesen

- **H1 wird unterstützt:** Wenn zyklische GC deaktiviert ist und externe Referenzen entfernt wurden, verbleiben zyklische Objekte im Speicher. Mit wachsender Graphgröße wächst die Anzahl der nicht freigegebenen Objekte.
- **H2 wird bestätigt:** Nach Aktivierung und Auslösung der zyklischen GC werden die zuvor „orphaned“ zyklischen Referenzen aufgelöst (Objekte werden freigegeben).

Wichtiger Hinweis zur Interpretation:
- Das Verhalten ist kein „klassischer Memory Leak“ im Sinne eines verlorenen Handles, sondern ein demonstriertes Zusammenspiel von Reference Counting vs. zyklischer GC.

---

## 4. Unit-Tests (neu)

Es wurden zwei kleine, zielgerichtete Unit-Tests ergänzt, um Kernlogik unabhängig von Streamlit zu prüfen:

- Search-Engine Indexing/Queries (`ElephantSearchEngine`)
- Aufräumen/Brechen von Beziehungen (`MemoryStore.clear_and_cleanup()`)

### Tests ausführen

Im Repo-Root:

```bash
pytest -q
```

---

## 5. Fazit

Die Code-Struktur ist für den didaktischen Zweck (Memory-Management + zyklische Objektgraphen) passend. Die wichtigsten Verbesserungen in der Finalisierung waren Dokumentation, Reproduzierbarkeit und eine semantisch saubere GC-Demo.


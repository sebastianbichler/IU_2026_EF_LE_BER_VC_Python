# RabbitFarm – Der Gemüsehof des Hasen

## 1. Projektüberblick

Rudi, der Hase, betreibt einen nachhaltigen Gemüsehof im Wald.  
Die Anwendung soll ihn dabei unterstützen,

- Anbauflächen zu planen,
- Lagerbestände im Blick zu behalten,
- Abo-Kisten an Waldtiere zu liefern,
- Einnahmen und Ausgaben zu dokumentieren und
- Ernteerträge (auch als Datenströme) effizient auszuwerten.

Zusätzlich wird ein wissenschaftlicher Fokus auf **funktionales Programmieren** und **Lazy Evaluation** gelegt:  
Sensordaten der Beete werden als endlose Datenströme per **Generatoren** und **itertools** verarbeitet.

---

## 2. Wissenschaftlicher Fokus: Funktionales Programmieren & Lazy Evaluation

- [x] Forschungsfrage präzisieren  
      *„Speichereffizienz von Lazy Evaluation: Vergleich von Eager- vs. Lazy-Datenverarbeitung in Stream-Processing-Systemen.“*
- [x] Implementierung der Vergleichsfunktionen:
  - [x] `process_eager()` - Listen-basierte Verarbeitung in `main.py`
  - [x] `process_lazy()` - Generator-basierte Verarbeitung in `main.py`
  - [x] `benchmark_eager()` und `benchmark_lazy()` für Performance-Vergleich
- [x] Bezug zur Anwendung herstellen:
  - [x] Endlose Sensordatenströme der Anbauflächen (`stream_soil_moisture()` in `sensors.py`)
  - [x] Lazy-Berechnung von Bewässerungsplänen (Filterung und Map-Operationen)
- [x] Jupyter Notebook für Demonstration:
  - [x] Notebook in `static/notebooks/layz_vs_eager.ipynb` vorhanden
  - [x] Vollständiges Notebook mit Visualisierungen erstellt: `static/notebooks/lazy_vs_eager_complete.ipynb`
- [ ] Literaturverweis aufnehmen:
  - [ ] *Functional Programming in Python* (David Mertz)

---

## 3. Ziele der Anwendung (High Level)

- [x] Rudi kann seine **Gemüsebeete und Kulturen** planen und verwalten (implementiert in `main.py`).
- [x] Der **Lagerbestand** (Menge, Frische, Haltbarkeit) wird automatisch aktualisiert (`Inventory` Klasse).
- [x] **Kundenbestellungen** (Abo-Kisten) können erfasst, geplant und geliefert werden (`Order`, `SubscriptionBox` Klassen).
- [x] **Gewinne und Ausgaben** werden erfasst und ausgewertet (`calculate_profit()` in `services.py`).
- [ ] **Ernteerträge** vergangener Saisons werden visualisiert (Diagramme) - noch zu implementieren.
- [x] Sensordaten werden als **endlose Streams** verarbeitet (Lazy Evaluation - `stream_soil_moisture()`).
- [ ] Die Anwendung ist gut strukturiert, getestet und dokumentiert (Portfolio-Anforderungen) - Tests fehlen noch.

---

## 4. Software-Requirements (User Stories mit Checkboxes)

### 4.1 Muss-Anforderungen (MVP)

- [ x ] **SR1 – Gemüseverwaltung**  
  - [ x ] Rudi kann Gemüsesorten anlegen, bearbeiten, löschen.  
  - [ x ] Attribute: Name, Sorte (z.B. Karotte, Salat), Pflanzdatum, voraussichtlicher Erntetermin, Beet.

- [ x ] **SR2 – Beet-Management**  
  - [ x ] Beete können angelegt werden (z.B. „Beet A“, „Tunnel 1“).  
  - [ x ] Jedem Beet können mehrere Gemüsesorten zugeordnet werden.  

- [ x ] **SR3 – Lagerbestände**  
  - [ x ] Ernte kann vom Beet ins Lager übernommen werden.  
  - [ x ] Attribute: Gemüsesorte, Menge (Stück / kg), Erntedatum, Haltbarkeit / Frische-Status.  

- [ x ] **SR4 – Kunden & Abo-Kisten**  
  - [ x ] Kunden (Waldtiere) können angelegt werden (Name, Art, bevorzugtes Gemüse).  
  - [ x ] Abo-Kisten können definiert werden (z.B. wöchentlich, Inhalt, Preis).  
  - [ x ] Bestellungen werden mit Lieferdatum und Lieferstatus gespeichert.

- [ x ] **SR5 – Einnahmen & Ausgaben**  
  - [ x ] Einnahmen aus Abo-Kisten und Einzelverkäufen erfassen.  
  - [ x ] Ausgaben für Saatgut, Dünger, Wasser etc. erfassen.  

- [ ] **SR6 – Ernte-Visualisierung**  
  - [ ] Diagramm für Ernteerträge pro Saison und Gemüsesorte erstellen  
        (z.B. mit `matplotlib` oder einem anderen Visualisierungs-Framework).
        **Status:** Noch nicht implementiert - nur Visualisierungen für Lazy vs Eager vorhanden.

### 4.2 Erweiterte Anforderungen (Science & Lazy Evaluation)

- [ x ] **SR7 – Vergleich Eager vs. Lazy**  
  - [ x ] Eager-Variante der Sensordatenverarbeitung (Liste im Speicher).  
  - [ x ] Lazy-Variante (Generator/Iterator).  
  - [ x ] Einfacher Vergleich der Speicher-/Performance-Kennzahlen  
        (z.B. mit `sys.getsizeof`, grober Zeitvergleich).

### 4.3 Kann-Anforderungen (Nice to Have)

- [ ] Rezeptvorschläge je nach Lagerbestand generieren.  
- [ ] Saisonale Angebote („Herbstkiste“, „Vitamin-C-Woche“) automatisch erstellen.  
- [ ] Export von Berichten als CSV/JSON.

---

## 5. Domänenmodell (Klassenplanung)

- [x] **Klasse `Vegetable` (Gemuese)**
  - [x] Attribute: `name`, `sort`, `plant_date`, `harvest_date`, `bed_id`, `shelf_life_days`, `amount`.
  - [x] Methoden: `is_fresh()`, `freshness_ratio()`.

- [x] **Klasse `Bed` (Beet)**
  - [x] Attribute: `id`, `name`, `size_m2`.
  - [x] Zuordnung zu Gemüse über `bed_id` in `Vegetable`.

- [x] **Klasse `Inventory` (Lagerbestand)**
  - [x] Attribute: `items` (Liste von `Vegetable`).
  - [x] Methoden: `add_harvest()`, `get_fresh_items()`, `get_expired_items()`, `get_total_amount()`.

- [x] **Klasse `Customer` (Kunde)**
  - [x] Attribute: `name`, `species`, `subscription_type`.
  - [x] Methoden: `__str__()`.

- [x] **Klasse `SubscriptionBox` (AboKiste)**
  - [x] Attribute: `customer`, `vegetables`, `delivery_date`, `price`.
  - [x] Methoden: `__str__()`.

- [x] **Klasse `Order` (Bestellung)**
  - [x] Attribute: `customer`, `vegetables`, `delivery_date`, `price`.
  - [x] Methoden: `__str__()`.

- [x] **Generatorfunktionen für Sensordaten**
  - [x] `stream_soil_moisture()` in `sensors.py` liefert endlose Datenströme für Beete.
  - [x] Filter-/Map-Funktionen im funktionalen Stil in `main.py` (`process_eager()`, `process_lazy()`).

---

## 6. Technische Planung

- [x] **Projektstruktur definieren**
  - [x] `src/__init__.py`
  - [x] `src/models.py` (Domänenklassen: Vegetable, Bed, Customer, Inventory, Order, SubscriptionBox)
  - [x] `src/services.py` (Bestelllogik, Gewinnberechnung)
  - [x] `src/sensors.py` (Generatoren, Lazy Evaluation für Sensordaten)
  - [x] `src/main.py` (CLI-Interface, Datenpersistenz)
  - [x] `tests/` (Verzeichnis vorhanden)
  - [x] `data/` (JSON-Datenhaltung: `rabbitfarm_data.json`)

- [x] **Einfache Benutzeroberfläche wählen**
  - [x] Entscheidung: Menübasierte CLI (Textbasiert) - implementiert in `main.py`.
  - [x] Menüstruktur: Gemüse, Beete, Lager, Kunden, Finanzen, Sensordaten.

- [x] **Datenhaltung**
  - [x] Implementiert: In-Memory + JSON-Dateien als Persistenz (`rabbitfarm_data.json`).
  - [x] `save_data()` und `load_data()` Funktionen implementiert.

---

## 7. Tests

- [ ] **Unit-Tests**
  - [ ] Für zentrale Domänenklassen (z.B. `Gemuese`, `Beet`, `LagerEintrag`, `Bestellung`).
  - [ ] Tests für Generatorfunktionen (z.B. erste *n* Sensordaten prüfen).

- [ ] **Integrationstests (mind. 3)**
  - [ ] Test 1: „Vom Beet ins Lager“ – Pflanzung → Ernte → Lagerbestand.  
  - [ ] Test 2: „Abo-Kiste“ – Erstellung Bestellung → Lager wird korrekt reduziert.  
  - [ ] Test 3: „Lazy Stream“ – Sensordaten-Stream → Bewässerungsentscheidungen.

- [ ] **Test-Setup**
  - [ ] `pytest` einrichten.
  - [ ] Testdaten / Fixtures anlegen.

---

## 8. Dokumentation

- [ ] **README.md**
  - [ ] Projektbeschreibung (Story + Fachteil).
  - [ ] Installationsanleitung (Python-Version, virtuelles Environment).
  - [ ] `requirements.txt` / `pyproject.toml` dokumentieren.
  - [ ] How-To-Use (Beispiele für typische Workflows).

- [ ] **Developer-Dokumentation (Markdown im Repo)**
  - [ ] Software Requirements (dieses Dokument verlinken).  
  - [ ] Architekturübersicht (Domänenmodell, wichtige Module).  
  - [ ] Sequenz-/Use-Case-Diagramme (Mermaid o.Ä.) für typische Abläufe:
    - [ ] Bestellung einer Abo-Kiste
    - [ ] Verarbeitung von Sensordaten (Lazy Stream)

- [ ] **Wissenschaftlicher Teil**
  - [ ] Kurzes Kapitel zur Forschungsfrage & Methodik.  
  - [ ] Beschreibung Eager vs. Lazy in der eigenen Implementierung.  
  - [ ] Kurze Diskussion von Ergebnissen (z.B. Speichervergleich).

---

## 9. CI / Tooling

- [x] `requirements.txt` anlegen.
  - [x] Dependencies: `matplotlib`, `numpy`, `pandas`, `memory-profiler`, `jupyter`, `ipykernel`.
- [ ] Linting / Formatierung:
  - [ ] `flake8` oder `ruff`.
  - [ ] `black` oder `autopep8`.
- [ ] Automatisierte Tests:
  - [ ] `pytest` in CI-Pipeline integrieren.
- [ ] (Optional) GitHub Actions / GitLab CI:
  - [ ] Job: Setup Python
  - [ ] Job: Install requirements
  - [ ] Job: Lint
  - [ ] Job: Tests

---

## 10. Zeitplanung (Portfolio-Phasen)

> **Konzeptionsphase**
- [ ] Anforderungen finalisieren (dieses Dokument).  
- [ ] Grobes Domänenmodell als Skizze/Mermaid-Diagramm.  
- [ ] Konzept-Präsentation vorbereiten.

> **Erarbeitungsphase**
- [x] Minimale lauffähige App (MVP) implementiert.  
- [x] Alle Software-Requirements (SR1-SR7) vollständig umgesetzt.  
- [ ] Erste Tests & Dokumentation im Projekt - Tests fehlen noch.

> **Finalisierungsphase**
- [ ] Alle geplanten Features (so weit möglich) implementieren.  
- [ ] Testsuite vollständig.  
- [ ] Dokumentation + wissenschaftlicher Teil final.  
- [ ] Projekt-Reflexion (Abstract) schreiben.

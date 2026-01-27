# RabbitFarm – Der Gemüsehof des Hasen 🥕🐇

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

- [ ] Forschungsfrage präzisieren  
      *„Speichereffizienz von Lazy Evaluation: Vergleich von Eager- vs. Lazy-Datenverarbeitung in Stream-Processing-Systemen.“*
- [ ] Kurze theoretische Zusammenfassung zu:
  - [ ] Iteratoren & Generatoren in Python // nicht sicher !!
  - [ ] Lazy vs. Eager Evaluation
  - [ ] Relevanz für Stream Processing / Sensordaten
- [ ] Bezug zur Anwendung herstellen:
  - [ ] Endlose Sensordatenströme der Anbauflächen
  - [ ] Lazy-Berechnung von Ernteerträgen und Bewässerungsplänen
- [ ] Literaturverweis aufnehmen:
  - [ ] *Functional Programming in Python* (David Mertz)

---

## 3. Ziele der Anwendung (High Level)

- [ ] Rudi kann seine **Gemüsebeete und Kulturen** planen und verwalten.
- [ ] Der **Lagerbestand** (Menge, Frische, Haltbarkeit) wird automatisch aktualisiert.
- [ ] **Kundenbestellungen** (Abo-Kisten) können erfasst, geplant und geliefert werden.
- [ ] **Gewinne und Ausgaben** werden erfasst und ausgewertet.
- [ ] **Ernteerträge** vergangener Saisons werden visualisiert (Diagramme).
- [ ] Sensordaten werden als **endlose Streams** verarbeitet (Lazy Evaluation).
- [ ] Die Anwendung ist gut strukturiert, getestet und dokumentiert (Portfolio-Anforderungen).

---

## 4. Software-Requirements (User Stories mit Checkboxes)

### 4.1 Muss-Anforderungen (MVP)

- [ x ] **SR1 – Gemüseverwaltung**  
  - [ x ] Rudi kann Gemüsesorten anlegen, bearbeiten, löschen.  
  - [ x ] Attribute: Name, Sorte (z.B. Karotte, Salat), Pflanzdatum, voraussichtlicher Erntetermin, Beet.

- [ x ] **SR2 – Beet-Management**  
  - [ x ] Beete können angelegt werden (z.B. „Beet A“, „Tunnel 1“).  
  - [ x ] Jedem Beet können mehrere Gemüsesorten zugeordnet werden.  
  - [ x ] Übersicht: Was wächst aktuell wo?

- [ x ] **SR3 – Lagerbestände**  
  - [ x ] Ernte kann vom Beet ins Lager übernommen werden.  
  - [ x ] Attribute: Gemüsesorte, Menge (Stück / kg), Erntedatum, Haltbarkeit / Frische-Status.  
  - [ x ] Warnung / Markierung bei überschrittener Haltbarkeit.

- [ x ] **SR4 – Kunden & Abo-Kisten**  
  - [ x ] Kunden (Waldtiere) können angelegt werden (Name, Art, bevorzugtes Gemüse).  
  - [ x ] Abo-Kisten können definiert werden (z.B. wöchentlich, Inhalt, Preis).  
  - [ x ] Bestellungen werden mit Lieferdatum und Lieferstatus gespeichert.

- [ x ] **SR5 – Einnahmen & Ausgaben**  
  - [ x ] Einnahmen aus Abo-Kisten und Einzelverkäufen erfassen.  
  - [ x ] Ausgaben für Saatgut, Dünger, Wasser etc. erfassen.  
  - [ x ] Einfacher Übersichtsbericht: Gewinn/Verlust nach Zeitraum.

- [ x ] **SR6 – Ernte-Visualisierung**  
  - [ x ] Diagramm für Ernteerträge pro Saison und Gemüsesorte erstellen  
        (z.B. mit `matplotlib` oder einem anderen Visualisierungs-Framework).

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

- [ ] **Klasse `Gemuese`**
  - [ ] Attribute: `name`, `sorte`, `pflanzdatum`, `erntedatum`, `beet_id`.
  - [ ] Methoden: z.B. `tage_bis_ernte()`, `ist_erntebereit()`.

- [ ] **Klasse `Beet`**
  - [ ] Attribute: `id`, `name`, `flaeche_m2`, Liste von `Gemuese`.
  - [ ] Methoden: `freie_flaeche()`, `geplante_ernte()`.

- [ ] **Klasse `Lagerbestand` / `LagerEintrag`**
  - [ ] Attribute: `genuese`, `menge`, `erntedatum`, `haltbar_bis`.
  - [ ] Methoden: `ist_abgelaufen()`, `frische_score()`.

- [ ] **Klasse `Kunde`**
  - [ ] Attribute: `name`, `tierart`, `adresse`, `praeferenzen`.
  - [ ] Methoden: `mag_gemuese(art)`.

- [ ] **Klasse `Bestellung` / `AboKiste`**
  - [ ] Attribute: `kunde`, `lieferdatum`, `inhalt`, `preis`, `status`.
  - [ ] Methoden: `berechne_gesamtpreis()`, `markiere_geliefert()`.

- [ ] **Klasse `Lieferung`**
  - [ ] Attribute: `bestellung`, `route`, `lieferstatus`.
  - [ ] Methoden: `starten()`, `abschliessen()`.

- [ ] **Klasse `Hof`**
  - [ ] Aggregiert Beete, Lager, Kunden, Bestellungen, Finanzen.  
  - [ ] Methoden: zentrale API für CLI/GUI.

- [ ] **Klasse `SensorStream` / Generatorfunktionen**
  - [ ] Funktion/Objekt, das endlose Datenströme für Beete liefert.  
  - [ ] Filter-/Map-Funktionen im funktionalen Stil.

---

## 6. Technische Planung

- [ ] **Projektstruktur definieren**
  - [ ] `src/rabbitfarm/__init__.py`
  - [ ] `src/rabbitfarm/models/` (Domänenklassen)
  - [ ] `src/rabbitfarm/services/` (z.B. Bestelllogik, Lagerlogik)
  - [ ] `src/rabbitfarm/streams/` (Generatoren, Lazy Evaluation)
  - [ ] `tests/` (Unit- & Integrationstests)
  - [ ] `data/` (Beispieldaten, ggf. CSV/JSON)

- [ ] **Einfache Benutzeroberfläche wählen**
  - [ ] Entscheidung: CLI-Menü, TUI, oder einfache Web-Variante (z.B. `Flask`).
  - [ ] MVP: Menübasierte CLI (Textbasiert).

- [ ] **Datenhaltung**
  - [ ] Entscheidung: In-Memory + JSON-Dateien / CSV als Persistenz.  
  - [ ] Optional: SQLite-DB.

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

- [ ] `requirements.txt` anlegen (oder `pyproject.toml`).
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
- [ ] Minimale lauffähige App (MVP) implementieren.  
- [ ] Mindestens 2 Software-Requirements vollständig umgesetzt.  
- [ ] Erste Tests & Dokumentation im Projekt.

> **Finalisierungsphase**
- [ ] Alle geplanten Features (so weit möglich) implementieren.  
- [ ] Testsuite vollständig.  
- [ ] Dokumentation + wissenschaftlicher Teil final.  
- [ ] Projekt-Reflexion (Abstract) schreiben.

---

## 11. Offene Punkte / Ideen

- [ ] Konkrete Beispielkunden & -rezepte ausarbeiten (Storytelling).  
- [ ] Saisonale Events (z.B. „Karottenfestival“, „Salatwoche“).  
- [ ] Erweiterung um einfache Weboberfläche.  
- [ ] Optionale Export-/Importfunktionen für Daten (Backup).
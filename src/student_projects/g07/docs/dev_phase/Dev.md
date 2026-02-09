# Erarbeitungsphase – Umsetzungsstand

## Struktur

Die Projektstruktur von `g07` ist in der lokalen `README.md` (im g07-Verzeichnis) dokumentiert.

Für `g07` relevant (Orientierung):

- Einstiegspunkt/GUI: `app.py`
- Datengenerierung: `data/generator.py`
- Datenmodell: `models/`
- In-Memory Store & Monitoring: `memory/`
- Suche & Indizes: `search/engine.py`
- Projektdoku: `docs/` (u.a. `concept_phase/`, `dev_phase/diagrams/`)

## Umgesetzte Komponenten

- Dashboard/UI: `app.py` (Streamlit) mit Tabs für Overview, Datengenerierung, Suche, Genealogie
- Datenmodell: `models/` (Elefant, Herde, Event, Wasserstelle) inkl. zyklischer Beziehungen
- Datengenerierung: `data/generator.py` (Familien/Herden/Events/Wasserstellen)
- In-Memory Storage + Monitoring: `memory/store.py`, `memory/monitor.py`
- Suche/Indexing: `search/engine.py` (Dictionary-basierte Indizes)

## Abgleich gegen Anforderungen (Concept.md)

Legende: ✅ umgesetzt · 🟨 teilweise · ⛔ offen

- F01 Ereignisse erfassen: ✅ (Event-Objekte inkl. Jahr/Ort/Beteiligte)
- F02 Ereignisse indexieren: ✅ (Jahr-/Ort-Indizes im Search-Engine-Modul)
- F03 Elefanten modellieren: ✅ (`models/elephant.py`)
- F04 Verwandtschaftsbeziehungen: ✅ (Eltern/Kinder + Herd-Zugehörigkeit)
- F05 Zirkuläre Referenzen erzeugen: ✅ (bidirektionale Beziehungen; Orphaning-Demo im UI)
- F06 Stammbäume visualisieren: ✅ (Genealogy-Visualisierung via Plotly in `app.py`)
- F07 Wasserstellen-Suche: ✅ (Search-Engine-Funktionalität + UI)
- F08 Erinnerungs-Bot: ✅/🟨 (zeitbasierte Hinweise/Alerts im Search-Kontext; Umfang je UI-Flow)
- F09 Speicherverhalten messen: ✅ (psutil-basiertes Monitoring + Metriken im UI)
- F10 GC-Vergleich (GC an/aus): 🟨 (GC-Demo via „Referenzen brechen“ + `gc.collect()`; reproduzierbarer Vergleichslauf mit explizitem `gc.disable()/gc.enable()` und identischen Szenarien fehlt)

- NF02 Reproduzierbarkeit (Experimente): ⛔ (Messläufe/Experimente sind noch nicht konsistent als reproduzierbare Abfolge in `docs/` beschrieben)

## Real verwendete externe Abhängigkeiten

- Externe Dependencies: Streamlit, Plotly, psutil (siehe `requirements.txt`)
- Tests: aktuell keine automatisierten Tests im Projekt
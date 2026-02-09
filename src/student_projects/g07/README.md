# 1 Elephant Memory Cloud

Dieses Projekt ist ein Python-basierter Prototyp zur Untersuchung von **Reference Counting und zyklischer Garbage Collection** in komplexen Objektgraphen.

Anhand eines thematisch eingebetteten Szenarios (Elefanten, Stammbäume, Ereignisse) werden bewusst zirkuläre Referenzen erzeugt, analysiert und hinsichtlich ihres Speicherverhaltens untersucht. Ziel ist ein reproduzierbarer experimenteller Nachweis der Wirksamkeit des Garbage Collectors in Python.

## 1.1 Installation

Die allgemeinen Voraussetzungen hinsichtlich Python, virtuellen Umgebungen und der globalen Installation von Abhängigkeiten (pip) ist dem übergeordneten Projekt zu entnehmen.

Virtuelle Umbegung erstellen & Programm starten:
```
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

## 1.2 Bibliotheken (Kurzüberblick)

### 1.2.1 Standardbibliothek
- gc
- sys
- tracemalloc
- weakref
- datetime

### 1.2.2 Externe Bibliotheken
- streamlit – Webbasierte Visualisierung und Dashboard
- plotly – Interaktive Diagramme und Auswertungen
- psutil – Systemressourcen und Speicher-Monitoring

Optionale Analyse- und Visualisierungstools sind/ werden in der weiteren Dokumentation aufgeführt.

## 1.3 Struktur

```
g07/
├── app.py
├── requirements.txt
├── data/
│   └── generator.py
├── memory/
│   ├── monitor.py
│   └── store.py
├── models/
│   ├── elephant.py
│   ├── herd.py
│   ├── event.py
│   └── water_source.py
├── search/
│   └── engine.py
├── docs/
│   ├── concept_phase/ (Concept.md)
│   └── dev_phase/ (Dev.md, diagrams/)
└── tests/
```

---

# 2 Projektphasen – Übersicht

Dieses Dokument beschreibt die Struktur und Zielsetzung der einzelnen Projektphasen der *Elephant Memory Cloud*.

Alle phasenbezogenen Dokumente dienen der **Planung, Nachvollziehbarkeit und Bewertung** des Projekts und sind bewusst voneinander getrennt. Änderungen oder Erweiterungen erfolgen ausschließlich innerhalb der jeweiligen Phase.

## 2.1 Ziel dieses Verzeichnisses

Das Verzeichnis `docs/` bündelt **alle konzeptionellen und planerischen Dokumente**, die den Projektverlauf strukturieren oder anderweitig dokumentieren.

* Jede Phase besitzt ein eigenes Unterverzeichnis
* Jede Phase hat klar definierte Ziele, Artefakte und Ergebnisse
* Abgeschlossene Phasen werden nicht überschrieben, sondern versioniert

## 2.2 Phasenübersicht

### 2.2.1 Konzeptionsphase

**Zeitraum:** 05.01.2026 – 26.01.2026

**Ziel:**

* Fachliches und technisches Verständnis der Aufgabenstellung
* Definition von Anforderungen
* Festlegung des wissenschaftlichen Untersuchungsfokus

**Zentrale Fragestellungen:**

* Welche Funktionalität muss das System bereitstellen?
* Welche nicht-funktionalen Anforderungen gelten?
* Wie wird das Thema Memory Management experimentell untersucht?

**Dokumente:**

* `docs/concept_phase/` – Gesamtkonzept & Anforderungen

### 2.2.2 Erarbeitungsphase

**Zeitraum:** 26.01.2026 – 09.02.2026

**Ziel:**

* Erstellung eines lauffähigen Projekts
* Umsetzung 1-2 der erarbeiteten Requirements aus der Konzeptionsphase
* Dokumentation; READMEs, UML-Diagramme, etc.

**Dokumente:**
* `docs/dev_phase`


### 2.2.3 Finalisierungsphase

* t.b.d

---

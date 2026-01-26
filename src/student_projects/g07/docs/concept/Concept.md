# Elephant Memory Cloud

## 1. Projektkontext

* **Modul:** Einführung in die Programmierung mit Python (5. Semester)
* **Projektzeitraum:** 05.01.2026 – März 2026
* **Gruppengröße:** 3 Personen
* **Vorkenntnisse:** Keine praktischen Python-Erfahrungen
* **Abgabe Konzeptionsphase:** 26.01.2026

Dieses Dokument beschreibt die konzeptionelle Planung des Projekts *Elephant Memory Cloud* mit Fokus auf funktionale und nicht‑funktionale Anforderungen sowie den wissenschaftlichen Untersuchungsschwerpunkt *Memory Management in Python*.

---

## 2. Projektidee & Zielsetzung

Die *Elephant Memory Cloud* ist ein Python‑Prototyp eines digitalen Gedächtnisses für „Ella Elefant“.
Ziel ist **nicht** die Entwicklung eines produktionsreifen Systems, sondern:

* das strukturierte Modellieren komplexer Objektbeziehungen,
* die gezielte Erzeugung zirkulärer Referenzen,
* und deren Analyse im Kontext von Reference Counting und zyklischer Garbage Collection.

Die thematische Einbettung (Savanne, Elefanten, Wasserstellen) dient ausschließlich der Veranschaulichung.

---

## 3. Abgrenzung & Mindestumfang (Konzeptionsabgabe)

### Mindestumfang (verpflichtend)

* Definiertes Datenmodell mit absichtlich erzeugten Zyklen
* Reproduzierbare GC‑Experimente
* Messung und Dokumentation von Speicherverhalten
* Funktionsfähige, einfache Visualisierung

### Erweiterungen (optional)

* Komfortfunktionen im UI
* Erweiterte Visualisierungen
* Zusätzliche Analysemetriken

---

## 4. Funktionale Anforderungen

### F01 – Ereignisse erfassen

Das System muss Ereignisse mit folgenden Attributen speichern können:

* Jahr
* Ort (Wasserstelle)
* Beteiligte Elefanten / Herden

### F02 – Ereignisse indexieren

Das System muss Ereignisse effizient nach Jahr und Ort durchsuchen können.

### F03 – Elefanten modellieren

Das System muss einzelne Elefanten als Objekte abbilden können.

### F04 – Verwandtschaftsbeziehungen abbilden

Das System muss Eltern‑, Kind‑ und Herdenbeziehungen zwischen Elefanten modellieren.

### F05 – Zirkuläre Referenzen erzeugen

Das System muss absichtlich zirkuläre Referenzen zwischen Objekten erzeugen (z. B. Eltern ↔ Kinder).

### F06 – Stammbäume visualisieren

Das System muss Verwandtschaftsgraphen visuell darstellen können.

### F07 – Wasserstellen‑Suche

Das System muss auf Basis historischer Ereignisdaten eine einfache Suche nach Wasserstellen ermöglichen.

### F08 – Erinnerungs‑Bot

Das System muss zeitbasierte Erinnerungen (Jahrestage, Migrationen) ausgeben können.

### F09 – Speicherverhalten messen

Das System muss Speicherverbrauch und Objektanzahl während der Laufzeit erfassen.

### F10 – GC‑Vergleich ermöglichen

Das System muss identische Szenarien mit aktivierter und deaktivierter Garbage Collection ausführen können.

---

## 5. Nicht‑funktionale Anforderungen

### NF01 – Nachvollziehbarkeit

Der Code muss didaktisch nachvollziehbar und kommentiert sein.

### NF02 – Reproduzierbarkeit

Alle Experimente müssen reproduzierbar dokumentiert sein.

### NF03 – Messbarkeit

Speicherverhalten muss quantitativ erfasst werden.

### NF04 – Begrenzter Scope

Keine Cloud‑Architektur, keine Persistenzdatenbanken, keine KI/ML‑Verfahren.

### NF05 – Performance‑Abgrenzung

Ab einer großen Anzahl von Knoten kann die Visualisierung primär durch Browser‑Rendering limitiert sein. Dies stellt **kein** Memory‑Problem der Python‑Applikation dar und wird explizit dokumentiert.

### NF06 – Plattformunabhängigkeit

Das System muss lokal auf Standard‑Entwicklungsrechnern lauffähig sein.

---

## 6. Wissenschaftlicher Schwerpunkt: Memory Management

### 6.1 Theoretischer Hintergrund

* Reference Counting in Python
* Zyklische Garbage Collection
* Problem zirkulärer Objektgraphen

**Begriffliche Abgrenzung:**
Es werden keine klassischen Memory Leaks untersucht, sondern leak‑ähnliches Verhalten durch nicht freigegebene Referenzzyklen.

### 6.2 Hypothesen

* H1: Ohne zyklische GC steigt die Anzahl nicht freigegebener Objekte mit der Größe des Objektgraphen.
* H2: Mit aktivierter GC werden zyklische Referenzen nach Entfernen externer Referenzen aufgelöst.

### 6.3 Messgrößen

* Speicherverbrauch (RAM)
* Anzahl existierender Objekte
* Anzahl und Dauer von GC‑Zyklen

### 6.4 Versuchsaufbau

1. Aufbau großer zyklischer Objektgraphen
2. Entfernen externer Referenzen
3. Vergleich:

   * GC deaktiviert
   * GC aktiviert
4. Grafische Auswertung

---

## 7. Visualisierung & UI

### Technologie

* **Streamlit** als Web‑UI

### Zweck der Visualisierung

* Verständnis komplexer Verwandtschaftsgraphen
* Unterstützung der GC‑Analyse

### Abgrenzung

Bei sehr großen Stammbäumen kann die Performance primär durch das Browser‑Rendering limitiert sein. Diese Grenze wird dokumentiert und nicht als Speicherproblem interpretiert.

---

## 8. Technologien & Bibliotheken

### Python Standardbibliothek

* gc
* sys
* tracemalloc
* weakref
* datetime

### Externe Bibliotheken

* streamlit (UI)
* networkx (Graphmodellierung)
* matplotlib (Diagramme)
* graphviz (Graphdarstellung, optional)
* objgraph (Objektanalyse, optional)

Alle verwendeten Bibliotheken werden im Projekt explizit dokumentiert und begründet.

---

## 9. Projektstruktur (geplant)

```
data/
docs/
memory/
models/
search/
static/
templates/
tests/
app.py
README.md
```

---

## 10. Arbeitsteilung

* **Teilbereich A:** Datenmodell, Zyklen, GC‑Experimente
* **Teilbereich B:** Logik, Suche, Bot
* **Teilbereich C:** Visualisierung, Streamlit‑UI, Diagramme

---

## 11. Verlinkung externer Dokumente

* UML‑Diagramme: `docs/uml/`
* GC‑Messprotokolle: `docs/experiments/`
* Feature‑Planung: `docs/features.md`
* Epics & User Stories: `docs/epics_stories.md`
* Wissenschaftliche Quellen: `docs/references.md`

---


Eine vollständige Literaturliste wird separat gepflegt.

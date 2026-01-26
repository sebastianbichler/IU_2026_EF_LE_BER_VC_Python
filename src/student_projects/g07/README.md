# 1 Elephant Memory Cloud

Dieses Projekt ist ein Python-basierter Prototyp zur Untersuchung von **Reference Counting und zyklischer Garbage Collection** in komplexen Objektgraphen.

Anhand eines thematisch eingebetteten Szenarios (Elefanten, Stammbäume, Ereignisse) werden bewusst zirkuläre Referenzen erzeugt, analysiert und hinsichtlich ihres Speicherverhaltens untersucht. Ziel ist ein reproduzierbarer experimenteller Nachweis der Wirksamkeit des Garbage Collectors in Python.

## 1.1 Installation

Die allgemeinen Voraussetzungen hinsichtlich Python, virtuellen Umgebungen und der Installation von Abhängigkeiten (pip) ist dem übergeordneten Projekt zu entnehmen.

## 1.2 Bibliotheken (Kurzüberblick)

### 1.2.1 Standardbibliothek
- gc
- sys
- tracemalloc
- weakref
- datetime

### 1.2.2 Externe Bibliotheken
- streamlit – Webbasierte Visualisierung
- networkx – Modellierung von Graphen und Stammbäumen
- matplotlib – Diagramme und Auswertungen

Optionale Analyse- und Visualisierungstools sind/ werden in der weiteren Dokumentation aufgeführt.

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

* docs/phase_1/`Konzept.md` – Gesamtkonzept & Anforderungen

### 2.2.2 t.b.d
### 2.2.3 t.b.d.

---

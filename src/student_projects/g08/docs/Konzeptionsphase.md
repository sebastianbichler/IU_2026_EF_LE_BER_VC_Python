# Konzeptionsphase

## Ziel

Ziel der Konzeptionsphase war die strukturierte Planung des Projekts Bear Honeyworks.

Dabei wurden:
- Anforderungen definiert und priorisiert
- Systemarchitektur entworfen
- Diagramme erstellt
- Technologien ausgewählt

---

## Anforderungen

Die Anforderungen wurden nach dem MoSCoW-Prinzip priorisiert:

- Must: Typprüfung, Domänenmodell, Produktionslogik
- Should: Lagerverwaltung, Bestellverarbeitung
- Could: Demonstration von Typfehlern, Erweiterbarkeit

→ siehe: Anforderungen.md

---

## Systemdesign

Folgende Diagramme wurden erstellt:

- Kontextdiagramm
- Use-Case-Diagramm

Diese beschreiben:
- die Systemgrenzen
- die Interaktion mit Nutzern und Tools
- die wichtigsten Anwendungsfälle

---

## Architektur

Das System wurde modular aufgebaut:

- Domain -> Fachlogik
- Services -> Geschäftsprozesse
- Repositories -> Datenzugriff
- UI -> Demo (Streamlit)

Ziel:
- klare Trennung der Verantwortlichkeiten
- saubere Typverträge zwischen Modulen

---

## Technologien

Auswahl basierend auf Projektziel:

- Python -> dynamische Sprache als Basis
- mypy -> statische Typprüfung
- typing -> Typdefinitionen
- Streamlit -> einfache Demo-Oberfläche

---

## Wissenschaftlicher Hintergrund

- Gradual Typing (Siek & Taha)
- PEP 484 (Type Hints)

Ziel:
- Verbindung zwischen Theorie und Praxis herstellen

---

## Ergebnis

Am Ende der Konzeptionsphase liegt vor:

- vollständiges Konzept
- definierte Anforderungen
- Architekturentwurf
- technische Grundlage für die Umsetzung

Diese Phase bildet die Basis für die weitere Implementierung und Analyse.
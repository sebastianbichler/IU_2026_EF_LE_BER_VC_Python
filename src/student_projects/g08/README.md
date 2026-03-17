# Bear Honeyworks

Bear Honeyworks ist eine fiktive Honigfabrik-Anwendung zur Demonstration von **statischer Typprüfung mit mypy** in Python.

Die Anwendung kombiniert:
- saubere Softwarearchitektur (Domain / Services / Repository)
- statische Typprüfung (mypy)
- automatisierte Tests (pytest)
- einfache UI mit Streamlit
- CLI-Ausführung

---

## Features

- Honigproduktion durch Bären
- Lagerverwaltung von Honiggläsern
- Bestellverarbeitung
- Auswertungen (nach Sorte & Bär)
- Demonstration von Typfehlern mit mypy
- Unit- und Integrationstests

---

## Installation

```bash
python -m venv .venv
source .venv/bin/activate   # Mac/Linux
.venv\Scripts\activate      # Windows

pip install -r requirements.txt
```

---

## Anwendung starten

CLI Starten

```bash
honeyworks
```

--- 

## Tests ausführen

```bash
PYTHONPATH=src pytest
```
--- 

## mypy Typprüfung

```bash
mypy
```
--- 

## Typfehler demonstrieren

```bash
mypy tests/test_mypy_demo_fail.py
```

Erwartung: mypy meldet einen Fehler

--- 

## Korrigierte Variante prüfen

```bash
mypy tests/test_mypy_demo_ok.py
```

Erwartung: Keine fehler

--- 

## CI/CD
Das Projekt enthält eine CI-Pipeline (z. B. GitHub Actions), die automatisch:
	- Abhängigkeiten installiert
	- Tests ausführt (pytest)
	- statische Typprüfung durchführt (mypy)

--- 

## Projektstruktur
```bash 
.
├── data/           # JSON-Daten (Persistenz)
├── docs/           # Dokumentation (Phasen, Konzept, Anforderungen)
├── src/            # Hauptanwendung
│   └── bear_honeyworks/
│       ├── domain/
│       ├── services/
│       ├── repositories/
│       ├── ui/
│       └── cli/
├── tests/          # Unit- & Integrationstests
├── requirements.txt
└── pyproject.toml
```
---

## Ziel des Projekts

Ziel ist es, die Vorteile statischer Typprüfung in Python zu demonstrieren:
	- frühe Fehlererkennung
	- bessere Codequalität
	- klare Schnittstellen durch Typannotationen
	- Unterstützung durch IDEs
	- wartbare Softwarearchitektur

--- 

## Dokumentation

Weitere Details befinden sich im Ordner docs/:
	- Anforderungen
	- Konzept
	- Projektphasen
	- Quellenverzeichnis

## Hinweis

Dieses Projekt wurde im Rahmen des IU-Moduls
„Einführung in die Programmierung mit Python“ erstellt.

## Mitglieder

Donalies Philipp
Gärtner Cedric
Mannstein Max


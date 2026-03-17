# Bear Honeyworks

## Projektübersicht

Bear Honeyworks ist eine vereinfachte Produktions- und Verwaltungssoftware für eine fiktive Honigfabrik, die von einem Bären betrieben wird.
Der Bär übernimmt dabei sowohl die Honigproduktion als auch die Verwaltung von Lagerbestand und Bestellungen.

Die Prozesse der Honigfabrik werden softwareseitig modelliert und umfassen unter anderem:
	•	die Erzeugung von Honiggläsern
	•	die Verwaltung des Lagerbestands
	•	die Verarbeitung von Bestellungen

Die narrative Einbettung dient der anschaulichen Domänenmodellierung, während der fachliche Schwerpunkt des Projekts auf der statischen Typprüfung mit mypy liegt.

Ziel ist es zu untersuchen, wie durch konsequente Typannotationen in Python:
	•	Typfehler frühzeitig erkannt
	•	Laufzeitfehler vermieden
	•	Codequalität und Wartbarkeit verbessert

werden können.


## Installation & Start

### Voraussetzungen

- Python 3.10 oder höher
- pip

---

### 1. Repository klonen

```bash
git clone <REPO-URL>
cd g08
```
### 2. Virtuelle Umgebung erstellen (empfohlen)

```bash
python -m venv .venv
source .venv/bin/activate  
```
### 3. Abhängigkeiten installieren

```bash
pip install -e .
pip install streamlit pandas
```

### 4. Anwendung starten

```bash
honeyworks
```

--- 

## Alternative (ohne Installation)

Falls das Projekt nicht installiert wurde:

```bash
PYTHONPATH=src streamlit run src/bear_honeyworks/ui/app.py
```

## Typprüfung

Die Statische Typprüfung kann mit folgendem Befehl ausgeführt werden:

```bash
mypy
```
--- 

## CI / Qualitätssicherung

Das Projekt verwendet automatisierte Qualitätssicherung über:

- **mypy** zur statischen Typprüfung
- **pytest** für Unit- und Integrationstests
- **GitHub Actions** zur automatischen Ausführung der Checks bei Push und Pull Request

### Lokale Ausführung

```bash
mypy
PYTHONPATH=src pytest
```
--- 
## Gruppenmitglieder

Max Mannstein
Philipp Donalies
Cedric Gärtner
--- 


# Links zu den Dateien

## Konzept

[Konzept](Konzept.md)

## Anforderungen

[Anforderungen](Anforderungen.md)


## Einarbeitungsphase

[Einarbeitungsphase](Einarbeitungsphase.md)


## Konzeptionsphase

[Konzeptionsphase](Konzeptionsphase.md)


## Finalisierungsphase

[Finalisierungsphase](Finalisierungsphase.md)

## Testbeschreibung

[Testbeschreibung](../tests/Testbeschreibung.md)

## Requirements
[Requiremnets](../requirements.txt)
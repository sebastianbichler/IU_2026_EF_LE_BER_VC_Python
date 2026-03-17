# Tests – Bear Honeyworks

Dieser Ordner enthält automatisierte Tests und Demo-Dateien zur statischen Typprüfung mit **mypy**.

## Inhalt

### Funktionale Tests mit pytest

Diese Tests prüfen das Laufzeitverhalten der Anwendung:

- `test_production_service.py`  
  Prüft, ob die Produktionslogik ein korrektes `HoneyJar` erzeugt.

- `test_inventory_service.py`  
  Prüft, ob Honiggläser korrekt im Lager gespeichert werden.

- `test_order_service.py`  
  Prüft, ob Bestellungen korrekt verarbeitet werden und ob die Qualitätslogik greift.

### mypy-Demo-Dateien

Diese Dateien dienen zur Demonstration statischer Typprüfung:

- `test_mypy_demo_fail.py`  
  Enthält absichtlich einen Typfehler, damit mypy eine Fehlermeldung ausgibt.

- `test_mypy_demo_ok.py`  
  Enthält die korrigierte Variante ohne Typfehler.

---

## Tests ausführen

### Alle pytest-Tests starten

```bash
PYTHONPATH=src pytest
```

---

## Mypy Demo Ausführen

### Typfehler demonstrieren

```bash
mypy tests/test_mypy_demo_fail.py
```
Erwartetes Ergebnis:
mypy meldet einen Fehler, weil ein falscher Rückgabetyp verwendet wird

### Korrigierte Variante prüfen

```bash
mypy tests/test_mypy_demo_ok.py
```

Erwartetes Ergebnis:
mypy meldet keine Fehler

---

## Zweck der Tests

Die Tests verfolgen zwei Ziele:
1. Funktionale Korrektheit
    mit pytest wird geprüft ob die Geschäftslogik korrekt funktioniert

2. Statische Typprüfung
    mit mypy wird geprüft, ob die Typannotationen korrekt eingehalten werden.

Dadurch wird sowohl das Verhalten als auch die Typkonsistenz der Anwendung abgesichert.

--- 

## Hinweis
Für die Ausführung der Tests wird vorausgesetzt, dass:
	- das Projekt korrekt installiert wurde
	- die virtuelle Umgebung aktiv ist
	- alle benötigten Pakete installiert sind